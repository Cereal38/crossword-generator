#!/usr/bin/env python3

import sys

from Class.dictionary import Dictionary
from Class.grid import Grid


def help_mode():
    """Show the help message"""
    print("Usage: python main.py [args]")
    print("\nExample: python main.py --file:words.txt -i:100")
    print("\nArguments:")
    print("  -h, --help: ......... Show the help message")
    print("  -f, --file: ......... Path to the .txt file containing the words (1)")
    print("  -d, --db: ........... Number of words to get from the database (default: 5)")
    print("  -i, --iterations: ... Number of iterations to get the best crossword puzzle (default: 50)")

    print("\n(1) File format for the --file argument:\n\tword1 : definition1\n\tword2 : definition2\n\t...")
    print("\nNote: You can't use the --file and --db arguments at the same time.")
    exit(0)

def file_mode(file_path: str, nb_iterations: int):
    """File mode
    :param file_path: Path to the .txt file containing the words
    :param nb_iterations: Number of iterations to get the best crossword puzzle
    """
    pass

def db_mode(nb_words_db: int, nb_iterations: int):
    """Database mode
    :param nb_words_db: Number of words to get from the database
    :param nb_iterations: Number of iterations to get the best crossword puzzle
    """
    grid = Grid()

    # Get the words from the database
    dictionary = Dictionary()
    words = dictionary.get_random_words(nb_words_db)

    pass

def main():
    
    # Variables
    mode = "" # "file" or "db"
    file_path = ""
    nb_words_db = 5
    nb_iterations = 50

    # Get the arguments
    args = sys.argv[1:]
    # Args without the values
    args_base = [ arg.split(":")[0] for arg in args ]

    # Unrecognized arguments > error
    allowed_args = ["-h", "--help", "-f", "--file", "-d", "--db", "-i", "--iterations"]
    for arg in args_base:
        if arg not in allowed_args:
            print(f"Unrecognized argument: {arg}")
            exit(1)

    # -h, --help or no arguments
    if len(args) == 0 or "-h" in args_base or "--help" in args_base:
        help_mode()

    # -f, --file and -d, --db used at the same time > error
    if ("-f" in args_base or "--file" in args_base) and ("-d" in args_base or "--db" in args_base):
        print("You can't use the --file and --db arguments at the same time.")
        exit(1)
    
    # -f, --file
    if "-f" in args_base or "--file" in args_base:
        mode = "file"
        for arg in args:
            if arg.startswith("-f:"):
                file_path = arg.split(":")[1]
            elif arg.startswith("--file:"):
                file_path = arg.split(":")[1]
        if file_path == "":
            print("You must specify a file path")
            exit(1)
        # Check if the file exists
        try:
            f = open(file_path, "r")
            f.close()
        except FileNotFoundError:
            print(f"File '{file_path}' not found")
            exit(1)
    
    # -d, --db
    if "-d" in args_base or "--db" in args_base:
        mode = "db"
        for arg in args:
            if arg.startswith("-d:"):
                nb_words_db = int(arg.split(":")[1])
            elif arg.startswith("--db:"):
                nb_words_db = int(arg.split(":")[1])
        if nb_words_db <= 0:
            print("The number of words must be greater than 0")
            exit(1)
    
    # -i, --iterations
    if "-i" in args_base or "--iterations" in args_base:
        for arg in args:
            if arg.startswith("-i:"):
                nb_iterations = int(arg.split(":")[1])
            elif arg.startswith("--iterations:"):
                nb_iterations = int(arg.split(":")[1])
        if nb_iterations <= 0:
            print("The number of iterations must be greater than 0")
            exit(1)
    
    if mode == "file":
        file_mode(file_path, nb_iterations)

    elif mode == "db":
        db_mode(nb_words_db, nb_iterations)


if __name__ == "__main__":
    main()
