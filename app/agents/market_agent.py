from app.tools.market_data import fetch_market_data

def market_agent(state):

    ticker = state["ticker"]

    market = fetch_market_data(ticker)

    return {
        "market": market
    }
