from app.tools.market_data import fetch_market_data
from app.tools.indicators import calculate_rsi

def market_agent(state):

    ticker = state["ticker"]

    try:
        market = fetch_market_data(ticker)

    except Exception as e:

        print(f"Market Agent Error: {e}")

        market = {}

    try:
        rsi = calculate_rsi(ticker)
    except Exception:
        rsi = "N/A"

    return {
        "market": {
            "price": market.get("price", "N/A"),
            "pe_ratio": market.get("pe_ratio", "N/A"),
            "rsi": rsi
        }
    }
