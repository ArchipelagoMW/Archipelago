from .locations import level_name_to_id


def is_auto_scroll(state, player, level):
    level_id = level_name_to_id[level]
    if state.has_any(["Cancel Auto Scroll", f"Cancel Auto Scroll - {level}"], player):
        return False
    return state.multiworld.worlds[player].auto_scroll_levels[level_id] > 0


def has_pipe_right(state, player):
    return state.has_any(["Pipe Traversal - Right", "Pipe Traversal"], player)


def has_pipe_left(state, player):
    return state.has_any(["Pipe Traversal - Left", "Pipe Traversal"], player)


def has_pipe_down(state, player):
    return state.has_any(["Pipe Traversal - Down", "Pipe Traversal"], player)


def has_pipe_up(state, player):
    return state.has_any(["Pipe Traversal - Up", "Pipe Traversal"], player)


def has_level_progression(state, item, player, count=1):
    return state.count(item, player) + (state.count(item + " x2", player) * 2) >= count


def mushroom_zone_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Mushroom Zone")
    reachable_coins = 38
    if state.has_any(["Mushroom", "Fire Flower"], player) or not auto_scroll:
        # Was able to get all but 1, being lenient.
        reachable_coins += 2
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


def tree_zone_1_coins(state, player, coins):
    return coins <= 87 or not is_auto_scroll(state, player, "Tree Zone 1")


def tree_zone_2_normal_exit(state, player):
    return has_pipe_right(state, player) or state.has("Tree Zone 2 Midway Bell", player)


def tree_zone_2_secret_exit(state, player):
    return has_pipe_right(state, player) and state.has("Carrot", player)


def tree_zone_2_midway_bell(state, player):
    return has_pipe_right(state, player) or state.has("Tree Zone 2 Midway Bell", player)


def tree_zone_2_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Tree Zone 2")
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


def tree_zone_3_normal_exit(state, player):
    return not is_auto_scroll(state, player, "Tree Zone 3")


def tree_zone_3_coins(state, player, coins):
    if is_auto_scroll(state, player, "Tree Zone 3"):
        return coins <= 4
    if coins <= 19:
        return True
    elif state.has_any(["Mushroom", "Fire Flower"], player) and coins <= 21:
        return True
    return state.has("Carrot", player)


def tree_zone_4_normal_exit(state, player):
    return has_pipe_down(state, player) and tree_zone_4_midway_bell(state, player)


def tree_zone_4_midway_bell(state, player):
    return ((has_pipe_right(state, player) and has_pipe_up(state, player))
            or state.has("Tree Zone 4 Midway Bell", player))


def tree_zone_4_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Tree Zone 4")
    entryway = 14
    hall = 4
    first_trip_downstairs = 31
    second_trip_downstairs = 15
    downstairs_with_auto_scroll = 12
    final_room = 10

    reachable_coins_from_start = 0
    reachable_coins_from_bell = 0

    if has_pipe_up(state, player):
        reachable_coins_from_start += entryway
        if has_pipe_right(state, player):
            reachable_coins_from_start += hall
            if has_pipe_down(state, player):
                if auto_scroll:
                    reachable_coins_from_start += downstairs_with_auto_scroll
                else:
                    reachable_coins_from_start += final_room + first_trip_downstairs + second_trip_downstairs
    if state.has("Tree Zone 4 Midway Bell", player):
        if has_pipe_down(state, player) and (auto_scroll or not has_pipe_left(state, player)):
            reachable_coins_from_bell += final_room
        elif has_pipe_left(state, player) and not auto_scroll:
            if has_pipe_down(state, player):
                reachable_coins_from_bell += first_trip_downstairs
                if has_pipe_right(state, player):
                    reachable_coins_from_bell += entryway + hall
                    if has_pipe_up(state, player):
                        reachable_coins_from_bell += second_trip_downstairs + final_room
            else:
                reachable_coins_from_bell += entryway + hall
    return coins <= max(reachable_coins_from_start, reachable_coins_from_bell)


