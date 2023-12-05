#!/usr/bin/env python3

import pyinquirer

from Class.dictionary import Dictionary


def main():
  questions = [
    {
      'type': 'confirm',
      'name': 'choice',
      'message': 'Do you want to proceed?'
    }
  ]

  answers = pyinquirer.prompt(questions)
  choice = answers['choice']

  if choice:
    print('You chose yes.')
  else:
    print('You chose no.')


if __name__ == "__main__":
  main()
