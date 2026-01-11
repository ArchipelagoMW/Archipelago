from .Constants import *


HINT_DATA = {

    # Shops
    "Island Shop Power Gem": {
        "scenes": [0xB11, 0xC0E, 0x1014],
        "slot_data": ["shop_hints"]
    },
    "Island Shop Quiver": {
        "scenes": [0xB11, 0xC0E, 0x1014],
        "slot_data": ["shop_hints"],
        "has_items": ["Bow (Progressive)"]
    },
    "Island Shop Bombchu Bag Plus": {
        "locations": ["Island Shop Bombchu Bag", "Island Shop Heart Container"],
        "scenes": [0xB11, 0xC0E, 0x1014],
        "slot_data": ["shop_hints"],
        "has_items": ["Bow (Progressive)", "Bombchus (Progressive)"]
    },

    # Beedle
    "Beedle Shop Wisdom Gem": {
        "scenes": [0x500],
        "slot_data": ["shop_hints"],
    },
    "Beedle Shop Bomb Bag": {
        "scenes": [0x500],
        "slot_data": ["shop_hints"],
        "has_items": ["Bombs (Progressive)"]
    },
    "Masked Beedle": {
        "locations": ["Masked Beedle Heart Container", "Masked Beedle Courage Gem"],
        "scenes": [0x500],
        "slot_data": ["shop_hints", "randomize_masked_beedle"],
    },

    # Eddo
    "Cannon Island": {
        "locations": ["Cannon Island Cannon", "Cannon Island Salvage Arm"],
        "slot_data": ["shop_hints"],
        "scenes": [0x130B],
    },

    # Spirit Island
    "Spirit Island 1": {
        "locations": LOCATION_GROUPS["Spirit Upgrades"],
        "scenes": [0x1701],
        "slot_data": [("spirit_island_hints", 0)]
    },
    "Spirit Island 2": {
        "locations": ["Spirit Island Power Upgrade Level 2",
                      "Spirit Island Wisdom Upgrade Level 2",
                      "Spirit Island Courage Upgrade Level 2"],
        "scenes": [0x1701],
        "slot_data": [("spirit_island_hints", 1)]
    },

    # Dungeon Hints
    "Oshus Dungeon Hints": {
        "scenes": [0xb0A],
        "slot_data": [("dungeon_hint_location", 1), ("goal_requirements", [1, 2])],
        "locations": ["Dungeon Hints"]
    },
    "TotOK Dungeon Hints": {
        "scenes": [0x2600],
        "slot_data": [("dungeon_hint_location", 2), ("goal_requirements", [1, 2])],
        "locations": ["Dungeon Hints"]
    },

    # Minigame Hints
    "Bannan Island Cannon Game": {
        "scenes": [0x1400],
        "has_items": ["Bombs (Progressive)"],
        "slot_data": [("randomize_minigames", 1)],
    },
    "Molida Archery 1700": {
        "scenes": [0xC0B],
        "slot_data": [("randomize_minigames", 1)],
    },
    "Molida Archery 2000": {
        "scenes": [0xC0B],
        "slot_data": [("randomize_minigames", 1), ("logic", [1, 2])],
    },
    "Dee Ess Win Goron Game": {
        "scenes": [0x1B00],
        "slot_data": [("randomize_minigames", 1)],
    },
    "Harrow Island": {
        "scenes": [0x1800],
        "slot_data": [("randomize_harrow", 1)],
        "locations": ["Harrow Island Dig 1", "Harrow Island Dig 2", "Harrow Island Dig 3", "Harrow Island Dig 4"]
    },
    "Maze Island": {
        "scenes": [0x1900],
        "slot_data": [("randomize_minigames", 1)],
        "locations": ["Maze Island Beginner", "Maze Island Normal", "Maze Island Expert", "Maze Island Bonus Reward"]
    },
    "Ocean NW Prince of Red Lion Combat Reward": {
        "scenes": [0x700],
        "slot_data": [("randomize_minigames", 1)],
    },
    "Fishing Hints": {
        "scenes": [0x1401],
        "slot_data": [("randomize_fishing", 1)],
        "locations": LOCATION_GROUPS["Fish"]
    },

}
