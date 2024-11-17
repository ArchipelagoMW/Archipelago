from typing import List, Callable, TYPE_CHECKING

from worlds.AutoWorld import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from BaseClasses import Entrance, Location, ItemClassification, Req
from BaseRules import AllReq, AnyReq, meets_req, req_to_rule, all_reqs_to_rule, any_req_to_rule, complex_reqs_to_rule, RULE_ALWAYS_TRUE

from .DeathWishLocations import dw_prereqs, dw_candles
from .Locations import death_wishes
from .Options import EndGoal
from .Rules import HOOKSHOT_REQ, hit_requirements, zipline_logic, get_difficulty, hat_requirements, painting_requirements
from .Types import HatType, Difficulty, HatInTimeLocation, HatInTimeItem, LocData, HitType

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
    player = world.player
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

        dw = world.multiworld.get_region(name, player)
        if not world.options.DWShuffle and name in dw_stamp_costs.keys():
            stamp_rec = Req("Stamps", dw_stamp_costs[name])
            for entrance in dw.entrances:
                add_rule(entrance, req_to_rule(player, stamp_rec))

        main_objective = world.multiworld.get_location(f"{name} - Main Objective", player)
        all_clear = world.multiworld.get_location(f"{name} - All Clear", player)
        main_stamp = world.multiworld.get_location(f"Main Stamp - {name}", player)
        bonus_stamps = world.multiworld.get_location(f"Bonus Stamps - {name}", player)
        if not world.options.DWEnableBonus:
            # place nothing, but let the locations exist still, so we can use them for bonus stamp rules
            all_clear.address = None
            all_clear.place_locked_item(HatInTimeItem("Nothing", ItemClassification.filler, None, player))
            all_clear.show_in_spoiler = False

        # No need for rules if excluded - stamps will be auto-granted
        if world.is_dw_excluded(name):
            continue

        modify_dw_rules(world, name)
        add_dw_rules(world, main_objective)
        add_dw_rules(world, all_clear)
        add_rule(main_stamp, main_objective.access_rule)
        add_rule(all_clear, main_objective.access_rule)
        # Only set bonus stamp rules if we don't auto complete bonuses
        if not world.options.DWAutoCompleteBonuses and not world.is_bonus_excluded(all_clear.name):
            add_rule(bonus_stamps, all_clear.access_rule)

    if world.options.DWShuffle:
        for i in range(len(world.dw_shuffle)-1):
            name = world.dw_shuffle[i+1]
            prev_dw = world.multiworld.get_region(world.dw_shuffle[i], player)
            entrance = world.multiworld.get_entrance(f"{prev_dw.name} -> {name}", player)
            prev_dw_req = Req(f"1 Stamp - {prev_dw.name}", 1)
            add_rule(entrance, req_to_rule(player, prev_dw_req))
    else:
        for key, reqs in dw_prereqs.items():
            if key == "Snatcher Coins in Nyakuza Metro" and not world.is_dlc2():
                continue

            access_rules: List[Callable[[CollectionState], bool]] = []
            entrances: List[Entrance] = []

            for parent in reqs:
                entrance = world.multiworld.get_entrance(f"{parent} -> {key}", player)
                entrances.append(entrance)

                if not world.is_dw_excluded(parent):
                    parent_req = Req(f"1 Stamp - {parent}", 1)
                    access_rules.append(req_to_rule(player, parent_req))

            for entrance in entrances:
                for rule in access_rules:
                    add_rule(entrance, rule)

    if world.options.EndGoal == EndGoal.option_seal_the_deal:
        seal_req = Req("1 Stamp - Seal the Deal", 1)
        world.multiworld.completion_condition[player] = req_to_rule(player, seal_req)


