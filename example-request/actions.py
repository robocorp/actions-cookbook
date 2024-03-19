from typing import Optional
from robocorp.actions import action, Request


@action
def print_request(request: Request) -> str:
    """
    Prints passed in headers and cookies from the request
    """

    headers: Optional[str] = request.headers
    cookies: Optional[str] = request.cookies

    for key in headers:
        print(f"🐤 {key}: {headers[key]}")

    for key in cookies:
        print(f"🍪 {key}: {cookies[key]}")

    return "Hello"
