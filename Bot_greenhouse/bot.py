import requests
from requests.exceptions import RequestException
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters, ConversationHandler
from dotenv import load_dotenv

# Состояния для ConversationHandler
WAITING_FOR_PREFERENCES = 1

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")
BAKEND_URL = os.getenv("BAKEND_URL")


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
    return ConversationHandler.END

async def handle_preferences_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = """
*Укажите ваши предпочтения, аллергии или другие ограничения по питанию*
Например: "Веган, аллергия на орехи" или "Без лактозы"
"""
    await update.message.reply_text(response, parse_mode="Markdown")
    return WAITING_FOR_PREFERENCES

async def handle_preferences_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_preferences = update.message.text
    
    try:
        # Формируем данные точно по формату, который ожидает бэкенд
        payload = {
            "id": str(update.effective_user.id),  # Преобразуем ID в строку
            "restrictions": user_preferences
        }
        
        # Отправляем запрос с теми же заголовками, что и в curl
        response = requests.post(
            f"{BAKEND_URL}/users",
            json=payload,
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            timeout=5
        )
        
        # Проверяем статус ответа
        response.raise_for_status()
        
        # Логируем успешный запрос
        print(f"Успешный запрос к бэкенду. Ответ: {response.json()}")
        
        answer = "✅ Спасибо! Мы учтем ваши предпочтения"
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к бэкенду: {str(e)}")
        answer = "⚠️ Произошла ошибка при сохранении предпочтений. Попробуйте позже."
    
    await update.message.reply_text(answer, parse_mode="Markdown")
    await start(update, context)
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🌱 У меня особые предпочтения":
        return await handle_preferences_start(update, context)
    elif text == "🕒 Что сегодня свежее?":
        response = "Сегодня особо рекомендуем:\n• Сырники с малиной (безглютеновые)\n• Тыквенный крем-суп\n• Сет 'Фермерский' с котлетой из нута\n\nПолный список в меню 👇"
        await update.message.reply_text(response)
    elif text == "📍 Где вы находитесь?":
        response = "Мы находимся в офисе 2ГИС, 1 этаж.\nРаботаем Пн-Пт с 8:00 до 18:00.\n\nХотите забронировать столик?"
        await update.message.reply_text(response)
    else:
        await start(update, context)
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        ],
        states={
            WAITING_FOR_PREFERENCES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_preferences_input)
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    print("Бот 'Теплица' запущен и готов к работе 🌿")
    application.run_polling()

if __name__ == "__main__":
    main()