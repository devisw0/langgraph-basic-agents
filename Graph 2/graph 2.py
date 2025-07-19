from typing import TypedDict, Dict, List
from langgraph.graph import StateGraph

#main goal of this graph is how to handle multiple inputs, perform operations on list data, and have a more complex AgentState

#Creating our State
class SumAgentState(TypedDict):
    nums: List[int]
    name: str
    result: str

#Creating our first Node
def sumprocessor(state:SumAgentState) -> SumAgentState:

    state['result'] = f"Hello {state['name']}! your sum is {sum(state['nums'])}"

    return state

#Now we must create the blue print of the graph
graph = StateGraph(SumAgentState) #Remember Graph must take input of state and output of state

#Next we have to add our nodes
graph.add_node("adder", sumprocessor) #add_node(name of node, what function)
graph.set_entry_point("adder") #connecting entry point to our adder node
graph.set_finish_point("adder") #connecting end point to our adder node

#now we have created graph blueprint, added our node and connected entry and end nodes to our node
#we must compile
app = graph.compile()

#Now we can invoke since our graph was compiled
#The input to it must have keys of exact name of key and type of values (if they are used)
end_result = app.invoke({"nums": [1,2,4,5], "name": "User"})
#printing end_result would result in the full dictionary
print(end_result)

#so we just look for specific key's value. in our case we just want result's value
print(end_result['result'])

#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("graph2.png", "wb") as f: #context manager
    f.write(png_data)
