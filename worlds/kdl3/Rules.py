from worlds.generic.Rules import set_rule, add_rule
from .Locations import location_table, level_consumables
from .Names import LocationName, AnimalFriendSpawns
from .Items import copy_ability_table
import typing
from BaseClasses import MultiWorld

if typing.TYPE_CHECKING:
    from . import KDL3World
    from BaseClasses import CollectionState


def can_reach_level(state: "CollectionState", player: int, level: int, open_world: bool,
                    ow_boss_req: int):
    if level == 1:
        return True
    else:
        if open_world:
            return state.has(f"{LocationName.level_names_inverse[level-1]} - Stage Completion", player, ow_boss_req)
        else:
            return state.has(f"{LocationName.level_names_inverse[level-1]} 6 - Stage Completion", player)


def can_reach_rick(state: "CollectionState", player: int) -> bool:
    return state.has("Rick", player) and state.has("Rick Spawn", player)


def can_reach_kine(state: "CollectionState", player: int) -> bool:
    return state.has("Kine", player) and state.has("Kine Spawn", player)


def can_reach_coo(state: "CollectionState", player: int) -> bool:
    return state.has("Coo", player) and state.has("Coo Spawn", player)


def can_reach_nago(state: "CollectionState", player: int) -> bool:
    return state.has("Nago", player) and state.has("Nago Spawn", player)


def can_reach_chuchu(state: "CollectionState", player: int) -> bool:
    return state.has("ChuChu", player) and state.has("ChuChu Spawn", player)


def can_reach_pitch(state: "CollectionState", player: int) -> bool:
    return state.has("Pitch", player) and state.has("Pitch Spawn", player)


def set_rules(world: "KDL3World") -> None:

    # Level 1
    add_rule(world.multiworld.get_location(LocationName.grass_land_muchi, world.player),
             lambda state: can_reach_chuchu(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.grass_land_chao, world.player),
             lambda state: state.has("Stone", world.player))
    add_rule(world.multiworld.get_location(LocationName.grass_land_mine, world.player),
             lambda state: can_reach_kine(state, world.player))

    # Level 2
    add_rule(world.multiworld.get_location(LocationName.ripple_field_5, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_kamuribana, world.player),
             lambda state: can_reach_pitch(state, world.player) and state.has("Clean", world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_bakasa, world.player),
             lambda state: can_reach_kine(state, world.player) and state.has("Parasol", world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_toad, world.player),
             lambda state: state.has("Needle", world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_mama_pitch, world.player),
             lambda state: can_reach_pitch(state, world.player) and can_reach_kine(state, world.player)
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
             lambda state: can_reach_nago(state, world.player))
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
                                    and can_reach_level(state, world.player, i+1,
                                                        world.multiworld.open_world[world.player],
                                                        world.multiworld.ow_boss_requirement[world.player]))
        set_rule(world.multiworld.get_location(purification, world.player),
                 lambda state, i=i: state.has("Heart Star", world.player, world.boss_requirements[world.player][i - 1])
                                    and can_reach_level(state, world.player, i+1,
                                                        world.multiworld.open_world[world.player],
                                                        world.multiworld.ow_boss_requirement[world.player]))

    if world.multiworld.strict_bosses[world.player]:
        for level in range(2, 6):
            add_rule(world.multiworld.get_entrance(f"To Level {level}", world.player),
                     lambda state, i=level: state.has(f"Level {i - 1} Boss Purified", world.player))

    set_rule(world.multiworld.get_entrance("To Level 6", world.player),
             lambda state: state.has("Heart Star", world.player, world.required_heart_stars[world.player]))

    for level in range(2, 6):
        add_rule(world.multiworld.get_entrance(f"To Level {level}", world.player),
                 lambda state, i=level: can_reach_level(state, world.player, i,
                                                        world.multiworld.open_world[world.player],
                                                        world.multiworld.ow_boss_requirement[world.player]))

    if world.multiworld.goal_speed[world.player] == 0:
        add_rule(world.multiworld.get_entrance("To Level 6", world.player),
                 lambda state: state.has_all(["Level 1 Boss Purified", "Level 2 Boss Purified", "Level 3 Boss Purified",
                                              "Level 4 Boss Purified", "Level 5 Boss Purified"], world.player))
