from typing import TypedDict
from langgraph.graph import StateGraph
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def generate_advice(state: 'State'):
    prompt = f"""
    My BMI is {state['bmi']} and category is {state['category']}.
    Give short health advice.
    """
    
    response = llm.invoke(prompt)
    
    return {**state, "advice": response.content}
class State(TypedDict):
    height:float
    weight:float
    bmi:float
    category:str
    advice: str

def calculate(state:State):
    h=state['height']
    w=state['weight']
    state['bmi']=w/h**2
    return state

def categorize_bmi(state: State):
    bmi = state["bmi"]
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return {**state,"category":category}

builder=StateGraph(State)
builder.add_node("calculate",calculate)
builder.add_node("categorize_bmi",categorize_bmi)
builder.add_node("advice", generate_advice)
builder.set_entry_point("calculate")
builder.add_edge("calculate","categorize_bmi")
builder.add_edge("categorize_bmi","advice")
graph=builder.compile()
res=graph.invoke({
    "height": 1.75,
    "weight":   170
})
print(res)
