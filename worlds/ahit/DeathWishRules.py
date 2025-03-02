from worlds.AutoWorld import CollectionState
from .Rules import can_use_hat, can_use_hookshot, can_hit, zipline_logic, get_difficulty, has_paintings
from .Types import HatType, Difficulty, HatInTimeLocation, HatInTimeItem, LocData, HitType
from .DeathWishLocations import dw_prereqs, dw_candles
from BaseClasses import Entrance, Location, ItemClassification
from worlds.generic.Rules import add_rule, set_rule
from typing import List, Callable, TYPE_CHECKING
from .Locations import death_wishes
from .Options import EndGoal

if TYPE_CHECKING:
    from . import HatInTimeWorld


# Any speedruns expect the player to have Sprint Hat
dw_requirements = {
    "Beat the Heat": LocData(hit_type=HitType.umbrella),
    "So You're Back From Outer Space": LocData(hookshot=True),
    "Mafia's Jumps": LocData(required_hats=[HatType.ICE]),
    "Vault Codes in the Wind": LocData(required_hats=[HatType.SPRINT]),

    "Security Breach": LocData(hit_type=HitType.umbrella_or_brewing),
    "10 Seconds until Self-Destruct": LocData(hookshot=True),
    "Community Rift: Rhythm Jump Studio": LocData(required_hats=[HatType.ICE]),

    "Speedrun Well": LocData(hookshot=True, hit_type=HitType.umbrella_or_brewing),
    "Boss Rush": LocData(hit_type=HitType.umbrella, hookshot=True),
    "Community Rift: Twilight Travels": LocData(hookshot=True, required_hats=[HatType.DWELLER]),

    "Bird Sanctuary": LocData(hookshot=True),
    "Wound-Up Windmill": LocData(hookshot=True),
    "The Illness has Speedrun": LocData(hookshot=True),
    "Community Rift: The Mountain Rift": LocData(hookshot=True, required_hats=[HatType.DWELLER]),
    "Camera Tourist": LocData(misc_required=["Camera Badge"]),

    "The Mustache Gauntlet": LocData(hookshot=True, required_hats=[HatType.DWELLER]),

    "Rift Collapse: Deep Sea": LocData(hookshot=True),
}

