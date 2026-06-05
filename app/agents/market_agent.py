from app.tools.market_data import fetch_market_data
from app.tools.indicators import calculate_rsi

def market_agent(state):
    ticker = state["ticker"]

    try:
        market = fetch_market_data(ticker)
    except Exception:
        market = {
            "price": "N/A"
        }
    rsi = calculate_rsi(ticker)

    return {
        "market": {
            "price": market["price"],
            "pe_ratio": market["pe_ratio"],
            "volatility": market["volatility"],
            "rsi": rsi
        }
    }
