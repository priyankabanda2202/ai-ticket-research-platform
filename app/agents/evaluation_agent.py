def evaluation_agent(state):

    market = state["market"]
    sentiment = state["sentiment"]
    decision = state["decision"]

    completeness_score = 100

    if market.get("price") == "N/A":
        completeness_score -= 30

    if market.get("pe_ratio") == "N/A":
        completeness_score -= 20

    return {
        "evaluation": {
            "completeness_score": completeness_score,
            "quality": "PASS"
        }
    }