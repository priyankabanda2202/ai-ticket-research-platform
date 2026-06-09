from app.tools.market_data import fetch_market_data
from app.tools.indicators import calculate_rsi

def market_agent(state):
    ticker = state["ticker"]

    # 1. Safely execute data fetching with fallbacks to handle API issues or rate limits
    try:
        market = fetch_market_data(ticker) or {}
    except Exception:
        market = {}

    try:
        rsi = calculate_rsi(ticker)
    except Exception:
        rsi = "N/A"

    # 2. Extract metrics defensively using .get() to prevent KeyError crashes
    price = market.get("price", "N/A")
    pe_ratio = market.get("pe_ratio", "N/A")
    volatility = market.get("volatility", "N/A")

    return {
        "market": {
            "price": price,
            "pe_ratio": pe_ratio,
            "volatility": volatility,
            "rsi": rsi
        }
    }