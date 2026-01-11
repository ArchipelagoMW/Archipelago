LANAYRU_REQUIREMENTS = {
    "Lanayru Mine - Landing": {
        "hint_region": "Lanayru Mine",
        "macros": {
            "Lanayru Mine Ancient Flower Farming": "Can Hit Timeshift Stone",
            "Goddess Cube at Lanayru Mine Entrance": "Has Goddess Sword",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Clawshot Path to Caves": "Clawshots",
            "Pass Statues in Mine": (
                "Can Hit Timeshift Stone "
                "& (Bomb Bag | Has Hook Beetle)"
            ),
        },
        "locations": {
            "Chest behind First Landing": "Clawshots",
            "Chest near First Timeshift Stone": "Can Hit Timeshift Stone",
            "Chest behind Statue": "Can Hit Timeshift Stone & (Bomb Bag | Has Hook Beetle)",
        },
    },
    "Lanayru Mine - Door to Caves": {
        "hint_region": "Lanayru Mine",
        "exits": {
            "Clawshot Path to Mine": "Clawshots",
            "Door to Caves": "Nothing",
        },
        "locations": {},
    },
    "Lanayru Mine - Ending": {
        "hint_region": "Lanayru Mine",
        "exits": {
            "Pass Statues in Mine": "Bomb Bag | Has Hook Beetle",
            "Minecart Ride out of Mine": "Nothing",
        },
        "locations": {
            "Chest at the End of Mine": "Nothing",
        },
    },
    "Lanayru Desert - Desert Entry": {
        "hint_region": "Lanayru Desert",
        "macros": {
            "Can Retrieve Party Wheel": "Bomb Bag & Scrapper",
            "Lanayru Desert Ancient Flower Farming": "Bomb Bag",
            "Goddess Cube near Caged Robot": "Has Goddess Sword & (Clawshots | Upgraded Skyward Strike)",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Minecart Ride out of Desert": "Bomb Bag & can_reach_region Lanayru Mine - Ending",
            "Sand Oasis": "Has Hook Beetle | Clawshots",
            "Stone Cache": "Clawshots | option_lmf_open",
        },
        "locations": {
            "Chest near Party Wheel": "Bomb Bag",
            "Chest near Caged Robot": "Nothing",
            "Rescue Caged Robot": "Bomb Bag | Has Hook Beetle",
        },
    },
    "Lanayru Desert - Sand Oasis": {
        "hint_region": "Lanayru Desert",
        "macros": {
            "Goddess Cube in Sand Oasis": "Has Goddess Sword",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Desert Entry": "Nothing",
            "Path to Temple of Time": "Nothing",
            "Raised Entrance to Caves": "Clawshots",
        },
        "locations": {
            "Chest near Sand Oasis": "Clawshots",
        },
    },
    "Lanayru Desert - Higher Ledge in Sand Oasis": {
        "hint_region": "Lanayru Desert",
        "exits": {
            "Sand Oasis": "Nothing",
            "Path to Caves": "Nothing",
        },
        "locations": {},
    },
    "Lanayru Desert - Temple of Time - Desert Gorge": {
        "hint_region": "Lanayru Desert",
        "exits": {
            "Fly to Sky": "Nothing",
            "Path to Sand Oasis": "Nothing",
            "Minecart through Tree Root": "Has Hook Beetle",
        },
        "locations": {},
    },
    "Lanayru Desert - Temple of Time - Temple": {
        "hint_region": "Lanayru Desert",
        "macros": {
            "Goddess Cube at Ride near Temple of Time": "Has Goddess Sword & Distance Activator",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Minecart to Desert Gorge": "Distance Activator",
            "Path to North Desert": "Distance Activator",
        },
        "locations": {},
    },
    "Lanayru Desert - North Desert": {
        "hint_region": "Lanayru Desert",
        "macros": {
            "Can Raise LMF": (
                "option_lmf_open "
                "| (option_lmf_main_node & Has Practice Sword) "
                "| Can Activate Nodes"
            ),
            "Can Activate Nodes": (
                "Can Activate Fire Node & Can Activate Lightning Node & Can Activate Water Node"
            ),
            "Can Activate Water Node": "Bomb Bag & Has Practice Sword",
            "Lanayru Desert Ancient Flower Farming near Main Node": "Bomb Bag | Has Hook Beetle",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Path to Temple of Time": "Nothing",
            "Stone Cache": "Nothing",
            "Door to Lightning Node": "Nothing",
            "Dungeon Entrance in Lanayru Desert": "Can Raise LMF",
            "Trial Gate in Lanayru Desert": "Goddess's Harp & Nayru's Wisdom",
        },
        "locations": {
            "Chest on Platform near Lightning Node": "Clawshots",
            "Chest on top of Lanayru Mining Facility": "Can Raise LMF",
        },
    },
    "Lanayru Desert - Stone Cache": {
        "hint_region": "Lanayru Desert",
        "macros": {
            "Goddess Cube in Secret Passageway": (
                "Has Goddess Sword & Clawshots & Bomb Bag"
            ),
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Desert Entry": "Nothing",
            "North Desert": "Nothing",
            "Door to Fire Node": "Nothing",
        },
        "locations": {
            "Chest on Platform near Fire Node": "Clawshots",
            "Secret Passageway Chest": "Bomb Bag | Has Tough Beetle"
        },
    },
    "Lanayru Desert - Fire Node": {
        "hint_region": "Lanayru Desert",
        "macros": {
            "Can Activate Fire Node": (
                "Bomb Bag "
                "& Has Hook Beetle "
                "& Can Defeat Ampilus "
                "& Has Practice Sword"
            ),
        },
        "exits": {
            "Exit Fire Node": "Nothing",
        },
        "locations": {
            "Fire Node - Shortcut Chest": "Can Defeat Ampilus",
            "Fire Node - First Small Chest": "Bomb Bag",
            "Fire Node - Second Small Chest": "Bomb Bag",
            "Fire Node - Left Ending Chest": "Bomb Bag & Has Hook Beetle & Can Defeat Ampilus",
            "Fire Node - Right Ending Chest": "Bomb Bag & Has Hook Beetle & Can Defeat Ampilus",
        },
    },
    "Lanayru Desert - Lightning Node": {
        "hint_region": "Lanayru Desert",
        "macros": {
            "Can Activate Lightning Node": "Bomb Bag & Has Practice Sword",
        },
        "exits": {
            "Exit Lightning Node": "Nothing",
        },
        "locations": {
            "Lightning Node - First Chest": "Bomb Bag",
            "Lightning Node - Second Chest": "Bomb Bag",
            "Lightning Node - Raised Chest near Generator": (
                "Bomb Bag & (Has Beetle | Has Bow)"
            )
        },
    },
    "Lanayru Caves - Caves": {
        "hint_region": "Lanayru Caves",
        "exits": {
            "North Exit": "Nothing",
            "East Exit": "Nothing",
            "South Exit past Crawlspace": "Nothing",
            "West Exit by Clawshot Target": "Clawshots & Lanayru Caves Small Key",
        },
        "locations": {
            "Chest": "Nothing",
            "Golo's Gift": "Nothing",
        },
    },
    "Lanayru Caves - Past Locked Door": {
        "hint_region": "Lanayru Caves",
        "exits": {
            "Path away from Door": "Nothing",
            "Through Door": "Lanayru Caves Small Key"
        },
        "locations": {},
    },
    "Lanayru Caves - Past Crawlspace": {
        "hint_region": "Lanayru Caves",
        "exits": {
            "Path away from Crawlspace": "Nothing",
            "Through Crawlspace": "Bomb Bag",
        },
        "locations": {},
    },
    "Lanayru Gorge - Gorge": {
        "hint_region": "Lanayru Gorge",
        "macros": {
            "Lanayru Gorge Ancient Flower Farming": "Can Hit Timeshift Stone & Gust Bellows",
            "Goddess Cube in Lanayru Gorge": "Has Goddess Sword & Can Hit Timeshift Stone",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Path to Caves": "Nothing",
        },
        "locations": {
            "Thunder Dragon's Reward": "Can Hit Timeshift Stone & Life Tree Fruit",
            "Item on Pillar": "Has Beetle",
            "Digging Spot": (
                "Can Hit Timeshift Stone & Gust Bellows & Has Digging Mitts"
            ),
        },
    },
    "Lanayru Sand Sea - Door to Caves": {
        "hint_region": "Lanayru Sand Sea",
        "exits": {
            "Clawshot Path to Harbor": "Clawshots",
            "Door to Caves": "Lanayru Caves Small Key",
        },
        "locations": {
            "Ancient Harbour - Rupee on First Pillar": "Has Beetle",
            "Ancient Harbour - Left Rupee on Entrance Crown": "Has Quick Beetle",
            "Ancient Harbour - Right Rupee on Entrance Crown": "Has Quick Beetle",
        },
    },
    "Lanayru Sand Sea - Ancient Harbor": {
        "hint_region": "Lanayru Sand Sea",
        "macros": {
            "Goddess Cube in Ancient Harbor": "Has Goddess Sword & Clawshots",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Clawshot Path to Caves": "Clawshots",
            "Boat to Sea": "Can Hit Timeshift Stone",
        },
        "locations": {},
    },
    "Lanayru Sand Sea - Sea": {
        "hint_region": "Lanayru Sand Sea",
        "exits": {
            "Dock at Ancient Harbor": "Nothing",
            "Dock at Skipper's Retreat": "Nothing",
            "Dock at Shipyard": "Nothing",
            "Dock at Pirate Stronghold": "Nothing",
            "Dungeon Entrance in Lanayru Sand Sea": "Sea Chart & Has Practice Sword",
        },
        "locations": {},
    },
    "Lanayru Sand Sea - Skipper's Retreat - Dock": {
        "hint_region": "Lanayru Sand Sea",
        "exits": {
            "Fly to Sky": "Nothing",
            "Boat to Sea": "Nothing",
            "After Rock": "Clawshots & (Bomb Bag | Has Hook Beetle)",
        },
        "locations": {},
    },
    "Lanayru Sand Sea - Skipper's Retreat - After Rock": {
        "hint_region": "Lanayru Sand Sea",
        "macros": {
            "Goddess Cube in Skipper's Retreat": "Has Goddess Sword & Clawshots",
        },
        "exits": {
            "Dock": "Nothing", # Zipline
            "Top of Skipper's Retreat": (
                "Whip & Clawshots & (Has Slingshot | Has Beetle | Has Bow)"
            ),
        },
        "locations": {
            "Skipper's Retreat - Chest after Moblin": "Nothing",
        },
    },
    "Lanayru Sand Sea - Skipper's Retreat - Top of Skipper's Retreat": {
        "hint_region": "Lanayru Sand Sea",
        "exits": {
            "Shack": "Clawshots",
        },
        "locations": {
            "Skipper's Retreat - Chest on top of Cacti Pillar": "Clawshots",
        },
    },
    "Lanayru Sand Sea - Skipper's Retreat - Shack": {
        "hint_region": "Lanayru Sand Sea",
        "exits": {
            "Top of Skipper's Retreat": "Clawshots",
            "After Rock": "Nothing", # Jump down
            "Skydive": "Nothing",
        },
        "locations": {
            "Skipper's Retreat - Chest in Shack": "Gust Bellows",
        },
    },
    "Lanayru Sand Sea - Skipper's Retreat - Skydive": {
        "hint_region": "Lanayru Sand Sea",
        "exits": {
            "Dock": "Clawshots",
        },
        "locations": {
            "Skipper's Retreat - Skydive Chest": "Nothing",
        },
    },
    "Lanayru Sand Sea - Shipyard": {
        "hint_region": "Lanayru Sand Sea",
        "exits": {
            "Fly to Sky": "Nothing",
            "Boat to Sea": "Nothing",
        },
        "locations": {
            "Rickety Coaster -- Heart Stopping Track in 1'05": (
                "Gust Bellows & Can Defeat Moldarachs"
            ),
        },
    },
    "Lanayru Sand Sea - Pirate Stronghold": {
        "hint_region": "Lanayru Sand Sea",
        "macros": {
            "Can Open Pirate Stronghold": "Can Defeat Beamos & Can Defeat Armos",
            "Pirate Stronghold Ancient Flower Farming": "Nothing",
            "Goddess Cube in Pirate Stronghold": (
                "Has Goddess Sword & Clawshots & Can Open Pirate Stronghold"
            ),
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Boat to Sea": "Nothing",
        },
        "locations": {
            "Pirate Stronghold - Rupee on East Sea Pillar": "Has Quick Beetle",
            "Pirate Stronghold - Rupee on West Sea Pillar": "Has Quick Beetle",
            "Pirate Stronghold - Rupee on Bird Statue Pillar or Nose": "Has Quick Beetle",
            "Pirate Stronghold - First Chest": "Nothing",
            "Pirate Stronghold - Second Chest": "Nothing",
            "Pirate Stronghold - Third Chest": "Nothing",
        },
    },
    "Lanayru Silent Realm": {
        "hint_region": "Lanayru Silent Realm",
        "exits": {
            "Trial Gate": "Nothing",
        },
        "locations": {
            "Trial Reward": "Nothing",
            "Relic 1": "Nothing",
            "Relic 2": "Nothing",
            "Relic 3": "Nothing",
            "Relic 4": "Nothing",
            "Relic 5": "Nothing",
            "Relic 6": "Nothing",
            "Relic 7": "Nothing",
            "Relic 8": "Nothing",
            "Relic 9": "Nothing",
            "Relic 10": "Nothing",
        },
    },
}
