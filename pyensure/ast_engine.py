import ast
from typing import Any

from .errors import EnsureError


RULE_CACHE: dict[str, ast.AST] = {}


def evaluate(
    rule: str,
    context: dict[str, Any]
) -> bool:
    """
    Parse rule into AST and safely evaluate it.
    """

    if rule not in RULE_CACHE:
        RULE_CACHE[rule] = ast.parse(
            rule,
            mode="eval"
        )

    tree = RULE_CACHE[rule]

    return bool(
        safe_eval(tree, context)
    )


def safe_eval(
    node: ast.AST,
    context: dict[str, Any]
) -> Any:

    # Root expression
    if isinstance(node, ast.Expression):
        return safe_eval(node.body, context)

    # Comparisons: x > 0
    elif isinstance(node, ast.Compare):

        left = safe_eval(node.left, context)
        right = safe_eval(node.comparators[0], context)

        op = node.ops[0]

        if isinstance(op, ast.Gt):
            return left > right

        elif isinstance(op, ast.Lt):
            return left < right

        elif isinstance(op, ast.GtE):
            return left >= right

        elif isinstance(op, ast.LtE):
            return left <= right

        elif isinstance(op, ast.Eq):
            return left == right

        elif isinstance(op, ast.NotEq):
            return left != right

        else:
            raise EnsureError(
                f"Operator not allowed: {type(op).__name__}"
            )

    # Variable names: x
    elif isinstance(node, ast.Name):

        if node.id not in context:
            raise EnsureError(
                f"Unknown variable: {node.id}"
            )

        return context[node.id]

    # Constants: numbers, strings, booleans
    elif isinstance(node, ast.Constant):
        return node.value

    # Object attributes and callable values
    # user.age, user.method
    elif isinstance(node, ast.Attribute):

        obj = safe_eval(node.value, context)

        return getattr(obj, node.attr)

    # Function and method calls
    # is_even(x), user.is_adult()
    elif isinstance(node, ast.Call):

        func = safe_eval(node.func, context)

        args = [
            safe_eval(arg, context)
            for arg in node.args
        ]

        return func(*args)

    # Boolean logic
    # x > 0 and y > 0
    elif isinstance(node, ast.BoolOp):

        if isinstance(node.op, ast.And):

            return all(
                safe_eval(value, context)
                for value in node.values
            )

        elif isinstance(node.op, ast.Or):

            return any(
                safe_eval(value, context)
                for value in node.values
            )

        else:
            raise EnsureError(
                f"Unsupported boolean operator: "
                f"{type(node.op).__name__}"
            )

    # Block everything else
    else:
        raise EnsureError(
            f"Unsupported syntax: {type(node).__name__}"
        )