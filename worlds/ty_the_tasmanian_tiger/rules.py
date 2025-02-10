import enum
from typing import Callable

from worlds.ty_the_tasmanian_tiger.regions import Ty1LevelCode, ty1_levels
import re

from BaseClasses import MultiWorld, CollectionState
from worlds.ty_the_tasmanian_tiger.options import Ty1Options

def has_progressive_rang(player: int, options: Ty1Options, state: CollectionState, level: int):
    return state.has("Progressive Rang", player, level + 1
                        if options.progressive_elementals and not options.start_with_boom else level)

def has_stopwatch(player: int, state: CollectionState, level: Ty1LevelCode):
    return state.has("Stopwatch - " + ty1_levels[level], player)

def can_go_water(player: int, options: Ty1Options, state: CollectionState):
    return state.has("Swim", player) or state.has("Dive", player) or has_progressive_rang(player, options, state, 2)

def has_all_bilbies(player: int, state: CollectionState, level: Ty1LevelCode):
    return state.has("Bilby - " + ty1_levels[level], player, 5)

class TheggType(enum.Enum):
    FIRE_THEGG = 0,
    ICE_THEGG = 1,
    AIR_THEGG = 2

def has_theggs(player: int, state: CollectionState, thegg_type: TheggType, amount: int):
    if thegg_type == TheggType.FIRE_THEGG:
        return state.has("Fire Thunder Egg", player, amount)
    if thegg_type == TheggType.ICE_THEGG:
        return state.has("Ice Thunder Egg", player, amount)
    if thegg_type == TheggType.AIR_THEGG:
        return state.has("Air Thunder Egg", player, amount)

