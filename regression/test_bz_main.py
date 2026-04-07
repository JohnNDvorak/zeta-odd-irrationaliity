from __future__ import annotations

import pytest


@pytest.mark.skip(reason="Gate 2 numeric reproduction is deferred until CAS integration exists.")
def test_bz_main_regression() -> None:
    raise AssertionError("placeholder")
