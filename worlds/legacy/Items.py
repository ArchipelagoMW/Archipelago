import typing

from BaseClasses import Item


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    event: bool = False


class LegacyItem(Item):
    game: str = "Rogue Legacy"

    def __init__(self, name, player: int = None, event: bool = False):
        if event:
            super(LegacyItem, self).__init__(name, True, None, player)
        else:
            item_data = item_table[name]
            super(LegacyItem, self).__init__(
                name, item_data.progression, item_data.code, player)


item_vendors_table = {
    "Blacksmith": ItemData(90000, True),
    "Enchantress": ItemData(90001, True),
}

base_item_table = {
    "Architect": ItemData(90002, False),

    # Classes
    "Paladins": ItemData(90003, True),
    "Archmages": ItemData(90004, True),
    "Barbarian Kings": ItemData(90005, True),
    "Assassins": ItemData(90006, True),
    "Progressive Shinobis": ItemData(90007, True),
    "Progressive Miners": ItemData(90008, True),
    "Progressive Lichs": ItemData(90009, True),
    "Progressive Spellthieves": ItemData(90010, True),
    "Dragons": ItemData(90011, True),
    "Traitors": ItemData(90012, True),

    # Skill Unlocks
    "Health Up": ItemData(90013, True),
    "Mana Up": ItemData(90014, True),
    "Attack Up": ItemData(90015, True),
    "Magic Damage Up": ItemData(90016, True),
    "Armor Up": ItemData(90017, True),
    "Equip Up": ItemData(90018, True),
    "Crit Chance Up": ItemData(90019, False),
    "Crit Damage Up": ItemData(90020, False),
    "Down Strike Up": ItemData(90021, False),
    "Gold Gain Up": ItemData(90022, False),
    "Potion Efficiency Up": ItemData(90023, False),
    "Invulnerability Time Up": ItemData(90024, False),
    "Mana Cost Down": ItemData(90025, False),
    "Death Defiance": ItemData(90026, False),
    "Haggling": ItemData(90027, False),
    "Randomize Children": ItemData(90028, False),

    # Misc. Items
    "Triple Stat Increases": ItemData(90030, False),
    "1000 Gold": ItemData(90031, False),
    "3000 Gold": ItemData(90032, False),
    "5000 Gold": ItemData(90033, False),
}

equipment_item_table = {
    "Squire Armor Blueprints": ItemData(90040, True),
    "Silver Armor Blueprints": ItemData(90041, True),
    "Guardian Armor Blueprints": ItemData(90042, True),
    "Imperial Armor Blueprints": ItemData(90043, True),
    "Royal Armor Blueprints": ItemData(90044, True),
    "Knight Armor Blueprints": ItemData(90045, True),
    "Ranger Armor Blueprints": ItemData(90046, True),
    "Sky Armor Blueprints": ItemData(90047, True),
    "Dragon Armor Blueprints": ItemData(90048, True),
    "Slayer Armor Blueprints": ItemData(90049, True),
    "Blood Armor Blueprints": ItemData(90050, True),
    "Sage Armor Blueprints": ItemData(90051, True),
    "Retribution Armor Blueprints": ItemData(90052, True),
    "Holy Armor Blueprints": ItemData(90053, True),
    "Dark Armor Blueprints": ItemData(90054, True),
}

rune_item_table = {
    "Vault Runes": ItemData(90060, True),
    "Sprint Runes": ItemData(90061, True),
    "Vampire Runes": ItemData(90062, True),
    "Sky Runes": ItemData(90063, True),
    "Siphon Runes": ItemData(90064, True),
    "Retaliation Runes": ItemData(90065, True),
    "Bounty Runes": ItemData(90066, True),
    "Haste Runes": ItemData(90067, True),
    "Curse Runes": ItemData(90068, True),
    "Grace Runes": ItemData(90069, True),
    "Balance Runes": ItemData(90070, True),
}

item_table = {
    **item_vendors_table,
    **base_item_table,
    **equipment_item_table,
    **rune_item_table,
}

extra_item_table = [
    "Triple Stat Increases",
    "1000 Gold",
    "3000 Gold",
    "5000 Gold",
]

# Anything not listed here will be added only once.
item_frequencies: typing.Dict[str, int] = {
    "Progressive Shinobis": 2,
    "Progressive Miners": 2,
    "Progressive Lichs": 2,
    "Progressive Spellthieves": 2,
    "Health Up": 15,
    "Mana Up": 15,
    "Attack Up": 15,
    "Magic Damage Up": 15,
    "Armor Up": 10,
    "Equip Up": 10,
    "Crit Chance Up": 5,
    "Crit Damage Up": 5,

    # Do not include these items in the pool by default. They will be added later to fill empty locations.
    "Triple Stat Increases": 0,
    "1000 Gold": 0,
    "3000 Gold": 0,
    "5000 Gold": 0,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
lookup_id_to_name[None] = "Victory"
