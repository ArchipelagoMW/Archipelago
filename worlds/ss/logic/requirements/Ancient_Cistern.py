ANCIENT_CISTERN_REQUIREMENTS = {
    "Ancient Cistern - Main Room": {
        "hint_region": "Ancient Cistern",
        "macros": {
            "Can Lower AC Statue": (
                "Whip & (Can Emerge to AC Main Room from Gutters | Clawshots)"
            ),
        },
        "exits": {
            "Dungeon Exit": "Nothing",
            "East Room": "Nothing",
            "Past Waterfall": "Water Dragon's Scale & Whip",
            "Statue": "Ancient Cistern Small Key x2 | Can Lower AC Statue",
        },
        "locations": {
            "Rupee in West Hand": "Water Dragon's Scale",
            "Rupee in East Hand": "Water Dragon's Scale",
            "Chest after Whip Hooks": "Whip",
            "Chest near Vines": (
                "Can Emerge to AC Main Room from Gutters "
                "| (Whip & Clawshots)"
            ),
        },
    },
    "Ancient Cistern - Statue": {
        "hint_region": "Ancient Cistern",
        "exits": {
            "Main Room": "Nothing",
            "Basement": "Can Lower AC Statue",
            "Boss Room": "Whip & Ancient Cistern Boss Key",
        },
        "locations": {
            "Chest in Key Locked Room": (
                "Ancient Cistern Small Key x2 & (Can Defeat Stalmaster | Can Lower AC Statue)"
            ),
        },
    },
    "Ancient Cistern - East Room": {
        "hint_region": "Ancient Cistern",
        "exits": {
            "Main Room": "Nothing",
        },
        "locations": {
            "First Rupee in East Part in Short Tunnel": (
                "Water Dragon's Scale & Can Unlock Combination Lock"
            ),
            "Second Rupee in East Part in Short Tunnel": (
                "Water Dragon's Scale & Can Unlock Combination Lock"
            ),
            "Third Rupee in East Part in Short Tunnel": (
                "Water Dragon's Scale & Can Unlock Combination Lock"
            ),
            "Rupee in East Part in Cubby": (
                "Water Dragon's Scale & Can Unlock Combination Lock"
            ),
            "Rupee in East Part in Main Tunnel": (
                "Water Dragon's Scale & Can Unlock Combination Lock"
            ),
            "Chest in East Part": (
                "Water Dragon's Scale & Can Unlock Combination Lock"
            ),
        },
    },
    "Ancient Cistern - Past Waterfall": {
        "hint_region": "Ancient Cistern",
        "exits": {
            "Main Room": "Water Dragon's Scale",
            "Gutters": "Whip",
        },
        "locations": {
            "Chest behind the Waterfall": "Nothing",
        },
    },
    "Ancient Cistern - Gutters": {
        "hint_region": "Ancient Cistern",
        "macros": {
            "Can Reach AC Boko Door": "Water Dragon's Scale & Whip & (Has Beetle | Has Bow)",
        },
        "exits": {
            "Past Gutters": "Can Reach AC Boko Door & Ancient Cistern Small Key x2"
        },
        "locations": {
            "Bokoblin": "Can Reach AC Boko Door & Whip"
        },
    },
    "Ancient Cistern - Past Gutters": {
        "hint_region": "Ancient Cistern",
        "macros": {
            "Can Emerge to AC Main Room from Gutters": "Nothing",
        },
        "exits": {
            "Dungeon Exit": "Nothing",
            "Main Room": "Can Emerge to AC Main Room from Gutters",
        },
        "locations": {
            "Rupee under Lilypad": "Water Dragon's Scale & Whip",
        },
    },
    "Ancient Cistern - Basement": {
        "hint_region": "Ancient Cistern",
        "macros": {
            "Can Reach AC Thread": "Whip & (Clawshots | Has Hook Beetle)",
        },
        "exits": {
            "Statue": "Nothing",
        },
        "locations": {
            "Boss Key Chest": "Can Reach AC Thread",
        },
    },
    "Ancient Cistern - Boss Room": {
        "hint_region": "Ancient Cistern",
        "macros": {
            "Can Beat Koloktos": "Whip & (Has Practice Sword | Bomb Bag | Has Bow)",
        },
        "exits": {
            "Statue": "Nothing",
            "Flame Room": "Can Beat Koloktos",
        },
        "locations": {
            "Heart Container": "Can Beat Koloktos",
        },
    },
    "Ancient Cistern - Flame Room": {
        "hint_region": "Ancient Cistern",
        "macros": {
            "Can Beat Ancient Cistern": "Has Goddess Sword",
        },
        "exits": {
            "Boss Room": "Nothing",
            "Strike Crest": "Can Beat Ancient Cistern",
        },
        "locations": {
            "Farore's Flame": "Can Beat Ancient Cistern",
        },
    },
}
