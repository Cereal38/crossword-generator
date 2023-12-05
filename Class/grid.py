import random as rd

from Class.box import Box


class Grid():
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = [[Box(row, col) for col in range(columns)] for row in range(rows)]
  
  def fill_grid_randomly(self):
    for row in self.grid:
      for box in row:
        if rd.random() < 0.2:
          box.set_black()
        else:
          box.set_letter(chr(rd.randint(65, 90)))

  def display(self):
    for row in self.grid:
      for box in row:
        if box.is_black:
          print("X", end=" ")
        elif box.letter is not None:
          print(box.get_letter(), end=" ")
      print()
