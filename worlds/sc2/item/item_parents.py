"""
Utilities for telling item parentage hierarchy.
ItemData in item_tables.py will point from child item -> parent rule.
Rules have a `parent_items()` method which links rule -> parent items.
Rules may be more complex than all or any items being present. Call them to determine if they are satisfied.
"""

from typing import Dict, List, Iterable, Sequence, Optional, TYPE_CHECKING
import abc
from . import item_names, parent_names, item_tables, item_groups

if TYPE_CHECKING:
    from ..options import Starcraft2Options


class PresenceRule(abc.ABC):
    """Contract for a parent presence rule. This should be a protocol in Python 3.10+"""
    constraint_group: Optional[str]
    """Identifies the group this item rule is a part of, subject to min/max upgrades per unit"""
    display_string: str
    """Main item to count as the parent for min/max upgrades per unit purposes"""
    @abc.abstractmethod
    def __call__(self, inventory: Iterable[str], options: 'Starcraft2Options') -> bool: ...
    @abc.abstractmethod
    def parent_items(self) -> Sequence[str]: ...


class ItemPresent(PresenceRule):
    def __init__(self, item_name: str) -> None:
        self.item_name = item_name
        self.constraint_group = item_name
        self.display_string = item_name

    def __call__(self, inventory: Iterable[str], options: 'Starcraft2Options') -> bool:
        return self.item_name in inventory

    def parent_items(self) -> List[str]:
        return [self.item_name]


class AnyOf(PresenceRule):
    def __init__(self, group: Iterable[str], main_item: Optional[str] = None, display_string: Optional[str] = None) -> None:
        self.group = set(group)
        self.constraint_group = main_item
        self.display_string = display_string or main_item or ' | '.join(group)

    def __call__(self, inventory: Iterable[str], options: 'Starcraft2Options') -> bool:
        return len(self.group.intersection(inventory)) > 0

    def parent_items(self) -> List[str]:
        return sorted(self.group)


class AllOf(PresenceRule):
    def __init__(self, group: Iterable[str], main_item: Optional[str] = None) -> None:
        self.group = set(group)
        self.constraint_group = main_item
        self.display_string = main_item or ' & '.join(group)

    def __call__(self, inventory: Iterable[str], options: 'Starcraft2Options') -> bool:
        return len(self.group.intersection(inventory)) == len(self.group)

    def parent_items(self) -> List[str]:
        return sorted(self.group)


class AnyOfGroupAndOneOtherItem(PresenceRule):
    def __init__(self, group: Iterable[str], item_name: str) -> None:
        self.group = set(group)
        self.item_name = item_name
        self.constraint_group = item_name
        self.display_string = item_name

    def __call__(self, inventory: Iterable[str], options: 'Starcraft2Options') -> bool:
        return (len(self.group.intersection(inventory)) > 0) and self.item_name in inventory

    def parent_items(self) -> List[str]:
        return sorted(self.group) + [self.item_name]


class MorphlingOrItem(PresenceRule):
    def __init__(self, item_name: str, has_parent: bool = True) -> None:
        self.item_name = item_name
        self.constraint_group = None  # Keep morphs from counting towards the parent unit's upgrade count
        self.display_string = f'{item_name} Morphs'

    def __call__(self, inventory: Iterable[str], options: 'Starcraft2Options') -> bool:
        return (options.enable_morphling.value != 0) or self.item_name in inventory

    def parent_items(self) -> List[str]:
        return [self.item_name]


class MorphlingOrAnyOf(PresenceRule):
    def __init__(self, group: Iterable[str], display_string: str, main_item: Optional[str] = None) -> None:
        self.group = set(group)
        self.constraint_group = main_item
        self.display_string = display_string

    def __call__(self, inventory: Iterable[str], options: 'Starcraft2Options') -> bool:
        return (options.enable_morphling.value != 0) or (len(self.group.intersection(inventory)) > 0)

    def parent_items(self) -> List[str]:
        return sorted(self.group)


parent_present: Dict[str, PresenceRule] = {
    item_name: ItemPresent(item_name)
    for item_name in item_tables.item_table
}

