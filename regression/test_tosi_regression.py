from __future__ import annotations

import pytest


@pytest.mark.skip(reason="Tosi decomposition checks are pending future CAS-enabled regressions.")
def test_tosi_regression() -> None:
    raise AssertionError("placeholder")
