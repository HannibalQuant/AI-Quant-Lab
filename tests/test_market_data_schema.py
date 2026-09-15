"""Synthetic governed market-bar contracts, normalized datasets and attacks."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.data import (
    DataQualityState,
    DatasetLock,
    DatasetLockId,
    DecimalValue,
    InstrumentClass,
    InstrumentId,
    InstrumentIdentity,
    ObservationId,
    RawField,
    RawObservation,
    ReconciliationDisposition,
    SourceId,
    SourceIdentity,
    SourceType,
    TemporalCoordinates,
)
from ai_quant_lab.core.integrity import IntegrityMismatch, fingerprint_record, verify_integrity
from ai_quant_lab.core.market_data import (
    AlignmentKind,
    BarConflict,
    BarFinality,
    BarPairDisposition,
    BarTimestampMeaning,
    GapDisposition,
    InvalidOHLCGeometry,
    InvalidTimeframe,
    MarketBar,
    MarketBarId,
    MarketDataError,
    MarketDataSchema,
    MarketDataSchemaId,
    NormalizedBarManifest,
    NormalizedDatasetAssemblyError,
    SchemaMappingError,
    TimeframeId,
    TimeframeIdentity,
    TimeframeUnit,
    VolumeSemantic,
    assemble_normalized_dataset,
    bar_ref,
    classify_bars,
    classify_fixed_gaps,
    normalize_bar,
)
from ai_quant_lab.core.model import (
    DatasetId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
)

V1 = ObjectVersion(1)
T0 = datetime(2025, 1, 1, tzinfo=UTC)
F = "sha256:" + "a" * 64


def stamp(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def timeframe(count: int = 1, unit: TimeframeUnit = TimeframeUnit.HOUR) -> TimeframeIdentity:
    suffix = {TimeframeUnit.MINUTE: "m", TimeframeUnit.HOUR: "h", TimeframeUnit.DAY: "d"}[unit]
    return TimeframeIdentity(
        TimeframeId(f"{count}{suffix}"), V1, unit, count, AlignmentKind.UTC_EPOCH_FIXED, V1
    )


def schema(
    tf: TimeframeIdentity,
    *,
    volume: bool = True,
    timestamp_meaning: BarTimestampMeaning = BarTimestampMeaning.OPEN,
) -> MarketDataSchema:
    return MarketDataSchema(
        MarketDataSchemaId("synthetic-ohlcv"),
        V1,
        TraceabilityRef(tf.timeframe_id, V1, fingerprint_record(tf)),
        timestamp_meaning,
        "bar_open_time",
        "bar_close_time",
        "open",
        "high",
        "low",
        "close",
        "volume" if volume else None,
        "finality",
        VolumeSemantic.BASE if volume else VolumeSemantic.ABSENT,
        V1,
    )


def raw(
    opening: datetime = T0,
    *,
    tf: TimeframeIdentity | None = None,
    source: str = "synthetic-source",
    instrument: str = "synthetic-spot",
    name: str = "raw-one",
    prices: tuple[str, str, str, str] = ("1", "2", "0", "1.5"),
    available: datetime | None = None,
    finality: BarFinality = BarFinality.FINAL,
    volume: str | None = "0",
    timestamp_meaning: BarTimestampMeaning = BarTimestampMeaning.OPEN,
    extra: RawField | None = None,
) -> RawObservation:
    tf = tf or timeframe()
    bar_close = opening + tf.duration
    available = available or bar_close + timedelta(seconds=5)
    source_obj = SourceIdentity(
        SourceId(source),
        V1,
        "Synthetic Provider",
        SourceType.SYNTHETIC_FIXTURE,
        "feed-v1",
        "fixture-v1",
        None,
        V1,
    )
    instrument_obj = InstrumentIdentity(
        InstrumentId(instrument),
        V1,
        "TESTUSD",
        InstrumentClass.SPOT,
        "TEST",
        "USD",
        None,
        None,
        V1,
    )
    fields = [
        RawField("bar_open_time", stamp(opening)),
        RawField("bar_close_time", stamp(bar_close)),
        RawField("open", DecimalValue.from_text(prices[0])),
        RawField("high", DecimalValue.from_text(prices[1])),
        RawField("low", DecimalValue.from_text(prices[2])),
        RawField("close", DecimalValue.from_text(prices[3])),
        RawField("finality", finality.value),
    ]
    if volume is not None:
        fields.append(RawField("volume", DecimalValue.from_text(volume)))
    if extra is not None:
        fields.append(extra)
    event_time = opening if timestamp_meaning is BarTimestampMeaning.OPEN else bar_close
    return RawObservation(
        ObservationId(name),
        V1,
        TraceabilityRef(source_obj.source_id, V1, fingerprint_record(source_obj)),
        TraceabilityRef(instrument_obj.instrument_id, V1, fingerprint_record(instrument_obj)),
        TemporalCoordinates(event_time, available, available + timedelta(seconds=2)),
        tuple(sorted(fields, key=lambda field: field.name)),
        TraceabilityRef(ProvenanceId("raw-fixture"), V1, F),
        None,
        DataQualityState.ACCEPTED,
        ReconciliationDisposition.UNIQUE,
    )


def normalize(
    observation: RawObservation | None = None,
    *,
    tf: TimeframeIdentity | None = None,
    bar_name: str = "bar-one",
    version: ObjectVersion = V1,
    schema_override: MarketDataSchema | None = None,
    supersedes: TraceabilityRef | None = None,
) -> MarketBar:
    tf = tf or timeframe()
    observation = observation or raw(tf=tf)
    mapping = schema_override or schema(
        tf, volume=any(field.name == "volume" for field in observation.payload)
    )
    return normalize_bar(
        observation,
        mapping,
        tf,
        MarketBarId(bar_name),
        version,
        V1,
        TraceabilityRef(ProvenanceId("normalization-fixture"), V1, F),
        supersedes=supersedes,
    ).bar


def dataset(
    bars: tuple[MarketBar, ...], cutoff: datetime = T0 + timedelta(hours=5)
) -> tuple[NormalizedBarManifest, DatasetLock]:
    return assemble_normalized_dataset(
        bars,
        DatasetId("normalized-bars"),
        V1,
        cutoff,
        bars[0].schema_ref,
        V1,
        TraceabilityRef(DatasetLockId("raw-dataset-lock"), V1, F),
        TraceabilityRef(ProvenanceId("normalized-manifest"), V1, F),
        DatasetLockId("normalized-lock"),
        V1,
        cutoff,
    )


@pytest.mark.parametrize(
    ("count", "unit", "label"),
    (
        (15, TimeframeUnit.MINUTE, "15m"),
        (30, TimeframeUnit.MINUTE, "30m"),
        (1, TimeframeUnit.HOUR, "1h"),
        (2, TimeframeUnit.HOUR, "2h"),
        (3, TimeframeUnit.HOUR, "3h"),
        (4, TimeframeUnit.HOUR, "4h"),
        (1, TimeframeUnit.DAY, "1d"),
    ),
)
def test_exact_fixed_timeframe_identity(count: int, unit: TimeframeUnit, label: str) -> None:
    tf = timeframe(count, unit)
    assert tf.timeframe_id == TimeframeId(label)
    assert decode(encode(tf), TimeframeIdentity) == tf
    verify_integrity(tf, fingerprint_record(tf))


def test_timeframe_rejects_alias_calendar_and_alignment() -> None:
    with pytest.raises(InvalidTimeframe):
        TimeframeIdentity(
            TimeframeId("60m"), V1, TimeframeUnit.HOUR, 1, AlignmentKind.UTC_EPOCH_FIXED, V1
        )
    with pytest.raises(InvalidTimeframe):
        TimeframeIdentity(
            TimeframeId("1h"), V1, TimeframeUnit.HOUR, 0, AlignmentKind.UTC_EPOCH_FIXED, V1
        )
    with pytest.raises(InvalidTimeframe):
        replace(timeframe(1, TimeframeUnit.DAY), alignment=AlignmentKind.CALENDAR_UNRESOLVED)
    with pytest.raises(InvalidTimeframe):
        timeframe(4).require_aligned(T0 + timedelta(hours=1))


def test_market_bar_roundtrip_lineage_and_knowledge_time() -> None:
    opening = T0 + timedelta(hours=10)
    observation = raw(opening, name="raw-delayed")
    bar = normalize(observation)
    assert bar.bar_open == opening
    assert bar.bar_close == opening + timedelta(hours=1)
    assert bar.legitimate_knowledge_time == opening + timedelta(hours=1, seconds=5)
    assert bar.source_observation_ref.expected_fingerprint == fingerprint_record(observation)
    assert decode(encode(bar), MarketBar) == bar
    verify_integrity(bar, fingerprint_record(bar))
    assert bar.volume == DecimalValue.from_text("0")


def test_missing_volume_is_not_zero_volume() -> None:
    without = normalize(raw(volume=None))
    with_zero = normalize(raw(volume="0", name="raw-zero"), bar_name="bar-zero")
    assert without.volume is None and without.volume_semantic is VolumeSemantic.ABSENT
    assert with_zero.volume == DecimalValue.from_text("0")
    assert fingerprint_record(without) != fingerprint_record(with_zero)
    with pytest.raises(MarketDataError):
        replace(with_zero, volume=None)


@pytest.mark.parametrize(
    "prices",
    (
        ("3", "2", "0", "1"),
        ("1", "0", "-1", "0"),
        ("1", "2", "1.5", "1"),
        ("1", "2", "0", "3"),
        ("1", "2", "0", "-1"),
        ("1", "-2", "0", "1"),
    ),
)
def test_invalid_ohlc_geometry_is_never_repaired(prices: tuple[str, str, str, str]) -> None:
    with pytest.raises(InvalidOHLCGeometry):
        normalize(raw(prices=prices))


def test_negative_prices_can_be_structurally_valid() -> None:
    bar = normalize(raw(prices=("-2", "-1", "-3", "-2.5")))
    assert bar.close == DecimalValue.from_text("-2.5")


def test_float_nonfinite_and_negative_volume_fail_closed() -> None:
    with pytest.raises(ValueError):
        RawField("open", 1.5)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        DecimalValue.from_text("NaN")
    with pytest.raises(ValueError):
        DecimalValue.from_text("Infinity")
    with pytest.raises(MarketDataError):
        normalize(raw(volume="-1"))


def test_schema_version_unknown_fields_and_event_meaning() -> None:
    tf = timeframe()
    observation = raw()
    with pytest.raises(SchemaMappingError):
        normalize(
            observation,
            schema_override=replace(schema(tf), contract_version=ObjectVersion(2)),
        )
    with pytest.raises(SchemaMappingError):
        normalize(raw(extra=RawField("unexpected", "x")))
    with pytest.raises(SchemaMappingError):
        normalize(
            observation, schema_override=schema(tf, timestamp_meaning=BarTimestampMeaning.CLOSE)
        )
    with pytest.raises(SchemaMappingError):
        replace(schema(tf), close_field="open")


def test_wrong_timeframe_contract_and_binding_fail_closed() -> None:
    tf4 = timeframe(4)
    with pytest.raises(SchemaMappingError):
        normalize(raw(), schema_override=schema(tf4))
    with pytest.raises(SchemaMappingError):
        normalize(raw(), tf=replace(timeframe(), contract_version=ObjectVersion(2)))
    with pytest.raises(MarketDataError):
        replace(normalize(raw()), timeframe_ref=TraceabilityRef(SourceId("wrong"), V1, F))


def test_malformed_misaligned_and_wrong_interval_are_not_repaired() -> None:
    observation = raw()
    malformed_fields = tuple(
        replace(field, value="2025-01-01 00:00") if field.name == "bar_open_time" else field
        for field in observation.payload
    )
    with pytest.raises(SchemaMappingError):
        normalize(replace(observation, payload=malformed_fields))
    misaligned = raw(T0 + timedelta(minutes=1))
    with pytest.raises(InvalidTimeframe):
        normalize(misaligned)
    interval = tuple(
        replace(field, value=stamp(T0 + timedelta(hours=2)))
        if field.name == "bar_close_time"
        else field
        for field in observation.payload
    )
    with pytest.raises(InvalidTimeframe):
        normalize(replace(observation, payload=interval))


def test_naive_non_utc_and_early_final_availability_rejected() -> None:
    bar = normalize(raw())
    with pytest.raises(ValueError):
        replace(bar, bar_open=datetime(2025, 1, 1))
    with pytest.raises(ValueError):
        replace(bar, bar_open=datetime(2025, 1, 1, tzinfo=timezone(timedelta(hours=1))))
    with pytest.raises(ValueError):
        replace(bar, availability_time=T0 + timedelta(hours=1, seconds=-1))
    with pytest.raises(SchemaMappingError):
        normalize(raw(available=T0 + timedelta(minutes=30)))


def test_nonaccepted_raw_and_derived_fields_do_not_normalize() -> None:
    observation = raw()
    with pytest.raises(SchemaMappingError):
        normalize(replace(observation, quality=DataQualityState.QUARANTINED))
    for name in ("signal_buy", "strategy_label", "indicator_rsi", "order_side"):
        with pytest.raises(ValueError):
            RawField(name, "injected")


def test_corrected_raw_cannot_launder_into_unlinked_bar() -> None:
    first = raw()
    updated = replace(
        raw(name="corrected", finality=BarFinality.CORRECTED_FINAL),
        supersedes=TraceabilityRef(first.observation_id, first.version, fingerprint_record(first)),
        reconciliation=ReconciliationDisposition.CORRECTION,
    )
    with pytest.raises(SchemaMappingError):
        normalize(updated)


def test_finality_incomplete_representation_and_dataset_exclusion() -> None:
    forming = normalize(raw(finality=BarFinality.INCOMPLETE, available=T0 + timedelta(minutes=30)))
    assert forming.finality is BarFinality.INCOMPLETE
    with pytest.raises(NormalizedDatasetAssemblyError):
        dataset((forming,))
    final = normalize(raw())
    assert final.legitimate_knowledge_time > final.bar_close


def test_research_cutoff_cannot_see_delayed_bar() -> None:
    bar = normalize(raw())
    with pytest.raises(NormalizedDatasetAssemblyError):
        dataset((bar,), cutoff=bar.bar_close)
    manifest, lock = dataset((bar,))
    assert lock.manifest_ref.expected_fingerprint == fingerprint_record(manifest)
    assert lock.temporal_cutoff >= bar.legitimate_knowledge_time


def test_4h_interval_sequence_and_mechanical_1h_gap() -> None:
    tf4 = timeframe(4)
    series4 = tuple(
        normalize(
            raw(T0 + timedelta(hours=offset), tf=tf4, name=f"raw4-{offset}"),
            tf=tf4,
            bar_name=f"bar4-{offset}",
        )
        for offset in (0, 4, 8)
    )
    assert [bar.bar_close for bar in series4] == [T0 + timedelta(hours=x) for x in (4, 8, 12)]
    assert all(
        x.disposition is GapDisposition.CONTIGUOUS for x in classify_fixed_gaps(series4, tf4)
    )
    hourly = tuple(
        normalize(
            raw(T0 + timedelta(hours=offset), name=f"raw1-{offset}"), bar_name=f"bar1-{offset}"
        )
        for offset in (10, 11, 13)
    )
    gaps = classify_fixed_gaps(hourly, timeframe())
    assert [gap.missing_intervals for gap in gaps] == [0, 1]
    assert gaps[-1].disposition is GapDisposition.MECHANICAL_GAP
    assert not any(bar.bar_open == T0 + timedelta(hours=12) for bar in hourly)


def test_duplicate_conflict_and_no_arrival_winner() -> None:
    first = normalize(raw(), bar_name="first")
    duplicate = normalize(raw(name="second"), bar_name="second")
    conflict = normalize(raw(name="third", prices=("1", "2", "0", "1.9")), bar_name="third")
    assert classify_bars((first, duplicate))[0].disposition is BarPairDisposition.DUPLICATE
    assert classify_bars((first, conflict))[0].disposition is BarPairDisposition.CONFLICT
    assert classify_bars((conflict, first))[0].disposition is BarPairDisposition.CONFLICT
    with pytest.raises(BarConflict):
        dataset((first, conflict))
    with pytest.raises(BarConflict):
        dataset((first, duplicate))


def test_source_timeframe_and_instrument_business_keys_do_not_collapse() -> None:
    first = normalize(raw(), bar_name="one")
    other_source = normalize(raw(source="other-source"), bar_name="two")
    other_instrument = normalize(raw(instrument="other-instrument"), bar_name="three")
    tf4 = timeframe(4)
    other_timeframe = normalize(raw(tf=tf4), tf=tf4, bar_name="four")
    assert (
        len({bar.business_key for bar in (first, other_source, other_instrument, other_timeframe)})
        == 4
    )


def test_explicit_correction_preserves_prior_bar() -> None:
    original_raw = raw()
    original = normalize(original_raw, bar_name="original")
    changed = replace(
        raw(
            name="raw-corrected",
            prices=("1", "2", "0", "1.9"),
            finality=BarFinality.CORRECTED_FINAL,
        ),
        reconciliation=ReconciliationDisposition.CORRECTION,
        supersedes=TraceabilityRef(
            original_raw.observation_id, V1, fingerprint_record(original_raw)
        ),
    )
    corrected = normalize_bar(
        changed,
        schema(timeframe()),
        timeframe(),
        MarketBarId("corrected"),
        ObjectVersion(2),
        V1,
        TraceabilityRef(ProvenanceId("normalization-fixture"), V1, F),
        supersedes=bar_ref(original),
    ).bar
    assert corrected.supersedes == bar_ref(original)
    assert corrected.finality is BarFinality.CORRECTED_FINAL
    assert original.close == DecimalValue.from_text("1.5")
    assert fingerprint_record(original) != fingerprint_record(corrected)


def test_order_independent_exact_normalized_manifest_and_lock() -> None:
    bars = tuple(
        normalize(raw(T0 + timedelta(hours=i), name=f"raw-{i}"), bar_name=f"bar-{i}")
        for i in (0, 1, 2)
    )
    first, first_lock = dataset(bars)
    second, second_lock = dataset(tuple(reversed(bars)))
    assert first == second and first_lock == second_lock
    assert decode(encode(first), NormalizedBarManifest) == first
    assert decode(encode(first_lock), DatasetLock) == first_lock
    for record in (first, first_lock):
        verify_integrity(record, fingerprint_record(record))
    assert first.raw_dataset_lock_ref.object_id == DatasetLockId("raw-dataset-lock")
    changed, changed_lock = dataset(bars[:2])
    assert fingerprint_record(first) != fingerprint_record(changed)
    assert fingerprint_record(first_lock) != fingerprint_record(changed_lock)


def test_fingerprints_change_for_every_material_bar_dimension() -> None:
    bar = normalize(raw())
    expected = fingerprint_record(bar)
    mutations = (
        replace(bar, open=DecimalValue.from_text("1.1")),
        replace(bar, close=DecimalValue.from_text("1.6")),
        replace(bar, availability_time=bar.availability_time + timedelta(seconds=1)),
        replace(bar, source_ref=TraceabilityRef(SourceId("other"), V1, F)),
        replace(bar, instrument_ref=TraceabilityRef(InstrumentId("other"), V1, F)),
        replace(bar, timeframe_ref=TraceabilityRef(TimeframeId("4h"), V1, F)),
    )
    for changed in mutations:
        assert fingerprint_record(changed) != expected
        with pytest.raises(IntegrityMismatch):
            verify_integrity(changed, expected)
    with pytest.raises(FrozenInstanceError):
        setattr(bar, "close", DecimalValue.from_text("2"))  # noqa: B010 - immutable negative test


def test_duplicate_keys_unknown_fields_and_type_attacks() -> None:
    bar = normalize(raw())
    original = encode(bar)
    with pytest.raises(ValueError):
        decode(
            original.replace(b'"$type":"MarketBar"', b'"$type":"MarketBar","$type":"MarketBar"'),
            MarketBar,
        )
    with pytest.raises(ValueError):
        decode(original.replace(b'"payload":{', b'"payload":{"unexpected":1,'), MarketBar)
    with pytest.raises(ValueError):
        decode(original, RawObservation)
    with pytest.raises(ValueError):
        decode(
            original.replace(b'"$representation_version":1', b'"$representation_version":2'),
            MarketBar,
        )


@pytest.mark.parametrize("fixture_index", tuple(range(10)))
def test_read_only_golden_bar_scenarios(fixture_index: int) -> None:
    fixtures = json.loads(
        (Path(__file__).parent / "golden" / "market_bar_scenarios_v1.json").read_text(
            encoding="utf-8"
        )
    )
    scenario = fixtures["scenarios"][fixture_index]
    assert scenario["name"] and scenario["expected_disposition"]
    if fixture_index < 6:
        builders = (
            lambda: normalize(raw()),
            lambda: normalize(raw(tf=timeframe(4)), tf=timeframe(4)),
            lambda: normalize(raw(available=T0 + timedelta(hours=1, minutes=5))),
            lambda: normalize(raw(volume=None)),
            lambda: normalize(raw(volume="0")),
            lambda: normalize(
                raw(
                    finality=BarFinality.INCOMPLETE,
                    available=T0 + timedelta(minutes=30),
                )
            ),
        )
        assert fingerprint_record(builders[fixture_index]()) == scenario["fingerprint"]
