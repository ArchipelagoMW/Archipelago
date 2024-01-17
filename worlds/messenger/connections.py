from typing import Dict, List


CONNECTIONS: Dict[str, Dict[str, Dict[str, List[str]]]] = {
    "Ninja Village": {
        "Right": {
            "exits": [
                "Autumn Hills - Left",
            ],
            "rules": ["True"],
        },
    },
    "Autumn Hills": {
        "Left": {
            "exits": [
                "Ninja Village - Right",
            ],
            "rules": ["True"],
        },
        "Right": {
            "exits": [
                "Forlorn Temple - Left",
                "Autumn Hills - Leaf Golem Shop",
            ],
            "rules": ["True", "True"],
        },
        "Bottom": {
            "exits": [
                "Catacombs - Bottom Left",
            ],
            "rules": ["True"],
        },
        "Portal": {
            "exits": [
                "Tower HQ",
                "Autumn Hills - Dimension Climb Shop",
            ],
            "rules": ["True", "Wingsuit, Rope Dart"],
        },
        "Climbing Claws Shop": {
            "exits": [
                "Autumn Hills - Left",
                "Autumn Hills - Hope Path Shop",
            ],
            "rules": ["True", "True"],
        },
        "Hope Path Shop": {
            "exits": [
                "Autumn Hills - Climbing Claws Shop",
                "Autumn Hills - Hope Path Checkpoint",
                "Autumn Hills - Lakeside Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Dimension Climb Shop": {
            "exits": [
                "Autumn Hills - Lakeside Checkpoint",
                "Autumn Hills - Portal",
                "Autumn Hills - Double Swing Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Leaf Golem Shop": {
            "exits": [
                "Autumn Hills - Spike Ball Swing Checkpoint",
                "Autumn Hills - Right",
            ],
            "rules": ["True", "True"],
        },
        "Hope Path Checkpoint": {
            "exits": [
                "Autumn Hills - Hope Path Shop",
                "Autumn Hills - Key of Hope Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Key of Hope Checkpoint": {
            "exits": [
                "Autumn Hills - Hope Path Checkpoint",
                "Autumn Hills - Lakeside Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Lakeside Checkpoint": {
            "exits": [
                "Autumn Hills - Hope Path Shop",
                "Autumn Hills - Dimension Climb Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Double Swing Checkpoint": {
            "exits": [
                "Autumn Hills - Dimension Climb Shop",
                "Autumn Hills - Spike Ball Swing Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Spike Ball Swing Checkpoint": {
            "exits": [
                "Autumn Hills - Double Swing Checkpoint",
                "Autumn Hills - Leaf Golem Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Forlorn Temple": {
        "Left": {
            "exits": [
                "Autumn Hills - Right",
                "Forlorn Temple - Outside Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Right": {
            "exits": [
                "Bamboo Creek - Top Left",
                "Forlorn Temple - Demon King Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Bottom": {
            "exits": [
                "Catacombs - Top Left",
                "Forlorn Temple - Outside Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Outside Shop": {
            "exits": [
                "Forlorn Temple - Left",
                "Forlorn Temple - Bottom",
                "Forlorn Temple - Entrance Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Entrance Shop": {
            "exits": [
                "Forlorn Temple - Outside Shop",
                "Forlorn Temple - Sunny Day Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Sunny Day Checkpoint": {
            "exits": [
                "Forlorn Temple - Outside Shop",
                "Forlorn Temple - Rocket Maze Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Rocket Maze Checkpoint": {
            "exits": [
                "Forlorn Temple - Sunny Day Checkpoint",
                "Forlorn Temple - Climb Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Climb Shop": {
            "exits": [
                "Forlorn Temple - Rocket Maze Checkpoint",
                "Forlorn Temple - Rocket Sunset Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Rocket Sunset Shop": {
            "exits": [
                "Forlorn Temple - Climb Shop",
                "Forlorn Temple - Descent Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Descent Shop": {
            "exits": [
                "Forlorn Temple - Rocket Sunset Shop",
                "Forlorn Temple - Final Fall Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Final Fall Shop": {
            "exits": [
                "Forlorn Temple - Descent Shop",
                "Forlorn Temple - Demon King Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Demon King Shop": {
            "exits": [
                "Forlorn Temple - Final Fall Shop",
                "Forlorn Temple - Right",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Catacombs": {
        "Top Left": {
            "exits": [
                "Forlorn Temple - Bottom",
                "Catacombs - Triple Spike Crushers Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Bottom Left": {
            "exits": [
                "Autumn Hills - Bottom",
                "Catacombs - Triple Spike Crushers Shop",
                "Catacombs - Death Trap Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Bottom": {
            "exits": [
                "Dark Cave - Right",
                "Catacombs - Dirty Pond Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Right": {
            "exits": [
                "Bamboo Creek - Bottom Left",
                "Catacombs - Ruxxtin Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Triple Spike Crushers Shop": {
            "exits": [
                "Catacombs - Bottom Left",
                "Catacombs - Death Trap Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Ruxxtin Shop": {
            "exits": [
                "Catacombs - Right",
                "Catacombs - Dirty Pond Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Death Trap Checkpoint": {
            "exits": [
                "Catacombs - Triple Spike Crushers Shop",
                "Catacombs - Bottom Left",
                "Catacombs - Dirty Pond Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Crusher Gauntlet Checkpoint": {
            "exits": [
                "Catacombs - Dirty Pond Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Dirty Pond Checkpoint": {
            "exits": [
                "Catacombs - Bottom",
                "Catacombs - Death Trap Checkpoint",
                "Catacombs - Crusher Gauntlet Checkpoint",
                "Catacombs - Ruxxtin Shop",
            ],
            "rules": ["True", "True", "True", "True"],
        },
    },
    "Bamboo Creek": {
        "Bottom Left": {
            "exits": [
                "Catacombs - Right",
                "Bamboo Creek - Spike Crushers Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Top Left": {
            "exits": [
                "Forlorn Temple - Right",
                "Bamboo Creek - Abandoned Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Right": {
            "exits": [
                "Howling Grotto - Left",
                "Bamboo Creek - Time Loop Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Spike Crushers Shop": {
            "exits": [
                "Bamboo Creek - Bottom Left",
                "Bamboo Creek - Abandoned Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Abandoned Shop": {
            "exits": [
                "Bamboo Creek - Top Left",
                "Bamboo Creek - Spike Crushers Shop",
                "Bamboo Creek - Spike Doors Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Time Loop Shop": {
            "exits": [
                "Bamboo Creek - Right",
                "Bamboo Creek - Spike Doors Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Spike Ball Pits Checkpoint": {
            "exits": [
                "Bamboo Creek - Spike Doors Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Spike Doors Checkpoint": {
            "exits": [
                "Bamboo Creek - Abandoned Shop",
                "Bamboo Creek - Spike Ball Pits Checkpoint",
                "Bamboo Creek - Time Loop Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Howling Grotto": {
        "Left": {
            "exits": [
                "Bamboo Creek - Right",
                "Howling Grotto - Wingsuit Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Top": {
            "exits": [
                "Howling Grotto - Crushing Pits Shop",
                "Quillshroom Marsh - Bottom Right",
            ],
            "rules": ["True", "True", "True"],
        },
        "Right": {
            "exits": [
                "Howling Grotto - Emerald Golem Shop",
                "Quillshroom Marsh - Top Left",
            ],
            "rules": ["True", "True", "True"],
        },
        "Bottom": {
            "exits": [
                "Howling Grotto - Lost Woods Checkpoint",
                "Sunken Shrine - Left",
            ],
            "rules": ["True", "True", "True"],
        },
        "Portal": {
            "exits": [
                "Howling Grotto - Crushing Pits Shop",
                "Tower HQ",
            ],
            "rules": ["True", "True", "True"],
        },
        "Wingsuit Shop": {
            "exits": [
                "Howling Grotto - Left",
                "Howling Grotto - Lost Woods Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Crushing Pits Shop": {
            "exits": [
                "Howling Grotto - Lost Woods Checkpoint",
                "Howling Grotto - Portal",
                "Howling Grotto - Breezy Crushers Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Emerald Golem Shop": {
            "exits": [
                "Howling Grotto - Breezy Crushers Checkpoint",
                "Howling Grotto - Right",
            ],
            "rules": ["True", "True", "True"],
        },
        "Lost Woods Checkpoint": {
            "exits": [
                "Howling Grotto - Wingsuit Shop",
                "Howling Grotto - Crushing Pits Shop",
                "Howling Grotto - Bottom",
            ],
            "rules": ["True", "True", "True"],
        },
        "Breezy Crushers Checkpoint": {
            "exits": [
                "Howling Grotto - Crushing Pits Shop",
                "Howling Grotto - Emerald Golem Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Quillshroom Marsh": {
        "Top Left": {
            "exits": [
                "Howling Grotto - Right",
                "Quillshroom Marsh - Seashell Checkpoint",
                "Quillshroom Marsh - Spikey Window Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Bottom Left": {
            "exits": [
                "Howling Grotto - Top",
                "Quillshroom Marsh - Sand Trap Shop",
                "Quillshroom Marsh - Bottom Right",
            ],
            "rules": ["True", "True", "True"],
        },
        "Top Right": {
            "exits": [
                "Quillshroom Marsh - Queen of Quills Shop",
                "Searing Crags - Left",
            ],
            "rules": ["True", "True", "True"],
        },
        "Bottom Right": {
            "exits": [
                "Quillshroom Marsh - Bottom Left",
                "Quillshroom Marsh - Sand Trap Shop",
                "Searing Crags - Bottom",
            ],
            "rules": ["True", "True", "True"],
        },
        "Spikey Window Shop": {
            "exits": [
                "Quillshroom Marsh - Top Left",
                "Quillshroom Marsh - Seashell Checkpoint",
                "Quillshroom Marsh - Quicksand Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Sand Trap Shop": {
            "exits": [
                "Quillshroom Marsh - Quicksand Checkpoint",
                "Quillshroom Marsh - Bottom Left",
                "Quillshroom Marsh - Bottom Right",
                "Quillshroom Marsh - Spike Wave Checkpoint",
            ],
            "rules": ["True", "True", "True", "True"],
        },
        "Queen of Quills Shop": {
            "exits": [
                "Quillshroom Marsh - Spike Wave Checkpoint",
                "Quillshroom Marsh - Top Right",
            ],
            "rules": ["True", "True", "True"],
        },
        "Seashell Checkpoint": {
            "exits": [
                "Quillshroom Marsh - Top Left",
                "Quillshroom Marsh - Spikey Window Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Quicksand Checkpoint": {
            "exits": [
                "Quillshroom Marsh - Spikey Window Shop",
                "Quillshroom Marsh - Sand Trap Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Spike Wave Checkpoint": {
            "exits": [
                "Quillshroom Marsh - Sand Trap Shop",
                "Quillshroom Marsh - Queen of Quills Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Searing Crags": {
        "Left": {
            "exits": [
                "Quillshroom Marsh - Top Right",
                "Searing Crags - Rope Dart Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Top": {
            "exits": [
                "Searing Crags - Colossuses Shop",
                "Glacial Peak - Bottom",
            ],
            "rules": ["True", "True", "True"],
        },
        "Bottom": {
            "exits": [
                "Searing Crags - Portal",
                "Quillshroom Marsh - Bottom Right",
            ],
            "rules": ["True", "True", "True"],
        },
        "Right": {
            "exits": [
                "Searing Crags - Portal",
                "Underworld - Left",
            ],
            "rules": ["True", "True", "True"],
        },
        "Portal": {
            "exits": [
                "Searing Crags - Bottom",
                "Searing Crags - Right",
                "Searing Crags - Before Final Climb Shop",
                "Searing Crags - Colossuses Shop",
                "Tower HQ",
            ],
            "rules": ["True", "True", "True", "True", "True"],
        },
        "Rope Dart Shop": {
            "exits": [
                "Searing Crags - Left",
                "Searing Crags - Triple Ball Spinner Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Triple Ball Spinner Shop": {
            "exits": [
                "Searing Crags - Triple Ball Spinner Checkpoint",
                "Searing Crags - Searing Mega Shard Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Searing Mega Shard Shop": {
            "exits": [
                "Searing Crags - Triple Ball Spinner Shop",
                "Searing Crags - Raining Rocks Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Before Final Climb Shop": {
            "exits": [
                "Searing Crags - Raining Rocks Checkpoint",
                "Searing Crags - Portal",
                "Searing Crags - Colossuses Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Colossuses Shop": {
            "exits": [
                "Searing Crags - Before Final Climb Shop",
                "Searing Crags - Key of Strength Shop",
                "Searing Crags - Portal",
                "Searing Crags - Top",
            ],
            "rules": ["True", "True", "True", "True"],
        },
        "Key of Strength Shop": {
            "exits": [
                "Searing Crags - Searing Mega Shard Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Triple Ball Spinner Checkpoint": {
            "exits": [
                "Searing Crags - Rope Dart Shop",
                "Searing Crags - Triple Ball Spinner Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Raining Rocks Checkpoint": {
            "exits": [
                "Searing Crags - Searing Mega Shard Shop",
                "Searing Crags - Before Final Climb Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Glacial Peak": {
        "Bottom": {
            "exits": [
                "Searing Crags - Top",
                "Glacial Peak - Ice Climbers' Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Left": {
            "exits": [
                "Elemental Skylands",
                "Glacial Peak - Projectile Spike Pit Checkpoint",
                "Glacial Peak - Glacial Mega Shard Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Top": {
            "exits": [
                "Glacial Peak - Tower Entrance Shop",
                "Cloud Ruins - Left",
                "Glacial Peak - Portal",
            ],
            "rules": ["True", "True", "True"],
        },
        "Portal": {
            "exits": [
                "Glacial Peak - Top",
                "Tower HQ",
            ],
            "rules": ["True", "True", "True"],
        },
        "Ice Climbers' Shop": {
            "exits": [
                "Glacial Peak - Bottom",
                "Glacial Peak - Projectile Spike Pit Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Glacial Mega Shard Shop": {
            "exits": [
                "Glacial Peak - Left",
                "Glacial Peak - Air Swag Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Tower Entrance Shop": {
            "exits": [
                "Glacial Peak - Top",
                "Glacial Peak - Free Climbing Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Projectile Spike Pit Checkpoint": {
            "exits": [
                "Glacial Peak - Ice Climbers' Shop",
                "Glacial Peak - Left",
            ],
            "rules": ["True", "True", "True"],
        },
        "Air Swag Checkpoint": {
            "exits": [
                "Glacial Peak - Glacial Mega Shard Shop",
                "Glacial Peak - Free Climbing Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Free Climbing Checkpoint": {
            "exits": [
                "Glacial Peak - Air Swag Checkpoint",
                "Glacial Peak - Tower Entrance Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Tower of Time": {
        "Left": {
            "exits": [
                "Tower of Time - Entrance Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Entrance Shop": {
            "exits": [
                "Tower of Time - First Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Arcane Golem Shop": {
            "exits": [
                "Tower HQ",
                "Tower of Time - Sixth Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "First Checkpoint": {
            "exits": [
                "Tower of Time - Entrance Shop",
                "Tower of Time - Second Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Second Checkpoint": {
            "exits": [
                "Tower of Time - First Checkpoint",
                "Tower of Time - Third Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Third Checkpoint": {
            "exits": [
                "Tower of Time - Second Checkpoint",
                "Tower of Time - Fourth Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Fourth Checkpoint": {
            "exits": [
                "Tower of Time - Third Checkpoint",
                "Tower of Time - Fifth Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Fifth Checkpoint": {
            "exits": [
                "Tower of Time - Fourth Checkpoint",
                "Tower of Time - Sixth Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Sixth Checkpoint": {
            "exits": [
                "Tower of Time - Fifth Checkpoint",
                "Tower of Time - Arcane Golem Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Cloud Ruins": {
        "Left": {
            "exits": [
                "Glacial Peak - Top",
                "Cloud Ruins - Entrance Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Entrance Shop": {
            "exits": [
                "Cloud Ruins - Left",
                "Cloud Ruins - Spike Float Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Pillar Glide Shop": {
            "exits": [
                "Cloud Ruins - Spike Float Checkpoint",
                "Cloud Ruins - Ghost Pit Checkpoint",
                "Cloud Ruins - Crushers' Descent Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Crushers' Descent Shop": {
            "exits": [
                "Cloud Ruins - Pillar Glide Shop",
                "Cloud Ruins - Toothbrush Alley Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Seeing Spikes Shop": {
            "exits": [
                "Cloud Ruins - Toothbrush Alley Checkpoint",
                "Cloud Ruins - Sliding Spikes Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Sliding Spikes Shop": {
            "exits": [
                "Cloud Ruins - Seeing Spikes Shop",
                "Cloud Ruins - Saw Pit Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Final Flight Shop": {
            "exits": [
                "Cloud Ruins - Saw Pit Checkpoint",
                "Cloud Ruins - Manfred's Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Manfred's Shop": {
            "exits": [
                "Cloud Ruins - Final Flight Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Spike Float Checkpoint": {
            "exits": [
                "Cloud Ruins - Entrance Shop",
                "Cloud Ruins - Pillar Glide Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Ghost Pit Checkpoint": {
            "exits": [
                "Cloud Ruins - Spike Float Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Toothbrush Alley Checkpoint": {
            "exits": [
                "Cloud Ruins - Crushers' Descent Shop",
                "Cloud Ruins - Seeing Spikes Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Saw Pit Checkpoint": {
            "exits": [
                "Cloud Ruins - Sliding Spikes Shop",
                "Cloud Ruins - Final Flight Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Underworld": {
        "Left": {
            "exits": [
                "Underworld - Entrance Shop",
                "Searing Crags - Right",
            ],
            "rules": ["True", "True", "True"],
        },
        "Entrance Shop": {
            "exits": [
                "Underworld - Left",
                "Underworld - Hot Dip Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Fireball Wave Shop": {
            "exits": [
                "Underworld - Hot Dip Checkpoint",
                "Underworld - Long Climb Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Long Climb Shop": {
            "exits": [
                "Underworld - Fireball Wave Shop",
                "Underworld - Hot Tub Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Barm'athaziel Shop": {
            "exits": [
                "Underworld - Hot Tub Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Key of Chaos Shop": {
            "exits": [
                "Underworld - Lava Run Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Hot Dip Checkpoint": {
            "exits": [
                "Underworld - Entrance Shop",
                "Underworld - Fireball Wave Shop",
                "Underworld - Lava Run Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Hot Tub Checkpoint": {
            "exits": [
                "Underworld - Long Climb Shop",
                "Underworld - Barm'athaziel Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Lava Run Checkpoint": {
            "exits": [
                "Underworld - Hot Dip Checkpoint",
                "Underworld - Key of Chaos Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Dark Cave": {
        "Right": {
            "exits": [
                "Catacombs - Bottom",
                "Dark Cave - Left",
            ],
            "rules": ["True", "True", "True"],
        },
        "Left": {
            "exits": [
                "Riviere Turquoise - Right",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Riviere Turquoise": {
        "Right": {
            "exits": [
                "Riviere Turquoise - Portal",
            ],
            "rules": ["True", "True", "True"],
        },
        "Portal": {
            "exits": [
                "Riviere Turquoise - Waterfall Shop",
                "Tower HQ",
            ],
            "rules": ["True", "True", "True"],
        },
        "Waterfall Shop": {
            "exits": [
                "Riviere Turquoise - Portal",
                "Riviere Turquoise - Flower Flight Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Launch of Faith Shop": {
            "exits": [
                "Riviere Turquoise - Flower Flight Checkpoint",
                "Riviere Turquoise - Log Flume Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Log Flume Shop": {
            "exits": [
                "Riviere Turquoise - Launch of Faith Shop",
                "Riviere Turquoise - Log Climb Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Log Climb Shop": {
            "exits": [
                "Riviere Turquoise - Log Flume Shop",
                "Riviere Turquoise - Restock Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Restock Shop": {
            "exits": [
                "Riviere Turquoise - Log Climb Shop",
                "Riviere Turquoise - Butterfly Matriarch Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Butterfly Matriarch Shop": {
            "exits": [
                "Riviere Turquoise - Restock Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Flower Flight Checkpoint": {
            "exits": [
                "Riviere Turquoise - Waterfall Shop",
                "Riviere Turquoise - Launch of Faith Shop",
            ],
            "rules": ["True", "True", "True"],
        },
    },
    "Sunken Shrine": {
        "Left": {
            "exits": [
                "Howling Grotto - Bottom",
                "Sunken Shrine - Portal",
            ],
            "rules": ["True", "True", "True"],
        },
        "Portal": {
            "exits": [
                "Sunken Shrine - Left",
                "Sunken Shrine - Entrance Shop",
                "Sunken Shrine - Sun Path Shop",
                "Sunken Shrine - Moon Path Shop",
                "Tower HQ",
            ],
            "rules": ["True", "True", "True", "True", "True"],
        },
        "Entrance Shop": {
            "exits": [
                "Sunken Shrine - Portal",
                "Sunken Shrine - Lifeguard Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Lifeguard Shop": {
            "exits": [
                "Sunken Shrine - Entrance Shop",
                "Sunken Shrine - Lightfoot Tabi Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Sun Path Shop": {
            "exits": [
                "Sunken Shrine - Portal",
                "Sunken Shrine - Tabi Gauntlet Shop",
            ],
            "rules": ["True", "True", "True"],
        },
        "Tabi Gauntlet Shop": {
            "exits": [
                "Sunken Shrine - Sun Path Shop",
                "Sunken Shrine - Sun Crest Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Moon Path Shop": {
            "exits": [
                "Sunken Shrine - Portal",
                "Sunken Shrine - Waterfall Paradise Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Lightfoot Tabi Checkpoint": {
            "exits": [
                "Sunken Shrine - Portal",
            ],
            "rules": ["True", "True", "True"],
        },
        "Sun Crest Checkpoint": {
            "exits": [
                "Sunken Shrine - Tabi Gauntlet Shop",
                "Sunken Shrine - Portal",
            ],
            "rules": ["True", "True", "True"],
        },
        "Waterfall Paradise Checkpoint": {
            "exits": [
                "Sunken Shrine - Moon Path Shop",
                "Sunken Shrine - Moon Crest Checkpoint",
            ],
            "rules": ["True", "True", "True"],
        },
        "Moon Crest Checkpoint": {
            "exits": [
                "Sunken Shrine - Waterfall Paradise Checkpoint",
                "Sunken Shrine - Portal",
            ],
            "rules": ["True", "True", "True"],
        },
    },
}
