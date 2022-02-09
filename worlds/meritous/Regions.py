# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import MeritousLocation, alpha_store, beta_store, gamma_store, chest_store, special_store, location_table

meritous_regions = ["Atlas Dome", "Chest rewards",
                    "PSI Keys", "Meridian", "Ataraxia", "Merodach", "Endgame"]


def create_regions(world: MultiWorld, player: int):
    region_paid_stores = Region(
        "Atlas Dome", RegionType.Generic, "Atlas Dome", player, world)
    region_paid_stores.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_paid_stores) for loc_name in [*alpha_store]]
    region_paid_stores.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_paid_stores) for loc_name in [*beta_store]]
    region_paid_stores.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_paid_stores) for loc_name in [*gamma_store]]
    world.regions.append(region_paid_stores)

    region_chest_store = Region(
        "Chest rewards", RegionType.Generic, "Chest rewards", player, world)
    region_chest_store.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_chest_store) for loc_name in [*chest_store]]
    world.regions.append(region_chest_store)

    region_psi_keys = Region(
        "PSI Keys", RegionType.Generic, "PSI Keys", player, world)
    region_psi_keys.locations += [MeritousLocation(
        player, "PSI Key Storage {i}", location_table["PSI Key Storage {i}"], region_psi_keys) for i in range(1, 4)]
    world.regions.append(region_psi_keys)

    for boss in ["Meridian", "Ataraxia", "Merodach"]:
        boss_region = Region(boss, RegionType.Generic, boss, player, world)
        boss_region.locations += MeritousLocation(
            player, boss, location_table[boss], boss_region)
        world.regions.append(boss_region)

    region_end_game = Region(
        "Endgame", RegionType.Generic, "Endgame", player, world)
    locations_end_game = ["Cursed Seal", "Agate Knife"]
    region_end_game.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_end_game) for loc_name in locations_end_game]
    world.regions.append(region_end_game)


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player, '', sourceRegion)
    connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)
