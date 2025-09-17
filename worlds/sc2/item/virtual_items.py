
from typing import TYPE_CHECKING, NamedTuple
import enum
from .item_tables import item_table
from . import item_names

if TYPE_CHECKING:
    from BaseClasses import Item
    from collections import Counter



class LogicEffect(enum.IntFlag):
    NONE = 0
    TERRAN_INFANTRY_ARMOR = enum.auto()
    TERRAN_INFANTRY_WEAPON = enum.auto()
    TERRAN_VEHICLE_ARMOR = enum.auto()
    TERRAN_VEHICLE_WEAPON = enum.auto()
    TERRAN_SHIP_ARMOR = enum.auto()
    TERRAN_SHIP_WEAPON = enum.auto()
    ZERG_MELEE_ATTACK = enum.auto()
    ZERG_RANGED_ATTACK = enum.auto()
    ZERG_GROUND_ARMOR = enum.auto()
    ZERG_AIR_ATTACK = enum.auto()
    ZERG_AIR_ARMOR = enum.auto()
    PROTOSS_GROUND_ARMOR = enum.auto()
    PROTOSS_GROUND_WEAPON = enum.auto()
    PROTOSS_AIR_ARMOR = enum.auto()
    PROTOSS_AIR_WEAPON = enum.auto()
    # Note(phaneros): shield tracking is incomplete when bundling by air/ground; not used by logic
    PROTOSS_SHIELDS = enum.auto()

    TERRAN_DEFENSE_RATING = enum.auto()
    BUNKER_DEFENSE_RATING = enum.auto()
    TVZ_DEFENSE_RATING = enum.auto()

    ZERG_MUTALISK_RATING = enum.auto()
    """
    Checking against 10+N guarantees mutas + N powerful upgrades (+attack, glaives).
    >=14 is competent mutas
    """

    TERRAN_UPGRADE = (
         TERRAN_INFANTRY_WEAPON|TERRAN_INFANTRY_ARMOR
        |TERRAN_VEHICLE_WEAPON|TERRAN_VEHICLE_ARMOR
        |TERRAN_SHIP_WEAPON|TERRAN_SHIP_ARMOR
    ),
    ZERG_UPGRADE = (
         ZERG_MELEE_ATTACK|ZERG_RANGED_ATTACK|ZERG_GROUND_ARMOR
        |ZERG_AIR_ATTACK|ZERG_AIR_ARMOR
    )
    PROTOSS_UPGRADE = (
         PROTOSS_GROUND_WEAPON|PROTOSS_GROUND_ARMOR
        |PROTOSS_AIR_WEAPON|PROTOSS_AIR_ARMOR
        # |PROTOSS_SHIELDS
    )


class LogicSet(NamedTuple):
    """Represents a set of items that achieve a virtual item if combined"""
    items: tuple[str, ...]
    effect: LogicEffect


