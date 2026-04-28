import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
YUKASSA_TOKEN = os.environ["YUKASSA_TOKEN"]

GUIDE = {
    "title": "Гайд по эргономике и планировке",
    "description": "Как сделать удобную квартиру без ошибок",
    "price": 990,
    "file_id": None
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"📘 Купить гайд — {GUIDE['price']}₽", callback_data="buy")]
    ]

    await update.message.reply_text(
        "Привет! Здесь вы можете купить гайд 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# кнопка купить
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title=GUIDE["title"],
        description=GUIDE["description"],
        payload="guide_1",
        provider_token=YUKASSA_TOKEN,
        currency="RUB",
        prices=[LabeledPrice("Гайд", GUIDE["price"] * 100)],
    )

# подтверждение оплаты
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

# после оплаты
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Оплата прошла! Вот ваш гайд 👇")

    if GUIDE["file_id"]:
        await context.bot.send_document(
            chat_id=update.message.chat_id,
            document=GUIDE["file_id"]
        )
    else:
        await update.message.reply_text(
            "Файл пока не прикреплён. Добавьте file_id в код."
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    # ВАЖНО: polling для Render (не webhook)
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
