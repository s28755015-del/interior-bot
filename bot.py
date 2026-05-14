import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
YUKASSA_TOKEN = os.environ["YUKASSA_TOKEN"]

GUIDES = {
    "guide_1": {
        "title": "Эргономика и планировка интерьера",
        "description": "Как грамотно распланировать пространство и избежать ошибок",
        "price": 150,
        "file_id": "BQACAgIAAxkBAAMxagGz568rXfWa7bPe_-n3D4LBG7kAAsOhAAJM5wlI87vG4qVZCOM7BA",
    },
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            f"📘 {GUIDES['guide_1']['title']} — {GUIDES['guide_1']['price']}₽",
            callback_data="guide_1"
        )]
    ]

    await update.message.reply_text(
        "Привет! Выбери продукт 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    guide = GUIDES.get(query.data)
    if not guide:
        return

    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title=guide["title"],
        description=guide["description"],
        payload=query.data,
        provider_token=YUKASSA_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(guide["title"], guide["price"] * 100)],
    )

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guide = GUIDES["guide_1"]

    await update.message.reply_text("✅ Оплата прошла успешно! Отправляю PDF 👇")

    await context.bot.send_document(
        chat_id=update.message.chat_id,
        document=guide["file_id"]
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    app.run_polling()

if __name__ == "__main__":
    main()
