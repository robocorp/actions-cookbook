from robocorp.actions import action
from langchain.llms import Ollama

ollama = Ollama(base_url='http://localhost:11434',
                model="mistral")

@action
def chat(question: str) -> str:
    """Chat with Mistral LLM.

    Args:
        question (str): Your question.

    Returns:
        str: Answer from Mistral.
    """
    return ollama(question)
