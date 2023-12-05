import random as rd

from Class.box import Box


class Grid():
  """Grid class
  This class represents the grid of a crossword puzzle.
  """
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = [[Box(row, col) for col in range(columns)] for row in range(rows)]
  
  def fill_grid_randomly(self):
    """Fill the grid with random values"""
    for row in self.grid:
      for box in row:
        if rd.random() < 0.05:
          box.set_black()
        elif rd.random() < 0.3:
          box.set_letter(None)
        else:
          box.set_letter(chr(rd.randint(65, 90)))

  def display_cli(self):
    """Display the grid in the command line"""
    for row in self.grid:
      for box in row:
        if box.is_black:
          print("■", end=" ")
        elif box.letter is not None:
          print(box.get_letter(), end=" ")
        else:
          print(" ", end=" ")
      print()
