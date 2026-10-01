"""Boundary and causality tests for the isolated RR4 entry gate."""

from decimal import Decimal
from types import SimpleNamespace

import pytest
from run import short_allowed


@pytest.mark.parametrize("threshold", [4, 8, 12])
def test_exact_threshold_and_adjacent_values(threshold):
    bars = [SimpleNamespace(close=SimpleNamespace(text="100")) for _ in range(19)]
    boundary = Decimal(100 - threshold)
    bars[18].close.text = str(boundary)
    assert short_allowed(bars, 18, Decimal(threshold))
    bars[18].close.text = str(boundary + Decimal("0.000001"))
    assert not short_allowed(bars, 18, Decimal(threshold))
    bars[18].close.text = str(boundary - Decimal("0.000001"))
    assert short_allowed(bars, 18, Decimal(threshold))


def test_warmup_and_disabled_control():
    assert not short_allowed([], 17, Decimal(4))
    assert short_allowed([], 0, None)


def test_gate_never_reads_future_bar():
    class CompletedBars:
        def __getitem__(self, index):
            assert index in (0, 18)
            return SimpleNamespace(close=SimpleNamespace(text="100" if index == 0 else "92"))

    assert short_allowed(CompletedBars(), 18, Decimal(8))