LOGIC_EFFECTS = {
    # Weapon/armour ups
    item_table[item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON].code: (LogicEffect.TERRAN_INFANTRY_WEAPON, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR].code: (LogicEffect.TERRAN_INFANTRY_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON].code: (LogicEffect.TERRAN_VEHICLE_WEAPON, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR].code: (LogicEffect.TERRAN_VEHICLE_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON].code: (LogicEffect.TERRAN_SHIP_WEAPON, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR].code: (LogicEffect.TERRAN_SHIP_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_WEAPON_UPGRADE].code: (LogicEffect.TERRAN_INFANTRY_WEAPON|LogicEffect.TERRAN_VEHICLE_WEAPON|LogicEffect.TERRAN_SHIP_WEAPON, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE].code: (LogicEffect.TERRAN_INFANTRY_ARMOR|LogicEffect.TERRAN_VEHICLE_ARMOR|LogicEffect.TERRAN_SHIP_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE].code: (LogicEffect.TERRAN_INFANTRY_WEAPON|LogicEffect.TERRAN_INFANTRY_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE].code: (LogicEffect.TERRAN_VEHICLE_WEAPON|LogicEffect.TERRAN_VEHICLE_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_SHIP_UPGRADE].code: (LogicEffect.TERRAN_SHIP_WEAPON|LogicEffect.TERRAN_SHIP_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE].code: (LogicEffect.TERRAN_UPGRADE, 1),
    item_table[item_names.PROGRESSIVE_ZERG_MELEE_ATTACK].code: (LogicEffect.ZERG_MELEE_ATTACK, 1),
    item_table[item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK].code: (LogicEffect.ZERG_RANGED_ATTACK, 1),
    item_table[item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE].code: (LogicEffect.ZERG_GROUND_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_ZERG_FLYER_ATTACK].code: (LogicEffect.ZERG_AIR_ATTACK|LogicEffect.ZERG_MUTALISK_RATING, 1),
    item_table[item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE].code: (LogicEffect.ZERG_AIR_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_ZERG_WEAPON_UPGRADE].code: (LogicEffect.ZERG_MELEE_ATTACK|LogicEffect.ZERG_RANGED_ATTACK|LogicEffect.ZERG_AIR_ATTACK, 1),
    item_table[item_names.PROGRESSIVE_ZERG_ARMOR_UPGRADE].code: (LogicEffect.ZERG_GROUND_ARMOR|LogicEffect.ZERG_AIR_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_ZERG_GROUND_UPGRADE].code: (LogicEffect.ZERG_MELEE_ATTACK|LogicEffect.ZERG_RANGED_ATTACK|LogicEffect.ZERG_GROUND_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_ZERG_FLYER_UPGRADE].code: (LogicEffect.ZERG_AIR_ATTACK|LogicEffect.ZERG_AIR_ARMOR|LogicEffect.ZERG_MUTALISK_RATING, 1),
    item_table[item_names.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE].code: (LogicEffect.ZERG_UPGRADE|LogicEffect.ZERG_MUTALISK_RATING, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON].code: (LogicEffect.PROTOSS_GROUND_WEAPON, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR].code: (LogicEffect.PROTOSS_GROUND_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_SHIELDS].code: (LogicEffect.PROTOSS_SHIELDS, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON].code: (LogicEffect.PROTOSS_AIR_WEAPON, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR].code: (LogicEffect.PROTOSS_AIR_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE].code: (LogicEffect.PROTOSS_GROUND_WEAPON|LogicEffect.PROTOSS_AIR_WEAPON, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE].code: (LogicEffect.PROTOSS_GROUND_ARMOR|LogicEffect.PROTOSS_AIR_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE].code: (LogicEffect.PROTOSS_GROUND_WEAPON|LogicEffect.PROTOSS_GROUND_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE].code: (LogicEffect.PROTOSS_AIR_WEAPON|LogicEffect.PROTOSS_AIR_ARMOR, 1),
    item_table[item_names.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE].code: (LogicEffect.PROTOSS_UPGRADE, 1),

    # General defense rating
    item_table[item_names.SIEGE_TANK].code: (LogicEffect.TERRAN_DEFENSE_RATING, 5),
    item_table[item_names.PLANETARY_FORTRESS].code: (LogicEffect.TERRAN_DEFENSE_RATING, 3),
    item_table[item_names.PERDITION_TURRET].code: (LogicEffect.TERRAN_DEFENSE_RATING|LogicEffect.TVZ_DEFENSE_RATING, 2),
    item_table[item_names.DEVASTATOR_TURRET].code: (LogicEffect.TERRAN_DEFENSE_RATING, 2),
    item_table[item_names.LIBERATOR].code: (LogicEffect.TERRAN_DEFENSE_RATING, 4),  # adjusted to 2 vs zerg
    item_table[item_names.WIDOW_MINE].code: (LogicEffect.TERRAN_DEFENSE_RATING, 1),

    item_table[item_names.HIVE_MIND_EMULATOR].code: (LogicEffect.TVZ_DEFENSE_RATING, 3),
    item_table[item_names.PSI_DISRUPTER].code: (LogicEffect.TVZ_DEFENSE_RATING, 3),

    # Bunker component of defense rating (this contribution gets capped to 3)
    item_table[item_names.MARINE].code: (LogicEffect.BUNKER_DEFENSE_RATING, 3),
    item_table[item_names.DOMINION_TROOPER].code: (LogicEffect.BUNKER_DEFENSE_RATING, 3),
    item_table[item_names.MARAUDER].code: (LogicEffect.BUNKER_DEFENSE_RATING, 3),
    item_table[item_names.FIREBAT].code: (LogicEffect.BUNKER_DEFENSE_RATING, 1),
    item_table[item_names.GHOST].code: (LogicEffect.BUNKER_DEFENSE_RATING, 1),
    item_table[item_names.SPECTRE].code: (LogicEffect.BUNKER_DEFENSE_RATING, 1),

    # Mutalisk rating
    item_table[item_names.MUTALISK].code: (LogicEffect.ZERG_MUTALISK_RATING, 10),
    item_table[item_names.MUTALISK_SEVERING_GLAIVE].code: (LogicEffect.ZERG_MUTALISK_RATING, 1),
    item_table[item_names.MUTALISK_SUNDERING_GLAIVE].code: (LogicEffect.ZERG_MUTALISK_RATING, 1),
    item_table[item_names.MUTALISK_VICIOUS_GLAIVE].code: (LogicEffect.ZERG_MUTALISK_RATING, 1),
}
LOGIC_MINIMUM_COUNTERS = {
    # When the key is added or removed,
    # the counter for value's name is recalculated as the minimum value of all of its component bits.
    item_table[item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_WEAPON_UPGRADE].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_SHIP_UPGRADE].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE].code: LogicEffect.TERRAN_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON].code: LogicEffect.PROTOSS_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR].code: LogicEffect.PROTOSS_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON].code: LogicEffect.PROTOSS_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR].code: LogicEffect.PROTOSS_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE].code: LogicEffect.PROTOSS_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE].code: LogicEffect.PROTOSS_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE].code: LogicEffect.PROTOSS_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE].code: LogicEffect.PROTOSS_UPGRADE,
    item_table[item_names.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE].code: LogicEffect.PROTOSS_UPGRADE,
}


def after_add_item(inventory: "Counter[str]", item: "Item") -> None:
    effects, count = LOGIC_EFFECTS.get(item.code, (LogicEffect.NONE, 0))
    if count:
        for effect in effects:
            inventory[effect.name] += count
    min_counter = LOGIC_MINIMUM_COUNTERS.get(item.code)
    if min_counter:
        inventory[min_counter.name] = min(
            inventory[effect.name] for effect in min_counter
        )

def after_remove_item(inventory: "Counter[str]", item: "Item") -> None:
    effects, count = LOGIC_EFFECTS.get(item.code, (LogicEffect.NONE, 0))
    if count:
        for effect in effects:
            inventory[effect.name] -= count
    min_counter = LOGIC_MINIMUM_COUNTERS.get(item.code)
    if min_counter:
        if inventory[min_counter.name] > inventory[item.name]:
            inventory[min_counter.name] = inventory[item.name]