# Terran
parent_present[parent_names.DOMINION_TROOPER_WEAPONS] = AnyOf([
    item_names.DOMINION_TROOPER_B2_HIGH_CAL_LMG,
    item_names.DOMINION_TROOPER_CPO7_SALAMANDER_FLAMETHROWER,
    item_names.DOMINION_TROOPER_HAILSTORM_LAUNCHER,
], main_item=item_names.DOMINION_TROOPER)
parent_present[parent_names.INFANTRY_UNITS] = AnyOf(item_groups.barracks_units, display_string='Terran Infantry')
parent_present[parent_names.INFANTRY_WEAPON_UNITS] = AnyOf(item_groups.barracks_wa_group, display_string='Terran Infantry')
parent_present[parent_names.ORBITAL_COMMAND_AND_PLANETARY] = AnyOfGroupAndOneOtherItem(
    item_groups.orbital_command_abilities,
    item_names.PLANETARY_FORTRESS,
)
parent_present[parent_names.SIEGE_TANK_AND_TRANSPORT] = AnyOfGroupAndOneOtherItem(
    (item_names.MEDIVAC, item_names.HERCULES),
    item_names.SIEGE_TANK,
)
parent_present[parent_names.SIEGE_TANK_AND_MEDIVAC] = AllOf((item_names.SIEGE_TANK, item_names.MEDIVAC), item_names.SIEGE_TANK)
parent_present[parent_names.SPIDER_MINE_SOURCE] = AnyOf(item_groups.spider_mine_sources, display_string='Spider Mines')
parent_present[parent_names.STARSHIP_UNITS] = AnyOf(item_groups.starport_units, display_string='Terran Starships')
parent_present[parent_names.STARSHIP_WEAPON_UNITS] = AnyOf(item_groups.starport_wa_group, display_string='Terran Starships')
parent_present[parent_names.VEHICLE_UNITS] = AnyOf(item_groups.factory_units, display_string='Terran Vehicles')
parent_present[parent_names.VEHICLE_WEAPON_UNITS] = AnyOf(item_groups.factory_wa_group, display_string='Terran Vehicles')
parent_present[parent_names.TERRAN_MERCENARIES] = AnyOf(item_groups.terran_mercenaries, display_string='Terran Mercenaries')

# Zerg
parent_present[parent_names.ANY_NYDUS_WORM] = AnyOf((item_names.NYDUS_WORM, item_names.ECHIDNA_WORM), item_names.NYDUS_WORM)
parent_present[parent_names.BANELING_SOURCE] = AnyOf(
    (item_names.ZERGLING_BANELING_ASPECT, item_names.KERRIGAN_SPAWN_BANELINGS),
    item_names.ZERGLING_BANELING_ASPECT,
)
parent_present[parent_names.INFESTED_UNITS] = AnyOf(item_groups.infterr_units, display_string='Infested')
parent_present[parent_names.INFESTED_FACTORY_OR_STARPORT] = AnyOf(
    (item_names.INFESTED_DIAMONDBACK, item_names.INFESTED_SIEGE_TANK, item_names.INFESTED_LIBERATOR, item_names.INFESTED_BANSHEE, item_names.BULLFROG)
)
parent_present[parent_names.MORPH_SOURCE_AIR] = MorphlingOrAnyOf((item_names.MUTALISK, item_names.CORRUPTOR), "Mutalisk/Corruptor Morphs")
parent_present[parent_names.MORPH_SOURCE_ROACH] = MorphlingOrItem(item_names.ROACH)
parent_present[parent_names.MORPH_SOURCE_ZERGLING] = MorphlingOrItem(item_names.ZERGLING)
parent_present[parent_names.MORPH_SOURCE_HYDRALISK] = MorphlingOrItem(item_names.HYDRALISK)
parent_present[parent_names.MORPH_SOURCE_ULTRALISK] = MorphlingOrItem(item_names.ULTRALISK)
parent_present[parent_names.ZERG_UPROOTABLE_BUILDINGS] = AnyOf(
    (item_names.SPINE_CRAWLER, item_names.SPORE_CRAWLER, item_names.INFESTED_MISSILE_TURRET, item_names.INFESTED_BUNKER),
)
parent_present[parent_names.ZERG_MELEE_ATTACKER] = AnyOf(item_groups.zerg_melee_wa, display_string='Zerg Ground')
parent_present[parent_names.ZERG_MISSILE_ATTACKER] = AnyOf(item_groups.zerg_ranged_wa, display_string='Zerg Ground')
parent_present[parent_names.ZERG_CARAPACE_UNIT] = AnyOf(item_groups.zerg_ground_units, display_string='Zerg Flyers')
parent_present[parent_names.ZERG_FLYING_UNIT] = AnyOf(item_groups.zerg_air_units, display_string='Zerg Flyers')
parent_present[parent_names.ZERG_MERCENARIES] = AnyOf(item_groups.zerg_mercenaries, display_string='Zerg Mercenaries')
parent_present[parent_names.ZERG_OUROBOUROS_CONDITION] = AnyOfGroupAndOneOtherItem(
    (item_names.ZERGLING, item_names.ROACH, item_names.HYDRALISK, item_names.ABERRATION),
    item_names.ECHIDNA_WORM
)

