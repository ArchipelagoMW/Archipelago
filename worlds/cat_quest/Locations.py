from typing import List, TypedDict

class Location(TypedDict):
    id: int
    inGameId: str
    title: str
    royalArt: str

locations: List[Location] = [
    # Main Quests
    {
        "id": base_id + 1,
        "inGameId": "MainQuest_001",
        "title": "A Whole New World",
        "royalArt": "none"
    },
    {
        "id": base_id + 2,
        "inGameId": "MainQuest_002",
        "title": "The Catpital (1)",
        "royalArt": "none"
    },
    {
        "id": base_id + 3,
        "inGameId": "MainQuest_003",
        "title": "The Catpital (2)",
        "royalArt": "none"
    },
    {
        "id": base_id + 4,
        "inGameId": "MainQuest_004",
        "title": "The Dragon and the Cat",
        "royalArt": "none"
    },
    {
        "id": base_id + 5,
        "inGameId": "MainQuest_005",
        "title": "The Old Ruins",
        "royalArt": "none"
    },
    {
        "id": base_id + 6,
        "inGameId": "MainQuest_006",
        "title": "Of Sea and Rock (1)",
        "royalArt": "none"
    },
    {
        "id": base_id + 7,
        "inGameId": "MainQuest_007",
        "title": "Of Sea and Rock (2)",
        "royalArt": "none"
    },
    {
        "id": base_id + 8,
        "inGameId": "MainQuest_008",
        "title": "The Old Friend",
        "royalArt": "none"
    },
    {
        "id": base_id + 9,
        "inGameId": "MainQuest_009",
        "title": "The Dragonblood",
        "royalArt": "none"
    },
    {
        "id": base_id + 10,
        "inGameId": "MainQuest_010",
        "title": "The Dragonsbane",
        "royalArt": "none"
    },
    {
        "id": base_id + 11,
        "inGameId": "MainQuest_011",
        "title": "The Dragons Void",
        "royalArt": "none"
    },
    {
        "id": base_id + 12,
        "inGameId": "MainQuest_012",
        "title": "Epilogue",
        "royalArt": "none"
    },

    # Sanctuary Quests
    {
        "id": base_id + 13,
        "inGameId": "sanctuary_one",
        "title": "I. The Strange Charm",
        "royalArt": "none"
    },
    {
        "id": base_id + 14,
        "inGameId": "sanctuary_two",
        "title": "II. The Escape",
        "royalArt": "none"
    },
    {
        "id": base_id + 15,
        "inGameId": "sanctuary_three",
        "title": "III. The Sacrifice",
        "royalArt": "none"
    },
    {
        "id": base_id + 16,
        "inGameId": "sanctuary_four",
        "title": "IV. The Sanctuary",
        "royalArt": "none"
    },

    # Great Spirit Quests
    {
        "id": base_id + 19,
        "inGameId": "greatspirit_one",
        "title": "I. The Servant of God",
        "royalArt": "none"
    },
    {
        "id": base_id + 20,
        "inGameId": "greatspirit_two",
        "title": "II. The Offerings",
        "royalArt": "none"
    },
    {
        "id": base_id + 21,
        "inGameId": "greatspirit_three",
        "title": "III. The Prayer",
        "royalArt": "none"
    },
    {
        "id": base_id + 22,
        "inGameId": "greatspirit_four",
        "title": "IV. The Godcat, Mauth",
        "royalArt": "none"
    },

    # Kitmas Quests
    {
        "id": base_id + 23, 
        "inGameId": "kitmas_one", 
        "title": "The First Day of Kitmas", 
        "royalArt": "none"
    },
    {
        "id": base_id + 24, 
        "inGameId": "kitmas_two", 
        "title": "The Second Day of Kitmas", 
        "royalArt": "none"
    },
    {
        "id": base_id + 25, 
        "inGameId": "kitmas_three", 
        "title": "The Third Day of Kitmas", 
        "royalArt": "none"
    },
    {
        "id": base_id + 26, 
        "inGameId": "kitmas_four", 
        "title": "The Fourth Day of Kitmas", 
        "royalArt": "none"
    },
    {
        "id": base_id + 27, 
        "inGameId": "kitmas_five", 
        "title": "Mewry Kitmas!", 
        "royalArt": "none"
    },

    # Missing Quests
    {
        "id": base_id + 28, 
        "inGameId": "missing_one", 
        "title": "I. The Missing Soldiers", 
        "royalArt": "none"
    },
    {
        "id": base_id + 29, 
        "inGameId": "missing_two", 
        "title": "II. The Rescue", 
        "royalArt": "none"
    },

    # Faded King Quests
    {
        "id": base_id + 30, 
        "inGameId": "faded_king_one", 
        "title": "I. The King's Mage", 
        "royalArt": "none"
    },
    {
        "id": base_id + 31, 
        "inGameId": "faded_king_three", 
        "title": "II. The Mage Search", 
        "royalArt": "none"
    },
    {
        "id": base_id + 32, 
        "inGameId": "faded_king_four", 
        "title": "III. The Spirits", 
        "royalArt": "none"
    },
    {
        "id": base_id + 33, 
        "inGameId": "faded_king_five", 
        "title": "IV. The Lion King", 
        "royalArt": "none"
    },

    # East Quests
    {
        "id": base_id + 34, 
        "inGameId": "east_one", 
        "title": "I. The East Suspicion", 
        "royalArt": "none"
    },
    {
        "id": base_id + 35, 
        "inGameId": "east_two", 
        "title": "II. The East Shipment", 
        "royalArt": "none"
    },
    {
        "id": base_id + 36, 
        "inGameId": "east_three", 
        "title": "III. The East Escort", 
        "royalArt": "none"
    },
    {
        "id": base_id + 37, 
        "inGameId": "east_four", 
        "title": "IV. The East Catfrontation", 
        "royalArt": "none"
    },

    # Meat Quests
    {
        "id": base_id + 38, 
        "inGameId": "meatmeatmeat", 
        "title": "I. Meat Meat Meat!", 
        "royalArt": "none"
    },
    {
        "id": base_id + 39, 
        "inGameId": "red_riding_kitty", 
        "title": "II. Meatmeatmeatmeat!!", 
        "royalArt": "none"
    },
    {
        "id": base_id + 40, 
        "inGameId": "distraction", 
        "title": "III. Meat Disposal Crew", 
        "royalArt": "none"
    },
    {
        "id": base_id + 41, 
        "inGameId": "crafty_merchant", 
        "title": "IV. The Meat Seller", 
        "royalArt": "none"
    },

    # Whisperer Quests
    {
        "id": base_id + 42, 
        "inGameId": "the_whisperer_one", 
        "title": "I. The Growling Peasant", 
        "royalArt": "none"
    },
    {
        "id": base_id + 43, 
        "inGameId": "the_whisperer_two", 
        "title": "II. The Catnip Ritual", 
        "royalArt": "none"
    },
    {
        "id": base_id + 44, 
        "inGameId": "the_whisperer_three", 
        "title": "III. The Circle", 
        "royalArt": "none"
    },
    {
        "id": base_id + 45, 
        "inGameId": "the_whisperer_four", 
        "title": "IV. Fur-reedom!", 
        "royalArt": "none"
    },
    {
        "id": base_id + 46, 
        "inGameId": "the_whisperer_five", 
        "title": "V. The Whispurrer", 
        "royalArt": "none"
    },

    # Waters Quests
    {
        "id": base_id + 47, 
        "inGameId": "waters_one", 
        "title": "I. Path to Water Walking", 
        "royalArt": "none"
    },
    {
        "id": base_id + 48, 
        "inGameId": "waters_three", 
        "title": "II. The Fusion", 
        "royalArt": "none"
    },
    {
        "id": base_id + 49, 
        "inGameId": "waters_four", 
        "title": "III. Rogue Mages", 
        "royalArt": "none"
    },
    {
        "id": base_id + 50, 
        "inGameId": "waters_five", 
        "title": "IV. The Miracle", 
        "royalArt": "none"
    },

    # Mage vs Science Quests
    {#?
        "id": base_id + 51, 
        "inGameId": "magevscience_one", 
        "title": "I. The Peace Offering", 
        "royalArt": "none"
    },
    {#?
        "id": base_id + 52, 
        "inGameId": "magevscience_two", 
        "title": "II. The Blame", 
        "royalArt": "none"
    },
    {#?
        "id": base_id + 53, 
        "inGameId": "magevscience_three", 
        "title": "III. Road to Recovery", 
        "royalArt": "none"
    },

    # West Quests
    {
        "id": base_id + 54, 
        "inGameId": "west_one", 
        "title": "I. The West Investigation", 
        "royalArt": "none"
    },
    {
        "id": base_id + 55, 
        "inGameId": "west_two", 
        "title": "II. The West Heist", 
        "royalArt": "none"
    },
    {
        "id": base_id + 56, 
        "inGameId": "west_three", 
        "title": "III. The Magic Lock", 
        "royalArt": "none"
    },
    {
        "id": base_id + 57, 
        "inGameId": "west_four", 
        "title": "IV. The Revelation", 
        "royalArt": "none"
    },

    # Flíght Quests
    {
        "id": base_id + 58, 
        "inGameId": "magesold_one", 
        "title": "I. The Flying Bush", 
        "royalArt": "none"
    },
    {
        "id": base_id + 59, 
        "inGameId": "magesold_two", 
        "title": "II. The Magic Tree", 
        "royalArt": "none"
    },
    {
        "id": base_id + 60, 
        "inGameId": "magesold_three", 
        "title": "III. The Cult", 
        "royalArt": "none"
    },
    {
        "id": base_id + 61, 
        "inGameId": "magesold_four", 
        "title": "IV. Dragonflight", 
        "royalArt": "none"
    },

    # Dark Past Quests
    {
        "id": base_id + 62, 
        "inGameId": "darkpast_one", 
        "title": "I. The Missing Pages", 
        "royalArt": "none"
    },
    {
        "id": base_id + 63, 
        "inGameId": "darkpast_two", 
        "title": "II. The Protected Pages", 
        "royalArt": "none"
    },
    {
        "id": base_id + 64, 
        "inGameId": "darkpast_three", 
        "title": "III. The Runaway Archeologist", 
        "royalArt": "none"
    },
    {
        "id": base_id + 65, 
        "inGameId": "darkpast_four", 
        "title": "IV. The Treasure", 
        "royalArt": "none"
    },

    # Blacksmith Quests
    {
        "id": base_id + 66, 
        "inGameId": "blacksmith_assistance", 
        "title": "I. Blacksmith Assistance", 
        "royalArt": "none"
    },
    {
        "id": base_id + 67, 
        "inGameId": "blacksmith_apprentice", 
        "title": "II. Blacksmith Apprentice", 
        "royalArt": "none"
    },
    {
        "id": base_id + 68, 
        "inGameId": "blacksmith_journeyman", 
        "title": "III. Blacksmith Journeyman", 
        "royalArt": "none"
    },
    {
        "id": base_id + 69, 
        "inGameId": "blacksmith_master", 
        "title": "IV. Blacksmith Master", 
        "royalArt": "none"
    },

    # Misc Quests
    {#?
        "id": base_id + 70, 
        "inGameId": "wyvern_attack", 
        "title": "The Dragon Worshippers", 
        "royalArt": "none"
    },
    {
        "id": base_id + 71, 
        "inGameId": "the_heirloom", 
        "title": "The Heirloom Armor", 
        "royalArt": "none"
    },
    {
        "id": base_id + 72, 
        "inGameId": "furbidden_mystery", 
        "title": "The Furbidden History", 
        "royalArt": "none"
    },
    {
        "id": base_id + 73, 
        "inGameId": "golden_key", 
        "title": "The Golden Key", 
        "royalArt": "none"
    },
    {
        "id": base_id + 74, 
        "inGameId": "ultimate_dragonsbane", 
        "title": "The Ultimate Dragonsbane", 
        "royalArt": "none"
    },
    {
        "id": base_id + 75, 
        "inGameId": "pawtato_one", 
        "title": "The Pawtato Mystery", 
        "royalArt": "none"
    },
    {
        "id": base_id + 76, 
        "inGameId": "advertising_one", 
        "title": "Everyone's invited!", 
        "royalArt": "none"
    },
    {
        "id": base_id + 77, 
        "inGameId": "slashy_one", 
        "title": "The Forgotten Hero", 
        "royalArt": "none"
    },
    {#?
        "id": base_id + 78, 
        "inGameId": "TutorialQuest_001", 
        "title": "Beginnings", 
        "royalArt": "none"
    },

    # Catnip Cure Quests
    {
        "id": base_id + 79, 
        "inGameId": "catnip_cure_A", 
        "title": "I. The Catnip Cure", 
        "royalArt": "none"
    },
    {
        "id": base_id + 80, 
        "inGameId": "catnip_cure_B", 
        "title": "I. The Catnip Cure...again", 
        "royalArt": "none"
    },
    {
        "id": base_id + 81, 
        "inGameId": "knightmare_A", 
        "title": "II. The Knightmare", 
        "royalArt": "none"
    },
    {
        "id": base_id + 82, 
        "inGameId": "knightmare_B", 
        "title": "II. The Knightmare... again", 
        "royalArt": "none"
    },
    {
        "id": base_id + 83, 
        "inGameId": "book_A", 
        "title": "III. The Book", 
        "royalArt": "none"
    },
    {
        "id": base_id + 84, 
        "inGameId": "book_B", 
        "title": "III. The Book...again", 
        "royalArt": "none"
    },
    {
        "id": base_id + 85, 
        "inGameId": "resolution_A", 
        "title": "IV. The Twin Resolution", 
        "royalArt": "none"
    }
]