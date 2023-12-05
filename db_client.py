#!/usr/bin/env python3

from Class.dictionary import Dictionary


def main():

  dictionary = Dictionary()
  
  print("Type 'help' for help. Type 'q' to quit.")

  while True:
    command = input(">>> ")
    if command == "help":
      print("\thelp: display this help")
      print("\tcreate: create the dictionary (Init the DB)")
      print("\tdrop: drop the dictionary (Drop the DB)")
      print("\tadd: add a word to the dictionary (Insert a row in the DB)")
    
    elif command == "create":
      dictionary.create_table()
      print("\tDictionary created")

    elif command == "drop":
      dictionary.drop_table()
      print("\tDictionary dropped")

    elif command == "add":
      word = input("\tWord: ")
      definition = input("\tDefinition: ")
      dictionary.add_word(word, definition)
      print("\tWord added")

    elif command == "q":
      break

    else:
      print("\tUnknown command")


if __name__ == "__main__":
  main()
