from typing import TYPE_CHECKING, Dict
from BaseClasses import Region, CollectionState, Location
from worlds.generic.Rules import add_rule

from .locations import location_table, Hidden
from ...options import PorgyFuelDifficulty, PorgyRadar

if TYPE_CHECKING:
    from ... import UFO50World


fuel = "Porgy - Fuel Tank"
fish_gratitude = "Porgy - Fish Gratitude"
torpedo = "Porgy - Torpedo Upgrade"
mcguffin = "Porgy - Strange Light"
buster = "Porgy - Buster Torpedoes Module"
missile = "Porgy - Missile System Module"
depth_charge = "Porgy - Depth Charge Module"
spotlight = "Porgy - Spotlight Module"
drill = "Porgy - Drill Module"
radar = "Porgy - Radar System Module"
homing = "Porgy - Targeting System Module"
efficiency = "Porgy - Efficient Fuel Module"

ship_rocks = "Bombed Open the Ship"
urchin_rock = "Bombed the Buster Urchin Path Exit Rock"
leftmost_rock = "Bombed the Leftmost Abyss Entrance Rock"
second_left_rock = "Bombed the Second from Left Abyss Entrance Rock"
rightmost_rock = "Bombed the Rightmost Abyss Rock"


def get_porgy_location(name: str, world: "UFO50World") -> Location:
    return world.get_location(f"Porgy - {name}")


def has_bomb(state: CollectionState, player: int) -> bool:
    return state.has_any((depth_charge, missile), player)


def has_light(state: CollectionState, world: "UFO50World") -> bool:
    return world.options.porgy_lanternless or state.has(spotlight, world.player)


