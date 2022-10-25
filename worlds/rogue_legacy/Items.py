import typing

from BaseClasses import Item
from .definitions import ItemNames


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


class LegacyItem(Item):
    game: str = "Rogue Legacy"


# Separate tables for each type of item.
vendors_table = {
    ItemNames.blacksmith: ItemData(90000, True),
    ItemNames.enchantress: ItemData(90001, True),
    ItemNames.architect: ItemData(90002, False),
}

static_classes_table = {
    ItemNames.knight: ItemData(90080, False),
    ItemNames.paladin: ItemData(90081, False),
    ItemNames.mage: ItemData(90082, False),
    ItemNames.archmage: ItemData(90083, False),
    ItemNames.barbarian: ItemData(90084, False),
    ItemNames.barbarian_king: ItemData(90085, False),
    ItemNames.knave: ItemData(90086, False),
    ItemNames.assassin: ItemData(90087, False),
    ItemNames.shinobi: ItemData(90088, False),
    ItemNames.hokage: ItemData(90089, False),
    ItemNames.miner: ItemData(90090, False),
    ItemNames.spelunker: ItemData(90091, False),
    ItemNames.lich: ItemData(90092, False),
    ItemNames.lich_king: ItemData(90093, False),
    ItemNames.spellthief: ItemData(90094, False),
    ItemNames.spellsword: ItemData(90095, False),
    ItemNames.dragon: ItemData(90096, False),
    ItemNames.traitor: ItemData(90097, False),
}

progressive_classes_table = {
    ItemNames.progressive_knight: ItemData(90003, False, 2),
    ItemNames.progressive_mage: ItemData(90004, False, 2),
    ItemNames.progressive_barbarian: ItemData(90005, False, 2),
    ItemNames.progressive_knave: ItemData(90006, False, 2),
    ItemNames.progressive_shinobi: ItemData(90007, False, 2),
    ItemNames.progressive_miner: ItemData(90008, False, 2),
    ItemNames.progressive_lich: ItemData(90009, False, 2),
    ItemNames.progressive_spellthief: ItemData(90010, False, 2),
}

configurable_skill_unlocks_table = {
    ItemNames.health: ItemData(90013, True, 15),
    ItemNames.mana: ItemData(90014, True, 15),
    ItemNames.attack: ItemData(90015, True, 15),
    ItemNames.magic_damage: ItemData(90016, True, 15),
    ItemNames.armor: ItemData(90017, True, 10),
    ItemNames.equip: ItemData(90018, True, 10),
    ItemNames.crit_chance: ItemData(90019, False, 5),
    ItemNames.crit_damage: ItemData(90020, False, 5),
}

skill_unlocks_table = {
    ItemNames.down_strike: ItemData(90021, False),
    ItemNames.gold_gain: ItemData(90022, False),
    ItemNames.potion_efficiency: ItemData(90023, False),
    ItemNames.invulnerability_time: ItemData(90024, False),
    ItemNames.mana_cost_down: ItemData(90025, False),
    ItemNames.death_defiance: ItemData(90026, False),
    ItemNames.haggling: ItemData(90027, False),
    ItemNames.random_children: ItemData(90028, False),
}

blueprints_table = {
    ItemNames.squire_blueprints: ItemData(90040, False),
    ItemNames.silver_blueprints: ItemData(90041, False),
    ItemNames.guardian_blueprints: ItemData(90042, False),
    ItemNames.imperial_blueprints: ItemData(90043, False),
    ItemNames.royal_blueprints: ItemData(90044, False),
    ItemNames.knight_blueprints: ItemData(90045, False),
    ItemNames.ranger_blueprints: ItemData(90046, False),
    ItemNames.sky_blueprints: ItemData(90047, False),
    ItemNames.dragon_blueprints: ItemData(90048, False),
    ItemNames.slayer_blueprints: ItemData(90049, False),
    ItemNames.blood_blueprints: ItemData(90050, False),
    ItemNames.sage_blueprints: ItemData(90051, False),
    ItemNames.retribution_blueprints: ItemData(90052, False),
    ItemNames.holy_blueprints: ItemData(90053, False),
    ItemNames.dark_blueprints: ItemData(90054, False),
}

progressive_blueprint_table = {
    ItemNames.progressive_blueprints: ItemData(90055, False),
}

runes_table = {
    ItemNames.vault_runes: ItemData(90060, False),
    ItemNames.sprint_runes: ItemData(90061, False),
    ItemNames.vampire_runes: ItemData(90062, False),
    ItemNames.sky_runes: ItemData(90063, False),
    ItemNames.siphon_runes: ItemData(90064, False),
    ItemNames.retaliation_runes: ItemData(90065, False),
    ItemNames.bounty_runes: ItemData(90066, False),
    ItemNames.haste_runes: ItemData(90067, False),
    ItemNames.curse_runes: ItemData(90068, False),
    ItemNames.grace_runes: ItemData(90069, False),
    ItemNames.balance_runes: ItemData(90070, False),
}

misc_items_table = {
    ItemNames.trip_stat_increase: ItemData(90030, False),
    ItemNames.gold_1000: ItemData(90031, False),
    ItemNames.gold_3000: ItemData(90032, False),
    ItemNames.gold_5000: ItemData(90033, False),
    # ItemName.rage_trap: ItemData(90034, False),
}

# Complete item table.
item_table = {
    **vendors_table,
    **static_classes_table,
    **progressive_classes_table,
    **configurable_skill_unlocks_table,
    **skill_unlocks_table,
    **blueprints_table,
    **progressive_blueprint_table,
    **runes_table,
    **misc_items_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
