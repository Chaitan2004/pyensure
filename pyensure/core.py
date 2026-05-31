import inspect
from functools import wraps
from typing import Any, Callable

from .ast_engine import evaluate
from .errors import EnsureError
from . import settings


def _format_context(context: dict[str, Any]) -> str:
    return ", ".join(
        f"{k}={v}"
        for k, v in context.items()
    )


def ensure(
    pre: tuple[str, ...] | list[str] = (),
    post: tuple[str, ...] | list[str] = ()
) -> Callable:

    def decorator(fn: Callable) -> Callable:

        allowed_globals: dict[str, Any] = {
            name: value
            for name, value in fn.__globals__.items()
            if callable(value)
            and not name.startswith("__")
        }

        async def _run_async(
            *args: Any,
            **kwargs: Any
        ) -> Any:

            if not settings.CONTRACTS_ENABLED:
                return await fn(*args, **kwargs)

            sig = inspect.signature(fn)

            bound = sig.bind(*args, **kwargs)

            bound.apply_defaults()

            context: dict[str, Any] = dict(
                bound.arguments
            )

            context.update(allowed_globals)

            # PRE conditions
            for rule in pre:

                if not evaluate(rule, context):

                    raise EnsureError(
                        (
                            f"Pre-condition failed: "
                            f"{rule}\n"
                            f"Context: "
                            f"{_format_context(context)}"
                        ),
                        rule=rule,
                        context=context
                    )

            result = await fn(*args, **kwargs)

            context["result"] = result

            # POST conditions
            for rule in post:

                if not evaluate(rule, context):

                    raise EnsureError(
                        (
                            f"Post-condition failed: "
                            f"{rule}\n"
                            f"Context: "
                            f"{_format_context(context)}"
                        ),
                        rule=rule,
                        context=context
                    )

            return result

        def _run_sync(
            *args: Any,
            **kwargs: Any
        ) -> Any:

            if not settings.CONTRACTS_ENABLED:
                return fn(*args, **kwargs)

            sig = inspect.signature(fn)

            bound = sig.bind(*args, **kwargs)

            bound.apply_defaults()

            context: dict[str, Any] = dict(
                bound.arguments
            )

            context.update(allowed_globals)

            # PRE conditions
            for rule in pre:

                if not evaluate(rule, context):

                    raise EnsureError(
                        (
                            f"Pre-condition failed: "
                            f"{rule}\n"
                            f"Context: "
                            f"{_format_context(context)}"
                        ),
                        rule=rule,
                        context=context
                    )

            result = fn(*args, **kwargs)

            context["result"] = result

            # POST conditions
            for rule in post:

                if not evaluate(rule, context):

                    raise EnsureError(
                        (
                            f"Post-condition failed: "
                            f"{rule}\n"
                            f"Context: "
                            f"{_format_context(context)}"
                        ),
                        rule=rule,
                        context=context
                    )

            return result

        if inspect.iscoroutinefunction(fn):

            @wraps(fn)
            async def async_wrapper(
                *args: Any,
                **kwargs: Any
            ) -> Any:
                return await _run_async(
                    *args,
                    **kwargs
                )

            return async_wrapper

        @wraps(fn)
        def wrapper(
            *args: Any,
            **kwargs: Any
        ) -> Any:
            return _run_sync(
                *args,
                **kwargs
            )

        return wrapper

    return decorator