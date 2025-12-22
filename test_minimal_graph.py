"""
Minimal test to verify graph execution
"""
from typing import TypedDict, Annotated, List
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages

class SimpleState(TypedDict):
    messages: Annotated[list, add_messages]
    count: int

def node_a(state: SimpleState):
    print(f"[NODE_A] count={state.get('count', 0)}")
    return {"messages": [AIMessage(content=f"Response {state.get('count', 0)}")], "count": state.get('count', 0) + 1}

def node_b(state: SimpleState):
    print(f"[NODE_B] count={state.get('count', 0)}")
    return {"messages": [HumanMessage(content=f"Feedback {state.get('count', 0)}")]}

def should_continue(state: SimpleState):
    count = state.get('count', 0)
    print(f"[SHOULD_CONTINUE] count={count}")
    if count >= 3:
        print(f"[SHOULD_CONTINUE] END")
        return END
    print(f"[SHOULD_CONTINUE] Continue to node_b")
    return "node_b"

# Build graph
builder = StateGraph(SimpleState)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_edge(START, "node_a")
builder.add_conditional_edges("node_a", should_continue)
builder.add_edge("node_b", "node_a")

graph = builder.compile()

# Test
print("=" * 80)
print("Testing minimal graph")
print("=" * 80)

inputs = {"messages": [HumanMessage(content="test")], "count": 0}
for event in graph.stream(inputs):
    print(f"Event: {list(event.keys())}")

print("=" * 80)
print("Done")
print("=" * 80)

