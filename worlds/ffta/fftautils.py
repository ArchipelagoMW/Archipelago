textDict = {
    '0': 0xA7, '1': 0xA8, '2': 0xA9, '3': 0xAA, '4': 0xAB, '5': 0xAC, '6': 0xAD, '7': 0xAE, '8': 0xAF, '9': 0xB0,
    'A': 0xB1, 'B': 0xB2, 'C': 0xB3, 'D': 0xB4, 'E': 0xB5, 'F': 0xB6, 'G': 0xB7, 'H': 0xB8, 'I': 0xB9, 'J': 0xBA,
    'K': 0xBB, 'L': 0xBC, 'M': 0xBD, 'N': 0xBE, 'O': 0xBF, 'P': 0xC0, 'Q': 0xC1, 'R': 0xC2, 'S': 0xC3, 'T': 0xC4,
    'U': 0xC5, 'V': 0xC6, 'W': 0xC7, 'X': 0xC8, 'Y': 0xC9, 'Z': 0xCA, 'a': 0xCB, 'b': 0xCC, 'c': 0xCD, 'd': 0xCE,
    'e': 0xCF, 'f': 0xD0, 'g': 0xD1, 'h': 0xD2, 'i': 0xD3, 'j': 0xD4, 'k': 0xD5, 'l': 0xD6, 'm': 0xD7, 'n': 0xD8,
    'o': 0xD9, 'p': 0xDA, 'q': 0xDB, 'r': 0xDC, 's': 0xDD, 't': 0xDE, 'u': 0xDF, 'v': 0xE0, 'w': 0xE1, 'x': 0xE2,
    'y': 0xE3, 'z': 0xE4, '.': 0xE5, '?': 0xEB, '!': 0xEC, ',': 0xED, ':': 0xEF, '_': 0xF0, '/': 0xF2, '~': 0xF3,
    '"': 0xF6, '+': 0xFE, '-': 0xFF
}


# Algorithm "xor" from p. 4 of Marsaglia, "Xorshift RNGs"
# source: https://en.wikipedia.org/w/index.php?title=Xorshift&oldid=1214507567 (accessed: 30/03/24)
def xorshift32(state):
    """
    Calculates the next state of the RNG state.
    Used when ProgressiveExcessItems is set to random.
    This algorithm matches the one implemented in the rom exactly (chosen for ease of implementation in rom).
    This keeps the random items generated consistent between client and rom.

    :param state: Current 32-bit RNG state
    :return: Next 32-bit RNG state
    """
    state = (state ^ (state << 13)) & 0xFFFFFFFF
    state = (state ^ (state >> 17)) & 0xFFFFFFFF
    state = (state ^ (state << 5)) & 0xFFFFFFFF
    return state
