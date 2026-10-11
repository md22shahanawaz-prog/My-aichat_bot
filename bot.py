import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# 1. Create a dummy website server to keep Render Free tier happy
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. Configure the Gemini AI & Telegram Bot
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Sorry, I encountered an error processing that.")

if __name__ == "__main__":
    # Start the dummy web server in the background
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("Bot is up and running...")
    bot.infinity_polling()
