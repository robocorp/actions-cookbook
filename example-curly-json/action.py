import json

from robocorp.actions import action
import requests
import shlex
import jmespath
from datetime import datetime


def curl_to_request(command: str) -> requests.Response:
    # Split the cURL command into parts
    parts = shlex.split(command)

    # Initial values
    method = 'GET'
    headers = {}
    data = None
    json_data = None
    url = ''

    # Parse the cURL command
    for i in range(len(parts)):
        if parts[i] == 'curl':
            continue
        elif parts[i].startswith('http'):
            url = parts[i]
        elif parts[i] == '-X' or parts[i] == '--request':
            method = parts[i + 1].upper()
        elif parts[i] in ['-H', '--header']:
            header = parts[i + 1].split(':', 1)
            headers[header[0].strip()] = header[1].strip()
        elif parts[i] in ['-d', '--data']:
            data = parts[i + 1]
        elif parts[i] in ['-j', '--json']:
            json_data = parts[i + 1]

    # Making the request
    if method == 'GET':
        result = requests.get(url, headers=headers)
    elif method == 'POST':
        if json_data:
            result = requests.post(url, headers=headers, json=json_data)
        else:
            result = requests.post(url, headers=headers, data=data)
    # Add other methods as needed
    else:
        raise ValueError(f"HTTP method {method} not supported.")

    return result


def truncate_output_with_beginning_clue(output: str, max_chars: int = 2000) -> str:
    beginning_clue = "[Cut] "  # A very short clue at the beginning to indicate possible truncation

    if len(output) > max_chars:
        truncated_output = output[:max_chars - len(beginning_clue)]
        chars_missed = len(output) - len(truncated_output)
        truncated_message = f"[+{chars_missed}]"
        return beginning_clue + truncated_output + truncated_message
    else:
        return output


@action
def curl_command(command: str) -> str:
    """
    Executes a cURL command and returns a truncated JSON response.
    Only supports GET and POST methods and assumes the response is in JSON format.

    Args:
        command (str): A valid cURL command string.
                      Example: "curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"value\"}' http://example.com"

    Returns:
        str: SON response from the HTTP request, truncated if over 2000 characters.
    """
    data = curl_to_request(command).json()
    with open("response.json", "w") as f:
        json.dump(data, f, indent=4)
    return truncate_output_with_beginning_clue(str(data))


@action
def jmespath_search(query: str) -> str:
    """
    Executes a JMESPath query on the JSON data stored by last curl_command.

    Args:
        query (str): A valid JMESPath query string.
                     Example: "people[?age > `30`].name"

    Returns:
        str: The result of the JMESPath query, truncated if over 2000 characters.
    """
    with open("response.json", "r") as f:
        json_data = json.load(f)

    result = jmespath.search(query, json_data)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"jmespath_result_{timestamp}.json"

    output_data = {
        "query": query,
        "result": result
    }

    with open(filename, "w") as f:
        json.dump(output_data, f, indent=4)

    return truncate_output_with_beginning_clue(str(result))