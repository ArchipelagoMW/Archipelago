structure_contents = {
    "dragons_roar": {
        "Luster Dragon",
        "Armed Dragon LV3",
        "Armed Dragon LV5",
        "Masked Dragon",
        "Twin-Headed Behemoth",
        "Stamping Destruction",
        "Nobleman of Crossout",
        "Creature Swap"
    },
    "zombie_madness": {
        "Pyramid Turtle",
        "Regenerating Mummy",
        "Ryu Kokki",
        "Book of Life",
        "Call of the Mummy",
        "Creature Swap"
    },
    "blazing_destruction": {
        "Inferno",
        "Solar Flare Dragon",
        "UFO Turtle",
        "Ultimate Baseball Kid",
        "Fire Beaters",
        "Tribute to The Doomed",
        "Level Limit - Area B"
    },
    "fury_from_the_deep": {
        "Mother Grizzly",
        "Water Beaters",
        "Gravity Bind"
    },
    "warriors_triumph": {
        "Gearfried the Iron Knight",
        "D.D. Warrior Lady",
        "Marauding Captain",
        "Exiled Force",
        "Reinforcement of the Army",
        "Warrior Beaters"
    },
    "spellcasters_judgement": {
        "Dark Magician",
        "Apprentice Magician",
        "Breaker the Magical Warrior",
        "Magician of Faith",
        "Skilled Dark Magician",
        "Tsukuyomi",
        "Magical Dimension",
        "Spell-Counter Cards"
    }
}


def get_deck_content_locations(deck: str) -> dict[str, str]:
    location = {}
    i = 1
    for content in structure_contents.get(deck):
        location[deck + " " + str(i)] = content
        i = i + 1
    return location

