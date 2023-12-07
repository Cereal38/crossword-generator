import random as rd

from ortools.sat.python import cp_model

from Class.cell import Cell
from Class.dictionary import Dictionary
from Tools.generator import generate


class Grid():
  """Grid class
  This class represents the grid of a crossword puzzle.
  """
  def __init__(self):
    self.grid = []
  
  def rows(self) -> int:
    """Return the number of rows of the grid"""
    return len(self.grid)
  
  def columns(self) -> int:
    """Return the number of columns of the grid"""
    if self.rows() > 0:
      return len(self.grid[0])
    else:
      return 0

  def display_cli(self):
    """Display the grid in the command line"""
    for row in self.grid:
      for box in row:
        if box.is_black:
          print("■", end=" ")
        elif box.letter is not None:
          print(box.get_letter(), end=" ")
        else:
          print(".", end=" ")
      print()
  
  def generate_grid(self, nb_words):
    """Generate the grid with random words"""
    
    # dictionary = Dictionary()
    # words = dictionary.get_random_words(nb_words)
    # for word in words:
    #   print(word)
    words = [("HELLO", "A greeting")]#, ("WORLD", "The world"), ("PYTHON", "Blabla"), ("TEST", "blablba")]

    # Generate the grid
    grid = generate(words)
    self.grid = grid
    self.rows = len(grid)
    self.columns = len(grid[0])
