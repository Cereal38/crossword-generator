
from copy import deepcopy

from Class.cell import Cell
from Class.grid import Grid


def generate(words: list) -> list:
  """Generate the grid with given words"""
  
  words_copy = deepcopy(words)

  grid = Grid(0, 0)

  # Init the grid by creating a list to receive the longest word
  longest_word = words_copy.pop(words_copy.index(max(words_copy, key=lambda x: len(x[0]))))

  print(longest_word)

  

  return grid
