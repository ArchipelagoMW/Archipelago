from BaseClasses import Location
from .data.Zones import ZONE, ZONE_TO_NAME
from .data.Constants import RELIC_NAMES, BASE_LOCATION_ID

LOCATION_TO_ABREV = dict()
ABREV_TO_LOCATION = dict()
AP_ID_TO_NAME = dict()
ZONE_LOCATIONS = dict()
BREAKABLE_LOCATIONS = dict()

locations = {
    # Colosseum items
    "Colosseum Second Part - Bottom Right Room":
        {
            "ap_id": 0,
            "zones": [ZONE["ARE"]],
            "index": 0,
            "entities": [0x3162, 0x3768],
            "as_relic": {"y": 0x0075},
            "vanilla_item": "Heart Vessel",
        },
    "Colosseum First Part - Bottom Left Room":
        {
            "ap_id": 1,
            "zones": [ZONE["ARE"]],
            "index": 1,
            "entities": [0x3180, 0x3808],
            "as_relic": {"y": 0x0078},
            "vanilla_item": "Shield rod",
        },
    "Colosseum Second Part - Bottom Left Room":
        {
            "ap_id": 2,
            "zones": [ZONE["ARE"]],
            "index": 3,
            "entities": [0x34a0, 0x3b28],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Blood cloak",
        },
    "Colosseum First Part - Next to Royal Chapel Passage":
        {
            "ap_id": 3,
            "zones": [ZONE["ARE"]],
            "index": 4,
            "entities": [0x34e6, 0x3ba0],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Knight shield",
        },
    "Colosseum First Part - Before Minotaurus & Werewolf":
        {
            "ap_id": 4,
            "zones": [ZONE["ARE"]],
            "index": 5,
            "entities": [0x352c, 0x3b78],
            "as_relic": {"y": 0x0094},
            "vanilla_item": "Library card",
        },
    "Colosseum First Part - Bottom Right Room":
        {
            "ap_id": 5,
            "zones": [ZONE["ARE"]],
            "index": 6,
            "entities": [0x3482, 0x3b0a],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Green tea",
        },
    "Colosseum Junction Tunnel - Attic":
        {
            "ap_id": 6,
            "zones": [ZONE["ARE"]],
            "index": 7,
            "entities": [0x34be, 0x3b46],
            "as_relic": {"y": 0x0098},
            "vanilla_item": "Holy sword",
        },
    "Colosseum Second Part - Behind Mist Crate":
        {
            "ap_id": 7,
            "zones": [ZONE["ARE"]],
            "index": 2,  # Test if index 2 works
            "entities": [0x304a, 0x36c8],
            "as_item": {"y": 0x0099},
            "vanilla_item": "Form of mist",
        },
    # Catacombs items
    "Catacombs Upper - After Save Point Breakable Wall":
        {
            "ap_id": 8,
            "zones": [ZONE["CAT"]],
            "index": 0,
            "entities": [0x2e28, 0x3708],
            "as_relic": {"x": 0x0020, "y": 0x008f},
            "vanilla_item": "Cat-eye circl.",
        },
    "Catacombs Bottom - Above Discus Lord Breakable Wall Room":
        {
            "ap_id": 9,
            "zones": [ZONE["CAT"]],
            "index": 1,
            "entities": [0x2c3e, 0x351e],
            "as_relic": {"y": 0x0098},
            "vanilla_item": "Icebrand",
        },
    "Catacombs Bottom - After Save Point":
        {
            "ap_id": 10,
            "zones": [ZONE["CAT"]],
            "index": 2,
            "entities": [0x2c20, 0x3500],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Walk armor",
        },
    "Catacombs Bottom - After Granfaloon":
        {
            "ap_id": 11,
            "zones": [ZONE["CAT"]],
            "index": 3,
            "entities": [0x2c02, 0x34e2],
            "as_relic": {"y": 0x0098},
            "vanilla_item": "Mormegil",
        },
    "Catacombs After Dark Spiked Area - Bottom Left Breakable":
        {
            "ap_id": 12,
            "zones": [ZONE["CAT"]],
            "index": 4,
            "entities": [0x3422, 0x3d02],
            "as_relic": {"x": 0x0020, "y": 0x0088},
            "vanilla_item": "Library card",
        },
    "Catacombs Bottom - Above Discus Lord Red Vase 2":
        {
            "ap_id": 13,
            "zones": [ZONE["CAT"]],
            "index": 6,
            "entities": [0x2ea0, 0x3730],
            "as_relic": {},
            "vanilla_item": "Heart Vessel",
        },
    "Catacombs Bottom - Above Discus Lord Red Vase 1":
        {
            "ap_id": 14,
            "zones": [ZONE["CAT"]],
            "index": 7,
            "entities": [0x2eaa, 0x3762],
            "as_relic": {},
            "vanilla_item": "Ballroom mask",
        },
    "Catacombs Upper - After Save Point":
        {
            "ap_id": 15,
            "zones": [ZONE["CAT"]],
            "index": 8,
            "entities": [0x2e32, 0x3712],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Bloodstone",
        },
    "Catacombs Bottom - After Crypt Left Item":
        {
            "ap_id": 16,
            "zones": [ZONE["CAT"]],
            "index": 9,
            "entities": [0x3198, 0x3a78],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Life Vessel",
        },
    "Catacombs Bottom - After Crypt Right Item":
        {
            "ap_id": 17,
            "zones": [ZONE["CAT"]],
            "index": 10,
            "entities": [0x31a2, 0x3a82],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Heart Vessel",
        },
    "Catacombs After Dark Spiked Area - Red Vase 2":
        {
            "ap_id": 18,
            "zones": [ZONE["CAT"]],
            "index": 11,
            "entities": [0x3350, 0x3be0],
            "as_relic": {},
            "vanilla_item": "Cross shuriken",
        },
    "Catacombs After Dark Spiked Area - Red Vase 1":
        {
            "ap_id": 19,
            "zones": [ZONE["CAT"]],
            "index": 12,
            "entities": [0x333c, 0x3bea],
            "as_relic": {},
            "vanilla_item": "Cross shuriken",
        },
    "Catacombs After Dark Spiked Area - Red Vase 4":
        {
            "ap_id": 20,
            "zones": [ZONE["CAT"]],
            "index": 13,
            "entities": [0x335a, 0x3c30],
            "as_relic": {},
            "vanilla_item": "Karma coin",
        },
    "Catacombs After Dark Spiked Area - Red Vase 3":
        {
            "ap_id": 21,
            "zones": [ZONE["CAT"]],
            "index": 14,
            "entities": [0x3346, 0x3c3a],
            "as_relic": {},
            "vanilla_item": "Karma coin",
        },
    "Catacombs After Dark Spiked Area - Bottom Right Item":
        {
            "ap_id": 22,
            "zones": [ZONE["CAT"]],
            "index": 15,
            "entities": [0x3404, 0x3ce4],
            "as_relic": {"x": 0x04d0, "y": 0x0090},
            "vanilla_item": "Pork bun",
        },
    "Catacombs After Dark Spiked Area - Bottom Left Item":
        {
            "ap_id": 23,
            "zones": [ZONE["CAT"]],
            "index": 16,
            "entities": [0x342c, 0x3d2a],
            "as_relic": {"y": 0x0094},
            "vanilla_item": "Spike breaker",
        },
    "Catacombs Bottom - Sarcophagus 1":
        {
            "ap_id": 24,
            "zones": [ZONE["CAT"]],
            "index": 17,
            "entities": [0x3206, 0x3ae6],
            "as_relic": {},
            "vanilla_item": "Monster vial 3",
        },
    "Catacombs Bottom - Sarcophagus 2":
        {
            "ap_id": 25,
            "zones": [ZONE["CAT"]],
            "index": 18,
            "entities": [0x321a, 0x3afa],
            "as_relic": {},
            "vanilla_item": "Monster vial 3",
        },
    "Catacombs Bottom - Sarcophagus 3":
        {
            "ap_id": 26,
            "zones": [ZONE["CAT"]],
            "index": 19,
            "entities": [0x3224, 0x3b04],
            "as_relic": {},
            "vanilla_item": "Monster vial 3",
        },
    "Catacombs Bottom - Sarcophagus 4":
        {
            "ap_id": 27,
            "zones": [ZONE["CAT"]],
            "index": 20,
            "entities": [0x3238, 0x3b18],
            "as_relic": {},
            "vanilla_item": "Monster vial 3",
        },
    # Abandoned Mine items
    "Abandoned Mine Demon Side - Behind Breakable Wall Item 1":
        {
            "ap_id": 28,
            "zones": [ZONE["CHI"]],
            "index": 0,
            "entities": [0x1a34, 0x1dcc],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Power of sire",
        },
    "Abandoned Mine Bottom - Right Item":
        {
            "ap_id": 29,
            "zones": [ZONE["CHI"]],
            "index": 1,
            "entities": [0x1a8e, 0x1dfe],
            "as_relic": {"y": 0x0070},
            "vanilla_item": "Karma coin",
        },
    "Abandoned Mine Demon Side - Item on the Floor":
        {
            "ap_id": 30,
            "zones": [ZONE["CHI"]],
            "index": 4,
            "entities": [0x1d0e, 0x207e],
            "as_relic": {"y": 0x0190},
            "vanilla_item": "Ring of ares",
        },
    "Abandoned Mine Bottom - Left Item":
        {
            "ap_id": 31,
            "zones": [ZONE["CHI"]],
            "index": 5,
            "entities": [0x1a84, 0x1df4],
            "as_relic": {"y": 0x005f},
            "vanilla_item": "Combat knife",
        },
    "Abandoned Mine - Bottom Descend Item 2":
        {
            "ap_id": 32,
            "zones": [ZONE["CHI"]],
            "index": 6,
            "entities": [0x1c6e, 0x1fca],
            "as_relic": {"y": 0x01f0},
            "vanilla_item": "Shiitake",
        },
    "Abandoned Mine - Bottom Descend Item 1":
        {
            "ap_id": 33,
            "zones": [ZONE["CHI"]],
            "index": 7,
            "entities": [0x1c46, 0x1fc0],
            "as_relic": {"y": 0x0190},
            "vanilla_item": "Shiitake",
        },
    "Abandoned Mine Demon Side - Behind Breakable Wall Item 2":
        {
            "ap_id": 34,
            "zones": [ZONE["CHI"]],
            "index": 8,
            "entities": [0x1a3e, 0x1dd6],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Barley tea",
        },
    "Abandoned Mine Demon Side - Behind Breakable Wall Item 3":
        {
            "ap_id": 35,
            "zones": [ZONE["CHI"]],
            "index": 9,
            "entities": [0x1a48, 0x1dc2],
            "as_relic": {"y": 0x0085},
            "vanilla_item": "Peanuts",
        },
    "Abandoned Mine Demon Side - Behind Breakable Wall Item 4":
        {
            "ap_id": 36,
            "zones": [ZONE["CHI"]],
            "index": 10,
            "entities": [0x1a52, 0x1da4],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Peanuts",
        },
    "Abandoned Mine Demon Side - Behind Breakable Wall Item 5":
        {
            "ap_id": 37,
            "zones": [ZONE["CHI"]],
            "index": 11,
            "entities": [0x1a5c, 0x1dae],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Peanuts",
        },
    "Abandoned Mine Demon Side - Behind Breakable Wall Item 6":
        {
            "ap_id": 38,
            "zones": [ZONE["CHI"]],
            "index": 12,
            "entities": [0x1a66, 0x1db8],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Peanuts",
        },
    "Abandoned Mine Demon Side - Item on Breakable Wall":
        {
            "ap_id": 39,
            "zones": [ZONE["CHI"]],
            "despawn": True,
            "entities": [0x1cfa, 0x2074],
            "addresses": [0x045e9602],
            "bin_addresses": [0xf4eee, 0x438d686],
            "rom_address": 0xdfcf6,
            "break_flag": 0x03be3d,
            "break_mask": 0x1,
            "vanilla_item": "Turkey",
        },
    "Abandoned Mine - Middle Descend Left Room":
        {
            "ap_id": 40,
            "zones": [ZONE["CHI"]],
            "index": 2,  # Test if index 2 works
            "entities": [0x1ade, 0x1e62],
            "as_item": {"y": 0x00b8},
            "vanilla_item": "Demon card",
        },
    # Royal Chapel items
    "Royal Chapel Stairs - Red Vase on Alcove 4":
        {
            "ap_id": 41,
            "zones": [ZONE["DAI"]],
            "index": 0,
            "entities": [0x2928, 0x32a6],
            "as_relic": {},
            "vanilla_item": "Ankh of life",
        },
    "Royal Chapel Stairs - Upper Alcove":
        {
            "ap_id": 42,
            "zones": [ZONE["DAI"]],
            "index": 1,
            "entities": [0x2982, 0x3242],
            "as_relic": {},
            "vanilla_item": "Morningstar",
        },
    "Royal Chapel - Item Behind Maria":
        {
            "ap_id": 43,
            "zones": [ZONE["DAI"]],
            "index": 2,
            "entities": [0x281a, 0x31c0],
            "as_relic": {"y": 0x009a},
            "vanilla_item": "Silver ring",
        },
    "Royal Chapel Stairs - Bottom Red Vase":
        {
            "ap_id": 44,
            "zones": [ZONE["DAI"]],
            "index": 3,
            "entities": [0x28ba, 0x3328],
            "as_relic": {},
            "vanilla_item": "Aquamarine",
        },
    "Royal Chapel Stairs - Red Vase on Alcove 1":
        {
            "ap_id": 45,
            "zones": [ZONE["DAI"]],
            "index": 4,
            "entities": [0x28e2, 0x32f6],
            "as_relic": {},
            "vanilla_item": "Mystic pendant",
        },
    "Royal Chapel Stairs - Red Vase on Alcove 2":
        {
            "ap_id": 46,
            "zones": [ZONE["DAI"]],
            "index": 5,
            "entities": [0x28f6, 0x32d8],
            "as_relic": {},
            "vanilla_item": "Magic missile",
        },
    "Royal Chapel Stairs - Red Vase on Alcove 3":
        {
            "ap_id": 47,
            "zones": [ZONE["DAI"]],
            "index": 6,
            "entities": [0x291e, 0x32b0],
            "as_relic": {},
            "vanilla_item": "Shuriken",
        },
    "Royal Chapel Stairs - Red Vase on Alcove 5":
        {
            "ap_id": 48,
            "zones": [ZONE["DAI"]],
            "index": 7,
            "entities": [0x2946, 0x3292],
            "as_relic": {},
            "vanilla_item": "TNT",
        },
    "Royal Chapel Stairs - Red Vase on Alcove 6":
        {
            "ap_id": 49,
            "zones": [ZONE["DAI"]],
            "index": 8,
            "entities": [0x2964, 0x326a],
            "as_relic": {},
            "vanilla_item": "Boomerang",
        },
    "Royal Chapel - Inner Chapel Doorway Roof":
        {
            "ap_id": 50,
            "zones": [ZONE["DAI"]],
            "index": 9,
            "entities": [0x289c, 0x31f2],
            "as_relic": {"y": 0x0120},
            "vanilla_item": "Goggles",
        },
    "Royal Chapel Tower 1 - Top Item":
        {
            "ap_id": 51,
            "zones": [ZONE["DAI"]],
            "index": 10,
            "entities": [0x2da6, 0x36b6],
            "as_relic": {"y": 0x00f0},
            "vanilla_item": "Silver plate",
        },
    "Royal Chapel Tower 1 - Yellow Vase":
        {
            "ap_id": 52,
            "zones": [ZONE["DAI"]],
            "index": 11,
            "entities": [0x2e82, 0x36c0],
            "as_relic": {"y": 0x019f},
            "vanilla_item": "Str. potion",
        },
    "Royal Chapel Tower 1 - Red Vase":
        {
            "ap_id": 53,
            "zones": [ZONE["DAI"]],
            "index": 12,
            "entities": [0x2d9c, 0x36ca],
            "as_relic": {},
            "vanilla_item": "Life Vessel",
        },
    "Royal Chapel Tower 2 - Top Item":
        {
            "ap_id": 54,
            "zones": [ZONE["DAI"]],
            "index": 13,
            "entities": [0x2f5e, 0x38aa],
            "as_relic": {"y": 0x01f0},
            "vanilla_item": "Zircon",
        },
    "Royal Chapel Tower 3 - Top Item":
        {
            "ap_id": 55,
            "zones": [ZONE["DAI"]],
            "index": 14,
            "entities": [0x3026, 0x3972],
            "as_relic": {"y": 0x00ef},
            "vanilla_item": "Cutlass",
        },
    "Royal Chapel Tower 3 - Red Vase":
        {
            "ap_id": 56,
            "zones": [ZONE["DAI"]],
            "index": 15,
            "entities": [0x3008, 0x397c],  # TODO [ 0x2e82, 0x36c0 ] was wrong
            "as_relic": {},
            "vanilla_item": "Potion",
        },
    # Long Library items
    "Long Library - Deeper Library Upper Part Flame on Table":
        {
            "ap_id": 57,
            "zones": [ZONE["LIB"]],
            "index": 1,
            "entities": [0x3312, 0x39ac],
            "as_relic": {},
            "vanilla_item": "Stone mask",
        },
    "Long Library - Deeper Library Behind Bookshelf Item 2":
        {
            "ap_id": 58,
            "zones": [ZONE["LIB"]],
            "index": 2,
            "entities": [0x35b0, 0x3c5e],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Holy rod",
        },
    "Long Library - Item Bellow Librarian":
        {
            "ap_id": 59,
            "zones": [ZONE["LIB"]],
            "index": 4,
            "entities": [0x3286, 0x398e],
            "as_relic": {"y": 0x01b0},
            "vanilla_item": "Bronze cuirass"
        },
    "Long Library - Deeper Library Lower Part Statue 1":
        {
            "ap_id": 60,
            "zones": [ZONE["LIB"]],
            "index": 5,
            "entities": [0x377c, 0x3f10],
            "as_relic": {},
            "vanilla_item": "Takemitsu",
        },
    "Long Library - Deeper Library Lower Part Statue 2":
        {
            "ap_id": 61,
            "zones": [ZONE["LIB"]],
            "index": 6,
            "entities": [0x3786, 0x3f1a],
            "as_relic": {},
            "vanilla_item": "Onyx",
        },
    "Long Library - Deeper Library Lower Part Red Vase":
        {
            "ap_id": 62,
            "zones": [ZONE["LIB"]],
            "index": 7,
            "entities": [0x379a, 0x3f24],
            "as_relic": {},
            "vanilla_item": "Frankfurter",
        },
    "Long Library - Top Left Room Item 2":
        {
            "ap_id": 63,
            "zones": [ZONE["LIB"]],
            "index": 8,
            "entities": [0x357e, 0x3c36],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Potion",
        },
    "Long Library - Top Left Room Item 3":
        {
            "ap_id": 64,
            "zones": [ZONE["LIB"]],
            "index": 9,
            "entities": [0x3588, 0x3c40],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Antivenom",
        },
    "Long Library - Deeper Library Behind Bookshelf Item 1":
        {
            "ap_id": 65,
            "zones": [ZONE["LIB"]],
            "index": 10,
            "entities": [0x35a6, 0x3c68],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Topaz circlet",
        },
    "Long Library - Deeper Library Behind Mist Crate":
        {
            "ap_id": 66,
            "zones": [ZONE["LIB"]],
            "index": 0,  # Test if index 0 works
            "entities": [0x3826, 0x3f06],
            "as_item": {},
            "vanilla_item": "Soul of bat",
        },
    "Long Library - Top Right Floor":
        {
            "ap_id": 67,
            "zones": [ZONE["LIB"]],
            "index": 3,  # Test if index 3 works
            "entities": [0x3510, 0x3a92],
            "as_item": {"y": 0x00b9},
            "vanilla_item": "Faerie scroll"
        },
    "Long Library - Top Left Room Item 1":
        {
            "ap_id": 68,
            "zones": [ZONE["LIB"]],
            "index": 11,
            "entities": [0x3574, 0x3c2c],
            "as_item": {"y": 0x00b9},
            "vanilla_item": "Faerie card",
        },
    "Long Library - Librarian Shop Item":
        {
            "ap_id": 69,
            "zones": [ZONE["LIB"]],
            "addresses": [0x047a321c],
            # bin for jewel item 0xf4f3a/0x438d6d2
            # rom_address 0x0dfd42
            "vanilla_item": "Jewel of open"
        },
    # Marble Galley items
    "Marble Gallery - Left Clock Before Olrox's Quarter":
        {
            "ap_id": 70,
            "zones": [ZONE["NO0"]],
            "index": 0,
            "entities": [0x3652, 0x44d2],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Life Vessel",
        },
    "Marble Gallery - Right Clock Item 1":
        {
            "ap_id": 71,
            "zones": [ZONE["NO0"]],
            "index": 1,
            "entities": [0x3670, 0x44f0],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Alucart shield",
        },
    "Marble Gallery - Right Clock Item 2":
        {
            "ap_id": 72,
            "zones": [ZONE["NO0"]],
            "index": 2,
            "entities": [0x367a, 0x44fa],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Heart Vessel",
        },
    "Marble Gallery - Middle clock Left Item 1":
        {
            "ap_id": 73,
            "zones": [ZONE["NO0"]],
            "index": 3,
            "entities": [0x296c, 0x37f6],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Life apple",
        },
    "Marble Gallery - Middle clock Left Item 2":
        {
            "ap_id": 74,
            "zones": [ZONE["NO0"]],
            "index": 4,
            "entities": [0x2976, 0x3800],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Hammer",
        },
    "Marble Gallery - Middle clock Left Item 3":
        {
            "ap_id": 75,
            "zones": [ZONE["NO0"]],
            "index": 5,
            "entities": [0x2980, 0x380a],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Potion",
        },
    "Marble Gallery - Right Clock Item 3":
        {
            "ap_id": 76,
            "zones": [ZONE["NO0"]],
            "index": 6,
            "entities": [0x3698, 0x4518],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Alucart mail",
        },
    "Marble Gallery - Right Clock Item 4":
        {
            "ap_id": 77,
            "zones": [ZONE["NO0"]],
            "index": 7,
            "entities": [0x36a2, 0x4522],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Alucart sword",
        },
    "Marble Gallery - Inside Clock Left Item":
        {
            "ap_id": 78,
            "zones": [ZONE["NO0"]],
            "index": 8,
            "entities": [0x36c0, 0x4540],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Life Vessel",
        },
    "Marble Gallery - Inside Clock Right Item":
        {
            "ap_id": 79,
            "zones": [ZONE["NO0"]],
            "index": 9,
            "entities": [0x36ca, 0x454a],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Heart Vessel",
        },
    "Marble Gallery - Bellow Red Trap Door Right Item":
        {
            "ap_id": 80,
            "zones": [ZONE["NO0"]],
            "index": 10,
            "entities": [0x3742, 0x45b8],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Library card",
        },
    "Marble Gallery - Bellow Red Trap Door Left Item":
        {
            "ap_id": 81,
            "zones": [ZONE["NO0"]],
            "index": 11,
            "entities": [0x372e, 0x45c2],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Attack potion",
        },
    "Marble Gallery - Descend to Entrance Item 2":
        {
            "ap_id": 82,
            "zones": [ZONE["NO0"]],
            "index": 12,
            "entities": [0x3134, 0x3fa0],
            "as_relic": {},
            "vanilla_item": "Hammer",
        },
    "Marble Gallery - Descend to Entrance Item 1":
        {
            "ap_id": 83,
            "zones": [ZONE["NO0"]],
            "index": 13,
            "entities": [0x3170, 0x3f14],
            "as_relic": {"y": 0x00f9},
            "vanilla_item": "Str. potion",
        },
    "Marble Gallery - Item Given by Maria":
        {
            "ap_id": 84,
            "zones": [ZONE["CEN"]],
            "addresses": [0x0456e368],
            "erase":
                {
                    "instructions": [{"addresses": [0x0456e360], "instruction": 0x08063ff6}]
                },
            "break_flag": 0x03bec4,
            "break_mask": 0x1,
            "vanilla_item": "Holy glasses",
        },
    "Marble Gallery - Descend to Entrance Item 3":
        {
            "ap_id": 85,
            "zones": [ZONE["NO0"]],
            "index": 14,
            "entities": [0x309e, 0x3ff0],
            "as_item": {"x": 0x0043},
            "vanilla_item": "Spirit orb"
        },
    "Marble Gallery - Middle clock Right Item":
        {
            "ap_id": 86,
            "zones": [ZONE["NO0"]],
            "index": 15,
            "entities": [0x298a, 0x37ec],
            "as_item": {"y": 0x00b9},
            "vanilla_item": "Gravity boots",
        },
    # Outer Wall items
    "Outer Wall - Item 1 Behind Mist Grate":
        {
            "ap_id": 87,
            "zones": [ZONE["NO1"]],
            "index": 0,
            "entities": [0x36d4, 0x3eba],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Jewel knuckles"
        },
    "Outer Wall - Item 2 Behind Mist Grate":
        {
            "ap_id": 88,
            "zones": [ZONE["NO1"]],
            "index": 1,
            "entities": [0x36e8, 0x3ec4],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Mirror cuirass",
        },
    "Outer Wall - Red Vase Near Elevator Switch":
        {
            "ap_id": 89,
            "zones": [ZONE["NO1"]],
            "index": 2,
            "entities": [0x3b34, 0x4220],
            "as_relic": {},
            "vanilla_item": "Heart Vessel"
        },
    "Outer Wall - Yellow Vase on High Ledge":
        {
            "ap_id": 90,
            "zones": [ZONE["NO1"]],
            "index": 3,
            "entities": [0x37ba, 0x3f6e],
            "as_relic": {},
            "vanilla_item": "Garnet",
        },
    "Outer Wall - Item After Doppleganger 10":
        {
            "ap_id": 91,
            "zones": [ZONE["NO1"]],
            "index": 4,
            "entities": [0x363e, 0x3e24],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Gladius"
        },
    "Outer Wall - Red Vase After Doppleganger 10":
        {
            "ap_id": 92,
            "zones": [ZONE["NO1"]],
            "index": 5,
            "entities": [0x3bc0, 0x4450],
            "as_relic": {},
            "vanilla_item": "Life Vessel"
        },
    "Outer Wall - Red Vase Near Marble Gallery Door":
        {
            "ap_id": 93,
            "zones": [ZONE["NO1"]],
            "index": 6,
            "entities": [0x3774, 0x3f3c],
            "as_relic": {},
            "vanilla_item": "Zircon"
        },
    "Outer Wall - Breakable Wall in Room Behind Armor Lord":
        {
            "ap_id": 94,
            "zones": [ZONE["NO1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x3698, 0x3e7e],
            "addresses": [0x04a197d8],
            "bin_addresses": [0xf4ed4, 0x438d66c],
            "rom_address": 0xdfcdc,
            "break_flag": 0x03bdfe,
            "break_mask": 0x1,
            "vanilla_item": "Pot roast"
        },
    "Outer Wall - Inside of Elevator":
        {
            "ap_id": 95,
            "zones": [ZONE["NO1"]],
            "index": 7,
            "entities": [0x3c2e, 0x4356],
            "as_item": {"y": 0x0331},
            "vanilla_item": "Soul of wolf"
        },
    # Olrox's Quarters items
    "Olrox\'s Quarters Path to Royal Chapel - On Wooden Display":
        {
            "ap_id": 96,
            "zones": [ZONE["NO2"]],
            "index": 1,
            "entities": [0x3718, 0x3e7c],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Heart Vessel",
        },
    "Olrox\'s Quarters Lower Part - Room Behind Breakable Wall Vase 3":
        {
            "ap_id": 97,
            "zones": [ZONE["NO2"]],
            "index": 4,
            "entities": [0x34c0, 0x3bd4],
            "as_relic": {},
            "vanilla_item": "Broadsword",
        },
    "Olrox\'s Quarters Lower Part - Room Behind Breakable Wall Vase 2":
        {
            "ap_id": 98,
            "zones": [ZONE["NO2"]],
            "index": 5,
            "entities": [0x34b6, 0x3bde],
            "as_relic": {},
            "vanilla_item": "Onyx",
        },
    "Olrox\'s Quarters Lower Part - Room Behind Breakable Wall Vase 1":
        {
            "ap_id": 99,
            "zones": [ZONE["NO2"]],
            "index": 6,
            "entities": [0x34ac, 0x3be8],
            "as_relic": {},
            "vanilla_item": "Cheese",
        },
    "Olrox\'s Quarters Upper Part - Ascend Shaft Red Vase 1":
        {
            "ap_id": 100,
            "zones": [ZONE["NO2"]],
            "index": 7,
            "entities": [0x3970, 0x40ac],
            "as_relic": {},
            "vanilla_item": "Manna prism",
         },
    "Olrox\'s Quarters Upper Part - Ascend Shaft Red Vase 2":
        {
            "ap_id": 101,
            "zones": [ZONE["NO2"]],
            "index": 8,
            "entities": [0x397a, 0x40a2],
            "as_relic": {},
            "vanilla_item": "Resist fire",
        },
    "Olrox\'s Quarters Upper Part - Ascend Shaft Red Vase 3":
        {
            "ap_id": 102,
            "zones": [ZONE["NO2"]],
            "index": 9,
            "entities": [0x3984, 0x4098],
            "as_relic": {},
            "vanilla_item": "Luck potion",
        },
    "Olrox\'s Quarters Upper Part - Ledge Before Drop to Courtyard":
        {
            "ap_id": 103,
            "zones": [ZONE["NO2"]],
            "index": 10,
            "entities": [0x34e8, 0x3c06],
            "as_relic": {},
            "vanilla_item": "Estoc",
        },
    "Olrox\'s Quarters - Hole Before Olrox":
        {
            "ap_id": 104,
            "zones": [ZONE["NO2"]],
            "index": 11,
            "entities": [0x3470, 0x3b98],
            "as_relic": {"y": 0x00d0},
            "vanilla_item": "Iron ball",
        },
    "Olrox\'s Quarters Courtyard - Right Room":
        {
            "ap_id": 105,
            "zones": [ZONE["NO2"]],
            "index": 12,
            "entities": [0x3434, 0x3b5c],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Garnet",
        },
    "Olrox\'s Quarters - After Olrox":
        {
            "ap_id": 106,
            "zones": [ZONE["NO2"]],
            "index": 0,
            "entities": [0x35f6, 0x3d1e],
            "as_item": {"y": 0x009d},
            "vanilla_item": "Echo of bat",
        },
    "Olrox\'s Quarters Path to Royal Chapel - Hidden Attic":
        {
            "ap_id": 107,
            "zones": [ZONE["NO2"]],
            "index": 2,
            "entities": [0x3416, 0x3b3e],
            "as_item": {"y": 0x009c},
            "vanilla_item": "Sword card",
        },
    # Castle Entrance items
    "Entrance - Above First Encounter With Death":
        {
            "ap_id": 108,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 0,
            "entities": [0x3e68, 0x45f4, 0x3c08, 0x4344],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Heart Vessel"
        },
    "Entrance - Right Alcove in Cube of Zoe Room":
        {
            "ap_id": 109,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 1,
            "entities": [0x3e86, 0x4612, 0x3c26, 0x4362],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Life Vessel"
        },
    "Entrance - Wolf/Bat Secret Room Right Item":
        {
            "ap_id": 110,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 2,
            "entities": [0x40a2, 0x4824, 0x3e60, 0x4588],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Life apple",
        },
    "Entrance - Behind Stone Wall in Cube of Zoe Room":
        {
            "ap_id": 111,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 4,
            "entities": [0x4156, 0x48ba, 0x3f1e, 0x4632],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Shield potion"
        },
    "Entrance - Attic Above Mermans":
        {
            "ap_id": 112,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 5,
            "entities": [0x3ea4, 0x4630, 0x3c44, 0x4380],
            "as_relic": {"y": 0x0050},
            "vanilla_item": "Holy mail",
        },
    "Entrance - By Underground Caverns Bottom Exit":
        {
            "ap_id": 113,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 6,
            "entities": [0x4228, 0x49b4, 0x400e, 0x474a],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Life Vessel",
        },
    "Entrance - Castle Entrance Teleport Exit":
        {
            "ap_id": 114,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 7,
            "entities": [0x4066, 0x47f2, 0x3e1a, 0x4556],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Heart Vessel"
        },
    "Entrance - Attic Near Start Gate Right item":
        {
            "ap_id": 115,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 8,
            "entities": [0x41ec, 0x491e, 0x3fd2, 0x4696],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Life Vessel",
        },
    "Entrance - Wolf/Bat Secret Room Left Item":
        {
            "ap_id": 116,
            "zones": [ZONE["NP3"]],
            "index": 9,
            "entities": [0x3e56, 0x459c],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Jewel sword",
        },
    "Entrance - Breakable Wall Above Merman":
        {
            "ap_id": 117,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x4304, 0x4a4a, 0x40e0, 0x47cc],
            "addresses": [0x04ba9774, 0x05431554],
            "bin_addresses": [0xf4ed6, 0x438d66e],
            "rom_address": 0xdfcde,
            "break_flag": 0x03be1f,
            "break_mask": 0x1,
            "vanilla_item": "Pot roast"
        },
    "Entrance - Breakable Ledge Before Death":
        {
            "ap_id": 118,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x3fd0, 0x4752, 0x3d70, 0x4498],
            "addresses": [0x04baa2b0, 0x05431f60],
            "bin_addresses": [0xf4ed8, 0x438d670],
            "rom_address": 0xdfce0,
            "break_flag": 0x03be24,
            "break_mask": 0x1,
            "vanilla_item": "Turkey"
        },
    "Entrance - Pedestal in Cube of Zoe Room":
        {
            "ap_id": 119,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 3,  # Test if index 3 works
            "entities": [0x411a, 0x48a6, 0x3ece, 0x460a],
            "as_item": {"y": 0x007b},
            "vanilla_item": "Cube of zoe"
        },
    "Entrance - Attic Near Start Gate Left item":
        {
            "ap_id": 120,
            "zones": [ZONE["NO3"], ZONE["NP3"]],
            "index": 10,
            "entities": [0x41e2, 0x4914, 0x3fbe, 0x468c],
            "as_item": {"y": 0x00c8},
            "vanilla_item": "Power of wolf",
        },
    # Underground Caverns items
    "Underground Caverns - Wooden Stand Close to Stairway":
        {
            "ap_id": 121,
            "zones": [ZONE["NO4"], ZONE["NO4"]],
            "index": 0,
            "entities": [0x3316, 0x439e, 0x380c, 0x4ace],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Heart Vessel"
        },
    "Underground Caverns - Middle of Stairway Room":
        {
            "ap_id": 122,
            "zones": [ZONE["NO4"]],
            "index": 1,
            "entities": [0x3334, 0x43bc],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Life Vessel"
        },
    "Underground Caverns Scylla Area - After Fight Item":
        {
            "ap_id": 123,
            "zones": [ZONE["NO4"], ZONE["BO3"]],
            "index": 2,
            "entities": [0x3352, 0x43da, 0x1e42, 0x2006],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Crystal cloak"
        },
    "Underground Caverns - Top Underwater Item":
        {
            "ap_id": 124,
            "zones": [ZONE["NO4"]],
            "index": 4,
            "entities": [0x3a6e, 0x4ca4],
            "as_relic": {"y": 0x0150},
            "vanilla_item": "Antivenom"
        },
    "Underground Caverns - Bottom Underwater Item":
        {
            "ap_id": 125,
            "zones": [ZONE["NO4"]],
            "index": 5,
            "entities": [0x3a64, 0x4cea],
            "as_relic": {"y": 0x01c2},
            "vanilla_item": "Life Vessel"
        },
    "Underground Caverns - Hidden Room Behind Waterfall":
        {
            "ap_id": 126,
            "zones": [ZONE["NO4"]],
            "index": 6,
            "entities": [0x3f6e, 0x5000],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Life Vessel"
        },
    "Underground Caverns - Top Left Room From Waterfall":
        {
            "ap_id": 127,
            "zones": [ZONE["NO4"]],
            "index": 7,
            "entities": [0x3fa0, 0x503c],
            "as_relic": {"y": 0x00b5},
            "vanilla_item": "Herald shield"
        },
    "Underground Caverns - Red Vase on Ledge Next to Marble Gallery":
        {
            "ap_id": 128,
            "zones": [ZONE["NO4"]],
            "index": 9,
            "entities": [0x329e, 0x4308],
            "as_relic": {},
            "vanilla_item": "Zircon"
        },
    "Underground Caverns Succubus Side - Succubus item":
        {
            "ap_id": 129,
            "zones": [ZONE["NO4"]],
            "index": 10,
            "entities": [0x4270, 0x52ee],
            "addresses": [0x04c324b4],
            "tile_id": True,
            "vanilla_item": "Gold ring"
        },
    "Underground Caverns - Breakable Wall Close to Stairway":
        {
            "ap_id": 130,
            "zones": [ZONE["NO4"]],
            "index": 11,
            "entities": [0x3262, 0x42ea],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Bandanna"
        },
    "Underground Caverns - Bottom of Stairway":
        {
            "ap_id": 131,
            "zones": [ZONE["NO4"]],
            "index": 12,
            "entities": [0x3550, 0x461e],
            "as_relic": {"y": 0x08a0},
            "vanilla_item": "Shiitake"
        },
    "Underground Caverns Succubus Side - Red Vase 1":
        {
            "ap_id": 132,
            "zones": [ZONE["NO4"]],
            "index": 13,
            "entities": [0x3406, 0x4448],
            "as_relic": {},
            "vanilla_item": "Claymore"
        },
    "Underground Caverns Succubus Side - Red Vase 2":
        {
            "ap_id": 133,
            "zones": [ZONE["NO4"]],
            "index": 14,
            "entities": [0x3640, 0x46b4],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Underground Caverns Succubus Side - Red Vase 3":
        {
            "ap_id": 134,
            "zones": [ZONE["NO4"]],
            "index": 15,
            "entities": [0x364a, 0x46be],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Underground Caverns Succubus Side - Red Vase 4":
        {
            "ap_id": 135,
            "zones": [ZONE["NO4"]],
            "index": 16,
            "entities": [0x362c, 0x46c8],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Underground Caverns Succubus Side - Red Vase 5":
        {
            "ap_id": 136,
            "zones": [ZONE["NO4"]],
            "index": 17,
            "entities": [0x3636, 0x46d2],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Underground Caverns Succubus Side - Red Vase 6":
        {
            "ap_id": 137,
            "zones": [ZONE["NO4"]],
            "index": 18,
            "entities": [0x3654, 0x46dc],
            "as_relic": {},
            "vanilla_item": "Moonstone"
        },
    "Underground Caverns Scylla Area - Right item":
        {
            "ap_id": 138,
            "zones": [ZONE["NO4"], ZONE["BO3"]],
            "index": 19,
            "entities": [0x423e, 0x52bc, 0x1e24, 0x1fde],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Scimitar"
        },
    "Underground Caverns Scylla Area - Left item":
        {
            "ap_id": 139,
            "zones": [ZONE["NO4"], ZONE["BO3"]],
            "index": 20,
            "entities": [0x4216, 0x52c6, 0x1df2, 0x1fe8],
            "as_relic": {"y": 0x00c8},
            "vanilla_item": "Resist ice"
        },
    "Underground Caverns Scylla Area - Red Vase":
        {
            "ap_id": 140,
            "zones": [ZONE["NO4"], ZONE["BO3"]],
            "index": 21,
            "entities": [0x41da, 0x5262, 0x1d5c, 0x1f20],
            "as_relic": {},
            "vanilla_item": "Pot roast"
        },
    "Underground Caverns Ice Area - On Alcove":
        {
            "ap_id": 141,
            "zones": [ZONE["NO4"]],
            "index": 22,
            "entities": [0x3d16, 0x4d6c],
            "tile_index": 1,
            "as_relic": {"x": 0x053f, "y": 0x0052},
            "vanilla_item": "Onyx"
        },
    "Underground Caverns Ice Area - Underwater Item 1":
        {
            "ap_id": 142,
            "zones": [ZONE["NO4"]],
            "index": 23,
            "entities": [0x3c80, 0x4e66],
            "as_relic": {"y": 0x00f5},
            "vanilla_item": "Knuckle duster"
        },
    "Underground Caverns Ice Area - Underwater Item 2":
        {
            "ap_id": 143,
            "zones": [ZONE["NO4"]],
            "index": 24,
            "entities": [0x3cee, 0x4e70],
            "as_relic": {},
            "vanilla_item": "Life Vessel"
        },
    "Underground Caverns Ice Area - Underwater Item 3":
        {
            "ap_id": 144,
            "zones": [ZONE["NO4"]],
            "index": 25,
            "entities": [0x3dd4, 0x4e7a],
            "as_relic": {"y": 0x0130},
            "vanilla_item": "Elixir"
        },
    "Underground Caverns - Bellow Stairway":
        {
            "ap_id": 145,
            "zones": [ZONE["NO4"]],
            "index": 26,
            "entities": [0x3c58, 0x4b3c],
            "as_relic": {"y": 0x0060},
            "vanilla_item": "Toadstool"
        },
    "Underground Caverns - Alcove Next to Drowned Guards":
        {
            "ap_id": 146,
            "zones": [ZONE["NO4"]],
            "index": 27,
            "entities": [0x3bea, 0x4b0a],
            "as_relic": {"y": 0x0050},
            "vanilla_item": "Shiitake"
        },
    "Underground Caverns - Bellow Wooden Bridge Left Item":
        {
            "ap_id": 147,
            "zones": [ZONE["NO4"]],
            "index": 28,
            "entities": [0x4130, 0x51fe],
            "as_relic": {"y": 0x00d0},
            "vanilla_item": "Life Vessel"
        },
    "Underground Caverns - Bellow Wooden Bridge Right Item":
        {
            "ap_id": 148,
            "zones": [ZONE["NO4"]],
            "index": 29,
            "as_relic": {"y": 0x00d0},
            "entities": [0x4176, 0x5208],
            "vanilla_item": "Heart Vessel"
        },
    "Underground Caverns - Underwater Stream":
        {
            "ap_id": 149,
            "zones": [ZONE["NO4"]],
            "index": 30,
            "entities": [0x3f28, 0x4fb0],
            "as_relic": {"y": 0x00d0},
            "vanilla_item": "Pentagram"
        },
    "Underground Caverns - Alcove Behind Waterfall":
        {
            "ap_id": 150,
            "zones": [ZONE["NO4"]],
            "index": 31,
            "entities": [0x37da, 0x47e0],
            "as_relic": {"x": 0x0110, "y": 0x021f},
            "vanilla_item": "Secret boots"
        },
    "Underground Caverns - Waterfall Upper Item":
        {
            "ap_id": 151,
            "zones": [ZONE["NO4"]],
            "index": 32,
            "entities": [0x36cc, 0x47ea],
            "as_relic": {"x": 0x0030},
            "vanilla_item": "Shiitake"
        },
    "Underground Caverns - Waterfall Bottom Item":
        {
            "ap_id": 152,
            "zones": [ZONE["NO4"]],
            "index": 33,
            "entities": [0x36d6, 0x4876],
            "as_relic": {"x": 0x0040, "y": 0x051c},
            "vanilla_item": "Toadstool"
        },
    "Underground Caverns - Next to Castle Entrance Passage":
        {
            "ap_id": 153,
            "zones": [ZONE["NO4"]],
            "index": 35,
            "entities": [0x36ae, 0x4736],
            "as_relic": {"y": 0x0095},
            "vanilla_item": "Shiitake"
        },
    "Underground Caverns - Air Pocket Item":
        {
            "ap_id": 154,
            "zones": [ZONE["NO4"]],
            "index": 36,
            "entities": [0x3c4e, 0x4c72],
            "as_relic": {"y": 0x00f2},
            "vanilla_item": "Nunchaku"
        },
    "Underground Caverns Ice Area - After Ferryman":
        {
            "ap_id": 155,
            "zones": [ZONE["NO4"]],
            "index": 3,  # Test if index 3 works
            "entities": [0x3ea6, 0x4f38],
            "as_item": {"y": 0x00b9},
            "vanilla_item": "Holy symbol"
        },
    "Underground Caverns - After Ferryman":
        {
            "ap_id": 156,
            "zones": [ZONE["NO4"]],
            "index": 8,  # Test if index 8 works
            "entities": [0x4004, 0x50aa],
            "as_item": {"y": 0x00b9},
            "vanilla_item": "Merman statue"
        },
    # Alchemy Laboratory items
    "Alchemy Lab. - Globe by the Bottom Entrance":
        {
            "ap_id": 157,
            "zones": [ZONE["NZ0"]],
            "index": 0,
            "entities": [0x2df2, 0x377c],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Hide cuirass"
        },
    "Alchemy Lab. - Globe in Hidden Room Behind Breakable Wall":
        {
            "ap_id": 158,
            "zones": [ZONE["NZ0"]],
            "index": 1,
            "entities": [0x2eec, 0x3844],
            "as_relic": {},
            "vanilla_item": "Heart Vessel"
        },
    "Alchemy Lab. - Globe After Spike Puzzle":
        {
            "ap_id": 159,
            "zones": [ZONE["NZ0"]],
            "index": 2,
            "entities": [0x2f32, 0x388a],
            "as_relic": {},
            "vanilla_item": "Cloth cape"
        },
    "Alchemy Lab. - Tank in Hidden Basement on Breakable Floor":
        {
            "ap_id": 160,
            "zones": [ZONE["NZ0"]],
            "index": 3,
            "entities": [0x2a28, 0x338a],
            "as_relic": {"x": 0x0080, "y": 0x01b0},
            "vanilla_item": "Life Vessel"
        },
    "Alchemy Lab. - Globe on Middle Elevator Shaft Room":
        {
            "ap_id": 161,
            "zones": [ZONE["NZ0"]],
            "index": 6,
            "entities": [0x3108, 0x3a60],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Sunglasses"
        },
    "Alchemy Lab. - Flame on Table Middle Way Up":
        {
            "ap_id": 162,
            "zones": [ZONE["NZ0"]],
            "index": 7,
            "entities": [0x2956, 0x32c2],
            "as_relic": {"x": 0x0080, "y": 0x01a5},
            "vanilla_item": "Resist thunder"
        },
    "Alchemy Lab. - Flame Near Spike Switch":
        {
            "ap_id": 163,
            "zones": [ZONE["NZ0"]],
            "index": 8,
            "entities": [0x2cf8, 0x36b4],
            "as_relic": {"y": 0x01c0},
            "vanilla_item": "Leather shield"
        },
    "Alchemy Lab. - Item by Cannon":
        {
            "ap_id": 164,
            "zones": [ZONE["NZ0"]],
            "index": 9,
            "entities": [0x2ca8, 0x360a],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Basilard"
        },
    "Alchemy Lab. - Globe in Big Room With Axe Lord and Spittle Bone":
        {
            "ap_id": 165,
            "zones": [ZONE["NZ0"]],
            "index": 10,
            "entities": [0x2b72, 0x3556],
            "as_relic": {},
            "vanilla_item": "Potion"
        },
    "Alchemy Lab. - Globe in Attic With Powerup Tanks":
        {
            "ap_id": 166,
            "zones": [ZONE["NZ0"]],
            "index": 4,
            "entities": [0x3054, 0x3998],
            "replace_with_relic": False,
            "addresses": [0x054b1d5a],
            "as_item": {"x": 0x007e, "y": 0x00b9},
            "vanilla_item": "Skill of wolf"
        },
    "Alchemy Lab. - Globe in Upper-left Room of Slogra and Gaibon":
        {
            "ap_id": 167,
            "zones": [ZONE["NZ0"], ZONE["NZ0"]],
            "index": 5,
            "entities": [0x2a8c, 0x33d0, 0x2ad2, 0x343e],
            "replace_with_relic": False,
            "addresses": [0x054b1d58],
            "as_item": {"x": 0x007e, "y": 0x00b9},
            "vanilla_item": "Bat card"
        },
    # Clock tower items
    "Clock Tower - Bellow Broken Bridge Item 2":
        {
            "ap_id": 168,
            "zones": [ZONE["NZ1"]],
            "index": 0,
            "entities": [0x2a52, 0x34ea],
            "as_relic": {"y": 0x03b0},
            "vanilla_item": "Magic missile"
        },
    "Clock Tower - Bellow Broken Bridge Item 1":
        {
            "ap_id": 169,
            "zones": [ZONE["NZ1"]],
            "index": 1,
            "entities": [0x2a0c, 0x34f4],
            "as_relic": {"y": 0x03b0},
            "vanilla_item": "Pentagram"
        },
    "Clock Tower - Rotating Gears Puzzle Room Item 1":
        {
            "ap_id": 170,
            "zones": [ZONE["NZ1"]],
            "index": 3,
            "entities": [0x284a, 0x327e],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Star flail"
        },
    "Clock Tower - Rotating Gears Puzzle Room Item 2":
        {
            "ap_id": 171,
            "zones": [ZONE["NZ1"]],
            "index": 4,
            "entities": [0x287c, 0x3288],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Gold plate"
        },
    "Clock Tower - Rotating Gears Puzzle Room Item 3":
        {
            "ap_id": 172,
            "zones": [ZONE["NZ1"]],
            "index": 5,
            "entities": [0x2886, 0x3292],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Steel helm"
        },
    "Clock Tower - Behind Breakable Wall Close to Bronze Statue":
        {
            "ap_id": 173,
            "zones": [ZONE["NZ1"]],
            "index": 6,
            "entities": [0x2d18, 0x372e],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Healing mail"
        },
    "Clock Tower - On Top of Column Item 2":
        {
            "ap_id": 174,
            "zones": [ZONE["NZ1"]],
            "index": 7,
            "entities": [0x29e4, 0x33c8],
            "as_relic": {"y": 0x0280},
            "vanilla_item": "Bekatowa"
        },
    "Clock Tower - On Top of Column Item 1":
        {
            "ap_id": 175,
            "zones": [ZONE["NZ1"]],
            "index": 8,
            "entities": [0x29c6, 0x33d2],
            "as_relic": {"y": 0x0290},
            "vanilla_item": "Shaman shield"
        },
    "Clock Tower - On Top of Column Item 3":
        {
            "ap_id": 176,
            "zones": [ZONE["NZ1"]],
            "index": 9,
            "entities": [0x2a02, 0x33dc],
            "as_relic": {"y": 0x0290},
            "vanilla_item": "Ice mail"
        },
    "Clock Tower - Gears Puzzle Room Breakable Wall Room Left Item":
        {
            "ap_id": 177,
            "zones": [ZONE["NZ1"]],
            "index": 10,
            "entities": [0x243a, 0x2e5a],
            "as_relic": {"y": 0x01a0},
            "vanilla_item": "Life Vessel"
        },
    "Clock Tower - Gears Puzzle Room Breakable Wall Room Right Item":
        {
            "ap_id": 178,
            "zones": [ZONE["NZ1"]],
            "index": 11,
            "entities": [0x2458, 0x2e64],
            "as_relic": {"y": 0x01a0},
            "vanilla_item": "Heart Vessel"
        },
    "Clock Tower - Before Karasuman Breakable Wall Item 2":
        {
            "ap_id": 179,
            "zones": [ZONE["NZ1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2d68, 0x379c],
            "addresses": [0x055737a4],
            "bin_addresses": [0xf4eda, 0x438d672],
            "rom_address": 0xdfce2,
            "break_flag": 0x03be8f,
            "break_mask": 0x4,
            "vanilla_item": "Bwaka knife"
        },
    "Clock Tower - After Rotating Gears Behind Breakable Wall":
        {
            "ap_id": 180,
            "zones": [ZONE["NZ1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2caa, 0x363e],
            "addresses": [0x0557379c],
            "bin_addresses": [0xf4edc, 0x438d674],
            "rom_address": 0xdfce4,
            "break_flag": 0x03be8f,
            "break_mask": 0x1,
            "vanilla_item": "Pot roast"
        },
    "Clock Tower - Before Karasuman Breakable Wall Item 1":
        {
            "ap_id": 181,
            "zones": [ZONE["NZ1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2d4a, 0x3760],
            "addresses": [0x055737a0],
            "bin_addresses": [0xf4ede, 0x438d676],
            "rom_address": 0xdfce6,
            "break_flag": 0x03be8f,
            "break_mask": 0x2,
            "vanilla_item": "Shuriken"
        },
    "Clock Tower - Before Karasuman Breakable Wall Item 3":
        {
            "ap_id": 182,
            "zones": [ZONE["NZ1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2d86, 0x376a],
            "addresses": [0x055737a8],
            "bin_addresses": [0xf4ee0, 0x438d678],
            "rom_address": 0xdfce8,
            "break_flag": 0x03be8f,
            "break_mask": 0x8,
            "vanilla_item": "TNT"
        },
    "Clock Tower - Top Right Room in Open Area":
        {
            "ap_id": 183,
            "zones": [ZONE["NZ1"]],
            "index": 2,
            "entities": [0x28ae, 0x32ba],
            "as_item": {"y": 0x00c9},
            "vanilla_item": "Fire of bat"
        },
    # Castle Keep items
    "Castle Keep - Open Area Bottom Left on Ledge":
        {
            "ap_id": 184,
            "zones": [ZONE["TOP"]],
            "index": 0,
            "entities": [0x212e, 0x2842],
            "as_relic": {"y": 0x06c0},
            "vanilla_item": "Turquoise"
        },
    "Castle Keep - Open Area Bottom Left on Ledge Breakable Wall":
        {
            "ap_id": 185,
            "zones": [ZONE["TOP"]],
            "index": 1,
            "despawn": True,
            "entities": [0x2124, 0x282e],
            "as_relic": {"x": 0x0190},
            "vanilla_item": "Turkey"
        },
    "Castle Keep - Open Area Top Left Alcove Breakable Wall":
        {
            "ap_id": 186,
            "zones": [ZONE["TOP"]],
            "index": 2,
            "entities": [0x211a, 0x27a2],
            "as_relic": {"x": 0x0190, "y": 0x04b5},
            "vanilla_item": "Fire mail"
        },
    "Castle Keep - Top Right Room by Dual Moving Platforms":
        {
            "ap_id": 187,
            "zones": [ZONE["TOP"]],
            "index": 3,
            "entities": [0x23b8, 0x2964],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Tyrfing"
        },
    "Castle Keep - Hidden Stair Room Left Statue 1":
        {
            "ap_id": 188,
            "zones": [ZONE["TOP"]],
            "index": 4,
            "entities": [0x23fe, 0x29be],
            "as_relic": {"y": 0x00cf},
            "vanilla_item": "Sirloin"
        },
    "Castle Keep - Hidden Stair Room Left Statue 2":
        {
            "ap_id": 189,
            "zones": [ZONE["TOP"]],
            "index": 5,
            "entities": [0x2408, 0x29c8],
            "as_relic": {"y": 0x00cf},
            "vanilla_item": "Turkey"
        },
    "Castle Keep - Hidden Stair Room Left Yellow Vase 1":
        {
            "ap_id": 190,
            "zones": [ZONE["TOP"]],
            "index": 6,
            "despawn": True,
            "entities": [0x2412, 0x29d2],
            "as_relic": {"y": 0x00cf},
            "vanilla_item": "Pot roast"
        },
    "Castle Keep - Hidden Stair Room Left Yellow Vase 2":
        {
            "ap_id": 191,
            "zones": [ZONE["TOP"]],
            "index": 7,
            "entities": [0x241c, 0x29dc],
            "as_relic": {"y": 0x00cf},
            "vanilla_item": "Frankfurter"
        },
    "Castle Keep - Hidden Stair Room Right Yellow Vase 1":
        {
            "ap_id": 192,
            "zones": [ZONE["TOP"]],
            "index": 8,
            "entities": [0x2430, 0x29e6],
            "as_relic": {"y": 0x00cf},
            "vanilla_item": "Resist stone"
        },
    "Castle Keep - Hidden Stair Room Right Yellow Vase 2":
        {
            "ap_id": 193,
            "zones": [ZONE["TOP"]],
            "index": 9,
            "entities": [0x243a, 0x29f0],
            "as_relic": {"y": 0x00cf},
            "vanilla_item": "Resist dark"
        },
    "Castle Keep - Hidden Stair Room Right Statue 1":
        {
            "ap_id": 194,
            "zones": [ZONE["TOP"]],
            "index": 10,
            "entities": [0x2444, 0x29fa],
            "as_relic": {"y": 0x00cf},
            "vanilla_item": "Resist holy"
        },
    "Castle Keep - Hidden Stair Room Right Statue 2":
        {
            "ap_id": 195,
            "zones": [ZONE["TOP"]],
            "index": 11,
            "entities": [0x244e, 0x29b4],
            "as_relic": {"y": 0x00be},
            "vanilla_item": "Platinum mail"
        },
    "Castle Keep - Attic by Elevator Surround by Torches":
        {
            "ap_id": 196,
            "zones": [ZONE["TOP"]],
            "index": 12,
            "entities": [0x2476, 0x2a22],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Falchion"
        },
    "Castle Keep - Open Area Top Right Room Item 1":
        {
            "ap_id": 197,
            "zones": [ZONE["TOP"]],
            "index": 13,
            "entities": [0x25d4, 0x2b80],
            "as_relic": {"y": 0x0190},
            "vanilla_item": "Life Vessel"
        },
    "Castle Keep - Open Area Top Right Room Item 3":
        {
            "ap_id": 198,
            "zones": [ZONE["TOP"]],
            "index": 14,
            "entities": [0x25e8, 0x2b94],
            "as_relic": {"y": 0x0210},
            "vanilla_item": "Life Vessel"
        },
    "Castle Keep - Open Area Top Right Room Item 2":
        {
            "ap_id": 199,
            "zones": [ZONE["TOP"]],
            "index": 15,
            "entities": [0x25f2, 0x2b8a],
            "as_relic": {"y": 0x01b0},
            "vanilla_item": "Heart Vessel"
        },
    "Castle Keep - Open Area Top Right Room Item 4":
        {
            "ap_id": 200,
            "zones": [ZONE["TOP"]],
            "index": 16,
            "entities": [0x25de, 0x2b9e],
            "as_relic": {"y": 0x0250},
            "vanilla_item": "Heart Vessel"
        },
    "Castle Keep - Red Vase Before Richter":
        {
            "ap_id": 201,
            "zones": [ZONE["TOP"]],
            "index": 18,
            "entities": [0x2250, 0x2748],
            "as_relic": {},
            "vanilla_item": "Heart Vessel"
        },
    "Castle Keep - Open Area Bottom Left Floor Item":
        {
            "ap_id": 202,
            "zones": [ZONE["TOP"]],
            "index": 17,  # Test if index 17 works
            "entities": [0x2142, 0x286a],
            "as_item": {"y": 0x0729},
            "vanilla_item": "Leap stone"
        },
    "Castle Keep - Open Area Top Left Alcove":
        {
            "ap_id": 203,
            "zones": [ZONE["TOP"]],
            "index": 19,
            "entities": [0x2138, 0x27ac],
            "as_item": {"y": 0x04c8},
            "vanilla_item": "Power of mist"
        },
    "Castle Keep - Open Area Top Right Room Item 5":
        {
            "ap_id": 204,
            "zones": [ZONE["TOP"]],
            "index": 20,
            "entities": [0x25fc, 0x2ba8],
            "as_item": {"y": 0x02a8},
            "vanilla_item": "Ghost card"
        },
    # Reverse Colosseum items
    "Reverse Colosseum Junction Tunnel - Breakable Floor Room":
        {
            "ap_id": 205,
            "zones": [ZONE["RARE"]],
            "index": 0,
            "entities": [0x2446, 0x29e6],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Fury plate"
        },
    "Reverse Colosseum Right Part - Top Right Room":
        {
            "ap_id": 206,
            "zones": [ZONE["RARE"]],
            "index": 1,
            "entities": [0x213a, 0x26e4],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Zircon"
        },
    "Reverse Colosseum Right Part - Top Left Room":
        {
            "ap_id": 207,
            "zones": [ZONE["RARE"]],
            "index": 2,
            "entities": [0x2400, 0x29aa],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Buffalo star"
        },
    "Reverse Colosseum Left Part - Top Right Room":
        {
            "ap_id": 208,
            "zones": [ZONE["RARE"]],
            "index": 3,
            "entities": [0x2428, 0x29c8],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Gram"
        },
    "Reverse Colosseum Left Part - Top Left Room":
        {
            "ap_id": 209,
            "zones": [ZONE["RARE"]],
            "index": 4,
            "entities": [0x2036, 0x2612],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Aquamarine"
        },
    "Reverse Colosseum Left Part - Left Item on Floor":
        {
            "ap_id": 210,
            "zones": [ZONE["RARE"]],
            "index": 5,
            "entities": [0x219e, 0x27ac],
            "as_relic": {},
            "vanilla_item": "Heart Vessel"
        },
    "Reverse Colosseum Left Part - Middle Item on Floor":
        {
            "ap_id": 211,
            "zones": [ZONE["RARE"]],
            "index": 6,
            "entities": [0x21a8, 0x27b6],
            "as_relic": {},
            "vanilla_item": "Life Vessel"
        },
    "Reverse Colosseum Left Part - Right Item on Floor":
        {
            "ap_id": 212,
            "zones": [ZONE["RARE"]],
            "index": 7,
            "entities": [0x21b2, 0x27c0],
            "as_relic": {},
            "vanilla_item": "Heart Vessel"
        },
    # Floating Catacombs items
    "Floating Catacombs Bottom - After Save Point Item":
        {
            "ap_id": 213,
            "zones": [ZONE["RCAT"]],
            "index": 0,
            "entities": [0x285c, 0x338a],
            "as_relic": {"x": 0x00c0},
            "vanilla_item": "Magic missile"
        },
    "Floating Catacombs Bottom - After Save Point Breakable Wall":
        {
            "ap_id": 214,
            "zones": [ZONE["RCAT"]],
            "index": 1,
            "entities": [0x2866, 0x3380],
            "as_relic": {"x": 0x00d0, "y": 0x0080},
            "vanilla_item": "Buffalo star"
        },
    "Floating Catacombs After Spike Tunnel - Top Left Vase":
        {
            "ap_id": 215,
            "zones": [ZONE["RCAT"]],
            "index": 2,
            "entities": [0x2d34, 0x384e],
            "as_relic": {},
            "vanilla_item": "Resist thunder"
        },
    "Floating Catacombs After Spike Tunnel - Top Right Vase":
        {
            "ap_id": 216,
            "zones": [ZONE["RCAT"]],
            "index": 3,
            "entities": [0x2d48, 0x3858],
            "as_relic": {},
            "vanilla_item": "Resist fire"
        },
    "Floating Catacombs After Spike Tunnel - Bottom Left Vase":
        {
            "ap_id": 217,
            "zones": [ZONE["RCAT"]],
            "index": 4,
            "entities": [0x2d2a, 0x389e],
            "as_relic": {},
            "vanilla_item": "Karma coin"
        },
    "Floating Catacombs After Spike Tunnel - Bottom Right Vase":
        {
            "ap_id": 218,
            "zones": [ZONE["RCAT"]],
            "index": 5,
            "entities": [0x2d3e, 0x38a8],
            "as_relic": {},
            "vanilla_item": "Karma coin"
        },
    "Floating Catacombs After Spike Tunnel - Deep Left Item":
        {
            "ap_id": 219,
            "zones": [ZONE["RCAT"]],
            "index": 6,
            "entities": [0x2dde, 0x3902],
            "as_relic": {"x": 0x0030, "y": 0x0085},
            "vanilla_item": "Red bean bun"
        },
    "Floating Catacombs After Spike Tunnel - Deep Right Item":
        {
            "ap_id": 220,
            "zones": [ZONE["RCAT"]],
            "index": 7,
            "entities": [0x3036, 0x3b64],
            "as_relic": {"x": 0x02c0},
            "vanilla_item": "Elixir"
        },
    "Floating Catacombs After Spike Tunnel - Deep Right Breakable Wall Item":
        {
            "ap_id": 221,
            "zones": [ZONE["RCAT"]],
            "index": 8,
            "entities": [0x3040, 0x3b5a],
            "as_relic": {"x": 0x02d0, "y": 0x0080},
            "vanilla_item": "Library card"
        },
    "Floating Catacombs Upper - Start of Crypt Left Item":
        {
            "ap_id": 222,
            "zones": [ZONE["RCAT"]],
            "index": 9,
            "entities": [0x296a, 0x3498],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Life Vessel"
        },
    "Floating Catacombs Upper - Start of Crypt Right Item":
        {
            "ap_id": 223,
            "zones": [ZONE["RCAT"]],
            "index": 10,
            "entities": [0x2974, 0x348e],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Heart Vessel"
        },
    "Floating Catacombs Upper - After Crypt Cave Upper Red Vase":
        {
            "ap_id": 224,
            "zones": [ZONE["RCAT"]],
            "index": 11,
            "entities": [0x2b36, 0x366e],
            "as_relic": {},
            "vanilla_item": "Shield potion"
        },
    "Floating Catacombs Upper - After Crypt Cave Bottom Red Vase":
        {
            "ap_id": 225,
            "zones": [ZONE["RCAT"]],
            "index": 12,
            "entities": [0x2b2c, 0x36b4],
            "as_relic": {},
            "vanilla_item": "Attack potion"
        },
    "Floating Catacombs Upper - After Crypt Breakable Wall Room":
        {
            "ap_id": 226,
            "zones": [ZONE["RCAT"]],
            "index": 13,
            "entities": [0x25dc, 0x3100],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Necklace of j"
        },
    "Floating Catacombs Upper - Before Galamoth Save Point":
        {
            "ap_id": 227,
            "zones": [ZONE["RCAT"]],
            "index": 14,
            "entities": [0x25be, 0x30e2],
            "as_relic": {"y": 0x00c8},
            "vanilla_item": "Diamond"
        },
    "Floating Catacombs Upper - After Galamoth Left Item":
        {
            "ap_id": 228,
            "zones": [ZONE["RCAT"]],
            "index": 15,
            "entities": [0x2816, 0x333a],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Heart Vessel"
        },
    "Floating Catacombs Upper - After Galamoth Right Item":
        {
            "ap_id": 229,
            "zones": [ZONE["RCAT"]],
            "index": 16,
            "entities": [0x2820, 0x3344],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Life Vessel"
        },
    "Floating Catacombs Upper - After Galamoth Deeper Room Right Item":
        {
            "ap_id": 230,
            "zones": [ZONE["RCAT"]],
            "index": 17,
            "entities": [0x25a0, 0x30c4],
            "as_relic": {"y": 0x00c8},
            "vanilla_item": "Ruby circlet"
        },
    "Floating Catacombs Upper - After Galamoth Deeper Room Left Item":
        {
            "ap_id": 231,
            "zones": [ZONE["RCAT"]],
            "index": 18,
            "entities": [0x2596, 0x30ba],
            "as_item": {"x": 0x0016, "y": 0x00b1},
            "vanilla_item": "Gas cloud"
        },
    # Cave items
    "Cave Demon Side - Breakable Wall Room Left Item":
        {
            "ap_id": 232,
            "zones": [ZONE["RCHI"]],
            "index": 0,
            "entities": [0x1910, 0x1d7a],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Power of sire"
        },
    "Cave Demon Side - Breakable Wall Room Right Item":
        {
            "ap_id": 233,
            "zones": [ZONE["RCHI"]],
            "index": 1,
            "entities": [0x191a, 0x1d70],
            "as_relic": {"y": 0x00a0},
            "vanilla_item": "Life apple"
        },
    "Cave - Middle Ascend Right Item":
        {
            "ap_id": 234,
            "zones": [ZONE["RCHI"]],
            "index": 2,
            "entities": [0x1cda, 0x213a],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Alucard sword"
        },
    "Cave - Upper Right Room Left Item(Shared with Demon Side)":
        {
            # TODO This green tea is shared in Cave - Upper Right Room
            "ap_id": 235,
            "zones": [ZONE["RCHI"], ZONE["RCHI"]],
            "index": 3,
            # TODO First entity is the item(Changing does not matter), second the wall, flag wall destroyed 0x03be45
            "entities": [0x1938, 0x1d98, 0x1a8c, 0x1ece],
            "as_relic": {"y": 0x00a0},  # TODO Better the wall start broke and only use upper room
            "vanilla_item": "Green tea"
        },
    "Cave - Upper Right Room Right Item":
        {
            "ap_id": 236,
            "zones": [ZONE["RCHI"]],
            "index": 4,
            "entities": [0x1942, 0x1da2],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Power of sire"
        },
    "Cave - Upper Ascend Item 2":
        {
            "ap_id": 237,
            "zones": [ZONE["RCHI"]],
            "index": 6,
            "entities": [0x1bd6, 0x204a],
            "as_relic": {"y": 0x0127},
            "vanilla_item": "Shiitake"
        },
    "Cave - Upper Ascend Item 1":
        {
            "ap_id": 238,
            "zones": [ZONE["RCHI"]],
            "index": 7,
            "entities": [0x1c30, 0x207c],
            "as_relic": {"y": 0x02e8},
            "vanilla_item": "Shiitake"
        },
    "Cave - Death Item":
        {
            "ap_id": 239,
            "zones": [ZONE["RCHI"]],
            "index": 5,
            "entities": [0x18f2, 0x1d52],
            "reward": {"zones": ZONE["RBO2"], "index": 0x15},
            "kill_time": 0x03ca58,
            "erase":
                {
                    "instructions": [{"addresses": [0x06644cf0], "instruction": 0x34020000}]
                },
            "as_item": {"y": 0x0079},
            "vanilla_item": "Eye of vlad"
        },
    # Anti-Chapel items
    "Anti-Chapel Stairs - Bottom Yellow Vase":
        {
            "ap_id": 240,
            "zones": [ZONE["RDAI"]],
            "index": 2,
            "entities": [0x1e78, 0x2924],
            "as_relic": {},
            "vanilla_item": "Fire boomerang"
        },
    "Anti-Chapel Stairs - Red Vase Alcove 3":
        {
            "ap_id": 241,
            "zones": [ZONE["RDAI"]],
            "index": 3,
            "entities": [0x1f36, 0x2852],
            "as_relic": {},
            "vanilla_item": "Diamond"
        },
    "Anti-Chapel Stairs - Red Vase at Top":
        {
            "ap_id": 242,
            "zones": [ZONE["RDAI"]],
            "index": 4,
            "entities": [0x1fd6, 0x27b2],
            "as_relic": {},
            "vanilla_item": "Zircon"
        },
    "Anti-Chapel Stairs - Red Vase Alcove 6":
        {
            "ap_id": 243,
            "zones": [ZONE["RDAI"]],
            "index": 5,
            "entities": [0x1fae, 0x27e4],
            "as_relic": {},
            "vanilla_item": "Heart Vessel"
        },
    "Anti-Chapel Stairs - Red Vase Alcove 5":
        {
            "ap_id": 244,
            "zones": [ZONE["RDAI"]],
            "index": 6,
            "entities": [0x1f9a, 0x27f8],
            "as_relic": {},
            "vanilla_item": "Shuriken"
        },
    "Anti-Chapel Stairs - Red Vase Alcove 4":
        {
            "ap_id": 245,
            "zones": [ZONE["RDAI"]],
            "index": 7,
            "entities": [0x1f4a, 0x283e],
            "as_relic": {},
            "vanilla_item": "TNT"
        },
    "Anti-Chapel Stairs - Red Vase Alcove 2":
        {
            "ap_id": 246,
            "zones": [ZONE["RDAI"]],
            "index": 8,
            "entities": [0x1efa, 0x288e],
            "as_relic": {},
            "vanilla_item": "Boomerang"
        },
    "Anti-Chapel Stairs - Red Vase Alcove 1":
        {
            "ap_id": 247,
            "zones": [ZONE["RDAI"]],
            "index": 9,
            "entities": [0x1ed2, 0x28c0],
            "as_relic": {},
            "vanilla_item": "Javelin"
        },
    "Anti-Chapel Tower 3  - Bottom Item":
        {
            "ap_id": 248,
            "zones": [ZONE["RDAI"]],
            "index": 10,
            "entities": [0x2364, 0x2d66],
            "as_relic": {},
            "vanilla_item": "Manna prism"
        },
    "Anti-Chapel Tower 3 - Yellow Vase":
        {
            "ap_id": 249,
            "zones": [ZONE["RDAI"]],
            "index": 11,
            "entities": [0x2288, 0x2d5c],
            "as_relic": {},
            "vanilla_item": "Smart potion"
        },
    "Anti-Chapel Tower 3 - Red Vase":
        {
            "ap_id": 250,
            "zones": [ZONE["RDAI"]],
            "index": 12,
            "entities": [0x23be, 0x2d52],
            "as_relic": {},
            "vanilla_item": "Life Vessel"
        },
    "Anti-Chapel Tower 2 - Bottom Item":
        {
            "ap_id": 251,
            "zones": [ZONE["RDAI"]],
            "index": 13,
            "entities": [0x2472, 0x2e06],
            "as_relic": {"y": 0x030f},
            "vanilla_item": "Talwar"
        },
    "Anti-Chapel Tower 1 - Bottom Item":
        {
            "ap_id": 252,
            "zones": [ZONE["RDAI"]],
            "index": 14,
            "entities": [0x254e, 0x2ed8],
            "as_relic": {"y": 0x0320},
            "vanilla_item": "Bwaka knife"
        },
    "Anti-Chapel Tower 1 - Red Vase":
        {
            "ap_id": 253,
            "zones": [ZONE["RDAI"]],
            "index": 15,
            "entities": [0x2562, 0x2ece],
            "as_relic": {},
            "vanilla_item": "Magic missile"
        },
    "Anti-Chapel - After Spiked Tunnel":
        {
            "ap_id": 254,
            "zones": [ZONE["RDAI"]],
            "index": 16,
            "entities": [0x1d7e, 0x26d6],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Twilight cloak"
        },
    "Anti-Chapel - Next to Upper Save Point":
        {
            "ap_id": 255,
            "zones": [ZONE["RDAI"]],
            "index": 17,
            "entities": [0x25a8, 0x2f00],
            "as_relic": {"y": 0x0070},
            "vanilla_item": "Heart Vessel"
        },
    "Medusa Kill Item":
        {
            "ap_id": 256,
            "zones": [ZONE["RDAI"]],
            "index": 0,  # Test if index 0 works
            "entities": [0x1dc4, 0x2730],
            "reward": {"zones": ZONE["RBO3"], "index": 0x11},
            "kill_time": 0x03ca64,
            "as_item": {"y": 0x00c9},
            "erase":
                {
                    "instructions": [{"addresses": [0x06757b54], "instruction": 0x34020000}]
                },
            "vanilla_item": "Heart of vlad"
        },
    # Forbidden Library items
    "Forbidden Library - Inner Study Red Vase":
        {
            "ap_id": 257,
            "zones": [ZONE["RLIB"]],
            "index": 0,
            "entities": [0x1a42, 0x1fec],
            "as_relic": {},
            "vanilla_item": "Turquoise"
        },
    "Forbidden Library - Inner Study Left Statue":
        {
            "ap_id": 258,
            "zones": [ZONE["RLIB"]],
            "index": 1,
            "entities": [0x1a4c, 0x1ff6],
            "as_relic": {},
            "vanilla_item": "Opal"
        },
    "Forbidden Library - Inner Study Right Statue":
        {
            "ap_id": 259,
            "zones": [ZONE["RLIB"]],
            "index": 2,
            "entities": [0x1a56, 0x2000],
            "as_relic": {},
            "vanilla_item": "Library card"
        },
    "Forbidden Library Main Area - Bottom Right Room Left Item":
        {
            "ap_id": 260,
            "zones": [ZONE["RLIB"]],
            "index": 3,
            "entities": [0x1ace, 0x206e],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Resist fire"
        },
    "Forbidden Library Main Area - Bottom Right Room Middle Item":
        {
            "ap_id": 261,
            "zones": [ZONE["RLIB"]],
            "index": 4,
            "entities": [0x1ad8, 0x2078],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Resist ice"
        },
    "Forbidden Library Main Area - Bottom Right Room Right Item":
        {
            "ap_id": 262,
            "zones": [ZONE["RLIB"]],
            "index": 5,
            "entities": [0x1ae2, 0x2082],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Resist stone"
        },
    "Forbidden Library Inner Part - Bottom Left Room Green Candle":
        {
            "ap_id": 263,
            "zones": [ZONE["RLIB"]],
            "index": 6,
            "entities": [0x1ccc, 0x226c],
            "as_relic": {},
            "vanilla_item": "Neutron bomb"
        },
    "Forbidden Library Inner Part - Bottom Left Room Behind Bookshelf":
        {
            "ap_id": 264,
            "zones": [ZONE["RLIB"]],
            "index": 7,
            "entities": [0x1b00, 0x20a0],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Badelaire"
        },
    "Forbidden Library Inner Part - Behind Mist Crate":
        {
            "ap_id": 265,
            "zones": [ZONE["RLIB"]],
            "index": 8,
            "entities": [0x1b82, 0x2122],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Staurolite"
        },
    # Black Marble Gallery items
    "Black Marble Gallery - Corridor to Entrance Item on Spike Trap":
        {
            "ap_id": 266,
            "zones": [ZONE["RNO0"]],
            "index": 0,
            "entities": [0x373a, 0x4a10],
            "as_relic": {"y": 0x02c0},
            "vanilla_item": "Library card"
        },
    "Black Marble Gallery - Ascend to Entrance Item on Floor 2":
        {
            "ap_id": 267,
            "zones": [ZONE["RNO0"]],
            "index": 1,
            "entities": [0x3ab4, 0x4a2e],
            "as_relic": {"y": 0x0130},
            "vanilla_item": "Potion"
        },
    "Black Marble Gallery - Ascend to Entrance Item on Floor 1":
        {
            "ap_id": 268,
            "zones": [ZONE["RNO0"]],
            "index": 2,
            "entities": [0x3abe, 0x4a92],
            "as_relic": {"y": 0x0330},
            "vanilla_item": "Antivenom"
        },
    "Black Marble Gallery - Middle Clock Right Item":
        {
            "ap_id": 269,
            "zones": [ZONE["RNO0"]],
            "index": 3,
            "entities": [0x3c1c, 0x4c22],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Life Vessel"
        },
    "Black Marble Gallery - Middle Clock Left Item":
        {
            "ap_id": 270,
            "zones": [ZONE["RNO0"]],
            "index": 4,
            "entities": [0x3bb8, 0x4c18],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Heart Vessel"
        },
    "Black Marble Gallery - Left Clock Second Room Item on Left":
        {
            "ap_id": 271,
            "zones": [ZONE["RNO0"]],
            "index": 5,
            "entities": [0x44d2, 0x5532],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Resist dark"
        },
    "Black Marble Gallery - Left Clock Second Room Item on Right":
        {
            "ap_id": 272,
            "zones": [ZONE["RNO0"]],
            "index": 6,
            "entities": [0x44dc, 0x553c],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Resist holy"
        },
    "Black Marble Gallery - Left Clock First Room Item on Left":
        {
            "ap_id": 273,
            "zones": [ZONE["RNO0"]],
            "index": 7,
            "entities": [0x44aa, 0x550a],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Resist thunder"
        },
    "Black Marble Gallery - Left Clock First Room Item on Right":
        {
            "ap_id": 274,
            "zones": [ZONE["RNO0"]],
            "index": 8,
            "entities": [0x44b4, 0x5514],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Resist fire"
        },
    "Black Marble Gallery - Behind Magic Blue Door":
        {
            "ap_id": 275,
            "zones": [ZONE["RNO0"]],
            "index": 9,
            "entities": [0x407c, 0x510e],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Meal ticket"
        },
    "Black Marble Gallery - Hole on the Ceiling":
        {
            "ap_id": 276,
            "zones": [ZONE["RNO0"]],
            "index": 10,
            "entities": [0x4568, 0x55b],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Iron ball"
        },
    "Black Marble Gallery - Item Inside the Clock":
        {
            "ap_id": 277,
            "zones": [ZONE["RNO0"]],
            "index": 11,
            "entities": [0x44fa, 0x555a],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Heart refresh"
        },
    # Reverse Outer Wall items
    "Reverse Outer Wall - Item at the Top":
        {
            "ap_id": 278,
            "zones": [ZONE["RNO1"]],
            "index": 0,
            "entities": [0x2058, 0x26fe],
            "as_relic": {"y": 0x00d0},
            "vanilla_item": "Heart Vessel"
        },
    "Reverse Outer Wall - Mist Crate Room Left Item":
        {
            "ap_id": 279,
            "zones": [ZONE["RNO1"]],
            "index": 1,
            "entities": [0x215c, 0x2852],
            "tile_index": 2,
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Shotel"
        },
    "Reverse Outer Wall - Mist Crate Room Right Item":
        {
            "ap_id": 280,
            "zones": [ZONE["RNO1"]],
            "index": 2,
            "entities": [0x2170, 0x285c],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Hammer"
        },
    "Reverse Outer Wall - Red Vase Near Door to BMG":
        {
            "ap_id": 281,
            "zones": [ZONE["RNO1"]],
            "index": 3,
            "entities": [0x21de, 0x28d4],
            "as_relic": {},
            "vanilla_item": "Life Vessel"
        },
    "Reverse Outer Wall - Yellow Vase on Alcove Near Creature":
        {
            "ap_id": 282,
            "zones": [ZONE["RNO1"]],
            "index": 4,
            "entities": [0x221a, 0x291a],
            "as_relic": {},
            "vanilla_item": "Luck potion"
        },
    "Reverse Outer Wall - Item on the Floor Near Creature":
        {
            "ap_id": 283,
            "zones": [ZONE["RNO1"]],
            "index": 5,
            "entities": [0x2350, 0x2a46],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Shield potion"
        },
    "Reverse Outer Wall - Red Vase Near Creature":
        {
            "ap_id": 284,
            "zones": [ZONE["RNO1"]],
            "index": 6,
            "entities": [0x242c, 0x2a8c],
            "as_relic": {},
            "vanilla_item": "High potion"
        },
    "Reverse Outer Wall - Bottom Red Vase Near Elevator Machinery":
        {
            "ap_id": 285,
            "zones": [ZONE["RNO1"]],
            "index": 7,
            "entities": [0x2544, 0x2c8a],
            "as_relic": {},
            "vanilla_item": "Garnet"
        },
    "Reverse Outer Wall - Breakable Wall on Room Below Mist Crate":
        {
            "ap_id": 286,
            "zones": [ZONE["RNO1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x21ac, 0x288e],
            "as_relic": {"y": 0x0058},
            "addresses": [0x0507d08c],
            "bin_addresses": [0xf4ee2, 0x438d67a],
            "rom_address": 0xdfcea,
            "break_flag": 0x03be04,
            "break_mask": 0x1,
            "vanilla_item": "Dim sum set"
        },
    "Creature Kill Item":
        {
            "ap_id": 287,
            "zones": [ZONE["RNO1"]],
            "index": 8,
            "entities": [0x2332, 0x2a1e],
            "reward": {"zones": ZONE["RBO4"], "index": 0x12},
            "as_item": {"y": 0x00b9},
            "kill_time": 0x03ca68,
            "erase":
                {
                    "instructions": [{"addresses": [0x067ec398], "instruction": 0x34020000}]
                },
            "vanilla_item": "Tooth of vlad"
        },
    # Death Wing's Lair items
    "Death Wing\'s Lair Main Area - Room Behind Breakable Wall Left Red Vase":
        {
            "ap_id": 288,
            "zones": [ZONE["RNO2"]],
            "index": 0,
            "entities": [0x29f2, 0x31d6],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Opal"
        },
    "Death Wing\'s Lair Main Area - Room Behind Breakable Wall Middle Red Vase":
        {
            "ap_id": 289,
            "zones": [ZONE["RNO2"]],
            "index": 1,
            "entities": [0x29fc, 0x31e0],
            "tile_index": 3,
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Sword of hador"
        },
    "Death Wing\'s Lair Main Area - Room Behind Breakable Wall Right Red Vase":
        {
            "ap_id": 290,
            "zones": [ZONE["RNO2"]],
            "index": 2,
            "as_relic": {"y": 0x0080},
            "entities": [0x2a06, 0x31ea],
            "vanilla_item": "High potion"
        },
    "Death Wing\'s Lair Upper Part - Top Red Vase on Shaft":
        {
            "ap_id": 291,
            "zones": [ZONE["RNO2"]],
            "index": 3,
            "entities": [0x293e, 0x3122],
            "as_relic": {},
            "vanilla_item": "Shield potion"
        },
    "Death Wing\'s Lair Upper Part - Middle Red Vase on Shaft":
        {
            "ap_id": 292,
            "zones": [ZONE["RNO2"]],
            "index": 4,
            "entities": [0x2948, 0x312c],
            "as_relic": {},
            "vanilla_item": "Luck potion"
        },
    "Death Wing\'s Lair Upper Part - Bottom Red Vase on Shaft":
        {
            "ap_id": 293,
            "zones": [ZONE["RNO2"]],
            "index": 5,
            "entities": [0x2952, 0x3136],
            "as_relic": {},
            "vanilla_item": "Manna prism"
        },
    "Death Wing\'s Lair - Red Vase Next to Path to Courtyard":
        {
            "ap_id": 294,
            "zones": [ZONE["RNO2"]],
            "index": 6,
            "entities": [0x2664, 0x2e34],
            "as_relic": {},
            "vanilla_item": "Aquamarine"
        },
    "Death Wing\'s Lair Courtyard - Top Left Room":
        {
            "ap_id": 295,
            "zones": [ZONE["RNO2"]],
            "index": 7,
            "entities": [0x298e, 0x3172],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Alucard mail"
        },
    "Death Wing\'s Lair Path to Anti-Chapel - Bellow Wooden Pedestal":
        {
            "ap_id": 296,
            "zones": [ZONE["RNO2"]],
            "index": 8,
            "entities": [0x2b78, 0x33c0],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Life Vessel"
        },
    "Death Wing\'s Lair Path to Anti-Chapel - Breakable Floor Room":
        {
            "ap_id": 297,
            "zones": [ZONE["RNO2"]],
            "index": 9,
            "entities": [0x2970, 0x3154],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Heart refresh"
        },
    "Death Wing\'s Lair - Attic Before Akmodan II":
        {
            "ap_id": 298,
            "zones": [ZONE["RNO2"]],
            "index": 10,
            "entities": [0x29ac, 0x3190],
            "as_relic": {"y": 0x0040},
            "vanilla_item": "Shuriken"
        },
    "Death Wing\'s Lair - After Akmodan II":
        {
            "ap_id": 299,
            "zones": [ZONE["RNO2"]],
            "index": 11,
            "entities": [0x2aa6, 0x329e],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Heart Vessel"
        },
    "Death Wing\'s Lair - Akmodan II Item":
        {
            "ap_id": 300,
            "zones": [ZONE["RNO2"]],
            "index": 12,
            "entities": [0x29d4, 0x31b8],
            "reward": {"zones": ZONE["RBO7"], "index": 0x13},
            "kill_time": 0x03ca74,
            "as_item": {"y": 0x01b9},
            "erase":
                {
                    "instructions": [{"addresses": [0x069e8524], "instruction": 0x34020000}]
                },
            "vanilla_item": "Rib of vlad"
        },
    # Reverse Entrance items
    "Reverse Entrance - Main Gate Bottom Left Item":
        {
            "ap_id": 301,
            "zones": [ZONE["RNO3"]],
            "index": 0,
            "entities": [0x2f94, 0x36c4],
            "as_relic": {"y": 0x0280},
            "vanilla_item": "Hammer"
        },
    "Reverse Entrance - Main Gate Bottom Right Item":
        {
            "ap_id": 302,
            "zones": [ZONE["RNO3"]],
            "index": 1,
            "entities": [0x2fda, 0x36ce],
            "as_relic": {"y": 0x0280},
            "vanilla_item": "Antivenom"
        },
    "Reverse Entrance - Breakable Ledge on Main Corridor":
        {
            "ap_id": 303,
            "zones": [ZONE["RNO3"]],
            "index": 2,
            "entities": [0x302a, 0x3700],
            "as_relic": {"y": 0x0050},
            "vanilla_item": "High potion"
        },
    "Reverse Entrance - Bellow Stone Pedestal":
        {
            "ap_id": 304,
            "zones": [ZONE["RNO3"]],
            "index": 3,
            "entities": [0x2e5e, 0x3566],
            "as_relic": {"y": 0x02c0},
            "vanilla_item": "Heart Vessel"
        },
    "Reverse Entrance - Wolf/Bat Secret Room Left Item":
        {
            "ap_id": 305,
            "zones": [ZONE["RNO3"]],
            "index": 4,
            "entities": [0x2d96, 0x3476],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Zircon"
        },
    "Reverse Entrance - Wolf/Bat Secret Room Middle Item":
        {
            "ap_id": 306,
            "zones": [ZONE["RNO3"]],
            "index": 5,
            "entities": [0x2da0, 0x346c],
            "as_relic": {"y": 0x00a5},
            "vanilla_item": "Opal"
        },
    "Reverse Entrance - Wolf/Bat Secret Room Right Item":
        {
            "ap_id": 307,
            "zones": [ZONE["RNO3"]],
            "index": 6,
            "entities": [0x2daa, 0x3462],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Beryl circlet"
        },
    "Reverse Entrance - Hole in Main Corridor Back Item":
        {
            "ap_id": 308,
            "zones": [ZONE["RNO3"]],
            "index": 7,
            "entities": [0x2d28, 0x33fe],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Fire boomerang"
        },
    "Reverse Entrance - Middle Room in Open Area Before Main Corridor":
        {
            "ap_id": 309,
            "zones": [ZONE["RNO3"]],
            "index": 8,
            "entities": [0x2ce2, 0x33ae],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Life Vessel"
        },
    "Reverse Entrance - Room by Nova Skeleton on the Ledge":
        {
            "ap_id": 310,
            "zones": [ZONE["RNO3"]],
            "index": 9,
            "entities": [0x2d00, 0x33cc],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Talisman"
        },
    "Reverse Entrance - Breakable Big Rock in Main Corridor":
        {
            "ap_id": 311,
            "zones": [ZONE["RNO3"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2f26, 0x3610],
            "addresses": [0x051e6e4c],
            "bin_addresses": [0xf4ee4, 0x438d67c],
            "rom_address": 0xdfcec,
            "break_flag": 0x03be27,
            "break_mask": 0x1,
            "vanilla_item": "Pot roast"
        },
    # Reverse Caverns items
    "Reverse Caverns Upper - End of Cavern":
        {
            "ap_id": 312,
            "zones": [ZONE["RNO4"]],
            "index": 0,
            "entities": [0x3880, 0x47da],
            "as_relic": {"x": 0x0080, "y": 0x0080},
            "vanilla_item": "Alucard shield"
        },
    "Reverse Caverns Upper - Near Exit":
        {
            "ap_id": 313,
            "zones": [ZONE["RNO4"]],
            "index": 1,
            "entities": [0x3bfa, 0x4b68],
            "as_relic": {"x": 0x004a, "y": 0x0080},
            "vanilla_item": "Shiitake"
        },
    "Reverse Caverns Waterfall - Alcove 1":
        {
            "ap_id": 314,
            "zones": [ZONE["RNO4"]],
            "index": 2,
            "entities": [0x31aa, 0x4078],
            "as_relic": {"x": 0x01c5, "y": 0x0110},
            "vanilla_item": "Toadstool"
        },
    "Reverse Caverns Waterfall - Alcove 2":
        {
            "ap_id": 315,
            "zones": [ZONE["RNO4"]],
            "index": 3,
            "entities": [0x31b4, 0x4082],
            "as_relic": {"x": 0x01d0, "y": 0x02d0},
            "vanilla_item": "Shiitake"
        },
    "Reverse Caverns Waterfall - Bottom Right Room":
        {
            "ap_id": 316,
            "zones": [ZONE["RNO4"]],
            "index": 4,
            "entities": [0x381c, 0x476c],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Garnet"
        },
    "Reverse Caverns Bottom - Underwater Stream":
        {
            "ap_id": 317,
            "zones": [ZONE["RNO4"]],
            "index": 5,
            "entities": [0x3754, 0x46a4],
            "as_relic": {"y": 0x0040},
            "vanilla_item": "Bat pentagram"
        },
    "Reverse Caverns Bottom - Underwater Top Item":
        {
            "ap_id": 318,
            "zones": [ZONE["RNO4"]],
            "index": 6,
            "entities": [0x336c, 0x4122],
            "as_relic": {"y": 0x0040},
            "vanilla_item": "Life Vessel"
        },
    "Reverse Caverns Bottom - Item on Air Pocket":
        {
            "ap_id": 319,
            "zones": [ZONE["RNO4"]],
            "index": 7,
            "entities": [0x31dc, 0x4154],
            "as_relic": {"y": 0x00d8},
            "vanilla_item": "Heart Vessel"
        },
    "Reverse Caverns Bottom - Underwater Bottom Item":
        {
            "ap_id": 320,
            "zones": [ZONE["RNO4"]],
            "index": 8,
            "entities": [0x3362, 0x414a],
            "as_relic": {},
            "vanilla_item": "Potion"
        },
    "Reverse Caverns Bottom - Alcove Near Water Leak":
        {
            "ap_id": 321,
            "zones": [ZONE["RNO4"]],
            "index": 9,
            "entities": [0x3236, 0x42b2],
            "as_relic": {"y": 0x01c5},
            "vanilla_item": "Shiitake"
        },
    "Reverse Caverns Bottom - Near Stairs Hole":
        {
            "ap_id": 322,
            "zones": [ZONE["RNO4"]],
            "index": 10,
            "entities": [0x31d2, 0x42a8],
            "as_relic": {"y": 0x01d0},
            "vanilla_item": "Shiitake"
        },
    "Reverse Caverns Stairs - Middle Room":
        {
            "ap_id": 323,
            "zones": [ZONE["RNO4"]],
            "index": 11,
            "entities": [0x3bbe, 0x4b0e],
            "as_relic": {"y": 0x0090},
            "vanilla_item": "Opal"
        },
    "Reverse Caverns Stairs - Bottom Item":
        {
            "ap_id": 324,
            "zones": [ZONE["RNO4"]],
            "index": 12,
            "entities": [0x3b96, 0x4af0],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Life Vessel"
        },
    "Reverse Caverns Stairs - Bottom Item Behind Breakable Wall":
        {
            "ap_id": 325,
            "zones": [ZONE["RNO4"]],
            "index": 13,
            "entities": [0x2d72, 0x3cc2],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Diamond"
        },
    "Reverse Caverns Bottom - Red Vase Near Exit":
        {
            "ap_id": 326,
            "zones": [ZONE["RNO4"]],
            "index": 14,
            "entities": [0x3b5a, 0x4ac8],
            "as_relic": {},
            "vanilla_item": "Zircon"
        },
    "Reverse Caverns Succubus Side - First Red Vase":
        {
            "ap_id": 327,
            "zones": [ZONE["RNO4"]],
            "index": 15,
            "entities": [0x2e12, 0x3dc6],
            "as_relic": {},
            "vanilla_item": "Heart Vessel"
        },
    "Reverse Caverns Succubus Side - Bottom Left Red Vase":
        {
            "ap_id": 328,
            "zones": [ZONE["RNO4"]],
            "index": 16,
            "entities": [0x3056, 0x3fce],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Reverse Caverns Succubus Side - Middle Left Red Vase":
        {
            "ap_id": 329,
            "zones": [ZONE["RNO4"]],
            "index": 17,
            "entities": [0x3060, 0x3fba],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Reverse Caverns Succubus Side - Middle Right Red Vase":
        {
            "ap_id": 330,
            "zones": [ZONE["RNO4"]],
            "index": 18,
            "entities": [0x3074, 0x3fc4],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Reverse Caverns Succubus Side - Top Right Red Vase":
        {
            "ap_id": 331,
            "zones": [ZONE["RNO4"]],
            "index": 19,
            "entities": [0x307e, 0x3fa6],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Reverse Caverns Succubus Side - Top Left Red Vase":
        {
            "ap_id": 332,
            "zones": [ZONE["RNO4"]],
            "index": 20,
            "entities": [0x306a, 0x3fb0],
            "as_relic": {},
            "vanilla_item": "Meal ticket"
        },
    "Reverse Caverns Doppleganger - Item on Alcove":
        {
            "ap_id": 333,
            "zones": [ZONE["RNO4"]],
            "index": 21,
            "entities": [0x3af6, 0x4a28],
            "as_relic": {"y": 0x0040},
            "vanilla_item": "Zircon"
        },
    "Reverse Caverns Doppleganger - Bottom Area Left Red Vase":
        {
            "ap_id": 334,
            "zones": [ZONE["RNO4"]],
            "index": 22,
            "entities": [0x39c0, 0x4910],
            "as_relic": {},
            "vanilla_item": "Pot roast"
        },
    "Reverse Caverns Doppleganger - Bottom Area Right Room":
        {
            "ap_id": 335,
            "zones": [ZONE["RNO4"]],
            "index": 23,
            "entities": [0x309c, 0x3fec],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Dark blade"
        },
    "Reverse Caverns Ice Area - Underwater Alcove Item":
        {
            "ap_id": 336,
            "zones": [ZONE["RNO4"]],
            "index": 24,
            "entities": [0x342a, 0x42da],
            "as_relic": {"y": 0x0100},
            "vanilla_item": "Manna prism"
        },
    "Reverse Caverns Ice Area - Inside Cave":
        {
            "ap_id": 337,
            "zones": [ZONE["RNO4"]],
            "index": 25,
            "entities": [0x3416, 0x43de],
            "as_relic": {"y": 0x01d0},
            "vanilla_item": "Elixir"
        },
    "Reverse Caverns Waterfall - Behind Waterfall Room":
        {
            "ap_id": 338,
            "zones": [ZONE["RNO4"]],
            "index": 26,
            "entities": [0x37c2, 0x473a],
            "as_relic": {"x": 0x0080, "y": 0x0080},
            "vanilla_item": "Osafune katana"
        },
    "Reverse Caverns Ice Area - At End":
        {
            "ap_id": 339,
            "zones": [ZONE["RNO4"]],
            "index": 27,
            "entities": [0x3718, 0x4686],
            "as_item": {"y": 0x00b9},
            "vanilla_item": "Force of echo"
        },
    # Necromancy Laboratory items
    "Necromancy Lab. - Breakable Wall on Tunnel Right of Elevator Shaft":
        {
            "ap_id": 340,
            "zones": [ZONE["RNZ0"]],
            "index": 1,
            "entities": [0x26b0, 0x2f7c],
            "as_relic": {},
            "vanilla_item": "Heart Vessel"
        },
    "Necromancy Lab. - Bottom Room From Spike Traps":
        {
            "ap_id": 341,
            "zones": [ZONE["RNZ0"]],
            "index": 2,
            "entities": [0x26f6, 0x2fc2],
            "as_relic": {},
            "vanilla_item": "Life Vessel"
        },
    "Necromancy Lab. - Middle Room on Elevator Shaft":
        {
            "ap_id": 342,
            "zones": [ZONE["RNZ0"]],
            "index": 3,
            "entities": [0x289a, 0x3166],
            "as_relic": {"x": 0x0080, "y": 0x0080},
            "vanilla_item": "Goddess shield"
        },
    "Necromancy Lab. - Blue Flame in Room With Lesser and Fire Demons":
        {
            "ap_id": 343,
            "zones": [ZONE["RNZ0"]],
            "index": 4,
            "entities": [0x2598, 0x2dec],
            "as_relic": {},
            "vanilla_item": "Manna prism"
        },
    "Necromancy Lab. - Breakable Ceil on Tunnel Right of Elevator Shaft":
        {
            "ap_id": 344,
            "zones": [ZONE["RNZ0"]],
            "index": 5,
            "entities": [0x2322, 0x2be4],
            "as_relic": {"x": 0x0080, "y": 0x0070},
            "vanilla_item": "Katana"
        },
    "Necromancy Lab. - Hole in Room With Lesser and Fire Demons":
        {
            "ap_id": 345,
            "zones": [ZONE["RNZ0"]],
            "index": 6,
            "entities": [0x2804, 0x30e4],
            "as_relic": {},
            "vanilla_item": "High potion"
        },
    "Necromancy Lab. - Globe in Bitterfly Room":
        {
            "ap_id": 346,
            "zones": [ZONE["RNZ0"]],
            "index": 7,
            "entities": [0x24d0, 0x2d10],
            "as_relic": {},
            "vanilla_item": "Turquoise"
        },
    "Necromancy Lab. - Bottom Left Room From Beezelbub":
        {
            "ap_id": 347,
            "zones": [ZONE["RNZ0"]],
            "index": 8,
            "entities": [0x2368, 0x2c48],
            "as_relic": {"x": 0x0082, "y": 0x0080},
            "vanilla_item": "Ring of arcana"
        },
    "Necromancy Lab. - Globe in the Room With Lesser Demons and Ctulhu":
        {
            "ap_id": 348,
            "zones": [ZONE["RNZ0"]],
            "index": 9,
            "entities": [0x262e, 0x2edc],
            "as_relic": {},
            "vanilla_item": "Resist dark"
        },
    # Reverse Clock Tower items
    "Reverse Clock Tower Open Area - Above Stone Bridge Left Item":
        {
            "ap_id": 349,
            "zones": [ZONE["RNZ1"]],
            "index": 0,
            "entities": [0x2ad6, 0x32ee],
            "as_relic": {"y": 0x0165},
            "vanilla_item": "Magic missile"
        },
    "Reverse Clock Tower Open Area - Above Stone Bridge Right Item":
        {
            "ap_id": 350,
            "zones": [ZONE["RNZ1"]],
            "index": 1,
            "entities": [0x2aea, 0x3316],
            "as_relic": {"y": 0x0180},
            "vanilla_item": "Karma coin"
        },
    "Reverse Clock Tower Open Area - Left Column":
        {
            "ap_id": 351,
            "zones": [ZONE["RNZ1"]],
            "index": 2,
            "entities": [0x2af4, 0x3352],
            "as_relic": {"y": 0x0248},
            "vanilla_item": "Str. potion"
        },
    "Reverse Clock Tower Open Area - Middle Column":
        {
            "ap_id": 352,
            "zones": [ZONE["RNZ1"]],
            "index": 3,
            "entities": [0x2afe, 0x335c],
            "as_relic": {"y": 0x0258},
            "vanilla_item": "Luminus"
        },
    "Reverse Clock Tower Open Area - Right Column":
        {
            "ap_id": 353,
            "zones": [ZONE["RNZ1"]],
            "index": 4,
            "entities": [0x2b12, 0x3348],
            "as_relic": {"y": 0x0248},
            "vanilla_item": "Smart potion"
        },
    "Reverse Clock Tower Open Area - Bottom Left Room":
        {
            "ap_id": 354,
            "zones": [ZONE["RNZ1"]],
            "index": 5,
            "entities": [0x2a36, 0x329e],
            "as_relic": {"y": 0x0060},
            "vanilla_item": "Dragon helm"
        },
    "Reverse Clock Tower Medusa Area - Gears Puzzle Room Left Item":
        {
            "ap_id": 355,
            "zones": [ZONE["RNZ1"]],
            "index": 6,
            "entities": [0x29dc, 0x3280],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Diamond"
        },
    "Reverse Clock Tower Medusa Area - Gears Puzzle Room Middle Item":
        {
            "ap_id": 356,
            "zones": [ZONE["RNZ1"]],
            "index": 7,
            "entities": [0x2a0e, 0x3276],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Life apple"
        },
    "Reverse Clock Tower Medusa Area - Gears Puzzle Room Right Item":
        {
            "ap_id": 357,
            "zones": [ZONE["RNZ1"]],
            "index": 8,
            "entities": [0x2a18, 0x326c],
            "as_relic": {"y": 0x00c0},
            "vanilla_item": "Sunstone"
        },
    "Reverse Clock Tower Medusa Area - Room Behind Bottom Left Breakable Wall Left Item":
        {
            "ap_id": 358,
            "zones": [ZONE["RNZ1"]],
            "index": 9,
            "entities": [0x25c2, 0x2e34],
            "as_relic": {"y": 0x0038},
            "vanilla_item": "Life Vessel"
        },
    "Reverse Clock Tower Medusa Area - Room Behind Bottom Left Breakable Wall Right Item":
        {
            "ap_id": 359,
            "zones": [ZONE["RNZ1"]],
            "index": 10,
            "entities": [0x25e0, 0x2e2a],
            "as_relic": {"y": 0x0038},
            "vanilla_item": "Heart Vessel"
        },
    "Reverse Clock Tower - Behind Breakable Wall Next to Bronze Statue":
        {
            "ap_id": 360,
            "zones": [ZONE["RNZ1"]],
            "index": 11,
            "entities": [0x2d06, 0x3578],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Moon rod"
        },
    "Reverse Clock Tower - Near Darkwing Bat Middle Breakable Wall":
        {
            "ap_id": 361,
            "zones": [ZONE["RNZ1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2d56, 0x3596],
            "addresses": [0x059bc354],
            "bin_addresses": [0xf4ee6, 0x438d67e],
            "rom_address": 0xdfcee,
            "break_flag": 0x03be97,
            "break_mask": 0x4,
            "vanilla_item": "Bwaka knife"
        },
    "Reverse Clock Tower - Breakable Wall Item on Brackets":
        {
            "ap_id": 362,
            "zones": [ZONE["RNZ1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2bd0, 0x34a6],
            "addresses": [0x059bc34c],
            "bin_addresses": [0xf4ee8, 0x438d680],
            "rom_address": 0xdfcf0,
            "break_flag": 0x03be97,
            "break_mask": 0x1,
            "vanilla_item": "Pot roast"
        },
    "Reverse Clock Tower - Near Darkwing Bat Right Breakable Wall":
        {
            "ap_id": 363,
            "zones": [ZONE["RNZ1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2d74, 0x3596],
            "addresses": [0x059bc350],
            "bin_addresses": [0xf4eea, 0x438d682],
            "rom_address": 0xdfcf2,
            "break_flag": 0x03be97,
            "break_mask": 0x2,
            "vanilla_item": "Shuriken"
        },
    "Reverse Clock Tower - Near Darkwing Bat Left Breakable Wall":
        {
            "ap_id": 364,
            "zones": [ZONE["RNZ1"]],
            "despawn": True,
            "no_offset": True,
            "entities": [0x2d38, 0x35d2],
            "addresses": [0x059bc358],
            "bin_addresses": [0xf4eec, 0x438d684],
            "rom_address": 0xdfcf4,
            "break_flag": 0x03be97,
            "break_mask": 0x8,
            "vanilla_item": "TNT"
        },
    "Reverse Clock Tower - Darkwing Bat Item":
        {
            "ap_id": 365,
            "zones": [ZONE["RNZ1"]],
            "index": 12,
            "entities": [0x2dce, 0x3640],
            "erase_entity": False,
            "ids": [{"zones": ZONE["RNZ1"], "addresses": [0x059e8074, 0x059ee2e4, 0x059bdb30]}],
            "kill_time": 0x03ca78,
            "erase":
                {
                    "instructions": [{"addresses": [0x059ee594], "instruction": 0x34020000},
                                     {"addresses": [0x059ee2d0], "instruction": 0x34020000},
                                     {"addresses": [0x059ee2d4], "instruction": 0x00000000}]
                },
            "as_item": {"y": 0x00c9},
            "vanilla_item": "Ring of vlad"
        },
    # Reverse Castle Keep items
    "R. Castle Keep - Open Area Top Right Breakable Wall":
        {
            "ap_id": 366,
            "zones": [ZONE["RTOP"]],
            "index": 0,
            "entities": [0x1c80, 0x2004],  # TODO Swapped with Iron ball
            "tile_index": 2,
            "as_relic": {"x": 0x0670},
            "vanilla_item": "Sword of dawn"
        },
    "R. Castle Keep - Open Area Bottom Left Underpass Breakable Wall":
        {
            "ap_id": 367,
            "zones": [ZONE["RTOP"]],
            "index": 1,
            "entities": [0x1c76, 0x2040],  # TODO Swapped with Sword of dawn
            "as_relic": {"x": 0x0670},
            "vanilla_item": "Iron ball"
        },
    "R. Castle Keep - Red Vase After Entering":
        {
            "ap_id": 368,
            "zones": [ZONE["RTOP"]],
            "index": 2,
            "entities": [0x1b9a, 0x209a],
            "as_relic": {},
            "vanilla_item": "Zircon"
        },
    "R. Castle Keep - Bellow Stairs Right Statue 2":
        {
            "ap_id": 369,
            "zones": [ZONE["RTOP"]],
            "index": 4,
            "entities": [0x1d66, 0x2162],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Bastard sword"
        },
    "R. Castle Keep - Bellow Stairs Right Statue 1":
        {
            "ap_id": 370,
            "zones": [ZONE["RTOP"]],
            "index": 5,
            "entities": [0x1d5c, 0x216c],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Life Vessel"
        },
    "R. Castle Keep - Bellow Stairs Right Yellow Vase 2":
        {
            "ap_id": 371,
            "zones": [ZONE["RTOP"]],
            "index": 6,
            "entities": [0x1d52, 0x2176],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Heart Vessel"
        },
    "R. Castle Keep - Bellow Stairs Right Yellow Vase 1":
        {
            "ap_id": 372,
            "zones": [ZONE["RTOP"]],
            "index": 7,
            "entities": [0x1d48, 0x2180],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Life Vessel"
        },
    "R. Castle Keep - Bellow Stairs Left Yellow Vase 2":
        {
            "ap_id": 373,
            "zones": [ZONE["RTOP"]],
            "index": 8,
            "entities": [0x1d34, 0x218a],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Heart Vessel"
        },
    "R. Castle Keep - Bellow Stairs Left Yellow Vase 1":
        {
            "ap_id": 374,
            "zones": [ZONE["RTOP"]],
            "index": 9,
            "entities": [0x1d2a, 0x2194],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Life Vessel"
        },
    "R. Castle Keep - Bellow Stairs Left Statue 1":
        {
            "ap_id": 375,
            "zones": [ZONE["RTOP"]],
            "index": 10,
            "entities": [0x1d20, 0x219e],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Heart Vessel"
        },
    "R. Castle Keep - Bellow Stairs Left Statue 2":
        {
            "ap_id": 376,
            "zones": [ZONE["RTOP"]],
            "index": 11,
            "entities": [0x1d16, 0x21a8],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Royal cloak"
        },
    "R. Castle Keep - Open Area Bottom Right Room Item 1":
        {
            "ap_id": 377,
            "zones": [ZONE["RTOP"]],
            "index": 17,
            "entities": [0x1e06, 0x2248],
            "as_relic": {"y": 0x0148},
            "vanilla_item": "Resist fire"
        },
    "R. Castle Keep - Open Area Bottom Right Room Item 2":
        {
            "ap_id": 378,
            "zones": [ZONE["RTOP"]],
            "index": 18,
            "entities": [0x1de8, 0x223e],
            "as_relic": {"y": 0x0128},
            "vanilla_item": "Resist ice"
        },
    "R. Castle Keep - Open Area Bottom Right Room Item 4":
        {
            "ap_id": 379,
            "zones": [ZONE["RTOP"]],
            "index": 19,
            "entities": [0x1dfc, 0x222a],
            "as_relic": {"y": 0x0087},
            "vanilla_item": "Resist thunder"
        },
    "R. Castle Keep - Open Area Bottom Right Room Item 3":
        {
            "ap_id": 380,
            "zones": [ZONE["RTOP"]],
            "index": 20,
            "entities": [0x1df2, 0x2234],
            "as_relic": {"y": 0x00c8},
            "vanilla_item": "Resist stone"
        },
    "R. Castle Keep - Open Area Bottom Right Room Window Item":
        {
            "ap_id": 381,
            "zones": [ZONE["RTOP"]],
            "index": 21,
            "entities": [0x1dde, 0x225c],
            "as_relic": {"y": 0x0190},
            "vanilla_item": "High potion"
        },
    "R. Castle Keep - Open Area Top Right Ledge":
        {
            "ap_id": 382,
            "zones": [ZONE["RTOP"]],
            "index": 22,
            "entities": [0x1c6c, 0x1ffa],
            "as_relic": {"y": 0x0110},
            "vanilla_item": "Garnet"
        },
    "R. Castle Keep - Bottom Left Room on Dual Elevator Area":
        {
            "ap_id": 383,
            "zones": [ZONE["RTOP"]],
            "index": 23,
            "entities": [0x1e2e, 0x227a],
            "as_relic": {"y": 0x0080},
            "vanilla_item": "Lightning mail"
        },
    "R. Castle Keep - Bellow Save Point":
        {
            "ap_id": 384,
            "zones": [ZONE["RTOP"]],
            "index": 24,
            "entities": [0x1e4c, 0x22a2],
            "as_relic": {"y": 0x00b0},
            "vanilla_item": "Library card"
        },
    # Bosses items
    "Reverse Colosseum - Trio item":
        {
            "ap_id": 385,
            "zones": [ZONE["RARE"]],
            "index": 8,
            "entities": [0x23ba, 0x293c],
            "reward": {"zones": ZONE["RBO0"], "index": 0x02},
            "kill_time": 0x03ca54,
            "as_item": {"y": 0x00d9},
            "erase":
                {
                    "instructions": [{"addresses": [0x06487bd4], "instruction": 0x34020000}]
                },
            "trio": True,
            "vanilla_item": "Life Vessel"
        }
}

for k, v in locations.items():
    # NO0
    if v["zones"][0] == 8:
        if 8 in ZONE_LOCATIONS:
            ZONE_LOCATIONS[8].append({k: v})
            ZONE_LOCATIONS[3].append({k: v})
        else:
            ZONE_LOCATIONS[8] = [{k: v}]
            ZONE_LOCATIONS[3] = [{k: v}]
    # NO3 / NP3
    elif v["zones"][0] == 11 or v["zones"][0] == 12:
        if 11 in ZONE_LOCATIONS:
            ZONE_LOCATIONS[11].append({k: v})
            ZONE_LOCATIONS[12].append({k: v})
        else:
            ZONE_LOCATIONS[11] = [{k: v}]
            ZONE_LOCATIONS[12] = [{k: v}]
    # NO4
    elif v["zones"][0] == 13:
        if 13 in ZONE_LOCATIONS:
            ZONE_LOCATIONS[13].append({k: v})
            ZONE_LOCATIONS[36].append({k: v})
        else:
            ZONE_LOCATIONS[13] = [{k: v}]
            ZONE_LOCATIONS[36] = [{k: v}]
    # RARE
    elif v["zones"][0] == 18:
        if 18 in ZONE_LOCATIONS:
            ZONE_LOCATIONS[18].append({k: v})
            ZONE_LOCATIONS[41].append({k: v})
        else:
            ZONE_LOCATIONS[18] = [{k: v}]
            ZONE_LOCATIONS[41] = [{k: v}]
    # RCHI
    elif v["zones"][0] == 21:
        if 21 in ZONE_LOCATIONS:
            ZONE_LOCATIONS[21].append({k: v})
            ZONE_LOCATIONS[43].append({k: v})
        else:
            ZONE_LOCATIONS[21] = [{k: v}]
            ZONE_LOCATIONS[43] = [{k: v}]
    # RDAI
    elif v["zones"][0] == 22:
        if 22 in ZONE_LOCATIONS:
            ZONE_LOCATIONS[22].append({k: v})
            ZONE_LOCATIONS[44].append({k: v})
        else:
            ZONE_LOCATIONS[22] = [{k: v}]
            ZONE_LOCATIONS[44] = [{k: v}]
    # RNO1
    elif v["zones"][0] == 25:
        if 25 in ZONE_LOCATIONS:
            ZONE_LOCATIONS[25].append({k: v})
            ZONE_LOCATIONS[45].append({k: v})
        else:
            ZONE_LOCATIONS[25] = [{k: v}]
            ZONE_LOCATIONS[45] = [{k: v}]
    # RNO2
    elif v["zones"][0] == 26:
        if 26 in ZONE_LOCATIONS:
            ZONE_LOCATIONS[26].append({k: v})
            ZONE_LOCATIONS[48].append({k: v})
        else:
            ZONE_LOCATIONS[26] = [{k: v}]
            ZONE_LOCATIONS[48] = [{k: v}]
    else:
        if v["zones"][0] in ZONE_LOCATIONS:
            ZONE_LOCATIONS[v["zones"][0]].append({k: v})
        else:
            ZONE_LOCATIONS[v["zones"][0]] = [{k: v}]
    zone = ZONE_TO_NAME[v["zones"][0]]
    vanilla: str = v["vanilla_item"]
    if vanilla in RELIC_NAMES:
        LOCATION_TO_ABREV[k] = vanilla
        ABREV_TO_LOCATION[vanilla] = k
    else:
        if "index" in v:
            index = str(v["index"])
        else:
            if "addresses" in v:
                index = str(v["addresses"][0])
            else:
                index = "NULL"
        res_str = zone + '_' + vanilla + '_' + index
        LOCATION_TO_ABREV[k] = res_str
        ABREV_TO_LOCATION[res_str] = k

    if "bin_addresses" in v:
        BREAKABLE_LOCATIONS[k] = v

    AP_ID_TO_NAME[v["ap_id"] + BASE_LOCATION_ID] = k


class SotnLocation(Location):
    game = "Symphony of the Night"
