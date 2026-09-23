"""Exact Sprint 17 implementation-precondition registry."""

# fmt: off  # Dense governed register mirrors Sprint 12 Section 48.

from dataclasses import dataclass
from enum import StrEnum


class UnresolvedGovernancePrecondition(ValueError):
    pass


class PreconditionStatus(StrEnum):
    OPEN = "OPEN"
    PARTIALLY_RESOLVED = "PARTIALLY_RESOLVED"
    RESOLVED = "RESOLVED"
    DEFERRED = "DEFERRED"
    BLOCKING_FOR_DOMAIN = "BLOCKING_FOR_DOMAIN"


@dataclass(frozen=True, slots=True)
class ImplementationPrecondition:
    precondition_id: str
    title: str
    affected_modules: tuple[str, ...]
    affected_implementation: tuple[str, ...]
    authority_owner: str
    required_decision: str
    status: PreconditionStatus
    fail_closed_default: str
    dependencies: tuple[str, ...]
    required_tests: tuple[str, ...]
    sprint_1_resolution: str
    source: str = "planning/PHASE_2_INTEGRATION_TRACEABILITY_IMPLEMENTATION_READINESS_REVIEW_v1.md#48"

    @property
    def is_satisfied(self) -> bool:
        return self.status is PreconditionStatus.RESOLVED

    def require_resolved(self, domain: str) -> None:
        if not self.is_satisfied:
            raise UnresolvedGovernancePrecondition(
                f"{self.precondition_id} is {self.status}; {domain} remains fail-closed"
            )


def _split(value: str) -> tuple[str, ...]:
    return tuple(item for item in value.split(",") if item)


def _ip(number: int, title: str, modules: str, domains: str, owner: str, decision: str,
        status: PreconditionStatus, default: str, deps: str, tests: str, note: str
        ) -> ImplementationPrecondition:
    return ImplementationPrecondition(
        f"IP-{number:02d}", title, _split(modules), _split(domains), owner, decision, status,
        default, _split(deps), _split(tests), note
    )


P = PreconditionStatus
PRECONDITIONS = (
    _ip(1, "Principal authentication model", "IAM-01", "IAM,command,agents", "IAM + Security", "Approve authentication and threat model", P.OPEN, "No consequential admission", "", "T08,T14", "OPEN: no authentication runtime"),
    _ip(2, "Integrity/signature/tamper-evidence model", "AUD-01,AUD-02,AUD-03", "ART,EVI,AUD", "GOV + Security", "Approve integrity/signature model", P.PARTIALLY_RESOLVED, "Unverifiable is inadmissible", "IP-04", "T04,T05,T25", "PARTIAL: canonical persisted bytes and verified reload detect tamper; signatures/trust roots and authenticity remain open"),
    _ip(3, "Authority/delegation/revocation binding", "IAM-02,GOV-01", "IAM,mutations", "GOV + IAM", "Approve binding semantics", P.OPEN, "No inferred authority", "IP-01", "T08,T13,T14", "OPEN: IDs grant no authority"),
    _ip(4, "Canonical serialization/ID/hash/equivalence", "AUD-01,DAT-05", "artifacts,data", "ART + DAT", "Approve representation scope", P.PARTIALLY_RESOLVED, "No unsupported lock claim", "", "T04,T36", "PARTIAL: governed dataset, admission, eligibility, validation, robustness, optimization-selection and Pine-source intake artifacts persist and reconstruct with exact canonical identity; broader representation authority remains open"),
    _ip(5, "Time/clock/timezone/ordering rules", "DAT-03,ORC-02", "DAT,STA,commands", "STA + DAT", "Approve temporal specification", P.PARTIALLY_RESOLVED, "Hold ambiguity", "", "T16,T35", "PARTIAL: eligibility binds explicit UTC/availability semantics, deterministic cutoff and explicit calendar policy without substituting ingestion time; vendor late-data/calendar/clock trust policy remains open"),
    _ip(6, "Emergency and release/reactivation authority", "RSK-02,HUM-02", "RSK,DEC,HUM,command", "GOV + humans", "Approve roles/dual control", P.OPEN, "Containment persists", "IP-03,IP-07", "T09,T11,T33", "OPEN: no emergency runtime"),
    _ip(7, "Approval/confirmation/expiry policy", "HUM-01,HUM-02", "command,decision", "GOV + IAM", "Approve scoped policy", P.OPEN, "Require fresh confirmation", "IP-03", "T09,T14,T35", "OPEN: no approval runtime"),
    _ip(8, "Evidence/validation/monitoring freshness", "AUD-02,VAL-06,MON-01", "EVI,VAL,MON", "EVI + VAL + MON", "Approve freshness crosswalk", P.OPEN, "Unassessed/stale cannot authorize", "IP-05", "T05,T20,T27", "OPEN: UNASSESSED is explicit"),
    _ip(9, "Validation method specifications", "VAL-01,VAL-02,VAL-03,VAL-04,VAL-05,VAL-06,VAL-07", "VAL", "VAL + GOV", "Approve method scopes", P.PARTIALLY_RESOLVED, "No validation claim outside exact bounded method", "IP-08", "T12,T20,T21,T22", "PARTIAL: exact fixed-strategy robustness plus bounded Bonferroni-controlled grid selection add deterministic evidence; protected holdout evidence, dependence-aware methods, general multiplicity correction and broader method approval remain open"),
    _ip(10, "Monitoring thresholds/windows/multiplicity", "MON-01,MON-02,MON-03", "MON", "MON + VAL + RSK", "Approve methodology", P.OPEN, "Observation only", "IP-08", "T22,T23,T34", "OPEN: outside Sprint 1"),
    _ip(11, "Data quality/reconciliation semantics", "DAT-01,DAT-02,DAT-03,DAT-04,DAT-05", "DAT", "DAT + GOV", "Approve source contracts", P.PARTIALLY_RESOLVED, "Quarantine unknown/conflict", "IP-04,IP-05", "T15,T16,T32", "PARTIAL: versioned eligibility policy applies explicit row/rejection/quarantine/gap/completeness bounds to an exact quality snapshot; universal provider quality acceptance remains open"),
    _ip(12, "Retention/privacy/licensing/legal policy", "AUD-01,AUD-02,AUD-03,DAT-01", "AUD,DAT,ledgers", "GOV + Legal + Data", "Approve policy", P.OPEN, "Preserve and restrict", "", "T25,T30", "OPEN: eligibility enforces declared permission, retention and local-use restrictions fail-closed; no legal verification, competent legal authority, recovery or deletion workflow exists"),
    _ip(13, "Trust-boundary threat model/adapters", "IAM-01,HUM-01,ORC-01", "adapters,MACP,SMI", "Security + IAM", "Approve threat model", P.OPEN, "Adapters disabled", "IP-01,IP-02", "T22,T37", "OPEN: bounded Pine intake rejects unsupported static features and remains local-only, but does not authenticate the actor, source author, TradingView platform or broader adapter boundary"),
    _ip(14, "Implementation governance/change/release", "GOV-01,GOV-02,AUD-03", "Phase 3", "GOV + QA + AUD", "Approve wave gates", P.PARTIALLY_RESOLVED, "No wave promotion", "", "T30,T31,T38", "PARTIAL: immutable Pine source custody, selected-candidate/evidence lineage, golden evidence and tamper tests extend CI evidence; Pine/Python parity and production release criteria remain open"),
)


def precondition(precondition_id: str) -> ImplementationPrecondition:
    try:
        return next(item for item in PRECONDITIONS if item.precondition_id == precondition_id)
    except StopIteration as exc:
        raise KeyError(precondition_id) from exc
# fmt: on
