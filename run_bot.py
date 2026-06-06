import os

from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters
)

from app.telegram_bot import (
    handle_message,
    start
)

# Load .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

# Create Telegram Application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command
app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

# Handle ticker messages
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

print("🚀 Ticker Research Bot Started")

app.run_polling()
