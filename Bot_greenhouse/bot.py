from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

BOT_TOKEN = "7607901680:AAGvfP5AABJcuuP-qJNwFnpzYBryGbzusbY"
WEB_APP_URL = "https://greenhouse-nu.vercel.app/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🍅 *Добро пожаловать в "Теплицу"!* 🌱

Мы - кафе с домашней кухней, где каждый найдет что-то по вкусу:
• Полезные завтраки
• Сытные бизнес-ланчи
• Свежие полуфабрикаты с собой
• Блюда для особых диет

*Давайте подберем идеальный вариант для вас!*
"""
    
    keyboard = [
        [KeyboardButton("🍽️ Открыть меню", web_app=WebAppInfo(url=WEB_APP_URL))],
        [KeyboardButton("🌱 У меня особые предпочтения")],
        [KeyboardButton("🕒 Что сегодня свежее?")],
        [KeyboardButton("📍 Где вы находитесь?")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🌱 У меня особые предпочтения":
        response = """
*Укажите ваши предпочтения:*
1. Вегетарианское
2. Веганское
3. Безглютеновое
4. Низкоуглеводное
5. Другое (уточню в чате)

Или просто нажмите "🍽️ Открыть меню" для фильтрации вариантов.
"""
        await update.message.reply_text(response, parse_mode="Markdown")
    elif text == "🕒 Что сегодня свежее?":
        response = "Сегодня особо рекомендуем:\n• Сырники с малиной (безглютеновые)\n• Тыквенный крем-суп\n• Сет 'Фермерский' с котлетой из нута\n\nПолный список в меню 👇"
        await update.message.reply_text(response)
    elif text == "📍 Где вы находитесь?":
        response = "Мы находимся в офисе 2ГИС, 1 этаж.\nРаботаем Пн-Пт с 8:00 до 18:00.\n\nХотите забронировать столик?"
        await update.message.reply_text(response)
    else:
        await start(update, context)

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот 'Теплица' запущен и готов к работе 🌿")
    application.run_polling()

if __name__ == "__main__":
    main()