from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState


def dashes(state: CollectionState, player: int, has: int, needs: int) -> bool:
    dashes: int = needs - has
    return True if dashes <= 0 else state.has("Stamina Bar", player, dashes)


def walljumps(state: CollectionState, player: int, has: int, needs: int) -> bool:
    walljumps: int = needs - has
    return True if walljumps <= 0 else state.has("Wall Jump", player, walljumps)


def can_slide(state: CollectionState, player: int, option: bool) -> bool:
    return True if option else state.has("Slide", player)


def can_slam(state: CollectionState, player: int, option: bool) -> bool:
    return True if option else state.has("Slam", player)


def has_arm(state: CollectionState, player: int, option: bool) -> bool:
    return True if option else state.has("Feedbacker", player)


def rev0(state: CollectionState, player: int) -> bool:
    """Revolver - Piercer"""
    return state.has("Revolver - Piercer", player)


def rev0_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Revolver - Piercer"""
    return state.has_all({"Revolver - Piercer", "Secondary Fire - Piercer"}, player) if fire2 else rev0(state, player)


def rev1(state: CollectionState, player: int) -> bool:
    """Revolver - Sharpshooter"""
    return state.has("Revolver - Sharpshooter", player)


def rev1_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Revolver - Sharpshooter"""
    return state.has_all({"Revolver - Sharpshooter", "Secondary Fire - Sharpshooter"}, player) if fire2 else rev1(state, player)


def rev2(state: CollectionState, player: int) -> bool:
    """Revolver - Marksman"""
    return state.has("Revolver - Marksman", player)


def rev2_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Revolver - Marksman"""
    return state.has_all({"Revolver - Marksman", "Secondary Fire - Marksman"}, player) if fire2 else rev2(state, player)


def revalt(state: CollectionState, player: int):
    return state.has("Revolver - Alternate", player)


def sho0(state: CollectionState, player: int) -> bool:
    """Shotgun - Core Eject"""
    return state.has("Shotgun - Core Eject", player)


def sho0_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Shotgun - Core Eject"""
    return state.has_all({"Shotgun - Core Eject", "Secondary Fire - Core Eject"}, player) if fire2 else sho0(state, player)


def sho1(state: CollectionState, player: int) -> bool:
    """Shotgun - Pump Charge"""
    return state.has("Shotgun - Pump Charge", player)


def sho1_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Shotgun - Pump Charge"""
    return state.has_all({"Shotgun - Pump Charge", "Secondary Fire - Pump Charge"}, player) if fire2 else sho1(state, player)


def nai0(state: CollectionState, player: int) -> bool:
    """Nailgun - Attractor"""
    return state.has("Nailgun - Attractor", player)


def nai0_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Nailgun - Attractor"""
    return state.has_all({"Nailgun - Attractor", "Secondary Fire - Attractor"}, player) if fire2 else nai0(state, player)


def nai1(state: CollectionState, player: int) -> bool:
    """Nailgun - Overheat"""
    return state.has("Nailgun - Overheat", player)


def nai1_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Nailgun - Overheat"""
    return state.has_all({"Nailgun - Overheat", "Secondary Fire - Overheat"}, player) if fire2 else nai1(state, player)


def naialt(state: CollectionState, player: int):
    return state.has("Nailgun - Alternate", player)


def rai0(state: CollectionState, player: int) -> bool:
    """Railgun - Electric"""
    return state.has("Railgun - Electric", player)


def rai1(state: CollectionState, player: int) -> bool:
    """Railgun - Screwdriver"""
    return state.has("Railgun - Screwdriver", player)


def rai2(state: CollectionState, player: int) -> bool:
    """Railgun - Malicious"""
    return state.has("Railgun - Malicious", player)


def rock0(state: CollectionState, player: int) -> bool:
    """Rocket Launcher - Freezeframe"""
    return state.has("Rocket Launcher - Freezeframe", player)


def rock0_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Rocket Launcher - Freezeframe"""
    return state.has_all({"Rocket Launcher - Freezeframe", "Secondary Fire - Freezeframe"}, player) if fire2 else rock0(state, player)


def rock1(state: CollectionState, player: int) -> bool:
    """Rocket Launcher - S.R.S. Cannon"""
    return state.has("Rocket Launcher - S.R.S. Cannon", player)


def rock1_fire2(state: CollectionState, player: int, fire2: bool) -> bool:
    """Rocket Launcher - S.R.S. Cannon"""
    return state.has_all({"Rocket Launcher - S.R.S. Cannon", "Secondary Fire - S.R.S. Cannon"}, player) if fire2 else rock1(state, player)


def arm0(state: CollectionState, player: int) -> bool:
    """Feedbacker"""
    return state.has("Feedbacker", player)


def arm1(state: CollectionState, player: int) -> bool:
    """Knuckleblaster"""
    return state.has("Knuckleblaster", player)


def arm2(state: CollectionState, player: int) -> bool:
    """Whiplash"""
    return state.has("Whiplash", player)


def can_punch(state: CollectionState, player: int, option: bool) -> bool:
    return has_arm(state, player, option) or arm1(state, player)


def grab_item(state: CollectionState, player: int, option: bool) -> bool:
    return has_arm(state, player, option) or arm1(state, player) or arm2(state, player)


def can_proj_boost(state: CollectionState, player: int, arm: bool) -> bool:
    if arm:
        return (
            sho0(state, player)
            or sho1(state, player)
        )
    else:
        return (
            (
                sho0(state, player)
                or sho1(state, player)
            )
            and arm0(state, player)
        )


def slam_storage(state: CollectionState, player: int, slam: bool, has: int) -> bool:
    return (
        can_slam(state, player, slam)
        and walljumps(state, player, has, 1)
    )


def good_weapon(state: CollectionState, player: int, fire2: bool, arm: bool, slide: bool, dash: int) -> bool:
    return (
        (
            rev0(state, player)
            or rev1(state, player)
            or rev2(state, player)
            or sho0_fire2(state, player, fire2)
            or sho1_fire2(state, player, fire2)
            or can_proj_boost(state, player, arm)
        )
        and (
            can_slide(state, player, slide)
            or dashes(state, player, dash, 1)
        )
    )


def can_break_glass(state: CollectionState, player: int, fire2: bool, arm: bool) -> bool:
    return (
        rai0(state, player)
        or rai2(state, player)
        or rock0(state, player)
        or rock1(state, player)
        or arm1(state, player)
        or rev0_fire2(state, player, fire2)
        or rev1_fire2(state, player, fire2)
        or rev2_fire2(state, player, fire2)
        or (
            state.has_any({"Revolver - Piercer", "Revolver - Marksman", "Revolver - Sharpshooter"}, player)
            and revalt(state, player)
        )
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
    )


def can_break_walls(state: CollectionState, player: int, fire2: bool, arm: bool) -> bool:
    return (
        rai0(state, player)
        or rai2(state, player)
        or rock0(state, player)
        or rock1(state, player)
        or arm1(state, player)
        or nai1_fire2(state, player, fire2)
        or (
            state.has_any({"Revolver - Piercer", "Revolver - Marksman", "Revolver - Sharpshooter"}, player)
            and revalt(state, player)
        )
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
    )


def jump_general(state: CollectionState, player: int, slam: bool, fire2: bool, arm: bool, has: int, needs: int) -> bool:
    return (
        can_slam(state, player, slam)
        or walljumps(state, player, has, needs)
        or rock0(state, player)
        or rock1(state, player)
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
        or rai2(state, player)
    )


