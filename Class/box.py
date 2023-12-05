
class Box():
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.number = None
    self.letter = None
    self.is_black = False

  def set_number(self, number):
    self.number = number

  def get_number(self):
    return self.number

  def set_letter(self, letter):
    self.letter = letter

  def get_letter(self):
    return self.letter

  def set_black(self):
    self.is_black = True

  def is_black(self):
    return self.is_black