def decision_agent(state):
    market = state["market"]
    sentiment = state["sentiment"]

    if sentiment["score"] > 0.6 and market["rsi"] < 70:
        rec = "BUY"
        confidence = 0.8
    elif sentiment["score"] < 0.4 or market["volatility"] == "high":
        rec = "SELL"
        confidence = 0.75
    else:
        rec = "HOLD"
        confidence = 0.6

    return {
        "decision": {
            "recommendation": rec,
            "confidence": confidence,
            "rationale": "Decision based on sentiment, momentum, and risk"
        }
    }