def can_combat(target_score: int, state: CollectionState, player: int) -> bool:
    score = state.count(torpedo, player)

    if score >= target_score:
        return True
    # it's low enough that the other items here won't save it, so we might as well early out
    if score < target_score - 12:
        return False

    score += state.count(fish_gratitude, player) // 5 * 2

    if score >= target_score:
        return True
    # it's low enough that the other items here won't save it, so we might as well early out
    if score < target_score - 4:
        return False

    extra_power_count: int = state.has(buster, player) + state.has(missile, player)
    slots = min(4, 2 + state.count(mcguffin, player) // 2)

    score += min(extra_power_count, slots - 1) * 2

    if score >= target_score:
        return True
    return False


def has_abyss_combat_logic(state: CollectionState, player: int) -> bool:
    torpedo_count = state.count(torpedo, player)
    # from looking at the map and hidden items, it seems they expect you to have 8 torpedo upgrades
    # as well as the missile launcher and/or burst torpedoes and the first 2 fish helpers
    if torpedo_count < 8:
        return False
    if torpedo_count < 10:
        return state.has(fish_gratitude, player, 5)
    return True


def setup_lantern_and_radar_table(world: "UFO50World") -> None:
    world.porgy_lantern_and_radar_slots_req = {}
    for location_name, location_data in location_table.items():
        mods_needed = 0
        if not world.options.porgy_lanternless and location_data.region_name == "Abyss":
            mods_needed += 1
        if location_data.concealed == Hidden.has_tell and world.options.porgy_radar == PorgyRadar.option_required:
            mods_needed += 1
        elif location_data.concealed == Hidden.no_tell and world.options.porgy_radar >= PorgyRadar.option_required:
            mods_needed += 1
        world.porgy_lantern_and_radar_slots_req[location_name] = mods_needed
    mods_needed = 0

    # setting up the shortcut version
    if not world.options.porgy_lanternless:
        mods_needed += 1
    world.porgy_lantern_and_radar_slots_req[""] = mods_needed
    world.porgy_lantern_and_radar_slots_req["Abyss Rock"] = mods_needed


def has_fuel(amount: int, state: CollectionState, world: "UFO50World") -> bool:
    """
    Checks if you have enough fuel based on which fuel difficulty option was chosen.
    """
    if world.options.porgy_fuel_difficulty == PorgyFuelDifficulty.option_easy:
        # medium
        amount = round(amount * 1.5)
    elif world.options.porgy_fuel_difficulty == PorgyFuelDifficulty.option_medium:
        # easy
        amount = round(amount * 1.25)

    # you start with 4 fuel tanks
    if amount <= 4:
        return True
    # max fuel is 24, requiring all fuel tanks is a pain
    amount = min(amount, 21)
    return state.has(fuel, world.player, amount - 4)


def has_fuel_opt_eff(amount: int, state: CollectionState, world: "UFO50World") -> bool:
    """
    Runs has_fuel, and if it fails, checkes for the Efficient Fuel module and runs it again with less fuel required.
    Use this if the location cannot require more than 2 modules.
    """
    if has_fuel(amount, state, world):
        return True
    return state.has(efficiency, world.player) and has_fuel(round(3 * amount / 4), state, world)


def has_fuel_and_slots(fuel_needed: int, loc_name: str, extra_mods_needed: int,
                       state: CollectionState, world: "UFO50World") -> bool:
    """
    A mix of has_fuel_opt_eff and has_enough_slots, basically.
    loc_name is used to figure out if you need the Spotlight and if you need the Radar.
    loc_name is either the name of the location, "Abyss Rock" to tell it to check the Lanternless option,
    or "" to tell it that no Spotlight or Radar are required.
    extra_mods_needed is how many mod slots you need on top of that may be required by the location.
    """
    num_slots = min(4, state.count(mcguffin, world.player) // 2 + 2)
    # if you don't have enough slots, it's not possible for you to get any further here
    slots_needed = world.porgy_lantern_and_radar_slots_req[loc_name] + extra_mods_needed
    if slots_needed > num_slots:
        return False
    # conversely, if you have enough fuel now, you don't need to check further
    if has_fuel(fuel_needed, state, world):
        return True

    fuel_with_efficiency = round(3 * fuel_needed / 4)
    slots_needed += 1
    if slots_needed > num_slots:
        return False
    return has_fuel(fuel_with_efficiency, state, world)


# set the basic fuel requirements for spots that don't have multiple viable routes
def set_fuel_and_radar_reqs(world: "UFO50World", on_touch: bool) -> None:
    for loc_name, loc_data in location_table.items():
        try:
            loc = get_porgy_location(loc_name, world)
        except KeyError:
            if loc_name == "Cherry":
                continue
            else:
                raise Exception("UFO 50: Unknown error occurred in Porgy regarding location names.")
        if (loc_data.concealed == Hidden.no_tell and world.options.porgy_radar >= PorgyRadar.option_required
                or loc_data.concealed == Hidden.has_tell and world.options.porgy_radar == PorgyRadar.option_required):
            add_rule(loc, lambda state: state.has(radar, world.player))

        fuel_needed = loc_data.fuel_touch if on_touch else loc_data.fuel_get
        # if it is not set, it means it has some special requirements
        if not fuel_needed:
            continue
        add_rule(loc, lambda state, amt=fuel_needed: has_fuel_opt_eff(amt, state, world))


# there's going to be a lot of parentheses containing and/or that don't need them, it's for sanity purposes
def create_rules(world: "UFO50World", regions: Dict[str, Region]) -> None:
    player = world.player
    check_on_touch = bool(world.options.porgy_check_on_touch)
    set_fuel_and_radar_reqs(world, check_on_touch)
    setup_lantern_and_radar_table(world)

    regions["Menu"].connect(regions["Shallows"])
    regions["Shallows"].connect(regions["Deeper"])
    regions["Shallows"].connect(regions["Shallows - Buster"],
                                rule=lambda state: state.has(buster, player))
    regions["Shallows"].connect(regions["Shallows - Missile"],
                                rule=lambda state: has_bomb(state, player))
    regions["Shallows"].connect(regions["Shallows - Depth"],
                                rule=lambda state: state.has(depth_charge, player))
    regions["Shallows"].connect(regions["Sunken Ship"],
                                rule=lambda state: state.has("Porgy - Bombed Open the Ship", player))
    regions["Sunken Ship"].connect(regions["Sunken Ship - Buster"],
                                   rule=lambda state: state.has(buster, player))
    # vanilla seems to want you to have 8 torpedo upgrades, 2 fish friends, missiles, and buster before abyss
    regions["Deeper"].connect(regions["Abyss"],
                              rule=lambda state: has_light(state, world) and can_combat(16, state, player))

    # events
    add_rule(get_porgy_location("Sunken Ship", world),
             rule=lambda state: state.has(depth_charge, world.player)
             or (state.has(missile, world.player) and has_fuel_opt_eff(6, state, world)))

    add_rule(get_porgy_location("Rock at Buster Urchin Path", world),
             rule=lambda state:
             (state.has_all((missile, buster), player) and has_fuel_and_slots(7, "", 2, state, world))
             or (state.has(depth_charge, player) and has_fuel_opt_eff(7, state, world)))

    add_rule(get_porgy_location("Rock at Leftmost Abyss Entrance", world),
             rule=lambda state: has_fuel_opt_eff(7, state, world) and state.has(depth_charge, player))

    add_rule(get_porgy_location("Rock at Second from Left Abyss Entrance", world),
             rule=lambda state: (has_fuel_opt_eff(6, state, world) and state.has(depth_charge, player))
             or (has_fuel_opt_eff(7, state, world) and state.has(missile, player)))

    add_rule(get_porgy_location("Rightmost Abyss Rock", world),
             rule=lambda state: (has_fuel_and_slots(8, "Abyss Rock", 1, state, world)
                                 and state.has(depth_charge, player))
             or (state.has(missile, player)
                 and (has_fuel_and_slots(12, "Abyss Rock", 2, state, world) and state.has(buster, player))
                 or (has_fuel_and_slots(11, "Abyss Rock", 2, state, world) and state.has(drill, player))))

    # buster is covered by the region
    add_rule(get_porgy_location("Shallows Upper Mid - Fuel Tank in Floor at Surface", world),
             lambda state: state.has(depth_charge, player))

    add_rule(get_porgy_location("Deeper Upper Mid - Spotlight Module", world),
             lambda state: state.has(depth_charge, player))

    add_rule(get_porgy_location("Deeper Upper Left - Fuel Tank behind ! Blocks", world),
             lambda state: state.has(buster, player))

    # bosses
    add_rule(get_porgy_location("Lamia", world),
             lambda state: (has_fuel_opt_eff(7, state, world) and can_combat(5, state, player))
             or (state.has(depth_charge, player) and has_fuel_opt_eff(5, state, world)))

    add_rule(get_porgy_location("Iku Turso", world),
             lambda state: (has_fuel_opt_eff(7, state, world) and can_combat(5, state, player))
             or (state.has(depth_charge, player) and has_fuel_opt_eff(5, state, world)))

    add_rule(get_porgy_location("Bakunawa", world),
             lambda state: (has_fuel_opt_eff(10, state, world) and can_combat(12, state, player))
             or (state.has(depth_charge, player) and has_fuel_opt_eff(8, state, world)))

    add_rule(get_porgy_location("Neptune", world),
             lambda state: (has_fuel_opt_eff(10, state, world) and can_combat(12, state, player))
             or (state.has(depth_charge, player) and has_fuel_opt_eff(8, state, world)))

    add_rule(get_porgy_location("Dracula", world),
             lambda state: (has_fuel_opt_eff(13, state, world) and can_combat(20, state, player))
             or (state.has(depth_charge, player) and has_fuel_opt_eff(13, state, world)))

    if check_on_touch:
        # shallows coral maze, buster covered by region
        loc = "Shallows Upper Right - Fuel Tank in Coral Maze"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state:
                 (has_fuel_opt_eff(7, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(3, loc, 2, state, world)))
        loc = "Shallows Upper Right - Torpedo Upgrade in Coral Maze"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_fuel_opt_eff(9, state, world)
                 or (state.has(drill, player) and has_fuel_and_slots(5, loc, 2, state, world)))
        loc = "Shallows Upper Right - Egg in Coral Maze"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_fuel_opt_eff(11, state, world)
                 or (state.has(drill, player) and has_fuel_and_slots(7, loc, 2, state, world)))

        # faster through the ship
        loc = "Deeper Upper Left - Torpedo Upgrade in Wall"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_fuel_opt_eff(4, state, world)
                 or (state.has(depth_charge, player)
                     and has_fuel_and_slots(3, loc, 1, state, world)))

        loc = "Deeper Upper Mid - Torpedo Upgrade in Ceiling"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_bomb(state, player)
                 and has_fuel_and_slots(3, loc, 1, state, world))

        loc = "Deeper Upper Mid - Egg in Dirt"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: state.has(drill, player)
                 and has_fuel_and_slots(3, loc, 1, state, world))

        loc = "Deeper Lower Mid - Fuel Tank in Floor"
        add_rule(get_porgy_location(loc, world),
                 lambda state: state.has(depth_charge, player)
                 and has_fuel_and_slots(4, loc, 1, state, world))

        loc = "Deeper Lower Right - Fuel Tank in Ceiling"
        add_rule(get_porgy_location(loc, world),
                 lambda state: has_bomb(state, player)
                 and has_fuel_and_slots(4, loc, 1, state, world))

        # abyss
        # requires spotlight (covered by the region)
        # unless noted otherwise, routes were added together using partial routes
        # recommended to get more accurate numbers over time, probably during testing
        loc = "Abyss Upper Left - Egg on Seaweed near Urchins"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state:
                 # go through the ship
                 (state.has(depth_charge, player) and has_fuel_and_slots(4, loc, 1, state, world))
                 # go around and through the dirt instead, less fuel than opening ship with missile
                 or (state.has(drill, player) and has_fuel_and_slots(5, loc, 1, state, world)))

        loc = "Abyss Upper Left - Egg on Seaweed above Torpedo Upgrade"
        add_rule(get_porgy_location(loc, world),
                 # itemless: not valid
                 # drill only: 6.5/13
                 # depth only: 4/8
                 # missile only: not valid
                 # buster only: 6/10
                 # buster + drill: 5/10
                 # drill + missile: 7/14 (worse than drill only)
                 # buster + missile: x/9
                 # buster + drill + depth charge path: 4/8 (same as depth only, so not relevant)
                 # buster + drill + missile path: x/8 (7 to open the rock with missile, 8 for the more efficient path)
                 rule=lambda state:
                 (state.has(depth_charge, player) and has_fuel_and_slots(4, loc, 1, state, world))
                 or (state.has_all((drill, buster), player)
                     and has_fuel_and_slots(5, loc, 2, state, world))
                 or (state.has(buster, player) and has_fuel_and_slots(6, loc, 1, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(7, loc, 1, state, world)))

        loc = "Abyss Upper Left - Torpedo Upgrade in Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # see above
                 rule=lambda state:
                 (state.has(depth_charge, player) and has_fuel_and_slots(4, loc, 1, state, world))
                 or (state.has_all((drill, buster), player) and has_fuel_and_slots(5, loc, 2, state, world))
                 or (state.has(buster, player) and has_fuel_and_slots(6, loc, 1, state, world))
                 or (state.has_all((drill, missile), player) and has_fuel_and_slots(7, loc, 2, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(8, loc, 1, state, world)))

        loc = "Abyss Lower Left - Egg in Facility"
        add_rule(get_porgy_location(loc, world),
                 # hard-requires drill, depth, or buster
                 # drill only: invalid
                 # buster only: invalid
                 # depth only: 7/10, only because you can only bring 2 depth charges with you
                 # buster + drill: 9/14
                 # buster + depth: 6/12 (12 > 10)
                 # drill + depth: 6/11 (11 > 10)
                 # buster + drill + missile: 8/12 (must bring missile with you, so you need the slots for it)
                 # buster + drill + depth: worse than depth only
                 rule=lambda state:
                 (state.has(depth_charge, player)
                  and (has_fuel_and_slots(7, loc, 1, state, world)
                       or (state.has_any((buster, drill), player) and has_fuel_and_slots(6, loc, 2, state, world))))
                 or (state.has_all((buster, drill), player) and has_fuel_and_slots(9, loc, 2, state, world))
                 or (state.has_all((buster, drill, missile), player) and has_fuel_and_slots(8, loc, 3, state, world)))

        loc = "Abyss Lower Left - Torpedo Upgrade in Facility"
        add_rule(get_porgy_location(loc, world),
                 # almost the same as the previous one, with slightly different fuel amounts
                 # hard-requires drill, depth, or buster
                 # drill only: invalid
                 # buster only: invalid
                 # depth only: 7/10
                 # buster + drill: 9/15
                 # buster + depth: 6/x
                 # drill + depth: 6/x
                 # buster + drill + missile: 9/13 (must bring missile with you, so you need the slots for it)
                 # buster + drill + depth: worse than depth only
                 rule=lambda state:
                 (state.has(depth_charge, player)
                  and (has_fuel_and_slots(7, loc, 1, state, world)
                       or (state.has_any((buster, drill), player) and has_fuel_and_slots(6, loc, 2, state, world))))
                 or (state.has_all((buster, drill), player) and has_fuel_and_slots(9, loc, 2, state, world))
                 or (state.has_all((buster, drill, missile), player) and has_fuel_and_slots(9, loc, 3, state, world)))

        loc = "Abyss Lower Left - Fuel Tank in Facility Floor"
        add_rule(get_porgy_location(loc, world),
                 # requires buster and depth
                 # buster + depth: 7/9
                 # all others look worse
                 rule=lambda state:
                 state.has_all((buster, depth_charge), player) and has_fuel_and_slots(7, loc, 2, state, world))

        loc = "Abyss Upper Mid - Torpedo Upgrade in Wall"
        add_rule(get_porgy_location(loc, world),
                 # depth + drill: 3.375/6.75 (don't need to bring depth with for non-touch)
                 # drill only: 4.375/8.75
                 # drill + missile: x/7.75
                 # buster only: 4.75/9.5
                 # depth only: 4.75/9.5
                 rule=lambda state:
                 (state.has_all((depth_charge, drill), player) and has_fuel_and_slots(4, loc, 2, state, world))
                 or (state.has_any((drill, buster, depth_charge), player)
                     and has_fuel_and_slots(5, loc, 1, state, world)))

        loc = "Abyss Upper Mid - Efficient Fuel Module"
        add_rule(get_porgy_location(loc, world),
                 # depth + drill: 3.625/7.25
                 # depth only: 5.125/10.25
                 rule=lambda state:
                 (state.has(depth_charge, player) and has_fuel_and_slots(6, loc, 1, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(4, loc, 1, state, world)))

        loc = "Abyss Upper Mid - Torpedo Upgrade in Cave"
        add_rule(get_porgy_location(loc, world),
                 # drill hard-required
                 # depth + drill: 4/8
                 # depth + drill + buster: same amount as depth + drill, so invalid
                 # drill + buster: 4/8
                 # drill + buster + missile (to pre-open rock, but only go down with drill): 7/8
                 # drill only: 5/10
                 rule=lambda state:
                 state.has(drill, player)
                 and (has_fuel_and_slots(5, loc, 1, state, world)
                      or (state.has_any((buster, depth_charge), player)
                          and has_fuel_and_slots(4, loc, 2, state, world))))

        loc = "Abyss Upper Mid - Egg on Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 4.5/9
                 # buster only: 4.5/9
                 # drill only: 4.75/9.5
                 # drill + break second to left rock: x/7.5
                 rule=lambda state: state.has_any((depth_charge, buster, drill), player)
                 and has_fuel_and_slots(5, loc, 1, state, world))

        loc = "Abyss Upper Mid - Egg in Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # buster only: 4/8
                 # depth only: 4/8
                 # drill only: 5/10
                 # drill + break second to left rock: x/8
                 rule=lambda state:
                 (state.has_any((urchin_rock, buster), player) and has_fuel_and_slots(4, loc, 1, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(5, loc, 1, state, world)))

        loc = "Abyss Upper Mid - Torpedo Upgrade behind Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # buster only: 4.25/8.5
                 # depth only: 4.25/8.5
                 # drill only: 5.25/10.5
                 rule=lambda state:
                 (state.has_any((urchin_rock, buster), player) and has_fuel_and_slots(5, loc, 1, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(6, loc, 1, state, world)))

        loc = "Abyss Upper Right - Egg by Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # buster only: 4.75/9.5
                 # depth only: 7.75/15.5
                 # drill only: 4.5/9
                 rule=lambda state:
                 (state.has_any((buster, drill), player) and has_fuel_and_slots(5, loc, 1, state, world))
                 or (state.has(depth_charge, player) and has_fuel_and_slots(8, loc, 1, state, world))
                 or (state.has(urchin_rock, player) and has_fuel_opt_eff(8, state, world))
                 or (state.has(rightmost_rock, player)))  # requires 8 fuel already

        loc = "Abyss Lower Right - Fuel Tank in Floor"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 4.5/9, and dpeth is required, this is the only path we need to evaluate
                 rule=lambda state: state.has(depth_charge, player) and has_fuel_and_slots(5, loc, 1, state, world))

        loc = "Abyss Lower Right - Egg by Skull"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 7/14
                 # drill only: 4.25/8.5
                 # buster only: 5.5/11
                 rule=lambda state:
                 (state.has(depth_charge, player) and has_fuel_and_slots(7, loc, 1, state, world))
                 or (state.has(rightmost_rock, player))  # requires 8 fuel min already
                 or (state.has(drill, player) and has_fuel_and_slots(5, loc, 1, state, world))
                 or (state.has(buster, player) and has_fuel_and_slots(6, loc, 1, state, world)))

        loc = "Abyss Lower Right - Radar System Module"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 6.5/12
                 # drill only: 5.5/10.25
                 # missile path requires drill and is exclusively longer than the drill only path
                 rule=lambda state:
                 (state.has(drill, player) and has_fuel_and_slots(6, loc, 1, state, world))
                 or (state.has(depth_charge, player) and has_fuel_and_slots(7, loc, 1, state, world)))

        loc = "Abyss Lower Right - Armor Plating Module"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 5.5/11
                 # buster only: 5.625/11.25
                 # drill only: 5.375/10.75
                 rule=lambda state:
                 (state.has_any((depth_charge, drill, buster), player) and has_fuel_and_slots(6, loc, 1, state, world))
                 or (state.has_any((rightmost_rock, urchin_rock), player)))  # fuel is covered by the event

    else:
        # shallows coral maze
        # buster is covered by the region
        loc = "Shallows Upper Right - Fuel Tank in Coral Maze"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_fuel_opt_eff(13, state, world)
                 or (state.has(drill, player) and has_fuel_and_slots(6, loc, 2, state, world)))
        loc = "Shallows Upper Right - Torpedo Upgrade in Coral Maze"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_fuel_opt_eff(15, state, world)
                 or (state.has(drill, player) and has_fuel_and_slots(8, loc, 2, state, world)))
        loc = "Shallows Upper Right - Egg in Coral Maze"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_fuel_opt_eff(16, state, world)
                 or (state.has(drill, player) and has_fuel_and_slots(9, loc, 2, state, world)))

        # faster through the ship
        loc = "Deeper Upper Left - Torpedo Upgrade in Wall"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_fuel_opt_eff(8, state, world)
                 or (state.has(ship_rocks, player) and has_fuel_opt_eff(5, state, world)))

        loc = "Deeper Upper Mid - Torpedo Upgrade in Ceiling"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: has_bomb(state, player)
                 and has_fuel_and_slots(6, loc, 1, state, world))

        loc = "Deeper Upper Mid - Egg in Dirt"
        add_rule(get_porgy_location(loc, world),
                 rule=lambda state: state.has(drill, player)
                 and has_fuel_and_slots(5, loc, 1, state, world))

        loc = "Deeper Lower Mid - Fuel Tank in Floor"
        add_rule(get_porgy_location(loc, world),
                 lambda state: state.has(depth_charge, player)
                 and has_fuel_and_slots(7, loc, 1, state, world))

        loc = "Deeper Lower Right - Fuel Tank in Ceiling"
        add_rule(get_porgy_location(loc, world),
                 lambda state: has_bomb(state, player)
                 and has_fuel_and_slots(7, loc, 1, state, world))

        # abyss
        loc = "Abyss Upper Left - Egg on Seaweed near Urchins"
        add_rule(get_porgy_location(loc, world),
                 # I promise you this rule is correct, buster can't reach it
                 rule=lambda state:
                 state.has_any((depth_charge, drill), player) and has_fuel_and_slots(9, loc, 1, state, world))

        loc = "Abyss Upper Left - Egg on Seaweed above Torpedo Upgrade"
        add_rule(get_porgy_location(loc, world),
                 # see this check in the on touch section
                 rule=lambda state:
                 (state.has(depth_charge, player) and has_fuel_and_slots(8, loc, 1, state, world))
                 or (state.has_all((drill, buster, urchin_rock), player)
                     and has_fuel_and_slots(8, loc, 2, state, world))
                 or (state.has_all((buster, urchin_rock), player) and has_fuel_and_slots(9, loc, 1, state, world))
                 or (state.has(buster, player) and has_fuel_and_slots(10, loc, 1, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(13, loc, 1, state, world)))

        loc = "Abyss Upper Left - Torpedo Upgrade in Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # see above
                 # you can shoot the seaweed below without depth or fish buddies
                 rule=lambda state:
                 (state.has(depth_charge, player) and has_fuel_and_slots(8, loc, 1, state, world))
                 or (state.has_all((drill, buster, urchin_rock), player)
                     and has_fuel_and_slots(8, loc, 2, state, world))
                 or (state.has_all((buster, urchin_rock), player) and has_fuel_and_slots(9, loc, 1, state, world))
                 or (state.has(buster, player) and has_fuel_and_slots(10, loc, 1, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(13, loc, 1, state, world)))

        loc = "Abyss Lower Left - Egg in Facility"
        add_rule(get_porgy_location(loc, world),
                 # hard-requires drill, depth, or buster
                 # drill only: invalid
                 # buster only: invalid
                 # depth only: 7/10, only because you can only bring 2 depth charges with you
                 # buster + drill: 9/14
                 # buster + depth: 6/12 (12 > 10)
                 # drill + depth: 6/11 (11 > 10)
                 # buster + drill + missile: 8/12 (must bring missile with you, so you need the slots for it)
                 # buster + drill + depth: worse than depth only
                 rule=lambda state:
                 (state.has(depth_charge, player) and has_fuel_and_slots(10, loc, 1, state, world))
                 or (state.has_all((buster, drill), player) and has_fuel_and_slots(14, loc, 2, state, world))
                 or (state.has_all((buster, drill, missile), player) and has_fuel_and_slots(12, loc, 3, state, world)))

        loc = "Abyss Lower Left - Torpedo Upgrade in Facility"
        add_rule(get_porgy_location(loc, world),
                 # hard-requires drill, depth, or buster
                 # drill only: invalid
                 # buster only: invalid
                 # depth only: 7/10
                 # buster + drill: 9/15
                 # buster + depth: 6/x
                 # drill + depth: 6/x
                 # buster + drill + missile: 9/13 (must bring missile with you, so you need the slots for it)
                 # buster + drill + depth: worse than depth only
                 rule=lambda state:
                 (state.has(depth_charge, player) and has_fuel_and_slots(10, loc, 1, state, world))
                 or (state.has_all((buster, drill), player) and has_fuel_and_slots(15, loc, 2, state, world))
                 or (state.has_all((buster, drill, missile), player) and has_fuel_and_slots(13, loc, 3, state, world)))

        loc = "Abyss Lower Left - Fuel Tank in Facility Floor"
        add_rule(get_porgy_location(loc, world),
                 # requires buster and depth
                 # buster + depth: 7/9
                 # all others look worse
                 rule=lambda state:
                 state.has_all((buster, depth_charge), player) and has_fuel_and_slots(9, loc, 2, state, world))

        loc = "Abyss Upper Mid - Torpedo Upgrade in Wall"
        add_rule(get_porgy_location(loc, world),
                 # depth + drill: 3.375/6.75 (don't need to bring depth with for non-touch)
                 # drill only: 4.375/8.75
                 # drill + missile: x/7.75 (don't need to bring missile for non-touch)
                 # buster only: 4.75/9.5
                 # depth only: 4.75/9.5
                 rule=lambda state:
                 state.has(drill, player)
                 and ((state.has(second_left_rock, player) and has_fuel_and_slots(7, loc, 1, state, world))
                      or (has_fuel_and_slots(9, loc, 1, state, world)))
                 or (state.has(buster, player) and has_fuel_and_slots(10, loc, 1, state, world))
                 or (state.has(urchin_rock, player) and has_fuel_and_slots(10, loc, 0, state, world)))

        loc = "Abyss Upper Mid - Efficient Fuel Module"
        add_rule(get_porgy_location(loc, world),
                 # depth + drill: 3.625/7.25
                 # depth only: 5.125/10.25
                 rule=lambda state: state.has(depth_charge, player)
                 and has_fuel_and_slots(11, loc, 1, state, world)
                 or (state.has(drill, player) and has_fuel_and_slots(8, loc, 2, state, world)))

        loc = "Abyss Upper Mid - Torpedo Upgrade in Cave"
        add_rule(get_porgy_location(loc, world),
                 # depth + drill: 4/8
                 # depth + drill + buster: same amount as depth + drill, so invalid
                 # drill + buster: 4/8
                 # drill + buster + missile (to pre-open rock, but only go down with drill): 7/8
                 # drill only: 5/10
                 rule=lambda state: state.has(drill, player)
                 and ((state.has(urchin_rock, player) and has_fuel_and_slots(8, loc, 1, state, world))
                      or has_fuel_and_slots(10, loc, 1, state, world)))

        loc = "Abyss Upper Mid - Egg on Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 4.5/9
                 # buster only: 4.5/9
                 # drill only: 4.75/9.5
                 # drill + break second to left rock: x/7.5
                 rule=lambda state:
                 (state.has_any((depth_charge, buster), player) and has_fuel_and_slots(9, loc, 1, state, world))
                 or (state.has(drill, player)
                     and (has_fuel_and_slots(10, loc, 1, state, world)
                          or (state.has(second_left_rock, player) and has_fuel_and_slots(8, loc, 1, state, world)))))

        loc = "Abyss Upper Mid - Egg in Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # buster only: 4/8
                 # depth only: 4/8
                 # drill only: 5/10
                 # drill + break second to left rock: slower than breaking urchin path rock
                 rule=lambda state:
                 (state.has(buster, player) and has_fuel_and_slots(8, loc, 1, state, world))
                 or (state.has(urchin_rock, player) and has_fuel_and_slots(8, loc, 0, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(10, loc, 1, state, world)))

        loc = "Abyss Upper Mid - Torpedo Upgrade behind Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # buster only: 4.25/8.5
                 # depth only: 4.25/8.5
                 # drill only: 5.25/10.5
                 # drill + break second to left rock: slower than breaking urchin path rock
                 rule=lambda state:
                 (state.has(buster, player) and has_fuel_and_slots(9, loc, 1, state, world))
                 or (state.has(urchin_rock, player) and has_fuel_opt_eff(9, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(11, loc, 1, state, world)))

        loc = "Abyss Upper Right - Egg by Seaweed"
        add_rule(get_porgy_location(loc, world),
                 # buster only: 4.75/9.5
                 # depth only: 7.75/15.5
                 # drill only: 4.5/9
                 rule=lambda state:
                 (state.has(drill, player) and has_fuel_and_slots(9, loc, 1, state, world))
                 or (state.has(buster, player) and has_fuel_and_slots(10, loc, 1, state, world))
                 or (state.has(depth_charge, player) and has_fuel_and_slots(16, loc, 1, state, world)))

        loc = "Abyss Lower Right - Fuel Tank in Floor"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 4.5/9, and since it's required, this is the only logically relevant path
                 rule=lambda state: state.has(depth_charge, player) and has_fuel_and_slots(9, loc, 1, state, world))

        loc = "Abyss Lower Right - Egg by Skull"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 7/14
                 # drill only: 4.25/8.5
                 # buster only: 5.5/11
                 rule=lambda state:
                 (state.has(rightmost_rock, player) and has_fuel_opt_eff(14, state, world))
                 or (state.has(drill, player) and has_fuel_and_slots(9, loc, 1, state, world))
                 or (state.has(buster, player) and has_fuel_and_slots(11, loc, 1, state, world)))

        loc = "Abyss Lower Right - Radar System Module"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 6.5/12
                 # drill only: 5.5/10.25
                 rule=lambda state:
                 (state.has(drill, player) and has_fuel_and_slots(11, loc, 1, state, world))
                 or (state.has(depth_charge, player) and has_fuel_and_slots(12, loc, 1, state, world)))

        loc = "Abyss Lower Right - Armor Plating Module"
        add_rule(get_porgy_location(loc, world),
                 # depth only: 5.5/11
                 # buster only: 5.625/11.25
                 # drill only: 5.375/10.75
                 rule=lambda state:
                 (state.has_any((depth_charge, drill), player) and has_fuel_and_slots(11, loc, 1, state, world))
                 or (state.has(buster, player) and has_fuel_and_slots(12, loc, 1, state, world)))

    add_rule(get_porgy_location("Garden", world),
             rule=lambda state: get_porgy_location("Lamia", world).can_reach(state))

    add_rule(get_porgy_location("Gold", world),
             rule=lambda state: can_combat(26, state, player) and has_fuel(16, state, world))
    if "Porgy" in world.options.cherry_allowed_games:
        add_rule(get_porgy_location("Cherry", world),
                 rule=lambda state: can_combat(26, state, player) and has_fuel(16, state, world)
                 and state.has_all((depth_charge, drill), player)
                 and has_light(state, world))
