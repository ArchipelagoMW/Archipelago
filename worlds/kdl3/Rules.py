from worlds.generic.Rules import set_rule, add_rule
from .Locations import location_table, level_consumables
from .Names import LocationName
from .Items import copy_ability_table
import typing

if typing.TYPE_CHECKING:
    from . import KDL3World
    from BaseClasses import CollectionState


def can_reach_level(state: "CollectionState", player: int, level: int, player_levels: dict, open_world: bool,
                    ow_boss_req: int):
    if level == 1:
        return True
    else:
        if open_world:
            finishable_stages = 0
            for stage in player_levels[level - 1]:
                if state.can_reach(location_table[stage], "Location", player):
                    finishable_stages += 1
            if finishable_stages >= ow_boss_req:
                return True
            else:
                return False
        else:
            return state.can_reach(location_table[player_levels[level - 1][5]], "Location", player)


def can_reach_coo(state: "CollectionState", player: int) -> bool:
    return state.can_reach("Grass Land 3 - Complete", "Location", player) or \
        state.can_reach("Grass Land 5 - Complete", "Location", player) or \
        state.can_reach("Grass Land 6 - Complete", "Location", player) or \
        state.can_reach("Ripple Field 2 - Complete", "Location", player) or \
        state.can_reach("Ripple Field 6 - Complete", "Location", player) or \
        state.can_reach("Sand Canyon 2 - Complete", "Location", player) or \
        state.can_reach("Sand Canyon 3 - Complete", "Location", player) or \
        state.can_reach("Sand Canyon 6 - Complete", "Location", player) or \
        state.can_reach("Cloudy Park 1 - Complete", "Location", player) or \
        state.can_reach("Cloudy Park 4 - Complete", "Location", player) or \
        state.can_reach("Cloudy Park 5 - Complete", "Location", player) or \
        state.can_reach("Cloudy Park 6 - Complete", "Location", player) or \
        state.can_reach("Iceberg 3 - Complete", "Location", player) or \
        state.can_reach("Iceberg 5 - Complete", "Location", player) or \
        state.can_reach("Iceberg 6 - Complete", "Location", player)
    #  We purposefully leave out Iceberg 4 here, since access to Coo is conditional
    #  on having either Coo and Burning, or potentially Nago and Burning


def can_reach_nago(state: "CollectionState", player: int) -> bool:
    return state.can_reach(LocationName.grass_land_1, "Location", player) \
        or state.can_reach(LocationName.grass_land_5, "Location", player) \
        or state.can_reach(LocationName.grass_land_6, "Location", player) \
        or state.can_reach(LocationName.ripple_field_1, "Location", player) \
        or state.can_reach(LocationName.ripple_field_4, "Location", player) \
        or state.can_reach(LocationName.ripple_field_6, "Location", player) \
        or state.can_reach(LocationName.sand_canyon_4, "Location", player) \
        or state.can_reach(LocationName.sand_canyon_6, "Location", player) \
        or state.can_reach(LocationName.cloudy_park_1, "Location", player) \
        or state.can_reach(LocationName.cloudy_park_2, "Location", player) \
        or state.can_reach(LocationName.cloudy_park_6, "Location", player) \
        or state.can_reach(LocationName.iceberg_2, "Location", player) \
        or state.can_reach(LocationName.iceberg_3, "Location", player) \
        or state.can_reach(LocationName.iceberg_6, "Location", player)


