from queue import Queue, Empty
from threading import Thread

from fastapi import FastAPI
from pydantic import BaseModel

from lada.runner import run_code

app = FastAPI()

output_queue: Queue[str] = Queue()


# Request and Response models for pay_money
class EvaluatePythonRequest(BaseModel):
    code: str


class EvaluatePythonResponse(BaseModel):
    output: str


# Request and Response models for callback
class CallbackRequest(BaseModel):
    action_id: str


TIMEOUT_MESSAGE = "Code execution ongoing; use callback 'ABC123' for results post-completion."


def truncate_output_with_beginning_clue(output: str, max_chars: int = 2000) -> str:
    beginning_clue = "[Cut] "  # A very short clue at the beginning to indicate possible truncation

    if len(output) > max_chars:
        truncated_output = output[:max_chars - len(beginning_clue)]
        chars_missed = len(output) - len(truncated_output)
        truncated_message = f"[+{chars_missed}]"
        return beginning_clue + truncated_output + truncated_message
    else:
        return output


@app.post("/evaluate_python", response_model=EvaluatePythonResponse)
def evaluate_python(request: EvaluatePythonRequest):

    def threaded_run_code():
        try:
            result = run_code(request.code)
        except Exception as e:
            result = str(e)
        output_queue.put(result)

    thread = Thread(target=threaded_run_code)
    thread.start()

    try:
        outs = output_queue.get(timeout=20)
    except Empty:
        return EvaluatePythonResponse(output=TIMEOUT_MESSAGE)
    return EvaluatePythonResponse(output=truncate_output_with_beginning_clue(outs))


@app.post("/callback", response_model=EvaluatePythonResponse)
def callback(request: CallbackRequest):
    try:
        outs = output_queue.get(timeout=20)
    except Empty:
        return EvaluatePythonResponse(output=TIMEOUT_MESSAGE)
    return EvaluatePythonResponse(output=truncate_output_with_beginning_clue(outs))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=60000)
