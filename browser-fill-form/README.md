# Fill in forms with Playwright

This recipe shows how to use [robocorp.browser](https://robocorp.com/docs/python/robocorp/robocorp-browser) (Playwright) for filling online forms. Some of the key aspects to learn from this example are:

1. Using Pydantic models to define input data

A [custom input data model](https://github.com/robocorp/robocorp/blob/master/action_server/docs/guides/04-custom-data.md) is defined as a class using Pydantic, an addition to robocorp.actions since 0.0.8 version.

```python
class Prospect(BaseModel):
  first_name: Annotated[str, Field(description="User's first name")]
  last_name: Annotated[str, Field(description="User's last name")]
  company_name: Annotated[str, Field(description="Company name")]
  email: Annotated[str, Field(description="User's email address")]
  phone: Annotated[str, Field(description="User's phone number, use international format.")]
    

@action(is_consequential="False")
def fill_form_with_user_data(data: Prospect) -> str:
  """
  Fill in Robocorp Contact form with user details using a browser.

  Args:
    data: A person object that will be entered to the Robocorp Contact form.

  Returns:
    str: True if operation was success, and False if it failed, including an error message.

  """
  # here be dragons
```

Note that when using the Annotated type, the natural language descriptions of the fields are defined within the class, not in each separate `@action`'s docstrings. This way you'll only need to describe them once, and reuse the same class in all your actions. As a reminder, these descriptions are vital for the LLM to understand how to call your Actions.

2. Browser in headless (or not)

This example by default opens the browser in a "visible" mode, so `headless=False`.

```python
browser.configure(
  browser_engine="chromium",
  screenshot="only-on-failure",
  headless=False,
)
```

This way it's easy to see what happens in the browser when testing things out. The browser window will pop up on your laptop when running the Action Server locally. For production use, it's however recommended to switch to headless mode as there is no one to watch the browser in real time.

**Tip!** Add `slowmo=100` in your browser configuration to slow down interactions when testing things. It'll be easier to see with your own eyes what's happening. That value `100` is time in milliseconds between each interaction.

## Running the actions

When ready with your code, just follow the [instruction for serving the Actions with Action Server](https://github.com/robocorp/robocorp/blob/master/action_server/docs/guides/00-startup-command-line.md). To get them usable for example for a Custom GPT from your local machine, it's just this:

```bash
action-server start --expose
```

Head over to our Youtube channel for a [video](https://www.youtube.com/watch?v=7aq6QDCaUmA) how AI Actions and Custom GPTs play together nicely!