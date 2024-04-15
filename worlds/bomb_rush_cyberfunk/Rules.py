from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState
from typing import Dict
from .Regions import Stages


def graffitiM(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group("graffitim", player) * 7 >= spots if limit else state.has_group("graffitim", player)


def graffitiL(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group("graffitil", player) * 6 >= spots if limit else state.has_group("graffitil", player)


def graffitiXL(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group("graffitixl", player) * 4 >= spots if limit else state.has_group("graffitixl", player)


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


def millennium_mall_all_challenges(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return millennium_mall_challenge4(state, player, limit, glitched)


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
        return graffitiM(state, player, limit, 114)
    else:
        return graffitiM(state, player, limit, 88)


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


def spots_s(state: CollectionState, player: int, limit: bool, glitched: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 0

    if glitched:
        total += 75

        if access_cache["brink_terminal_entrance"]:
            total += 13

        if access_cache["chapter3"]:
            total += 6

    else:
        # chapter 1
        # hideout
        total += 10

        # versum hill area 1
        if access_cache["versum_hill_entrance"]:
            total += 1

            # versum hill area 2
            if access_cache["versum_hill_ch1_roadblock"]:
                total += 11

                # versum hill OldHeadArea
                if access_cache["versum_hill_oldhead"]:
                    total += 1

                # versum hill area 4
                if access_cache["versum_hill_basketball_court"]:

                    # chapter 2
                    # millennium square + mataan
                    if access_cache["chapter2"]:
                        # 7 in square, 5 in mataan
                        total += 12
                        
                        # brink terminal area 1
                        if access_cache["brink_terminal_entrance"]:
                            total += 9

                            # brink terminal dock OldHeadArea
                            if access_cache["brink_terminal_oldhead_dock"]:
                                total += 1

                            # brink terminal tower area
                            if access_cache["brink_terminal_plaza"]:
                                total += 3

                                # brink terminal inside tower
                                if access_cache["brink_terminal_tower"]:

                                    # chapter 3
                                    # millennium square 2
                                    if access_cache["chapter3"]:
                                        total += 6

                                        # millennium mall area 1
                                        if access_cache["millennium_mall_entrance"]:
                                            total += 3

                                            # millennium mall area 2
                                            if access_cache["millennium_mall_switch"]:
                                                total += 4

                                                # millennium mall area 3
                                                if access_cache["millennium_mall_theater"]:
                                                    total += 3

                                                    # chapter 4
                                                    # pyramid island area 1
                                                    if access_cache["chapter4"]:
                                                        # 2 in pyramid
                                                        total += 2

                                                        # pyramid island area 2
                                                        if access_cache["pyramid_island_gate"]:
                                                            total += 5

                                                            # pyramid island OldHeadArea
                                                            if access_cache["pyramid_island_oldhead"]:
                                                                total += 2

                                                            # pyramid island area 3
                                                            if access_cache["pyramid_island_upper_half"]:
                                                                total += 8

                                                                # pyramid island area 4
                                                                if access_cache["pyramid_island_crew_battle"]:

                                                                    # chapter 5
                                                                    # pyramid island 2
                                                                    if access_cache["chapter5"]:

                                                                        # mataan area 2
                                                                        if access_cache["mataan_smoke_wall"]:
                                                                            total += 3

                                                                            # mataan area 3
                                                                            if access_cache["mataan_deep_city"]:
                                                                                total += 5

                                                                                # mataan OldHeadArea
                                                                                if access_cache["mataan_oldhead"]:
                                                                                    total += 3

                                                                                    if access_cache["mataan_deepest"]:
                                                                                        total += 2

    if limit:
        sprayable: int = 5 + (state.count_group("characters", player) * 5)
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        return total


def spots_m(state: CollectionState, player: int, limit: bool, glitched: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 0

    if glitched:
        total += 99

        if access_cache["brink_terminal_entrance"]:
            total += 21

        if access_cache["chapter3"]:
            total += 3
        
    else:
        # chapter 1
        # hideout
        total += 4

        # versum hill area 1
        if access_cache["versum_hill_entrance"]:
            total += 3

            # versum hill area 2
            if access_cache["versum_hill_ch1_roadblock"]:
                total += 13

                # versum hill OldHeadArea
                if access_cache["versum_hill_oldhead"]:
                    total += 4

                # versum hill area 3
                if access_cache["versum_hill_all_challenges"]:
                    total += 3

                # versum hill area 4
                if access_cache["versum_hill_basketball_court"]:

                    # chapter 2
                    # millennium square + mataan
                    if access_cache["chapter2"]:
                        # 12 in square, 4 in mataan
                        total += 16
                        
                        # brink terminal area 1
                        if access_cache["brink_terminal_entrance"]:
                            total += 13

                            # brink terminal dock OldHeadArea
                            if access_cache["brink_terminal_oldhead_dock"]:
                                total += 4

                            # brink terminal tower area
                            if access_cache["brink_terminal_plaza"]:
                                total += 4

                                # brink terminal inside tower
                                if access_cache["brink_terminal_tower"]:

                                    # chapter 3
                                    # millennium square 2
                                    if access_cache["chapter3"]:
                                        total += 3

                                        # millennium mall area 1
                                        if access_cache["millennium_mall_entrance"]:
                                            total += 5

                                            # millennium mall OldHeadArea
                                            if access_cache["millennium_mall_oldhead_ceiling"]:
                                                total += 1

                                            # millennium mall area 2
                                            if access_cache["millennium_mall_big"]:
                                                total += 6

                                                # millennium mall area 3
                                                if access_cache["millennium_mall_theater"]:
                                                    total += 4

                                                    # chapter 4
                                                    # pyramid island area 1
                                                    if access_cache["chapter4"]:
                                                        # 2 in pyramid
                                                        total += 2

                                                        # pyramid island area 2
                                                        if access_cache["pyramid_island_gate"]:
                                                            total += 3

                                                            # pyramid island OldHeadArea
                                                            if access_cache["pyramid_island_oldhead"]:
                                                                total += 5

                                                            # pyramid island area 3
                                                            if access_cache["pyramid_island_upper_half"]:
                                                                total += 8

                                                                # pyramid island area 4
                                                                if access_cache["pyramid_island_crew_battle"]:

                                                                    # chapter 5
                                                                    # pyramid island 2
                                                                    if access_cache["chapter5"]:
                                                                        total += 2

                                                                        # mataan area 2
                                                                        if access_cache["mataan_smoke_wall"]:

                                                                            # mataan area 3
                                                                            if access_cache["mataan_deep_city"]:
                                                                                total += 7

                                                                                # center island
                                                                                if access_cache["skateboard"]:
                                                                                    total += 1

                                                                                # mataan OldHeadArea
                                                                                if access_cache["mataan_oldhead"]:
                                                                                    total += 1

                                                                                    # mataan area 4
                                                                                    if access_cache["mataan_smoke_wall2"]:
                                                                                        total += 1

                                                                                        if access_cache["mataan_deepest"]:
                                                                                            total += 10

    if limit:
        sprayable: int = state.count_group("graffitim", player) * 7
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitim", player):
            return total
        else:
            return 0
        

def spots_l(state: CollectionState, player: int, limit: bool, glitched: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 0

    if glitched:
        total += 90

        if access_cache["brink_terminal_entrance"]:
            total += 18

        if access_cache["chapter3"]:
            total += 4

        if access_cache["chapter4"]:
            total += 1

    else:
        # chapter 1
        # hideout
        total += 7

        if access_cache["inline_skates"]:
            total += 1

        # versum hill area 1
        if access_cache["versum_hill_entrance"]:
            total += 2

            # versum hill area 2
            if access_cache["versum_hill_ch1_roadblock"]:
                total += 13

                # versum hill OldHeadArea
                if access_cache["versum_hill_oldhead"]:
                    total += 2

                # versum hill area 3
                if access_cache["versum_hill_all_challenges"]:
                    total += 1

                # versum hill area 4
                if access_cache["versum_hill_basketball_court"]:

                    # chapter 2
                    # millennium square + mataan
                    if access_cache["chapter2"]:
                        # 7 in square, 7 in mataan
                        total += 14
                        
                        # brink terminal area 1
                        if access_cache["brink_terminal_entrance"]:
                            total += 10

                            # brink terminal underground OldHeadArea
                            if access_cache["brink_terminal_oldhead_underground"]:
                                total += 1

                            # brink terminal dock OldHeadArea
                            if access_cache["brink_terminal_oldhead_dock"]:
                                total += 4

                            # brink terminal tower area
                            if access_cache["brink_terminal_plaza"]:
                                total += 2

                                # brink terminal inside tower
                                if access_cache["brink_terminal_tower"]:
                                    total += 1

                                    # chapter 3
                                    # millennium square 2
                                    if access_cache["chapter3"]:
                                        total += 4

                                        # millennium mall area 1
                                        if access_cache["millennium_mall_entrance"]:
                                            total += 3
                                            
                                            # millennium mall OldHeadArea
                                            if access_cache["millennium_mall_oldhead_ceiling"]:
                                                total += 3

                                            # millennium mall area 2
                                            if access_cache["millennium_mall_big"]:
                                                total += 8

                                                # millennium mall area 3
                                                if access_cache["millennium_mall_theater"]:
                                                    total += 4

                                                    # chapter 4
                                                    # pyramid island area 1
                                                    if access_cache["chapter4"]:
                                                        # 1 in square, 4 in pyramid
                                                        total += 5

                                                        # pyramid island area 2
                                                        if access_cache["pyramid_island_gate"]:
                                                            total += 4

                                                            # pyramid island OldHeadArea
                                                            if access_cache["pyramid_island_oldhead"]:
                                                                total += 2

                                                            # pyramid island area 3
                                                            if access_cache["pyramid_island_upper_half"]:
                                                                total += 5

                                                                # pyramid island area 4
                                                                if access_cache["pyramid_island_crew_battle"]:
                                                                    total += 1

                                                                    # chapter 5
                                                                    # pyramid island 2
                                                                    if access_cache["chapter5"]:
                                                                        total += 1

                                                                        # mataan area 2
                                                                        if access_cache["mataan_smoke_wall"]:
                                                                            total += 1

                                                                            # mataan area 3
                                                                            if access_cache["mataan_deep_city"]:
                                                                                total += 2

                                                                                # center island
                                                                                if access_cache["skateboard"]:
                                                                                    total += 1

                                                                                # mataan OldHeadArea
                                                                                if access_cache["mataan_oldhead"]:
                                                                                    total += 2

                                                                                    # mataan area 4
                                                                                    if access_cache["mataan_smoke_wall2"]:
                                                                                        total += 2

                                                                                        # mataan area 4 part 2 + area 5
                                                                                        if access_cache["mataan_deepest"]:
                                                                                            total += 7

    if limit:
        sprayable: int = state.count_group("graffitil", player) * 6
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitil", player):
            return total
        else:
            return 0
        

def spots_xl(state: CollectionState, player: int, limit: bool, glitched: bool, access_cache: Dict[str, bool]) -> int:
    total: int = 0

    if glitched:
        total += 50

        if access_cache["brink_terminal_entrance"]:
            total += 7

            if access_cache["chapter4"]:
                total += 1

        if access_cache["chapter3"]:
            total += 3

    else:
        # chapter 1
        # hideout
        total += 3

        # versum hill area 1
        if access_cache["versum_hill_entrance"]:

            # versum hill area 2
            if access_cache["versum_hill_ch1_roadblock"]:
                total += 6

                # versum hill area 4
                if access_cache["versum_hill_basketball_court"]:
                    total += 1

                    # chapter 2
                    # millennium square + mataan
                    if access_cache["chapter2"]:
                        # 4 in square, 5 in mataan
                        total += 9
                        
                        # brink terminal area 1
                        if access_cache["brink_terminal_entrance"]:
                            total += 3

                            # brink terminal underground OldHeadArea
                            if access_cache["brink_terminal_oldhead_underground"]:
                                total += 1

                            # brink terminal dock OldHeadArea
                            if access_cache["brink_terminal_oldhead_dock"]:
                                total += 2

                            # brink terminal tower area
                            if access_cache["brink_terminal_plaza"]:
                                total += 1

                                # brink terminal inside tower
                                if access_cache["brink_terminal_tower"]:
                                    total += 1

                                    # chapter 3
                                    # millennium square 2
                                    if access_cache["chapter3"]:
                                        total += 3

                                        # millennium mall area 1
                                        if access_cache["millennium_mall_entrance"]:
                                            total += 2

                                            # millennium mall OldHeadArea
                                            if access_cache["millennium_mall_oldhead_ceiling"]:
                                                total += 1

                                            # millennium mall area 2
                                            if access_cache["millennium_mall_big"]:
                                                total += 5

                                                # millennium mall area 3
                                                if access_cache["millennium_mall_theater"]:
                                                    total += 5

                                                    # chapter 4
                                                    # pyramid island area 1
                                                    if access_cache["chapter4"]:
                                                        # 1 in terminal, 2 in pyramid
                                                        total += 3

                                                        # pyramid island area 2
                                                        if access_cache["pyramid_island_gate"]:

                                                            # pyramid island OldHeadArea
                                                            if access_cache["pyramid_island_oldhead"]:
                                                                total += 3

                                                            # pyramid island area 3
                                                            if access_cache["pyramid_island_upper_half"]:
                                                                total += 5

                                                                # pyramid island area 4
                                                                if access_cache["pyramid_island_crew_battle"]:

                                                                    # chapter 5
                                                                    # pyramid island 2
                                                                    if access_cache["chapter5"]:

                                                                        # mataan area 2
                                                                        if access_cache["mataan_smoke_wall"]:
                                                                            total += 2

                                                                            # mataan area 3
                                                                            if access_cache["mataan_deep_city"]:
                                                                                total += 2

                                                                                # mataan OldHeadArea
                                                                                if access_cache["mataan_oldhead"]:
                                                                                    total += 2

                                                                                    if access_cache["mataan_deepest"]:
                                                                                        total += 2

    if limit:
        sprayable: int = state.count_group("graffitixl", player) * 4
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitixl", player):
            return total
        else:
            return 0


def graffiti_spots(state: CollectionState, player: int, movestyle: int, limit: int, glitched: bool, spots: int) -> bool:
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
        if not access and not "oldhead" in fname:
            stop = True

    total: int = spots_s(state, player, limit, glitched, access_cache) \
        + spots_m(state, player, limit, glitched, access_cache) \
        + spots_l(state, player, limit, glitched, access_cache) \
        + spots_xl(state, player, limit, glitched, access_cache)

    return total >= spots


def rep(state: CollectionState, player: int, required: int) -> bool:
    return state.has("rep", player, required)


def rules(brcworld):
    world = brcworld.multiworld
    player = brcworld.player

    movestyle = brcworld.options.starting_movestyle
    limit = brcworld.options.limited_graffiti
    glitched = brcworld.options.logic
    extra = brcworld.options.extra_rep_required
    photos = not brcworld.options.skip_polo_photos

    # entrances
    for e in world.get_region(Stages.BT1, player).entrances:
        set_rule(e, lambda state: brink_terminal_entrance(state, player))

    if not glitched:
        # versum hill
        for e in world.get_region(Stages.VH1, player).entrances:
            set_rule(e, lambda state: versum_hill_entrance(state, player))
        for e in world.get_region(Stages.VH2, player).entrances:
            set_rule(e, lambda state: versum_hill_ch1_roadblock(state, player, limit))
        for e in world.get_region(Stages.VHO, player).entrances:
            set_rule(e, lambda state: versum_hill_oldhead(state, player))
        for e in world.get_region(Stages.VH3, player).entrances:
            set_rule(e, lambda state: versum_hill_all_challenges(state, player))
        for e in world.get_region(Stages.VH4, player).entrances:
            set_rule(e, lambda state: versum_hill_basketball_court(state, player))

        # millennium square
        for e in world.get_region(Stages.MS, player).entrances:
            set_rule(e, lambda state: millennium_square_entrance(state, player))

        # brink terminal
        for e in world.get_region(Stages.BTO1, player).entrances:
            set_rule(e, lambda state: brink_terminal_oldhead_underground(state, player))
        for e in world.get_region(Stages.BTO2, player).entrances:
            set_rule(e, lambda state: brink_terminal_oldhead_dock(state, player))
        for e in world.get_region(Stages.BT2, player).entrances:
            set_rule(e, lambda state: brink_terminal_plaza(state, player))
        for e in world.get_region(Stages.BT3, player).entrances:
            set_rule(e, lambda state: brink_terminal_tower(state, player))

        # millennium mall
        for e in world.get_region(Stages.MM1, player).entrances:
            set_rule(e, lambda state: millennium_mall_entrance(state, player))
        for e in world.get_region(Stages.MMO1, player).entrances:
            set_rule(e, lambda state: millennium_mall_oldhead_ceiling(state, player, limit))
        for e in world.get_region(Stages.MM2, player).entrances:
            set_rule(e, lambda state: millennium_mall_big(state, player, limit, glitched))
        for e in world.get_region(Stages.MMO2, player).entrances:
            set_rule(e, lambda state: millennium_mall_oldhead_race(state, player))
        for e in world.get_region(Stages.MM3, player).entrances:
            set_rule(e, lambda state: millennium_mall_theater(state, player, limit))

        # pyramid island
        for e in world.get_region(Stages.PI1, player).entrances:
            set_rule(e, lambda state: pyramid_island_entrance(state, player))
        for e in world.get_region(Stages.PI2, player).entrances:
            set_rule(e, lambda state: pyramid_island_gate(state, player))
        for e in world.get_region(Stages.PIO, player).entrances:
            set_rule(e, lambda state: pyramid_island_oldhead(state, player))
        for e in world.get_region(Stages.PI3, player).entrances:
            set_rule(e, lambda state: pyramid_island_all_challenges(state, player, limit, glitched))
        for e in world.get_region(Stages.PI4, player).entrances:
            set_rule(e, lambda state: pyramid_island_top(state, player))

        # mataan
        for e in world.get_region(Stages.MA1, player).entrances:
            set_rule(e, lambda state: mataan_entrance(state, player))
        for e in world.get_region(Stages.MA2, player).entrances:
            set_rule(e, lambda state: mataan_smoke_wall(state, player))
        for e in world.get_region(Stages.MA3, player).entrances:
            set_rule(e, lambda state: mataan_deep_city(state, player, limit, glitched))
        for e in world.get_region(Stages.MAO, player).entrances:
            set_rule(e, lambda state: mataan_oldhead(state, player))
        for e in world.get_region(Stages.MA4, player).entrances:
            set_rule(e, lambda state: mataan_smoke_wall2(state, player, limit, glitched))
        for e in world.get_region(Stages.MA5, player).entrances:
            set_rule(e, lambda state: mataan_deepest(state, player, limit, glitched))

    """
    for e in world.get_region("Versum Hill", player).entrances:
        set_rule(e, lambda state: versum_hill_entrance(state, player, glitched))
    for e in world.get_region("Millennium Square", player).entrances:
        set_rule(e, lambda state: millennium_square_entrance(state, player, glitched))
    for e in world.get_region("Brink Terminal", player).entrances:
        set_rule(e, lambda state: brink_terminal_entrance(state, player))
    for e in world.get_region("Millennium Mall", player).entrances:
        set_rule(e, lambda state: millennium_mall_entrance(state, player, glitched))
    for e in world.get_region("Pyramid Island", player).entrances:
        set_rule(e, lambda state: pyramid_island_entrance(state, player, glitched))
    for e in world.get_region("Mataan", player).entrances:
        set_rule(e, lambda state: mataan_entrance(state, player, glitched))
    """

    # locations
    # hideout
    set_rule(world.get_location("Hideout: BMX garage skateboard", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(world.get_location("Hideout: Unlock phone app", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(world.get_location("Hideout: Vinyl joins the crew", player),
        lambda state: current_chapter(state, player, 4))
    set_rule(world.get_location("Hideout: Solace joins the crew", player),
        lambda state: current_chapter(state, player, 5))
    
    # versum hill
    set_rule(world.get_location("Versum Hill: Wallrunning challenge reward", player),
        lambda state: versum_hill_challenge1(state, player))
    set_rule(world.get_location("Versum Hill: Manual challenge reward", player),
        lambda state: versum_hill_challenge2(state, player))
    set_rule(world.get_location("Versum Hill: Corner challenge reward", player),
        lambda state: versum_hill_challenge3(state, player))
    set_rule(world.get_location("Versum Hill: BMX gate outfit", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(world.get_location("Versum Hill: Glass floor skates", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(world.get_location("Versum Hill: Basketball court shortcut CD", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(world.get_location("Versum Hill: Rave joins the crew", player),
        lambda state: versum_hill_rave(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Frank joins the crew", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(world.get_location("Versum Hill: Rietveld joins the crew", player),
        lambda state: current_chapter(state, player, 2))
    if photos:
        set_rule(world.get_location("Versum Hill: Big Polo", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Versum Hill: Trash Polo", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Versum Hill: Fruit stand Polo", player),
            lambda state: camera(state, player))
    
    # millennium square
    if photos:
        set_rule(world.get_location("Millennium Square: Half pipe Polo", player),
            lambda state: camera(state, player))
    
    # brink terminal
    set_rule(world.get_location("Brink Terminal: Upside grind challenge reward", player),
        lambda state: brink_terminal_challenge1(state, player))
    set_rule(world.get_location("Brink Terminal: Manual challenge reward", player),
        lambda state: brink_terminal_challenge2(state, player))
    set_rule(world.get_location("Brink Terminal: Score challenge reward", player),
        lambda state: brink_terminal_challenge3(state, player))
    set_rule(world.get_location("Brink Terminal: BMX gate graffiti", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(world.get_location("Brink Terminal: Mesh's skateboard", player),
        lambda state: brink_terminal_mesh(state, player, limit, glitched))
    set_rule(world.get_location("Brink Terminal: Rooftop glass CD", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(world.get_location("Brink Terminal: Mesh joins the crew", player),
        lambda state: brink_terminal_mesh(state, player, limit, glitched))
    set_rule(world.get_location("Brink Terminal: Eclipse joins the crew", player),
        lambda state: current_chapter(state, player, 3))
    if photos:
        set_rule(world.get_location("Brink Terminal: Behind glass Polo", player),
            lambda state: camera(state, player))
    
    # millennium mall
    set_rule(world.get_location("Millennium Mall: Glass cylinder CD", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(world.get_location("Millennium Mall: Trick challenge reward", player),
        lambda state: millennium_mall_challenge1(state, player))
    set_rule(world.get_location("Millennium Mall: Slide challenge reward", player),
        lambda state: millennium_mall_challenge2(state, player))
    set_rule(world.get_location("Millennium Mall: Fish challenge reward", player),
        lambda state: millennium_mall_challenge3(state, player))
    set_rule(world.get_location("Millennium Mall: Score challenge reward", player),
        lambda state: millennium_mall_challenge4(state, player))
    set_rule(world.get_location("Millennium Mall: Atrium BMX gate BMX", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(world.get_location("Millennium Mall: Shine joins the crew", player),
        lambda state: current_chapter(state, player, 4))
    set_rule(world.get_location("Millennium Mall: DOT.EXE joins the crew", player),
        lambda state: current_chapter(state, player, 4))
    
    # pyramid island
    set_rule(world.get_location("Pyramid Island: BMX gate BMX", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(world.get_location("Pyramid Island: Score challenge reward", player),
        lambda state: pyramid_island_challenge1(state, player))
    set_rule(world.get_location("Pyramid Island: Score challenge 2 reward", player),
        lambda state: pyramid_island_challenge2(state, player))
    set_rule(world.get_location("Pyramid Island: Quarter pipe challenge reward", player),
        lambda state: pyramid_island_challenge3(state, player))
    set_rule(world.get_location("Pyramid Island: Shortcut glass CD", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(world.get_location("Pyramid Island: Maze outfit", player),
        lambda state: skateboard(state, player, movestyle))
    if not glitched:
        add_rule(world.get_location("Pyramid Island: Rise joins the crew", player),
            lambda state: camera(state, player))
    set_rule(world.get_location("Pyramid Island: Devil Theory joins the crew", player),
        lambda state: current_chapter(state, player, 5))
    if photos:
        set_rule(world.get_location("Pyramid Island: Polo pile 1", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Polo pile 2", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Polo pile 3", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Polo pile 4", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Maze glass Polo", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Maze classroom Polo", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Maze vent Polo", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Big maze Polo", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Maze desk Polo", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Pyramid Island: Maze forklift Polo", player),
            lambda state: camera(state, player))

    # mataan
    set_rule(world.get_location("Mataan: Race challenge reward", player),
        lambda state: mataan_challenge1(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Wallrunning challenge reward", player),
        lambda state: mataan_challenge2(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Score challenge reward", player),
        lambda state: mataan_challenge3(state, player))
    if photos:
        set_rule(world.get_location("Mataan: Trash Polo", player),
            lambda state: camera(state, player))
        set_rule(world.get_location("Mataan: Shopping Polo", player),
            lambda state: camera(state, player))

    # events
    set_rule(world.get_location("Versum Hill: Complete Chapter 1", player),
        lambda state: versum_hill_crew_battle(state, player, limit, glitched))
    set_rule(world.get_location("Brink Terminal: Complete Chapter 2", player),
        lambda state: brink_terminal_crew_battle(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Complete Chapter 3", player),
        lambda state: millennium_mall_crew_battle(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Complete Chapter 4", player),
        lambda state: pyramid_island_crew_battle(state, player, limit, glitched))
    set_rule(world.get_location("Defeat Faux", player),
        lambda state: mataan_faux(state, player, limit, glitched))
    
    if extra:
        add_rule(world.get_location("Defeat Faux", player),
            lambda state: rep(state, player, 1000))

    # graffiti spots
    set_rule(world.get_location("Tagged 5 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 5))
    set_rule(world.get_location("Tagged 10 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 10))
    set_rule(world.get_location("Tagged 15 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 15))
    set_rule(world.get_location("Tagged 20 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 20))
    set_rule(world.get_location("Tagged 25 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 25))
    set_rule(world.get_location("Tagged 30 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 30))
    set_rule(world.get_location("Tagged 35 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 35))
    set_rule(world.get_location("Tagged 40 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 40))
    set_rule(world.get_location("Tagged 45 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 45))
    set_rule(world.get_location("Tagged 50 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 50))
    set_rule(world.get_location("Tagged 55 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 55))
    set_rule(world.get_location("Tagged 60 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 60))
    set_rule(world.get_location("Tagged 65 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 65))
    set_rule(world.get_location("Tagged 70 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 70))
    set_rule(world.get_location("Tagged 75 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 75))
    set_rule(world.get_location("Tagged 80 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 80))
    set_rule(world.get_location("Tagged 85 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 85))
    set_rule(world.get_location("Tagged 90 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 90))
    set_rule(world.get_location("Tagged 95 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 95))
    set_rule(world.get_location("Tagged 100 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 100))
    set_rule(world.get_location("Tagged 105 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 105))
    set_rule(world.get_location("Tagged 110 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 110))
    set_rule(world.get_location("Tagged 115 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 115))
    set_rule(world.get_location("Tagged 120 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 120))
    set_rule(world.get_location("Tagged 125 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 125))
    set_rule(world.get_location("Tagged 130 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 130))
    set_rule(world.get_location("Tagged 135 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 135))
    set_rule(world.get_location("Tagged 140 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 140))
    set_rule(world.get_location("Tagged 145 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 145))
    set_rule(world.get_location("Tagged 150 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 150))
    set_rule(world.get_location("Tagged 155 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 155))
    set_rule(world.get_location("Tagged 160 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 160))
    set_rule(world.get_location("Tagged 165 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 165))
    set_rule(world.get_location("Tagged 170 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 170))
    set_rule(world.get_location("Tagged 175 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 175))
    set_rule(world.get_location("Tagged 180 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 180))
    set_rule(world.get_location("Tagged 185 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 185))
    set_rule(world.get_location("Tagged 190 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 190))
    set_rule(world.get_location("Tagged 195 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 195))
    set_rule(world.get_location("Tagged 200 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 200))
    set_rule(world.get_location("Tagged 205 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 205))
    set_rule(world.get_location("Tagged 210 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 210))
    set_rule(world.get_location("Tagged 215 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 215))
    set_rule(world.get_location("Tagged 220 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 220))
    set_rule(world.get_location("Tagged 225 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 225))
    set_rule(world.get_location("Tagged 230 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 230))
    set_rule(world.get_location("Tagged 235 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 235))
    set_rule(world.get_location("Tagged 240 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 240))
    set_rule(world.get_location("Tagged 245 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 245))
    set_rule(world.get_location("Tagged 250 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 250))
    set_rule(world.get_location("Tagged 255 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 255))
    set_rule(world.get_location("Tagged 260 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 260))
    set_rule(world.get_location("Tagged 265 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 265))
    set_rule(world.get_location("Tagged 270 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 270))
    set_rule(world.get_location("Tagged 275 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 275))
    set_rule(world.get_location("Tagged 280 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 280))
    set_rule(world.get_location("Tagged 285 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 285))
    set_rule(world.get_location("Tagged 290 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 290))
    set_rule(world.get_location("Tagged 295 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 295))
    set_rule(world.get_location("Tagged 300 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 300))
    set_rule(world.get_location("Tagged 305 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 305))
    set_rule(world.get_location("Tagged 310 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 310))
    set_rule(world.get_location("Tagged 315 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 315))
    set_rule(world.get_location("Tagged 320 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 320))
    set_rule(world.get_location("Tagged 325 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 325))
    set_rule(world.get_location("Tagged 330 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 300))
    set_rule(world.get_location("Tagged 335 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 335))
    set_rule(world.get_location("Tagged 340 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 340))
    set_rule(world.get_location("Tagged 345 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 345))
    set_rule(world.get_location("Tagged 350 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 350))
    set_rule(world.get_location("Tagged 355 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 355))
    set_rule(world.get_location("Tagged 360 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 360))
    set_rule(world.get_location("Tagged 365 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 365))
    set_rule(world.get_location("Tagged 370 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 370))
    set_rule(world.get_location("Tagged 375 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 375))
    set_rule(world.get_location("Tagged 380 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 380))
    set_rule(world.get_location("Tagged 385 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 385))
    set_rule(world.get_location("Tagged 389 Graffiti Spots", player),
        lambda state: graffiti_spots(state, player, movestyle, limit, glitched, 389))
    
    