import yfinance as yf

def fetch_market_data(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "price": info.get("currentPrice"),
        "pe_ratio": info.get("trailingPE"),
        "volatility": "high" if info.get("beta", 1) > 1.2 else "medium"
    }