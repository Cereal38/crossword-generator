#!/usr/bin/env python3

from Class.grid import Grid


def main():
  grid = Grid()
  grid.generate_grid(20)
  grid.display_cli()


if __name__ == "__main__":
  main()
