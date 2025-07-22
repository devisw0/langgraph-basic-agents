from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
import os
from pathlib import Path


# __file__ = …/Agents/Agent 1/Agent 1.py
project_root = Path(__file__).parents[2]         
# ↑ two levels up: Agents/Agent 1 → Agents → langgraph-basic-agents
env_path = project_root / ".env"

print("Loading .env from:", env_path)   # sanity check
load_dotenv(dotenv_path=env_path)

#Call state
class AgentState(TypedDict):
    messages:List[HumanMessage]


llm = ChatOpenAI(model = "gpt-4o") #instance of the ChatOpenAI model wiht langchain and using model gpt-4o

#Creating our node fucntion
def process_node(state:AgentState)->AgentState:
    response = llm.invoke(state['messages']) #invoking our llm (ChatOpenAI with our message)
    print(f"\nAI: {response.content}")
    return state

#create blueprint of graph of type our state
graph = StateGraph(AgentState)



#Add nodes
graph.add_node("process", process_node)
graph.add_edge(START,"process")
graph.add_edge("process", END)
app  = graph.compile()

# user_input = input("Enter something: ")
# # app.invoke({"messages": [HumanMessage(content=user_input)]})

#we can also do it so we can continuously ask questions

user_input = input('Enter Something:')
Exit = 'exit'
while user_input.lower() != Exit:
    app.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input('Enter Something:')



#visualizing our graph
#app is like the graph ina flowing state, get_graph takes a static moment (like a picture of a show) we can use
#draw turns it into bytes using a mermaid diagramming language we can write in a file
png_data = app.get_graph().draw_mermaid_png()
# write it out
with open("conditional-graph.png", "wb") as f: #context manager
    f.write(png_data)
