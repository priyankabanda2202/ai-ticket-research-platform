from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents.validation_agent import validation_agent
from app.agents.market_agent import market_agent
from app.agents.sentiment_agent import sentiment_agent
from app.agents.evaluation_agent import evaluation_agent
from app.agents.decision_agent import decision_agent
from app.agents.report_agent import report_agent

# 1. Update the explicit state shape to hold our new telemetry keys
class AgentState(TypedDict):
    ticker: str
    validation_status: str  # Tracks pass/fail gate strings
    market: dict
    sentiment: dict
    evaluation: dict        # Stores completeness scores and quality status
    decision: dict
    report_path: str

def build_graph():
    # 2. Pass the updated AgentState schema to the StateGraph
    graph = StateGraph(AgentState)
    
    # 3. Register all nodes (including validation and evaluation layers)
    graph.add_node("validation", validation_agent)
    graph.add_node("market", market_agent)
    graph.add_node("sentiment", sentiment_agent)
    graph.add_node("evaluation", evaluation_agent)
    graph.add_node("decision", decision_agent)
    graph.add_node("report", report_agent)
    
    # 4. Re-route the workflow graph edges sequentially
    # Gatekeeper -> Data Gathering -> Telemetry Eval -> Logic Processing -> PDF Artifact Creation
    graph.set_entry_point("validation")
    
    graph.add_edge("validation", "market")
    graph.add_edge("market", "sentiment")
    graph.add_edge("sentiment", "evaluation")
    graph.add_edge("evaluation", "decision")
    graph.add_edge("decision", "report")
    graph.add_edge("report", END)
    
    return graph.compile()