from math import ceil
from typing import TYPE_CHECKING, Dict, List
from . import names
from .locations import (needle_man_locations, magnet_man_locations, gemini_man_locations, hard_man_locations,
                        top_man_locations, snake_man_locations, spark_man_locations, shadow_man_locations,
                        doc_air_locations, doc_crash_locations, doc_flash_locations, doc_bubble_locations,
                        doc_wood_locations, doc_heat_locations, doc_metal_locations, doc_quick_locations,
                        wily_1_locations, wily_2_locations, wily_3_locations, wily_5_locations,
                        wily_6_locations, energy_pickups, etank_1ups)
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import MM3World
    from BaseClasses import CollectionState

bosses = {
    "Needle Man": 0,
    "Magnet Man": 1,
    "Gemini Man": 2,
    "Hard Man": 3,
    "Top Man": 4,
    "Snake Man": 5,
    "Spark Man": 6,
    "Shadow Man": 7,
    "Doc Robot (Metal)": 8,
    "Doc Robot (Quick)": 9,
    "Doc Robot (Air)": 10,
    "Doc Robot (Crash)": 11,
    "Doc Robot (Flash)": 12,
    "Doc Robot (Bubble)": 13,
    "Doc Robot (Wood)": 14,
    "Doc Robot (Heat)": 15,
    "Break Man": 16,
    "Kamegoro Maker": 17,
    "Yellow Devil MK-II": 18,
    "Holograph Mega Man": 19,
    "Wily Machine 3": 20,
    "Gamma": 21
}

weapons_to_id = {
    "Mega Buster": 0,
    "Needle Cannon": 1,
    "Magnet Missile": 2,
    "Gemini Laser": 3,
    "Hard Knuckle": 4,
    "Top Spin": 5,
    "Search Snake": 6,
    "Spark Shot": 7,
    "Shadow Blade": 8,
}

weapon_damage: Dict[int, List[int]] = {
    0: [1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 0, ],  # Mega Buster
    1: [4, 1, 1, 0, 2, 4, 2, 1, 0, 1, 1, 2, 4, 2, 4, 2, 0, 3, 1, 1, 1, 0, ],  # Needle Cannon
    2: [1, 4, 2, 4, 1, 0, 0, 1, 4, 2, 4, 1, 1, 0, 0, 1, 0, 3, 1, 0, 1, 0, ],  # Magnet Missile
    3: [7, 2, 4, 1, 0, 1, 1, 1, 1, 4, 2, 0, 4, 1, 1, 1, 0, 3, 1, 1, 1, 0, ],  # Gemini Laser
    4: [0, 2, 2, 4, 7, 2, 2, 2, 4, 1, 2, 7, 0, 2, 2, 2, 0, 1, 5, 4, 7, 4, ],  # Hard Knuckle
    5: [1, 1, 2, 0, 4, 2, 1, 7, 0, 1, 1, 4, 1, 1, 2, 7, 0, 1, 0, 7, 0, 2, ],  # Top Spin
    6: [1, 1, 5, 0, 1, 4, 0, 1, 0, 4, 1, 1, 1, 0, 4, 1, 0, 1, 0, 7, 4, 2, ],  # Search Snake
    7: [0, 7, 1, 0, 1, 1, 4, 1, 2, 1, 4, 1, 0, 4, 1, 1, 0, 0, 0, 0, 7, 0, ],  # Spark Shot
    8: [2, 7, 2, 0, 1, 2, 4, 4, 2, 2, 0, 1, 2, 4, 2, 4, 0, 1, 3, 2, 2, 2, ],  # Shadow Blade
}

weapons_to_name: Dict[int, str] = {
    1: names.needle_cannon,
    2: names.magnet_missile,
    3: names.gemini_laser,
    4: names.hard_knuckle,
    5: names.top_spin,
    6: names.search_snake,
    7: names.spark_shock,
    8: names.shadow_blade
}

minimum_weakness_requirement: Dict[int, int] = {
    0: 1,  # Mega Buster is free
    1: 1,  # 112 shots of Needle Cannon
    2: 2,  # 14 shots of Magnet Missile
    3: 1,  # 28 shots of Gemini Laser
    4: 2,  # 14 uses of Hard Knuckle
    5: 4,  # an unknown amount of Top Spin (4 means you should be able to be fine)
    6: 1,  # 56 uses of Search Snake
    7: 2,  # 14 uses of Spark Shot
    8: 1,  # 56 uses of Shadow Blade
}

