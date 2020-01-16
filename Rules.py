import collections
import logging
from BaseClasses import CollectionState


def set_rules(world, player):

    if world.logic[player] == 'nologic':
        logging.getLogger('').info('WARNING! Seeds generated under this logic often require major glitches and may be impossible!')
        if world.mode[player] != 'inverted':
            world.get_region('Links House', player).can_reach_private = lambda state: True
            world.get_region('Sanctuary', player).can_reach_private = lambda state: True
            old_rule = world.get_region('Old Man House', player).can_reach
            world.get_region('Old Man House', player).can_reach_private = lambda state: state.can_reach('Old Man', 'Location', player) or old_rule(state)
            return
        else:
            world.get_region('Inverted Links House', player).can_reach_private = lambda state: True
            world.get_region('Inverted Dark Sanctuary', player).entrances[0].parent_region.can_reach_private = lambda state: True
            if world.shuffle[player] != 'vanilla':
                old_rule = world.get_region('Old Man House', player).can_reach
                world.get_region('Old Man House', player).can_reach_private = lambda state: state.can_reach('Old Man', 'Location', player) or old_rule(state)
            world.get_region('Hyrule Castle Ledge', player).can_reach_private = lambda state: True
            return

    global_rules(world, player)
    if world.mode[player] != 'inverted':
        default_rules(world, player)

    if world.mode[player] == 'open':
        open_rules(world, player)
    elif world.mode[player] == 'standard':
        standard_rules(world, player)
    elif world.mode[player] == 'inverted':
        open_rules(world, player)
        inverted_rules(world, player)
    else:
        raise NotImplementedError('Not implemented yet')

    if world.logic[player] == 'noglitches':
        no_glitches_rules(world, player)
    elif world.logic[player] == 'minorglitches':
        logging.getLogger('').info('Minor Glitches may be buggy still. No guarantee for proper logic checks.')
    else:
        raise NotImplementedError('Not implemented yet')

    if world.goal[player] == 'dungeons':
        # require all dungeons to beat ganon
        add_rule(world.get_location('Ganon', player), lambda state: state.can_reach('Master Sword Pedestal', 'Location', player) and state.has('Beat Agahnim 1', player) and state.has('Beat Agahnim 2', player) and state.has_crystals(7, player))
    elif world.goal[player] == 'ganon':
        # require aga2 to beat ganon
        add_rule(world.get_location('Ganon', player), lambda state: state.has('Beat Agahnim 2', player))
    
    if world.mode[player] != 'inverted':
        set_big_bomb_rules(world, player)
    else:
        set_inverted_big_bomb_rules(world, player)

    # if swamp and dam have not been moved we require mirror for swamp palace
    if not world.swamp_patch_required[player]:
        add_rule(world.get_entrance('Swamp Palace Moat', player), lambda state: state.has_Mirror(player))

    if world.mode[player] != 'inverted':
        set_bunny_rules(world, player)
    else:
        set_inverted_bunny_rules(world, player)

def set_rule(spot, rule):
    spot.access_rule = rule

def set_defeat_dungeon_boss_rule(location):
    # Lambda required to defer evaluation of dungeon.boss since it will change later if boos shuffle is used
    set_rule(location, lambda state: location.parent_region.dungeon.boss.can_defeat(state))

def set_always_allow(spot, rule):
    spot.always_allow = rule

def add_rule(spot, rule, combine='and'):
    old_rule = spot.access_rule
    if combine == 'or':
        spot.access_rule = lambda state: rule(state) or old_rule(state)
    else:
        spot.access_rule = lambda state: rule(state) and old_rule(state)


def add_lamp_requirement(spot, player):
    add_rule(spot, lambda state: state.has('Lamp', player, state.world.lamps_needed_for_dark_rooms))


def forbid_item(location, item, player):
    old_rule = location.item_rule
    location.item_rule = lambda i: (i.name != item or i.player != player) and old_rule(i)

def add_item_rule(location, rule):
    old_rule = location.item_rule
    location.item_rule = lambda item: rule(item) and old_rule(item)

def item_in_locations(state, item, player, locations):
    for location in locations:
        if item_name(state, location[0], location[1]) == (item, player):
            return True
    return False

def item_name(state, location, player):
    location = state.world.get_location(location, player)
    if location.item is None:
        return None
    return (location.item.name, location.item.player)

