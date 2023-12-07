
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

def word_can_be_added(word: str, row: int, column: int, direction: str, grid) -> bool:
  """Check if a word can be added to the grid at the given position and direction"""
  
  # Check all concerned cells and see if :
  # 1 - Theses are empty OR the letter is the same
  # 2 - 2 words are not "side by side"
  # 3 - There is one space before and after the word

  cells_to_check = [] # Format: [ { "letter": "a", "row": 0, "column": 0 }, ... ]
  if direction == "horizontal":
    cells_to_check = [ { "letter": letter, "row": row, "column": column + i } for i, letter in enumerate(word) ]
  elif direction == "vertical":
    cells_to_check = [ { "letter": letter, "row": row + i, "column": column } for i, letter in enumerate(word) ]

  # 1 - Check if the cells are empty or if the letter are the same
  for cell in cells_to_check:
    if grid.rows() > cell["row"] + 1 and \
      grid.columns() > cell["column"] + 1 and \
      grid.grid[cell["row"]][cell["column"]].get_letter() is not None and \
      grid.grid[cell["row"]][cell["column"]].get_letter() != cell["letter"]:
    
      return False
  
  return True


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
    print(current_word)

    for word in words_added.get_words():
      matching_letters = matching_words(current_word[0], word)
      rd.shuffle(matching_letters)
      print(matching_letters)

      if len(matching_letters) > 0:
        for matching_letter in matching_letters:

          direction = word["direction"]
          new_word_direction = "horizontal" if direction == "vertical" else "vertical"
          new_word_row = matching_letter["row"] if new_word_direction == "horizontal" else matching_letter["row"] - matching_letter["index"]
          new_word_column = matching_letter["column"] if new_word_direction == "vertical" else matching_letter["column"] - matching_letter["index"]

          if word_can_be_added(current_word[0], matching_letter["row"], matching_letter["column"], direction, grid):
            grid.set_word(current_word[0], new_word_row, new_word_column, new_word_direction)
            words_added.add(current_word[0], new_word_row, new_word_column, new_word_direction)
            break
      

