
from copy import deepcopy


def generate(grid, words: list):
  """Generate the grid with given words"""
  
  words_copy = deepcopy(words)

  # Reset the grid
  grid.reset()

  # Add the longest word to the grid
  longest_word = words_copy.pop(words_copy.index(max(words_copy, key=lambda x: len(x[0]))))
  grid.add_rows(1)
  grid.add_columns(len(longest_word[0]))
  grid.set_word(longest_word[0], 0, 0, "horizontal")
