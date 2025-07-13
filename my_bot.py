from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# Читаем токен из переменной окружения
TOKEN = os.environ.get("BOT_TOKEN")

# Пути к папкам с файлами и картинками
FAQ_TEXTS_DIR = os.path.join(os.getcwd(), 'faq_texts')
FAQ_PHOTOS_DIR = os.path.join(os.getcwd(), 'faq_photos')

# Главное меню
MAIN_MENU = [
    ['📚 1️⃣ Часто задаваемые вопросы', '📞 2️⃣ Контакты'],
    ['🛒 3️⃣ Где купить', '🎁 4️⃣ Сертификаты'],
    ['💊 5️⃣ Чем NL отличается от аптеки?']
]

# Меню FAQ
FAQ_MENU = [
    'Где производится продукция?',
    'Что такое ED Smart?',
    'Чем ED Smart отличается от обычного протеина?',
    'Есть ли продукция для женского здоровья?',
    'Можно ли давать продукцию детям?',
    'Как выбрать продукцию под себя?',
    'Что такое DrainEffect и как он работает?',
    'Есть ли продукция для иммунитета?',
    'Есть ли продукция для мужчин?',
    'Есть ли продукция для очищения организма?',
    'Есть ли продукты для животных?',
    'Почему продукция NL такая дорогая?',
    'БАД — это химия?'
]

FAQ_QUESTIONS_TO_FILE = {
    'Где производится продукция?': 'faq_1.txt',
    'Что такое ED Smart?': 'faq_2.txt',
    'Чем ED Smart отличается от обычного протеина?': 'faq_3.txt',
    'Есть ли продукция для женского здоровья?': 'faq_4.txt',
    'Можно ли давать продукцию детям?': 'faq_5.txt',
    'Как выбрать продукцию под себя?': 'faq_6.txt',
    'Что такое DrainEffect и как он работает?': 'faq_7.txt',
    'Есть ли продукция для иммунитета?': 'faq_8.txt',
    'Есть ли продукция для мужчин?': 'faq_9.txt',
    'Есть ли продукция для очищения организма?': 'faq_10.txt',
    'Есть ли продукты для животных?': 'faq_11.txt',
    'Почему продукция NL такая дорогая?': 'faq_12.txt',
    'БАД — это химия?': 'faq_13.txt',
}

FAQ_QUESTIONS_TO_IMAGES = {
    'Что такое ED Smart?': ['faq_2.jpg'],
    'Есть ли продукция для женского здоровья?': ['faq_4_1.jpg', 'faq_4_2.jpg', 'faq_4_3.jpg', 'faq_4_4.jpg', 'faq_4_5.jpg'],
    'Можно ли давать продукцию детям?': ['faq_5.jpg'],
    'Что такое DrainEffect и как он работает?': ['faq_7.jpg'],
    'Есть ли продукция для иммунитета?': ['faq_8_1.jpg', 'faq_8_2.jpg', 'faq_8_3.jpg'],
    'Есть ли продукция для мужчин?': ['faq_9.jpg'],
    'Есть ли продукты для животных?': ['faq_11.jpg'],
}

CONTACTS_TEXT = (
    "📞 Мои контакты:\n"
    "— Telegram: @nikkushka\n"
    "— Телефон: +375 29 338 42 39 (WhatsApp/Viber)\n"
    "— Instagram: @nikkussyaa\n\n"
    "💬 Как со мной связаться:\n"
    "— По вопросам заказов — в личные сообщения (Telegram/WhatsApp/Viber/Instagram).\n"
    "— Отзывы и результаты — можно в общий чат!"
)

WHERE_TO_BUY_TEXT = (
    "🔗 Официальный магазин NL:\n"
    "https://ng.nlstar.com\n\n"
    "🛒 Как оформить заказ:\n"
    "1. Зарегистрируйся на сайте.\n"
    "2. Укажи ID партнёра: 375-6632182\n"
    "3. Выбери продукты и оформи заказ.\n"
    "4. Получай кэшбэк до 10% с каждой покупки!"
)

