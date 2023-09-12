from worlds.AutoWorld import World, CollectionState
from .Locations import LocData, death_wishes, HatInTimeLocation
from .Rules import can_use_hat, can_use_hookshot, can_hit, zipline_logic, has_paintings
from .Types import HatType
from .DeathWishLocations import dw_prereqs, dw_candles
from .Items import HatInTimeItem
from BaseClasses import Entrance, Location, ItemClassification
from worlds.generic.Rules import add_rule
from typing import List, Callable

# Any speedruns expect the player to have Sprint Hat
dw_requirements = {
    "Beat the Heat": LocData(umbrella=True),
    "So You're Back From Outer Space": LocData(hookshot=True),
    "She Speedran from Outer Space": LocData(required_hats=[HatType.SPRINT]),
    "Mafia's Jumps": LocData(required_hats=[HatType.ICE]),
    "Vault Codes in the Wind": LocData(required_hats=[HatType.SPRINT]),

    "Security Breach": LocData(hit_requirement=1),
    "10 Seconds until Self-Destruct": LocData(hookshot=True),
    "Community Rift: Rhythm Jump Studio": LocData(required_hats=[HatType.ICE]),

    "Speedrun Well": LocData(hookshot=True, hit_requirement=1, required_hats=[HatType.SPRINT]),
    "Boss Rush": LocData(hit_requirement=1, umbrella=True),
    "Community Rift: Twilight Travels": LocData(hookshot=True, required_hats=[HatType.DWELLER]),

    "Bird Sanctuary": LocData(hookshot=True),
    "Wound-Up Windmill": LocData(hookshot=True),
    "The Illness has Speedrun": LocData(hookshot=True, required_hats=[HatType.SPRINT]),
    "Community Rift: The Mountain Rift": LocData(hookshot=True, required_hats=[HatType.DWELLER]),
    "Camera Tourist": LocData(misc_required=["Camera Badge"]),

    "The Mustache Gauntlet": LocData(hookshot=True, required_hats=[HatType.DWELLER]),

    "Rift Collapse - Deep Sea": LocData(hookshot=True, required_hats=[HatType.DWELLER]),
}

# Includes main objective requirements
dw_bonus_requirements = {
    # Some One-Hit Hero requirements need badge pins as well because of Hookshot
    "So You're Back From Outer Space": LocData(required_hats=[HatType.SPRINT]),
    "Encore! Encore!": LocData(misc_required=["One-Hit Hero Badge"]),

    "10 Seconds until Self-Destruct": LocData(misc_required=["One-Hit Hero Badge", "Badge Pin"]),

    "Boss Rush": LocData(misc_required=["One-Hit Hero Badge"]),
    "Community Rift: Twilight Travels": LocData(required_hats=[HatType.BREWING]),

    "Bird Sanctuary": LocData(misc_required=["One-Hit Hero Badge", "Badge Pin"], required_hats=[HatType.DWELLER]),
    "Wound-Up Windmill": LocData(misc_required=["One-Hit Hero Badge", "Badge Pin"]),

    "The Mustache Gauntlet": LocData(required_hats=[HatType.ICE]),

    "Rift Collapse - Deep Sea": LocData(required_hats=[HatType.SPRINT]),
}

dw_stamp_costs = {
    "So You're Back From Outer Space":  2,
    "Collect-a-thon":                   5,
    "She Speedran from Outer Space":    8,
    "Encore! Encore!":                  10,

    "Security Breach":                  4,
    "The Great Big Hootenanny":         7,
    "10 Seconds until Self-Destruct":   15,
    "Killing Two Birds":                25,
    "Snatcher Coins in Nyakuza Metro":  30,

    "Speedrun Well":                10,
    "Boss Rush":                    15,
    "Quality Time with Snatcher":   20,
    "Breaching the Contract":       40,

    "Bird Sanctuary":           15,
    "Wound-Up Windmill":        30,
    "The Illness has Speedrun": 35,

    "The Mustache Gauntlet":    35,
    "No More Bad Guys":         50,
    "Seal the Deal":            70,
}


