import random as rd

from ortools.sat.python import cp_model

from Class.box import Box
from Class.dictionary import Dictionary
from Tools.letters import letter_int_to_str, letter_str_to_int


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
  
  def generate_grid(self, nb_words):
    """Generate the grid using constraints programming"""
    
    # Create the model
    model = cp_model.CpModel()

    # Get words from the database
    # Format: [(word1, definition1), (word2, definition2), ...]
    dictionary = Dictionary()
    words = dictionary.get_random_words(nb_words)

    # Create a list to hold variables for each cell in the grid
    # Values: 0 -> Empty, 1 -> A, 2 -> B, ...
    cells = [[model.NewIntVar(0, 26, f'cell_{r}_{c}') for c in range(self.columns)] for r in range(self.rows)]

    # Constraint 1 - Each cell must contain a letter or None
    for row in cells:
      for cell in row:
        model.Add(cell >= 0)
        model.Add(cell <= 26)
    
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Fill the grid with the solution
    for row in self.grid:
      for box in row:
        box.set_letter(letter_int_to_str(solver.Value(cells[box.row][box.col])))
    