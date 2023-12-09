
import random as rd
from copy import deepcopy

INITIAL_GRID_SIZE = 50


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
    self.length = 0
  
  def __len__(self):
    return self.length
  
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

def sort_words_by_len(words: list) -> None:
  """Sort a list of words by length"""
  words.sort(key=lambda x: len(x[0]), reverse=True)

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
  
  for i in range(len(cells_to_check)):

    cell = cells_to_check[i]

    # 1 - Check if the cells are empty or if the letter are the same
    if grid.get_cell(cell["row"], cell["column"]).get_letter() is not None and \
      grid.get_cell(cell["row"], cell["column"]).get_letter() != cell["letter"]:
      return False

    # 2 - Check if 2 words are not side by side
    # Basically, check we check if we are about to place a letter next to another letter
    # Exception: If the letter was already placed we don't check this constraint  
    if grid.get_cell(cell["row"], cell["column"]).get_letter() != cell["letter"]:
      if direction == "horizontal":
        letter_above = grid.get_cell(cell["row"] - 1, cell["column"]).get_letter() is not None
        letter_below = grid.get_cell(cell["row"] + 1, cell["column"]).get_letter() is not None
        if letter_above or letter_below:
          return False
      elif direction == "vertical":
        letter_left = grid.get_cell(cell["row"], cell["column"] - 1).get_letter() is not None
        letter_right = grid.get_cell(cell["row"], cell["column"] + 1).get_letter() is not None
        if letter_left or letter_right:
          return False
  
    # 3 - Check if there is one space before and after the word
    # Check the first letter
    if direction == "horizontal" and column > 0 and grid.get_cell(row, column - 1).get_letter() is not None:
      return False
    elif direction == "vertical" and row > 0 and grid.get_cell(row - 1, column).get_letter() is not None:
      return False
    # Check the last letter
    if direction == "horizontal" and column + len(word) < grid.columns() and grid.get_cell(row, column + len(word)).get_letter() is not None:
      return False
    elif direction == "vertical" and row + len(word) < grid.rows() and grid.get_cell(row + len(word), column).get_letter() is not None:
      return False
  
  return True

def reduce_grid(grid):
  """Remove all useless rows and cols from the grid"""
  first_row_index = INITIAL_GRID_SIZE - 1
  last_row_index = 0
  first_col_index = INITIAL_GRID_SIZE - 1
  last_col_index = 0

  # Find all interesting indexes
  for i in range(grid.rows()):
    for j in range(grid.columns()):
      if grid.get_cell(i, j).get_letter() is not None:
        first_row_index = min(first_row_index, i)
        last_row_index = max(last_row_index, i)
        first_col_index = min(first_col_index, j)
        last_col_index = max(last_col_index, j)
  
  # Remove useless rows
  grid.remove_rows(grid.rows() - last_row_index - 1, "end")
  grid.remove_rows(first_row_index, "start")
  grid.remove_columns(grid.columns() - last_col_index - 1, "end")
  grid.remove_columns(first_col_index, "start")

def add_black_cells(grid):
  """Add black cells to the grid
  Black cells are empty cells surrounded by 4 letters
  """
  for i in range(grid.rows()):
    for j in range(grid.columns()):
      if grid.get_cell(i, j).get_letter() is None:
        if i > 0 and j > 0 and i < grid.rows() - 1 and j < grid.columns() - 1:
          if grid.get_cell(i - 1, j).get_letter() is not None and \
            grid.get_cell(i + 1, j).get_letter() is not None and \
            grid.get_cell(i, j - 1).get_letter() is not None and \
            grid.get_cell(i, j + 1).get_letter() is not None:
            grid.get_cell(i, j).set_black()

def generate(grid, words: list):
  """Generate the grid with given words"""

  # Algorithm:
  # 1 - Sort the words by length
  # 2 - Add the longest word to the grid (at the middle)
  # 3 - Check each word to add and "join" the first that match in the grid
  # 4 - Repeat step 3 until all words are added or no word can be added during the step 3

  if len(words) == 0:
    raise ValueError("Words list must not be empty")
  
  words_copy = deepcopy(words)
  sort_words_by_len(words_copy)

  for word in words_copy:
    print(word[0])

  grid.reset()
  grid.add_rows(INITIAL_GRID_SIZE)
  grid.add_columns(INITIAL_GRID_SIZE)

  words_added = WordsAdded()

  # Add the longest word to the grid (at the middle)
  longest_word = words_copy.pop(0)
  direction = rd.choice(["horizontal", "vertical"])
  grid.set_word(longest_word[0], INITIAL_GRID_SIZE // 2, INITIAL_GRID_SIZE // 2, direction)
  words_added.add(longest_word[0], INITIAL_GRID_SIZE // 2, INITIAL_GRID_SIZE // 2, direction)


  # Add the other words to the grid
  no_word_can_be_added = False
  while len(words_copy) > 0 and not no_word_can_be_added:

    no_word_can_be_added = True

    a_word_had_already_been_added = False

    # Check each word to add until one can be added
    for word_to_add in words_copy:

      if a_word_had_already_been_added:
        break

      # Check each word already added to the grid and "join" the first that match
      for word_added in words_added.get_words():

        if a_word_had_already_been_added:
          break

        matching_letters = matching_words(word_to_add[0], word_added)
        rd.shuffle(matching_letters)

        # Check if the word can be added to the grid at the matching letter position
        if len(matching_letters) > 0:
          for matching_letter in matching_letters:

            if a_word_had_already_been_added:
              break

            direction = word_added["direction"]
            # Get position and direction of the new word
            new_word_direction = "horizontal" if direction == "vertical" else "vertical"
            new_word_row = matching_letter["row"] if new_word_direction == "horizontal" else matching_letter["row"] - matching_letter["index"]
            new_word_column = matching_letter["column"] if new_word_direction == "vertical" else matching_letter["column"] - matching_letter["index"]

            # If the word can be added, add it and break the loop
            can_be_added = word_can_be_added(word_to_add[0], new_word_row, new_word_column, new_word_direction, grid)
            if can_be_added:
              grid.set_word(word_to_add[0], new_word_row, new_word_column, new_word_direction)
              words_added.add(word_to_add[0], new_word_row, new_word_column, new_word_direction)
              words_copy.remove(word_to_add)
              a_word_had_already_been_added = True
              no_word_can_be_added = False
        
  
  reduce_grid(grid)

  add_black_cells(grid)

  grid.set_nb_words(len(words) - words_added.length)

