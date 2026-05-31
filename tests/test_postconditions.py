import pytest

from pyensure import ensure, EnsureError


@ensure(post=("result > 0",))
def positive_result(x):
    return x


@ensure(post=("result > 0",))
def negative_result(x):
    return x


@pytest.mark.parametrize("value", [1, 5, 99])
def test_postcondition_pass(value):
    assert positive_result(value) == value


@pytest.mark.parametrize("value", [0, -1, -5])
def test_postcondition_fail(value):
    with pytest.raises(EnsureError):
        negative_result(value)