def challenge_0_1(state: CollectionState, player: int, fire2: bool, arm: bool) -> bool:
    return (
        rai0(state, player)
        or rai2(state, player)
        or rock0(state, player)
        or rock1(state, player)
        or rev0_fire2(state, player, fire2)
        or rev1_fire2(state, player, fire2)
        or rev2_fire2(state, player, fire2)
        or (
            state.has_any({"Revolver - Piercer", "Revolver - Marksman", "Revolver - Sharpshooter"}, player)
            and revalt(state, player)
        )
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
    )


def secret_0_2(state: CollectionState, player: int, slam: bool, fire2: bool, arm: bool, has: int) -> bool:
    return (
        walljumps(state, player, has, 3)
        or (
            walljumps(state, player, has, 2)
            and can_slam(state, player, slam)
        )
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
        or rai2(state, player)
        or rock0(state, player)
        or rock1(state, player)
    )


def challenge_0_3(state: CollectionState, player: int, slam: bool, fire2: bool, arm: bool, has: int) -> bool:
    return (
        slam_storage(state, player, slam, has)
        or (
            (
                sho0_fire2(state, player, fire2)
                or can_proj_boost(state, player, arm)
            )
            and walljumps(state, player, has, 3)
        )
        or (
            sho1_fire2(state, player, fire2)
            and can_proj_boost(state, player, arm)
        )
        or rock0_fire2(state, player, fire2)
        or rai2(state, player)
    )


def level_0_5(state: CollectionState, player: int, slide: bool, fire2: bool, has_walljumps: int, has_dashes: int) -> bool:
    return (
        (
            can_slide(state, player, slide)
            and (
                walljumps(state, player, has_walljumps, 2)
                or dashes(state, player, has_dashes, 2)
            )
        )
        or rock0_fire2(state, player, fire2)
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or rai2(state, player)
    )


def jump_1_1(state: CollectionState, player: int, slam: bool, fire2: bool, arm: bool) -> bool:
    return (
        can_slam(state, player, slam)
        or rock0(state, player)
        or rock1(state, player)
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
        or rai2(state, player)
    )


def secret1_2_1(state: CollectionState, player: int, fire2: bool, arm: bool, has: int) -> bool:
    return (
        dashes(state, player, has, 1)
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
        or rai2(state, player)
        or rock0(state, player)
        or rock1(state, player)
    )


def secret3_2_1(state: CollectionState, player: int, fire2: bool, has_walljumps: int, has_dashes: int) -> bool:
    return (
        (
            (
                dashes(state, player, has_dashes, 2)
                or (
                    walljumps(state, player, has_walljumps, 1)
                    and dashes(state, player, has_dashes, 1)
                )
            )
            and (
                sho1_fire2(state, player, fire2)
                or rai2(state, player)
            )
        )
        or rock0_fire2(state, player, fire2)
    )


def secret5_2_1(state: CollectionState, player: int, slam: bool, fire2: bool, arm: bool, has_walljumps: int, has_dashes: int) -> bool:
    return (
        can_slam(state, player, slam)
        or rai2(state, player)
        or rock0(state, player)
        or rock1(state, player)
        or (
            walljumps(state, player, has_walljumps, 1)
            and dashes(state, player, has_dashes, 1)
        )
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
    )


def challenge_2_1(state: CollectionState, player: int, slam: bool, fire2: bool, has_walljumps: int, has_dashes: int) -> bool:
    return (
        (
            dashes(state, player, has_dashes, 1)
            and walljumps(state, player, has_walljumps, 1)
            and can_slam(state, player, slam)
        )
        or rock0_fire2(state, player, fire2)
    )


def secret3_2_3(state: CollectionState, player: int, slam: bool, fire2: bool, has_walljumps: int, has_dashes: int) -> bool:
    return (
        can_slam(state, player, slam)
        or rai2(state, player)
        or (
            walljumps(state, player, has_walljumps, 2)
            or (
                walljumps(state, player, has_walljumps, 1)
                and dashes(state, player, has_dashes, 1)
            )
        )
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or rock0_fire2(state, player, fire2)
    )


def jump_3_2(state: CollectionState, player: int, slam: bool, fire2: bool, arm: bool, has_walljumps: int, has_dashes: int) -> bool:
    return (
        can_slam(state, player, slam)
        or rai2(state, player)
        or rock0(state, player)
        or rock1(state, player)
        or walljumps(state, player, has_walljumps, 1)
        or dashes(state, player, has_dashes, 1)
        or sho0_fire2(state, player, fire2)
        or sho1_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
    )


def challenge_4_1(state: CollectionState, player: int, slam: bool, fire2: bool, has_walljumps: int, has_dashes: int) -> bool:
    return (
        rock0_fire2(state, player, fire2)
        or (
            walljumps(state, player, has_walljumps, 2)
            and dashes(state, player, has_dashes, 2)
            and can_slam(state, player, slam)
        )
    )


def level_4_3(state: CollectionState, player: int, fire2: bool, arm: bool) -> bool:
    return (
        has_arm(state, player, arm)
        or arm1(state, player)
        or rai2(state, player)
        or sho0_fire2(state, player, fire2)
        or can_proj_boost(state, player, arm)
    )


def level_4_4(state: CollectionState, player: int, slam: bool, fire2: bool, skulls: bool, has_walljumps: int, has_dashes: int) -> bool:
    if skulls:
        return (
            (
                arm2(state, player)
                and state.has("Blue Skull (4-4)", player)
            )
            or (
                (
                    dashes(state, player, has_dashes, 1)
                    and walljumps(state, player, has_walljumps, 1)
                )
                or walljumps(state, player, has_walljumps, 2)
            )
            or can_slam(state, player, slam)
            or rock0_fire2(state, player, fire2)
        )
    else:
        return (
            arm2(state, player)
            or (
                (
                    dashes(state, player, has_dashes, 1)
                    and walljumps(state, player, has_walljumps, 1)
                )
                or walljumps(state, player, has_walljumps, 2)
            )
            or can_slam(state, player, slam)
            or rock0_fire2(state, player, fire2)
    )


def level_5_1(state: CollectionState, player: int, slam: bool, fire2: bool, has_walljumps: int, has_dashes: int) -> bool:
    return (
        (
            can_slam(state, player, slam)
            and walljumps(state, player, has_walljumps, 3)
            and dashes(state, player, has_dashes, 2)
        )
        or rock0_fire2(state, player, fire2)
        or arm2(state, player)
    )


