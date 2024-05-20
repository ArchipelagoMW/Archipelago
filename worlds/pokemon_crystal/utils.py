from .data import data, BASE_OFFSET


def get_random_pokemon(random, types=None, base_only=False):
    pokemon_pool = []
    if types is None or types[0] is None:
        pokemon_pool = [pkmn_name for pkmn_name, pkmn_data in data.pokemon.items() if
                        pkmn_name != "UNOWN" and (pkmn_data.is_base or not base_only)]
    else:
        pokemon_pool = [pkmn_name for pkmn_name, pkmn_data in data.pokemon.items()
                        if pkmn_name != "UNOWN" and pkmn_data.types == types]
    return random.choice(pokemon_pool)


def get_random_nezumi(random):
    pokemon_pool = ["RATTATA", "RATICATE", "NIDORAN_F", "NIDORAN_M", "NIDORINA", "NIDORINO", "PIKACHU", "RAICHU",
                    "SANDSHREW", "SANDSLASH", "CYNDAQUIL", "QUILAVA", "SENTRET", "FURRET", "MARILL"]
    return random.choice(pokemon_pool)


def get_random_types(random):
    if random.randint(0, 25) < 11:
        type1 = random.choice(data.types)
        type2 = random.choice([t for t in data.types if t != type1])
        return [type1, type2]
    return [random.choice(data.types)]


def get_random_base_stats(random, bst=None):
    if bst is None:
        bst = random.randint(180, 680)
    randoms = [random.random() + 0.28 for i in range(0, 6)]
    total = sum(randoms)
    return [int((stat * bst) / total) for stat in randoms]


def get_random_held_item(random):
    helditems = [item.item_const for item_id, item in data.items.items()
                 if "Unique" not in item.tags and "INVALID" not in item.tags and "Trap" not in item.tags]
    return random.choice(helditems)


def get_random_filler_item(random):
    weighted_pool = [["Rare Candy"] * 3, ["Ether", "Elixer", "Max Ether", "Max Elixer", "Mysteryberry"] * 5,
                     ["Water Stone", "Fire Stone", "Thunderstone", "Leaf Stone", "Sun Stone", "Moon Stone"] * 2,
                     ["Escape Rope"] * 3, ["Nugget", "Star Piece", "Stardust", "Pearl", "Big Pearl"] * 2,
                     ["Poke Ball", "Great Ball", "Ultra Ball"] * 5,
                     ["Potion", "Super Potion", "Hyper Potion", "Energy Root", "Energypowder"] * 12,
                     ["Full Restore"] * 2, ["Repel", "Super Repel", "Max Repel"] * 3,
                     ["Revive", "Revival Herb"] * 4 + ["Max Revive"] * 2,
                     ["HP Up", "PP Up", "Protein", "Carbos", "Calcium", "Iron"] * 5,
                     ["Guard Spec", "Dire Hit", "X Attack", "X Defend", "X Speed", "X Special"] * 2,
                     ["Heal Powder", "Burn Heal", "Parlyz Heal", "Ice Heal", "Antidote", "Awakening", "Full Heal"] * 5]
    group = random.choice(weighted_pool)
    return random.choice(group)


def get_random_pokemon_id(random):
    pokemon_pool = [i for i in range(1, 251) if i != 0xC9]
    return random.choice(pokemon_pool)


def get_tmhm_compatibility(tms, tm_value, hm_value, types, vanilla_learnset, random):
    tmhms = []
    for tm_name, tm_data in tms.items():
        use_value = hm_value if tm_data.is_hm else tm_value
        if tm_data.type in types:
            use_value = use_value * 2
        if use_value == 0:
            if tm_name in vanilla_learnset:
                tmhms.append(tm_name)
        elif random.randint(0, 99) < use_value:
            tmhms.append(tm_name)
    return tmhms


def get_random_colors(random):
    color1 = convert_color(random.randint(0, 31), random.randint(0, 31), random.randint(0, 31))
    color2 = convert_color(random.randint(0, 31), random.randint(0, 31), random.randint(0, 31))
    return [color1[0], color1[1], color2[0], color2[1]]


def get_type_colors(types, random):
    type1 = types[0]
    type2 = types[1] if len(types) == 2 else type1
    c1 = type_palettes[type1][0]
    c2 = type_palettes[type2][1]
    r1, g1, b1 = shift_color(c1[0], c1[1], c1[2], random)
    r2, g2, b2 = shift_color(c2[0], c2[1], c2[2], random)
    color1 = convert_color(r1, g1, b1)
    color2 = convert_color(r2, g2, b2)
    return [color1[0], color1[1], color2[0], color2[1]]


def shift_color(r: int, g: int, b: int, random):
    return r + random.randint(-1, 1), \
           g + random.randint(-1, 1), \
           b + random.randint(-1, 1)


def convert_color(r: int, g: int, b: int):
    color = 0
    color += sorted((0, r, 31))[1]
    color += (sorted((0, g, 31))[1] << 5)
    color += (sorted((0, b, 31))[1] << 10)
    return color.to_bytes(2, "little")


def convert_to_ingame_text(text: str):
    charmap = {
        "…": 0x75,
        " ": 0x7f,
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
        "Ä": 0xc0,
        "Ö": 0xc1,
        "Ü": 0xc2,
        "ä": 0xc3,
        "ö": 0xc4,
        "ü": 0xc5,
        "'": 0xe0,
        "-": 0xe3,
        "?": 0xe6,
        "!": 0xe7,
        ".": 0xe8,
        "&": 0xe9,
        "é": 0xea,
        "→": 0xeb,
        "▷": 0xec,
        "▶": 0xed,
        "▼": 0xee,
        "♂": 0xef,
        "¥": 0xf0,
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


type_palettes = {
    "NORMAL": [[31, 27, 31], [31, 24, 30]],
    "FIGHTING": [[30, 17, 1], [24, 9, 0]],
    "FLYING": [[17, 21, 31], [15, 11, 28]],
    "POISON": [[27, 21, 31], [15, 10, 24]],
    "GROUND": [[28, 19, 13], [24, 14, 0]],
    "ROCK": [[21, 20, 22], [18, 15, 4]],
    "BUG": [[23, 25, 6], [16, 18, 4]],
    "GHOST": [[10, 8, 14], [5, 3, 15]],
    "STEEL": [[19, 19, 21], [12, 14, 13]],
    "FIRE": [[31, 7, 0], [31, 15, 0]],
    "WATER": [[5, 8, 31], [2, 4, 26]],
    "GRASS": [[8, 31, 5], [4, 24, 2]],
    "ELECTRIC": [[31, 23, 7], [31, 17, 0]],
    "PSYCHIC_TYPE": [[31, 14, 30], [24, 4, 14]],
    "ICE": [[17, 25, 30], [22, 27, 30]],
    "DRAGON": [[16, 20, 25], [9, 12, 23]],
    "DARK": [[4, 2, 7], [3, 2, 6]],
}
