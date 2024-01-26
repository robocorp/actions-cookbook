# Word guessing game example

This is a simple word guessing game with global highscores running with [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) and using OpenAI locally to handle the game mechanics.

Note that there is no strict user authentication, the user is only asked for an username by the AI agent.

## Quickstart

You will need an [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key) to get started quickly. Set it in the `.env` file:

```shell
OPENAI_API_KEY=XXXXXX
```

Start the game by staring action server:

```shell
action-server start --expose
```