def set_dw_rules(world: World):
    if "Snatcher's Hit List" not in world.get_excluded_dws() \
       or "Camera Tourist" not in world.get_excluded_dws():
        set_enemy_rules(world)

    dw_list: List[str] = []
    if world.multiworld.DWShuffle[world.player].value > 0:
        dw_list = world.get_dw_shuffle()
    else:
        for name in death_wishes.keys():
            dw_list.append(name)

    for name in dw_list:
        if name == "Snatcher Coins in Nyakuza Metro" and not world.is_dlc2():
            continue

        dw = world.multiworld.get_region(name, world.player)
        temp_list: List[Location] = []
        main_objective = world.multiworld.get_location(f"{name} - Main Objective", world.player)
        full_clear = world.multiworld.get_location(f"{name} - All Clear", world.player)
        main_stamp = world.multiworld.get_location(f"Main Stamp - {name}", world.player)
        bonus_stamps = world.multiworld.get_location(f"Bonus Stamps - {name}", world.player)
        temp_list.append(main_objective)
        temp_list.append(full_clear)

        if world.multiworld.DWShuffle[world.player].value == 0:
            if name in dw_stamp_costs.keys():
                for entrance in dw.entrances:
                    add_rule(entrance, lambda state, n=name: get_total_dw_stamps(state, world) >= dw_stamp_costs[n])

        if world.multiworld.DWEnableBonus[world.player].value == 0:
            # place nothing, but let the locations exist still, so we can use them for bonus stamp rules
            full_clear.address = None
            full_clear.place_locked_item(HatInTimeItem("Nothing", ItemClassification.filler, None, world.player))
            full_clear.show_in_spoiler = False

        # No need for rules if excluded - stamps will be auto-granted
        if world.is_dw_excluded(name):
            continue

        # Specific Rules
        if name == "The Illness has Speedrun":
            # killing the flowers without the umbrella is way too slow
            add_rule(main_objective, lambda state: state.has("Umbrella", world.player))
        elif name == "The Mustache Gauntlet":
            # don't get burned bonus requires a way to kill fire crows without being burned
            add_rule(full_clear, lambda state: state.has("Umbrella", world.player)
                     or can_use_hat(state, world, HatType.ICE))
        elif name == "Vault Codes in the Wind":
            add_rule(main_objective, lambda state: can_use_hat(state, world, HatType.TIME_STOP), "or")

        if name in dw_candles:
            set_candle_dw_rules(name, world)

        main_rule: Callable[[CollectionState], bool]

        for i in range(len(temp_list)):
            loc = temp_list[i]
            data: LocData

            if loc.name == main_objective.name:
                data = dw_requirements.get(name)
            else:
                data = dw_bonus_requirements.get(name)

            if data is None:
                continue

            if data.hookshot:
                add_rule(loc, lambda state: can_use_hookshot(state, world))

            for hat in data.required_hats:
                if hat is not HatType.NONE:
                    add_rule(loc, lambda state, h=hat: can_use_hat(state, world, h))

            for misc in data.misc_required:
                add_rule(loc, lambda state, item=misc: state.has(item, world.player))

            if data.umbrella and world.multiworld.UmbrellaLogic[world.player].value > 0:
                add_rule(loc, lambda state: state.has("Umbrella", world.player))

            if data.paintings > 0 and world.multiworld.ShuffleSubconPaintings[world.player].value > 0:
                add_rule(loc, lambda state, paintings=data.paintings: state.has("Progressive Painting Unlock",
                                                                                world.player, paintings))

            if data.hit_requirement > 0:
                if data.hit_requirement == 1:
                    add_rule(loc, lambda state: can_hit(state, world))
                elif data.hit_requirement == 2:  # Can bypass with Dweller Mask (dweller bells)
                    add_rule(loc, lambda state: can_hit(state, world) or can_use_hat(state, world, HatType.DWELLER))

            main_rule = main_objective.access_rule

            if loc.name == main_objective.name:
                add_rule(main_stamp, loc.access_rule)
            elif loc.name == full_clear.name:
                add_rule(loc, main_rule)
                # Only set bonus stamp rules if we don't auto complete bonuses
                if world.multiworld.DWAutoCompleteBonuses[world.player].value == 0 \
                   and not world.is_bonus_excluded(loc.name):
                    add_rule(bonus_stamps, loc.access_rule)

    if world.multiworld.DWShuffle[world.player].value > 0:
        dw_shuffle = world.get_dw_shuffle()
        for i in range(len(dw_shuffle)):
            if i == 0:
                continue

            name = dw_shuffle[i]
            prev_dw = world.multiworld.get_region(dw_shuffle[i-1], world.player)
            entrance = world.multiworld.get_entrance(f"{prev_dw.name} -> {name}", world.player)
            add_rule(entrance, lambda state, n=prev_dw.name: state.has(f"1 Stamp - {n}", world.player))
    else:
        for key, reqs in dw_prereqs.items():
            if key == "Snatcher Coins in Nyakuza Metro" and not world.is_dlc2():
                continue

            access_rules: List[Callable[[CollectionState], bool]] = []
            entrances: List[Entrance] = []

            for parent in reqs:
                entrance = world.multiworld.get_entrance(f"{parent} -> {key}", world.player)
                entrances.append(entrance)

                if not world.is_dw_excluded(parent):
                    access_rules.append(lambda state, n=parent: state.has(f"1 Stamp - {n}", world.player))

            for entrance in entrances:
                for rule in access_rules:
                    add_rule(entrance, rule)

    if world.multiworld.EndGoal[world.player].value == 3:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("1 Stamp - Seal the Deal",
                                                                                      world.player)