robot_masters: Dict[int, str] = {
    0: "Needle Man Defeated",
    1: "Magnet Man Defeated",
    2: "Gemini Man Defeated",
    3: "Hard Man Defeated",
    4: "Top Man Defeated",
    5: "Snake Man Defeated",
    6: "Spark Man Defeated",
    7: "Shadow Man Defeated"
}

weapon_costs = {
    0: 0,
    1: 0.25,
    2: 2,
    3: 1,
    4: 2,
    5: 7,  # Not really, but we can really only rely on Top for one RBM
    6: 0.5,
    7: 2,
    8: 0.5,
}


def can_defeat_enough_rbms(state: "CollectionState", player: int, required: int) -> bool:
    can_defeat = 0

    for boss in robot_masters:
        if state.has(robot_masters[boss], player):
            can_defeat += 1
    return can_defeat >= required


def has_rush_vertical(state: "CollectionState", player: int):
    return state.has_any([names.rush_coil, names.rush_jet], player)


def can_traverse_long_water(state: "CollectionState", player: int):
    return state.has_any([names.rush_marine, names.rush_jet], player)


def has_rush_jet(state: "CollectionState", player: int):
    return state.has(names.rush_jet, player)


def set_rules(world: "MM3World") -> None:
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings
    if hasattr(world.multiworld, "re_gen_passthrough"):
        slot_data = getattr(world.multiworld, "re_gen_passthrough")["Mega Man 3"]
        world.weapon_damage = slot_data["weapon_damage"]
    else:
        if world.options.random_weakness == world.options.random_weakness.option_shuffled:
            weapon_tables = [table for weapon, table in weapon_damage.items() if weapon != 0]
            world.random.shuffle(weapon_tables)
            for i in range(1, 9):
                world.weapon_damage[i] = weapon_tables.pop()
        elif world.options.random_weakness == world.options.random_weakness.option_randomized:
            world.weapon_damage = {i: [] for i in range(9)}
            for boss in range(22):
                for weapon in world.weapon_damage:
                    world.weapon_damage[weapon].append(min(14, max(0, int(world.random.normalvariate(3, 3)))))
                if not any([world.weapon_damage[weapon][boss] >= 4
                            for weapon in range(1, 9)]):
                    # failsafe, there should be at least one defined non-Buster weakness
                    weapon = world.random.randint(1, 7)
                    world.weapon_damage[weapon][boss] = world.random.randint(4, 14)  # Force weakness
            # handle Break Man
            boss = 16
            for weapon in world.weapon_damage:
                world.weapon_damage[weapon][boss] = 0
            weapon = world.random.choice(list(world.weapon_damage.keys()))
            world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

        if world.options.strict_weakness:
            for weapon in weapon_damage:
                for i in range(22):
                    if i == 16:
                        continue  # Break is only weak to buster on non-random, and minimal damage on random
                    elif weapon == 0:
                        world.weapon_damage[weapon][i] = 0
                    elif i in (20, 21) and not world.options.random_weakness:
                        continue
                        # Gamma and Wily Machine need all weaknesses present, so allow
                    elif 4 > world.weapon_damage[weapon][i] > 0:
                        world.weapon_damage[weapon][i] = 0
            # handle special cases
            for boss in range(22):
                for weapon in range(1, 9):
                    if (0 < world.weapon_damage[weapon][boss] < minimum_weakness_requirement[weapon] and
                            not any(world.weapon_damage[i][boss] >= minimum_weakness_requirement[weapon]
                                    for i in range(1, 8) if i != weapon)):
                        world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

    for p_boss in world.options.plando_weakness:
        for p_weapon in world.options.plando_weakness[p_boss]:
            if not any(w for w in world.weapon_damage
                       if w != weapons_to_id[p_weapon]
                          and world.weapon_damage[w][bosses[p_boss]] > minimum_weakness_requirement[w]):
                # we need to replace this weakness
                weakness = world.random.choice([key for key in world.weapon_damage if key != weapons_to_id[p_weapon]])
                world.weapon_damage[weakness][bosses[p_boss]] = minimum_weakness_requirement[weakness]
            world.weapon_damage[weapons_to_id[p_weapon]][bosses[p_boss]] \
                = world.options.plando_weakness[p_boss][p_weapon]

    if world.weapon_damage[0][world.options.starting_robot_master.value] < 1:
        world.weapon_damage[0][world.options.starting_robot_master.value] = 1

    # weakness validation, it is better to confirm a completable seed than respect plando
    boss_health = {boss: 0x1C if boss != 12 else 0x1C * 2 for boss in range(8)}

    weapon_energy = {key: float(0x1C) for key in weapon_costs}
    weapon_boss = {boss: {weapon: world.weapon_damage[weapon][boss] for weapon in world.weapon_damage}
                   for boss in range(8)}
    flexibility = [(sum(1 if weapon_boss[boss][weapon] > 0 else 0 for weapon in range(9)) *
                    sum(weapon_boss[boss].values()), boss) for boss in weapon_boss]
    for _, boss in sorted(flexibility):
        boss_damage = weapon_boss[boss]
        weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                         boss_damage.items() if weapon_energy[weapon]}
        while boss_health[boss] > 0:
            if boss_damage[0]:
                boss_health[boss] = 0  # if we can buster, we should buster
                continue
            highest, wp = max(zip(weapon_weight.values(), weapon_weight.keys()))
            uses = weapon_energy[wp] // weapon_costs[wp]
            if int(uses * boss_damage[wp]) > boss_health[boss]:
                used = ceil(boss_health[boss] / boss_damage[wp])
                weapon_energy[wp] -= weapon_costs[wp] * used
                boss_health[boss] = 0
            elif highest <= 0:
                # we are out of weapons that can actually damage the boss
                # so find the weapon that has the most uses, and apply that as an additional weakness
                # it should be impossible to be out of energy
                wp, max_uses = max((weapon, weapon_energy[weapon] // weapon_costs[weapon]) for weapon in weapon_weight
                                   if weapon != 0)
                world.weapon_damage[wp][boss] = minimum_weakness_requirement[wp]
                used = min(int(weapon_energy[wp] // weapon_costs[wp]),
                           ceil(boss_health[boss] // minimum_weakness_requirement[wp]))
                weapon_energy[wp] -= weapon_costs[wp] * used
                boss_health[boss] -= int(used * minimum_weakness_requirement[wp])
                weapon_weight.pop(wp)
            else:
                # drain the weapon and continue
                boss_health[boss] -= int(uses * boss_damage[wp])
                weapon_energy[wp] -= weapon_costs[wp] * uses
                weapon_weight.pop(wp)

    for i, boss_locations in zip(range(22), [
        needle_man_locations,
        magnet_man_locations,
        gemini_man_locations,
        hard_man_locations,
        top_man_locations,
        snake_man_locations,
        spark_man_locations,
        shadow_man_locations,
        doc_metal_locations,
        doc_quick_locations,
        doc_air_locations,
        doc_crash_locations,
        doc_flash_locations,
        doc_bubble_locations,
        doc_wood_locations,
        doc_heat_locations,
        wily_1_locations,
        wily_2_locations,
        wily_3_locations,
        wily_5_locations,
        wily_6_locations
    ]):
        if world.weapon_damage[0][i] > 0:
            continue  # this can always be in logic
        weapons = []
        for weapon in range(1, 9):
            if world.weapon_damage[weapon][i] > 0:
                if world.weapon_damage[weapon][i] < minimum_weakness_requirement[weapon]:
                    continue
                weapons.append(weapons_to_name[weapon])
        if not weapons:
            raise Exception(f"Attempted to have boss {i} with no weakness! Seed: {world.multiworld.seed}")
        for location in boss_locations:
            if i in (20, 21):
                # multi-phase fights, get all potential weaknesses
                # we should probably do this smarter, but this works for now
                add_rule(world.multiworld.get_location(location, world.player),
                         lambda state, weps=tuple(weapons): state.has_all(weps, world.player))
            else:
                add_rule(world.multiworld.get_location(location, world.player),
                         lambda state, weps=tuple(weapons): state.has_any(weps, world.player))

    # Need to defeat x amount of robot masters for Wily 4
    add_rule(world.multiworld.get_location(names.wily_stage_4, world.player),
             lambda state: can_defeat_enough_rbms(state, world.player, world.options.wily_4_requirement.value))

    # Handle Doc Robo stage connections
    for entrance, location in (("To Doc Robot (Needle) - Crash", names.doc_air),
                               ("To Doc Robot (Gemini) - Bubble", names.doc_flash),
                               ("To Doc Robot (Shadow) - Heat", names.doc_wood),
                               ("To Doc Robot (Spark) - Quick", names.doc_metal)):
        entrance_object = world.get_entrance(entrance)
        add_rule(entrance_object, lambda state, loc=location: state.can_reach(loc, "Location", world.player))

    # finally, real logic
    for location in hard_man_locations:
        add_rule(world.get_location(location), lambda state: has_rush_vertical(state, world.player))

    for location in gemini_man_locations:
        add_rule(world.get_location(location), lambda state: state.has_any([names.rush_coil, names.rush_jet,
                                                                            names.rush_marine],
                                                                           world.player))

    add_rule(world.get_entrance("To Doc Robot (Spark) - Metal"),
             lambda state: has_rush_vertical(state, world.player) and
                           state.has_any([names.shadow_blade, names.gemini_laser], world.player))
    add_rule(world.get_entrance("To Doc Robot (Needle) - Air"),
             lambda state: has_rush_vertical(state, world.player))
    add_rule(world.get_entrance("To Doc Robot (Needle) - Crash"),
             lambda state: has_rush_jet(state, world.player))
    add_rule(world.get_entrance("To Doc Robot (Gemini) - Bubble"),
             lambda state: has_rush_vertical(state, world.player) and can_traverse_long_water(state, world.player))

    for location in wily_1_locations:
        add_rule(world.get_location(location), lambda state: has_rush_vertical(state, world.player))

    for location in wily_2_locations:
        add_rule(world.get_location(location), lambda state: has_rush_jet(state, world.player))

    # Wily 3 technically needs vertical
    # However, Wily 3 requires beating Wily 2, and Wily 2 explicitly needs Jet
    # So we can skip the additional rule on Wily 3

    if world.options.consumables in (world.options.consumables.option_1up_etank,
                                     world.options.consumables.option_all):
        add_rule(world.get_location(names.needle_man_c2), lambda state: has_rush_jet(state, world.player))
        add_rule(world.get_location(names.gemini_man_c1), lambda state: has_rush_jet(state, world.player))
        add_rule(world.get_location(names.gemini_man_c3),
                 lambda state: has_rush_vertical(state, world.player)
                               or state.has_any([names.gemini_laser, names.shadow_blade], world.player))
        for location in etank_1ups["Hard Man Stage"]:
            add_rule(world.get_location(location), lambda state: has_rush_vertical(state, world.player))
        add_rule(world.get_location(names.top_man_c6), lambda state: has_rush_vertical(state, world.player))
        add_rule(world.get_location(names.doc_needle_c2), lambda state: has_rush_jet(state, world.player))
        add_rule(world.get_location(names.doc_needle_c3), lambda state: has_rush_jet(state, world.player))
        add_rule(world.get_location(names.doc_gemini_c1), lambda state: has_rush_vertical(state, world.player))
        add_rule(world.get_location(names.doc_gemini_c2), lambda state: has_rush_vertical(state, world.player))
        add_rule(world.get_location(names.wily_1_c8), lambda state: has_rush_vertical(state, world.player))
        for location in [names.wily_1_c4, names.wily_1_c8]:
            add_rule(world.get_location(location), lambda state: state.has(names.hard_knuckle, world.player))
        for location in etank_1ups["Wily Stage 2"]:
            if location == names.wily_2_c3:
                continue
            add_rule(world.get_location(location), lambda state: has_rush_jet(state, world.player))
    if world.options.consumables in (world.options.consumables.option_weapon_health,
                                     world.options.consumables.option_all):
        add_rule(world.get_location(names.gemini_man_c2), lambda state: has_rush_vertical(state, world.player))
        add_rule(world.get_location(names.gemini_man_c4), lambda state: has_rush_vertical(state, world.player))
        add_rule(world.get_location(names.gemini_man_c5), lambda state: has_rush_vertical(state, world.player))
        for location in energy_pickups["Hard Man Stage"]:
            if location == names.hard_man_c1:
                continue
            add_rule(world.get_location(location), lambda state: has_rush_vertical(state, world.player))
        for location in [names.top_man_c2, names.top_man_c3, names.top_man_c4, names.top_man_c7]:
            add_rule(world.get_location(location), lambda state: has_rush_vertical(state, world.player))
        for location in [names.wily_1_c5, names.wily_1_c6, names.wily_1_c7]:
            add_rule(world.get_location(location), lambda state: state.has(names.hard_knuckle, world.player))
        for location in [names.wily_1_c6, names.wily_1_c7, names.wily_1_c11, names.wily_1_c12]:
            add_rule(world.get_location(location), lambda state: has_rush_vertical(state, world.player))
        for location in energy_pickups["Wily Stage 2"]:
            if location in (names.wily_2_c1, names.wily_2_c2, names.wily_2_c4):
                continue
            add_rule(world.get_location(location), lambda state: has_rush_jet(state, world.player))
