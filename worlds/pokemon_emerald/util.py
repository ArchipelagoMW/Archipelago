import orjson
from typing import Any, Dict, List, Optional, Tuple, Iterable

from .data import NATIONAL_ID_TO_SPECIES_ID, EncounterType, data


CHARACTER_DECODING_MAP = {
    0x00: " ", 0x01: "À", 0x02: "Á", 0x03: "Â", 0x04: "Ç",
    0x05: "È", 0x06: "É", 0x07: "Ê", 0x08: "Ë", 0x09: "Ì",
    0x0B: "Î", 0x0C: "Ï", 0x0D: "Ò", 0x0E: "Ó", 0x0F: "Ô",
    0x10: "Œ", 0x11: "Ù", 0x12: "Ú", 0x13: "Û", 0x14: "Ñ",
    0x15: "ß", 0x16: "à", 0x17: "á", 0x19: "ç", 0x1A: "è",
    0x1B: "é", 0x1C: "ê", 0x1D: "ë", 0x1E: "ì", 0x20: "î",
    0x21: "ï", 0x22: "ò", 0x23: "ó", 0x24: "ô", 0x25: "œ",
    0x26: "ù", 0x27: "ú", 0x28: "û", 0x29: "ñ", 0x2A: "°",
    0x2B: "ª", 0x2D: "&", 0x2E: "+", 0x35: "=", 0x36: ";",
    0x50: "▯", 0x51: "¿", 0x52: "¡", 0x5A: "Í", 0x5B: "%",
    0x5C: "(", 0x5D: ")", 0x68: "â", 0x6F: "í", 0x79: "⬆",
    0x7A: "⬇", 0x7B: "⬅", 0x7C: "➡", 0x7D: "*", 0x84: "ᵉ",
    0x85: "<", 0x86: ">", 0xA1: "0", 0xA2: "1", 0xA3: "2",
    0xA4: "3", 0xA5: "4", 0xA6: "5", 0xA7: "6", 0xA8: "7",
    0xA9: "8", 0xAA: "9", 0xAB: "!", 0xAC: "?", 0xAD: ".",
    0xAE: "-", 0xB0: "…", 0xB1: "“", 0xB2: "”", 0xB3: "‘",
    0xB4: "’", 0xB5: "♂", 0xB6: "♀", 0xB8: ",", 0xB9: "×",
    0xBA: "/", 0xBB: "A", 0xBC: "B", 0xBD: "C", 0xBE: "D",
    0xBF: "E", 0xC0: "F", 0xC1: "G", 0xC2: "H", 0xC3: "I",
    0xC4: "J", 0xC5: "K", 0xC6: "L", 0xC7: "M", 0xC8: "N",
    0xC9: "O", 0xCA: "P", 0xCB: "Q", 0xCC: "R", 0xCD: "S",
    0xCE: "T", 0xCF: "U", 0xD0: "V", 0xD1: "W", 0xD2: "X",
    0xD3: "Y", 0xD4: "Z", 0xD5: "a", 0xD6: "b", 0xD7: "c",
    0xD8: "d", 0xD9: "e", 0xDA: "f", 0xDB: "g", 0xDC: "h",
    0xDD: "i", 0xDE: "j", 0xDF: "k", 0xE0: "l", 0xE1: "m",
    0xE2: "n", 0xE3: "o", 0xE4: "p", 0xE5: "q", 0xE6: "r",
    0xE7: "s", 0xE8: "t", 0xE9: "u", 0xEA: "v", 0xEB: "w",
    0xEC: "x", 0xED: "y", 0xEE: "z", 0xEF: "▶", 0xF0: ":",
}

CHARACTER_ENCODING_MAP = {value: key for key, value in CHARACTER_DECODING_MAP.items()}
CHARACTER_ENCODING_MAP.update({
    "'": CHARACTER_ENCODING_MAP["’"],
    "\"": CHARACTER_ENCODING_MAP["”"],
    "_": CHARACTER_ENCODING_MAP[" "],
})

ALLOWED_TRAINER_NAME_CHARACTERS = frozenset({
    " ", "0", "1", "2", "3", "4", "5", "6", "7", "8",
    "9", "!", "?", ".", "-", "…", "“", "”", "‘", "’",    
    "♂", "♀", ",", "/", "A", "B", "C", "D", "E", "F",
    "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
    "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z",
})


