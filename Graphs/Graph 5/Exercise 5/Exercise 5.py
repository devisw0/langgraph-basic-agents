from typing import TypedDict, List
from langgraph.graph import START,END, StateGraph
import random

#creating our state
class AgentState(TypedDict):
    player_name:str
    upperbound:int
    lowerbound:int
    guesses:List[int]
    attempts:int
    target_number: int
    hint:str
    total_attempts_allowed:int
    curr_guess: int

#creating our nodes
def setup(state:AgentState)-> AgentState:
    print(f"Hello {state['player_name']} are you ready?")
    state['guesses'] = []
    state['attempts'] = 0
    state['lowerbound'] = 1
    state['upperbound'] = 20
    state['target_number'] = random.randint(state['lowerbound'],state['upperbound'])
    state["hint"] = "Game Started! Try to guess the number!"
    print(f"{state['player_name']} The game has begun. I'm thinking of a number between 1 and 20.")
    state["total_attempts_allowed"] = 7 #counter
    state['curr_guess'] = 0

    return state

#Guess Node
def guess_node(state:AgentState) -> AgentState:
    state['curr_guess'] = random.randint(state['lowerbound'],state['upperbound'])
    state['guesses'].append(state['curr_guess'])
    state['attempts'] +=1
    
    return state

#Hint Node
def hint_node(state:AgentState)->AgentState:
    if state['curr_guess'] > state['target_number']:
        state['upperbound'] = state['curr_guess']
        state["hint"] = f"The number {state['curr_guess']} is too high. Try lower!"
    elif state['curr_guess'] < state['target_number']:
        state['lowerbound'] = state['curr_guess']
        state["hint"] = f"The number {state['curr_guess']} is too low. Try higher!"
    else:
        state["hint"] = f"Correct! the number was {state['target_number']}"
    
    return state

#Should we try again function/edge
def should_we_continue(state:AgentState) -> str:
    if state['hint'] == f"Correct! the number was {state['target_number']}" or state['attempts'] >= state['total_attempts_allowed']:
        return "End"
    else:
        return "Guess"
    

#Creating blueprint of graph of type our state
graph = StateGraph(AgentState)

#creating nodes
graph.add_node("setup", setup)
graph.add_node("guess", guess_node)
graph.add_node("hint",hint_node)

#add our edges
graph.add_edge(START,"setup")
graph.add_edge("setup", "guess")
graph.add_edge("guess","hint")
graph.add_conditional_edges( #(where we start edges from, the function, mapping from edges to nodes in dict format)
    "hint",
    should_we_continue,
    {
        "End": END,
        "Guess": "guess"
    }
)

#Now we compile
app = graph.compile()

#now we can invoke
result = app.invoke({"player_name": "User"})
print(result)


#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("conditional-graph.png", "wb") as f: #context manager
    f.write(png_data)