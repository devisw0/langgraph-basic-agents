from typing import TypedDict, Dict, List
from langgraph.graph import StateGraph


#Create State
class Exercise3State(TypedDict):
    name:str
    age:int
    skills:str
    result: str


#Create 1st Node

def namenode(state:Exercise3State) -> Exercise3State:
    state['result'] = f"{state['name']}, welcome to the system! "
    return state

#Create 2nd node

def agenode(state:Exercise3State) ->Exercise3State:
    state['result'] = state['result'] + f"You are {state['age']} years old! "
    return state

#Create 3rd Node

def skillsnode(state:Exercise3State) -> Exercise3State:
    state['result'] = state['result'] + f"You have skills in: "
    return state

#Now we created our nodes, we must create our graph blueprint specifying it is of our type state
graph = StateGraph(Exercise3State)

#Next add our nodes
graph.add_node("name", namenode) #(we name the node, the function the node performs)
graph.add_node("age", agenode)
graph.add_node("skills", skillsnode)

#now we must connect the starting and ending nodes
graph.set_entry_point("name")
#but we still have to connect the induvidual nodes
#to do this we use edges
graph.add_edge("name","age") #.add_edge(first edge, second edge we link/go to)
graph.add_edge("age", "skills")

graph.set_finish_point("skills") #notice now we have finish point connected to another node since we have multiple

#we have attached the starting and ending nodes to where they should be respectively as well as the edges
#next we must compile
app = graph.compile()

#now that the graph is compiled, we can invoke!
result = app.invoke({"name": "User", "age": 24, "skills": "Python, Langgraph"})
print(result)
#printing will result in entire dictionary printed so we specify the result
print(result['result'])


#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("Exercise 3.png", "wb") as f: #context manager
    f.write(png_data)
