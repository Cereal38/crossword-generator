#!/usr/bin/env python3

import sys

from Class.grid import Grid
from Tools.image_generator import generate_crossword_png

# ### main.py

# This script allows to generate a crossword puzzle

# ```shell
# python main.py [args]
# ```

# #### Arguments

# | Argument             | Description                                           | Default value |
# | -------------------- | ----------------------------------------------------- | ------------- |
# | `-h`, `--help`       | Show the help message and exit                        |               |
# | `-f`, `--file`       | Path to the .txt file containing the words (1)        |               |
# | `-d`, `--db`         | Number of words to get from the database              | 5             |
# | `-i`, `--iterations` | Number of iterations to get the best crossword puzzle | 50            |

# (1) File format for the `--file` argument:

# ```text
# word1 : definition1
# word2 : definition2
# ...
# ```

# Note: You can't use the `--file` and `--db` arguments at the same time.
# But you have to use one of them.

def main():
    """Main function"""
    # Get the arguments
    args = sys.argv[1:]

    if len(args) == 0 or "-h" in args or "--help" in args:
        print("Usage: python main.py [args]")
        print("Arguments:")
        print("  -h, --help: ......... Show the help message")
        print("  -f, --file: ......... Path to the .txt file containing the words (1)")
        print("  -d, --db: ........... Number of words to get from the database")
        print("  -i, --iterations: ... Number of iterations to get the best crossword puzzle")

        print("\n(1) File format for the --file argument:\n\tword1 : definition1\n\tword2 : definition2\n\t...")
        print("\nNote: You can't use the --file and --db arguments at the same time.")
        exit(0)

    # Get the file path
    file_path = None
    if "-f" in args or "--file" in args:
        file_path = args[args.index("-f") + 1] if "-f" in args else args[args.index("--file") + 1]

    # Get the number of words to get from the database
    nb_words = 5
    if "-d" in args or "--db" in args:
        nb_words = int(args[args.index("-d") + 1] if "-d" in args else args[args.index("--db") + 1])

    # Get the number of iterations
    nb_iterations = 50
    if "-i" in args or "--iterations" in args:
        nb_iterations = int(args[args.index("-i") + 1] if "-i" in args else args[args.index("--iterations") + 1])

    # Check if the file path is given
    if file_path is None:
        print("You must specify a file path")
        exit(1)

    # Create a grid
    grid = Grid()

    # Generate the grid
    grid.generate_grid(file_path, nb_words, nb_iterations)
    grid.display_cli()

if __name__ == "__main__":
    main()
