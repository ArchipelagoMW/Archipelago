from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState
from typing import Dict
from .Regions import Stages


def graffitiM(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group_unique("graffitim", player) * 7 >= spots if limit \
        else state.has_group("graffitim", player)


def graffitiL(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group_unique("graffitil", player) * 6 >= spots if limit \
        else state.has_group("graffitil", player)


def graffitiXL(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group_unique("graffitixl", player) * 4 >= spots if limit \
        else state.has_group("graffitixl", player)


def skateboard(state: CollectionState, player: int, movestyle: int) -> bool:
    return True if movestyle == 2 else state.has_group("skateboard", player)


def inline_skates(state: CollectionState, player: int, movestyle: int) -> bool:
    return True if movestyle == 3 else state.has_group("skates", player)


def bmx(state: CollectionState, player: int, movestyle: int) -> bool:
    return True if movestyle == 1 else state.has_group("bmx", player)


def camera(state: CollectionState, player: int) -> bool:
    return state.has("Camera App", player)


def is_girl(state: CollectionState, player: int) -> bool:
    return state.has_group("girl", player)


def current_chapter(state: CollectionState, player: int, chapter: int) -> bool:
    return state.has("Chapter Completed", player, chapter-1)
    

def versum_hill_entrance(state: CollectionState, player: int) -> bool:
    return rep(state, player, 20)
    

def versum_hill_ch1_roadblock(state: CollectionState, player: int, limit: bool) -> bool:
    return graffitiL(state, player, limit, 10)
    

def versum_hill_challenge1(state: CollectionState, player: int) -> bool:
    return rep(state, player, 50)
    

def versum_hill_challenge2(state: CollectionState, player: int) -> bool:
    return rep(state, player, 58)
    

def versum_hill_challenge3(state: CollectionState, player: int) -> bool:
    return rep(state, player, 65)
    

def versum_hill_all_challenges(state: CollectionState, player: int) -> bool:
    return versum_hill_challenge3(state, player)


def versum_hill_basketball_court(state: CollectionState, player: int) -> bool:
    return rep(state, player, 90)
    

def versum_hill_oldhead(state: CollectionState, player: int) -> bool:
    return rep(state, player, 120)
    

def versum_hill_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            rep(state, player, 90)
            and graffitiM(state, player, limit, 98)
        )
    else:
        return (
            rep(state, player, 90)
            and graffitiM(state, player, limit, 27)
        )
    

def versum_hill_rietveld(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            current_chapter(state, player, 2)
            and graffitiM(state, player, limit, 114)
        )
    else:
        return (
            current_chapter(state, player, 2)
            and graffitiM(state, player, limit, 67)
        )
    

def versum_hill_rave(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        if current_chapter(state, player, 4):
            return (
                graffitiL(state, player, limit, 90)
                and graffitiXL(state, player, limit, 51)
            )
        elif current_chapter(state, player, 3):
            return (
                graffitiL(state, player, limit, 89)
                and graffitiXL(state, player, limit, 51)
            )
        else:
            return (
                graffitiL(state, player, limit, 85)
                and graffitiXL(state, player, limit, 48)
            )
    else:
        return (
            graffitiL(state, player, limit, 26)
            and graffitiXL(state, player, limit, 10)
        )


def millennium_square_entrance(state: CollectionState, player: int) -> bool:
    return current_chapter(state, player, 2)


def brink_terminal_entrance(state: CollectionState, player: int) -> bool:
    return (
        is_girl(state, player)
        and rep(state, player, 180)
        and current_chapter(state, player, 2)
    )


def brink_terminal_challenge1(state: CollectionState, player: int) -> bool:
    return rep(state, player, 188)


def brink_terminal_challenge2(state: CollectionState, player: int) -> bool:
    return rep(state, player, 200)


def brink_terminal_challenge3(state: CollectionState, player: int) -> bool:
    return rep(state, player, 220)


def brink_terminal_all_challenges(state: CollectionState, player: int) -> bool:
    return brink_terminal_challenge3(state, player)


def brink_terminal_plaza(state: CollectionState, player: int) -> bool:
    return brink_terminal_all_challenges(state, player)
    

def brink_terminal_tower(state: CollectionState, player: int) -> bool:
    return rep(state, player, 280)
    

def brink_terminal_oldhead_underground(state: CollectionState, player: int) -> bool:
    return rep(state, player, 250)
    

def brink_terminal_oldhead_dock(state: CollectionState, player: int) -> bool:
    return rep(state, player, 320)
    

def brink_terminal_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            rep(state, player, 280)
            and graffitiL(state, player, limit, 103)
        )
    else:
        return (
            rep(state, player, 280)
            and graffitiL(state, player, limit, 62)
        )
    

def brink_terminal_mesh(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            graffitiM(state, player, limit, 114)
            and graffitiXL(state, player, limit, 45)
        )
    else:
        return (
            graffitiM(state, player, limit, 67)
            and graffitiXL(state, player, limit, 45)
        )


def millennium_mall_entrance(state: CollectionState, player: int) -> bool:
    return (
        rep(state, player, 380)
        and current_chapter(state, player, 3)
    )
    

def millennium_mall_oldhead_ceiling(state: CollectionState, player: int, limit: bool) -> bool:
    return (
        rep(state, player, 580)
        or millennium_mall_theater(state, player, limit)
    )
    

def millennium_mall_switch(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            graffitiM(state, player, limit, 114)
            and current_chapter(state, player, 3)
        )
    else:
        return (
            graffitiM(state, player, limit, 72)
            and current_chapter(state, player, 3)
        )
    

def millennium_mall_big(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return millennium_mall_switch(state, player, limit, glitched)
    

def millennium_mall_oldhead_race(state: CollectionState, player: int) -> bool:
    return rep(state, player, 530)
    

def millennium_mall_challenge1(state: CollectionState, player: int) -> bool:
    return rep(state, player, 434)


def millennium_mall_challenge2(state: CollectionState, player: int) -> bool:
    return rep(state, player, 442)


def millennium_mall_challenge3(state: CollectionState, player: int) -> bool:
    return rep(state, player, 450)


def millennium_mall_challenge4(state: CollectionState, player: int) -> bool:
    return rep(state, player, 458)


def millennium_mall_all_challenges(state: CollectionState, player: int) -> bool:
    return millennium_mall_challenge4(state, player)


def millennium_mall_theater(state: CollectionState, player: int, limit: bool) -> bool:
    return (
        rep(state, player, 491)
        and graffitiM(state, player, limit, 78)
    )
    

def millennium_mall_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            rep(state, player, 491)
            and graffitiM(state, player, limit, 114)
            and graffitiL(state, player, limit, 107)
        )
    else:
        return (
            rep(state, player, 491)
            and graffitiM(state, player, limit, 78)
            and graffitiL(state, player, limit, 80)
        )


def pyramid_island_entrance(state: CollectionState, player: int) -> bool:
    return current_chapter(state, player, 4)
    

def pyramid_island_gate(state: CollectionState, player: int) -> bool:
    return rep(state, player, 620)
    

def pyramid_island_oldhead(state: CollectionState, player: int) -> bool:
    return rep(state, player, 780)
    

def pyramid_island_challenge1(state: CollectionState, player: int) -> bool:
    return (
        rep(state, player, 630)
        and current_chapter(state, player, 4)
    )


def pyramid_island_race(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched: 
        return (
            pyramid_island_challenge1(state, player)
            and graffitiL(state, player, limit, 108)
        )
    else:
        return (
            pyramid_island_challenge1(state, player)
            and graffitiL(state, player, limit, 93)
        )


def pyramid_island_challenge2(state: CollectionState, player: int) -> bool:
    return rep(state, player, 650)


def pyramid_island_challenge3(state: CollectionState, player: int) -> bool:
    return rep(state, player, 660)


def pyramid_island_all_challenges(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            graffitiM(state, player, limit, 114)
            and rep(state, player, 660)
        )
    else:
        return (
            graffitiM(state, player, limit, 88)
            and rep(state, player, 660)
        )


def pyramid_island_upper_half(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return pyramid_island_all_challenges(state, player, limit, glitched)
    

def pyramid_island_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            rep(state, player, 730)
            and graffitiL(state, player, limit, 108)
        )
    else:
        return (
            rep(state, player, 730)
            and graffitiL(state, player, limit, 97)
        )


def pyramid_island_top(state: CollectionState, player: int) -> bool:
    return current_chapter(state, player, 5)


def mataan_entrance(state: CollectionState, player: int) -> bool:
    return current_chapter(state, player, 2)
    

def mataan_smoke_wall(state: CollectionState, player: int) -> bool:
    return (
        current_chapter(state, player, 5)
        and rep(state, player, 850)
    )
    

def mataan_challenge1(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            current_chapter(state, player, 5)
            and rep(state, player, 864)
            and graffitiL(state, player, limit, 108)
        )
    else:
        return (
            current_chapter(state, player, 5)
            and rep(state, player, 864)
            and graffitiL(state, player, limit, 98)
        )


def mataan_deep_city(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return mataan_challenge1(state, player, limit, glitched)
    

def mataan_oldhead(state: CollectionState, player: int) -> bool:
    return rep(state, player, 935)
    

def mataan_challenge2(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            rep(state, player, 880)
            and graffitiXL(state, player, limit, 59)
        )
    else:
        return (
            rep(state, player, 880)
            and graffitiXL(state, player, limit, 57)
        )


def mataan_challenge3(state: CollectionState, player: int) -> bool:
    return rep(state, player, 920)


def mataan_all_challenges(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return (
        mataan_challenge2(state, player, limit, glitched)
        and mataan_challenge3(state, player)
    )


def mataan_smoke_wall2(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return (
        mataan_all_challenges(state, player, limit, glitched)
        and rep(state, player, 960)
    )


def mataan_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return (
            mataan_smoke_wall2(state, player, limit, glitched)
            and graffitiM(state, player, limit, 122)
            and graffitiXL(state, player, limit, 59)
        )
    else:
        return (
            mataan_smoke_wall2(state, player, limit, glitched)
            and graffitiM(state, player, limit, 117)
            and graffitiXL(state, player, limit, 57)
        )
    

def mataan_deepest(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return mataan_crew_battle(state, player, limit, glitched)
    

def mataan_faux(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return (
        mataan_deepest(state, player, limit, glitched)
        and graffitiM(state, player, limit, 122)
    )


def spots_s_glitchless(state: CollectionState, player: int, limit: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 10
    conditions: Dict[str, int] = {
        "versum_hill_entrance": 1,
        "versum_hill_ch1_roadblock": 11,
        "chapter2": 12,
        "versum_hill_oldhead": 1,
        "brink_terminal_entrance": 9,
        "brink_terminal_plaza": 3,
        "brink_terminal_tower": 0,
        "chapter3": 6,
        "brink_terminal_oldhead_dock": 1,
        "millennium_mall_entrance": 3,
        "millennium_mall_switch": 4,
        "millennium_mall_theater": 3,
        "chapter4": 2,
        "pyramid_island_gate": 5,
        "pyramid_island_upper_half": 8,
        "pyramid_island_oldhead": 2,
        "mataan_smoke_wall": 3,
        "mataan_deep_city": 5,
        "mataan_oldhead": 3,
        "mataan_deepest": 2
    }

    for access_name, graffiti_count in conditions.items():
        if access_cache[access_name]:
            total += graffiti_count
        else:
            break

    if limit:
        sprayable: int = 5 + (state.count_group_unique("characters", player) * 5)
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        return total
    

def spots_s_glitched(state: CollectionState, player: int, limit: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 75
    conditions: Dict[str, int] = {
        "brink_terminal_entrance": 13,
        "chapter3": 6
    }

    for access_name, graffiti_count in conditions.items():
        if access_cache[access_name]:
            total += graffiti_count
        else:
            break

    if limit:
        sprayable: int = 5 + (state.count_group_unique("characters", player) * 5)
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        return total
    

def spots_m_glitchless(state: CollectionState, player: int, limit: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 4
    conditions: Dict[str, int] = {
        "versum_hill_entrance": 3,
        "versum_hill_ch1_roadblock": 13,
        "versum_hill_all_challenges": 3,
        "chapter2": 16,
        "versum_hill_oldhead": 4,
        "brink_terminal_entrance": 13,
        "brink_terminal_plaza": 4,
        "brink_terminal_tower": 0,
        "chapter3": 3,
        "brink_terminal_oldhead_dock": 4,
        "millennium_mall_entrance": 5,
        "millennium_mall_big": 6,
        "millennium_mall_theater": 4,
        "chapter4": 2,
        "millennium_mall_oldhead_ceiling": 1,
        "pyramid_island_gate": 3,
        "pyramid_island_upper_half": 8,
        "chapter5": 2,
        "pyramid_island_oldhead": 5,
        "mataan_deep_city": 7,
        "skateboard": 1,
        "mataan_oldhead": 1,
        "mataan_smoke_wall2": 1,
        "mataan_deepest": 10
    }

    for access_name, graffiti_count in conditions.items():
        if access_cache[access_name]:
            total += graffiti_count
        elif access_name != "skateboard":
            break

    if limit:
        sprayable: int = state.count_group_unique("graffitim", player) * 7
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitim", player):
            return total
        else:
            return 0
        

def spots_m_glitched(state: CollectionState, player: int, limit: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 99
    conditions: Dict[str, int] = {
        "brink_terminal_entrance": 21,
        "chapter3": 3
    }

    for access_name, graffiti_count in conditions.items():
        if access_cache[access_name]:
            total += graffiti_count
        else:
            break

    if limit:
        sprayable: int = state.count_group_unique("graffitim", player) * 7
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitim", player):
            return total
        else:
            return 0
        

def spots_l_glitchless(state: CollectionState, player: int, limit: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 7
    conditions: Dict[str, int] = {
        "inline_skates": 1,
        "versum_hill_entrance": 2,
        "versum_hill_ch1_roadblock": 13,
        "versum_hill_all_challenges": 1,
        "chapter2": 14,
        "versum_hill_oldhead": 2,
        "brink_terminal_entrance": 10,
        "brink_terminal_plaza": 2,
        "brink_terminal_oldhead_underground": 1,
        "brink_terminal_tower": 1,
        "chapter3": 4,
        "brink_terminal_oldhead_dock": 4,
        "millennium_mall_entrance": 3,
        "millennium_mall_big": 8,
        "millennium_mall_theater": 4,
        "chapter4": 5,
        "millennium_mall_oldhead_ceiling": 3,
        "pyramid_island_gate": 4,
        "pyramid_island_upper_half": 5,
        "pyramid_island_crew_battle": 1,
        "chapter5": 1,
        "pyramid_island_oldhead": 2,
        "mataan_smoke_wall": 1,
        "mataan_deep_city": 2,
        "skateboard": 1,
        "mataan_oldhead": 2,
        "mataan_deepest": 7
    }

    for access_name, graffiti_count in conditions.items():
        if access_cache[access_name]:
            total += graffiti_count
        elif not (access_name == "inline_skates" or access_name == "skateboard"):
            break

    if limit:
        sprayable: int = state.count_group_unique("graffitil", player) * 6
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitil", player):
            return total
        else:
            return 0
        

def spots_l_glitched(state: CollectionState, player: int, limit: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 88
    conditions: Dict[str, int] = {
        "brink_terminal_entrance": 18,
        "chapter3": 4,
        "chapter4": 1
    }

    for access_name, graffiti_count in conditions.items():
        if access_cache[access_name]:
            total += graffiti_count
        else:
            break

    if limit:
        sprayable: int = state.count_group_unique("graffitil", player) * 6
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitil", player):
            return total
        else:
            return 0
        

def spots_xl_glitchless(state: CollectionState, player: int, limit: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 3
    conditions: Dict[str, int] = {
        "versum_hill_ch1_roadblock": 6,
        "versum_hill_basketball_court": 1,
        "chapter2": 9,
        "brink_terminal_entrance": 3,
        "brink_terminal_plaza": 1,
        "brink_terminal_oldhead_underground": 1,
        "brink_terminal_tower": 1,
        "chapter3": 3,
        "brink_terminal_oldhead_dock": 2,
        "millennium_mall_entrance": 2,
        "millennium_mall_big": 5,
        "millennium_mall_theater": 5,
        "chapter4": 3,
        "millennium_mall_oldhead_ceiling": 1,
        "pyramid_island_upper_half": 5,
        "pyramid_island_oldhead": 3,
        "mataan_smoke_wall": 2,
        "mataan_deep_city": 2,
        "mataan_oldhead": 2,
        "mataan_deepest": 2
    }

    for access_name, graffiti_count in conditions.items():
        if access_cache[access_name]:
            total += graffiti_count
        else:
            break

    if limit:
        sprayable: int = state.count_group_unique("graffitixl", player) * 4
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitixl", player):
            return total
        else:
            return 0
        

def spots_xl_glitched(state: CollectionState, player: int, limit: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 51
    conditions: Dict[str, int] = {
        "brink_terminal_entrance": 7,
        "chapter3": 3,
        "chapter4": 1
    }

    for access_name, graffiti_count in conditions.items():
        if access_cache[access_name]:
            total += graffiti_count
        else:
            break

    if limit:
        sprayable: int = state.count_group_unique("graffitixl", player) * 4
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitixl", player):
            return total
        else:
            return 0


def build_access_cache(state: CollectionState, player: int, movestyle: int, limit: bool, glitched: bool) -> Dict[str, bool]:
    funcs: Dict[str, tuple] = {
        "versum_hill_entrance": (state, player),
        "versum_hill_ch1_roadblock": (state, player, limit),
        "versum_hill_oldhead": (state, player),
        "versum_hill_all_challenges": (state, player),
        "versum_hill_basketball_court": (state, player),
        "brink_terminal_entrance": (state, player),
        "brink_terminal_oldhead_underground": (state, player),
        "brink_terminal_oldhead_dock": (state, player),
        "brink_terminal_plaza": (state, player),
        "brink_terminal_tower": (state, player),
        "millennium_mall_entrance": (state, player),
        "millennium_mall_switch": (state, player, limit, glitched),
        "millennium_mall_oldhead_ceiling": (state, player, limit),
        "millennium_mall_big": (state, player, limit, glitched),
        "millennium_mall_theater": (state, player, limit),
        "pyramid_island_gate": (state, player),
        "pyramid_island_oldhead": (state, player),
        "pyramid_island_upper_half": (state, player, limit, glitched),
        "pyramid_island_crew_battle": (state, player, limit, glitched),
        "mataan_smoke_wall": (state, player),
        "mataan_deep_city": (state, player, limit, glitched),
        "mataan_oldhead": (state, player),
        "mataan_smoke_wall2": (state, player, limit, glitched),
        "mataan_deepest": (state, player, limit, glitched)
    }

    access_cache: Dict[str, bool] = {
        "skateboard": skateboard(state, player, movestyle),
        "inline_skates": inline_skates(state, player, movestyle),
        "chapter2": current_chapter(state, player, 2),
        "chapter3": current_chapter(state, player, 3),
        "chapter4": current_chapter(state, player, 4),
        "chapter5": current_chapter(state, player, 5)
    }
    
    stop: bool = False
    for fname, fvars in funcs.items():
        if stop:
            access_cache[fname] = False
            continue
        func = globals()[fname]
        access: bool = func(*fvars)
        access_cache[fname] = access
        if not access and "oldhead" not in fname:
            stop = True

    return access_cache


def graffiti_spots(state: CollectionState, player: int, movestyle: int, limit: bool, glitched: bool, spots: int) -> bool:
    access_cache = build_access_cache(state, player, movestyle, limit, glitched)

    total: int = 0

    if glitched:
        total = spots_s_glitched(state, player, limit, access_cache) \
        + spots_m_glitched(state, player, limit, access_cache) \
        + spots_l_glitched(state, player, limit, access_cache) \
        + spots_xl_glitched(state, player, limit, access_cache)
    else:
        total = spots_s_glitchless(state, player, limit, access_cache) \
        + spots_m_glitchless(state, player, limit, access_cache) \
        + spots_l_glitchless(state, player, limit, access_cache) \
        + spots_xl_glitchless(state, player, limit, access_cache)

    return total >= spots


def rep(state: CollectionState, player: int, required: int) -> bool:
    return state.has("rep", player, required)


def rules(brcworld):
    multiworld = brcworld.multiworld
    player = brcworld.player

    movestyle = brcworld.options.starting_movestyle
    limit = brcworld.options.limited_graffiti
    glitched = brcworld.options.logic
    extra = brcworld.options.extra_rep_required
    photos = not brcworld.options.skip_polo_photos

    # entrances
    for e in multiworld.get_region(Stages.BT1, player).entrances:
        set_rule(e, lambda state: brink_terminal_entrance(state, player))

    if not glitched:
        # versum hill
        for e in multiworld.get_region(Stages.VH1, player).entrances:
            set_rule(e, lambda state: versum_hill_entrance(state, player))
        for e in multiworld.get_region(Stages.VH2, player).entrances:
            set_rule(e, lambda state: versum_hill_ch1_roadblock(state, player, limit))
        for e in multiworld.get_region(Stages.VHO, player).entrances:
            set_rule(e, lambda state: versum_hill_oldhead(state, player))
        for e in multiworld.get_region(Stages.VH3, player).entrances:
            set_rule(e, lambda state: versum_hill_all_challenges(state, player))
        for e in multiworld.get_region(Stages.VH4, player).entrances:
            set_rule(e, lambda state: versum_hill_basketball_court(state, player))

        # millennium square
        for e in multiworld.get_region(Stages.MS, player).entrances:
            set_rule(e, lambda state: millennium_square_entrance(state, player))

        # brink terminal
        for e in multiworld.get_region(Stages.BTO1, player).entrances:
            set_rule(e, lambda state: brink_terminal_oldhead_underground(state, player))
        for e in multiworld.get_region(Stages.BTO2, player).entrances:
            set_rule(e, lambda state: brink_terminal_oldhead_dock(state, player))
        for e in multiworld.get_region(Stages.BT2, player).entrances:
            set_rule(e, lambda state: brink_terminal_plaza(state, player))
        for e in multiworld.get_region(Stages.BT3, player).entrances:
            set_rule(e, lambda state: brink_terminal_tower(state, player))

        # millennium mall
        for e in multiworld.get_region(Stages.MM1, player).entrances:
            set_rule(e, lambda state: millennium_mall_entrance(state, player))
        for e in multiworld.get_region(Stages.MMO1, player).entrances:
            set_rule(e, lambda state: millennium_mall_oldhead_ceiling(state, player, limit))
        for e in multiworld.get_region(Stages.MM2, player).entrances:
            set_rule(e, lambda state: millennium_mall_big(state, player, limit, glitched))
        for e in multiworld.get_region(Stages.MMO2, player).entrances:
            set_rule(e, lambda state: millennium_mall_oldhead_race(state, player))
        for e in multiworld.get_region(Stages.MM3, player).entrances:
            set_rule(e, lambda state: millennium_mall_theater(state, player, limit))

        # pyramid island
        for e in multiworld.get_region(Stages.PI1, player).entrances:
            set_rule(e, lambda state: pyramid_island_entrance(state, player))
        for e in multiworld.get_region(Stages.PI2, player).entrances:
            set_rule(e, lambda state: pyramid_island_gate(state, player))
        for e in multiworld.get_region(Stages.PIO, player).entrances:
            set_rule(e, lambda state: pyramid_island_oldhead(state, player))
        for e in multiworld.get_region(Stages.PI3, player).entrances:
            set_rule(e, lambda state: pyramid_island_upper_half(state, player, limit, glitched))
        for e in multiworld.get_region(Stages.PI4, player).entrances:
            set_rule(e, lambda state: pyramid_island_top(state, player))

        # mataan
        for e in multiworld.get_region(Stages.MA1, player).entrances:
            set_rule(e, lambda state: mataan_entrance(state, player))
        for e in multiworld.get_region(Stages.MA2, player).entrances:
            set_rule(e, lambda state: mataan_smoke_wall(state, player))
        for e in multiworld.get_region(Stages.MA3, player).entrances:
            set_rule(e, lambda state: mataan_deep_city(state, player, limit, glitched))
        for e in multiworld.get_region(Stages.MAO, player).entrances:
            set_rule(e, lambda state: mataan_oldhead(state, player))
        for e in multiworld.get_region(Stages.MA4, player).entrances:
            set_rule(e, lambda state: mataan_smoke_wall2(state, player, limit, glitched))
        for e in multiworld.get_region(Stages.MA5, player).entrances:
            set_rule(e, lambda state: mataan_deepest(state, player, limit, glitched))

    # locations
    # hideout
    set_rule(multiworld.get_location("Hideout: BMX garage skateboard", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(multiworld.get_location("Hideout: Unlock phone app", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(multiworld.get_location("Hideout: Vinyl joins the crew", player),
        lambda state: current_chapter(state, player, 4))
    set_rule(multiworld.get_location("Hideout: Solace joins the crew", player),
        lambda state: current_chapter(state, player, 5))
    
    # versum hill
    set_rule(multiworld.get_location("Versum Hill: Wallrunning challenge reward", player),
        lambda state: versum_hill_challenge1(state, player))
    set_rule(multiworld.get_location("Versum Hill: Manual challenge reward", player),
        lambda state: versum_hill_challenge2(state, player))
    set_rule(multiworld.get_location("Versum Hill: Corner challenge reward", player),
        lambda state: versum_hill_challenge3(state, player))
    set_rule(multiworld.get_location("Versum Hill: BMX gate outfit", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(multiworld.get_location("Versum Hill: Glass floor skates", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(multiworld.get_location("Versum Hill: Basketball court shortcut CD", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(multiworld.get_location("Versum Hill: Rave joins the crew", player),
        lambda state: versum_hill_rave(state, player, limit, glitched))
    set_rule(multiworld.get_location("Versum Hill: Frank joins the crew", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(multiworld.get_location("Versum Hill: Rietveld joins the crew", player),
        lambda state: versum_hill_rietveld(state, player, limit, glitched))
    if photos:
        set_rule(multiworld.get_location("Versum Hill: Big Polo", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Versum Hill: Trash Polo", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Versum Hill: Fruit stand Polo", player),
            lambda state: camera(state, player))
    
    # millennium square
    if photos:
        set_rule(multiworld.get_location("Millennium Square: Half pipe Polo", player),
            lambda state: camera(state, player))
    
    # brink terminal
    set_rule(multiworld.get_location("Brink Terminal: Upside grind challenge reward", player),
        lambda state: brink_terminal_challenge1(state, player))
    set_rule(multiworld.get_location("Brink Terminal: Manual challenge reward", player),
        lambda state: brink_terminal_challenge2(state, player))
    set_rule(multiworld.get_location("Brink Terminal: Score challenge reward", player),
        lambda state: brink_terminal_challenge3(state, player))
    set_rule(multiworld.get_location("Brink Terminal: BMX gate graffiti", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(multiworld.get_location("Brink Terminal: Mesh's skateboard", player),
        lambda state: brink_terminal_mesh(state, player, limit, glitched))
    set_rule(multiworld.get_location("Brink Terminal: Rooftop glass CD", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(multiworld.get_location("Brink Terminal: Mesh joins the crew", player),
        lambda state: brink_terminal_mesh(state, player, limit, glitched))
    set_rule(multiworld.get_location("Brink Terminal: Eclipse joins the crew", player),
        lambda state: current_chapter(state, player, 3))
    if photos:
        set_rule(multiworld.get_location("Brink Terminal: Behind glass Polo", player),
            lambda state: camera(state, player))
    
    # millennium mall
    set_rule(multiworld.get_location("Millennium Mall: Glass cylinder CD", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(multiworld.get_location("Millennium Mall: Trick challenge reward", player),
        lambda state: millennium_mall_challenge1(state, player))
    set_rule(multiworld.get_location("Millennium Mall: Slide challenge reward", player),
        lambda state: millennium_mall_challenge2(state, player))
    set_rule(multiworld.get_location("Millennium Mall: Fish challenge reward", player),
        lambda state: millennium_mall_challenge3(state, player))
    set_rule(multiworld.get_location("Millennium Mall: Score challenge reward", player),
        lambda state: millennium_mall_challenge4(state, player))
    set_rule(multiworld.get_location("Millennium Mall: Atrium BMX gate BMX", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(multiworld.get_location("Millennium Mall: Shine joins the crew", player),
        lambda state: current_chapter(state, player, 4))
    set_rule(multiworld.get_location("Millennium Mall: DOT.EXE joins the crew", player),
        lambda state: current_chapter(state, player, 4))
    
    # pyramid island
    set_rule(multiworld.get_location("Pyramid Island: BMX gate BMX", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(multiworld.get_location("Pyramid Island: Score challenge reward", player),
        lambda state: pyramid_island_challenge1(state, player))
    set_rule(multiworld.get_location("Pyramid Island: Score challenge 2 reward", player),
        lambda state: pyramid_island_challenge2(state, player))
    set_rule(multiworld.get_location("Pyramid Island: Quarter pipe challenge reward", player),
        lambda state: pyramid_island_challenge3(state, player))
    set_rule(multiworld.get_location("Pyramid Island: Shortcut glass CD", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(multiworld.get_location("Pyramid Island: Maze outfit", player),
        lambda state: skateboard(state, player, movestyle))
    if not glitched:
        add_rule(multiworld.get_location("Pyramid Island: Rise joins the crew", player),
            lambda state: camera(state, player))
    set_rule(multiworld.get_location("Pyramid Island: Devil Theory joins the crew", player),
        lambda state: current_chapter(state, player, 5))
    if photos:
        set_rule(multiworld.get_location("Pyramid Island: Polo pile 1", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Polo pile 2", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Polo pile 3", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Polo pile 4", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Maze glass Polo", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Maze classroom Polo", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Maze vent Polo", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Big maze Polo", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Maze desk Polo", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Pyramid Island: Maze forklift Polo", player),
            lambda state: camera(state, player))

    # mataan
    set_rule(multiworld.get_location("Mataan: Race challenge reward", player),
        lambda state: mataan_challenge1(state, player, limit, glitched))
    set_rule(multiworld.get_location("Mataan: Wallrunning challenge reward", player),
        lambda state: mataan_challenge2(state, player, limit, glitched))
    set_rule(multiworld.get_location("Mataan: Score challenge reward", player),
        lambda state: mataan_challenge3(state, player))
    set_rule(multiworld.get_location("Mataan: Coil joins the crew", player),
        lambda state: mataan_deepest(state, player, limit, glitched))
    if photos:
        set_rule(multiworld.get_location("Mataan: Trash Polo", player),
            lambda state: camera(state, player))
        set_rule(multiworld.get_location("Mataan: Shopping Polo", player),
            lambda state: camera(state, player))

    # events
    set_rule(multiworld.get_location("Versum Hill: Complete Chapter 1", player),
        lambda state: versum_hill_crew_battle(state, player, limit, glitched))
    set_rule(multiworld.get_location("Brink Terminal: Complete Chapter 2", player),
        lambda state: brink_terminal_crew_battle(state, player, limit, glitched))
    set_rule(multiworld.get_location("Millennium Mall: Complete Chapter 3", player),
        lambda state: millennium_mall_crew_battle(state, player, limit, glitched))
    set_rule(multiworld.get_location("Pyramid Island: Complete Chapter 4", player),
        lambda state: pyramid_island_crew_battle(state, player, limit, glitched))
    set_rule(multiworld.get_location("Defeat Faux", player),
        lambda state: mataan_faux(state, player, limit, glitched))
    
    if extra:
        add_rule(multiworld.get_location("Defeat Faux", player),
            lambda state: rep(state, player, 1000))

    # graffiti spots
    spots: int = 0
    while spots < 385:
        spots += 5
        set_rule(multiworld.get_location(f"Tagged {spots} Graffiti Spots", player),
            lambda state, spot_count=spots: graffiti_spots(state, player, movestyle, limit, glitched, spot_count))

    set_rule(multiworld.get_location("Tagged 389 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 389))
