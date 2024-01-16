# API and Slack notify example

This example contains 2 actions.

First action `get_porssisahko` gets electricity API data from https://api.porssisahko.net

The second action `slack_message` handles posting a message into Slack channel.

# To make the Slack messaging work

- Get a Slack webhook URL from your Slack's `Incoming WebHooks`
- copy `.env.example` to `.env`
- copy your webhook url to `.env` from Slack

# Running actions

## Running action-server locally

To run this use `action-server start`.

You may then check http://localhost:8080 for the Action Server UI.
There you can try the actions `get_porssisahko` and `slack_message` out.

## Running test action test runs

These are defined in the `robot.yaml` file and can be run using `Robocorp Code` VSCode extension.
This example contains two task that can be run to test actions: `Test - Slack` and `Test - Porssisahko`.
The `Test - Slack` can be fed test data using `devdata/input_slack.json` file, where action parameters
are given values.

## Running action as a custom OpenAI GPT Action

You can expose this action to internet with `action-server start --expose`.
Then you may use it in services such as OpenAI GPT Action.

This way both actions can be used as necessary by requesting the GPT for example.

`Get electricity prices and post them to Slack channel "mika-dev"` (both actions are going to be used) or
`Get electricity prices for next four hours` (only `get_porssisahko` is going to be used)
