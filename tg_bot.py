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

# --- PROFESSIONAL HANDLER FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "💼 **Welcome to your Professional Routine & Assistant Bot.**\n\n"
        "This bot is configured to assist with your daily workflows, tasks, and reference links. "
        "Please use the following commands to navigate the platform:\n\n"
        "📌 `/help` - View the directory of all available commands\n"
        "📌 `/github` - Access version control repositories and source code\n"
        "📌 `/linkedin` - Open the professional profile\n"
        "📌 `/reddit` - Access the configured platform profile"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "💡 **Command Directory & Help Center**\n\n"
        "You can manage your workflows using these verified parameters:\n"
        "• `/start` - Reinitialize the system and view welcoming options\n"
        "• `/help` - Display this command instruction panel\n"
        "• `/github` - Redirect to the target GitHub development account\n"
        "• `/linkedin` - View the configured LinkedIn networking profile\n"
        "• `/reddit` - Direct link to open the target Reddit network page"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def reddit_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗣️ **Platform Redirect:** Click the following link to view the configured profile: [Reddit](https://www.reddit.com/user/angeline30/)", parse_mode='Markdown')

async def github_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💻 **Source Code Repository:** Click the following link to view deployment projects: [GitHub](https://github.com/joeserrato)", parse_mode='Markdown')

async def linkedIn_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💼 **Professional Profile:** Click the following link to view the networking registry: [LinkedIn](https://www.linkedin.com/in/joeangelineserrato/)", parse_mode='Markdown')

async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ **System Notification:** Standard text parsing is not configured for: *'%s'*\n\n"
        "Please input a verified system slash command (e.g., `/help` or `/start`) to continue." % update.message.text,
        parse_mode='Markdown'
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ **Invalid Command Execution:** \n"
        "The command *'%s'* is unrecognized by the core application. Please review the `/help` documentation for proper command structures." % update.message.text,
        parse_mode='Markdown'
    )

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("github", github_url))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("linkedin", linkedIn_url))
app.add_handler(CommandHandler("reddit", reddit_url))

app.add_handler(MessageHandler(filters.COMMAND, unknown))
app.add_handler(MessageHandler(filters.TEXT, unknown_text))

# Function to run the bot
def run_bot():
    print("Bot application starting...")
    app.run_polling()

# Run both the bot and Flask server
if __name__ == "__main__":
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=lambda: flask_app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Flask server running securely on port 10000")
    
    # Run the bot in the main thread
    run_bot()