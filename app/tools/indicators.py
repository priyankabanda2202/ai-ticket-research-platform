import pandas as pd
import yfinance as yf

def calculate_rsi(ticker: str, period: int = 14) -> float:
    # 1. Download data
    data = yf.download(ticker, period="1mo", group_by="ticker")
    
    if data.empty:
        return 50.0  # Safe default fallback value if download fails
        
    # 2. Extract 'Close' cleanly using cross-section across any MultiIndex level
    if isinstance(data.columns, pd.MultiIndex):
        if 'Close' in data.columns.get_level_values(0):
            close_series = data.xs('Close', axis=1, level=0)
        else:
            close_series = data.xs('Close', axis=1, level=1)
    else:
        close_series = data['Close']
    
    # 3. If a 1-column DataFrame remains, crush it into a flat Series
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.squeeze()

    # 4. Mathematical processing calculation for RSI
    delta = close_series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    
    # Guardrail against division-by-zero
    loss = loss.replace(0, 0.00001)
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # 5. Extract the final index item element safely
    final_rsi = rsi.dropna().iloc[-1]
    return float(final_rsi)