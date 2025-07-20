
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

API_TOKEN = "7606743572:AAE2AZxcHSn86P1s1Nt8haLYs1drbWK8sdM"
ADMIN_ID = 564085453

bot = telebot.TeleBot(API_TOKEN)

# Test kalitlarini saqlash
test_answers = {}

# Keyboard
menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
menu_markup.row(KeyboardButton("📄 Test ishlash"), KeyboardButton("✅ Testni tekshirish"))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Nimani xohlaysiz?", reply_markup=menu_markup)

@bot.message_handler(commands=['add_test'])
def add_test(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Faqat admin yangi test qo‘shishi mumkin.")
        return

    try:
        parts = message.text.split(maxsplit=2)
        test_id = parts[1]
        answers = parts[2].strip().upper()
        test_answers[test_id] = answers
        bot.reply_to(message, f"{test_id} test qo‘shildi. Kalit: {answers}")
    except:
        bot.reply_to(message, "❌ Format: /add_test test1 ABCDABCD...")

@bot.message_handler(func=lambda message: message.text == "📄 Test ishlash")
def send_test_pdf(message):
    # Hozircha PDF yo‘q – fayl bo‘lganida shundan yuboriladi
    bot.send_message(message.chat.id, "Hozircha hech qanday test PDF mavjud emas.")

@bot.message_handler(func=lambda message: message.text == "✅ Testni tekshirish")
def ask_for_answers(message):
    bot.send_message(message.chat.id, "Test ID va javoblaringizni kiriting. (Masalan: test1 ABCDCABDA...)")

@bot.message_handler(func=lambda message: True)
def handle_answers(message):
    try:
        parts = message.text.strip().split(maxsplit=1)
        test_id = parts[0]
        user_answers = parts[1].strip().upper()

        correct_answers = test_answers.get(test_id)
        if not correct_answers:
            bot.reply_to(message, f"{test_id} testi topilmadi.")
            return

        score = sum(1 for a, b in zip(user_answers, correct_answers) if a == b)
        total = len(correct_answers)
        bot.reply_to(message, f"✅ Natija: {score}/{total} ta to‘g‘ri.")

    except Exception as e:
        bot.reply_to(message, "❌ Noto‘g‘ri format. Masalan: test1 ABCDCABDA...")

bot.polling()
