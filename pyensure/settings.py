CONTRACTS_ENABLED: bool = True


def enable() -> None:
    global CONTRACTS_ENABLED
    CONTRACTS_ENABLED = True


def disable() -> None:
    global CONTRACTS_ENABLED
    CONTRACTS_ENABLED = False