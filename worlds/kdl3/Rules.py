from worlds.generic.Rules import set_rule, add_rule
from .Locations import location_table, level_consumables
from .Names import LocationName, EnemyAbilities
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
            return state.has(f"{LocationName.level_names_inverse[level - 1]} - Stage Completion", player, ow_boss_req)
        else:
            return state.has(f"{LocationName.level_names_inverse[level - 1]} 6 - Stage Completion", player)


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


def can_reach_burning(state: "CollectionState", player: int) -> bool:
    return state.has("Burning", player) and state.has("Burning Ability", player)


def can_reach_stone(state: "CollectionState", player: int) -> bool:
    return state.has("Stone", player) and state.has("Stone Ability", player)


def can_reach_ice(state: "CollectionState", player: int) -> bool:
    return state.has("Ice", player) and state.has("Ice Ability", player)


def can_reach_needle(state: "CollectionState", player: int) -> bool:
    return state.has("Needle", player) and state.has("Needle Ability", player)


def can_reach_clean(state: "CollectionState", player: int) -> bool:
    return state.has("Clean", player) and state.has("Clean Ability", player)


def can_reach_parasol(state: "CollectionState", player: int) -> bool:
    return state.has("Parasol", player) and state.has("Parasol Ability", player)


def can_reach_spark(state: "CollectionState", player: int) -> bool:
    return state.has("Spark", player) and state.has("Spark Ability", player)


def can_reach_cutter(state: "CollectionState", player: int) -> bool:
    return state.has("Cutter", player) and state.has("Cutter Ability", player)


ability_map = {
    "No Ability": lambda state, player: True,
    "Burning Ability": can_reach_burning,
    "Stone Ability": can_reach_stone,
    "Ice Ability": can_reach_ice,
    "Needle Ability": can_reach_needle,
    "Clean Ability": can_reach_clean,
    "Parasol Ability": can_reach_parasol,
    "Spark Ability": can_reach_spark,
    "Cutter Ability": can_reach_cutter,
}


def can_assemble_rob(state: "CollectionState", player: int, copy_abilities: typing.Dict[str,str]):
    # check animal requirements
    if not can_reach_coo(state, player) and can_reach_kine(state, player):
        return False
    # probably some cleaner way to handle this
    room1 = EnemyAbilities.enemy_restrictive[1]
    room2 = EnemyAbilities.enemy_restrictive[2]
    room3 = EnemyAbilities.enemy_restrictive[3]
    room4 = EnemyAbilities.enemy_restrictive[4]
    for abilities, bukisets in [room1, room2, room3, room4]:
        iterator = iter(x for x in bukisets if copy_abilities[x] in abilities)
        target_bukiset = next(iterator, None)
        can_reach = False
        while target_bukiset is not None:
            can_reach = can_reach | ability_map[copy_abilities[target_bukiset]](state, player)
            target_bukiset = next(iterator, None)
        if not can_reach:
            return False
    # now the known needed abilities
    return can_reach_parasol(state, player) and can_reach_stone(state, player)


def can_fix_angel_wings(state: "CollectionState", player: int, copy_abilities: typing.Dict[str,str]):
    can_reach = True
    for enemy in {"Sparky", "Blocky", "Jumper Shoot", "Yuki", "Sir Kibble", "Haboki", "Boboo", "Captain Stitch"}:
        can_reach = can_reach & ability_map[copy_abilities[enemy]](state, player)
    return can_reach


