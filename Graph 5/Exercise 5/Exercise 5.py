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

#creating our nodes
def setup(state:AgentState)-> AgentState:
    print(f"Hello {state['player_name']} are you ready?")
    state['guesses'] = []
    state['attempts'] = 0
    state['lowerbound'] = 0
    state['upperbound'] = 20
    state['target_number'] = random.randint(state['lowerbound'],state['upperbound'])
    state["hint"] = "Game Started! Try to guess the number!"
    print(f"{state['player_name']} The game has begun. I'm thinking of a number between 1 and 20.")
    state["total_attempts_allowed"] = 7 #counter

def guess_node(state:AgentState) -> AgentState:
    for i in range(state['lowerbound'],state['upperbound']+1):
        cpu_guess = random.randint(random.randint(state['lowerbound'],state['upperbound']))
        