# Protoss
parent_present[parent_names.ARCHON_SOURCE] = AnyOf(
    (item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT_ARCHON_MERGE, item_names.DARK_TEMPLAR_ARCHON_MERGE),
    main_item="Archon",
)
parent_present[parent_names.CARRIER_CLASS] = AnyOf(
    (item_names.CARRIER, item_names.TRIREME, item_names.SKYLORD),
    main_item=item_names.CARRIER,
)
parent_present[parent_names.CARRIER_OR_TRIREME] = AnyOf(
    (item_names.CARRIER, item_names.TRIREME),
    main_item=item_names.CARRIER,
)
parent_present[parent_names.DARK_ARCHON_SOURCE] = AnyOf(
    (item_names.DARK_ARCHON, item_names.DARK_TEMPLAR_DARK_ARCHON_MELD),
    main_item=item_names.DARK_ARCHON,
)
parent_present[parent_names.DARK_TEMPLAR_CLASS] = AnyOf(
    (item_names.DARK_TEMPLAR, item_names.AVENGER, item_names.BLOOD_HUNTER),
    main_item=item_names.DARK_TEMPLAR,
)
parent_present[parent_names.STORM_CASTER] = AnyOf(
    (item_names.HIGH_TEMPLAR, item_names.SIGNIFIER),
    main_item=item_names.HIGH_TEMPLAR,
)
parent_present[parent_names.IMMORTAL_OR_ANNIHILATOR] = AnyOf(
    (item_names.IMMORTAL, item_names.ANNIHILATOR),
    main_item=item_names.IMMORTAL,
)
parent_present[parent_names.PHOENIX_CLASS] = AnyOf(
    (item_names.PHOENIX, item_names.MIRAGE, item_names.SKIRMISHER),
    main_item=item_names.PHOENIX,
)
parent_present[parent_names.SENTRY_CLASS] = AnyOf(
    (item_names.SENTRY, item_names.ENERGIZER, item_names.HAVOC),
    main_item=item_names.SENTRY,
)
parent_present[parent_names.SENTRY_CLASS_OR_SHIELD_BATTERY] = AnyOf(
    (item_names.SENTRY, item_names.ENERGIZER, item_names.HAVOC, item_names.SHIELD_BATTERY),
    main_item=item_names.SENTRY,
)
parent_present[parent_names.STALKER_CLASS] = AnyOf(
    (item_names.STALKER, item_names.SLAYER, item_names.INSTIGATOR),
    main_item=item_names.STALKER,
)
parent_present[parent_names.SUPPLICANT_AND_ASCENDANT] = AllOf(
    (item_names.SUPPLICANT, item_names.ASCENDANT),
    main_item=item_names.ASCENDANT,
)
parent_present[parent_names.VOID_RAY_CLASS] = AnyOf(
    (item_names.VOID_RAY, item_names.DESTROYER, item_names.PULSAR, item_names.DAWNBRINGER),
    main_item=item_names.VOID_RAY,
)
parent_present[parent_names.ZEALOT_OR_SENTINEL_OR_CENTURION] = AnyOf(
    (item_names.ZEALOT, item_names.SENTINEL, item_names.CENTURION),
    main_item=item_names.ZEALOT,
)
parent_present[parent_names.SCOUT_CLASS] = AnyOf(
    (item_names.SCOUT, item_names.OPPRESSOR, item_names.CALADRIUS, item_names.MISTWING),
    main_item=item_names.SCOUT,
)
parent_present[parent_names.SCOUT_OR_OPPRESSOR_OR_MISTWING] = AnyOf(
    (item_names.SCOUT, item_names.OPPRESSOR, item_names.MISTWING),
    main_item=item_names.SCOUT,
)
parent_present[parent_names.PROTOSS_STATIC_DEFENSE] = AnyOf(
    (item_names.NEXUS_OVERCHARGE, item_names.PHOTON_CANNON, item_names.KHAYDARIN_MONOLITH, item_names.SHIELD_BATTERY),
    main_item=item_names.PHOTON_CANNON,
)
parent_present[parent_names.PROTOSS_ATTACKING_BUILDING] = AnyOf(
    (item_names.NEXUS_OVERCHARGE, item_names.PHOTON_CANNON, item_names.KHAYDARIN_MONOLITH),
    main_item=item_names.PHOTON_CANNON,
)


parent_id_to_children: Dict[str, Sequence[str]] = {}
"""Parent identifier to child items. Only contains parent rules with children."""
child_item_to_parent_items: Dict[str, Sequence[str]] = {}
"""Child item name to all parent items that can possibly affect its presence rule. Populated for all item names."""

parent_item_to_ids: Dict[str, Sequence[str]] = {}
"""Parent item to parent identifiers it affects. Populated for all items and parent IDs."""
parent_item_to_children: Dict[str, Sequence[str]] = {}
"""Parent item to child item names. Populated for all items and parent IDs."""
item_upgrade_groups: Dict[str, Sequence[str]] = {}
"""Mapping of upgradable item group -> child items. Only populated for groups with child items."""
# Note(mm): "All items" promise satisfied by the basic ItemPresent auto-generated rules

def _init() -> None:
    for item_name, item_data in item_tables.item_table.items():
        if item_data.parent is None:
            continue
        parent_id_to_children.setdefault(item_data.parent, []).append(item_name)  # type: ignore
        child_item_to_parent_items[item_name] = parent_present[item_data.parent].parent_items()

    for parent_id, presence_func in parent_present.items():
        for parent_item in presence_func.parent_items():
            parent_item_to_ids.setdefault(parent_item, []).append(parent_id)  # type: ignore
            parent_item_to_children.setdefault(parent_item, []).extend(parent_id_to_children.get(parent_id, []))  # type: ignore
        if presence_func.constraint_group is not None and parent_id_to_children.get(parent_id):
            item_upgrade_groups.setdefault(presence_func.constraint_group, []).extend(parent_id_to_children[parent_id])  # type: ignore

_init()
