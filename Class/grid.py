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
  
  def reset(self):
    """Reset the grid"""
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
  
  def add_rows(self, nb_rows: int = 1, position: str = "end"):
    """Add rows to the grid
    :param nb_rows: Number of rows to add (default: 1)
    :param position: Position of the rows to add - "start" or "end" (default "end")
    """
    if position == "end":
      for i in range(nb_rows):
        self.grid.append([ Cell() for i in range(self.columns()) ])
    elif position == "start":
      for i in range(nb_rows):
        self.grid.insert(0, [ Cell() for i in range(self.columns()) ])
    else:
      raise ValueError("Position must be 'start' or 'end'")
  
  def add_columns(self, nb_columns: int = 1, position: str = "end"):
    """Add columns to the grid
    :param nb_columns: Number of columns to add (default: 1)
    :param position: Position of the columns to add - "start" or "end" (default "end")
    """
    if position == "end":
      for row in self.grid:
        for i in range(nb_columns):
          row.append(Cell())
    elif position == "start":
      for row in self.grid:
        for i in range(nb_columns):
          row.insert(0, Cell())
    else:
      raise ValueError("Position must be 'start' or 'end'")
  
  def set_word(self, word: str, row: int, column: int, direction: str):
    """Set a word in the grid
    :param word: Word to set
    :param row: Row id (first letter)
    :param column: Column if (first letter)
    :param direction: Direction of the word - "horizontal" or "vertical"
    """
    if direction == "horizontal":
      for i in range(len(word)):
        self.grid[row][column + i].set_letter(word[i])
    elif direction == "vertical":
      for i in range(len(word)):
        self.grid[row + i][column].set_letter(word[i])
    else:
      raise ValueError("Direction must be 'horizontal' or 'vertical'")

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
    words = [("HELLO", "A greeting"), ("WORLD", "The world"), ("PYTHON", "Blabla"), ("TEST", "blablba")]

    # Generate the grid
    generate(self, words)