def get_location_rules(world: MultiWorld, options: Ty1Options, player: int):
    location_rules = {
        "rules": {
            "Two Up - Collect 300 Opals":
                lambda state:
                    (options.logic_difficulty == 0 and
                        ((state.has("Second Rang", player) and can_go_water(player, options, state)) or has_progressive_rang(player, options, state, 1)))
                    or options.logic_difficulty == 1,
            "Two Up - Time Attack":
                lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.A1),
            "WitP - Wombat Race":
                lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.A2),
            "WitP - Truck Trouble":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "WitP - Drive Me Batty":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "Ship Rex - Race Rex":
                lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.A3),
            "Ship Rex - Quicksand Coconuts":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "BotRT - Collect 300 Opals":
                lambda state:
                    can_go_water(player, options, state),
            "BotRT - Find 5 Bilbies":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5))
                     or (options.logic_difficulty == 1 and
                         (state.has("Second Rang", player) and can_go_water(player, options, state)) or state.has("Flamerang", player) or has_progressive_rang(player, options, state, 2))),
            "BotRT - Time Attack":
                 lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.B1),
            "BotRT - Home, Sweet, Home":
                lambda state:
                    state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5),
            "BotRT - Heat Dennis' House":
                lambda state:
                    state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5),
            "BotRT - Ty Diving":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Dive", player) or has_progressive_rang(player, options, state, 4)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Dive", player) or state.has("Zappyrang", player) or has_progressive_rang(player, options, state, 4))),
            "BotRT - Neddy The Bully":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "Snow Worries - Collect 300 Opals":
                lambda state:
                    state.has("Aquarang", player) or has_progressive_rang(player, options, state, 3),
            "Snow Worries - Find 5 Bilbies":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Flamerang", player) or state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1))),
            "Snow Worries - Time Attack":
                lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.B2),
            "Snow Worries - Koala Chaos":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "Snow Worries - The Old Mill":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "Snow Worries - Trap The Yabby":
                lambda state:
                    state.has("Aquarang", player) or has_progressive_rang(player, options, state, 3),
            "Snow Worries - Musical Icicle":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "Outback Safari - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(player, state, Ty1LevelCode.B3),
            "Outback Safari - Time Attack":
                lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.B3),
            "Outback Safari - Toxic Trouble":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "LLPoF - Find 5 Bilbies":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.C1),
            "LLPoF - Time Attack":
                lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.C1),
            "LLPoF - Fiery Furnace":
                lambda state:
                    state.has("Frostyrang", player) or has_progressive_rang(player, options, state, 6),
            "LLPoF - Muddy Towers":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Dive", player) or state.has("Flamerang", player) or has_progressive_rang(player, options, state, 4))),
            "BtBS - Collect 300 Opals":
                lambda state:
                    options.logic_difficulty == 0 or
                    (options.logic_difficulty == 1 and
                     (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1))),
            "BtBS - Find 5 Bilbies":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                    or options.logic_difficulty == 1,
            "BtBS - Wombat Rematch":
                lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.C2),
            "BtBS - Cable Car Capers":
                lambda state:
                    options.logic_difficulty == 0 or
                    (options.logic_difficulty == 1 and has_progressive_rang(player, options, state, 0)),
            "RMtS - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(player, state, Ty1LevelCode.C3),
            "RMtS - Race Rex":
                lambda state:
                    has_stopwatch(player, state, Ty1LevelCode.C3),
            "RMtS - Parrot Beard's Booty":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "RMtS - Frill Boat Battle":
                lambda state:
                    has_progressive_rang(player, options, state, 0),
            "RMtS - Geyser Hop":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Second Rang", player) or state.has("Doomerang", player) or (state.has("Swim", player) and state.has("Frostyrang", player))
                            or has_progressive_rang(player, options, state, 1))),
            "RMtS - Volcanic Panic":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Second Rang", player) or (state.has("Swim", player) and state.has("Frostyrang", player))
                            or has_progressive_rang(player, options, state,1))),
            "BotRT - Golden Cog 1":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or options.logic_difficulty == 1,
            "BotRT - Golden Cog 2":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                    or options.logic_difficulty == 1,
            "BotRT - Golden Cog 8":
                lambda state:
                    (options.logic_difficulty == 0 and
                        ((can_go_water(player, options, state) and (state.has("Aquarang", player)) or
                            state.has("Frostyrang", player) or has_progressive_rang(player, options, state, 3))))
                    or (options.logic_difficulty == 1 and
                        ((can_go_water(player, options, state) and (state.has("Aquarang", player)) or
                          state.has("Frostyrang", player) or state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))),
            "BotRT - Golden Cog 10":
                lambda state:
                    can_go_water(player, options, state) or has_progressive_rang(player, options, state, 2),
            "Snow Worries - Golden Cog 3":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or (options.logic_difficulty == 1 and
                        (can_go_water(player, options, state) or state.has("Second Rang", player)
                        or has_progressive_rang(player, options, state, 1))),
            "Snow Worries - Golden Cog 7":
                lambda state:
                    state.has("Aquarang", player) or has_progressive_rang(player, options, state, 3),
            "LLPoF - Golden Cog 4":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Flamerang", player) or state.has("Kaboomerang", player) or has_progressive_rang(player, options, state, 5)))
                    or options.logic_difficulty == 1,
            "LLPoF - Golden Cog 5":
                lambda state:
                    (options.logic_difficulty == 0 and
                         (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or options.logic_difficulty == 1,
            "BtBS - Golden Cog 7":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Flamerang", player) or state.has("Kaboomerang", player) or has_progressive_rang(player, options, state, 5)))
                    or options.logic_difficulty == 1,
            "RMtS - Golden Cog 2":
                lambda state:
                    state.has("Second Rang", player) or state.has("Frostyrang", player) or has_progressive_rang(player, options, state, 1),
            "RMtS - Golden Cog 6":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or options.logic_difficulty == 1,
            "RMtS - Golden Cog 8":
                lambda state:
                    (state.has("Aquarang", player) and can_go_water(player, options, state))
                        or state.has("Frostyrang", player) or has_progressive_rang(player, options, state, 3),
            "Two Up - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.A1),
            "WitP - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.A2),
            "Ship Rex - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.A3),
            "BotRT - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.B1),
            "Snow Worries - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.B2),
            "Outback Safari - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.B3),
            "LLPoF - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.C1),
            "BtBS - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.C2),
            "RMtS - Bilby Completion":
                lambda state:
                has_all_bilbies(player, state, Ty1LevelCode.C3),
            "BotRT - Bilby Mum":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5))
                    or (options.logic_difficulty == 1 and
                        (state.has("Second Rang", player) and can_go_water(player, options, state)) or state.has("Flamerang", player) or has_progressive_rang(player, options, state, 2))),
            "Snow Worries - Bilby Mum":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Flamerang", player) or state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1))),
            "BtBS - Bilby Dad":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                    or options.logic_difficulty == 1,
            "BtBS - Bilby Mum":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                    or options.logic_difficulty == 1,
            "Snow Worries - PF 13":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Flamerang", player) or state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1))),
            "Attribute - Doomerang":
                lambda state:
                    (state.has("Frostyrang", player) and state.has("Flamerang", player)) or has_progressive_rang(player, options, state, 6),
            "Attribute - Extra Health":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (
                            can_go_water(player, options, state) and
                            (
                                state.has("Second Rang", player)
                                and state.has("Flamerang", player)
                                and state.has("Frostyrang", player)
                                and state.has("Zappyrang", player)
                            )
                        ) or has_progressive_rang(player, options, state, 7)
                    ) or (options.logic_difficulty == 1 and
                        (
                            can_go_water(player, options, state) and
                            (
                                state.has("Second Rang", player)
                                and state.has("Flamerang", player)
                                and state.has("Frostyrang", player)
                                and state.has("Zappyrang", player)
                            )
                        ) or has_progressive_rang(player, options, state, 4)
                    ),
            "Attribute - Zoomerang":
                lambda state:
                    state.has("Golden Cog", player, 15),
            "Attribute - Multirang":
                lambda state:
                    state.has("Golden Cog", player, 30),
            "Attribute - Infrarang":
                lambda state:
                    state.has("Golden Cog", player, 45),
            "Attribute - Megarang":
                lambda state:
                    state.has("Golden Cog", player, 60),
            "Attribute - Kaboomarang":
                lambda state:
                    state.has("Golden Cog", player, 75),
            "Attribute - Chronorang":
                lambda state:
                    state.has("Golden Cog", player, 90),
            "BotRT - All Golden Cogs":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (has_progressive_rang(player, options, state, 5) or
                            (state.has("Flamerang", player) and
                            can_go_water(player, options, state) and
                            (state.has("Aquarang", player) or state.has("Frostyrang", player))))
                    )
                    or (options.logic_difficulty == 1 and
                        (has_progressive_rang(player, options, state, 2) or
                            (can_go_water(player, options, state) and
                            (state.has("Aquarang", player) or state.has("Frostyrang", player) or state.has("Second Rang", player))))
                    ),
            "Snow Worries - All Golden Cogs":
                lambda state:
                    (options.logic_difficulty == 0 and (has_progressive_rang(player, options, state, 3)
                        or (state.has("Aquarang", player) and state.has("Second Rang",player))))
                    or (options.logic_difficulty == 1 and
                        (has_progressive_rang(player, options, state, 3) or state.has("Aquarang", player))),
            "LLPoF - All Golden Cogs":
                lambda state:
                    (options.logic_difficulty == 0 and
                        ((state.has("Second Rang", player) and state.has("Flamerang", player)) or state.has("Kaboomerang", player)
                        or has_progressive_rang(player, options, state, 5)))
                    or options.logic_difficulty == 1,
            "BtBS - All Golden Cogs":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Flamerang", player) or state.has("Kaboomerang", player)
                        or has_progressive_rang(player, options, state, 5)))
                    or options.logic_difficulty == 1,
            "RMtS - All Golden Cogs":
                lambda state:
                    (state.has("Second Rang", player) and (state.has("Aquarang", player) or state.has("Frostyrang", player))) or has_progressive_rang(player, options, state, 3),
            "Snow Worries - All Picture Frames":
                lambda state:
                    (options.logic_difficulty == 0 and
                     (state.has("Flamerang", player) or has_progressive_rang(player, options, state, 5)))
                or (options.logic_difficulty == 1 and
                    (state.has("Flamerang", player) or state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1))),
            "Rainbow Cliffs - All Picture Frames":
                lambda state:
                    (options.logic_difficulty == 0 and ((state.has("Second Rang", player) and state.has("Flamerang", player)) or has_progressive_rang(player, options, state, 5)))
                    or (options.logic_difficulty == 1 and (state.has("Dive", player) or state.has("Flamerang", player) or has_progressive_rang(player, options, state, 4))),
            "Platypus Talisman":
                lambda state:
                    (state.has("Aquarang", player) and state.has("Flamerang", player) and can_go_water(player, options, state)) or has_progressive_rang(player, options, state, 5),
            "Cockatoo Talisman":
                lambda state:
                    (options.logic_difficulty == 0 and
                     ((state.has("Frostyrang", player) and state.has("Flamerang", player)) or has_progressive_rang(player, options, state, 6)))
                     or (options.logic_difficulty == 1 and
                      ((state.has("Frostyrang", player) and state.has("Flamerang", player)) or has_progressive_rang(player, options, state, 6) or state.has("Doomerang", player))),
            "Dingo Talisman":
                lambda state:
                    state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1),
            "Tiger Talisman":
                lambda state:
                    (options.logic_difficulty == 0 and
                        ((state.has("Flamerang", player) and state.has("Frostyrang", player) and state.has("Doomerang", player)) or has_progressive_rang(player, options, state, 8)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Doomerang", player) or has_progressive_rang(player, options, state, 8))),
            "Attribute - Flamerang":
                lambda state:
                    has_theggs(player, state, TheggType.FIRE_THEGG, options.hub_te_counts.value) and state.has("Frog Talisman", player),
            "Attribute - Frostyrang":
                lambda state:
                    has_theggs(player, state, TheggType.ICE_THEGG, options.hub_te_counts.value) and state.has("Platypus Talisman", player),
            "Attribute - Zappyrang":
                lambda state:
                    has_theggs(player, state, TheggType.AIR_THEGG, options.hub_te_counts.value) and state.has("Cockatoo Talisman", player),
            # Above water next to Julius' lab (pontoon scale)
            "Rainbow Scale 11":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or (options.logic_difficulty == 1 and
                        (state.has("Swim", player) or state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1))),
            # Inside starting pillar
            "Rainbow Scale 15":
                lambda state:
                    (options.logic_difficulty == 0 and
                        (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or (options.logic_difficulty == 1),
            # Underwater near Julius' lab
            "Rainbow Scale 16":
                lambda state:
                    state.has("Swim", player) or state.has("Dive", player) or has_progressive_rang(player, options, state, 2),
            # Underwater near waterfall cave
            "Rainbow Scale 21":
                lambda state:
                    state.has("Swim", player) or state.has("Dive", player) or has_progressive_rang(player, options, state, 2),
            # Floating in the air next to starting pillar
            "Rainbow Scale 24":
                lambda state:
                    (options.logic_difficulty == 0 and
                         (state.has("Second Rang", player) or has_progressive_rang(player, options, state, 1)))
                    or (options.logic_difficulty == 1),
        }
    }
    return location_rules

def set_rules(world: MultiWorld, options: Ty1Options, player: int):
    rules_lookup = get_location_rules(world, options, player)
    for location_name, rule in rules_lookup["rules"].items():
        try:
            world.get_location(location_name, player).access_rule = rule
        except KeyError:
            pass

    if options.goal == 0:
        world.completion_condition[player] = lambda state: (state.has("Beat Cass", player))
    if options.goal == 1:
        world.completion_condition[player] = lambda state: (state.has("Beat Bull", player) and state.has("Beat Crikey", player)
                                                            and state.has("Beat Fluffy", player) and state.has("Beat Shadow", player)
                                                            and state.has("Beat Cass", player))
    if options.goal == 2:
        world.completion_condition[player] = lambda state: (state.has("Fire Thunder Egg", player, 24)
                                                            and state.has("Ice Thunder Egg", player, 24)
                                                            and state.has("Air Thunder Egg", player, 24))
    if options.goal == 3:
        world.completion_condition[player] = lambda state: (state.has("Fire Thunder Egg", player, 24)
                                                            and state.has("Ice Thunder Egg", player, 24)
                                                            and state.has("Air Thunder Egg", player, 24)
                                                            and state.has("Golden Cog", player, 90)
                                                            and state.has("Frog Talisman", player)
                                                            and state.has("Platypus Talisman", player)
                                                            and state.has("Cockatoo Talisman", player)
                                                            and state.has("Dingo Talisman", player)
                                                            and state.has("Tiger Talisman", player))
