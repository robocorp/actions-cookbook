from sema4ai.actions import action, Secret


@action
def greet_with_secret(name: str, secret_message: Secret) -> str:
    """
    Greets user with a secret message

    Args:
        name (str): Name of the user

    Returns:
        str: Returns a greeting with a secret message
    """
    return f"Hello {name}, the secret message is {secret_message.value}"
