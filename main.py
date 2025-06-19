import logging

logging.getLogger().setLevel(logging.WARNING)

from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import datetime
import re

load_dotenv()

class BasicChatBot(TypedDict):
    messages: Annotated[list, add_messages]

def get_system_time(format: str = "%Y-%m-%dT%H:%M:%SZ") -> dict:
    now = datetime.datetime.now(datetime.timezone.utc)
    return {"utc": now.strftime(format)}

import difflib

def user_asked_for_time(message: str) -> bool:
    message = message.lower().strip()

    target_phrases = [
        "what time is it",
        "what's the time",
        "what is the time",
        "whats the time"
    ]

    message = re.sub(r"[^\w\s]", "", message)

    for phrase in target_phrases:
        similarity = difflib.SequenceMatcher(None, message, phrase).ratio()
        if similarity >= 0.85:
            return True

    return False


llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

def chatbot(state: BasicChatBot):
    user_msg = state["messages"][-1].content

    if user_asked_for_time(user_msg):
        time_info = get_system_time()
        return {"messages": [AIMessage(content=f'{{"utc": "{time_info["utc"]}"}}')]}
    else:
        ai_response = llm.invoke(state["messages"])
        return {"messages": [ai_response]}

graph = StateGraph(BasicChatBot)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.set_finish_point("chatbot")

app = graph.compile()

print("Hi!, ask me a question")

while True:
    user_input = input("> ")
    if user_input.strip().lower() in ["exit", "end", "quit"]:
        break

    result = app.invoke({"messages": [HumanMessage(content=user_input)]})

    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            print(msg.content)
