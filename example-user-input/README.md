# Concept Example of a greeter with user input

To run this use `poetry run python server.py` and 
then under actions `action-server start`.

You may then check http://localhost:8080 for the Action Server UI.
There you can try the action `greet` out.

You can expose this action to internet with `action-server start --expose`.
Then you may use it in services such as OpenAI GPT Action.

Target for this concept is to allow following user input during action execution:
```python
@action
def greeter(name: str) -> str:
    place = request_input(f"Ask from the user: Where are you from {name}?")
    return f"Hello {name} from {place}!"
```

If this is awesome in your opinion, voice it at https://github.com/robocorp/robocorp/issues/174.
