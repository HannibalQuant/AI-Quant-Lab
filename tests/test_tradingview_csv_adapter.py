"""Phase 3 Sprint 27 governed TradingView CSV adapter tests."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_quant_lab.core.market_data import (
    AlignmentKind,
    TimeframeId,
    TimeframeIdentity,
    TimeframeUnit,
)
from ai_quant_lab.core.model import ObjectVersion
from ai_quant_lab.core.tradingview_csv_adapter import (
    TradingViewCsvAdapterError,
    TradingViewCsvAdapterPolicy,
    normalize_tradingview_csv,
    write_canonical_csv,
)

V1 = ObjectVersion(1)


def timeframe_4h() -> TimeframeIdentity:
    return TimeframeIdentity(
        TimeframeId("4h"),
        V1,
        TimeframeUnit.HOUR,
        4,
        AlignmentKind.UTC_EPOCH_FIXED,
        V1,
    )


def policy() -> TradingViewCsvAdapterPolicy:
    return TradingViewCsvAdapterPolicy(
        time_column="time",
        volume_column="Volume",
        timestamp_unit="unix_seconds",
        source_timezone="UTC",
        derive_bar_close_from_timeframe=True,
        derive_finality_from_historical_export=True,
        availability_at_bar_close=True,
    )


def source_csv() -> str:
    return (
        "time,open,high,low,close,Volume,EMA,RSI\n"
        "1641168000,170,172,168,171,1000,169,55\n"
        "1641182400,171,174,170,173,1100,170,58\n"
    )


def test_tradingview_export_normalizes_deterministically_and_preserves_source_hash(
    tmp_path: Path,
) -> None:
    source = tmp_path / "solusdt_4h_tv.csv"
    source.write_text(source_csv(), encoding="utf-8")
    first = normalize_tradingview_csv(
        source,
        allowed_root=tmp_path,
        timeframe=timeframe_4h(),
        policy=policy(),
    )
    second = normalize_tradingview_csv(
        source,
        allowed_root=tmp_path,
        timeframe=timeframe_4h(),
        policy=policy(),
    )

    assert first == second
    assert first.source_sha256 == hashlib.sha256(source.read_bytes()).hexdigest()
    assert first.source_row_count == first.canonical_row_count == 2
    assert first.first_bar_open == datetime(2022, 1, 3, tzinfo=UTC)
    assert first.last_bar_close == datetime(2022, 1, 3, 8, tzinfo=UTC)
    assert first.canonical_csv.startswith(
        "bar_open_time,bar_close_time,open,high,low,close,volume,finality,availability_time\n"
    )
    assert (
        "2022-01-03T00:00:00.000000Z,2022-01-03T04:00:00.000000Z,"
        "170,172,168,171,1000,final,2022-01-03T04:00:00.000000Z\n"
    ) in first.canonical_csv
    assert "EMA" not in first.canonical_csv
    assert "RSI" not in first.canonical_csv


def test_canonical_output_is_written_without_mutating_source(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    source.write_text(source_csv(), encoding="utf-8")
    before = source.read_bytes()
    result = normalize_tradingview_csv(
        source,
        allowed_root=tmp_path,
        timeframe=timeframe_4h(),
        policy=policy(),
    )
    destination = tmp_path / "canonical.csv"
    digest = write_canonical_csv(result, destination, allowed_root=tmp_path)

    assert source.read_bytes() == before
    assert digest == result.canonical_sha256
    assert hashlib.sha256(destination.read_bytes()).hexdigest() == result.canonical_sha256


@pytest.mark.parametrize(
    "policy_overrides",
    [
        {
            "derive_finality_from_historical_export": False,
            "availability_at_bar_close": True,
        },
        {
            "derive_finality_from_historical_export": True,
            "availability_at_bar_close": False,
        },
    ],
)
def test_missing_semantic_authority_fails_closed(
    policy_overrides: dict[str, bool],
) -> None:
    with pytest.raises(TradingViewCsvAdapterError):
        TradingViewCsvAdapterPolicy(
            time_column="time",
            volume_column="Volume",
            **policy_overrides,
        )


def test_missing_mapping_and_misaligned_or_duplicate_time_fail_closed(tmp_path: Path) -> None:
    missing = tmp_path / "missing.csv"
    missing.write_text("time,open,high,low,close\n1641168000,1,2,0.5,1.5\n", encoding="utf-8")
    with pytest.raises(TradingViewCsvAdapterError, match="mapped columns"):
        normalize_tradingview_csv(
            missing,
            allowed_root=tmp_path,
            timeframe=timeframe_4h(),
            policy=policy(),
        )

    misaligned = tmp_path / "misaligned.csv"
    misaligned.write_text(
        "time,open,high,low,close,Volume\n1641171600,1,2,0.5,1.5,10\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="misaligned"):
        normalize_tradingview_csv(
            misaligned,
            allowed_root=tmp_path,
            timeframe=timeframe_4h(),
            policy=policy(),
        )

    duplicate = tmp_path / "duplicate.csv"
    duplicate.write_text(
        "time,open,high,low,close,Volume\n1641168000,1,2,0.5,1.5,10\n1641168000,1.5,2,1,1.8,11\n",
        encoding="utf-8",
    )
    with pytest.raises(TradingViewCsvAdapterError, match="strictly ascending"):
        normalize_tradingview_csv(
            duplicate,
            allowed_root=tmp_path,
            timeframe=timeframe_4h(),
            policy=policy(),
        )


def test_source_boundary_and_overwrite_are_fail_closed(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    source = root / "source.csv"
    source.write_text(source_csv(), encoding="utf-8")
    result = normalize_tradingview_csv(
        source,
        allowed_root=root,
        timeframe=timeframe_4h(),
        policy=policy(),
    )

    existing = root / "existing.csv"
    existing.write_text("do-not-overwrite", encoding="utf-8")
    with pytest.raises(TradingViewCsvAdapterError, match="must not overwrite"):
        write_canonical_csv(result, existing, allowed_root=root)

    outside = tmp_path / "outside.csv"
    outside.write_text(source_csv(), encoding="utf-8")
    with pytest.raises(TradingViewCsvAdapterError, match="outside"):
        normalize_tradingview_csv(
            outside,
            allowed_root=root,
            timeframe=timeframe_4h(),
            policy=policy(),
        )
