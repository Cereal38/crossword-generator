#!/usr/bin/env python3

from Class.grid import Grid


def main():
  grid = Grid(8, 8)
  grid.generate_grid(5)
  grid.display_cli()


if __name__ == "__main__":
  main()
