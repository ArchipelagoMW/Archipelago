from .Types import HatInTimeLocation, HatInTimeItem
from .Regions import create_region
from BaseClasses import Region, LocationProgressType, ItemClassification
from worlds.generic.Rules import add_rule
from typing import List, TYPE_CHECKING
from .Locations import death_wishes
from .Options import EndGoal

if TYPE_CHECKING:
    from . import HatInTimeWorld


dw_prereqs = {
    "So You're Back From Outer Space":  ["Beat the Heat"],
    "Snatcher's Hit List":              ["Beat the Heat"],
    "Snatcher Coins in Mafia Town":     ["So You're Back From Outer Space"],
    "Rift Collapse: Mafia of Cooks":    ["So You're Back From Outer Space"],
    "Collect-a-thon":                   ["So You're Back From Outer Space"],
    "She Speedran from Outer Space":    ["Rift Collapse: Mafia of Cooks"],
    "Mafia's Jumps":                    ["She Speedran from Outer Space"],
    "Vault Codes in the Wind":          ["Collect-a-thon", "She Speedran from Outer Space"],
    "Encore! Encore!":                  ["Collect-a-thon"],

    "Security Breach":                          ["Beat the Heat"],
    "Rift Collapse: Dead Bird Studio":          ["Security Breach"],
    "The Great Big Hootenanny":                 ["Security Breach"],
    "10 Seconds until Self-Destruct":           ["The Great Big Hootenanny"],
    "Killing Two Birds":                        ["Rift Collapse: Dead Bird Studio", "10 Seconds until Self-Destruct"],
    "Community Rift: Rhythm Jump Studio":       ["10 Seconds until Self-Destruct"],
    "Snatcher Coins in Battle of the Birds":    ["The Great Big Hootenanny"],
    "Zero Jumps":                               ["Rift Collapse: Dead Bird Studio"],
    "Snatcher Coins in Nyakuza Metro":          ["Killing Two Birds"],

    "Speedrun Well":                    ["Beat the Heat"],
    "Rift Collapse: Sleepy Subcon":     ["Speedrun Well"],
    "Boss Rush":                        ["Speedrun Well"],
    "Quality Time with Snatcher":       ["Rift Collapse: Sleepy Subcon"],
    "Breaching the Contract":           ["Boss Rush", "Quality Time with Snatcher"],
    "Community Rift: Twilight Travels": ["Quality Time with Snatcher"],
    "Snatcher Coins in Subcon Forest":  ["Rift Collapse: Sleepy Subcon"],

    "Bird Sanctuary":                       ["Beat the Heat"],
    "Snatcher Coins in Alpine Skyline":     ["Bird Sanctuary"],
    "Wound-Up Windmill":                    ["Bird Sanctuary"],
    "Rift Collapse: Alpine Skyline":        ["Bird Sanctuary"],
    "Camera Tourist":                       ["Rift Collapse: Alpine Skyline"],
    "Community Rift: The Mountain Rift":    ["Rift Collapse: Alpine Skyline"],
    "The Illness has Speedrun":             ["Rift Collapse: Alpine Skyline", "Wound-Up Windmill"],

    "The Mustache Gauntlet":            ["Wound-Up Windmill"],
    "No More Bad Guys":                 ["The Mustache Gauntlet"],
    "Seal the Deal":                    ["Encore! Encore!", "Killing Two Birds",
                                         "Breaching the Contract", "No More Bad Guys"],

    "Rift Collapse: Deep Sea":          ["Rift Collapse: Mafia of Cooks", "Rift Collapse: Dead Bird Studio",
                                         "Rift Collapse: Sleepy Subcon", "Rift Collapse: Alpine Skyline"],

    "Cruisin' for a Bruisin'":          ["Rift Collapse: Deep Sea"],
}

dw_candles = [
    "Snatcher's Hit List",
    "Zero Jumps",
    "Camera Tourist",
    "Snatcher Coins in Mafia Town",
    "Snatcher Coins in Battle of the Birds",
    "Snatcher Coins in Subcon Forest",
    "Snatcher Coins in Alpine Skyline",
    "Snatcher Coins in Nyakuza Metro",
]

annoying_dws = [
    "Vault Codes in the Wind",
    "Boss Rush",
    "Camera Tourist",
    "The Mustache Gauntlet",
    "Rift Collapse: Deep Sea",
    "Cruisin' for a Bruisin'",
    "Seal the Deal",  # Non-excluded if goal
]

