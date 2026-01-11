ELDIN_REQUIREMENTS = {
    "Eldin Volcano - Volcano Entry": {
        "hint_region": "Eldin Volcano",
        "macros": {
            "Goddess Cube at Eldin Entrance": "Has Goddess Sword",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Volcano East": "Nothing",
            "Volcano Ascent": "Bomb Bag",
            "Speak to Gossip Stone": "Nothing",
        },
        "locations": {
            "Rupee on Ledge before First Room": "Nothing",
            "Chest behind Bombable Wall in First Room": "Nothing",
            "Rupee behind Bombable Wall in First Room": "Nothing",
            "Rupee in Crawlspace in First Room": "Nothing",
        },
    },
    "Eldin Volcano - Volcano East": {
        "hint_region": "Eldin Volcano",
        "macros": {
            "Goddess Cube near Mogma Turf Entrance": "Has Goddess Sword",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Volcano Entry": "Bomb Bag | Clawshots",
            "Volcano Ascent": "Bomb Bag | Has Hook Beetle",
            "Mogma Cave": "Nothing",
        },
        "locations": {
            "Chest after Crawlspace": "Nothing",
            "Southeast Rupee above Mogma Turf Entrance": "Has Beetle",
            "North Rupee above Mogma Turf Entrance": "Has Beetle",
            "Chest behind Bombable Wall near Cliff": "Nothing",
            "Item on Cliff": "Nothing",
        },
    },
    "Eldin Volcano - Volcano Ascent": {
        "hint_region": "Eldin Volcano",
        "exits": {
            "Fly to Sky": "Nothing",
            "Volcano Entry": "Nothing",
            "Volcano East": "Nothing",
            "Thrill Digger Cliff": "Has Slingshot | Has Bow",
            "Bottom of Sand Slide": "Bomb Bag | Has Hook Beetle",
            "Trial Gate in Eldin Volcano": "Goddess's Harp & Din's Power",
        },
        "locations": {
            "Chest behind Bombable Wall near Volcano Ascent": "Nothing",
        },
    },
    "Eldin Volcano - Thrill Digger Cliff": {
        "hint_region": "Eldin Volcano",
        "exits": {
            "Volcano Ascent": "Nothing",
            "Thrill Digger Cave": "Nothing",
            "Near Temple Entrance": "Nothing",
        },
        "locations": {
            "Left Rupee behind Bombable Wall on First Slope": "Nothing",
            "Right Rupee behind Bombable Wall on First Slope": "Nothing",
        },
    },
    "Eldin Volcano - Thrill Digger Cave": {
        "hint_region": "Eldin Volcano",
        "macros": {
            "Thrill Digger Minigame": "Has Digging Mitts",
        },
        "exits": {
            "Exit Thrill Digger Cave": "Nothing",
        },
        "locations": {},
    },
    "Eldin Volcano - Near Temple Entrance": {
        "hint_region": "Eldin Volcano",
        "macros": {
            "Can Retrieve Crystal Ball": "Clawshots & Scrapper",
            "Goddess Cube East of Earth Temple Entrance": "Has Goddess Sword",
            "Goddess Cube West of Earth Temple Entrance": (
                "Has Goddess Sword & Has Digging Mitts"
            ),
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Thrill Digger Cliff": "can_reach_region Eldin Volcano - Thrill Digger Cliff",
            "Hot Cave": "Nothing",
            "Dungeon Entrance in Eldin Volcano": "Key Piece x5",
        },
        "locations": {
            "Digging Spot in front of Earth Temple": "Has Digging Mitts",
            "Digging Spot below Tower": "Has Digging Mitts",
            "Digging Spot behind Boulder on Sandy Slope": "Has Digging Mitts",
        },
    },
    "Eldin Volcano - Hot Cave": {
        "hint_region": "Eldin Volcano",
        "macros": {
            "Can Survive Eldin Hot Cave": (
                "Fireshield Earrings | option_damage_multiplier_under_12"
            ),
        },
        "exits": {
            "Near Temple Entrance": "can_reach_region Eldin Volcano - Near Temple Entrance",
            "Sand Slide": "Can Survive Eldin Hot Cave",
            "Upper Path out of Hot Cave": "Fireshield Earrings",
        },
        "locations": {},
    },
    "Eldin Volcano - Sand Slide": {
        "hint_region": "Eldin Volcano",
        "macros": {
            "Goddess Cube on Sand Slide": "Has Goddess Sword",
        },
        "exits": {
            "Bottom of Sand Slide": "Nothing",
        },
        "locations": {
            "Digging Spot after Vents": "Has Digging Mitts",
        },
    },
    "Eldin Volcano - Bottom of Sand Slide": {
        "hint_region": "Eldin Volcano",
        "exits": {
            "Volcano Ascent": "Nothing",
            "Hot Cave": "Nothing",
        },
        "locations": {
            "Digging Spot after Draining Lava": "Has Digging Mitts",
        },
    },
    "Mogma Turf - Entry": {
        "hint_region": "Mogma Turf",
        "macros": {
            "Can Retrieve Guld": "Scrapper",
            "Goddess Cube in Mogma Turf": "Has Goddess Sword",
        },
        "exits": {
            "Use First Air Vent": "Nothing",
            "Use Digging Air Vent": "Has Digging Mitts",
        },
        "locations": {
            "Free Fall Chest": "Nothing",
            "Chest behind Bombable Wall at Entrance": "Nothing",
            "Defeat Bokoblins": "Can Defeat Bokoblins",
        },
    },
    "Mogma Turf - After Digging Air Vent": {
        "hint_region": "Mogma Turf",
        "exits": {
            "Jump off Ledge": "Nothing",
            "Use Last Air Vent": "Nothing",
        },
        "locations": {
            "Sand Slide Chest": "Nothing",
            "Chest behind Bombable Wall in Fire Maze": "Nothing",
        },
    },
    "Volcano Summit - Summit": {
        "hint_region": "Volcano Summit",
        "macros": {
            "Goddess Cube inside Volcano Summit": "Has Goddess Sword & Upgraded Skyward Strike",
        },
        "exits": {
            "Path out of Summit before Sandy Slope": "Nothing",
            "Path out of Summit after Lava Platforms": "Fireshield Earrings",
            "Upper Path out of Summit after Lava Platforms": "Fireshield Earrings",
        },
        "locations": {},
    },
    "Volcano Summit - Waterfall": {
        "hint_region": "Volcano Summit",
        "macros": {
            "Goddess Cube in Summit Waterfall": "Has Goddess Sword",
        },
        "exits": {
            "Path out of Waterfall": "Nothing",
        },
        "locations": {
            "Chest behind Bombable Wall in Waterfall Area": "Clawshots",
        },
    },
    "Volcano Summit - Before First Frog": {
        "hint_region": "Volcano Summit",
        "macros": {
            "Can Water First Frog": "Has Bottle",
        },
        "exits": {
            "Path across from First Frog": "Nothing",
            "Pass First Frog": "Can Water First Frog",
        },
        "locations": {},
    },
    "Volcano Summit - Between Frogs": {
        "hint_region": "Volcano Summit",
        "macros": {
            "Can Water Second Frog": "Clawshots & Has Bottle",
        },
        "exits": {
            "Pass First Frog": "Can Water First Frog",
            "Pass Second Frog": "Can Water Second Frog",
        },
        "locations": {
            "Item behind Digging": "Has Mogma Mitts",
        },
    },
    "Volcano Summit - After Second Frog": {
        "hint_region": "Volcano Summit",
        "macros": {
            "Goddess Cube near Fire Sanctuary Entrance": "Has Goddess Sword & Clawshots",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Pass Second Frog": "Can Water Second Frog",
            "Dungeon Entrance in Volcano Summit": "Nothing",
        },
        "locations": {},
    },
    "Bokoblin Base - Prison": {
        "hint_region": "Bokoblin Base",
        "exits": {
            "Speak to Gossip Stone": "Nothing",
            "Dig to Volcano": "Has Mogma Mitts",
        },
        "locations": {
            "Plats' Gift": "Nothing",
        },
    },
    "Bokoblin Base - Volcano": {
        "hint_region": "Bokoblin Base",
        "macros": {
            "Can Bypass Boko Base Watchtower": "Bomb Bag | Has Slingshot | Has Bow",
            "Boko Base Goddess Cube near Mogma Turf Entrance": "Has Goddess Sword",
        },
        "exits": {
            "Dig to Prison": "Has Mogma Mitts",
            "Use Air Vent": "Clawshots & ( Bomb Bag | (Whip & Can Bypass Boko Base Watchtower) )"
        },
        "locations": {
            "Chest near Bone Bridge": "Has Mogma Mitts",
            "Chest on Cliff": "Has Mogma Mitts & Gust Bellows",
            "Chest near Drawbridge": (
                "Has Mogma Mitts "
                "& (Clawshots | Can Bypass Boko Base Watchtower)"
            ),
        },
    },
    "Bokoblin Base - Top of Volcano": {
        "hint_region": "Bokoblin Base",
        "macros": {
            "Boko Base Goddess Cube East of Earth Temple Entrance": "Has Goddess Sword",
            "Boko Base Goddess Cube West of Earth Temple Entrance": (
                "Has Goddess Sword "
                "& Has Mogma Mitts "
                "& Can Bypass Boko Base Watchtower"
            ),
        },
        "exits": {
            "Path through Hot Cave": "Bomb Bag & Fireshield Earrings",
        },
        "locations": {
            "Chest East of Earth Temple Entrance": "Nothing",
            "Chest West of Earth Temple Entrance": (
                "Has Mogma Mitts "
                "& Can Bypass Boko Base Watchtower "
                "& (Has Slingshot | Has Bow | Bomb Bag | Has Goddess Sword)"
            ),
        },
    },
    "Bokoblin Base - Summit": {
        "hint_region": "Bokoblin Base",
        "macros": {
            "Boko Base Goddess Cube inside Volcano Summit": "Has Goddess Sword",
        },
        "exits": {
            "Dragon's Lair": "Nothing",
        },
        "locations": {
            "First Chest in Volcano Summit": "Nothing",
            "Raised Chest in Volcano Summit": "Nothing",
            "Chest in Volcano Summit Alcove": "Has Practice Sword",
        },
    },
    "Bokoblin Base - Dragon's Lair": {
        "hint_region": "Bokoblin Base",
        "macros": {
            "Can Speak to Fire Dragon": "Has Beetle | Has Bow",
        },
        "exits": {
            "Exit Dragon's Lair": "Nothing",
            "Exit Bokoblin Base": "Can Speak to Fire Dragon",
        },
        "locations": {
            "Fire Dragon's Reward": "Can Speak to Fire Dragon",
        },
    },
    "Eldin Silent Realm": {
        "hint_region": "Eldin Silent Realm",
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