def set_rules(world: "KDL3World") -> None:
    for level in range(1, len(world.player_levels[world.player]) + 1):
        for stage in range(len(world.player_levels[world.player][level])):
            if stage != 6:
                if not world.multiworld.open_world[world.player]:
                    set_rule(
                        world.multiworld.get_location(location_table[world.player_levels[world.player][level][stage]],
                                                      world.player),
                        lambda state, level=level, stage=stage: True if stage == 0
                        else state.can_reach(
                            location_table[world.player_levels[world.player][level][stage - 1]], "Location",
                            world.player))
                    set_rule(
                        world.multiworld.get_location(
                            location_table[world.player_levels[world.player][level][stage] + 0x100], world.player),
                        lambda state, level=level, stage=stage: True if stage == 0
                        else state.can_reach(
                            location_table[world.player_levels[world.player][level][stage - 1]], "Location",
                            world.player))
                    if world.multiworld.consumables[world.player]:
                        stage_idx = world.player_levels[world.player][level][stage] & 0xFF
                        if stage_idx in level_consumables:
                            for consumable in level_consumables[stage_idx]:
                                set_rule(
                                    world.multiworld.get_location(
                                        location_table[0x770300 + consumable],
                                        world.player),
                                    lambda state, level=level, stage=stage: True if stage == 0
                                    else state.can_reach(
                                        location_table[world.player_levels[world.player][level][stage - 1]], "Location",
                                        world.player))

    # Level 1
    add_rule(world.multiworld.get_location(LocationName.grass_land_muchi, world.player),
             lambda state: state.has("ChuChu", world.player))
    add_rule(world.multiworld.get_location(LocationName.grass_land_chao, world.player),
             lambda state: state.has("Stone", world.player))
    add_rule(world.multiworld.get_location(LocationName.grass_land_mine, world.player),
             lambda state: state.has("Kine", world.player))

    # Level 2
    add_rule(world.multiworld.get_location(LocationName.ripple_field_5, world.player),
             lambda state: state.has("Kine", world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_kamuribana, world.player),
             lambda state: state.has("Pitch", world.player) and state.has("Clean", world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_bakasa, world.player),
             lambda state: state.has("Kine", world.player) and state.has("Parasol", world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_toad, world.player),
             lambda state: state.has("Needle", world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_mama_pitch, world.player),
             lambda state: state.has("Pitch", world.player) and state.has("Kine", world.player)
                           and state.has("Burning", world.player) and state.has("Stone", world.player))

    # Level 3
    add_rule(world.multiworld.get_location(LocationName.sand_canyon_5, world.player),
             lambda state: state.has("Cutter", world.player))
    add_rule(world.multiworld.get_location(LocationName.sand_canyon_auntie, world.player),
             lambda state: state.has("Clean", world.player))
    add_rule(world.multiworld.get_location(LocationName.sand_canyon_nyupun, world.player),
             lambda state: state.has("ChuChu", world.player) and state.has("Cutter", world.player))
    add_rule(world.multiworld.get_location(LocationName.sand_canyon_rob, world.player),
             lambda state: (state.has("Kine", world.player) and state.has("Coo", world.player))
                           and state.has("Parasol", world.player)
                           and state.has("Stone", world.player)
                           and (state.has("Clean", world.player) or state.has("Spark", world.player))
                           and (state.has("Ice", world.player) or state.has("Needle", world.player))
             )

    # Level 4
    add_rule(world.multiworld.get_location(LocationName.cloudy_park_hibanamodoki, world.player),
             lambda state: state.has("Coo", world.player) and state.has("Clean", world.player))
    add_rule(world.multiworld.get_location(LocationName.cloudy_park_piyokeko, world.player),
             lambda state: state.has("Needle", world.player))
    add_rule(world.multiworld.get_location(LocationName.cloudy_park_mikarin, world.player),
             lambda state: state.has("Coo", world.player))
    add_rule(world.multiworld.get_location(LocationName.cloudy_park_pick, world.player),
             lambda state: state.has("Rick", world.player))

    # Level 5
    add_rule(world.multiworld.get_location(LocationName.iceberg_4, world.player),
             lambda state: state.has("Burning", world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_kogoesou, world.player),
             lambda state: state.has("Burning", world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_samus, world.player),
             lambda state: state.has("Ice", world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_name, world.player),
             lambda state: state.has("Coo", world.player) and state.has("Burning", world.player)
                           and state.has("ChuChu", world.player) and can_reach_coo(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_shiro, world.player),
             lambda state: state.has("Nago", world.player) and can_reach_nago(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_angel, world.player),
             lambda state: state.has_all([ability for ability in copy_ability_table.keys()], world.player))
    # cleaner than writing out 8 ands

    # Consumables
    if world.multiworld.consumables[world.player]:
        add_rule(world.multiworld.get_location(LocationName.grass_land_1_u1, world.player),
                 lambda state: state.has("Parasol", world.player))
        add_rule(world.multiworld.get_location(LocationName.grass_land_1_m1, world.player),
                 lambda state: state.has("Spark", world.player))
        add_rule(world.multiworld.get_location(LocationName.grass_land_2_u1, world.player),
                 lambda state: state.has("Needle", world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_2_u1, world.player),
                 lambda state: state.has("Kine", world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_2_m1, world.player),
                 lambda state: state.has("Kine", world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_3_u1, world.player),
                 lambda state: state.has("Cutter", world.player) or state.has("Spark", world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_4_u1, world.player),
                 lambda state: state.has("Stone", world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_4_m2, world.player),
                 lambda state: state.has("Stone", world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_5_m1, world.player),
                 lambda state: state.has("Kine", world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_5_u1, world.player),
                 lambda state: state.has("Kine", world.player)
                               and state.has("Burning", world.player) and state.has("Stone", world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_5_m2, world.player),
                 lambda state: state.has("Kine", world.player)
                               and state.has("Burning", world.player) and state.has("Stone", world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_4_u1, world.player),
                 lambda state: state.has("Clean", world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_4_m2, world.player),
                 lambda state: state.has("Needle", world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_5_u2, world.player),
                 lambda state: state.has("Ice", world.player) and state.has("Rick", world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_5_u3, world.player),
                 lambda state: state.has("Ice", world.player) and state.has("Rick", world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_5_u4, world.player),
                 lambda state: state.has("Ice", world.player) and state.has("Rick", world.player))
        add_rule(world.multiworld.get_location(LocationName.cloudy_park_6_u1, world.player),
                 lambda state: state.has("Cutter", world.player))

    for boss_flag, purification, i in zip(["Level 1 Boss", "Level 2 Boss",
                                           "Level 3 Boss", "Level 4 Boss", "Level 5 Boss"],
                                          [LocationName.grass_land_whispy, LocationName.ripple_field_acro,
                                           LocationName.sand_canyon_poncon, LocationName.cloudy_park_ado,
                                           LocationName.iceberg_dedede],
                                          range(1, 6)):
        set_rule(world.multiworld.get_location(boss_flag, world.player),
                 lambda state, i=i: state.has("Heart Star", world.player, world.boss_requirements[world.player][i - 1])
                                    and state.can_reach(location_table[world.player_levels[world.player][i][5]],
                                                        "Location",
                                                        world.player))
        set_rule(world.multiworld.get_location(purification, world.player),
                 lambda state, i=i: state.has("Heart Star", world.player, world.boss_requirements[world.player][i - 1])
                                    and state.can_reach(location_table[world.player_levels[world.player][i][5]],
                                                        "Location",
                                                        world.player))

    if world.multiworld.strict_bosses[world.player]:
        for level in range(2, 6):
            add_rule(world.multiworld.get_entrance(f"To Level {level}", world.player),
                     lambda state, i=level: state.has("Heart Star", world.player,
                                                      world.boss_requirements[world.player][i - 2]))

    set_rule(world.multiworld.get_entrance("To Level 6", world.player),
             lambda state: state.has("Heart Star", world.player, world.required_heart_stars[world.player]))

    for level in range(2, 6):
        add_rule(world.multiworld.get_entrance(f"To Level {level}", world.player),
                 lambda state, i=level: can_reach_level(state, world.player, i,
                                                        world.player_levels[world.player],
                                                        world.multiworld.open_world[world.player],
                                                        world.multiworld.ow_boss_requirement[world.player]))

    if world.multiworld.goal_speed[world.player] == 0:
        add_rule(world.multiworld.get_entrance("To Level 6", world.player),
                 lambda state: state.has("Level 1 Boss Purified", world.player)
                               and state.has("Level 2 Boss Purified", world.player)
                               and state.has("Level 3 Boss Purified", world.player)
                               and state.has("Level 4 Boss Purified", world.player)
                               and state.has("Level 5 Boss Purified", world.player))
