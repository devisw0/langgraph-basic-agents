import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv
from pathlib import Path


#Chatbot with conversational memory
# __file__ = …/Agents/Agent 1/Agent 1.py
project_root = Path(__file__).parents[2]         
# ↑ two levels up: Agents/Agent 1 → Agents → langgraph-basic-agents
env_path = project_root / ".env"


#Creating our State structure
class AgentState(TypedDict):
    messages: List[Union[HumanMessage,AIMessage]]


llm = ChatOpenAI(model="gpt-4o")

def process_node(state:AgentState)->AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state['messages']) #So this node basically sends whatever content to the chatgpt API invoke = call for
    state["messages"].append(AIMessage(content=response.content)) #appending to our messages list the openAI response and wrapping it with AIMessage to indicate the role
    print(f"\nAI: {response.content}") #just printing
    return state


#create blueprint of graph of type our state
graph = StateGraph(AgentState)



#Add nodes
graph.add_node("process", process_node)
graph.add_edge(START,"process")
graph.add_edge("process", END)
app  = graph.compile()

conversation_history = []

user_input = input("Enter: ")
while user_input.lower() != "exit":
    conversation_history.append(HumanMessage(user_input))
    result = app.invoke({"messages": conversation_history}) #giving the llm the entire conversational memories
    #result is of type AgentState ?
    conversation_history = result["messages"] 
    user_input = input("Enter: ")