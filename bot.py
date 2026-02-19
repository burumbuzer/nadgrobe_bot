from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter

from pole import PoleGame

import configparser
config = configparser.ConfigParser()
config.read("config.ini")

bot = TeleBot(config["Telegram"]["TOKEN"].replace("'", "").replace('"', ''))

CURRENT_GAMES = {}

@bot.message_handler(commands=["start"])
def start_game_handler(message: types.Message):
  game = PoleGame()
  CURRENT_GAMES[message.chat.id] = game
  bot.send_message(message.chat.id, text=f"Начало игры!\n\n{game.printWord()}")

@bot.message_handler(content_types=["text"])
def process_game_handler(message: types.Message):
  if message.chat.id in CURRENT_GAMES:
    game = CURRENT_GAMES[message.chat.id]
  else:
    return
  
  if len(message.text) == 1:
    if game.checkLetter(str.lower(message.text)) and not game.end:
      bot.send_message(message.chat.id, f"Буква {str.upper(message.text)} есть в слове!\n\n{str.upper(game.printWord())}")
    elif not game.checkLetter(str.lower(message.text)):
      bot.send_message(message.chat.id, f"Буквы {str.upper(message.text)} нет в слове!\n\n{str.upper(game.printWord())}")
  elif len(message.text) > 1:
    if len(str.split(message.text)) == 1:
      if not game.checkWord(str.lower(message.text)):
        bot.send_message(message.chat.id, f"Слово {str.upper(message.text)} неверное!\n\n{str.upper(game.printWord())}")

  if game.end:
    bot.send_message(message.chat.id, f"Конец игры!\n\nЗагаданное слово: {str.upper(game.printWord())}\n\nПлюс 52 балла юзеру @{message.from_user.username}!")
    del CURRENT_GAMES[message.chat.id]



bot.infinity_polling()