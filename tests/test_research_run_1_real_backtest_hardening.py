"""Research Run #1 real-data backtest scaling regressions."""

from __future__ import annotations

from decimal import Decimal

import pytest

from ai_quant_lab.core.dataset_store import (
    RepositoryObjectKey,
    StoredObjectType,
    _object_byte_limit,
)
from ai_quant_lab.core.model import ObjectVersion
from ai_quant_lab.core.multi_signal_runtime import (
    MultiSignalAccountingError,
    _match_fixed_notional,
)

V1 = ObjectVersion(1)
V2 = ObjectVersion(2)
FINGERPRINT = "sha256:" + "a" * 64


def _key(object_type: StoredObjectType, version: ObjectVersion = V1) -> RepositoryObjectKey:
    return RepositoryObjectKey(object_type, version, FINGERPRINT)


def test_fixed_notional_accepts_only_one_decimal128_ulp_of_round_trip_drift() -> None:
    expected = Decimal("100")
    one_ulp_below = expected - Decimal("1E-31")

    _match_fixed_notional(
        one_ulp_below,
        expected,
        "entry fill does not match governed fixed notional",
    )

    with pytest.raises(
        MultiSignalAccountingError,
        match="entry fill does not match governed fixed notional",
    ):
        _match_fixed_notional(
            expected - Decimal("2E-31"),
            expected,
            "entry fill does not match governed fixed notional",
        )


def test_large_backtest_limit_is_type_specific_and_bounded() -> None:
    assert _object_byte_limit(_key(StoredObjectType.RAW_OBSERVATION)) == 1_000_000
    assert _object_byte_limit(_key(StoredObjectType.DATASET_MANIFEST)) == 8_000_000
    assert _object_byte_limit(_key(StoredObjectType.NORMALIZED_BAR_MANIFEST)) == 8_000_000
    assert (
        _object_byte_limit(_key(StoredObjectType.BACKTEST_RESULT_ARTIFACT, V2))
        == 16_000_000
    )
    assert _object_byte_limit(_key(StoredObjectType.BACKTEST_RUN_RECORD, V2)) == 1_000_000
