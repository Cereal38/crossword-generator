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
    # TODO: Remove hardcoding
    # dictionary = Dictionary()
    # words = dictionary.get_random_words(nb_words)
    # for word in words:
    #   print(word)
    words = [("HELLO", "A greeting"), ("WORLD", "The world")]

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
    # Example: word = "HELLO"
    #          (0_0_8 AND 0_1_5 AND 0_2_12 AND 0_3_12 AND 0_4_15) OR
    #          (0_0_8 AND 1_0_5 AND 2_0_12 AND 3_0_12 AND 4_0_15) OR
    #          ...
    # for word in words:
    #   word_str = word[0]
    #   word_len = len(word_str)
    #   # List of all possible positions for the word
    #   positions = []
    #   for i in range(self.rows):
    #     for j in range(self.columns - word_len + 1):
    #       positions.append([ (i, j + k, letter_str_to_int(word_str[k])) for k in range(word_len)])
      
    #   for i in range(self.columns):
    #     for j in range(self.rows - word_len + 1):
    #       positions.append([ (j + k, i, letter_str_to_int(word_str[k])) for k in range(word_len)])

    #   # Format constraints
    #   position_constraints = []
    #   for position in positions:
    #       cell_constraints = [cells[i][j][k] for (i, j, k) in position]
    #       position_var = model.NewBoolVar('')
    #       model.AddBoolAnd(cell_constraints).OnlyEnforceIf(position_var)
    #       model.AddBoolOr([position_var.Not(), position_var]).OnlyEnforceIf(position_var.Not())
    #       position_constraints.append(position_var)
    #   model.AddBoolOr(position_constraints)

    # ============= CONSTRAINT 3 =============
    # WORDS MUST BE CONNECTED
    # Generate a list of couple of words that must be connected
    # Format: [ ( (index_word1, index_intersection1), (index_word2, index_intersection2) ), ... ]
    # TODO: Remove hardcoding
    connected_words_list = [ ( (0, 2), (1, 3) ) ]
    for connected_words in connected_words_list:
      word1_str = words[connected_words[0][0]][0]
      word1_len = len(word1_str)
      word2_str = words[connected_words[1][0]][0]
      word2_len = len(word2_str)
      intersection1 = connected_words[0][1]
      intersection2 = connected_words[1][1]
      # List of all possible positions for the words
      positions = []
      for i in range(self.rows):
        for j in range(self.columns - word1_len + 1):
          # Check if the words2 can be placed at the intersection
          if (i - intersection2) >= 0 and (i + (word2_len-1) - intersection2) < self.rows:
            temp_positions = [(i, j + k, letter_str_to_int(word1_str[k])) for k in range(word1_len) ]
            temp_positions += [(i - intersection2 + k, j + intersection1, letter_str_to_int(word2_str[k])) for k in range(word2_len) ]
            positions.append(temp_positions)
      
      # for i in range(self.columns):
      #   for j in range(self.rows - word1_len + 1):
      #     positions.append([ (j + k, i, letter_str_to_int(word1_str[k])) for k in range(word1_len)])
      
      # Format constraints and submit them to the model
      position_constraints = []
      for position in positions:
          cell_constraints = [cells[i][j][k] for (i, j, k) in position]
          position_var = model.NewBoolVar('')
          model.AddBoolAnd(cell_constraints).OnlyEnforceIf(position_var)
          model.AddBoolOr([position_var.Not(), position_var]).OnlyEnforceIf(position_var.Not())
          position_constraints.append(position_var)
      model.AddBoolOr(position_constraints)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE:
      print("No solution found.")
    else:
      # Fill the grid with the solution
      for i in range(self.rows):
        for j in range(self.columns):
          for k in range(27):
            if solver.Value(cells[i][j][k]) == 1:
              self.grid[i][j].set_letter(letter_int_to_str(k))
              break
    
    