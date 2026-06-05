import yfinance as yf

def fetch_market_data(ticker):

    try:

        stock = yf.Ticker(ticker)

        hist = stock.history(period="1d")

        price = float(hist["Close"].iloc[-1])

        return {
            "price": price
        }

    except Exception as e:

        print("Market Data Error:", e)

        return {
            "price": "Unavailable"
        }