# includes the above as well
annoying_bonuses = [
    "So You're Back From Outer Space",
    "Encore! Encore!",
    "Snatcher's Hit List",
    "Vault Codes in the Wind",
    "10 Seconds until Self-Destruct",
    "Killing Two Birds",
    "Zero Jumps",
    "Boss Rush",
    "Bird Sanctuary",
    "The Mustache Gauntlet",
    "Wound-Up Windmill",
    "Camera Tourist",
    "Rift Collapse: Deep Sea",
    "Cruisin' for a Bruisin'",
    "Seal the Deal",
]

dw_classes = {
    "Beat the Heat":                    "Hat_SnatcherContract_DeathWish_HeatingUpHarder",
    "So You're Back From Outer Space":  "Hat_SnatcherContract_DeathWish_BackFromSpace",
    "Snatcher's Hit List":              "Hat_SnatcherContract_DeathWish_KillEverybody",
    "Collect-a-thon":                   "Hat_SnatcherContract_DeathWish_PonFrenzy",
    "Rift Collapse: Mafia of Cooks":    "Hat_SnatcherContract_DeathWish_RiftCollapse_MafiaTown",
    "Encore! Encore!":                  "Hat_SnatcherContract_DeathWish_MafiaBossEX",
    "She Speedran from Outer Space":    "Hat_SnatcherContract_DeathWish_Speedrun_MafiaAlien",
    "Mafia's Jumps":                    "Hat_SnatcherContract_DeathWish_NoAPresses_MafiaAlien",
    "Vault Codes in the Wind":          "Hat_SnatcherContract_DeathWish_MovingVault",
    "Snatcher Coins in Mafia Town":     "Hat_SnatcherContract_DeathWish_Tokens_MafiaTown",

    "Security Breach":                          "Hat_SnatcherContract_DeathWish_DeadBirdStudioMoreGuards",
    "The Great Big Hootenanny":                 "Hat_SnatcherContract_DeathWish_DifficultParade",
    "Rift Collapse: Dead Bird Studio":          "Hat_SnatcherContract_DeathWish_RiftCollapse_Birds",
    "10 Seconds until Self-Destruct":           "Hat_SnatcherContract_DeathWish_TrainRushShortTime",
    "Killing Two Birds":                        "Hat_SnatcherContract_DeathWish_BirdBossEX",
    "Snatcher Coins in Battle of the Birds":    "Hat_SnatcherContract_DeathWish_Tokens_Birds",
    "Zero Jumps":                               "Hat_SnatcherContract_DeathWish_NoAPresses",

    "Speedrun Well":                    "Hat_SnatcherContract_DeathWish_Speedrun_SubWell",
    "Rift Collapse: Sleepy Subcon":     "Hat_SnatcherContract_DeathWish_RiftCollapse_Subcon",
    "Boss Rush":                        "Hat_SnatcherContract_DeathWish_BossRush",
    "Quality Time with Snatcher":       "Hat_SnatcherContract_DeathWish_SurvivalOfTheFittest",
    "Breaching the Contract":           "Hat_SnatcherContract_DeathWish_SnatcherEX",
    "Snatcher Coins in Subcon Forest":  "Hat_SnatcherContract_DeathWish_Tokens_Subcon",

    "Bird Sanctuary":                   "Hat_SnatcherContract_DeathWish_NiceBirdhouse",
    "Rift Collapse: Alpine Skyline":    "Hat_SnatcherContract_DeathWish_RiftCollapse_Alps",
    "Wound-Up Windmill":                "Hat_SnatcherContract_DeathWish_FastWindmill",
    "The Illness has Speedrun":         "Hat_SnatcherContract_DeathWish_Speedrun_Illness",
    "Snatcher Coins in Alpine Skyline": "Hat_SnatcherContract_DeathWish_Tokens_Alps",
    "Camera Tourist":                   "Hat_SnatcherContract_DeathWish_CameraTourist_1",

    "The Mustache Gauntlet":            "Hat_SnatcherContract_DeathWish_HardCastle",
    "No More Bad Guys":                 "Hat_SnatcherContract_DeathWish_MuGirlEX",

    "Seal the Deal":                    "Hat_SnatcherContract_DeathWish_BossRushEX",
    "Rift Collapse: Deep Sea":          "Hat_SnatcherContract_DeathWish_RiftCollapse_Cruise",
    "Cruisin' for a Bruisin'":          "Hat_SnatcherContract_DeathWish_EndlessTasks",

    "Community Rift: Rhythm Jump Studio":   "Hat_SnatcherContract_DeathWish_CommunityRift_RhythmJump",
    "Community Rift: Twilight Travels":     "Hat_SnatcherContract_DeathWish_CommunityRift_TwilightTravels",
    "Community Rift: The Mountain Rift":    "Hat_SnatcherContract_DeathWish_CommunityRift_MountainRift",

    "Snatcher Coins in Nyakuza Metro":      "Hat_SnatcherContract_DeathWish_Tokens_Metro",
}