CERTIFICATES_TEXT = (
    "🌸 Все продукты NL проходят строгую сертификацию и соответствуют международным стандартам качества!\n\n"
    "🔹 Как проверить сертификаты?\n"
    "1️⃣ Перейди на страницу любого продукта на сайте.\n"
    "2️⃣ В разделе «Документы» — сертификаты, декларации и др.\n\n"
    "💡 Пример:\n"
    "— Lactoferra: https://ng.nlstar.com/ru/product/73604"
)

NL_VS_PHARMACY_TEXT = (
    "🌿 NL vs Аптека: выбирай осознанно\n\n"
    "✅ 1. Состав, который работает\n"
    "✅ 2. Комплексный подход\n"
    "✅ 3. Качество и безопасность\n"
    "💬 Отзывы клиентов: «NL — через 2 недели кожа сияет!»"
)

def main_menu_keyboard():
    return ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)

def faq_menu_keyboard():
    buttons = [[q] for q in FAQ_MENU]
    buttons.append(['Назад', 'Меню'])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def back_menu_keyboard():
    return ReplyKeyboardMarkup([['Назад', 'Меню']], resize_keyboard=True)

def read_faq_text(filename):
    try:
        with open(os.path.join(FAQ_TEXTS_DIR, filename), 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return "Извините, ответ временно недоступен."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🌸 Привет! Я — @VNLhelperbot_ \n"
        "Твой помощник по продукции NL.\n\n"
        "💡 Я умею:\n"
        "— Отвечать на вопросы\n"
        "— Подсказывать, где купить\n"
        "— Рассказывать о составе, сертификатах и т.д.\n\n"
        "✨ Выбери интересующий раздел:"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == '📚 1️⃣ Часто задаваемые вопросы':
        await update.message.reply_text('📌 Выбери вопрос:', reply_markup=faq_menu_keyboard())
        return
    elif text == '📞 2️⃣ Контакты':
        await update.message.reply_text(CONTACTS_TEXT, reply_markup=back_menu_keyboard())
        return
    elif text == '🛒 3️⃣ Где купить':
        await update.message.reply_text(WHERE_TO_BUY_TEXT, reply_markup=back_menu_keyboard())
        return
    elif text == '🎁 4️⃣ Сертификаты':
        await update.message.reply_text(CERTIFICATES_TEXT, reply_markup=back_menu_keyboard())
        return
    elif text == '💊 5️⃣ Чем NL отличается от аптеки?':
        await update.message.reply_text(NL_VS_PHARMACY_TEXT, reply_markup=back_menu_keyboard())
        return

    if text in FAQ_MENU:
        filename = FAQ_QUESTIONS_TO_FILE.get(text)
        if not filename:
            await update.message.reply_text("Извините, ответ временно недоступен.", reply_markup=faq_menu_keyboard())
            return

        answer_text = read_faq_text(filename)
        photos = FAQ_QUESTIONS_TO_IMAGES.get(text)
        if photos:
            media_group = []
            for photo_name in photos:
                photo_path = os.path.join(FAQ_PHOTOS_DIR, photo_name)
                if os.path.isfile(photo_path):
                    media_group.append(InputMediaPhoto(open(photo_path, 'rb')))
            if media_group:
                await update.message.reply_text(answer_text)
                await update.message.reply_media_group(media_group)
                return

        await update.message.reply_text(answer_text, reply_markup=faq_menu_keyboard())
        return

    if text == 'Назад':
        await update.message.reply_text('📌 Выбери вопрос:', reply_markup=faq_menu_keyboard())
        return
    if text == 'Меню':
        await update.message.reply_text('Вы вернулись в главное меню.', reply_markup=main_menu_keyboard())
        return

    await update.message.reply_text(
        "Извините, я не понимаю этот запрос.\nПожалуйста, выберите кнопку из меню.",
        reply_markup=main_menu_keyboard()
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_message))

    PORT = int(os.environ.get('PORT', 8443))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://telegram-nl-bot.onrender.com/{TOKEN}"
    )
