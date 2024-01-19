from queue import Queue
from threading import Thread
from typing import Tuple

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

output_queue: Queue[Tuple[str, str, str]] = Queue()
input_queue: Queue[Tuple[str, str]] = Queue()


# Request and Response models for pay_money
class GreetingRequest(BaseModel):
    name: str


# Request and Response models for callback
class CallbackRequest(BaseModel):
    action_id: str
    payload: str


class Response(BaseModel):
    output: str


def request_input(query: str) -> str:
    output_queue.put(("input", "id123", query))
    return input_queue.get()[1]


# FUTURE @action
def greeter(name: str) -> str:
    place = request_input(f"Ask from the user: Where are you from {name}?")
    return f"Hello {name} from {place}!"


# Define the /pay_money endpoint
@app.post("/greeter", response_model=Response)
def pay_money(request: GreetingRequest):
    def threaded_pay_money():
        result = greeter(request.name)
        output_queue.put(("result", "id123", result))

    # Spin a new thread for the magic pay money operation
    thread = Thread(target=threaded_pay_money)
    thread.start()

    outs = output_queue.get()
    if outs[0] == "input":
        return Response(output=f"Input required: {outs[2]}. Send response as callback payload with action_id {outs[1]}")
    return Response(output=outs[2])


# Define the /callback endpoint
@app.post("/callback", response_model=Response)
def callback(request: CallbackRequest):
    input_queue.put((request.action_id, request.payload))
    outs = output_queue.get()
    if outs[0] == "input":
        return Response(output=f"Input required: {outs[2]}. Send response as callback payload with action_id {outs[1]}")
    return Response(output=outs[2])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=60000)