def create_dw_regions(world: "HatInTimeWorld"):
    if world.options.DWExcludeAnnoyingContracts:
        for name in annoying_dws:
            world.excluded_dws.append(name)

    if not world.options.DWEnableBonus and world.options.DWAutoCompleteBonuses:
        for name in death_wishes:
            world.excluded_bonuses.append(name)
    if world.options.DWExcludeAnnoyingBonuses and not world.options.DWAutoCompleteBonuses:
        for name in annoying_bonuses:
            world.excluded_bonuses.append(name)

    if world.options.DWExcludeCandles:
        for name in dw_candles:
            if name not in world.excluded_dws:
                world.excluded_dws.append(name)

    spaceship = world.multiworld.get_region("Spaceship", world.player)
    dw_map: Region = create_region(world, "Death Wish Map")
    entrance = spaceship.connect(dw_map, "-> Death Wish Map")
    add_rule(entrance, lambda state: state.has("Time Piece", world.player, world.options.DWTimePieceRequirement))

    if world.options.DWShuffle:
        # Connect Death Wishes randomly to one another in a linear sequence
        dw_list: List[str] = []
        for name in death_wishes.keys():
            # Don't shuffle excluded or invalid Death Wishes
            if not world.is_dlc2() and name == "Snatcher Coins in Nyakuza Metro" or world.is_dw_excluded(name):
                continue

            dw_list.append(name)

        world.random.shuffle(dw_list)
        count = world.random.randint(world.options.DWShuffleCountMin.value, world.options.DWShuffleCountMax.value)
        dw_shuffle: List[str] = []
        total = min(len(dw_list), count)
        for i in range(total):
            dw_shuffle.append(dw_list[i])

        # Seal the Deal is always last if it's the goal
        if world.options.EndGoal == EndGoal.option_seal_the_deal:
            if "Seal the Deal" in dw_shuffle:
                dw_shuffle.remove("Seal the Deal")

            dw_shuffle.append("Seal the Deal")

        world.dw_shuffle = dw_shuffle
        prev_dw = dw_map
        for death_wish_name in dw_shuffle:
            dw = create_region(world, death_wish_name)
            prev_dw.connect(dw)
            create_dw_locations(world, dw)
            prev_dw = dw
    else:
        # DWShuffle is disabled, use vanilla connections
        for key in death_wishes.keys():
            if key == "Snatcher Coins in Nyakuza Metro" and not world.is_dlc2():
                world.excluded_dws.append(key)
                continue

            dw = create_region(world, key)
            if key == "Beat the Heat":
                dw_map.connect(dw, f"{dw_map.name} -> Beat the Heat")
            elif key in dw_prereqs.keys():
                for name in dw_prereqs[key]:
                    parent = world.multiworld.get_region(name, world.player)
                    parent.connect(dw, f"{parent.name} -> {key}")

            create_dw_locations(world, dw)


def create_dw_locations(world: "HatInTimeWorld", dw: Region):
    loc_id = death_wishes[dw.name]
    main_objective = HatInTimeLocation(world.player, f"{dw.name} - Main Objective", loc_id, dw)
    full_clear = HatInTimeLocation(world.player, f"{dw.name} - All Clear", loc_id + 1, dw)
    main_stamp = HatInTimeLocation(world.player, f"Main Stamp - {dw.name}", None, dw)
    bonus_stamps = HatInTimeLocation(world.player, f"Bonus Stamps - {dw.name}", None, dw)
    main_stamp.show_in_spoiler = False
    bonus_stamps.show_in_spoiler = False
    dw.locations.append(main_stamp)
    dw.locations.append(bonus_stamps)
    main_stamp.place_locked_item(HatInTimeItem(f"1 Stamp - {dw.name}",
                                               ItemClassification.progression, None, world.player))
    bonus_stamps.place_locked_item(HatInTimeItem(f"2 Stamp - {dw.name}",
                                                 ItemClassification.progression, None, world.player))

    if dw.name in world.excluded_dws:
        main_objective.progress_type = LocationProgressType.EXCLUDED
        full_clear.progress_type = LocationProgressType.EXCLUDED
    elif world.is_bonus_excluded(dw.name):
        full_clear.progress_type = LocationProgressType.EXCLUDED

    dw.locations.append(main_objective)
    dw.locations.append(full_clear)
