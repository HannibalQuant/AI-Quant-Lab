"""Fail-closed normalization of bounded TradingView bar exports into canonical AIQL CSV."""

from __future__ import annotations

import csv
import hashlib
import io
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ai_quant_lab.core.csv_import import (
    MAX_CONTROLLED_HISTORICAL_FILE_BYTES,
    MAX_CONTROLLED_HISTORICAL_ROWS,
)
from ai_quant_lab.core.market_data import TimeframeIdentity
from ai_quant_lab.core.model import require_utc

MAX_TRADINGVIEW_COLUMNS = 64
MAX_TRADINGVIEW_LINE_BYTES = 16_384
_CANONICAL_HEADER = (
    "bar_open_time,bar_close_time,open,high,low,close,volume,finality,availability_time\n"
)


class TradingViewCsvAdapterError(ValueError):
    """TradingView source cannot be normalized without inventing source semantics."""


@dataclass(frozen=True, slots=True)
class TradingViewCsvAdapterPolicy:
    """Explicit operator policy for deterministic derivation from a bar-open export."""

    time_column: str
    open_column: str = "open"
    high_column: str = "high"
    low_column: str = "low"
    close_column: str = "close"
    volume_column: str = ""
    timestamp_unit: str = "unix_seconds"
    source_timezone: str = "UTC"
    derive_bar_close_from_timeframe: bool = True
    derive_finality_from_historical_export: bool = False
    availability_at_bar_close: bool = False

    def __post_init__(self) -> None:
        required = (
            self.time_column,
            self.open_column,
            self.high_column,
            self.low_column,
            self.close_column,
            self.volume_column,
        )
        if any(not isinstance(item, str) or not item.strip() for item in required):
            raise TradingViewCsvAdapterError("source column names must be explicit non-empty text")
        if self.timestamp_unit not in {"unix_seconds", "unix_milliseconds"}:
            raise TradingViewCsvAdapterError(
                "TradingView timestamp unit must be explicitly declared"
            )
        if self.source_timezone != "UTC":
            raise TradingViewCsvAdapterError(
                "only explicitly declared UTC TradingView exports are supported"
            )
        if not self.derive_bar_close_from_timeframe:
            raise TradingViewCsvAdapterError("bar close derivation must be explicitly authorized")
        if not self.derive_finality_from_historical_export:
            raise TradingViewCsvAdapterError(
                "historical finality derivation must be explicitly authorized"
            )
        if not self.availability_at_bar_close:
            raise TradingViewCsvAdapterError(
                "availability-at-close semantics must be explicitly authorized"
            )


@dataclass(frozen=True, slots=True)
class TradingViewCsvNormalizationResult:
    source_sha256: str
    source_size: int
    source_row_count: int
    canonical_sha256: str
    canonical_row_count: int
    first_bar_open: datetime
    last_bar_close: datetime
    canonical_csv: str
    transformation_notes: tuple[str, ...]
    provenance_note: str


def _stamp(value: datetime) -> str:
    require_utc(value, "TradingView derived timestamp")
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def _timestamp(text: str, unit: str) -> datetime:
    if not text or text.strip() != text:
        raise TradingViewCsvAdapterError("TradingView time value is empty or padded")
    try:
        raw = int(text)
    except ValueError as exc:
        raise TradingViewCsvAdapterError("TradingView time must be an integer epoch value") from exc
    divisor = 1 if unit == "unix_seconds" else 1000
    if unit == "unix_milliseconds" and raw % 1000:
        raise TradingViewCsvAdapterError(
            "sub-second TradingView timestamps are outside the governed bar-open profile"
        )
    try:
        return datetime.fromtimestamp(raw / divisor, tz=UTC)
    except (OverflowError, OSError, ValueError) as exc:
        raise TradingViewCsvAdapterError("TradingView epoch timestamp is out of range") from exc


