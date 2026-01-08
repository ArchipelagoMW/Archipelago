rule_logic = {
  0: {
    "green": {
      "1": [0, 0, 1, False],
      "2": [3, 30, 1, False],
      "3": [4, 60, 2, True],
      "4": [5, 80, 3, True],
      "5": [6, 100, 4, True],
    },
    "yellow": {
      "1": [0, 0, 1, True],
      "2": [3, 30, 1, True],
      "3": [4, 60, 2, True],
      "4": [5, 80, 3, True],
      "5": [6, 100, 4, True],
    },
    "letters": [1, 10, 0, False],
    "pointShop": [3, 40, 2, False],
    "streak": [6, 100, 4, True]
  },
  1: {
    "green": {
      "1": [0, 0, 1, False],
      "2": [2, 30, 1, False],
      "3": [3, 60, 2, False],
      "4": [4, 80, 3, True],
      "5": [5, 100, 4, True],
    },
    "yellow": {
      "1": [0, 0, 1, True],
      "2": [2, 30, 1, True],
      "3": [3, 60, 2, True],
      "4": [4, 80, 3, True],
      "5": [5, 100, 4, True],
    },
    "letters": [1, 10, 0, False],
    "pointShop": [2, 20, 1, False],
    "streak": [5, 100, 4, True]
  },
  2: {
    "green": {
      "1": [0, 0, 1, False],
      "2": [1, 30, 1, False],
      "3": [2, 60, 2, False],
      "4": [3, 80, 3, False],
      "5": [4, 100, 4, True],
    },
    "yellow": {
      "1": [0, 0, 1, True],
      "2": [1, 30, 1, True],
      "3": [2, 60, 2, True],
      "4": [3, 80, 3, True],
      "5": [4, 100, 4, True],
    },
    "letters": [1, 10, 0, False],
    "pointShop": [1, 3, 1, False],
    "streak": [4, 100, 4, True]
  }
}

letter_scores = {
  "Letter A": 10,
  "Letter E": 10,
  "Letter I": 10,
  "Letter O": 10,
  "Letter U": 10,
  "Letter Y": 7,

  "Letter B": 8,
  "Letter C": 8,
  "Letter D": 9,
  "Letter F": 7,
  "Letter G": 9,
  "Letter H": 7,
  "Letter J": 3,
  "Letter K": 6,
  "Letter L": 10,
  "Letter M": 8,
  "Letter N": 10,
  "Letter P": 8,
  "Letter Q": 1,
  "Letter R": 10,
  "Letter S": 10,
  "Letter T": 10,
  "Letter V": 7,
  "Letter W": 7,
  "Letter X": 3,
  "Letter Z": 1
}