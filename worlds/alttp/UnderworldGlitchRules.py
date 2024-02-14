from BaseClasses import Entrance
from worlds.generic.Rules import set_rule, add_rule
from .StateHelpers import can_bomb_clip, has_sword, has_beam_sword, has_fire_source, can_melt_things, has_misery_mire_medallion


# We actually need the logic to properly "mark" these regions as Light or Dark world. 
# Therefore we need to make these connections during the normal link_entrances stage, rather than during set_rules.
def underworld_glitch_connections(world, player):
    specrock = world.get_region('Spectacle Rock Cave (Bottom)', player)
    mire = world.get_region('Misery Mire (West)', player)

    kikiskip = Entrance(player, 'Kiki Skip', specrock)
    mire_to_hera = Entrance(player, 'Mire to Hera Clip', mire)
    mire_to_swamp = Entrance(player, 'Hera to Swamp Clip', mire)
    specrock.exits.append(kikiskip)
    mire.exits.extend([mire_to_hera, mire_to_swamp])

    if world.fix_fake_world[player]: 
        kikiskip.connect(world.get_entrance('Palace of Darkness Exit', player).connected_region)
        mire_to_hera.connect(world.get_entrance('Tower of Hera Exit', player).connected_region)
        mire_to_swamp.connect(world.get_entrance('Swamp Palace Exit', player).connected_region)
    else: 
        kikiskip.connect(world.get_region('Palace of Darkness (Entrance)', player))
        mire_to_hera.connect(world.get_region('Tower of Hera (Bottom)', player))
        mire_to_swamp.connect(world.get_region('Swamp Palace (Entrance)', player))


# For some entrances, we need to fake having pearl, because we're in fake DW/LW. 
# This creates a copy of the input state that has Moon Pearl. 
def fake_pearl_state(state, player): 
    if state.has('Moon Pearl', player):
        return state
    fake_state = state.copy()
    fake_state.prog_items[player]['Moon Pearl'] += 1
    return fake_state


# Sets the rules on where we can actually go using this clip.
# Behavior differs based on what type of ER shuffle we're playing. 
def dungeon_reentry_rules(world, player, clip: Entrance, dungeon_region: str, dungeon_exit: str): 
    fix_dungeon_exits = world.fix_palaceofdarkness_exit[player]
    fix_fake_worlds = world.fix_fake_world[player]

    dungeon_entrance = [r for r in world.get_region(dungeon_region, player).entrances if r.name != clip.name][0]
    if not fix_dungeon_exits: # vanilla, simple, restricted, dungeonssimple; should never have fake worlds fix
        # Dungeons are only shuffled among themselves. We need to check SW, MM, and AT because they can't be reentered trivially. 
        if dungeon_entrance.name == 'Skull Woods Final Section': 
            set_rule(clip, lambda state: False) # entrance doesn't exist until you fire rod it from the other side
        elif dungeon_entrance.name == 'Misery Mire': 
            add_rule(clip, lambda state: has_sword(state, player) and has_misery_mire_medallion(state, player)) # open the dungeon
        elif dungeon_entrance.name == 'Agahnims Tower': 
            add_rule(clip, lambda state: state.has('Cape', player) or has_beam_sword(state, player) or state.has('Beat Agahnim 1', player)) # kill/bypass barrier
        # Then we set a restriction on exiting the dungeon, so you can't leave unless you got in normally. 
        add_rule(world.get_entrance(dungeon_exit, player), lambda state: dungeon_entrance.can_reach(state))
    elif not fix_fake_worlds: # full, dungeonsfull; fixed dungeon exits, but no fake worlds fix
        # Entry requires the entrance's requirements plus a fake pearl, but you don't gain logical access to the surrounding region. 
        add_rule(clip, lambda state: dungeon_entrance.access_rule(fake_pearl_state(state, player)))
        # exiting restriction
        add_rule(world.get_entrance(dungeon_exit, player), lambda state: dungeon_entrance.can_reach(state))
    # Otherwise, the shuffle type is crossed, dungeonscrossed, or insanity; all of these do not need additional rules on where we can go, 
    # since the clip links directly to the exterior region. 