def tree_zone_5_boss(state, player):
    return has_pipe_right(state, player) and (has_pipe_up(state, player) or state.has("Carrot", player))


def tree_zone_5_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Tree Zone 5")
    reachable_coins = 0
    if state.has_any(["Mushroom", "Fire Flower"], player):
        reachable_coins += 2
    if state.has("Carrot", player):
        reachable_coins += 18
        if has_pipe_up(state, player) and not auto_scroll:
            reachable_coins += 13
    elif has_pipe_up(state, player):
        reachable_coins += 13
    return coins <= reachable_coins


def pumpkin_zone_1_normal_exit(state, player):
    return pumpkin_zone_1_midway_bell(state, player)


def pumpkin_zone_1_midway_bell(state, player):
    return ((has_pipe_down(state, player) and not is_auto_scroll(state, player, "Pumpkin Zone 1"))
            or state.has("Pumpkin Zone 1 Midway Bell", player))
    
    
def pumpkin_zone_1_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Pumpkin Zone 1")
    if auto_scroll:
        return coins <= 12 and state.has("Pumpkin Zone 1 Midway Bell", player)
    reachable_coins = 0
    if state.has("Pumpkin Zone 1 Midway Bell", player) or has_pipe_down(state, player):
        reachable_coins += 38
        if has_pipe_up(state, player):
            reachable_coins += 2
    return coins <= reachable_coins


def pumpkin_zone_2_normal_exit(state, player):
    return has_pipe_down(state, player) and has_pipe_up(state, player) and has_pipe_right(state, player) and state.has(
        "Water Physics", player) and not is_auto_scroll(state, player, "Pumpkin Zone 2")


def pumpkin_zone_2_secret_exit(state, player):
    return pumpkin_zone_2_normal_exit(state, player) and state.has_any(["Mushroom", "Fire Flower"], player)


def pumpkin_zone_2_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Pumpkin Zone 2")
    reachable_coins = 17
    if has_pipe_down(state, player):
        if not auto_scroll:
            reachable_coins += 7
        if (has_pipe_up(state, player) or auto_scroll) and state.has("Water Physics", player):
            reachable_coins += 6
            if has_pipe_right(state, player) and not auto_scroll:
                reachable_coins += 1
                if state.has_any(["Mushroom", "Fire Flower"], player):
                    reachable_coins += 5
    return coins <= reachable_coins


def pumpkin_zone_secret_course_1_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Pumpkin Zone Secret Course 1")
    # We'll be a bit forgiving. I was able to reach 43 while small.
    if coins <= 40:
        return True
    if state.has("Carrot", player):
        if auto_scroll:
            return coins <= 172
        return True
    return False


def pumpkin_zone_3_secret_exit(state, player):
    return state.has("Carrot", player)


def pumpkin_zone_3_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Pumpkin Zone 3")
    reachable_coins = 38
    if has_pipe_up(state, player) and ((not auto_scroll) or has_pipe_down(state, player)):
        reachable_coins += 12
    if has_pipe_down(state, player) and not auto_scroll:
        reachable_coins += 11
    return coins <= reachable_coins


def pumpkin_zone_4_boss(state, player):
    return has_pipe_right(state, player)


def pumpkin_zone_4_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Pumpkin Zone 4")
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


def mario_zone_1_normal_exit(state, player):
    return has_pipe_right(state, player) and (not is_auto_scroll(state, player, "Mario Zone 1")
                                              or state.has_any(["Mushroom", "Fire Flower", "Carrot",
                                                                "Mario Zone 1 Midway Bell"], player))


def mario_zone_1_midway_bell(state, player):
    # It is possible to get as small mario, but it is a very precise jump and you will die afterward.
    return ((state.has_any(["Mushroom", "Fire Flower", "Carrot"], player) and has_pipe_right(state, player))
            or state.has("Mario Zone 1 Midway Bell", player))