def global_rules(world, player):
    # ganon can only carry triforce
    add_item_rule(world.get_location('Ganon', player), lambda item: item.name == 'Triforce' and item.player == player)

    # we can s&q to the old man house after we rescue him. This may be somewhere completely different if caves are shuffled!
    old_rule = world.get_region('Old Man House', player).can_reach_private
    world.get_region('Old Man House', player).can_reach_private = lambda state: state.can_reach('Old Man', 'Location', player) or old_rule(state)

    set_rule(world.get_location('Sunken Treasure', player), lambda state: state.has('Open Floodgate', player))
    set_rule(world.get_location('Dark Blacksmith Ruins', player), lambda state: state.has('Return Smith', player))
    set_rule(world.get_location('Purple Chest', player), lambda state: state.has('Pick Up Purple Chest', player))  # Can S&Q with chest
    set_rule(world.get_location('Ether Tablet', player), lambda state: state.has('Book of Mudora', player) and state.has_beam_sword(player))
    set_rule(world.get_location('Master Sword Pedestal', player), lambda state: state.has('Red Pendant', player) and state.has('Blue Pendant', player) and state.has('Green Pendant', player))

    set_rule(world.get_location('Missing Smith', player), lambda state: state.has('Get Frog', player) and state.can_reach('Blacksmiths Hut', 'Region', player)) # Can't S&Q with smith
    set_rule(world.get_location('Blacksmith', player), lambda state: state.has('Return Smith', player))
    set_rule(world.get_location('Magic Bat', player), lambda state: state.has('Magic Powder', player))
    set_rule(world.get_location('Sick Kid', player), lambda state: state.has_bottle(player))
    set_rule(world.get_location('Library', player), lambda state: state.has_Boots(player))
    set_rule(world.get_location('Mimic Cave', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_location('Sahasrahla', player), lambda state: state.has('Green Pendant', player))


    set_rule(world.get_location('Spike Cave', player), lambda state:
             state.has('Hammer', player) and state.can_lift_rocks(player) and
             ((state.has('Cape', player) and state.can_extend_magic(player, 16, True)) or
                 (state.has('Cane of Byrna', player) and
                     (state.can_extend_magic(player, 12, True) or
                     (state.world.can_take_damage and (state.has_Boots(player) or state.has_hearts(player, 4))))))
            )

    set_rule(world.get_location('Hookshot Cave - Top Right', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_location('Hookshot Cave - Top Left', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_location('Hookshot Cave - Bottom Right', player), lambda state: state.has('Hookshot', player) or state.has('Pegasus Boots', player))
    set_rule(world.get_location('Hookshot Cave - Bottom Left', player), lambda state: state.has('Hookshot', player))

    set_rule(world.get_entrance('Sewers Door', player), lambda state: state.has_key('Small Key (Escape)', player) or (world.retro[player] and world.mode[player] == 'standard')) # standard retro cannot access the shop
    set_rule(world.get_entrance('Sewers Back Door', player), lambda state: state.has_key('Small Key (Escape)', player))
    set_rule(world.get_entrance('Agahnim 1', player), lambda state: state.has_sword(player) and state.has_key('Small Key (Agahnims Tower)', player, 2))
    set_defeat_dungeon_boss_rule(world.get_location('Agahnim 1', player))
    set_rule(world.get_location('Castle Tower - Dark Maze', player), lambda state: state.has_key('Small Key (Agahnims Tower)', player))

    set_rule(world.get_location('Eastern Palace - Big Chest', player), lambda state: state.has('Big Key (Eastern Palace)', player))
    set_rule(world.get_location('Eastern Palace - Boss', player), lambda state: state.can_shoot_arrows(player) and state.has('Big Key (Eastern Palace)', player) and world.get_location('Eastern Palace - Boss', player).parent_region.dungeon.boss.can_defeat(state))
    set_rule(world.get_location('Eastern Palace - Prize', player), lambda state: state.can_shoot_arrows(player) and state.has('Big Key (Eastern Palace)', player) and world.get_location('Eastern Palace - Prize', player).parent_region.dungeon.boss.can_defeat(state))
    for location in ['Eastern Palace - Boss', 'Eastern Palace - Big Chest']:
        forbid_item(world.get_location(location, player), 'Big Key (Eastern Palace)', player)

    set_rule(world.get_location('Desert Palace - Big Chest', player), lambda state: state.has('Big Key (Desert Palace)', player))
    set_rule(world.get_location('Desert Palace - Torch', player), lambda state: state.has_Boots(player))
    set_rule(world.get_entrance('Desert Palace East Wing', player), lambda state: state.has_key('Small Key (Desert Palace)', player))
    set_rule(world.get_location('Desert Palace - Prize', player), lambda state: state.has_key('Small Key (Desert Palace)', player) and state.has('Big Key (Desert Palace)', player) and state.has_fire_source(player) and world.get_location('Desert Palace - Prize', player).parent_region.dungeon.boss.can_defeat(state))
    set_rule(world.get_location('Desert Palace - Boss', player), lambda state: state.has_key('Small Key (Desert Palace)', player) and state.has('Big Key (Desert Palace)', player) and state.has_fire_source(player) and world.get_location('Desert Palace - Boss', player).parent_region.dungeon.boss.can_defeat(state))
    for location in ['Desert Palace - Boss', 'Desert Palace - Big Chest']:
        forbid_item(world.get_location(location, player), 'Big Key (Desert Palace)', player)

    for location in ['Desert Palace - Boss', 'Desert Palace - Big Key Chest', 'Desert Palace - Compass Chest']:
        forbid_item(world.get_location(location, player), 'Small Key (Desert Palace)', player)

    set_rule(world.get_entrance('Tower of Hera Small Key Door', player), lambda state: state.has_key('Small Key (Tower of Hera)', player) or item_name(state, 'Tower of Hera - Big Key Chest', player) == ('Small Key (Tower of Hera)', player))
    set_rule(world.get_entrance('Tower of Hera Big Key Door', player), lambda state: state.has('Big Key (Tower of Hera)', player))
    set_rule(world.get_location('Tower of Hera - Big Chest', player), lambda state: state.has('Big Key (Tower of Hera)', player))
    set_rule(world.get_location('Tower of Hera - Big Key Chest', player), lambda state: state.has_fire_source(player))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Tower of Hera - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Tower of Hera)' and item.player == player)
    set_defeat_dungeon_boss_rule(world.get_location('Tower of Hera - Boss', player))
    set_defeat_dungeon_boss_rule(world.get_location('Tower of Hera - Prize', player))
    for location in ['Tower of Hera - Boss', 'Tower of Hera - Big Chest', 'Tower of Hera - Compass Chest']:
        forbid_item(world.get_location(location, player), 'Big Key (Tower of Hera)', player)
#    for location in ['Tower of Hera - Big Key Chest']:
#        forbid_item(world.get_location(location, player), 'Small Key (Tower of Hera)', player)

    set_rule(world.get_entrance('Swamp Palace Moat', player), lambda state: state.has('Flippers', player) and state.has('Open Floodgate', player))
    set_rule(world.get_entrance('Swamp Palace Small Key Door', player), lambda state: state.has_key('Small Key (Swamp Palace)', player))
    set_rule(world.get_entrance('Swamp Palace (Center)', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_location('Swamp Palace - Big Chest', player), lambda state: state.has('Big Key (Swamp Palace)', player) or item_name(state, 'Swamp Palace - Big Chest', player) == ('Big Key (Swamp Palace)', player))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Swamp Palace - Big Chest', player), lambda state, item: item.name == 'Big Key (Swamp Palace)' and item.player == player)
    set_rule(world.get_entrance('Swamp Palace (North)', player), lambda state: state.has('Hookshot', player))
    set_defeat_dungeon_boss_rule(world.get_location('Swamp Palace - Boss', player))
    set_defeat_dungeon_boss_rule(world.get_location('Swamp Palace - Prize', player))
    for location in ['Swamp Palace - Entrance']:
        forbid_item(world.get_location(location, player), 'Big Key (Swamp Palace)', player)

    set_rule(world.get_entrance('Thieves Town Big Key Door', player), lambda state: state.has('Big Key (Thieves Town)', player))
    set_rule(world.get_entrance('Blind Fight', player), lambda state: state.has_key('Small Key (Thieves Town)', player))
    set_defeat_dungeon_boss_rule(world.get_location('Thieves\' Town - Boss', player))
    set_defeat_dungeon_boss_rule(world.get_location('Thieves\' Town - Prize', player))
    set_rule(world.get_location('Thieves\' Town - Big Chest', player), lambda state: (state.has_key('Small Key (Thieves Town)', player) or item_name(state, 'Thieves\' Town - Big Chest', player) == ('Small Key (Thieves Town)', player)) and state.has('Hammer', player))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Thieves\' Town - Big Chest', player), lambda state, item: item.name == 'Small Key (Thieves Town)' and item.player == player and state.has('Hammer', player))
    set_rule(world.get_location('Thieves\' Town - Attic', player), lambda state: state.has_key('Small Key (Thieves Town)', player))
    for location in ['Thieves\' Town - Attic', 'Thieves\' Town - Big Chest', 'Thieves\' Town - Blind\'s Cell', 'Thieves\' Town - Boss']:
        forbid_item(world.get_location(location, player), 'Big Key (Thieves Town)', player)
    for location in ['Thieves\' Town - Attic', 'Thieves\' Town - Boss']:
        forbid_item(world.get_location(location, player), 'Small Key (Thieves Town)', player)

    set_rule(world.get_entrance('Skull Woods First Section South Door', player), lambda state: state.has_key('Small Key (Skull Woods)', player))
    set_rule(world.get_entrance('Skull Woods First Section (Right) North Door', player), lambda state: state.has_key('Small Key (Skull Woods)', player))
    set_rule(world.get_entrance('Skull Woods First Section West Door', player), lambda state: state.has_key('Small Key (Skull Woods)', player, 2))  # ideally would only be one key, but we may have spent thst key already on escaping the right section
    set_rule(world.get_entrance('Skull Woods First Section (Left) Door to Exit', player), lambda state: state.has_key('Small Key (Skull Woods)', player, 2))
    set_rule(world.get_location('Skull Woods - Big Chest', player), lambda state: state.has('Big Key (Skull Woods)', player) or item_name(state, 'Skull Woods - Big Chest', player) == ('Big Key (Skull Woods)', player))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Skull Woods - Big Chest', player), lambda state, item: item.name == 'Big Key (Skull Woods)' and item.player == player)
    set_rule(world.get_entrance('Skull Woods Torch Room', player), lambda state: state.has_key('Small Key (Skull Woods)', player, 3) and state.has('Fire Rod', player) and state.has_sword(player))  # sword required for curtain
    set_defeat_dungeon_boss_rule(world.get_location('Skull Woods - Boss', player))
    set_defeat_dungeon_boss_rule(world.get_location('Skull Woods - Prize', player))
    for location in ['Skull Woods - Boss']:
        forbid_item(world.get_location(location, player), 'Small Key (Skull Woods)', player)

    set_rule(world.get_entrance('Ice Palace Entrance Room', player), lambda state: state.can_melt_things(player))
    set_rule(world.get_location('Ice Palace - Big Chest', player), lambda state: state.has('Big Key (Ice Palace)', player))
    set_rule(world.get_entrance('Ice Palace (Kholdstare)', player), lambda state: state.can_lift_rocks(player) and state.has('Hammer', player) and state.has('Big Key (Ice Palace)', player) and (state.has_key('Small Key (Ice Palace)', player, 2) or (state.has('Cane of Somaria', player) and state.has_key('Small Key (Ice Palace)', player, 1))))
    # TODO: investigate change from VT. Changed to hookshot or 2 keys (no checking for big key in specific chests)
    set_rule(world.get_entrance('Ice Palace (East)', player), lambda state: (state.has('Hookshot', player) or (item_in_locations(state, 'Big Key (Ice Palace)', player, [('Ice Palace - Spike Room', player), ('Ice Palace - Big Key Chest', player), ('Ice Palace - Map Chest', player)]) and state.has_key('Small Key (Ice Palace)', player))) and (state.world.can_take_damage or state.has('Hookshot', player) or state.has('Cape', player) or state.has('Cane of Byrna', player)))
    set_rule(world.get_entrance('Ice Palace (East Top)', player), lambda state: state.can_lift_rocks(player) and state.has('Hammer', player))
    set_defeat_dungeon_boss_rule(world.get_location('Ice Palace - Boss', player))
    set_defeat_dungeon_boss_rule(world.get_location('Ice Palace - Prize', player))
    for location in ['Ice Palace - Big Chest', 'Ice Palace - Boss']:
        forbid_item(world.get_location(location, player), 'Big Key (Ice Palace)', player)

    set_rule(world.get_entrance('Misery Mire Entrance Gap', player), lambda state: (state.has_Boots(player) or state.has('Hookshot', player)) and (state.has_sword(player) or state.has('Fire Rod', player) or state.has('Ice Rod', player) or state.has('Hammer', player) or state.has('Cane of Somaria', player) or state.can_shoot_arrows(player)))  # need to defeat wizzrobes, bombs don't work ...
    set_rule(world.get_location('Misery Mire - Big Chest', player), lambda state: state.has('Big Key (Misery Mire)', player))
    set_rule(world.get_location('Misery Mire - Spike Chest', player), lambda state: (state.world.can_take_damage and state.has_hearts(player, 4)) or state.has('Cane of Byrna', player) or state.has('Cape', player))
    set_rule(world.get_entrance('Misery Mire Big Key Door', player), lambda state: state.has('Big Key (Misery Mire)', player))
    # you can squander the free small key from the pot by opening the south door to the north west switch room, locking you out of accessing a color switch ...
    # big key gives backdoor access to that from the teleporter in the north west
    set_rule(world.get_location('Misery Mire - Map Chest', player), lambda state: state.has_key('Small Key (Misery Mire)', player, 1) or state.has('Big Key (Misery Mire)', player))
    # in addition, you can open the door to the map room before getting access to a color switch, so this is locked behing 2 small keys or the big key...
    set_rule(world.get_location('Misery Mire - Main Lobby', player), lambda state: state.has_key('Small Key (Misery Mire)', player, 2) or state.has_key('Big Key (Misery Mire)', player))
    # we can place a small key in the West wing iff it also contains/blocks the Big Key, as we cannot reach and softlock with the basement key door yet
    set_rule(world.get_entrance('Misery Mire (West)', player), lambda state: state.has_key('Small Key (Misery Mire)', player, 2) if ((item_name(state, 'Misery Mire - Compass Chest', player) in [('Big Key (Misery Mire)', player)]) or
                                                                                                                 (item_name(state, 'Misery Mire - Big Key Chest', player) in [('Big Key (Misery Mire)', player)])) else state.has_key('Small Key (Misery Mire)', player, 3))
    set_rule(world.get_location('Misery Mire - Compass Chest', player), lambda state: state.has_fire_source(player))
    set_rule(world.get_location('Misery Mire - Big Key Chest', player), lambda state: state.has_fire_source(player))
    set_rule(world.get_entrance('Misery Mire (Vitreous)', player), lambda state: state.has('Cane of Somaria', player))
    set_defeat_dungeon_boss_rule(world.get_location('Misery Mire - Boss', player))
    set_defeat_dungeon_boss_rule(world.get_location('Misery Mire - Prize', player))
    for location in ['Misery Mire - Big Chest', 'Misery Mire - Boss']:
        forbid_item(world.get_location(location, player), 'Big Key (Misery Mire)', player)

    set_rule(world.get_entrance('Turtle Rock Entrance Gap', player), lambda state: state.has('Cane of Somaria', player))
    set_rule(world.get_entrance('Turtle Rock Entrance Gap Reverse', player), lambda state: state.has('Cane of Somaria', player))
    set_rule(world.get_location('Turtle Rock - Compass Chest', player), lambda state: state.has('Cane of Somaria', player))  # We could get here from the middle section without Cane as we don't cross the entrance gap!
    set_rule(world.get_location('Turtle Rock - Roller Room - Left', player), lambda state: state.has('Cane of Somaria', player) and state.has('Fire Rod', player))
    set_rule(world.get_location('Turtle Rock - Roller Room - Right', player), lambda state: state.has('Cane of Somaria', player) and state.has('Fire Rod', player))
    set_rule(world.get_location('Turtle Rock - Big Chest', player), lambda state: state.has('Big Key (Turtle Rock)', player) and (state.has('Cane of Somaria', player) or state.has('Hookshot', player)))
    set_rule(world.get_entrance('Turtle Rock (Big Chest) (North)', player), lambda state: state.has('Cane of Somaria', player) or state.has('Hookshot', player))
    set_rule(world.get_entrance('Turtle Rock Big Key Door', player), lambda state: state.has('Big Key (Turtle Rock)', player))
    set_rule(world.get_entrance('Turtle Rock (Dark Room) (North)', player), lambda state: state.has('Cane of Somaria', player))
    set_rule(world.get_entrance('Turtle Rock (Dark Room) (South)', player), lambda state: state.has('Cane of Somaria', player))
    set_rule(world.get_location('Turtle Rock - Eye Bridge - Bottom Left', player), lambda state: state.has('Cane of Byrna', player) or state.has('Cape', player) or state.has('Mirror Shield', player))
    set_rule(world.get_location('Turtle Rock - Eye Bridge - Bottom Right', player), lambda state: state.has('Cane of Byrna', player) or state.has('Cape', player) or state.has('Mirror Shield', player))
    set_rule(world.get_location('Turtle Rock - Eye Bridge - Top Left', player), lambda state: state.has('Cane of Byrna', player) or state.has('Cape', player) or state.has('Mirror Shield', player))
    set_rule(world.get_location('Turtle Rock - Eye Bridge - Top Right', player), lambda state: state.has('Cane of Byrna', player) or state.has('Cape', player) or state.has('Mirror Shield', player))
    set_rule(world.get_entrance('Turtle Rock (Trinexx)', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 4) and state.has('Big Key (Turtle Rock)', player) and state.has('Cane of Somaria', player))
    set_defeat_dungeon_boss_rule(world.get_location('Turtle Rock - Boss', player))
    set_defeat_dungeon_boss_rule(world.get_location('Turtle Rock - Prize', player))

    set_rule(world.get_entrance('Palace of Darkness Bonk Wall', player), lambda state: state.can_shoot_arrows(player))
    set_rule(world.get_entrance('Palace of Darkness Hammer Peg Drop', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Palace of Darkness Bridge Room', player), lambda state: state.has_key('Small Key (Palace of Darkness)', player, 1))  # If we can reach any other small key door, we already have back door access to this area
    set_rule(world.get_entrance('Palace of Darkness Big Key Door', player), lambda state: state.has_key('Small Key (Palace of Darkness)', player, 6) and state.has('Big Key (Palace of Darkness)', player) and state.can_shoot_arrows(player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Palace of Darkness (North)', player), lambda state: state.has_key('Small Key (Palace of Darkness)', player, 4))
    set_rule(world.get_location('Palace of Darkness - Big Chest', player), lambda state: state.has('Big Key (Palace of Darkness)', player))

    set_rule(world.get_entrance('Palace of Darkness Big Key Chest Staircase', player), lambda state: state.has_key('Small Key (Palace of Darkness)', player, 6)  or (item_name(state, 'Palace of Darkness - Big Key Chest', player) in [('Small Key (Palace of Darkness)', player)] and state.has_key('Small Key (Palace of Darkness)', player, 3)))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Palace of Darkness - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Palace of Darkness)' and item.player == player and state.has_key('Small Key (Palace of Darkness)', player, 5))
    else:
        forbid_item(world.get_location('Palace of Darkness - Big Key Chest', player), 'Small Key (Palace of Darkness)', player)

    set_rule(world.get_entrance('Palace of Darkness Spike Statue Room Door', player), lambda state: state.has_key('Small Key (Palace of Darkness)', player, 6) or (item_name(state, 'Palace of Darkness - Harmless Hellway', player) in [('Small Key (Palace of Darkness)', player)] and state.has_key('Small Key (Palace of Darkness)', player, 4)))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Palace of Darkness - Harmless Hellway', player), lambda state, item: item.name == 'Small Key (Palace of Darkness)' and item.player == player and state.has_key('Small Key (Palace of Darkness)', player, 5))
    else:
        forbid_item(world.get_location('Palace of Darkness - Harmless Hellway', player), 'Small Key (Palace of Darkness)', player)

    set_rule(world.get_entrance('Palace of Darkness Maze Door', player), lambda state: state.has_key('Small Key (Palace of Darkness)', player, 6))
    set_defeat_dungeon_boss_rule(world.get_location('Palace of Darkness - Boss', player))
    set_defeat_dungeon_boss_rule(world.get_location('Palace of Darkness - Prize', player))

    # these key rules are conservative, you might be able to get away with more lenient rules
    randomizer_room_chests = ['Ganons Tower - Randomizer Room - Top Left', 'Ganons Tower - Randomizer Room - Top Right', 'Ganons Tower - Randomizer Room - Bottom Left', 'Ganons Tower - Randomizer Room - Bottom Right']
    compass_room_chests = ['Ganons Tower - Compass Room - Top Left', 'Ganons Tower - Compass Room - Top Right', 'Ganons Tower - Compass Room - Bottom Left', 'Ganons Tower - Compass Room - Bottom Right']

    set_rule(world.get_location('Ganons Tower - Bob\'s Torch', player), lambda state: state.has_Boots(player))
    set_rule(world.get_entrance('Ganons Tower (Tile Room)', player), lambda state: state.has('Cane of Somaria', player))
    set_rule(world.get_entrance('Ganons Tower (Hookshot Room)', player), lambda state: state.has('Hammer', player))

    set_rule(world.get_entrance('Ganons Tower (Map Room)', player), lambda state: state.has_key('Small Key (Ganons Tower)', player, 4) or (item_name(state, 'Ganons Tower - Map Chest', player) in [('Big Key (Ganons Tower)', player), ('Small Key (Ganons Tower)', player)] and state.has_key('Small Key (Ganons Tower)', player, 3)))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Ganons Tower - Map Chest', player), lambda state, item: item.name == 'Small Key (Ganons Tower)' and item.player == player and state.has_key('Small Key (Ganons Tower)', player, 3))
    else:
        forbid_item(world.get_location('Ganons Tower - Map Chest', player), 'Small Key (Ganons Tower)', player)

    # It is possible to need more than 2 keys to get through this entance if you spend keys elsewhere. We reflect this in the chest requirements.
    # However we need to leave these at the lower values to derive that with 3 keys it is always possible to reach Bob and Ice Armos.
    set_rule(world.get_entrance('Ganons Tower (Double Switch Room)', player), lambda state: state.has_key('Small Key (Ganons Tower)', player, 2))
    # It is possible to need more than 3 keys ....
    set_rule(world.get_entrance('Ganons Tower (Firesnake Room)', player), lambda state: state.has_key('Small Key (Ganons Tower)', player, 3))

    #The actual requirements for these rooms to avoid key-lock
    set_rule(world.get_location('Ganons Tower - Firesnake Room', player), lambda state: state.has_key('Small Key (Ganons Tower)', player, 3) or (item_in_locations(state, 'Big Key (Ganons Tower)', player, zip(randomizer_room_chests, [player] * len(randomizer_room_chests))) and state.has_key('Small Key (Ganons Tower)', player, 2)))
    for location in randomizer_room_chests:
        set_rule(world.get_location(location, player), lambda state: state.has_key('Small Key (Ganons Tower)', player, 4) or (item_in_locations(state, 'Big Key (Ganons Tower)', player, zip(randomizer_room_chests, [player] * len(randomizer_room_chests))) and state.has_key('Small Key (Ganons Tower)', player, 3)))

    # Once again it is possible to need more than 3 keys...
    set_rule(world.get_entrance('Ganons Tower (Tile Room) Key Door', player), lambda state: state.has_key('Small Key (Ganons Tower)', player, 3) and state.has('Fire Rod', player))
    # Actual requirements
    for location in compass_room_chests:
        set_rule(world.get_location(location, player), lambda state: state.has('Fire Rod', player) and (state.has_key('Small Key (Ganons Tower)', player, 4) or (item_in_locations(state, 'Big Key (Ganons Tower)', player, zip(compass_room_chests, [player] * len(compass_room_chests))) and state.has_key('Small Key (Ganons Tower)', player, 3))))

    set_rule(world.get_location('Ganons Tower - Big Chest', player), lambda state: state.has('Big Key (Ganons Tower)', player))

    set_rule(world.get_location('Ganons Tower - Big Key Room - Left', player), lambda state: world.get_location('Ganons Tower - Big Key Room - Left', player).parent_region.dungeon.bosses['bottom'].can_defeat(state))
    set_rule(world.get_location('Ganons Tower - Big Key Chest', player), lambda state: world.get_location('Ganons Tower - Big Key Chest', player).parent_region.dungeon.bosses['bottom'].can_defeat(state))
    set_rule(world.get_location('Ganons Tower - Big Key Room - Right', player), lambda state: world.get_location('Ganons Tower - Big Key Room - Right', player).parent_region.dungeon.bosses['bottom'].can_defeat(state))

    set_rule(world.get_entrance('Ganons Tower Big Key Door', player), lambda state: state.has('Big Key (Ganons Tower)', player) and state.can_shoot_arrows(player))
    set_rule(world.get_entrance('Ganons Tower Torch Rooms', player), lambda state: state.has_fire_source(player) and world.get_entrance('Ganons Tower Torch Rooms', player).parent_region.dungeon.bosses['middle'].can_defeat(state))
    set_rule(world.get_location('Ganons Tower - Pre-Moldorm Chest', player), lambda state: state.has_key('Small Key (Ganons Tower)', player, 3))
    set_rule(world.get_entrance('Ganons Tower Moldorm Door', player), lambda state: state.has_key('Small Key (Ganons Tower)', player, 4))
    set_rule(world.get_entrance('Ganons Tower Moldorm Gap', player), lambda state: state.has('Hookshot', player) and world.get_entrance('Ganons Tower Moldorm Gap', player).parent_region.dungeon.bosses['top'].can_defeat(state))
    set_defeat_dungeon_boss_rule(world.get_location('Agahnim 2', player))
    for location in ['Ganons Tower - Big Chest', 'Ganons Tower - Mini Helmasaur Room - Left', 'Ganons Tower - Mini Helmasaur Room - Right',
                     'Ganons Tower - Pre-Moldorm Chest', 'Ganons Tower - Validation Chest']:
        forbid_item(world.get_location(location, player), 'Big Key (Ganons Tower)', player)

    set_rule(world.get_location('Ganon', player), lambda state: state.has_beam_sword(player) and state.has_fire_source(player) and state.has_crystals(world.crystals_needed_for_ganon[player], player)
                                                        and (state.has('Tempered Sword', player) or state.has('Golden Sword', player) or (state.has('Silver Arrows', player) and state.can_shoot_arrows(player)) or state.has('Lamp', player) or state.can_extend_magic(player, 12)))  # need to light torch a sufficient amount of times
    set_rule(world.get_entrance('Ganon Drop', player), lambda state: state.has_beam_sword(player))  # need to damage ganon to get tiles to drop


def default_rules(world, player):
    if world.mode[player] == 'standard':
        world.get_region('Hyrule Castle Secret Entrance', player).can_reach_private = lambda state: True
        old_rule = world.get_region('Links House', player).can_reach_private
        world.get_region('Links House', player).can_reach_private = lambda state: state.can_reach('Sanctuary', 'Region', player) or old_rule(state)
    else:
        # these are default save&quit points and always accessible
        world.get_region('Links House', player).can_reach_private = lambda state: True
        world.get_region('Sanctuary', player).can_reach_private = lambda state: True

    # overworld requirements
    set_rule(world.get_entrance('Kings Grave', player), lambda state: state.has_Boots(player))
    set_rule(world.get_entrance('Kings Grave Outer Rocks', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Kings Grave Inner Rocks', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Kings Grave Mirror Spot', player), lambda state: state.has_Pearl(player) and state.has_Mirror(player))
    # Caution: If king's grave is releaxed at all to account for reaching it via a two way cave's exit in insanity mode, then the bomb shop logic will need to be updated (that would involve create a small ledge-like Region for it)
    set_rule(world.get_entrance('Bonk Fairy (Light)', player), lambda state: state.has_Boots(player))
    set_rule(world.get_entrance('Bat Cave Drop Ledge', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Lumberjack Tree Tree', player), lambda state: state.has_Boots(player) and state.has('Beat Agahnim 1', player))
    set_rule(world.get_entrance('Bonk Rock Cave', player), lambda state: state.has_Boots(player))
    set_rule(world.get_entrance('Desert Palace Stairs', player), lambda state: state.has('Book of Mudora', player))
    set_rule(world.get_entrance('Sanctuary Grave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('20 Rupee Cave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('50 Rupee Cave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Death Mountain Entrance Rock', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Bumper Cave Entrance Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Flute Spot 1', player), lambda state: state.has('Ocarina', player))
    set_rule(world.get_entrance('Lake Hylia Central Island Teleporter', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Dark Desert Teleporter', player), lambda state: state.has('Ocarina', player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('East Hyrule Teleporter', player), lambda state: state.has('Hammer', player) and state.can_lift_rocks(player) and state.has_Pearl(player)) # bunny cannot use hammer
    set_rule(world.get_entrance('South Hyrule Teleporter', player), lambda state: state.has('Hammer', player) and state.can_lift_rocks(player) and state.has_Pearl(player)) # bunny cannot use hammer
    set_rule(world.get_entrance('Kakariko Teleporter', player), lambda state: ((state.has('Hammer', player) and state.can_lift_rocks(player)) or state.can_lift_heavy_rocks(player)) and state.has_Pearl(player)) # bunny cannot lift bushes
    set_rule(world.get_location('Flute Spot', player), lambda state: state.has('Shovel', player))

    set_rule(world.get_location('Zora\'s Ledge', player), lambda state: state.has('Flippers', player))
    set_rule(world.get_entrance('Waterfall of Wishing', player), lambda state: state.has('Flippers', player))  # can be fake flippered into, but is in weird state inside that might prevent you from doing things. Can be improved in future Todo
    set_rule(world.get_location('Frog', player), lambda state: state.can_lift_heavy_rocks(player)) # will get automatic moon pearl requirement
    set_rule(world.get_location('Potion Shop', player), lambda state: state.has('Mushroom', player))
    set_rule(world.get_entrance('Desert Palace Entrance (North) Rocks', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Desert Ledge Return Rocks', player), lambda state: state.can_lift_rocks(player))  # should we decide to place something that is not a dungeon end up there at some point
    set_rule(world.get_entrance('Checkerboard Cave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Agahnims Tower', player), lambda state: state.has('Cape', player) or state.has_beam_sword(player) or state.has('Beat Agahnim 1', player))  # barrier gets removed after killing agahnim, relevant for entrance shuffle
    set_rule(world.get_entrance('Top of Pyramid', player), lambda state: state.has('Beat Agahnim 1', player))
    set_rule(world.get_entrance('Old Man Cave Exit (West)', player), lambda state: False)  # drop cannot be climbed up
    set_rule(world.get_entrance('Broken Bridge (West)', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_entrance('Broken Bridge (East)', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_entrance('East Death Mountain Teleporter', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Fairy Ascension Rocks', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Paradox Cave Push Block Reverse', player), lambda state: state.has('Mirror', player))  # can erase block
    set_rule(world.get_entrance('Death Mountain (Top)', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Turtle Rock Teleporter', player), lambda state: state.can_lift_heavy_rocks(player) and state.has('Hammer', player))
    set_rule(world.get_entrance('East Death Mountain (Top)', player), lambda state: state.has('Hammer', player))

    set_rule(world.get_location('Catfish', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Northeast Dark World Broken Bridge Pass', player), lambda state: state.has_Pearl(player) and (state.can_lift_rocks(player) or state.has('Hammer', player) or state.has('Flippers', player)))
    set_rule(world.get_entrance('East Dark World Broken Bridge Pass', player), lambda state: state.has_Pearl(player) and (state.can_lift_rocks(player) or state.has('Hammer', player)))
    set_rule(world.get_entrance('South Dark World Bridge', player), lambda state: state.has('Hammer', player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Bonk Fairy (Dark)', player), lambda state: state.has_Pearl(player) and state.has_Boots(player))
    set_rule(world.get_entrance('West Dark World Gap', player), lambda state: state.has_Pearl(player) and state.has('Hookshot', player))
    set_rule(world.get_entrance('Palace of Darkness', player), lambda state: state.has_Pearl(player)) # kiki needs pearl
    set_rule(world.get_entrance('Hyrule Castle Ledge Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Hyrule Castle Main Gate', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: (state.has_Pearl(player) and state.has('Flippers', player) or state.has_Mirror(player)))  # Overworld Bunny Revival
    set_rule(world.get_location('Bombos Tablet', player), lambda state: state.has('Book of Mudora', player) and state.has_beam_sword(player) and state.has_Mirror(player))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (South)', player), lambda state: state.has_Pearl(player) and state.has('Flippers', player))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Fairy', player), lambda state: state.has_Pearl(player)) # bomb required
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Spike Cave', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has_Pearl(player) and (state.has('Hammer', player) or state.can_lift_rocks(player)))  # Fake Flippers
    set_rule(world.get_entrance('Village of Outcasts Heavy Rock', player), lambda state: state.has_Pearl(player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Hype Cave', player), lambda state: state.has_Pearl(player)) # bomb required
    set_rule(world.get_entrance('Brewery', player), lambda state: state.has_Pearl(player)) # bomb required
    set_rule(world.get_entrance('Thieves Town', player), lambda state: state.has_Pearl(player)) # bunny cannot pull
    set_rule(world.get_entrance('Skull Woods First Section Hole (North)', player), lambda state: state.has_Pearl(player)) # bunny cannot lift bush
    set_rule(world.get_entrance('Skull Woods Second Section Hole', player), lambda state: state.has_Pearl(player)) # bunny cannot lift bush
    set_rule(world.get_entrance('Maze Race Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Cave 45 Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('East Dark World Bridge', player), lambda state: state.has_Pearl(player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Lake Hylia Island Mirror Spot', player), lambda state: state.has_Pearl(player) and state.has_Mirror(player) and state.has('Flippers', player))
    set_rule(world.get_entrance('Lake Hylia Central Island Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('East Dark World River Pier', player), lambda state: state.has_Pearl(player) and state.has('Flippers', player))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Graveyard Ledge Mirror Spot', player), lambda state: state.has_Pearl(player) and state.has_Mirror(player))
    set_rule(world.get_entrance('Bumper Cave Entrance Rock', player), lambda state: state.has_Pearl(player) and state.can_lift_rocks(player))
    set_rule(world.get_entrance('Bumper Cave Ledge Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Bat Cave Drop Ledge Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Dark World Hammer Peg Cave', player), lambda state: state.has_Pearl(player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Village of Outcasts Eastern Rocks', player), lambda state: state.has_Pearl(player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Peg Area Rocks', player), lambda state: state.has_Pearl(player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Village of Outcasts Pegs', player), lambda state: state.has_Pearl(player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Grassy Lawn Pegs', player), lambda state: state.has_Pearl(player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Bumper Cave Exit (Top)', player), lambda state: state.has('Cape', player))
    set_rule(world.get_entrance('Bumper Cave Exit (Bottom)', player), lambda state: state.has('Cape', player) or state.has('Hookshot', player))

    set_rule(world.get_entrance('Skull Woods Final Section', player), lambda state: state.has('Fire Rod', player) and state.has_Pearl(player)) # bunny cannot use fire rod
    set_rule(world.get_entrance('Misery Mire', player), lambda state: state.has_Pearl(player) and state.has_sword(player) and state.has_misery_mire_medallion(player))  # sword required to cast magic (!)
    set_rule(world.get_entrance('Desert Ledge (Northeast) Mirror Spot', player), lambda state: state.has_Mirror(player))

    set_rule(world.get_entrance('Desert Ledge Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Desert Palace Stairs Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Desert Palace Entrance (North) Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Spectacle Rock Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Hookshot Cave', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))

    set_rule(world.get_entrance('East Death Mountain (Top) Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Mimic Cave Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Spiral Cave Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Fairy Ascension Mirror Spot', player), lambda state: state.has_Mirror(player) and state.has_Pearl(player))  # need to lift flowers
    set_rule(world.get_entrance('Isolated Ledge Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Superbunny Cave Exit (Bottom)', player), lambda state: False)  # Cannot get to bottom exit from top. Just exists for shuffling
    set_rule(world.get_entrance('Floating Island Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Turtle Rock', player), lambda state: state.has_Pearl(player) and state.has_sword(player) and state.has_turtle_rock_medallion(player) and state.can_reach('Turtle Rock (Top)', 'Region', player))  # sword required to cast magic (!)

    set_rule(world.get_entrance('Pyramid Hole', player), lambda state: state.has('Beat Agahnim 2', player) or world.open_pyramid[player])
    set_rule(world.get_entrance('Ganons Tower', player), lambda state: False) # This is a safety for the TR function below to not require GT entrance in its key logic.

    if world.swords[player] == 'swordless':
        swordless_rules(world, player)

    set_trock_key_rules(world, player)

    set_rule(world.get_entrance('Ganons Tower', player), lambda state: state.has_crystals(world.crystals_needed_for_gt[player], player))

def inverted_rules(world, player):
    # s&q regions. link's house entrance is set to true so the filler knows the chest inside can always be reached
    world.get_region('Inverted Links House', player).can_reach_private = lambda state: True
    world.get_region('Inverted Links House', player).entrances[0].can_reach = lambda state: True
    world.get_region('Inverted Dark Sanctuary', player).entrances[0].parent_region.can_reach_private = lambda state: True

    old_rule = world.get_region('Hyrule Castle Ledge', player).can_reach_private
    world.get_region('Hyrule Castle Ledge', player).can_reach_private = lambda state: (state.has_Mirror(player) and state.has('Beat Agahnim 1', player) and state.can_reach_light_world(player)) or old_rule(state)

    # overworld requirements 
    set_rule(world.get_location('Maze Race', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Mini Moldorm Cave', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Light Hype Fairy', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Potion Shop Pier', player), lambda state: state.has('Flippers', player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Light World Pier', player), lambda state: state.has('Flippers', player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Kings Grave', player), lambda state: state.has_Boots(player) and state.can_lift_heavy_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Kings Grave Outer Rocks', player), lambda state: state.can_lift_heavy_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Kings Grave Inner Rocks', player), lambda state: state.can_lift_heavy_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Potion Shop Inner Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Potion Shop Outer Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Potion Shop Outer Rock', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Potion Shop Inner Rock', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Graveyard Cave Inner Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Graveyard Cave Outer Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Secret Passage Inner Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Secret Passage Outer Bushes', player), lambda state: state.has_Pearl(player))
    # Caution: If king's grave is releaxed at all to account for reaching it via a two way cave's exit in insanity mode, then the bomb shop logic will need to be updated (that would involve create a small ledge-like Region for it)
    set_rule(world.get_entrance('Bonk Fairy (Light)', player), lambda state: state.has_Boots(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Bat Cave Drop Ledge', player), lambda state: state.has('Hammer', player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Lumberjack Tree Tree', player), lambda state: state.has_Boots(player) and state.has_Pearl(player) and state.has('Beat Agahnim 1', player))
    set_rule(world.get_entrance('Bonk Rock Cave', player), lambda state: state.has_Boots(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Desert Palace Stairs', player), lambda state: state.has('Book of Mudora', player))  # bunny can use book
    set_rule(world.get_entrance('Sanctuary Grave', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('20 Rupee Cave', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('50 Rupee Cave', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Death Mountain Entrance Rock', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Bumper Cave Entrance Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Lake Hylia Central Island Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Dark Lake Hylia Central Island Teleporter', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Dark Desert Teleporter', player), lambda state: state.can_flute(player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('East Dark World Teleporter', player), lambda state: state.has('Hammer', player) and state.can_lift_rocks(player) and state.has_Pearl(player)) # bunny cannot use hammer
    set_rule(world.get_entrance('South Dark World Teleporter', player), lambda state: state.has('Hammer', player) and state.can_lift_rocks(player) and state.has_Pearl(player)) # bunny cannot use hammer
    set_rule(world.get_entrance('West Dark World Teleporter', player), lambda state: ((state.has('Hammer', player) and state.can_lift_rocks(player)) or state.can_lift_heavy_rocks(player)) and state.has_Pearl(player))
    set_rule(world.get_location('Flute Spot', player), lambda state: state.has('Shovel', player) and state.has_Pearl(player))

    set_rule(world.get_location('Zora\'s Ledge', player), lambda state: state.has('Flippers', player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Waterfall of Wishing', player), lambda state: state.has('Flippers', player) and state.has_Pearl(player))  # can be fake flippered into, but is in weird state inside that might prevent you from doing things. Can be improved in future Todo
    set_rule(world.get_location('Frog', player), lambda state: state.can_lift_heavy_rocks(player) or (state.can_reach('Light World', 'Region', player) and state.has_Mirror(player)))
    set_rule(world.get_location('Mushroom', player), lambda state: state.has_Pearl(player)) # need pearl to pick up bushes
    set_rule(world.get_entrance('Bush Covered Lawn Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Bush Covered Lawn Inner Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Bush Covered Lawn Outer Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Bomb Hut Inner Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Bomb Hut Outer Bushes', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('North Fairy Cave Drop', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Lost Woods Hideout Drop', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_location('Potion Shop', player), lambda state: state.has('Mushroom', player) and (state.can_reach('Potion Shop Area', 'Region', player))) # new inverted region, need pearl for bushes or access to potion shop door/waterfall fairy
    set_rule(world.get_entrance('Desert Palace Entrance (North) Rocks', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Desert Ledge Return Rocks', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))  # should we decide to place something that is not a dungeon end up there at some point
    set_rule(world.get_entrance('Checkerboard Cave', player), lambda state: state.can_lift_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Hyrule Castle Secret Entrance Drop', player), lambda state: state.has_Pearl(player))
    set_rule(world.get_entrance('Old Man Cave Exit (West)', player), lambda state: False)  # drop cannot be climbed up
    set_rule(world.get_entrance('Broken Bridge (West)', player), lambda state: state.has('Hookshot', player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Broken Bridge (East)', player), lambda state: state.has('Hookshot', player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Dark Death Mountain Teleporter (East Bottom)', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Fairy Ascension Rocks', player), lambda state: state.can_lift_heavy_rocks(player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Paradox Cave Push Block Reverse', player), lambda state: state.has('Mirror', player))  # can erase block
    set_rule(world.get_entrance('Death Mountain (Top)', player), lambda state: state.has('Hammer', player) and state.has_Pearl(player))
    set_rule(world.get_entrance('Dark Death Mountain Teleporter (East)', player), lambda state: state.can_lift_heavy_rocks(player) and state.has('Hammer', player) and state.has_Pearl(player))  # bunny cannot use hammer
    set_rule(world.get_entrance('East Death Mountain (Top)', player), lambda state: state.has('Hammer', player) and state.has_Pearl(player))  # bunny can not use hammer

    set_rule(world.get_location('Catfish', player), lambda state: state.can_lift_rocks(player) or (state.has('Flippers', player) and state.has_Mirror(player) and state.has_Pearl(player) and state.can_reach('Light World', 'Region', player)))
    set_rule(world.get_entrance('Northeast Dark World Broken Bridge Pass', player), lambda state: ((state.can_lift_rocks(player) or state.has('Hammer', player)) or state.has('Flippers', player)))
    set_rule(world.get_entrance('East Dark World Broken Bridge Pass', player), lambda state: (state.can_lift_rocks(player) or state.has('Hammer', player)))
    set_rule(world.get_entrance('South Dark World Bridge', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Bonk Fairy (Dark)', player), lambda state: state.has_Boots(player))
    set_rule(world.get_entrance('West Dark World Gap', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: state.has('Flippers', player))
    set_rule(world.get_location('Bombos Tablet', player), lambda state: state.has('Book of Mudora', player) and state.has_beam_sword(player))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (South)', player), lambda state: state.has('Flippers', player))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Pier', player), lambda state: state.has('Flippers', player))
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Spike Cave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has('Flippers', player) and (state.has('Hammer', player) or state.can_lift_rocks(player)))  # Fake Flippers
    set_rule(world.get_entrance('Village of Outcasts Heavy Rock', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('East Dark World Bridge', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Lake Hylia Central Island Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('East Dark World River Pier', player), lambda state: state.has('Flippers', player))  # ToDo any fake flipper set up? (Qirn Jump)
    set_rule(world.get_entrance('Bumper Cave Entrance Rock', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Bumper Cave Ledge Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Hammer Peg Area Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Dark World Hammer Peg Cave', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Village of Outcasts Eastern Rocks', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Peg Area Rocks', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Village of Outcasts Pegs', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Grassy Lawn Pegs', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Bumper Cave Exit (Top)', player), lambda state: state.has('Cape', player))
    set_rule(world.get_entrance('Bumper Cave Exit (Bottom)', player), lambda state: state.has('Cape', player) or state.has('Hookshot', player))

    set_rule(world.get_entrance('Skull Woods Final Section', player), lambda state: state.has('Fire Rod', player)) 
    set_rule(world.get_entrance('Misery Mire', player), lambda state: state.has_sword(player) and state.has_misery_mire_medallion(player))  # sword required to cast magic (!)

    set_rule(world.get_entrance('Hookshot Cave', player), lambda state: state.can_lift_rocks(player))

    set_rule(world.get_entrance('East Death Mountain Mirror Spot (Top)', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Death Mountain (Top) Mirror Spot', player), lambda state: state.has_Mirror(player))

    set_rule(world.get_entrance('East Death Mountain Mirror Spot (Bottom)', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Dark Death Mountain Ledge Mirror Spot (East)', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Dark Death Mountain Ledge Mirror Spot (West)', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Laser Bridge Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Superbunny Cave Exit (Bottom)', player), lambda state: False)  # Cannot get to bottom exit from top. Just exists for shuffling
    set_rule(world.get_entrance('Floating Island Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Turtle Rock', player), lambda state: state.has_sword(player) and state.has_turtle_rock_medallion(player) and state.can_reach('Turtle Rock (Top)', 'Region', player)) # sword required to cast magic (!)
    
    # new inverted spots
    set_rule(world.get_entrance('Post Aga Teleporter', player), lambda state: state.has('Beat Agahnim 1', player))
    set_rule(world.get_entrance('Mire Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Desert Palace Stairs Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Death Mountain Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('East Dark World Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('West Dark World Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('South Dark World Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Northeast Dark World Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Potion Shop Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Shopping Mall Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Maze Race Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Desert Palace North Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Death Mountain (Top) Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Graveyard Cave Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Bomb Hut Mirror Spot', player), lambda state: state.has_Mirror(player))
    set_rule(world.get_entrance('Skull Woods Mirror Spot', player), lambda state: state.has_Mirror(player))
    
    # inverted flute spots

    set_rule(world.get_entrance('DDM Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('NEDW Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('WDW Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('SDW Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('EDW Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('DLHL Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('DD Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('EDDM Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('Dark Grassy Lawn Flute', player), lambda state: state.can_flute(player))
    set_rule(world.get_entrance('Hammer Peg Area Flute', player), lambda state: state.can_flute(player))
    
    set_rule(world.get_entrance('Inverted Pyramid Hole', player), lambda state: state.has('Beat Agahnim 2', player) or world.open_pyramid[player])
    set_rule(world.get_entrance('Inverted Ganons Tower', player), lambda state: False) # This is a safety for the TR function below to not require GT entrance in its key logic.

    if world.swords[player] == 'swordless':
        swordless_rules(world, player)

    set_trock_key_rules(world, player)

    set_rule(world.get_entrance('Inverted Ganons Tower', player), lambda state: state.has_crystals(world.crystals_needed_for_gt[player], player))

def no_glitches_rules(world, player):
    if world.mode[player] != 'inverted':
        set_rule(world.get_entrance('Zoras River', player), lambda state: state.has('Flippers', player) or state.can_lift_rocks(player))
        set_rule(world.get_entrance('Lake Hylia Central Island Pier', player), lambda state: state.has('Flippers', player))  # can be fake flippered to
        set_rule(world.get_entrance('Hobo Bridge', player), lambda state: state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: state.has_Pearl(player) and state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has_Pearl(player) and state.has('Flippers', player) and (state.has('Hammer', player) or state.can_lift_rocks(player)))
        set_rule(world.get_entrance('Dark Lake Hylia Ledge Drop', player), lambda state: state.has_Pearl(player) and state.has('Flippers', player))
    else:
        set_rule(world.get_entrance('Zoras River', player), lambda state: state.has_Pearl(player) and (state.has('Flippers', player) or state.can_lift_rocks(player)))
        set_rule(world.get_entrance('Lake Hylia Central Island Pier', player), lambda state: state.has_Pearl(player) and state.has('Flippers', player))  # can be fake flippered to
        set_rule(world.get_entrance('Lake Hylia Island', player), lambda state: state.has_Pearl(player) and state.has('Flippers', player))
        set_rule(world.get_entrance('Hobo Bridge', player), lambda state: state.has_Pearl(player) and state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has('Flippers', player) and (state.has('Hammer', player) or state.can_lift_rocks(player)))
        set_rule(world.get_entrance('Dark Lake Hylia Ledge Drop', player), lambda state: state.has('Flippers', player))
        set_rule(world.get_entrance('East Dark World Pier', player), lambda state: state.has('Flippers', player))

    add_rule(world.get_entrance('Ganons Tower (Hookshot Room)', player), lambda state: state.has('Hookshot', player) or state.has_Boots(player))
    add_rule(world.get_entrance('Ganons Tower (Double Switch Room)', player), lambda state: state.has('Hookshot', player))
    DMs_room_chests = ['Ganons Tower - DMs Room - Top Left', 'Ganons Tower - DMs Room - Top Right', 'Ganons Tower - DMs Room - Bottom Left', 'Ganons Tower - DMs Room - Bottom Right']
    for location in DMs_room_chests:
        add_rule(world.get_location(location, player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_entrance('Paradox Cave Push Block Reverse', player), lambda state: False)  # no glitches does not require block override
    set_rule(world.get_entrance('Paradox Cave Bomb Jump', player), lambda state: False)
    set_rule(world.get_entrance('Skull Woods First Section Bomb Jump', player), lambda state: False)

    # Light cones in standard depend on which world we actually are in, not which one the location would normally be
    # We add Lamp requirements only to those locations which lie in the dark world (or everything if open
    DW_Entrances = ['Bumper Cave (Bottom)', 'Superbunny Cave (Top)', 'Superbunny Cave (Bottom)', 'Hookshot Cave', 'Bumper Cave (Top)', 'Hookshot Cave Back Entrance', 'Dark Death Mountain Ledge (East)',
                    'Turtle Rock Isolated Ledge Entrance', 'Thieves Town', 'Skull Woods Final Section', 'Ice Palace', 'Misery Mire', 'Palace of Darkness', 'Swamp Palace', 'Turtle Rock', 'Dark Death Mountain Ledge (West)']

    def check_is_dark_world(region):
        for entrance in region.entrances:
            if entrance.name in DW_Entrances:
                return True
        return False

    def add_conditional_lamp(spot, region, spottype='Location'):
        if spottype == 'Location':
            spot = world.get_location(spot, player)
        else:
            spot = world.get_entrance(spot, player)
        if (not world.dark_world_light_cone and check_is_dark_world(world.get_region(region, player))) or (not world.light_world_light_cone and not check_is_dark_world(world.get_region(region, player))):
            add_lamp_requirement(spot, player)

    add_conditional_lamp('Misery Mire (Vitreous)', 'Misery Mire (Entrance)', 'Entrance')
    add_conditional_lamp('Turtle Rock (Dark Room) (North)', 'Turtle Rock (Entrance)', 'Entrance')
    add_conditional_lamp('Turtle Rock (Dark Room) (South)', 'Turtle Rock (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness Big Key Door', 'Palace of Darkness (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness Maze Door', 'Palace of Darkness (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness - Dark Basement - Left', 'Palace of Darkness (Entrance)', 'Location')
    add_conditional_lamp('Palace of Darkness - Dark Basement - Right', 'Palace of Darkness (Entrance)', 'Location')
    if world.mode[player] != 'inverted':
        add_conditional_lamp('Agahnim 1', 'Agahnims Tower', 'Entrance')
        add_conditional_lamp('Castle Tower - Dark Maze', 'Agahnims Tower', 'Location')
    else:
        add_conditional_lamp('Agahnim 1', 'Inverted Agahnims Tower', 'Entrance')
        add_conditional_lamp('Castle Tower - Dark Maze', 'Inverted Agahnims Tower', 'Location')
    add_conditional_lamp('Old Man', 'Old Man Cave', 'Location')
    add_conditional_lamp('Old Man Cave Exit (East)', 'Old Man Cave', 'Entrance')
    add_conditional_lamp('Death Mountain Return Cave Exit (East)', 'Death Mountain Return Cave', 'Entrance')
    add_conditional_lamp('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave', 'Entrance')
    add_conditional_lamp('Old Man House Front to Back', 'Old Man House', 'Entrance')
    add_conditional_lamp('Old Man House Back to Front', 'Old Man House', 'Entrance')
    add_conditional_lamp('Eastern Palace - Big Key Chest', 'Eastern Palace', 'Location')
    add_conditional_lamp('Eastern Palace - Boss', 'Eastern Palace', 'Location')
    add_conditional_lamp('Eastern Palace - Prize', 'Eastern Palace', 'Location')

    if not world.sewer_light_cone[player]:
        add_lamp_requirement(world.get_location('Sewers - Dark Cross', player), player)
        add_lamp_requirement(world.get_entrance('Sewers Back Door', player), player)
        add_lamp_requirement(world.get_entrance('Throne Room', player), player)


def open_rules(world, player):
    # softlock protection as you can reach the sewers small key door with a guard drop key
    set_rule(world.get_location('Hyrule Castle - Boomerang Chest', player), lambda state: state.has_key('Small Key (Escape)', player))
    set_rule(world.get_location('Hyrule Castle - Zelda\'s Chest', player), lambda state: state.has_key('Small Key (Escape)', player))


def swordless_rules(world, player):

    set_rule(world.get_entrance('Agahnim 1', player), lambda state: (state.has('Hammer', player) or state.has('Fire Rod', player) or state.can_shoot_arrows(player) or state.has('Cane of Somaria', player)) and state.has_key('Small Key (Agahnims Tower)', player, 2))
    set_rule(world.get_location('Ether Tablet', player), lambda state: state.has('Book of Mudora', player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Skull Woods Torch Room', player), lambda state: state.has_key('Small Key (Skull Woods)', player, 3) and state.has('Fire Rod', player))  # no curtain
    set_rule(world.get_entrance('Ice Palace Entrance Room', player), lambda state: state.has('Fire Rod', player) or state.has('Bombos', player)) #in swordless mode bombos pads are present in the relevant parts of ice palace
    set_rule(world.get_location('Ganon', player), lambda state: state.has('Hammer', player) and state.has_fire_source(player) and state.has('Silver Arrows', player) and state.can_shoot_arrows(player) and state.has_crystals(world.crystals_needed_for_ganon[player], player))
    set_rule(world.get_entrance('Ganon Drop', player), lambda state: state.has('Hammer', player))  # need to damage ganon to get tiles to drop

    if world.mode[player] != 'inverted':
        set_rule(world.get_entrance('Agahnims Tower', player), lambda state: state.has('Cape', player) or state.has('Hammer', player) or state.has('Beat Agahnim 1', player))  # barrier gets removed after killing agahnim, relevant for entrance shuffle
        set_rule(world.get_entrance('Turtle Rock', player), lambda state: state.has_Pearl(player) and state.has_turtle_rock_medallion(player) and state.can_reach('Turtle Rock (Top)', 'Region', player))   # sword not required to use medallion for opening in swordless (!)
        set_rule(world.get_entrance('Misery Mire', player), lambda state: state.has_Pearl(player) and state.has_misery_mire_medallion(player))  # sword not required to use medallion for opening in swordless (!)
        set_rule(world.get_location('Bombos Tablet', player), lambda state: state.has('Book of Mudora', player) and state.has('Hammer', player) and state.has_Mirror(player))    
    else:
        # only need ddm access for aga tower in inverted
        set_rule(world.get_entrance('Turtle Rock', player), lambda state: state.has_turtle_rock_medallion(player) and state.can_reach('Turtle Rock (Top)', 'Region', player))   # sword not required to use medallion for opening in swordless (!)
        set_rule(world.get_entrance('Misery Mire', player), lambda state: state.has_misery_mire_medallion(player))  # sword not required to use medallion for opening in swordless (!)
        set_rule(world.get_location('Bombos Tablet', player), lambda state: state.has('Book of Mudora', player) and state.has('Hammer', player))


def standard_rules(world, player):
    set_rule(world.get_entrance('Hyrule Castle Exit (East)', player), lambda state: state.can_reach('Sanctuary', 'Region', player))
    set_rule(world.get_entrance('Hyrule Castle Exit (West)', player), lambda state: state.can_reach('Sanctuary', 'Region', player))


def set_trock_key_rules(world, player):


    # First set all relevant locked doors to impassible.
    for entrance in ['Turtle Rock Dark Room Staircase', 'Turtle Rock (Chain Chomp Room) (North)', 'Turtle Rock (Chain Chomp Room) (South)', 'Turtle Rock Pokey Room']:
        set_rule(world.get_entrance(entrance, player), lambda state: False)

    all_state = world.get_all_state(True)
    
    # Check if each of the four main regions of the dungoen can be reached. The previous code section prevents key-costing moves within the dungeon.
    can_reach_back = all_state.can_reach(world.get_region('Turtle Rock (Eye Bridge)', player)) if world.can_access_trock_eyebridge[player] is None else world.can_access_trock_eyebridge[player]
    world.can_access_trock_eyebridge[player] = can_reach_back
    can_reach_front = all_state.can_reach(world.get_region('Turtle Rock (Entrance)', player)) if world.can_access_trock_front[player] is None else world.can_access_trock_front[player]
    world.can_access_trock_front[player] = can_reach_front
    can_reach_big_chest = all_state.can_reach(world.get_region('Turtle Rock (Big Chest)', player)) if world.can_access_trock_big_chest[player] is None else world.can_access_trock_big_chest[player]
    world.can_access_trock_big_chest[player] = can_reach_big_chest
    can_reach_middle = all_state.can_reach(world.get_region('Turtle Rock (Second Section)', player)) if world.can_access_trock_middle[player] is None else world.can_access_trock_middle[player]
    world.can_access_trock_middle[player] = can_reach_middle

    # No matter what, the key requirement for going from the middle to the bottom should be three keys.
    set_rule(world.get_entrance('Turtle Rock Dark Room Staircase', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 3))

    # The following represent the most common and most restrictive key rules. These are overwritten later as needed.
    set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (South)', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 4))
    set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (North)', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 4))
    set_rule(world.get_entrance('Turtle Rock Pokey Room', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 4))

    # No matter what, the Big Key cannot be in the Big Chest or held by Trinexx.
    non_big_key_locations = ['Turtle Rock - Big Chest', 'Turtle Rock - Boss']

    def tr_big_key_chest_keys_needed(state):
        # This function handles the key requirements for the TR Big Chest in the situations it having the Big Key should logically require 2 keys, small key
        # should logically require no keys, and anything else should logically require 4 keys.
        item = item_name(state, 'Turtle Rock - Big Key Chest', player)
        if item in [('Small Key (Turtle Rock)', player)]:
            return 0
        if item in [('Big Key (Turtle Rock)', player)]:
            return 2
        return 4

    # Now we need to set rules based on which entrances we have access to. The most important point is whether we have back access. If we have back access, we
    # might open all the locked doors in any order so we need maximally restrictive rules.
    if can_reach_back:
        set_rule(world.get_location('Turtle Rock - Big Key Chest', player), lambda state: (state.has_key('Small Key (Turtle Rock)', player, 4) or item_name(state, 'Turtle Rock - Big Key Chest', player) == ('Small Key (Turtle Rock)', player)))
        if world.accessibility[player] != 'locations':
            set_always_allow(world.get_location('Turtle Rock - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Turtle Rock)' and item.player == player
                                                                                                            and state.can_reach(world.get_region('Turtle Rock (Eye Bridge)', player)))
        else:
            forbid_item(world.get_location('Turtle Rock - Big Key Chest', player), 'Small Key (Turtle Rock)', player)
    elif can_reach_front and can_reach_middle:
        set_rule(world.get_location('Turtle Rock - Big Key Chest', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, tr_big_key_chest_keys_needed(state)))
        if world.accessibility[player] != 'locations':
            set_always_allow(world.get_location('Turtle Rock - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Turtle Rock)' and item.player == player
                                                                                                            and state.can_reach(world.get_region('Turtle Rock (Entrance)', player)) and state.can_reach(world.get_region('Turtle Rock (Second Section)', player)))
        else:
            forbid_item(world.get_location('Turtle Rock - Big Key Chest', player), 'Small Key (Turtle Rock)', player)
        non_big_key_locations += ['Turtle Rock - Crystaroller Room', 'Turtle Rock - Eye Bridge - Bottom Left',
                                  'Turtle Rock - Eye Bridge - Bottom Right', 'Turtle Rock - Eye Bridge - Top Left',
                                  'Turtle Rock - Eye Bridge - Top Right']
    elif can_reach_front:
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (North)', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 2))
        set_rule(world.get_entrance('Turtle Rock Pokey Room', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 1))
        set_rule(world.get_location('Turtle Rock - Big Key Chest', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, tr_big_key_chest_keys_needed(state)))
        if world.accessibility[player] != 'locations':
            set_always_allow(world.get_location('Turtle Rock - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Turtle Rock)' and item.player == player and state.has_key('Small Key (Turtle Rock)', player, 2)
                                                                                                            and state.can_reach(world.get_region('Turtle Rock (Entrance)', player)))
        else:
            forbid_item(world.get_location('Turtle Rock - Big Key Chest', player), 'Small Key (Turtle Rock)', player)
        non_big_key_locations += ['Turtle Rock - Crystaroller Room', 'Turtle Rock - Eye Bridge - Bottom Left',
                                  'Turtle Rock - Eye Bridge - Bottom Right', 'Turtle Rock - Eye Bridge - Top Left',
                                  'Turtle Rock - Eye Bridge - Top Right']
    elif can_reach_big_chest:
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (South)', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 2) if item_in_locations(state, 'Big Key (Turtle Rock)', player, [('Turtle Rock - Compass Chest', player), ('Turtle Rock - Roller Room - Left', player), ('Turtle Rock - Roller Room - Right', player)]) else state.has_key('Small Key (Turtle Rock)', player, 4))
        set_rule(world.get_location('Turtle Rock - Big Key Chest', player), lambda state: (state.has_key('Small Key (Turtle Rock)', player, 4) or item_name(state, 'Turtle Rock - Big Key Chest', player) == ('Small Key (Turtle Rock)', player)))
        if world.accessibility[player] != 'locations':
            set_always_allow(world.get_location('Turtle Rock - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Turtle Rock)' and item.player == player
                                                                                                            and state.can_reach(world.get_region('Turtle Rock (Big Chest)', player)))
        else:
            forbid_item(world.get_location('Turtle Rock - Big Key Chest', player), 'Small Key (Turtle Rock)', player)
        non_big_key_locations += ['Turtle Rock - Crystaroller Room', 'Turtle Rock - Eye Bridge - Bottom Left',
                                  'Turtle Rock - Eye Bridge - Bottom Right', 'Turtle Rock - Eye Bridge - Top Left',
                                  'Turtle Rock - Eye Bridge - Top Right']
        if not world.keyshuffle[player]:
            non_big_key_locations += ['Turtle Rock - Big Key Chest']
    else:
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (South)', player), lambda state: state.has_key('Small Key (Turtle Rock)', player, 2) if item_in_locations(state, 'Big Key (Turtle Rock)', player, [('Turtle Rock - Compass Chest', player), ('Turtle Rock - Roller Room - Left', player), ('Turtle Rock - Roller Room - Right', player)]) else state.has_key('Small Key (Turtle Rock)', player, 4))
        set_rule(world.get_location('Turtle Rock - Big Key Chest', player), lambda state: (state.has_key('Small Key (Turtle Rock)', player, 4) or item_name(state, 'Turtle Rock - Big Key Chest', player) == ('Small Key (Turtle Rock)', player)))
        if world.accessibility[player] != 'locations':
            set_always_allow(world.get_location('Turtle Rock - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Turtle Rock)' and item.player == player)
        non_big_key_locations += ['Turtle Rock - Crystaroller Room', 'Turtle Rock - Eye Bridge - Bottom Left',
                                  'Turtle Rock - Eye Bridge - Bottom Right', 'Turtle Rock - Eye Bridge - Top Left',
                                  'Turtle Rock - Eye Bridge - Top Right']
        if not world.keyshuffle[player]:
            non_big_key_locations += ['Turtle Rock - Big Key Chest', 'Turtle Rock - Chain Chomps']

    # set big key restrictions
    for location in non_big_key_locations:
        forbid_item(world.get_location(location, player), 'Big Key (Turtle Rock)', player)

    # small key restriction
    for location in ['Turtle Rock - Boss']:
        forbid_item(world.get_location(location, player), 'Small Key (Turtle Rock)', player)


def set_big_bomb_rules(world, player):
    # this is a mess
    bombshop_entrance = world.get_region('Big Bomb Shop', player).entrances[0]
    Normal_LW_entrances = ['Blinds Hideout',
                           'Bonk Fairy (Light)',
                           'Lake Hylia Fairy',
                           'Light Hype Fairy',
                           'Desert Fairy',
                           'Chicken House',
                           'Aginahs Cave',
                           'Sahasrahlas Hut',
                           'Cave Shop (Lake Hylia)',
                           'Blacksmiths Hut',
                           'Sick Kids House',
                           'Lost Woods Gamble',
                           'Fortune Teller (Light)',
                           'Snitch Lady (East)',
                           'Snitch Lady (West)',
                           'Bush Covered House',
                           'Tavern (Front)',
                           'Light World Bomb Hut',
                           'Kakariko Shop',
                           'Mini Moldorm Cave',
                           'Long Fairy Cave',
                           'Good Bee Cave',
                           '20 Rupee Cave',
                           '50 Rupee Cave',
                           'Ice Rod Cave',
                           'Bonk Rock Cave',
                           'Library',
                           'Potion Shop',
                           'Dam',
                           'Lumberjack House',
                           'Lake Hylia Fortune Teller',
                           'Eastern Palace',
                           'Kakariko Gamble Game',
                           'Kakariko Well Cave',
                           'Bat Cave Cave',
                           'Elder House (East)',
                           'Elder House (West)',
                           'North Fairy Cave',
                           'Lost Woods Hideout Stump',
                           'Lumberjack Tree Cave',
                           'Two Brothers House (East)',
                           'Sanctuary',
                           'Hyrule Castle Entrance (South)',
                           'Hyrule Castle Secret Entrance Stairs']
    LW_walkable_entrances = ['Dark Lake Hylia Ledge Fairy',
                             'Dark Lake Hylia Ledge Spike Cave',
                             'Dark Lake Hylia Ledge Hint',
                             'Mire Shed',
                             'Dark Desert Hint',
                             'Dark Desert Fairy',
                             'Misery Mire']
    Northern_DW_entrances = ['Brewery',
                             'C-Shaped House',
                             'Chest Game',
                             'Dark World Hammer Peg Cave',
                             'Red Shield Shop',
                             'Dark Sanctuary Hint',
                             'Fortune Teller (Dark)',
                             'Dark World Shop',
                             'Dark World Lumberjack Shop',
                             'Thieves Town',
                             'Skull Woods First Section Door',
                             'Skull Woods Second Section Door (East)']
    Southern_DW_entrances = ['Hype Cave',
                             'Bonk Fairy (Dark)',
                             'Archery Game',
                             'Big Bomb Shop',
                             'Dark Lake Hylia Shop',
                             'Swamp Palace']
    Isolated_DW_entrances = ['Spike Cave',
                             'Cave Shop (Dark Death Mountain)',
                             'Dark Death Mountain Fairy',
                             'Mimic Cave',
                             'Skull Woods Second Section Door (West)',
                             'Skull Woods Final Section',
                             'Ice Palace',
                             'Turtle Rock',
                             'Dark Death Mountain Ledge (West)',
                             'Dark Death Mountain Ledge (East)',
                             'Bumper Cave (Top)',
                             'Superbunny Cave (Top)',
                             'Superbunny Cave (Bottom)',
                             'Hookshot Cave',
                             'Ganons Tower',
                             'Turtle Rock Isolated Ledge Entrance',
                             'Hookshot Cave Back Entrance']
    Isolated_LW_entrances = ['Capacity Upgrade',
                             'Tower of Hera',
                             'Death Mountain Return Cave (West)',
                             'Paradox Cave (Top)',
                             'Fairy Ascension Cave (Top)',
                             'Spiral Cave',
                             'Desert Palace Entrance (East)']
    West_LW_DM_entrances = ['Old Man Cave (East)',
                            'Old Man House (Bottom)',
                            'Old Man House (Top)',
                            'Death Mountain Return Cave (East)',
                            'Spectacle Rock Cave Peak',
                            'Spectacle Rock Cave',
                            'Spectacle Rock Cave (Bottom)']
    East_LW_DM_entrances = ['Paradox Cave (Bottom)',
                            'Paradox Cave (Middle)',
                            'Hookshot Fairy',
                            'Spiral Cave (Bottom)']
    Mirror_from_SDW_entrances = ['Two Brothers House (West)',
                                 'Cave 45']
    Castle_ledge_entrances = ['Hyrule Castle Entrance (West)',
                              'Hyrule Castle Entrance (East)',
                              'Agahnims Tower']
    Desert_mirrorable_ledge_entrances = ['Desert Palace Entrance (West)',
                                         'Desert Palace Entrance (North)',
                                         'Desert Palace Entrance (South)',
                                         'Checkerboard Cave']

    set_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.can_reach('East Dark World', 'Region', player) and state.can_reach('Big Bomb Shop', 'Region', player) and state.has('Crystal 5', player) and state.has('Crystal 6', player))

    #crossing peg bridge starting from the southern dark world
    def cross_peg_bridge(state):
        return state.has('Hammer', player) and state.has_Pearl(player)

    # returning via the eastern and southern teleporters needs the same items, so we use the southern teleporter for out routing.
    # crossing preg bridge already requires hammer so we just add the gloves to the requirement
    def southern_teleporter(state):
        return state.can_lift_rocks(player) and cross_peg_bridge(state)

    # the basic routes assume you can reach eastern light world with the bomb.
    # you can then use the southern teleporter, or (if you have beaten Aga1) the hyrule castle gate warp
    def basic_routes(state):
        return southern_teleporter(state) or state.can_reach('Top of Pyramid', 'Entrance', player)

    # Key for below abbreviations:
    # P = pearl
    # A = Aga1
    # H = hammer
    # M = Mirror
    # G = Glove

    if bombshop_entrance.name in Normal_LW_entrances:
        #1. basic routes
        #2. Can reach Eastern dark world some other way, mirror, get bomb, return to mirror spot, walk to pyramid: Needs mirror
        # -> M or BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: basic_routes(state) or state.has_Mirror(player))
    elif bombshop_entrance.name in LW_walkable_entrances:
        #1. Mirror then basic routes
        # -> M and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has_Mirror(player) and basic_routes(state))
    elif bombshop_entrance.name in Northern_DW_entrances:
        #1. Mirror and basic routes
        #2. Go to south DW and then cross peg bridge: Need Mitts and hammer and moon pearl
        # -> (Mitts and CPB) or (M and BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.can_lift_heavy_rocks(player) and cross_peg_bridge(state)) or (state.has_Mirror(player) and basic_routes(state)))
    elif bombshop_entrance.name == 'Bumper Cave (Bottom)':
        #1. Mirror and Lift rock and basic_routes
        #2. Mirror and Flute and basic routes (can make difference if accessed via insanity or w/ mirror from connector, and then via hyrule castle gate, because no gloves are needed in that case)
        #3. Go to south DW and then cross peg bridge: Need Mitts and hammer and moon pearl
        # -> (Mitts and CPB) or (((G or Flute) and M) and BR))
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.can_lift_heavy_rocks(player) and cross_peg_bridge(state)) or (((state.can_lift_rocks(player) or state.has('Ocarina', player)) and state.has_Mirror(player)) and basic_routes(state)))
    elif bombshop_entrance.name in Southern_DW_entrances:
        #1. Mirror and enter via gate: Need mirror and Aga1
        #2. cross peg bridge: Need hammer and moon pearl
        # -> CPB or (M and A)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: cross_peg_bridge(state) or (state.has_Mirror(player) and state.can_reach('Top of Pyramid', 'Entrance', player)))
    elif bombshop_entrance.name in Isolated_DW_entrances:
        # 1. mirror then flute then basic routes
        # -> M and Flute and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has_Mirror(player) and state.has('Ocarina', player) and basic_routes(state))
    elif bombshop_entrance.name in Isolated_LW_entrances:
        # 1. flute then basic routes
        # Prexisting mirror spot is not permitted, because mirror might have been needed to reach these isolated locations.
        # -> Flute and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Ocarina', player) and basic_routes(state))
    elif bombshop_entrance.name in West_LW_DM_entrances:
        # 1. flute then basic routes or mirror
        # Prexisting mirror spot is permitted, because flute can be used to reach west DM directly.
        # -> Flute and (M or BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Ocarina', player) and (state.has_Mirror(player) or basic_routes(state)))
    elif bombshop_entrance.name in East_LW_DM_entrances:
        # 1. flute then basic routes or mirror and hookshot
        # Prexisting mirror spot is permitted, because flute can be used to reach west DM directly and then east DM via Hookshot
        # -> Flute and ((M and Hookshot) or BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Ocarina', player) and ((state.has_Mirror(player) and state.has('Hookshot', player)) or basic_routes(state)))
    elif bombshop_entrance.name == 'Fairy Ascension Cave (Bottom)':
        # Same as East_LW_DM_entrances except navigation without BR requires Mitts
        # -> Flute and ((M and Hookshot and Mitts) or BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Ocarina', player) and ((state.has_Mirror(player) and state.has('Hookshot', player) and state.can_lift_heavy_rocks(player)) or basic_routes(state)))
    elif bombshop_entrance.name in Castle_ledge_entrances:
        # 1. mirror on pyramid to castle ledge, grab bomb, return through mirror spot: Needs mirror
        # 2. flute then basic routes
        # -> M or (Flute and BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has_Mirror(player) or (state.has('Ocarina', player) and basic_routes(state)))
    elif bombshop_entrance.name in Desert_mirrorable_ledge_entrances:
        # Cases when you have mire access: Mirror to reach locations, return via mirror spot, move to center of desert, mirror anagin and:
        # 1. Have mire access, Mirror to reach locations, return via mirror spot, move to center of desert, mirror again and then basic routes
        # 2. flute then basic routes
        # -> (Mire access and M) or Flute) and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: ((state.can_reach('Dark Desert', 'Region', player) and state.has_Mirror(player)) or state.has('Ocarina', player)) and basic_routes(state))
    elif bombshop_entrance.name == 'Old Man Cave (West)':
        # 1. Lift rock then basic_routes
        # 2. flute then basic_routes
        # -> (Flute or G) and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Ocarina', player) or state.can_lift_rocks(player)) and basic_routes(state))
    elif bombshop_entrance.name == 'Graveyard Cave':
        # 1. flute then basic routes
        # 2. (has west dark world access) use existing mirror spot (required Pearl), mirror again off ledge
        # -> (Flute or (M and P and West Dark World access) and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Ocarina', player) or (state.can_reach('West Dark World', 'Region', player) and state.has_Pearl(player) and state.has_Mirror(player))) and basic_routes(state))
    elif bombshop_entrance.name in Mirror_from_SDW_entrances:
        # 1. flute then basic routes
        # 2. (has South dark world access) use existing mirror spot, mirror again off ledge
        # -> (Flute or (M and South Dark World access) and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Ocarina', player) or (state.can_reach('South Dark World', 'Region', player) and state.has_Mirror(player))) and basic_routes(state))
    elif bombshop_entrance.name == 'Dark World Potion Shop':
        # 1. walk down by lifting rock: needs gloves and pearl`
        # 2. walk down by hammering peg: needs hammer and pearl
        # 3. mirror and basic routes
        # -> (P and (H or Gloves)) or (M and BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has_Pearl(player) and (state.has('Hammer', player) or state.can_lift_rocks(player))) or (state.has_Mirror(player) and basic_routes(state)))
    elif bombshop_entrance.name == 'Kings Grave':
        # same as the Normal_LW_entrances case except that the pre-existing mirror is only possible if you have mitts
        # (because otherwise mirror was used to reach the grave, so would cancel a pre-existing mirror spot)
        # to account for insanity, must consider a way to escape without a cave for basic_routes
        # -> (M and Mitts) or ((Mitts or Flute or (M and P and West Dark World access)) and BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.can_lift_heavy_rocks(player) and state.has_Mirror(player)) or ((state.can_lift_heavy_rocks(player) or state.has('Ocarina', player) or (state.can_reach('West Dark World', 'Region', player) and state.has_Pearl(player) and state.has_Mirror(player))) and basic_routes(state)))
    elif bombshop_entrance.name == 'Waterfall of Wishing':
        # same as the Normal_LW_entrances case except in insanity it's possible you could be here without Flippers which
        # means you need an escape route of either Flippers or Flute
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Flippers', player) or state.has('Ocarina', player)) and (basic_routes(state) or state.has_Mirror(player)))

def set_inverted_big_bomb_rules(world, player):
    bombshop_entrance = world.get_region('Inverted Big Bomb Shop', player).entrances[0]
    Normal_LW_entrances = ['Blinds Hideout',
                           'Bonk Fairy (Light)',
                           'Lake Hylia Fairy',
                           'Light Hype Fairy',
                           'Desert Fairy',
                           'Chicken House',
                           'Aginahs Cave',
                           'Sahasrahlas Hut',
                           'Cave Shop (Lake Hylia)',
                           'Blacksmiths Hut',
                           'Sick Kids House',
                           'Lost Woods Gamble',
                           'Fortune Teller (Light)',
                           'Snitch Lady (East)',
                           'Snitch Lady (West)',
                           'Tavern (Front)',
                           'Kakariko Shop',
                           'Mini Moldorm Cave',
                           'Long Fairy Cave',
                           'Good Bee Cave',
                           '20 Rupee Cave',
                           '50 Rupee Cave',
                           'Ice Rod Cave',
                           'Bonk Rock Cave',
                           'Library',
                           'Potion Shop',
                           'Dam',
                           'Lumberjack House',
                           'Lake Hylia Fortune Teller',
                           'Eastern Palace',
                           'Kakariko Gamble Game',
                           'Kakariko Well Cave',
                           'Bat Cave Cave',
                           'Elder House (East)',
                           'Elder House (West)',
                           'North Fairy Cave',
                           'Lost Woods Hideout Stump',
                           'Lumberjack Tree Cave',
                           'Two Brothers House (East)',
                           'Sanctuary',
                           'Hyrule Castle Entrance (South)',
                           'Hyrule Castle Secret Entrance Stairs',
                           'Hyrule Castle Entrance (West)',
                           'Hyrule Castle Entrance (East)',
                           'Inverted Ganons Tower',
                           'Cave 45',
                           'Checkerboard Cave']
    LW_DM_entrances = ['Old Man Cave (East)',
                       'Old Man House (Bottom)',
                       'Old Man House (Top)',
                       'Death Mountain Return Cave (East)',
                       'Spectacle Rock Cave Peak',
                       'Spectacle Rock Cave',
                       'Spectacle Rock Cave (Bottom)',
                       'Tower of Hera',
                       'Death Mountain Return Cave (West)',
                       'Paradox Cave (Top)',
                       'Fairy Ascension Cave (Top)',
                       'Spiral Cave',
                       'Paradox Cave (Bottom)',
                       'Paradox Cave (Middle)',
                       'Hookshot Fairy',
                       'Spiral Cave (Bottom)',
                       'Mimic Cave',
                       'Fairy Ascension Cave (Bottom)',
                       'Desert Palace Entrance (West)',
                       'Desert Palace Entrance (North)',
                       'Desert Palace Entrance (South)']
    Northern_DW_entrances = ['Brewery',
                             'C-Shaped House',
                             'Chest Game',
                             'Dark World Hammer Peg Cave',
                             'Red Shield Shop',
                             'Dark Sanctuary Hint',
                             'Fortune Teller (Dark)',
                             'Dark World Shop',
                             'Dark World Lumberjack Shop',
                             'Thieves Town',
                             'Skull Woods First Section Door',
                             'Skull Woods Second Section Door (East)']
    Southern_DW_entrances = ['Hype Cave',
                             'Bonk Fairy (Dark)',
                             'Archery Game',
                             'Inverted Big Bomb Shop',
                             'Dark Lake Hylia Shop',
                             'Swamp Palace']
    Isolated_DW_entrances = ['Spike Cave',
                             'Cave Shop (Dark Death Mountain)',
                             'Dark Death Mountain Fairy',
                             'Skull Woods Second Section Door (West)',
                             'Skull Woods Final Section',
                             'Turtle Rock',
                             'Dark Death Mountain Ledge (West)',
                             'Dark Death Mountain Ledge (East)',
                             'Bumper Cave (Top)',
                             'Superbunny Cave (Top)',
                             'Superbunny Cave (Bottom)',
                             'Hookshot Cave',
                             'Turtle Rock Isolated Ledge Entrance',
                             'Hookshot Cave Back Entrance',
                             'Inverted Agahnims Tower',
                             'Dark Lake Hylia Ledge Fairy',
                             'Dark Lake Hylia Ledge Spike Cave',
                             'Dark Lake Hylia Ledge Hint',
                             'Mire Shed',
                             'Dark Desert Hint',
                             'Dark Desert Fairy',
                             'Misery Mire']
    LW_bush_entrances = ['Bush Covered House',
                         'Light World Bomb Hut',
                         'Graveyard Cave']
    
    set_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.can_reach('East Dark World', 'Region', player) and state.can_reach('Inverted Big Bomb Shop', 'Region', player) and state.has('Crystal 5', player) and state.has('Crystal 6', player))

    #crossing peg bridge starting from the southern dark world
    def cross_peg_bridge(state):
        return state.has('Hammer', player)

    # Key for below abbreviations:
    # P = pearl
    # A = Aga1
    # H = hammer
    # M = Mirror
    # G = Glove
    if bombshop_entrance.name in Normal_LW_entrances:
        # Just walk to the castle and mirror.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has_Mirror(player))
    elif bombshop_entrance.name in LW_DM_entrances:
        # For these entrances, you cannot walk to the castle/pyramid and thus must use Mirror and then Flute.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.can_flute(player) and state.has_Mirror(player))
    elif bombshop_entrance.name in Northern_DW_entrances:
        # You can just fly with the Flute, you can take a long walk with Mitts and Hammer,
        # or you can leave a Mirror portal nearby and then walk to the castle to Mirror again.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.can_flute or (state.can_lift_heavy_rocks(player) and cross_peg_bridge(state)) or (state.has_Mirror(player) and state.can_reach('Light World', 'Region', player)))
    elif bombshop_entrance.name in Southern_DW_entrances:
        # This is the same as north DW without the Mitts rock present.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: cross_peg_bridge(state) or state.can_flute(player) or (state.has_Mirror(player) and state.can_reach('Light World', 'Region', player)))
    elif bombshop_entrance.name in Isolated_DW_entrances:
        # There's just no way to escape these places with the bomb and no Flute.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.can_flute(player))
    elif bombshop_entrance.name in LW_bush_entrances:
        # These entrances are behind bushes in LW so you need either Pearl or the tools to solve NDW bomb shop locations.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has_Mirror(player) and (state.can_flute(player) or state.has_Pearl(player) or (state.can_lift_heavy_rocks(player) and cross_peg_bridge(state))))
    elif bombshop_entrance.name == 'Bumper Cave (Bottom)':
        # This is mostly the same as NDW but the Mirror path requires being able to lift a rock.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.can_flute or (state.can_lift_heavy_rocks(player) and cross_peg_bridge(state)) or (state.has_Mirror(player) and state.can_lift_rocks(player) and state.can_reach('Light World', 'Region', player)))
    elif bombshop_entrance.name == 'Old Man Cave (West)':
        # The three paths back are Mirror and DW walk, Mirror and Flute, or LW walk and then Mirror.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has_Mirror(player) and ((state.can_lift_heavy_rocks(player) and cross_peg_bridge(state)) or (state.can_lift_rocks(player) and state.has_Pearl(player)) or state.can_flute(player)))
    elif bombshop_entrance.name == 'Dark World Potion Shop':
        # You either need to Flute to 5 or cross the rock/hammer choice pass to the south.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.can_flute(player) or state.has('Hammer', player) or state.can_lift_rocks(player))
    elif bombshop_entrance.name == 'Kings Grave':
        # Either lift the rock and walk to the castle to Mirror or Mirror immediately and Flute.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.can_flute(player) or state.can_lift_heavy_rocks(player)) and state.has_Mirror(player))
    elif bombshop_entrance.name == 'Two Brothers House (West)':
        # First you must Mirror. Then you can either Flute, cross the peg bridge, or use the Agah 1 portal to Mirror again.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.can_flute(player) or cross_peg_bridge(state) or state.has('Beat Agahnim 1', player)) and state.has_Mirror(player))
    elif bombshop_entrance.name == 'Waterfall of Wishing':
        # You absolutely must be able to swim to return it from here.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Flippers', player) and state.has_Pearl(player) and state.has_Mirror(player))
    elif bombshop_entrance.name == 'Ice Palace':
        # You can swim to the dock or use the Flute to get off the island.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Flippers', player) or state.can_flute(player))
    elif bombshop_entrance.name == 'Capacity Upgrade':
        # You must Mirror but then can use either Ice Palace return path.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Flippers', player) or state.can_flute(player)) and state.has_Mirror(player))


def set_bunny_rules(world, player):

    # regions for the exits of multi-entrace caves/drops that bunny cannot pass
    # Note spiral cave may be technically passible, but it would be too absurd to require since OHKO mode is a thing.
    bunny_impassable_caves = ['Bumper Cave', 'Two Brothers House', 'Hookshot Cave', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)', 'Turtle Rock (Entrance)', 'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Skull Woods Second Section (Drop)',
                              'Turtle Rock (Eye Bridge)', 'Sewers', 'Pyramid', 'Spiral Cave (Top)', 'Desert Palace Main (Inner)', 'Fairy Ascension Cave (Drop)']

    bunny_accessible_locations = ['Link\'s Uncle', 'Sahasrahla', 'Sick Kid', 'Lost Woods Hideout', 'Lumberjack Tree', 'Checkerboard Cave', 'Potion Shop', 'Spectacle Rock Cave', 'Pyramid', 'Hype Cave - Generous Guy', 'Peg Cave', 'Bumper Cave Ledge', 'Dark Blacksmith Ruins']


    def path_to_access_rule(path, entrance):
        return lambda state: state.can_reach(entrance) and all(rule(state) for rule in path)

    def options_to_access_rule(options):
        return lambda state: any(rule(state) for rule in options)

    def get_rule_to_add(region):
        if not region.is_light_world:
            return lambda state: state.has_Pearl(player)
        # in this case we are mixed region.
        # we collect possible options.

        # The base option is having the moon pearl
        possible_options = [lambda state: state.has_Pearl(player)]

        # We will search entrances recursively until we find
        # one that leads to an exclusively light world region
        # for each such entrance a new option is added that consist of:
        #    a) being able to reach it, and
        #    b) being able to access all entrances from there to `region`
        seen = set([region])
        queue = collections.deque([(region, [])])
        while queue:
            (current, path) = queue.popleft()
            for entrance in current.entrances:
                new_region = entrance.parent_region
                if new_region in seen:
                    continue
                new_path = path + [entrance.access_rule]
                seen.add(new_region)
                if not new_region.is_light_world:
                    continue # we don't care about pure dark world entrances
                if new_region.is_dark_world:
                    queue.append((new_region, new_path))
                else:
                    # we have reached pure light world, so we have a new possible option
                    possible_options.append(path_to_access_rule(new_path, entrance))
        return options_to_access_rule(possible_options)

    # Add requirements for bunny-impassible caves if they occur in the dark world
    for region in [world.get_region(name, player) for name in bunny_impassable_caves]:

        if not region.is_dark_world:
            continue
        rule = get_rule_to_add(region)
        for exit in region.exits:
            add_rule(exit, rule)

    paradox_shop = world.get_region('Light World Death Mountain Shop', player)
    if paradox_shop.is_dark_world:
        add_rule(paradox_shop.entrances[0], get_rule_to_add(paradox_shop))

    # Add requirements for all locations that are actually in the dark world, except those available to the bunny
    for location in world.get_locations():
        if location.player == player and location.parent_region.is_dark_world:

            if location.name in bunny_accessible_locations:
                continue

            add_rule(location, get_rule_to_add(location.parent_region))

def set_inverted_bunny_rules(world, player):

    # regions for the exits of multi-entrace caves/drops that bunny cannot pass
    # Note spiral cave may be technically passible, but it would be too absurd to require since OHKO mode is a thing.
    bunny_impassable_caves = ['Bumper Cave', 'Two Brothers House', 'Hookshot Cave', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)', 'Turtle Rock (Entrance)', 'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Skull Woods Second Section (Drop)',
                              'Turtle Rock (Eye Bridge)', 'Sewers', 'Pyramid', 'Spiral Cave (Top)', 'Desert Palace Main (Inner)', 'Fairy Ascension Cave (Drop)', 'The Sky']

    bunny_accessible_locations = ['Link\'s Uncle', 'Sahasrahla', 'Sick Kid', 'Lost Woods Hideout', 'Lumberjack Tree', 'Checkerboard Cave', 'Potion Shop', 'Spectacle Rock Cave', 'Pyramid', 'Hype Cave - Generous Guy', 'Peg Cave', 'Bumper Cave Ledge', 'Dark Blacksmith Ruins', 'Bombos Tablet', 'Ether Tablet', 'Purple Chest']


    def path_to_access_rule(path, entrance):
        return lambda state: state.can_reach(entrance) and all(rule(state) for rule in path)

    def options_to_access_rule(options):
        return lambda state: any(rule(state) for rule in options)

    def get_rule_to_add(region):
        if not region.is_dark_world:
            return lambda state: state.has_Pearl(player)
        # in this case we are mixed region.
        # we collect possible options.

        # The base option is having the moon pearl
        possible_options = [lambda state: state.has_Pearl(player)]

        # We will search entrances recursively until we find
        # one that leads to an exclusively dark world region
        # for each such entrance a new option is added that consist of:
        #    a) being able to reach it, and
        #    b) being able to access all entrances from there to `region`
        seen = set([region])
        queue = collections.deque([(region, [])])
        while queue:
            (current, path) = queue.popleft()
            for entrance in current.entrances:
                new_region = entrance.parent_region
                if new_region in seen:
                    continue
                new_path = path + [entrance.access_rule]
                seen.add(new_region)
                if not new_region.is_dark_world:
                    continue # we don't care about pure light world entrances
                if new_region.is_light_world:
                    queue.append((new_region, new_path))
                else:
                    # we have reached pure dark world, so we have a new possible option
                    possible_options.append(path_to_access_rule(new_path, entrance))
        return options_to_access_rule(possible_options)

    # Add requirements for bunny-impassible caves if they occur in the light world
    for region in [world.get_region(name, player) for name in bunny_impassable_caves]:

        if not region.is_light_world:
            continue
        rule = get_rule_to_add(region)
        for exit in region.exits:
            add_rule(exit, rule)

    paradox_shop = world.get_region('Light World Death Mountain Shop', player)
    if paradox_shop.is_light_world:
        add_rule(paradox_shop.entrances[0], get_rule_to_add(paradox_shop))

    # Add requirements for all locations that are actually in the light world, except those available to the bunny
    for location in world.get_locations():
        if location.player == player and location.parent_region.is_light_world:

            if location.name in bunny_accessible_locations:
                continue

            add_rule(location, get_rule_to_add(location.parent_region))


