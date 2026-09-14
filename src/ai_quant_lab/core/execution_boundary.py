"""EXE-01 documentary boundary. No order, position, capital, or adapter API exists."""

from dataclasses import dataclass

from ai_quant_lab.core.model import ExecutionState


class ExecutionBoundaryViolation(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ExecutionBoundary:
    module_id: str = "EXE-01"
    state: ExecutionState = ExecutionState.PLANNED_CLOSED

    def reject(self, requested_capability: str) -> None:
        raise ExecutionBoundaryViolation(
            f"{self.module_id} is {self.state}; {requested_capability!r} is unavailable"
        )


EXE_01 = ExecutionBoundary()
