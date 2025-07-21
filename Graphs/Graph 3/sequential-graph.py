from typing import TypedDict, Dict, List
from langgraph.graph import StateGraph

#main goal how to create and handle multiple nodes in langgraph

#Create State
class multiplenodes(TypedDict):
    name: str
    age: str
    final: str

def first_node(state:multiplenodes) -> multiplenodes:
    """This is the first node of our sequence"""
    state["final"] = f"Hi {state['name']},"
    return state

def second_node(state:multiplenodes) -> multiplenodes:
    """This is the second node of our sequence"""
    state["final"] = state["final"] + f" you are {state['age']} years old!"
    return state

#After Creating our node functions and our State format, we must initialize the graph and set its blueprint to type of our state
graph = StateGraph(multiplenodes)

#Now we must create the nodes
graph.add_node("first_node", first_node) #(name, function)
graph.add_node("second_node", second_node)

#next set entry point
graph.set_entry_point("first_node")

#now before we set exit point we must connect the first and second node using an edge
graph.add_edge("first_node", "second_node")

#now since our start node is connected and our other nodes are connected we now connect the finish point
graph.set_finish_point("second_node")

#now we must compile and save it into a variable
app = graph.compile()

#now that we have compiled our graph (its loaded) we must invoke
result = app.invoke({"name": "User", "age": "24"})
print(result)

#we can specify what output we want
final_result = result['final']
print(final_result)

#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("sequential-graph.png", "wb") as f: #context manager
    f.write(png_data)
