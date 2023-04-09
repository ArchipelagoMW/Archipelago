from BaseClasses import MultiWorld, CollectionState
from typing import List, NamedTuple, Set

from worlds.generic import Rules as GenericRules
from . import Locations, Options, Items


holy_mountain_regions: List[str] = [
    "Holy Mountain 1 (To Coal Pits)",
    "Holy Mountain 2 (To Snowy Depths)",
    "Holy Mountain 3 (To Hiisi Base)",
    "Holy Mountain 4 (To Underground Jungle)",
    "Holy Mountain 5 (To The Vault)",
    "Holy Mountain 6 (To Temple of the Art)",
    "Holy Mountain 7 (To The Laboratory)",
]


class EntranceLock(NamedTuple):
    source: str
    destination: str
    event: str
    items_needed: int


entrance_locks: List[EntranceLock] = [
    EntranceLock("Mines", "Holy Mountain 1 (To Coal Pits)", "Portal to Holy Mountain 1", 1),
    EntranceLock("Coal Pits", "Holy Mountain 2 (To Snowy Depths)", "Portal to Holy Mountain 2", 2),
    EntranceLock("Snowy Depths", "Holy Mountain 3 (To Hiisi Base)", "Portal to Holy Mountain 3", 3),
    EntranceLock("Hiisi Base", "Holy Mountain 4 (To Underground Jungle)", "Portal to Holy Mountain 4", 4),
    EntranceLock("Underground Jungle", "Holy Mountain 5 (To The Vault)", "Portal to Holy Mountain 5", 5),
    EntranceLock("The Vault", "Holy Mountain 6 (To Temple of the Art)", "Portal to Holy Mountain 6", 6),
    EntranceLock("Temple of the Art", "Holy Mountain 7 (To The Laboratory)", "Portal to Holy Mountain 7", 7),
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


def get_perk_count(state: CollectionState, player: int) -> int:
    perk_list: List[str] = list(filter(Items.item_is_perk, Items.item_table.keys()))
    perk_count = 0
    for perk in perk_list:
        perk_count = perk_count + state.item_count(perk, player)
    return perk_count


def get_orb_count(state: CollectionState, player: int) -> int:
    return state.item_count("Orb", player)


def has_perk_count(state: CollectionState, player: int, amount: int) -> bool:
    return get_perk_count(state, player) >= amount


def has_orb_count(state: CollectionState, player: int, amount: int) -> bool:
    return get_orb_count(state, player) >= amount


def forbid_items_at_location(world: MultiWorld, location_name: str, items: Set[str], player: int):
    location = world.get_location(location_name, player)
    GenericRules.forbid_items_for_player(location, items, player)


# Prevent gold and potions from appearing as purchasable items in shops (because physics will destroy them)
def ban_items_from_shops(world: MultiWorld, player: int) -> None:
    for location_name in Locations.location_name_to_id.keys():
        if "Shop Item" not in location_name:
            continue
        forbid_items_at_location(world, location_name, items_hidden_from_shops, player)


# Prevent high tier wands from appearing in early Holy Mountain shops
def ban_early_high_tier_wands(world: MultiWorld, player: int) -> None:
    for i, region_name in enumerate(holy_mountain_regions):
        wands_to_forbid = wand_tiers[i+1:]

        locations_in_region = Locations.location_region_mapping[region_name].keys()
        for location_name in locations_in_region:
            forbid_items_at_location(world, location_name, wands_to_forbid, player)

    # Prevent high tier wands from appearing in the Secret shop
    wands_to_forbid = wand_tiers[3:]
    locations_in_region = Locations.location_region_mapping["Secret Shop"].keys()
    for location_name in locations_in_region:
        forbid_items_at_location(world, location_name, wands_to_forbid, player)


def lock_holy_mountains_into_spheres(world: MultiWorld, player: int) -> None:
    for lock in entrance_locks:
        location = world.get_entrance(f"From {lock.source} To {lock.destination}", player)
        GenericRules.set_rule(location, lambda state, evt=lock.event: state.has(evt, player))


def holy_mountain_unlock_conditions(world: MultiWorld, player: int) -> None:
    vic = world.victory_condition[player].value
    for lock in entrance_locks:
        if vic == Options.VictoryCondition.option_greed_ending:
            world.get_location(lock.event, player).access_rule = \
                lambda state, items_needed=lock.items_needed: has_perk_count(state, player, items_needed//2)

        elif vic == Options.VictoryCondition.option_pure_ending:
            world.get_location(lock.event, player).access_rule = \
                lambda state, items_needed=lock.items_needed: has_perk_count(state, player, items_needed//2) \
                and has_orb_count(state, player, items_needed)

        elif vic == Options.VictoryCondition.option_peaceful_ending:
            world.get_location(lock.event, player).access_rule = \
                lambda state, items_needed=lock.items_needed: has_perk_count(state, player, items_needed//2) \
                and has_orb_count(state, player, items_needed * 3)


def victory_unlock_conditions(world: MultiWorld, player: int) -> None:
    vic = world.victory_condition[player].value
    victory_location = world.get_location("Victory", player)
    if vic == Options.VictoryCondition.option_pure_ending:
        victory_location.access_rule = lambda state: has_orb_count(state, player, 11)
    elif vic == Options.VictoryCondition.option_peaceful_ending:
        victory_location.access_rule = lambda state: has_orb_count(state, player, 33)


def create_all_rules(world: MultiWorld, player: int) -> None:
    ban_items_from_shops(world, player)
    ban_early_high_tier_wands(world, player)
    lock_holy_mountains_into_spheres(world, player)
    holy_mountain_unlock_conditions(world, player)

    # Prevent the Map perk (used to find Toveri) from being on Toveri (boss)
    if world.bosses_as_checks[player].value >= Options.BossesAsChecks.option_all_bosses:
        forbid_items_at_location(world, "Toveri", {"Perk (Spatial Awareness)"}, player)
