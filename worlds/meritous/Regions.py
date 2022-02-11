# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import MeritousLocation, alpha_store, beta_store, gamma_store, chest_store, special_store, location_table

meritous_regions = ["Meridian", "Ataraxia", "Merodach", "Endgame"]


def create_regions(world: MultiWorld, player: int):
    region_primary = Region(
        "Menu", RegionType.Generic, "Atlas Dome", player, world)
    region_primary.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_primary) for loc_name in alpha_store]
    region_primary.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_primary) for loc_name in beta_store]
    region_primary.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_primary) for loc_name in gamma_store]
    region_primary.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_primary) for loc_name in chest_store]
    region_primary.locations += [MeritousLocation(
        player, f"PSI Key Storage {i}", location_table[f"PSI Key Storage {i}"], region_primary) for i in range(1, 4)]
    world.regions.append(region_primary)

    for boss in ["Meridian", "Ataraxia", "Merodach"]:
        boss_region = Region(boss, RegionType.Generic, boss, player, world)
        boss_region.locations += [MeritousLocation(
            player, boss, location_table[boss], boss_region)]
        world.regions.append(boss_region)

    region_end_game = Region(
        "Endgame", RegionType.Generic, "Endgame", player, world)
    locations_end_game = ["Place of Power", "The Last Place You'll Look"]
    region_end_game.locations += [MeritousLocation(
        player, loc_name, location_table[loc_name], region_end_game) for loc_name in locations_end_game]
    world.regions.append(region_end_game)

    region_final_boss = Region(
        "Final Boss", RegionType.Generic, "Final Boss", player, world)
    region_final_boss.locations = [MeritousLocation(
        player, "Wervyn Anixil", None, region_final_boss)]
    world.regions.append(region_final_boss)

    region_tfb = Region("True Final Boss", RegionType.Generic,
                        "True Final Boss", player, world)
    region_tfb.locations = [MeritousLocation(
        player, "Wervyn Anixil?", None, region_tfb)]
    world.regions.append(region_tfb)


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player, '', sourceRegion)
    connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)
