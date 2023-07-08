import telebot
from telebot import types
import json

bot = telebot.TeleBot("655146488:AAHe6uGJ77kUFe3Y1XnsPIIjTDhXCUg2BDY")
CHANNEL_ID = -1001199050800

# Load texts from the file
with open("text.txt", "r", encoding="utf-8") as file:
    texts = json.load(file)

# Language buttons
language_buttons = {
    'ru': 'Русский 🇷🇺',
    'en': 'English 🇺🇸'
}

# Define the language keyboard
def get_language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*language_buttons.values())
    return keyboard

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        language = 'ru'
        bot.send_message(chat_id, texts[language]['welcome'], reply_markup=get_language_keyboard())
    except Exception as e:
        print(e)

# Handle language selection
@bot.message_handler(func=lambda message: message.text in language_buttons.values())
def select_language(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        language = 'ru' if message.text == language_buttons['ru'] else 'en'
        member = bot.get_chat_member(CHANNEL_ID, user_id)

        if member.status in ['member', 'administrator', 'creator']:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.row(texts[language]['watch_stream'], texts[language]['donate'])
            bot.reply_to(message, texts[language]['subscribed'], reply_markup=keyboard)
        else:
            bot.reply_to(message, texts[language]['not_subscribed'])
    except telebot.apihelper.ApiException as e:
        if e.result.status_code == 403 and "Forbidden: bot was blocked by the user" in e.result.text:
            bot.reply_to(message, "Вы заблокировали меня. Пожалуйста, разблокируйте меня, чтобы я мог отправлять вам сообщения.")
        else:
            bot.reply_to(message, texts[language]['error'])
    except Exception as e:
        print(e)

# Handle "Watch the stream" button
@bot.message_handler(func=lambda message: message.text == texts['ru']['watch_stream'] or message.text == texts['en']['watch_stream'])
def watch_stream(message):
    chat_id = message.chat.id

    try:
        language = 'ru' if message.text == texts['ru']['watch_stream'] else 'en'
        stream_description = texts[language]['stream_description']
        stream_url = texts[language]['stream_here'] + " t.me/temp290?livestream"
        bot.send_message(chat_id, stream_description)
        bot.send_sticker(chat_id, "CAACAgIAAxkBAAEJjR5koEBWkkiVjuccUz8jkav4piWR7wACQAEAAvbGuQl7xojgceriay8E")
        bot.send_message(chat_id, stream_url)

    except Exception as e:
        print(e)

# Handle "Donate" button
@bot.message_handler(func=lambda message: message.text == texts['ru']['donate'] or message.text == texts['en']['donate'])
def donate(message):
    chat_id = message.chat.id

    try:
        language = 'ru' if message.text == texts['ru']['donate'] else 'en'
        channel_message = bot.forward_message(chat_id, CHANNEL_ID, message_id=119)

        if channel_message.text:
            bot.send_message(chat_id, texts[language]['donate'])
            bot.send_message(chat_id, channel_message.text)
        else:
            bot.send_message(chat_id, texts[language]['support_me'])
    except Exception as e:
        print(e)

# Start the bot
try:
    bot.polling()
except Exception as e:
    print(e)
