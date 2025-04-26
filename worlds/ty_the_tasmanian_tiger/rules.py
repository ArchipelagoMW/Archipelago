import enum
from typing import Dict

from BaseClasses import CollectionState
from worlds.ty_the_tasmanian_tiger.regions import Ty1LevelCode, ty1_levels, ty1_levels_short


vanilla_boss_map = [7, 19, 15]


thegg_type_names = {
    0: "Fire Thunder Egg",
    1: "Ice Thunder Egg",
    2: "Air Thunder Egg"
}


ty1_rangs: Dict[int, str] = {
    1: "Second Rang",
    2: "Swim",
    3: "Aquarang",
    4: "Dive",
    5: "Flamerang",
    6: "Frostyrang",
    7: "Zappyrang",
    8: "Doomerang"
}


class Ty1Rang(enum.IntEnum):
    SECOND_RANG = 1
    SWIM = 2
    AQUARANG = 3
    DIVE = 4
    FLAMERANG = 5
    FROSTYRANG = 6
    ZAPPYRANG = 7
    DOOMERANG = 8


class TheggType(enum.Enum):
    FIRE_THEGG = 0,
    ICE_THEGG = 1,
    AIR_THEGG = 2


def has_progressive_rang(world, state: CollectionState, level: int):
    return state.has("Progressive Rang", world.player, level)


def has_stopwatch(world, state: CollectionState, level: Ty1LevelCode):
    return state.has(f"Stopwatch - {ty1_levels[level]}", world.player)


def has_all_bilbies(world, state: CollectionState, level: Ty1LevelCode):
    return state.has(f"Bilby - {ty1_levels[level]}", world.player, 5)


def can_reach_bilbies(world, state: CollectionState, level: Ty1LevelCode):
    return (state.can_reach_location(f"{ty1_levels_short[level]} - Bilby Dad", world.player) and
            state.can_reach_location(f"{ty1_levels_short[level]} - Bilby Mum", world.player) and
            state.can_reach_location(f"{ty1_levels_short[level]} - Bilby Boy", world.player) and
            state.can_reach_location(f"{ty1_levels_short[level]} - Bilby Girl", world.player) and
            state.can_reach_location(f"{ty1_levels_short[level]} - Bilby Grandma", world.player))


def can_reach_cogs(world, state: CollectionState, level: Ty1LevelCode):
    result = True
    for i in range(10):
        if not state.can_reach_location(f"{ty1_levels_short[level]} - Golden Cog {str(i + 1)}", world.player):
            result = False
    return result


def has_level(world, state: CollectionState, level_index: int):
    if world.options.level_unlock_style == 0:
        return True
    if world.options.level_unlock_style == 2:
        if level_index == 9:
            return (state.has("Progressive Level", world.player, 9)
                    or state.has("Portal - Cass' Pass", world.player))
        portal_name = f"Portal - {ty1_levels[Ty1LevelCode(world.portal_map[level_index])]}"
        return (state.has("Progressive Level", world.player, level_index)
                or state.has(portal_name, world.player))
    if world.options.level_unlock_style == 1:
        if level_index == 9:
            return (state.has("Progressive Level", world.player, 12)
                    or state.has("Portal - Cass' Pass", world.player))
        portal_name: str = f"Portal - {ty1_levels[Ty1LevelCode(world.portal_map[level_index])]}"
        prog_count: int = level_index + (level_index > 2) + (level_index > 5)
        return (state.has("Progressive Level", world.player, prog_count)
                or state.has(portal_name, world.player))


def has_boss(world, state: CollectionState, level_index: int):
    if world.options.level_unlock_style != 1:
        return state.has(thegg_type_names[level_index], world.player, world.options.thegg_gating)
    portal_name = f"Portal - {ty1_levels[Ty1LevelCode(vanilla_boss_map[level_index])]}"
    if world.options.progressive_level:
        return state.has("Progressive Level", world.player, 3 + (4 * level_index))
    return state.has(portal_name, world.player)


