import pytest

from pyensure import ensure, EnsureError


class User:

    def __init__(self, age):
        self.age = age

    def get_age(self):
        return self.age


@ensure(pre=("user.get_age() >= 18",))
def register(user):
    return True


@pytest.mark.parametrize("age", [18, 20, 40])
def test_method_call_pass(age):
    assert register(User(age)) is True


@pytest.mark.parametrize("age", [10, 15, 17])
def test_method_call_fail(age):
    with pytest.raises(EnsureError):
        register(User(age))
