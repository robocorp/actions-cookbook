import requests
from robocorp.actions import action

API_URL = "https://icanhazdadjoke.com/"

@action
def get_a_random_joke() -> str:
    """Returns a random joke

    Returns:
        str: A random joke
    """
    headers = {
        "Accept": "application/json",
        "User-Agent": "My FastAPI app (https://myapp.com/contact)",
    }

    resp = requests.get(API_URL, headers=headers)
    data = resp.json()
    return data["joke"]


@action
def search_jokes(term: str) -> str:
    """Finds jokes for a given term.

    Args:
        term (str): A term to create a joke about. Use only single words, no sentences.

    Returns:
        str: A joke
    """

    url = f"{API_URL}/search?term={term}&page={0}&limit={5}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "My FastAPI app (https://myapp.com/contact)",
    }

    resp = requests.get(url, headers=headers)
    data = resp.json()

    return_string = ""

    for joke in data["results"]:
        return_string += f"{joke['joke']}\n"
        return_string += "\n---\n\n"
    return return_string
