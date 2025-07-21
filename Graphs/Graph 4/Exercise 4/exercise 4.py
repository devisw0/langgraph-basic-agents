from typing import TypedDict
from langgraph.graph import StateGraph, START, END


#we must first create our state format
class AgentState(TypedDict):
    num1:int
    num2:int
    operation1:str
    num3:int
    num4:int
    operation2:str
    result1:int
    result2:int

#create node functions
def adder1(state:AgentState)->AgentState:
    state['result1'] = state['num1'] + state['num2']
    return state
def subtractor1(state:AgentState) ->AgentState:
    state['result1'] = state['num1'] - state['num2']
    return state

#creating first decider function
def decider_1(state:AgentState) ->AgentState:
    if state['operation1'] == "+":
        return "addition_operation1"
    if state['operation1'] == "-":
        return "subtraction_operation1"

#creating the second add and subtraction nodes
def adder2(state:AgentState)->AgentState:
    state['result2'] = state['num3'] + state['num4']
    return state
def subtractor2(state:AgentState) ->AgentState:
    state['result2'] = state['num3'] - state['num4']
    return state

#creating the second router node function
def decider2(state:AgentState) -> AgentState:
    if state['operation2'] == "+":
        return "addition_operation2"
    if state['operation2'] == "-":
        return "subtraction_operation1"
    
#creating blueprint of the graph and setting its data to type AgentState
graph = StateGraph(AgentState)

#Add our Nodes
graph.add_node("add_node1",adder1)
graph.add_node("subtract_node1",subtractor1)
graph.add_node("router1", lambda state:state) #we are saying there is no change in the state in the router node

graph.add_node("add_node2",adder2)
graph.add_node("subtract_node2",subtractor2)
graph.add_node("router2", lambda state:state) #we are saying there is no change in the state in the router node

#now add our edges
graph.add_edge(START,"router1")

#starting node connected to router. now we need to create conditional edges from our router to adder1 and subtractor 1
#(what node to start at, what function to do, mapping (dictionary format -> {pathname:nodename}))
#where path name comes to what is returned from the function
graph.add_conditional_edges(
    "router1",
    decider_1,
    {
        "addition_operation1": "add_node1",
        "subtraction_operation1": "subtract_node1"
    }
)

#now we need to connect the adder1 and subtractor1 to our router 2
graph.add_edge("add_node1", "router2")
graph.add_edge("subtract_node1", "router2")

#add conditional edge from our 2nd router
#(what node to start at, what function to do, mapping (dictionary format -> {pathname:nodename}))
#where path name comes to what is returned from the function
graph.add_conditional_edges(
    "router2",
    decider2,
    {
     "addition_operation2":"add_node2",
     "subtraction_operation1": "subtract_node2" 
    }
)

#now connect end nodes to the final add and subtract nodes
graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)

#now compile our graph
app = graph.compile()

#and now we can incoke with inputs!!
result = app.invoke({"num1":7, "num2": 4, "operation1": "+", "num3": 3, "num4": 9, "operation2":"-"})
print(result)

#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("conditional-graph.png", "wb") as f: #context manager
    f.write(png_data)