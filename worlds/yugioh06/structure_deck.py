from typing import Dict, List

structure_contents: Dict[str, List[str]] = {
    "dragons_roar": [
        "Luster Dragon",
        "Armed Dragon LV3",
        "Armed Dragon LV5",
        "Masked Dragon",
        "Twin-Headed Behemoth",
        "Stamping Destruction",
        "Nobleman of Crossout",
        "Creature Swap",
        "Reload",
        "Stamping Destruction",
        "Heavy Storm",
        "Dust Tornado",
        "Mystical Space Typhoon"
    ],
    "zombie_madness": [
        "Pyramid Turtle",
        "Regenerating Mummy",
        "Ryu Kokki",
        "Book of Life",
        "Call of the Mummy",
        "Creature Swap",
        "Reload",
        "Heavy Storm",
        "Dust Tornado",
        "Mystical Space Typhoon"
    ],
    "blazing_destruction": [
        "Inferno",
        "Solar Flare Dragon",
        "UFO Turtle",
        "Ultimate Baseball Kid",
        "Fire Beaters",
        "Tribute to The Doomed",
        "Level Limit - Area B",
        "Heavy Storm",
        "Dust Tornado",
        "Mystical Space Typhoon"
    ],
    "fury_from_the_deep": [
        "Mother Grizzly",
        "Water Beaters",
        "Gravity Bind",
        "Reload",
        "Mobius the Frost Monarch",
        "Heavy Storm",
        "Dust Tornado",
        "Mystical Space Typhoon"
    ],
    "warriors_triumph": [
        "Gearfried the Iron Knight",
        "D.D. Warrior Lady",
        "Marauding Captain",
        "Exiled Force",
        "Reinforcement of the Army",
        "Warrior Beaters",
        "Reload",
        "Heavy Storm",
        "Dust Tornado",
        "Mystical Space Typhoon"
    ],
    "spellcasters_judgement": [
        "Dark Magician",
        "Apprentice Magician",
        "Breaker the Magical Warrior",
        "Magician of Faith",
        "Skilled Dark Magician",
        "Tsukuyomi",
        "Magical Dimension",
        "Mage Power",
        "Spell-Counter Cards",
        "Heavy Storm",
        "Dust Tornado",
        "Mystical Space Typhoon"
    ],
    "worst": [],
}


def get_deck_content_locations(deck: str) -> Dict[str, str]:
    return {
        f"{deck} {i}": content
        for i, content in enumerate(structure_contents[deck], 1)
    }


worst_deck = {
    "Dark Gray": 3,
    "Djinn the Watcher of the Wind": 3,
    "Flying Fish": 1,
    "Gate Deeg": 3,
    "Genin": 3,
    "Graveyard and the Hand of Invitation": 3,
    "Kanikabuto": 3,
    "Lightning Conger": 3,
    "Necrolancer the Timelord": 3,
    "Nemuriko": 3,
    "Obese Marmot of Nefariousness": 3,
    "The Drdek": 3,
    "The Shadow Who Controls the Dark": 3,
    "Turtle Raccoon": 3,
}