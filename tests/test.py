import pytest

from pyensure import EnsureError, ensure


@ensure(pre=("x > 0",), post=("result > x",))
def add_one(x):
    return x + 1


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1, 2),
        (5, 6),
        (50, 51),
    ]
)
def test_add_one_pass(value, expected):
    assert add_one(value) == expected


@pytest.mark.parametrize("value", [0, -1, -50])
def test_add_one_fail(value):
    with pytest.raises(EnsureError):
        add_one(value)
