from robocorp.actions import action

import json
from dotenv import load_dotenv

from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_robocorp import ActionServerToolkit

load_dotenv()

@action
def chat_completion(messages: str) -> str:
    """
    Chatbot completion endpoint used by the playground chatbot.
    Should not be used as a tool by itself.

    Args:
        messages (str): Stringified cha message history and input to the AI

    Returns:
        str: Returned AI completion response
    """

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    toolkit = ActionServerToolkit(url="http://localhost:8080", report_trace=True)
    tools = toolkit.get_tools()

    prompt = hub.pull("hwchase17/structured-chat-agent")
    agent = create_structured_chat_agent(llm, tools, prompt)

    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    input = messages_to_input(messages)
    response = executor.invoke(input)

    return response["output"]

def messages_to_input(messages: str):
    messages_json = json.loads(messages)

    output = {
        "input": messages_json["input"],
        "chat_history": [],
    }

    for message in messages_json["messages"]:
        if message["role"] == "user":
            output["chat_history"].append(HumanMessage(content=message["content"]))
        else:
            output["chat_history"].append(AIMessage(content=message["content"]))

    return output