def mario_zone_1_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Mario Zone 1")
    reachable_coins = 0
    if has_pipe_right(state, player) or (has_pipe_left(state, player)
                                         and state.has("Mario Zone 1 Midway Bell", player) and not auto_scroll):
        reachable_coins += 32
    if has_pipe_right(state, player) and (state.has_any(["Mushroom", "Fire Flower", "Carrot"], player)
                                          or not auto_scroll):
        reachable_coins += 8
        # coins from end section. I was able to get 13 as small mario, giving some leniency
        if state.has("Carrot", player):
            reachable_coins += 28
        else:
            reachable_coins += 12
        if state.has("Fire Flower", player) and not auto_scroll:
            reachable_coins += 46
    return coins <= reachable_coins


def mario_zone_3_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Mario Zone 3")
    reachable_coins = 10
    if state.has("Carrot", player):
        reachable_spike_coins = 15
    else:
        sprites = state.multiworld.worlds[player].sprite_data["Mario Zone 3"]
        reachable_spike_coins = min(3, len({sprites[i]["sprite"] == "Claw Grabber" for i in (17, 18, 25)})
                                    + state.has("Mushroom", player) + state.has("Fire Flower", player)) * 5
    reachable_coins += reachable_spike_coins
    if not auto_scroll:
        reachable_coins += 10
    if state.has("Fire Flower", player):
        reachable_coins += 22
        if auto_scroll:
            reachable_coins -= 3 + reachable_spike_coins
    return coins <= reachable_coins


def mario_zone_4_boss(state, player):
    return has_pipe_right(state, player)


def mario_zone_4_coins(state, player, coins):
    return coins <= 60 or not is_auto_scroll(state, player, "Mario Zone 4")


def not_blocked_by_sharks(state, player):
    sharks = [state.multiworld.worlds[player].sprite_data["Turtle Zone 1"][i]["sprite"]
              for i in (27, 28)].count("Shark")
    if state.has("Carrot", player) or not sharks:
        return True
    if sharks == 2:
        return state.has_all(["Mushroom", "Fire Flower"], player)
    if sharks == 1:
        return state.has_any(["Mushroom", "Fire Flower"], player)
    return False


def turtle_zone_1_normal_exit(state, player):
    return not_blocked_by_sharks(state, player)


def turtle_zone_1_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Turtle Zone 1")
    reachable_coins = 30
    if not_blocked_by_sharks(state, player):
        reachable_coins += 13
        if auto_scroll:
            reachable_coins -= 1
    if state.has("Water Physics", player) or state.has("Carrot", player):
        reachable_coins += 10
    if state.has("Carrot", player):
        reachable_coins += 24
        if auto_scroll:
            reachable_coins -= 10
    return coins <= reachable_coins


def turtle_zone_2_normal_exit(state, player):
    return (has_pipe_up(state, player) and has_pipe_down(state, player) and has_pipe_right(state, player) and
            has_pipe_left(state, player) and state.has("Water Physics", player)
            and not is_auto_scroll(state, player, "Turtle Zone 2"))


def turtle_zone_2_secret_exit(state, player):
    return (has_pipe_up(state, player) and state.has("Water Physics", player)
            and not is_auto_scroll(state, player, "Turtle Zone 2"))


def turtle_zone_2_midway_bell(state, player):
    return ((state.has("Water Physics", player) and not is_auto_scroll(state, player, "Turtle Zone 2"))
            or state.has("Turtle Zone 2 Midway Bell", player))
    
    
def turtle_zone_2_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Turtle Zone 2")
    reachable_coins = 2
    if auto_scroll:
        if state.has("Water Physics", player):
            reachable_coins += 6
    else:
        reachable_coins += 2
        if state.has("Water Physics", player):
            reachable_coins += 20
        elif state.has("Turtle Zone 2 Midway Bell", player):
            reachable_coins += 4
        if (has_pipe_right(state, player) and has_pipe_down(state, player)
                and state.has_any(["Water Physics", "Turtle Zone 2 Midway Bell"], player)):
            reachable_coins += 1
            if has_pipe_left(state, player) and has_pipe_up(state, player):
                reachable_coins += 1
                if state.has("Water Physics", player):
                    reachable_coins += 1
    return coins <= reachable_coins


