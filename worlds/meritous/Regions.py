# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import MeritousLocation, location_table

meritous_regions = ["Meridian", "Ataraxia", "Merodach", "Endgame"]


def _generate_entrances(player: int, entrance_list: [str], parent: Region):
    return [Entrance(player, entrance, parent) for entrance in entrance_list]


def create_regions(world: MultiWorld, player: int):
    regions = ["First", "Second", "Third", "Last"]
    bosses = ["Meridian", "Ataraxia", "Merodach"]

    for x, name in enumerate(regions):
        fullname = f"{name} Quarter"
        insidename = fullname
        if x == 0:
            insidename = "Menu"

        region = Region(insidename, player, world)
        for store in ["Alpha Cache", "Beta Cache", "Gamma Cache", "Reward Chest"]:
            for y in range(1, 7):
                loc_name = f"{store} {(x * 6) + y}"
                region.locations += [MeritousLocation(player, loc_name, location_table[loc_name], region)]

        if x < 3:
            storage_loc = f"PSI Key Storage {x + 1}"
            region.locations += [MeritousLocation(player, storage_loc, location_table[storage_loc], region)]
            region.exits += _generate_entrances(player, [f"To {bosses[x]}"], region)
        else:
            locations_end_game = ["Place of Power", "The Last Place You'll Look"]
            region.locations += [
                MeritousLocation(player, loc_name, location_table[loc_name], region)
                for loc_name in locations_end_game]
            region.exits += _generate_entrances(player, ["Back to the entrance",
                                                         "Back to the entrance with the Knife"],
                                                region)

        world.regions += [region]

    for x, boss in enumerate(bosses):
        boss_region = Region(boss, player, world)
        boss_region.locations += [
            MeritousLocation(player, boss, location_table[boss], boss_region),
            MeritousLocation(player, f"{boss} Defeat", None, boss_region)
        ]
        boss_region.exits = _generate_entrances(player, [f"To {regions[x + 1]} Quarter"], boss_region)
        world.regions.append(boss_region)

    region_final_boss = Region("Final Boss", player, world)
    region_final_boss.locations += [MeritousLocation(
        player, "Wervyn Anixil", None, region_final_boss)]
    world.regions.append(region_final_boss)

    region_tfb = Region("True Final Boss", player, world)
    region_tfb.locations += [MeritousLocation(
        player, "Wervyn Anixil?", None, region_tfb)]
    world.regions.append(region_tfb)

    entrance_map = {
        "To Meridian": {
            "to": "Meridian",
            "rule": lambda state: state.has_group("PSI Keys", player, 1) and
                                  state.has_group("Important Artifacts", player, 1)
        },
        "To Second Quarter": {
            "to": "Second Quarter",
            "rule": lambda state: state.has("Meridian Defeated", player)
        },
        "To Ataraxia": {
            "to": "Ataraxia",
            "rule": lambda state: state.has_group("PSI Keys", player, 2) and
                                  state.has_group("Important Artifacts", player, 2)
        },
        "To Third Quarter": {
            "to": "Third Quarter",
            "rule": lambda state: state.has("Ataraxia Defeated", player)
        },
        "To Merodach": {
            "to": "Merodach",
            "rule": lambda state: state.has_group("PSI Keys", player, 3) and
                                  state.has_group("Important Artifacts", player, 3)
        },
        "To Last Quarter": {
            "to": "Last Quarter",
            "rule": lambda state: state.has("Merodach Defeated", player)
        },
        "Back to the entrance": {
            "to": "Final Boss",
            "rule": lambda state: state.has("Cursed Seal", player)
        },
        "Back to the entrance with the Knife": {
            "to": "True Final Boss",
            "rule": lambda state: state.has_all(["Cursed Seal", "Agate Knife"], player)
        }
    }

    for entrance in entrance_map:
        connection_data = entrance_map[entrance]
        connection = world.get_entrance(entrance, player)
        connection.access_rule = connection_data["rule"]
        connection.connect(world.get_region(connection_data["to"], player))
