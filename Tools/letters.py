
def letter_int_to_str(letter_int):
  """Convert a letter integer to a letter string
  0 -> None
  1 -> A
  ...
  26 -> Z
  """
  if letter_int == 0:
    return None
  else:
    return chr(letter_int + 64)
  
def letter_str_to_int(letter_str):
  """Convert a letter string to a letter integer
  None -> 0
  A -> 1
  ...
  Z -> 26
  """
  if letter_str is None:
    return 0
  else:
    return ord(letter_str) - 64
  