def add_dw_rules(world: "HatInTimeWorld", loc: Location):
    bonus: bool = "All Clear" in loc.name
    if not bonus:
        data = dw_requirements.get(loc.parent_region.name)
    else:
        data = dw_bonus_requirements.get(loc.parent_region.name)

    if data is None:
        return

    player = world.player
    if data.hookshot:
        add_rule(loc, req_to_rule(player, HOOKSHOT_REQ))

    for hat in data.required_hats:
        add_rule(loc, req_to_rule(player, hat_requirements(world, hat)))

    for misc in data.misc_required:
        add_rule(loc, req_to_rule(player, Req(misc, 1)))

    if data.paintings > 0 and world.options.ShuffleSubconPaintings:
        add_rule(loc, req_to_rule(player, painting_requirements(world, 1)))

    if data.hit_type is not HitType.none and world.options.UmbrellaLogic:
        brewing_hat_req = hat_requirements(world, HatType.BREWING)
        umbrella_req = Req("Umbrella", 1)
        if data.hit_type == HitType.umbrella:
            add_rule(loc, req_to_rule(player, umbrella_req))

        elif data.hit_type == HitType.umbrella_or_brewing:
            add_rule(loc, any_req_to_rule(player, umbrella_req, brewing_hat_req))

        elif data.hit_type == HitType.dweller_bell:
            dweller_hat_req = hat_requirements(world, HatType.DWELLER)
            add_rule(loc, any_req_to_rule(player, umbrella_req, brewing_hat_req, dweller_hat_req))


def modify_dw_rules(world: "HatInTimeWorld", name: str):
    player = world.player
    difficulty: Difficulty = get_difficulty(world)
    main_objective = world.multiworld.get_location(f"{name} - Main Objective", player)
    full_clear = world.multiworld.get_location(f"{name} - All Clear", player)
    umbrella_req = Req("Umbrella", 1)

    if name == "The Illness has Speedrun":
        # All stamps with hookshot only in Expert
        if difficulty >= Difficulty.EXPERT:
            set_rule(full_clear, RULE_ALWAYS_TRUE)
        else:
            add_rule(main_objective, req_to_rule(player, umbrella_req))

    elif name == "The Mustache Gauntlet":
        brewing_hat_req = hat_requirements(world, HatType.BREWING)
        ice_hat_req = hat_requirements(world, HatType.ICE)
        add_rule(main_objective, any_req_to_rule(player, umbrella_req, ice_hat_req, brewing_hat_req))

    elif name == "Vault Codes in the Wind":
        # Sprint is normally expected here
        if difficulty >= Difficulty.HARD:
            set_rule(main_objective, RULE_ALWAYS_TRUE)

    elif name == "Speedrun Well":
        # All stamps with nothing :)
        if difficulty >= Difficulty.EXPERT:
            set_rule(main_objective, RULE_ALWAYS_TRUE)

    elif name == "Mafia's Jumps":
        if difficulty >= Difficulty.HARD:
            set_rule(main_objective, RULE_ALWAYS_TRUE)
            set_rule(full_clear, RULE_ALWAYS_TRUE)

    elif name == "So You're Back from Outer Space":
        # Without Hookshot
        if difficulty >= Difficulty.HARD:
            set_rule(main_objective, RULE_ALWAYS_TRUE)

    elif name == "Wound-Up Windmill":
        # No badge pin required. Player can switch to One Hit Hero after the checkpoint and do level without it.
        if difficulty >= Difficulty.MODERATE:
            set_rule(full_clear, all_reqs_to_rule(player, HOOKSHOT_REQ, Req("One-Hit Hero Badge", 1)))

    if name in dw_candles:
        set_candle_dw_rules(name, world)


def set_candle_dw_rules(name: str, world: "HatInTimeWorld"):
    player = world.player
    main_objective = world.multiworld.get_location(f"{name} - Main Objective", player)
    full_clear = world.multiworld.get_location(f"{name} - All Clear", player)
    paintings_noskip = painting_requirements(world, 1, False)

    if name == "Zero Jumps":
        ice_hat_req = hat_requirements(world, HatType.ICE)
        add_rule(main_objective, req_to_rule(player, Req("Zero Jumps", 1)))
        add_rule(full_clear, all_reqs_to_rule(player,
                                              Req("Zero Jumps", 4),
                                              Req("Train Rush (Zero Jumps)", 1),
                                              ice_hat_req))

        # No Ice Hat/painting required in Expert for Toilet Zero Jumps
        # This painting wall can only be skipped via cherry hover.
        if get_difficulty(world) < Difficulty.EXPERT or world.options.NoPaintingSkips:
            set_rule(world.multiworld.get_location("Toilet of Doom (Zero Jumps)", player),
                     complex_reqs_to_rule(player, AllReq([
                         HOOKSHOT_REQ,
                         hit_requirements(world),
                         paintings_noskip,
                     ])))
        else:
            set_rule(world.multiworld.get_location("Toilet of Doom (Zero Jumps)", player),
                     complex_reqs_to_rule(player, AllReq([
                         HOOKSHOT_REQ,
                         hit_requirements(world),
                     ])))

        set_rule(world.multiworld.get_location("Contractual Obligations (Zero Jumps)", player),
                 req_to_rule(player, paintings_noskip))

    elif name == "Snatcher's Hit List":
        add_rule(main_objective, req_to_rule(player, Req("Mafia Goon", 1)))
        add_rule(full_clear, req_to_rule(player, Req("Enemy", 12)))

    elif name == "Camera Tourist":
        add_rule(main_objective, req_to_rule(player, Req("Enemy", 8)))
        add_rule(full_clear, all_reqs_to_rule(player, Req("Boss", 6), Req("Triple Enemy Photo", 1)))

    elif "Snatcher Coins" in name:
        coins: List[str] = []
        for coin in required_snatcher_coins[name]:
            coins.append(Req(coin, 1))
            add_rule(full_clear, req_to_rule(player, Req(coin, 1)))

        # any coin works for the main objective
        add_rule(main_objective, any_req_to_rule(player, *coins))


