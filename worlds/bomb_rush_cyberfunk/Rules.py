from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState


def graffitiM(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group("graffitim", player) * 9 >= spots if limit else state.has_group("graffitim", player)


def graffitiL(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group("graffitil", player) * 8 >= spots if limit else state.has_group("graffitil", player)


def graffitiXL(state: CollectionState, player: int, limit: bool, spots: int) -> bool:
    return state.count_group("graffitixl", player) * 6 >= spots if limit else state.has_group("graffitixl", player)


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
    

def hideout_tutorial(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return rep(state, player, 20)
    

def versum_hill_entrance(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return hideout_tutorial(state, player, glitched)
    

def versum_hill_ch1_roadblock(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        if brink_terminal_entrance(state, player):
            return hideout_tutorial(state, player, glitched) and graffitiL(state, player, limit, 103)
        else:
            return hideout_tutorial(state, player, glitched) and graffitiL(state, player, limit, 85)
    else:
        return hideout_tutorial(state, player, glitched) and graffitiL(state, player, limit, 10)
    

def versum_hill_challenge1(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return rep(state, player, 50)
    else:
        return versum_hill_ch1_roadblock(state, player, limit, glitched) and rep(state, player, 50)
    

def versum_hill_challenge2(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return rep(state, player, 58)
    else:
        return versum_hill_ch1_roadblock(state, player, limit, glitched) and rep(state, player, 58)
    

def versum_hill_challenge3(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return rep(state, player, 65)
    else: 
        return versum_hill_ch1_roadblock(state, player, limit, glitched) and rep(state, player, 65)
    

def versum_hill_all_challenges(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return versum_hill_challenge3(state, player, limit, glitched)


def versum_hill_basketball_court(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return versum_hill_all_challenges(state, player, limit, glitched) and rep(state, player, 90)
    

def versum_hill_oldhead(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return versum_hill_ch1_roadblock(state, player, limit, glitched) and rep(state, player, 120)
    

def versum_hill_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return versum_hill_all_challenges(state, player, limit, glitched) and rep(state, player, 90) and graffitiM(state, player, limit, 98)
    else:
        return versum_hill_all_challenges(state, player, limit, glitched) and rep(state, player, 90) and graffitiM(state, player, limit, 27)
    

def versum_hill_rave(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        if current_chapter(state, player, 4):
            return versum_hill_oldhead(state, player, limit, glitched) and graffitiL(state, player, limit, 90) and graffitiXL(state, player, limit, 51)
        elif current_chapter(state, player, 3):
            return versum_hill_oldhead(state, player, limit, glitched) and graffitiL(state, player, limit, 89) and graffitiXL(state, player, limit, 51)
        else:
            return versum_hill_oldhead(state, player, limit, glitched) and graffitiL(state, player, limit, 85) and graffitiXL(state, player, limit, 48)
    else:
        return versum_hill_oldhead(state, player, limit, glitched) and graffitiL(state, player, limit, 26) and graffitiXL(state, player, limit, 10)


def millennium_square_entrance(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return current_chapter(state, player, 2)


def brink_terminal_entrance(state: CollectionState, player: int) -> bool:
    return is_girl(state, player) and rep(state, player, 180) and current_chapter(state, player, 2)


def brink_terminal_challenge1(state: CollectionState, player: int) -> bool:
    return rep(state, player, 188) and brink_terminal_entrance(state, player)


def brink_terminal_challenge2(state: CollectionState, player: int) -> bool:
    return rep(state, player, 200) and brink_terminal_entrance(state, player)


def brink_terminal_challenge3(state: CollectionState, player: int) -> bool:
    return rep(state, player, 220) and brink_terminal_entrance(state, player)


def brink_terminal_all_challenges(state: CollectionState, player: int) -> bool:
    return brink_terminal_challenge3(state, player)


def brink_terminal_plaza(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return brink_terminal_all_challenges(state, player)
    

def brink_terminal_tower(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return brink_terminal_plaza(state, player, glitched) and rep(state, player, 280)
    

def brink_terminal_oldhead_underground(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return rep(state, player, 250)
    

def brink_terminal_oldhead_dock(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return rep(state, player, 320)
    

def brink_terminal_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return brink_terminal_all_challenges(state, player) and rep(state, player, 280) and graffitiL(state, player, limit, 103)
    else:
        return brink_terminal_all_challenges(state, player) and rep(state, player, 280) and graffitiL(state, player, limit, 62)
    

def brink_terminal_mesh(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        if current_chapter(state, player, 3):
            return brink_terminal_plaza(state, player, glitched) and brink_terminal_oldhead_dock(state, player, glitched) and graffitiM(state, player, limit, 122) and graffitiXL(state, player, limit, 45)
        else:
            return brink_terminal_plaza(state, player, glitched) and brink_terminal_oldhead_dock(state, player, glitched) and graffitiM(state, player, limit, 119) and graffitiXL(state, player, limit, 45)
    else:
        return brink_terminal_plaza(state, player, glitched) and brink_terminal_oldhead_dock(state, player, glitched) and graffitiM(state, player, limit, 67) and graffitiXL(state, player, limit, 45)


def millennium_mall_entrance(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return rep(state, player, 380) and current_chapter(state, player, 3)
    

def millennium_mall_oldhead_ceiling(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return rep(state, player, 580)
    

def millennium_mall_switch(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return graffitiM(state, player, limit, 122) and current_chapter(state, player, 3)
    else:
        return graffitiM(state, player, limit, 72) and current_chapter(state, player, 3)
    

def millennium_mall_big(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return millennium_mall_switch(state, player, limit, glitched)
    

def millennium_mall_oldhead_race(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return millennium_mall_big(state, player, limit, glitched) and rep(state, player, 530)
    

def millennium_mall_challenge1(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return millennium_mall_switch(state, player, limit, glitched) and rep(state, player, 434)


def millennium_mall_challenge2(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return millennium_mall_switch(state, player, limit, glitched) and rep(state, player, 442)


def millennium_mall_challenge3(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return millennium_mall_switch(state, player, limit, glitched) and rep(state, player, 450)


def millennium_mall_challenge4(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return millennium_mall_switch(state, player, limit, glitched) and rep(state, player, 458)


def millennium_mall_all_challenges(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return millennium_mall_challenge4(state, player, limit, glitched)


def millennium_mall_theater(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return millennium_mall_all_challenges(state, player, limit, glitched) and rep(state, player, 491) and graffitiM(state, player, limit, 78)
    

def millennium_mall_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return millennium_mall_all_challenges(state, player, limit, glitched) and millennium_mall_theater(state, player, limit, glitched) and rep(state, player, 491) and graffitiM(state, player, limit, 122) and graffitiL(state, player, limit, 107)
    else:
        return millennium_mall_all_challenges(state, player, limit, glitched) and millennium_mall_theater(state, player, limit, glitched) and rep(state, player, 491) and graffitiL(state, player, limit, 80)


def pyramid_island_entrance(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return current_chapter(state, player, 4)
    

def pyramid_island_gate(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return rep(state, player, 620)
    

def pyramid_island_oldhead(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return rep(state, player, 780)
    

def pyramid_island_challenge1(state: CollectionState, player: int) -> bool:
    return rep(state, player, 630) and current_chapter(state, player, 4)


def pyramid_island_race(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched: 
        return pyramid_island_challenge1(state, player) and graffitiL(state, player, limit, 108)
    else:
        return pyramid_island_challenge1(state, player) and graffitiL(state, player, limit, 93)


def pyramid_island_challenge2(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return pyramid_island_race(state, player, limit, glitched) and rep(state, player, 650)


def pyramid_island_challenge3(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return pyramid_island_race(state, player, limit, glitched) and rep(state, player, 660)


def pyramid_island_all_challenges(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return pyramid_island_challenge3(state, player, limit, glitched) and graffitiM(state, player, limit, 122)
    else:
        return pyramid_island_challenge3(state, player, limit, glitched) and graffitiM(state, player, limit, 88)


def pyramid_island_upper_half(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return pyramid_island_all_challenges(state, player, limit, glitched)
    

def pyramid_island_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return pyramid_island_all_challenges(state, player, limit, glitched) and rep(state, player, 730) and graffitiL(state, player, limit, 108)
    else:
        return pyramid_island_all_challenges(state, player, limit, glitched) and rep(state, player, 730) and graffitiL(state, player, limit, 97)


def pyramid_island_top(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return current_chapter(state, player, 5)


def mataan_entrance(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return current_chapter(state, player, 2)
    

def mataan_smoke_wall(state: CollectionState, player: int, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return current_chapter(state, player, 5) and rep(state, player, 850)
    

def mataan_challenge1(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return current_chapter(state, player, 5) and rep(state, player, 864) and graffitiL(state, player, limit, 108)
    else:
        return current_chapter(state, player, 5) and rep(state, player, 864) and graffitiL(state, player, limit, 98)


def mataan_deep_city(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return mataan_challenge1(state, player, limit, glitched)
    

def mataan_oldhead(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return mataan_deep_city(state, player, limit, glitched) and rep(state, player, 935)
    

def mataan_challenge2(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return mataan_challenge1(state, player, limit, glitched) and rep(state, player, 880) and graffitiXL(state, player, limit, 59)
    else:
        return mataan_challenge1(state, player, limit, glitched) and rep(state, player, 880) and graffitiXL(state, player, limit, 57)


def mataan_challenge3(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return mataan_challenge1(state, player, limit, glitched) and rep(state, player, 920)


def mataan_all_challenges(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return mataan_challenge2(state, player, limit, glitched) and mataan_challenge3(state, player, limit, glitched)


def mataan_smoke_wall2(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return mataan_all_challenges(state, player, limit, glitched) or rep(state, player, 960)


def mataan_crew_battle(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return mataan_all_challenges(state, player, limit, glitched) and graffitiM(state, player, limit, 122) and graffitiXL(state, player, limit, 59)
    else:
        return mataan_all_challenges(state, player, limit, glitched) and graffitiM(state, player, limit, 117) and graffitiXL(state, player, limit, 57)
    

def mataan_deepest(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    if glitched:
        return True
    else:
        return mataan_crew_battle(state, player, limit, glitched)
    

def mataan_faux(state: CollectionState, player: int, limit: bool, glitched: bool) -> bool:
    return mataan_crew_battle(state, player, limit, glitched) and graffitiM(state, player, limit, 122)


def spots_s(state: CollectionState, player: int, limit: bool, glitched: bool) -> int:
    sprayable: int = state.count_group("characters", player) * 5
    total: int = 0

    if glitched:
        total += 75

        if brink_terminal_entrance(state, player):
            total += 13

        if current_chapter(state, player, 3):
            total += 6

    else:
        # chapter 1
        # hideout
        total += 10

        # versum hill area 1
        if versum_hill_entrance(state, player, glitched):
            total += 1

            # versum hill area 2
            if versum_hill_ch1_roadblock(state, player, limit, glitched):
                total += 11

                # versum hill OldHeadArea
                if versum_hill_oldhead(state, player, limit, glitched):
                    total += 1

                # versum hill area 4
                if versum_hill_basketball_court(state, player, limit, glitched):

                    # chapter 2
                    # millennium square + mataan
                    if current_chapter(state, player, 2):
                        # 7 in square, 5 in mataan
                        total += 12
                        
                        # brink terminal area 1
                        if brink_terminal_entrance(state, player):
                            total += 9

                            # brink terminal dock OldHeadArea
                            if brink_terminal_oldhead_dock(state, player, glitched):
                                total += 1

                            # brink terminal tower area
                            if brink_terminal_plaza(state, player, glitched):
                                total += 3

                                # brink terminal inside tower
                                if brink_terminal_tower(state, player, glitched):

                                    # chapter 3
                                    # millennium square 2
                                    if current_chapter(state, player, 3):
                                        total += 6

                                        # millennium mall area 1
                                        if millennium_mall_entrance(state, player, glitched):
                                            total += 3

                                            # millennium mall area 2
                                            if millennium_mall_switch(state, player, limit, glitched):
                                                total += 4

                                                # millennium mall area 3
                                                if millennium_mall_theater(state, player, limit, glitched):
                                                    total += 3

                                                    # chapter 4
                                                    # pyramid island area 1
                                                    if current_chapter(state, player, 4):
                                                        # 2 in pyramid
                                                        total += 2

                                                        # pyramid island area 2
                                                        if pyramid_island_gate(state, player, glitched):
                                                            total += 5

                                                            # pyramid island OldHeadArea
                                                            if pyramid_island_oldhead(state, player, glitched):
                                                                total += 2

                                                            # pyramid island area 3
                                                            if pyramid_island_upper_half(state, player, limit, glitched):
                                                                total += 8

                                                                # pyramid island area 4
                                                                if pyramid_island_crew_battle(state, player, limit, glitched):

                                                                    # chapter 5
                                                                    # pyramid island 2
                                                                    if current_chapter(state, player, 5):

                                                                        # mataan area 2
                                                                        if mataan_smoke_wall(state, player, glitched):
                                                                            total += 3

                                                                            # mataan area 3
                                                                            if mataan_deep_city(state, player, limit, glitched):
                                                                                total += 5

                                                                                # mataan OldHeadArea
                                                                                if mataan_oldhead(state, player, limit,  glitched):
                                                                                    total += 3

                                                                                    if mataan_deepest(state, player, limit, glitched):
                                                                                        total += 2

    if limit:
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        return total


def spots_m(state: CollectionState, player: int, movestyle: int, limit: bool, glitched: bool) -> int:
    sprayable: int = state.count_group("graffitim", player) * 9
    total: int = 0

    if glitched:
        total += 99

        if brink_terminal_entrance(state, player):
            total += 21

        if current_chapter(state, player, 3):
            total += 3
        
    else:
        # chapter 1
        # hideout
        total += 4

        # versum hill area 1
        if versum_hill_entrance(state, player, glitched):
            total += 3

            # versum hill area 2
            if versum_hill_ch1_roadblock(state, player, limit, glitched):
                total += 13

                # versum hill OldHeadArea
                if versum_hill_oldhead(state, player, limit, glitched):
                    total += 4

                # versum hill area 3
                if versum_hill_all_challenges(state, player, limit, glitched):
                    total += 3

                # versum hill area 4
                if versum_hill_basketball_court(state, player, limit, glitched):

                    # chapter 2
                    # millennium square + mataan
                    if current_chapter(state, player, 2):
                        # 12 in square, 4 in mataan
                        total += 16
                        
                        # brink terminal area 1
                        if brink_terminal_entrance(state, player):
                            total += 13

                            # brink terminal dock OldHeadArea
                            if brink_terminal_oldhead_dock(state, player, glitched):
                                total += 4

                            # brink terminal tower area
                            if brink_terminal_plaza(state, player, glitched):
                                total += 4

                                # brink terminal inside tower
                                if brink_terminal_tower(state, player, glitched):

                                    # chapter 3
                                    # millennium square 2
                                    if current_chapter(state, player, 3):
                                        total += 3

                                        # millennium mall area 1
                                        if millennium_mall_entrance(state, player, glitched):
                                            total += 5

                                            # millennium mall OldHeadArea
                                            if millennium_mall_oldhead_ceiling(state, player, glitched):
                                                total += 1

                                            # millennium mall area 2
                                            if millennium_mall_big(state, player, limit, glitched):
                                                total += 6

                                                # millennium mall area 3
                                                if millennium_mall_theater(state, player, limit, glitched):
                                                    total += 4

                                                    # chapter 4
                                                    # pyramid island area 1
                                                    if current_chapter(state, player, 4):
                                                        # 2 in pyramid
                                                        total += 2

                                                        # pyramid island area 2
                                                        if pyramid_island_gate(state, player, glitched):
                                                            total += 3

                                                            # pyramid island OldHeadArea
                                                            if pyramid_island_oldhead(state, player, glitched):
                                                                total += 5

                                                            # pyramid island area 3
                                                            if pyramid_island_upper_half(state, player, limit, glitched):
                                                                total += 8

                                                                # pyramid island area 4
                                                                if pyramid_island_crew_battle(state, player, limit, glitched):

                                                                    # chapter 5
                                                                    # pyramid island 2
                                                                    if current_chapter(state, player, 5):
                                                                        total += 2

                                                                        # mataan area 2
                                                                        if mataan_smoke_wall(state, player, glitched):

                                                                            # mataan area 3
                                                                            if mataan_deep_city(state, player, limit, glitched):
                                                                                total += 7

                                                                                # center island
                                                                                if skateboard(state, player, movestyle):
                                                                                    total += 1

                                                                                # mataan OldHeadArea
                                                                                if mataan_oldhead(state, player, limit, glitched):
                                                                                    total += 1

                                                                                    # mataan area 4
                                                                                    if mataan_smoke_wall2(state, player, limit, glitched):
                                                                                        total += 1

                                                                                        if mataan_deepest(state, player, limit, glitched):
                                                                                            total += 10

    if limit:
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitim", player):
            return total
        else:
            return 0
        

def spots_l(state: CollectionState, player: int, movestyle: int, limit: bool, glitched: bool) -> int:
    sprayable: int = state.count_group("graffitil", player) * 8
    total: int = 0

    if glitched:
        total += 90

        if brink_terminal_entrance(state, player):
            total += 18

        if current_chapter(state, player, 3):
            total += 4

        if current_chapter(state, player, 4):
            total += 1

    else:
        # chapter 1
        # hideout
        total += 7

        if inline_skates(state, player, movestyle):
            total += 1

        # versum hill area 1
        if versum_hill_entrance(state, player, glitched):
            total += 2

            # versum hill area 2
            if versum_hill_ch1_roadblock(state, player, limit, glitched):
                total += 13

                # versum hill OldHeadArea
                if versum_hill_oldhead(state, player, limit, glitched):
                    total += 2

                # versum hill area 3
                if versum_hill_all_challenges(state, player, limit, glitched):
                    total += 1

                # versum hill area 4
                if versum_hill_basketball_court(state, player, limit, glitched):

                    # chapter 2
                    # millennium square + mataan
                    if current_chapter(state, player, 2):
                        # 7 in square, 7 in mataan
                        total += 14
                        
                        # brink terminal area 1
                        if brink_terminal_entrance(state, player):
                            total += 10

                            # brink terminal underground OldHeadArea
                            if brink_terminal_oldhead_underground(state, player, glitched):
                                total += 1

                            # brink terminal dock OldHeadArea
                            if brink_terminal_oldhead_dock(state, player, glitched):
                                total += 4

                            # brink terminal tower area
                            if brink_terminal_plaza(state, player, glitched):
                                total += 2

                                # brink terminal inside tower
                                if brink_terminal_tower(state, player, glitched):
                                    total += 1

                                    # chapter 3
                                    # millennium square 2
                                    if current_chapter(state, player, 3):
                                        total += 4

                                        # millennium mall area 1
                                        if millennium_mall_entrance(state, player, glitched):
                                            total += 3
                                            
                                            # millennium mall OldHeadArea
                                            if millennium_mall_oldhead_ceiling(state, player, glitched):
                                                total += 3

                                            # millennium mall area 2
                                            if millennium_mall_big(state, player, limit, glitched):
                                                total += 8

                                                # millennium mall area 3
                                                if millennium_mall_theater(state, player, limit, glitched):
                                                    total += 4

                                                    # chapter 4
                                                    # pyramid island area 1
                                                    if current_chapter(state, player, 4):
                                                        # 1 in square, 4 in pyramid
                                                        total += 1

                                                        # pyramid island area 2
                                                        if pyramid_island_gate(state, player, glitched):
                                                            total += 4

                                                            # pyramid island OldHeadArea
                                                            if pyramid_island_oldhead(state, player, glitched):
                                                                total += 2

                                                            # pyramid island area 3
                                                            if pyramid_island_upper_half(state, player, limit, glitched):
                                                                total += 5

                                                                # pyramid island area 4
                                                                if pyramid_island_crew_battle(state, player, limit, glitched):
                                                                    total += 1

                                                                    # chapter 5
                                                                    # pyramid island 2
                                                                    if current_chapter(state, player, 5):
                                                                        total += 1

                                                                        # mataan area 2
                                                                        if mataan_smoke_wall(state, player, glitched):
                                                                            total += 1

                                                                            # mataan area 3
                                                                            if mataan_deep_city(state, player, limit, glitched):
                                                                                total += 2

                                                                                # center island
                                                                                if skateboard(state, player, movestyle):
                                                                                    total += 1

                                                                                # mataan OldHeadArea
                                                                                if mataan_oldhead(state, player, limit, glitched):
                                                                                    total += 2

                                                                                    # mataan area 4
                                                                                    if mataan_smoke_wall2(state, player, limit, glitched):
                                                                                        total += 2

                                                                                        # mataan area 4 part 2 + area 5
                                                                                        if mataan_deepest(state, player, limit, glitched):
                                                                                            total += 7

    if limit:
        if total <= sprayable:
            return total
        else:
            return sprayable
    else:
        if state.has_group("graffitil", player):
            return total
        else:
            return 0
        

def spots_xl(state: CollectionState, player: int, movestyle: int, limit: bool, glitched: bool) -> int:
    sprayable: int = state.count_group("graffitixl", player) * 6
    total: int = 0

    if glitched:
        total += 50

        if brink_terminal_entrance(state, player):
            total += 8

        if current_chapter(state, player, 3):
            total += 3

    else:
        # chapter 1
        # hideout
        total += 3

        # versum hill area 1
        if versum_hill_entrance(state, player, glitched):

            # versum hill area 2
            if versum_hill_ch1_roadblock(state, player, limit, glitched):
                total += 6

                # versum hill area 4
                if versum_hill_basketball_court(state, player, limit, glitched):
                    total += 1

                    # chapter 2
                    # millennium square + mataan
                    if current_chapter(state, player, 2):
                        # 4 in square, 4 in mataan
                        total += 9
                        
                        # brink terminal area 1
                        if brink_terminal_entrance(state, player):
                            total += 3

                            # brink terminal underground OldHeadArea
                            if brink_terminal_oldhead_underground(state, player, glitched):
                                total += 1

                            # brink terminal dock OldHeadArea
                            if brink_terminal_oldhead_dock(state, player, glitched):
                                total += 2

                            # brink terminal tower area
                            if brink_terminal_plaza(state, player, glitched):
                                total += 1

                                # brink terminal inside tower
                                if brink_terminal_tower(state, player, glitched):
                                    total += 1

                                    # chapter 3
                                    # millennium square 2
                                    if current_chapter(state, player, 3):
                                        total += 3

                                        # millennium mall area 1
                                        if millennium_mall_entrance(state, player, glitched):
                                            total += 2

                                            # millennium mall OldHeadArea
                                            if millennium_mall_oldhead_ceiling(state, player, glitched):
                                                total += 1

                                            # millennium mall area 2
                                            if millennium_mall_big(state, player, limit, glitched):
                                                total += 5

                                                # millennium mall area 3
                                                if millennium_mall_theater(state, player, limit, glitched):
                                                    total += 5

                                                    # chapter 4
                                                    # pyramid island area 1
                                                    if current_chapter(state, player, 4):
                                                        # 1 in terminal, 2 in pyramid
                                                        total += 3

                                                        # pyramid island area 2
                                                        if pyramid_island_gate(state, player, glitched):

                                                            # pyramid island OldHeadArea
                                                            if pyramid_island_oldhead(state, player, glitched):
                                                                total += 3

                                                            # pyramid island area 3
                                                            if pyramid_island_upper_half(state, player, limit, glitched):
                                                                total += 5

                                                                # pyramid island area 4
                                                                if pyramid_island_crew_battle(state, player, limit, glitched):

                                                                    # chapter 5
                                                                    # pyramid island 2
                                                                    if current_chapter(state, player, 5):

                                                                        # mataan area 2
                                                                        if mataan_smoke_wall(state, player, glitched):
                                                                            total += 2

                                                                            # mataan area 3
                                                                            if mataan_deep_city(state, player, limit, glitched):
                                                                                total += 2

                                                                                # mataan OldHeadArea
                                                                                if mataan_oldhead(state, player, limit, glitched):
                                                                                    total += 2

                                                                                    if mataan_deepest(state, player, limit, glitched):
                                                                                        total += 2

    if limit:
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
    total: int = spots_s(state, player, limit, glitched) + spots_m(state, player, movestyle, limit, glitched) \
        + spots_l(state, player, movestyle, limit, glitched) + spots_xl(state, player, movestyle, limit, glitched)

    return total >= spots


def rep(state: CollectionState, player: int, required: int) -> bool:
    total: int = (state.count("8 REP", player) * 8) + (state.count("16 REP", player) * 16) \
        + (state.count("24 REP", player) * 24) + (state.count("32 REP", player) * 32) \
            + (state.count("48 REP", player) * 48)

    return total >= required


def rules(brcworld):
    world = brcworld.multiworld
    player = brcworld.player

    movestyle = brcworld.options.starting_movestyle
    limit = brcworld.options.limited_graffiti
    glitched = brcworld.options.logic
    extra = brcworld.options.extra_rep_required

    # entrances
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
    set_rule(world.get_location("Versum Hill: Under bridge graffiti", player),
        lambda state: versum_hill_ch1_roadblock(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Train rail ledge skateboard", player),
        lambda state: versum_hill_ch1_roadblock(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Train station CD", player),
        lambda state: versum_hill_ch1_roadblock(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Billboard platform outfit", player),
        lambda state: versum_hill_ch1_roadblock(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Hilltop Robo Post CD", player),
        lambda state: versum_hill_ch1_roadblock(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Hill secret skateboard", player),
        lambda state: versum_hill_ch1_roadblock(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Rooftop CD", player),
        lambda state: versum_hill_ch1_roadblock(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Wallrunning challenge reward", player),
        lambda state: versum_hill_challenge1(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Manual challenge reward", player),
        lambda state: versum_hill_challenge2(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Corner challenge reward", player),
        lambda state: versum_hill_challenge3(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Side street alley outfit", player),
        lambda state: versum_hill_all_challenges(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Side street secret skateboard", player),
        lambda state: versum_hill_all_challenges(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Basketball court alley skateboard", player),
        lambda state: versum_hill_basketball_court(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Basketball court Robo Post CD", player),
        lambda state: versum_hill_basketball_court(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Underground mall billboard graffiti", player),
        lambda state: versum_hill_oldhead(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Underground mall vending machine skateboard", player),
        lambda state: versum_hill_oldhead(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: BMX gate outfit", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(world.get_location("Versum Hill: Glass floor skates", player),
        lambda state: (
            versum_hill_ch1_roadblock(state, player, limit, glitched)
            and inline_skates(state, player, movestyle)
        ))
    set_rule(world.get_location("Versum Hill: Basketball court shortcut CD", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(world.get_location("Versum Hill: Rave joins the crew", player),
        lambda state: versum_hill_rave(state, player, limit, glitched))
    set_rule(world.get_location("Versum Hill: Frank joins the crew", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(world.get_location("Versum Hill: Rietveld joins the crew", player),
        lambda state: current_chapter(state, player, 2))
    set_rule(world.get_location("Versum Hill: Big Polo", player),
        lambda state: camera(state, player))
    set_rule(world.get_location("Versum Hill: Trash Polo", player),
        lambda state: camera(state, player))
    set_rule(world.get_location("Versum Hill: Fruit stand Polo", player),
        lambda state: (
            camera(state, player)
            and versum_hill_oldhead(state, player, limit, glitched)
        ))
    
    # millennium square
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
    set_rule(world.get_location("Brink Terminal: Underground ramp skates", player),
        lambda state: brink_terminal_oldhead_underground(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: Rooftop halfpipe graffiti", player),
        lambda state: brink_terminal_tower(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: Wire grind CD", player),
        lambda state: brink_terminal_plaza(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: Rooftop glass CD", player),
        lambda state: (
            brink_terminal_tower(state, player, glitched)
            and inline_skates(state, player, movestyle)
        ))
    set_rule(world.get_location("Brink Terminal: Tower core outfit", player),
        lambda state: brink_terminal_tower(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: High rooftop outfit", player),
        lambda state: brink_terminal_tower(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: Ocean platform CD", player),
        lambda state: brink_terminal_oldhead_dock(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: End of dock CD", player),
        lambda state: brink_terminal_oldhead_dock(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: Dock Robo Post outfit", player),
        lambda state: brink_terminal_oldhead_dock(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: Control room skates", player),
        lambda state: brink_terminal_oldhead_dock(state, player, glitched))
    set_rule(world.get_location("Brink Terminal: Mesh joins the crew", player),
        lambda state: brink_terminal_mesh(state, player, limit, glitched))
    set_rule(world.get_location("Brink Terminal: Eclipse joins the crew", player),
        lambda state: current_chapter(state, player, 3))
    set_rule(world.get_location("Brink Terminal: Behind glass Polo", player),
        lambda state: camera(state, player))
    
    # millennium mall
    set_rule(world.get_location("Millennium Mall: Glass cylinder CD", player),
        lambda state: inline_skates(state, player, movestyle))
    set_rule(world.get_location("Millennium Mall: Court vending machine graffiti", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Trick challenge reward", player),
        lambda state: millennium_mall_challenge1(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Slide challenge reward", player),
        lambda state: millennium_mall_challenge2(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Fish challenge reward", player),
        lambda state: millennium_mall_challenge3(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Score challenge reward", player),
        lambda state: millennium_mall_challenge4(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Court top floor Robo Post CD", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Court top floor floating CD", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Court top floor BMX", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Theater entrance BMX", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Court BMX gate BMX", player),
        lambda state: (
            millennium_mall_big(state, player, limit, glitched)
            and bmx(state, player, movestyle)
        ))
    set_rule(world.get_location("Millennium Mall: Upside down rail outfit", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Theater stage corner graffiti", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Theater hanging billboards graffiti", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Theater garage graffiti", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Theater maintenance CD", player),
        lambda state: millennium_mall_big(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Race track Robo Post CD", player),
        lambda state: millennium_mall_oldhead_race(state, player, limit, glitched))
    set_rule(world.get_location("Millennium Mall: Hanging lights CD", player),
        lambda state: millennium_mall_oldhead_ceiling(state, player, glitched))
    set_rule(world.get_location("Millennium Mall: Shine joins the crew", player),
        lambda state: current_chapter(state, player, 4))
    set_rule(world.get_location("Millennium Mall: DOT.EXE joins the crew", player),
        lambda state: current_chapter(state, player, 4))
    
    # pyramid island
    set_rule(world.get_location("Pyramid Island: BMX gate BMX", player),
        lambda state: bmx(state, player, movestyle))
    set_rule(world.get_location("Pyramid Island: Quarter pipe rooftop graffiti", player),
        lambda state: pyramid_island_gate(state, player, glitched))
    set_rule(world.get_location("Pyramid Island: Supply port Robo Post CD", player),
        lambda state: pyramid_island_gate(state, player, glitched))
    set_rule(world.get_location("Pyramid Island: Above gate ledge CD", player),
        lambda state: pyramid_island_gate(state, player, glitched))
    set_rule(world.get_location("Pyramid Island: Smoke hole BMX", player),
        lambda state: pyramid_island_gate(state, player, glitched))
    set_rule(world.get_location("Pyramid Island: Above gate rail outfit", player),
        lambda state: pyramid_island_gate(state, player, glitched))
    set_rule(world.get_location("Pyramid Island: Rail loop outfit", player),
        lambda state: pyramid_island_gate(state, player, glitched))
    set_rule(world.get_location("Pyramid Island: Score challenge reward", player),
        lambda state: pyramid_island_challenge1(state, player))
    set_rule(world.get_location("Pyramid Island: Score challenge 2 reward", player),
        lambda state: pyramid_island_challenge2(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Quarter pipe challenge reward", player),
        lambda state: pyramid_island_challenge3(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Wind turbines CD", player),
        lambda state: pyramid_island_upper_half(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Shortcut glass CD", player),
        lambda state: (
            pyramid_island_upper_half(state, player, limit, glitched)
            and inline_skates(state, player, movestyle)
        ))
    set_rule(world.get_location("Pyramid Island: Turret jump CD", player),
        lambda state: pyramid_island_upper_half(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Helipad BMX", player),
        lambda state: pyramid_island_upper_half(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Pipe outfit", player),
        lambda state: pyramid_island_upper_half(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Trash outfit", player),
        lambda state: pyramid_island_upper_half(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Pyramid top CD", player),
        lambda state: pyramid_island_crew_battle(state, player, limit, glitched))
    set_rule(world.get_location("Pyramid Island: Pyramid top Robo Post CD", player),
        lambda state: pyramid_island_top(state, player, glitched))
    set_rule(world.get_location("Pyramid Island: Maze outfit", player),
        lambda state: (
            pyramid_island_oldhead(state, player, glitched)
            and skateboard(state, player, movestyle)
        ))
    set_rule(world.get_location("Pyramid Island: Rise joins the crew", player),
        lambda state: pyramid_island_crew_battle(state, player, limit, glitched))
    if not glitched:
        add_rule(world.get_location("Pyramid Island: Rise joins the crew", player),
            lambda state: camera(state, player))
    set_rule(world.get_location("Pyramid Island: Devil Theory joins the crew", player),
        lambda state: current_chapter(state, player, 5))
    set_rule(world.get_location("Pyramid Island: Polo pile 1", player),
        lambda state: camera(state, player))
    set_rule(world.get_location("Pyramid Island: Polo pile 2", player),
        lambda state: camera(state, player))
    set_rule(world.get_location("Pyramid Island: Polo pile 3", player),
        lambda state: camera(state, player))
    set_rule(world.get_location("Pyramid Island: Polo pile 4", player),
        lambda state: camera(state, player))
    set_rule(world.get_location("Pyramid Island: Maze glass Polo", player),
        lambda state: (
            camera(state, player)
            and pyramid_island_oldhead(state, player, glitched)
        ))
    set_rule(world.get_location("Pyramid Island: Maze classroom Polo", player),
        lambda state: (
            camera(state, player)
            and pyramid_island_oldhead(state, player, glitched)
        ))
    set_rule(world.get_location("Pyramid Island: Maze vent Polo", player),
        lambda state: (
            camera(state, player)
            and pyramid_island_oldhead(state, player, glitched)
        ))
    set_rule(world.get_location("Pyramid Island: Big maze Polo", player),
        lambda state: (
            camera(state, player)
            and pyramid_island_oldhead(state, player, glitched)
        ))
    set_rule(world.get_location("Pyramid Island: Maze desk Polo", player),
        lambda state: (
            camera(state, player)
            and pyramid_island_oldhead(state, player, glitched)
        ))
    set_rule(world.get_location("Pyramid Island: Maze forklift Polo", player),
        lambda state: (
            camera(state, player)
            and pyramid_island_oldhead(state, player, glitched)
        ))

    # mataan
    set_rule(world.get_location("Mataan: Trash CD", player),
        lambda state: mataan_smoke_wall(state, player, glitched))
    set_rule(world.get_location("Mataan: Half pipe CD", player),
        lambda state: mataan_smoke_wall(state, player, glitched))
    set_rule(world.get_location("Mataan: Across bull horns graffiti", player),
        lambda state: mataan_smoke_wall(state, player, glitched))
    set_rule(world.get_location("Mataan: Small rooftop graffiti", player),
        lambda state: mataan_smoke_wall(state, player, glitched))
    set_rule(world.get_location("Mataan: Trash graffiti", player),
        lambda state: mataan_smoke_wall(state, player, glitched))
    set_rule(world.get_location("Mataan: Deep city Robo Post CD", player),
        lambda state: mataan_deep_city(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Deep city tower CD", player),
        lambda state: mataan_deep_city(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Race challenge reward", player),
        lambda state: mataan_challenge1(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Wallrunning challenge reward", player),
        lambda state: mataan_challenge2(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Score challenge reward", player),
        lambda state: mataan_challenge3(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Deep city vent jump BMX", player),
        lambda state: mataan_deep_city(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Deep city side wires outfit", player),
        lambda state: mataan_deep_city(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Deep city center island outfit", player),
        lambda state: mataan_deep_city(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Red light rail graffiti", player),
        lambda state: mataan_oldhead(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Red light side alley outfit", player),
        lambda state: mataan_oldhead(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Statue hand outfit", player),
        lambda state: mataan_smoke_wall2(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Crane CD", player),
        lambda state: mataan_deepest(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Elephant tower glass outfit", player),
        lambda state: mataan_deepest(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Helipad outfit", player),
        lambda state: mataan_deepest(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Vending machine CD", player),
        lambda state: mataan_deepest(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Coil joins the crew", player),
        lambda state: mataan_crew_battle(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Flesh Prince joins the crew", player),
        lambda state: mataan_crew_battle(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Futurism joins the crew", player),
        lambda state: mataan_crew_battle(state, player, limit, glitched))
    set_rule(world.get_location("Mataan: Trash Polo", player),
        lambda state: (
            camera(state, player)
            and mataan_smoke_wall(state, player, glitched)
        ))
    set_rule(world.get_location("Mataan: Shopping Polo", player),
        lambda state: (
            camera(state, player)
            and mataan_deepest(state, player, limit, glitched)
        ))

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
    
    