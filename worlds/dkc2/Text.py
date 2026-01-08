from .Names import ItemName

text_mapping = {
    "°": 0x00, # New lines

    "A": 0x41, "B": 0x42, "C": 0x43, "D": 0x44, "E": 0x45, "F": 0x46, "G": 0x47, "H": 0x48, "I": 0x49, "J": 0x4A,
    "K": 0x4B, "L": 0x4C, "M": 0x4D, "N": 0x4E, "O": 0x4F, "P": 0x50, "Q": 0x51, "R": 0x52, "S": 0x53, "T": 0x54,
    "U": 0x55, "V": 0x56, "W": 0x57, "X": 0x58, "Y": 0x59, "Z": 0x5A, "Ñ": 0x4E,

    "!": 0x21, ".": 0x2E, "-": 0x2D, ",": 0x2C, "?": 0x3F, " ": 0x20, ":": 0x3A, ";": 0x3B, "<": 0x3C, "=": 0x3D,
    ">": 0x3E, "/": 0x2F, '"': 0x22, "%": 0x25, "&": 0x26, "'": 0x27, "(": 0x28, ")": 0x29, "*": 0x2A, "+": 0x2B,
    "$": 0x24, "@": 0x40, "#": 0x24,

    "0": 0x30, "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34, "5": 0x35, "6": 0x36, "7": 0x37, "8": 0x38, "9": 0x39,

    "a": 0x61, "b": 0x62, "c": 0x63, "d": 0x64, "e": 0x65, "f": 0x66, "g": 0x67, "h": 0x68, "i": 0x69, "j": 0x6A,
    "k": 0x6B, "l": 0x6C, "m": 0x6D, "n": 0x6E, "o": 0x6F, "p": 0x70, "q": 0x71, "r": 0x72, "s": 0x73, "t": 0x74,
    "u": 0x75, "v": 0x76, "w": 0x77, "x": 0x78, "y": 0x79, "z": 0x7A, "ñ": 0x6E,
}

goal_texts = {
    "flying_krock_items" : [
       #"********************************"
        "",
        "",
        "",
        "",
        "Yo Ho Ho! Landlubber monkeys!",
        "Lost some animals and abilities?",
        "Maybe you'll find them somewhere",
        "alongside my airship. Don't be",
        "hasty! I'm thinking of doing",
        "some good ol' keelhauling later",
        "Har-har-har-har!",
        "",
        "                Kaptain K.Rool  ",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ],
    "flying_krock_tokens": [
        #"********************************"
        "",
        "",
        "",
        "",
        "Yo Ho Ho! Krock got your ape?",
        "I've taken your abilities!",
        "I've taken your pets!",
        "You'll need to defeat TOKENS of my",
        "seadogs to reach my airship.",
        "Donkey Kong will walk the Plank",
        "Har-har-har-har!",
        "",
        "                Kaptain K.Rool  ",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ],
    "lost_world": [
        #"********************************"
        "",
        "",
        "",
        "",
        "Har-har-har you pesky apes!",
        "Your abilities and pets are mine",
        "I've hidden ROCKS rocks to reach ",
        "the kore of the island. Find",
        "them or else... but I warn ya!",
        "Dead monkeys tell no tales in",
        "Crocodile Isle! Har-har-har!",
        "",
        "                Kaptain K.Rool  ",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ],
    "kompletionist_item": [
        #"********************************"
        "",
        "",
        "",
        "",
        "Har-har-har you scurvy dogs!",
        "You'll have to beat me twice to",
        "save that son of a banana eater.",
        "Find my airship and ROCKS Lost",
        "World Rocks or my krew will",
        "blow the ape down!",
        "Har-har-har-har!",
        "",
        "                Kaptain K.Rool  ",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ],
    "kompletionist_tokens": [
        #"********************************"
        "",
        "",
        "",
        "",
        "Avast ye monkey reading this!",
        "I've taken your abilities, pets",
        "and that banana carouser ape!",
        "You'll face this old salt twice!",
        "Reach my airship by defeating TOKENS",
        "of my scallywags and find ROCKS",
        "rocks for the kore or I'll make",
        "some ape shark bait! Har-har-har",
        "",
        "                Kaptain K.Rool  ",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]
}

