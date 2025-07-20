from langgraph.graph import StateGraph, START,END
import random
from typing import Dict,List,TypedDict

class AgentState(TypedDict):
    name:str
    number: List[int]
    counter:int


#greeting node
def greetingnode(state:AgentState)->AgentState:
    """Greeting node that says hi to the person"""
    state['name'] = f"Hi there {state['name']}"
    state['counter'] = 0 #important line
    return state

def random_node(state:AgentState)-> AgentState:
    """Generates a random number from 0 to 10"""
    state["number"].append(random.randint(0,10))
    state['counter'] +=1
    return state

#recall our conditional edge. this looping edge is actually a conditional edge too!!
def should_continue(state:AgentState)->AgentState:
    """function to decide what to do next"""
    if state['counter'] <5:
        print("ENTERING LOOP", state['counter'])
        return "loop"
    else:
        return "exit"
    

graph = StateGraph(AgentState)

graph.add_node("greeting",greetingnode)
graph.add_node("random", random_node)
graph.add_edge("greeting","random")

graph.add_conditional_edges(
    "random", #source node
    should_continue, #action we want to perform
    {
        "exit": END, #end the graph
        "loop":"random"
    }

)

graph.set_entry_point("greeting")

app = graph.compile()
result = app.invoke({"name":"User", "number":[], "counter": -100})
print(result)

#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("conditional-graph.png", "wb") as f: #context manager
    f.write(png_data)