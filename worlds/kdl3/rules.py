from BaseClasses import ItemClassification
from worlds.generic.Rules import set_rule, add_rule
from .items import KDL3Item
from .locations import location_table
from .names import location_name, enemy_abilities, animal_friend_spawns
from .options import GoalSpeed
import typing

if typing.TYPE_CHECKING:
    from . import KDL3World
    from BaseClasses import CollectionState


def can_reach_boss(state: "CollectionState", player: int, level: int, open_world: int,
                   ow_boss_req: int, player_levels: typing.Dict[int, typing.List[int]]) -> bool:
    if open_world:
        return state.has(f"{location_name.level_names_inverse[level]} - Stage Completion", player, ow_boss_req)
    else:
        return state.can_reach(location_table[player_levels[level][5]], "Location", player)


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


ability_map: typing.Dict[str, typing.Callable[["CollectionState", int], bool]] = {
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


def can_assemble_rob(state: "CollectionState", player: int, copy_abilities: typing.Dict[str, str]) -> bool:
    # check animal requirements
    if not (can_reach_coo(state, player) and can_reach_kine(state, player)):
        return False
    for abilities, bukisets in enemy_abilities.enemy_restrictive[1:5]:
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


def can_fix_angel_wings(state: "CollectionState", player: int, copy_abilities: typing.Dict[str, str]) -> bool:
    can_reach = True
    for enemy in {"Sparky", "Blocky", "Jumper Shoot", "Yuki", "Sir Kibble", "Haboki", "Boboo", "Captain Stitch"}:
        can_reach = can_reach & ability_map[copy_abilities[enemy]](state, player)
    return can_reach


def set_rules(world: "KDL3World") -> None:
    goal = world.options.goal.value
    goal_location = world.multiworld.get_location(location_name.goals[goal], world.player)
    goal_location.place_locked_item(KDL3Item("Love-Love Rod", ItemClassification.progression, None, world.player))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Love-Love Rod", world.player)

    # Level 1
    set_rule(world.multiworld.get_location(location_name.grass_land_muchi, world.player),
             lambda state: can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(location_name.grass_land_chao, world.player),
             lambda state: can_reach_stone(state, world.player))
    set_rule(world.multiworld.get_location(location_name.grass_land_mine, world.player),
             lambda state: can_reach_kine(state, world.player))

    # Level 2
    set_rule(world.multiworld.get_location(location_name.ripple_field_5, world.player),
             lambda state: can_reach_kine(state, world.player))
    set_rule(world.multiworld.get_location(location_name.ripple_field_kamuribana, world.player),
             lambda state: can_reach_pitch(state, world.player) and can_reach_clean(state, world.player))
    set_rule(world.multiworld.get_location(location_name.ripple_field_bakasa, world.player),
             lambda state: can_reach_kine(state, world.player) and can_reach_parasol(state, world.player))
    set_rule(world.multiworld.get_location(location_name.ripple_field_toad, world.player),
             lambda state: can_reach_needle(state, world.player))
    set_rule(world.multiworld.get_location(location_name.ripple_field_mama_pitch, world.player),
             lambda state: (can_reach_pitch(state, world.player) and
                            can_reach_kine(state, world.player) and
                            can_reach_burning(state, world.player) and
                            can_reach_stone(state, world.player)))

    # Level 3
    set_rule(world.multiworld.get_location(location_name.sand_canyon_5, world.player),
             lambda state: can_reach_cutter(state, world.player))
    set_rule(world.multiworld.get_location(location_name.sand_canyon_auntie, world.player),
             lambda state: can_reach_clean(state, world.player))
    set_rule(world.multiworld.get_location(location_name.sand_canyon_nyupun, world.player),
             lambda state: can_reach_chuchu(state, world.player) and can_reach_cutter(state, world.player))
    set_rule(world.multiworld.get_location(location_name.sand_canyon_rob, world.player),
             lambda state: can_assemble_rob(state, world.player, world.copy_abilities)
             )

    # Level 4
    set_rule(world.multiworld.get_location(location_name.cloudy_park_hibanamodoki, world.player),
             lambda state: can_reach_coo(state, world.player) and can_reach_clean(state, world.player))
    set_rule(world.multiworld.get_location(location_name.cloudy_park_piyokeko, world.player),
             lambda state: can_reach_needle(state, world.player))
    set_rule(world.multiworld.get_location(location_name.cloudy_park_mikarin, world.player),
             lambda state: can_reach_coo(state, world.player))
    set_rule(world.multiworld.get_location(location_name.cloudy_park_pick, world.player),
             lambda state: can_reach_rick(state, world.player))

    # Level 5
    set_rule(world.multiworld.get_location(location_name.iceberg_4, world.player),
             lambda state: can_reach_burning(state, world.player))
    set_rule(world.multiworld.get_location(location_name.iceberg_kogoesou, world.player),
             lambda state: can_reach_burning(state, world.player))
    set_rule(world.multiworld.get_location(location_name.iceberg_samus, world.player),
             lambda state: can_reach_ice(state, world.player))
    set_rule(world.multiworld.get_location(location_name.iceberg_name, world.player),
             lambda state: (can_reach_coo(state, world.player) and
                            can_reach_burning(state, world.player) and
                            can_reach_chuchu(state, world.player)))
    # ChuChu is guaranteed here, but we use this for consistency
    set_rule(world.multiworld.get_location(location_name.iceberg_shiro, world.player),
             lambda state: can_reach_nago(state, world.player))
    set_rule(world.multiworld.get_location(location_name.iceberg_angel, world.player),
             lambda state: can_fix_angel_wings(state, world.player, world.copy_abilities))

    # Consumables
    if world.options.consumables:
        set_rule(world.multiworld.get_location(location_name.grass_land_1_u1, world.player),
                 lambda state: can_reach_parasol(state, world.player))
        set_rule(world.multiworld.get_location(location_name.grass_land_1_m1, world.player),
                 lambda state: can_reach_spark(state, world.player))
        set_rule(world.multiworld.get_location(location_name.grass_land_2_u1, world.player),
                 lambda state: can_reach_needle(state, world.player))
        set_rule(world.multiworld.get_location(location_name.ripple_field_2_u1, world.player),
                 lambda state: can_reach_kine(state, world.player))
        set_rule(world.multiworld.get_location(location_name.ripple_field_2_m1, world.player),
                 lambda state: can_reach_kine(state, world.player))
        set_rule(world.multiworld.get_location(location_name.ripple_field_3_u1, world.player),
                 lambda state: can_reach_cutter(state, world.player) or can_reach_spark(state, world.player))
        set_rule(world.multiworld.get_location(location_name.ripple_field_4_u1, world.player),
                 lambda state: can_reach_stone(state, world.player))
        set_rule(world.multiworld.get_location(location_name.ripple_field_4_m2, world.player),
                 lambda state: can_reach_stone(state, world.player))
        set_rule(world.multiworld.get_location(location_name.ripple_field_5_m1, world.player),
                 lambda state: can_reach_kine(state, world.player))
        set_rule(world.multiworld.get_location(location_name.ripple_field_5_u1, world.player),
                 lambda state: (can_reach_kine(state, world.player) and
                                can_reach_burning(state, world.player) and
                                can_reach_stone(state, world.player)))
        set_rule(world.multiworld.get_location(location_name.ripple_field_5_m2, world.player),
                 lambda state: (can_reach_kine(state, world.player) and
                                can_reach_burning(state, world.player) and
                                can_reach_stone(state, world.player)))
        set_rule(world.multiworld.get_location(location_name.sand_canyon_4_u1, world.player),
                 lambda state: can_reach_clean(state, world.player))
        set_rule(world.multiworld.get_location(location_name.sand_canyon_4_m2, world.player),
                 lambda state: can_reach_needle(state, world.player))
        set_rule(world.multiworld.get_location(location_name.sand_canyon_5_u2, world.player),
                 lambda state: can_reach_ice(state, world.player) and
                               (can_reach_rick(state, world.player) or can_reach_coo(state, world.player)
                                or can_reach_chuchu(state, world.player) or can_reach_pitch(state, world.player)
                                or can_reach_nago(state, world.player)))
        set_rule(world.multiworld.get_location(location_name.sand_canyon_5_u3, world.player),
                 lambda state: can_reach_ice(state, world.player) and
                               (can_reach_rick(state, world.player) or can_reach_coo(state, world.player)
                                or can_reach_chuchu(state, world.player) or can_reach_pitch(state, world.player)
                                or can_reach_nago(state, world.player)))
        set_rule(world.multiworld.get_location(location_name.sand_canyon_5_u4, world.player),
                 lambda state: can_reach_ice(state, world.player) and
                               (can_reach_rick(state, world.player) or can_reach_coo(state, world.player)
                                or can_reach_chuchu(state, world.player) or can_reach_pitch(state, world.player)
                                or can_reach_nago(state, world.player)))
        set_rule(world.multiworld.get_location(location_name.cloudy_park_6_u1, world.player),
                 lambda state: can_reach_cutter(state, world.player))

    if world.options.starsanity:
        # ranges are our friend
        for i in range(7, 11):
            set_rule(world.multiworld.get_location(f"Grass Land 1 - Star {i}", world.player),
                     lambda state: can_reach_cutter(state, world.player))
        for i in range(11, 14):
            set_rule(world.multiworld.get_location(f"Grass Land 1 - Star {i}", world.player),
                     lambda state: can_reach_parasol(state, world.player))
        for i in [1, 3, 4, 9, 10]:
            set_rule(world.multiworld.get_location(f"Grass Land 2 - Star {i}", world.player),
                     lambda state: can_reach_stone(state, world.player))
        set_rule(world.multiworld.get_location("Grass Land 2 - Star 2", world.player),
                 lambda state: can_reach_burning(state, world.player))
        set_rule(world.multiworld.get_location("Ripple Field 2 - Star 17", world.player),
                 lambda state: can_reach_kine(state, world.player))
        for i in range(41, 43):
            # any star past this point also needs kine, but so does the exit
            set_rule(world.multiworld.get_location(f"Ripple Field 5 - Star {i}", world.player),
                     lambda state: can_reach_kine(state, world.player))
        for i in range(46, 49):
            # also requires kine, but only for access from the prior room
            set_rule(world.multiworld.get_location(f"Ripple Field 5 - Star {i}", world.player),
                     lambda state: can_reach_burning(state, world.player) and can_reach_stone(state, world.player))
        for i in range(12, 18):
            set_rule(world.multiworld.get_location(f"Sand Canyon 5 - Star {i}", world.player),
                     lambda state: can_reach_ice(state, world.player) and
                                   (can_reach_rick(state, world.player) or can_reach_coo(state, world.player)
                                    or can_reach_chuchu(state, world.player) or can_reach_pitch(state, world.player)
                                    or can_reach_nago(state, world.player)))
        for i in range(21, 23):
            set_rule(world.multiworld.get_location(f"Sand Canyon 5 - Star {i}", world.player),
                     lambda state: can_reach_chuchu(state, world.player))
        for r in [range(19, 21), range(23, 31)]:
            for i in r:
                set_rule(world.multiworld.get_location(f"Sand Canyon 5 - Star {i}", world.player),
                         lambda state: can_reach_clean(state, world.player))
        for i in range(31, 41):
            set_rule(world.multiworld.get_location(f"Sand Canyon 5 - Star {i}", world.player),
                     lambda state: can_reach_burning(state, world.player))
        for r in [range(1, 31), range(44, 51)]:
            for i in r:
                set_rule(world.multiworld.get_location(f"Cloudy Park 4 - Star {i}", world.player),
                         lambda state: can_reach_coo(state, world.player))
        for i in [18, *list(range(20, 25))]:
            set_rule(world.multiworld.get_location(f"Cloudy Park 6 - Star {i}", world.player),
                     lambda state: can_reach_ice(state, world.player))
        for i in [19, *list(range(25, 30))]:
            set_rule(world.multiworld.get_location(f"Cloudy Park 6 - Star {i}", world.player),
                     lambda state: can_reach_ice(state, world.player))
    # copy ability access edge cases
    # Kirby cannot eat enemies fully submerged in water. Vast majority of cases, the enemy can be brought to the surface
    # and eaten by inhaling while falling on top of them
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_2_E3, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_3_E6, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    # Ripple Field 4 E5, E7, and E8 are doable, but too strict to leave in logic
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_4_E5, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_4_E7, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_4_E8, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_5_E1, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_5_E2, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_5_E3, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Ripple_Field_5_E4, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Sand_Canyon_4_E7, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Sand_Canyon_4_E8, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Sand_Canyon_4_E9, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))
    set_rule(world.multiworld.get_location(enemy_abilities.Sand_Canyon_4_E10, world.player),
             lambda state: can_reach_kine(state, world.player) or can_reach_chuchu(state, world.player))

    # animal friend rules
    set_rule(world.multiworld.get_location(animal_friend_spawns.iceberg_4_a2, world.player),
             lambda state: can_reach_coo(state, world.player) and can_reach_burning(state, world.player))
    set_rule(world.multiworld.get_location(animal_friend_spawns.iceberg_4_a3, world.player),
             lambda state: can_reach_chuchu(state, world.player) and can_reach_coo(state, world.player)
                           and can_reach_burning(state, world.player))

    for boss_flag, purification, i in zip(["Level 1 Boss - Purified", "Level 2 Boss - Purified",
                                           "Level 3 Boss - Purified", "Level 4 Boss - Purified",
                                           "Level 5 Boss - Purified"],
                                          [location_name.grass_land_whispy, location_name.ripple_field_acro,
                                           location_name.sand_canyon_poncon, location_name.cloudy_park_ado,
                                           location_name.iceberg_dedede],
                                          range(1, 6)):
        set_rule(world.multiworld.get_location(boss_flag, world.player),
                 lambda state, x=i: (state.has("Heart Star", world.player, world.boss_requirements[x - 1])
                                     and can_reach_boss(state, world.player, x,
                                                        world.options.open_world.value,
                                                        world.options.ow_boss_requirement.value,
                                                        world.player_levels)))
        set_rule(world.multiworld.get_location(purification, world.player),
                 lambda state, x=i: (state.has("Heart Star", world.player, world.boss_requirements[x - 1])
                                     and can_reach_boss(state, world.player, x,
                                                        world.options.open_world.value,
                                                        world.options.ow_boss_requirement.value,
                                                        world.player_levels)))

    if world.options.open_world:
        for boss_flag, level in zip(["Level 1 Boss - Defeated", "Level 2 Boss - Defeated", "Level 3 Boss - Defeated",
                                     "Level 4 Boss - Defeated", "Level 5 Boss - Defeated"],
                                    location_name.level_names.keys()):
            set_rule(world.get_location(boss_flag),
                     lambda state, lvl=level: state.has(f"{lvl} - Stage Completion", world.player,
                                                        world.options.ow_boss_requirement.value))

    set_rule(world.multiworld.get_entrance("To Level 6", world.player),
             lambda state: state.has("Heart Star", world.player, world.required_heart_stars))

    for level in range(2, 6):
        set_rule(world.multiworld.get_entrance(f"To Level {level}", world.player),
                 lambda state, x=level: state.has(f"Level {x - 1} Boss Defeated", world.player))

    if world.options.strict_bosses:
        for level in range(2, 6):
            add_rule(world.multiworld.get_entrance(f"To Level {level}", world.player),
                     lambda state, x=level: state.has(f"Level {x - 1} Boss Purified", world.player))

    if world.options.goal_speed == GoalSpeed.option_normal:
        add_rule(world.multiworld.get_entrance("To Level 6", world.player),
                 lambda state: state.has_all(["Level 1 Boss Purified", "Level 2 Boss Purified", "Level 3 Boss Purified",
                                              "Level 4 Boss Purified", "Level 5 Boss Purified"], world.player))
