"""
A simple AI Action template for comparing timezones

Please checkout the base guidance on AI Actions in our main repository readme:
https://github.com/robocorp/robocorp/blob/master/README.md

"""

from robocorp.actions import action
from datetime import datetime
import pytz
import requests

JOKES_API_URL = "https://icanhazdadjoke.com/"

@action
def compare_time_zones(user_timezone: str, compare_to_timezones: str) -> str:
    """
    Compares user timezone time difference to given timezones

    Args:
        user_timezone (str): User timezone in tz database format. Example: "Europe/Helsinki"
        compare_to_timezones (str): Comma seperated timezones in tz database format. Example: "America/New_York, Asia/Kolkata"

    Returns:
        str: List of requested timezones, their current time and the user time difference in hours
    """
    output: list[str] = []

    try:
        user_tz = pytz.timezone(user_timezone)
        user_now = datetime.now(user_tz)
    except pytz.InvalidTimeError:
        return f"Timezone '{user_timezone}' could not be found. Use tz database format."
    
    output.append(f"- Current time in {user_timezone} is {user_now.strftime('%I:%M %p')}")

    target_timezones = [s.strip() for s in compare_to_timezones.split(',')]
    for timezone in target_timezones:
        try:
            target_tz = pytz.timezone(timezone)
            target_now = datetime.now(target_tz)
            time_diff = (int(user_now.strftime('%z')) - int(target_now.strftime('%z'))) / 100

            output.append(f"- Current time in {timezone} is {target_now.strftime('%I:%M %p')}, the difference with {user_timezone} is {time_diff} hours")
        except pytz.InvalidTimeError:
            output.append(f"- Timezone '{timezone}' could not be found. Use tz database format.")

    # Pretty print for log
    print("\n".join(output))
    
    return "\n".join(output)


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

    resp = requests.get(JOKES_API_URL, headers=headers)
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

    url = f"{JOKES_API_URL}/search?term={term}&page={0}&limit={5}"
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