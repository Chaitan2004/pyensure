# pyensure

[![PyPI version](https://img.shields.io/pypi/v/pyensure-core)](https://pypi.org/project/pyensure-core/)
[![Python](https://img.shields.io/pypi/pyversions/pyensure-core)](https://pypi.org/project/pyensure-core/)
[![License](https://img.shields.io/pypi/l/pyensure-core)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen)](#testing)
[![Type Hints](https://img.shields.io/badge/type--hints-supported-blue)](#)
[![Async Support](https://img.shields.io/badge/async-supported-success)](#)
[![AST Powered](https://img.shields.io/badge/AST-powered-orange)](#)

Lightweight Design by Contract for Python with preconditions, postconditions, async support, rule caching, and AST-powered validation.

**Write contracts, not validation boilerplate.**

`pyensure` helps you define runtime contracts for Python functions using a clean decorator-based API.

Instead of scattering validation logic throughout your codebase, define expectations declaratively.

```python
from pyensure import ensure

@ensure(
    pre=("amount > 0",)
)
def withdraw(amount):
    return amount
```

---

# Installation

```bash
pip install pyensure-core
```

# Import

```python
from pyensure import ensure
from pyensure import EnsureError
```

> Package name on PyPI: `pyensure-core`
>
> Import name in Python: `pyensure`

---

# Why pyensure?

As applications grow, validation logic often becomes mixed with business logic:

```python
def withdraw(user, amount):

    if amount <= 0:
        raise ValueError("Amount must be positive")

    if user.balance < amount:
        raise ValueError("Insufficient balance")

    # business logic
```

With `pyensure`:

```python
@ensure(
    pre=(
        "amount > 0",
        "user.balance >= amount"
    )
)
def withdraw(user, amount):

    # business logic
    ...
```

This keeps contracts separate from implementation and makes intent immediately visible.

---

# Features

## Preconditions

Validate function inputs before execution.

```python
from pyensure import ensure

@ensure(
    pre=("x > 0",)
)
def add_one(x):
    return x + 1
```

---

## Postconditions

Validate results after execution.

```python
@ensure(
    post=("result > 0",)
)
def generate_score():
    return 10
```

The function result is automatically exposed as:

```python
result
```

inside post-condition expressions.

---

## Attribute Access

Access object attributes directly.

```python
@ensure(
    pre=("user.age >= 18",)
)
def register(user):
    return True
```

---

## Function Calls

Use helper functions directly inside rules.

```python
def is_even(x):
    return x % 2 == 0

@ensure(
    pre=("is_even(user_id)",)
)
def process(user_id):
    return user_id
```

Functions defined in the decorated function's module are automatically available.

No registration required.

---

## Method Calls

Use instance methods inside rules.

```python
class User:

    def get_age(self):
        return 25

@ensure(
    pre=("user.get_age() >= 18",)
)
def register(user):
    return True
```

---

## Boolean Expressions

### AND

```python
@ensure(
    pre=("x > 0 and y > 0",)
)
def add(x, y):
    return x + y
```

### OR

```python
@ensure(
    pre=("user.is_admin or user.age >= 18",)
)
def access(user):
    return True
```

---

## Async Support

Works with both synchronous and asynchronous functions.

```python
@ensure(
    pre=("user.age >= 18",)
)
async def create_user(user):
    return user
```

```python
user = User()

await create_user(user)
```

---

## Runtime Contract Control

Disable all contract checks globally when needed.

```python
from pyensure import disable, enable

disable()

# contracts are skipped
withdraw(-100)

enable()
```

Useful for:

* benchmarking
* performance testing
* temporary contract suspension

---

## AST-Based Rule Evaluation

Rules are parsed using Python's Abstract Syntax Tree (AST).

Benefits:

* Controlled rule evaluation
* Clear validation boundaries
* Custom error handling
* Extensible architecture
* No direct use of `eval()`

---

## Rule Caching

Parsed AST trees are cached internally.

Benefits:

* Faster repeated evaluations
* Avoids reparsing the same rule
* Lower runtime overhead

---

## Type Hints

The library is fully typed.

Benefits:

* IDE autocomplete
* Static analysis
* Better maintainability
* Improved developer experience

---

## Custom Exceptions

All contract-related failures raise:

```python
from pyensure import EnsureError
```

Example:

```python
try:
    withdraw(-100)

except EnsureError as e:
    print(e)
```

---

# How It Works

```text
Decorator
    ↓
Build Context
    ↓
Parse / Cache AST
    ↓
Evaluate Preconditions
    ↓
Execute Function
    ↓
Evaluate Postconditions
```

Rules are parsed into Python AST nodes and evaluated against the function context.

The return value of the decorated function is automatically exposed as:

```python
result
```

for post-condition validation.

---

# Quick Start

```python
from pyensure import ensure

@ensure(
    pre=("x > 0",),
    post=("result > x",)
)
def add_one(x):
    return x + 1

print(add_one(5))
```

Output:

```text
6
```

---

# Supported Syntax

## Comparisons

```python
x > 0
x < 0
x >= 0
x <= 0
x == 0
x != 0
```

## Attributes

```python
user.age
user.balance
```

## Function Calls

```python
is_even(x)
validate_email(email)
```

## Method Calls

```python
user.get_age()
user.is_active()
```

## Boolean Operators

```python
x > 0 and y > 0

x > 0 or y > 0
```

## Constants

```python
10
"hello"
True
False
```

---

# Limitations

## Chained Comparisons Are Not Supported

The following is NOT supported:

```python
1 < x < 10
```

Instead write:

```python
x > 1 and x < 10
```

---

## Single Rule Syntax

For a single rule, use:

```python
@ensure(pre=("x > 0",))
```

or

```python
@ensure(pre=["x > 0"])
```

Remember the trailing comma for single-element tuples.

Incorrect:

```python
@ensure(pre=("x > 0"))
```

This is interpreted as a string, not a tuple.

---

## Unsupported Python Syntax

The following are intentionally unsupported:

```python
[x for x in items]
```

```python
lambda x: x + 1
```

```python
{x: y}
```

and other advanced Python constructs.

`pyensure` focuses on runtime contracts rather than executing arbitrary Python code.

---

# Example: Business Rule Validation

```python
class User:

    def __init__(self, balance):
        self.balance = balance


@ensure(
    pre=(
        "amount > 0",
        "user.balance >= amount"
    ),
    post=("result == True",)
)
def withdraw(user, amount):

    user.balance -= amount

    return True
```

---

# Testing

Current test status:

```text
20 passed
```

Covered functionality:

* Preconditions
* Postconditions
* Attributes
* Function calls
* Method calls
* Boolean operators
* Async support
* Global enable/disable
* AST evaluation
* Error handling
* Rule caching

---

# Design Goals

* Simple API
* Minimal dependencies
* Readable contracts
* Runtime validation
* Async-friendly
* Production-ready
* Easy integration into existing codebases

---

# License

MIT License

---

# Roadmap

Future improvements may include:

* Enhanced error introspection
* Rich contract failure diagnostics
* Additional AST node support
* Advanced configuration options
* Contract reporting and debugging tools
