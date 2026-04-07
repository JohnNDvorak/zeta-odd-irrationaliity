from __future__ import annotations

import pytest


@pytest.mark.skip(reason="Arithmetic-loss regression requires the deferred certificate backend.")
def test_bz_arithmetic_loss_regression() -> None:
    raise AssertionError("placeholder")
