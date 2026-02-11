rule_logic = {
  1: {
    "green": {
      "1": [0, 0, 1, False],
      "2": [2, 50, 2, True],
      "3": [4, 120, 4, True],
      "4": [5, 170, 5, True],
      "5": [6, 190, 5, True],
    },
    "yellow": {
      "1": [0, 0, 2, True],
      "2": [2, 50, 3, True],
      "3": [4, 120, 4, True],
      "4": [5, 170, 5, True],
      "5": [6, 190, 5, True],
    },
    "letters": [1, 3, 1, False],
    "streak": [6, 190, 5, True]
  },
  2: {
    "green": {
      "1": [0, 0, 1, False],
      "2": [2, 50, 2, False],
      "3": [3, 105, 3, True],
      "4": [5, 150, 5, True],
      "5": [6, 175, 6, True],
    },
    "yellow": {
      "1": [0, 0, 2, True],
      "2": [2, 50, 3, True],
      "3": [3, 105, 3, True],
      "4": [5, 150, 5, True],
      "5": [6, 175, 6, True],
    },
    "letters": [1, 3, 1, False],
    "streak": [6, 175, 6, True]
  },
  3: {
    "green": {
      "1": [0, 0, 1, False],
      "2": [1, 40, 2, False],
      "3": [2, 90, 3, False],
      "4": [4, 120, 4, True],
      "5": [5, 150, 5, True],
    },
    "yellow": {
      "1": [0, 0, 2, True],
      "2": [2, 40, 3, True],
      "3": [4, 90, 4, True],
      "4": [5, 120, 5, True],
      "5": [6, 150, 6, True],
    },
    "letters": [1, 3, 1, False],
    "streak": [6, 150, 6, True]
  },
  4: {
    "green": {
      "1": [0, 0, 1, False],
      "2": [2, 30, 2, False],
      "3": [3, 75, 3, False],
      "4": [4, 100, 4, True],
      "5": [5, 125, 5, True],
    },
    "yellow": {
      "1": [0, 0, 1, True],
      "2": [1, 30, 1, True],
      "3": [2, 75, 2, True],
      "4": [3, 100, 3, True],
      "5": [4, 125, 4, True],
    },
    "letters": [1, 3, 1, False],
    "streak": [4, 125, 4, True]
  },
  5: {
    "green": {
      "1": [0, 0, 1, False],
      "2": [1, 20, 2, False],
      "3": [2, 60, 2, False],
      "4": [3, 85, 3, False],
      "5": [3, 100, 3, True],
    },
    "yellow": {
      "1": [0, 0, 1, True],
      "2": [1, 20, 2, True],
      "3": [2, 60, 2, True],
      "4": [3, 85, 3, True],
      "5": [3, 100, 3, True],
    },
    "letters": [1, 3, 1, False],
    "streak": [3, 100, 3, True]
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