def normalize_tradingview_csv(
    source_path: Path,
    *,
    allowed_root: Path,
    timeframe: TimeframeIdentity,
    policy: TradingViewCsvAdapterPolicy,
) -> TradingViewCsvNormalizationResult:
    """Normalize one local TradingView export while preserving exact source-byte lineage."""

    if not source_path.is_absolute() or not allowed_root.is_absolute():
        raise TradingViewCsvAdapterError("source and allowed root must be absolute paths")
    if source_path.suffix != ".csv" or ".." in source_path.parts:
        raise TradingViewCsvAdapterError("only bounded local lowercase .csv input is supported")
    if allowed_root.is_symlink() or source_path.is_symlink():
        raise TradingViewCsvAdapterError("symlink input is prohibited")
    try:
        root = allowed_root.resolve(strict=True)
        path = source_path.resolve(strict=True)
        path.relative_to(root)
    except (OSError, ValueError) as exc:
        raise TradingViewCsvAdapterError("source is missing or outside the allowed root") from exc
    if not path.is_file():
        raise TradingViewCsvAdapterError("source must be a regular file")

    data = path.read_bytes()
    if len(data) > MAX_CONTROLLED_HISTORICAL_FILE_BYTES:
        raise TradingViewCsvAdapterError(
            "TradingView export exceeds controlled historical byte bound"
        )
    source_sha256 = hashlib.sha256(data).hexdigest()
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise TradingViewCsvAdapterError("TradingView export must be strict UTF-8") from exc
    if text.startswith("\ufeff") or "\x00" in text:
        raise TradingViewCsvAdapterError("BOM and NUL bytes are prohibited")
    if any(len(line.encode("utf-8")) > MAX_TRADINGVIEW_LINE_BYTES for line in text.splitlines()):
        raise TradingViewCsvAdapterError("TradingView row exceeds bounded line size")

    reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
    headers = reader.fieldnames
    if (
        headers is None
        or len(headers) > MAX_TRADINGVIEW_COLUMNS
        or len(headers) != len(set(headers))
    ):
        raise TradingViewCsvAdapterError("TradingView header is missing, duplicated, or too wide")
    required = {
        policy.time_column,
        policy.open_column,
        policy.high_column,
        policy.low_column,
        policy.close_column,
    }
    required.add(policy.volume_column)
    if not required.issubset(headers):
        raise TradingViewCsvAdapterError("TradingView export is missing explicitly mapped columns")

    output = io.StringIO(newline="")
    output.write(_CANONICAL_HEADER)
    writer = csv.writer(output, lineterminator="\n")
    previous_open: datetime | None = None
    first_open: datetime | None = None
    last_close: datetime | None = None
    count = 0

    try:
        for row in reader:
            count += 1
            if count > MAX_CONTROLLED_HISTORICAL_ROWS:
                raise TradingViewCsvAdapterError(
                    "TradingView export exceeds controlled historical row bound"
                )
            if None in row or any(value is None for value in row.values()):
                raise TradingViewCsvAdapterError("TradingView row width does not match the header")
            opened = _timestamp(row[policy.time_column], policy.timestamp_unit)
            timeframe.require_aligned(opened)
            if previous_open is not None and opened <= previous_open:
                raise TradingViewCsvAdapterError(
                    "TradingView bar opens must be unique and strictly ascending"
                )
            closed = opened + timeframe.duration
            volume = row[policy.volume_column]
            writer.writerow(
                (
                    _stamp(opened),
                    _stamp(closed),
                    row[policy.open_column],
                    row[policy.high_column],
                    row[policy.low_column],
                    row[policy.close_column],
                    volume,
                    "final",
                    _stamp(closed),
                )
            )
            first_open = opened if first_open is None else first_open
            last_close = closed
            previous_open = opened
    except csv.Error as exc:
        raise TradingViewCsvAdapterError("TradingView CSV syntax is invalid") from exc

    if count == 0 or first_open is None or last_close is None:
        raise TradingViewCsvAdapterError("TradingView export contains no data rows")
    canonical_csv = output.getvalue()
    canonical_bytes = canonical_csv.encode("utf-8")
    if len(canonical_bytes) > MAX_CONTROLLED_HISTORICAL_FILE_BYTES:
        raise TradingViewCsvAdapterError(
            "canonical TradingView output exceeds controlled historical byte bound"
        )
    canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
    provenance_note = (
        f"tv_adapter_v1;source_sha256={source_sha256};"
        f"canonical_sha256={canonical_sha256}"
    )
    return TradingViewCsvNormalizationResult(
        source_sha256,
        len(data),
        count,
        canonical_sha256,
        count,
        first_open,
        last_close,
        canonical_csv,
        (
            "source bytes preserved by SHA-256; source file is not rewritten",
            "bar_close_time derived as bar_open_time + exact governed timeframe duration",
            "finality=final derived only under explicit historical-export operator declaration",
            (
                "availability_time=bar_close_time derived only under explicit "
                "confirmed-bar research policy"
            ),
            (
                "extra TradingView indicator columns are ignored and never treated as "
                "governed OHLCV source fields"
            ),
        ),
        provenance_note,
    )


def write_canonical_csv(
    result: TradingViewCsvNormalizationResult,
    destination: Path,
    *,
    allowed_root: Path,
) -> str:
    """Write canonical bytes inside an explicit local boundary and return their SHA-256."""

    if (
        not destination.is_absolute()
        or not allowed_root.is_absolute()
        or destination.suffix != ".csv"
    ):
        raise TradingViewCsvAdapterError("canonical destination must be an absolute .csv path")
    if destination.exists():
        raise TradingViewCsvAdapterError(
            "canonical destination must not overwrite an existing file"
        )
    try:
        root = allowed_root.resolve(strict=True)
        parent = destination.parent.resolve(strict=True)
        parent.relative_to(root)
    except (OSError, ValueError) as exc:
        raise TradingViewCsvAdapterError(
            "canonical destination is outside the allowed root"
        ) from exc
    destination.write_text(result.canonical_csv, encoding="utf-8", newline="")
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    if digest != result.canonical_sha256:
        destination.unlink(missing_ok=True)
        raise TradingViewCsvAdapterError("canonical write failed exact byte verification")
    return digest
