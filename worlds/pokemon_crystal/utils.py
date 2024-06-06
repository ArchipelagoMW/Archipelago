from .data import data


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


def get_free_fly_location(random, johto_only):
    location_pool = [22, 21, 19, 23, 25]
    if not johto_only:
        location_pool += [3, 4, 5, 7, 8, 10, 9, 11]
    return random.choice(location_pool)


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
