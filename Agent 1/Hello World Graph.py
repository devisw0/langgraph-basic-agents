from typing import Dict, TypedDict
from langgraph.graph import StateGraph #framework to design and manage flow of tasks using a graph
from IPython.display import Image, display

#Agent State - keeps track of our info while app runs

class AgentState(TypedDict):#In langgraph the state must be a class
    #Our State schema
    message: str



#First Node

#To define a node you just use a normal standard python function
def greeting_node(state:AgentState) -> AgentState: #Both input and output type of a node must be a state (Initial State -> Updated State)
    """Simple Node that adds a greeting message to the state """ 
    #Doc Strings tells the LLMS what this function does
    state['message'] = "Hey " + state["message"] + ", how is your day going?"
    #We take the message input from our state and make edits to it
    return state


#Creating Graph to design and manage flow

graph = StateGraph(AgentState)
#Just a graph with a state now, empty

#Adding a node to graph
graph.add_node("greeter", greeting_node) #2 parameters: the name of the node, and then the action

#Need to set Starting and Ending points for the graph
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")
#we are saying connect the entry point to our node that was called greeter
#we are also saying to connect the finish point to our node that was called greeter

#need to compile graph
app = graph.compile()


#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("graph.png", "wb") as f: #context manager
    f.write(png_data)


#Now we can run our Graph
result = app.invoke({"message": "Bob"})
#outputs a state (just like the input of the graph)!

#and we know the output will be a dictionary (like input)
#Need to get the value of message key
print(result['message'])
