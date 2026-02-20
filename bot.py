from telebot import types, TeleBot

from pole import *

import configparser
config = configparser.ConfigParser()
config.read("config.ini")

bot = TeleBot(config["Telegram"]["TOKEN"])

CURRENT_GAMES = {}


@bot.message_handler(commands=["start", "play"])
def start_game_handler(message: types.Message):
  '''
  Начало игры, отзывается на /start и /play
  '''
  game = PoleGame("test")
  CURRENT_GAMES[message.chat.id] = game
  bot.send_message(message.chat.id, text=f"Начало игры!\n\n{game.print_word()}")


@bot.message_handler(func=lambda message: message.chat.id in CURRENT_GAMES, content_types=["text"])
def process_game_handler(message: types.Message):
  '''
  Процесс игры, срабатывает если игра была запущена в этом чате командами выше
  '''
  if message.chat.id in CURRENT_GAMES:
    game = CURRENT_GAMES[message.chat.id]
  else:
    return
  
  if len(message.text) == 1:
    if game.check_letter(str.lower(message.text)) and not game.end:
      bot.send_message(message.chat.id, f"Буква {str.upper(message.text)} есть в слове!\n\n{str.upper(game.print_word())}")
    elif not game.check_letter(str.lower(message.text)):
      bot.send_message(message.chat.id, f"Буквы {str.upper(message.text)} нет в слове!\n\n{str.upper(game.print_word())}")
  elif len(message.text) > 1:
    if len(str.split(message.text)) == 1:
      if not game.check_word(str.lower(message.text)):
        bot.send_message(message.chat.id, f"Слово {str.upper(message.text)} неверное!\n\n{str.upper(game.print_word())}")

  if game.end:
    bot.send_message(message.chat.id, f"Конец игры!\n\nЗагаданное слово: {str.upper(game.print_word())}\n\nПлюс 52 балла юзеру @{message.from_user.username}!")
    del CURRENT_GAMES[message.chat.id]



bot.infinity_polling()