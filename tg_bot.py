import os
import threading
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import ContextTypes

# Load environment variables
load_dotenv()

# Get token
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found! Make sure it's set in environment variables.")

# Create Flask app for Render's health checks
flask_app = Flask(__name__)

@flask_app.route('/')
def health():
    return "Bot is running!", 200

@flask_app.route('/health')
def health_check():
    return "OK", 200

# Create Telegram bot application
app = Application.builder().token(BOT_TOKEN).build()

# --- FUN AND ENGAGING HANDLER FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **Yooo! Welcome to your personal routine & helper bot!** ✨\n\n"
        "Let's get this productivity going! Focus sa goals today at bawal tamarin. "
        "Here are the commands you can play with to check your links or get help:\n\n"
        "📌 `/help` - Show all commands\n"
        "📌 `/youtube` - Watch some tutorials or clips\n"
        "📌 `/linkedin` - Check professional profile\n"
        "📌 `/gmail` - Quick email link\n"
        "📌 `/geeks` - GeeksforGeeks resources"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "💡 **Need a hand? I got you!**\n\n"
        "You can control me using these standard commands:\n"
        "• `/start` - Restart the conversation and greetings\n"
        "• `/youtube` - Go straight to YouTube\n"
        "• `/linkedin` - View LinkedIn profile\n"
        "• `/gmail` - Shoot an email over\n"
        "• `/geeks` - Read up on GeeksforGeeks articles"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def gmail_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📧 **Gmail Ready:** Click here to check your inbox or drop a mail: [Google Mail](https://mail.google.com/)", parse_mode='Markdown')

async def youtube_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺 **Time for some videos!** Open [YouTube](https://www.youtube.com/) and lock in.", parse_mode='Markdown')

async def linkedIn_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 **Networking mode on!** Check out the professional profile here: [LinkedIn](https://www.linkedin.com/)", parse_mode='Markdown')

async def geeks_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤓 **Coding time!** Here is your link to read up and practice logic: [GeeksforGeeks](https://www.geeksforgeeks.org/)", parse_mode='Markdown')

async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤔 **Oops, wait lang!** Hindi ko pa masyadong gets yung regular text na pinasa mo: *'%s'*\n\n"
        "Try using actual slash commands like `/help` or `/start` para smooth!" % update.message.text,
        parse_mode='Markdown'
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ **Hala, invalid command!** \n"
        "Walang command na *'%s'* sa system list natin. Subukan mong tingnan ang `/help` para sa tamang syntax." % update.message.text,
        parse_mode='Markdown'
    )

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("youtube", youtube_url))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("linkedin", linkedIn_url))
app.add_handler(CommandHandler("gmail", gmail_url))
app.add_handler(CommandHandler("geeks", geeks_url))

app.add_handler(MessageHandler(filters.COMMAND, unknown))
app.add_handler(MessageHandler(filters.TEXT, unknown_text))

# Function to run the bot
def run_bot():
    print("Bot is starting...")
    app.run_polling()

# Run both the bot and Flask server
if __name__ == "__main__":
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=lambda: flask_app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Flask server started on port 10000")
    
    # Run the bot in the main thread
    run_bot()