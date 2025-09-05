CONNECTIONS: dict[str, dict[str, list[str]]] = {
    "Ninja Village": {
        "Right": [
            "Autumn Hills - Left",
            "Ninja Village - Nest",
        ],
        "Nest": [
            "Ninja Village - Right",
        ],
    },
    "Autumn Hills": {
        "Left": [
            "Ninja Village - Right",
            "Autumn Hills - Climbing Claws Shop",
        ],
        "Right": [
            "Forlorn Temple - Left",
            "Autumn Hills - Leaf Golem Shop",
        ],
        "Bottom": [
            "Catacombs - Bottom Left",
            "Autumn Hills - Double Swing Checkpoint",
        ],
        "Portal": [
            "Tower HQ",
            "Autumn Hills - Dimension Climb Shop",
        ],
        "Climbing Claws Shop": [
            "Autumn Hills - Left",
            "Autumn Hills - Hope Path Shop",
            "Autumn Hills - Lakeside Checkpoint",
            "Autumn Hills - Key of Hope Checkpoint",
        ],
        "Hope Path Shop": [
            "Autumn Hills - Climbing Claws Shop",
            "Autumn Hills - Hope Latch Checkpoint",
            "Autumn Hills - Lakeside Checkpoint",
        ],
        "Dimension Climb Shop": [
            "Autumn Hills - Lakeside Checkpoint",
            "Autumn Hills - Portal",
            "Autumn Hills - Double Swing Checkpoint",
        ],
        "Leaf Golem Shop": [
            "Autumn Hills - Spike Ball Swing Checkpoint",
            "Autumn Hills - Right",
        ],
        "Hope Latch Checkpoint": [
            "Autumn Hills - Hope Path Shop",
            "Autumn Hills - Key of Hope Checkpoint",
        ],
        "Key of Hope Checkpoint": [
            "Autumn Hills - Hope Latch Checkpoint",
            "Autumn Hills - Lakeside Checkpoint",
        ],
        "Lakeside Checkpoint": [
            "Autumn Hills - Climbing Claws Shop",
            "Autumn Hills - Dimension Climb Shop",
        ],
        "Double Swing Checkpoint": [
            "Autumn Hills - Dimension Climb Shop",
            "Autumn Hills - Spike Ball Swing Checkpoint",
            "Autumn Hills - Bottom",
        ],
        "Spike Ball Swing Checkpoint": [
            "Autumn Hills - Double Swing Checkpoint",
            "Autumn Hills - Leaf Golem Shop",
        ],
    },
    "Forlorn Temple": {
        "Left": [
            "Autumn Hills - Right",
            "Forlorn Temple - Outside Shop",
        ],
        "Right": [
            "Bamboo Creek - Top Left",
            "Forlorn Temple - Demon King Shop",
        ],
        "Bottom": [
            "Catacombs - Top Left",
            "Forlorn Temple - Outside Shop",
        ],
        "Outside Shop": [
            "Forlorn Temple - Left",
            "Forlorn Temple - Bottom",
            "Forlorn Temple - Entrance Shop",
        ],
        "Entrance Shop": [
            "Forlorn Temple - Outside Shop",
            "Forlorn Temple - Sunny Day Checkpoint",
        ],
        "Climb Shop": [
            "Forlorn Temple - Rocket Maze Checkpoint",
            "Forlorn Temple - Rocket Sunset Shop",
        ],
        "Rocket Sunset Shop": [
            "Forlorn Temple - Climb Shop",
            "Forlorn Temple - Descent Shop",
        ],
        "Descent Shop": [
            "Forlorn Temple - Rocket Sunset Shop",
            "Forlorn Temple - Saw Gauntlet Shop",
        ],
        "Saw Gauntlet Shop": [
            "Forlorn Temple - Demon King Shop",
        ],
        "Demon King Shop": [
            "Forlorn Temple - Saw Gauntlet Shop",
            "Forlorn Temple - Right",
        ],
        "Sunny Day Checkpoint": [
            "Forlorn Temple - Rocket Maze Checkpoint",
        ],
        "Rocket Maze Checkpoint": [
            "Forlorn Temple - Climb Shop",
        ],
    },
    "Catacombs": {
        "Top Left": [
            "Forlorn Temple - Bottom",
            "Catacombs - Triple Spike Crushers Shop",
        ],
        "Bottom Left": [
            "Autumn Hills - Bottom",
            "Catacombs - Triple Spike Crushers Shop",
            "Catacombs - Death Trap Checkpoint",
        ],
        "Bottom": [
            "Dark Cave - Right",
            "Catacombs - Dirty Pond Checkpoint",
        ],
        "Right": [
            "Bamboo Creek - Bottom Left",
            "Catacombs - Ruxxtin Shop",
        ],
        "Triple Spike Crushers Shop": [
            "Catacombs - Bottom Left",
            "Catacombs - Death Trap Checkpoint",
        ],
        "Ruxxtin Shop": [
            "Catacombs - Right",
            "Catacombs - Dirty Pond Checkpoint",
        ],
        "Death Trap Checkpoint": [
            "Catacombs - Triple Spike Crushers Shop",
            "Catacombs - Bottom Left",
            "Catacombs - Dirty Pond Checkpoint",
        ],
        "Crusher Gauntlet Checkpoint": [
            "Catacombs - Dirty Pond Checkpoint",
        ],
        "Dirty Pond Checkpoint": [
            "Catacombs - Bottom",
            "Catacombs - Death Trap Checkpoint",
            "Catacombs - Crusher Gauntlet Checkpoint",
            "Catacombs - Ruxxtin Shop",
        ],
    },
    "Bamboo Creek": {
        "Bottom Left": [
            "Catacombs - Right",
            "Bamboo Creek - Spike Crushers Shop",
        ],
        "Top Left": [
            "Bamboo Creek - Abandoned Shop",
            "Forlorn Temple - Right",
        ],
        "Right": [
            "Howling Grotto - Left",
            "Bamboo Creek - Time Loop Shop",
        ],
        "Spike Crushers Shop": [
            "Bamboo Creek - Bottom Left",
            "Bamboo Creek - Abandoned Shop",
        ],
        "Abandoned Shop": [
            "Bamboo Creek - Spike Crushers Shop",
            "Bamboo Creek - Spike Doors Checkpoint",
        ],
        "Time Loop Shop": [
            "Bamboo Creek - Right",
            "Bamboo Creek - Spike Doors Checkpoint",
        ],
        "Spike Ball Pits Checkpoint": [
            "Bamboo Creek - Spike Doors Checkpoint",
        ],
        "Spike Doors Checkpoint": [
            "Bamboo Creek - Abandoned Shop",
            "Bamboo Creek - Spike Ball Pits Checkpoint",
            "Bamboo Creek - Time Loop Shop",
        ],
    },
    "Howling Grotto": {
        "Left": [
            "Bamboo Creek - Right",
            "Howling Grotto - Wingsuit Shop",
        ],
        "Top": [
            "Howling Grotto - Crushing Pits Shop",
            "Quillshroom Marsh - Bottom Left",
        ],
        "Right": [
            "Howling Grotto - Emerald Golem Shop",
            "Quillshroom Marsh - Top Left",
        ],
        "Bottom": [
            "Howling Grotto - Lost Woods Checkpoint",
            "Sunken Shrine - Left",
        ],
        "Portal": [
            "Howling Grotto - Crushing Pits Shop",
            "Tower HQ",
        ],
        "Wingsuit Shop": [
            "Howling Grotto - Left",
            "Howling Grotto - Lost Woods Checkpoint",
        ],
        "Crushing Pits Shop": [
            "Howling Grotto - Lost Woods Checkpoint",
            "Howling Grotto - Portal",
            "Howling Grotto - Breezy Crushers Checkpoint",
            "Howling Grotto - Top",
        ],
        "Emerald Golem Shop": [
            "Howling Grotto - Breezy Crushers Checkpoint",
            "Howling Grotto - Right",
        ],
        "Lost Woods Checkpoint": [
            "Howling Grotto - Wingsuit Shop",
            "Howling Grotto - Crushing Pits Shop",
            "Howling Grotto - Bottom",
        ],
        "Breezy Crushers Checkpoint": [
            "Howling Grotto - Crushing Pits Shop",
            "Howling Grotto - Emerald Golem Shop",
        ],
    },
    "Quillshroom Marsh": {
        "Top Left": [
            "Howling Grotto - Right",
            "Quillshroom Marsh - Seashell Checkpoint",
            "Quillshroom Marsh - Spikey Window Shop",
        ],
        "Bottom Left": [
            "Howling Grotto - Top",
            "Quillshroom Marsh - Sand Trap Shop",
        ],
        "Top Right": [
            "Quillshroom Marsh - Queen of Quills Shop",
            "Searing Crags - Left",
        ],
        "Bottom Right": [
            "Quillshroom Marsh - Sand Trap Shop",
            "Searing Crags - Bottom",
        ],
        "Spikey Window Shop": [
            "Quillshroom Marsh - Top Left",
            "Quillshroom Marsh - Seashell Checkpoint",
            "Quillshroom Marsh - Quicksand Checkpoint",
        ],
        "Sand Trap Shop": [
            "Quillshroom Marsh - Quicksand Checkpoint",
            "Quillshroom Marsh - Bottom Left",
            "Quillshroom Marsh - Bottom Right",
            "Quillshroom Marsh - Spike Wave Checkpoint",
        ],
        "Queen of Quills Shop": [
            "Quillshroom Marsh - Spike Wave Checkpoint",
            "Quillshroom Marsh - Top Right",
        ],
        "Seashell Checkpoint": [
            "Quillshroom Marsh - Top Left",
            "Quillshroom Marsh - Spikey Window Shop",
        ],
        "Quicksand Checkpoint": [
            "Quillshroom Marsh - Spikey Window Shop",
            "Quillshroom Marsh - Sand Trap Shop",
        ],
        "Spike Wave Checkpoint": [
            "Quillshroom Marsh - Sand Trap Shop",
            "Quillshroom Marsh - Queen of Quills Shop",
        ],
    },
    "Searing Crags": {
        "Left": [
            "Quillshroom Marsh - Top Right",
            "Searing Crags - Rope Dart Shop",
        ],
        "Top": [
            "Searing Crags - Colossuses Shop",
            "Glacial Peak - Bottom",
        ],
        "Bottom": [
            "Searing Crags - Portal",
            "Quillshroom Marsh - Bottom Right",
        ],
        "Right": [
            "Searing Crags - Portal",
            "Underworld - Left",
        ],
        "Portal": [
            "Searing Crags - Bottom",
            "Searing Crags - Right",
            "Searing Crags - Before Final Climb Shop",
            "Searing Crags - Colossuses Shop",
            "Tower HQ",
        ],
        "Rope Dart Shop": [
            "Searing Crags - Left",
            "Searing Crags - Triple Ball Spinner Checkpoint",
        ],
        "Falling Rocks Shop": [
            "Searing Crags - Triple Ball Spinner Checkpoint",
            "Searing Crags - Searing Mega Shard Shop",
        ],
        "Searing Mega Shard Shop": [
            "Searing Crags - Falling Rocks Shop",
            "Searing Crags - Before Final Climb Shop",
            "Searing Crags - Key of Strength Shop",
        ],
        "Before Final Climb Shop": [
            "Searing Crags - Raining Rocks Checkpoint",
            "Searing Crags - Portal",
            "Searing Crags - Colossuses Shop",
        ],
        "Colossuses Shop": [
            "Searing Crags - Before Final Climb Shop",
            "Searing Crags - Key of Strength Shop",
            "Searing Crags - Portal",
            "Searing Crags - Top",
        ],
        "Key of Strength Shop": [
            "Searing Crags - Searing Mega Shard Shop",
        ],
        "Triple Ball Spinner Checkpoint": [
            "Searing Crags - Rope Dart Shop",
            "Searing Crags - Falling Rocks Shop",
        ],
        "Raining Rocks Checkpoint": [
            "Searing Crags - Searing Mega Shard Shop",
            "Searing Crags - Before Final Climb Shop",
        ],
    },
    "Glacial Peak": {
        "Bottom": [
            "Searing Crags - Top",
            "Glacial Peak - Ice Climbers' Shop",
        ],
        "Left": [
            "Elemental Skylands - Air Shmup",
            "Glacial Peak - Projectile Spike Pit Checkpoint",
            "Glacial Peak - Glacial Mega Shard Shop",
        ],
        "Top": [
            "Glacial Peak - Tower Entrance Shop",
            "Cloud Ruins - Left",
        ],
        "Portal": [
            "Glacial Peak - Tower Entrance Shop",
            "Tower HQ",
        ],
        "Ice Climbers' Shop": [
            "Glacial Peak - Bottom",
            "Glacial Peak - Projectile Spike Pit Checkpoint",
        ],
        "Glacial Mega Shard Shop": [
            "Glacial Peak - Left",
            "Glacial Peak - Air Swag Checkpoint",
        ],
        "Tower Entrance Shop": [
            "Glacial Peak - Top",
            "Glacial Peak - Free Climbing Checkpoint",
            "Glacial Peak - Portal",
        ],
        "Projectile Spike Pit Checkpoint": [
            "Glacial Peak - Ice Climbers' Shop",
            "Glacial Peak - Left",
        ],
        "Air Swag Checkpoint": [
            "Glacial Peak - Glacial Mega Shard Shop",
            "Glacial Peak - Free Climbing Checkpoint",
        ],
        "Free Climbing Checkpoint": [
            "Glacial Peak - Air Swag Checkpoint",
            "Glacial Peak - Tower Entrance Shop",
        ],
    },
    "Tower of Time": {
        "Left": [
            "Tower of Time - Final Chance Shop",
        ],
        "Final Chance Shop": [
            "Tower of Time - First Checkpoint",
        ],
        "Arcane Golem Shop": [
            "Tower of Time - Sixth Checkpoint",
        ],
        "First Checkpoint": [
            "Tower of Time - Second Checkpoint",
        ],
        "Second Checkpoint": [
            "Tower of Time - Third Checkpoint",
        ],
        "Third Checkpoint": [
            "Tower of Time - Fourth Checkpoint",
        ],
        "Fourth Checkpoint": [
            "Tower of Time - Fifth Checkpoint",
        ],
        "Fifth Checkpoint": [
            "Tower of Time - Sixth Checkpoint",
        ],
        "Sixth Checkpoint": [
            "Tower of Time - Arcane Golem Shop",
        ],
    },
    "Cloud Ruins": {
        "Left": [
            "Glacial Peak - Top",
            "Cloud Ruins - Cloud Entrance Shop",
        ],
        "Cloud Entrance Shop": [
            "Cloud Ruins - Left",
            "Cloud Ruins - Spike Float Checkpoint",
        ],
        "Pillar Glide Shop": [
            "Cloud Ruins - Spike Float Checkpoint",
            "Cloud Ruins - Ghost Pit Checkpoint",
            "Cloud Ruins - Crushers' Descent Shop",
        ],
        "Crushers' Descent Shop": [
            "Cloud Ruins - Pillar Glide Shop",
            "Cloud Ruins - Toothbrush Alley Checkpoint",
        ],
        "Seeing Spikes Shop": [
            "Cloud Ruins - Toothbrush Alley Checkpoint",
            "Cloud Ruins - Sliding Spikes Shop",
        ],
        "Sliding Spikes Shop": [
            "Cloud Ruins - Seeing Spikes Shop",
            "Cloud Ruins - Saw Pit Checkpoint",
        ],
        "Final Flight Shop": [
            "Cloud Ruins - Saw Pit Checkpoint",
            "Cloud Ruins - Manfred's Shop",
        ],
        "Manfred's Shop": [
            "Cloud Ruins - Final Flight Shop",
        ],
        "Spike Float Checkpoint": [
            "Cloud Ruins - Cloud Entrance Shop",
            "Cloud Ruins - Pillar Glide Shop",
        ],
        "Ghost Pit Checkpoint": [
            "Cloud Ruins - Pillar Glide Shop",
        ],
        "Toothbrush Alley Checkpoint": [
            "Cloud Ruins - Crushers' Descent Shop",
            "Cloud Ruins - Seeing Spikes Shop",
        ],
        "Saw Pit Checkpoint": [
            "Cloud Ruins - Sliding Spikes Shop",
            "Cloud Ruins - Final Flight Shop",
        ],
    },
    "Underworld": {
        "Left": [
            "Underworld - Left Shop",
            "Searing Crags - Right",
        ],
        "Left Shop": [
            "Underworld - Left",
            "Underworld - Hot Dip Checkpoint",
        ],
        "Fireball Wave Shop": [
            "Underworld - Hot Dip Checkpoint",
            "Underworld - Long Climb Shop",
        ],
        "Long Climb Shop": [
            "Underworld - Fireball Wave Shop",
            "Underworld - Hot Tub Checkpoint",
        ],
        "Barm'athaziel Shop": [
            "Underworld - Hot Tub Checkpoint",
        ],
        "Key of Chaos Shop": [
        ],
        "Hot Dip Checkpoint": [
            "Underworld - Left Shop",
            "Underworld - Fireball Wave Shop",
            "Underworld - Lava Run Checkpoint",
        ],
        "Hot Tub Checkpoint": [
            "Underworld - Long Climb Shop",
            "Underworld - Barm'athaziel Shop",
        ],
        "Lava Run Checkpoint": [
            "Underworld - Hot Dip Checkpoint",
            "Underworld - Key of Chaos Shop",
        ],
    },
    "Dark Cave": {
        "Right": [
            "Catacombs - Bottom",
            "Dark Cave - Left",
        ],
        "Left": [
            "Riviere Turquoise - Right",
        ],
    },
    "Riviere Turquoise": {
        "Right": [
            "Riviere Turquoise - Portal",
        ],
        "Portal": [
            "Riviere Turquoise - Waterfall Shop",
            "Tower HQ",
        ],
        "Waterfall Shop": [
            "Riviere Turquoise - Portal",
            "Riviere Turquoise - Flower Flight Checkpoint",
        ],
        "Launch of Faith Shop": [
            "Riviere Turquoise - Flower Flight Checkpoint",
            "Riviere Turquoise - Log Flume Shop",
        ],
        "Log Flume Shop": [
            "Riviere Turquoise - Log Climb Shop",
        ],
        "Log Climb Shop": [
            "Riviere Turquoise - Restock Shop",
        ],
        "Restock Shop": [
            "Riviere Turquoise - Butterfly Matriarch Shop",
        ],
        "Butterfly Matriarch Shop": [
        ],
        "Flower Flight Checkpoint": [
            "Riviere Turquoise - Waterfall Shop",
            "Riviere Turquoise - Launch of Faith Shop",
        ],
    },
    "Elemental Skylands": {
        "Air Shmup": [
            "Elemental Skylands - Air Intro Shop",
        ],
        "Air Intro Shop": [
            "Elemental Skylands - Air Seal Checkpoint",
            "Elemental Skylands - Air Generator Shop",
        ],
        "Air Seal Checkpoint": [
            "Elemental Skylands - Air Intro Shop",
            "Elemental Skylands - Air Generator Shop",
        ],
        "Air Generator Shop": [
            "Elemental Skylands - Earth Shmup",
        ],
        "Earth Shmup": [
            "Elemental Skylands - Earth Intro Shop",
        ],
        "Earth Intro Shop": [
            "Elemental Skylands - Earth Generator Shop",
        ],
        "Earth Generator Shop": [
            "Elemental Skylands - Water Shmup",
        ],
        "Water Shmup": [
            "Elemental Skylands - Water Intro Shop",
        ],
        "Water Intro Shop": [
            "Elemental Skylands - Water Generator Shop",
        ],
        "Water Generator Shop": [
            "Elemental Skylands - Fire Shmup",
        ],
        "Fire Shmup": [
            "Elemental Skylands - Fire Intro Shop",
        ],
        "Fire Intro Shop": [
            "Elemental Skylands - Fire Generator Shop",
        ],
        "Fire Generator Shop": [
            "Elemental Skylands - Right",
        ],
        "Right": [
            "Glacial Peak - Left",
        ],
    },
    "Sunken Shrine": {
        "Left": [
            "Howling Grotto - Bottom",
            "Sunken Shrine - Portal",
        ],
        "Portal": [
            "Sunken Shrine - Left",
            "Sunken Shrine - Above Portal Shop",
            "Sunken Shrine - Sun Path Shop",
            "Sunken Shrine - Moon Path Shop",
            "Tower HQ",
        ],
        "Above Portal Shop": [
            "Sunken Shrine - Portal",
            "Sunken Shrine - Lifeguard Shop",
        ],
        "Lifeguard Shop": [
            "Sunken Shrine - Above Portal Shop",
            "Sunken Shrine - Lightfoot Tabi Checkpoint",
        ],
        "Sun Path Shop": [
            "Sunken Shrine - Portal",
            "Sunken Shrine - Tabi Gauntlet Shop",
        ],
        "Tabi Gauntlet Shop": [
            "Sunken Shrine - Sun Path Shop",
            "Sunken Shrine - Sun Crest Checkpoint",
        ],
        "Moon Path Shop": [
            "Sunken Shrine - Portal",
            "Sunken Shrine - Waterfall Paradise Checkpoint",
        ],
        "Lightfoot Tabi Checkpoint": [
            "Sunken Shrine - Portal",
        ],
        "Sun Crest Checkpoint": [
            "Sunken Shrine - Tabi Gauntlet Shop",
            "Sunken Shrine - Portal",
        ],
        "Waterfall Paradise Checkpoint": [
            "Sunken Shrine - Moon Path Shop",
            "Sunken Shrine - Moon Crest Checkpoint",
        ],
        "Moon Crest Checkpoint": [
            "Sunken Shrine - Waterfall Paradise Checkpoint",
            "Sunken Shrine - Portal",
        ],
    },
}