def encode_string(string: str, length: Optional[int] = None) -> bytes:
    arr = []
    length = len(string) if length is None else length

    for i in range(length):
        if i >= len(string):
            arr.append(0xFF)
            continue

        char = string[i]
        if char in CHARACTER_ENCODING_MAP:
            arr.append(CHARACTER_ENCODING_MAP[char])
        else:
            arr.append(CHARACTER_ENCODING_MAP["?"])

    return bytes(arr)


def decode_string(string_data: Iterable[int]) -> str:
    string = ""
    for code in string_data:
        if code == 0xFF:
            break

        if code in CHARACTER_DECODING_MAP:
            string += CHARACTER_DECODING_MAP[code]
        else:
            raise KeyError(f"The following value does not correspond to a character in Pokemon Emerald: {code}")

    return string


def get_encounter_type_label(encounter_type: EncounterType, slot: int) -> str:
    if encounter_type == EncounterType.FISHING:
        return {
            0: "Old Rod",
            1: "Old Rod",
            2: "Good Rod",
            3: "Good Rod",
            4: "Good Rod",
            5: "Super Rod",
            6: "Super Rod",
            7: "Super Rod",
            8: "Super Rod",
            9: "Super Rod",
        }[slot]
    
    return {
        EncounterType.LAND: 'Land',
        EncounterType.WATER: 'Water',
        EncounterType.ROCK_SMASH: 'Rock Smash',
    }[encounter_type]


def get_easter_egg(easter_egg: str) -> Tuple[int, int]:
    easter_egg = easter_egg.upper()
    result1 = 0
    result2 = 0
    for c in easter_egg:
        result1 = ((result1 << 5) - result1 + ord(c)) & 0xFFFFFFFF
        result2 = ((result2 << 4) - result2 + ord(c)) & 0xFF

    if result1 == 0x9137C17B:
        value = (result2 + 23) & 0xFF
        if value > 0 and (value < 252 or (value > 276 and value < 412)):
            return (1, value)
    elif result1 == 0x9AECC7C6:
        value = (result2 + 64) & 0xFF
        if value > 0 and value < 355:
            return (2, value)
    elif result1 == 0x506D2690:
        value = (result2 + 169) & 0xFF
        if value > 0 and value < 78:
            return (3, value)
    elif result1 == 0xA7850E45 and (result1 ^ result2) & 0xFF == 96:
        return (4, 0)

    return (0, 0)


def location_name_to_label(name: str) -> str:
    return data.locations[name].label


def int_to_bool_array(num: int) -> List[bool]:
    binary_string = format(num, "064b")
    bool_array = [bit == "1" for bit in reversed(binary_string)]
    return bool_array


def bool_array_to_int(bool_array: List[bool]) -> int:
    binary_string = "".join(["1" if bit else "0" for bit in reversed(bool_array)])
    num = int(binary_string, 2)
    return num


_SUBSTRUCT_ORDERS = [
    [0, 1, 2, 3], [0, 1, 3, 2], [0, 2, 1, 3], [0, 3, 1, 2],
    [0, 2, 3, 1], [0, 3, 2, 1], [1, 0, 2, 3], [1, 0, 3, 2],
    [2, 0, 1, 3], [3, 0, 1, 2], [2, 0, 3, 1], [3, 0, 2, 1],
    [1, 2, 0, 3], [1, 3, 0, 2], [2, 1, 0, 3], [3, 1, 0, 2],
    [2, 3, 0, 1], [3, 2, 0, 1], [1, 2, 3, 0], [1, 3, 2, 0],
    [2, 1, 3, 0], [3, 1, 2, 0], [2, 3, 1, 0], [3, 2, 1, 0],
]

_LANGUAGE_IDS = {
    "Japanese": 1,
    "English": 2,
    "French": 3,
    "Italian": 4,
    "German": 5,
    "Spanish": 7,
}

_MODERN_ITEM_TO_EMERALD_ITEM = {
    item.modern_id: item.item_id
    for item in data.items.values()
    if item.modern_id is not None
}


def _encrypt_or_decrypt_substruct(substruct_data: Iterable[int], key: int) -> bytearray:
    modified_data = bytearray()
    for i in range(int(len(substruct_data) / 4)):
        modified_data.extend((int.from_bytes(substruct_data[i * 4 : (i + 1) * 4], "little") ^ key).to_bytes(4, "little"))

    return modified_data


