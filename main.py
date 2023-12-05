#!/usr/bin/env python3

from Class.grid import Grid


def main():
  grid = Grid(10, 10)
  grid.fill_grid_randomly()
  grid.display_cli()


if __name__ == "__main__":
  main()