item_order = [0x00, 0x01, 0x02, 0x03, 0x05, 0x04, 0x06, 0x07, 0x09, 0x0A, 0x0B, 0x08, 0x0D, 0x0C, 0x14, 0x0F, 0x10, 0x11, 0x12, 0x13]
item_names = {
    0x00: "CARRY",
    0x01: "CARTWHEEL",
    0x02: "CLIMB",
    0x03: "CLING",
    0x04: "H.SPIN",
    0x05: "SWIM",
    0x06: "T.ATTACK",
    0x07: "RAMBI",
    0x08: "SQUAWKS",
    0x09: "ENGUARDE",
    0x0A: "SQUITTER",
    0x0B: "RATTLY",
    0x0C: "CLAPPER",
    0x0D: "GLIMMER",
    0x0F: "KANNONS",
    0x10: "B.KONG",
    0x11: "B.CTRL",
    0x12: "B.INVIN",
    0x13: "B.WARP",
    0x14: "S.KART",
    0x28: "GG",
    0x29: "CA",
    0x2A: "KQ",
    0x2B: "KR",
    0x2C: "GU",
    0x2D: "KE",
    0x2E: "FK",
    0x30: "CA",
    0x31: "KQ",
    0x32: "KR",
    0x33: "GU",
    0x34: "KE",
}

classification_colors = [
    0x30,
    0x34,
    0x38,
    0x3C,
    0x2C,
]

shorter_item_names = {
    ItemName.gangplank_galleon: "Galleon Access",
    ItemName.crocodile_cauldron: "Cauldron Access",
    ItemName.krem_quay: "Quay Access",
    ItemName.krazy_kremland: "Kremland Access",
    ItemName.gloomy_gulch: "Gulch Access",
    ItemName.krools_keep: "Keep Access",
    ItemName.the_flying_krock: "Krock Access",
    ItemName.lost_world_cauldron: "Lost World @ Cauldron",
    ItemName.lost_world_quay: "Lost World @ Quay",
    ItemName.lost_world_kremland: "Lost World @ Kremland",
    ItemName.lost_world_gulch: "Lost World @ Gulch",
    ItemName.lost_world_keep: "Lost World @ Keep",

}

def string_to_bytes(input_string: str):
    out_array = bytearray()
    for letter in input_string:
        out_array.append(text_mapping[letter] if letter in text_mapping else text_mapping["*"])
    
    return out_array

def message_received_to_bytes(ctx, message: list, in_map: bool):
    out_array = list()

    for _ in range(0x20):
        if in_map:
            out_array.append(0x80)
            out_array.append(0x22)
        else:
            out_array.append(0x00)
            out_array.append(0x20)
            
    is_tracker = message[0]
    
    if is_tracker:
        # Handle tracker messages
        line_1: str = message[1][:30]
        line_2: str = message[2][:30]
        line: str = line_1.center(32, " ") + line_2.center(32, " ")
        color = 0x20
        for letter in line:
            letter = text_mapping[letter] if letter in text_mapping else text_mapping["*"]
            letter -= 0x20
            if in_map:
                out_array.append(letter + 0x80)
                out_array.append(color | 0x02)
            else:
                out_array.append(letter)
                out_array.append(color)

    else:
        # Handle received/sent messages
        player = message[1].upper()
        item = message[2]
        if item in shorter_item_names:
            item = shorter_item_names[item]
        item = item.upper()
        classification = message[3]
        is_received = message[4]

        idx = 3
        if classification & 0x03 == 0x03:
            idx = 0
        elif classification & 0x01:
            idx = 1
        elif classification & 0x02:
            idx = 2
        elif classification & 0x04:
            idx = 4
        
        if is_received:
            line = f"RECEIVED¡{item}"
        else:
            line = f"SENT¡{item}"
        line = line[:30]
        line = line.center(32, " ")
        color = 0x20
        for letter in line:
            if letter == "¡":
                letter = " "
                color = classification_colors[idx]
            letter = text_mapping[letter] if letter in text_mapping else text_mapping["*"]
            letter -= 0x20
            if in_map:
                out_array.append(letter + 0x80)
                out_array.append(color | 0x02)
            else:
                out_array.append(letter)
                out_array.append(color)

        if is_received:
            line = f"FROM¡{player}"
        else:
            line = f"TO¡{player}"
        line = line[:30]
        line = line.center(32, " ")
        color = 0x20
        for letter in line:
            if letter == "¡":
                letter = " "
                if ctx.slot_info[ctx.slot].name == message[1]:
                    color = 0x24
                else:
                    color = 0x28
            letter = text_mapping[letter] if letter in text_mapping else text_mapping["*"]
            letter -= 0x20
            if in_map:
                out_array.append(letter + 0x80)
                out_array.append(color | 0x02)
            else:
                out_array.append(letter)
                out_array.append(color)

    for _ in range(0x20):
        if in_map:
            out_array.append(0x80)
            out_array.append(0x22)
        else:
            out_array.append(0x00)
            out_array.append(0x20)

    return bytearray(out_array)