def pokemon_data_to_json(pokemon_data: Iterable[int]) -> str:
    personality = int.from_bytes(pokemon_data[0:4], "little")
    tid = int.from_bytes(pokemon_data[4:8], "little")

    substruct_order = _SUBSTRUCT_ORDERS[personality % 24]
    substructs = []
    for i in substruct_order:
        substructs.append(pokemon_data[32 + (i * 12) : 32 + ((i + 1) * 12)])

    decrypted_substructs = [_encrypt_or_decrypt_substruct(substruct, personality ^ tid) for substruct in substructs]

    iv_ability_info = int.from_bytes(decrypted_substructs[3][4:8], "little")
    met_info = int.from_bytes(decrypted_substructs[3][2:4], "little")

    held_item = int.from_bytes(decrypted_substructs[0][2:4], "little")

    json_object = {
        "version": "1",
        "personality": personality,
        "nickname": decode_string(pokemon_data[8:18]),
        "language": {v: k for k, v in _LANGUAGE_IDS.items()}[pokemon_data[18]],
        "species": data.species[int.from_bytes(decrypted_substructs[0][0:2], "little")].national_dex_number,
        "experience": int.from_bytes(decrypted_substructs[0][4:8], "little"),
        "ability": iv_ability_info >> 31,
        "ivs": [(iv_ability_info >> (i * 5)) & 0x1F for i in range(6)],
        "evs": list(decrypted_substructs[2][0:6]),
        "conditions": list(decrypted_substructs[2][6:12]),
        "pokerus": decrypted_substructs[3][0],
        "location_met": decrypted_substructs[3][1],
        "level_met": met_info & 0b0000000001111111,
        "game": (met_info & 0b0000011110000000) >> 7,
        "ball": (met_info & 0b0111100000000000) >> 11,
        "moves": [
            [
                int.from_bytes(decrypted_substructs[1][i * 2 : (i + 1) * 2], "little"),
                decrypted_substructs[1][8 + i],
                (decrypted_substructs[0][8] & (0b00000011 << (i * 2))) >> (i * 2)
            ] for i in range(4)
        ],
        "trainer": {
            "name": decode_string(pokemon_data[20:27]),
            "id": tid,
            "female": (met_info & 0b1000000000000000) != 0,
        },
    }

    if held_item != 0:
        json_object["item"] = data.items[held_item].modern_id

    return orjson.dumps(json_object).decode("utf-8")


