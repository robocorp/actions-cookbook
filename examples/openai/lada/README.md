# Local Advanced Data Analysis (LADA)

A Python Notebook environment running on local machine
that you may connect to OpenAI GPT as an [Action](https://platform.openai.com/docs/actions/introduction/what-is-an-action-in-a-gpt).

Why LADA :car: ?:
 * Use as Large Data Files as you want (it is on your own machine, OpenAI has strict limits that people have been hitting)
 * Process as long time as you need (allows process to run as long as needed - OpenAI has about 30 second evaluation time)
 * Any custom tools and or custom data sources, including access to internet (Install what you need, it is your environment)

![](lada.jpg)

# Make it run

To make this run.
You need to have [Poetry](https://python-poetry.org/) and [Robocorp Action Server](https://github.com/robocorp/robocorp/tree/master/action_server).

On a terminal
```
poetry install
poetry run python -m lada.server
```

On another terminal
```
cd actions
action-server start --expose
```

# To make the image expose work

- Register to [ImageKit](https://imagekit.io/)
- copy `.env.example` to `.env`
- copy your ImageKit keys to `.env` from imagekit

# To install additional packages

```poetry add YOUR_PACKAGE```