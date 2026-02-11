import json
from pathlib import Path

royal_arts = [
    {"name": "Royal Art of Water Walking", "inGameId": "art.water"},
    {"name": "Royal Art of Flight", "inGameId": "art.flight"},
]

skills = [
    {"name": "Flamepurr", "inGameId": "skill.flamepurr"},
    {"name": "Healing Paw", "inGameId": "skill.healing_paw"},
    {"name": "Lightnyan", "inGameId": "skill.lightnyan"},
    {"name": "Cattrap", "inGameId": "skill.cattrap"},
    {"name": "Purrserk", "inGameId": "skill.purrserk"},
    {"name": "Astropaw", "inGameId": "skill.astropaw"},
    {"name": "Freezepaw", "inGameId": "skill.freezepaw"},
]

prog_skills = [
    {"name": "Progressive Flamepurr", "inGameId": "skill.flamepurr"},
    {"name": "Progressive Healing Paw", "inGameId": "skill.healing_paw"},
    {"name": "Progressive Lightnyan", "inGameId": "skill.lightnyan"},
    {"name": "Progressive Cattrap", "inGameId": "skill.cattrap"},
    {"name": "Progressive Purrserk", "inGameId": "skill.purrserk"},
    {"name": "Progressive Astropaw", "inGameId": "skill.astropaw"},
    {"name": "Progressive Freezepaw", "inGameId": "skill.freezepaw"},
]

prog_skill_uprades = [
    {"name": "Progressive Flamepurr Upgrade", "inGameId": "skillupgrade.flamepurr"},
    {"name": "Progressive Healing Paw Upgrade", "inGameId": "skillupgrade.healing_paw"},
    {"name": "Progressive Lightnyan Upgrade", "inGameId": "skillupgrade.lightnyan"},
    {"name": "Progressive Cattrap Upgrade", "inGameId": "skillupgrade.cattrap"},
    {"name": "Progressive Purrserk Upgrade", "inGameId": "skillupgrade.purrserk"},
    {"name": "Progressive Astropaw Upgrade", "inGameId": "skillupgrade.astropaw"},
    {"name": "Progressive Freezepaw Upgrade", "inGameId": "skillupgrade.freezepaw"},
]

prog_magic_levels = [
    {"name": "Progressive Magic Level", "inGameId": "magiclevel.magiclevel"},
]

misc = [
    # Golden Key
    {"name": "Golden Key", "inGameId": "key.golden"},
]

fillers = [
    # Gold
    {"name": "50 Gold", "inGameId": "gold.50"},
    {"name": "500 Gold", "inGameId": "gold.500"},
    {"name": "750 Gold", "inGameId": "gold.750"},
    {"name": "1000 Gold", "inGameId": "gold.1000"},
    {"name": "5000 Gold", "inGameId": "gold.5000"},

    # Exp
    {"name": "500 Exp", "inGameId": "exp.500"},
    {"name": "1000 Exp", "inGameId": "exp.1000"},
    {"name": "5000 Exp", "inGameId": "exp.5000"},
    {"name": "7500 Exp", "inGameId": "exp.7500"},
    {"name": "10K Exp", "inGameId": "exp.10000"},
    {"name": "20K Exp", "inGameId": "exp.20000"},
]


monumentLocations = [
    {
        "inGameId": "MonumentTrigger_Catpital",
        "name": "Monument by The Catpital",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_PussPlains",
        "name": "Monument in Puss Plains",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_TwinPeaks",
        "name": "Monument below The Furbidden Fields",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_SouthPoint",
        "name": "Monument at South Point",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_EastPawt",
        "name": "Monument along East Pawt River",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_HillyHills_01",
        "name": "Monument by Hilly Hills Coast",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_HillyHills_02",
        "name": "Monument by The Unknown Head",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_MountainPass",
        "name": "Monument above Mountain Pass",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_Windmew",
        "name": "Monument by Windmew Lake",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_NorthPoint",
        "name": "Monument at North Point",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_Purrning",
        "name": "Monument by Winters Edge",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_OldMaster",
        "name": "Monument on Old Master's Island",
        "art": "either",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_KeyIsland",
        "name": "Monument on Key Island",
        "art": "either",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_MonsterIsle",
        "name": "Monument on Monster Isle",
        "art": "either",
        "hasFist": False
    },
    {
        "inGameId": "MonumentTrigger_DeathIsle",
        "name": "Monument on Death Isle",
        "art": "either",
        "hasFist": False
    }
]

templeLocations = [
    {
        "inGameId": "flamepurr",
        "name": "The Catpital Temple (Flamepurr)",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "healing_paw",
        "name": "Bermewda's Triangle Temple (Healing Paw)",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "lightnyan",
        "name": "East Pawt Temple (Lightnyan)",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "cattrap",
        "name": "Windmew City Temple (Cattrap)",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "purrserk",
        "name": "South Pawt Temple (Purrserk)",
        "art": "either",
        "hasFist": False
    },
    {
        "inGameId": "astropaw",
        "name": "Death Isle Temple (Astropaw)",
        "art": "either",
        "hasFist": False
    },
    {
        "inGameId": "freezepaw",
        "name": "Felingard Lake Temple (Freezepaw)",
        "art": "none",
        "hasFist": False
    }
]

