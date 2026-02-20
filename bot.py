from telebot import types, TeleBot
from telebot.callback_data import CallbackData, CallbackDataFilter

from pole import *
from database import GameDatabase

import configparser
config = configparser.ConfigParser()
config.read("config.ini")

bot = TeleBot(config["Telegram"]["TOKEN"])
db = GameDatabase()

CURRENT_GAMES = {}

dictionaries_factory = CallbackData('dict_name', prefix="dict")
def dictionaries_keyboard():
  return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=INI_DICTIONARIES[d]["visible_name"],
                    callback_data=dictionaries_factory.new(dict_name=d)
                )
            ]
            for d in INI_DICTIONARIES
        ]
    )


@bot.message_handler(commands=["top"])
def top_handler(message: types.Message):
  '''
  Отравляет топ-15 игроков чата
  '''
  top_list = db.get_top_points(message.chat.id)
  bot.send_message(chat_id=message.chat.id, text="\n".join(f"@{username}: {points}" for username, points in top_list))


@bot.message_handler(commands=["start", "play"])
def start_game_handler(message: types.Message):
  '''
  Начало игры, отзывается на /start и /play
  '''
  bot.send_message(message.chat.id, text=f"Начало игры!\n\nВыберите тему", reply_markup=dictionaries_keyboard())

@bot.callback_query_handler(func=None)
def dictionary_callback(call: types.CallbackQuery):
  callback_data: dict = dictionaries_factory.parse(callback_data=call.data)
  game = PoleGame(callback_data['dict_name'])
  CURRENT_GAMES[call.message.chat.id] = game
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Начало игры!\n\n{game.print_word()}\n\nТема: {game.theme}")


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
      db.change_points(message.from_user.username, message.from_user.id, message.chat.id, -2)
  elif len(message.text) > 1:
    if len(str.split(message.text)) == 1:
      if not game.check_word(str.lower(message.text)):
        bot.send_message(message.chat.id, f"Слово {str.upper(message.text)} неверное!\n\n-2 очка\n\n{str.upper(game.print_word())}")
        db.change_points(message.from_user.username, message.from_user.id, message.chat.id, -2)
  if game.end:
    bot.send_message(message.chat.id, f"Конец игры!\n\nЗагаданное слово: {str.upper(game.print_word())}\n\n+15 очков @{message.from_user.username}!")
    db.change_points(message.from_user.username, message.from_user.id, message.chat.id, 15)
    del CURRENT_GAMES[message.chat.id]


bot.infinity_polling()
del db