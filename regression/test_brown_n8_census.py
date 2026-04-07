from __future__ import annotations

import pytest


@pytest.mark.skip(reason="Brown N=8 census recovery is not implemented in the Python-only scaffold.")
def test_brown_n8_census_regression() -> None:
    raise AssertionError("placeholder")
