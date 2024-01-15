import requests
from robocorp.actions import action

SERVER_URL = "http://localhost:60000"


@action
def evaluate_python(code: str) -> str:
    """Execute a Python command in a REPL environment.

    This action takes a string representing a Python code, executes it, and returns the output.

    Args:
        code (str): The Python code to execute.

    Returns:
        str: The output from executing the command.
    """
    response = requests.post(f"{SERVER_URL}/evaluate_python", json={"code": code})
    return response.json()["output"]


@action
def callback(action_id: str) -> str:
    """Use this to check if a given evaluate_python action has been done
    Args:
        action_id (str): id given in original action result for callback

    Returns:
        str: The output from execution.
    """
    response = requests.post(f"{SERVER_URL}/callback", json={"action_id": action_id,})
    return response.json()["output"]