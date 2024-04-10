# Template: Python - Actions

This template gets you started in creating Actions for [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme).

`Actions` and `Action Server` enable you to "give your AI Agents hands" meaning that your AI/LLM Agent can help your users perform distinct actions that get executed based on the LLM discussion.

## Quickstart

👉 Follow the Action Server [Quickstart guide](https://github.com/robocorp/robocorp?tab=readme-ov-file#%EF%B8%8F-quickstart) in the main repository.


## Dependency management

Dependencies need to be added to [`package.yaml`](package.yaml).

👉 [package.yaml documentation](https://github.com/robocorp/robocorp/blob/master/action_server/docs/guides/01-package-yaml.md) in the main repository.

## Actions in VS Code 

👉 Using [Robocorp Code extension for VS Code](https://marketplace.visualstudio.com/items?itemName=robocorp.robocorp-code), you can get everything set up and running in VS Code in no time.

The template has a few files that enable the extension to find and set up your action environment and provide code completion. There is also a side panel where we have and will add some easy-to-use functionalities.

![](docs/vscode.png)

When debugging your Actions Python code, you probably do not want to give the inputs every time you run and always be running the Action Server. `Robocorp Code` integration allows you to run and debug actions from within VSCode, enabling custom input to be specified as `.json` files.


## What does the template Action do?

The template is a simple starting point to show how to get started.

The action enables you to get the timezone differences between locations.

We use [pytz](https://pypi.org/project/pytz/) as an example to show that you can leverage the whole Python ecosystem. Robocorp provides a [bunch of libraries](https://pypi.org/search/?q=robocorp-); you can make your own. The sky is the limit.

🚀 Now, go get'em

