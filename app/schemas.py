from pydantic import BaseModel

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