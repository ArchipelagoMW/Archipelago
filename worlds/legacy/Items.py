import typing

from BaseClasses import Item
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


class LegacyItem(Item):
    game: str = "Rogue Legacy"

    def __init__(self, name, advancement: bool = False, code: int = None, player: int = None):
        super(LegacyItem, self).__init__(name, advancement, code, player)


# Separate tables for each type of item.
vendors_table = {
    ItemName.blacksmith: ItemData(90000, True),
    ItemName.enchantress: ItemData(90001, True),
    ItemName.architect: ItemData(90002, False),
}

static_classes_table = {
    ItemName.knight: ItemData(90080, True),
    ItemName.paladin: ItemData(90081, True),
    ItemName.mage: ItemData(90082, True),
    ItemName.archmage: ItemData(90083, True),
    ItemName.barbarian: ItemData(90084, True),
    ItemName.barbarian_king: ItemData(90085, True),
    ItemName.knave: ItemData(90086, True),
    ItemName.assassin: ItemData(90087, True),
    ItemName.shinobi: ItemData(90088, True),
    ItemName.hokage: ItemData(90089, True),
    ItemName.miner: ItemData(90090, True),
    ItemName.spelunker: ItemData(90091, True),
    ItemName.lich: ItemData(90092, True),
    ItemName.lich_king: ItemData(90093, True),
    ItemName.spellthief: ItemData(90094, True),
    ItemName.spellsword: ItemData(90095, True),
    ItemName.dragon: ItemData(90096, True),
    ItemName.traitor: ItemData(90097, True),
}

progressive_classes_table = {
    ItemName.progressive_knight: ItemData(90003, True, 2),
    ItemName.progressive_mage: ItemData(90004, True, 2),
    ItemName.progressive_barbarian: ItemData(90005, True, 2),
    ItemName.progressive_knave: ItemData(90006, True, 2),
    ItemName.progressive_shinobi: ItemData(90007, True, 2),
    ItemName.progressive_miner: ItemData(90008, True, 2),
    ItemName.progressive_lich: ItemData(90009, True, 2),
    ItemName.progressive_spellthief: ItemData(90010, True, 2),
}

skill_unlocks_table = {
    ItemName.health: ItemData(90013, True, 15),
    ItemName.mana: ItemData(90014, True, 15),
    ItemName.attack: ItemData(90015, True, 15),
    ItemName.magic_damage: ItemData(90016, True, 15),
    ItemName.armor: ItemData(90017, True, 10),
    ItemName.equip: ItemData(90018, True, 10),
    ItemName.crit_chance: ItemData(90019, False, 5),
    ItemName.crit_damage: ItemData(90020, False, 5),
    ItemName.down_strike: ItemData(90021, False),
    ItemName.gold_gain: ItemData(90022, False),
    ItemName.potion_efficiency: ItemData(90023, False),
    ItemName.invulnerability_time: ItemData(90024, False),
    ItemName.mana_cost_down: ItemData(90025, False),
    ItemName.death_defiance: ItemData(90026, False),
    ItemName.haggling: ItemData(90027, False),
    ItemName.random_children: ItemData(90028, False),
}

blueprints_table = {
    ItemName.squire_blueprints: ItemData(90040, True),
    ItemName.silver_blueprints: ItemData(90041, True),
    ItemName.guardian_blueprints: ItemData(90042, True),
    ItemName.imperial_blueprints: ItemData(90043, True),
    ItemName.royal_blueprints: ItemData(90044, True),
    ItemName.knight_blueprints: ItemData(90045, True),
    ItemName.ranger_blueprints: ItemData(90046, True),
    ItemName.sky_blueprints: ItemData(90047, True),
    ItemName.dragon_blueprints: ItemData(90048, True),
    ItemName.slayer_blueprints: ItemData(90049, True),
    ItemName.blood_blueprints: ItemData(90050, True),
    ItemName.sage_blueprints: ItemData(90051, True),
    ItemName.retribution_blueprints: ItemData(90052, True),
    ItemName.holy_blueprints: ItemData(90053, True),
    ItemName.dark_blueprints: ItemData(90054, True),
}

runes_table = {
    ItemName.vault_runes: ItemData(90060, True),
    ItemName.sprint_runes: ItemData(90061, True),
    ItemName.vampire_runes: ItemData(90062, True),
    ItemName.sky_runes: ItemData(90063, True),
    ItemName.siphon_runes: ItemData(90064, True),
    ItemName.retaliation_runes: ItemData(90065, True),
    ItemName.bounty_runes: ItemData(90066, True),
    ItemName.haste_runes: ItemData(90067, True),
    ItemName.curse_runes: ItemData(90068, True),
    ItemName.grace_runes: ItemData(90069, True),
    ItemName.balance_runes: ItemData(90070, True),
}

misc_items_table = {
    ItemName.trip_stat_increase: ItemData(90030, False),
    ItemName.gold_1000: ItemData(90031, False),
    ItemName.gold_3000: ItemData(90032, False),
    ItemName.gold_5000: ItemData(90033, False),
}

# Complete item table.
item_table = {
    **vendors_table,
    **static_classes_table,
    **progressive_classes_table,
    **skill_unlocks_table,
    **blueprints_table,
    **runes_table,
    **misc_items_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
