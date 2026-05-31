import pytest

from pyensure import ensure, EnsureError


@ensure(pre=("x > 0",))
async def add_one(x):
    return x + 1


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1, 2),
        (5, 6),
        (20, 21),
    ]
)
@pytest.mark.asyncio
async def test_async_pass(value, expected):
    result = await add_one(value)
    assert result == expected


@pytest.mark.parametrize("value", [0, -1, -10])
@pytest.mark.asyncio
async def test_async_fail(value):
    with pytest.raises(EnsureError):
        await add_one(value)
