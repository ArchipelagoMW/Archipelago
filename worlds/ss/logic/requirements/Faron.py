FARON_REQUIREMENTS = {
    "Sealed Grounds - Spiral": {
        "hint_region": "Sealed Grounds",
        "exits": {
            "Fly to Sky": "Nothing",
            "Sealed Temple": "Nothing",
        },
        "locations": {},
    },
    "Sealed Grounds - Sealed Temple": {
        "hint_region": "Sealed Grounds",
        "macros": {
            "Can Raise Gate of Time": "Goddess's Harp",
            "Can Reach Past": (
                "Can Raise Gate of Time "
                "& _sword_requirement_met "
                "& (_can_beat_required_dungeons | option_unrequired_dungeons)"
            ),
        },
        "exits": {
            "Spiral": "Nothing",
            "Behind the Temple": "Nothing",
            "Hylia's Realm": (
                "Can Reach Past "
                "& (Has Completed Triforce | option_no_triforce)"
            ),
        },
        "locations": {
            "Chest inside Sealed Temple": "Nothing",
            "Song from Impa": "Goddess's Harp",
            "Zelda's Blessing": "Can Reach Past",
        },
    },
    "Sealed Grounds - Behind the Temple": {
        "hint_region": "Sealed Grounds",
        "exits": {
            "Fly to Sky": "Nothing",
            "Sealed Temple": "Nothing",
            "Path to Forest": "Nothing",
        },
        "locations": {
            "Gorko's Goddess Wall Reward": (
                "Goddess's Harp & Ballad of the Goddess & Has Goddess Sword"
            ),
        },
    },
    "Hylia's Realm": {
        "hint_region": "Hylia's Realm",
        "exits": {
            "Door to Temple": "Nothing",
        },
        "locations": {
            "Defeat Demise": "Has Practice Sword",
        },
    },
    "Faron Woods - Forest Entry": {
        "hint_region": "Faron Woods",
        "exits": {
            "Fly to Sky": "Nothing",
            "Path out of Forest": "Nothing",
            "In the Woods": "Can Cut Trees | Clawshots",
        },
        "locations": {},
    },
    "Faron Woods - In the Woods": {
        "hint_region": "Faron Woods",
        "macros": {
            "Can Retrieve Oolo": "Bomb Bag & Scrapper",
            "Faron Woods Amber Relic Farming": "Nothing",
            "Goddess Cube on East Great Tree with Clawshot Target": (
                "Has Goddess Sword "
                "& (Clawshots | can_reach_region Faron Woods - Outside Top of Great Tree)"
            ),
            "Goddess Cube on East Great Tree with Rope": (
                "Has Goddess Sword "
                "& can_reach_region Faron Woods - Outside Top of Great Tree"
            ),
            "Goddess Cube on West Great Tree near Exit": (
                "Has Goddess Sword "
                "& can_reach_region Faron Woods - Outside Top of Great Tree"
            ),
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Forest Entry": "Nothing",
            "Viewing Platform": "Nothing",
            "Inside Lower Great Tree": "Water Dragon's Scale",
            "Great Tree Platforms": "Clawshots",
            "Jump into Lake": (
                "Water Dragon's Scale "
                "& ( (Can Talk to Yerbal & Has Goddess Sword) "
                "| (Can Talk to Yerbal & option_lake_floria_yerbal) "
                "| (option_lake_floria_open) )"
            )
        },
        "locations": {
            "Item behind Lower Bombable Rock": "Bomb Bag",
            "Item on Tree": "Nothing",
            "Kikwi Elder's Reward": (
                "Can Defeat Bokoblins "
                "& Can Cut Trees "
                "& (Has Practice Sword | Has Beetle)"
            ),
            "Rupee on Hollow Tree Root": "Nothing",
            "Rupee on Hollow Tree Branch": "Has Beetle",
            "Rupee on Platform near Floria Door": "Has Beetle",
            "Chest behind Upper Bombable Rock": "Bomb Bag",
        },
    },
    "Faron Woods - Viewing Platform": {
        "hint_region": "Faron Woods",
        "exits": {
            "Fly to Sky": "Nothing",
            "In the Woods": "Nothing",
            "Deep Woods Entry": "Distance Activator | Bomb Bag",
            "Trial Gate in Faron Woods": "Goddess's Harp & Farore's Courage",
        },
        "locations": {},
    },
    "Faron Woods - Deep Woods Entry": {
        "hint_region": "Faron Woods",
        "macros": {
            "Deep Woods Hornet Larvae Farming": "Nothing",
        },
        "exits": {
            "Viewing Platform": "Nothing",
            "Deep Woods after Beehive": "Distance Activator | Bomb Bag | Has Goddess Sword",
        },
        "locations": {},
    },
    "Faron Woods - Deep Woods after Beehive": {
        "hint_region": "Faron Woods",
        "macros": {
            "Initial Goddess Cube": "Has Goddess Sword",
            "Goddess Cube in Deep Woods": "Has Goddess Sword",
            "Goddess Cube on top of Skyview": "Has Goddess Sword & Clawshots",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Deep Woods Entry": "Nothing",
            "Dungeon Entrance in Deep Woods": "Distance Activator",
        },
        "locations": {
            "Deep Woods Chest": "Nothing",
        },
    },
    "Faron Woods - Inside Lower Great Tree - Water": {
        "hint_region": "Faron Woods",
        "exits": {
            "In the Woods": "Water Dragon's Scale",
            "After Swinging Platforms": "Gust Bellows",
            "Upper Ledge": "Gust Bellows",
        },
        "locations": {},
    },
    "Faron Woods - Inside Lower Great Tree - After Swinging Platforms": {
        "hint_region": "Faron Woods",
        "exits": {
            "Water": "Nothing",
            "Upper Ledge": "Gust Bellows",
            "Great Tree Platforms": "Nothing",
        },
        "locations": {},
    },
    "Faron Woods - Inside Lower Great Tree - Upper Ledge": {
        "hint_region": "Faron Woods",
        "exits": {
            "Water": "Nothing",
            "After Swinging Platforms": "Nothing",
        },
        "locations": {
            "Chest inside Great Tree": "Nothing",
        },
    },
    "Faron Woods - Inside Upper Great Tree": {
        "hint_region": "Faron Woods",
        "exits": {
            "Lower Exit": "Nothing",
            "Upper Exit": "Nothing",
            "Jump Down to Lower Great Tree": "Can Defeat Moblins",
            "Speak to Water Dragon": "Nothing",
        },
        "locations": {},
    },
    "Faron Woods - Great Tree Platforms": {
        "hint_region": "Faron Woods",
        "exits": {
            "Lower Exit": "Nothing",
            "Upper Exit": "Nothing",
            "In the Woods": "Nothing",
            "Viewing Platform": "Nothing",
        },
        "locations": {},
    },
    "Faron Woods - Outside Top of Great Tree": {
        "hint_region": "Faron Woods",
        "macros": {
            "Can Talk to Yerbal": "Has Slingshot | Has Beetle"
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "In the Woods": "Nothing",
            "Viewing Platform": "Nothing",
            "Inside Upper Great Tree": "Nothing",
        },
        "locations": {
            "Rupee on Great Tree North Branch": "Has Beetle",
            "Rupee on Great Tree West Branch": "Has Beetle",
        },
    },
    "Lake Floria - Lake": {
        "hint_region": "Lake Floria",
        "exits": {
            "Higher Ledge in Lake": "Water Dragon's Scale",
            "Dragon's Lair": "Water Dragon's Scale",
        },
        "locations": {
            "Rupee under Central Boulder": "Water Dragon's Scale",
            "Rupee behind Southwest Boulder": "Water Dragon's Scale",
            "Left Rupee behind Northwest Boulder": "Water Dragon's Scale",
            "Right Rupee behind Northwest Boulder": "Water Dragon's Scale",
        },
    },
    "Lake Floria - Higher Ledge in Lake": {
        "hint_region": "Lake Floria",
        "macros": {
            "Goddess Cube in Lake Floria": "Has Goddess Sword",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Lake": "Water Dragon's Scale",
        },
        "locations": {
            "Lake Floria Chest": "Nothing",
        },
    },
    "Lake Floria - Dragon's Lair": {
        "hint_region": "Lake Floria",
        "exits": {
            "Lake": "Water Dragon's Scale",
            "Waterfall": "Nothing",
        },
        "locations": {
            "Dragon Lair South Chest": "Water Dragon's Scale",
            "Dragon Lair East Chest": "Nothing",
        },
    },
    "Lake Floria - Waterfall": {
        "hint_region": "Lake Floria",
        "macros": {
            "Goddess Cube in Floria Waterfall": "Has Goddess Sword & Clawshots",
        },
        "exits": {
            "Fly to Sky": "Nothing",
            "Dragon's Lair": "Nothing",
            "Path into Forest": "Nothing",
            "Ancient Cistern Ledge": "Water Dragon's Scale",
        },
        "locations": {
            "Rupee on High Ledge outside Ancient Cistern Entrance": "Has Beetle",
        },
    },
    "Lake Floria - Ancient Cistern Ledge": {
        "hint_region": "Lake Floria",
        "exits": {
            "Waterfall": "Nothing",
            "Dungeon Entrance in Lake Floria": "Nothing",
        },
        "locations": {},
    },
    "Flooded Faron Woods": {
        "hint_region": "Flooded Faron Woods",
        "exits": {
            "Speak to Water Dragon": "Nothing",
        },
        "locations": {
            "Yellow Tadtone under Lilypad": "Water Dragon's Scale",
            "8 Light Blue Tadtones near Viewing Platform": "Water Dragon's Scale",
            "4 Purple Tadtones under Viewing Platform": "Water Dragon's Scale",
            "Red Moving Tadtone near Viewing Platform": "Water Dragon's Scale",
            "Light Blue Tadtone under Great Tree Root": "Water Dragon's Scale",
            "8 Yellow Tadtones near Kikwi Elder": "Water Dragon's Scale",
            "4 Light Blue Moving Tadtones under Kikwi Elder": "Water Dragon's Scale",
            "4 Red Moving Tadtones North West of Great Tree": "Water Dragon's Scale",
            "Green Tadtone behind Upper Bombable Rock": "Water Dragon's Scale",
            "2 Dark Blue Tadtones in Grass West of Great Tree": "Water Dragon's Scale",
            "8 Green Tadtones in West Tunnel": "Water Dragon's Scale",
            "2 Red Tadtones in Grass near Lower Bombable Rock": "Water Dragon's Scale",
            "16 Dark Blue Tadtones in the South West": "Water Dragon's Scale",
            "4 Purple Moving Tadtones near Floria Gate": "Water Dragon's Scale",
            "Dark Blue Moving Tadtone inside Small Hollow Tree": "Water Dragon's Scale",
            "4 Yellow Tadtones under Small Hollow Tree": "Water Dragon's Scale",
            "8 Purple Tadtones in Clearing after Small Hollow Tree": "Water Dragon's Scale",
            "Water Dragon's Reward": "Group of Tadtones x17",
        },
    },
    "Faron Silent Realm": {
        "hint_region": "Faron Silent Realm",
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
