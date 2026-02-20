import sqlite3

class GameDatabase():
  conn: sqlite3.Connection
  cursor: sqlite3.Cursor

  def __init__(self):
    self.conn = sqlite3.connect("game.db", check_same_thread=False)
    self.cursor = self.conn.cursor()
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS Users (
      id INTEGER PRIMARY KEY,
      username TEXT NOT NULL,
      telegram_id INTEGER NOT NULL,
      telegram_chat_id INTEGER NOT NULL,
      points INTEGER NOT NULL
      )
      ''')
    self.conn.commit()

  def __del__(self):
    self.conn.close()

  def change_points(self, username: str, telegram_id: int, telegram_chat_id: int, points: int):
    self.cursor.execute("SELECT points FROM Users WHERE telegram_id = ? and telegram_chat_id = ?", (telegram_id, telegram_chat_id))
    user_points_tuple = self.cursor.fetchall()
    if user_points_tuple == []:
      self.cursor.execute("INSERT INTO Users (username, telegram_id, telegram_chat_id, points) VALUES (?, ?, ?, ?)", (username, telegram_id, telegram_chat_id, 0))
      self.cursor.execute("SELECT points FROM Users WHERE telegram_id = ? and telegram_chat_id = ?", (telegram_id, telegram_chat_id))
      user_points_tuple = self.cursor.fetchall()
    user_points = user_points_tuple[0][0]
    user_points += points
    if user_points < 0: user_points = 0
    self.cursor.execute("UPDATE Users SET points = ? WHERE telegram_id = ? and telegram_chat_id = ?", (user_points, telegram_id, telegram_chat_id))
    self.conn.commit()

  def get_points(self, telegram_id: int, telegram_chat_id: int) -> int:
    self.cursor.execute("SELECT points FROM Users WHERE telegram_id = ? and telegram_chat_id = ?", (telegram_id, telegram_chat_id))
    try: 
      return self.cursos.fetchone()[0]
    except:
      return 0
  
  def get_top_points(self, telegram_chat_id: int) -> list:
    return self.cursor.execute("SELECT username, points FROM Users WHERE telegram_chat_id = ? LIMIT 15", (telegram_chat_id))