def turtle_zone_secret_course_normal_exit(state, player):
    return state.has_any(["Fire Flower", "Carrot"], player)


def turtle_zone_secret_course_coins(state, player, coins):
    reachable_coins = 53
    if state.has("Carrot", player):
        reachable_coins += 44
    elif state.has("Fire Flower", player):
        reachable_coins += 36  # was able to get 38, some leniency
    return coins <= reachable_coins


def turtle_zone_3_boss(state, player):
    return has_pipe_right(state, player)


def turtle_zone_3_coins(state, player, coins):
    return state.has_any(["Water Physics", "Mushroom", "Fire Flower", "Carrot"], player) or coins <= 51


def hippo_zone_normal_or_secret_exit(state, player):
    return (state.has_any(["Hippo Bubble", "Water Physics"], player)
            or (state.has("Carrot", player)
                and not is_auto_scroll(state, player, "Hippo Zone")))


def hippo_zone_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Hippo Zone")
    # This is all somewhat forgiving.
    reachable_coins = 4
    if auto_scroll:
        if state.has("Hippo Bubble", player):
            reachable_coins = 160
        elif state.has("Carrot", player):
            reachable_coins = 90
        elif state.has("Water Physics", player):
            reachable_coins = 28
    else:
        if state.has_any(["Water Physics", "Hippo Bubble", "Carrot"], player):
            reachable_coins += 108
            if state.has_any(["Mushroom", "Fire Flower", "Hippo Bubble"], player):
                reachable_coins += 6
        if state.has_all(["Fire Flower", "Water Physics"], player):
            reachable_coins += 1
        if state.has("Hippo Bubble", player):
            reachable_coins += 52
    return coins <= reachable_coins


def space_zone_1_normal_exit(state, player):
    # It is possible, however tricky, to beat the Moon Stage without Carrot or Space Physics.
    # However, it requires somewhat precisely jumping off enemies. Enemy shuffle may make this impossible.
    # Instead, I will just always make one or the other required, since it is difficult without them anyway.
    return state.has_any(["Space Physics", "Carrot"], player)


def space_zone_1_secret_exit(state, player):
    # One or the other is actually necessary for the secret exit.
    return state.has_any(["Space Physics", "Carrot"], player) and not is_auto_scroll(state, player, "Space Zone 1")


def space_zone_1_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Space Zone 1")
    if auto_scroll:
        reachable_coins = 12
        if state.has_any(["Carrot", "Space Physics"], player):
            reachable_coins += 20
        # If you have Space Physics, you can't make it up to the upper section. We have to assume you might have it,
        # so the coins up there must be out of logic if there is auto scrolling.
        if state.has("Space Physics", player):
            reachable_coins += 40
        return coins <= reachable_coins
    return (coins <= 21 or (coins <= 50 and state.has_any(["Mushroom", "Fire Flower"], player))
            or state.has_any(["Carrot", "Space Physics"], player))


def space_zone_2_midway_bell(state, player):
    return state.has_any(["Space Physics", "Space Zone 2 Midway Bell", "Mushroom", "Fire Flower", "Carrot"], player)


def space_zone_2_boss(state, player):
    if has_pipe_right(state, player):
        if state.has("Space Physics", player):
            return True
        if (state.has("Space Zone 2 Midway Bell", player)
                or not state.multiworld.worlds[player].options.shuffle_midway_bells):
            # Reaching the midway bell without space physics requires taking damage once. Reaching the end pipe from the
            # midway bell also requires taking damage once.
            if state.has_any(["Mushroom", "Fire Flower", "Carrot"], player):
                return True
        else:
            # With no midway bell, you'll have to be able to take damage twice.
            if state.has("Mushroom", player) and state.has_any(["Fire Flower", "Carrot"], player):
                return True
    return False


