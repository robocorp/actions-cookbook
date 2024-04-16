# Secret example

Starting with robocorp-actions 0.2.0, it is possible to define and read secrets in actions.

Check out the [robocorp-actions guide](https://github.com/robocorp/robocorp/blob/master/action_server/docs/guides/07-secrets.md) for more information.

To run this use `action-server start`.

You may then check http://localhost:8080 for the Action Server UI.
There you can try the action `print_request` out.

You can expose this action to internet with `action-server start --expose`.
Then you may use it in services such as OpenAI GPT Action.