questLocations = [
    # Main Quests
    {
        "inGameId": "MainQuest_001_PC",
        "name": "A Whole New World",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MainQuest_002",
        "name": "The Catpital (1)",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MainQuest_003",
        "name": "The Catpital (2)",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MainQuest_004",
        "name": "The Dragon and the Cat",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "MainQuest_005",
        "name": "The Old Ruins",
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_006",
        "name": "Of Sea and Rock (1)",
        "art": "water",
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_007",
        "name": "Of Sea and Rock (2)",
        "art": "both",
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_008",
        "name": "The Old Friend",
        "art": "both",
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_009",
        "name": "The Dragonblood",
        "art": "both",
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_010",
        "name": "The Dragonsbane",
        "art": "both",
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_011",
        "name": "The Dragons Void",
        "art": "both",
        "hasFist": True
    },
    {
        "inGameId": "MainQuest_012",
        "name": "Epilogue",
        "art": "both",
        "hasFist": True
    },

    # Sanctuary Quests
    {
        "inGameId": "sanctuary_one",
        "name": "I. The Strange Charm",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "sanctuary_two",
        "name": "II. The Escape",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "sanctuary_three",
        "name": "III. The Sacrifice",
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "sanctuary_four",
        "name": "IV. The Sanctuary",
        "art": "none",
        "hasFist": False
    },

    # Great Spirit Quests
    {
        "inGameId": "greatspirit_one",
        "name": "I. The Servant of God",
        "art": "either",
        "hasFist": False
    },
    {
        "inGameId": "greatspirit_two",
        "name": "II. The Offerings",
        "art": "water",
        "hasFist": False
    },
    {
        "inGameId": "greatspirit_three",
        "name": "III. The Prayer",
        "art": "water",
        "hasFist": False
    },
    {
        "inGameId": "greatspirit_four",
        "name": "IV. The Godcat, Mauth",
        "art": "water",
        "hasFist": False
    },

    # Kitmas Quests
    {
        "inGameId": "kitmas_one", 
        "name": "The First Day of Kitmas", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "kitmas_two", 
        "name": "The Second Day of Kitmas", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "kitmas_three", 
        "name": "The Third Day of Kitmas", 
        "art": "water",
        "hasFist": False
    },
    {
        "inGameId": "kitmas_four", 
        "name": "The Fourth Day of Kitmas", 
        "art": "water",
        "hasFist": False
    },
    {
        "inGameId": "kitmas_five", 
        "name": "Mewry Kitmas!", 
        "art": "water",
        "hasFist": False
    },

    # Missing Quests
    {
        "inGameId": "missing_one", 
        "name": "I. The Missing Soldiers", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "missing_two", 
        "name": "II. The Rescue", 
        "art": "none",
        "hasFist": False
    },

    # Faded King Quests
    {
        "inGameId": "faded_king_one", 
        "name": "I. The King's Mage", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "faded_king_three", 
        "name": "II. The Mage Search", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "faded_king_four", 
        "name": "III. The Spirits", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "faded_king_five", 
        "name": "IV. The Lion King", 
        "art": "none",
        "hasFist": True
    },

    # East Quests
    {
        "inGameId": "east_one", 
        "name": "I. The East Suspicion", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "east_two", 
        "name": "II. The East Shipment", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "east_three", 
        "name": "III. The East Escort", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "east_four", 
        "name": "IV. The East Catfrontation", 
        "art": "none",
        "hasFist": True
    },

    # Meat Quests
    {
        "inGameId": "meatmeatmeat", 
        "name": "I. Meat Meat Meat!", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "red_riding_kitty", 
        "name": "II. Meatmeatmeatmeat!!", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "distraction", 
        "name": "III. Meat Disposal Crew", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "crafty_merchant", 
        "name": "IV. The Meat Seller", 
        "art": "none",
        "hasFist": True
    },

    # Whisperer Quests
    {
        "inGameId": "the_whisperer_one", 
        "name": "I. The Growling Peasant", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "the_whisperer_two", 
        "name": "II. The Catnip Ritual", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "the_whisperer_three", 
        "name": "III. The Circle", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "the_whisperer_four", 
        "name": "IV. Fur-reedom!", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "the_whisperer_five", 
        "name": "V. The Whispurrer", 
        "art": "none",
        "hasFist": False
    },

    # Waters Quests
    {
        "inGameId": "waters_one", 
        "name": "I. Path to Water Walking", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "waters_three", 
        "name": "II. The Fusion", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "waters_four", 
        "name": "III. Rogue Mages", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "waters_five", 
        "name": "IV. The Miracle", 
        "art": "water",
        "hasFist": False
    },

    # West Quests
    {
        "inGameId": "west_one", 
        "name": "I. The West Investigation", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "west_two", 
        "name": "II. The West Heist", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "west_three", 
        "name": "III. The Magic Lock", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "west_four", 
        "name": "IV. The Revelation", 
        "art": "none",
        "hasFist": True
    },

    # Flight Quests
    {
        "inGameId": "magesold_one", 
        "name": "I. The Flying Bush", 
        "art": "either",
        "hasFist": True
    },
    {
        "inGameId": "magesold_two", 
        "name": "II. The Magic Tree", 
        "art": "either",
        "hasFist": True
    },
    {
        "inGameId": "magesold_three", 
        "name": "III. The Cult", 
        "art": "either",
        "hasFist": True
    },
    {
        "inGameId": "magesold_four", 
        "name": "IV. Dragonflight", 
        "art": "either",
        "hasFist": True
    },

    # Dark Past Quests
    {
        "inGameId": "darkpast_one", 
        "name": "I. The Missing Pages", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "darkpast_two", 
        "name": "II. The Protected Pages", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "darkpast_three", 
        "name": "III. The Runaway Archeologist", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "darkpast_four", 
        "name": "IV. The Treasure", 
        "art": "none",
        "hasFist": True
    },

    # Blacksmith Quests
    {
        "inGameId": "blacksmith_assistance", 
        "name": "I. Blacksmith Assistance", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "blacksmith_apprentice", 
        "name": "II. Blacksmith Apprentice", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "blacksmith_journeyman", 
        "name": "III. Blacksmith Journeyman", 
        "art": "none",
        "hasFist": True
    },
    {
        "inGameId": "blacksmith_master", 
        "name": "IV. Blacksmith Master", 
        "art": "none",
        "hasFist": True
    },

    # Misc Quests
    {
        "inGameId": "wyvern_attack", 
        "name": "The Dragon Worshippers", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "the_heirloom", 
        "name": "The Heirloom Armor", 
        "art": "water",
        "hasFist": True
    },
    {
        "inGameId": "furbidden_mystery", 
        "name": "The Furbidden History", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "golden_key", 
        "name": "The Golden Key", 
        "art": "either",
        "hasFist": False
    },
    {
        "inGameId": "ultimate_dragonsbane", 
        "name": "The Ultimate Dragonsbane", 
        "art": "water",
        "hasFist": False
    },
    {
        "inGameId": "pawtato_one", 
        "name": "The Pawtato Mystery", 
        "art": "water",
        "hasFist": False
    },
    {
        "inGameId": "advertising_one", 
        "name": "Everyone's invited!", 
        "art": "flight",
        "hasFist": False
    },
    {
        "inGameId": "slashy_one", 
        "name": "The Forgotten Hero", 
        "art": "either",
        "hasFist": False
    },

    # Catnip Cure Quests
    {
        "inGameId": "catnip_cure_A", 
        "name": "I. The Catnip Cure", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "catnip_cure_B", 
        "name": "I. The Catnip Cure...again", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "knightmare_A", 
        "name": "II. The Knightmare", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "knightmare_B", 
        "name": "II. The Knightmare... again", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "book_A", 
        "name": "III. The Book", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "book_B", 
        "name": "III. The Book...again", 
        "art": "none",
        "hasFist": False
    },
    {
        "inGameId": "resolution_A", 
        "name": "IV. The Twin Resolution", 
        "art": "none",
        "hasFist": False
    }
]