def has_rang(world, state: CollectionState, rang_id: int):
    return state.has(ty1_rangs[rang_id], world.player) or has_progressive_rang(world, state, rang_id)


def can_go_water(world, state: CollectionState):
    return has_rang(world, state, Ty1Rang.SWIM) or has_rang(world, state, Ty1Rang.DIVE)


def can_ice_swim(world, state: CollectionState):
    return can_go_water(world, state) and has_rang(world, state, Ty1Rang.FROSTYRANG)


def can_throw_water(world, state: CollectionState):
    return can_go_water(world, state) and has_rang(world, state, Ty1Rang.AQUARANG)


def has_theggs(world, state: CollectionState, thegg_type: TheggType, amount: int):
    if thegg_type == TheggType.FIRE_THEGG:
        return state.has("Fire Thunder Egg", world.player, amount)
    if thegg_type == TheggType.ICE_THEGG:
        return state.has("Ice Thunder Egg", world.player, amount)
    if thegg_type == TheggType.AIR_THEGG:
        return state.has("Air Thunder Egg", world.player, amount)


def get_rules(world):
    rules = {
        "locations": {
            "Two Up - Collect 300 Opals":
                lambda state:
                    state.can_reach_region("Two Up - Upper Area", world.player)
                    and state.can_reach_region("Two Up - End Area", world.player),
            "Two Up - Time Attack":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.A1) if world.options.gate_time_attacks
                    else state.can_reach_location("Two Up - Glide The Gap", world.player),
            "WitP - Wombat Race":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.A2) if world.options.gate_time_attacks
                    else state.can_reach_location("WitP - Truck Trouble", world.player),
            "Ship Rex - Race Rex":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.A3) if world.options.gate_time_attacks
                    else state.can_reach_location("Ship Rex - Where's Elle?", world.player),
            "BotRT - Collect 300 Opals":
                lambda state:
                    can_go_water(world, state),
            "BotRT - Find 5 Bilbies":
                lambda state:
                    can_reach_bilbies(world, state, Ty1LevelCode.B1),
            "BotRT - Time Attack":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.B1) if world.options.gate_time_attacks
                    else state.can_reach_location("BotRT - Home, Sweet, Home", world.player),
            "BotRT - Home, Sweet, Home":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG),
            "BotRT - Heat Dennis' House":
                lambda state:
                    state.can_reach_location("BotRT - Home, Sweet, Home", world.player),
            "BotRT - Ty Diving":
                lambda state:
                    has_rang(world, state, Ty1Rang.DIVE)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.ZAPPYRANG)),
            "Snow Worries - Collect 300 Opals":
                lambda state:
                    has_rang(world, state, Ty1Rang.AQUARANG),
            "Snow Worries - Koala Chaos":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG) or world.options.logic_difficulty == 1,
            "Snow Worries - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.B2),
            "Snow Worries - Time Attack":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.B2) if world.options.gate_time_attacks
                    else state.can_reach_location("Snow Worries - Koala Chaos", world.player),
            "Snow Worries - Trap The Yabby":
                lambda state:
                    has_rang(world, state, Ty1Rang.AQUARANG),
            "Outback Safari - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.B3),
            "Outback Safari - Time Attack":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.B3) if world.options.gate_time_attacks
                    else state.can_reach_location("Outback Safari - Emu Roundup", world.player),
            "LLPoF - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.C1),
            "LLPoF - Time Attack":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.C1) if world.options.gate_time_attacks
                    else state.can_reach_location("LLPoF - Lenny The Lyrebird", world.player),
            "LLPoF - Fiery Furnace":
                lambda state:
                    has_rang(world, state, Ty1Rang.FROSTYRANG),
            "LLPoF - Muddy Towers":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.DIVE)),
            "BtBS - Collect 300 Opals":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "BtBS - Find 5 Bilbies":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or world.options.logic_difficulty == 1,
            "BtBS - Wombat Rematch":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.C2) if world.options.gate_time_attacks
                    else state.can_reach_location("BtBS - Koala Crisis", world.player),
            "BtBS - Koala Crisis":
                lambda state:
                    has_rang(world, state, Ty1Rang.FROSTYRANG)
                    or world.options.logic_difficulty == 1,
            "RMtS - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.C3),
            "RMtS - Race Rex":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.C3) if world.options.gate_time_attacks
                    else state.can_reach_location("RMtS - Treasure Hunt", world.player),
            "RMtS - Geyser Hop":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or (world.options.logic_difficulty == 1
                        and (can_ice_swim(world, state)
                             or has_rang(world, state, Ty1Rang.DOOMERANG))),
            "RMtS - Volcanic Panic":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG) or
                    (world.options.logic_difficulty == 1 and can_ice_swim(world, state)),
            "BotRT - Golden Cog 1":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "BotRT - Golden Cog 2":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or world.options.logic_difficulty == 1,
            "BotRT - Golden Cog 8":
                lambda state:
                    can_throw_water(world, state) or has_rang(world, state, Ty1Rang.FROSTYRANG)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.SECOND_RANG)),
            "BotRT - Golden Cog 10":
                lambda state:
                    can_go_water(world, state),
            "Snow Worries - Golden Cog 3":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or (world.options.logic_difficulty == 1 and can_go_water(world, state)),
            "Snow Worries - Golden Cog 7":
                lambda state:
                    has_rang(world, state, Ty1Rang.AQUARANG),
            "LLPoF - Golden Cog 4":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player)
                    or world.options.logic_difficulty == 1,
            "LLPoF - Golden Cog 5":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "LLPoF - Golden Cog 10":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "BtBS - Golden Cog 7":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player)
                    or world.options.logic_difficulty == 1,
            "RMtS - Golden Cog 2":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG) or has_rang(world, state, Ty1Rang.FROSTYRANG),
            "RMtS - Golden Cog 6":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "RMtS - Golden Cog 8":
                lambda state:
                    can_throw_water(world, state) or has_rang(world, state, Ty1Rang.FROSTYRANG),
            "Two Up - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.A1),
            "WitP - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.A2),
            "Ship Rex - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.A3),
            "BotRT - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.B1),
            "Snow Worries - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.B2),
            "Outback Safari - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.B3),
            "LLPoF - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.C1),
            "BtBS - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.C2),
            "RMtS - Bilby Completion":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.C3),
            "BotRT - Bilby Mum":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or (world.options.logic_difficulty == 1
                        and has_rang(world, state, Ty1Rang.SECOND_RANG)
                        and can_go_water(world, state)),
            "Snow Worries - Bilby Mum":
                lambda state:
                    (has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player))
                    or world.options.logic_difficulty == 1,
            "BtBS - Bilby Dad":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or world.options.logic_difficulty == 1,
            "BtBS - Bilby Mum":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or world.options.logic_difficulty == 1,
            "Snow Worries - PF 13":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.SECOND_RANG)),
            "Ship Rex - Opal 28":
                lambda state:
                    can_go_water(world, state),
            "Ship Rex - Opal 59":
                lambda state:
                    can_go_water(world, state),
            "Ship Rex - Opal 93":
                lambda state:
                    can_go_water(world, state),
            "Ship Rex - Opal 94":
                lambda state:
                    can_go_water(world, state),
            "Ship Rex - Opal 95":
                lambda state:
                    can_go_water(world, state),
            "Snow Worries - Opal 64":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player)
                    or world.options.logic_difficulty == 1,
            "Snow Worries - Opal 69":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player)
                    or world.options.logic_difficulty == 1,
            "Snow Worries - Opal 74":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player)
                    or world.options.logic_difficulty == 1,
            "Snow Worries - Opal 79":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player)
                    or world.options.logic_difficulty == 1,
            "Snow Worries - Opal 84":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player)
                    or world.options.logic_difficulty == 1,
            "Snow Worries - Opal 85":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) or state.has("Kaboomerang", world.player)
                    or world.options.logic_difficulty == 1,
            "LLPoF - Opal 91":
                lambda state:
                has_rang(world, state, Ty1Rang.SECOND_RANG)
                or world.options.logic_difficulty == 1,
            "LLPoF - Opal 98":
                lambda state:
                has_rang(world, state, Ty1Rang.SECOND_RANG)
                or world.options.logic_difficulty == 1,
            "LLPoF - Opal 101":
                lambda state:
                has_rang(world, state, Ty1Rang.SECOND_RANG)
                or world.options.logic_difficulty == 1,
            "Attribute - Doomerang":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) and has_rang(world, state, Ty1Rang.FROSTYRANG),
            "Attribute - Extra Health":
                lambda state:
                    can_go_water(world, state) and
                    (world.options.logic_difficulty == 1 or
                        all(state.can_reach_region(region, world.player) for region in [
                            "Bli Bli Station Gate",
                            "Pippy Beach",
                            "Lake Burril",
                            "Final Gauntlet"
                        ])),
            "Attribute - Zoomerang":
                lambda state:
                    state.has("Golden Cog", world.player, world.options.cog_gating * 1),
            "Attribute - Multirang":
                lambda state:
                    state.has("Golden Cog", world.player, world.options.cog_gating * 2),
            "Attribute - Infrarang":
                lambda state:
                    state.has("Golden Cog", world.player, world.options.cog_gating * 3),
            "Attribute - Megarang":
                lambda state:
                    state.has("Golden Cog", world.player, world.options.cog_gating * 4),
            "Attribute - Kaboomarang":
                lambda state:
                    state.has("Golden Cog", world.player, world.options.cog_gating * 5),
            "Attribute - Chronorang":
                lambda state:
                    state.has("Golden Cog", world.player, world.options.cog_gating * 6),
            "BotRT - All Golden Cogs":
                lambda state:
                    can_reach_cogs(world, state, Ty1LevelCode.B1),
            "Snow Worries - All Golden Cogs":
                lambda state:
                    can_reach_cogs(world, state, Ty1LevelCode.B2),
            "LLPoF - All Golden Cogs":
                lambda state:
                    can_reach_cogs(world, state, Ty1LevelCode.C1),
            "BtBS - All Golden Cogs":
                lambda state:
                    can_reach_cogs(world, state, Ty1LevelCode.C2),
            "RMtS - All Golden Cogs":
                lambda state:
                    can_reach_cogs(world, state, Ty1LevelCode.C3),
            "Snow Worries - All Picture Frames":
                lambda state:
                    state.can_reach_location("Snow Worries - Bilby Mum", world.player),
            "Rainbow Cliffs - All Picture Frames":
                lambda state:
                    state.can_reach_region("Final Gauntlet - PF", world.player) and
                    state.can_reach_region("Pippy Beach - PF", world.player) and
                    state.can_reach_region("Bli Bli Station Gate - PF", world.player),
            "Platypus Talisman":
                lambda state:
                    can_throw_water(world, state) and has_rang(world, state, Ty1Rang.FLAMERANG),
            "Cockatoo Talisman":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) and has_rang(world, state, Ty1Rang.FROSTYRANG)
                    or world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.DOOMERANG),
            "Dingo Talisman":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Tiger Talisman":
                lambda state:
                    has_rang(world, state, Ty1Rang.DOOMERANG) and
                    (world.options.logic_difficulty == 1 or (has_rang(world, state, Ty1Rang.FLAMERANG)
                     and has_rang(world, state, Ty1Rang.FROSTYRANG))),
            "Attribute - Flamerang":
                lambda state:
                    has_theggs(world, state, TheggType.FIRE_THEGG, world.options.thegg_gating.value)
                    and state.has("Frog Talisman", world.player),
            "Attribute - Frostyrang":
                lambda state:
                    has_theggs(world, state, TheggType.ICE_THEGG, world.options.thegg_gating.value)
                    and state.has("Platypus Talisman", world.player)
                    and state.can_reach_location("Attribute - Flamerang", world.player),
            "Attribute - Zappyrang":
                lambda state:
                    has_theggs(world, state, TheggType.AIR_THEGG, world.options.thegg_gating.value)
                    and state.has("Cockatoo Talisman", world.player)
                    and state.can_reach_location("Attribute - Frostyrang", world.player),
            "Rainbow Scale 11":
                lambda state:
                    has_rang(world, state, Ty1Rang.FROSTYRANG)
                    or world.options.logic_difficulty == 1,
            "Rainbow Scale 7":
                lambda state:
                has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "Rainbow Scale 15":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "Rainbow Scale 16":
                lambda state:
                    can_go_water(world, state),
            "Rainbow Scale 21":
                lambda state:
                    can_go_water(world, state),
            "Rainbow Scale 24":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Two Up - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("Two Up - Time Attack", world.player)
                    and has_rang(world, state, Ty1Rang.DIVE) if world.options.logic_difficulty == 1 else True,
            "WitP - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("WitP - Wombat Race", world.player),
            "Ship Rex - Time Attack Challenge":
                lambda state:
                    has_rang(world, state, Ty1Rang.DIVE) and
                    state.can_reach_location("Ship Rex - Race Rex", world.player),
            "BotRT - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("BotRT - Time Attack", world.player)
                    and can_go_water(world, state) if world.options.logic_difficulty == 1 else True,
            "Snow Worries - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("Snow Worries - Time Attack", world.player),
            "Outback Safari - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("Outback Safari - Race Shazza", world.player),
            "LLPoF - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("LLPoF - Time Attack", world.player),
            "BtBS - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("BtBS - Wombat Rematch", world.player),
            "RMtS - Time Attack Challenge":
                lambda state:
                    has_rang(world, state, Ty1Rang.DIVE) and
                    state.can_reach_location("RMtS - Race Rex", world.player),
            "Two Up - Extra Life 2":
                lambda state:
                    can_go_water(world, state),
            "Crikey's Cove - Extra Life 1":
                lambda state:
                    can_go_water(world, state),
            "RMtS - Extra Life 2":
                lambda state:
                    can_go_water(world, state),
            "Cass' Pass - Extra Life 1":
                lambda state:
                    can_go_water(world, state),
            "Cass' Pass - Extra Life 2":
                lambda state:
                    can_go_water(world, state),
            "Cass' Crest - Extra Life 1":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Cass' Crest - Extra Life 2":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Cass' Crest - Extra Life 4":
                lambda state:
                    can_go_water(world, state),
            "Cass' Crest - Extra Life 5":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Beat Bull":
                lambda state:
                    state.can_reach_location("Frog Talisman", world.player),
            "Beat Crikey":
                lambda state:
                    state.can_reach_location("Cockatoo Talisman", world.player),
            "Beat Fluffy":
                lambda state:
                    state.can_reach_location("Platypus Talisman", world.player),
            "Beat Shadow":
                lambda state:
                    state.can_reach_location("Dingo Talisman", world.player),
            "Beat Cass":
                lambda state:
                    state.can_reach_location("Tiger Talisman", world.player)
        },
        "entrances": {
            "Z1 - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "A Zone Gate":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "A Zone Gate - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Z1 -> B Zone":
                lambda state: 
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.DIVE)),
            "B Zone - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Z1 -> C Zone":
                lambda state:
                    has_rang(world, state, Ty1Rang.FROSTYRANG)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.DIVE)),
            "Z1 -> E Zone":
                lambda state:
                    has_rang(world, state, Ty1Rang.ZAPPYRANG)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.DIVE)),
            "E Zone - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "A1 Portal":
                lambda state:
                    has_level(world, state, 0),
            "A2 Portal":
                lambda state:
                    has_level(world, state, 1),
            "A3 Portal":
                lambda state:
                    has_level(world, state, 2),
            "A4 Portal":
                lambda state:
                    has_boss(world, state, 0),
            "B1 Portal":
                lambda state:
                    has_level(world, state, 3),
            "B2 Portal":
                lambda state:
                    has_level(world, state, 4),
            "B3 Portal":
                lambda state:
                    has_level(world, state, 5),
            "D4 Portal":
                lambda state:
                    has_boss(world, state, 1),
            "C1 Portal":
                lambda state:
                    has_level(world, state, 6),
            "C2 Portal":
                lambda state:
                    has_level(world, state, 7),
            "C3 Portal":
                lambda state:
                    has_level(world, state, 8),
            "C4 Portal":
                lambda state:
                    has_boss(world, state, 2),
            "E1 Portal":
                lambda state:
                    has_level(world, state, 9),
            "D2 -> E4":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG) and state.has("Beat Shadow", world.player)
                    and (not world.options.req_bosses
                         or (state.has("Beat Bull", world.player)
                             and state.has("Beat Crikey", world.player)
                             and state.has("Beat Fluffy", world.player))),
            "Two Up - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Two Up - Upper Area":
                lambda state:
                    world.options.logic_difficulty == 1 or
                    (has_rang(world, state, Ty1Rang.SWIM) or has_rang(world, state, Ty1Rang.DIVE)
                     or has_rang(world, state, Ty1Rang.SECOND_RANG)),
            "Two Up - Upper Area - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Two Up - End Area":
                lambda state:
                    world.options.logic_difficulty == 1 or
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Walk in the Park - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Ship Rex - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Ship Rex - Sea Gate":
                lambda state:
                    (world.options.logic_difficulty == 0 and can_throw_water(world, state))
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.DIVE)),
            "Ship Rex - Gate - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Bridge on the River Ty - Underwater":
                lambda state:
                    can_go_water(world, state),
            "Bridge on the River Ty - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Bridge on the River Ty - Broken Bridge Glide":
                lambda state:
                    world.options.logic_difficulty == 1 or has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Bridge on the River Ty - Beyond Broken Bridge Underwater":
                lambda state:
                    can_go_water(world, state),
            "Bridge on the River Ty - Broken Bridge - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Snow Worries - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Snow Worries - Underwater":
                lambda state:
                   state.has("Swim", world.player)
                   or world.options.logic_difficulty == 1 and state.has("Dive", world.player),
            "Lyre, Lyre Pants on Fire - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Beyond the Black Stump - Behind Burning Logs":
                lambda state:
                    world.options.logic_difficulty == 1 or has_rang(world, state, Ty1Rang.FROSTYRANG),
            "Beyond the Black Stump - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Beyond the Black Stump - Upper Area":
                lambda state:
                    world.options.logic_difficulty == 1 or has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Beyond the Black Stump - Glide":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Beyond the Black Stump - Upper Area - PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Rex Marks the Spot, PF":
                lambda state:
                    not world.options.frames_require_infra or state.has("Infrarang", world.player),
            "Rex Marks the Spot - Underwater":
                lambda state:
                    can_go_water(world, state),
        }
    }
    return rules


def set_rules(world):
    from . import Ty1World
    world: Ty1World
    rules_lookup = get_rules(world)
    for entrance_name, rule in rules_lookup["entrances"].items():
        try:
            world.get_entrance(entrance_name).access_rule = rule
        except KeyError:
            pass

    for location_name, rule in rules_lookup["locations"].items():
        try:
            world.get_location(location_name).access_rule = rule
        except KeyError:
            pass

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Beat Cass", world.player)
