
import sqlite3


class Dictionary():
    """A class to represent a dictionary.
    The words are the keys (can't be duplicated).
    """

    def __init__(self):
        self.conn = sqlite3.connect('db/db.sqlite')
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS dictionary (
                         word TEXT PRIMARY KEY,
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
        try:
            self.cur.execute("""
                             INSERT INTO dictionary (word, definition)
                             VALUES (?, ?)
                             """, (word, definition))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"    Word '{word}' already exists")
    
    def load_words(self, file_path):
        """Load words from a text file
        The file must be formatted as follow:
        word1 : definition1
        word2 : definition2
        ...
        """
        with open(file_path, "r") as f:
            for line in f:
                word, definition = line.split(":")
                # Remove spaces
                word = word.strip()
                definition = definition.strip()
                self.add_word(word, definition)
    
    def get_random_words(self, number):
        """Get a list of random words from the dictionary"""
        self.cur.execute("""
                         SELECT word, definition FROM dictionary
                         ORDER BY RANDOM()
                         LIMIT ?
                         """, (number,))
        return self.cur.fetchall()