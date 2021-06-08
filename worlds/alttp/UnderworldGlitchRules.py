
from BaseClasses import Entrance
from worlds.alttp.Items import ItemFactory
from worlds.generic.Rules import set_rule, add_rule

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
    fake_state.prog_items['Moon Pearl', player] += 1
    return fake_state


def underworld_glitches_rules(world, player): 
    fix_dungeon_exits = world.fix_palaceofdarkness_exit[player]
    fix_fake_worlds = world.fix_fake_world[player]

    # Ice Palace Entrance Clip
    # This is the easiest one since it's a simple internal clip. Just need to also add melting to freezor chest since it's otherwise assumed. 
    add_rule(world.get_entrance('Ice Palace Entrance Room', player), lambda state: state.can_bomb_clip(world.get_region('Ice Palace (Entrance)', player), player), combine='or')
    add_rule(world.get_location('Ice Palace - Freezor Chest', player), lambda state: state.can_melt_things(player))



    # Kiki Skip
    kikiskip = world.get_entrance('Kiki Skip', player)
    set_rule(kikiskip, lambda state: state.can_bomb_clip(kikiskip.parent_region, player))
    pod_entrance = [r for r in world.get_region('Palace of Darkness (Entrance)', player).entrances if r.name != 'Kiki Skip'][0]
    # Behavior differs based on what type of ER shuffle we're playing. 
    if not fix_dungeon_exits: # vanilla, simple, restricted, dungeonssimple (this should always have no FWF)
        # Dungeons are only shuffled among themselves. We need to check SW, MM, and AT because they can't be reentered trivially. 
        if pod_entrance.name == 'Skull Woods Final Section': 
            set_rule(kikiskip, lambda state: False)
        elif pod_entrance.name == 'Misery Mire': 
            add_rule(kikiskip, lambda state: state.has_sword(player) and state.has_misery_mire_medallion(player))
        elif pod_entrance.name == 'Agahnims Tower': 
            add_rule(kikiskip, lambda state: state.has('Cape', player) or state.has_beam_sword(player) or state.has('Beat Agahnim 1', player))

        # Then we set a restriction on exiting the dungeon, so you can't leave unless you got in normally.
        add_rule(world.get_entrance('Palace of Darkness Exit', player), lambda state: pod_entrance.can_reach(state))
    elif not fix_fake_worlds: # full, dungeonsfull; has fixed exits but no FWF
        # Entry requires the entrance's requirements plus a fake pearl, but you don't gain logical access to the surrounding region. 
        add_rule(kikiskip, lambda state: pod_entrance.access_rule(fake_pearl_state(state, player)))
        # exiting restriction
        add_rule(world.get_entrance('Palace of Darkness Exit', player), lambda state: pod_entrance.can_reach(state))



    # Mire -> Hera -> Swamp
    # Using mire keys on other dungeon doors
    mire = world.get_region('Misery Mire (West)', player)
    mire_clip = lambda state: state.can_reach('Misery Mire (West)', 'Region', player) and state.can_bomb_clip(mire, player) and state.has_fire_source(player)
    hera_clip = lambda state: state.can_reach('Tower of Hera (Top)', 'Region', player) and state.can_bomb_clip(world.get_region('Tower of Hera (Top)', player), player)
    add_rule(world.get_entrance('Tower of Hera Big Key Door', player), lambda state: mire_clip(state) and state.has('Big Key (Misery Mire)', player), combine='or')
    add_rule(world.get_entrance('Swamp Palace Small Key Door', player), lambda state: mire_clip(state), combine='or')
    add_rule(world.get_entrance('Swamp Palace (Center)', player), lambda state: mire_clip(state) or hera_clip(state), combine='or')

    # Build the rule for SP moat. 
    # We need to be able to s+q to old man, then go to either Mire or Hera at either Hera or GT. 
    # First we require a certain type of entrance shuffle, then build the rule from its pieces. 
    if not world.swamp_patch_required[player]:
        mirrorless_moat_rules = []
        if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull', 'dungeonscrossed']: 
            mirrorless_moat_rules.append(lambda state: state.can_reach('Old Man S&Q', 'Entrance', player) and mire_clip(state))
            rule_map = {
                'Misery Mire (Entrance)': (lambda state: True),
                'Tower of Hera (Bottom)': (lambda state: state.can_reach('Tower of Hera Big Key Door', 'Entrance', player))
            }
            inverted = world.mode[player] == 'inverted'
            hera_rule = lambda state: (state.has('Moon Pearl', player) or not inverted) and \
                                      rule_map.get(world.get_entrance('Tower of Hera', player).connected_region.name, lambda state: False)(state)
            gt_rule = lambda state: (state.has('Moon Pearl', player) or inverted) and \
                                    rule_map.get(world.get_entrance(('Ganons Tower' if not inverted else 'Inverted Ganons Tower'), player).connected_region.name, lambda state: False)(state)
            mirrorless_moat_rules.append(lambda state: hera_rule(state) or gt_rule(state))
        else: 
            mirrorless_moat_rules.append(lambda state: False) # all function returns True on empty list

        add_rule(world.get_entrance('Swamp Palace Moat', player), lambda state: state.has('Magic Mirror', player) or all([rule(state) for rule in mirrorless_moat_rules]))

    # Using the entrances for various ER types. Hera -> Swamp never matters because you can only logically traverse with the mire keys
    mire_to_hera = world.get_entrance('Mire to Hera Clip', player)
    mire_to_swamp = world.get_entrance('Hera to Swamp Clip', player)
    set_rule(mire_to_hera, mire_clip)
    set_rule(mire_to_swamp, lambda state: mire_clip(state) and state.has('Flippers', player))
    hera_entrance = [r for r in world.get_region('Tower of Hera (Bottom)', player).entrances if r.name != 'Mire to Hera Clip'][0]
    swamp_entrance = [r for r in world.get_region('Swamp Palace (Entrance)', player).entrances if r.name != 'Hera to Swamp Clip'][0]
    if not fix_dungeon_exits: 
        if hera_entrance.name == 'Skull Woods Final Section': 
            set_rule(mire_to_hera, lambda state: False)
        elif hera_entrance.name == 'Misery Mire': 
            add_rule(mire_to_hera, lambda state: state.has_sword(player) and state.has_misery_mire_medallion(player))
        elif hera_entrance.name == 'Agahnims Tower': 
            add_rule(mire_to_hera, lambda state: state.has('Cape', player) or state.has_beam_sword(player) or state.has('Beat Agahnim 1', player))
        add_rule(world.get_entrance('Tower of Hera Exit', player), lambda state: hera_entrance.can_reach(state))

        if swamp_entrance.name == 'Skull Woods Final Section': 
            set_rule(mire_to_swamp, lambda state: False)
        elif swamp_entrance.name == 'Misery Mire': 
            add_rule(mire_to_swamp, lambda state: state.has_sword(player) and state.has_misery_mire_medallion(player))
        elif swamp_entrance.name == 'Agahnims Tower': 
            add_rule(mire_to_swamp, lambda state: state.has('Cape', player) or state.has_beam_sword(player) or state.has('Beat Agahnim 1', player))
        add_rule(world.get_entrance('Swamp Palace Exit', player), lambda state: swamp_entrance.can_reach(state))
    elif not fix_fake_worlds: 
        add_rule(mire_to_hera, lambda state: hera_entrance.access_rule(fake_pearl_state(state, player)))
        add_rule(world.get_entrance('Tower of Hera Exit', player), lambda state: hera_entrance.can_reach(state))

        add_rule(mire_to_swamp, lambda state: swamp_entrance.access_rule(fake_pearl_state(state, player)))
        add_rule(world.get_entrance('Swamp Palace Exit', player), lambda state: swamp_entrance.can_reach(state))
