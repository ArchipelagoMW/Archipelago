from BaseClasses import LocationProgressType
from typing import List, TypedDict

class Location(TypedDict):
    inGameId: str
    name: str
    art: str
    progress_type: LocationProgressType
    hasFist: bool

templeLocations: List[Location] = [
    {
        "inGameId": "flamepurr",
        "name": "The Catpital Temple (Flamepurr)",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "healing_paw",
        "name": "Bermewda's Triangle Temple (Healing Paw)",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "lightnyan",
        "name": "East Pawt Temple (Lightnyan)",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "cattrap",
        "name": "Windmew City Temple (Cattrap)",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "purrserk",
        "name": "South Pawt Temple (Purrserk)",
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "astropaw",
        "name": "Death Isle Temple (Astropaw)",
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "freezepaw",
        "name": "Felingard Lake Temple (Freezepaw)",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    }
]

questLocations: List[Location] = [
    # Main Quests
    {
        "inGameId": "MainQuest_001_PC",
        "name": "A Whole New World",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "MainQuest_002",
        "name": "The Catpital (1)",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "MainQuest_003",
        "name": "The Catpital (2)",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "MainQuest_004",
        "name": "The Dragon and the Cat",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "MainQuest_005",
        "name": "The Old Ruins",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_006",
        "name": "Of Sea and Rock (1)",
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_007",
        "name": "Of Sea and Rock (2)",
        "art": "both",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_008",
        "name": "The Old Friend",
        "art": "both",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_009",
        "name": "The Dragonblood",
        "art": "both",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_010",
        "name": "The Dragonsbane",
        "art": "both",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_011",
        "name": "The Dragons Void",
        "art": "both",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_012",
        "name": "Epilogue",
        "art": "both",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },

    # Sanctuary Quests
    {
        "inGameId": "sanctuary_one",
        "name": "I. The Strange Charm",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "sanctuary_two",
        "name": "II. The Escape",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "sanctuary_three",
        "name": "III. The Sacrifice",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "sanctuary_four",
        "name": "IV. The Sanctuary",
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },

    # Great Spirit Quests
    {
        "inGameId": "greatspirit_one",
        "name": "I. The Servant of God",
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "greatspirit_two",
        "name": "II. The Offerings",
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "greatspirit_three",
        "name": "III. The Prayer",
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "greatspirit_four",
        "name": "IV. The Godcat, Mauth",
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },

    # Kitmas Quests
    {
        "inGameId": "kitmas_one", 
        "name": "The First Day of Kitmas", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "kitmas_two", 
        "name": "The Second Day of Kitmas", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "kitmas_three", 
        "name": "The Third Day of Kitmas", 
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "kitmas_four", 
        "name": "The Fourth Day of Kitmas", 
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "kitmas_five", 
        "name": "Mewry Kitmas!", 
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },

    # Missing Quests
    {
        "inGameId": "missing_one", 
        "name": "I. The Missing Soldiers", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "missing_two", 
        "name": "II. The Rescue", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },

    # Faded King Quests
    {
        "inGameId": "faded_king_one", 
        "name": "I. The King's Mage", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "faded_king_three", 
        "name": "II. The Mage Search", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "faded_king_four", 
        "name": "III. The Spirits", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "faded_king_five", 
        "name": "IV. The Lion King", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },

    # East Quests
    {
        "inGameId": "east_one", 
        "name": "I. The East Suspicion", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "east_two", 
        "name": "II. The East Shipment", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "east_three", 
        "name": "III. The East Escort", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "east_four", 
        "name": "IV. The East Catfrontation", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },

    # Meat Quests
    {
        "inGameId": "meatmeatmeat", 
        "name": "I. Meat Meat Meat!", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "red_riding_kitty", 
        "name": "II. Meatmeatmeatmeat!!", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "distraction", 
        "name": "III. Meat Disposal Crew", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "crafty_merchant", 
        "name": "IV. The Meat Seller", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },

    # Whisperer Quests
    {
        "inGameId": "the_whisperer_one", 
        "name": "I. The Growling Peasant", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "the_whisperer_two", 
        "name": "II. The Catnip Ritual", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "the_whisperer_three", 
        "name": "III. The Circle", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "the_whisperer_four", 
        "name": "IV. Fur-reedom!", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "the_whisperer_five", 
        "name": "V. The Whispurrer", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },

    # Waters Quests
    {
        "inGameId": "waters_one", 
        "name": "I. Path to Water Walking", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "waters_three", 
        "name": "II. The Fusion", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "waters_four", 
        "name": "III. Rogue Mages", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "waters_five", 
        "name": "IV. The Miracle", 
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },

    # West Quests
    {
        "inGameId": "west_one", 
        "name": "I. The West Investigation", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "west_two", 
        "name": "II. The West Heist", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "west_three", 
        "name": "III. The Magic Lock", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "west_four", 
        "name": "IV. The Revelation", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },

    # Flight Quests
    {
        "inGameId": "magesold_one", 
        "name": "I. The Flying Bush", 
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "magesold_two", 
        "name": "II. The Magic Tree", 
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "magesold_three", 
        "name": "III. The Cult", 
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "magesold_four", 
        "name": "IV. Dragonflight", 
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },

    # Dark Past Quests
    {
        "inGameId": "darkpast_one", 
        "name": "I. The Missing Pages", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "darkpast_two", 
        "name": "II. The Protected Pages", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "darkpast_three", 
        "name": "III. The Runaway Archeologist", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "darkpast_four", 
        "name": "IV. The Treasure", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },

    # Blacksmith Quests
    {
        "inGameId": "blacksmith_assistance", 
        "name": "I. Blacksmith Assistance", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "blacksmith_apprentice", 
        "name": "II. Blacksmith Apprentice", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "blacksmith_journeyman", 
        "name": "III. Blacksmith Journeyman", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "blacksmith_master", 
        "name": "IV. Blacksmith Master", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },

    # Misc Quests
    {
        "inGameId": "wyvern_attack", 
        "name": "The Dragon Worshippers", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "the_heirloom", 
        "name": "The Heirloom Armor", 
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": True
    },
    {
        "inGameId": "furbidden_mystery", 
        "name": "The Furbidden History", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "golden_key", 
        "name": "The Golden Key", 
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "ultimate_dragonsbane", 
        "name": "The Ultimate Dragonsbane", 
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "pawtato_one", 
        "name": "The Pawtato Mystery", 
        "art": "water",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "advertising_one", 
        "name": "Everyone's invited!", 
        "art": "flight",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "slashy_one", 
        "name": "The Forgotten Hero", 
        "art": "either",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },

    # Catnip Cure Quests
    {
        "inGameId": "catnip_cure_A", 
        "name": "I. The Catnip Cure", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "catnip_cure_B", 
        "name": "I. The Catnip Cure...again", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "knightmare_A", 
        "name": "II. The Knightmare", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "knightmare_B", 
        "name": "II. The Knightmare... again", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "book_A", 
        "name": "III. The Book", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "book_B", 
        "name": "III. The Book...again", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    },
    {
        "inGameId": "resolution_A", 
        "name": "IV. The Twin Resolution", 
        "art": "none",
        "progress_type": LocationProgressType.DEFAULT,
        "hasFist": False
    }
]