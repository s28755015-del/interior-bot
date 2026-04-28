import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, PreCheckoutQueryHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
YUKASSA_TOKEN = os.environ["YUKASSA_TOKEN"]

GUIDES = {
    "guide_1": {
        "title": "Гайд по цвету в интерьере",
        "description": "Как подбирать цвета и не ошибиться",
        "price": 990,
        "file_id": None,
    },
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"📘 {g['title']} — {g['price']}₽", callback_data=key)] for key, g in GUIDES.items()]
    await update.message.reply_text("Выберите гайд 👇", reply_markup=InlineKeyboardMarkup(keyboard))

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

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guide_key = update.message.successful_payment.invoice_payload
    guide = GUIDES.get(guide_key)
    await update.message.reply_text("✅ Оплата прошла! Отправляю гайд...")
    if guide and guide["file_id"]:
        await context.bot.send_document(chat_id=update.message.chat_id, document=guide["file_id"])
    else:
        await update.message.reply_text("Напишите мне в личку и я пришлю гайд вручную 🙏")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
