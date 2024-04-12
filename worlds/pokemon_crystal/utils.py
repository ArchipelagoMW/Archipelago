from .data import data, BASE_OFFSET


def get_random_pokemon(random, types=None):
    pokemon_pool = []
    if types is None or types[0] is None:
        pokemon_pool = [pkmn_name for pkmn_name, _data in data.pokemon.items() if pkmn_name != "UNOWN"]
    else:
        pokemon_pool = [pkmn_name for pkmn_name, pkmn_data in data.pokemon.items()
                        if pkmn_name != "UNOWN" and pkmn_data.types == types]
    return random.choice(pokemon_pool)


def get_random_held_item(random):
    helditems = [item.item_const for item_id, item in data.items.items()
                 if "Unique" not in item.tags and "INVALID" not in item.tags]
    return random.choice(helditems)


def get_random_filler_item(random):
    helditems = [item_id for item_id, item in data.items.items()
                 if "Unique" not in item.tags and "INVALID" not in item.tags]
    return random.choice(helditems) + BASE_OFFSET


def get_random_pokemon_id(random):
    pokemon_pool = [i for i in range(1, 251) if i != 0xC9]
    return random.choice(pokemon_pool)


def convert_color(r: int, g: int, b: int):
    color = 0
    color += sorted((0, r, 31))[1]
    color += (sorted((0, g, 31))[1] << 5)
    color += (sorted((0, b, 31))[1] << 10)
    return color


def convert_to_ingame_text(text: str):
    charmap = {
        "A": 0x80,
        "B": 0x81,
        "C": 0x82,
        "D": 0x83,
        "E": 0x84,
        "F": 0x85,
        "G": 0x86,
        "H": 0x87,
        "I": 0x88,
        "J": 0x89,
        "K": 0x8a,
        "L": 0x8b,
        "M": 0x8c,
        "N": 0x8d,
        "O": 0x8e,
        "P": 0x8f,
        "Q": 0x90,
        "R": 0x91,
        "S": 0x92,
        "T": 0x93,
        "U": 0x94,
        "V": 0x95,
        "W": 0x96,
        "X": 0x97,
        "Y": 0x98,
        "Z": 0x99,
        "(": 0x9a,
        ")": 0x9b,
        ":": 0x9c,
        ";": 0x9d,
        "[": 0x9e,
        "]": 0x9f,
        "a": 0xa0,
        "b": 0xa1,
        "c": 0xa2,
        "d": 0xa3,
        "e": 0xa4,
        "f": 0xa5,
        "g": 0xa6,
        "h": 0xa7,
        "i": 0xa8,
        "j": 0xa9,
        "k": 0xaa,
        "l": 0xab,
        "m": 0xac,
        "n": 0xad,
        "o": 0xae,
        "p": 0xaf,
        "q": 0xb0,
        "r": 0xb1,
        "s": 0xb2,
        "t": 0xb3,
        "u": 0xb4,
        "v": 0xb5,
        "w": 0xb6,
        "x": 0xb7,
        "y": 0xb8,
        "z": 0xb9,
        "'": 0xe0,
        "-": 0xe3,
        "?": 0xe6,
        "!": 0xe7,
        ".": 0xe8,
        "&": 0xe9,
        "/": 0xf3,
        ",": 0xf4,
        "0": 0xf6,
        "1": 0xf7,
        "2": 0xf8,
        "3": 0xf9,
        "4": 0xfa,
        "5": 0xfb,
        "6": 0xfc,
        "7": 0xfd,
        "8": 0xfe,
        "9": 0xff
    }
    return [charmap[char] if char in charmap else charmap["?"] for char in text]
