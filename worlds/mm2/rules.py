from math import ceil
from typing import TYPE_CHECKING, Dict, List
from . import names
from .locations import heat_man_locations, air_man_locations, wood_man_locations, bubble_man_locations, \
    quick_man_locations, flash_man_locations, metal_man_locations, crash_man_locations, wily_1_locations, \
    wily_2_locations, wily_3_locations, wily_4_locations, wily_5_locations, wily_6_locations
from .options import bosses, weapons_to_id, Consumables, RandomWeaknesses
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import MM2World
    from BaseClasses import CollectionState

weapon_damage: Dict[int, List[int]] = {
    0: [2,  2,  1,   1,  2,   2,  1,   1,   1,  7,  1,  0,    1,   -1],  # Mega Buster
    1: [-1, 6,  0xE, 0,  0xA, 6,  4,   6,   8,  13, 8,  0,    0xE, -1],  # Atomic Fire
    2: [2,  0,  4,   0,  2,   0,  0,   0xA, 0,  0,  0,  0,    1,   -1],  # Air Shooter
    3: [0,  8,  -1,  0,  0,   0,  0,   0,   0,  0,  0,  0,    0,   -1],  # Leaf Shield
    4: [6,  0,  0,   -1, 0,   2,  0,   1,   0,  14, 1,  0,    0,    1],  # Bubble Lead
    5: [2,  2,  0,   2,  0,   0,  4,   1,   1,  7,  2,  0,    1,   -1],  # Quick Boomerang
    6: [-1, 0,  2,   2,  4,   3,  0,   0,   1,  0,  1,  0x14, 1,   -1],  # Crash Bomber
    7: [1,  0,  2,   4,  0,   4,  0xE, 0,   0,  7,  0,  0,    1,   -1],  # Metal Blade
    8: [0,  0,  0,   0,  2,   0,  0,   0,   0,  0,  0,  0,    0,    0],  # Time Stopper
}

weapons_to_name: Dict[int, str] = {
    1: names.atomic_fire,
    2: names.air_shooter,
    3: names.leaf_shield,
    4: names.bubble_lead,
    5: names.quick_boomerang,
    6: names.crash_bomber,
    7: names.metal_blade,
    8: names.time_stopper
}

minimum_weakness_requirement: Dict[int, int] = {
    0: 1,  # Mega Buster is free
    1: 14,  # 2 shots of Atomic Fire
    2: 2,  # 14 shots of Air Shooter
    3: 4,  # 9 uses of Leaf Shield, 3 ends up 1 damage off
    4: 1,  # 56 uses of Bubble Lead
    5: 1,  # 224 uses of Quick Boomerang
    6: 4,  # 7 uses of Crash Bomber
    7: 1,  # 112 uses of Metal Blade
    8: 4,  # 1 use of Time Stopper, but setting to 4 means we shave the entire HP bar
}

robot_masters: Dict[int, str] = {
    0: "Heat Man Defeated",
    1: "Air Man Defeated",
    2: "Wood Man Defeated",
    3: "Bubble Man Defeated",
    4: "Quick Man Defeated",
    5: "Flash Man Defeated",
    6: "Metal Man Defeated",
    7: "Crash Man Defeated"
}

weapon_costs = {
    0: 0,
    1: 10,
    2: 2,
    3: 3,
    4: 0.5,
    5: 0.125,
    6: 4,
    7: 0.25,
    8: 7,
}


def can_defeat_enough_rbms(state: "CollectionState", player: int,
                           required: int, boss_requirements: Dict[int, List[int]]):
    can_defeat = 0
    for boss, reqs in boss_requirements.items():
        if boss in robot_masters:
            if state.has_all(map(lambda x: weapons_to_name[x], reqs), player):
                can_defeat += 1
                if can_defeat >= required:
                    return True
    return False


