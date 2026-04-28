import os
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

BOT_TOKEN = os.environ["BOT_TOKEN"]
YUKASSA_TOKEN = os.environ["YUKASSA_TOKEN"]

GUIDE = {
    "title": "Гайд по планировке",
    "description": "Как сделать удобный интерьер без ошибок",
    "price": 990
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Купить гайд", callback_data="buy")]
    ]

    await update.message.reply_text(
        "Привет! Нажмите, чтобы купить гайд 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

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

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def success(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Оплата прошла ✅")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, success))

    # ВАЖНО: только это, без asyncio
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
