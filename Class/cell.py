
class Cell():
  def __init__(self):
    self.number = None
    self.letter = None

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