RANDOMIZED_CONNECTIONS: dict[str, str] = {
    "Ninja Village - Right":            "Autumn Hills - Left",
    "Autumn Hills - Left":              "Ninja Village - Right",
    "Autumn Hills - Right":             "Forlorn Temple - Left",
    "Autumn Hills - Bottom":            "Catacombs - Bottom Left",
    "Forlorn Temple - Left":            "Autumn Hills - Right",
    "Forlorn Temple - Right":           "Bamboo Creek - Top Left",
    "Forlorn Temple - Bottom":          "Catacombs - Top Left",
    "Catacombs - Top Left":             "Forlorn Temple - Bottom",
    "Catacombs - Bottom Left":          "Autumn Hills - Bottom",
    "Catacombs - Bottom":               "Dark Cave - Right",
    "Catacombs - Right":                "Bamboo Creek - Bottom Left",
    "Bamboo Creek - Bottom Left":       "Catacombs - Right",
    "Bamboo Creek - Right":             "Howling Grotto - Left",
    "Bamboo Creek - Top Left":          "Forlorn Temple - Right",
    "Howling Grotto - Left":            "Bamboo Creek - Right",
    "Howling Grotto - Top":             "Quillshroom Marsh - Bottom Left",
    "Howling Grotto - Right":           "Quillshroom Marsh - Top Left",
    "Howling Grotto - Bottom":          "Sunken Shrine - Left",
    "Quillshroom Marsh - Top Left":     "Howling Grotto - Right",
    "Quillshroom Marsh - Bottom Left":  "Howling Grotto - Top",
    "Quillshroom Marsh - Top Right":    "Searing Crags - Left",
    "Quillshroom Marsh - Bottom Right": "Searing Crags - Bottom",
    "Searing Crags - Left":             "Quillshroom Marsh - Top Right",
    "Searing Crags - Top":              "Glacial Peak - Bottom",
    "Searing Crags - Bottom":           "Quillshroom Marsh - Bottom Right",
    "Searing Crags - Right":            "Underworld - Left",
    "Glacial Peak - Bottom":            "Searing Crags - Top",
    "Glacial Peak - Top":               "Cloud Ruins - Left",
    "Glacial Peak - Left":              "Elemental Skylands - Air Shmup",
    "Cloud Ruins - Left":               "Glacial Peak - Top",
    "Elemental Skylands - Right":       "Glacial Peak - Left",
    "Tower HQ":                         "Tower of Time - Left",
    "Artificer":                        "Corrupted Future",
    "Underworld - Left":                "Searing Crags - Right",
    "Dark Cave - Right":                "Catacombs - Bottom",
    "Dark Cave - Left":                 "Riviere Turquoise - Right",
    "Sunken Shrine - Left":             "Howling Grotto - Bottom",
}

