
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from admin_tools import add_test, list_tests, remove_test
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 564085453

TEST_NAME, TEST_ANSWERS = range(2)
pending_tests = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum!\n/test yoki /check orqali foydalanishingiz mumkin.")

async def addtest_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("Faqat admin qo‘shishi mumkin.")
    await update.message.reply_text("Yangi test nomini kiriting:")
    return TEST_NAME

async def addtest_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pending_tests[update.effective_user.id] = {"name": update.message.text}
    await update.message.reply_text("Endi test javoblarini kiriting (masalan: ABCDBAD...):")
    return TEST_ANSWERS

async def addtest_answers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    test_info = pending_tests.get(update.effective_user.id, {})
    name = test_info.get("name")
    answers = update.message.text
    add_test(name, answers)
    await update.message.reply_text(f"✅ Test "{name}" muvaffaqiyatli qo‘shildi.")
    return ConversationHandler.END

async def list_all_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    tests = list_tests()
    await update.message.reply_text("Testlar ro‘yxati:\n" + "\n".join(tests) if tests else "Hech qanday test yo‘q.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    addtest_conv = ConversationHandler(
        entry_points=[CommandHandler("addtest", addtest_start)],
        states={
            TEST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, addtest_name)],
            TEST_ANSWERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, addtest_answers)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(addtest_conv)
    app.add_handler(CommandHandler("listtests", list_all_tests))

    app.run_polling()
