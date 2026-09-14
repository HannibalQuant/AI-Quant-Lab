import pytest

from ai_quant_lab.core.governance import (
    PRECONDITIONS, PreconditionStatus, UnresolvedGovernancePrecondition, precondition,
)


def test_exact_fourteen_preconditions_are_registered() -> None:
    assert [item.precondition_id for item in PRECONDITIONS] == [
        f"IP-{number:02d}" for number in range(1, 15)
    ]


def test_precondition_register_is_immutable() -> None:
    assert isinstance(PRECONDITIONS, tuple)


@pytest.mark.parametrize("item", PRECONDITIONS)
def test_open_or_partial_never_counts_as_satisfied(item: object) -> None:
    assert not item.is_satisfied  # type: ignore[attr-defined]


def test_open_precondition_blocks_affected_domain() -> None:
    with pytest.raises(UnresolvedGovernancePrecondition):
        precondition("IP-01").require_resolved("command")


def test_status_summary_is_honest() -> None:
    statuses = [item.status for item in PRECONDITIONS]
    assert statuses.count(PreconditionStatus.RESOLVED) == 0
    assert statuses.count(PreconditionStatus.PARTIALLY_RESOLVED) == 4
    assert statuses.count(PreconditionStatus.OPEN) == 10
