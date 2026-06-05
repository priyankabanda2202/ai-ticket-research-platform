from telegram import Update
from telegram.ext import ContextTypes
from app.graph import build_graph

graph = build_graph()

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

        rsi = market.get("rsi", "N/A")
        sentiment = sentiment_data.get("sentiment", "Neutral")

        reply = f"""
📈 *STOCK ANALYSIS*

━━━━━━━━━━━━━━━

🏢 *Ticker:* `{ticker}`

🟢 *Recommendation:* *{decision['recommendation']}*

🎯 *Confidence:* {confidence}%

📊 *RSI:* {rsi}

📰 *Sentiment:* {sentiment}

━━━━━━━━━━━━━━━

💡 *AI Insight*

{decision['rationale']}
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