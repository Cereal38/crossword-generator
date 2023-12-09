
class Cell():
  def __init__(self):
    self.number = None
    self.letter = None
    self.is_black = False

  # TODO: Allow to set the number of the word
  # /!\ 2 words can start at the same cell
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