# All items in the exact order they should be loaded
all_items = fillers + royal_arts + skills + prog_skills + prog_skill_uprades + prog_magic_levels + misc
all_locations = questLocations + templeLocations + monumentLocations

# Map: numeric ID → item

item_id_dict = {}
current_id = 1

for item in all_items:
    item_id_dict[item["name"]] = current_id
    current_id += 1

location_id_dict = {}
current_id = 1

for location in all_locations:
    location_id_dict[location["name"]] = current_id
    current_id += 1


item_data = [
    {"name": item["name"], "id": item["inGameId"]}
    for item in all_items
]

location_data = [
    {"name": location["name"], "id": location["inGameId"]}
    for location in all_locations
]
    
# Output path (same folder as this script)
location_output_file = Path(__file__).parent / "location_to_ids.json"
item_output_file = Path(__file__).parent / "items_to_ids.json"
locationdata_output_file = Path(__file__).parent / "location_data.json"
itemdata_output_file = Path(__file__).parent / "item_data.json"

# Write JSON with indentation
with location_output_file.open("w", encoding="utf-8") as f:
    json.dump(location_id_dict, f, indent=2, ensure_ascii=False)

print(f"JSON file created at {location_output_file}")

with item_output_file.open("w", encoding="utf-8") as f:
    json.dump(item_id_dict, f, indent=2, ensure_ascii=False)

print(f"JSON file created at {item_output_file}")



with locationdata_output_file.open("w", encoding="utf-8") as f:
    json.dump(location_data, f, indent=2, ensure_ascii=False)

print(f"JSON file created at {locationdata_output_file}")

with itemdata_output_file.open("w", encoding="utf-8") as f:
    json.dump(item_data, f, indent=2, ensure_ascii=False)

print(f"JSON file created at {itemdata_output_file}")