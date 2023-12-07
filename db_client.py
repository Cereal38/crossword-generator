#!/usr/bin/env python3

import os

from Class.dictionary import Dictionary


def main():

  dictionary = Dictionary()
  
  print("Type 'help' for help. Type 'q' to quit.")

  while True:
    command = input(">>> ")
    if command == "help":
      print("    help: display this help")
      print("    create: create the dictionary (Init the DB)")
      print("    drop: drop the dictionary (Drop the DB)")
      print("    load: load a text file into the dictionary")
      print("    add: add a word to the dictionary (Insert a row in the DB)")
    
    elif command == "create":
      dictionary.create_table()
      print("    Dictionary created")

    elif command == "drop":
      dictionary.drop_table()
      print("    Dictionary dropped")
    
    elif command == "load":
      print("    Enter the path to the file")
      print("    File must be formatted as follow:\n")
      print("    word1 : definition1")
      print("    word2 : definition2")
      print("    ...\n")
      file_path = input("    Path: ")
      if os.path.exists(file_path):
        dictionary.load_words(file_path)
        print("    Words loaded")
      else:
        print("    File not found")

    elif command == "add":
      word = input("    Word: ")
      definition = input("    Definition: ")
      dictionary.add_word(word, definition)
      print("    Word added")

    elif command == "q":
      break

    else:
      print("    Unknown command")


if __name__ == "__main__":
  main()
