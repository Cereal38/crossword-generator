
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
    return sorted(self.words, key=lambda x: len(x["word"]))

def pop_longest_word(words: list) -> str:
  """Pop the longest word from the list"""
  longest_word = words.pop(words.index(max(words, key=lambda x: len(x[0]))))
  return longest_word
  

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

  print(words_added.get_words())
