from typing import Dict, TypedDict
from langgraph.graph import StateGraph #framework to design and manage flow of tasks using a graph


#Agent State - keeps track of our info while app runs

class AgentState(TypedDict):#In langgraph the state must be a class
    message: str



#First Node

#To define a node you just use a normal standard python function
def greeting_node(state:AgentState) -> AgentState: #Both input and output type of a node must be a state (Initial State -> Updated State)
    """Simple Node that adds a greeting message to the state """ 
    #Doc Strings tells the LLMS what this function does
    state['message'] = "Hey" + state["message"] + ", how is your day going?"
    #We take the message input from our state and make edits to it
    return state