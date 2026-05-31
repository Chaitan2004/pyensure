import pytest

from pyensure import ensure, EnsureError


def is_even(x):
    return x % 2 == 0


@ensure(pre=("is_even(x)",))
def process(x):
    return x


@pytest.mark.parametrize("value", [0, 2, 4, 100])
def test_function_call_pass(value):
    assert process(value) == value


@pytest.mark.parametrize("value", [1, 3, 99])
def test_function_call_fail(value):
    with pytest.raises(EnsureError):
        process(value)
