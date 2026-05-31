from typing import Any


class EnsureError(Exception):

    def __init__(
        self,
        message: str,
        rule: str | None = None,
        context: dict[str, Any] | None = None
    ) -> None:

        super().__init__(message)

        self.rule: str | None = rule

        self.context: dict[str, Any] = (
            context or {}
        )
