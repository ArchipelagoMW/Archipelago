from typing import List, TypedDict

class Location(TypedDict):
    id: int
    inGameId: str
    title: str
    art: str

base_id = 123500

locations: List[Location] = [
    # Main Quests
    {
        "id": base_id + 1,
        "inGameId": "MainQuest_001",
        "title": "A Whole New World",
        "art": "none"
    },
    {
        "id": base_id + 2,
        "inGameId": "MainQuest_002",
        "title": "The Catpital (1)",
        "art": "none"
    },
    {
        "id": base_id + 3,
        "inGameId": "MainQuest_003",
        "title": "The Catpital (2)",
        "art": "none"
    },
    {
        "id": base_id + 4,
        "inGameId": "MainQuest_004",
        "title": "The Dragon and the Cat",
        "art": "none"
    },
    {
        "id": base_id + 5,
        "inGameId": "MainQuest_005",
        "title": "The Old Ruins",
        "art": "none"
    },
    {
        "id": base_id + 6,
        "inGameId": "MainQuest_006",
        "title": "Of Sea and Rock (1)",
        "art": "none"
    },
    {
        "id": base_id + 7,
        "inGameId": "MainQuest_007",
        "title": "Of Sea and Rock (2)",
        "art": "none"
    },
    {
        "id": base_id + 8,
        "inGameId": "MainQuest_008",
        "title": "The Old Friend",
        "art": "none"
    },
    {
        "id": base_id + 9,
        "inGameId": "MainQuest_009",
        "title": "The Dragonblood",
        "art": "none"
    },
    {
        "id": base_id + 10,
        "inGameId": "MainQuest_010",
        "title": "The Dragonsbane",
        "art": "none"
    },
    {
        "id": base_id + 11,
        "inGameId": "MainQuest_011",
        "title": "The Dragons Void",
        "art": "none"
    },
    {
        "id": base_id + 12,
        "inGameId": "MainQuest_012",
        "title": "Epilogue",
        "art": "none"
    },

    # Sanctuary Quests
    {
        "id": base_id + 13,
        "inGameId": "sanctuary_one",
        "title": "I. The Strange Charm",
        "art": "none"
    },
    {
        "id": base_id + 14,
        "inGameId": "sanctuary_two",
        "title": "II. The Escape",
        "art": "none"
    },
    {
        "id": base_id + 15,
        "inGameId": "sanctuary_three",
        "title": "III. The Sacrifice",
        "art": "none"
    },
    {
        "id": base_id + 16,
        "inGameId": "sanctuary_four",
        "title": "IV. The Sanctuary",
        "art": "none"
    },

    # Great Spirit Quests
    {
        "id": base_id + 17,
        "inGameId": "greatspirit_one",
        "title": "I. The Servant of God",
        "art": "none"
    },
    {
        "id": base_id + 18,
        "inGameId": "greatspirit_two",
        "title": "II. The Offerings",
        "art": "none"
    },
    {
        "id": base_id + 19,
        "inGameId": "greatspirit_three",
        "title": "III. The Prayer",
        "art": "none"
    },
    {
        "id": base_id + 20,
        "inGameId": "greatspirit_four",
        "title": "IV. The Godcat, Mauth",
        "art": "none"
    },

    # Kitmas Quests
    {
        "id": base_id + 21, 
        "inGameId": "kitmas_one", 
        "title": "The First Day of Kitmas", 
        "art": "none"
    },
    {
        "id": base_id + 22, 
        "inGameId": "kitmas_two", 
        "title": "The Second Day of Kitmas", 
        "art": "none"
    },
    {
        "id": base_id + 23, 
        "inGameId": "kitmas_three", 
        "title": "The Third Day of Kitmas", 
        "art": "none"
    },
    {
        "id": base_id + 24, 
        "inGameId": "kitmas_four", 
        "title": "The Fourth Day of Kitmas", 
        "art": "none"
    },
    {
        "id": base_id + 25, 
        "inGameId": "kitmas_five", 
        "title": "Mewry Kitmas!", 
        "art": "none"
    },

    # Missing Quests
    {
        "id": base_id + 26, 
        "inGameId": "missing_one", 
        "title": "I. The Missing Soldiers", 
        "art": "none"
    },
    {
        "id": base_id + 27, 
        "inGameId": "missing_two", 
        "title": "II. The Rescue", 
        "art": "none"
    },

    # Faded King Quests
    {
        "id": base_id + 28, 
        "inGameId": "faded_king_one", 
        "title": "I. The King's Mage", 
        "art": "none"
    },
    {
        "id": base_id + 29, 
        "inGameId": "faded_king_three", 
        "title": "II. The Mage Search", 
        "art": "none"
    },
    {
        "id": base_id + 30, 
        "inGameId": "faded_king_four", 
        "title": "III. The Spirits", 
        "art": "none"
    },
    {
        "id": base_id + 31, 
        "inGameId": "faded_king_five", 
        "title": "IV. The Lion King", 
        "art": "none"
    },

    # East Quests
    {
        "id": base_id + 32, 
        "inGameId": "east_one", 
        "title": "I. The East Suspicion", 
        "art": "none"
    },
    {
        "id": base_id + 33, 
        "inGameId": "east_two", 
        "title": "II. The East Shipment", 
        "art": "none"
    },
    {
        "id": base_id + 34, 
        "inGameId": "east_three", 
        "title": "III. The East Escort", 
        "art": "none"
    },
    {
        "id": base_id + 35, 
        "inGameId": "east_four", 
        "title": "IV. The East Catfrontation", 
        "art": "none"
    },

    # Meat Quests
    {
        "id": base_id + 36, 
        "inGameId": "meatmeatmeat", 
        "title": "I. Meat Meat Meat!", 
        "art": "none"
    },
    {
        "id": base_id + 37, 
        "inGameId": "red_riding_kitty", 
        "title": "II. Meatmeatmeatmeat!!", 
        "art": "none"
    },
    {
        "id": base_id + 38, 
        "inGameId": "distraction", 
        "title": "III. Meat Disposal Crew", 
        "art": "none"
    },
    {
        "id": base_id + 39, 
        "inGameId": "crafty_merchant", 
        "title": "IV. The Meat Seller", 
        "art": "none"
    },

    # Whisperer Quests
    {
        "id": base_id + 40, 
        "inGameId": "the_whisperer_one", 
        "title": "I. The Growling Peasant", 
        "art": "none"
    },
    {
        "id": base_id + 41, 
        "inGameId": "the_whisperer_two", 
        "title": "II. The Catnip Ritual", 
        "art": "none"
    },
    {
        "id": base_id + 42, 
        "inGameId": "the_whisperer_three", 
        "title": "III. The Circle", 
        "art": "none"
    },
    {
        "id": base_id + 43, 
        "inGameId": "the_whisperer_four", 
        "title": "IV. Fur-reedom!", 
        "art": "none"
    },
    {
        "id": base_id + 44, 
        "inGameId": "the_whisperer_five", 
        "title": "V. The Whispurrer", 
        "art": "none"
    },

    # Waters Quests
    {
        "id": base_id + 45, 
        "inGameId": "waters_one", 
        "title": "I. Path to Water Walking", 
        "art": "none"
    },
    {
        "id": base_id + 46, 
        "inGameId": "waters_three", 
        "title": "II. The Fusion", 
        "art": "none"
    },
    {
        "id": base_id + 47, 
        "inGameId": "waters_four", 
        "title": "III. Rogue Mages", 
        "art": "none"
    },
    {
        "id": base_id + 48, 
        "inGameId": "waters_five", 
        "title": "IV. The Miracle", 
        "art": "none"
    },

    # West Quests
    {
        "id": base_id + 49, 
        "inGameId": "west_one", 
        "title": "I. The West Investigation", 
        "art": "none"
    },
    {
        "id": base_id + 50, 
        "inGameId": "west_two", 
        "title": "II. The West Heist", 
        "art": "none"
    },
    {
        "id": base_id + 51, 
        "inGameId": "west_three", 
        "title": "III. The Magic Lock", 
        "art": "none"
    },
    {
        "id": base_id + 52, 
        "inGameId": "west_four", 
        "title": "IV. The Revelation", 
        "art": "none"
    },

    # Flight Quests
    {
        "id": base_id + 53, 
        "inGameId": "magesold_one", 
        "title": "I. The Flying Bush", 
        "art": "none"
    },
    {
        "id": base_id + 54, 
        "inGameId": "magesold_two", 
        "title": "II. The Magic Tree", 
        "art": "none"
    },
    {
        "id": base_id + 55, 
        "inGameId": "magesold_three", 
        "title": "III. The Cult", 
        "art": "none"
    },
    {
        "id": base_id + 56, 
        "inGameId": "magesold_four", 
        "title": "IV. Dragonflight", 
        "art": "none"
    },

    # Dark Past Quests
    {
        "id": base_id + 57, 
        "inGameId": "darkpast_one", 
        "title": "I. The Missing Pages", 
        "art": "none"
    },
    {
        "id": base_id + 58, 
        "inGameId": "darkpast_two", 
        "title": "II. The Protected Pages", 
        "art": "none"
    },
    {
        "id": base_id + 59, 
        "inGameId": "darkpast_three", 
        "title": "III. The Runaway Archeologist", 
        "art": "none"
    },
    {
        "id": base_id + 60, 
        "inGameId": "darkpast_four", 
        "title": "IV. The Treasure", 
        "art": "none"
    },

    # Blacksmith Quests
    {
        "id": base_id + 61, 
        "inGameId": "blacksmith_assistance", 
        "title": "I. Blacksmith Assistance", 
        "art": "none"
    },
    {
        "id": base_id + 62, 
        "inGameId": "blacksmith_apprentice", 
        "title": "II. Blacksmith Apprentice", 
        "art": "none"
    },
    {
        "id": base_id + 63, 
        "inGameId": "blacksmith_journeyman", 
        "title": "III. Blacksmith Journeyman", 
        "art": "none"
    },
    {
        "id": base_id + 64, 
        "inGameId": "blacksmith_master", 
        "title": "IV. Blacksmith Master", 
        "art": "none"
    },

    # Misc Quests
    {#?
        "id": base_id + 65, 
        "inGameId": "wyvern_attack", 
        "title": "The Dragon Worshippers", 
        "art": "none"
    },
    {
        "id": base_id + 66, 
        "inGameId": "the_heirloom", 
        "title": "The Heirloom Armor", 
        "art": "none"
    },
    {
        "id": base_id + 67, 
        "inGameId": "furbidden_mystery", 
        "title": "The Furbidden History", 
        "art": "none"
    },
    {
        "id": base_id + 68, 
        "inGameId": "golden_key", 
        "title": "The Golden Key", 
        "art": "none"
    },
    {
        "id": base_id + 69, 
        "inGameId": "ultimate_dragonsbane", 
        "title": "The Ultimate Dragonsbane", 
        "art": "none"
    },
    {
        "id": base_id + 70, 
        "inGameId": "pawtato_one", 
        "title": "The Pawtato Mystery", 
        "art": "none"
    },
    {
        "id": base_id + 71, 
        "inGameId": "advertising_one", 
        "title": "Everyone's invited!", 
        "art": "none"
    },
    {
        "id": base_id + 72, 
        "inGameId": "slashy_one", 
        "title": "The Forgotten Hero", 
        "art": "none"
    },

    # Catnip Cure Quests
    {
        "id": base_id + 73, 
        "inGameId": "catnip_cure_A", 
        "title": "I. The Catnip Cure", 
        "art": "none"
    },
    {
        "id": base_id + 74, 
        "inGameId": "catnip_cure_B", 
        "title": "I. The Catnip Cure...again", 
        "art": "none"
    },
    {
        "id": base_id + 75, 
        "inGameId": "knightmare_A", 
        "title": "II. The Knightmare", 
        "art": "none"
    },
    {
        "id": base_id + 76, 
        "inGameId": "knightmare_B", 
        "title": "II. The Knightmare... again", 
        "art": "none"
    },
    {
        "id": base_id + 77, 
        "inGameId": "book_A", 
        "title": "III. The Book", 
        "art": "none"
    },
    {
        "id": base_id + 78, 
        "inGameId": "book_B", 
        "title": "III. The Book...again", 
        "art": "none"
    },
    {
        "id": base_id + 79, 
        "inGameId": "resolution_A", 
        "title": "IV. The Twin Resolution", 
        "art": "none"
    }
]