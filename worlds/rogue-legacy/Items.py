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


# Separate tables for each type of item.
vendors_table = {
    ItemName.blacksmith: ItemData(90000, True),
    ItemName.enchantress: ItemData(90001, True),
    ItemName.architect: ItemData(90002, False),
}

static_classes_table = {
    ItemName.knight: ItemData(90080, False),
    ItemName.paladin: ItemData(90081, False),
    ItemName.mage: ItemData(90082, False),
    ItemName.archmage: ItemData(90083, False),
    ItemName.barbarian: ItemData(90084, False),
    ItemName.barbarian_king: ItemData(90085, False),
    ItemName.knave: ItemData(90086, False),
    ItemName.assassin: ItemData(90087, False),
    ItemName.shinobi: ItemData(90088, False),
    ItemName.hokage: ItemData(90089, False),
    ItemName.miner: ItemData(90090, False),
    ItemName.spelunker: ItemData(90091, False),
    ItemName.lich: ItemData(90092, False),
    ItemName.lich_king: ItemData(90093, False),
    ItemName.spellthief: ItemData(90094, False),
    ItemName.spellsword: ItemData(90095, False),
    ItemName.dragon: ItemData(90096, False),
    ItemName.traitor: ItemData(90097, False),
}

progressive_classes_table = {
    ItemName.progressive_knight: ItemData(90003, False, 2),
    ItemName.progressive_mage: ItemData(90004, False, 2),
    ItemName.progressive_barbarian: ItemData(90005, False, 2),
    ItemName.progressive_knave: ItemData(90006, False, 2),
    ItemName.progressive_shinobi: ItemData(90007, False, 2),
    ItemName.progressive_miner: ItemData(90008, False, 2),
    ItemName.progressive_lich: ItemData(90009, False, 2),
    ItemName.progressive_spellthief: ItemData(90010, False, 2),
}

configurable_skill_unlocks_table = {
    ItemName.health: ItemData(90013, True, 15),
    ItemName.mana: ItemData(90014, True, 15),
    ItemName.attack: ItemData(90015, True, 15),
    ItemName.magic_damage: ItemData(90016, True, 15),
    ItemName.armor: ItemData(90017, True, 10),
    ItemName.equip: ItemData(90018, True, 10),
    ItemName.crit_chance: ItemData(90019, False, 5),
    ItemName.crit_damage: ItemData(90020, False, 5),
}

skill_unlocks_table = {
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
    ItemName.squire_blueprints: ItemData(90040, False),
    ItemName.silver_blueprints: ItemData(90041, False),
    ItemName.guardian_blueprints: ItemData(90042, False),
    ItemName.imperial_blueprints: ItemData(90043, False),
    ItemName.royal_blueprints: ItemData(90044, False),
    ItemName.knight_blueprints: ItemData(90045, False),
    ItemName.ranger_blueprints: ItemData(90046, False),
    ItemName.sky_blueprints: ItemData(90047, False),
    ItemName.dragon_blueprints: ItemData(90048, False),
    ItemName.slayer_blueprints: ItemData(90049, False),
    ItemName.blood_blueprints: ItemData(90050, False),
    ItemName.sage_blueprints: ItemData(90051, False),
    ItemName.retribution_blueprints: ItemData(90052, False),
    ItemName.holy_blueprints: ItemData(90053, False),
    ItemName.dark_blueprints: ItemData(90054, False),
}

progressive_blueprint_table = {
    ItemName.progressive_blueprints: ItemData(90055, False),
}

runes_table = {
    ItemName.vault_runes: ItemData(90060, False),
    ItemName.sprint_runes: ItemData(90061, False),
    ItemName.vampire_runes: ItemData(90062, False),
    ItemName.sky_runes: ItemData(90063, False),
    ItemName.siphon_runes: ItemData(90064, False),
    ItemName.retaliation_runes: ItemData(90065, False),
    ItemName.bounty_runes: ItemData(90066, False),
    ItemName.haste_runes: ItemData(90067, False),
    ItemName.curse_runes: ItemData(90068, False),
    ItemName.grace_runes: ItemData(90069, False),
    ItemName.balance_runes: ItemData(90070, False),
}

misc_items_table = {
    ItemName.trip_stat_increase: ItemData(90030, False),
    ItemName.gold_1000: ItemData(90031, False),
    ItemName.gold_3000: ItemData(90032, False),
    ItemName.gold_5000: ItemData(90033, False),
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
