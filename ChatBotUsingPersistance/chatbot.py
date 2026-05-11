from typing import TypedDict,Annotated,List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)
def chat_node(state: ChatState)->ChatState:
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages": [response]   
    }
builder = StateGraph(ChatState)
builder.add_node("chat", chat_node)
builder.set_entry_point("chat")
builder.add_edge("chat", END)
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
if __name__ == "__main__":
    print("💬 Gemini Chatbot (type 'exit' to quit)\n")

    thread_id = "user_1"   # same thread = memory persist

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        result = graph.invoke(
            {
                "messages": [HumanMessage(content=user_input)]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )
        print(result)
        print("Bot:", result["messages"][-1].content)