def set_rules(world: "MM2World") -> None:
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings
    if (hasattr(world.multiworld, "re_gen_passthrough")
            and "Mega Man 2" in getattr(world.multiworld, "re_gen_passthrough")):
        slot_data = getattr(world.multiworld, "re_gen_passthrough")["Mega Man 2"]
        world.weapon_damage = slot_data["weapon_damage"]
        world.wily_5_weapons = slot_data["wily_5_weapons"]
    else:
        if world.options.random_weakness == RandomWeaknesses.option_shuffled:
            weapon_tables = [table.copy() for weapon, table in weapon_damage.items() if weapon not in (0, 8)]
            world.random.shuffle(weapon_tables)
            for i in range(1, 8):
                world.weapon_damage[i] = weapon_tables.pop()
            # alien must take minimum required damage from his weakness
            alien_weakness = next(weapon for weapon in range(8) if world.weapon_damage[weapon][13] != -1)
            world.weapon_damage[alien_weakness][13] = minimum_weakness_requirement[alien_weakness]
            world.weapon_damage[8] = [0 for _ in range(14)]
            world.weapon_damage[8][world.random.choice(range(8))] = 2
        elif world.options.random_weakness == RandomWeaknesses.option_randomized:
            world.weapon_damage = {i: [] for i in range(9)}
            for boss in range(13):
                for weapon in world.weapon_damage:
                    world.weapon_damage[weapon].append(min(14, max(-1, int(world.random.normalvariate(3, 3)))))
                if not any([world.weapon_damage[weapon][boss] >= max(4, minimum_weakness_requirement[weapon])
                            for weapon in range(1, 7)]):
                    # failsafe, there should be at least one defined non-Buster weakness
                    weapon = world.random.randint(1, 7)
                    world.weapon_damage[weapon][boss] = world.random.randint(
                        max(4, minimum_weakness_requirement[weapon]), 14)  # Force weakness
            # special case, if boobeam trap has a weakness to Crash, it needs to be max damage
            if world.weapon_damage[6][11] > 4:
                world.weapon_damage[6][11] = 14
            # handle the alien
            boss = 13
            for weapon in world.weapon_damage:
                world.weapon_damage[weapon].append(-1)
            weapon = world.random.choice(list(world.weapon_damage.keys()))
            world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

        if world.options.strict_weakness:
            for weapon in weapon_damage:
                for i in range(13):
                    if weapon == 0:
                        world.weapon_damage[weapon][i] = 0
                    elif i in (8, 12) and not world.options.random_weakness:
                        continue
                        # Mecha Dragon only has damage range of 0-1, so allow the 1
                        # Wily Machine needs all three weaknesses present, so allow
                    elif 4 > world.weapon_damage[weapon][i] > 0:
                        world.weapon_damage[weapon][i] = 0

        for p_boss in world.options.plando_weakness:
            boss = bosses[p_boss]
            for p_weapon in world.options.plando_weakness[p_boss]:
                weapon = weapons_to_id[p_weapon]
                if world.options.plando_weakness[p_boss][p_weapon] < minimum_weakness_requirement[weapon] \
                        and not any(w != weapon
                                    and world.weapon_damage[w][boss] >= minimum_weakness_requirement[w]
                                    for w in world.weapon_damage):
                    # we need to replace this weakness
                    weakness = world.random.choice([key for key in world.weapon_damage if key != weapon])
                    world.weapon_damage[weakness][boss] = minimum_weakness_requirement[weakness]
                world.weapon_damage[weapon][boss] = world.options.plando_weakness[p_boss][p_weapon]

        # handle special cases
        for boss in range(14):
            for weapon in (1, 2, 3, 6, 8):
                if (0 < world.weapon_damage[weapon][boss] < minimum_weakness_requirement[weapon] and
                        not any(world.weapon_damage[i][boss] >= minimum_weakness_requirement[i]
                                for i in range(9) if i != weapon)):
                    # Weapon does not have enough possible ammo to kill the boss, raise the damage
                    world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

        for weapon in (1, 6):
            if (world.weapon_damage[weapon][9] >= minimum_weakness_requirement[weapon] and
                    not any(world.weapon_damage[i][9] >= minimum_weakness_requirement[i]
                            for i in range(9) if i not in (1, 6))):
                # Atomic Fire and Crash Bomber cannot be Picopico-kun's only weakness
                world.weapon_damage[weapon][9] = 0
                weakness = world.random.choice((2, 3, 4, 5, 7, 8))
                world.weapon_damage[weakness][9] = minimum_weakness_requirement[weakness]

        if (world.weapon_damage[1][11] >= minimum_weakness_requirement[1] and
                not any(world.weapon_damage[i][11] >= minimum_weakness_requirement[i]
                        for i in range(9) if i != 1)):
            # Atomic Fire cannot be Boobeam Trap's only weakness
            world.weapon_damage[1][11] = 0
            weakness = world.random.choice((2, 3, 4, 5, 6, 7, 8))
            world.weapon_damage[weakness][11] = minimum_weakness_requirement[weakness]

        if world.weapon_damage[0][world.options.starting_robot_master.value] < 1:
            world.weapon_damage[0][world.options.starting_robot_master.value] = \
                weapon_damage[0][world.options.starting_robot_master.value]

        # final special case
        # There's a vanilla crash if Time Stopper kills Wily phase 1
        # There's multiple fixes, but ensuring Wily cannot take Time Stopper damage is best
        if world.weapon_damage[8][12] > 0:
            world.weapon_damage[8][12] = 0

        # weakness validation, it is better to confirm a completable seed than respect plando
        boss_health = {boss: 0x1C if boss != 12 else 0x1C * 2 for boss in [*range(8), 12]}

        weapon_energy = {key: float(0x1C) for key in weapon_costs}
        weapon_boss = {boss: {weapon: world.weapon_damage[weapon][boss] for weapon in world.weapon_damage}
                       for boss in [*range(8), 12]}
        flexibility = {
            boss: (
                    sum(damage_value > 0 for damage_value in
                        weapon_damages.values())  # Amount of weapons that hit this boss
                    * sum(weapon_damages.values())  # Overall damage that those weapons do
            )
            for boss, weapon_damages in weapon_boss.items() if boss != 12
        }
        flexibility = sorted(flexibility, key=flexibility.get)  # Fast way to sort dict by value
        used_weapons = {i: set() for i in [*range(8), 12]}
        for boss in [*flexibility, 12]:
            boss_damage = weapon_boss[boss]
            weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                             boss_damage.items() if weapon_energy[weapon] > 0}
            if boss_damage[8]:
                boss_damage[8] = 1.75 * boss_damage[8]
            if any(boss_damage[i] > 0 for i in range(8)) and 8 in weapon_weight:
                # We get exactly one use of Time Stopper during the rush
                # So we want to make sure that use is absolutely needed
                weapon_weight[8] = min(weapon_weight[8], 0.001)
            while boss_health[boss] > 0:
                if boss_damage[0] > 0:
                    boss_health[boss] = 0  # if we can buster, we should buster
                    continue
                highest, wp = max(zip(weapon_weight.values(), weapon_weight.keys()))
                uses = weapon_energy[wp] // weapon_costs[wp]
                if int(uses * boss_damage[wp]) > boss_health[boss]:
                    used = ceil(boss_health[boss] / boss_damage[wp])
                    weapon_energy[wp] -= weapon_costs[wp] * used
                    boss_health[boss] = 0
                    used_weapons[boss].add(wp)
                elif highest <= 0:
                    # we are out of weapons that can actually damage the boss
                    # so find the weapon that has the most uses, and apply that as an additional weakness
                    # it should be impossible to be out of energy, simply because even if every boss took 1 from
                    # Quick Boomerang and no other, it would only be 28 off from defeating all 9,
                    # which Metal Blade should be able to cover
                    wp, max_uses = max((weapon, weapon_energy[weapon] // weapon_costs[weapon])
                                       for weapon in weapon_weight
                                       if weapon != 0 and (weapon != 8 or boss != 12))
                    # Wily Machine cannot under any circumstances take damage from Time Stopper, prevent this
                    world.weapon_damage[wp][boss] = minimum_weakness_requirement[wp]
                    used = min(int(weapon_energy[wp] // weapon_costs[wp]),
                               ceil(boss_health[boss] / minimum_weakness_requirement[wp]))
                    weapon_energy[wp] -= weapon_costs[wp] * used
                    boss_health[boss] -= int(used * minimum_weakness_requirement[wp])
                    weapon_weight.pop(wp)
                    used_weapons[boss].add(wp)
                else:
                    # drain the weapon and continue
                    boss_health[boss] -= int(uses * boss_damage[wp])
                    weapon_energy[wp] -= weapon_costs[wp] * uses
                    weapon_weight.pop(wp)
                    used_weapons[boss].add(wp)

        world.wily_5_weapons = {boss: sorted(used_weapons[boss]) for boss in used_weapons}

    for i, boss_locations in enumerate([
        heat_man_locations,
        air_man_locations,
        wood_man_locations,
        bubble_man_locations,
        quick_man_locations,
        flash_man_locations,
        metal_man_locations,
        crash_man_locations,
        wily_1_locations,
        wily_2_locations,
        wily_3_locations,
        wily_4_locations,
        wily_5_locations,
        wily_6_locations
    ]):
        if world.weapon_damage[0][i] > 0:
            continue  # this can always be in logic
        weapons = []
        for weapon in range(1, 9):
            if world.weapon_damage[weapon][i] > 0:
                if world.weapon_damage[weapon][i] < minimum_weakness_requirement[weapon]:
                    continue  # Atomic Fire can only be considered logical for bosses it can kill in 2 hits
                weapons.append(weapons_to_name[weapon])
        if not weapons:
            raise Exception(f"Attempted to have boss {i} with no weakness! Seed: {world.multiworld.seed}")
        for location in boss_locations:
            if i == 12:
                add_rule(world.get_location(location),
                         lambda state, weps=tuple(weapons): state.has_all(weps, world.player))
                # TODO: when has_list gets added, check for a subset of possible weaknesses
            else:
                add_rule(world.get_location(location),
                         lambda state, weps=tuple(weapons): state.has_any(weps, world.player))

    # Always require Crash Bomber for Boobeam Trap
    add_rule(world.get_location(names.wily_4),
             lambda state: state.has(names.crash_bomber, world.player))
    add_rule(world.get_location(names.wily_stage_4),
             lambda state: state.has(names.crash_bomber, world.player))

    # Need to defeat x amount of robot masters for Wily 5
    add_rule(world.get_location(names.wily_5),
             lambda state: can_defeat_enough_rbms(state, world.player, world.options.wily_5_requirement.value,
                                                  world.wily_5_weapons))
    add_rule(world.get_location(names.wily_stage_5),
             lambda state: can_defeat_enough_rbms(state, world.player, world.options.wily_5_requirement.value,
                                                  world.wily_5_weapons))

    if not world.options.yoku_jumps:
        add_rule(world.get_entrance("To Heat Man Stage"),
                 lambda state: state.has(names.item_2, world.player))

    if not world.options.enable_lasers:
        add_rule(world.get_entrance("To Quick Man Stage"),
                 lambda state: state.has(names.time_stopper, world.player))

    if world.options.consumables in (Consumables.option_1up_etank,
                                     Consumables.option_all):
        add_rule(world.get_location(names.flash_man_c2),
                 lambda state: state.has_any([names.item_1, names.item_2, names.item_3], world.player))
        add_rule(world.get_location(names.quick_man_c1),
                 lambda state: state.has_any([names.item_1, names.item_2, names.item_3], world.player))
        add_rule(world.get_location(names.metal_man_c2),
                 lambda state: state.has_any([names.item_1, names.item_2], world.player))
        add_rule(world.get_location(names.metal_man_c3),
                 lambda state: state.has_any([names.item_1, names.item_2], world.player))
        add_rule(world.get_location(names.crash_man_c3),
                 lambda state: state.has_any([names.item_1, names.item_2, names.item_3], world.player))
        add_rule(world.get_location(names.wily_2_c5),
                 lambda state: state.has(names.crash_bomber, world.player))
        add_rule(world.get_location(names.wily_2_c6),
                 lambda state: state.has(names.crash_bomber, world.player))
        add_rule(world.get_location(names.wily_3_c2),
                 lambda state: state.has(names.crash_bomber, world.player))
    if world.options.consumables in (Consumables.option_weapon_health,
                                     Consumables.option_all):
        add_rule(world.get_location(names.flash_man_c3),
                 lambda state: state.has(names.crash_bomber, world.player))
        add_rule(world.get_location(names.flash_man_c4),
                 lambda state: state.has(names.crash_bomber, world.player))
        add_rule(world.get_location(names.wily_3_c1),
                 lambda state: state.has(names.crash_bomber, world.player))