def create_enemy_events(world: "HatInTimeWorld"):
    no_tourist = "Camera Tourist" in world.excluded_dws
    player = world.player
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

            region = world.multiworld.get_region(area, player)
            event = HatInTimeLocation(player, f"{enemy} - {area}", None, region)
            event.place_locked_item(HatInTimeItem(enemy, ItemClassification.progression, None, player))
            region.locations.append(event)
            event.show_in_spoiler = False

    dweller_hat_req = hat_requirements(world, HatType.DWELLER)
    for name in triple_enemy_locations:
        if name == "Time Rift - Tour" and (not world.is_dlc1() or world.options.ExcludeTour):
            continue

        if world.options.DWShuffle and name in death_wishes.keys() and name not in world.dw_shuffle:
            continue

        region = world.multiworld.get_region(name, player)
        event = HatInTimeLocation(player, f"Triple Enemy Photo - {name}", None, region)
        event.place_locked_item(HatInTimeItem("Triple Enemy Photo", ItemClassification.progression, None, player))
        region.locations.append(event)
        event.show_in_spoiler = False
        if name == "The Mustache Gauntlet":
            add_rule(event, all_reqs_to_rule(player, HOOKSHOT_REQ, dweller_hat_req))


def set_enemy_rules(world: "HatInTimeWorld"):
    no_tourist = "Camera Tourist" in world.excluded_dws or "Camera Tourist" in world.excluded_bonuses
    player = world.player
    dweller_hat_req = hat_requirements(world, HatType.DWELLER)

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

            event = world.multiworld.get_location(f"{enemy} - {area}", player)

            if enemy == "Toxic Flower":
                add_rule(event, req_to_rule(player, HOOKSHOT_REQ))

                if area == "The Illness has Spread" and zipline_logic(world):
                    add_rule(event, any_req_to_rule(player, Req("Zipline Unlock - The Birdhouse Path"),
                                                    Req("Zipline Unlock - The Lava Cake Path"),
                                                    Req("Zipline Unlock - The Windmill Path")))

            elif enemy == "Director":
                if area == "Dead Bird Studio Basement":
                    add_rule(event, req_to_rule(player, HOOKSHOT_REQ))

            elif enemy == "Snatcher" or enemy == "Mustache Girl":
                if area == "Boss Rush":
                    # need to be able to kill toilet and snatcher
                    add_rule(event,
                             complex_reqs_to_rule(player, AllReq([
                                 HOOKSHOT_REQ,
                                 hit_requirements(world),
                             ])))
                    if enemy == "Mustache Girl":
                        add_rule(event, complex_reqs_to_rule(player, AllReq([
                            HOOKSHOT_REQ,
                            hit_requirements(world, True),
                        ])))

                elif area == "The Finale" and enemy == "Mustache Girl":
                    add_rule(event, all_reqs_to_rule(player, HOOKSHOT_REQ, dweller_hat_req))

            elif enemy == "Shock Squid" or enemy == "Ninja Cat":
                if area == "Time Rift - Deep Sea":
                    add_rule(event, req_to_rule(player, HOOKSHOT_REQ))


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
    "Conductor",
    "Toilet",
    "Snatcher",
    "Toxic Flower",
    "Mustache Girl",
]
