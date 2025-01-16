from typing import List, TypedDict

class Location(TypedDict):
    id: int
    inGameId: str
    name: str
    art: str

base_id = 123500

locations: List[Location] = [
    # Main Quests
    {
        "id": base_id + 1,
        "inGameId": "MainQuest_001_PC",
        "name": "A Whole New World",
        "art": "none"
    },
    {
        "id": base_id + 2,
        "inGameId": "MainQuest_002",
        "name": "The Catpital (1)",
        "art": "none"
    },
    {
        "id": base_id + 3,
        "inGameId": "MainQuest_003",
        "name": "The Catpital (2)",
        "art": "none"
    },
    {
        "id": base_id + 4,
        "inGameId": "MainQuest_004",
        "name": "The Dragon and the Cat",
        "art": "none"
    },
    {
        "id": base_id + 5,
        "inGameId": "MainQuest_005",
        "name": "The Old Ruins",
        "art": "none"
    },
    {
        "id": base_id + 6,
        "inGameId": "MainQuest_006",
        "name": "Of Sea and Rock (1)",
        "art": "water"
    },
    {
        "id": base_id + 7,
        "inGameId": "MainQuest_007",
        "name": "Of Sea and Rock (2)",
        "art": "both"
    },
    {
        "id": base_id + 8,
        "inGameId": "MainQuest_008",
        "name": "The Old Friend",
        "art": "both"
    },
    {
        "id": base_id + 9,
        "inGameId": "MainQuest_009",
        "name": "The Dragonblood",
        "art": "both"
    },
    {
        "id": base_id + 10,
        "inGameId": "MainQuest_010",
        "name": "The Dragonsbane",
        "art": "both"
    },
    {
        "id": base_id + 11,
        "inGameId": "MainQuest_011",
        "name": "The Dragons Void",
        "art": "both"
    },
    {
        "id": base_id + 12,
        "inGameId": "MainQuest_012",
        "name": "Epilogue",
        "art": "both"
    },

    # Sanctuary Quests
    {
        "id": base_id + 13,
        "inGameId": "sanctuary_one",
        "name": "I. The Strange Charm",
        "art": "none"
    },
    {
        "id": base_id + 14,
        "inGameId": "sanctuary_two",
        "name": "II. The Escape",
        "art": "none"
    },
    {
        "id": base_id + 15,
        "inGameId": "sanctuary_three",
        "name": "III. The Sacrifice",
        "art": "none"
    },
    {
        "id": base_id + 16,
        "inGameId": "sanctuary_four",
        "name": "IV. The Sanctuary",
        "art": "none"
    },

    # Great Spirit Quests
    {
        "id": base_id + 17,
        "inGameId": "greatspirit_one",
        "name": "I. The Servant of God",
        "art": "either"
    },
    {
        "id": base_id + 18,
        "inGameId": "greatspirit_two",
        "name": "II. The Offerings",
        "art": "water"
    },
    {
        "id": base_id + 19,
        "inGameId": "greatspirit_three",
        "name": "III. The Prayer",
        "art": "water"
    },
    {
        "id": base_id + 20,
        "inGameId": "greatspirit_four",
        "name": "IV. The Godcat, Mauth",
        "art": "water"
    },

    # Kitmas Quests
    {
        "id": base_id + 21, 
        "inGameId": "kitmas_one", 
        "name": "The First Day of Kitmas", 
        "art": "none"
    },
    {
        "id": base_id + 22, 
        "inGameId": "kitmas_two", 
        "name": "The Second Day of Kitmas", 
        "art": "none"
    },
    {
        "id": base_id + 23, 
        "inGameId": "kitmas_three", 
        "name": "The Third Day of Kitmas", 
        "art": "water"
    },
    {
        "id": base_id + 24, 
        "inGameId": "kitmas_four", 
        "name": "The Fourth Day of Kitmas", 
        "art": "water"
    },

    # Missing Quests
    {
        "id": base_id + 26, 
        "inGameId": "missing_one", 
        "name": "I. The Missing Soldiers", 
        "art": "none"
    },
    {
        "id": base_id + 27, 
        "inGameId": "missing_two", 
        "name": "II. The Rescue", 
        "art": "none"
    },

    # Faded King Quests
    {
        "id": base_id + 28, 
        "inGameId": "faded_king_one", 
        "name": "I. The King's Mage", 
        "art": "none"
    },
    {
        "id": base_id + 29, 
        "inGameId": "faded_king_three", 
        "name": "II. The Mage Search", 
        "art": "none"
    },
    {
        "id": base_id + 30, 
        "inGameId": "faded_king_four", 
        "name": "III. The Spirits", 
        "art": "none"
    },
    {
        "id": base_id + 31, 
        "inGameId": "faded_king_five", 
        "name": "IV. The Lion King", 
        "art": "none"
    },

    # East Quests
    {
        "id": base_id + 32, 
        "inGameId": "east_one", 
        "name": "I. The East Suspicion", 
        "art": "none"
    },
    {
        "id": base_id + 33, 
        "inGameId": "east_two", 
        "name": "II. The East Shipment", 
        "art": "none"
    },
    {
        "id": base_id + 34, 
        "inGameId": "east_three", 
        "name": "III. The East Escort", 
        "art": "none"
    },
    {
        "id": base_id + 35, 
        "inGameId": "east_four", 
        "name": "IV. The East Catfrontation", 
        "art": "none"
    },

    # Meat Quests
    {
        "id": base_id + 36, 
        "inGameId": "meatmeatmeat", 
        "name": "I. Meat Meat Meat!", 
        "art": "none"
    },
    {
        "id": base_id + 37, 
        "inGameId": "red_riding_kitty", 
        "name": "II. Meatmeatmeatmeat!!", 
        "art": "none"
    },
    {
        "id": base_id + 38, 
        "inGameId": "distraction", 
        "name": "III. Meat Disposal Crew", 
        "art": "none"
    },
    {
        "id": base_id + 39, 
        "inGameId": "crafty_merchant", 
        "name": "IV. The Meat Seller", 
        "art": "none"
    },

    # Whisperer Quests
    {
        "id": base_id + 40, 
        "inGameId": "the_whisperer_one", 
        "name": "I. The Growling Peasant", 
        "art": "none"
    },
    {
        "id": base_id + 41, 
        "inGameId": "the_whisperer_two", 
        "name": "II. The Catnip Ritual", 
        "art": "none"
    },
    {
        "id": base_id + 42, 
        "inGameId": "the_whisperer_three", 
        "name": "III. The Circle", 
        "art": "none"
    },
    {
        "id": base_id + 43, 
        "inGameId": "the_whisperer_four", 
        "name": "IV. Fur-reedom!", 
        "art": "none"
    },
    {
        "id": base_id + 44, 
        "inGameId": "the_whisperer_five", 
        "name": "V. The Whispurrer", 
        "art": "none"
    },

    # Waters Quests
    {
        "id": base_id + 45, 
        "inGameId": "waters_one", 
        "name": "I. Path to Water Walking", 
        "art": "none"
    },
    {
        "id": base_id + 46, 
        "inGameId": "waters_three", 
        "name": "II. The Fusion", 
        "art": "none"
    },
    {
        "id": base_id + 47, 
        "inGameId": "waters_four", 
        "name": "III. Rogue Mages", 
        "art": "none"
    },
    {
        "id": base_id + 48, 
        "inGameId": "waters_five", 
        "name": "IV. The Miracle", 
        "art": "water"
    },

    # West Quests
    {
        "id": base_id + 49, 
        "inGameId": "west_one", 
        "name": "I. The West Investigation", 
        "art": "none"
    },
    {
        "id": base_id + 50, 
        "inGameId": "west_two", 
        "name": "II. The West Heist", 
        "art": "none"
    },
    {
        "id": base_id + 51, 
        "inGameId": "west_three", 
        "name": "III. The Magic Lock", 
        "art": "none"
    },
    {
        "id": base_id + 52, 
        "inGameId": "west_four", 
        "name": "IV. The Revelation", 
        "art": "none"
    },

    # Flight Quests
    {
        "id": base_id + 53, 
        "inGameId": "magesold_one", 
        "name": "I. The Flying Bush", 
        "art": "either"
    },
    {
        "id": base_id + 54, 
        "inGameId": "magesold_two", 
        "name": "II. The Magic Tree", 
        "art": "either"
    },
    {
        "id": base_id + 55, 
        "inGameId": "magesold_three", 
        "name": "III. The Cult", 
        "art": "either"
    },
    {
        "id": base_id + 56, 
        "inGameId": "magesold_four", 
        "name": "IV. Dragonflight", 
        "art": "either"
    },

    # Dark Past Quests
    {
        "id": base_id + 57, 
        "inGameId": "darkpast_one", 
        "name": "I. The Missing Pages", 
        "art": "none"
    },
    {
        "id": base_id + 58, 
        "inGameId": "darkpast_two", 
        "name": "II. The Protected Pages", 
        "art": "none"
    },
    {
        "id": base_id + 59, 
        "inGameId": "darkpast_three", 
        "name": "III. The Runaway Archeologist", 
        "art": "none"
    },
    {
        "id": base_id + 60, 
        "inGameId": "darkpast_four", 
        "name": "IV. The Treasure", 
        "art": "none"
    },

    # Blacksmith Quests
    {
        "id": base_id + 61, 
        "inGameId": "blacksmith_assistance", 
        "name": "I. Blacksmith Assistance", 
        "art": "none"
    },
    {
        "id": base_id + 62, 
        "inGameId": "blacksmith_apprentice", 
        "name": "II. Blacksmith Apprentice", 
        "art": "none"
    },
    {
        "id": base_id + 63, 
        "inGameId": "blacksmith_journeyman", 
        "name": "III. Blacksmith Journeyman", 
        "art": "none"
    },
    {
        "id": base_id + 64, 
        "inGameId": "blacksmith_master", 
        "name": "IV. Blacksmith Master", 
        "art": "none"
    },

    # Misc Quests
    {
        "id": base_id + 65, 
        "inGameId": "wyvern_attack", 
        "name": "The Dragon Worshippers", 
        "art": "none"
    },
    {
        "id": base_id + 66, 
        "inGameId": "the_heirloom", 
        "name": "The Heirloom Armor", 
        "art": "water"
    },
    {
        "id": base_id + 68, 
        "inGameId": "golden_key", 
        "name": "The Golden Key", 
        "art": "either"
    },
    {
        "id": base_id + 69, 
        "inGameId": "ultimate_dragonsbane", 
        "name": "The Ultimate Dragonsbane", 
        "art": "water"
    },
    {
        "id": base_id + 70, 
        "inGameId": "pawtato_one", 
        "name": "The Pawtato Mystery", 
        "art": "water"
    },


    # Catnip Cure Quests
    {
        "id": base_id + 73, 
        "inGameId": "catnip_cure_A", 
        "name": "I. The Catnip Cure", 
        "art": "none"
    },
    {
        "id": base_id + 74, 
        "inGameId": "catnip_cure_B", 
        "name": "I. The Catnip Cure...again", 
        "art": "none"
    },
    {
        "id": base_id + 75, 
        "inGameId": "knightmare_A", 
        "name": "II. The Knightmare", 
        "art": "none"
    },
    {
        "id": base_id + 76, 
        "inGameId": "knightmare_B", 
        "name": "II. The Knightmare... again", 
        "art": "none"
    },
    {
        "id": base_id + 77, 
        "inGameId": "book_A", 
        "name": "III. The Book", 
        "art": "none"
    },
    {
        "id": base_id + 78, 
        "inGameId": "book_B", 
        "name": "III. The Book...again", 
        "art": "none"
    },
    {
        "id": base_id + 79, 
        "inGameId": "resolution_A", 
        "name": "IV. The Twin Resolution", 
        "art": "none"
    }
]

endgame_locations: List[Location] = [
    # Endgame Quests
    {
        "id": base_id + 25, 
        "inGameId": "kitmas_five", 
        "name": "Mewry Kitmas!", 
        "art": "water"
    },
    {
        "id": base_id + 71, 
        "inGameId": "advertising_one", 
        "name": "Everyone's invited!", 
        "art": "flight"
    },
    {
        "id": base_id + 72, 
        "inGameId": "slashy_one", 
        "name": "The Forgotten Hero", 
        "art": "either"
    },
    {
        "id": base_id + 67, 
        "inGameId": "furbidden_mystery", 
        "name": "The Furbidden History", 
        "art": "none"
    }
]