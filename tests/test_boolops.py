import pytest

from pyensure import ensure, EnsureError


@ensure(pre=("x > 0 and y > 0",))
def add(x, y):
    return x + y


@ensure(pre=("x > 0 or y > 0",))
def add_or(x, y):
    return x + y


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (1, 2, 3),
        (10, 5, 15),
        (100, 1, 101),
    ]
)
def test_and_pass(x, y, expected):
    assert add(x, y) == expected


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (-1, 2),
        (1, 0),
        (0, 0),
    ]
)
def test_and_fail(x, y):
    with pytest.raises(EnsureError):
        add(x, y)


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (-1, 2, 1),
        (3, -2, 1),
        (1, 1, 2),
    ]
)
def test_or_pass(x, y, expected):
    assert add_or(x, y) == expected


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (-1, -2),
        (0, 0),
        (-10, 0),
    ]
)
def test_or_fail(x, y):
    with pytest.raises(EnsureError):
        add_or(x, y)
