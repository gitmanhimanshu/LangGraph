from typing import TypedDict
from langgraph.graph import StateGraph, END
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

class BlogState(TypedDict):
    topic:str
    blog:str

llm=ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0.7
)
def generateblog(state:BlogState)->BlogState:
    topic=state['topic']
    prompt=f"""
    Write a detailed, engaging blog post on the topic: "{topic}".

    Requirements:
    - Catchy title
    - Introduction
    - Subheadings
    - Informative content
    - Conclusion
    - Friendly tone
    """
    response=llm.invoke(prompt)
    return {
        "topic":topic,
        "blog":response.content
    }
builder=StateGraph(BlogState)
builder.add_node('blog_generator',generateblog)
builder.set_entry_point('blog_generator')
builder.add_edge('blog_generator',END)
graph=builder.compile()
if __name__ == "__main__":
    print(graph.get_graph().draw_ascii())
    user_input = input("Enter blog topic: ")

    result = graph.invoke({
        "topic": user_input,
        "blog": ""
    })
    

    print("\n📝 Generated Blog:\n")
    print(result["blog"])
