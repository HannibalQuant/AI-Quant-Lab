from __future__ import annotations

import hashlib
from pathlib import Path


_ROOT = Path(__file__).resolve().parents[1]
_PINE = _ROOT / "docs/research/artifacts/AIQL_RR3_SOLUSDT_4H_CANDIDATE_2_FINAL.pine"
_HANDOFF = (
    _ROOT / "docs/research/RESEARCH_RUN_3_CANDIDATE_2_CHAMPION_FREEZE_HANDOFF_v1.md"
)
_EXPECTED_PINE_SHA256 = "4c3857331eba9c1c7cf141c91c63595ae9d7fa0ac3e719cc1abf9a5891e6aaf3"


def test_rr3_champion_pine_is_exact_frozen_artifact() -> None:
    payload = _PINE.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == _EXPECTED_PINE_SHA256

    source = payload.decode("utf-8")
    required = (
        "//@version=6",
        'strategy(\n    "AIQL RR3 SOLUSDT 4H Candidate 2"',
        "fastEmaLength = 12",
        "mediumEmaLength = 72",
        "slowEmaLength = 160",
        "rsiLongMin = 61.0",
        "rsiShortMax = 38.0",
        "emaSeparationMinPct = 0.2",
        "adxSlopeLength = 1",
        "atrPctMin = 0.5",
        "atrPctMax = 4.0",
        "pyramiding=0",
        "process_orders_on_close=false",
        "calc_on_every_tick=false",
        "commission_value=0.1",
    )
    for token in required:
        assert token in source

    forbidden = (
        "request.security",
        "request.security_lower_tf",
        "strategy.risk.",
        "alert(",
        "alertcondition(",
        "webhook",
    )
    lowered = source.lower()
    for token in forbidden:
        assert token.lower() not in lowered


def test_rr3_champion_handoff_keeps_research_authority_closed() -> None:
    handoff = _HANDOFF.read_text(encoding="utf-8")

    required = (
        "FROZEN_RESEARCH_CHAMPION",
        "MANUAL_TRADINGVIEW_RESEARCH_VERIFIED_WITH_KNOWN_PARITY_LIMITATIONS",
        "RR3 Candidate #5",
        "RR3 Candidate #8",
        "RR3 Candidate #11",
        "RR3 Candidate #146",
        "paper monitoring authorization: `NOT_AUTHORIZED`",
        "deployment authorization: `NOT_AUTHORIZED`",
        "live execution: `NOT_AUTHORIZED`",
        "execution state: `PLANNED_CLOSED`",
    )
    for token in required:
        assert token in handoff
