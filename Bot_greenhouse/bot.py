from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7607901680:AAGvfP5AABJcuuP-qJNwFnpzYBryGbzusbY"
WEB_APP_URL = "https://ya.ru"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(text="START", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Нажми кнопку START, чтобы открыть приложение 👇",
        reply_markup=reply_markup
    )

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    print("Бот запущен. Нажми Ctrl+C для остановки.")
    application.run_polling()

if __name__ == "__main__":
    main()
