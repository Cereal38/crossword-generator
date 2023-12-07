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
          print(".", end=" ")
      print()
  
  def generate_grid(self, nb_words):
    """Generate the grid using constraints programming"""
    
    # Create the model
    model = cp_model.CpModel()

    # Get words from the database
    # Format: [(word1, definition1), (word2, definition2), ...]
    # TODO: Remove hardcoding
    # dictionary = Dictionary()
    # words = dictionary.get_random_words(nb_words)
    # for word in words:
    #   print(word)
    words = [("HELLO", "A greeting"), ("WORLD", "The world"), ("PYTHON", "Blabla"), ("TEST", "blablba")]

    # Create a list to hold variables for each cell in the grid
    # Example: 0_0_0 -> cell in row 0, column 0 is empty
    #          0_0_1 -> cell in row 0, column 0 contains the letter 'A'
    #          0_0_2 -> cell in row 0, column 0 contains the letter 'B'
    #          ...
    cells = [ [ [model.NewBoolVar(f"{i}_{j}_{k}") for k in range(27)] for j in range(self.columns)] for i in range(self.rows)]

    # ============= CONSTRAINT 1 =============
    # EACH CELL MUST CONTAIN EXACTLY ONE LETTER OR BE EMPTY
    for i in range(self.rows):
      for j in range(self.columns):
        model.Add(sum(cells[i][j]) == 1)

    # ============= CONSTRAINT 2 =============
    # ALL WORDS MUST BE IN THE GRID EXACTLY ONCE
    # (We also check if cells preceding and following a word are empty)
    # Example: word = "HELLO"
    #          (0_0_8 AND 0_1_5 AND 0_2_12 AND 0_3_12 AND 0_4_15) OR
    #          (0_0_8 AND 1_0_5 AND 2_0_12 AND 3_0_12 AND 4_0_15) OR
    #          ...
    for word in words:
      word_str = word[0]
      word_len = len(word_str)
      # List of all possible positions for the word
      positions = []
      # Horizontal positions
      for i in range(self.rows):
        for j in range(self.columns - word_len + 1):
          positions.append([ (i, j + k, letter_str_to_int(word_str[k])) for k in range(word_len)])
          # Check if the cell preceding the word is empty
          if j > 0:
            positions[-1].append((i, j - 1, 0))
          # Check if the cell following the word is empty
          if j + word_len < self.columns:
            positions[-1].append((i, j + word_len, 0))
      
      # Vertical positions
      for i in range(self.columns):
        for j in range(self.rows - word_len + 1):
          positions.append([ (j + k, i, letter_str_to_int(word_str[k])) for k in range(word_len)])
          # Check if the cell preceding a letter is empty
          if j > 0:
            positions[-1].append((j - 1, i, 0))
          # Check if the cell following a letter is empty
          if j + word_len < self.rows:
            positions[-1].append((j + word_len, i, 0))

      # Format constraints
      temp_constraints = []
      for position in positions:
          new_bool_var = model.NewBoolVar(f"{word_str}_{position}")
          temp_constraints.append(new_bool_var)
          model.AddBoolAnd([cells[i][j][k] for (i, j, k) in position]).OnlyEnforceIf(new_bool_var)

      # XOR constraint
      model.Add(sum(temp_constraints) == 1)          
  
    # # ============= CONSTRAINT 3 =============
    # # ALL WORDS MUST INTERSECT
    # # We check if :
    # # <Number of letters in the grid> == <Number of letters in all words> - <Number of words> - 1
    number_of_letters_in_words = sum([len(word[0]) for word in words])
    number_of_words = len(words)
    # We check if the number of values different than [i][j][0] is correct
    model.Add(sum([sum([sum(cells[i][j][1:]) for j in range(self.columns)]) for i in range(self.rows)]) == number_of_letters_in_words - (number_of_words - 1))

    # # ============= CONSTRAINT 4 =============
    # # WORDS CAN'T BE SIDE BY SIDE
    # # We check if a letter (X) is in a situation like this:
    # #   L L
    # #   X L   OR   L X   ...
    # #              L L
    # #
    # # For cell 11 we check : NOT( NOT(c[0][1][0]) AND NOT(c[0][2][0]) AND NOT(c[1][2][0]) ) AND ...
    # # It's equal to : ( c[0][1][0] OR c[0][2][0] OR c[1][2][0] ) AND ...
    for i in range(1, self.rows - 1):
      for j in range(1, self.columns - 1):
        # Only if the cell contains a letter
        model.AddBoolOr([cells[i-1][j][0], cells[i-1][j+1][0], cells[i][j+1][0]]).OnlyEnforceIf(cells[i][j][0].Not())
        model.AddBoolOr([cells[i][j+1][0], cells[i+1][j+1][0], cells[i+1][j][0]]).OnlyEnforceIf(cells[i][j][0].Not())
        model.AddBoolOr([cells[i][j-1][0], cells[i+1][j-1][0], cells[i+1][j][0]]).OnlyEnforceIf(cells[i][j][0].Not())
        model.AddBoolOr([cells[i-1][j][0], cells[i-1][j-1][0], cells[i][j-1][0]]).OnlyEnforceIf(cells[i][j][0].Not())

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.INFEASIBLE:
      print("No solution found.")
    elif status == cp_model.UNKNOWN:
      print("The solver could not determine if a solution exists.")
    else:
      print(solver.ResponseStats())
       # Fill the grid with the solution
      for i in range(self.rows):
        for j in range(self.columns):
          for k in range(27):
            if solver.Value(cells[i][j][k]) == 1:
              self.grid[i][j].set_letter(letter_int_to_str(k))
              break
    