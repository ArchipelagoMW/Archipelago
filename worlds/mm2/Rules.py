import typing
from . import Names
from .Locations import heat_man_locations, air_man_locations, wood_man_locations, bubble_man_locations, \
    quick_man_locations, flash_man_locations, metal_man_locations, crash_man_locations, wily_1_locations, \
    wily_2_locations, wily_3_locations, wily_4_locations, wily_5_locations, wily_6_locations
from worlds.generic.Rules import set_rule, add_rule

if typing.TYPE_CHECKING:
    from . import MM2World
    from BaseClasses import CollectionState

weapon_damage: typing.Dict[int, typing.List[int]] = {
    0: [2, 2, 1, 1, 2, 2, 1, 1, 1, 7, 1, 0, 1, -1],  # Mega Buster
    1: [-1, 6, 0xE, 0, 0xA, 6, 4, 6, 8, 13, 8, 0, 0xE, -1],  # Atomic Fire
    2: [2, 0, 4, 0, 2, 0, 0, 0xA, 0, 0, 0, 0, 1, -1],  # Air Shooter
    3: [0, 8, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],  # Leaf Shield
    4: [6, 0, 0, -1, 0, 2, 0, 1, 0, 14, 1, 0, 0, 1],  # Bubble Lead
    5: [2, 2, 0, 2, 0, 0, 4, 1, 1, 7, 2, 0, 1, -1],  # Quick Boomerang
    6: [-1, 0, 2, 2, 4, 3, 0, 0, 1, 0, 1, 0x14, 1, -1],  # Crash Bomber
    7: [1, 0, 2, 4, 0, 4, 0xE, 0, 0, 7, 0, 0, 1, -1],  # Metal Blade
}

weapons_to_name = {
    1: Names.atomic_fire,
    2: Names.air_shooter,
    3: Names.leaf_shield,
    4: Names.bubble_lead,
    5: Names.quick_boomerang,
    6: Names.crash_bomber,
    7: Names.metal_blade
}

minimum_weakness_requirement = {
    0: 1,  # Mega Buster is free
    1: 14,  # 2 shots of Atomic Fire
    2: 1,  # 14 shots of Air Shooter, although you likely hit more than one shot
    3: 4,  # 9 uses of Leaf Shield, 3 ends up 1 damage off
    4: 1,  # 56 uses of Bubble Lead
    5: 1,  # 224 uses of Quick Boomerang
    6: 4,  # 7 uses of Crash Bomber
    7: 1,  # 112 uses of Metal Blade
}

robot_masters = {
    0: "Heat Man Defeated",
    1: "Air Man Defeated",
    2: "Wood Man Defeated",
    3: "Bubble Man Defeated",
    4: "Quick Man Defeated",
    5: "Flash Man Defeated",
    6: "Metal Man Defeated",
    7: "Crash Man Defeated"
}


def can_defeat_enough_rbms(state: "CollectionState", player: int, required: int):
    can_defeat = 0
    for boss in robot_masters:
        if state.has(robot_masters[boss], player):
            can_defeat += 1
    return can_defeat >= required


def set_rules(world: "MM2World") -> None:
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings
    if world.options.random_weakness:
        world.weapon_damage = {i: [] for i in range(8)}
        for boss in range(13):
            for weapon in world.weapon_damage:
                world.weapon_damage[weapon].append(min(14, max(-1, int(world.random.normalvariate(3, 3)))))
            if not any([world.weapon_damage[weapon][boss] > 4 for weapon in range(1, 7)]):
                # failsafe, there should be at least one defined non-Buster weakness
                weapon = world.random.randint(1, 7)
                world.weapon_damage[weapon][boss] = world.random.randint(4, 14)  # Force weakness
        # handle the alien
        boss = 13
        for weapon in world.weapon_damage:
            world.weapon_damage[weapon].append(-1)
        weapon = world.random.choice(list(world.weapon_damage.keys()))
        world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

    if world.options.strict_weakness:
        for weapon in weapon_damage:
            for i in range(13):
                if i == 8 and not world.options.random_weakness:
                    continue
                if weapon == 0 or 4 > world.weapon_damage[weapon][i] > 0:
                    world.weapon_damage[weapon][i] = 0
        # handle atomic fire
        for boss in range(14):
            if world.weapon_damage[1][boss] >= 4 and not any(world.weapon_damage[i][boss] > 0 for i in range(2, 8)):
                # Atomic Fire can only shoot two fully powered shots
                # So we need to be able to kill the boss in 2 hits
                world.weapon_damage[1][boss] = 14
        starting = world.options.starting_robot_master.value
        world.weapon_damage[0][starting] = 1

    for i, boss in zip(range(14), [
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
        if i == 11:
            continue  # Boobeam Trap is handled after
        weapons = []
        for weapon in range(1, 8):
            if world.weapon_damage[weapon][i] > 0:
                if weapon == 1 and world.weapon_damage[weapon][i] < 14:
                    continue  # Atomic Fire can only be considered logical for bosses it can kill in 2 hits
                weapons.append(weapons_to_name[weapon])
        if not weapons:
            raise Exception(f"Attempted to have boss {i} with no weakness! Seed: {world.multiworld.seed}")
        for location in boss:
            add_rule(world.multiworld.get_location(location, world.player),
                     lambda state, weps=tuple(weapons): state.has_any(weps, world.player))

    # Always require Crash Bomber for Boobeam Trap
    add_rule(world.multiworld.get_location(Names.wily_4, world.player),
             lambda state: state.has(Names.crash_bomber, world.player))
    add_rule(world.multiworld.get_location(Names.wily_stage_4, world.player),
             lambda state: state.has(Names.crash_bomber, world.player))

    # Need to defeat x amount of robot masters for Wily 5
    add_rule(world.multiworld.get_location(Names.wily_5, world.player),
             lambda state: can_defeat_enough_rbms(state, world.player, world.options.wily_5_requirement.value))
    add_rule(world.multiworld.get_location(Names.wily_stage_5, world.player),
             lambda state: can_defeat_enough_rbms(state, world.player, world.options.wily_5_requirement.value))

    if not world.options.yoku_jumps:
        add_rule(world.multiworld.get_entrance("To Heat Man Stage", world.player),
                 lambda state: state.has(Names.item_2, world.player))

    if not world.options.enable_lasers:
        add_rule(world.multiworld.get_entrance("To Quick Man Stage", world.player),
                 lambda state: state.has(Names.time_stopper, world.player))

    if world.options.consumables:
        add_rule(world.multiworld.get_location(Names.flash_man_c2, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2, Names.item_3], world.player))
        add_rule(world.multiworld.get_location(Names.flash_man_c3, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.flash_man_c4, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.quick_man_c1, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2, Names.item_3], world.player))
        add_rule(world.multiworld.get_location(Names.metal_man_c2, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2], world.player))
        add_rule(world.multiworld.get_location(Names.metal_man_c3, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2], world.player))
        add_rule(world.multiworld.get_location(Names.crash_man_c3, world.player),
                 lambda state: state.has_any([Names.item_1, Names.item_2, Names.item_3], world.player))
        add_rule(world.multiworld.get_location(Names.wily_2_c5, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.wily_2_c6, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.wily_3_c1, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
        add_rule(world.multiworld.get_location(Names.wily_3_c2, world.player),
                 lambda state: state.has(Names.crash_bomber, world.player))
