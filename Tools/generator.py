
import random as rd
from copy import deepcopy


class WordsAdded():
  """WordsAdded class
  This class represents a list of words already added to the grid.
  Format: [ {
    "word": "hi",
    "direction": "horizontal"
    "letters": [
      { "letter": "h", "row": 0, "column": 0, available: True },
      { "letter": "i", "row": 0, "column": 1, available: True }
    ]
  }, ... ]
  """
  def __init__(self):
    self.words = []
  
  def add(self, word: str, row: int, column: int, direction: str):
    """Add a word to the list"""
    self.words.append({
      "word": word,
      "direction": direction,
      "letters": [
        { "letter": letter, "row": row, "column": column + i, "available": True } if direction == "horizontal" else 
        { "letter": letter, "row": row + i, "column": column, "available": True }
        for i, letter in enumerate(word)
      ]
    })
  
  def get_words(self) -> list:
    """Return the list of words already added to the grid"""
    return sorted(self.words, key=lambda x: len(x["word"]))

def pop_longest_word(words: list) -> str:
  """Pop the longest word from the list"""
  longest_word = words.pop(words.index(max(words, key=lambda x: len(x[0]))))
  return longest_word

def matching_words(word1: str, word2: dict) -> list:
  """Check if two words can be matched.
  Return a list of dict containing the position of the matching letter.
  Format: [ { "letter": "h", "index": 2, "row": 0, "column": 0 }, ... ]

  :param word1: Str
  :param word2: A word from the words added Class
  """
  matching_letters = []

  for i, letter in enumerate(word1):
    for letter2 in word2["letters"]:
      if letter == letter2["letter"] and letter2["available"]:
        matching_letters.append({
          "letter": letter,
          "index": i,
          "row": letter2["row"],
          "column": letter2["column"]
        })
  
  return matching_letters


def generate(grid, words: list):
  """Generate the grid with given words"""

  if len(words) == 0:
    raise ValueError("Words list must not be empty")
  
  words_copy = deepcopy(words)

  grid.reset()

  words_added = WordsAdded()

  # Add the longest word to the grid
  longest_word = pop_longest_word(words_copy)
  direction = rd.choice(["horizontal", "vertical"])
  grid.set_word(longest_word[0], 0, 0, direction)
  words_added.add(longest_word[0], 0, 0, direction)

  # Add the other words to the grid
  while len(words_copy) > 0:
    current_word = pop_longest_word(words_copy)

    for word in words_added.get_words():
      matching_letters = matching_words(current_word[0], word)

      if len(matching_letters) > 0:
        matching_letter = rd.choice(matching_letters)
        grid.set_word(current_word[0], matching_letter["row"], matching_letter["column"], "horizontal" if word["direction"] == "vertical" else "vertical")
        words_added.add(current_word[0], matching_letter["row"], matching_letter["column"], "horizontal" if word["direction"] == "vertical" else "vertical")
        break
      

