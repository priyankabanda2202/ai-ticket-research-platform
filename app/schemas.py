from pydantic import BaseModel
from typing import TypedDict, Optional

# ==========================================
# 1. Your Existing Pydantic Web API Schemas
# ==========================================
class TickerRequest(BaseModel):
    ticker: str

class MarketData(BaseModel):
    price: float
    rsi: float
    pe_ratio: float
    volatility: str

class SentimentData(BaseModel):
    sentiment: str
    score: float
    drivers: list[str]

class DecisionOutput(BaseModel):
    recommendation: str
    confidence: float
    rationale: str

# ==========================================
# 2. Add the Evaluation Pydantic Schema
# ==========================================
class EvaluationData(BaseModel):
    completeness_score: float
    quality: str

# ==========================================
# 3. Your LangGraph State Definition
# ==========================================
class AgentState(TypedDict):
    ticker: str
    market: Optional[dict]       # Stores data from MarketData
    sentiment: Optional[dict]    # Stores data from SentimentData
    decision: Optional[dict]     # Stores data from DecisionOutput
    evaluation: Optional[dict]   # <--- ADD THIS LINE FOR YOUR EVALS AGENT
    report_path: Optional[str]