
import random as rd
from copy import deepcopy


class WordsAdded():
  """WordsAdded class
  This class represents a list of words already added to the grid.
  Format: [ {
    "word": "hi",
    "direction": "horizontal"
    "letters": [
      { "letter": "h", "row": 0, "column": 0 },
      { "letter": "i", "row": 0, "column": 1 },
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
        { "letter": letter, "row": row, "column": column + i } if direction == "horizontal" else { "letter": letter, "row": row + i, "column": column }
        for i, letter in enumerate(word)
      ]
    })
  
  def get_words(self) -> list:
    """Return the list of words already added to the grid"""
    return sorted(self.words_added, key=lambda x: len(x["word"]))
  

def generate(grid, words: list):
  """Generate the grid with given words"""

  if len(words) == 0:
    raise ValueError("Words list must not be empty")
  
  words_copy = deepcopy(words)

  grid.reset()

  # A list of words already added to the grid
  # Sorted by length
  # Format: [ {
  #   "direction": "horizontal"
  #   "letters": [
  #     { "letter": "h", "row": 0, "column": 0 },
  #     { "letter": "i", "row": 0, "column": 1 },
  #   ]
  # }, ... ]
  words_added = []

  # Add the longest word to the grid
  longest_word = words_copy.pop(words_copy.index(max(words_copy, key=lambda x: len(x[0]))))
  grid.set_word(longest_word[0], 0, 0, rd.choice(["horizontal", "vertical"]))