# Includes main objective requirements
dw_bonus_requirements = {
    # Some One-Hit Hero requirements need badge pins as well because of Hookshot
    "So You're Back From Outer Space": LocData(required_hats=[HatType.SPRINT]),
    "Encore! Encore!": LocData(misc_required=["One-Hit Hero Badge"]),

    "10 Seconds until Self-Destruct": LocData(misc_required=["One-Hit Hero Badge", "Badge Pin"]),

    "Boss Rush": LocData(misc_required=["One-Hit Hero Badge", "Badge Pin"]),
    "Community Rift: Twilight Travels": LocData(required_hats=[HatType.BREWING]),

    "Bird Sanctuary": LocData(misc_required=["One-Hit Hero Badge", "Badge Pin"], required_hats=[HatType.DWELLER]),
    "Wound-Up Windmill": LocData(misc_required=["One-Hit Hero Badge", "Badge Pin"]),
    "The Illness has Speedrun": LocData(required_hats=[HatType.SPRINT]),

    "The Mustache Gauntlet": LocData(required_hats=[HatType.ICE]),

    "Rift Collapse: Deep Sea": LocData(required_hats=[HatType.DWELLER]),
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

required_snatcher_coins = {
    "Snatcher Coins in Mafia Town": ["Snatcher Coin - Top of HQ", "Snatcher Coin - Top of Tower",
                                     "Snatcher Coin - Under Ruined Tower"],

    "Snatcher Coins in Battle of the Birds": ["Snatcher Coin - Top of Red House", "Snatcher Coin - Train Rush",
                                              "Snatcher Coin - Picture Perfect"],

    "Snatcher Coins in Subcon Forest": ["Snatcher Coin - Swamp Tree", "Snatcher Coin - Manor Roof",
                                        "Snatcher Coin - Giant Time Piece"],

    "Snatcher Coins in Alpine Skyline": ["Snatcher Coin - Goat Village Top", "Snatcher Coin - Lava Cake",
                                         "Snatcher Coin - Windmill"],

    "Snatcher Coins in Nyakuza Metro": ["Snatcher Coin - Green Clean Tower", "Snatcher Coin - Bluefin Cat Train",
                                        "Snatcher Coin - Pink Paw Fence"],
}


def set_dw_rules(world: "HatInTimeWorld"):
    if "Snatcher's Hit List" not in world.excluded_dws or "Camera Tourist" not in world.excluded_dws:
        set_enemy_rules(world)

    dw_list: List[str] = []
    if world.options.DWShuffle:
        dw_list = world.dw_shuffle
    else:
        for name in death_wishes.keys():
            dw_list.append(name)

    for name in dw_list:
        if name == "Snatcher Coins in Nyakuza Metro" and not world.is_dlc2():
            continue

        dw = world.multiworld.get_region(name, world.player)
        if not world.options.DWShuffle and name in dw_stamp_costs.keys():
            for entrance in dw.entrances:
                add_rule(entrance, lambda state, n=name: state.has("Stamps", world.player, dw_stamp_costs[n]))

        main_objective = world.multiworld.get_location(f"{name} - Main Objective", world.player)
        all_clear = world.multiworld.get_location(f"{name} - All Clear", world.player)
        main_stamp = world.multiworld.get_location(f"Main Stamp - {name}", world.player)
        bonus_stamps = world.multiworld.get_location(f"Bonus Stamps - {name}", world.player)
        if not world.options.DWEnableBonus:
            # place nothing, but let the locations exist still, so we can use them for bonus stamp rules
            all_clear.address = None
            all_clear.place_locked_item(HatInTimeItem("Nothing", ItemClassification.filler, None, world.player))
            all_clear.show_in_spoiler = False

        # No need for rules if excluded - stamps will be auto-granted
        if world.is_dw_excluded(name):
            continue

        modify_dw_rules(world, name)
        add_dw_rules(world, main_objective)
        add_dw_rules(world, all_clear)
        add_rule(main_stamp, main_objective.access_rule)
        add_rule(all_clear, main_objective.access_rule)
        # Only set bonus stamp rules to require All Clear if we don't auto complete bonuses
        if not world.options.DWAutoCompleteBonuses and not world.is_bonus_excluded(all_clear.name):
            add_rule(bonus_stamps, all_clear.access_rule)
        else:
            # As soon as the Main Objective is completed, the bonuses auto-complete.
            add_rule(bonus_stamps, main_objective.access_rule)

    if world.options.DWShuffle:
        for i in range(len(world.dw_shuffle)-1):
            name = world.dw_shuffle[i+1]
            prev_dw = world.multiworld.get_region(world.dw_shuffle[i], world.player)
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

    if world.options.EndGoal == EndGoal.option_seal_the_deal:
        world.multiworld.completion_condition[world.player] = lambda state: \
            state.has("1 Stamp - Seal the Deal", world.player)


def add_dw_rules(world: "HatInTimeWorld", loc: Location):
    bonus: bool = "All Clear" in loc.name
    if not bonus:
        data = dw_requirements.get(loc.parent_region.name)
    else:
        data = dw_bonus_requirements.get(loc.parent_region.name)

    if data is None:
        return

    if data.hookshot:
        add_rule(loc, lambda state: can_use_hookshot(state, world))

    for hat in data.required_hats:
        add_rule(loc, lambda state, h=hat: can_use_hat(state, world, h))

    for misc in data.misc_required:
        add_rule(loc, lambda state, item=misc: state.has(item, world.player))

    if data.paintings > 0 and world.options.ShuffleSubconPaintings:
        add_rule(loc, lambda state, paintings=data.paintings: has_paintings(state, world, paintings))

    if data.hit_type is not HitType.none and world.options.UmbrellaLogic:
        if data.hit_type == HitType.umbrella:
            add_rule(loc, lambda state: state.has("Umbrella", world.player))

        elif data.hit_type == HitType.umbrella_or_brewing:
            add_rule(loc, lambda state: state.has("Umbrella", world.player)
                     or can_use_hat(state, world, HatType.BREWING))

        elif data.hit_type == HitType.dweller_bell:
            add_rule(loc, lambda state: state.has("Umbrella", world.player)
                     or can_use_hat(state, world, HatType.BREWING)
                     or can_use_hat(state, world, HatType.DWELLER))


def modify_dw_rules(world: "HatInTimeWorld", name: str):
    difficulty: Difficulty = get_difficulty(world)
    main_objective = world.multiworld.get_location(f"{name} - Main Objective", world.player)
    full_clear = world.multiworld.get_location(f"{name} - All Clear", world.player)

    if name == "The Illness has Speedrun":
        # All stamps with hookshot only in Expert
        if difficulty >= Difficulty.EXPERT:
            set_rule(full_clear, lambda state: True)
        else:
            add_rule(main_objective, lambda state: state.has("Umbrella", world.player))

    elif name == "The Mustache Gauntlet":
        add_rule(main_objective, lambda state: state.has("Umbrella", world.player)
                 or can_use_hat(state, world, HatType.ICE) or can_use_hat(state, world, HatType.BREWING))

    elif name == "Vault Codes in the Wind":
        # Sprint is normally expected here
        if difficulty >= Difficulty.HARD:
            set_rule(main_objective, lambda state: True)

    elif name == "Speedrun Well":
        # All stamps with nothing :)
        if difficulty >= Difficulty.EXPERT:
            set_rule(main_objective, lambda state: True)

    elif name == "Mafia's Jumps":
        if difficulty >= Difficulty.HARD:
            set_rule(main_objective, lambda state: True)
            set_rule(full_clear, lambda state: True)

    elif name == "So You're Back from Outer Space":
        # Without Hookshot
        if difficulty >= Difficulty.HARD:
            set_rule(main_objective, lambda state: True)

    elif name == "Wound-Up Windmill":
        # No badge pin required. Player can switch to One Hit Hero after the checkpoint and do level without it.
        if difficulty >= Difficulty.MODERATE:
            set_rule(full_clear, lambda state: can_use_hookshot(state, world)
                     and state.has("One-Hit Hero Badge", world.player))

    if name in dw_candles:
        set_candle_dw_rules(name, world)


def set_candle_dw_rules(name: str, world: "HatInTimeWorld"):
    main_objective = world.multiworld.get_location(f"{name} - Main Objective", world.player)
    full_clear = world.multiworld.get_location(f"{name} - All Clear", world.player)

    if name == "Zero Jumps":
        add_rule(main_objective, lambda state: state.has("Zero Jumps", world.player))
        add_rule(full_clear, lambda state: state.has("Zero Jumps", world.player, 4)
                 and state.has("Train Rush (Zero Jumps)", world.player) and can_use_hat(state, world, HatType.ICE))

        # No Ice Hat/painting required in Expert for Toilet Zero Jumps
        # This painting wall can only be skipped via cherry hover.
        if get_difficulty(world) < Difficulty.EXPERT or world.options.NoPaintingSkips:
            set_rule(world.multiworld.get_location("Toilet of Doom (Zero Jumps)", world.player),
                     lambda state: can_use_hookshot(state, world) and can_hit(state, world)
                     and has_paintings(state, world, 1, False))
        else:
            set_rule(world.multiworld.get_location("Toilet of Doom (Zero Jumps)", world.player),
                     lambda state: can_use_hookshot(state, world) and can_hit(state, world))

        set_rule(world.multiworld.get_location("Contractual Obligations (Zero Jumps)", world.player),
                 lambda state: has_paintings(state, world, 1, False))

    elif name == "Snatcher's Hit List":
        add_rule(main_objective, lambda state: state.has("Mafia Goon", world.player))
        add_rule(full_clear, lambda state: state.has("Enemy", world.player, 12))

    elif name == "Camera Tourist":
        add_rule(main_objective, lambda state: state.has("Enemy", world.player, 8))
        add_rule(full_clear, lambda state: state.has("Boss", world.player, 6)
                 and state.has("Triple Enemy Photo", world.player))

    elif "Snatcher Coins" in name:
        coins: List[str] = []
        for coin in required_snatcher_coins[name]:
            coins.append(coin)
            add_rule(full_clear, lambda state, c=coin: state.has(c, world.player))

        # any coin works for the main objective
        add_rule(main_objective, lambda state: state.has(coins[0], world.player)
                 or state.has(coins[1], world.player)
                 or state.has(coins[2], world.player))


def create_enemy_events(world: "HatInTimeWorld"):
    no_tourist = "Camera Tourist" in world.excluded_dws
    for enemy, regions in hit_list.items():
        if no_tourist and enemy in bosses:
            continue

        for area in regions:
            if (area == "Bon Voyage!" or area == "Time Rift - Deep Sea") and not world.is_dlc1():
                continue

            if area == "Time Rift - Tour" and (not world.is_dlc1() or world.options.ExcludeTour):
                continue

            if area == "Bluefin Tunnel" and not world.is_dlc2():
                continue

            if world.options.DWShuffle and area in death_wishes.keys() and area not in world.dw_shuffle:
                continue

            region = world.multiworld.get_region(area, world.player)
            event = HatInTimeLocation(world.player, f"{enemy} - {area}", None, region)
            event.place_locked_item(HatInTimeItem(enemy, ItemClassification.progression, None, world.player))
            region.locations.append(event)
            event.show_in_spoiler = False

    for name in triple_enemy_locations:
        if name == "Time Rift - Tour" and (not world.is_dlc1() or world.options.ExcludeTour):
            continue

        if world.options.DWShuffle and name in death_wishes.keys() and name not in world.dw_shuffle:
            continue

        region = world.multiworld.get_region(name, world.player)
        event = HatInTimeLocation(world.player, f"Triple Enemy Photo - {name}", None, region)
        event.place_locked_item(HatInTimeItem("Triple Enemy Photo", ItemClassification.progression, None, world.player))
        region.locations.append(event)
        event.show_in_spoiler = False
        if name == "The Mustache Gauntlet":
            add_rule(event, lambda state: can_use_hookshot(state, world) and can_use_hat(state, world, HatType.DWELLER))


def set_enemy_rules(world: "HatInTimeWorld"):
    no_tourist = "Camera Tourist" in world.excluded_dws or "Camera Tourist" in world.excluded_bonuses
    difficulty = get_difficulty(world)

    for enemy, regions in hit_list.items():
        if no_tourist and enemy in bosses:
            continue

        for area in regions:
            if (area == "Bon Voyage!" or area == "Time Rift - Deep Sea") and not world.is_dlc1():
                continue

            if area == "Time Rift - Tour" and (not world.is_dlc1() or world.options.ExcludeTour):
                continue

            if area == "Bluefin Tunnel" and not world.is_dlc2():
                continue

            if world.options.DWShuffle and area in death_wishes and area not in world.dw_shuffle:
                continue

            event = world.multiworld.get_location(f"{enemy} - {area}", world.player)

            if enemy == "Toxic Flower":
                add_rule(event, lambda state: can_use_hookshot(state, world))

                if area == "The Illness has Spread":
                    add_rule(event, lambda state: not zipline_logic(world) or
                             state.has("Zipline Unlock - The Birdhouse Path", world.player)
                             or state.has("Zipline Unlock - The Lava Cake Path", world.player)
                             or state.has("Zipline Unlock - The Windmill Path", world.player))

            elif enemy == "Toilet":
                if area == "Toilet of Doom":
                    # The boss firewall is in the way and can only be skipped on Expert logic using a cherry hover.
                    add_rule(event, lambda state: has_paintings(state, world, 1, allow_skip=difficulty == Difficulty.EXPERT))
                    if difficulty < Difficulty.HARD:
                        # Hard logic and above can cross the boss arena gap with a cherry bridge.
                        add_rule(event, lambda state: can_use_hookshot(state, world))

            elif enemy == "Director":
                if area == "Dead Bird Studio Basement":
                    add_rule(event, lambda state: can_use_hookshot(state, world))

            elif enemy == "Snatcher" or enemy == "Mustache Girl":
                if area == "Boss Rush":
                    # need to be able to kill toilet and snatcher
                    add_rule(event, lambda state: can_hit(state, world) and can_use_hookshot(state, world))
                    if enemy == "Mustache Girl":
                        add_rule(event, lambda state: can_hit(state, world, True) and can_use_hookshot(state, world))

                elif area == "The Finale" and enemy == "Mustache Girl":
                    add_rule(event, lambda state: can_use_hookshot(state, world)
                             and can_use_hat(state, world, HatType.DWELLER))

            elif enemy == "Shock Squid" or enemy == "Ninja Cat":
                if area == "Time Rift - Deep Sea":
                    add_rule(event, lambda state: can_use_hookshot(state, world))


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

    "Director":        ["Dead Bird Studio Basement", "Killing Two Birds", "Boss Rush"],
    "Toilet":           ["Toilet of Doom", "Boss Rush"],

    "Snatcher":         ["Your Contract has Expired", "Breaching the Contract", "Boss Rush",
                         "Quality Time with Snatcher"],

    "Toxic Flower":     ["The Illness has Spread", "The Illness has Speedrun"],

    "Mustache Girl":    ["The Finale", "Boss Rush", "No More Bad Guys"],
}

# Camera Tourist has a bonus that requires getting three different types of enemies in one photo.
triple_enemy_locations = [
    "She Came from Outer Space",
    "She Speedran from Outer Space",
    "Mafia's Jumps",
    "The Mustache Gauntlet",
    "The Birdhouse",
    "Bird Sanctuary",
    "Time Rift - Tour",
]

bosses = [
    "Mafia Boss",
    "Director",
    "Toilet",
    "Snatcher",
    "Toxic Flower",
    "Mustache Girl",
]
