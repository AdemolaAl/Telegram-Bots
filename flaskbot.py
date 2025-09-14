from flask import Flask, request

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Start command handler (/start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! 👋 I’m your simple Python bot.") 


async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    questions = ['a', 'b' , 'c' , 'd']
    await context.bot.send_poll(chat_id=update.effective_chat.id, question="What is your favorite letter?", options=questions, is_anonymous=False, allows_multiple_answers=False)

# Echo handler (repeats whatever you send)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"You said: {user_text}")



async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Google", url="https://google.com")],
        [InlineKeyboardButton("Say Hello", callback_data="hello")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # required
    if query.data == "hello":
        await query.edit_message_text(text="Hello from button! 👋")

def main():
    # Replace with your token from BotFather
    TOKEN = '7347291610:AAG3ng31egMHtIzoYejeDcnUQoyQL4MPYlA'

    # Create bot application
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))  # /start command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # echo messages
    app.add_handler(CommandHandler("poll", poll))  # /poll command

    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT, echo))  # keep echo
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
