def validation_agent(state):

    ticker = state["ticker"]

    if not ticker:
        raise ValueError("Ticker cannot be empty")

    if len(ticker) > 10:
        raise ValueError("Invalid ticker")

    return {}