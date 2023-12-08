#!/usr/bin/env python3

import sys

from Class.grid import Grid


def main():
  if len(sys.argv) < 2:
    print("Usage: ./main.py <nb_words>")
    return

  nb_words = int(sys.argv[1])
  
  grid = Grid()
  grid.generate_grid(nb_words)
  grid.display_cli()


if __name__ == "__main__":
  main()
