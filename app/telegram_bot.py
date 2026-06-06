from telegram import Update
from telegram.ext import ContextTypes
from app.graph import build_graph

graph = build_graph()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
📈 Welcome to Ticker Research Bot

Send any stock ticker:

AAPL
MSFT
NVDA
AMZN
GOOGL

and I'll generate:

✅ Market Analysis
✅ RSI
✅ Sentiment Analysis
✅ Buy/Sell Recommendation
✅ PDF Research Report
"""
    )
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ticker = update.message.text.strip().upper()

    msg = await update.message.reply_text("🔍 Analyzing...")

    try:
        result = graph.invoke({"ticker": ticker})
        print(result)

        decision = result["decision"]
        market = result.get("market", {})
        sentiment_data = result.get("sentiment", {})
        
        confidence = round(decision.get("confidence", 0) * 100)
        
        price = market.get("price", "N/A")
        pe_ratio = market.get("pe_ratio", "N/A")
        rsi = market.get("rsi", "N/A")
        volatility = market.get("volatility", "N/A")
        
        sentiment = sentiment_data.get("sentiment", "Neutral")
        sentiment_score = round(sentiment_data.get("score", 0) * 100)
        
        reply = f"""
        📈 *STOCK ANALYSIS*
        
        ━━━━━━━━━━━━━━━
        
        🏢 *Ticker:* `{ticker}`
        
        💰 *Price:* ${price}
        
        📊 *P/E Ratio:* {pe_ratio}
        
        📉 *RSI:* {rsi}
        
        ⚡ *Volatility:* {volatility}
        
        📰 *Sentiment:* {sentiment} ({sentiment_score}%)
        
        🟢 *Recommendation:* *{decision['recommendation']}*
        
        🎯 *Confidence:* {confidence}%
        
        ━━━━━━━━━━━━━━━
        
        💡 *AI Insight*
        
        _{decision['rationale']}_
        
        🌐 Dashboard:
        https://ai-ticket-research-platform.onrender.com
        """

        await msg.edit_text(
            reply,
            parse_mode="Markdown"
        )

    except Exception as e:
        print("ERROR:", e)
        await msg.edit_text(
            f"❌ Error occurred:\n\n{str(e)}"
        )
#    print(result)
