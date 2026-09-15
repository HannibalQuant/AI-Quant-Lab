"""Governed, synthetic-only fixed-duration OHLCV normalization contracts."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from itertools import pairwise
from typing import cast

from ai_quant_lab.core.data import (
    DataQualityState,
    DatasetLock,
    DatasetLockId,
    DecimalValue,
    InstrumentId,
    InvalidDataContract,
    ObservationId,
    RawObservation,
    SourceId,
)
from ai_quant_lab.core.model import (
    DatasetId,
    GovernedId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    require_utc,
)


class MarketDataError(InvalidDataContract):
    """Invalid market-data contract or unadmitted transformation."""


class InvalidTimeframe(MarketDataError):
    pass


class InvalidOHLCGeometry(MarketDataError):
    pass


class SchemaMappingError(MarketDataError):
    pass


class BarConflict(MarketDataError):
    pass


class NormalizedDatasetAssemblyError(MarketDataError):
    pass


def _fingerprint(
    record: TimeframeIdentity
    | MarketDataSchema
    | MarketBar
    | NormalizedBarManifest
    | RawObservation,
) -> str:
    # Late import avoids a codec/integrity/domain import cycle during type registration.
    from ai_quant_lab.core.integrity import fingerprint_record

    return fingerprint_record(record)


class TimeframeId(GovernedId):
    namespace = "timeframe"


class MarketDataSchemaId(GovernedId):
    namespace = "market-data-schema"


class MarketBarId(GovernedId):
    namespace = "market-bar"


class TimeframeUnit(StrEnum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"


class AlignmentKind(StrEnum):
    UTC_EPOCH_FIXED = "utc_epoch_fixed"
    CALENDAR_UNRESOLVED = "calendar_unresolved"


class BarFinality(StrEnum):
    INCOMPLETE = "incomplete"
    FINAL = "final"
    CORRECTED_FINAL = "corrected_final"


class VolumeSemantic(StrEnum):
    BASE = "base"
    QUOTE = "quote"
    CONTRACTS = "contracts"
    SHARES = "shares"
    TICKS = "ticks"
    PROVIDER_DEFINED = "provider_defined"
    ABSENT = "absent"


class BarTimestampMeaning(StrEnum):
    OPEN = "open"
    CLOSE = "close"


class NormalizationDisposition(StrEnum):
    NORMALIZED = "normalized"


class BarPairDisposition(StrEnum):
    UNIQUE = "unique"
    DUPLICATE = "duplicate"
    CONFLICT = "conflict"
    CORRECTION = "correction"


class GapDisposition(StrEnum):
    CONTIGUOUS = "contiguous"
    MECHANICAL_GAP = "mechanical_gap"
    OVERLAP = "overlap"


def _exact_ref(reference: TraceabilityRef, identifier: type[GovernedId], field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise MarketDataError(
            f"{field} requires exact {identifier.namespace} fingerprint reference"
        )


def _timestamp(value: str, field: str) -> datetime:
    if not isinstance(value, str):
        raise SchemaMappingError(f"{field} must be timestamp text")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
    except ValueError as exc:
        raise SchemaMappingError(f"{field} must be canonical UTC microsecond Z") from exc
    return parsed


@dataclass(frozen=True, slots=True)
class TimeframeIdentity:
    timeframe_id: TimeframeId
    version: ObjectVersion
    unit: TimeframeUnit
    count: int
    alignment: AlignmentKind
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if not isinstance(self.count, int) or isinstance(self.count, bool) or self.count < 1:
            raise InvalidTimeframe("timeframe count must be positive")
        if not isinstance(self.unit, TimeframeUnit) or not isinstance(
            self.alignment, AlignmentKind
        ):
            raise InvalidTimeframe("timeframe unit and alignment must be explicit")
        token = {TimeframeUnit.MINUTE: "m", TimeframeUnit.HOUR: "h", TimeframeUnit.DAY: "d"}[
            self.unit
        ]
        if self.timeframe_id.value != f"{self.count}{token}":
            raise InvalidTimeframe("timeframe ID must use exact non-alias unit/count")
        if self.alignment is AlignmentKind.CALENDAR_UNRESOLVED:
            raise InvalidTimeframe("calendar/session alignment requires governed calendar")
        # A fixed 1d is 24h from UTC epoch, never an implicit venue/session daily bar.

    @property
    def duration(self) -> timedelta:
        return {
            TimeframeUnit.MINUTE: timedelta(minutes=self.count),
            TimeframeUnit.HOUR: timedelta(hours=self.count),
            TimeframeUnit.DAY: timedelta(days=self.count),
        }[self.unit]

    def require_aligned(self, bar_open: datetime) -> None:
        require_utc(bar_open, "bar_open")
        elapsed = bar_open - datetime(1970, 1, 1, tzinfo=UTC)
        if elapsed % self.duration != timedelta():
            raise InvalidTimeframe("bar open is misaligned with UTC epoch fixed duration")


@dataclass(frozen=True, slots=True)
class MarketDataSchema:
    schema_id: MarketDataSchemaId
    version: ObjectVersion
    timeframe_ref: TraceabilityRef
    timestamp_meaning: BarTimestampMeaning
    open_time_field: str
    close_time_field: str
    open_field: str
    high_field: str
    low_field: str
    close_field: str
    volume_field: str | None
    finality_field: str
    volume_semantic: VolumeSemantic
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        _exact_ref(self.timeframe_ref, TimeframeId, "timeframe_ref")
        fields = (
            self.open_time_field,
            self.close_time_field,
            self.open_field,
            self.high_field,
            self.low_field,
            self.close_field,
            self.finality_field,
        ) + (() if self.volume_field is None else (self.volume_field,))
        if any(not isinstance(field, str) or not field for field in fields) or len(fields) != len(
            set(fields)
        ):
            raise SchemaMappingError("schema field mapping requires unique nonempty names")
        if (self.volume_field is None) != (self.volume_semantic is VolumeSemantic.ABSENT):
            raise SchemaMappingError("absent volume and semantic must agree")
        if not isinstance(self.timestamp_meaning, BarTimestampMeaning):
            raise SchemaMappingError("event-time meaning must be explicit")


@dataclass(frozen=True, slots=True)
class MarketBar:
    bar_id: MarketBarId
    version: ObjectVersion
    source_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    timeframe_ref: TraceabilityRef
    schema_ref: TraceabilityRef
    normalization_version: ObjectVersion
    bar_open: datetime
    bar_close: datetime
    availability_time: datetime
    ingestion_time: datetime
    open: DecimalValue
    high: DecimalValue
    low: DecimalValue
    close: DecimalValue
    volume: DecimalValue | None
    volume_semantic: VolumeSemantic
    finality: BarFinality
    source_observation_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    supersedes: TraceabilityRef | None = None
    contract_version: ObjectVersion = dataclass_field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        for value, identifier, field in (
            (self.source_ref, SourceId, "source_ref"),
            (self.instrument_ref, InstrumentId, "instrument_ref"),
            (self.timeframe_ref, TimeframeId, "timeframe_ref"),
            (self.schema_ref, MarketDataSchemaId, "schema_ref"),
            (self.source_observation_ref, ObservationId, "source_observation_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact_ref(value, identifier, field)
        for field in ("bar_open", "bar_close", "availability_time", "ingestion_time"):
            require_utc(getattr(self, field), field)
        if not self.bar_open < self.bar_close:
            raise MarketDataError("bar interval requires [open, close) and open < close")
        if not self.bar_open <= self.availability_time <= self.ingestion_time:
            raise MarketDataError("bar availability/ingestion cannot precede its open")
        if self.finality is not BarFinality.INCOMPLETE and self.availability_time < self.bar_close:
            raise MarketDataError("final bar cannot be known before its close")
        if not all(
            isinstance(value, DecimalValue)
            for value in (self.open, self.high, self.low, self.close)
        ):
            raise MarketDataError("OHLC values require exact finite DecimalValue")
        values = tuple(
            Decimal(value.text) for value in (self.open, self.high, self.low, self.close)
        )
        opening, high, low, closing = values
        if high < low or high < opening or high < closing or low > opening or low > closing:
            raise InvalidOHLCGeometry("OHLC geometry is structurally inconsistent")
        if (self.volume is None) != (self.volume_semantic is VolumeSemantic.ABSENT):
            raise MarketDataError("missing volume is distinct from zero volume")
        if self.volume is not None and (
            not isinstance(self.volume, DecimalValue) or Decimal(self.volume.text) < 0
        ):
            raise MarketDataError("volume requires nonnegative exact DecimalValue")
        if self.supersedes is not None:
            _exact_ref(self.supersedes, MarketBarId, "supersedes")
            if self.supersedes.object_id == self.bar_id and self.supersedes.version == self.version:
                raise MarketDataError("bar cannot supersede its own version")
            if self.finality is not BarFinality.CORRECTED_FINAL:
                raise MarketDataError("supersession requires corrected finality")
        elif self.finality is BarFinality.CORRECTED_FINAL:
            raise MarketDataError("corrected finality requires prior exact bar")
        if not isinstance(self.finality, BarFinality):
            raise MarketDataError("bar finality must be explicit")

    @property
    def legitimate_knowledge_time(self) -> datetime:
        return self.availability_time

    @property
    def business_key(self) -> tuple[str, str, str, datetime]:
        return (
            str(self.source_ref.object_id),
            str(self.instrument_ref.object_id),
            str(self.timeframe_ref.object_id),
            self.bar_open,
        )


@dataclass(frozen=True, slots=True)
class NormalizationResult:
    source_observation_ref: TraceabilityRef
    schema_ref: TraceabilityRef
    timeframe_ref: TraceabilityRef
    normalization_version: ObjectVersion
    bar: MarketBar
    disposition: NormalizationDisposition = NormalizationDisposition.NORMALIZED


@dataclass(frozen=True, slots=True)
class BarPairFinding:
    business_key: tuple[str, str, str, datetime]
    disposition: BarPairDisposition
    references: tuple[TraceabilityRef, ...]


@dataclass(frozen=True, slots=True)
class GapFinding:
    previous_ref: TraceabilityRef
    next_ref: TraceabilityRef
    disposition: GapDisposition
    missing_intervals: int


@dataclass(frozen=True, slots=True)
class NormalizedBarManifest:
    dataset_id: DatasetId
    version: ObjectVersion
    created_at: datetime
    bar_refs: tuple[TraceabilityRef, ...]
    source_refs: tuple[TraceabilityRef, ...]
    instrument_refs: tuple[TraceabilityRef, ...]
    timeframe_refs: tuple[TraceabilityRef, ...]
    schema_ref: TraceabilityRef
    normalization_version: ObjectVersion
    raw_dataset_lock_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = dataclass_field(default_factory=lambda: ObjectVersion(1))
    membership_policy: str = "finalized_only"

    def __post_init__(self) -> None:
        require_utc(self.created_at, "created_at")
        for refs, identifier, field in (
            (self.bar_refs, MarketBarId, "bar_refs"),
            (self.source_refs, SourceId, "source_refs"),
            (self.instrument_refs, InstrumentId, "instrument_refs"),
            (self.timeframe_refs, TimeframeId, "timeframe_refs"),
        ):
            if not refs:
                raise NormalizedDatasetAssemblyError(f"{field} cannot be empty")
            for reference in refs:
                _exact_ref(reference, identifier, field)
            keys = [
                (str(ref.object_id), ref.version.number, ref.expected_fingerprint) for ref in refs
            ]
            if keys != sorted(keys) or len(keys) != len(set(keys)):
                raise NormalizedDatasetAssemblyError(f"{field} must be exact, sorted and unique")
        _exact_ref(self.schema_ref, MarketDataSchemaId, "schema_ref")
        _exact_ref(self.raw_dataset_lock_ref, DatasetLockId, "raw_dataset_lock_ref")
        _exact_ref(self.provenance_ref, ProvenanceId, "provenance_ref")
        if self.membership_policy != "finalized_only":
            raise NormalizedDatasetAssemblyError("only finalized_only bars are supported")


def normalize_bar(
    raw: RawObservation,
    schema: MarketDataSchema,
    timeframe: TimeframeIdentity,
    bar_id: MarketBarId,
    bar_version: ObjectVersion,
    normalization_version: ObjectVersion,
    provenance_ref: TraceabilityRef,
    *,
    supersedes: TraceabilityRef | None = None,
) -> NormalizationResult:
    if raw.quality is not DataQualityState.ACCEPTED:
        raise SchemaMappingError("only accepted raw observations may be normalized")
    if schema.contract_version != ObjectVersion(1) or timeframe.contract_version != ObjectVersion(
        1
    ):
        raise SchemaMappingError("unsupported timeframe/schema contract version")
    if schema.timeframe_ref != TraceabilityRef(
        timeframe.timeframe_id, timeframe.version, _fingerprint(timeframe)
    ):
        raise SchemaMappingError("schema binds a different exact timeframe")
    _exact_ref(provenance_ref, ProvenanceId, "normalization provenance")
    fields = {field.name: field.value for field in raw.payload}
    required = (
        schema.open_time_field,
        schema.close_time_field,
        schema.open_field,
        schema.high_field,
        schema.low_field,
        schema.close_field,
        schema.finality_field,
    ) + (() if schema.volume_field is None else (schema.volume_field,))
    if set(fields) != set(required):
        raise SchemaMappingError("source fields must match schema exactly; no silent drop")
    raw_open, raw_close = fields[schema.open_time_field], fields[schema.close_time_field]
    if not isinstance(raw_open, str) or not isinstance(raw_close, str):
        raise SchemaMappingError("source interval boundaries must be timestamp text")
    open_time = _timestamp(raw_open, schema.open_time_field)
    close_time = _timestamp(raw_close, schema.close_time_field)
    timeframe.require_aligned(open_time)
    if close_time - open_time != timeframe.duration:
        raise InvalidTimeframe("bar interval disagrees with exact timeframe duration")
    expected_event = (
        open_time if schema.timestamp_meaning is BarTimestampMeaning.OPEN else close_time
    )
    if raw.temporal.event_time != expected_event:
        raise SchemaMappingError("raw event timestamp differs from explicit schema meaning")
    finality_text = fields[schema.finality_field]
    if not isinstance(finality_text, str):
        raise SchemaMappingError("finality source field must be text")
    try:
        finality = BarFinality(finality_text)
    except ValueError as exc:
        raise SchemaMappingError("unsupported source bar finality") from exc
    if (raw.supersedes is None) != (supersedes is None):
        raise SchemaMappingError("raw correction and normalized correction lineage must agree")
    if supersedes is not None and finality is not BarFinality.CORRECTED_FINAL:
        raise SchemaMappingError("normalized correction requires explicit corrected finality")
    values = tuple(
        fields[name]
        for name in (schema.open_field, schema.high_field, schema.low_field, schema.close_field)
    )
    if not all(isinstance(value, DecimalValue) for value in values):
        raise SchemaMappingError("OHLC source values require exact DecimalValue")
    exact_values = cast(tuple[DecimalValue, DecimalValue, DecimalValue, DecimalValue], values)
    volume = None if schema.volume_field is None else fields[schema.volume_field]
    if volume is not None and not isinstance(volume, DecimalValue):
        raise SchemaMappingError("volume source value requires exact DecimalValue or absent schema")
    if finality is not BarFinality.INCOMPLETE and raw.temporal.availability_time < close_time:
        raise SchemaMappingError("raw source cannot reveal final bar before close")
    bar = MarketBar(
        bar_id,
        bar_version,
        raw.source_ref,
        raw.instrument_ref,
        schema.timeframe_ref,
        TraceabilityRef(schema.schema_id, schema.version, _fingerprint(schema)),
        normalization_version,
        open_time,
        close_time,
        raw.temporal.availability_time,
        raw.temporal.ingestion_time,
        exact_values[0],
        exact_values[1],
        exact_values[2],
        exact_values[3],
        volume,
        schema.volume_semantic,
        finality,
        TraceabilityRef(raw.observation_id, raw.version, _fingerprint(raw)),
        provenance_ref,
        supersedes,
    )
    return NormalizationResult(
        bar.source_observation_ref, bar.schema_ref, bar.timeframe_ref, normalization_version, bar
    )


def bar_ref(bar: MarketBar) -> TraceabilityRef:
    return TraceabilityRef(bar.bar_id, bar.version, _fingerprint(bar))


def classify_bars(bars: tuple[MarketBar, ...]) -> tuple[BarPairFinding, ...]:
    groups: dict[tuple[str, str, str, datetime], list[MarketBar]] = {}
    for bar in bars:
        groups.setdefault(bar.business_key, []).append(bar)
    findings: list[BarPairFinding] = []
    for key, group in sorted(groups.items()):
        content = {
            (
                bar.open,
                bar.high,
                bar.low,
                bar.close,
                bar.volume,
                bar.volume_semantic,
                bar.bar_close,
                bar.availability_time,
                bar.finality,
            )
            for bar in group
        }
        if len(group) == 1:
            status = (
                BarPairDisposition.CORRECTION if group[0].supersedes else BarPairDisposition.UNIQUE
            )
        elif len(content) == 1:
            status = BarPairDisposition.DUPLICATE
        else:
            status = BarPairDisposition.CONFLICT
        findings.append(
            BarPairFinding(
                key,
                status,
                tuple(sorted((bar_ref(item) for item in group), key=lambda x: str(x.object_id))),
            )
        )
    return tuple(findings)


def classify_fixed_gaps(
    bars: tuple[MarketBar, ...], timeframe: TimeframeIdentity
) -> tuple[GapFinding, ...]:
    if any(
        bar.timeframe_ref
        != TraceabilityRef(timeframe.timeframe_id, timeframe.version, _fingerprint(timeframe))
        for bar in bars
    ):
        raise InvalidTimeframe("gaps require same exact timeframe")
    series: dict[tuple[str, str, str], list[MarketBar]] = {}
    for bar in bars:
        series.setdefault(bar.business_key[:3], []).append(bar)
    findings: list[GapFinding] = []
    for group in series.values():
        ordered = sorted(group, key=lambda bar: (bar.bar_open, str(bar.bar_id)))
        for previous, following in pairwise(ordered):
            delta = following.bar_open - previous.bar_open
            duration = timeframe.duration
            if delta == duration:
                status, count = GapDisposition.CONTIGUOUS, 0
            elif delta > duration and delta % duration == timedelta():
                status, count = GapDisposition.MECHANICAL_GAP, int(delta / duration) - 1
            else:
                status, count = GapDisposition.OVERLAP, 0
            findings.append(GapFinding(bar_ref(previous), bar_ref(following), status, count))
    return tuple(findings)


def assemble_normalized_dataset(
    bars: tuple[MarketBar, ...],
    dataset_id: DatasetId,
    version: ObjectVersion,
    created_at: datetime,
    schema_ref: TraceabilityRef,
    normalization_version: ObjectVersion,
    raw_lock_ref: TraceabilityRef,
    provenance_ref: TraceabilityRef,
    lock_id: DatasetLockId,
    lock_version: ObjectVersion,
    cutoff: datetime,
) -> tuple[NormalizedBarManifest, DatasetLock]:
    require_utc(created_at, "created_at")
    require_utc(cutoff, "cutoff")
    if not bars or any(bar.finality is BarFinality.INCOMPLETE for bar in bars):
        raise NormalizedDatasetAssemblyError("finalized dataset requires nonempty final bars")
    if any(bar.availability_time > cutoff for bar in bars):
        raise NormalizedDatasetAssemblyError("availability exceeds dataset knowledge cutoff")
    if len({(bar.bar_id, bar.version) for bar in bars}) != len(bars):
        raise NormalizedDatasetAssemblyError("bar identity/version must be unique")
    if any(
        bar.schema_ref != schema_ref or bar.normalization_version != normalization_version
        for bar in bars
    ):
        raise NormalizedDatasetAssemblyError("mixed schema/normalization version forbidden")
    if any(
        finding.disposition in (BarPairDisposition.DUPLICATE, BarPairDisposition.CONFLICT)
        for finding in classify_bars(bars)
    ):
        raise BarConflict("duplicate/conflicting business key blocks finalized dataset")

    def sorted_refs(refs: tuple[TraceabilityRef, ...]) -> tuple[TraceabilityRef, ...]:
        return tuple(
            sorted(
                set(refs),
                key=lambda item: (
                    str(item.object_id),
                    item.version.number,
                    item.expected_fingerprint or "",
                ),
            )
        )

    manifest = NormalizedBarManifest(
        dataset_id,
        version,
        created_at,
        sorted_refs(tuple(bar_ref(bar) for bar in bars)),
        sorted_refs(tuple(bar.source_ref for bar in bars)),
        sorted_refs(tuple(bar.instrument_ref for bar in bars)),
        sorted_refs(tuple(bar.timeframe_ref for bar in bars)),
        schema_ref,
        normalization_version,
        raw_lock_ref,
        provenance_ref,
    )
    exact = TraceabilityRef(dataset_id, version, _fingerprint(manifest))
    lock = DatasetLock(lock_id, lock_version, exact, exact, created_at, cutoff, provenance_ref)
    return manifest, lock
