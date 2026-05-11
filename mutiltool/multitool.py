from typing import TypedDict,Annotated, List
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import (
    BaseMessage,
    HumanMessage
)
from langchain_google_genai import ChatGoogleGenerativeAI

# Tools
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
@tool
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.
    Example:
    2 + 3 * 10
    """

    try:
        result = eval(expression)
        return f"Result = {result}"

    except Exception as e:
        return f"Error: {str(e)}"

search_tool = TavilySearchResults(
    max_results=2
)
tools = [calculator, search_tool]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: ChatState):

    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


def should_continue(state: ChatState):

    messages = state["messages"]

    last_message = messages[-1]

    # Check tool calls
    if last_message.tool_calls:
        return "tools"

    return END
builder = StateGraph(ChatState)
builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
builder.add_node("tools", tool_node)
builder.set_entry_point("chatbot")
builder.add_conditional_edges(
    "chatbot",
    should_continue
)
builder.add_edge("tools", "chatbot")
graph = builder.compile()

if __name__ == "__main__":

    print("🤖 AI Agent Started")
    print("Type 'exit' to quit\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=user_input)
                ]
            }
        )

        print("\nBot:")
        print(result["messages"][-1].content)
        print("-" * 50)
