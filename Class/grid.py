from Class.cell import Cell
from Class.dictionary import Dictionary
from Tools.grid_generator import generate


class Grid():
  """Grid class
  This class represents the grid of a crossword puzzle.
  """
  def __init__(self):
    self.grid = []
    self.nb_words = 0
  
  def reset(self):
    """Reset the grid"""
    self.grid = []

  def set_nb_words(self, nb_words: int):
    """Set the number of words in the grid"""
    self.nb_words = nb_words
  
  def get_nb_words(self) -> int:
    """Return the number of words in the grid"""
    return self.nb_words
  
  def rows(self) -> int:
    """Return the number of rows of the grid"""
    return len(self.grid)
  
  def columns(self) -> int:
    """Return the number of columns of the grid"""
    if self.rows() > 0:
      return len(self.grid[0])
    else:
      return 0
  
  def get_cell(self, row: int, column: int) -> Cell:
    """Return the cell at the given position"""
    return self.grid[row][column]
  
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
  
  def remove_rows(self, nb_rows: int = 1, position: str = "end"):
    """Remove rows from the grid
    :param nb_rows: Number of rows to remove (default: 1)
    :param position: Position of the rows to remove - "start" or "end" (default "end")
    """
    if position == "end":
      for i in range(nb_rows):
        self.grid.pop()
    elif position == "start":
      for i in range(nb_rows):
        self.grid.pop(0)
    else:
      raise ValueError("Position must be 'start' or 'end'")
    
  def remove_columns(self, nb_columns: int = 1, position: str = "end"):
    """Remove columns from the grid
    :param nb_columns: Number of columns to remove (default: 1)
    :param position: Position of the columns to remove - "start" or "end" (default "end")
    """
    if position == "end":
      for row in self.grid:
        for i in range(nb_columns):
          row.pop()
    elif position == "start":
      for row in self.grid:
        for i in range(nb_columns):
          row.pop(0)
    else:
      raise ValueError("Position must be 'start' or 'end'")
  
  def set_word(self, word: str, row: int, column: int, direction: str):
    """Set a word in the grid
    :param word: Word to set
    :param row: Row id (first letter)
    :param column: Column if (first letter)
    :param direction: Direction of the word - "horizontal" or "vertical"
    """
    # Set the word
    for i in range(len(word)):
      if direction == "horizontal":
        self.grid[row][column + i].set_letter(word[i])
      elif direction == "vertical":
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
          print(box.get_letter().upper(), end=" ")
        else:
          print(" ", end=" ")
      print()
  
  def generate_grid(self, words: list, nb_iterations: int) -> list:
    """Generate a grid with given words
    :param words: List of words to add to the grid - [(word1, definition1), ...]
    :param nb_iterations: Number of iterations to get the best grid

    :return: A list of associations between number, words, def - [{"number": 1, "word": "word1", "definition": "definition1"}, ...]
    """

    temp_grid = Grid()
    
    for i in range(nb_iterations):
      temp_grid.reset()
      generate(temp_grid, words)

      more_words = temp_grid.get_nb_words() > self.get_nb_words()
      equal_words = temp_grid.get_nb_words() == self.get_nb_words()
      smaller_grid = temp_grid.rows() * temp_grid.columns() < self.rows() * self.columns()
      if more_words or (equal_words and smaller_grid):
        self.grid = temp_grid.grid
        self.set_nb_words(temp_grid.get_nb_words())
      nb_iterations -= 1

