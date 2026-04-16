from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. Define State
class GraphState(TypedDict):
    a: float
    b: float
    c: float
    discriminant: float
    result: str

# 2. Nodes (Steps)

# Step 1: Take input (already passed in state)
def input_node(state: GraphState):
    return state

# Step 2: Show equation
def show_equation(state: GraphState):
    a, b, c = state["a"], state["b"], state["c"]
    equation = f"{a}x^2 + {b}x + {c} = 0"
    print("Equation:", equation)
    return state

# Step 3: Calculate discriminant
def calculate_discriminant(state: GraphState):
    a, b, c = state["a"], state["b"], state["c"]
    d = b**2 - 4*a*c
    print("Discriminant:", d)
    return {**state, "discriminant": d}

# 3. Conditional check function
def check_condition(state: GraphState):
    d = state["discriminant"]
    if d > 0:
        return "real_roots"
    elif d == 0:
        return "repeated_roots"
    else:
        return "no_real_roots"

# 4. Branch Nodes

def real_roots(state: GraphState):
    a, b, d = state["a"], state["b"], state["discriminant"]
    root1 = (-b + d**0.5) / (2*a)
    root2 = (-b - d**0.5) / (2*a)
    result = f"Two real roots: {root1}, {root2}"
    print(result)
    return {**state, "result": result}

def repeated_roots(state: GraphState):
    a, b = state["a"], state["b"]
    root = -b / (2*a)
    result = f"One repeated root: {root}"
    print(result)
    return {**state, "result": result}

def no_real_roots(state: GraphState):
    result = "No real roots"
    print(result)
    return {**state, "result": result}

# 5. Build Graph
graph = StateGraph(GraphState)

graph.add_node("input", input_node)
graph.add_node("show_equation", show_equation)
graph.add_node("calculate_discriminant", calculate_discriminant)

graph.add_node("real_roots", real_roots)
graph.add_node("repeated_roots", repeated_roots)
graph.add_node("no_real_roots", no_real_roots)

# Flow
graph.set_entry_point("input")

graph.add_edge("input", "show_equation")
graph.add_edge("show_equation", "calculate_discriminant")

# Conditional branching
graph.add_conditional_edges(
    "calculate_discriminant",
    check_condition,
    {
        "real_roots": "real_roots",
        "repeated_roots": "repeated_roots",
        "no_real_roots": "no_real_roots"
    }
)

# End connections
graph.add_edge("real_roots", END)
graph.add_edge("repeated_roots", END)
graph.add_edge("no_real_roots", END)

# Compile
app = graph.compile()
print(app.get_graph().draw_ascii())
# 6. Run Example
result = app.invoke({"a": 1, "b": -3, "c": 2})
print("Final Output:", result["result"])