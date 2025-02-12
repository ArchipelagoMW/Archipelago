import enum
from typing import Dict

from BaseClasses import MultiWorld
from worlds.ty_the_tasmanian_tiger.regions import Ty1LevelCode, ty1_levels, ty1_levels_short


def has_progressive_rang(world, state, level: int):
    return state.has("Progressive Rang", world.player, level + 1 if (
            world.options.progressive_elementals and not world.options.start_with_boom
    ) else level)


def has_stopwatch(world, state, level: Ty1LevelCode):
    return state.has("Stopwatch - " + ty1_levels[level], world.player)


def has_all_bilbies(world, state, level: Ty1LevelCode):
    return state.has("Bilby - " + ty1_levels[level], world.player, 5)


def can_reach_bilbies(world, state, level: Ty1LevelCode):
    return (state.can_reach_location(ty1_levels_short[level] + " - Bilby Dad", world.player) and
            state.can_reach_location(ty1_levels_short[level] + " - Bilby Mum", world.player) and
            state.can_reach_location(ty1_levels_short[level] + " - Bilby Boy", world.player) and
            state.can_reach_location(ty1_levels_short[level] + " - Bilby Girl", world.player) and
            state.can_reach_location(ty1_levels_short[level] + " - Bilby Grandma", world.player))


def can_reach_cogs(world, state, level: Ty1LevelCode):
    result = True
    for i in range(10):
        if not state.can_reach_location(ty1_levels_short[level] + " - Golden Cog " + str(i + 1), world.player):
            result = False
    return result


