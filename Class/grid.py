
class Grid():
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = [[' ' for _ in range(columns)] for _ in range(rows)]

  def display(self):
    for row in self.grid:
      print(' '.join(row))