def json_to_pokemon_data(json_str: str) -> bytearray:
    pokemon_json: Dict[str, Any] = orjson.loads(json_str)

    # Default values to cover for optional or accidentally missed fields
    default_pokemon = {
        "nickname": "A",
        "personality": 0,
        "species": 1,
        "experience": 0,
        "ability": 0,
        "ivs": [0, 0, 0, 0, 0, 0],
        "evs": [0, 0, 0, 0, 0, 0],
        "conditions": [0, 0, 0, 0, 0, 0],
        "pokerus": 0,
        "game": 3,
        "location_met": 0,
        "level_met": 1,
        "ball": 4,
        "moves": [[33, 35, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
    }

    default_trainer = {
        "name": "A",
        "id": 0,
        "female": False,
    }

    pokemon_json = {**default_pokemon, **{k: v for k, v in pokemon_json.items()}}
    pokemon_json["trainer"] = {**default_trainer, **pokemon_json["trainer"]}

    # Cutting string lengths to Emerald sizes
    pokemon_json["nickname"] = pokemon_json["nickname"][0:10]
    pokemon_json["trainer"]["name"] = pokemon_json["trainer"]["name"][0:7]

    # Handle data from incompatible games
    if pokemon_json["species"] > 387:
        pokemon_json["species"] = 201  # Unown
    if pokemon_json["ball"] > 12:
        pokemon_json["ball"] = 4  # Pokeball
    if "game" not in pokemon_json or (pokemon_json["game"] > 5 and pokemon_json["game"] != 15):
        pokemon_json["game"] = 0  # Unknown
        pokemon_json["location_met"] = 0  # Littleroot

    substructs = [bytearray([0 for _ in range(12)]) for _ in range(4)]

    # Substruct type 0
    for i, byte in enumerate(NATIONAL_ID_TO_SPECIES_ID[pokemon_json["species"]].to_bytes(2, "little")):
        substructs[0][0 + i] = byte

    if "item" in pokemon_json:
        if pokemon_json["item"] in _MODERN_ITEM_TO_EMERALD_ITEM:
            for i, byte in enumerate(_MODERN_ITEM_TO_EMERALD_ITEM[pokemon_json["item"]].to_bytes(2, "little")):
                substructs[0][2 + i] = byte

    for i, byte in enumerate((pokemon_json["experience"]).to_bytes(4, "little")):
        substructs[0][4 + i] = byte

    for i, move_info in enumerate(pokemon_json["moves"]):
        substructs[0][8] |= ((move_info[2] & 0b11) << (2 * i))

    substructs[0][9] = data.species[NATIONAL_ID_TO_SPECIES_ID[pokemon_json["species"]]].friendship

    # Substruct type 1
    for i, move_info in enumerate(pokemon_json["moves"]):
        for j, byte in enumerate(move_info[0].to_bytes(2, "little")):
            substructs[1][(i * 2) + j] = byte

        substructs[1][8 + i] = move_info[1]

    # Substruct type 2
    for i, ev in enumerate(pokemon_json["evs"]):
        substructs[2][0 + i] = ev

    for i, condition in enumerate(pokemon_json["conditions"]):
        substructs[2][6 + i] = condition

    # Substruct type 3
    substructs[3][0] = pokemon_json["pokerus"]
    substructs[3][1] = pokemon_json["location_met"]

    origin = pokemon_json["level_met"] | (pokemon_json["game"] << 7) | (pokemon_json["ball"] << 11)
    origin |= (1 << 15) if pokemon_json["trainer"]["female"] else 0
    for i, byte in enumerate(origin.to_bytes(2, "little")):
        substructs[3][2 + i] = byte

    iv_ability_info = 0
    for i, iv in enumerate(pokemon_json["ivs"]):
        iv_ability_info |= iv << (i * 5)
    iv_ability_info |= 1 << 31 if pokemon_json["ability"] == 1 else 0
    for i, byte in enumerate(iv_ability_info.to_bytes(4, "little")):
        substructs[3][4 + i] = byte

    # Main data
    pokemon_data = bytearray([0 for _ in range(80)])
    for i, byte in enumerate(pokemon_json["personality"].to_bytes(4, "little")):
        pokemon_data[0 + i] = byte

    for i, byte in enumerate(pokemon_json["trainer"]["id"].to_bytes(4, "little")):
        pokemon_data[4 + i] = byte

    for i, byte in enumerate(encode_string(pokemon_json["nickname"], 10)):
        pokemon_data[8 + i] = byte

    pokemon_data[18] = _LANGUAGE_IDS[pokemon_json["language"]]
    pokemon_data[19] = 0b00000010  # Flags for Bad Egg, Has Species, Is Egg, padding bits (low to high)

    for i, byte in enumerate(encode_string(pokemon_json["trainer"]["name"], 7)):
        pokemon_data[20 + i] = byte

    # Markings, 1 byte

    checksum = 0
    for i in range(4):
        for j in range(6):
            checksum += int.from_bytes(substructs[i][j * 2 : (j + 1) * 2], "little")
    checksum &= 0xFFFF
    for i, byte in enumerate(checksum.to_bytes(2, "little")):
        pokemon_data[28 + i] = byte

    # Separator, 2 bytes

    substruct_order = [_SUBSTRUCT_ORDERS[pokemon_json["personality"] % 24].index(n) for n in [0, 1, 2, 3]]
    encrypted_substructs = [None for _ in range(4)]
    encryption_key = pokemon_json["personality"] ^ pokemon_json["trainer"]["id"]
    encrypted_substructs[0] = _encrypt_or_decrypt_substruct(substructs[substruct_order[0]], encryption_key)
    encrypted_substructs[1] = _encrypt_or_decrypt_substruct(substructs[substruct_order[1]], encryption_key)
    encrypted_substructs[2] = _encrypt_or_decrypt_substruct(substructs[substruct_order[2]], encryption_key)
    encrypted_substructs[3] = _encrypt_or_decrypt_substruct(substructs[substruct_order[3]], encryption_key)

    for i in range(4):
        for j in range(12):
            pokemon_data[32 + (i * 12) + j] = encrypted_substructs[i][j]

    return pokemon_data