def set_rules(world: "KDL3World") -> None:
    # Level 1
    add_rule(world.multiworld.get_location(LocationName.grass_land_muchi, world.player),
             lambda state: can_reach_chuchu(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.grass_land_chao, world.player),
             lambda state: can_reach_stone(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.grass_land_mine, world.player),
             lambda state: can_reach_kine(state, world.player))

    # Level 2
    add_rule(world.multiworld.get_location(LocationName.ripple_field_5, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_kamuribana, world.player),
             lambda state: can_reach_pitch(state, world.player) and can_reach_clean(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_bakasa, world.player),
             lambda state: can_reach_kine(state, world.player) and can_reach_parasol(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_toad, world.player),
             lambda state: can_reach_needle(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.ripple_field_mama_pitch, world.player),
             lambda state: can_reach_pitch(state, world.player) and can_reach_kine(state, world.player)
                           and can_reach_burning(state, world.player) and can_reach_stone(state, world.player))

    # Level 3
    add_rule(world.multiworld.get_location(LocationName.sand_canyon_5, world.player),
             lambda state: can_reach_cutter(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.sand_canyon_auntie, world.player),
             lambda state: can_reach_clean(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.sand_canyon_nyupun, world.player),
             lambda state: can_reach_chuchu(state, world.player) and can_reach_cutter(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.sand_canyon_rob, world.player),
             lambda state: can_assemble_rob(state, world.player, world.copy_abilities)
             )

    # Level 4
    add_rule(world.multiworld.get_location(LocationName.cloudy_park_hibanamodoki, world.player),
             lambda state: can_reach_coo(state, world.player) and can_reach_clean(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.cloudy_park_piyokeko, world.player),
             lambda state: can_reach_needle(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.cloudy_park_mikarin, world.player),
             lambda state: can_reach_coo(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.cloudy_park_pick, world.player),
             lambda state: can_reach_rick(state, world.player))

    # Level 5
    add_rule(world.multiworld.get_location(LocationName.iceberg_4, world.player),
             lambda state: can_reach_burning(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_kogoesou, world.player),
             lambda state: can_reach_burning(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_samus, world.player),
             lambda state: can_reach_ice(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_name, world.player),
             lambda state: can_reach_coo(state, world.player) and can_reach_burning(state, world.player)
                           and can_reach_chuchu(state, world.player))
    # ChuChu is guaranteed here, but we use this for consistency
    add_rule(world.multiworld.get_location(LocationName.iceberg_shiro, world.player),
             lambda state: can_reach_nago(state, world.player))
    add_rule(world.multiworld.get_location(LocationName.iceberg_angel, world.player),
             lambda state: can_fix_angel_wings(state, world.player, world.copy_abilities))

    # Consumables
    if world.multiworld.consumables[world.player]:
        add_rule(world.multiworld.get_location(LocationName.grass_land_1_u1, world.player),
                 lambda state: can_reach_parasol(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.grass_land_1_m1, world.player),
                 lambda state: can_reach_spark(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.grass_land_2_u1, world.player),
                 lambda state: can_reach_needle(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_2_u1, world.player),
                 lambda state: can_reach_kine(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_2_m1, world.player),
                 lambda state: can_reach_kine(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_3_u1, world.player),
                 lambda state: can_reach_cutter(state, world.player) or can_reach_spark(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_4_u1, world.player),
                 lambda state: can_reach_stone(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_4_m2, world.player),
                 lambda state: can_reach_stone(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_5_m1, world.player),
                 lambda state: can_reach_kine(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_5_u1, world.player),
                 lambda state: can_reach_kine(state, world.player)
                               and can_reach_burning(state, world.player) and can_reach_stone(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.ripple_field_5_m2, world.player),
                 lambda state: can_reach_kine(state, world.player)
                               and can_reach_burning(state, world.player) and can_reach_stone(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_4_u1, world.player),
                 lambda state: can_reach_clean(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_4_m2, world.player),
                 lambda state: can_reach_needle(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_5_u2, world.player),
                 lambda state: can_reach_ice(state, world.player) and can_reach_rick(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_5_u3, world.player),
                 lambda state: can_reach_ice(state, world.player) and can_reach_rick(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.sand_canyon_5_u4, world.player),
                 lambda state: can_reach_ice(state, world.player) and can_reach_rick(state, world.player))
        add_rule(world.multiworld.get_location(LocationName.cloudy_park_6_u1, world.player),
                 lambda state: can_reach_cutter(state, world.player))

    # copy ability access edge cases
    # water locked: most mony, joe, and some blipper/glunk/squishy
    # sand canyon 4 all
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_2_E3, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_3_E6, world.player),
             lambda state: can_reach_kine(state, world.player))
    # Ripple Field 4 E5, E7, and E8 are strict, but doable
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_4_E5, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_4_E7, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_4_E8, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_5_E1, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_5_E2, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_5_E3, world.player),
             lambda state: can_reach_kine(state, world.player))
    add_rule(world.multiworld.get_location(EnemyAbilities.Ripple_Field_5_E4, world.player),
             lambda state: can_reach_kine(state, world.player))

    for boss_flag, purification, i in zip(["Level 1 Boss", "Level 2 Boss",
                                           "Level 3 Boss", "Level 4 Boss", "Level 5 Boss"],
                                          [LocationName.grass_land_whispy, LocationName.ripple_field_acro,
                                           LocationName.sand_canyon_poncon, LocationName.cloudy_park_ado,
                                           LocationName.iceberg_dedede],
                                          range(1, 6)):
        set_rule(world.multiworld.get_location(boss_flag, world.player),
                 lambda state, i=i: state.has("Heart Star", world.player, world.boss_requirements[world.player][i - 1])
                                    and can_reach_level(state, world.player, i + 1,
                                                        world.multiworld.open_world[world.player],
                                                        world.multiworld.ow_boss_requirement[world.player]))
        set_rule(world.multiworld.get_location(purification, world.player),
                 lambda state, i=i: state.has("Heart Star", world.player, world.boss_requirements[world.player][i - 1])
                                    and can_reach_level(state, world.player, i + 1,
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
