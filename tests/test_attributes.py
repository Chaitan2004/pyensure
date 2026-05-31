import pytest

from pyensure import ensure, EnsureError


class User:

    def __init__(self, age):
        self.age = age


@ensure(pre=("user.age >= 18",))
def register(user):
    return True


@pytest.mark.parametrize("age", [18, 20, 65])
def test_attribute_pass(age):
    assert register(User(age)) is True


@pytest.mark.parametrize("age", [0, 16, 17])
def test_attribute_fail(age):
    with pytest.raises(EnsureError):
        register(User(age))