def get_total_dw_stamps(state: CollectionState, world: World) -> int:
    if world.multiworld.DWShuffle[world.player].value > 0:
        return 999  # no stamp costs in death wish shuffle

    count: int = 0
    peace_and_tranquility: bool = world.multiworld.DWEnableBonus[world.player].value == 0 \
        and world.multiworld.DWAutoCompleteBonuses[world.player].value == 0

    for name in death_wishes:
        if name == "Snatcher Coins in Nyakuza Metro" and not world.is_dlc2():
            continue

        if state.has(f"1 Stamp - {name}", world.player):
            count += 1
        else:
            continue

        # If bonus rewards and auto bonus completion is off, obtaining stamps via P&T is in logic
        # Candles don't have P&T
        if peace_and_tranquility and name not in dw_candles:
            count += 2
            continue

        if state.has(f"2 Stamps - {name}", world.player):
            count += 2
        elif name not in dw_candles:
            # all non-candle bonus requirements allow the player to get the other stamp (like not having One Hit Hero)
            count += 1

    return count


def set_candle_dw_rules(name: str, world: World):
    main_objective = world.multiworld.get_location(f"{name} - Main Objective", world.player)
    full_clear = world.multiworld.get_location(f"{name} - All Clear", world.player)

    if name == "Zero Jumps":
        add_rule(main_objective, lambda state: get_zero_jump_clear_count(state, world) >= 1)
        add_rule(full_clear, lambda state: get_zero_jump_clear_count(state, world) >= 4
                 and state.has("Train Rush Cleared", world.player) and can_use_hat(state, world, HatType.ICE))

    elif name == "Snatcher's Hit List":
        add_rule(main_objective, lambda state: state.has("Mafia Goon", world.player))
        add_rule(full_clear, lambda state: get_reachable_enemy_count(state, world) >= 12)

    elif name == "Camera Tourist":
        add_rule(main_objective, lambda state: get_reachable_enemy_count(state, world) >= 8)
        add_rule(full_clear, lambda state: can_reach_all_bosses(state, world))

    elif name == "Snatcher Coins in Mafia Town":
        add_rule(main_objective, lambda state: state.has("MT Access", world.player)
                 or state.has("HUMT Access", world.player))

        add_rule(full_clear, lambda state: state.has("CTR Access", world.player)
                 or state.has("HUMT Access", world.player)
                 and (world.multiworld.UmbrellaLogic[world.player].value == 0 or state.has("Umbrella", world.player))
                 or state.has("DWTM Access", world.player)
                 or state.has("TGV Access", world.player))

    elif name == "Snatcher Coins in Battle of the Birds":
        add_rule(main_objective, lambda state: state.has("PP Access", world.player)
                 or state.has("DBS Access", world.player)
                 or state.has("Train Rush Cleared", world.player))

        add_rule(full_clear, lambda state: state.has("PP Access", world.player)
                 and state.has("DBS Access", world.player)
                 and state.has("Train Rush Cleared", world.player))

    elif name == "Snatcher Coins in Subcon Forest":
        add_rule(main_objective, lambda state: state.has("SF Access", world.player))

        add_rule(main_objective, lambda state: has_paintings(state, world, 1) and (can_use_hookshot(state, world)
                 or can_hit(state, world) or can_use_hat(state, world, HatType.DWELLER))
                 or has_paintings(state, world, 3))

        add_rule(full_clear, lambda state: has_paintings(state, world, 3) and can_use_hookshot(state, world)
                 and (can_hit(state, world) or can_use_hat(state, world, HatType.DWELLER)))

    elif name == "Snatcher Coins in Alpine Skyline":
        add_rule(main_objective, lambda state: state.has("LC Access", world.player)
                 or state.has("WM Access", world.player))

        add_rule(full_clear, lambda state: state.has("LC Access", world.player)
                 and state.has("WM Access", world.player))

    elif name == "Snatcher Coins in Nyakuza Metro":
        add_rule(main_objective, lambda state: state.has("Bluefin Tunnel Cleared", world.player)
                 or (state.has("Nyakuza Intro Cleared", world.player)
                 and (state.has("Metro Ticket - Pink", world.player)
                      or state.has("Metro Ticket - Yellow", world.player)
                      and state.has("Metro Ticket - Blue", world.player))))

        add_rule(full_clear, lambda state: state.has("Bluefin Tunnel Cleared", world.player)
                 and (state.has("Nyakuza Intro Cleared", world.player)
                 and (state.has("Metro Ticket - Pink", world.player)
                      or state.has("Metro Ticket - Yellow", world.player)
                      and state.has("Metro Ticket - Blue", world.player))))


