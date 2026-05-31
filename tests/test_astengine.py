import pytest

from pyensure.ast_engine import evaluate
from pyensure import EnsureError


@pytest.mark.parametrize(
    ("rule", "context", "expected"),
    [
        ("x > 0", {"x": 5}, True),
        ("x > 0", {"x": 0}, False),
        ('status == "success"', {"status": "success"}, True),
        ('status != "failed"', {"status": "success"}, True),
    ]
)
def test_evaluate_compare(rule, context, expected):
    assert evaluate(rule, context) is expected


@pytest.mark.parametrize("rule", ["abc > 0", "missing == 1"])
def test_unknown_variable(rule):
    with pytest.raises(EnsureError):
        evaluate(rule, {})


@pytest.mark.parametrize(
    ("rule", "context"),
    [
        ("[x for x in items]", {"items": [1, 2, 3]}),
        ("x + 1", {"x": 1}),
    ]
)
def test_unsupported_syntax(rule, context):
    with pytest.raises(EnsureError):
        evaluate(rule, context)