TRANSITIONS: list[str] = [
    "Ninja Village - Right",
    "Autumn Hills - Left",
    "Autumn Hills - Right",
    "Autumn Hills - Bottom",
    "Forlorn Temple - Left",
    "Forlorn Temple - Bottom",
    "Forlorn Temple - Right",
    "Catacombs - Top Left",
    "Catacombs - Right",
    "Catacombs - Bottom",
    "Catacombs - Bottom Left",
    "Dark Cave - Right",
    "Dark Cave - Left",
    "Riviere Turquoise - Right",
    "Howling Grotto - Left",
    "Howling Grotto - Right",
    "Howling Grotto - Top",
    "Howling Grotto - Bottom",
    "Sunken Shrine - Left",
    "Bamboo Creek - Top Left",
    "Bamboo Creek - Bottom Left",
    "Bamboo Creek - Right",
    "Quillshroom Marsh - Top Left",
    "Quillshroom Marsh - Bottom Left",
    "Quillshroom Marsh - Top Right",
    "Quillshroom Marsh - Bottom Right",
    "Searing Crags - Left",
    "Searing Crags - Bottom",
    "Searing Crags - Right",
    "Searing Crags - Top",
    "Glacial Peak - Bottom",
    "Glacial Peak - Top",
    "Glacial Peak - Left",
    "Elemental Skylands - Air Shmup",
    "Elemental Skylands - Right",
    "Tower HQ",
    "Tower of Time - Left",
    "Corrupted Future",
    "Cloud Ruins - Left",
    "Underworld - Left",
]
