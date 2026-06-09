import yfinance as yf

def fetch_market_data(ticker):
    # Establish a default fallback dictionary matching your ecosystem's schema
    default_response = {
        "price": "N/A",
        "pe_ratio": "N/A",
        "volatility": "N/A"
    }

    try:
        stock = yf.Ticker(ticker)
        
        # 1. Guardrail against historical data gaps (Empty symbols or network drops)
        hist = stock.history(period="1d")
        if hist.empty:
            return default_response

        # Extract the latest closing price safely
        price = float(hist["Close"].iloc[-1])

        # 2. Guardrail against missing company metadata info strings
        info = stock.info if stock.info else {}
        if not info:
            return default_response

        # 3. Defensively fetch metrics using .get() to avoid KeyError exceptions
        # (e.g., Unprofitable tech startups or biotech stocks don't have a P/E ratio)
        pe_ratio = info.get("trailingPE", "N/A")

        # 4. Deriving Volatility tier dynamically from the stock's Beta value
        beta = info.get("beta")
        if isinstance(beta, (int, float)):
            if beta > 1.3:
                volatility = "High"
            elif beta < 0.7:
                volatility = "Low"
            else:
                volatility = "Medium"
        else:
            volatility = "Medium" # Sensible engineering fallback line

        return {
            "price": price,
            "pe_ratio": pe_ratio,
            "volatility": volatility
        }

    except Exception as e:
        # Prevent logging from breaking production execution flows
        print(f"Telemetry Core Log — Market Data Pipeline Error for {ticker}: {e}")
        return default_response