from sema4ai.actions import action


@action
def greet(name: str) -> str:
    """Produces an excellent greeting for the given person

    Args:
        name (str): Name of the person to greet.

    Returns:
        str: An excellent greeting
    """
    return f"Hello {name}!"
