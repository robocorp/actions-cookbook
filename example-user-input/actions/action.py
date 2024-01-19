import requests
from robocorp.actions import action

SERVER_URL = "http://localhost:60000"


@action
def greeter(name: str) -> str:
    """Produces an excellent greeting for the given person.

    Args:
        name (str): Name of the person to greet.

    Returns:
        str: An excellent greeting
    """
    response = requests.post(f"{SERVER_URL}/greeter", json={"name": name})
    return response.json()["output"]


@action
def callback(action_id: str, payload: str) -> str:
    """Use this to check if a given greeter action has been done or give additional input.

    Args:
        action_id (str): id given in original action result for callback
        payload (str): action payload input

    Returns:
        str: The output from execution.
    """
    response = requests.post(f"{SERVER_URL}/callback", json={"action_id": action_id, "payload": payload})
    return response.json()["output"]