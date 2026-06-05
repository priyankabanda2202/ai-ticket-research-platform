import yfinance as yf
import numpy as np

def fetch_market_data(ticker):

    try:

        stock = yf.Ticker(ticker)

        hist = stock.history(period="3mo")

        price = float(hist["Close"].iloc[-1])

        # Calculate RSI
        delta = hist["Close"].diff()

        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        rsi_value = float(rsi.iloc[-1])

        # Simple volatility classification
        volatility_pct = hist["Close"].pct_change().std() * np.sqrt(252)

        if volatility_pct < 0.20:
            volatility = "Low"
        elif volatility_pct < 0.40:
            volatility = "Medium"
        else:
            volatility = "High"

        return {
            "price": round(price, 2),

            # Temporary value until you move to Finnhub/AlphaVantage
            "pe_ratio": 25.49,

            "rsi": round(rsi_value, 1),

            "volatility": volatility
        }

    except Exception as e:

        print("Market Data Error:", e)

        return {
            "price": None,
            "pe_ratio": None,
            "rsi": None,
            "volatility": "Unknown"
        }
