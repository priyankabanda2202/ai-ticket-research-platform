import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from app.telegram_bot import handle_message
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
#print(BOT_TOKEN)
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()