def rules(ultrakillworld):
    world = ultrakillworld.multiworld
    player = ultrakillworld.player

    fire2 = world.randomize_secondary_fire[player]
    arm = world.start_with_arm[player]
    slam = world.start_with_slam[player]
    slide = world.start_with_slide[player]
    skulls = world.randomize_skulls[player]
    boss = world.boss_rewards[player]
    challenge = world.challenge_rewards[player]
    prank = world.p_rank_rewards[player]
    secretcompletion = world.include_secret_mission_completion[player]
    goal = world.goal[player]

    dash: int = world.starting_stamina[player].value
    walljump: int = world.starting_walljumps[player].value

    # goal
    set_rule(world.get_entrance("To " + ultrakillworld.goal_name, player), \
        lambda state: state.has("Level Completed", player, \
            world.goal_requirement[player].value))


    # level entrances
    set_rule(world.get_entrance("To shop", player),
        lambda state: (
            state.has_group("levels", player)
            or state.has_group("layers", player)
        ))
    set_rule(world.get_entrance("To 0-2", player),
        lambda state: (
            state.has("0-2: THE MEATGRINDER", player)
            or state.has("OVERTURE: THE MOUTH OF HELL", player)
        ))
    set_rule(world.get_entrance("To 0-3", player),
        lambda state: (
            state.has("0-3: DOUBLE DOWN", player)
            or state.has("OVERTURE: THE MOUTH OF HELL", player)
        ))
    set_rule(world.get_entrance("To 0-4", player),
        lambda state: (
            state.has("0-4: A ONE-MACHINE ARMY", player)
            or state.has("OVERTURE: THE MOUTH OF HELL", player)
        ))
    set_rule(world.get_entrance("To 0-5", player),
        lambda state: (
            state.has("0-5: CERBERUS", player)
            or state.has("OVERTURE: THE MOUTH OF HELL", player)
        ))
    set_rule(world.get_entrance("To 1-1", player),
        lambda state: (
            state.has("1-1: HEART OF THE SUNRISE", player)
            or state.has("LAYER 1: LIMBO", player)
        ))
    set_rule(world.get_entrance("To 1-2", player),
        lambda state: (
            state.has("1-2: THE BURNING WORLD", player)
            or state.has("LAYER 1: LIMBO", player)
        ))
    set_rule(world.get_entrance("To 1-3", player),
        lambda state: (
            state.has("1-3: HALLS OF SACRED REMAINS", player)
            or state.has("LAYER 1: LIMBO", player)
        ))
    if goal.value != 0:
        set_rule(world.get_entrance("To 1-4", player),
            lambda state: (
                state.has("1-4: CLAIR DE LUNE", player)
                or state.has("LAYER 1: LIMBO", player)
            ))
    set_rule(world.get_entrance("To 2-1", player),
        lambda state: (
            state.has("2-1: BRIDGEBURNER", player)
            or state.has("LAYER 2: LUST", player)
        ))
    set_rule(world.get_entrance("To 2-2", player),
        lambda state: (
            state.has("2-2: DEATH AT 20,000 VOLTS", player)
            or state.has("LAYER 2: LUST", player)
        ))
    set_rule(world.get_entrance("To 2-3", player),
        lambda state: (
            state.has("2-3: SHEER HEART ATTACK", player)
            or state.has("LAYER 2: LUST", player)
        ))
    if goal.value != 1:
        set_rule(world.get_entrance("To 2-4", player),
            lambda state: (
                state.has("2-4: COURT OF THE CORPSE KING", player)
                or state.has("LAYER 2: LUST", player)
            ))
    set_rule(world.get_entrance("To 3-1", player),
        lambda state: (
            state.has("3-1: BELLY OF THE BEAST", player)
            or state.has("LAYER 3: GLUTTONY", player)
        ))
    if goal.value != 2:
        set_rule(world.get_entrance("To 3-2", player),
            lambda state: (
                state.has("3-2: IN THE FLESH", player)
                or state.has("LAYER 3: GLUTTONY", player)
            ))
    set_rule(world.get_entrance("To 4-1", player),
        lambda state: (
            state.has("4-1: SLAVES TO POWER", player)
            or state.has("LAYER 4: GREED", player)
        ))
    set_rule(world.get_entrance("To 4-2", player),
        lambda state: (
            state.has("4-2: GOD DAMN THE SUN", player)
            or state.has("LAYER 4: GREED", player)
        ))
    set_rule(world.get_entrance("To 4-3", player),
        lambda state: (
            state.has("4-3: A SHOT IN THE DARK", player)
            or state.has("LAYER 4: GREED", player)
        ))
    if goal.value != 3:
        set_rule(world.get_entrance("To 4-4", player),
            lambda state: (
                state.has("4-4: CLAIR DE SOLEIL", player)
                or state.has("LAYER 4: GREED", player)
            ))
    set_rule(world.get_entrance("To 5-1", player),
        lambda state: (
            state.has("5-1: IN THE WAKE OF POSEIDON", player)
            or state.has("LAYER 5: WRATH", player)
        ))
    set_rule(world.get_entrance("To 5-2", player),
        lambda state: (
            state.has("5-2: WAVES OF THE STARLESS SEA", player)
            or state.has("LAYER 5: WRATH", player)
        ))
    set_rule(world.get_entrance("To 5-3", player),
        lambda state: (
            state.has("5-3: SHIP OF FOOLS", player)
            or state.has("LAYER 5: WRATH", player)
        ))
    if goal.value != 4:
        set_rule(world.get_entrance("To 5-4", player),
            lambda state: (
                state.has("5-4: LEVIATHAN", player)
                or state.has("LAYER 5: WRATH", player)
            ))
    set_rule(world.get_entrance("To 6-1", player),
        lambda state: (
            state.has("6-1: CRY FOR THE WEEPER", player)
            or state.has("LAYER 6: HERESY", player)
        ))
    if goal.value != 5:
        set_rule(world.get_entrance("To 6-2", player),
            lambda state: (
                state.has("6-2: AESTHETICS OF HATE", player)
                or state.has("LAYER 6: HERESY", player)
            ))

    # secret mission entrances
    set_rule(world.get_entrance("To 0-S", player),
        lambda state: (
            secret_0_2(state, player, slam, fire2, arm, walljump)
            and grab_item(state, player, arm)
        ))
    if skulls:
        add_rule(world.get_entrance("To 0-S", player),
            lambda state: state.has("Blue Skull (0-2)", player))
    set_rule(world.get_entrance("To 1-S", player),
        lambda state: rev2_fire2(state, player, fire2))
    set_rule(world.get_entrance("To 2-S", player),
        lambda state: (
            secret3_2_3(state, player, slam, fire2, walljump, dash)
            and can_slide(state, player, slide)
        ))
    if skulls:
        add_rule(world.get_entrance("To 2-S", player),
            lambda state: state.has("Blue Skull (2-3)", player))
    set_rule(world.get_entrance("To 4-S", player),
        lambda state: (
            (
                jump_general(state, player, slam, fire2, arm, walljump, 2)
                or rev1_fire2(state, player, fire2)
            )
            and grab_item(state, player, arm)
        ))
    set_rule(world.get_entrance("To 5-S", player),
        lambda state: (
            can_slide(state, player, slide)
            and level_5_1(state, player, slam, fire2, walljump, dash)
            and grab_item(state, player, arm)
        ))
    if skulls:
        add_rule(world.get_entrance("To 5-S", player),
            lambda state: state.has("Blue Skull (5-1)", player, 3))



    # 0-1
    set_rule(world.get_location("0-1: Secret #1", player),
        lambda state: can_break_glass(state, player, fire2, arm))

    set_rule(world.get_location("0-1: Secret #3", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))
    set_rule(world.get_location("0-1: Secret #4", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))

    if challenge:
        set_rule(world.get_location("0-1: Get 5 kills with a single glass panel", player),
            lambda state: challenge_0_1(state, player, fire2, arm))

    if prank:
        set_rule(world.get_location("0-1: Perfect Rank", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash) or \
                state.has("Knuckleblaster", player))


    # 0-2
    set_rule(world.get_location("0-2: Secret #3", player),
        lambda state: (
            rock0_fire2(state, player, fire2)
            or sho0_fire2(state, player, fire2)
            or can_proj_boost(state, player, arm)
            or (
                walljumps(state, player, walljump, 1)
                and dashes(state, player, dash, 2)
            )
        ))


    set_rule(world.get_location("0-2: Secret #4", player),
        lambda state: can_slide(state, player, slide))
    if challenge:
        set_rule(world.get_location("0-2: Beat the secret encounter", player),
            lambda state: (
                can_slide(state, player, slide)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))

    if prank:
        add_rule(world.get_location("0-2: Perfect Rank", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))


    # 0-S
    if skulls and secretcompletion:
        add_rule(world.get_location("Cleared 0-S", player),
            lambda state: state.has_all({"Blue Skull (0-2)", "Blue Skull (0-S)", "Red Skull (0-S)"}, player))


    # 0-3
    set_rule(world.get_location("0-3: Secret #1", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))
    set_rule(world.get_location("0-3: Secret #2", player),
        lambda state: (
            (
                jump_general(state, player, slam, fire2, arm, walljump, 2)
                or dashes(state, player, dash, 1)
            )
            and can_break_walls(state, player, fire2, arm)
        ))

    set_rule(world.get_location("0-3: Secret #3", player),
        lambda state: can_break_walls(state, player, fire2, arm))
    set_rule(world.get_location("Cleared 0-3", player),
        lambda state: (
            can_break_walls(state, player, fire2, arm)
            or challenge_0_3(state, player, slam, fire2, arm, walljump)
        ))

    set_rule(world.get_location("0-3: Weapon", player),
        lambda state: good_weapon(state, player, fire2, arm, slide, dash))

    if challenge:
        set_rule(world.get_location("0-3: Kill only 1 enemy", player),
            lambda state: challenge_0_3(state, player, slam, fire2, arm, walljump))

    if prank:
        add_rule(world.get_location("0-3: Perfect Rank", player),
            lambda state: (
                can_break_walls(state, player, fire2, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))

    # 0-4
    set_rule(world.get_location("0-4: Secret #1", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))

    set_rule(world.get_location("0-4: Secret #2", player),
        lambda state: can_break_glass(state, player, fire2, arm))

    set_rule(world.get_location("0-4: Secret #3", player),
        lambda state: can_slide(state, player, slide))
    if challenge:
        set_rule(world.get_location("0-4: Slide uninterrupted for 17 seconds", player),
            lambda state: can_slide(state, player, slide))

    if prank:
        set_rule(world.get_location("0-4: Perfect Rank", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))


    # 0-5
    set_rule(world.get_location("Cleared 0-5", player),
        lambda state: level_0_5(state, player, slide, fire2, walljump, dash))
    
    if boss > 0:
        set_rule(world.get_location("0-5: Defeat the Cerberi", player),
            lambda state: level_0_5(state, player, slide, fire2, walljump, dash))

    if challenge:
        set_rule(world.get_location("0-5: Don't inflict fatal damage to any enemy", player),
            lambda state: level_0_5(state, player, slide, fire2, walljump, dash))

    if prank:
        set_rule(world.get_location("0-5: Perfect Rank", player),
            lambda state: (
                level_0_5(state, player, slide, fire2, walljump, dash)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))


    # 1-1
    set_rule(world.get_location("1-1: Secret #5", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))

    set_rule(world.get_location("1-1: Weapon", player),
        lambda state: grab_item(state, player, arm))
    set_rule(world.get_location("1-1: Secret #3", player),
        lambda state: grab_item(state, player, arm))
    set_rule(world.get_location("1-1: Secret #4", player),
        lambda state: grab_item(state, player, arm))
    add_rule(world.get_location("1-1: Secret #5", player),
        lambda state: grab_item(state, player, arm))
    if prank:
        set_rule(world.get_location("1-1: Perfect Rank", player),
            lambda state: grab_item(state, player, arm))

    if skulls:
        set_rule(world.get_location("Cleared 1-1", player),
            lambda state: (
                (
                    state.has_all({"Red Skull (1-1)", "Blue Skull (1-1)"}, player)
                    and grab_item(state, player, arm)
                )
                or rev2_fire2(state, player, fire2)
            ))

        add_rule(world.get_location("1-1: Weapon", player),
            lambda state: state.has("Red Skull (1-1)", player))
        add_rule(world.get_location("1-1: Secret #3", player),
            lambda state: state.has("Red Skull (1-1)", player))
        add_rule(world.get_location("1-1: Secret #4", player),
            lambda state: state.has("Red Skull (1-1)", player))
        add_rule(world.get_location("1-1: Secret #5", player),
            lambda state: state.has_all({"Red Skull (1-1)", "Blue Skull (1-1)"}, player))
        if prank:
            set_rule(world.get_location("1-1: Perfect Rank", player),
                lambda state: state.has_all({"Red Skull (1-1)", "Blue Skull (1-1)"}, player))
    else:
        set_rule(world.get_location("Cleared 1-1", player),
            lambda state: (
                grab_item(state, player, arm)
                or rev2_fire2(state, player, fire2)
            ))


    if challenge:
        set_rule(world.get_location("1-1: Complete the level in under 10 seconds", player),
            lambda state: rev2_fire2(state, player, fire2))

    if prank:
        add_rule(world.get_location("1-1: Perfect Rank", player),
            lambda state: (
                good_weapon(state, player, fire2, arm, slide, dash)
                and grab_item(state, player, arm)
            ))


    # 1-2
    if challenge:
        set_rule(world.get_location("1-2: Do not pick up any skulls", player),
            lambda state: rai0(state, player))

    set_rule(world.get_location("1-2: Secret #3", player),
        lambda state: grab_item(state, player, arm))

    if skulls:
        add_rule(world.get_location("1-2: Secret #3", player),
            lambda state: state.has("Blue Skull (1-2)", player))
        set_rule(world.get_location("1-2: Secret #4", player),
            lambda state: (
                state.has_all({"Blue Skull (1-2)", "Red Skull (1-2)"}, player)
                and grab_item(state, player, arm)
                or rai0(state, player)
            ))
        set_rule(world.get_location("1-2: Secret #5", player),
            lambda state: (
                state.has_all({"Blue Skull (1-2)", "Red Skull (1-2)"}, player)
                and grab_item(state, player, arm)
                or rai0(state, player)
            ))
        set_rule(world.get_location("Cleared 1-2", player),
            lambda state: (
                state.has_all({"Blue Skull (1-2)", "Red Skull (1-2)"}, player)
                and grab_item(state, player, arm)
                or rai0(state, player)
            ))
        if boss == 2:
            set_rule(world.get_location("1-2: Defeat the Very Cancerous Rodent", player),
                lambda state: (
                    (
                        state.has_all({"Blue Skull (1-2)", "Red Skull (1-2)"}, player)
                        and grab_item(state, player, arm)
                        or rai0(state, player)
                    )
                    and can_break_walls(state, player, fire2, arm)
                ))
        if prank:
            set_rule(world.get_location("1-2: Perfect Rank", player),
                lambda state: (
                    state.has_all({"Blue Skull (1-2)", "Red Skull (1-2)"}, player)
                    and grab_item(state, player, arm)
                ))
    else:
        set_rule(world.get_location("1-2: Secret #4", player),
            lambda state: (
                grab_item(state, player, arm)
                or rai0(state, player)
            ))
        set_rule(world.get_location("1-2: Secret #5", player),
            lambda state: (
                grab_item(state, player, arm)
                or rai0(state, player)
            ))
        set_rule(world.get_location("Cleared 1-2", player),
            lambda state: (
                grab_item(state, player, arm)
                or rai0(state, player)
            ))
        if boss == 2:
            set_rule(world.get_location("1-2: Defeat the Very Cancerous Rodent", player),
                lambda state: (
                    (
                        grab_item(state, player, arm)
                        or rai0(state, player)
                    )
                    and can_break_walls(state, player, fire2, arm)
                ))
        if prank:
            set_rule(world.get_location("1-2: Perfect Rank", player),
                lambda state: (
                    grab_item(state, player, arm)
                    or rai0(state, player)
                ))

    if prank:
        add_rule(world.get_location("1-2: Perfect Rank", player),
            lambda state: (
                good_weapon(state, player, fire2, arm, slide, dash)
                and grab_item(state, player, arm)
            ))


    # 1-3        
    set_rule(world.get_location("1-3: Secret #1", player),
        lambda state: can_break_glass(state, player, fire2, arm))

    set_rule(world.get_location("1-3: Secret #4", player),
        lambda state: can_slide(state, player, slide))
    set_rule(world.get_location("1-3: Secret #5", player),
        lambda state: can_slide(state, player, slide))

    if skulls:
        set_rule(world.get_location("Cleared 1-3", player),
            lambda state: state.has_any({"Red Skull (1-3)", "Blue Skull (1-3)"}, player))
        if prank:
            set_rule(world.get_location("1-3: Perfect Rank", player),
                lambda state: state.has_any({"Red Skull (1-3)", "Blue Skull (1-3)"}, player))
        if challenge:
            set_rule(world.get_location("1-3: Beat the secret encounter", player),
                lambda state: state.has_all({"Red Skull (1-3)", "Blue Skull (1-3)"}, player))

    add_rule(world.get_location("Cleared 1-3", player),
        lambda state: grab_item(state, player, arm))
    if prank:
        add_rule(world.get_location("1-3: Perfect Rank", player),
            lambda state: (
                grab_item(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))
    if challenge:
        add_rule(world.get_location("1-3: Beat the secret encounter", player),
            lambda state: (
                grab_item(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))


    # 1-4
    set_rule(world.get_location("1-4: Secret Weapon", player),
        lambda state: state.can_reach(world.get_region("1-1: HEART OF THE SUNRISE", player)) and \
            state.can_reach(world.get_region("1-2: THE BURNING WORLD", player)) and \
                state.can_reach(world.get_region("1-3: HALLS OF SACRED REMAINS", player)))

    add_rule(world.get_location("1-4: Secret Weapon", player),
        lambda state: (
            jump_1_1(state, player, slam, fire2, arm)
            and can_break_glass(state, player, fire2, arm)
            and can_break_walls(state, player, fire2, arm)
        ))

    if skulls:
        add_rule(world.get_location("1-4: Secret Weapon", player),
            lambda state: (
                state.has_all({"Red Skull (1-1)", "Blue Skull (1-1)", "Blue Skull (1-3)", "Red Skull (1-3)"}, player)
                and (
                    state.has_all({"Blue Skull (1-2)", "Red Skull (1-2)"}, player) or \
                    rai0(state, player)
                )
            ))

    add_rule(world.get_location("1-4: Secret Weapon", player),
        lambda state: grab_item(state, player, arm))

    if boss > 0:
        set_rule(world.get_location("1-4: Defeat V2", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))

    if challenge and goal != 0:
        add_rule(world.get_location("1-4: Do not pick up any skulls", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))

    if prank and goal != 0:
        add_rule(world.get_location("1-4: Perfect Rank", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))


    # 2-1
    set_rule(world.get_location("2-1: Secret #1", player),
        lambda state: (
            secret1_2_1(state, player, fire2, arm, dash)
            and can_break_walls(state, player, fire2, arm)
        ))

    set_rule(world.get_location("2-1: Secret #3", player),
        lambda state: secret3_2_1(state, player, fire2, walljump, dash))

    set_rule(world.get_location("2-1: Secret #5", player),
        lambda state: secret5_2_1(state, player, slam, fire2, arm, walljump, dash))
    set_rule(world.get_location("Cleared 2-1", player),
        lambda state: secret5_2_1(state, player, slam, fire2, arm, walljump, dash))

    if challenge:
        set_rule(world.get_location("2-1: Don't open any normal doors", player),
            lambda state: (
                challenge_2_1(state, player, slam, fire2, walljump, dash)
                and can_break_walls(state, player, fire2, arm)
            ))

    if prank:
        set_rule(world.get_location("2-1: Perfect Rank", player),
            lambda state: (
                secret5_2_1(state, player, slam, fire2, arm, walljump, dash)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))            

    # 2-2
    set_rule(world.get_location("2-2: Secret #4", player),
        lambda state: can_slide(state, player, slide))

    set_rule(world.get_location("2-2: Secret #2", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))
    set_rule(world.get_location("2-2: Secret #3", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 2))

    set_rule(world.get_location("2-2: Secret #5", player),
        lambda state: can_break_walls(state, player, fire2, arm))

    if challenge:
        set_rule(world.get_location("2-2: Beat the level in under 60 seconds", player),
            lambda state: (
                can_slide(state, player, slide)
                or dashes(state, player, dash, 2)
            ))

    if prank:
        add_rule(world.get_location("2-2: Perfect Rank", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))


    # 2-3
    set_rule(world.get_location("2-3: Secret #2", player),
        lambda state: can_slide(state, player, slide))
    set_rule(world.get_location("2-3: Secret #3", player),
        lambda state: (
            grab_item(state, player, arm)
            and secret3_2_3(state, player, slam, fire2, walljump, dash)
        ))
    set_rule(world.get_location("2-3: Secret #4", player),
        lambda state: grab_item(state, player, arm))
    set_rule(world.get_location("2-3: Secret #5", player),
        lambda state: can_slide(state, player, slide))
    set_rule(world.get_location("Cleared 2-3", player),
        lambda state: grab_item(state, player, arm))

    if skulls:
        add_rule(world.get_location("2-3: Secret #3", player),
            lambda state: state.has("Blue Skull (2-3)", player))
        add_rule(world.get_location("2-3: Secret #4", player),
            lambda state: state.has("Blue Skull (2-3)", player))
        add_rule(world.get_location("Cleared 2-3", player),
            lambda state: (
                (
                    secret3_2_3(state, player, slam, fire2, walljump, dash)
                    and state.has("Blue Skull (2-3)", player)
                    and can_slide(state, player, slide)
                )
                or state.has_all({"Blue Skull (2-3)", "Red Skull (2-3)"}, player)
            ))
        if challenge:
            set_rule(world.get_location("2-3: Don't touch any water", player),
                lambda state: state.has_all({"Blue Skull (2-3)", "Red Skull (2-3)"}, player))
        if prank:
            set_rule(world.get_location("2-3: Perfect Rank", player),
                lambda state: state.has_all({"Blue Skull (2-3)", "Red Skull (2-3)"}, player))

    if challenge:
        add_rule(world.get_location("2-3: Don't touch any water", player),
            lambda state: (
                secret3_2_3(state, player, slam, fire2, walljump, dash)
                and can_slide(state, player, slide)
                and grab_item(state, player, arm)
            ))

    if prank:
        add_rule(world.get_location("2-3: Perfect Rank", player),
            lambda state: (
                good_weapon(state, player, fire2, arm, slide, dash)
                and grab_item(state, player, arm)
            ))


    # 2-4
    if skulls:
        set_rule(world.get_location("Cleared 2-4", player),
            lambda state: state.has_all({"Blue Skull (2-4)", "Red Skull (2-4)"}, player))
        if boss > 0 and goal != 1:
            set_rule(world.get_location("2-4: Defeat the Corpse of King Minos", player),
                lambda state: state.has_all({"Blue Skull (2-4)", "Red Skull (2-4)"}, player))
        if challenge and goal != 1:
            add_rule(world.get_location("2-4: Parry a punch", player),
                lambda state: state.has_all({"Blue Skull (2-4)", "Red Skull (2-4)"}, player))
        if prank and goal != 1:
            add_rule(world.get_location("2-4: Perfect Rank", player),
                lambda state: state.has_all({"Blue Skull (2-4)", "Red Skull (2-4)"}, player))

    add_rule(world.get_location("Cleared 2-4", player),
        lambda state: grab_item(state, player, arm))
    if boss > 0 and goal != 1:
        add_rule(world.get_location("2-4: Defeat the Corpse of King Minos", player),
            lambda state: (
                grab_item(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))
    if challenge and goal != 1:
        add_rule(world.get_location("2-4: Parry a punch", player),
            lambda state: (
                grab_item(state, player, arm)
                and has_arm(state, player, arm)
            ))
    if prank and goal != 1:
        add_rule(world.get_location("2-4: Perfect Rank", player),
            lambda state: (
                grab_item(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))


    # 3-1
    set_rule(world.get_location("3-1: Secret #4", player),
        lambda state: can_slide(state, player, slide))

    if prank:
        add_rule(world.get_location("3-1: Perfect Rank", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))


    # 3-2
    set_rule(world.get_location("Cleared 3-2", player),
        lambda state: (
            can_slide(state, player, slide)
            and jump_3_2(state, player, slam, fire2, arm, walljump, dash)
        ))
    
    if boss > 0 and goal != 2:
        set_rule(world.get_location("3-2: Defeat Gabriel", player),
            lambda state: (
                can_slide(state, player, slide)
                and jump_3_2(state, player, slam, fire2, arm, walljump, dash)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))

    if challenge and goal != 2:
        set_rule(world.get_location("3-2: Drop Gabriel in a pit", player),
            lambda state: (
                can_slide(state, player, slide)
                and jump_3_2(state, player, slam, fire2, arm, walljump, dash)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))

    if prank and goal != 2:
        set_rule(world.get_location("3-2: Perfect Rank", player),
            lambda state: (
                can_slide(state, player, slide)
                and jump_3_2(state, player, slam, fire2, arm, walljump, dash)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))


    # 4-1
    set_rule(world.get_location("4-1: Secret #1", player),
        lambda state: (
            dashes(state, player, dash, 1)
            or rock0_fire2(state, player, fire2)
        ))

    set_rule(world.get_location("4-1: Secret #4", player),
        lambda state: (
            (
                walljumps(state, player, walljump, 2) and \
                state.has("Slam", player)
            )
            or rock0_fire2(state, player, fire2)
            or sho1_fire2(state, player, fire2)
            or rai2(state, player)
        ))

    set_rule(world.get_location("4-1: Secret #2", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))
    set_rule(world.get_location("4-1: Secret #3", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))
    set_rule(world.get_location("4-1: Secret #5", player),
        lambda state: jump_general(state, player, slam, fire2, arm, walljump, 1))

    if challenge:
        set_rule(world.get_location("4-1: Don't activate any enemies", player),
            lambda state: challenge_4_1(state, player, slam, fire2, walljump, dash))

    if prank:
        add_rule(world.get_location("4-1: Perfect Rank", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))


    # 4-2
    set_rule(world.get_location("4-2: Secret #4", player),
        lambda state: (
            jump_general(state, player, slam, fire2, arm, walljump, 2)
            or rev1_fire2(state, player, fire2)
        ))

    if skulls:
        set_rule(world.get_location("Cleared 4-2", player),
            lambda state: (
                jump_general(state, player, slam, fire2, arm, walljump, 2)
                or rev1_fire2(state, player, fire2)
                or (
                    state.has_all({"Blue Skull (4-2)", "Red Skull (4-2)"}, player)
                    and grab_item(state, player, arm)
                )
            ))
        if challenge:
            set_rule(world.get_location("4-2: Kill the Insurrectionist in under 10 seconds", player),
                lambda state: state.has_all({"Blue Skull (4-2)", "Red Skull (4-2)"}, player))
        if prank:
            set_rule(world.get_location("4-2: Perfect Rank", player),
                lambda state: state.has_all({"Blue Skull (4-2)", "Red Skull (4-2)"}, player))
    else:
        set_rule(world.get_location("Cleared 4-2", player),
            lambda state: (
                jump_general(state, player, slam, fire2, arm, walljump, 2)
                or rev1_fire2(state, player, fire2)
                or grab_item(state, player, arm)
            ))

    if challenge:
        add_rule(world.get_location("4-2: Kill the Insurrectionist in under 10 seconds", player),
            lambda state: grab_item(state, player, arm))

    if prank:
        add_rule(world.get_location("4-2: Perfect Rank", player),
            lambda state: (
                grab_item(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))


    # 4-3
    if challenge:
        add_rule(world.get_location("4-3: Don't pick up the torch", player),
        lambda state: (
            (
                sho0_fire2(state, player, fire2)
                or can_proj_boost(state, player, arm)
            )
            and grab_item(state, player, arm)
        ))

    add_rule(world.get_location("4-3: Secret #1", player),
        lambda state: level_4_3(state, player, fire2, arm))
    add_rule(world.get_location("4-3: Secret #2", player),
        lambda state: (
            level_4_3(state, player, fire2, arm)
            and can_slide(state, player, slide)
        ))
    add_rule(world.get_location("4-3: Secret #3", player),
        lambda state: level_4_3(state, player, fire2, arm))
    add_rule(world.get_location("4-3: Secret #4", player),
        lambda state: (
            level_4_3(state, player, fire2, arm)
            and can_break_walls(state, player, fire2, arm)
        ))
    add_rule(world.get_location("4-3: Secret #5", player),
        lambda state: (
            level_4_3(state, player, fire2, arm)
            and can_slide(state, player, slide)
        ))
    add_rule(world.get_location("Cleared 4-3", player),
        lambda state: (
            level_4_3(state, player, fire2, arm)
            and grab_item(state, player, arm)
        ))
    
    if boss == 2:
        set_rule(world.get_location("4-3: Defeat the Mysterious Druid Knight (& Owl)", player),
            lambda state: (
                level_4_3(state, player, fire2, arm)
                and can_break_walls(state, player, fire2, arm)
                and can_punch(state, player, arm)
            ))
    
    if prank:
        add_rule(world.get_location("4-3: Perfect Rank", player),
            lambda state: (
                level_4_3(state, player, fire2, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
                and grab_item(state, player, arm)
            ))

    if skulls:
        if boss == 2:
            add_rule(world.get_location("4-3: Defeat the Mysterious Druid Knight (& Owl)", player),
                lambda state: state.has("Blue Skull (4-3)", player))
        if challenge:
            add_rule(world.get_location("4-3: Don't pick up the torch", player),
                lambda state: state.has("Blue Skull (4-3)", player))


    # 4-4
    set_rule(world.get_location("Cleared 4-4", player),
        lambda state: (
            arm2(state, player)
            and level_4_4(state, player, slam, fire2, skulls, walljump, dash)
        ))
    
    set_rule(world.get_location("4-4: V2's Other Arm", player),
        lambda state: (
            level_4_4(state, player, slam, fire2, skulls, walljump, dash)
            and good_weapon(state, player, fire2, arm, slide, dash)
        ))
    
    if boss > 0 and goal != 3:
        set_rule(world.get_location("4-4: Defeat V2", player),
            lambda state: (
                level_4_4(state, player, slam, fire2, skulls, walljump, dash)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))
    
    if prank and goal != 3:
        set_rule(world.get_location("4-4: Perfect Rank", player),
            lambda state: (
                arm2(state, player)
                and level_4_4(state, player, slam, fire2, skulls, walljump, dash)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))

    if challenge and goal != 3:
        set_rule(world.get_location("4-4: Reach the boss room in 18 seconds", player),
            lambda state: (
                arm2(state, player)
                and dashes(state, player, dash, 3)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))

    set_rule(world.get_location("4-4: Secret Weapon", player),
        lambda state: (
            arm2(state, player)
            and rai0(state, player)
        ))

    if skulls:
        add_rule(world.get_location("4-4: Secret Weapon", player),
            lambda state: state.has("Blue Skull(4-4)", player))
        if challenge and goal != 3:
            add_rule(world.get_location("4-4: Reach the boss room in 18 seconds", player),
                lambda state: state.has("Blue Skull (4-4)", player))


    # 5-1
    if challenge:
        add_rule(world.get_location("5-1: Don't touch any water", player),
            lambda state: (
                arm2(state, player)
                or rock0_fire2(state, player, fire2)
            ))

    add_rule(world.get_location("5-1: Secret #1", player),
        lambda state: (
            can_slide(state, player, slide)
            and level_5_1(state, player, slam, fire2, walljump, dash)
        ))
    add_rule(world.get_location("5-1: Secret #2", player),
        lambda state: (
            can_slide(state, player, slide)
            and level_5_1(state, player, slam, fire2, walljump, dash)
        ))
    add_rule(world.get_location("5-1: Secret #3", player),
        lambda state: (
            can_slide(state, player, slide)
            and level_5_1(state, player, slam, fire2, walljump, dash)
        ))
    add_rule(world.get_location("5-1: Secret #4", player),
        lambda state: (
            can_slide(state, player, slide)
            and level_5_1(state, player, slam, fire2, walljump, dash)
        ))
    add_rule(world.get_location("5-1: Secret #5", player),
        lambda state: (
            can_slide(state, player, slide)
            and level_5_1(state, player, slam, fire2, walljump, dash)
            and grab_item(state, player, arm)
        ))
    add_rule(world.get_location("Cleared 5-1", player),
        lambda state: (
            can_slide(state, player, slide)
            and level_5_1(state, player, slam, fire2, walljump, dash)
            and grab_item(state, player, arm)
        ))
    if challenge:
        add_rule(world.get_location("5-1: Don't touch any water", player),
            lambda state: (
                can_slide(state, player, slide)
                and level_5_1(state, player, slam, fire2, walljump, dash)
                and grab_item(state, player, arm)
            ))
    if prank:
        add_rule(world.get_location("5-1: Perfect Rank", player),
            lambda state: (
                can_slide(state, player, slide)
                and level_5_1(state, player, slam, fire2, walljump, dash)
                and grab_item(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))

    if skulls:
        add_rule(world.get_location("5-1: Secret #5", player),
            lambda state: state.has("Blue Skull (5-1)", player, 3))
        add_rule(world.get_location("Cleared 5-1", player),
            lambda state: state.has("Blue Skull (5-1)", player, 3))
        if challenge:
            add_rule(world.get_location("5-1: Don't touch any water", player),
                lambda state: state.has("Blue Skull (5-1)", player, 3))
        if prank:
            add_rule(world.get_location("5-1: Perfect Rank", player),
                lambda state: state.has("Blue Skull (5-1)", player, 3))


    # 5-2
    add_rule(world.get_location("5-2: Secret #1", player),
        lambda state: (
            can_slide(state, player, slide)
            or rock0_fire2(state, player, fire2)
        ))

    add_rule(world.get_location("5-2: Secret #2", player),
        lambda state: (
            can_slam(state, player, slam)
            or dashes(state, player, dash, 1)
        ))
    add_rule(world.get_location("5-2: Secret #3", player),
        lambda state: (
            (
                can_slam(state, player, slam)
                or dashes(state, player, dash, 1)
            )
            and jump_general(state, player, slam, fire2, arm, walljump, 2)
        ))
    add_rule(world.get_location("5-2: Secret #4", player),
        lambda state: (
            (
                can_slam(state, player, slam)
                or dashes(state, player, dash, 1)
            )
            and jump_general(state, player, slam, fire2, arm, walljump, 2)
        ))
    add_rule(world.get_location("5-2: Secret #5", player),
        lambda state: (
            (
                can_slam(state, player, slam)
                or dashes(state, player, dash, 1)
            )
            and grab_item(state, player, arm)
            and can_punch(state, player, arm)
        ))
    add_rule(world.get_location("Cleared 5-2", player),
        lambda state: (
            (
                can_slam(state, player, slam)
                or dashes(state, player, dash, 1)
            )
            and grab_item(state, player, arm)
            and can_punch(state, player, arm)
        ))
    if challenge:
        add_rule(world.get_location("5-2: Don't fight the ferryman", player),
            lambda state: (
                (
                    can_slam(state, player, slam)
                    or dashes(state, player, dash, 1)
                )
                and rev2_fire2(state, player, fire2)
                and grab_item(state, player, arm)
                and can_punch(state, player, arm)
            ))
    if prank:
        add_rule(world.get_location("5-2: Perfect Rank", player),
            lambda state: (
                (
                    can_slam(state, player, slam)
                    or dashes(state, player, dash, 1)
                )
                and grab_item(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
                and can_punch(state, player, arm)
            ))

    if skulls:
        add_rule(world.get_location("5-2: Secret #5", player),
            lambda state: state.has_all({"Blue Skull (5-2)", "Red Skull (5-2)"}, player))
        add_rule(world.get_location("Cleared 5-2", player),
            lambda state: state.has_all({"Blue Skull (5-2)", "Red Skull (5-2)"}, player))
        if challenge:
            add_rule(world.get_location("5-2: Don't fight the ferryman", player),
                lambda state: state.has_all({"Blue Skull (5-2)", "Red Skull (5-2)"}, player))
        if prank:
            add_rule(world.get_location("5-2: Perfect Rank", player),
                lambda state: state.has_all({"Blue Skull (5-2)", "Red Skull (5-2)"}, player))


    # 5-3
    if skulls:
        set_rule(world.get_location("5-3: Secret #1", player),
            lambda state: state.has("Blue Skull (5-3)", player))
        set_rule(world.get_location("5-3: Secret #3", player),
            lambda state: state.has_all({"Blue Skull (5-3)", "Red Skull (5-3)"}, player))
        set_rule(world.get_location("5-3: Weapon", player),
            lambda state: state.has_any({"Blue Skull (5-3)", "Red Skull (5-3)"}, player))
        set_rule(world.get_location("5-3: Secret #4", player),
            lambda state: state.has_any({"Blue Skull (5-3)", "Red Skull (5-3)"}, player))
        set_rule(world.get_location("5-3: Secret #5", player),
            lambda state: state.has_any({"Blue Skull (5-3)", "Red Skull (5-3)"}, player))
        set_rule(world.get_location("Cleared 5-3", player),
            lambda state: state.has_any({"Blue Skull (5-3)", "Red Skull (5-3)"}, player))
        if challenge:
            set_rule(world.get_location("5-3: Don't touch any water", player),
                lambda state: state.has_all({"Blue Skull (5-3)", "Red Skull (5-3)"}, player))
        if prank:
            set_rule(world.get_location("5-3: Perfect Rank", player),
                lambda state: state.has_any({"Blue Skull (5-3)", "Red Skull (5-3)"}, player))

    add_rule(world.get_location("5-3: Secret #1", player),
        lambda state: grab_item(state, player, arm))
    add_rule(world.get_location("5-3: Secret #2", player),
        lambda state: good_weapon(state, player, fire2, arm, slide, dash))
    add_rule(world.get_location("5-3: Secret #3", player),
        lambda state: grab_item(state, player, arm))
    add_rule(world.get_location("5-3: Weapon", player),
        lambda state: (
            grab_item(state, player, arm)
            and can_punch(state, player, arm)
        ))
    add_rule(world.get_location("5-3: Secret #4", player),
        lambda state: (
            grab_item(state, player, arm)
            and can_punch(state, player, arm)
        ))
    add_rule(world.get_location("5-3: Secret #5", player),
        lambda state: (
            grab_item(state, player, arm)
            and can_punch(state, player, arm)
        ))
    add_rule(world.get_location("Cleared 5-3", player),
        lambda state: (
            grab_item(state, player, arm)
            and can_punch(state, player, arm)
        ))
    if challenge:
        add_rule(world.get_location("5-3: Don't touch any water", player),
            lambda state: (
                grab_item(state, player, arm)
                and can_punch(state, player, arm)
                and can_slide(state, player, slide)
                and dashes(state, player, dash, 3)
                and jump_general(state, player, slam, fire2, arm, walljump, 2)
            ))
    if prank:
        add_rule(world.get_location("5-3: Perfect Rank", player),
            lambda state: (
                grab_item(state, player, arm)
                and can_punch(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))


    # 5-4
    if boss > 0 and goal != 4:
        set_rule(world.get_location("5-4: Defeat the Leviathan", player),
            lambda state: good_weapon(state, player, fire2, arm, slide, dash))
    if challenge and goal != 4:
        set_rule(world.get_location("5-4: Reach the surface in under 10 seconds", player),
            lambda state: (
                rock0_fire2(state, player, fire2)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))
    if prank and goal != 4:
        set_rule(world.get_location("5-4: Perfect Rank", player),
            lambda state: (
                rock0_fire2(state, player, fire2)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))


    # 6-1
    add_rule(world.get_location("6-1: Secret #2", player),
        lambda state: grab_item(state, player, arm))
    add_rule(world.get_location("6-1: Secret #3", player),
        lambda state: grab_item(state, player, arm))
    set_rule(world.get_location("6-1: Secret #4", player),
        lambda state: (
            jump_general(state, player, slam, fire2, arm, walljump, 1)
            and grab_item(state, player, arm)
        ))
    set_rule(world.get_location("6-1: Secret #5", player),
        lambda state: (
            jump_general(state, player, slam, fire2, arm, walljump, 2)
            and grab_item(state, player, arm)
            and can_punch(state, player, arm)
        ))
    add_rule(world.get_location("Cleared 6-1", player),
        lambda state: (
            jump_general(state, player, slam, fire2, arm, walljump, 1)
            and grab_item(state, player, arm)
            and can_punch(state, player, arm)
        ))
    if challenge:
        set_rule(world.get_location("6-1: Beat the secret encounter", player),
            lambda state: (
                jump_general(state, player, slam, fire2, arm, walljump, 1)
                and grab_item(state, player, arm)
            ))
    if prank:
        set_rule(world.get_location("6-1: Perfect Rank", player),
            lambda state: (
                jump_general(state, player, slam, fire2, arm, walljump, 1)
                and grab_item(state, player, arm)
                and can_punch(state, player, arm)
                and good_weapon(state, player, fire2, arm, slide, dash)
            ))

    if skulls:
        add_rule(world.get_location("6-1: Secret #2", player),
            lambda state: state.has("Red Skull (6-1)", player))
        add_rule(world.get_location("6-1: Secret #3", player),
            lambda state: state.has("Red Skull (6-1)", player))
        add_rule(world.get_location("6-1: Secret #4", player),
            lambda state: state.has("Red Skull (6-1)", player))
        add_rule(world.get_location("6-1: Secret #5", player),
            lambda state: state.has("Red Skull (6-1)", player))
        add_rule(world.get_location("Cleared 6-1", player),
            lambda state: state.has("Red Skull (6-1)", player))
        if challenge:
            add_rule(world.get_location("6-1: Beat the secret encounter", player),
                lambda state: state.has("Red Skull (6-1)", player))
        if prank:
            add_rule(world.get_location("6-1: Perfect Rank", player),
                lambda state: state.has("Red Skull (6-1)", player))


    # 6-2                
    set_rule(world.get_location("Cleared 6-2", player),
        lambda state: (
            (
                can_slam(state, player, slam)
                or walljumps(state, player, walljump, 2)
                or sho1_fire2(state, player, fire2)
                or rai2(state, player)
                or rock0_fire2(state, player, fire2)
            )
            and good_weapon(state, player, fire2, arm, slide, dash)
        ))
    if goal != 5:
        if boss > 0:
            set_rule(world.get_location("6-2: Defeat Gabriel", player),
                lambda state: (
                    (
                        can_slam(state, player, slam)
                        or walljumps(state, player, walljump, 2)
                        or sho1_fire2(state, player, fire2)
                        or rai2(state, player)
                        or rock0_fire2(state, player, fire2)
                    )
                    and good_weapon(state, player, fire2, arm, slide, dash)
                ))
        if challenge:
            set_rule(world.get_location("6-2: Hit Gabriel into the ceiling", player),
                lambda state: (
                    (
                        can_slam(state, player, slam)
                        or walljumps(state, player, walljump, 2)
                        or sho1_fire2(state, player, fire2)
                        or rai2(state, player)
                        or rock0_fire2(state, player, fire2)
                    )
                    and (
                        rock0(state, player)
                        or rock1(state, player)
                    )
                    and good_weapon(state, player, fire2, arm, slide, dash)
                ))
        if prank:
            set_rule(world.get_location("6-2: Perfect Rank", player),
                lambda state: (
                    (
                        can_slam(state, player, slam)
                        or walljumps(state, player, walljump, 2)
                        or sho1_fire2(state, player, fire2)
                        or rai2(state, player)
                        or rock0_fire2(state, player, fire2)
                    )
                    and good_weapon(state, player, fire2, arm, slide, dash)
                ))


    # shop
    set_rule(world.get_location("Shop: Buy Revolver Variant 1", player),
        lambda state: (
            rev0(state, player)
            or rev1(state, player)
            or rev2(state, player)
        ))

    set_rule(world.get_location("Shop: Buy Revolver Variant 2", player),
        lambda state: (
            rev0(state, player)
            or rev1(state, player)
            or rev2(state, player)
        ))

    set_rule(world.get_location("Shop: Buy Shotgun Variant", player),
        lambda state: (
            sho0(state, player)
            or sho1(state, player)
        ))

    set_rule(world.get_location("Shop: Buy Nailgun Variant", player),
        lambda state: (
            nai0(state, player)
            or nai1(state, player)
        ))

    set_rule(world.get_location("Shop: Buy Railcannon Variant 1", player),
        lambda state: (
            rai0(state, player)
            or rai1(state, player)
            or rai2(state, player)
        ))

    set_rule(world.get_location("Shop: Buy Railcannon Variant 2", player),
        lambda state: (
            rai0(state, player)
            or rai1(state, player)
            or rai2(state, player)
        ))

    set_rule(world.get_location("Shop: Buy Rocket Launcher Variant", player),
        lambda state: (
            rock0(state, player)
            or rock1(state, player)
        ))