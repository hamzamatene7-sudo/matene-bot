from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

NAME, NETWORK, AMOUNT = range(3)

TOKEN = "8669945097:AAEG042Mbnfo-RJOBklmR_tn_rUc3SB5UaM"
ADMIN_ID = 7481000246


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبا بيك في Matene Phone VIP 👋\n\nأدخل اسمك:"
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    keyboard = [
        [KeyboardButton("موبيليس")],
        [KeyboardButton("جيزي")],
        [KeyboardButton("أوريدو")],
    ]

    await update.message.reply_text(
        "اختار الشبكة:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

    return NETWORK


async def get_network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["network"] = update.message.text

    keyboard = [
        [KeyboardButton("5000 دج"), KeyboardButton("10000 دج")],
        [KeyboardButton("15000 دج"), KeyboardButton("20000 دج")],
        [KeyboardButton("25000 دج"), KeyboardButton("30000 دج")],
    ]

    await update.message.reply_text(
        "اختار المبلغ:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

    return AMOUNT


async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text

    name = context.user_data["name"]
    network = context.user_data["network"]

    text = f"""
🔥 طلب جديد

👤 الاسم: {name}
📶 الشبكة: {network}
💰 المبلغ: {amount}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )

    await update.message.reply_text(
        "✅ تم إرسال الطلب بنجاح\n\n"
        "لإرسال طلب جديد اضغط /start"
    )

    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)
            ],
            NETWORK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_network)
            ],
            AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)
            ],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()