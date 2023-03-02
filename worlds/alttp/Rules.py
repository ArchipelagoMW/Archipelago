import collections
import logging
from typing import Iterator, Set

from worlds.alttp import OverworldGlitchRules
from BaseClasses import MultiWorld, Entrance
from worlds.alttp.Items import ItemFactory, progression_items, item_name_groups, item_table
from worlds.alttp.OverworldGlitchRules import overworld_glitches_rules, no_logic_rules
from worlds.alttp.Regions import location_table
from worlds.alttp.UnderworldGlitchRules import underworld_glitches_rules
from worlds.alttp.Bosses import GanonDefeatRule
from worlds.generic.Rules import set_rule, add_rule, forbid_item, add_item_rule, item_in_locations, \
    item_name
from worlds.alttp.Options import smallkey_shuffle
from worlds.alttp.Regions import LTTPRegionType


def set_rules(world):
    player = world.player
    world = world.multiworld
    if world.logic[player] == 'nologic':
        if player == next(player_id for player_id in world.get_game_players("A Link to the Past")
                          if world.logic[player_id] == 'nologic'):  # only warn one time
            logging.info(
                'WARNING! Seeds generated under this logic often require major glitches and may be impossible!')

        if world.players == 1:
            world.get_region('Menu', player).can_reach_private = lambda state: True
            no_logic_rules(world, player)
            for exit in world.get_region('Menu', player).exits:
                exit.hide_path = True
            return
        else:
            # Set access rules according to max glitches for multiworld progression.
            # Set accessibility to none, and shuffle assuming the no logic players can always win
            world.accessibility[player] = world.accessibility[player].from_text("minimal")
            world.progression_balancing[player].value = 0

    else:
        world.completion_condition[player] = lambda state: state.has('Triforce', player)

    global_rules(world, player)
    dungeon_boss_rules(world, player)

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
        raise NotImplementedError(f'World state {world.mode[player]} is not implemented yet')

    if world.logic[player] == 'noglitches':
        no_glitches_rules(world, player)
    elif world.logic[player] == 'owglitches':
        # Initially setting no_glitches_rules to set the baseline rules for some
        # entrances. The overworld_glitches_rules set is primarily additive.
        no_glitches_rules(world, player)
        fake_flipper_rules(world, player)
        overworld_glitches_rules(world, player)
    elif world.logic[player] in ['hybridglitches', 'nologic']: 
        no_glitches_rules(world, player)
        fake_flipper_rules(world, player)
        overworld_glitches_rules(world, player)
        underworld_glitches_rules(world, player)
    elif world.logic[player] == 'minorglitches':
        no_glitches_rules(world, player)
        fake_flipper_rules(world, player)
    else:
        raise NotImplementedError(f'Not implemented yet: Logic - {world.logic[player]}')

    if world.goal[player] == 'bosses':
        # require all bosses to beat ganon
        add_rule(world.get_location('Ganon', player), lambda state: state.can_reach('Master Sword Pedestal', 'Location', player) and state.has('Beat Agahnim 1', player) and state.has('Beat Agahnim 2', player) and state.has_crystals(7, player))
    elif world.goal[player] == 'ganon':
        # require aga2 to beat ganon
        add_rule(world.get_location('Ganon', player), lambda state: state.has('Beat Agahnim 2', player))

    if world.mode[player] != 'inverted':
        set_big_bomb_rules(world, player)
        if world.logic[player] in {'owglitches', 'hybridglitches', 'nologic'} and world.shuffle[player] not in {'insanity', 'insanity_legacy', 'madness'}:
            path_to_courtyard = mirrorless_path_to_castle_courtyard(world, player)
            add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.multiworld.get_entrance('Dark Death Mountain Offset Mirror', player).can_reach(state) and all(rule(state) for rule in path_to_courtyard), 'or')
    else:
        set_inverted_big_bomb_rules(world, player)

    # if swamp and dam have not been moved we require mirror for swamp palace
    # however there is mirrorless swamp in hybrid MG, so we don't necessarily want this. HMG handles this requirement itself. 
    if not world.swamp_patch_required[player] and world.logic[player] not in ['hybridglitches', 'nologic']:
        add_rule(world.get_entrance('Swamp Palace Moat', player), lambda state: state.has('Magic Mirror', player))

    # GT Entrance may be required for Turtle Rock for OWG and < 7 required
    ganons_tower = world.get_entrance('Inverted Ganons Tower' if world.mode[player] == 'inverted' else 'Ganons Tower', player)
    if world.crystals_needed_for_gt[player] == 7 and not (world.logic[player] in ['owglitches', 'hybridglitches', 'nologic'] and world.mode[player] != 'inverted'):
        set_rule(ganons_tower, lambda state: False)

    set_trock_key_rules(world, player)

    set_rule(ganons_tower, lambda state: state.has_crystals(state.multiworld.crystals_needed_for_gt[player], player))
    if world.mode[player] != 'inverted' and world.logic[player] in ['owglitches', 'hybridglitches', 'nologic']:
        add_rule(world.get_entrance('Ganons Tower', player), lambda state: state.multiworld.get_entrance('Ganons Tower Ascent', player).can_reach(state), 'or')

    set_bunny_rules(world, player, world.mode[player] == 'inverted')


def mirrorless_path_to_castle_courtyard(world, player):
    # If Agahnim is defeated then the courtyard needs to be accessible without using the mirror for the mirror offset glitch.
    # Only considering the secret passage for now (in non-insanity shuffle).  Basically, if it's Ganon you need the master sword.
    start = world.get_entrance('Hyrule Castle Secret Entrance Drop', player)
    target = world.get_region('Hyrule Castle Courtyard', player)
    seen = {start.parent_region, start.connected_region}
    queue = collections.deque([(start.connected_region, [])])
    while queue:
        (current, path) = queue.popleft()
        for entrance in current.exits:
            if entrance.connected_region not in seen:
                new_path = path + [entrance.access_rule]
                if entrance.connected_region == target:
                    return new_path
                else:
                    queue.append((entrance.connected_region, new_path))

    raise Exception(f"Could not find mirrorless path to castle courtyard for Player {player} ({world.get_player_name(player)})")


def set_defeat_dungeon_boss_rule(location):
    # Lambda required to defer evaluation of dungeon.boss since it will change later if boss shuffle is used
    set_rule(location, lambda state: location.parent_region.dungeon.boss.can_defeat(state))

def set_always_allow(spot, rule):
    spot.always_allow = rule


def add_lamp_requirement(world: MultiWorld, spot, player: int, has_accessible_torch: bool = False):
    if world.dark_room_logic[player] == "lamp":
        add_rule(spot, lambda state: state.has('Lamp', player))
    elif world.dark_room_logic[player] == "torches":  # implicitly lamp as well
        if has_accessible_torch:
            add_rule(spot, lambda state: state.has('Lamp', player) or state.has('Fire Rod', player))
        else:
            add_rule(spot, lambda state: state.has('Lamp', player))
    elif world.dark_room_logic[player] == "none":
        pass
    else:
        raise ValueError(f"Unknown Dark Room Logic: {world.dark_room_logic[player]}")


non_crossover_items = (item_name_groups["Small Keys"] | item_name_groups["Big Keys"] | progression_items) - {
    "Small Key (Universal)"}


def dungeon_boss_rules(world, player):
    boss_locations = {
        'Agahnim 1',
        'Tower of Hera - Boss',
        'Tower of Hera - Prize',
        'Swamp Palace - Boss',
        'Swamp Palace - Prize',
        'Thieves\' Town - Boss',
        'Thieves\' Town - Prize',
        'Skull Woods - Boss',
        'Skull Woods - Prize',
        'Ice Palace - Boss',
        'Ice Palace - Prize',
        'Misery Mire - Boss',
        'Misery Mire - Prize',
        'Turtle Rock - Boss',
        'Turtle Rock - Prize',
        'Palace of Darkness - Boss',
        'Palace of Darkness - Prize',
    }
    for location in boss_locations:
        set_defeat_dungeon_boss_rule(world.get_location(location, player))

