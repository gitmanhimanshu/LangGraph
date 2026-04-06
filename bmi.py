from typing import TypedDict
from langgraph.graph import StateGraph
class State(TypedDict):
    height:float
    weight:float
    bmi:float
    category:str

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
builder.set_entry_point("calculate")
builder.add_edge("calculate","categorize_bmi")
graph=builder.compile()
res=graph.invoke({
    "height": 1.75,
    "weight":   170
})
print(res)