ty1_rangs: Dict[int, str] = {
    0: "Boomerang",
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
    BOOMERANG = 0
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


thegg_type_names = {
    0: "Fire Thunder Egg",
    1: "Ice Thunder Egg",
    2: "Air Thunder Egg"
}


def has_level(world, state, level_index: int):
    if world.options.level_unlock_style == 0:
        return True
    if world.options.level_unlock_style == 2:
        if level_index == 9:
            return (state.has("Progressive Level", world.player, 9)
                    or state.has("Portal - Cass' Pass", world.player))
        portal_name = "Portal - " + ty1_levels[Ty1LevelCode(world.portal_map[level_index])]
        return (state.has("Progressive Level", world.player, level_index)
                or state.has(portal_name, world.player))
    if world.options.level_unlock_style == 1:
        if level_index == 9:
            return (state.has("Progressive Level", world.player, 12)
                    or state.has("Portal - Cass' Pass", world.player))
        portal_name = "Portal - " + ty1_levels[Ty1LevelCode(world.portal_map[level_index])]
        prog_count = level_index + (level_index > 2) + (level_index > 5)
        return (state.has("Progressive Level", world.player, prog_count)
                or state.has(portal_name, world.player))


def has_boss(world, state, level_index: int):
    if world.options.level_unlock_style != 1:
        return state.has(thegg_type_names[level_index], world.player, world.options.thegg_gating)
    portal_name = "Portal - " + ty1_levels[Ty1LevelCode(world.boss_map[level_index])]
    if world.options.progressive_level:
        return state.has("Progressive Level", world.player, 3 + (4 * level_index))
    return state.has(portal_name, world.player)


def has_rang(world, state, rang_id: int):
    return state.has(ty1_rangs[rang_id], world.player) or has_progressive_rang(world, state, rang_id)


def can_go_water(world, state):
    return has_rang(world, state, Ty1Rang.SWIM) or has_rang(world, state, Ty1Rang.DIVE)


def can_ice_swim(world, state):
    return can_go_water(world, state) and has_rang(world, state, Ty1Rang.FROSTYRANG)


def can_throw_water(world, state):
    return can_go_water(world, state) and has_rang(world, state, Ty1Rang.AQUARANG)


def has_theggs(world, state, thegg_type: TheggType, amount: int):
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
                    state.can_reach_region("Two Up - Upper Area", world.player) and state.can_reach_region("Two Up - End Area", world.player),
            "Two Up - Time Attack":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.A1) if world.options.gate_time_attacks
                    else state.can_reach_location("Two Up - Glide The Gap", world.player),
            "WitP - Wombat Race":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.A2) if world.options.gate_time_attacks
                    else state.can_reach_location("WitP - Truck Trouble", world.player),
            "WitP - Truck Trouble":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "WitP - Drive Me Batty":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "Ship Rex - Race Rex":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.A3) if world.options.gate_time_attacks
                    else state.can_reach_location("Ship Rex - Where's Elle?", world.player),
            "Ship Rex - Quicksand Coconuts":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
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
            "BotRT - Neddy The Bully":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "Snow Worries - Collect 300 Opals":
                lambda state:
                    has_rang(world, state, Ty1Rang.AQUARANG),
            "Snow Worries - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.B2),
            "Snow Worries - Time Attack":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.B2) if world.options.gate_time_attacks
                    else state.can_reach_location("Snow Worries - Koala Chaos", world.player),
            "Snow Worries - Koala Chaos":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "Snow Worries - The Old Mill":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "Snow Worries - Trap The Yabby":
                lambda state:
                    has_rang(world, state, Ty1Rang.AQUARANG),
            "Snow Worries - Musical Icicle":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "Outback Safari - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.B3),
            "Outback Safari - Time Attack":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.B3) if world.options.gate_time_attacks
                    else state.can_reach_location("Outback Safari - Emu Roundup", world.player),
            "Outback Safari - Toxic Trouble":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
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
            "BtBS - Cable Car Capers":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    or world.options.logic_difficulty == 1,
            "RMtS - Find 5 Bilbies":
                lambda state:
                    has_all_bilbies(world, state, Ty1LevelCode.C3),
            "RMtS - Race Rex":
                lambda state:
                    has_stopwatch(world, state, Ty1LevelCode.C3) if world.options.gate_time_attacks
                    else state.can_reach_location("RMtS - Treasure Hunt", world.player),
            "RMtS - Parrot Beard's Booty":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "RMtS - Frill Boat Battle":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "RMtS - Geyser Hop":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or (world.options.logic_difficulty == 1 and (can_ice_swim(world, state) or has_rang(world, state, Ty1Rang.DOOMERANG))),
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
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.SECOND_RANG) and can_go_water(world, state)),
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
            "Attribute - Doomerang":
                lambda state:
                    has_rang(world, state, Ty1Rang.FLAMERANG) and has_rang(world, state, Ty1Rang.FROSTYRANG),
            "Attribute - Extra Health":
                lambda state:
                    can_go_water(world, state) and
                    (state.can_reach_region("Bli Bli Station Gate", world.player)
                     and state.can_reach_region("Pippy Beach", world.player)
                     and state.can_reach_region("Lake Burril", world.player)
                     and state.can_reach_region("Final Gauntlet", world.player)) if world.options.logic_difficulty == 0 else True,
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
                    state.can_reach_region("Final Gauntlet - PF") and
                    state.can_reach_region("Pippy Beach - PF") and
                    state.can_reach_region("Bli Bli Station Gate - PF"),
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
                    ((has_rang(world, state, Ty1Rang.FLAMERANG)
                      and has_rang(world, state, Ty1Rang.FROSTYRANG))if world.options.logic_difficulty == 0 else True),
            "Attribute - Flamerang":
                lambda state:
                    has_theggs(world, state, TheggType.FIRE_THEGG, world.options.thegg_gating.value)
                    and state.has("Frog Talisman", world.player),
            "Attribute - Frostyrang":
                lambda state:
                    has_theggs(world, state, TheggType.ICE_THEGG, world.options.thegg_gating.value)
                    and state.has("Platypus Talisman", world.player),
            "Attribute - Zappyrang":
                lambda state:
                    has_theggs(world, state, TheggType.AIR_THEGG, world.options.thegg_gating.value)
                    and state.has("Cockatoo Talisman", world.player),
            "Rainbow Scale 11":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG) or has_rang(world, state, Ty1Rang.FROSTYRANG)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.SWIM)),
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
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "Two Up - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("Two Up - Time Attack", world.player),
            "WitP - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("WitP - Wombat Race", world.player),
            "Ship Rex - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("Ship Rex - Race Rex", world.player),
            "BotRT - Time Attack Challenge":
                lambda state:
                    state.can_reach_location("BotRT - Time Attack", world.player),
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
                    state.can_reach_location("RMtS - Race Rex", world.player),
        },
        "entrances": {
            "Z1 - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "A Zone Gate":
                lambda state:
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    or world.options.logic_difficulty == 1,
            "A Zone Gate - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Z1 -> B Zone":
                lambda state: 
                    has_rang(world, state, Ty1Rang.FLAMERANG)
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.DIVE)),
            "B Zone - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
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
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
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
                    has_rang(world, state, Ty1Rang.SECOND_RANG)
                    and (state.can_reach_location("Frog Talisman", world.player)
                         and state.can_reach_location("Platypus Talisman", world.player)
                         and state.can_reach_location("Cockatoo Talisman", world.player)) if world.options.req_bosses else (
                        True
                    ),
            "Two Up - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Two Up - Upper Area":
                lambda state:
                    world.options.logic_difficulty == 1 or
                    (has_rang(world, state, Ty1Rang.SWIM) or has_rang(world, state, Ty1Rang.DIVE)
                     or has_rang(world, state, Ty1Rang.SECOND_RANG)),
            "Two Up - Upper Area - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Two Up - End Area":
                lambda state:
                    world.options.logic_difficulty == 1 or
                    has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Walk in the Park - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Ship Rex - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Ship Rex - Sea Gate":
                lambda state:
                    (world.options.logic_difficulty == 0 and can_throw_water(world, state))
                    or (world.options.logic_difficulty == 1 and has_rang(world, state, Ty1Rang.DIVE)),
            "Ship Rex - Gate - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Bridge on the River Ty - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Bridge on the River Ty - Broken Bridge Glide":
                lambda state:
                    world.options.logic_difficulty == 1 or has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Bridge on the River Ty - Broken Bridge - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Snow Worries - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Snow Worries - Underwater":
                lambda state:
                    can_go_water(world, state),
            "Lyre, Lyre Pants on Fire - Gate":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG),
            "Lyre, Lyre Pants on Fire - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Lyre, Lyre Pants on Fire - Gate - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Beyond the Black Stump - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Beyond the Black Stump - Upper Area":
                lambda state:
                    world.options.logic_difficulty == 1 or has_rang(world, state, Ty1Rang.SECOND_RANG),
            "Beyond the Black Stump - Upper Area - PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Rex Marks the Spot, PF":
                lambda state:
                    has_rang(world, state, Ty1Rang.BOOMERANG)
                    and state.has("Infrarang", world.player) if world.options.frames_require_infra else True,
            "Rex Marks the Spot - Underwater":
                lambda state:
                    can_go_water(world, state),
        }
    }
    return rules


def set_rules(world):

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

    world.multiworld.completion_condition[world.player] = lambda state: (state.can_reach_location("Tiger Talisman", world.player) and (state.can_reach_location("Dingo Talisman", world.player)))
