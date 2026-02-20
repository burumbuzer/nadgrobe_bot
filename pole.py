import random
import configparser
INI_DICTIONARIES = configparser.ConfigParser()
INI_DICTIONARIES.read("dictionaries.ini", encoding="utf-8")
INI_DICTIONARIES = INI_DICTIONARIES._sections


# Загрузка словарей из файлов
DICTIONARIES = {}
for d in INI_DICTIONARIES: 
  with open(f"dicts\{INI_DICTIONARIES[d]['file']}", "r", encoding="utf-8") as file: # логгер + обработка ошибок
    process_dict = file.readlines()
  process_dict = [w.strip("\n") for w in process_dict]
  DICTIONARIES[d] = process_dict


class PoleGame():
  word: str
  guessedLetters: list[str]
  end: bool
  theme: str

  def __init__(self, dict_name: str):
    if dict_name not in DICTIONARIES:
      pass # логгер + обработка ошибок
    self.word = random.choice(DICTIONARIES[dict_name])
    self.guessedLetters = []
    self.end = False
    self.theme = INI_DICTIONARIES[dict_name]["visible_name"]

  def check_letter(self, letter: str) -> bool:
    if letter in self.word:
      self.guessedLetters.append(letter)
      if len(self.word) == len(self.guessedLetters):
        self.end = True
      return True
    else:
      return False
  
  def check_word(self, word: str) -> bool:
    if str.lower(word)==str.lower(self.word):
      self.end = True
      self.guessedLetters = [c for c in self.word]
      return True
    else:
      return False
    
  def print_word(self) -> str:
    return "".join(c if c in self.guessedLetters else "■" for c in self.word)