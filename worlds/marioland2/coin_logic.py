from .logic import has_pipe_down, has_pipe_up, has_pipe_right, has_pipe_left


def mushroom_zone_coins(state, player, coins, auto_scroll):
    reachable_coins = 40
    if has_pipe_down(state, player):
        # There's 24 in each of the underground sections.
        # The first one requires missing some question mark blocks if auto scrolling (the last +4).
        # If you go in the second without pipe up, you can get everything except the last 5 plus the ones in the first
        # underground section.
        reachable_coins += 19
        if has_pipe_up(state, player) or not auto_scroll:
            reachable_coins += 5
        if has_pipe_up(state, player):
            reachable_coins += 20
            if not auto_scroll:
                reachable_coins += 4
    return coins <= reachable_coins


def tree_zone_1_coins(state, player, coins, auto_scroll):
    return coins <= 87 or not auto_scroll


def tree_zone_2_coins(state, player, coins, auto_scroll):
    reachable_coins = 18
    if has_pipe_right(state, player):
        reachable_coins += 38
        if state.has("Carrot", player):
            reachable_coins += 12
            if not auto_scroll:
                reachable_coins += 30
    elif state.has("Tree Zone 2 Midway Bell", player):
        reachable_coins = 30
        if not auto_scroll:
            reachable_coins += 8
    return coins <= reachable_coins


def tree_zone_3_coins(state, player, coins, auto_scroll):
    if coins <= 19:
        return True
    elif state.has_any(["Mushroom", "Fire Flower"], player) and coins <= 21:
        return True
    return state.has("Carrot", player)


def tree_zone_4_coins(state, player, coins, auto_scroll):
    reachable_coins = 0
    if has_pipe_up(state, player):
        reachable_coins += 14
        if has_pipe_right(state, player):
            reachable_coins += 4
            if has_pipe_down(state, player):
                reachable_coins += 46
                if not auto_scroll:
                    reachable_coins += 10
    elif state.has("Tree Zone 4 Midway Bell", player):
        if not auto_scroll:
            if has_pipe_left(state, player):
                reachable_coins += 18
                if has_pipe_down(state, player):
                    reachable_coins += 46
                    if has_pipe_up(state, player):
                        reachable_coins += 10
        elif has_pipe_down(state, player):
            reachable_coins += 10
    return coins <= reachable_coins


def tree_zone_5_coins(state, player, coins, auto_scroll):
    reachable_coins = 0
    # Not actually sure if these platforms can be randomized / can make the coin blocks unreachable from below
    if ((not state.multiworld.worlds[player].options.randomize_platforms)
            or state.has_any(["Mushroom", "Fire Flower"], player)):
        reachable_coins += 2
    if state.has_any(["Mushroom", "Fire Flower"], player):
        reachable_coins += 2
    if state.has("Carrot", player):
        reachable_coins += 18
        if has_pipe_up(state, player) and not auto_scroll:
            reachable_coins += 13
    elif has_pipe_up(state, player):
        reachable_coins += 13
    return coins <= reachable_coins


def hippo_zone_coins(state, player, coins, auto_scroll):
    reachable_coins = 4
    if state.has_any(["Swim", "Hippo Bubble", "Carrot"], player):
        reachable_coins += 108
        if state.has_any(["Mushroom", "Fire Flower", "Hippo Bubble"], player):
            reachable_coins += 6
    if state.has_all(["Fire Flower", "Swim"], player):
        reachable_coins += 1
    if state.has("Hippo Bubble", player):
        # Probably some of these are reachable with Carrot
        reachable_coins += 52
    return coins <= reachable_coins


def pumpkin_zone_1_coins(state, player, coins, auto_scroll):
    reachable_coins = 0
    if state.has("Pumpkin Zone 1 Midway Bell", player) or has_pipe_down(state, player):
        reachable_coins += 38
        if has_pipe_up(state, player):
            reachable_coins += 2
    return coins <= reachable_coins


def pumpkin_zone_2_coins(state, player, coins, auto_scroll):
    reachable_coins = 17
    if has_pipe_down(state, player):
        reachable_coins += 7
        if state.has("Swim", player):
            reachable_coins += 6
            if has_pipe_up(state, player) and has_pipe_right(state, player):
                reachable_coins += 1
                if state.has_any(["Mushroom", "Fire Flower"], player):
                    reachable_coins += 5
    return coins <= reachable_coins


def pumpkin_zone_secret_course_1_coins(state, player, coins, auto_scroll):
    if coins <= 20:  # I've gotten as high as 22 but only once. We'll be a bit forgiving.
        return True
    return state.has("Carrot", player)


def pumpkin_zone_3_coins(state, player, coins, auto_scroll):
    reachable_coins = 38
    if has_pipe_up(state, player) and ((not auto_scroll) or has_pipe_down(state, player)):
        reachable_coins += 12
    if has_pipe_down(state, player) and not auto_scroll:
        reachable_coins += 11
    return coins <= reachable_coins


