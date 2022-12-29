from typing import Dict, Set

REGIONS: Dict[str, Set[str]] = {  # seal locations have the region in their name and may not be created so skip them here
    "Menu": {},
    "Tower HQ": {},
    "The Shop": {},
    "Ninja Village": {"Candle"},
    "Autumn Hills": {"Climbing Claws", "Key of Hope"},
    "Forlorn Temple": {"Demon King Crown"},
    "Catacombs": {"Necro", "Ruxxtin's Amulet"},
    "Bamboo Creek": {"Claustro"},
    "Howling Grotto": {"Wingsuit"},
    "Quillshroom Marsh": {"Seashell"},
    "Searing Crags": {"Rope Dart", "Pyro", "Key of Strength"},
    "Searing Crags Upper": {"Power Thistle"},
    "Glacial Peak": {},
    "Tower of Time": {},
    "Cloud Ruins": {"Acro"},
    "Underworld": {"Key of Chaos"},
    "Dark Cave": {},
    "Riviere Turquoise": {"Fairy Bottle"},
    "Sunken Shrine": {"Ninja Tabi", "Sun Crest", "Moon Crest", "Key of Love"},
    "Elemental Skylands": {"Key of Symbiosis"},
    "Corrupted Future": {"Key of Courage"},
    "Music Box": {"Rescue Phantom"}
}


REGION_CONNECTIONS: Dict[str, Set[str]] = {  # from -> to
    "Menu": {"Tower HQ"},
    "Tower HQ": {"Autumn Hills", "Howling Grotto", "Searing Crags", "Glacial Peak", "Tower of Time", "Riviere Turquoise",
                 "Sunken Shrine", "Corrupted Future", "The Shop", "Music Box"},
    "Ninja Village": {"Autumn Hills"},
    "Autumn Hills": {"Ninja Village", "Forlorn Temple", "Catacombs", "Tower HQ"},
    "Forlorn Temple": {"Autumn Hills", "Catacombs", "Bamboo Creek"},
    "Catacombs": {"Autumn Hills", "Forlorn Temple", "Bamboo Creek", "Dark Cave"},
    "Bamboo Creek": {"Forlorn Temple", "Catacombs", "Howling Grotto"},
    "Howling Grotto": {"Bamboo Creek", "Quillshroom Marsh", "Sunken Shrine", "Tower HQ"},
    "Quillshroom Marsh": {"Howling Grotto", "Searing Crags"},
    "Searing Crags": {"Searing Crags Upper", "Quillshroom Marsh", "Underworld", "Tower HQ"},
    "Searing Crags Upper": {"Searing Crags", "Glacial Peak"},
    "Glacial Peak": {"Searing Crags Upper", "Tower HQ", "Cloud Ruins", "Elemental Skylands"},
    "Cloud Ruins": {"Glacial Peak", "Underworld"},
    "Underworld": {"Searing Crags"},
    "Tower of Time": {"Tower HQ"},
    "Dark Cave": {"Catacombs", "Riviere Turquoise"},
    "Riviere Turquoise": {"Tower HQ"},
    "Sunken Shrine": {"Howling Grotto", "Tower HQ"},
    "Elemental Skylands": {"Glacial Peak"},
}

