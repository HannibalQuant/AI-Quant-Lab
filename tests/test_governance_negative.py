# fmt: off  # Capability attack cases are intentionally kept as one matrix.
import inspect

import pytest

import ai_quant_lab
from ai_quant_lab.core.execution_boundary import ExecutionBoundaryViolation
from ai_quant_lab.core.model import (
    ExecutionState,
    InvalidState,
    StateAssignment,
    StateAxis,
    StateVector,
)


def test_exe_01_is_planned_closed() -> None:
    assert ai_quant_lab.EXE_01.module_id == "EXE-01"
    assert ai_quant_lab.EXE_01.state is ExecutionState.PLANNED_CLOSED


@pytest.mark.parametrize(
    "capability",
    ["buy", "sell", "place_order", "open_position", "allocate_capital",
     "broker_api", "exchange_api", "trading_webhook", "paper_trading", "live_trading"],
)
def test_execution_capabilities_fail_closed(capability: str) -> None:
    with pytest.raises(ExecutionBoundaryViolation, match="PLANNED_CLOSED"):
        ai_quant_lab.EXE_01.reject(capability)


def test_execution_state_cannot_be_opened() -> None:
    with pytest.raises(InvalidState):
        StateAssignment(StateAxis.EXECUTION, "OPEN")


def test_state_axes_cannot_be_conflated() -> None:
    with pytest.raises(InvalidState):
        StateVector((StateAssignment(StateAxis.WORKFLOW, "held"),
                     StateAssignment(StateAxis.WORKFLOW, "approved")))


def test_package_exposes_no_execution_function() -> None:
    prohibited = {"buy", "sell", "order", "position", "capital", "broker", "exchange", "webhook"}
    exported = {name.lower() for name, _ in inspect.getmembers(ai_quant_lab)}
    assert not prohibited.intersection(exported)
# fmt: on
