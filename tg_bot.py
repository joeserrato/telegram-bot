import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Check if token exists
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

# Create the application with token from environment variable
app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Enter the text you want to show to the user whenever they start the bot"
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your Message")


async def gmail_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("https://mail.google.com/mail/u/2/#inbox")


async def youtube_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("https://www.youtube.com/")


async def linkedIn_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("https://www.linkedin.com/in/joeangelineserrato")


async def facebook_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("https://www.facebook.com/")


async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sorry I can't recognize you, you said '%s'" % update.message.text
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text
    )


# Add command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("youtube", youtube_url))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("linkedin", linkedIn_url))
app.add_handler(CommandHandler("gmail", gmail_url))
app.add_handler(CommandHandler("facebook", facebook_url))

# Handler for unknown commands
app.add_handler(MessageHandler(filters.COMMAND, unknown))

# Handler for unknown text messages
app.add_handler(MessageHandler(filters.TEXT, unknown_text))

# Start the bot
if __name__ == "__main__":
    app.run_polling()