def underworld_glitches_rules(world, player): 
    fix_dungeon_exits = world.fix_palaceofdarkness_exit[player]
    fix_fake_worlds = world.fix_fake_world[player]

    # Ice Palace Entrance Clip
    # This is the easiest one since it's a simple internal clip.
    # Need to also add melting to freezor chest since it's otherwise assumed.
    # Also can pick up the first jelly key from behind.
    add_rule(world.get_entrance('Ice Palace (Main)', player), lambda state: can_bomb_clip(state, world.get_region('Ice Palace (Entrance)', player), player), combine='or')
    add_rule(world.get_location('Ice Palace - Freezor Chest', player), lambda state: can_melt_things(state, player))
    add_rule(world.get_location('Ice Palace - Jelly Key Drop', player), lambda state: can_bomb_clip(state, world.get_region('Ice Palace (Entrance)', player), player), combine='or')


    # Kiki Skip
    kikiskip = world.get_entrance('Kiki Skip', player)
    set_rule(kikiskip, lambda state: can_bomb_clip(state, kikiskip.parent_region, player))
    dungeon_reentry_rules(world, player, kikiskip, 'Palace of Darkness (Entrance)', 'Palace of Darkness Exit')


    # Mire -> Hera -> Swamp
    # Using mire keys on other dungeon doors
    mire = world.get_region('Misery Mire (West)', player)
    mire_clip = lambda state: state.can_reach('Misery Mire (West)', 'Region', player) and can_bomb_clip(state, mire, player) and has_fire_source(state, player)
    hera_clip = lambda state: state.can_reach('Tower of Hera (Top)', 'Region', player) and can_bomb_clip(state, world.get_region('Tower of Hera (Top)', player), player)
    add_rule(world.get_entrance('Tower of Hera Big Key Door', player), lambda state: mire_clip(state) and state.has('Big Key (Misery Mire)', player), combine='or')
    add_rule(world.get_entrance('Swamp Palace Small Key Door', player), lambda state: mire_clip(state), combine='or')
    add_rule(world.get_entrance('Swamp Palace (Center)', player), lambda state: mire_clip(state) or hera_clip(state), combine='or')

    # Build the rule for SP moat. 
    # We need to be able to s+q to old man, then go to either Mire or Hera at either Hera or GT. 
    # First we require a certain type of entrance shuffle, then build the rule from its pieces. 
    if not world.swamp_patch_required[player]:
        if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull', 'dungeonscrossed']: 
            rule_map = {
                'Misery Mire (Entrance)': (lambda state: True),
                'Tower of Hera (Bottom)': (lambda state: state.can_reach('Tower of Hera Big Key Door', 'Entrance', player))
            }
            inverted = world.mode[player] == 'inverted'
            hera_rule = lambda state: (state.has('Moon Pearl', player) or not inverted) and \
                                      rule_map.get(world.get_entrance('Tower of Hera', player).connected_region.name, lambda state: False)(state)
            gt_rule = lambda state: (state.has('Moon Pearl', player) or inverted) and \
                                    rule_map.get(world.get_entrance(('Ganons Tower' if not inverted else 'Inverted Ganons Tower'), player).connected_region.name, lambda state: False)(state)
            mirrorless_moat_rule = lambda state: state.can_reach('Old Man S&Q', 'Entrance', player) and mire_clip(state) and (hera_rule(state) or gt_rule(state))
            add_rule(world.get_entrance('Swamp Palace Moat', player), lambda state: state.has('Magic Mirror', player) or mirrorless_moat_rule(state))
        else: 
            add_rule(world.get_entrance('Swamp Palace Moat', player), lambda state: state.has('Magic Mirror', player))

    # Using the entrances for various ER types. Hera -> Swamp never matters because you can only logically traverse with the mire keys
    mire_to_hera = world.get_entrance('Mire to Hera Clip', player)
    mire_to_swamp = world.get_entrance('Hera to Swamp Clip', player)
    set_rule(mire_to_hera, mire_clip)
    set_rule(mire_to_swamp, lambda state: mire_clip(state) and state.has('Flippers', player))
    dungeon_reentry_rules(world, player, mire_to_hera, 'Tower of Hera (Bottom)', 'Tower of Hera Exit')
    dungeon_reentry_rules(world, player, mire_to_swamp, 'Swamp Palace (Entrance)', 'Swamp Palace Exit')
