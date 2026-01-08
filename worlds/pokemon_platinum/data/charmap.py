# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/charmap.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

charmap: dict[str, int] = {
    "MALE": 443,
    "FEMALE": 444,
    ",": 429,
    ".": 430,
    "'": 435,
    "-": 446,
    ":": 452,
    ";": 453,
    "!": 427,
    "?": 428,
    "{\"}": 436,
    "\"": 437,
    "{'}": 434,
    "(": 441,
    ")": 442,
    "...": 431,
    "{.}": 432,
    "~": 451,
    "@": 464,
    "#": 448,
    "%": 466,
    "+": 445,
    "*": 447,
    "/": 433,
    "=": 449,
    "O.": 459,
    ".O": 459,
    "CIRCLE": 460,
    "SQUARE": 461,
    "TRIANGLE": 462,
    "DIAMOND": 463,
    "SPADE": 454,
    "CLUB": 455,
    "HEART": 456,
    "SUIT DIAMOND": 457,
    "STAR": 458,
    "NOTE": 465,
    "SUN": 467,
    "CLOUD": 468,
    "UMBRELLA": 469,
    "SILHOUETTE": 470,
    "SMILE": 471,
    "LAUGH": 472,
    "UPSET": 473,
    "FROWN": 474,
    "{Z}": 477,
    "^": 475,
    "{v}": 476,
    " ": 478,
}

def _init():
    A_val = 299
    charmap.update({chr(ord('A') + i):A_val + i for i in range(26)})
    a_val = 325
    charmap.update({chr(ord('a') + i):a_val + i for i in range(26)})
    zero_val = 289
    charmap.update({chr(ord('0') + i):zero_val + i for i in range(10)})

_init()