def pumpkin_zone_4_coins(state, player, coins, auto_scroll):
    reachable_coins = 29
    if has_pipe_down(state, player):
        if auto_scroll:
            if has_pipe_up(state, player):
                reachable_coins += 16
            else:
                reachable_coins += 4
        else:
            reachable_coins += 28
            # both sets of coins are down, but you need pipe up to return to go down to the next set in one playthrough
            if has_pipe_up(state, player):
                reachable_coins += 16
    return coins <= reachable_coins


def mario_zone_1_coins(state, player, coins, auto_scroll):
    reachable_coins = 0
    if has_pipe_right(state, player) or (has_pipe_left(state, player)
                                         and state.has("Mario Zone 1 Midway Bell", player)):
        reachable_coins += 32
    if has_pipe_right(state, player):
        reachable_coins += 8
        # coins from end section. I was able to get 13 as small mario, giving some leniency
        if state.has("Carrot", player):
            reachable_coins += 28
        else:
            reachable_coins += 12
        if state.has("Fire Flower", player):
            reachable_coins += 46
    return coins <= reachable_coins


def mario_zone_3_coins(state, player, coins, auto_scroll):
    reachable_coins = 34
    if state.has("Fire Flower", player):
        reachable_coins += 23
    return coins <= reachable_coins


def mario_zone_4_coins(state, player, coins, auto_scroll):
    return coins <= 63 or not auto_scroll


def turtle_zone_1_coins(state, player, coins, auto_scroll):
    reachable_coins = 37
    if auto_scroll:
        reachable_coins -= 1
    if state.has("Swim", player):
        reachable_coins += 16
    if state.has("Carrot", player):
        reachable_coins += 24
        if auto_scroll:
            reachable_coins -= 10
    return coins <= reachable_coins


def turtle_zone_2_coins(state, player, coins, auto_scroll):
    reachable_coins = 4
    if state.has("Swim", player):
        reachable_coins += 20
    elif state.has("Turtle Zone 2 Midway Bell", player):
        reachable_coins += 4
    if (has_pipe_right(state, player) and has_pipe_down(state, player)
            and state.has_any(["Swim", "Turtle Zone 2 Midway Bell"], player)):
        reachable_coins += 1
        if has_pipe_left(state, player) and has_pipe_up(state, player):
            reachable_coins += 1
            if state.has("Swim", player):
                reachable_coins += 1
    return coins <= reachable_coins


def turtle_zone_secret_course_coins(state, player, coins, auto_scroll):
    reachable_coins = 53
    if state.has("Carrot", player):
        reachable_coins += 44
    elif state.has("Fire Flower", player):
        reachable_coins += 36  # was able to get 38, some leniency
    return coins <= reachable_coins


def turtle_zone_4_coins(state, player, coins, auto_scroll):
    reachable_coins = 42
    if state.has("Swim", player):
        reachable_coins += 17
    return coins <= reachable_coins


def space_zone_1_coins(state, player, coins, auto_scroll):
    return (coins <= 21 or (coins <= 50 and state.has_any(["Mushroom", "Fire Flower"], player))
            or state.has_any(["Carrot", "Space Physics"], player))


def space_zone_2_coins(state, player, coins, auto_scroll):
    reachable_coins = 12
    if state.has_any(["Mushroom", "Fire Flower", "Carrot", "Space Physics"], player):
        reachable_coins += 15
        if state.has("Space Physics", player) or not auto_scroll:
            reachable_coins += 4  # last few bottom row question mark blocks that are hard to get when auto scrolling.
    if (state.has("Space Physics", player) or (
            state.has("Mushroom", player) and state.has_any(["Fire Flower", "Carrot"], player))):
        reachable_coins += 3
    if state.has("Space Physics", player):
        reachable_coins += 79
        if not auto_scroll:
            reachable_coins += 21
    return coins <= reachable_coins


def macro_zone_1_coins(state, player, coins, auto_scroll):
    reachable_coins = 0
    if has_pipe_down(state, player):
        reachable_coins += 74
        if not auto_scroll:
            reachable_coins += 4
            if state.has("Fire Flower", player):
                reachable_coins += 19
    elif (not auto_scroll) and state.has("Macro Zone 1 Midway Bell", player):
        reachable_coins += 67
    return coins <= reachable_coins


def macro_zone_secret_course_coins(state, player, coins, auto_scroll):
    return state.has_any(["Mushroom", "Fire Flower"], player)


def macro_zone_2_coins(state, player, coins, auto_scroll):
    if coins <= 27:
        return True
    if has_pipe_up(state, player) and state.has("Swim", player):
        if has_pipe_down(state, player):
            return True
        if state.has("Macro Zone 2 Midway Bell", player):
            # Cannot return to the first section from the bell
            return coins <= 42


def macro_zone_3_coins(state, player, coins, auto_scroll):
    if has_pipe_up(state, player) and has_pipe_down(state, player):
        return True
    reachable_coins = 31
    if has_pipe_up(state, player):
        reachable_coins += 36
    if has_pipe_down(state, player):
        reachable_coins += 18
    return coins <= reachable_coins


def macro_zone_4_coins(state, player, coins, auto_scroll):
    reachable_coins = 61
    if auto_scroll:
        reachable_coins -= 8
        if state.has("Carrot", player):
            reachable_coins += 6
    return coins <= reachable_coins
