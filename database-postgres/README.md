# Example: Actions - Make queries to Postgres database

This example gets you started in creating Actions for [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme).

`Actions` and `Action Server` enable you to "give your AI Agents hands" meaning that your AI/LLM Agent can help your users perform distinct actions that get executed based on the LLM discussion.

The example shows how to let your LLM app (like custom GPT) access a Postgres database, but only with queries that you have determined.

## What does this example Action do?

This has four Actions:
1. List customers by first name
2. List customers latest rental transactions
3. List availabitilty of a movie in different stores by the title
4. Update customers email address

Actions 1-3 are configured to be `is_consequential=False`, which means that when used with OpenAI custom GPTs, the user can allow the actions to run without explicit permission request every time. The last action that has a consequence on the actual data, is set to always require user consent to run.

## Quickstart

👉 Follow the Action Server [Quickstart guide](https://github.com/robocorp/robocorp?tab=readme-ov-file#%EF%B8%8F-quickstart) in the main repository.

👉 Set up your local Postgres server and set it up with the [DVD Rental example data](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/). Follow the instructions from the given site.


## Dependency management

We recommend placing your dependencies in [conda.yaml](conda.yaml).

👉 More on [managing your dependencies](https://github.com/robocorp/robocorp?tab=readme-ov-file#what-makes-a-python-function-an-%EF%B8%8Faction) in the main repository.


## Actions in VS Code

👉 Using [Robocorp Code extension for VS Code](https://marketplace.visualstudio.com/items?itemName=robocorp.robocorp-code), you can get everything set up and running in VS Code in no time.

The template has a few files that enable the extension to find and set up your action environment and provide code completion. There is also a side panel where we have and will add some easy-to-use functionalities.

When debugging your Actions Python code, you probably do not want to give the inputs every time you run and always be running the Action Server, so you can set your test inputs in [devdata](./devdata) folder and just run/debug your Python code.


🚀 Now, go get'em

