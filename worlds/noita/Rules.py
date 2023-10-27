from typing import List, NamedTuple, Set, TYPE_CHECKING

from BaseClasses import CollectionState
from . import Items, Locations
from .Options import BossesAsChecks, VictoryCondition
from worlds.generic import Rules as GenericRules

if TYPE_CHECKING:
    from . import NoitaWorld
else:
    NoitaWorld = object


class EntranceLock(NamedTuple):
    source: str
    destination: str
    event: str
    items_needed: int


entrance_locks: List[EntranceLock] = [
    EntranceLock("Mines", "Coal Pits Holy Mountain", "Portal to Holy Mountain 1", 1),
    EntranceLock("Coal Pits", "Snowy Depths Holy Mountain", "Portal to Holy Mountain 2", 2),
    EntranceLock("Snowy Depths", "Hiisi Base Holy Mountain", "Portal to Holy Mountain 3", 3),
    EntranceLock("Hiisi Base", "Underground Jungle Holy Mountain", "Portal to Holy Mountain 4", 4),
    EntranceLock("Underground Jungle", "Vault Holy Mountain", "Portal to Holy Mountain 5", 5),
    EntranceLock("The Vault", "Temple of the Art Holy Mountain", "Portal to Holy Mountain 6", 6),
    EntranceLock("Temple of the Art", "Laboratory Holy Mountain", "Portal to Holy Mountain 7", 7),
]


holy_mountain_regions: List[str] = [
    "Coal Pits Holy Mountain",
    "Snowy Depths Holy Mountain",
    "Hiisi Base Holy Mountain",
    "Underground Jungle Holy Mountain",
    "Vault Holy Mountain",
    "Temple of the Art Holy Mountain",
    "Laboratory Holy Mountain",
]


wand_tiers: List[str] = [
    "Wand (Tier 1)",    # Coal Pits
    "Wand (Tier 2)",    # Snowy Depths
    "Wand (Tier 3)",    # Hiisi Base
    "Wand (Tier 4)",    # Underground Jungle
    "Wand (Tier 5)",    # The Vault
    "Wand (Tier 6)",    # Temple of the Art
]


items_hidden_from_shops: Set[str] = {"Gold (200)", "Gold (1000)", "Potion", "Random Potion", "Secret Potion",
                                     "Chaos Die", "Greed Die", "Kammi", "Refreshing Gourd", "Sädekivi", "Broken Wand",
                                     "Powder Pouch"}


perk_list: List[str] = list(filter(Items.item_is_perk, Items.item_table.keys()))


# ----------------
# Helper Functions
# ----------------


def has_perk_count(state: CollectionState, player: int, amount: int) -> bool:
    return sum(state.item_count(perk, player) for perk in perk_list) >= amount


def has_orb_count(state: CollectionState, player: int, amount: int) -> bool:
    return state.item_count("Orb", player) >= amount


def forbid_items_at_location(world: NoitaWorld, location_name: str, items: Set[str]):
    location = world.multiworld.get_location(location_name, world.player)
    GenericRules.forbid_items_for_player(location, items, world.player)


# ----------------
# Rule Functions
# ----------------


# Prevent gold and potions from appearing as purchasable items in shops (because physics will destroy them)
def ban_items_from_shops(world: NoitaWorld) -> None:
    for location_name in Locations.location_name_to_id.keys():
        if "Shop Item" in location_name:
            forbid_items_at_location(world, location_name, items_hidden_from_shops)


# Prevent high tier wands from appearing in early Holy Mountain shops
def ban_early_high_tier_wands(world: NoitaWorld) -> None:
    for i, region_name in enumerate(holy_mountain_regions):
        wands_to_forbid = set(wand_tiers[i+1:])

        locations_in_region = Locations.location_region_mapping[region_name].keys()
        for location_name in locations_in_region:
            forbid_items_at_location(world, location_name, wands_to_forbid)

    # Prevent high tier wands from appearing in the Secret shop
    wands_to_forbid = set(wand_tiers[3:])
    locations_in_region = Locations.location_region_mapping["Secret Shop"].keys()
    for location_name in locations_in_region:
        forbid_items_at_location(world, location_name, wands_to_forbid)


def lock_holy_mountains_into_spheres(world: NoitaWorld) -> None:
    for lock in entrance_locks:
        location = world.multiworld.get_entrance(f"From {lock.source} To {lock.destination}", world.player)
        GenericRules.set_rule(location, lambda state, evt=lock.event: state.has(evt, world.player))


def holy_mountain_unlock_conditions(world: NoitaWorld) -> None:
    victory_condition = world.options.victory_condition.value
    for lock in entrance_locks:
        location = world.multiworld.get_location(lock.event, world.player)

        if victory_condition == VictoryCondition.option_greed_ending:
            location.access_rule = lambda state, items_needed=lock.items_needed: (
                has_perk_count(state, world.player, items_needed//2)
            )
        elif victory_condition == VictoryCondition.option_pure_ending:
            location.access_rule = lambda state, items_needed=lock.items_needed: (
                has_perk_count(state, world.player, items_needed//2) and
                has_orb_count(state, world.player, items_needed)
            )
        elif victory_condition == VictoryCondition.option_peaceful_ending:
            location.access_rule = lambda state, items_needed=lock.items_needed: (
                has_perk_count(state, world.player, items_needed//2) and
                has_orb_count(state, world.player, items_needed * 3)
            )


def biome_unlock_conditions(world: NoitaWorld):
    lukki_entrances = world.multiworld.get_region("Lukki Lair", world.player).entrances
    magical_entrances = world.multiworld.get_region("Magical Temple", world.player).entrances
    wizard_entrances = world.multiworld.get_region("Wizards' Den", world.player).entrances
    for entrance in lukki_entrances:
        entrance.access_rule = lambda state: state.has("Melee Immunity Perk", world.player) and\
                                             state.has("All-Seeing Eye Perk", world.player)
    for entrance in magical_entrances:
        entrance.access_rule = lambda state: state.has("All-Seeing Eye Perk", world.player)
    for entrance in wizard_entrances:
        entrance.access_rule = lambda state: state.has("All-Seeing Eye Perk", world.player)


def victory_unlock_conditions(world: NoitaWorld) -> None:
    victory_condition = world.options.victory_condition.value
    victory_location = world.multiworld.get_location("Victory", world.player)

    if victory_condition == VictoryCondition.option_pure_ending:
        victory_location.access_rule = lambda state: has_orb_count(state, world.player, 11)
    elif victory_condition == VictoryCondition.option_peaceful_ending:
        victory_location.access_rule = lambda state: has_orb_count(state, world.player, 33)


# ----------------
# Main Function
# ----------------


def create_all_rules(world: NoitaWorld) -> None:
    ban_items_from_shops(world)
    ban_early_high_tier_wands(world)
    lock_holy_mountains_into_spheres(world)
    holy_mountain_unlock_conditions(world)
    biome_unlock_conditions(world)
    victory_unlock_conditions(world)

    # Prevent the Map perk (used to find Toveri) from being on Toveri (boss)
    if world.options.bosses_as_checks.value >= BossesAsChecks.option_all_bosses:
        forbid_items_at_location(world, "Toveri", {"Spatial Awareness Perk"})
