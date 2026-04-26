from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os
load_dotenv()
class BlogState(TypedDict):
  blog:str
  topic:str
  is_good:bool
  iteration: int


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

def generate_blog(state:BlogState)->BlogState:
  topic=state['topic']
  iteration=state['iteration']
  prompt= f"""
    Write a high-quality blog post on: "{topic}"

    Requirements:
    - Catchy title
    - Introduction
    - Clear subheadings
    - Informative and engaging content
    - Conclusion
    - Friendly tone

    This is iteration {iteration}.
    If previous version was weak, improve depth, clarity, and engagement.
    """
  response =llm.invoke(prompt)
  return {
        **state,
        "blog": response.content,
        "iteration": iteration + 1
    }

def evaluate_blog(state: BlogState) -> BlogState:
    blog = state["blog"]

    prompt = f"""
    Evaluate the following blog:

    {blog}

    Check:
    - Is it engaging?
    - Is it well-structured?
    - Is it informative?

    Reply ONLY with:
    YES or NO
    """

    response = llm.invoke(prompt)
    verdict = response.content.strip().lower()
    print(state["iteration"])
    return {
        **state,
        "is_good": "yes" in verdict
    }


def decide_next(state:BlogState):
  if state['is_good'] or state['iteration']>=3:
    return END
  return "generate"
  
builder=StateGraph(BlogState)
builder.add_node("generate",generate_blog)
builder.add_node("evaluate", evaluate_blog)
builder.set_entry_point("generate")
builder.add_edge("generate", "evaluate")
builder.add_conditional_edges(
    "evaluate",
    decide_next,
    {
        "generate": "generate",
        END: END
    }
)
graph = builder.compile()

if __name__ == "__main__":
    print("\nGraph Structure:\n")
    print(graph.get_graph().draw_ascii())

    topic = input("\nEnter blog topic: ")

    result = graph.invoke({
        "topic": topic,
        "blog": "",
        "is_good": False,
        "iteration": 0
    })

    print("\n📝 Final Blog:\n")
    print(result["blog"])