def get_zero_jump_clear_count(state: CollectionState, world: World) -> int:
    total: int = 0

    for name, hats in zero_jumps.items():
        if not state.has(f"{name} Cleared", world.player):
            continue

        valid: bool = True

        for hat in hats:
            if not can_use_hat(state, world, hat):
                valid = False
                break

        if valid:
            total += 1

    return total


def get_reachable_enemy_count(state: CollectionState, world: World) -> int:
    count: int = 0
    for enemy in hit_list.keys():
        if enemy in bosses:
            continue

        if state.has(enemy, world.player):
            count += 1

    return count


def can_reach_all_bosses(state: CollectionState, world: World) -> bool:
    for boss in bosses:
        if not state.has(boss, world.player):
            return False

    return True


def create_enemy_events(world: World):
    no_tourist = "Camera Tourist" in world.get_excluded_dws() or "Camera Tourist" in world.get_excluded_bonuses()

    for enemy, regions in hit_list.items():
        if no_tourist and enemy in bosses:
            continue

        for area in regions:
            if (area == "Bon Voyage!" or area == "Time Rift - Deep Sea") and not world.is_dlc1():
                continue

            if area == "Time Rift - Tour" and (not world.is_dlc1()
               or world.multiworld.ExcludeTour[world.player].value > 0):
                continue

            if area == "Bluefin Tunnel" and not world.is_dlc2():
                continue

            if world.multiworld.DWShuffle[world.player].value > 0 and area in death_wishes \
               and area not in world.get_dw_shuffle():
                continue

            region = world.multiworld.get_region(area, world.player)
            event = HatInTimeLocation(world.player, f"{enemy} - {area}", None, region)
            event.place_locked_item(HatInTimeItem(enemy, ItemClassification.progression, None, world.player))
            region.locations.append(event)
            event.show_in_spoiler = False


def set_enemy_rules(world: World):
    no_tourist = "Camera Tourist" in world.get_excluded_dws() or "Camera Tourist" in world.get_excluded_bonuses()

    for enemy, regions in hit_list.items():
        if no_tourist and enemy in bosses:
            continue

        for area in regions:
            if (area == "Bon Voyage!" or area == "Time Rift - Deep Sea") and not world.is_dlc1():
                continue

            if area == "Time Rift - Tour" and (not world.is_dlc1()
                                               or world.multiworld.ExcludeTour[world.player].value > 0):
                continue

            if area == "Bluefin Tunnel" and not world.is_dlc2():
                continue

            if world.multiworld.DWShuffle[world.player].value > 0 and area in death_wishes \
               and area not in world.get_dw_shuffle():
                continue

            event = world.multiworld.get_location(f"{enemy} - {area}", world.player)

            if enemy == "Toxic Flower":
                add_rule(event, lambda state: can_use_hookshot(state, world))

                if area == "The Illness has Spread":
                    add_rule(event, lambda state: not zipline_logic(world) or
                             state.has("Zipline Unlock - The Birdhouse Path", world.player)
                             or state.has("Zipline Unlock - The Lava Cake Path", world.player)
                             or state.has("Zipline Unlock - The Windmill Path", world.player))

            elif enemy == "Director":
                if area == "Dead Bird Studio Basement":
                    add_rule(event, lambda state: can_use_hookshot(state, world))

            elif enemy == "Snatcher" or enemy == "Mustache Girl":
                if area == "Boss Rush":
                    # need to be able to kill toilet
                    add_rule(event, lambda state: can_hit(state, world))

                elif area == "The Finale" and enemy == "Mustache Girl":
                    add_rule(event, lambda state: can_use_hookshot(state, world)
                             and can_use_hat(state, world, HatType.DWELLER))

            elif enemy == "Shock Squid" or enemy == "Ninja Cat":
                if area == "Time Rift - Deep Sea":
                    add_rule(event, lambda state: can_use_hookshot(state, world))


