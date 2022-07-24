import telebot
import json
from templates.funcs import *

with open("token.txt", "r") as raw_token:
    token = raw_token.readlines()[0]

with open("texts.json", "r", encoding="utf-8") as raw_texts:
    texts = json.load(raw_texts)

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):

    bot.send_message(message.chat.id, texts["start"]["ua"], parse_mode="HTML")

def run(non_stop: bool) -> None:

    bot.polling(non_stop=non_stop)