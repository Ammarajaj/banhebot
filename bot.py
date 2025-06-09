from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = '7809016240:AAEoGRzXHBJpgdLrfx3KpJjzlOjXK2xnaVI'

BLOCKED_BOTS = ['hebot', 'whisperbot', 'anybot'] 

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message:
        print(f"📥 رسالة من: {message.from_user.username}")
        
        if message.via_bot:
            via_bot_username = message.via_bot.username.lower()
            print(f"🤖 الرسالة مرسلة عبر بوت: {via_bot_username}")

            if via_bot_username in BLOCKED_BOTS:
                try:
                    await message.delete()
                    print(f"🗑️ تم حذف رسالة من البوت المحظور: {via_bot_username}")
                except Exception as e:
                    print(f"❌ خطأ أثناء الحذف: {e}")
        else:
             print(f"ليست همسة {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, handle))

    print("🚀 البوت يعمل الآن...")
    app.run_polling()

if __name__== "__main__":
    main()