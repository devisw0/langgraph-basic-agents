from typing import TypedDict, Dict
from langgraph.graph import StateGraph

#Our state
class ComplimentState(TypedDict):
    name:str

#First Node
def compliment_node(username:ComplimentState) -> ComplimentState:
    """Here we will compliment the user"""

    username['name'] = username['name'] + ", you are doing a good job learning Langgraph!"
    return username

#Need to create a graph to design and manage our flow.
#We set what our node will do and the state format so lets start creating the graph
compliment_graph = StateGraph(ComplimentState) #saving our graph to a variable
#remember a graph takes input of type state and outputs type state (so does each node)

#we made our graph but it is empty. So we must add our created node first (compliment_node)
compliment_graph.add_node("complimentor", compliment_node) #add_node(node name, what it does)

#need to add and connect our starting and ending nodes
compliment_graph.set_entry_point("complimentor")
compliment_graph.set_finish_point("complimentor")

#now we need to compile our graph
complimentor_agent = compliment_graph.compile()
#Now we must run it (invoke our graph)
result = complimentor_agent.invoke({"name": "User"})
#we are specifying the graph input format (it must be exactly like it is in state)
#That is why our key for our dictionary is the exact match and our value is the same type as specified


#we are returned with a dictionary which is the same format as the input and output
#this is because the input and output of a node or the entire graph is the same format as the state
#So we have to specify what in the dictionary we want the output to be
print(result['name'])
#it works!

#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = complimentor_agent.get_graph().draw_mermaid_png()
# write it out
with open("graph.png", "wb") as f: #context manager
    f.write(png_data)
