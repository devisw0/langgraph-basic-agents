from typing import TypedDict
from langgraph.graph import StateGraph, START, END #START and END are just another way to add start and end point

#We must create our state and its format
class CondState(TypedDict):
    num1: int
    num2: int
    operation:str
    finalNumber: int

#First node creation
def adder(state:CondState) -> CondState:
    """This node adds the two numbers"""
    state['finalNumber'] = state['num1'] + state['num2']
    return state

#Second Node Creation
def subtractor(state:CondState) -> CondState:
    """This node subtracts the two numbers"""
    state['finalNumber'] = state['num1'] - state['num2']
    return state


def decide_next_node(state:CondState)->CondState:
    """This node will select the next node of the graph"""
    if state['operation'] == "+":
        return "addition_operation" #this is what we will call our edge that goes to the adder node
    elif state['operation'] == "-":
        return "subtraction_operation" #This is what we will call our edge that goes to the subtractor node
    
    #so if operator is + we will return the edge addition_operation and if its - we will return the subtraction_operation


#We must initialize the blueprint of the graph using the data format of our state
graph = StateGraph(CondState)

#Adding nodes to the graph
graph.add_node("add_node",adder)
graph.add_node("subtract_node",subtractor)
# graph.add_node("router", decide_next_node)
#this would not work as we do not return state (like the an object of type CondState (our state))

graph.add_node("router", lambda state: state) #the lambda function says the input state will be the output state
#passthrough function, as we do not change the state at all. We compare buy dont assign

#add edges
graph.add_edge(START, "router")

#conditional edges format (source node name, what action it needs to do, path map (what nodes to connect and where) it is in dictionary format )
graph.add_conditional_edges(
    "router",
    decide_next_node,

    {   #Edge : Node format
        #we say to which node the edge connects to
        "addition_operation": "add_node",
        "subtraction_operation": "subtract_node"
    }
)
#basically we said from the router node, perform the decide_next_node action
#then make conditional edges called ... to ... in the third argument

graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

app = graph.compile()
result = app.invoke({"num1": 7, "num2": 3, "operation": "+"})
print(result)
result2 = app.invoke({"num1": 7, "num2": 3, "operation": "-"})
print(result2)

#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("conditional-graph.png", "wb") as f: #context manager
    f.write(png_data)