def global_rules(world, player):
    # ganon can only carry triforce
    add_item_rule(world.get_location('Ganon', player), lambda item: item.name == 'Triforce' and item.player == player)
    # dungeon prizes can only be crystals/pendants
    crystals_and_pendants: Set[str] = \
        {item for item, item_data in item_table.items() if item_data.type == "Crystal"}
    prize_locations: Iterator[str] = \
        (locations for locations, location_data in location_table.items() if location_data[2] == True)
    for prize_location in prize_locations:
        add_item_rule(world.get_location(prize_location, player),
                      lambda item: item.name in crystals_and_pendants and item.player == player)
    # determines which S&Q locations are available - hide from paths since it isn't an in-game location
    world.get_region('Menu', player).can_reach_private = lambda state: True
    for exit in world.get_region('Menu', player).exits:
        exit.hide_path = True

    set_rule(world.get_entrance('Old Man S&Q', player), lambda state: state.can_reach('Old Man', 'Location', player))

    set_rule(world.get_location('Sunken Treasure', player), lambda state: state.has('Open Floodgate', player))
    set_rule(world.get_location('Dark Blacksmith Ruins', player), lambda state: state.has('Return Smith', player))
    set_rule(world.get_location('Purple Chest', player),
             lambda state: state.has('Pick Up Purple Chest', player))  # Can S&Q with chest
    set_rule(world.get_location('Ether Tablet', player), lambda state: state.can_retrieve_tablet(player))
    set_rule(world.get_location('Master Sword Pedestal', player), lambda state: state.has('Red Pendant', player) and state.has('Blue Pendant', player) and state.has('Green Pendant', player))

    set_rule(world.get_location('Missing Smith', player), lambda state: state.has('Get Frog', player) and state.can_reach('Blacksmiths Hut', 'Region', player)) # Can't S&Q with smith
    set_rule(world.get_location('Blacksmith', player), lambda state: state.has('Return Smith', player))
    set_rule(world.get_location('Magic Bat', player), lambda state: state.has('Magic Powder', player))
    set_rule(world.get_location('Sick Kid', player), lambda state: state.has_group("Bottles", player))
    set_rule(world.get_location('Library', player), lambda state: state.has('Pegasus Boots', player))
    set_rule(world.get_location('Mimic Cave', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_location('Sahasrahla', player), lambda state: state.has('Green Pendant', player))


    set_rule(world.get_location('Spike Cave', player), lambda state:
             state.has('Hammer', player) and state.can_lift_rocks(player) and
             ((state.has('Cape', player) and state.can_extend_magic(player, 16, True)) or
              (state.has('Cane of Byrna', player) and
               (state.can_extend_magic(player, 12, True) or
                (state.multiworld.can_take_damage[player] and (state.has('Pegasus Boots', player) or state.has_hearts(player, 4))))))
             )

    set_rule(world.get_location('Hookshot Cave - Top Right', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_location('Hookshot Cave - Top Left', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_location('Hookshot Cave - Bottom Right', player),
             lambda state: state.has('Hookshot', player) or state.has('Pegasus Boots', player))
    set_rule(world.get_location('Hookshot Cave - Bottom Left', player), lambda state: state.has('Hookshot', player))

    set_rule(world.get_entrance('Sewers Door', player),
             lambda state: state._lttp_has_key('Small Key (Hyrule Castle)', player) or (
                         world.smallkey_shuffle[player] == smallkey_shuffle.option_universal and world.mode[
                     player] == 'standard'))  # standard universal small keys cannot access the shop
    set_rule(world.get_entrance('Sewers Back Door', player),
             lambda state: state._lttp_has_key('Small Key (Hyrule Castle)', player))
    set_rule(world.get_entrance('Agahnim 1', player),
             lambda state: state.has_sword(player) and state._lttp_has_key('Small Key (Agahnims Tower)', player, 2))

    set_rule(world.get_location('Castle Tower - Room 03', player), lambda state: state.can_kill_most_things(player, 8))
    set_rule(world.get_location('Castle Tower - Dark Maze', player),
             lambda state: state.can_kill_most_things(player, 8) and state._lttp_has_key('Small Key (Agahnims Tower)',
                                                                                   player))

    set_rule(world.get_location('Eastern Palace - Big Chest', player),
             lambda state: state.has('Big Key (Eastern Palace)', player))
    ep_boss = world.get_location('Eastern Palace - Boss', player)
    set_rule(ep_boss, lambda state: state.has('Big Key (Eastern Palace)', player) and
                                    ep_boss.parent_region.dungeon.boss.can_defeat(state))
    ep_prize = world.get_location('Eastern Palace - Prize', player)
    set_rule(ep_prize, lambda state: state.has('Big Key (Eastern Palace)', player) and
                                     ep_prize.parent_region.dungeon.boss.can_defeat(state))
    if not world.enemy_shuffle[player]:
        add_rule(ep_boss, lambda state: state.can_shoot_arrows(player))
        add_rule(ep_prize, lambda state: state.can_shoot_arrows(player))

    set_rule(world.get_location('Desert Palace - Big Chest', player), lambda state: state.has('Big Key (Desert Palace)', player))
    set_rule(world.get_location('Desert Palace - Torch', player), lambda state: state.has('Pegasus Boots', player))
    set_rule(world.get_entrance('Desert Palace East Wing', player), lambda state: state._lttp_has_key('Small Key (Desert Palace)', player))
    set_rule(world.get_location('Desert Palace - Prize', player), lambda state: state._lttp_has_key('Small Key (Desert Palace)', player) and state.has('Big Key (Desert Palace)', player) and state.has_fire_source(player) and state.multiworld.get_location('Desert Palace - Prize', player).parent_region.dungeon.boss.can_defeat(state))
    set_rule(world.get_location('Desert Palace - Boss', player), lambda state: state._lttp_has_key('Small Key (Desert Palace)', player) and state.has('Big Key (Desert Palace)', player) and state.has_fire_source(player) and state.multiworld.get_location('Desert Palace - Boss', player).parent_region.dungeon.boss.can_defeat(state))

    # logic patch to prevent placing a crystal in Desert that's required to reach the required keys
    if not (world.smallkey_shuffle[player] and world.bigkey_shuffle[player]):
        add_rule(world.get_location('Desert Palace - Prize', player), lambda state: state.multiworld.get_region('Desert Palace Main (Outer)', player).can_reach(state))

    set_rule(world.get_entrance('Tower of Hera Small Key Door', player), lambda state: state._lttp_has_key('Small Key (Tower of Hera)', player) or item_name(state, 'Tower of Hera - Big Key Chest', player) == ('Small Key (Tower of Hera)', player))
    set_rule(world.get_entrance('Tower of Hera Big Key Door', player), lambda state: state.has('Big Key (Tower of Hera)', player))
    set_rule(world.get_location('Tower of Hera - Big Chest', player), lambda state: state.has('Big Key (Tower of Hera)', player))
    set_rule(world.get_location('Tower of Hera - Big Key Chest', player), lambda state: state.has_fire_source(player))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Tower of Hera - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Tower of Hera)' and item.player == player)

    set_rule(world.get_entrance('Swamp Palace Moat', player), lambda state: state.has('Flippers', player) and state.has('Open Floodgate', player))
    set_rule(world.get_entrance('Swamp Palace Small Key Door', player), lambda state: state._lttp_has_key('Small Key (Swamp Palace)', player))
    set_rule(world.get_entrance('Swamp Palace (Center)', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_location('Swamp Palace - Big Chest', player), lambda state: state.has('Big Key (Swamp Palace)', player) or item_name(state, 'Swamp Palace - Big Chest', player) == ('Big Key (Swamp Palace)', player))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Swamp Palace - Big Chest', player), lambda state, item: item.name == 'Big Key (Swamp Palace)' and item.player == player)
    set_rule(world.get_entrance('Swamp Palace (North)', player), lambda state: state.has('Hookshot', player))
    if not world.smallkey_shuffle[player] and world.logic[player] not in ['hybridglitches', 'nologic']:
        forbid_item(world.get_location('Swamp Palace - Entrance', player), 'Big Key (Swamp Palace)', player)

    set_rule(world.get_entrance('Thieves Town Big Key Door', player), lambda state: state.has('Big Key (Thieves Town)', player))
    set_rule(world.get_entrance('Blind Fight', player), lambda state: state._lttp_has_key('Small Key (Thieves Town)', player))
    set_rule(world.get_location('Thieves\' Town - Big Chest', player), lambda state: (state._lttp_has_key('Small Key (Thieves Town)', player) or item_name(state, 'Thieves\' Town - Big Chest', player) == ('Small Key (Thieves Town)', player)) and state.has('Hammer', player))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Thieves\' Town - Big Chest', player), lambda state, item: item.name == 'Small Key (Thieves Town)' and item.player == player and state.has('Hammer', player))
    set_rule(world.get_location('Thieves\' Town - Attic', player), lambda state: state._lttp_has_key('Small Key (Thieves Town)', player))

    set_rule(world.get_entrance('Skull Woods First Section South Door', player), lambda state: state._lttp_has_key('Small Key (Skull Woods)', player))
    set_rule(world.get_entrance('Skull Woods First Section (Right) North Door', player), lambda state: state._lttp_has_key('Small Key (Skull Woods)', player))
    set_rule(world.get_entrance('Skull Woods First Section West Door', player), lambda state: state._lttp_has_key('Small Key (Skull Woods)', player, 2))  # ideally would only be one key, but we may have spent thst key already on escaping the right section
    set_rule(world.get_entrance('Skull Woods First Section (Left) Door to Exit', player), lambda state: state._lttp_has_key('Small Key (Skull Woods)', player, 2))
    set_rule(world.get_location('Skull Woods - Big Chest', player), lambda state: state.has('Big Key (Skull Woods)', player) or item_name(state, 'Skull Woods - Big Chest', player) == ('Big Key (Skull Woods)', player))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Skull Woods - Big Chest', player), lambda state, item: item.name == 'Big Key (Skull Woods)' and item.player == player)
    set_rule(world.get_entrance('Skull Woods Torch Room', player), lambda state: state._lttp_has_key('Small Key (Skull Woods)', player, 3) and state.has('Fire Rod', player) and state.has_sword(player))  # sword required for curtain

    set_rule(world.get_entrance('Ice Palace Entrance Room', player), lambda state: state.can_melt_things(player))
    set_rule(world.get_location('Ice Palace - Big Chest', player), lambda state: state.has('Big Key (Ice Palace)', player))
    set_rule(world.get_entrance('Ice Palace (Kholdstare)', player), lambda state: state.can_lift_rocks(player) and state.has('Hammer', player) and state.has('Big Key (Ice Palace)', player) and (state._lttp_has_key('Small Key (Ice Palace)', player, 2) or (state.has('Cane of Somaria', player) and state._lttp_has_key('Small Key (Ice Palace)', player, 1))))
    set_rule(world.get_entrance('Ice Palace (East)', player), lambda state: (state.has('Hookshot', player) or (
                item_in_locations(state, 'Big Key (Ice Palace)', player, [('Ice Palace - Spike Room', player), ('Ice Palace - Big Key Chest', player), ('Ice Palace - Map Chest', player)]) and state._lttp_has_key('Small Key (Ice Palace)', player))) and (state.multiworld.can_take_damage[player] or state.has('Hookshot', player) or state.has('Cape', player) or state.has('Cane of Byrna', player)))
    set_rule(world.get_entrance('Ice Palace (East Top)', player), lambda state: state.can_lift_rocks(player) and state.has('Hammer', player))

    set_rule(world.get_entrance('Misery Mire Entrance Gap', player), lambda state: (state.has('Pegasus Boots', player) or state.has('Hookshot', player)) and (state.has_sword(player) or state.has('Fire Rod', player) or state.has('Ice Rod', player) or state.has('Hammer', player) or state.has('Cane of Somaria', player) or state.can_shoot_arrows(player)))  # need to defeat wizzrobes, bombs don't work ...
    set_rule(world.get_location('Misery Mire - Big Chest', player), lambda state: state.has('Big Key (Misery Mire)', player))
    set_rule(world.get_location('Misery Mire - Spike Chest', player), lambda state: (state.multiworld.can_take_damage[player] and state.has_hearts(player, 4)) or state.has('Cane of Byrna', player) or state.has('Cape', player))
    set_rule(world.get_entrance('Misery Mire Big Key Door', player), lambda state: state.has('Big Key (Misery Mire)', player))
    # you can squander the free small key from the pot by opening the south door to the north west switch room, locking you out of accessing a color switch ...
    # big key gives backdoor access to that from the teleporter in the north west
    set_rule(world.get_location('Misery Mire - Map Chest', player), lambda state: state._lttp_has_key('Small Key (Misery Mire)', player, 1) or state.has('Big Key (Misery Mire)', player))
    set_rule(world.get_location('Misery Mire - Main Lobby', player), lambda state: state._lttp_has_key('Small Key (Misery Mire)', player, 1) or state._lttp_has_key('Big Key (Misery Mire)', player))
    # we can place a small key in the West wing iff it also contains/blocks the Big Key, as we cannot reach and softlock with the basement key door yet
    set_rule(world.get_entrance('Misery Mire (West)', player), lambda state: state._lttp_has_key('Small Key (Misery Mire)', player, 2) if ((
                                                                                                                                                 item_name(state, 'Misery Mire - Compass Chest', player) in [('Big Key (Misery Mire)', player)]) or
                                                                                                                                     (
                                                                                                                                                 item_name(state, 'Misery Mire - Big Key Chest', player) in [('Big Key (Misery Mire)', player)])) else state._lttp_has_key('Small Key (Misery Mire)', player, 3))
    set_rule(world.get_location('Misery Mire - Compass Chest', player), lambda state: state.has_fire_source(player))
    set_rule(world.get_location('Misery Mire - Big Key Chest', player), lambda state: state.has_fire_source(player))
    set_rule(world.get_entrance('Misery Mire (Vitreous)', player), lambda state: state.has('Cane of Somaria', player))

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
    set_rule(world.get_entrance('Turtle Rock (Trinexx)', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, 4) and state.has('Big Key (Turtle Rock)', player) and state.has('Cane of Somaria', player))

    if not world.enemy_shuffle[player]:
        set_rule(world.get_entrance('Palace of Darkness Bonk Wall', player), lambda state: state.can_shoot_arrows(player))
    set_rule(world.get_entrance('Palace of Darkness Hammer Peg Drop', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Palace of Darkness Bridge Room', player), lambda state: state._lttp_has_key('Small Key (Palace of Darkness)', player, 1))  # If we can reach any other small key door, we already have back door access to this area
    set_rule(world.get_entrance('Palace of Darkness Big Key Door', player), lambda state: state._lttp_has_key('Small Key (Palace of Darkness)', player, 6) and state.has('Big Key (Palace of Darkness)', player) and state.can_shoot_arrows(player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Palace of Darkness (North)', player), lambda state: state._lttp_has_key('Small Key (Palace of Darkness)', player, 4))
    set_rule(world.get_location('Palace of Darkness - Big Chest', player), lambda state: state.has('Big Key (Palace of Darkness)', player))

    set_rule(world.get_entrance('Palace of Darkness Big Key Chest Staircase', player), lambda state: state._lttp_has_key('Small Key (Palace of Darkness)', player, 6) or (
                item_name(state, 'Palace of Darkness - Big Key Chest', player) in [('Small Key (Palace of Darkness)', player)] and state._lttp_has_key('Small Key (Palace of Darkness)', player, 3)))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Palace of Darkness - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Palace of Darkness)' and item.player == player and state._lttp_has_key('Small Key (Palace of Darkness)', player, 5))

    set_rule(world.get_entrance('Palace of Darkness Spike Statue Room Door', player), lambda state: state._lttp_has_key('Small Key (Palace of Darkness)', player, 6) or (
                item_name(state, 'Palace of Darkness - Harmless Hellway', player) in [('Small Key (Palace of Darkness)', player)] and state._lttp_has_key('Small Key (Palace of Darkness)', player, 4)))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Palace of Darkness - Harmless Hellway', player), lambda state, item: item.name == 'Small Key (Palace of Darkness)' and item.player == player and state._lttp_has_key('Small Key (Palace of Darkness)', player, 5))

    set_rule(world.get_entrance('Palace of Darkness Maze Door', player), lambda state: state._lttp_has_key('Small Key (Palace of Darkness)', player, 6))

    # these key rules are conservative, you might be able to get away with more lenient rules
    randomizer_room_chests = ['Ganons Tower - Randomizer Room - Top Left', 'Ganons Tower - Randomizer Room - Top Right', 'Ganons Tower - Randomizer Room - Bottom Left', 'Ganons Tower - Randomizer Room - Bottom Right']
    compass_room_chests = ['Ganons Tower - Compass Room - Top Left', 'Ganons Tower - Compass Room - Top Right', 'Ganons Tower - Compass Room - Bottom Left', 'Ganons Tower - Compass Room - Bottom Right']

    set_rule(world.get_location('Ganons Tower - Bob\'s Torch', player), lambda state: state.has('Pegasus Boots', player))
    set_rule(world.get_entrance('Ganons Tower (Tile Room)', player), lambda state: state.has('Cane of Somaria', player))
    set_rule(world.get_entrance('Ganons Tower (Hookshot Room)', player), lambda state: state.has('Hammer', player) and (state.has('Hookshot', player) or state.has('Pegasus Boots', player)))
    set_rule(world.get_entrance('Ganons Tower (Map Room)', player), lambda state: state._lttp_has_key('Small Key (Ganons Tower)', player, 4) or (
                item_name(state, 'Ganons Tower - Map Chest', player) in [('Big Key (Ganons Tower)', player), ('Small Key (Ganons Tower)', player)] and state._lttp_has_key('Small Key (Ganons Tower)', player, 3)))
    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Ganons Tower - Map Chest', player), lambda state, item: item.name == 'Small Key (Ganons Tower)' and item.player == player and state._lttp_has_key('Small Key (Ganons Tower)', player, 3) and state.can_reach('Ganons Tower (Hookshot Room)', 'region', player))

    # It is possible to need more than 2 keys to get through this entrance if you spend keys elsewhere. We reflect this in the chest requirements.
    # However we need to leave these at the lower values to derive that with 3 keys it is always possible to reach Bob and Ice Armos.
    set_rule(world.get_entrance('Ganons Tower (Double Switch Room)', player), lambda state: state._lttp_has_key('Small Key (Ganons Tower)', player, 2))
    # It is possible to need more than 3 keys ....
    set_rule(world.get_entrance('Ganons Tower (Firesnake Room)', player), lambda state: state._lttp_has_key('Small Key (Ganons Tower)', player, 3))

    #The actual requirements for these rooms to avoid key-lock
    set_rule(world.get_location('Ganons Tower - Firesnake Room', player), lambda state: state._lttp_has_key('Small Key (Ganons Tower)', player, 3) or ((
                                                                                                                                                             item_in_locations(state, 'Big Key (Ganons Tower)', player, zip(randomizer_room_chests, [player] * len(randomizer_room_chests))) or item_in_locations(state, 'Small Key (Ganons Tower)', player, [('Ganons Tower - Firesnake Room', player)])) and state._lttp_has_key('Small Key (Ganons Tower)', player, 2)))
    for location in randomizer_room_chests:
        set_rule(world.get_location(location, player), lambda state: state._lttp_has_key('Small Key (Ganons Tower)', player, 4) or (
                    item_in_locations(state, 'Big Key (Ganons Tower)', player, zip(randomizer_room_chests, [player] * len(randomizer_room_chests))) and state._lttp_has_key('Small Key (Ganons Tower)', player, 3)))

    # Once again it is possible to need more than 3 keys...
    set_rule(world.get_entrance('Ganons Tower (Tile Room) Key Door', player), lambda state: state._lttp_has_key('Small Key (Ganons Tower)', player, 3) and state.has('Fire Rod', player))
    # Actual requirements
    for location in compass_room_chests:
        set_rule(world.get_location(location, player), lambda state: state.has('Fire Rod', player) and (state._lttp_has_key('Small Key (Ganons Tower)', player, 4) or (
                    item_in_locations(state, 'Big Key (Ganons Tower)', player, zip(compass_room_chests, [player] * len(compass_room_chests))) and state._lttp_has_key('Small Key (Ganons Tower)', player, 3))))

    set_rule(world.get_location('Ganons Tower - Big Chest', player), lambda state: state.has('Big Key (Ganons Tower)', player))

    set_rule(world.get_location('Ganons Tower - Big Key Room - Left', player),
             lambda state: state.multiworld.get_location('Ganons Tower - Big Key Room - Left', player).parent_region.dungeon.bosses['bottom'].can_defeat(state))
    set_rule(world.get_location('Ganons Tower - Big Key Chest', player),
             lambda state: state.multiworld.get_location('Ganons Tower - Big Key Chest', player).parent_region.dungeon.bosses['bottom'].can_defeat(state))
    set_rule(world.get_location('Ganons Tower - Big Key Room - Right', player),
             lambda state: state.multiworld.get_location('Ganons Tower - Big Key Room - Right', player).parent_region.dungeon.bosses['bottom'].can_defeat(state))
    if world.enemy_shuffle[player]:
        set_rule(world.get_entrance('Ganons Tower Big Key Door', player),
                 lambda state: state.has('Big Key (Ganons Tower)', player))
    else:
        set_rule(world.get_entrance('Ganons Tower Big Key Door', player),
                 lambda state: state.has('Big Key (Ganons Tower)', player) and state.can_shoot_arrows(player))
    set_rule(world.get_entrance('Ganons Tower Torch Rooms', player),
             lambda state: state.has_fire_source(player) and state.multiworld.get_entrance('Ganons Tower Torch Rooms', player).parent_region.dungeon.bosses['middle'].can_defeat(state))
    set_rule(world.get_location('Ganons Tower - Pre-Moldorm Chest', player),
             lambda state: state._lttp_has_key('Small Key (Ganons Tower)', player, 3))
    set_rule(world.get_entrance('Ganons Tower Moldorm Door', player),
             lambda state: state._lttp_has_key('Small Key (Ganons Tower)', player, 4))
    set_rule(world.get_entrance('Ganons Tower Moldorm Gap', player),
             lambda state: state.has('Hookshot', player) and state.multiworld.get_entrance('Ganons Tower Moldorm Gap', player).parent_region.dungeon.bosses['top'].can_defeat(state))
    set_defeat_dungeon_boss_rule(world.get_location('Agahnim 2', player))
    ganon = world.get_location('Ganon', player)
    set_rule(ganon, lambda state: GanonDefeatRule(state, player))
    if world.goal[player] in ['ganontriforcehunt', 'localganontriforcehunt']:
        add_rule(ganon, lambda state: state.has_triforce_pieces(state.multiworld.treasure_hunt_count[player], player))
    elif world.goal[player] == 'ganonpedestal':
        add_rule(world.get_location('Ganon', player), lambda state: state.can_reach('Master Sword Pedestal', 'Location', player))
    else:
        add_rule(ganon, lambda state: state.has_crystals(state.multiworld.crystals_needed_for_ganon[player], player))
    set_rule(world.get_entrance('Ganon Drop', player), lambda state: state.has_beam_sword(player))  # need to damage ganon to get tiles to drop

    set_rule(world.get_location('Flute Activation Spot', player), lambda state: state.has('Flute', player))


def default_rules(world, player):
    """Default world rules when world state is not inverted."""
    # overworld requirements
    set_rule(world.get_entrance('Kings Grave', player), lambda state: state.has('Pegasus Boots', player))
    set_rule(world.get_entrance('Kings Grave Outer Rocks', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Kings Grave Inner Rocks', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Kings Grave Mirror Spot', player), lambda state: state.has('Moon Pearl', player) and state.has('Magic Mirror', player))
    # Caution: If king's grave is releaxed at all to account for reaching it via a two way cave's exit in insanity mode, then the bomb shop logic will need to be updated (that would involve create a small ledge-like Region for it)
    set_rule(world.get_entrance('Bonk Fairy (Light)', player), lambda state: state.has('Pegasus Boots', player))
    set_rule(world.get_entrance('Lumberjack Tree Tree', player), lambda state: state.has('Pegasus Boots', player) and state.has('Beat Agahnim 1', player))
    set_rule(world.get_entrance('Bonk Rock Cave', player), lambda state: state.has('Pegasus Boots', player))
    set_rule(world.get_entrance('Desert Palace Stairs', player), lambda state: state.has('Book of Mudora', player))
    set_rule(world.get_entrance('Sanctuary Grave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('20 Rupee Cave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('50 Rupee Cave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Death Mountain Entrance Rock', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Bumper Cave Entrance Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Flute Spot 1', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('Lake Hylia Central Island Teleporter', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Dark Desert Teleporter', player), lambda state: state.has('Activated Flute', player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('East Hyrule Teleporter', player), lambda state: state.has('Hammer', player) and state.can_lift_rocks(player) and state.has('Moon Pearl', player)) # bunny cannot use hammer
    set_rule(world.get_entrance('South Hyrule Teleporter', player), lambda state: state.has('Hammer', player) and state.can_lift_rocks(player) and state.has('Moon Pearl', player)) # bunny cannot use hammer
    set_rule(world.get_entrance('Kakariko Teleporter', player), lambda state: ((state.has('Hammer', player) and state.can_lift_rocks(player)) or state.can_lift_heavy_rocks(player)) and state.has('Moon Pearl', player)) # bunny cannot lift bushes
    set_rule(world.get_location('Flute Spot', player), lambda state: state.has('Shovel', player))
    set_rule(world.get_entrance('Bat Cave Drop Ledge', player), lambda state: state.has('Hammer', player))

    set_rule(world.get_location('Zora\'s Ledge', player), lambda state: state.has('Flippers', player))
    set_rule(world.get_entrance('Waterfall of Wishing', player), lambda state: state.has('Flippers', player))
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

    set_rule(world.get_entrance('Catfish Exit Rock', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Catfish Entrance Rock', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Northeast Dark World Broken Bridge Pass', player), lambda state: state.has('Moon Pearl', player) and (state.can_lift_rocks(player) or state.has('Hammer', player) or state.has('Flippers', player)))
    set_rule(world.get_entrance('East Dark World Broken Bridge Pass', player), lambda state: state.has('Moon Pearl', player) and (state.can_lift_rocks(player) or state.has('Hammer', player)))
    set_rule(world.get_entrance('South Dark World Bridge', player), lambda state: state.has('Hammer', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Bonk Fairy (Dark)', player), lambda state: state.has('Moon Pearl', player) and state.has('Pegasus Boots', player))
    set_rule(world.get_entrance('West Dark World Gap', player), lambda state: state.has('Moon Pearl', player) and state.has('Hookshot', player))
    set_rule(world.get_entrance('Palace of Darkness', player), lambda state: state.has('Moon Pearl', player)) # kiki needs pearl
    set_rule(world.get_entrance('Hyrule Castle Ledge Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Hyrule Castle Main Gate', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: (state.has('Moon Pearl', player) and state.has('Flippers', player) or state.has('Magic Mirror', player)))  # Overworld Bunny Revival
    set_rule(world.get_location('Bombos Tablet', player), lambda state: state.can_retrieve_tablet(player))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (South)', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Fairy', player), lambda state: state.has('Moon Pearl', player)) # bomb required
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Spike Cave', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Village of Outcasts Heavy Rock', player), lambda state: state.has('Moon Pearl', player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Hype Cave', player), lambda state: state.has('Moon Pearl', player)) # bomb required
    set_rule(world.get_entrance('Brewery', player), lambda state: state.has('Moon Pearl', player)) # bomb required
    set_rule(world.get_entrance('Thieves Town', player), lambda state: state.has('Moon Pearl', player)) # bunny cannot pull
    set_rule(world.get_entrance('Skull Woods First Section Hole (North)', player), lambda state: state.has('Moon Pearl', player)) # bunny cannot lift bush
    set_rule(world.get_entrance('Skull Woods Second Section Hole', player), lambda state: state.has('Moon Pearl', player)) # bunny cannot lift bush
    set_rule(world.get_entrance('Maze Race Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Cave 45 Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Bombos Tablet Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('East Dark World Bridge', player), lambda state: state.has('Moon Pearl', player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Lake Hylia Island Mirror Spot', player), lambda state: state.has('Moon Pearl', player) and state.has('Magic Mirror', player) and state.has('Flippers', player))
    set_rule(world.get_entrance('Lake Hylia Central Island Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('East Dark World River Pier', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))
    set_rule(world.get_entrance('Graveyard Ledge Mirror Spot', player), lambda state: state.has('Moon Pearl', player) and state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Bumper Cave Entrance Rock', player), lambda state: state.has('Moon Pearl', player) and state.can_lift_rocks(player))
    set_rule(world.get_entrance('Bumper Cave Ledge Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Bat Cave Drop Ledge Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Dark World Hammer Peg Cave', player), lambda state: state.has('Moon Pearl', player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Village of Outcasts Eastern Rocks', player), lambda state: state.has('Moon Pearl', player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Peg Area Rocks', player), lambda state: state.has('Moon Pearl', player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Village of Outcasts Pegs', player), lambda state: state.has('Moon Pearl', player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Grassy Lawn Pegs', player), lambda state: state.has('Moon Pearl', player) and state.has('Hammer', player))
    set_rule(world.get_entrance('Bumper Cave Exit (Top)', player), lambda state: state.has('Cape', player))
    set_rule(world.get_entrance('Bumper Cave Exit (Bottom)', player), lambda state: state.has('Cape', player) or state.has('Hookshot', player))

    set_rule(world.get_entrance('Skull Woods Final Section', player), lambda state: state.has('Fire Rod', player) and state.has('Moon Pearl', player)) # bunny cannot use fire rod
    set_rule(world.get_entrance('Misery Mire', player), lambda state: state.has('Moon Pearl', player) and state.has_sword(player) and state.has_misery_mire_medallion(player))  # sword required to cast magic (!)
    set_rule(world.get_entrance('Desert Ledge (Northeast) Mirror Spot', player), lambda state: state.has('Magic Mirror', player))

    set_rule(world.get_entrance('Desert Ledge Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Desert Palace Stairs Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Desert Palace Entrance (North) Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Spectacle Rock Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Hookshot Cave', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))

    set_rule(world.get_entrance('East Death Mountain (Top) Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Mimic Cave Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Spiral Cave Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Fairy Ascension Mirror Spot', player), lambda state: state.has('Magic Mirror', player) and state.has('Moon Pearl', player))  # need to lift flowers
    set_rule(world.get_entrance('Isolated Ledge Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Superbunny Cave Exit (Bottom)', player), lambda state: False)  # Cannot get to bottom exit from top. Just exists for shuffling
    set_rule(world.get_entrance('Floating Island Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Turtle Rock', player), lambda state: state.has('Moon Pearl', player) and state.has_sword(player) and state.has_turtle_rock_medallion(player) and state.can_reach('Turtle Rock (Top)', 'Region', player))  # sword required to cast magic (!)

    set_rule(world.get_entrance('Pyramid Hole', player), lambda state: state.has('Beat Agahnim 2', player) or world.open_pyramid[player].to_bool(world, player))

    if world.swordless[player]:
        swordless_rules(world, player)


def inverted_rules(world, player):
    # s&q regions.
    set_rule(world.get_entrance('Castle Ledge S&Q', player), lambda state: state.has('Magic Mirror', player) and state.has('Beat Agahnim 1', player))

    # overworld requirements 
    set_rule(world.get_location('Maze Race', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Mini Moldorm Cave', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Ice Rod Cave', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Light Hype Fairy', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Potion Shop Pier', player), lambda state: state.has('Flippers', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Light World Pier', player), lambda state: state.has('Flippers', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Kings Grave', player), lambda state: state.has('Pegasus Boots', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Kings Grave Outer Rocks', player), lambda state: state.can_lift_heavy_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Kings Grave Inner Rocks', player), lambda state: state.can_lift_heavy_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Potion Shop Inner Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Potion Shop Outer Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Potion Shop Outer Rock', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Potion Shop Inner Rock', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Graveyard Cave Inner Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Graveyard Cave Outer Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Secret Passage Inner Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Secret Passage Outer Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Bonk Fairy (Light)', player), lambda state: state.has('Pegasus Boots', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Bat Cave Drop Ledge', player), lambda state: state.has('Hammer', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Lumberjack Tree Tree', player), lambda state: state.has('Pegasus Boots', player) and state.has('Moon Pearl', player) and state.has('Beat Agahnim 1', player))
    set_rule(world.get_entrance('Bonk Rock Cave', player), lambda state: state.has('Pegasus Boots', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Desert Palace Stairs', player), lambda state: state.has('Book of Mudora', player))  # bunny can use book
    set_rule(world.get_entrance('Sanctuary Grave', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('20 Rupee Cave', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('50 Rupee Cave', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Death Mountain Entrance Rock', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Bumper Cave Entrance Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Lake Hylia Central Island Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Dark Lake Hylia Central Island Teleporter', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Dark Desert Teleporter', player), lambda state: state.has('Activated Flute', player) and state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('East Dark World Teleporter', player), lambda state: state.has('Hammer', player) and state.can_lift_rocks(player) and state.has('Moon Pearl', player)) # bunny cannot use hammer
    set_rule(world.get_entrance('South Dark World Teleporter', player), lambda state: state.has('Hammer', player) and state.can_lift_rocks(player) and state.has('Moon Pearl', player)) # bunny cannot use hammer
    set_rule(world.get_entrance('West Dark World Teleporter', player), lambda state: ((state.has('Hammer', player) and state.can_lift_rocks(player)) or state.can_lift_heavy_rocks(player)) and state.has('Moon Pearl', player))
    set_rule(world.get_location('Flute Spot', player), lambda state: state.has('Shovel', player) and state.has('Moon Pearl', player))

    set_rule(world.get_location('Zora\'s Ledge', player), lambda state: state.has('Flippers', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Waterfall of Wishing Cave', player), lambda state: state.has('Flippers', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Northeast Light World Return', player), lambda state: state.has('Flippers', player) and state.has('Moon Pearl', player))
    set_rule(world.get_location('Frog', player), lambda state: state.can_lift_heavy_rocks(player) and (state.has('Moon Pearl', player) or state.has('Beat Agahnim 1', player)) or (state.can_reach('Light World', 'Region', player) and state.has('Magic Mirror', player))) # Need LW access using Mirror or Portal
    set_rule(world.get_location('Missing Smith', player), lambda state: state.has('Get Frog', player) and state.can_reach('Blacksmiths Hut', 'Region', player)) # Can't S&Q with smith
    set_rule(world.get_location('Blacksmith', player), lambda state: state.has('Return Smith', player))
    set_rule(world.get_location('Magic Bat', player), lambda state: state.has('Magic Powder', player) and state.has('Moon Pearl', player))
    set_rule(world.get_location('Sick Kid', player), lambda state: state.has_group("Bottles", player))
    set_rule(world.get_location('Mushroom', player), lambda state: state.has('Moon Pearl', player)) # need pearl to pick up bushes
    set_rule(world.get_entrance('Bush Covered Lawn Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Bush Covered Lawn Inner Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Bush Covered Lawn Outer Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Bomb Hut Inner Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Bomb Hut Outer Bushes', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Light World Bomb Hut', player), lambda state: state.has('Moon Pearl', player)) # need bomb
    set_rule(world.get_entrance('North Fairy Cave Drop', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Lost Woods Hideout Drop', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_location('Potion Shop', player), lambda state: state.has('Mushroom', player) and (state.can_reach('Potion Shop Area', 'Region', player))) # new inverted region, need pearl for bushes or access to potion shop door/waterfall fairy
    set_rule(world.get_entrance('Desert Palace Entrance (North) Rocks', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Desert Ledge Return Rocks', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))  # should we decide to place something that is not a dungeon end up there at some point
    set_rule(world.get_entrance('Checkerboard Cave', player), lambda state: state.can_lift_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Hyrule Castle Secret Entrance Drop', player), lambda state: state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Old Man Cave Exit (West)', player), lambda state: False)  # drop cannot be climbed up
    set_rule(world.get_entrance('Broken Bridge (West)', player), lambda state: state.has('Hookshot', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Broken Bridge (East)', player), lambda state: state.has('Hookshot', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Dark Death Mountain Teleporter (East Bottom)', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('Fairy Ascension Rocks', player), lambda state: state.can_lift_heavy_rocks(player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Paradox Cave Push Block Reverse', player), lambda state: state.has('Mirror', player))  # can erase block
    set_rule(world.get_entrance('Death Mountain (Top)', player), lambda state: state.has('Hammer', player) and state.has('Moon Pearl', player))
    set_rule(world.get_entrance('Dark Death Mountain Teleporter (East)', player), lambda state: state.can_lift_heavy_rocks(player) and state.has('Hammer', player) and state.has('Moon Pearl', player))  # bunny cannot use hammer
    set_rule(world.get_entrance('East Death Mountain (Top)', player), lambda state: state.has('Hammer', player) and state.has('Moon Pearl', player))  # bunny can not use hammer

    set_rule(world.get_entrance('Catfish Entrance Rock', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Northeast Dark World Broken Bridge Pass', player), lambda state: ((state.can_lift_rocks(player) or state.has('Hammer', player)) or state.has('Flippers', player)))
    set_rule(world.get_entrance('East Dark World Broken Bridge Pass', player), lambda state: (state.can_lift_rocks(player) or state.has('Hammer', player)))
    set_rule(world.get_entrance('South Dark World Bridge', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Bonk Fairy (Dark)', player), lambda state: state.has('Pegasus Boots', player))
    set_rule(world.get_entrance('West Dark World Gap', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: state.has('Flippers', player))
    set_rule(world.get_location('Bombos Tablet', player), lambda state: state.can_retrieve_tablet(player))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (South)', player), lambda state: state.has('Flippers', player))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Pier', player), lambda state: state.has('Flippers', player))
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Spike Cave', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has('Flippers', player))  # Fake Flippers
    set_rule(world.get_entrance('Dark Lake Hylia Shallows', player), lambda state: state.has('Flippers', player))
    set_rule(world.get_entrance('Village of Outcasts Heavy Rock', player), lambda state: state.can_lift_heavy_rocks(player))
    set_rule(world.get_entrance('East Dark World Bridge', player), lambda state: state.has('Hammer', player))
    set_rule(world.get_entrance('Lake Hylia Central Island Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('East Dark World River Pier', player), lambda state: state.has('Flippers', player))
    set_rule(world.get_entrance('Bumper Cave Entrance Rock', player), lambda state: state.can_lift_rocks(player))
    set_rule(world.get_entrance('Bumper Cave Ledge Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Hammer Peg Area Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
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

    set_rule(world.get_entrance('East Death Mountain Mirror Spot (Top)', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Death Mountain (Top) Mirror Spot', player), lambda state: state.has('Magic Mirror', player))

    set_rule(world.get_entrance('East Death Mountain Mirror Spot (Bottom)', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Dark Death Mountain Ledge Mirror Spot (East)', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Dark Death Mountain Ledge Mirror Spot (West)', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Laser Bridge Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Floating Island Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Turtle Rock', player), lambda state: state.has_sword(player) and state.has_turtle_rock_medallion(player) and state.can_reach('Turtle Rock (Top)', 'Region', player)) # sword required to cast magic (!)

    # new inverted spots
    set_rule(world.get_entrance('Post Aga Teleporter', player), lambda state: state.has('Beat Agahnim 1', player))
    set_rule(world.get_entrance('Mire Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Desert Palace Stairs Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Death Mountain Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('East Dark World Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('West Dark World Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('South Dark World Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Catfish Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Potion Shop Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Shopping Mall Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Maze Race Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Desert Palace North Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Death Mountain (Top) Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Graveyard Cave Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Bomb Hut Mirror Spot', player), lambda state: state.has('Magic Mirror', player))
    set_rule(world.get_entrance('Skull Woods Mirror Spot', player), lambda state: state.has('Magic Mirror', player))

    # inverted flute spots

    set_rule(world.get_entrance('DDM Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('NEDW Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('WDW Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('SDW Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('EDW Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('DLHL Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('DD Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('EDDM Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('Dark Grassy Lawn Flute', player), lambda state: state.has('Activated Flute', player))
    set_rule(world.get_entrance('Hammer Peg Area Flute', player), lambda state: state.has('Activated Flute', player))

    set_rule(world.get_entrance('Inverted Pyramid Hole', player), lambda state: state.has('Beat Agahnim 2', player) or world.open_pyramid[player])

    if world.swordless[player]:
        swordless_rules(world, player)

def no_glitches_rules(world, player):
    """"""
    if world.mode[player] == 'inverted':
        set_rule(world.get_entrance('Zoras River', player), lambda state: state.has('Moon Pearl', player) and (state.has('Flippers', player) or state.can_lift_rocks(player)))
        set_rule(world.get_entrance('Lake Hylia Central Island Pier', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))  # can be fake flippered to
        set_rule(world.get_entrance('Lake Hylia Island Pier', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))  # can be fake flippered to
        set_rule(world.get_entrance('Lake Hylia Warp', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))  # can be fake flippered to
        set_rule(world.get_entrance('Northeast Light World Warp', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))  # can be fake flippered to
        set_rule(world.get_entrance('Hobo Bridge', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Ledge Drop', player), lambda state: state.has('Flippers', player))
        set_rule(world.get_entrance('East Dark World Pier', player), lambda state: state.has('Flippers', player))
    else:
        set_rule(world.get_entrance('Zoras River', player), lambda state: state.has('Flippers', player) or state.can_lift_rocks(player))
        set_rule(world.get_entrance('Lake Hylia Central Island Pier', player), lambda state: state.has('Flippers', player))  # can be fake flippered to
        set_rule(world.get_entrance('Hobo Bridge', player), lambda state: state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Ledge Drop', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))

    add_rule(world.get_entrance('Ganons Tower (Double Switch Room)', player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_entrance('Paradox Cave Push Block Reverse', player), lambda state: False)  # no glitches does not require block override
    forbid_bomb_jump_requirements(world, player)
    add_conditional_lamps(world, player)

def fake_flipper_rules(world, player):
    if world.mode[player] == 'inverted':
        set_rule(world.get_entrance('Zoras River', player), lambda state: state.has('Moon Pearl', player))
        set_rule(world.get_entrance('Lake Hylia Central Island Pier', player), lambda state: state.has('Moon Pearl', player))
        set_rule(world.get_entrance('Lake Hylia Island Pier', player), lambda state: state.has('Moon Pearl', player))
        set_rule(world.get_entrance('Lake Hylia Warp', player), lambda state: state.has('Moon Pearl', player))
        set_rule(world.get_entrance('Northeast Light World Warp', player), lambda state: state.has('Moon Pearl', player))
        set_rule(world.get_entrance('Hobo Bridge', player), lambda state: state.has('Moon Pearl', player))
        set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: True)
        set_rule(world.get_entrance('Dark Lake Hylia Ledge Drop', player), lambda state: True)
        set_rule(world.get_entrance('East Dark World Pier', player), lambda state: True)
        #qirn jump
        set_rule(world.get_entrance('East Dark World River Pier', player), lambda state: True)
    else:
        set_rule(world.get_entrance('Zoras River', player), lambda state: True)
        set_rule(world.get_entrance('Lake Hylia Central Island Pier', player), lambda state: True)
        set_rule(world.get_entrance('Hobo Bridge', player), lambda state: True)
        set_rule(world.get_entrance('Dark Lake Hylia Drop (East)', player), lambda state: state.has('Moon Pearl', player) and state.has('Flippers', player))
        set_rule(world.get_entrance('Dark Lake Hylia Teleporter', player), lambda state: state.has('Moon Pearl', player))
        set_rule(world.get_entrance('Dark Lake Hylia Ledge Drop', player), lambda state: state.has('Moon Pearl', player))
        #qirn jump
        set_rule(world.get_entrance('East Dark World River Pier', player), lambda state: state.has('Moon Pearl', player))


def forbid_bomb_jump_requirements(world, player):
    DMs_room_chests = ['Ganons Tower - DMs Room - Top Left', 'Ganons Tower - DMs Room - Top Right', 'Ganons Tower - DMs Room - Bottom Left', 'Ganons Tower - DMs Room - Bottom Right']
    for location in DMs_room_chests:
        add_rule(world.get_location(location, player), lambda state: state.has('Hookshot', player))
    set_rule(world.get_entrance('Paradox Cave Bomb Jump', player), lambda state: False)
    set_rule(world.get_entrance('Skull Woods First Section Bomb Jump', player), lambda state: False)


DW_Entrances = ['Bumper Cave (Bottom)',
                'Superbunny Cave (Top)',
                'Superbunny Cave (Bottom)',
                'Hookshot Cave',
                'Bumper Cave (Top)',
                'Hookshot Cave Back Entrance',
                'Dark Death Mountain Ledge (East)',
                'Turtle Rock Isolated Ledge Entrance',
                'Thieves Town',
                'Skull Woods Final Section',
                'Ice Palace',
                'Misery Mire',
                'Palace of Darkness',
                'Swamp Palace',
                'Turtle Rock',
                'Dark Death Mountain Ledge (West)']

def check_is_dark_world(region):
    for entrance in region.entrances:
        if entrance.name in DW_Entrances:
            return True
    return False


def add_conditional_lamps(world, player):
    # Light cones in standard depend on which world we actually are in, not which one the location would normally be
    # We add Lamp requirements only to those locations which lie in the dark world (or everything if open

    def add_conditional_lamp(spot, region, spottype='Location', accessible_torch=False):
        if (not world.dark_world_light_cone and check_is_dark_world(world.get_region(region, player))) or (
                not world.light_world_light_cone and not check_is_dark_world(world.get_region(region, player))):
            if spottype == 'Location':
                spot = world.get_location(spot, player)
            else:
                spot = world.get_entrance(spot, player)
            add_lamp_requirement(world, spot, player, accessible_torch)

    add_conditional_lamp('Misery Mire (Vitreous)', 'Misery Mire (Entrance)', 'Entrance')
    add_conditional_lamp('Turtle Rock (Dark Room) (North)', 'Turtle Rock (Entrance)', 'Entrance')
    add_conditional_lamp('Turtle Rock (Dark Room) (South)', 'Turtle Rock (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness Big Key Door', 'Palace of Darkness (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness Maze Door', 'Palace of Darkness (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness - Dark Basement - Left', 'Palace of Darkness (Entrance)',
                         'Location', True)
    add_conditional_lamp('Palace of Darkness - Dark Basement - Right', 'Palace of Darkness (Entrance)',
                         'Location', True)
    if world.mode[player] != 'inverted':
        add_conditional_lamp('Agahnim 1', 'Agahnims Tower', 'Entrance')
        add_conditional_lamp('Castle Tower - Dark Maze', 'Agahnims Tower')
    else:
        add_conditional_lamp('Agahnim 1', 'Inverted Agahnims Tower', 'Entrance')
        add_conditional_lamp('Castle Tower - Dark Maze', 'Inverted Agahnims Tower')
    add_conditional_lamp('Old Man', 'Old Man Cave')
    add_conditional_lamp('Old Man Cave Exit (East)', 'Old Man Cave', 'Entrance')
    add_conditional_lamp('Death Mountain Return Cave Exit (East)', 'Death Mountain Return Cave', 'Entrance')
    add_conditional_lamp('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave', 'Entrance')
    add_conditional_lamp('Old Man House Front to Back', 'Old Man House', 'Entrance')
    add_conditional_lamp('Old Man House Back to Front', 'Old Man House', 'Entrance')
    add_conditional_lamp('Eastern Palace - Big Key Chest', 'Eastern Palace')
    add_conditional_lamp('Eastern Palace - Boss', 'Eastern Palace', 'Location', True)
    add_conditional_lamp('Eastern Palace - Prize', 'Eastern Palace', 'Location', True)

    if not world.mode[player] == "standard":
        add_lamp_requirement(world, world.get_location('Sewers - Dark Cross', player), player)
        add_lamp_requirement(world, world.get_entrance('Sewers Back Door', player), player)
        add_lamp_requirement(world, world.get_entrance('Throne Room', player), player)


def open_rules(world, player):
    # softlock protection as you can reach the sewers small key door with a guard drop key
    set_rule(world.get_location('Hyrule Castle - Boomerang Chest', player),
             lambda state: state._lttp_has_key('Small Key (Hyrule Castle)', player))
    set_rule(world.get_location('Hyrule Castle - Zelda\'s Chest', player),
             lambda state: state._lttp_has_key('Small Key (Hyrule Castle)', player))


def swordless_rules(world, player):
    set_rule(world.get_entrance('Agahnim 1', player), lambda state: (state.has('Hammer', player) or state.has('Fire Rod', player) or state.can_shoot_arrows(player) or state.has('Cane of Somaria', player)) and state._lttp_has_key('Small Key (Agahnims Tower)', player, 2))
    set_rule(world.get_entrance('Skull Woods Torch Room', player), lambda state: state._lttp_has_key('Small Key (Skull Woods)', player, 3) and state.has('Fire Rod', player))  # no curtain
    set_rule(world.get_entrance('Ice Palace Entrance Room', player), lambda state: state.has('Fire Rod', player) or state.has('Bombos', player)) #in swordless mode bombos pads are present in the relevant parts of ice palace
    set_rule(world.get_entrance('Ganon Drop', player), lambda state: state.has('Hammer', player))  # need to damage ganon to get tiles to drop

    if world.mode[player] != 'inverted':
        set_rule(world.get_entrance('Agahnims Tower', player), lambda state: state.has('Cape', player) or state.has('Hammer', player) or state.has('Beat Agahnim 1', player))  # barrier gets removed after killing agahnim, relevant for entrance shuffle
        set_rule(world.get_entrance('Turtle Rock', player), lambda state: state.has('Moon Pearl', player) and state.has_turtle_rock_medallion(player) and state.can_reach('Turtle Rock (Top)', 'Region', player))   # sword not required to use medallion for opening in swordless (!)
        set_rule(world.get_entrance('Misery Mire', player), lambda state: state.has('Moon Pearl', player) and state.has_misery_mire_medallion(player))  # sword not required to use medallion for opening in swordless (!)
    else:
        # only need ddm access for aga tower in inverted
        set_rule(world.get_entrance('Turtle Rock', player), lambda state: state.has_turtle_rock_medallion(player) and state.can_reach('Turtle Rock (Top)', 'Region', player))   # sword not required to use medallion for opening in swordless (!)
        set_rule(world.get_entrance('Misery Mire', player), lambda state: state.has_misery_mire_medallion(player))  # sword not required to use medallion for opening in swordless (!)


def add_connection(parent_name, target_name, entrance_name, world, player):
    parent = world.get_region(parent_name, player)
    target = world.get_region(target_name, player)
    connection = Entrance(player, entrance_name, parent)
    parent.exits.append(connection)
    connection.connect(target)

def standard_rules(world, player):
    add_connection('Menu', 'Hyrule Castle Secret Entrance', 'Uncle S&Q', world, player)
    world.get_entrance('Uncle S&Q', player).hide_path = True
    set_rule(world.get_entrance('Hyrule Castle Exit (East)', player), lambda state: state.can_reach('Sanctuary', 'Region', player))
    set_rule(world.get_entrance('Hyrule Castle Exit (West)', player), lambda state: state.can_reach('Sanctuary', 'Region', player))
    set_rule(world.get_entrance('Links House S&Q', player), lambda state: state.can_reach('Sanctuary', 'Region', player))
    set_rule(world.get_entrance('Sanctuary S&Q', player), lambda state: state.can_reach('Sanctuary', 'Region', player))

def toss_junk_item(world, player):
    items = ['Rupees (20)', 'Bombs (3)', 'Arrows (10)', 'Rupees (5)', 'Rupee (1)', 'Bombs (10)',
             'Single Arrow', 'Rupees (50)', 'Rupees (100)', 'Single Bomb', 'Bee', 'Bee Trap',
             'Rupees (300)', 'Nothing']
    for item in items:
        big20 = next((i for i in world.itempool if i.name == item and i.player == player), None)
        if big20:
            world.itempool.remove(big20)
            return
    raise Exception("Unable to find a junk item to toss to make room for a TR small key")


def set_trock_key_rules(world, player):
    # First set all relevant locked doors to impassible.
    for entrance in ['Turtle Rock Dark Room Staircase', 'Turtle Rock (Chain Chomp Room) (North)', 'Turtle Rock (Chain Chomp Room) (South)', 'Turtle Rock Pokey Room', 'Turtle Rock Big Key Door']:
        set_rule(world.get_entrance(entrance, player), lambda state: False)

    all_state = world.get_all_state(use_cache=False)
    all_state.reachable_regions[player] = set()  # wipe reachable regions so that the locked doors actually work
    all_state.stale[player] = True

    # Check if each of the four main regions of the dungoen can be reached. The previous code section prevents key-costing moves within the dungeon.
    can_reach_back = all_state.can_reach(world.get_region('Turtle Rock (Eye Bridge)', player)) if world.can_access_trock_eyebridge[player] is None else world.can_access_trock_eyebridge[player]
    world.can_access_trock_eyebridge[player] = can_reach_back
    can_reach_front = all_state.can_reach(world.get_region('Turtle Rock (Entrance)', player)) if world.can_access_trock_front[player] is None else world.can_access_trock_front[player]
    world.can_access_trock_front[player] = can_reach_front
    can_reach_big_chest = all_state.can_reach(world.get_region('Turtle Rock (Big Chest)', player)) if world.can_access_trock_big_chest[player] is None else world.can_access_trock_big_chest[player]
    world.can_access_trock_big_chest[player] = can_reach_big_chest
    can_reach_middle = all_state.can_reach(world.get_region('Turtle Rock (Second Section)', player)) if world.can_access_trock_middle[player] is None else world.can_access_trock_middle[player]
    world.can_access_trock_middle[player] = can_reach_middle

    # If you can't enter from the back, the door to the front of TR requires only 2 small keys if the big key is in one of these chests since 2 key doors are locked behind the big key door.
    # If you can only enter from the middle, this includes all locations that can only be reached by exiting the front.  This can include Laser Bridge and Crystaroller if the front and back connect via Dark DM Ledge!
    front_locked_locations = {('Turtle Rock - Compass Chest', player), ('Turtle Rock - Roller Room - Left', player), ('Turtle Rock - Roller Room - Right', player)}
    if can_reach_middle and not can_reach_back and not can_reach_front:
        normal_regions = all_state.reachable_regions[player].copy()
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (South)', player), lambda state: True)
        all_state.update_reachable_regions(player)
        front_locked_regions = all_state.reachable_regions[player].difference(normal_regions)
        front_locked_locations = set((location.name, player) for region in front_locked_regions for location in region.locations)


    # The following represent the common key rules.

    # Big key door requires the big key, obviously. We removed this rule in the previous section to flag front_locked_locations correctly,
    # otherwise crystaroller room might not be properly marked as reachable through the back.
    set_rule(world.get_entrance('Turtle Rock Big Key Door', player), lambda state: state.has('Big Key (Turtle Rock)', player))

    # No matter what, the key requirement for going from the middle to the bottom should be three keys.
    set_rule(world.get_entrance('Turtle Rock Dark Room Staircase', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, 3))

    # Now we need to set rules based on which entrances we have access to. The most important point is whether we have back access. If we have back access, we
    # might open all the locked doors in any order so we need maximally restrictive rules.
    if can_reach_back:
        set_rule(world.get_location('Turtle Rock - Big Key Chest', player), lambda state: (state._lttp_has_key('Small Key (Turtle Rock)', player, 4) or item_name(state, 'Turtle Rock - Big Key Chest', player) == ('Small Key (Turtle Rock)', player)))
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (South)', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, 4))
        # Only consider wasting the key on the Trinexx door for going from the front entrance to middle section.  If other key doors are accessible, then these doors can be avoided
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (North)', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, 3))
        set_rule(world.get_entrance('Turtle Rock Pokey Room', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, 2))
    else:
        # Middle to front requires 2 keys if the back is locked, otherwise 4
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (South)', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, 2)
                if item_in_locations(state, 'Big Key (Turtle Rock)', player, front_locked_locations)
                else state._lttp_has_key('Small Key (Turtle Rock)', player, 4))

        # Front to middle requires 2 keys (if the middle is accessible then these doors can be avoided, otherwise no keys can be wasted)
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (North)', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, 2))
        set_rule(world.get_entrance('Turtle Rock Pokey Room', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, 1))

        set_rule(world.get_location('Turtle Rock - Big Key Chest', player), lambda state: state._lttp_has_key('Small Key (Turtle Rock)', player, tr_big_key_chest_keys_needed(state)))

        def tr_big_key_chest_keys_needed(state):
            # This function handles the key requirements for the TR Big Chest in the situations it having the Big Key should logically require 2 keys, small key
            # should logically require no keys, and anything else should logically require 4 keys.
            item = item_name(state, 'Turtle Rock - Big Key Chest', player)
            if item in [('Small Key (Turtle Rock)', player)]:
                return 0
            if item in [('Big Key (Turtle Rock)', player)]:
                return 2
            return 4

        # If TR is only accessible from the middle, the big key must be further restricted to prevent softlock potential
        if not can_reach_front and not world.smallkey_shuffle[player]:
            # Must not go in the Big Key Chest - only 1 other chest available and 2+ keys required for all other chests
            forbid_item(world.get_location('Turtle Rock - Big Key Chest', player), 'Big Key (Turtle Rock)', player)
            if not can_reach_big_chest:
                # Must not go in the Chain Chomps chest - only 2 other chests available and 3+ keys required for all other chests
                forbid_item(world.get_location('Turtle Rock - Chain Chomps', player), 'Big Key (Turtle Rock)', player)
            if world.accessibility[player] == 'locations' and world.goal[player] != 'icerodhunt':
                if world.bigkey_shuffle[player] and can_reach_big_chest:
                    # Must not go in the dungeon - all 3 available chests (Chomps, Big Chest, Crystaroller) must be keys to access laser bridge, and the big key is required first
                    for location in ['Turtle Rock - Chain Chomps', 'Turtle Rock - Compass Chest',
                                     'Turtle Rock - Roller Room - Left', 'Turtle Rock - Roller Room - Right']:
                        forbid_item(world.get_location(location, player), 'Big Key (Turtle Rock)', player)
                else:
                    # A key is required in the Big Key Chest to prevent a possible softlock.  Place an extra key to ensure 100% locations still works
                    item = ItemFactory('Small Key (Turtle Rock)', player)
                    location = world.get_location('Turtle Rock - Big Key Chest', player)
                    location.place_locked_item(item)
                    location.event = True
                    toss_junk_item(world, player)

    if world.accessibility[player] != 'locations':
        set_always_allow(world.get_location('Turtle Rock - Big Key Chest', player), lambda state, item: item.name == 'Small Key (Turtle Rock)' and item.player == player
                and state.can_reach(state.multiworld.get_region('Turtle Rock (Second Section)', player)))


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
                             'Village of Outcasts Shop',
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
        return state.has('Hammer', player) and state.has('Moon Pearl', player)

    # returning via the eastern and southern teleporters needs the same items, so we use the southern teleporter for out routing.
    # crossing preg bridge already requires hammer so we just add the gloves to the requirement
    def southern_teleporter(state):
        return state.can_lift_rocks(player) and cross_peg_bridge(state)

    # the basic routes assume you can reach eastern light world with the bomb.
    # you can then use the southern teleporter, or (if you have beaten Aga1) the hyrule castle gate warp
    def basic_routes(state):
        return southern_teleporter(state) or state.has('Beat Agahnim 1', player)

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
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: basic_routes(state) or state.has('Magic Mirror', player))
    elif bombshop_entrance.name in LW_walkable_entrances:
        #1. Mirror then basic routes
        # -> M and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Magic Mirror', player) and basic_routes(state))
    elif bombshop_entrance.name in Northern_DW_entrances:
        #1. Mirror and basic routes
        #2. Go to south DW and then cross peg bridge: Need Mitts and hammer and moon pearl
        # -> (Mitts and CPB) or (M and BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.can_lift_heavy_rocks(player) and cross_peg_bridge(state)) or (state.has('Magic Mirror', player) and basic_routes(state)))
    elif bombshop_entrance.name == 'Bumper Cave (Bottom)':
        #1. Mirror and Lift rock and basic_routes
        #2. Mirror and Flute and basic routes (can make difference if accessed via insanity or w/ mirror from connector, and then via hyrule castle gate, because no gloves are needed in that case)
        #3. Go to south DW and then cross peg bridge: Need Mitts and hammer and moon pearl
        # -> (Mitts and CPB) or (((G or Flute) and M) and BR))
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.can_lift_heavy_rocks(player) and cross_peg_bridge(state)) or (((state.can_lift_rocks(player) or state.has('Flute', player)) and state.has('Magic Mirror', player)) and basic_routes(state)))
    elif bombshop_entrance.name in Southern_DW_entrances:
        #1. Mirror and enter via gate: Need mirror and Aga1
        #2. cross peg bridge: Need hammer and moon pearl
        # -> CPB or (M and A)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: cross_peg_bridge(state) or (state.has('Magic Mirror', player) and state.has('Beat Agahnim 1', player)))
    elif bombshop_entrance.name in Isolated_DW_entrances:
        # 1. mirror then flute then basic routes
        # -> M and Flute and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Magic Mirror', player) and state.has('Activated Flute', player) and basic_routes(state))
    elif bombshop_entrance.name in Isolated_LW_entrances:
        # 1. flute then basic routes
        # Prexisting mirror spot is not permitted, because mirror might have been needed to reach these isolated locations.
        # -> Flute and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) and basic_routes(state))
    elif bombshop_entrance.name in West_LW_DM_entrances:
        # 1. flute then basic routes or mirror
        # Prexisting mirror spot is permitted, because flute can be used to reach west DM directly.
        # -> Flute and (M or BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) and (state.has('Magic Mirror', player) or basic_routes(state)))
    elif bombshop_entrance.name in East_LW_DM_entrances:
        # 1. flute then basic routes or mirror and hookshot
        # Prexisting mirror spot is permitted, because flute can be used to reach west DM directly and then east DM via Hookshot
        # -> Flute and ((M and Hookshot) or BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) and ((state.has('Magic Mirror', player) and state.has('Hookshot', player)) or basic_routes(state)))
    elif bombshop_entrance.name == 'Fairy Ascension Cave (Bottom)':
        # Same as East_LW_DM_entrances except navigation without BR requires Mitts
        # -> Flute and ((M and Hookshot and Mitts) or BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) and ((state.has('Magic Mirror', player) and state.has('Hookshot', player) and state.can_lift_heavy_rocks(player)) or basic_routes(state)))
    elif bombshop_entrance.name in Castle_ledge_entrances:
        # 1. mirror on pyramid to castle ledge, grab bomb, return through mirror spot: Needs mirror
        # 2. flute then basic routes
        # -> M or (Flute and BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Magic Mirror', player) or (state.has('Activated Flute', player) and basic_routes(state)))
    elif bombshop_entrance.name in Desert_mirrorable_ledge_entrances:
        # Cases when you have mire access: Mirror to reach locations, return via mirror spot, move to center of desert, mirror anagin and:
        # 1. Have mire access, Mirror to reach locations, return via mirror spot, move to center of desert, mirror again and then basic routes
        # 2. flute then basic routes
        # -> (Mire access and M) or Flute) and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: ((state.can_reach('Dark Desert', 'Region', player) and state.has('Magic Mirror', player)) or state.has('Activated Flute', player)) and basic_routes(state))
    elif bombshop_entrance.name == 'Old Man Cave (West)':
        # 1. Lift rock then basic_routes
        # 2. flute then basic_routes
        # -> (Flute or G) and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Activated Flute', player) or state.can_lift_rocks(player)) and basic_routes(state))
    elif bombshop_entrance.name == 'Graveyard Cave':
        # 1. flute then basic routes
        # 2. (has west dark world access) use existing mirror spot (required Pearl), mirror again off ledge
        # -> (Flute or (M and P and West Dark World access) and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Activated Flute', player) or (state.can_reach('West Dark World', 'Region', player) and state.has('Moon Pearl', player) and state.has('Magic Mirror', player))) and basic_routes(state))
    elif bombshop_entrance.name in Mirror_from_SDW_entrances:
        # 1. flute then basic routes
        # 2. (has South dark world access) use existing mirror spot, mirror again off ledge
        # -> (Flute or (M and South Dark World access) and BR
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Activated Flute', player) or (state.can_reach('South Dark World', 'Region', player) and state.has('Magic Mirror', player))) and basic_routes(state))
    elif bombshop_entrance.name == 'Dark World Potion Shop':
        # 1. walk down by lifting rock: needs gloves and pearl`
        # 2. walk down by hammering peg: needs hammer and pearl
        # 3. mirror and basic routes
        # -> (P and (H or Gloves)) or (M and BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Moon Pearl', player) and (state.has('Hammer', player) or state.can_lift_rocks(player))) or (state.has('Magic Mirror', player) and basic_routes(state)))
    elif bombshop_entrance.name == 'Kings Grave':
        # same as the Normal_LW_entrances case except that the pre-existing mirror is only possible if you have mitts
        # (because otherwise mirror was used to reach the grave, so would cancel a pre-existing mirror spot)
        # to account for insanity, must consider a way to escape without a cave for basic_routes
        # -> (M and Mitts) or ((Mitts or Flute or (M and P and West Dark World access)) and BR)
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.can_lift_heavy_rocks(player) and state.has('Magic Mirror', player)) or ((state.can_lift_heavy_rocks(player) or state.has('Activated Flute', player) or (state.can_reach('West Dark World', 'Region', player) and state.has('Moon Pearl', player) and state.has('Magic Mirror', player))) and basic_routes(state)))
    elif bombshop_entrance.name == 'Waterfall of Wishing':
        # same as the Normal_LW_entrances case except in insanity it's possible you could be here without Flippers which
        # means you need an escape route of either Flippers or Flute
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Flippers', player) or state.has('Activated Flute', player)) and (basic_routes(state) or state.has('Magic Mirror', player)))


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
                           'Checkerboard Cave',
                           'Inverted Big Bomb Shop']
    Isolated_LW_entrances = ['Old Man Cave (East)',
                             'Old Man House (Bottom)',
                             'Old Man House (Top)',
                             'Death Mountain Return Cave (East)',
                             'Spectacle Rock Cave Peak',
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
    Eastern_DW_entrances = ['Palace of Darkness',
                            'Palace of Darkness Hint',
                            'Dark Lake Hylia Fairy',
                            'East Dark World Hint']
    Northern_DW_entrances = ['Brewery',
                             'C-Shaped House',
                             'Chest Game',
                             'Dark World Hammer Peg Cave',
                             'Inverted Dark Sanctuary',
                             'Fortune Teller (Dark)',
                             'Dark World Lumberjack Shop',
                             'Thieves Town',
                             'Skull Woods First Section Door',
                             'Skull Woods Second Section Door (East)']
    Southern_DW_entrances = ['Hype Cave',
                             'Bonk Fairy (Dark)',
                             'Archery Game',
                             'Inverted Links House',
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
                             'Inverted Agahnims Tower']
    LW_walkable_entrances = ['Dark Lake Hylia Ledge Fairy',
                             'Dark Lake Hylia Ledge Spike Cave',
                             'Dark Lake Hylia Ledge Hint',
                             'Mire Shed',
                             'Dark Desert Hint',
                             'Dark Desert Fairy',
                             'Misery Mire',
                             'Red Shield Shop']
    LW_bush_entrances = ['Bush Covered House',
                         'Light World Bomb Hut',
                         'Graveyard Cave']
    LW_inaccessible_entrances = ['Desert Palace Entrance (East)',
                                 'Spectacle Rock Cave',
                                 'Spectacle Rock Cave (Bottom)']

    set_rule(world.get_entrance('Pyramid Fairy', player),
             lambda state: state.can_reach('East Dark World', 'Region', player) and state.can_reach('Inverted Big Bomb Shop', 'Region', player) and state.has('Crystal 5', player) and state.has('Crystal 6', player))

    # Key for below abbreviations:
    # P = pearl
    # A = Aga1
    # H = hammer
    # M = Mirror
    # G = Glove
    if bombshop_entrance.name in Eastern_DW_entrances:
        # Just walk to the pyramid
        pass
    elif bombshop_entrance.name in Normal_LW_entrances:
        # Just walk to the castle and mirror.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Magic Mirror', player))
    elif bombshop_entrance.name in Isolated_LW_entrances:
        # For these entrances, you cannot walk to the castle/pyramid and thus must use Mirror and then Flute.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) and state.has('Magic Mirror', player))
    elif bombshop_entrance.name in Northern_DW_entrances:
        # You can just fly with the Flute, you can take a long walk with Mitts and Hammer,
        # or you can leave a Mirror portal nearby and then walk to the castle to Mirror again.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) or (state.can_lift_heavy_rocks(player) and state.has('Hammer', player)) or (state.has('Magic Mirror', player) and state.can_reach('Light World', 'Region', player)))
    elif bombshop_entrance.name in Southern_DW_entrances:
        # This is the same as north DW without the Mitts rock present.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Hammer', player) or state.has('Activated Flute', player) or (state.has('Magic Mirror', player) and state.can_reach('Light World', 'Region', player)))
    elif bombshop_entrance.name in Isolated_DW_entrances:
        # There's just no way to escape these places with the bomb and no Flute.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player))
    elif bombshop_entrance.name in LW_walkable_entrances:
        # You can fly with the flute, or leave a mirror portal and walk through the light world
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) or (state.has('Magic Mirror', player) and state.can_reach('Light World', 'Region', player)))
    elif bombshop_entrance.name in LW_bush_entrances:
        # These entrances are behind bushes in LW so you need either Pearl or the tools to solve NDW bomb shop locations.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Magic Mirror', player) and (state.has('Activated Flute', player) or state.has('Moon Pearl', player) or (state.can_lift_heavy_rocks(player) and state.has('Hammer', player))))
    elif bombshop_entrance.name == 'Village of Outcasts Shop':
        # This is mostly the same as NDW but the Mirror path requires the Pearl, or using the Hammer
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) or (state.can_lift_heavy_rocks(player) and state.has('Hammer', player)) or (state.has('Magic Mirror', player) and state.can_reach('Light World', 'Region', player) and (state.has('Moon Pearl', player) or state.has('Hammer', player))))
    elif bombshop_entrance.name == 'Bumper Cave (Bottom)':
        # This is mostly the same as NDW but the Mirror path requires being able to lift a rock.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) or (state.can_lift_heavy_rocks(player) and state.has('Hammer', player)) or (state.has('Magic Mirror', player) and state.can_lift_rocks(player) and state.can_reach('Light World', 'Region', player)))
    elif bombshop_entrance.name == 'Old Man Cave (West)':
        # The three paths back are Mirror and DW walk, Mirror and Flute, or LW walk and then Mirror.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Magic Mirror', player) and ((state.can_lift_heavy_rocks(player) and state.has('Hammer', player)) or (state.can_lift_rocks(player) and state.has('Moon Pearl', player)) or state.has('Activated Flute', player)))
    elif bombshop_entrance.name == 'Dark World Potion Shop':
        # You either need to Flute to 5 or cross the rock/hammer choice pass to the south.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Activated Flute', player) or state.has('Hammer', player) or state.can_lift_rocks(player))
    elif bombshop_entrance.name == 'Kings Grave':
        # Either lift the rock and walk to the castle to Mirror or Mirror immediately and Flute.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Activated Flute', player) or state.can_lift_heavy_rocks(player)) and state.has('Magic Mirror', player))
    elif bombshop_entrance.name == 'Waterfall of Wishing':
        # You absolutely must be able to swim to return it from here.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Flippers', player) and state.has('Moon Pearl', player) and state.has('Magic Mirror', player))
    elif bombshop_entrance.name == 'Ice Palace':
        # You can swim to the dock or use the Flute to get off the island.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: state.has('Flippers', player) or state.has('Activated Flute', player))
    elif bombshop_entrance.name == 'Capacity Upgrade':
        # You must Mirror but then can use either Ice Palace return path.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Flippers', player) or state.has('Activated Flute', player)) and state.has('Magic Mirror', player))
    elif bombshop_entrance.name == 'Two Brothers House (West)':
        # First you must Mirror. Then you can either Flute, cross the peg bridge, or use the Agah 1 portal to Mirror again.
        add_rule(world.get_entrance('Pyramid Fairy', player), lambda state: (state.has('Activated Flute', player) or state.has('Hammer', player) or state.has('Beat Agahnim 1', player)) and state.has('Magic Mirror', player))
    elif bombshop_entrance.name in LW_inaccessible_entrances:
        # You can't get to the pyramid from these entrances without bomb duping.
        raise Exception('No valid path to open Pyramid Fairy. (Could not route from %s)' % bombshop_entrance.name)
    elif bombshop_entrance.name == 'Pyramid Fairy':
        # Self locking.  The shuffles don't put the bomb shop here, but doesn't lock anything important.
        set_rule(world.get_entrance('Pyramid Fairy', player), lambda state: False)
    else:
        raise Exception('No logic found for routing from %s to the pyramid.' % bombshop_entrance.name)


def set_bunny_rules(world: MultiWorld, player: int, inverted: bool):

    # regions for the exits of multi-entrance caves/drops that bunny cannot pass
    # Note spiral cave and two brothers house are passable in superbunny state for glitch logic with extra requirements.
    bunny_impassable_caves = ['Bumper Cave', 'Two Brothers House', 'Hookshot Cave', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)', 'Turtle Rock (Entrance)', 'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Skull Woods Second Section (Drop)',
                              'Turtle Rock (Eye Bridge)', 'Sewers', 'Pyramid', 'Spiral Cave (Top)', 'Desert Palace Main (Inner)', 'Fairy Ascension Cave (Drop)']

    bunny_accessible_locations = ['Link\'s Uncle', 'Sahasrahla', 'Sick Kid', 'Lost Woods Hideout', 'Lumberjack Tree',
                                  'Checkerboard Cave', 'Potion Shop', 'Spectacle Rock Cave', 'Pyramid',
                                  'Hype Cave - Generous Guy', 'Peg Cave', 'Bumper Cave Ledge', 'Dark Blacksmith Ruins',
                                  'Spectacle Rock', 'Bombos Tablet', 'Ether Tablet', 'Purple Chest', 'Blacksmith',
                                  'Missing Smith', 'Master Sword Pedestal', 'Bottle Merchant', 'Sunken Treasure',
                                  'Desert Ledge']

    def path_to_access_rule(path, entrance):
        return lambda state: state.can_reach(entrance.name, 'Entrance', entrance.player) and all(
            rule(state) for rule in path)

    def options_to_access_rule(options):
        return lambda state: any(rule(state) for rule in options)

    # Helper functions to determine if the moon pearl is required
    if inverted:
        def is_bunny(region):
            return region.is_light_world

        def is_link(region):
            return region.is_dark_world
    else:
        def is_bunny(region):
            return region.is_dark_world

        def is_link(region):
            return region.is_light_world

    def get_rule_to_add(region, location = None, connecting_entrance = None):
        # In OWG, a location can potentially be superbunny-mirror accessible or
        # bunny revival accessible.
        if world.logic[player] in ['minorglitches', 'owglitches', 'hybridglitches', 'nologic']:
            if region.name == 'Swamp Palace (Entrance)':  # Need to 0hp revive - not in logic
                return lambda state: state.has('Moon Pearl', player)
            if region.name == 'Tower of Hera (Bottom)':  # Need to hit the crystal switch
                return lambda state: state.has('Magic Mirror', player) and state.has_sword(player) or state.has('Moon Pearl', player)
            if region.name in OverworldGlitchRules.get_invalid_bunny_revival_dungeons():
                return lambda state: state.has('Magic Mirror', player) or state.has('Moon Pearl', player)
            if region.type == LTTPRegionType.Dungeon:
                return lambda state: True
            if (((location is None or location.name not in OverworldGlitchRules.get_superbunny_accessible_locations())
                    or (connecting_entrance is not None and connecting_entrance.name in OverworldGlitchRules.get_invalid_bunny_revival_dungeons()))
                    and not is_link(region)):
                return lambda state: state.has('Moon Pearl', player)
        else:
            if not is_link(region):
                return lambda state: state.has('Moon Pearl', player)

        # in this case we are mixed region.
        # we collect possible options.

        # The base option is having the moon pearl
        possible_options = [lambda state: state.has('Moon Pearl', player)]

        # We will search entrances recursively until we find
        # one that leads to an exclusively link state region
        # for each such entrance a new option is added that consist of:
        #    a) being able to reach it, and
        #    b) being able to access all entrances from there to `region`
        seen = {region}
        queue = collections.deque([(region, [])])
        while queue:
            (current, path) = queue.popleft()
            for entrance in current.entrances:
                new_region = entrance.parent_region
                if new_region in seen:
                    continue
                new_path = path + [entrance.access_rule]
                seen.add(new_region)
                if not is_link(new_region):
                    # For glitch rulesets, establish superbunny and revival rules.
                    if world.logic[player] in ['minorglitches', 'owglitches', 'hybridglitches', 'nologic'] and entrance.name not in OverworldGlitchRules.get_invalid_bunny_revival_dungeons():
                        if region.name in OverworldGlitchRules.get_sword_required_superbunny_mirror_regions():
                            possible_options.append(lambda state: path_to_access_rule(new_path, entrance) and state.has('Magic Mirror', player) and state.has_sword(player))
                        elif (region.name in OverworldGlitchRules.get_boots_required_superbunny_mirror_regions()
                              or location is not None and location.name in OverworldGlitchRules.get_boots_required_superbunny_mirror_locations()):
                            possible_options.append(lambda state: path_to_access_rule(new_path, entrance) and state.has('Magic Mirror', player) and state.has('Pegasus Boots', player))
                        elif location is not None and location.name in OverworldGlitchRules.get_superbunny_accessible_locations():
                            if new_region.name == 'Superbunny Cave (Bottom)' or region.name == 'Kakariko Well (top)':
                                possible_options.append(lambda state: path_to_access_rule(new_path, entrance))
                            else:
                                possible_options.append(lambda state: path_to_access_rule(new_path, entrance) and state.has('Magic Mirror', player))
                        if new_region.type != LTTPRegionType.Cave:
                            continue
                    else:
                        continue
                if is_bunny(new_region):
                    queue.append((new_region, new_path))
                else:
                    # we have reached pure link state, so we have a new possible option
                    possible_options.append(path_to_access_rule(new_path, entrance))
        return options_to_access_rule(possible_options)

    # Add requirements for bunny-impassible caves if link is a bunny in them
    for region in [world.get_region(name, player) for name in bunny_impassable_caves]:

        if not is_bunny(region):
            continue
        rule = get_rule_to_add(region)
        for exit in region.exits:
            add_rule(exit, rule)

    paradox_shop = world.get_region('Light World Death Mountain Shop', player)
    if is_bunny(paradox_shop):
        add_rule(paradox_shop.entrances[0], get_rule_to_add(paradox_shop))

    # Add requirements for all locations that are actually in the dark world, except those available to the bunny, including dungeon revival
    for entrance in world.get_entrances():
        if entrance.player == player and is_bunny(entrance.connected_region):
            if world.logic[player] in ['minorglitches', 'owglitches', 'hybridglitches', 'nologic'] :
                if entrance.connected_region.type == LTTPRegionType.Dungeon:
                    if entrance.parent_region.type != LTTPRegionType.Dungeon and entrance.connected_region.name in OverworldGlitchRules.get_invalid_bunny_revival_dungeons():
                        add_rule(entrance, get_rule_to_add(entrance.connected_region, None, entrance))
                    continue
                if entrance.connected_region.name == 'Turtle Rock (Entrance)':
                    add_rule(world.get_entrance('Turtle Rock Entrance Gap', player), get_rule_to_add(entrance.connected_region, None, entrance))
            for location in entrance.connected_region.locations:
                if world.logic[player] in ['minorglitches', 'owglitches', 'hybridglitches', 'nologic'] and entrance.name in OverworldGlitchRules.get_invalid_mirror_bunny_entrances():
                    continue
                if location.name in bunny_accessible_locations:
                    continue
                add_rule(location, get_rule_to_add(entrance.connected_region, location))