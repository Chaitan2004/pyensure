import pytest

from pyensure import ensure, disable, enable


@ensure(pre=("x > 0",))
def add_one(x):
    return x + 1


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (-5, -4),
        (0, 1),
        (10, 11),
    ]
)
def test_disable_contracts(value, expected):
    disable()

    try:
        assert add_one(value) == expected
    finally:
        enable()
