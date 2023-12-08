#!/usr/bin/env python3

import sys

from Class.grid import Grid
from Tools.image_generator import generate_crossword_png


def main():
  if len(sys.argv) < 2:
    print("Usage: ./main.py <nb_words>")
    return

  nb_words = int(sys.argv[1])
  
  grid = Grid()
  grid.generate_grid(nb_words)
  grid.display_cli()
  generate_crossword_png(grid)


if __name__ == "__main__":
  main()
