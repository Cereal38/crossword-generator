
import os
import sqlite3


class Dictionary():
    """A class to represent a dictionary.
    Multiple words written the same way but with different meanings can be added to the dictionary.
    """

    def __init__(self):
        self.conn = sqlite3.connect('db/db.sqlite')
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS dictionary (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         word TEXT,
                         definition TEXT
                         )
                         """)
        self.conn.commit()
  
    def drop_table(self):
        """Drop the table
        USE WITH CAUTION
        """
        self.cur.execute("""
                         DROP TABLE IF EXISTS dictionary
                         """)
        self.conn.commit()
    
    def add_word(self, word, definition):
        """Add a word to the dictionary"""
        self.cur.execute("""
                         INSERT INTO dictionary (word, definition)
                         VALUES (?, ?)
                         """, (word, definition))
        self.conn.commit()
    
    def get_random_words(self, number):
        """Get a list of random words from the dictionary"""
        self.cur.execute("""
                         SELECT word FROM dictionary
                         ORDER BY RANDOM()
                         LIMIT ?
                         """, (number,))
        return self.cur.fetchall()