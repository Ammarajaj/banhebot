import os
import nest_asyncio
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import threading

# حل مشكلة تداخل event loops
nest_asyncio.apply()

BOT_TOKEN = os.environ.get('BOT_TOKEN', '7809016240:AAEoGRzXHBJpgdLrfx3KpJjzlOjXK2xnaVI')
BLOCKED_BOTS = ['HEBot', 'whisperbot', 's8ebot']

# Flask app
app = Flask(name)

@app.route('/')
def home():
    return "🤖 البوت يعمل بشكل صحيح! 🚀"

# Telegram handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message:
        print(f"📥 رسالة من: {message.from_user.username}")
        if message.via_bot:
            via_bot_username = message.via_bot.username.lower()
            print(f"🤖 الرسالة مرسلة عبر بوت: {via_bot_username}")
            if via_bot_username in [bot.lower() for bot in BLOCKED_BOTS]:
                try:
                    await message.delete()
                    print(f"🗑️ تم حذف رسالة من البوت المحظور: {via_bot_username}")
                except Exception as e:
                    print(f"❌ خطأ أثناء الحذف: {e}")
        else:
            print("رسالة عادية (ليست عبر بوت)")

# تشغيل Flask في Thread منفصل
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# الوظيفة الأساسية لتشغيل البوت
async def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.ALL, handle))
    print("🚀 البوت بدأ التشغيل...")
    await app_bot.run_polling()

# هذا الجزء يتعامل مع تشغيل asyncio داخل بيئات مثل Replit
if name== "main":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "asyncio.run() cannot be called from a running event loop" in str(e):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise