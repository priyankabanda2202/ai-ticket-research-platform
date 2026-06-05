from typing import TypedDict
from langgraph.graph import StateGraph
from app.agents.market_agent import market_agent
from app.agents.sentiment_agent import sentiment_agent
from app.agents.decision_agent import decision_agent
from app.agents.report_agent import report_agent

# 1. Define the explicit state shape
class AgentState(TypedDict):
    ticker: str
    market: dict
    sentiment: dict
    decision: dict
    report_path: str

def build_graph():
    # 2. Pass the AgentState schema to the StateGraph
    graph = StateGraph(AgentState)
    
    graph.add_node("market", market_agent)
    graph.add_node("sentiment", sentiment_agent)
    graph.add_node("decision", decision_agent)
    graph.add_node("report", report_agent)
    
    graph.set_entry_point("market")
    graph.add_edge("market", "sentiment")
    graph.add_edge("sentiment", "decision")
    graph.add_edge("decision", "report")
    
    return graph.compile()