def space_zone_2_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Space Zone 2")
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


def space_zone_secret_course_coins(state, player, coins):
    return coins <= 96 or not is_auto_scroll(state, player, "Space Zone Secret Course")


def macro_zone_1_normal_exit(state, player):
    return has_pipe_down(state, player) or state.has("Macro Zone 1 Midway Bell", player)


def macro_zone_1_secret_exit(state, player):
    return state.has("Fire Flower", player) and has_pipe_up(state, player) and macro_zone_1_midway_bell(state, player)


def macro_zone_1_midway_bell(state, player):
    return has_pipe_down(state, player) or state.has("Macro Zone 1 Midway Bell", player)


def macro_zone_1_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Macro Zone 1")
    reachable_coins = 0
    if has_pipe_down(state, player):
        reachable_coins += 69
        if auto_scroll:
            if state.has_any(["Mushroom", "Fire Flower"], player):
                reachable_coins += 5
        else:
            reachable_coins += 9
            if state.has("Fire Flower", player):
                reachable_coins += 19
    elif state.has("Macro Zone 1 Midway Bell", player):
        if auto_scroll:
            reachable_coins += 16
            if state.has_any(["Mushroom", "Fire Flower"], player):
                reachable_coins += 5
        else:
            reachable_coins += 67
    return coins <= reachable_coins


def macro_zone_secret_course_coins(state, player, coins):
    return state.has_any(["Mushroom", "Fire Flower"], player)


def macro_zone_2_normal_exit(state, player):
    return (has_pipe_down(state, player) or state.has("Macro Zone 2 Midway Bell", player)) and state.has(
        "Water Physics", player) and has_pipe_up(state, player) and not is_auto_scroll(state, player, "Macro Zone 2")
    
    
def macro_zone_2_midway_bell(state, player):
    return ((has_pipe_down(state, player) and state.has("Water Physics", player))
            or state.has("Macro Zone 2 Midway Bell", player))


def macro_zone_2_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Macro Zone 2")
    if coins <= 27:
        return True
    if has_pipe_up(state, player) and state.has("Water Physics", player) and not auto_scroll:
        if has_pipe_down(state, player):
            return True
        if state.has("Macro Zone 2 Midway Bell", player):
            # Cannot return to the first section from the bell
            return coins <= 42
    return False


def macro_zone_3_normal_exit(state, player):
    return ((has_pipe_down(state, player) and has_pipe_up(state, player))
            or state.has("Macro Zone 3 Midway Bell", player))


def macro_zone_3_midway_bell(state, player):
    return macro_zone_3_normal_exit(state, player)


def macro_zone_3_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Macro Zone 3")
    reachable_coins = 7
    if not auto_scroll:
        reachable_coins += 17
    if has_pipe_up(state, player) and has_pipe_down(state, player):
        if auto_scroll:
            reachable_coins += 56
        else:
            return True
    elif has_pipe_up(state, player):
        if auto_scroll:
            reachable_coins += 12
        else:
            reachable_coins += 36
    elif has_pipe_down(state, player):
        reachable_coins += 18
    if state.has("Macro Zone 3 - Midway Bell", player):
        reachable_coins = max(reachable_coins, 30)
    return coins <= reachable_coins


def macro_zone_4_boss(state, player):
    return has_pipe_right(state, player)


def macro_zone_4_coins(state, player, coins):
    auto_scroll = is_auto_scroll(state, player, "Macro Zone 4")
    reachable_coins = 61
    if auto_scroll:
        reachable_coins -= 8
        if state.has("Carrot", player):
            reachable_coins += 6
    return coins <= reachable_coins


def marios_castle_wario(state, player):
    return (has_pipe_right(state, player) and 
           (has_pipe_left(state, player) or state.has("Mario's Castle Midway Bell", player)))


def marios_castle_midway_bell(state, player):
    return ((has_pipe_right(state, player) and has_pipe_left(state, player))
            or state.has("Mario's Castle Midway Bell", player))
