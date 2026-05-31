import pytest

from pyensure import ensure, EnsureError


@ensure(pre=("x > 0",))
def add_one(x):
    return x + 1


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1, 2),
        (5, 6),
        (100, 101),
    ]
)
def test_precondition_pass(value, expected):
    assert add_one(value) == expected


@pytest.mark.parametrize("value", [0, -1, -50])
def test_precondition_fail(value):
    with pytest.raises(EnsureError):
        add_one(value)
