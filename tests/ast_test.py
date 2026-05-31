import pytest

from pyensure import EnsureError
from pyensure.ast_engine import evaluate


class User:
    def __init__(self, age):
        self.age = age


@pytest.mark.parametrize(
    ("rule", "context", "expected"),
    [
        ("a > 0", {"a": 5}, True),
        ("a > 0", {"a": -1}, False),
        ('status == "success"', {"status": "success"}, True),
        ('status == "success"', {"status": "failed"}, False),
        ("user.age > 18", {"user": User(21)}, True),
        ("user.age > 18", {"user": User(17)}, False),
    ]
)
def test_evaluate_values(rule, context, expected):
    assert evaluate(rule, context) is expected


@pytest.mark.parametrize("rule", ["missing > 0", "user.height > 100"])
def test_evaluate_errors(rule):
    with pytest.raises((EnsureError, AttributeError)):
        evaluate(rule, {"user": User(17)})
