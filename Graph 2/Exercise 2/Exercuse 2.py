from typing import TypedDict, Dict, List
from langgraph.graph import StateGraph
import math

#Create our state
class operatoroption(TypedDict):
    name:str
    values: List[int]
    operator:str
    result:str

#Create our Node
def operation(state:operatoroption) -> operatoroption:
    if state['operator'] == "+":
        calc = sum(state['values'])
        state['result'] = f"Hello {state['name']}! based on you operator and your values, your result is {calc}"
        return state
    elif state['operator'] == "*":
        calc = math.prod(state['values'])
        state['result'] = f"Hello {state['name']}! based on you operator and your values, your result is {calc}"
        return state
    

#Now creating our blueprint
graph = StateGraph(operatoroption) #defining frame, my graph will work on a state that looks like this typed dict

#Next add our node
graph.add_node("optchoice", operation)

#connect it to starting and ending nodes
graph.set_entry_point("optchoice")
graph.set_finish_point("optchoice")

#Next compile and use that instance
app = graph.compile()

#Next invoke it
final_result = app.invoke({"name":"User", "values": [1,2,3,4], "operator":"*"})
final_result_add = app.invoke({"name":"User", "values": [1,2,3,4], "operator":"+"})
#will return entire dictionary if print
print(final_result)
print(final_result_add)

#So we must take exact key's value that we want to have
print(final_result['result'])
print(final_result_add['result'])

#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("exercise2.png", "wb") as f: #context manager
    f.write(png_data)
