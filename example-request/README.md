# Request example

Starting with robocorp-actions 0.1.0, it's possible to collect data from the received request by creating a request: Request argument.

The data currently available in the request is:

headers: contains all the headers received.
cookies: contains all the cookies received in headers in a dict-like API.

Check out [robocorp-actions guide](https://github.com/robocorp/robocorp/blob/master/actions/docs/guides/00-request.md) for more information.

To run this use `action-server start`.

You may then check http://localhost:8080 for the Action Server UI.
There you can try the action `print_request` out.

You can expose this action to internet with `action-server start --expose`.
Then you may use it in services such as OpenAI GPT Action.
