from typing import Dict, Set, List

REGIONS: Dict[str, List[str]] = {
    "Menu": [],
    "Tower HQ": [],
    "The Shop": [],
    "Tower of Time": [],
    "Ninja Village": ["Candle", "Astral Seed"],
    "Autumn Hills": ["Climbing Claws", "Key of Hope"],
    "Forlorn Temple": ["Demon King Crown"],
    "Catacombs": ["Necro", "Ruxxtin's Amulet"],
    "Bamboo Creek": ["Claustro"],
    "Howling Grotto": ["Wingsuit"],
    "Quillshroom Marsh": ["Seashell"],
    "Searing Crags": ["Rope Dart"],
    "Searing Crags Upper": ["Power Thistle", "Key of Strength", "Astral Tea Leaves"],
    "Glacial Peak": [],
    "Cloud Ruins": ["Acro"],
    "Underworld": ["Pyro", "Key of Chaos"],
    "Dark Cave": [],
    "Riviere Turquoise": ["Fairy Bottle"],
    "Sunken Shrine": ["Ninja Tabi", "Sun Crest", "Moon Crest", "Key of Love"],
    "Elemental Skylands": ["Key of Symbiosis"],
    "Corrupted Future": ["Key of Courage"],
    "Music Box": ["Rescue Phantom"]
}
"""seal locations have the region in their name and may not need to be created so skip them here"""


REGION_CONNECTIONS: Dict[str, Set[str]] = {
    "Menu": {"Tower HQ"},
    "Tower HQ": {"Autumn Hills", "Howling Grotto", "Searing Crags", "Glacial Peak", "Tower of Time", "Riviere Turquoise",
                 "Sunken Shrine", "Corrupted Future", "The Shop", "Music Box"},
    "Tower of Time": set(),
    "Ninja Village": set(),
    "Autumn Hills": {"Ninja Village", "Forlorn Temple", "Catacombs"},
    "Forlorn Temple": {"Catacombs", "Bamboo Creek"},
    "Catacombs": {"Autumn Hills", "Bamboo Creek", "Dark Cave"},
    "Bamboo Creek": {"Catacombs", "Howling Grotto"},
    "Howling Grotto": {"Bamboo Creek", "Quillshroom Marsh", "Sunken Shrine"},
    "Quillshroom Marsh": {"Howling Grotto", "Searing Crags"},
    "Searing Crags": {"Searing Crags Upper", "Quillshroom Marsh", "Underworld"},
    "Searing Crags Upper": {"Searing Crags", "Glacial Peak"},
    "Glacial Peak": {"Searing Crags Upper", "Tower HQ", "Cloud Ruins", "Elemental Skylands"},
    "Cloud Ruins": {"Underworld"},
    "Underworld": set(),
    "Dark Cave": {"Catacombs", "Riviere Turquoise"},
    "Riviere Turquoise": set(),
    "Sunken Shrine": {"Howling Grotto"},
    "Elemental Skylands": set()
}
"""Vanilla layout mapping with all Tower HQ portals open. from -> to"""
