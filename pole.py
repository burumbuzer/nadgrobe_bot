import random

DICT = ["манул", "ирбис", "горностай"]

class PoleGame():
  word: str
  guessedLetters: list[str]
  end: bool

  def __init__(self):
    self.word = random.choice(DICT)
    self.guessedLetters = []
    self.end = False

  def checkLetter(self, letter: str) -> bool:
    if letter in self.word:
      self.guessedLetters.append(letter)
      if len(self.word) == len(self.guessedLetters):
        self.end = True
      return True
    else:
      return False
  
  def checkWord(self, word: str) -> bool:
    if str.lower(word)==str.lower(self.word):
      self.end = True
      self.guessedLetters = [c for c in self.word]
      return True
    else:
      return False
    
  def printWord(self) -> str:
    return "".join(c if c in self.guessedLetters else "■" for c in self.word)