# Zero Jumps completable levels, with required hats if any
zero_jumps = {
    "Welcome to Mafia Town": [],
    "Cheating the Race": [HatType.TIME_STOP],
    "Picture Perfect": [],
    "Train Rush": [HatType.ICE],
    "Contractual Obligations": [],
    "Your Contract has Expired": [],
    "Mail Delivery Service": [],  # rule for needing sprint is already on act completion
}

# Enemies for Snatcher's Hit List/Camera Tourist, and where to find them
hit_list = {
    "Mafia Goon":       ["Mafia Town Area", "Time Rift - Mafia of Cooks", "Time Rift - Tour",
                         "Bon Voyage!", "The Mustache Gauntlet", "Rift Collapse: Mafia of Cooks",
                         "So You're Back From Outer Space"],

    "Sleepy Raccoon":   ["She Came from Outer Space", "Down with the Mafia!", "The Twilight Bell",
                         "She Speedran from Outer Space", "Mafia's Jumps", "The Mustache Gauntlet",
                         "Time Rift - Sleepy Subcon", "Rift Collapse: Sleepy Subcon"],

    "UFO":              ["Picture Perfect", "So You're Back From Outer Space", "Community Rift: Rhythm Jump Studio"],

    "Rat":              ["Down with the Mafia!", "Bluefin Tunnel"],

    "Shock Squid":      ["Bon Voyage!", "Time Rift - Sleepy Subcon", "Time Rift - Deep Sea",
                         "Rift Collapse: Sleepy Subcon"],

    "Shromb Egg":       ["The Birdhouse", "Bird Sanctuary"],

    "Spider":           ["Subcon Forest Area", "The Mustache Gauntlet", "Speedrun Well",
                         "The Lava Cake", "The Windmill"],

    "Crow":             ["Mafia Town Area", "The Birdhouse", "Time Rift - Tour", "Bird Sanctuary",
                         "Time Rift - Alpine Skyline", "Rift Collapse: Alpine Skyline"],

    "Pompous Crow":     ["The Birdhouse", "Time Rift - The Lab", "Bird Sanctuary", "The Mustache Gauntlet"],

    "Fiery Crow":       ["The Finale", "The Lava Cake", "The Mustache Gauntlet"],

    "Express Owl":      ["The Finale", "Time Rift - The Owl Express", "Time Rift - Deep Sea"],

    "Ninja Cat":        ["The Birdhouse", "The Windmill", "Bluefin Tunnel", "The Mustache Gauntlet",
                         "Time Rift - Curly Tail Trail", "Time Rift - Alpine Skyline", "Time Rift - Deep Sea",
                         "Rift Collapse: Alpine Skyline"],

    # Bosses
    "Mafia Boss":       ["Down with the Mafia!", "Encore! Encore!", "Boss Rush"],

    "Conductor":        ["Dead Bird Studio Basement", "Killing Two Birds", "Boss Rush"],
    "Toilet":           ["Toilet of Doom", "Boss Rush"],

    "Snatcher":         ["Your Contract has Expired", "Breaching the Contract", "Boss Rush",
                         "Quality Time with Snatcher"],

    "Toxic Flower":     ["The Illness has Spread", "The Illness has Speedrun"],

    "Mustache Girl":    ["The Finale", "Boss Rush", "No More Bad Guys"],
}

bosses = [
    "Mafia Boss",
    "Conductor",
    "Toilet",
    "Snatcher",
    "Toxic Flower",
    "Mustache Girl",
]
