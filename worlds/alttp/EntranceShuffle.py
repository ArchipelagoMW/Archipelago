# ToDo: With shuffle_ganon option, prevent gtower from linking to an exit only location through a 2 entrance cave.
from collections import defaultdict

from .OverworldGlitchRules import overworld_glitch_connections
from .UnderworldGlitchRules import underworld_glitch_connections
from .Regions import mark_light_world_regions
from .InvertedRegions import mark_dark_world_regions


def link_entrances(world, player):
    connect_two_way(world, 'Links House', 'Links House Exit', player) # unshuffled. For now
    connect_exit(world, 'Chris Houlihan Room Exit', 'Links House', player) # should always match link's house, except for plandos

    Dungeon_Exits = Dungeon_Exits_Base.copy()
    Cave_Exits = Cave_Exits_Base.copy()
    Old_Man_House = Old_Man_House_Base.copy()
    Cave_Three_Exits = Cave_Three_Exits_Base.copy()

    unbias_some_entrances(world, Dungeon_Exits, Cave_Exits, Old_Man_House, Cave_Three_Exits)

    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname, player)

    # if we do not shuffle, set default connections
    if world.entrance_shuffle[player] == 'vanilla':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname, player)
        for exitname, regionname in default_dungeon_connections:
            connect_simple(world, exitname, regionname, player)
    elif world.entrance_shuffle[player] == 'dungeons_simple':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname, player)

        simple_shuffle_dungeons(world, player)
    elif world.entrance_shuffle[player] == 'dungeons_full':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname, player)

        skull_woods_shuffle(world, player)

        dungeon_exits = list(Dungeon_Exits)
        lw_entrances = list(LW_Dungeon_Entrances)
        dw_entrances = list(DW_Dungeon_Entrances)

        if world.mode[player] == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
        else:
            dungeon_exits.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit', player)
        else:
            dw_entrances.append('Ganons Tower')
            dungeon_exits.append('Ganons Tower Exit')

        if world.mode[player] == 'standard':
            # rest of hyrule castle must be in light world, so it has to be the one connected to east exit of desert
            hyrule_castle_exits = [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')]
            connect_mandatory_exits(world, lw_entrances, hyrule_castle_exits, list(LW_Dungeon_Entrances_Must_Exit), player)
            connect_caves(world, lw_entrances, [], hyrule_castle_exits, player)
        else:
            connect_mandatory_exits(world, lw_entrances, dungeon_exits, list(LW_Dungeon_Entrances_Must_Exit), player)
        connect_mandatory_exits(world, dw_entrances, dungeon_exits, list(DW_Dungeon_Entrances_Must_Exit), player)
        connect_caves(world, lw_entrances, dw_entrances, dungeon_exits, player)
    elif world.entrance_shuffle[player] == 'dungeons_crossed':
        crossed_shuffle_dungeons(world, player)
    elif world.entrance_shuffle[player] == 'simple':
        simple_shuffle_dungeons(world, player)

        old_man_entrances = list(Old_Man_Entrances)
        caves = list(Cave_Exits)
        three_exit_caves = list(Cave_Three_Exits)

        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # we shuffle all 2 entrance caves as pairs as a start
        # start with the ones that need to be directed
        two_door_caves = list(Two_Door_Caves_Directional)
        world.random.shuffle(two_door_caves)
        world.random.shuffle(caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1, player)
            connect_two_way(world, entrance2, exit2, player)

        # now the remaining pairs
        two_door_caves = list(Two_Door_Caves)
        world.random.shuffle(two_door_caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1, player)
            connect_two_way(world, entrance2, exit2, player)

        # at this point only Light World death mountain entrances remain
        # place old man, has limited options
        remaining_entrances = ['Old Man Cave (West)', 'Old Man House (Bottom)', 'Death Mountain Return Cave (West)', 'Paradox Cave (Bottom)', 'Paradox Cave (Middle)', 'Paradox Cave (Top)',
                               'Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave (Top)', 'Spiral Cave', 'Spiral Cave (Bottom)']
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        remaining_entrances.extend(old_man_entrances)
        world.random.shuffle(remaining_entrances)
        old_man_entrance = remaining_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)

        # add old man house to ensure it is always somewhere on light death mountain
        caves.extend(list(Old_Man_House))
        caves.extend(list(three_exit_caves))

        # connect rest
        connect_caves(world, remaining_entrances, [], caves, player)

        # scramble holes
        scramble_holes(world, player)

        # place blacksmith, has limited options
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        # place remaining doors
        connect_doors(world, single_doors, door_targets, player)
    elif world.entrance_shuffle[player] == 'restricted':
        simple_shuffle_dungeons(world, player)

        lw_entrances = list(LW_Entrances + LW_Single_Cave_Doors + Old_Man_Entrances)
        dw_entrances = list(DW_Entrances + DW_Single_Cave_Doors)
        dw_must_exits = list(DW_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances)
        caves = list(Cave_Exits + Cave_Three_Exits)

        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors + Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Blacksmith_Multi_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        # in restricted, the only mandatory exits are in dark world
        connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits, player)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in lw_entrances]
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)
        lw_entrances.remove(old_man_exit)

        # place blacksmith, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in all_entrances]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        if blacksmith_hut in lw_entrances:
            lw_entrances.remove(blacksmith_hut)
        if blacksmith_hut in dw_entrances:
            dw_entrances.remove(blacksmith_hut)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in all_entrances]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
        if bomb_shop in lw_entrances:
            lw_entrances.remove(bomb_shop)
        if bomb_shop in dw_entrances:
            dw_entrances.remove(bomb_shop)

        # place the old man cave's entrance somewhere in the light world
        world.random.shuffle(lw_entrances)
        old_man_entrance = lw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)

        # place Old Man House in Light World
        connect_caves(world, lw_entrances, [], list(Old_Man_House), player) #for multiple seeds


        # now scramble the rest
        connect_caves(world, lw_entrances, dw_entrances, caves, player)

        # scramble holes
        scramble_holes(world, player)

        doors = lw_entrances + dw_entrances

        # place remaining doors
        connect_doors(world, doors, door_targets, player)

    elif world.entrance_shuffle[player] == 'full':
        skull_woods_shuffle(world, player)

        lw_entrances = list(LW_Entrances + LW_Dungeon_Entrances + LW_Single_Cave_Doors + Old_Man_Entrances)
        dw_entrances = list(DW_Entrances + DW_Dungeon_Entrances + DW_Single_Cave_Doors)
        dw_must_exits = list(DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit)
        lw_must_exits = list(LW_Dungeon_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances + ['Tower of Hera'])
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits)  # don't need to consider three exit caves, have one exit caves to avoid parity issues
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors + Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Blacksmith_Multi_Cave_Doors)
        door_targets = list(Single_Cave_Targets)
        old_man_house = list(Old_Man_House)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        if world.mode[player] == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
        else:
            caves.append(tuple(world.random.sample(
                ['Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'], 3)))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit', player)
        else:
            dw_entrances.append('Ganons Tower')
            caves.append('Ganons Tower Exit')
        

        # we randomize which world requirements we fulfill first so we get better dungeon distribution
        #we also places the Old Man House at this time to make sure he can be connected to the desert one way
        if world.random.randint(0, 1) == 0:
            caves += old_man_house
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits, player)
            try:
                caves.remove(old_man_house[0])
            except ValueError:
                pass
            else:  # if the cave wasn't placed we get here
                connect_caves(world, lw_entrances, [], old_man_house, player)
            connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits, player)
        else:
            connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits, player)
            caves += old_man_house
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits, player)
            try:
                caves.remove(old_man_house[0])
            except ValueError:
                pass
            else: #if the cave wasn't placed we get here
                connect_caves(world, lw_entrances, [], old_man_house, player)
        if world.mode[player] == 'standard':
            # rest of hyrule castle must be in light world
            connect_caves(world, lw_entrances, [], [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')], player)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in lw_entrances]
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)
        lw_entrances.remove(old_man_exit)

        # place blacksmith, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in all_entrances]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        if blacksmith_hut in lw_entrances:
            lw_entrances.remove(blacksmith_hut)
        if blacksmith_hut in dw_entrances:
            dw_entrances.remove(blacksmith_hut)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in all_entrances]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
        if bomb_shop in lw_entrances:
            lw_entrances.remove(bomb_shop)
        if bomb_shop in dw_entrances:
            dw_entrances.remove(bomb_shop)

        # place the old man cave's entrance somewhere in the light world
        old_man_entrance = lw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)


        # now scramble the rest
        connect_caves(world, lw_entrances, dw_entrances, caves, player)

        # scramble holes
        scramble_holes(world, player)

        doors = lw_entrances + dw_entrances

        # place remaining doors
        connect_doors(world, doors, door_targets, player)
    elif world.entrance_shuffle[player] == 'crossed':
        skull_woods_shuffle(world, player)

        entrances = list(LW_Entrances + LW_Dungeon_Entrances + LW_Single_Cave_Doors + Old_Man_Entrances + DW_Entrances + DW_Dungeon_Entrances + DW_Single_Cave_Doors)
        must_exits = list(DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + LW_Dungeon_Entrances_Must_Exit)

        old_man_entrances = list(Old_Man_Entrances + ['Tower of Hera'])
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits + Old_Man_House)  # don't need to consider three exit caves, have one exit caves to avoid parity issues
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors + Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Blacksmith_Multi_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        if world.mode[player] == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
        else:
            caves.append(tuple(world.random.sample(
                ['Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'], 3)))
            entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit', player)
        else:
            entrances.append('Ganons Tower')
            caves.append('Ganons Tower Exit')

        #place must-exit caves 
        connect_mandatory_exits(world, entrances, caves, must_exits, player)

        if world.mode[player] == 'standard':
            # rest of hyrule castle must be dealt with
            connect_caves(world, entrances, [], [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')], player)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in entrances]
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)
        entrances.remove(old_man_exit)

        # place blacksmith, has limited options
        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in entrances]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        entrances.remove(blacksmith_hut)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options

        # cannot place it anywhere already taken (or that are otherwise not eligable for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in entrances]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
        entrances.remove(bomb_shop)


        # place the old man cave's entrance somewhere
        world.random.shuffle(entrances)
        old_man_entrance = entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)


        # now scramble the rest
        connect_caves(world, entrances, [], caves, player)

        # scramble holes
        scramble_holes(world, player)

        # place remaining doors
        connect_doors(world, entrances, door_targets, player)

    elif world.entrance_shuffle[player] == 'insanity':
        # beware ye who enter here

        entrances = LW_Entrances + LW_Dungeon_Entrances + DW_Entrances + DW_Dungeon_Entrances + Old_Man_Entrances + ['Skull Woods Second Section Door (East)', 'Skull Woods First Section Door', 'Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave']
        entrances_must_exits = DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + LW_Dungeon_Entrances_Must_Exit + ['Skull Woods Second Section Door (West)']

        doors = LW_Entrances + LW_Dungeon_Entrances + LW_Dungeon_Entrances_Must_Exit + ['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave'] + Old_Man_Entrances +\
                DW_Entrances + DW_Dungeon_Entrances + DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)'] +\
                LW_Single_Cave_Doors + DW_Single_Cave_Doors

        # TODO: there are other possible entrances we could support here by way of exiting from a connector,
        # and rentering to find bomb shop. However appended list here is all those that we currently have
        # bomb shop logic for.
        # Specifically we could potentially add: 'Dark Death Mountain Ledge (East)' and doors associated with pits
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors + Bomb_Shop_Multi_Cave_Doors+['Desert Palace Entrance (East)', 'Turtle Rock Isolated Ledge Entrance', 'Bumper Cave (Top)', 'Hookshot Cave Back Entrance'])
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Blacksmith_Multi_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        world.random.shuffle(doors)

        old_man_entrances = list(Old_Man_Entrances) + ['Tower of Hera']

        caves = Cave_Exits + Dungeon_Exits + Cave_Three_Exits + ['Old Man House Exit (Bottom)', 'Old Man House Exit (Top)', 'Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)',
                                                                 'Kakariko Well Exit', 'Bat Cave Exit', 'North Fairy Cave Exit', 'Lost Woods Hideout Exit', 'Lumberjack Tree Exit', 'Sanctuary Exit']


        # shuffle up holes

        hole_entrances = ['Kakariko Well Drop', 'Bat Cave Drop', 'North Fairy Cave Drop', 'Lost Woods Hideout Drop', 'Lumberjack Tree Tree', 'Sanctuary Grave',
                          'Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole']

        hole_targets = ['Kakariko Well (top)', 'Bat Cave (right)', 'North Fairy Cave', 'Lost Woods Hideout (top)', 'Lumberjack Tree (top)', 'Sewer Drop', 'Skull Woods Second Section (Drop)',
                        'Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)']

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        if world.mode[player] == 'standard':
            # cannot move uncle cave
            connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance', player)
            connect_exit(world, 'Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance Stairs', player)
            connect_entrance(world, 'Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Exit', player)
        else:
            hole_entrances.append('Hyrule Castle Secret Entrance Drop')
            hole_targets.append('Hyrule Castle Secret Entrance')
            doors.append('Hyrule Castle Secret Entrance Stairs')
            entrances.append('Hyrule Castle Secret Entrance Stairs')
            caves.append('Hyrule Castle Secret Entrance Exit')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit', player)
            connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit', player)
            connect_entrance(world, 'Pyramid Hole', 'Pyramid', player)
        else:
            entrances.append('Ganons Tower')
            caves.extend(['Ganons Tower Exit', 'Pyramid Exit'])
            hole_entrances.append('Pyramid Hole')
            hole_targets.append('Pyramid')
            entrances_must_exits.append('Pyramid Entrance')
            doors.extend(['Ganons Tower', 'Pyramid Entrance'])

        world.random.shuffle(hole_entrances)
        world.random.shuffle(hole_targets)
        world.random.shuffle(entrances)

        # fill up holes
        for hole in hole_entrances:
            connect_entrance(world, hole, hole_targets.pop(), player)

        # hyrule castle handling
        if world.mode[player] == 'standard':
            # must connect front of hyrule castle to do escape
            connect_entrance(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
            connect_exit(world, 'Hyrule Castle Exit (South)', 'Hyrule Castle Entrance (South)', player)
            caves.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            doors.append('Hyrule Castle Entrance (South)')
            entrances.append('Hyrule Castle Entrance (South)')
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))

        # now let's deal with mandatory reachable stuff
        def extract_reachable_exit(cavelist):
            world.random.shuffle(cavelist)
            candidate = None
            for cave in cavelist:
                if isinstance(cave, tuple) and len(cave) > 1:
                    # special handling: TRock has two entries that we should consider entrance only
                    # ToDo this should be handled in a more sensible manner
                    if cave[0] in ['Turtle Rock Exit (Front)', 'Spectacle Rock Cave Exit (Peak)'] and len(cave) == 2:
                        continue
                    candidate = cave
                    break
            if candidate is None:
                raise KeyError('No suitable cave.')
            cavelist.remove(candidate)
            return candidate

        def connect_reachable_exit(entrance, caves, doors):
            cave = extract_reachable_exit(caves)

            exit = cave[-1]
            cave = cave[:-1]
            connect_exit(world, exit, entrance, player)
            connect_entrance(world, doors.pop(), exit, player)
            # rest of cave now is forced to be in this world
            caves.append(cave)

        # connect mandatory exits
        for entrance in entrances_must_exits:
            connect_reachable_exit(entrance, caves, doors)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [entrance for entrance in old_man_entrances if entrance in entrances]
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        entrances.remove(old_man_exit)

        connect_exit(world, 'Old Man Cave Exit (East)', old_man_exit, player)
        connect_entrance(world, doors.pop(), 'Old Man Cave Exit (East)', player)
        caves.append('Old Man Cave Exit (West)')

        # place blacksmith, has limited options
        blacksmith_doors = [door for door in blacksmith_doors if door in doors]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        doors.remove(blacksmith_hut)

        # place dam and pyramid fairy, have limited options
        bomb_shop_doors = [door for door in bomb_shop_doors if door in doors]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
        doors.remove(bomb_shop)

        # handle remaining caves
        for cave in caves:
            if isinstance(cave, str):
                cave = (cave,)

            for exit in cave:
                connect_exit(world, exit, entrances.pop(), player)
                connect_entrance(world, doors.pop(), exit, player)

        # place remaining doors
        connect_doors(world, doors, door_targets, player)

    else:
        raise NotImplementedError(
            f'{world.entrance_shuffle[player]} Shuffling not supported yet. Player {world.get_player_name(player)}')

    if world.glitches_required[player] in ['overworld_glitches', 'hybrid_major_glitches', 'no_logic']:
        overworld_glitch_connections(world, player)
        # mandatory hybrid major glitches connections
        if world.glitches_required[player] in ['hybrid_major_glitches', 'no_logic']:
            underworld_glitch_connections(world, player)

    # check for swamp palace fix
    if world.get_entrance('Dam', player).connected_region.name != 'Dam' or world.get_entrance('Swamp Palace', player).connected_region.name != 'Swamp Palace (Entrance)':
        world.worlds[player].swamp_patch_required = True

    # check for potion shop location
    if world.get_entrance('Potion Shop', player).connected_region.name != 'Potion Shop':
        world.worlds[player].powder_patch_required = True

    # check for ganon location
    if world.get_entrance('Pyramid Hole', player).connected_region.name != 'Pyramid':
        world.worlds[player].ganon_at_pyramid = False

    # check for Ganon's Tower location
    if world.get_entrance('Ganons Tower', player).connected_region.name != 'Ganons Tower (Entrance)':
        world.worlds[player].ganonstower_vanilla = False


def link_inverted_entrances(world, player):
    # Link's house shuffled freely, Houlihan set in mandatory_connections 

    Dungeon_Exits = Inverted_Dungeon_Exits_Base.copy()
    Cave_Exits = Cave_Exits_Base.copy()
    Old_Man_House = Old_Man_House_Base.copy()
    Cave_Three_Exits = Cave_Three_Exits_Base.copy()

    unbias_some_entrances(world, Dungeon_Exits, Cave_Exits, Old_Man_House, Cave_Three_Exits)

    # setup mandatory connections
    for exitname, regionname in inverted_mandatory_connections:
        connect_simple(world, exitname, regionname, player)

    # if we do not shuffle, set default connections
    if world.entrance_shuffle[player] == 'vanilla':
        for exitname, regionname in inverted_default_connections:
            connect_simple(world, exitname, regionname, player)
        for exitname, regionname in inverted_default_dungeon_connections:
            connect_simple(world, exitname, regionname, player)
    elif world.entrance_shuffle[player] == 'dungeons_simple':
        for exitname, regionname in inverted_default_connections:
            connect_simple(world, exitname, regionname, player)

        simple_shuffle_dungeons(world, player)
    elif world.entrance_shuffle[player] == 'dungeons_full':
        for exitname, regionname in inverted_default_connections:
            connect_simple(world, exitname, regionname, player)

        skull_woods_shuffle(world, player)

        dungeon_exits = list(Dungeon_Exits)
        lw_entrances = list(Inverted_LW_Dungeon_Entrances)
        lw_dungeon_entrances_must_exit = list(Inverted_LW_Dungeon_Entrances_Must_Exit)
        dw_entrances = list(Inverted_DW_Dungeon_Entrances)

        # randomize which desert ledge door is a must-exit
        if world.random.randint(0, 1):
            lw_dungeon_entrances_must_exit.append('Desert Palace Entrance (North)')
            lw_entrances.append('Desert Palace Entrance (West)')
        else:
            lw_dungeon_entrances_must_exit.append('Desert Palace Entrance (West)')
            lw_entrances.append('Desert Palace Entrance (North)')
        
        dungeon_exits.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        lw_entrances.append('Hyrule Castle Entrance (South)')
        
        if not world.shuffle_ganon:
            connect_two_way(world, 'Inverted Ganons Tower', 'Inverted Ganons Tower Exit', player)
            hc_ledge_entrances = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)']
        else:
            lw_entrances.append('Inverted Ganons Tower')
            dungeon_exits.append('Inverted Ganons Tower Exit')
            hc_ledge_entrances = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)', 'Inverted Ganons Tower']
        
        # shuffle aga door first. If it's on HC ledge, remaining HC ledge door must be must-exit
        all_entrances_aga = lw_entrances + dw_entrances
        aga_doors = [i for i in all_entrances_aga]
        world.random.shuffle(aga_doors)
        aga_door = aga_doors.pop()
        
        if aga_door in hc_ledge_entrances:
            lw_entrances.remove(aga_door)
            hc_ledge_entrances.remove(aga_door)

            world.random.shuffle(hc_ledge_entrances)
            hc_ledge_must_exit = hc_ledge_entrances.pop()
            lw_entrances.remove(hc_ledge_must_exit)
            lw_dungeon_entrances_must_exit.append(hc_ledge_must_exit)
        elif aga_door in lw_entrances:
            lw_entrances.remove(aga_door)
        else:
            dw_entrances.remove(aga_door)

        connect_two_way(world, aga_door, 'Inverted Agahnims Tower Exit', player)
        dungeon_exits.remove('Inverted Agahnims Tower Exit')

        connect_mandatory_exits(world, lw_entrances, dungeon_exits, lw_dungeon_entrances_must_exit, player)

        connect_caves(world, lw_entrances, dw_entrances, dungeon_exits, player)
    elif world.entrance_shuffle[player] == 'dungeons_crossed':
        inverted_crossed_shuffle_dungeons(world, player)
    elif world.entrance_shuffle[player] == 'simple':
        simple_shuffle_dungeons(world, player)

        old_man_entrances = list(Inverted_Old_Man_Entrances)
        caves = list(Cave_Exits)
        three_exit_caves = list(Cave_Three_Exits)

        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Inverted_Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Inverted_Single_Cave_Targets)

        # we shuffle all 2 entrance caves as pairs as a start
        # start with the ones that need to be directed
        two_door_caves = list(Inverted_Two_Door_Caves_Directional)
        world.random.shuffle(two_door_caves)
        world.random.shuffle(caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1, player)
            connect_two_way(world, entrance2, exit2, player)

        # now the remaining pairs
        two_door_caves = list(Inverted_Two_Door_Caves)
        world.random.shuffle(two_door_caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1, player)
            connect_two_way(world, entrance2, exit2, player)
        
        # place links house
        links_house_doors = [i for i in bomb_shop_doors + blacksmith_doors if
                             i not in Inverted_Dark_Sanctuary_Doors + Isolated_LH_Doors]
        links_house = world.random.choice(list(links_house_doors))
        connect_two_way(world, links_house, 'Inverted Links House Exit', player)
        if links_house in bomb_shop_doors:
            bomb_shop_doors.remove(links_house)
        if links_house in blacksmith_doors:
            blacksmith_doors.remove(links_house)
        if links_house in old_man_entrances:
            old_man_entrances.remove(links_house)

        # place dark sanc
        sanc_doors = [door for door in Inverted_Dark_Sanctuary_Doors if door in bomb_shop_doors]
        sanc_door = world.random.choice(sanc_doors)
        bomb_shop_doors.remove(sanc_door)

        connect_entrance(world, sanc_door, 'Inverted Dark Sanctuary', player)
        world.get_entrance('Inverted Dark Sanctuary Exit', player).connect(world.get_entrance(sanc_door, player).parent_region)
        
        lw_dm_entrances = ['Paradox Cave (Bottom)', 'Paradox Cave (Middle)', 'Paradox Cave (Top)', 'Old Man House (Bottom)',
                           'Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave (Top)', 'Spiral Cave (Bottom)', 'Old Man Cave (East)',
                           'Death Mountain Return Cave (East)', 'Spiral Cave', 'Old Man House (Top)', 'Spectacle Rock Cave', 
                           'Spectacle Rock Cave Peak', 'Spectacle Rock Cave (Bottom)']
        
        # place old man, bumper cave bottom to DDM entrances not in east bottom

        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, 'Bumper Cave (Bottom)', 'Old Man Cave Exit (West)', player)
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)
        if old_man_exit == 'Spike Cave':
            bomb_shop_doors.remove('Spike Cave')
            bomb_shop_doors.extend(old_man_entrances)

        # add old man house to ensure it is always somewhere on light death mountain
        caves.extend(list(Old_Man_House))
        caves.extend(list(three_exit_caves))

        # connect rest
        connect_caves(world, lw_dm_entrances, [], caves, player)
        
        # scramble holes
        scramble_inverted_holes(world, player)

        # place blacksmith, has limited options
        blacksmith_doors = [door for door in blacksmith_doors[:]]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        bomb_shop_doors = [door for door in bomb_shop_doors[:]]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Inverted Big Bomb Shop', player)
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        # place remaining doors
        connect_doors(world, single_doors, door_targets, player)
    
    elif world.entrance_shuffle[player] == 'restricted':
        simple_shuffle_dungeons(world, player)

        lw_entrances = list(Inverted_LW_Entrances + Inverted_LW_Single_Cave_Doors)
        dw_entrances = list(Inverted_DW_Entrances + Inverted_DW_Single_Cave_Doors + Inverted_Old_Man_Entrances)
        lw_must_exits = list(Inverted_LW_Entrances_Must_Exit)
        old_man_entrances = list(Inverted_Old_Man_Entrances)
        caves = list(Cave_Exits + Cave_Three_Exits + Old_Man_House)
        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Inverted_Bomb_Shop_Single_Cave_Doors + Inverted_Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Inverted_Blacksmith_Multi_Cave_Doors)
        door_targets = list(Inverted_Single_Cave_Targets)

        # place links house
        links_house_doors = [i for i in lw_entrances + dw_entrances + lw_must_exits if
                             i not in Inverted_Dark_Sanctuary_Doors + Isolated_LH_Doors]
        links_house = world.random.choice(list(links_house_doors))
        connect_two_way(world, links_house, 'Inverted Links House Exit', player)
        if links_house in lw_entrances:
            lw_entrances.remove(links_house)
        elif links_house in dw_entrances:
            dw_entrances.remove(links_house)
        elif links_house in lw_must_exits:
            lw_must_exits.remove(links_house)

        # place dark sanc
        sanc_doors = [door for door in Inverted_Dark_Sanctuary_Doors if door in dw_entrances]
        sanc_door = world.random.choice(sanc_doors)
        dw_entrances.remove(sanc_door)
        connect_entrance(world, sanc_door, 'Inverted Dark Sanctuary', player)
        world.get_entrance('Inverted Dark Sanctuary Exit', player).connect(world.get_entrance(sanc_door, player).parent_region)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        # place must exits
        connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits, player)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in dw_entrances]
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)
        dw_entrances.remove(old_man_exit)

        # place blacksmith, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligible for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in all_entrances]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        if blacksmith_hut in lw_entrances:
            lw_entrances.remove(blacksmith_hut)
        if blacksmith_hut in dw_entrances:
            dw_entrances.remove(blacksmith_hut)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligible for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in all_entrances]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Inverted Big Bomb Shop', player)
        if bomb_shop in lw_entrances:
            lw_entrances.remove(bomb_shop)
        if bomb_shop in dw_entrances:
            dw_entrances.remove(bomb_shop)

        # place the old man cave's entrance somewhere in the dark world
        world.random.shuffle(dw_entrances)
        old_man_entrance = dw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)

        # now scramble the rest
        connect_caves(world, lw_entrances, dw_entrances, caves, player)

        # scramble holes
        scramble_inverted_holes(world, player)

        doors = lw_entrances + dw_entrances
        # place remaining doors
        connect_doors(world, doors, door_targets, player)
    elif world.entrance_shuffle[player] == 'full':
        skull_woods_shuffle(world, player)

        lw_entrances = list(Inverted_LW_Entrances + Inverted_LW_Dungeon_Entrances + Inverted_LW_Single_Cave_Doors)
        dw_entrances = list(Inverted_DW_Entrances + Inverted_DW_Dungeon_Entrances + Inverted_DW_Single_Cave_Doors + Inverted_Old_Man_Entrances)
        lw_must_exits = list(Inverted_LW_Dungeon_Entrances_Must_Exit + Inverted_LW_Entrances_Must_Exit)
        old_man_entrances = list(Inverted_Old_Man_Entrances + Old_Man_Entrances + ['Inverted Agahnims Tower', 'Tower of Hera'])
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits)  # don't need to consider three exit caves, have one exit caves to avoid parity issues
        bomb_shop_doors = list(Inverted_Bomb_Shop_Single_Cave_Doors + Inverted_Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Inverted_Blacksmith_Multi_Cave_Doors)
        door_targets = list(Inverted_Single_Cave_Targets)
        old_man_house = list(Old_Man_House)

        # randomize which desert ledge door is a must-exit
        if world.random.randint(0, 1) == 0:
            lw_must_exits.append('Desert Palace Entrance (North)')
            lw_entrances.append('Desert Palace Entrance (West)')
        else:
            lw_must_exits.append('Desert Palace Entrance (West)')
            lw_entrances.append('Desert Palace Entrance (North)')

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        lw_entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Inverted Ganons Tower', 'Inverted Ganons Tower Exit', player)
            hc_ledge_entrances = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)']
        else:
            lw_entrances.append('Inverted Ganons Tower')
            caves.append('Inverted Ganons Tower Exit')
            hc_ledge_entrances = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)', 'Inverted Ganons Tower']

        # shuffle aga door first. if it's on hc ledge, then one other hc ledge door has to be must_exit
        all_entrances_aga = lw_entrances + dw_entrances
        aga_doors = [i for i in all_entrances_aga]
        world.random.shuffle(aga_doors)
        aga_door = aga_doors.pop()

        if aga_door in hc_ledge_entrances:
            lw_entrances.remove(aga_door)
            hc_ledge_entrances.remove(aga_door)

            world.random.shuffle(hc_ledge_entrances)
            hc_ledge_must_exit = hc_ledge_entrances.pop()
            lw_entrances.remove(hc_ledge_must_exit)
            lw_must_exits.append(hc_ledge_must_exit)
        elif aga_door in lw_entrances:
            lw_entrances.remove(aga_door)
        else:
            dw_entrances.remove(aga_door)

        connect_two_way(world, aga_door, 'Inverted Agahnims Tower Exit', player)
        caves.remove('Inverted Agahnims Tower Exit')

        # place links house
        links_house_doors = [i for i in lw_entrances + dw_entrances + lw_must_exits if
                             i not in Inverted_Dark_Sanctuary_Doors + Isolated_LH_Doors]
        links_house = world.random.choice(list(links_house_doors))
        connect_two_way(world, links_house, 'Inverted Links House Exit', player)
        if links_house in lw_entrances:
            lw_entrances.remove(links_house)
        if links_house in dw_entrances:
            dw_entrances.remove(links_house)
        if links_house in lw_must_exits:
            lw_must_exits.remove(links_house)

        # place dark sanc
        sanc_doors = [door for door in Inverted_Dark_Sanctuary_Doors if door in dw_entrances]
        sanc_door = world.random.choice(sanc_doors)
        dw_entrances.remove(sanc_door)
        connect_entrance(world, sanc_door, 'Inverted Dark Sanctuary', player)
        world.get_entrance('Inverted Dark Sanctuary Exit', player).connect(world.get_entrance(sanc_door, player).parent_region)
        
        # place old man house
        # no dw must exits in inverted, but we randomize whether cave is in light or dark world
        if world.random.randint(0, 1) == 0:
            caves += old_man_house
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits, player)
            try:
                caves.remove(old_man_house[0])
            except ValueError:
                pass
            else:  # if the cave wasn't placed we get here
                connect_caves(world, lw_entrances, [], old_man_house, player)
        else:
            connect_caves(world, dw_entrances, [], old_man_house, player)
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits, player)

        # put all HC exits in LW in inverted full shuffle
        connect_caves(world, lw_entrances, [], [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)', 'Hyrule Castle Exit (South)')], player)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in dw_entrances + lw_entrances]
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)
        if old_man_exit in dw_entrances:
            dw_entrances.remove(old_man_exit)
            old_man_world = 'dark'
        elif old_man_exit in lw_entrances:
            lw_entrances.remove(old_man_exit)
            old_man_world = 'light'

        # place blacksmith, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligible for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in all_entrances]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        if blacksmith_hut in lw_entrances:
            lw_entrances.remove(blacksmith_hut)
        if blacksmith_hut in dw_entrances:
            dw_entrances.remove(blacksmith_hut)
        bomb_shop_doors.extend(blacksmith_doors)

        # place bomb shop, has limited options
        all_entrances = lw_entrances + dw_entrances
        # cannot place it anywhere already taken (or that are otherwise not eligible for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in all_entrances]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Inverted Big Bomb Shop', player)
        if bomb_shop in lw_entrances:
            lw_entrances.remove(bomb_shop)
        if bomb_shop in dw_entrances:
            dw_entrances.remove(bomb_shop)

        # place the old man cave's entrance somewhere in the same world he'll exit from
        if old_man_world == 'light':
            world.random.shuffle(lw_entrances)
            old_man_entrance = lw_entrances.pop()
            connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)
        elif old_man_world == 'dark':
            world.random.shuffle(dw_entrances)
            old_man_entrance = dw_entrances.pop()
            connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)
        
        # now scramble the rest
        connect_caves(world, lw_entrances, dw_entrances, caves, player)

        # scramble holes
        scramble_inverted_holes(world, player)

        doors = lw_entrances + dw_entrances

        # place remaining doors
        connect_doors(world, doors, door_targets, player)
    elif world.entrance_shuffle[player] == 'crossed':
        skull_woods_shuffle(world, player)

        entrances = list(Inverted_LW_Entrances + Inverted_LW_Dungeon_Entrances + Inverted_LW_Single_Cave_Doors + Inverted_Old_Man_Entrances + Inverted_DW_Entrances + Inverted_DW_Dungeon_Entrances + Inverted_DW_Single_Cave_Doors)
        must_exits = list(Inverted_LW_Entrances_Must_Exit + Inverted_LW_Dungeon_Entrances_Must_Exit)

        old_man_entrances = list(Inverted_Old_Man_Entrances + Old_Man_Entrances + ['Inverted Agahnims Tower', 'Tower of Hera'])
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits + Old_Man_House)  # don't need to consider three exit caves, have one exit caves to avoid parity issues
        bomb_shop_doors = list(Inverted_Bomb_Shop_Single_Cave_Doors + Inverted_Bomb_Shop_Multi_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Inverted_Blacksmith_Multi_Cave_Doors)
        door_targets = list(Inverted_Single_Cave_Targets)

        # randomize which desert ledge door is a must-exit
        if world.random.randint(0, 1) == 0:
            must_exits.append('Desert Palace Entrance (North)')
            entrances.append('Desert Palace Entrance (West)')
        else:
            must_exits.append('Desert Palace Entrance (West)')
            entrances.append('Desert Palace Entrance (North)')

        caves.append(tuple(world.random.sample(
            ['Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'], 3)))
        entrances.append('Hyrule Castle Entrance (South)')
        
        if not world.shuffle_ganon:
            connect_two_way(world, 'Inverted Ganons Tower', 'Inverted Ganons Tower Exit', player)
            hc_ledge_entrances = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)']
        else:
            entrances.append('Inverted Ganons Tower')
            caves.append('Inverted Ganons Tower Exit')
            hc_ledge_entrances = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)', 'Inverted Ganons Tower']

        # shuffle aga door. if it's on hc ledge, then one other hc ledge door has to be must_exit
        aga_door = world.random.choice(list(entrances))
        
        if aga_door in hc_ledge_entrances:
            hc_ledge_entrances.remove(aga_door)

            world.random.shuffle(hc_ledge_entrances)
            hc_ledge_must_exit = hc_ledge_entrances.pop()
            entrances.remove(hc_ledge_must_exit)
            must_exits.append(hc_ledge_must_exit)

        entrances.remove(aga_door)
        connect_two_way(world, aga_door, 'Inverted Agahnims Tower Exit', player)
        caves.remove('Inverted Agahnims Tower Exit')


        # place links house
        links_house_doors = [i for i in entrances + must_exits if
                             i not in Inverted_Dark_Sanctuary_Doors + Isolated_LH_Doors]
        links_house = world.random.choice(list(links_house_doors))
        connect_two_way(world, links_house, 'Inverted Links House Exit', player)
        if links_house in entrances:
            entrances.remove(links_house)
        elif links_house in must_exits:
            must_exits.remove(links_house)

        # place dark sanc
        sanc_doors = [door for door in Inverted_Dark_Sanctuary_Doors if door in entrances]
        sanc_door = world.random.choice(sanc_doors)
        entrances.remove(sanc_door)
        connect_entrance(world, sanc_door, 'Inverted Dark Sanctuary', player)
        world.get_entrance('Inverted Dark Sanctuary Exit', player).connect(world.get_entrance(sanc_door, player).parent_region)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        
        #place must-exit caves 
        connect_mandatory_exits(world, entrances, caves, must_exits, player)


        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [door for door in old_man_entrances if door in entrances]
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)
        entrances.remove(old_man_exit)

        # place blacksmith, has limited options
        # cannot place it anywhere already taken (or that are otherwise not eligible for placement)
        blacksmith_doors = [door for door in blacksmith_doors if door in entrances]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        entrances.remove(blacksmith_hut)

        # place bomb shop, has limited options

        # cannot place it anywhere already taken (or that are otherwise not eligible for placement)
        bomb_shop_doors = [door for door in bomb_shop_doors if door in entrances]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Inverted Big Bomb Shop', player)
        entrances.remove(bomb_shop)
        
        # place the old man cave's entrance somewhere
        world.random.shuffle(entrances)
        old_man_entrance = entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)

        # now scramble the rest
        connect_caves(world, entrances, [], caves, player)

        # scramble holes
        scramble_inverted_holes(world, player)

        # place remaining doors
        connect_doors(world, entrances, door_targets, player)
    elif world.entrance_shuffle[player] == 'insanity':
        # beware ye who enter here

        entrances = Inverted_LW_Entrances + Inverted_LW_Dungeon_Entrances + Inverted_DW_Entrances + Inverted_DW_Dungeon_Entrances + Inverted_Old_Man_Entrances + Old_Man_Entrances + ['Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)', 'Skull Woods First Section Door', 'Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Entrance (South)']
        entrances_must_exits = Inverted_LW_Entrances_Must_Exit + Inverted_LW_Dungeon_Entrances_Must_Exit

        doors = Inverted_LW_Entrances + Inverted_LW_Dungeon_Entrances + Inverted_LW_Entrances_Must_Exit + Inverted_LW_Dungeon_Entrances_Must_Exit + ['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Secret Entrance Stairs'] + Inverted_Old_Man_Entrances +\
                Inverted_DW_Entrances + Inverted_DW_Dungeon_Entrances + ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)'] +\
                Inverted_LW_Single_Cave_Doors + Inverted_DW_Single_Cave_Doors + ['Desert Palace Entrance (West)', 'Desert Palace Entrance (North)']

        # randomize which desert ledge door is a must-exit
        if world.random.randint(0, 1) == 0:
            entrances_must_exits.append('Desert Palace Entrance (North)')
            entrances.append('Desert Palace Entrance (West)')
        else:
            entrances_must_exits.append('Desert Palace Entrance (West)')
            entrances.append('Desert Palace Entrance (North)')

        # TODO: there are other possible entrances we could support here by way of exiting from a connector,
        # and rentering to find bomb shop. However appended list here is all those that we currently have
        # bomb shop logic for.
        # Specifically we could potentially add: 'Dark Death Mountain Ledge (East)' and doors associated with pits
        bomb_shop_doors = list(Inverted_Bomb_Shop_Single_Cave_Doors + Inverted_Bomb_Shop_Multi_Cave_Doors + ['Turtle Rock Isolated Ledge Entrance', 'Hookshot Cave Back Entrance'])
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors + Inverted_Blacksmith_Multi_Cave_Doors)
        door_targets = list(Inverted_Single_Cave_Targets)

        world.random.shuffle(doors)

        old_man_entrances = list(Inverted_Old_Man_Entrances + Old_Man_Entrances) + ['Tower of Hera', 'Inverted Agahnims Tower']

        caves = Cave_Exits + Dungeon_Exits + Cave_Three_Exits + ['Old Man House Exit (Bottom)', 'Old Man House Exit (Top)', 'Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)',
                                                                 'Kakariko Well Exit', 'Bat Cave Exit', 'North Fairy Cave Exit', 'Lost Woods Hideout Exit', 'Lumberjack Tree Exit', 'Sanctuary Exit']


        # shuffle up holes
        hole_entrances = ['Kakariko Well Drop', 'Bat Cave Drop', 'North Fairy Cave Drop', 'Lost Woods Hideout Drop', 'Lumberjack Tree Tree', 'Sanctuary Grave',
                          'Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole']

        hole_targets = ['Kakariko Well (top)', 'Bat Cave (right)', 'North Fairy Cave', 'Lost Woods Hideout (top)', 'Lumberjack Tree (top)', 'Sewer Drop', 'Skull Woods Second Section (Drop)',
                        'Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)']

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'], player)

        hole_entrances.append('Hyrule Castle Secret Entrance Drop')
        hole_targets.append('Hyrule Castle Secret Entrance')
        entrances.append('Hyrule Castle Secret Entrance Stairs')
        caves.append('Hyrule Castle Secret Entrance Exit')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Inverted Ganons Tower', 'Inverted Ganons Tower Exit', player)
            connect_two_way(world, 'Inverted Pyramid Entrance', 'Pyramid Exit', player)
            connect_entrance(world, 'Inverted Pyramid Hole', 'Pyramid', player)
        else:
            entrances.append('Inverted Ganons Tower')
            caves.extend(['Inverted Ganons Tower Exit', 'Pyramid Exit'])
            hole_entrances.append('Inverted Pyramid Hole')
            hole_targets.append('Pyramid')
            doors.extend(['Inverted Ganons Tower', 'Inverted Pyramid Entrance'])

        world.random.shuffle(hole_entrances)
        world.random.shuffle(hole_targets)
        world.random.shuffle(entrances)

        # fill up holes
        for hole in hole_entrances:
            connect_entrance(world, hole, hole_targets.pop(), player)

        doors.append('Hyrule Castle Entrance (South)')
        caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))

        # place links house and dark sanc
        links_house_doors = [i for i in entrances + entrances_must_exits if
                             i not in Inverted_Dark_Sanctuary_Doors + Isolated_LH_Doors]
        links_house = world.random.choice(list(links_house_doors))
        connect_two_way(world, links_house, 'Inverted Links House Exit', player)
        if links_house in entrances:
            entrances.remove(links_house)
        elif links_house in entrances_must_exits:
            entrances_must_exits.remove(links_house)
        doors.remove(links_house)

        sanc_doors = [door for door in Inverted_Dark_Sanctuary_Doors if door in entrances]
        sanc_door = world.random.choice(sanc_doors)
        entrances.remove(sanc_door)
        doors.remove(sanc_door)
        connect_entrance(world, sanc_door, 'Inverted Dark Sanctuary', player)
        world.get_entrance('Inverted Dark Sanctuary Exit', player).connect(world.get_entrance(sanc_door, player).parent_region)

        # now let's deal with mandatory reachable stuff
        def extract_reachable_exit(cavelist):
            world.random.shuffle(cavelist)
            candidate = None
            for cave in cavelist:
                if isinstance(cave, tuple) and len(cave) > 1:
                    # special handling: TRock has two entries that we should consider entrance only
                    # ToDo this should be handled in a more sensible manner
                    if cave[0] in ['Turtle Rock Exit (Front)', 'Spectacle Rock Cave Exit (Peak)'] and len(cave) == 2:
                        continue
                    candidate = cave
                    break
            if candidate is None:
                raise KeyError('No suitable cave.')
            cavelist.remove(candidate)
            return candidate

        def connect_reachable_exit(entrance, caves, doors):
            cave = extract_reachable_exit(caves)

            exit = cave[-1]
            cave = cave[:-1]
            connect_exit(world, exit, entrance, player)
            connect_entrance(world, doors.pop(), exit, player)
            # rest of cave now is forced to be in this world
            caves.append(cave)

        # connect mandatory exits
        for entrance in entrances_must_exits:
            connect_reachable_exit(entrance, caves, doors)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        old_man_entrances = [entrance for entrance in old_man_entrances if entrance in entrances]
        world.random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        entrances.remove(old_man_exit)

        connect_exit(world, 'Old Man Cave Exit (East)', old_man_exit, player)
        connect_entrance(world, doors.pop(), 'Old Man Cave Exit (East)', player)
        caves.append('Old Man Cave Exit (West)')

        # place blacksmith, has limited options
        blacksmith_doors = [door for door in blacksmith_doors if door in doors]
        world.random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
        doors.remove(blacksmith_hut)

        # place dam and pyramid fairy, have limited options
        bomb_shop_doors = [door for door in bomb_shop_doors if door in doors]
        world.random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Inverted Big Bomb Shop', player)
        doors.remove(bomb_shop)

        # handle remaining caves
        for cave in caves:
            if isinstance(cave, str):
                cave = (cave,)

            for exit in cave:
                connect_exit(world, exit, entrances.pop(), player)
                connect_entrance(world, doors.pop(), exit, player)

        # place remaining doors
        connect_doors(world, doors, door_targets, player)
    else:
        raise NotImplementedError('Shuffling not supported yet')

    if world.glitches_required[player] in ['overworld_glitches', 'hybrid_major_glitches', 'no_logic']:
        overworld_glitch_connections(world, player)
        # mandatory hybrid major glitches connections
        if world.glitches_required[player] in ['hybrid_major_glitches', 'no_logic']:
            underworld_glitch_connections(world, player)

    # patch swamp drain
    if world.get_entrance('Dam', player).connected_region.name != 'Dam' or world.get_entrance('Swamp Palace', player).connected_region.name != 'Swamp Palace (Entrance)':
        world.worlds[player].swamp_patch_required = True

    # check for potion shop location
    if world.get_entrance('Potion Shop', player).connected_region.name != 'Potion Shop':
        world.worlds[player].powder_patch_required = True

    # check for ganon location
    if world.get_entrance('Inverted Pyramid Hole', player).connected_region.name != 'Pyramid':
        world.worlds[player].ganon_at_pyramid = False
   
    # check for Ganon's Tower location
    if world.get_entrance('Inverted Ganons Tower', player).connected_region.name != 'Ganons Tower (Entrance)':
        world.worlds[player].ganonstower_vanilla = False


def connect_simple(world, exitname, regionname, player):
    world.get_entrance(exitname, player).connect(world.get_region(regionname, player))


def connect_entrance(world, entrancename: str, exitname: str, player: int):
    entrance = world.get_entrance(entrancename, player)
    # check if we got an entrance or a region to connect to
    try:
        region = world.get_region(exitname, player)
        exit = None
    except KeyError:
        exit = world.get_entrance(exitname, player)
        region = exit.parent_region

    # if this was already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)

    target = exit_ids[exit.name][0] if exit is not None else exit_ids.get(region.name, None)
    addresses = door_addresses[entrance.name][0]

    entrance.connect(region, addresses, target)
    world.spoiler.set_entrance(entrance.name, exit.name if exit is not None else region.name, 'entrance', player)


def connect_exit(world, exitname, entrancename, player):
    entrance = world.get_entrance(entrancename, player)
    exit = world.get_entrance(exitname, player)

    # if this was already connected somewhere, remove the backreference
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    exit.connect(entrance.parent_region, door_addresses[entrance.name][1], exit_ids[exit.name][1])
    world.spoiler.set_entrance(entrance.name, exit.name, 'exit', player)


def connect_two_way(world, entrancename, exitname, player):
    entrance = world.get_entrance(entrancename, player)
    exit = world.get_entrance(exitname, player)

    # if these were already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    entrance.connect(exit.parent_region, door_addresses[entrance.name][0], exit_ids[exit.name][0])
    exit.connect(entrance.parent_region, door_addresses[entrance.name][1], exit_ids[exit.name][1])
    world.spoiler.set_entrance(entrance.name, exit.name, 'both', player)


def scramble_holes(world, player):
    hole_entrances = [('Kakariko Well Cave', 'Kakariko Well Drop'),
                      ('Bat Cave Cave', 'Bat Cave Drop'),
                      ('North Fairy Cave', 'North Fairy Cave Drop'),
                      ('Lost Woods Hideout Stump', 'Lost Woods Hideout Drop'),
                      ('Lumberjack Tree Cave', 'Lumberjack Tree Tree'),
                      ('Sanctuary', 'Sanctuary Grave')]

    hole_targets = [('Kakariko Well Exit', 'Kakariko Well (top)'),
                    ('Bat Cave Exit', 'Bat Cave (right)'),
                    ('North Fairy Cave Exit', 'North Fairy Cave'),
                    ('Lost Woods Hideout Exit', 'Lost Woods Hideout (top)'),
                    ('Lumberjack Tree Exit', 'Lumberjack Tree (top)')]

    if not world.shuffle_ganon:
        connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit', player)
        connect_entrance(world, 'Pyramid Hole', 'Pyramid', player)
    else:
        hole_targets.append(('Pyramid Exit', 'Pyramid'))

    if world.mode[player] == 'standard':
        # cannot move uncle cave
        connect_two_way(world, 'Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Exit', player)
        connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance', player)
    else:
        hole_entrances.append(('Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Drop'))
        hole_targets.append(('Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance'))

    # do not shuffle sanctuary into pyramid hole unless shuffle is crossed
    if world.entrance_shuffle[player] == 'crossed':
        hole_targets.append(('Sanctuary Exit', 'Sewer Drop'))
    if world.shuffle_ganon:
        world.random.shuffle(hole_targets)
        exit, target = hole_targets.pop()
        connect_two_way(world, 'Pyramid Entrance', exit, player)
        connect_entrance(world, 'Pyramid Hole', target, player)
    if world.entrance_shuffle[player] != 'crossed':
        hole_targets.append(('Sanctuary Exit', 'Sewer Drop'))

    world.random.shuffle(hole_targets)
    for entrance, drop in hole_entrances:
        exit, target = hole_targets.pop()
        connect_two_way(world, entrance, exit, player)
        connect_entrance(world, drop, target, player)


def scramble_inverted_holes(world, player):
    hole_entrances = [('Kakariko Well Cave', 'Kakariko Well Drop'),
                      ('Bat Cave Cave', 'Bat Cave Drop'),
                      ('North Fairy Cave', 'North Fairy Cave Drop'),
                      ('Lost Woods Hideout Stump', 'Lost Woods Hideout Drop'),
                      ('Lumberjack Tree Cave', 'Lumberjack Tree Tree'),
                      ('Sanctuary', 'Sanctuary Grave')]

    hole_targets = [('Kakariko Well Exit', 'Kakariko Well (top)'),
                    ('Bat Cave Exit', 'Bat Cave (right)'),
                    ('North Fairy Cave Exit', 'North Fairy Cave'),
                    ('Lost Woods Hideout Exit', 'Lost Woods Hideout (top)'),
                    ('Lumberjack Tree Exit', 'Lumberjack Tree (top)')]

    if not world.shuffle_ganon:
        connect_two_way(world, 'Inverted Pyramid Entrance', 'Pyramid Exit', player)
        connect_entrance(world, 'Inverted Pyramid Hole', 'Pyramid', player)
    else:
        hole_targets.append(('Pyramid Exit', 'Pyramid'))

    
    hole_entrances.append(('Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Drop'))
    hole_targets.append(('Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance'))

    # do not shuffle sanctuary into pyramid hole unless shuffle is crossed
    if world.entrance_shuffle[player] == 'crossed':
        hole_targets.append(('Sanctuary Exit', 'Sewer Drop'))
    if world.shuffle_ganon:
        world.random.shuffle(hole_targets)
        exit, target = hole_targets.pop()
        connect_two_way(world, 'Inverted Pyramid Entrance', exit, player)
        connect_entrance(world, 'Inverted Pyramid Hole', target, player)
    if world.entrance_shuffle[player] != 'crossed':
        hole_targets.append(('Sanctuary Exit', 'Sewer Drop'))

    world.random.shuffle(hole_targets)
    for entrance, drop in hole_entrances:
        exit, target = hole_targets.pop()
        connect_two_way(world, entrance, exit, player)
        connect_entrance(world, drop, target, player)

def connect_random(world, exitlist, targetlist, player, two_way=False):
    targetlist = list(targetlist)
    world.random.shuffle(targetlist)

    for exit, target in zip(exitlist, targetlist):
        if two_way:
            connect_two_way(world, exit, target, player)
        else:
            connect_entrance(world, exit, target, player)


def connect_mandatory_exits(world, entrances, caves, must_be_exits, player):

    # Keeps track of entrances that cannot be used to access each exit / cave
    if world.mode[player] == 'inverted':
        invalid_connections = Inverted_Must_Exit_Invalid_Connections.copy()
    else:
        invalid_connections = Must_Exit_Invalid_Connections.copy()
    invalid_cave_connections = defaultdict(set)

    if world.glitches_required[player] in ['overworld_glitches', 'hybrid_major_glitches', 'no_logic']:
        from . import OverworldGlitchRules
        for entrance in OverworldGlitchRules.get_non_mandatory_exits(world.mode[player] == 'inverted'):
            invalid_connections[entrance] = set()
            if entrance in must_be_exits:
                must_be_exits.remove(entrance)
                entrances.append(entrance)

    """This works inplace"""
    world.random.shuffle(entrances)
    world.random.shuffle(caves)

    # Handle inverted Aga Tower - if it depends on connections, then so does Hyrule Castle Ledge
    if world.mode[player] == 'inverted':
        for entrance in invalid_connections:
            if world.get_entrance(entrance, player).connected_region == world.get_region('Inverted Agahnims Tower',
                                                                                         player):
                for exit in invalid_connections[entrance]:
                    invalid_connections[exit] = invalid_connections[exit].union(
                        {'Inverted Ganons Tower', 'Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)'})
                break

    used_caves = []
    required_entrances = 0  # Number of entrances reserved for used_caves
    while must_be_exits:
        exit = must_be_exits.pop()
        # find multi exit cave
        cave = None
        for candidate in caves:
            if not isinstance(candidate, str) and (candidate in used_caves or len(candidate) < len(entrances) - required_entrances - 1):
                cave = candidate
                break

        if cave is None:
            raise KeyError('No more caves left. Should not happen!')

        # all caves are sorted so that the last exit is always reachable
        connect_two_way(world, exit, cave[-1], player)
        if len(cave) == 2:
            entrance = next(e for e in entrances[::-1] if e not in invalid_connections[exit] and e not in invalid_cave_connections[tuple(cave)])
            entrances.remove(entrance)
            connect_two_way(world, entrance, cave[0], player)
            if cave in used_caves:
                required_entrances -= 2
                used_caves.remove(cave)
            if entrance in invalid_connections:
                for exit2 in invalid_connections[entrance]:
                    invalid_connections[exit2] = invalid_connections[exit2].union(invalid_connections[exit]).union(invalid_cave_connections[tuple(cave)])
        elif cave[-1] == 'Spectacle Rock Cave Exit': #Spectacle rock only has one exit
            cave_entrances = []
            for cave_exit in cave[:-1]:
                entrance = next(e for e in entrances[::-1] if e not in invalid_connections[exit])
                cave_entrances.append(entrance)
                entrances.remove(entrance)
                connect_two_way(world,entrance,cave_exit, player)
                if entrance not in invalid_connections:
                    invalid_connections[exit] = set()
            if all(entrance in invalid_connections for entrance in cave_entrances):
                new_invalid_connections = invalid_connections[cave_entrances[0]].intersection(invalid_connections[cave_entrances[1]])
                for exit2 in new_invalid_connections:
                    invalid_connections[exit2] = invalid_connections[exit2].union(invalid_connections[exit])
        else:#save for later so we can connect to multiple exits
            if cave in used_caves:
                required_entrances -= 1
                used_caves.remove(cave)
            else:
                required_entrances += len(cave)-1
            caves.append(cave[0:-1])
            world.random.shuffle(caves)
            used_caves.append(cave[0:-1])
            invalid_cave_connections[tuple(cave[0:-1])] = invalid_cave_connections[tuple(cave)].union(invalid_connections[exit])
        caves.remove(cave)
    for cave in used_caves:
        if cave in caves: #check if we placed multiple entrances from this 3 or 4 exit 
            for cave_exit in cave:
                entrance = next(e for e in entrances[::-1] if e not in invalid_cave_connections[tuple(cave)])
                invalid_cave_connections[tuple(cave)] = set()
                entrances.remove(entrance)
                connect_two_way(world, entrance, cave_exit, player)
            caves.remove(cave)


def connect_caves(world, lw_entrances, dw_entrances, caves, player):
    """This works inplace"""
    world.random.shuffle(lw_entrances)
    world.random.shuffle(dw_entrances)
    world.random.shuffle(caves)
    # connect highest exit count caves first, prevent issue where we have 2 or 3 exits accross worlds left to fill
    caves.sort(key=lambda cave: 1 if isinstance(cave, str) else len(cave), reverse=True)
    for cave in caves:
        target = lw_entrances if world.random.randint(0, 1) else dw_entrances
        if isinstance(cave, str):
            cave = (cave,)

        # check if we can still fit the cave into our target group
        if len(target) < len(cave):
            # need to use other set
            target = lw_entrances if target is dw_entrances else dw_entrances

        for exit in cave:
            connect_two_way(world, target.pop(), exit, player)
    caves.clear() # emulating old behaviour of popping caves from the list in-place


def connect_doors(world, doors, targets, player):
    """This works inplace"""
    world.random.shuffle(doors)
    world.random.shuffle(targets)
    placing = min(len(doors), len(targets))
    for door, target in zip(doors, targets):
        connect_entrance(world, door, target, player)
    doors[:] = doors[placing:]
    targets[:] = targets[placing:]


def skull_woods_shuffle(world, player):
    connect_random(world, ['Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole'],
                   ['Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)', 'Skull Woods Second Section (Drop)'], player)
    connect_random(world, ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)'],
                   ['Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)'], player, True)


def simple_shuffle_dungeons(world, player):
    skull_woods_shuffle(world, player)

    dungeon_entrances = ['Eastern Palace', 'Tower of Hera', 'Thieves Town', 'Skull Woods Final Section', 'Palace of Darkness', 'Ice Palace', 'Misery Mire', 'Swamp Palace']
    dungeon_exits = ['Eastern Palace Exit', 'Tower of Hera Exit', 'Thieves Town Exit', 'Skull Woods Final Section Exit', 'Palace of Darkness Exit', 'Ice Palace Exit', 'Misery Mire Exit', 'Swamp Palace Exit']

    if world.mode[player] != 'inverted':
        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit', player)
        else:
            dungeon_entrances.append('Ganons Tower')
            dungeon_exits.append('Ganons Tower Exit')
    else:
        dungeon_entrances.append('Inverted Agahnims Tower')
        dungeon_exits.append('Inverted Agahnims Tower Exit')

    # shuffle up single entrance dungeons
    connect_random(world, dungeon_entrances, dungeon_exits, player, True)

    # mix up 4 door dungeons
    multi_dungeons = ['Desert', 'Turtle Rock']
    if world.mode[player] == 'open' or (world.mode[player] == 'inverted' and world.shuffle_ganon):
        multi_dungeons.append('Hyrule Castle')
    world.random.shuffle(multi_dungeons)

    dp_target = multi_dungeons[0]
    tr_target = multi_dungeons[1]
    if world.mode[player] not in ['open', 'inverted'] or (world.mode[player] == 'inverted' and world.shuffle_ganon is False):
        # place hyrule castle as intended
        hc_target = 'Hyrule Castle'
    else:
        hc_target = multi_dungeons[2]

    # ToDo improve this?

    if world.mode[player] != 'inverted':
        if hc_target == 'Hyrule Castle':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Hyrule Castle Exit (East)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Hyrule Castle Exit (West)', player)
            connect_two_way(world, 'Agahnims Tower', 'Agahnims Tower Exit', player)
        elif hc_target == 'Desert':
            connect_two_way(world, 'Desert Palace Entrance (South)', 'Hyrule Castle Exit (South)', player)
            connect_two_way(world, 'Desert Palace Entrance (East)', 'Hyrule Castle Exit (East)', player)
            connect_two_way(world, 'Desert Palace Entrance (West)', 'Hyrule Castle Exit (West)', player)
            connect_two_way(world, 'Desert Palace Entrance (North)', 'Agahnims Tower Exit', player)
        elif hc_target == 'Turtle Rock':
            connect_two_way(world, 'Turtle Rock', 'Hyrule Castle Exit (South)', player)
            connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Hyrule Castle Exit (East)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Hyrule Castle Exit (West)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Agahnims Tower Exit', player)

        if dp_target == 'Hyrule Castle':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Desert Palace Exit (South)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Desert Palace Exit (East)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Desert Palace Exit (West)', player)
            connect_two_way(world, 'Agahnims Tower', 'Desert Palace Exit (North)', player)
        elif dp_target == 'Desert':
            connect_two_way(world, 'Desert Palace Entrance (South)', 'Desert Palace Exit (South)', player)
            connect_two_way(world, 'Desert Palace Entrance (East)', 'Desert Palace Exit (East)', player)
            connect_two_way(world, 'Desert Palace Entrance (West)', 'Desert Palace Exit (West)', player)
            connect_two_way(world, 'Desert Palace Entrance (North)', 'Desert Palace Exit (North)', player)
        elif dp_target == 'Turtle Rock':
            connect_two_way(world, 'Turtle Rock', 'Desert Palace Exit (South)', player)
            connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Desert Palace Exit (East)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Desert Palace Exit (West)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Desert Palace Exit (North)', player)

        if tr_target == 'Hyrule Castle':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Turtle Rock Exit (Front)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Turtle Rock Ledge Exit (East)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Turtle Rock Ledge Exit (West)', player)
            connect_two_way(world, 'Agahnims Tower', 'Turtle Rock Isolated Ledge Exit', player)
        elif tr_target == 'Desert':
            connect_two_way(world, 'Desert Palace Entrance (South)', 'Turtle Rock Exit (Front)', player)
            connect_two_way(world, 'Desert Palace Entrance (North)', 'Turtle Rock Ledge Exit (East)', player)
            connect_two_way(world, 'Desert Palace Entrance (West)', 'Turtle Rock Ledge Exit (West)', player)
            connect_two_way(world, 'Desert Palace Entrance (East)', 'Turtle Rock Isolated Ledge Exit', player)
        elif tr_target == 'Turtle Rock':
            connect_two_way(world, 'Turtle Rock', 'Turtle Rock Exit (Front)', player)
            connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Turtle Rock Isolated Ledge Exit', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Turtle Rock Ledge Exit (West)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Turtle Rock Ledge Exit (East)', player)
    else:
        if hc_target == 'Hyrule Castle':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Hyrule Castle Exit (East)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Hyrule Castle Exit (West)', player)
            connect_two_way(world, 'Inverted Ganons Tower', 'Inverted Ganons Tower Exit', player)
        elif hc_target == 'Desert':
            connect_two_way(world, 'Desert Palace Entrance (South)', 'Hyrule Castle Exit (South)', player)
            connect_two_way(world, 'Desert Palace Entrance (East)', 'Hyrule Castle Exit (East)', player)
            connect_two_way(world, 'Desert Palace Entrance (West)', 'Hyrule Castle Exit (West)', player)
            connect_two_way(world, 'Desert Palace Entrance (North)', 'Inverted Ganons Tower Exit', player)
        elif hc_target == 'Turtle Rock':
            connect_two_way(world, 'Turtle Rock', 'Hyrule Castle Exit (South)', player)
            connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Inverted Ganons Tower Exit', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Hyrule Castle Exit (West)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Hyrule Castle Exit (East)', player)

        if dp_target == 'Hyrule Castle':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Desert Palace Exit (South)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Desert Palace Exit (East)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Desert Palace Exit (West)', player)
            connect_two_way(world, 'Inverted Ganons Tower', 'Desert Palace Exit (North)', player)
        elif dp_target == 'Desert':
            connect_two_way(world, 'Desert Palace Entrance (South)', 'Desert Palace Exit (South)', player)
            connect_two_way(world, 'Desert Palace Entrance (East)', 'Desert Palace Exit (East)', player)
            connect_two_way(world, 'Desert Palace Entrance (West)', 'Desert Palace Exit (West)', player)
            connect_two_way(world, 'Desert Palace Entrance (North)', 'Desert Palace Exit (North)', player)
        elif dp_target == 'Turtle Rock':
            connect_two_way(world, 'Turtle Rock', 'Desert Palace Exit (South)', player)
            connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Desert Palace Exit (East)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Desert Palace Exit (West)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Desert Palace Exit (North)', player)

        if tr_target == 'Hyrule Castle':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Turtle Rock Exit (Front)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Turtle Rock Ledge Exit (East)', player)
            connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Turtle Rock Ledge Exit (West)', player)
            connect_two_way(world, 'Inverted Ganons Tower', 'Turtle Rock Isolated Ledge Exit', player)
        elif tr_target == 'Desert':
            connect_two_way(world, 'Desert Palace Entrance (South)', 'Turtle Rock Exit (Front)', player)
            connect_two_way(world, 'Desert Palace Entrance (North)', 'Turtle Rock Ledge Exit (East)', player)
            connect_two_way(world, 'Desert Palace Entrance (West)', 'Turtle Rock Ledge Exit (West)', player)
            connect_two_way(world, 'Desert Palace Entrance (East)', 'Turtle Rock Isolated Ledge Exit', player)
        elif tr_target == 'Turtle Rock':
            connect_two_way(world, 'Turtle Rock', 'Turtle Rock Exit (Front)', player)
            connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Turtle Rock Isolated Ledge Exit', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Turtle Rock Ledge Exit (West)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Turtle Rock Ledge Exit (East)', player)

def crossed_shuffle_dungeons(world, player: int):
    lw_entrances = LW_Dungeon_Entrances.copy()
    dw_entrances = DW_Dungeon_Entrances.copy()

    for exitname, regionname in default_connections:
        connect_simple(world, exitname, regionname, player)

    skull_woods_shuffle(world, player)

    dungeon_exits = Dungeon_Exits_Base.copy()
    dungeon_entrances = lw_entrances+dw_entrances

    if not world.shuffle_ganon:
        connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit', player)
    else:
        dungeon_entrances.append('Ganons Tower')
        dungeon_exits.append('Ganons Tower Exit')

    if world.mode[player] == 'standard':
        # must connect front of hyrule castle to do escape
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
    else:
        dungeon_exits.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        dungeon_entrances.append('Hyrule Castle Entrance (South)')

    connect_mandatory_exits(world, dungeon_entrances, dungeon_exits,
                            LW_Dungeon_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit, player)

    if world.mode[player] == 'standard':
        connect_caves(world, dungeon_entrances, [], [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')], player)

    connect_caves(world, dungeon_entrances, [], dungeon_exits, player)
    assert not dungeon_exits , "make sure all exits are accounted for"

def inverted_crossed_shuffle_dungeons(world, player: int):

    lw_entrances = Inverted_LW_Dungeon_Entrances.copy()
    dw_entrances = Inverted_DW_Dungeon_Entrances.copy()
    lw_dungeon_entrances_must_exit = list(Inverted_LW_Dungeon_Entrances_Must_Exit)
    for exitname, regionname in inverted_default_connections:
        connect_simple(world, exitname, regionname, player)

    skull_woods_shuffle(world, player)

    dungeon_exits = Inverted_Dungeon_Exits_Base.copy()
    dungeon_entrances = lw_entrances+dw_entrances

    # randomize which desert ledge door is a must-exit
    if world.random.randint(0, 1):
        lw_dungeon_entrances_must_exit.append('Desert Palace Entrance (North)')
        dungeon_entrances.append('Desert Palace Entrance (West)')
    else:
        lw_dungeon_entrances_must_exit.append('Desert Palace Entrance (West)')
        dungeon_entrances.append('Desert Palace Entrance (North)')

    dungeon_exits.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
    dungeon_entrances.append('Hyrule Castle Entrance (South)')

    if not world.shuffle_ganon:
        connect_two_way(world, 'Inverted Ganons Tower', 'Inverted Ganons Tower Exit', player)
        hc_ledge_entrances = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)']
    else:
        dungeon_entrances.append('Inverted Ganons Tower')
        dungeon_exits.append('Inverted Ganons Tower Exit')
        hc_ledge_entrances = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)', 'Inverted Ganons Tower']

    # shuffle aga door first. If it's on HC ledge, remaining HC ledge door must be must-exit
    world.random.shuffle(dungeon_entrances)
    aga_door = dungeon_entrances.pop()

    if aga_door in hc_ledge_entrances:
        hc_ledge_entrances.remove(aga_door)
        world.random.shuffle(hc_ledge_entrances)
        hc_ledge_must_exit = hc_ledge_entrances.pop()
        dungeon_entrances.remove(hc_ledge_must_exit)
        lw_dungeon_entrances_must_exit.append(hc_ledge_must_exit)

    connect_two_way(world, aga_door, 'Inverted Agahnims Tower Exit', player)
    dungeon_exits.remove('Inverted Agahnims Tower Exit')

    connect_mandatory_exits(world, dungeon_entrances, dungeon_exits, lw_dungeon_entrances_must_exit, player)

    connect_caves(world, dungeon_entrances, [], dungeon_exits, player)
    assert not dungeon_exits, "make sure all exits are accounted for"

def unbias_some_entrances(world, Dungeon_Exits, Cave_Exits, Old_Man_House, Cave_Three_Exits):
    def shuffle_lists_in_list(ls):
        for i, item in enumerate(ls):
            if isinstance(item, list):
                ls[i] = world.random.sample(item, len(item))

    def tuplize_lists_in_list(ls):
        for i, item in enumerate(ls):
            if isinstance(item, list):
                ls[i] = tuple(item)

    shuffle_lists_in_list(Dungeon_Exits)
    shuffle_lists_in_list(Cave_Exits)
    shuffle_lists_in_list(Old_Man_House)
    shuffle_lists_in_list(Cave_Three_Exits)

    # paradox fixup
    if Cave_Three_Exits[1][0] == "Paradox Cave Exit (Bottom)":
        i = world.random.randint(1, 2)
        Cave_Three_Exits[1][0] = Cave_Three_Exits[1][i]
        Cave_Three_Exits[1][i] = "Paradox Cave Exit (Bottom)"

    # TR fixup
    tr_fixup = False
    for i, item in enumerate(Dungeon_Exits[-1]):
        if 'Turtle Rock Ledge Exit (East)' == item:
            tr_fixup = True
            if 0 != i:
                Dungeon_Exits[-1][i] = Dungeon_Exits[-1][0]
                Dungeon_Exits[-1][0] = 'Turtle Rock Ledge Exit (East)'
            break

    if not tr_fixup: raise RuntimeError("TR entrance shuffle fixup didn't happen")

    tuplize_lists_in_list(Dungeon_Exits)
    tuplize_lists_in_list(Cave_Exits)
    tuplize_lists_in_list(Old_Man_House)
    tuplize_lists_in_list(Cave_Three_Exits)


lookup = {
    "both": connect_two_way,
    "entrance": connect_entrance,
    "exit": lambda x, y, z, w: connect_exit(x, z, y, w)
}


def plando_connect(world, player: int):
    if world.plando_connections[player]:
        for connection in world.plando_connections[player]:
            func = lookup[connection.direction]
            try:
                func(world, connection.entrance, connection.exit, player)
            except Exception as e:
                raise Exception(f"Could not connect using {connection}") from e
        if world.mode[player] != 'inverted':
            mark_light_world_regions(world, player)
        else:
            mark_dark_world_regions(world, player)


LW_Dungeon_Entrances = ['Desert Palace Entrance (South)',
                        'Desert Palace Entrance (West)',
                        'Desert Palace Entrance (North)',
                        'Eastern Palace',
                        'Tower of Hera',
                        'Hyrule Castle Entrance (West)',
                        'Hyrule Castle Entrance (East)',
                        'Agahnims Tower']

LW_Dungeon_Entrances_Must_Exit = ['Desert Palace Entrance (East)']

DW_Dungeon_Entrances = ['Thieves Town',
                        'Skull Woods Final Section',
                        'Ice Palace',
                        'Misery Mire',
                        'Palace of Darkness',
                        'Swamp Palace',
                        'Turtle Rock',
                        'Dark Death Mountain Ledge (West)']

DW_Dungeon_Entrances_Must_Exit = ['Dark Death Mountain Ledge (East)',
                                  'Turtle Rock Isolated Ledge Entrance']

Dungeon_Exits_Base = [['Desert Palace Exit (South)', 'Desert Palace Exit (West)', 'Desert Palace Exit (East)'],
                 'Desert Palace Exit (North)',
                 'Eastern Palace Exit',
                 'Tower of Hera Exit',
                 'Thieves Town Exit',
                 'Skull Woods Final Section Exit',
                 'Ice Palace Exit',
                 'Misery Mire Exit',
                 'Palace of Darkness Exit',
                 'Swamp Palace Exit',
                 'Agahnims Tower Exit',
                 ['Turtle Rock Ledge Exit (East)',
                     'Turtle Rock Exit (Front)',  'Turtle Rock Ledge Exit (West)', 'Turtle Rock Isolated Ledge Exit']]

DW_Entrances_Must_Exit = ['Bumper Cave (Top)', 'Hookshot Cave Back Entrance']

Two_Door_Caves_Directional = [('Bumper Cave (Bottom)', 'Bumper Cave (Top)'),
                              ('Hookshot Cave', 'Hookshot Cave Back Entrance')]

Two_Door_Caves = [('Elder House (East)', 'Elder House (West)'),
                  ('Two Brothers House (East)', 'Two Brothers House (West)'),
                  ('Superbunny Cave (Bottom)', 'Superbunny Cave (Top)')]

Old_Man_Entrances = ['Old Man Cave (East)',
                     'Old Man House (Top)',
                     'Death Mountain Return Cave (East)',
                     'Spectacle Rock Cave',
                     'Spectacle Rock Cave Peak',
                     'Spectacle Rock Cave (Bottom)']

Old_Man_House_Base = [['Old Man House Exit (Bottom)', 'Old Man House Exit (Top)']]

Cave_Exits_Base = [['Elder House Exit (East)', 'Elder House Exit (West)'],
              ['Two Brothers House Exit (East)', 'Two Brothers House Exit (West)'],
              ['Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave Exit (East)'],
              ['Fairy Ascension Cave Exit (Bottom)', 'Fairy Ascension Cave Exit (Top)'],
              ['Bumper Cave Exit (Top)', 'Bumper Cave Exit (Bottom)'],
              ['Hookshot Cave Exit (South)', 'Hookshot Cave Exit (North)']]

Cave_Exits_Base += [('Superbunny Cave Exit (Bottom)', 'Superbunny Cave Exit (Top)'),
              ('Spiral Cave Exit (Top)', 'Spiral Cave Exit')]

Cave_Three_Exits_Base = [
    ('Spectacle Rock Cave Exit (Peak)', 'Spectacle Rock Cave Exit (Top)', 'Spectacle Rock Cave Exit'),
    ('Paradox Cave Exit (Top)', 'Paradox Cave Exit (Middle)', 'Paradox Cave Exit (Bottom)')
]


LW_Entrances = ['Elder House (East)',
                'Elder House (West)',
                'Two Brothers House (East)',
                'Two Brothers House (West)',
                'Old Man Cave (West)',
                'Old Man House (Bottom)',
                'Death Mountain Return Cave (West)',
                'Paradox Cave (Bottom)',
                'Paradox Cave (Middle)',
                'Paradox Cave (Top)',
                'Fairy Ascension Cave (Bottom)',
                'Fairy Ascension Cave (Top)',
                'Spiral Cave',
                'Spiral Cave (Bottom)']

DW_Entrances = ['Bumper Cave (Bottom)',
                'Superbunny Cave (Top)',
                'Superbunny Cave (Bottom)',
                'Hookshot Cave']

Bomb_Shop_Multi_Cave_Doors = ['Hyrule Castle Entrance (South)',
                              'Misery Mire',
                              'Thieves Town',
                              'Bumper Cave (Bottom)',
                              'Swamp Palace',
                              'Hyrule Castle Secret Entrance Stairs',
                              'Skull Woods First Section Door',
                              'Skull Woods Second Section Door (East)',
                              'Skull Woods Second Section Door (West)',
                              'Skull Woods Final Section',
                              'Ice Palace',
                              'Turtle Rock',
                              'Dark Death Mountain Ledge (West)',
                              'Dark Death Mountain Ledge (East)',
                              'Superbunny Cave (Top)',
                              'Superbunny Cave (Bottom)',
                              'Hookshot Cave',
                              'Ganons Tower',
                              'Desert Palace Entrance (South)',
                              'Tower of Hera',
                              'Two Brothers House (West)',
                              'Old Man Cave (East)',
                              'Old Man House (Bottom)',
                              'Old Man House (Top)',
                              'Death Mountain Return Cave (East)',
                              'Death Mountain Return Cave (West)',
                              'Spectacle Rock Cave Peak',
                              'Spectacle Rock Cave',
                              'Spectacle Rock Cave (Bottom)',
                              'Paradox Cave (Bottom)',
                              'Paradox Cave (Middle)',
                              'Paradox Cave (Top)',
                              'Fairy Ascension Cave (Bottom)',
                              'Fairy Ascension Cave (Top)',
                              'Spiral Cave',
                              'Spiral Cave (Bottom)',
                              'Palace of Darkness',
                              'Hyrule Castle Entrance (West)',
                              'Hyrule Castle Entrance (East)',
                              'Agahnims Tower',
                              'Desert Palace Entrance (West)',
                              'Desert Palace Entrance (North)'
                              # all entrances below this line would be possible for blacksmith_hut
                              # if it were not for dwarf checking multi-entrance caves
                              ]

Blacksmith_Multi_Cave_Doors = ['Eastern Palace',
                               'Elder House (East)',
                               'Elder House (West)',
                               'Two Brothers House (East)',
                               'Old Man Cave (West)',
                               'Sanctuary',
                               'Lumberjack Tree Cave',
                               'Lost Woods Hideout Stump',
                               'North Fairy Cave',
                               'Bat Cave Cave',
                               'Kakariko Well Cave']

LW_Single_Cave_Doors = ['Blinds Hideout',
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
                        'Library',
                        'Potion Shop',
                        'Dam',
                        'Lumberjack House',
                        'Lake Hylia Fortune Teller',
                        'Kakariko Gamble Game',
                        'Waterfall of Wishing',
                        'Capacity Upgrade',
                        'Bonk Rock Cave',
                        'Graveyard Cave',
                        'Checkerboard Cave',
                        'Cave 45',
                        'Kings Grave',
                        'Bonk Fairy (Light)',
                        'Hookshot Fairy',
                        'Mimic Cave']

DW_Single_Cave_Doors = ['Bonk Fairy (Dark)',
                        'Dark Sanctuary Hint',
                        'Dark Lake Hylia Fairy',
                        'C-Shaped House',
                        'Big Bomb Shop',
                        'Dark Death Mountain Fairy',
                        'Dark Lake Hylia Shop',
                        'Village of Outcasts Shop',
                        'Red Shield Shop',
                        'Mire Shed',
                        'East Dark World Hint',
                        'Dark Desert Hint',
                        'Spike Cave',
                        'Palace of Darkness Hint',
                        'Dark Lake Hylia Ledge Spike Cave',
                        'Cave Shop (Dark Death Mountain)',
                        'Dark World Potion Shop',
                        'Pyramid Fairy',
                        'Archery Game',
                        'Dark World Lumberjack Shop',
                        'Hype Cave',
                        'Brewery',
                        'Dark Lake Hylia Ledge Hint',
                        'Chest Game',
                        'Dark Desert Fairy',
                        'Dark Lake Hylia Ledge Fairy',
                        'Fortune Teller (Dark)',
                        'Dark World Hammer Peg Cave']

Blacksmith_Single_Cave_Doors = ['Blinds Hideout',
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
                                'Library',
                                'Potion Shop',
                                'Dam',
                                'Lumberjack House',
                                'Lake Hylia Fortune Teller',
                                'Kakariko Gamble Game']

Bomb_Shop_Single_Cave_Doors = ['Waterfall of Wishing',
                               'Capacity Upgrade',
                               'Bonk Rock Cave',
                               'Graveyard Cave',
                               'Checkerboard Cave',
                               'Cave 45',
                               'Kings Grave',
                               'Bonk Fairy (Light)',
                               'Hookshot Fairy',
                               'East Dark World Hint',
                               'Palace of Darkness Hint',
                               'Dark Lake Hylia Fairy',
                               'Dark Lake Hylia Ledge Fairy',
                               'Dark Lake Hylia Ledge Spike Cave',
                               'Dark Lake Hylia Ledge Hint',
                               'Hype Cave',
                               'Bonk Fairy (Dark)',
                               'Brewery',
                               'C-Shaped House',
                               'Chest Game',
                               'Dark World Hammer Peg Cave',
                               'Red Shield Shop',
                               'Dark Sanctuary Hint',
                               'Fortune Teller (Dark)',
                               'Village of Outcasts Shop',
                               'Dark World Lumberjack Shop',
                               'Dark World Potion Shop',
                               'Archery Game',
                               'Mire Shed',
                               'Dark Desert Hint',
                               'Dark Desert Fairy',
                               'Spike Cave',
                               'Cave Shop (Dark Death Mountain)',
                               'Dark Death Mountain Fairy',
                               'Mimic Cave',
                               'Big Bomb Shop',
                               'Dark Lake Hylia Shop']

Single_Cave_Doors = ['Pyramid Fairy']

Single_Cave_Targets = ['Blinds Hideout',
                       'Bonk Fairy (Light)',
                       'Lake Hylia Healer Fairy',
                       'Swamp Healer Fairy',
                       'Desert Healer Fairy',
                       'Kings Grave',
                       'Chicken House',
                       'Aginahs Cave',
                       'Sahasrahlas Hut',
                       'Cave Shop (Lake Hylia)',
                       'Sick Kids House',
                       'Lost Woods Gamble',
                       'Fortune Teller (Light)',
                       'Snitch Lady (East)',
                       'Snitch Lady (West)',
                       'Bush Covered House',
                       'Tavern (Front)',
                       'Light World Bomb Hut',
                       'Kakariko Shop',
                       'Cave 45',
                       'Graveyard Cave',
                       'Checkerboard Cave',
                       'Mini Moldorm Cave',
                       'Long Fairy Cave',
                       'Good Bee Cave',
                       '20 Rupee Cave',
                       '50 Rupee Cave',
                       'Ice Rod Cave',
                       'Bonk Rock Cave',
                       'Library',
                       'Potion Shop',
                       'Hookshot Fairy',
                       'Waterfall of Wishing',
                       'Capacity Upgrade',
                       'Pyramid Fairy',
                       'East Dark World Hint',
                       'Palace of Darkness Hint',
                       'Dark Lake Hylia Healer Fairy',
                       'Dark Lake Hylia Ledge Healer Fairy',
                       'Dark Lake Hylia Ledge Spike Cave',
                       'Dark Lake Hylia Ledge Hint',
                       'Hype Cave',
                       'Bonk Fairy (Dark)',
                       'Brewery',
                       'C-Shaped House',
                       'Chest Game',
                       'Dark World Hammer Peg Cave',
                       'Red Shield Shop',
                       'Dark Sanctuary Hint',
                       'Fortune Teller (Dark)',
                       'Village of Outcasts Shop',
                       'Dark Lake Hylia Shop',
                       'Dark World Lumberjack Shop',
                       'Archery Game',
                       'Mire Shed',
                       'Dark Desert Hint',
                       'Dark Desert Healer Fairy',
                       'Spike Cave',
                       'Cave Shop (Dark Death Mountain)',
                       'Dark Death Mountain Healer Fairy',
                       'Mimic Cave',
                       'Dark World Potion Shop',
                       'Lumberjack House',
                       'Lake Hylia Fortune Teller',
                       'Kakariko Gamble Game',
                       'Dam']

Inverted_LW_Dungeon_Entrances = ['Desert Palace Entrance (South)',
                                 'Eastern Palace',
                                 'Tower of Hera',
                                 'Hyrule Castle Entrance (West)',
                                 'Hyrule Castle Entrance (East)']

Inverted_DW_Dungeon_Entrances = ['Thieves Town',
                                 'Skull Woods Final Section',
                                 'Ice Palace',
                                 'Misery Mire',
                                 'Palace of Darkness',
                                 'Swamp Palace',
                                 'Turtle Rock',
                                 'Dark Death Mountain Ledge (West)',
                                 'Dark Death Mountain Ledge (East)',
                                 'Turtle Rock Isolated Ledge Entrance',
                                 'Inverted Agahnims Tower']

Inverted_LW_Dungeon_Entrances_Must_Exit = ['Desert Palace Entrance (East)']

Inverted_Dungeon_Exits_Base = [['Desert Palace Exit (South)', 'Desert Palace Exit (West)', 'Desert Palace Exit (East)'],
                 'Desert Palace Exit (North)',
                 'Eastern Palace Exit',
                 'Tower of Hera Exit',
                 'Thieves Town Exit',
                 'Skull Woods Final Section Exit',
                 'Ice Palace Exit',
                 'Misery Mire Exit',
                 'Palace of Darkness Exit',
                 'Swamp Palace Exit',
                 'Inverted Agahnims Tower Exit',
                 ['Turtle Rock Ledge Exit (East)',
                     'Turtle Rock Exit (Front)',  'Turtle Rock Ledge Exit (West)', 'Turtle Rock Isolated Ledge Exit']]

Inverted_LW_Entrances_Must_Exit = ['Death Mountain Return Cave (West)',
                                   'Two Brothers House (West)']

Inverted_Two_Door_Caves_Directional = [('Old Man Cave (West)', 'Death Mountain Return Cave (West)'),
                                       ('Two Brothers House (East)', 'Two Brothers House (West)')]


Inverted_Two_Door_Caves = [('Elder House (East)', 'Elder House (West)'),
                           ('Superbunny Cave (Bottom)', 'Superbunny Cave (Top)'),
                           ('Hookshot Cave', 'Hookshot Cave Back Entrance')]



Inverted_Old_Man_Entrances = ['Dark Death Mountain Fairy',
                              'Spike Cave']

Inverted_LW_Entrances = ['Elder House (East)',
                         'Elder House (West)',
                         'Two Brothers House (East)',
                         'Old Man Cave (East)',
                         'Old Man Cave (West)',
                         'Old Man House (Bottom)',
                         'Old Man House (Top)',
                         'Death Mountain Return Cave (East)',
                         'Paradox Cave (Bottom)',
                         'Paradox Cave (Middle)',
                         'Paradox Cave (Top)',
                         'Spectacle Rock Cave',
                         'Spectacle Rock Cave Peak',
                         'Spectacle Rock Cave (Bottom)',
                         'Fairy Ascension Cave (Bottom)',
                         'Fairy Ascension Cave (Top)',
                         'Spiral Cave',
                         'Spiral Cave (Bottom)']


Inverted_DW_Entrances = ['Bumper Cave (Bottom)',
                         'Superbunny Cave (Top)',
                         'Superbunny Cave (Bottom)',
                         'Hookshot Cave',
                         'Hookshot Cave Back Entrance']

Inverted_Bomb_Shop_Multi_Cave_Doors = ['Hyrule Castle Entrance (South)',
                                       'Misery Mire',
                                       'Thieves Town',
                                       'Bumper Cave (Bottom)',
                                       'Swamp Palace',
                                       'Hyrule Castle Secret Entrance Stairs',
                                       'Skull Woods First Section Door',
                                       'Skull Woods Second Section Door (East)',
                                       'Skull Woods Second Section Door (West)',
                                       'Skull Woods Final Section',
                                       'Ice Palace',
                                       'Turtle Rock',
                                       'Dark Death Mountain Ledge (West)',
                                       'Dark Death Mountain Ledge (East)',
                                       'Superbunny Cave (Top)',
                                       'Superbunny Cave (Bottom)',
                                       'Hookshot Cave',
                                       'Inverted Agahnims Tower',
                                       'Desert Palace Entrance (South)',
                                       'Tower of Hera',
                                       'Two Brothers House (West)',
                                       'Old Man Cave (East)',
                                       'Old Man House (Bottom)',
                                       'Old Man House (Top)',
                                       'Death Mountain Return Cave (East)',
                                       'Death Mountain Return Cave (West)',
                                       'Spectacle Rock Cave Peak',
                                       'Paradox Cave (Bottom)',
                                       'Paradox Cave (Middle)',
                                       'Paradox Cave (Top)',
                                       'Fairy Ascension Cave (Bottom)',
                                       'Fairy Ascension Cave (Top)',
                                       'Spiral Cave',
                                       'Spiral Cave (Bottom)',
                                       'Palace of Darkness',
                                       'Hyrule Castle Entrance (West)',
                                       'Hyrule Castle Entrance (East)',
                                       'Inverted Ganons Tower',
                                       'Desert Palace Entrance (West)',
                                       'Desert Palace Entrance (North)']

Inverted_Blacksmith_Multi_Cave_Doors = Blacksmith_Multi_Cave_Doors  # same as non-inverted

Inverted_LW_Single_Cave_Doors = LW_Single_Cave_Doors + ['Inverted Big Bomb Shop']

Inverted_DW_Single_Cave_Doors = ['Bonk Fairy (Dark)',
                                 'Inverted Dark Sanctuary',
                                 'Inverted Links House',
                                 'Dark Lake Hylia Fairy',
                                 'C-Shaped House',
                                 'Bumper Cave (Top)',
                                 'Dark Lake Hylia Shop',
                                 'Village of Outcasts Shop',
                                 'Red Shield Shop',
                                 'Mire Shed',
                                 'East Dark World Hint',
                                 'Dark Desert Hint',
                                 'Palace of Darkness Hint',
                                 'Dark Lake Hylia Ledge Spike Cave',
                                 'Cave Shop (Dark Death Mountain)',
                                 'Dark World Potion Shop',
                                 'Pyramid Fairy',
                                 'Archery Game',
                                 'Dark World Lumberjack Shop',
                                 'Hype Cave',
                                 'Brewery',
                                 'Dark Lake Hylia Ledge Hint',
                                 'Chest Game',
                                 'Dark Desert Fairy',
                                 'Dark Lake Hylia Ledge Fairy',
                                 'Fortune Teller (Dark)',
                                 'Dark World Hammer Peg Cave']


Inverted_Bomb_Shop_Single_Cave_Doors = ['Waterfall of Wishing',
                                        'Capacity Upgrade',
                                        'Bonk Rock Cave',
                                        'Graveyard Cave',
                                        'Checkerboard Cave',
                                        'Cave 45',
                                        'Kings Grave',
                                        'Bonk Fairy (Light)',
                                        'Hookshot Fairy',
                                        'East Dark World Hint',
                                        'Palace of Darkness Hint',
                                        'Dark Lake Hylia Fairy',
                                        'Dark Lake Hylia Ledge Fairy',
                                        'Dark Lake Hylia Ledge Spike Cave',
                                        'Dark Lake Hylia Ledge Hint',
                                        'Hype Cave',
                                        'Bonk Fairy (Dark)',
                                        'Brewery',
                                        'C-Shaped House',
                                        'Chest Game',
                                        'Dark World Hammer Peg Cave',
                                        'Red Shield Shop',
                                        'Inverted Dark Sanctuary',
                                        'Fortune Teller (Dark)',
                                        'Village of Outcasts Shop',
                                        'Dark World Lumberjack Shop',
                                        'Dark World Potion Shop',
                                        'Archery Game',
                                        'Mire Shed',
                                        'Dark Desert Hint',
                                        'Dark Desert Fairy',
                                        'Spike Cave',
                                        'Cave Shop (Dark Death Mountain)',
                                        'Bumper Cave (Top)',
                                        'Mimic Cave',
                                        'Dark Lake Hylia Shop',
                                        'Inverted Links House',
                                        'Inverted Big Bomb Shop']


Inverted_Single_Cave_Targets = ['Blinds Hideout',
                                'Bonk Fairy (Light)',
                                'Lake Hylia Healer Fairy',
                                'Swamp Healer Fairy',
                                'Desert Healer Fairy',
                                'Kings Grave',
                                'Chicken House',
                                'Aginahs Cave',
                                'Sahasrahlas Hut',
                                'Cave Shop (Lake Hylia)',
                                'Sick Kids House',
                                'Lost Woods Gamble',
                                'Fortune Teller (Light)',
                                'Snitch Lady (East)',
                                'Snitch Lady (West)',
                                'Bush Covered House',
                                'Tavern (Front)',
                                'Light World Bomb Hut',
                                'Kakariko Shop',
                                'Cave 45',
                                'Graveyard Cave',
                                'Checkerboard Cave',
                                'Mini Moldorm Cave',
                                'Long Fairy Cave',
                                'Good Bee Cave',
                                '20 Rupee Cave',
                                '50 Rupee Cave',
                                'Ice Rod Cave',
                                'Bonk Rock Cave',
                                'Library',
                                'Potion Shop',
                                'Hookshot Fairy',
                                'Waterfall of Wishing',
                                'Capacity Upgrade',
                                'Pyramid Fairy',
                                'East Dark World Hint',
                                'Palace of Darkness Hint',
                                'Dark Lake Hylia Healer Fairy',
                                'Dark Lake Hylia Ledge Healer Fairy',
                                'Dark Lake Hylia Ledge Spike Cave',
                                'Dark Lake Hylia Ledge Hint',
                                'Hype Cave',
                                'Bonk Fairy (Dark)',
                                'Brewery',
                                'C-Shaped House',
                                'Chest Game',
                                'Dark World Hammer Peg Cave',
                                'Red Shield Shop',
                                'Fortune Teller (Dark)',
                                'Village of Outcasts Shop',
                                'Dark Lake Hylia Shop',
                                'Dark World Lumberjack Shop',
                                'Archery Game',
                                'Mire Shed',
                                'Dark Desert Hint',
                                'Dark Desert Healer Fairy',
                                'Spike Cave',
                                'Cave Shop (Dark Death Mountain)',
                                'Dark Death Mountain Healer Fairy',
                                'Mimic Cave',
                                'Dark World Potion Shop',
                                'Lumberjack House',
                                'Lake Hylia Fortune Teller',
                                'Kakariko Gamble Game',
                                'Dam']

# in inverted we put dark sanctuary in west dark world for now
Inverted_Dark_Sanctuary_Doors = ['Inverted Dark Sanctuary',
                                 'Fortune Teller (Dark)',
                                 'Brewery',
                                 'C-Shaped House',
                                 'Chest Game',
                                 'Dark World Lumberjack Shop',
                                 'Red Shield Shop',
                                 'Bumper Cave (Bottom)',
                                 'Bumper Cave (Top)',
                                 'Thieves Town']

Isolated_LH_Doors = ['Kings Grave',
                     'Waterfall of Wishing',
                     'Desert Palace Entrance (South)',
                     'Desert Palace Entrance (North)',
                     'Capacity Upgrade',
                     'Ice Palace',
                     'Skull Woods Final Section',
                     'Dark World Hammer Peg Cave',
                     'Turtle Rock Isolated Ledge Entrance']

# Entrances that cannot be used to access a must_exit entrance - symmetrical to allow reverse lookups
Must_Exit_Invalid_Connections = defaultdict(set, {
    'Dark Death Mountain Ledge (East)': {'Dark Death Mountain Ledge (West)', 'Mimic Cave'},
    'Dark Death Mountain Ledge (West)': {'Dark Death Mountain Ledge (East)', 'Mimic Cave'},
    'Mimic Cave': {'Dark Death Mountain Ledge (West)', 'Dark Death Mountain Ledge (East)'},
    'Bumper Cave (Top)': {'Death Mountain Return Cave (West)'},
    'Death Mountain Return Cave (West)': {'Bumper Cave (Top)'},
    'Skull Woods Second Section Door (West)': {'Skull Woods Final Section'},
    'Skull Woods Final Section': {'Skull Woods Second Section Door (West)'},
})
Inverted_Must_Exit_Invalid_Connections = defaultdict(set, {
    'Bumper Cave (Top)': {'Death Mountain Return Cave (West)'},
    'Death Mountain Return Cave (West)': {'Bumper Cave (Top)'},
    'Desert Palace Entrance (North)': {'Desert Palace Entrance (West)'},
    'Desert Palace Entrance (West)': {'Desert Palace Entrance (North)'},
    'Inverted Ganons Tower': {'Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)'},
    'Hyrule Castle Entrance (West)': {'Hyrule Castle Entrance (East)', 'Inverted Ganons Tower'},
    'Hyrule Castle Entrance (East)': {'Hyrule Castle Entrance (West)', 'Inverted Ganons Tower'},
})

# these are connections that cannot be shuffled and always exist. They link together separate parts of the world we need to divide into regions
mandatory_connections = [('Links House S&Q', 'Links House'),
                         ('Sanctuary S&Q', 'Sanctuary'),
                         ('Old Man S&Q', 'Old Man House'),
                         ('Lake Hylia Central Island Pier', 'Lake Hylia Central Island'),
                         ('Lake Hylia Central Island Teleporter', 'Dark Lake Hylia Central Island'),
                         ('Zoras River', 'Zoras River'),
                         ('Kings Grave Outer Rocks', 'Kings Grave Area'),
                         ('Kings Grave Inner Rocks', 'Light World'),
                         ('Kings Grave Mirror Spot', 'Kings Grave Area'),
                         ('Kakariko Well (top to bottom)', 'Kakariko Well (bottom)'),
                         ('Master Sword Meadow', 'Master Sword Meadow'),
                         ('Hobo Bridge', 'Hobo Bridge'),
                         ('Desert Palace East Wing', 'Desert Palace East'),
                         ('Bat Cave Drop Ledge', 'Bat Cave Drop Ledge'),
                         ('Bat Cave Door', 'Bat Cave (left)'),
                         ('Lost Woods Hideout (top to bottom)', 'Lost Woods Hideout (bottom)'),
                         ('Lumberjack Tree (top to bottom)', 'Lumberjack Tree (bottom)'),
                         ('Desert Palace Stairs', 'Desert Palace Stairs'),
                         ('Desert Palace Stairs Drop', 'Light World'),
                         ('Desert Palace Entrance (North) Rocks', 'Desert Palace Entrance (North) Spot'),
                         ('Desert Ledge Return Rocks', 'Desert Ledge'),
                         ('Hyrule Castle Ledge Courtyard Drop', 'Hyrule Castle Courtyard'),
                         ('Hyrule Castle Main Gate', 'Hyrule Castle Courtyard'),
                         ('Throne Room', 'Sewers (Dark)'),
                         ('Sewers Door', 'Sewers'),
                         ('Sanctuary Push Door', 'Sanctuary'),
                         ('Sewer Drop', 'Sewers'),
                         ('Sewers Back Door', 'Sewers (Dark)'),
                         ('Sewers Secret Room', 'Sewers Secret Room'),
                         ('Agahnim 1', 'Agahnim 1'),
                         ('Flute Spot 1', 'Death Mountain'),
                         ('Death Mountain Entrance Rock', 'Death Mountain Entrance'),
                         ('Death Mountain Entrance Drop', 'Light World'),
                         ('Spectacle Rock Cave Drop', 'Spectacle Rock Cave (Bottom)'),
                         ('Spectacle Rock Cave Peak Drop', 'Spectacle Rock Cave (Bottom)'),
                         ('Death Mountain Return Ledge Drop', 'Light World'),
                         ('Old Man House Front to Back', 'Old Man House Back'),
                         ('Old Man House Back to Front', 'Old Man House'),
                         ('Broken Bridge (West)', 'East Death Mountain (Bottom)'),
                         ('Broken Bridge (East)', 'Death Mountain'),
                         ('East Death Mountain Drop', 'East Death Mountain (Bottom)'),
                         ('Spiral Cave Ledge Access', 'Spiral Cave Ledge'),
                         ('Spiral Cave Ledge Drop', 'East Death Mountain (Bottom)'),
                         ('Spiral Cave (top to bottom)', 'Spiral Cave (Bottom)'),
                         ('Hookshot Cave Bomb Wall (South)', 'Hookshot Cave (Upper)'),
                         ('Hookshot Cave Bomb Wall (North)', 'Hookshot Cave'),
                         ('East Death Mountain (Top)', 'East Death Mountain (Top)'),
                         ('Death Mountain (Top)', 'Death Mountain (Top)'),
                         ('Death Mountain Drop', 'Death Mountain'),
                         ('Spectacle Rock Drop', 'Death Mountain (Top)'),
                         ('Tower of Hera Small Key Door', 'Tower of Hera (Basement)'),
                         ('Tower of Hera Big Key Door', 'Tower of Hera (Top)'),

                         ('Top of Pyramid', 'East Dark World'),
                         ('Dark Lake Hylia Drop (East)', 'Dark Lake Hylia'),
                         ('Dark Lake Hylia Drop (South)', 'Dark Lake Hylia'),
                         ('Dark Lake Hylia Teleporter', 'Dark Lake Hylia'),
                         ('Dark Lake Hylia Ledge', 'Dark Lake Hylia Ledge'),
                         ('Dark Lake Hylia Ledge Drop', 'Dark Lake Hylia'),
                         ('East Dark World Pier', 'East Dark World'),
                         ('Lake Hylia Island Mirror Spot', 'Lake Hylia Island'),
                         ('Lake Hylia Central Island Mirror Spot', 'Lake Hylia Central Island'),
                         ('Hyrule Castle Ledge Mirror Spot', 'Hyrule Castle Ledge'),
                         ('South Dark World Bridge', 'South Dark World'),
                         ('East Dark World Bridge', 'East Dark World'),
                         ('Maze Race Mirror Spot', 'Maze Race Ledge'),
                         ('Village of Outcasts Heavy Rock', 'West Dark World'),
                         ('Village of Outcasts Drop', 'South Dark World'),
                         ('Village of Outcasts Eastern Rocks', 'Hammer Peg Area'),
                         ('Village of Outcasts Pegs', 'Dark Grassy Lawn'),
                         ('Peg Area Rocks', 'West Dark World'),
                         ('Grassy Lawn Pegs', 'West Dark World'),
                         ('Bat Cave Drop Ledge Mirror Spot', 'Bat Cave Drop Ledge'),
                         ('East Dark World River Pier', 'East Dark World'),
                         ('West Dark World Gap', 'West Dark World'),
                         ('East Dark World Broken Bridge Pass', 'East Dark World'),
                         ('Catfish Exit Rock', 'Northeast Dark World'),
                         ('Catfish Entrance Rock', 'Catfish'),
                         ('Northeast Dark World Broken Bridge Pass', 'Northeast Dark World'),
                         ('Bumper Cave Entrance Rock', 'Bumper Cave Entrance'),
                         ('Bumper Cave Entrance Drop', 'West Dark World'),
                         ('Bumper Cave Entrance Mirror Spot', 'Death Mountain Entrance'),
                         ('Bumper Cave Ledge Drop', 'West Dark World'),
                         ('Bumper Cave Ledge Mirror Spot', 'Death Mountain Return Ledge'),
                         ('Skull Woods Forest', 'Skull Woods Forest'),
                         ('Desert Ledge Mirror Spot', 'Desert Ledge'),
                         ('Desert Ledge (Northeast) Mirror Spot', 'Desert Ledge (Northeast)'),
                         ('Desert Palace Entrance (North) Mirror Spot', 'Desert Palace Entrance (North) Spot'),
                         ('Dark Desert Teleporter', 'Dark Desert'),
                         ('Desert Palace Stairs Mirror Spot', 'Desert Palace Stairs'),
                         ('East Hyrule Teleporter', 'East Dark World'),
                         ('South Hyrule Teleporter', 'South Dark World'),
                         ('Kakariko Teleporter', 'West Dark World'),
                         ('Death Mountain Teleporter', 'Dark Death Mountain (West Bottom)'),
                         ('Paradox Cave Push Block Reverse', 'Paradox Cave Chest Area'),
                         ('Paradox Cave Push Block', 'Paradox Cave Front'),
                         ('Paradox Cave Bomb Jump', 'Paradox Cave'),
                         ('Paradox Cave Drop', 'Paradox Cave Chest Area'),
                         ('Light World Death Mountain Shop', 'Light World Death Mountain Shop'),
                         ('Fairy Ascension Rocks', 'Fairy Ascension Plateau'),
                         ('Fairy Ascension Mirror Spot', 'Fairy Ascension Plateau'),
                         ('Fairy Ascension Drop', 'East Death Mountain (Bottom)'),
                         ('Fairy Ascension Ledge Drop', 'Fairy Ascension Plateau'),
                         ('Fairy Ascension Ledge', 'Fairy Ascension Ledge'),
                         ('Fairy Ascension Cave Climb', 'Fairy Ascension Cave (Top)'),
                         ('Fairy Ascension Cave Pots', 'Fairy Ascension Cave (Bottom)'),
                         ('Fairy Ascension Cave Drop', 'Fairy Ascension Cave (Drop)'),
                         ('Spectacle Rock Mirror Spot', 'Spectacle Rock'),
                         ('Dark Death Mountain Drop (East)', 'Dark Death Mountain (East Bottom)'),
                         ('Dark Death Mountain Drop (West)', 'Dark Death Mountain (West Bottom)'),
                         ('East Death Mountain (Top) Mirror Spot', 'East Death Mountain (Top)'),
                         ('Turtle Rock Teleporter', 'Turtle Rock (Top)'),
                         ('Turtle Rock Drop', 'Dark Death Mountain (Top)'),
                         ('Floating Island Drop', 'Dark Death Mountain (Top)'),
                         ('Floating Island Mirror Spot', 'Death Mountain Floating Island (Light World)'),
                         ('East Death Mountain Teleporter', 'Dark Death Mountain (East Bottom)'),
                         ('Isolated Ledge Mirror Spot', 'Fairy Ascension Ledge'),
                         ('Spiral Cave Mirror Spot', 'Spiral Cave Ledge'),
                         ('Mimic Cave Mirror Spot', 'Mimic Cave Ledge'),
                         ('Cave 45 Mirror Spot', 'Cave 45 Ledge'),
                         ('Bombos Tablet Mirror Spot', 'Bombos Tablet Ledge'),
                         ('Graveyard Ledge Mirror Spot', 'Graveyard Ledge'),
                         ('Superbunny Cave Climb', 'Superbunny Cave (Top)'),

                         ('Swamp Palace Moat', 'Swamp Palace (First Room)'),
                         ('Swamp Palace Small Key Door', 'Swamp Palace (Starting Area)'),
                         ('Swamp Palace (Center)', 'Swamp Palace (Center)'),
                         ('Swamp Palace (West)', 'Swamp Palace (West)'),
                         ('Swamp Palace (North)', 'Swamp Palace (North)'),
                         ('Thieves Town Big Key Door', 'Thieves Town (Deep)'),
                         ('Skull Woods Torch Room', 'Skull Woods Final Section (Mothula)'),
                         ('Skull Woods First Section Bomb Jump', 'Skull Woods First Section (Top)'),  # represents bomb jumping to big chest
                         ('Skull Woods First Section South Door', 'Skull Woods First Section (Right)'),
                         ('Skull Woods First Section West Door', 'Skull Woods First Section (Left)'),
                         ('Skull Woods First Section (Right) North Door', 'Skull Woods First Section'),
                         ('Skull Woods First Section (Left) Door to Right', 'Skull Woods First Section (Right)'),
                         ('Skull Woods First Section (Left) Door to Exit', 'Skull Woods First Section'),
                         ('Skull Woods First Section (Top) One-Way Path', 'Skull Woods First Section'),
                         ('Skull Woods Second Section (Drop)', 'Skull Woods Second Section'),
                         ('Blind Fight', 'Blind Fight'),
                         ('Desert Palace Pots (Outer)', 'Desert Palace Main (Inner)'),
                         ('Desert Palace Pots (Inner)', 'Desert Palace Main (Outer)'),
                         ('Ice Palace (Main)', 'Ice Palace (Main)'),
                         ('Ice Palace (Second Section)', 'Ice Palace (Second Section)'),
                         ('Ice Palace (East)', 'Ice Palace (East)'),
                         ('Ice Palace (East Top)', 'Ice Palace (East Top)'),
                         ('Ice Palace (Kholdstare)', 'Ice Palace (Kholdstare)'),
                         ('Misery Mire Entrance Gap', 'Misery Mire (Main)'),
                         ('Misery Mire (West)', 'Misery Mire (West)'),
                         ('Misery Mire Big Key Door', 'Misery Mire (Final Area)'),
                         ('Misery Mire (Vitreous)', 'Misery Mire (Vitreous)'),
                         ('Turtle Rock Entrance Gap', 'Turtle Rock (First Section)'),
                         ('Turtle Rock Entrance Gap Reverse', 'Turtle Rock (Entrance)'),
                         ('Turtle Rock Entrance to Pokey Room', 'Turtle Rock (Pokey Room)'),
                         ('Turtle Rock (Pokey Room) (South)', 'Turtle Rock (First Section)'),
                         ('Turtle Rock (Pokey Room) (North)', 'Turtle Rock (Chain Chomp Room)'),
                         ('Turtle Rock (Chain Chomp Room) (North)', 'Turtle Rock (Second Section)'),
                         ('Turtle Rock (Chain Chomp Room) (South)', 'Turtle Rock (Pokey Room)'),
                         ('Turtle Rock Chain Chomp Staircase', 'Turtle Rock (Chain Chomp Room)'),
                         ('Turtle Rock (Big Chest) (North)', 'Turtle Rock (Second Section)'),
                         ('Turtle Rock Big Key Door', 'Turtle Rock (Crystaroller Room)'),
                         ('Turtle Rock Big Key Door Reverse', 'Turtle Rock (Second Section)'),
                         ('Turtle Rock Dark Room Staircase', 'Turtle Rock (Dark Room)'),
                         ('Turtle Rock (Dark Room) (North)', 'Turtle Rock (Crystaroller Room)'),
                         ('Turtle Rock (Dark Room) (South)', 'Turtle Rock (Eye Bridge)'),
                         ('Turtle Rock Dark Room (South)', 'Turtle Rock (Dark Room)'),
                         ('Turtle Rock Second Section Bomb Wall', 'Turtle Rock (Second Section Bomb Wall)'),
                         ('Turtle Rock Second Section from Bomb Wall', 'Turtle Rock (Second Section)'),
                         ('Turtle Rock Eye Bridge Bomb Wall', 'Turtle Rock (Eye Bridge Bomb Wall)'),
                         ('Turtle Rock Eye Bridge from Bomb Wall', 'Turtle Rock (Eye Bridge)'),
                         ('Turtle Rock (Trinexx)', 'Turtle Rock (Trinexx)'),
                         ('Palace of Darkness Bridge Room', 'Palace of Darkness (Center)'),
                         ('Palace of Darkness Bonk Wall', 'Palace of Darkness (Bonk Section)'),
                         ('Palace of Darkness Big Key Chest Staircase', 'Palace of Darkness (Big Key Chest)'),
                         ('Palace of Darkness (North)', 'Palace of Darkness (North)'),
                         ('Palace of Darkness Big Key Door', 'Palace of Darkness (Final Section)'),
                         ('Palace of Darkness Hammer Peg Drop', 'Palace of Darkness (Center)'),
                         ('Palace of Darkness Spike Statue Room Door', 'Palace of Darkness (Harmless Hellway)'),
                         ('Palace of Darkness Maze Door', 'Palace of Darkness (Maze)'),
                         ('Ganons Tower (Tile Room)', 'Ganons Tower (Tile Room)'),
                         ('Ganons Tower (Tile Room) Key Door', 'Ganons Tower (Compass Room)'),
                         ('Ganons Tower (Bottom) (East)', 'Ganons Tower (Bottom)'),
                         ('Ganons Tower (Hookshot Room)', 'Ganons Tower (Hookshot Room)'),
                         ('Ganons Tower (Map Room)', 'Ganons Tower (Map Room)'),
                         ('Ganons Tower (Double Switch Room)', 'Ganons Tower (Firesnake Room)'),
                         ('Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)'),
                         ('Ganons Tower (Bottom) (West)', 'Ganons Tower (Bottom)'),
                         ('Ganons Tower Big Key Door', 'Ganons Tower (Top)'),
                         ('Ganons Tower Torch Rooms', 'Ganons Tower (Before Moldorm)'),
                         ('Ganons Tower Moldorm Door', 'Ganons Tower (Moldorm)'),
                         ('Ganons Tower Moldorm Gap', 'Agahnim 2'),
                         ('Ganon Drop', 'Bottom of Pyramid'),
                         ('Pyramid Drop', 'East Dark World')
                        ]

inverted_mandatory_connections = [('Links House S&Q', 'Inverted Links House'),
                                  ('Dark Sanctuary S&Q', 'Inverted Dark Sanctuary'),
                                  ('Old Man S&Q', 'Old Man House'),
                                  ('Castle Ledge S&Q', 'Hyrule Castle Ledge'),
                                  ('Lake Hylia Central Island Pier', 'Lake Hylia Central Island'),
                                  ('Lake Hylia Island Pier', 'Lake Hylia Island'),
                                  ('Lake Hylia Warp', 'Northeast Light World'),
                                  ('Northeast Light World Warp', 'Light World'),
                                  ('Zoras River', 'Zoras River'),
                                  ('Waterfall of Wishing Cave', 'Waterfall of Wishing Cave'),
                                  ('Northeast Light World Return', 'Northeast Light World'),
                                  ('Kings Grave Outer Rocks', 'Kings Grave Area'),
                                  ('Kings Grave Inner Rocks', 'Light World'),
                                  ('Kakariko Well (top to bottom)', 'Kakariko Well (bottom)'),
                                  ('Master Sword Meadow', 'Master Sword Meadow'),
                                  ('Hobo Bridge', 'Hobo Bridge'), 
                                  ('Desert Palace East Wing', 'Desert Palace East'),
                                  ('Bat Cave Drop Ledge', 'Bat Cave Drop Ledge'),
                                  ('Bat Cave Door', 'Bat Cave (left)'),
                                  ('Lost Woods Hideout (top to bottom)', 'Lost Woods Hideout (bottom)'),
                                  ('Lumberjack Tree (top to bottom)', 'Lumberjack Tree (bottom)'),
                                  ('Desert Palace Stairs', 'Desert Palace Stairs'),
                                  ('Desert Palace Stairs Drop', 'Light World'),
                                  ('Desert Palace Entrance (North) Rocks', 'Desert Palace Entrance (North) Spot'),
                                  ('Desert Ledge Return Rocks', 'Desert Ledge'),
                                  ('Throne Room', 'Sewers (Dark)'), ('Sewers Door', 'Sewers'),
                                  ('Sanctuary Push Door', 'Sanctuary'),
                                  ('Sewer Drop', 'Sewers'),
                                  ('Sewers Back Door', 'Sewers (Dark)'),
                                  ('Sewers Secret Room', 'Sewers Secret Room'),
                                  ('Agahnim 1', 'Agahnim 1'),
                                  ('Death Mountain Entrance Rock', 'Death Mountain Entrance'),
                                  ('Death Mountain Entrance Drop', 'Light World'),
                                  ('Spectacle Rock Cave Drop', 'Spectacle Rock Cave (Bottom)'),
                                  ('Spectacle Rock Cave Peak Drop', 'Spectacle Rock Cave (Bottom)'),
                                  ('Death Mountain Return Ledge Drop', 'Light World'),
                                  ('Old Man House Front to Back', 'Old Man House Back'),
                                  ('Old Man House Back to Front', 'Old Man House'),
                                  ('Broken Bridge (West)', 'East Death Mountain (Bottom)'),
                                  ('Broken Bridge (East)', 'Death Mountain'),
                                  ('East Death Mountain Drop', 'East Death Mountain (Bottom)'),
                                  ('Spiral Cave Ledge Access', 'Spiral Cave Ledge'),
                                  ('Spiral Cave Ledge Drop', 'East Death Mountain (Bottom)'),
                                  ('Spiral Cave (top to bottom)', 'Spiral Cave (Bottom)'),
                                  ('Hookshot Cave Bomb Wall (South)', 'Hookshot Cave (Upper)'),
                                  ('Hookshot Cave Bomb Wall (North)', 'Hookshot Cave'),
                                  ('East Death Mountain (Top)', 'East Death Mountain (Top)'),
                                  ('Death Mountain (Top)', 'Death Mountain (Top)'),
                                  ('Death Mountain Drop', 'Death Mountain'),
                                  ('Tower of Hera Small Key Door', 'Tower of Hera (Basement)'),
                                  ('Tower of Hera Big Key Door', 'Tower of Hera (Top)'),
                                  ('Dark Lake Hylia Drop (East)', 'Dark Lake Hylia'),
                                  ('Dark Lake Hylia Drop (South)', 'Dark Lake Hylia'),
                                  ('Dark Lake Hylia Teleporter', 'Dark Lake Hylia'),
                                  ('Dark Lake Hylia Ledge Pier', 'Dark Lake Hylia Ledge'),
                                  ('Dark Lake Hylia Ledge Drop', 'Dark Lake Hylia'),
                                  ('Ice Palace Missing Wall', 'Dark Lake Hylia Central Island'),
                                  ('Dark Lake Hylia Shallows', 'Dark Lake Hylia'),
                                  ('East Dark World Pier', 'East Dark World'),
                                  ('South Dark World Bridge', 'South Dark World'),
                                  ('East Dark World Bridge', 'East Dark World'),
                                  ('Village of Outcasts Heavy Rock', 'West Dark World'),
                                  ('Village of Outcasts Drop', 'South Dark World'),
                                  ('Village of Outcasts Eastern Rocks', 'Hammer Peg Area'),
                                  ('Village of Outcasts Pegs', 'Dark Grassy Lawn'),
                                  ('Peg Area Rocks', 'West Dark World'),
                                  ('Grassy Lawn Pegs', 'West Dark World'),
                                  ('East Dark World River Pier', 'Northeast Dark World'),
                                  ('West Dark World Gap', 'West Dark World'),
                                  ('East Dark World Broken Bridge Pass', 'East Dark World'),
                                  ('Northeast Dark World Broken Bridge Pass', 'Northeast Dark World'),
                                  ('Catfish Exit Rock', 'Northeast Dark World'),
                                  ('Catfish Entrance Rock', 'Catfish'),
                                  ('Bumper Cave Entrance Rock', 'Bumper Cave Entrance'),
                                  ('Bumper Cave Entrance Drop', 'West Dark World'),
                                  ('Bumper Cave Ledge Drop', 'West Dark World'),
                                  ('Skull Woods Forest', 'Skull Woods Forest'),
                                  ('Paradox Cave Push Block Reverse', 'Paradox Cave Chest Area'),
                                  ('Paradox Cave Push Block', 'Paradox Cave Front'),
                                  ('Paradox Cave Bomb Jump', 'Paradox Cave'),
                                  ('Paradox Cave Drop', 'Paradox Cave Chest Area'),
                                  ('Light World Death Mountain Shop', 'Light World Death Mountain Shop'),
                                  ('Fairy Ascension Rocks', 'Fairy Ascension Plateau'),
                                  ('Fairy Ascension Drop', 'East Death Mountain (Bottom)'),
                                  ('Fairy Ascension Ledge Drop', 'Fairy Ascension Plateau'),
                                  ('Fairy Ascension Ledge Access', 'Fairy Ascension Ledge'),
                                  ('Fairy Ascension Cave Climb', 'Fairy Ascension Cave (Top)'),
                                  ('Fairy Ascension Cave Pots', 'Fairy Ascension Cave (Bottom)'),
                                  ('Fairy Ascension Cave Drop', 'Fairy Ascension Cave (Drop)'),
                                  ('Dark Death Mountain Drop (East)', 'Dark Death Mountain (East Bottom)'),
                                  ('Superbunny Cave Climb', 'Superbunny Cave (Top)'),
                                  ('Swamp Palace Moat', 'Swamp Palace (First Room)'),
                                  ('Swamp Palace Small Key Door', 'Swamp Palace (Starting Area)'),
                                  ('Swamp Palace (Center)', 'Swamp Palace (Center)'),
                                  ('Swamp Palace (West)', 'Swamp Palace (West)'),
                                  ('Swamp Palace (North)', 'Swamp Palace (North)'),
                                  ('Thieves Town Big Key Door', 'Thieves Town (Deep)'),
                                  ('Skull Woods Torch Room', 'Skull Woods Final Section (Mothula)'),
                                  ('Skull Woods First Section Bomb Jump', 'Skull Woods First Section (Top)'),
                                  ('Skull Woods First Section South Door', 'Skull Woods First Section (Right)'),
                                  ('Skull Woods First Section West Door', 'Skull Woods First Section (Left)'),
                                  ('Skull Woods First Section (Right) North Door', 'Skull Woods First Section'),
                                  ('Skull Woods First Section (Left) Door to Right', 'Skull Woods First Section (Right)'),
                                  ('Skull Woods First Section (Left) Door to Exit', 'Skull Woods First Section'),
                                  ('Skull Woods First Section (Top) One-Way Path', 'Skull Woods First Section'),
                                  ('Skull Woods Second Section (Drop)', 'Skull Woods Second Section'),
                                  ('Blind Fight', 'Blind Fight'),
                                  ('Desert Palace Pots (Outer)', 'Desert Palace Main (Inner)'),
                                  ('Desert Palace Pots (Inner)', 'Desert Palace Main (Outer)'),
                                  ('Ice Palace (Main)', 'Ice Palace (Main)'),
                                  ('Ice Palace (Second Section)', 'Ice Palace (Second Section)'),
                                  ('Ice Palace (East)', 'Ice Palace (East)'),
                                  ('Ice Palace (East Top)', 'Ice Palace (East Top)'),
                                  ('Ice Palace (Kholdstare)', 'Ice Palace (Kholdstare)'),
                                  ('Misery Mire Entrance Gap', 'Misery Mire (Main)'),
                                  ('Misery Mire (West)', 'Misery Mire (West)'),
                                  ('Misery Mire Big Key Door', 'Misery Mire (Final Area)'),
                                  ('Misery Mire (Vitreous)', 'Misery Mire (Vitreous)'),
                                  ('Turtle Rock Entrance Gap', 'Turtle Rock (First Section)'),
                                  ('Turtle Rock Entrance Gap Reverse', 'Turtle Rock (Entrance)'),
                                  ('Turtle Rock Entrance to Pokey Room', 'Turtle Rock (Pokey Room)'),
                                  ('Turtle Rock (Pokey Room) (South)', 'Turtle Rock (First Section)'),
                                  ('Turtle Rock (Pokey Room) (North)', 'Turtle Rock (Chain Chomp Room)'),
                                  ('Turtle Rock (Chain Chomp Room) (North)', 'Turtle Rock (Second Section)'),
                                  ('Turtle Rock (Chain Chomp Room) (South)', 'Turtle Rock (Pokey Room)'),
                                  ('Turtle Rock Chain Chomp Staircase', 'Turtle Rock (Chain Chomp Room)'),
                                  ('Turtle Rock (Big Chest) (North)', 'Turtle Rock (Second Section)'),
                                  ('Turtle Rock Big Key Door', 'Turtle Rock (Crystaroller Room)'),
                                  ('Turtle Rock Big Key Door Reverse', 'Turtle Rock (Second Section)'),
                                  ('Turtle Rock Dark Room Staircase', 'Turtle Rock (Dark Room)'),
                                  ('Turtle Rock (Dark Room) (North)', 'Turtle Rock (Crystaroller Room)'),
                                  ('Turtle Rock (Dark Room) (South)', 'Turtle Rock (Eye Bridge)'),
                                  ('Turtle Rock Dark Room (South)', 'Turtle Rock (Dark Room)'),
                                  ('Turtle Rock Second Section Bomb Wall', 'Turtle Rock (Second Section Bomb Wall)'),
                                  ('Turtle Rock Second Section from Bomb Wall', 'Turtle Rock (Second Section)'),
                                  ('Turtle Rock Eye Bridge Bomb Wall', 'Turtle Rock (Eye Bridge Bomb Wall)'),
                                  ('Turtle Rock Eye Bridge from Bomb Wall', 'Turtle Rock (Eye Bridge)'),
                                  ('Turtle Rock (Trinexx)', 'Turtle Rock (Trinexx)'),
                                  ('Palace of Darkness Bridge Room', 'Palace of Darkness (Center)'),
                                  ('Palace of Darkness Bonk Wall', 'Palace of Darkness (Bonk Section)'),
                                  ('Palace of Darkness Big Key Chest Staircase', 'Palace of Darkness (Big Key Chest)'),
                                  ('Palace of Darkness (North)', 'Palace of Darkness (North)'),
                                  ('Palace of Darkness Big Key Door', 'Palace of Darkness (Final Section)'),
                                  ('Palace of Darkness Hammer Peg Drop', 'Palace of Darkness (Center)'),
                                  ('Palace of Darkness Spike Statue Room Door', 'Palace of Darkness (Harmless Hellway)'),
                                  ('Palace of Darkness Maze Door', 'Palace of Darkness (Maze)'),
                                  ('Ganons Tower (Tile Room)', 'Ganons Tower (Tile Room)'),
                                  ('Ganons Tower (Tile Room) Key Door', 'Ganons Tower (Compass Room)'),
                                  ('Ganons Tower (Bottom) (East)', 'Ganons Tower (Bottom)'),
                                  ('Ganons Tower (Hookshot Room)', 'Ganons Tower (Hookshot Room)'),
                                  ('Ganons Tower (Map Room)', 'Ganons Tower (Map Room)'),
                                  ('Ganons Tower (Double Switch Room)', 'Ganons Tower (Firesnake Room)'),
                                  ('Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)'),
                                  ('Ganons Tower (Bottom) (West)', 'Ganons Tower (Bottom)'),
                                  ('Ganons Tower Big Key Door', 'Ganons Tower (Top)'),
                                  ('Ganons Tower Torch Rooms', 'Ganons Tower (Before Moldorm)'),
                                  ('Ganons Tower Moldorm Door', 'Ganons Tower (Moldorm)'),
                                  ('Ganons Tower Moldorm Gap', 'Agahnim 2'),
                                  ('Ganon Drop', 'Bottom of Pyramid'),
                                  ('Pyramid Drop', 'East Dark World'),
                                  ('Post Aga Teleporter', 'Light World'),
                                  ('Secret Passage Inner Bushes', 'Light World'),
                                  ('Secret Passage Outer Bushes', 'Hyrule Castle Secret Entrance Area'),
                                  ('Potion Shop Inner Bushes', 'Light World'),
                                  ('Potion Shop Outer Bushes', 'Potion Shop Area'),
                                  ('Potion Shop Inner Rock', 'Northeast Light World'),
                                  ('Potion Shop Outer Rock', 'Potion Shop Area'),
                                  ('Potion Shop River Drop', 'River'),
                                  ('Graveyard Cave Inner Bushes', 'Light World'),
                                  ('Graveyard Cave Outer Bushes', 'Graveyard Cave Area'),
                                  ('Graveyard Cave Mirror Spot', 'West Dark World'),
                                  ('Light World River Drop', 'River'),
                                  ('Light World Pier', 'Light World'),
                                  ('Potion Shop Pier', 'Potion Shop Area'),
                                  ('Hyrule Castle Ledge Courtyard Drop', 'Light World'),
                                  ('Mimic Cave Ledge Access', 'Mimic Cave Ledge'),
                                  ('Mimic Cave Ledge Drop', 'East Death Mountain (Bottom)'),
                                  ('Turtle Rock Tail Drop', 'Turtle Rock (Top)'),
                                  ('Turtle Rock Drop', 'Dark Death Mountain'),
                                  ('Desert Ledge Drop', 'Light World'),
                                  ('Floating Island Drop', 'Dark Death Mountain'),
                                  ('Dark Lake Hylia Central Island Teleporter', 'Lake Hylia Central Island'),
                                  ('Dark Desert Teleporter', 'Light World'),
                                  ('East Dark World Teleporter', 'Light World'),
                                  ('South Dark World Teleporter', 'Light World'),
                                  ('West Dark World Teleporter', 'Light World'),
                                  ('Dark Death Mountain Teleporter (West)', 'Death Mountain'),
                                  ('Dark Death Mountain Teleporter (East)', 'East Death Mountain (Top)'),
                                  ('Dark Death Mountain Teleporter (East Bottom)', 'East Death Mountain (Bottom)'),
                                  ('Mire Mirror Spot', 'Dark Desert'),
                                  ('Dark Desert Drop', 'Dark Desert'),
                                  ('Desert Palace Stairs Mirror Spot', 'Dark Desert'),
                                  ('Desert Palace North Mirror Spot', 'Dark Desert'),
                                  ('Maze Race Mirror Spot', 'West Dark World'),
                                  ('Lake Hylia Central Island Mirror Spot', 'Dark Lake Hylia Central Island'),
                                  ('Hammer Peg Area Mirror Spot', 'Hammer Peg Area'),
                                  ('Bumper Cave Ledge Mirror Spot', 'Bumper Cave Ledge'),
                                  ('Bumper Cave Entrance Mirror Spot', 'Bumper Cave Entrance'),
                                  ('Death Mountain Mirror Spot', 'Dark Death Mountain'),
                                  ('East Death Mountain Mirror Spot (Top)', 'Dark Death Mountain'),
                                  ('East Death Mountain Mirror Spot (Bottom)', 'Dark Death Mountain (East Bottom)'),
                                  ('Death Mountain (Top) Mirror Spot', 'Dark Death Mountain'),
                                  ('Dark Death Mountain Ledge Mirror Spot (East)', 'Dark Death Mountain Ledge'),
                                  ('Dark Death Mountain Ledge Mirror Spot (West)', 'Dark Death Mountain Ledge'),
                                  ('Floating Island Mirror Spot', 'Death Mountain Floating Island (Dark World)'),
                                  ('Laser Bridge Mirror Spot', 'Dark Death Mountain Isolated Ledge'),
                                  ('East Dark World Mirror Spot', 'East Dark World'),
                                  ('West Dark World Mirror Spot', 'West Dark World'),
                                  ('South Dark World Mirror Spot', 'South Dark World'),
                                  ('Potion Shop Mirror Spot', 'Northeast Dark World'),
                                  ('Catfish Mirror Spot', 'Catfish'),
                                  ('Shopping Mall Mirror Spot', 'Dark Lake Hylia Ledge'),
                                  ('Skull Woods Mirror Spot', 'Skull Woods Forest (West)'),
                                  ('DDM Flute', 'The Sky'),
                                  ('DDM Landing', 'Dark Death Mountain'),
                                  ('NEDW Flute', 'The Sky'),
                                  ('NEDW Landing', 'Northeast Dark World'),
                                  ('WDW Flute', 'The Sky'),
                                  ('WDW Landing', 'West Dark World'),
                                  ('SDW Flute', 'The Sky'),
                                  ('SDW Landing', 'South Dark World'),
                                  ('EDW Flute', 'The Sky'),
                                  ('EDW Landing', 'East Dark World'),
                                  ('DLHL Flute', 'The Sky'),
                                  ('DLHL Landing', 'Dark Lake Hylia Ledge'),
                                  ('DD Flute', 'The Sky'),
                                  ('DD Landing', 'Dark Desert Ledge'),
                                  ('EDDM Flute', 'The Sky'),
                                  ('Dark Grassy Lawn Flute', 'The Sky'),
                                  ('Hammer Peg Area Flute', 'The Sky'),
                                  ('Chris Houlihan Room Exit', 'Pyramid Ledge'),
                                  ('Bush Covered Lawn Inner Bushes', 'Light World'),
                                  ('Bush Covered Lawn Outer Bushes', 'Bush Covered Lawn'),
                                  ('Bush Covered Lawn Mirror Spot', 'Dark Grassy Lawn'),
                                  ('Bomb Hut Inner Bushes', 'Light World'),
                                  ('Bomb Hut Outer Bushes', 'Bomb Hut Area'),
                                  ('Bomb Hut Mirror Spot', 'West Dark World')]
# non-shuffled entrance links
default_connections = [('Waterfall of Wishing', 'Waterfall of Wishing'),
                       ("Blinds Hideout", "Blinds Hideout"),
                       ('Dam', 'Dam'),
                       ('Lumberjack House', 'Lumberjack House'),
                       ("Hyrule Castle Secret Entrance Drop", "Hyrule Castle Secret Entrance"),
                       ("Hyrule Castle Secret Entrance Stairs", "Hyrule Castle Secret Entrance"),
                       ("Hyrule Castle Secret Entrance Exit", "Hyrule Castle Courtyard"),
                       ('Bonk Fairy (Light)', 'Bonk Fairy (Light)'),
                       ('Lake Hylia Fairy', 'Lake Hylia Healer Fairy'),
                       ('Lake Hylia Fortune Teller', 'Lake Hylia Fortune Teller'),
                       ('Light Hype Fairy', 'Swamp Healer Fairy'),
                       ('Desert Fairy', 'Desert Healer Fairy'),
                       ('Kings Grave', 'Kings Grave'),
                       ('Tavern North', 'Tavern'),
                       ('Chicken House', 'Chicken House'),
                       ('Aginahs Cave', 'Aginahs Cave'),
                       ('Sahasrahlas Hut', 'Sahasrahlas Hut'),
                       ('Cave Shop (Lake Hylia)', 'Cave Shop (Lake Hylia)'),
                       ('Capacity Upgrade', 'Capacity Upgrade'),
                       ('Kakariko Well Drop', 'Kakariko Well (top)'),
                       ('Kakariko Well Cave', 'Kakariko Well (bottom)'),
                       ('Kakariko Well Exit', 'Light World'),
                       ('Blacksmiths Hut', 'Blacksmiths Hut'),
                       ('Bat Cave Drop', 'Bat Cave (right)'),
                       ('Bat Cave Cave', 'Bat Cave (left)'),
                       ('Bat Cave Exit', 'Light World'),
                       ('Sick Kids House', 'Sick Kids House'),
                       ('Elder House (East)', 'Elder House'),
                       ('Elder House (West)', 'Elder House'),
                       ('Elder House Exit (East)', 'Light World'),
                       ('Elder House Exit (West)', 'Light World'),
                       ('North Fairy Cave Drop', 'North Fairy Cave'),
                       ('North Fairy Cave', 'North Fairy Cave'),
                       ('North Fairy Cave Exit', 'Light World'),
                       ('Lost Woods Gamble', 'Lost Woods Gamble'),
                       ('Fortune Teller (Light)', 'Fortune Teller (Light)'),
                       ('Snitch Lady (East)', 'Snitch Lady (East)'),
                       ('Snitch Lady (West)', 'Snitch Lady (West)'),
                       ('Bush Covered House', 'Bush Covered House'),
                       ('Tavern (Front)', 'Tavern (Front)'),
                       ('Light World Bomb Hut', 'Light World Bomb Hut'),
                       ('Kakariko Shop', 'Kakariko Shop'),
                       ('Lost Woods Hideout Drop', 'Lost Woods Hideout (top)'),
                       ('Lost Woods Hideout Stump', 'Lost Woods Hideout (bottom)'),
                       ('Lost Woods Hideout Exit', 'Light World'),
                       ('Lumberjack Tree Tree', 'Lumberjack Tree (top)'),
                       ('Lumberjack Tree Cave', 'Lumberjack Tree (bottom)'),
                       ('Lumberjack Tree Exit', 'Light World'),
                       ('Cave 45', 'Cave 45'),
                       ('Graveyard Cave', 'Graveyard Cave'),
                       ('Checkerboard Cave', 'Checkerboard Cave'),
                       ('Mini Moldorm Cave', 'Mini Moldorm Cave'),
                       ('Long Fairy Cave', 'Long Fairy Cave'),  # near East Light World Teleporter
                       ('Good Bee Cave', 'Good Bee Cave'),
                       ('20 Rupee Cave', '20 Rupee Cave'),
                       ('50 Rupee Cave', '50 Rupee Cave'),
                       ('Ice Rod Cave', 'Ice Rod Cave'),
                       ('Bonk Rock Cave', 'Bonk Rock Cave'),
                       ('Library', 'Library'),
                       ('Kakariko Gamble Game', 'Kakariko Gamble Game'),
                       ('Potion Shop', 'Potion Shop'),
                       ('Two Brothers House (East)', 'Two Brothers House'),
                       ('Two Brothers House (West)', 'Two Brothers House'),
                       ('Two Brothers House Exit (East)', 'Light World'),
                       ('Two Brothers House Exit (West)', 'Maze Race Ledge'),

                       ('Sanctuary', 'Sanctuary'),
                       ('Sanctuary Grave', 'Sewer Drop'),
                       ('Sanctuary Exit', 'Light World'),

                       ('Old Man Cave (West)', 'Old Man Cave'),
                       ('Old Man Cave (East)', 'Old Man Cave'),
                       ('Old Man Cave Exit (West)', 'Light World'),
                       ('Old Man Cave Exit (East)', 'Death Mountain'),
                       ('Old Man House (Bottom)', 'Old Man House'),
                       ('Old Man House Exit (Bottom)', 'Death Mountain'),
                       ('Old Man House (Top)', 'Old Man House Back'),
                       ('Old Man House Exit (Top)', 'Death Mountain'),
                       ('Death Mountain Return Cave (East)', 'Death Mountain Return Cave'),
                       ('Death Mountain Return Cave (West)', 'Death Mountain Return Cave'),
                       ('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Ledge'),
                       ('Death Mountain Return Cave Exit (East)', 'Death Mountain'),
                       ('Spectacle Rock Cave Peak', 'Spectacle Rock Cave (Peak)'),
                       ('Spectacle Rock Cave (Bottom)', 'Spectacle Rock Cave (Bottom)'),
                       ('Spectacle Rock Cave', 'Spectacle Rock Cave (Top)'),
                       ('Spectacle Rock Cave Exit', 'Death Mountain'),
                       ('Spectacle Rock Cave Exit (Top)', 'Death Mountain'),
                       ('Spectacle Rock Cave Exit (Peak)', 'Death Mountain'),
                       ('Paradox Cave (Bottom)', 'Paradox Cave Front'),
                       ('Paradox Cave (Middle)', 'Paradox Cave'),
                       ('Paradox Cave (Top)', 'Paradox Cave'),
                       ('Paradox Cave Exit (Bottom)', 'East Death Mountain (Bottom)'),
                       ('Paradox Cave Exit (Middle)', 'East Death Mountain (Bottom)'),
                       ('Paradox Cave Exit (Top)', 'East Death Mountain (Top)'),
                       ('Hookshot Fairy', 'Hookshot Fairy'),
                       ('Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave (Bottom)'),
                       ('Fairy Ascension Cave (Top)', 'Fairy Ascension Cave (Top)'),
                       ('Fairy Ascension Cave Exit (Bottom)', 'Fairy Ascension Plateau'),
                       ('Fairy Ascension Cave Exit (Top)', 'Fairy Ascension Ledge'),
                       ('Spiral Cave', 'Spiral Cave (Top)'),
                       ('Spiral Cave (Bottom)', 'Spiral Cave (Bottom)'),
                       ('Spiral Cave Exit', 'East Death Mountain (Bottom)'),
                       ('Spiral Cave Exit (Top)', 'Spiral Cave Ledge'),

                       ('Pyramid Fairy', 'Pyramid Fairy'),
                       ('East Dark World Hint', 'East Dark World Hint'),
                       ('Palace of Darkness Hint', 'Palace of Darkness Hint'),
                       ('Big Bomb Shop', 'Big Bomb Shop'),
                       ('Dark Lake Hylia Shop', 'Dark Lake Hylia Shop'),
                       ('Dark Lake Hylia Fairy', 'Dark Lake Hylia Healer Fairy'),
                       ('Dark Lake Hylia Ledge Fairy', 'Dark Lake Hylia Ledge Healer Fairy'),
                       ('Dark Lake Hylia Ledge Spike Cave', 'Dark Lake Hylia Ledge Spike Cave'),
                       ('Dark Lake Hylia Ledge Hint', 'Dark Lake Hylia Ledge Hint'),
                       ('Hype Cave', 'Hype Cave'),
                       ('Bonk Fairy (Dark)', 'Bonk Fairy (Dark)'),
                       ('Brewery', 'Brewery'),
                       ('C-Shaped House', 'C-Shaped House'),
                       ('Chest Game', 'Chest Game'),
                       ('Dark World Hammer Peg Cave', 'Dark World Hammer Peg Cave'),
                       ('Bumper Cave (Bottom)', 'Bumper Cave'),
                       ('Bumper Cave (Top)', 'Bumper Cave'),
                       ('Red Shield Shop', 'Red Shield Shop'),
                       ('Dark Sanctuary Hint', 'Dark Sanctuary Hint'),
                       ('Fortune Teller (Dark)', 'Fortune Teller (Dark)'),
                       ('Village of Outcasts Shop', 'Village of Outcasts Shop'),
                       ('Dark World Lumberjack Shop', 'Dark World Lumberjack Shop'),
                       ('Dark World Potion Shop', 'Dark World Potion Shop'),
                       ('Archery Game', 'Archery Game'),
                       ('Bumper Cave Exit (Top)', 'Bumper Cave Ledge'),
                       ('Bumper Cave Exit (Bottom)', 'West Dark World'),
                       ('Mire Shed', 'Mire Shed'),
                       ('Dark Desert Hint', 'Dark Desert Hint'),
                       ('Dark Desert Fairy', 'Dark Desert Healer Fairy'),
                       ('Spike Cave', 'Spike Cave'),
                       ('Hookshot Cave', 'Hookshot Cave'),
                       ('Superbunny Cave (Top)', 'Superbunny Cave (Top)'),
                       ('Cave Shop (Dark Death Mountain)', 'Cave Shop (Dark Death Mountain)'),
                       ('Dark Death Mountain Fairy', 'Dark Death Mountain Healer Fairy'),
                       ('Superbunny Cave (Bottom)', 'Superbunny Cave (Bottom)'),
                       ('Superbunny Cave Exit (Top)', 'Dark Death Mountain (Top)'),
                       ('Superbunny Cave Exit (Bottom)', 'Dark Death Mountain (East Bottom)'),
                       ('Hookshot Cave Exit (South)', 'Dark Death Mountain (Top)'),
                       ('Hookshot Cave Exit (North)', 'Death Mountain Floating Island (Dark World)'),
                       ('Hookshot Cave Back Entrance', 'Hookshot Cave (Upper)'),
                       ('Mimic Cave', 'Mimic Cave'),

                       ('Pyramid Hole', 'Pyramid'),
                       ('Pyramid Exit', 'Pyramid Ledge'),
                       ('Pyramid Entrance', 'Bottom of Pyramid')
                      ]

inverted_default_connections =  [('Waterfall of Wishing', 'Waterfall of Wishing'),
                                 ('Blinds Hideout', 'Blinds Hideout'),
                                 ('Dam', 'Dam'),
                                 ('Lumberjack House', 'Lumberjack House'),
                                 ('Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance'),
                                 ('Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance'),
                                 ('Hyrule Castle Secret Entrance Exit', 'Light World'),
                                 ('Bonk Fairy (Light)', 'Bonk Fairy (Light)'),
                                 ('Lake Hylia Fairy', 'Lake Hylia Healer Fairy'),
                                 ('Lake Hylia Fortune Teller', 'Lake Hylia Fortune Teller'),
                                 ('Light Hype Fairy', 'Swamp Healer Fairy'),
                                 ('Desert Fairy', 'Desert Healer Fairy'),
                                 ('Kings Grave', 'Kings Grave'),
                                 ('Tavern North', 'Tavern'),
                                 ('Chicken House', 'Chicken House'),
                                 ('Aginahs Cave', 'Aginahs Cave'),
                                 ('Sahasrahlas Hut', 'Sahasrahlas Hut'),
                                 ('Cave Shop (Lake Hylia)', 'Cave Shop (Lake Hylia)'),
                                 ('Capacity Upgrade', 'Capacity Upgrade'),
                                 ('Kakariko Well Drop', 'Kakariko Well (top)'),
                                 ('Kakariko Well Cave', 'Kakariko Well (bottom)'),
                                 ('Kakariko Well Exit', 'Light World'),
                                 ('Blacksmiths Hut', 'Blacksmiths Hut'),
                                 ('Bat Cave Drop', 'Bat Cave (right)'),
                                 ('Bat Cave Cave', 'Bat Cave (left)'),
                                 ('Bat Cave Exit', 'Light World'),
                                 ('Sick Kids House', 'Sick Kids House'),
                                 ('Elder House (East)', 'Elder House'),
                                 ('Elder House (West)', 'Elder House'),
                                 ('Elder House Exit (East)', 'Light World'),
                                 ('Elder House Exit (West)', 'Light World'),
                                 ('North Fairy Cave Drop', 'North Fairy Cave'),
                                 ('North Fairy Cave', 'North Fairy Cave'),
                                 ('North Fairy Cave Exit', 'Light World'),
                                 ('Lost Woods Gamble', 'Lost Woods Gamble'),
                                 ('Fortune Teller (Light)', 'Fortune Teller (Light)'),
                                 ('Snitch Lady (East)', 'Snitch Lady (East)'),
                                 ('Snitch Lady (West)', 'Snitch Lady (West)'),
                                 ('Bush Covered House', 'Bush Covered House'),
                                 ('Tavern (Front)', 'Tavern (Front)'),
                                 ('Light World Bomb Hut', 'Light World Bomb Hut'),
                                 ('Kakariko Shop', 'Kakariko Shop'),
                                 ('Lost Woods Hideout Drop', 'Lost Woods Hideout (top)'),
                                 ('Lost Woods Hideout Stump', 'Lost Woods Hideout (bottom)'),
                                 ('Lost Woods Hideout Exit', 'Light World'),
                                 ('Lumberjack Tree Tree', 'Lumberjack Tree (top)'),
                                 ('Lumberjack Tree Cave', 'Lumberjack Tree (bottom)'),
                                 ('Lumberjack Tree Exit', 'Light World'),
                                 ('Cave 45', 'Cave 45'),
                                 ('Graveyard Cave', 'Graveyard Cave'),
                                 ('Checkerboard Cave', 'Checkerboard Cave'),
                                 ('Mini Moldorm Cave', 'Mini Moldorm Cave'),
                                 ('Long Fairy Cave', 'Long Fairy Cave'),
                                 ('Good Bee Cave', 'Good Bee Cave'),
                                 ('20 Rupee Cave', '20 Rupee Cave'),
                                 ('50 Rupee Cave', '50 Rupee Cave'),
                                 ('Ice Rod Cave', 'Ice Rod Cave'),
                                 ('Bonk Rock Cave', 'Bonk Rock Cave'),
                                 ('Library', 'Library'),
                                 ('Kakariko Gamble Game', 'Kakariko Gamble Game'),
                                 ('Potion Shop', 'Potion Shop'),
                                 ('Two Brothers House (East)', 'Two Brothers House'),
                                 ('Two Brothers House (West)', 'Two Brothers House'),
                                 ('Two Brothers House Exit (East)', 'Light World'),
                                 ('Two Brothers House Exit (West)', 'Maze Race Ledge'),
                                 ('Sanctuary', 'Sanctuary'),
                                 ('Sanctuary Grave', 'Sewer Drop'),
                                 ('Sanctuary Exit', 'Light World'),
                                 ('Old Man House (Bottom)', 'Old Man House'),
                                 ('Old Man House Exit (Bottom)', 'Death Mountain'),
                                 ('Old Man House (Top)', 'Old Man House Back'),
                                 ('Old Man House Exit (Top)', 'Death Mountain'),
                                 ('Spectacle Rock Cave Peak', 'Spectacle Rock Cave (Peak)'),
                                 ('Spectacle Rock Cave (Bottom)', 'Spectacle Rock Cave (Bottom)'),
                                 ('Spectacle Rock Cave', 'Spectacle Rock Cave (Top)'),
                                 ('Spectacle Rock Cave Exit', 'Death Mountain'),
                                 ('Spectacle Rock Cave Exit (Top)', 'Death Mountain'),
                                 ('Spectacle Rock Cave Exit (Peak)', 'Death Mountain'),
                                 ('Paradox Cave (Bottom)', 'Paradox Cave Front'),
                                 ('Paradox Cave (Middle)', 'Paradox Cave'),
                                 ('Paradox Cave (Top)', 'Paradox Cave'),
                                 ('Paradox Cave Exit (Bottom)', 'East Death Mountain (Bottom)'),
                                 ('Paradox Cave Exit (Middle)', 'East Death Mountain (Bottom)'),
                                 ('Paradox Cave Exit (Top)', 'East Death Mountain (Top)'),
                                 ('Hookshot Fairy', 'Hookshot Fairy'),
                                 ('Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave (Bottom)'),
                                 ('Fairy Ascension Cave (Top)', 'Fairy Ascension Cave (Top)'),
                                 ('Fairy Ascension Cave Exit (Bottom)', 'Fairy Ascension Plateau'),
                                 ('Fairy Ascension Cave Exit (Top)', 'Fairy Ascension Ledge'),
                                 ('Spiral Cave', 'Spiral Cave (Top)'),
                                 ('Spiral Cave (Bottom)', 'Spiral Cave (Bottom)'),
                                 ('Spiral Cave Exit', 'East Death Mountain (Bottom)'),
                                 ('Spiral Cave Exit (Top)', 'Spiral Cave Ledge'),
                                 ('Pyramid Fairy', 'Pyramid Fairy'),
                                 ('East Dark World Hint', 'East Dark World Hint'),
                                 ('Palace of Darkness Hint', 'Palace of Darkness Hint'),
                                 ('Dark Lake Hylia Shop', 'Dark Lake Hylia Shop'),
                                 ('Dark Lake Hylia Fairy', 'Dark Lake Hylia Healer Fairy'),
                                 ('Dark Lake Hylia Ledge Fairy', 'Dark Lake Hylia Ledge Healer Fairy'),
                                 ('Dark Lake Hylia Ledge Spike Cave', 'Dark Lake Hylia Ledge Spike Cave'),
                                 ('Dark Lake Hylia Ledge Hint', 'Dark Lake Hylia Ledge Hint'),
                                 ('Hype Cave', 'Hype Cave'),
                                 ('Bonk Fairy (Dark)', 'Bonk Fairy (Dark)'),
                                 ('Brewery', 'Brewery'),
                                 ('C-Shaped House', 'C-Shaped House'),
                                 ('Chest Game', 'Chest Game'),
                                 ('Dark World Hammer Peg Cave', 'Dark World Hammer Peg Cave'),
                                 ('Red Shield Shop', 'Red Shield Shop'),
                                 ('Fortune Teller (Dark)', 'Fortune Teller (Dark)'),
                                 ('Village of Outcasts Shop', 'Village of Outcasts Shop'),
                                 ('Dark World Lumberjack Shop', 'Dark World Lumberjack Shop'),
                                 ('Dark World Potion Shop', 'Dark World Potion Shop'),
                                 ('Archery Game', 'Archery Game'),
                                 ('Mire Shed', 'Mire Shed'),
                                 ('Dark Desert Hint', 'Dark Desert Hint'),
                                 ('Dark Desert Fairy', 'Dark Desert Healer Fairy'),
                                 ('Spike Cave', 'Spike Cave'),
                                 ('Hookshot Cave', 'Hookshot Cave'),
                                 ('Superbunny Cave (Top)', 'Superbunny Cave (Top)'),
                                 ('Cave Shop (Dark Death Mountain)', 'Cave Shop (Dark Death Mountain)'),
                                 ('Superbunny Cave (Bottom)', 'Superbunny Cave (Bottom)'),
                                 ('Superbunny Cave Exit (Bottom)', 'Dark Death Mountain (East Bottom)'),
                                 ('Hookshot Cave Exit (North)', 'Death Mountain Floating Island (Dark World)'),
                                 ('Hookshot Cave Back Entrance', 'Hookshot Cave (Upper)'),
                                 ('Mimic Cave', 'Mimic Cave'),
                                 ('Inverted Pyramid Hole', 'Pyramid'),
                                 ('Inverted Links House', 'Inverted Links House'),
                                 ('Inverted Links House Exit', 'South Dark World'),
                                 ('Inverted Big Bomb Shop', 'Inverted Big Bomb Shop'),
                                 ('Inverted Dark Sanctuary', 'Inverted Dark Sanctuary'),
                                 ('Inverted Dark Sanctuary Exit', 'West Dark World'),
                                 ('Old Man Cave (West)', 'Bumper Cave'),
                                 ('Old Man Cave (East)', 'Death Mountain Return Cave'),
                                 ('Old Man Cave Exit (West)', 'West Dark World'),
                                 ('Old Man Cave Exit (East)', 'Dark Death Mountain'),
                                 ('Dark Death Mountain Fairy', 'Old Man Cave'),
                                 ('Bumper Cave (Bottom)', 'Old Man Cave'),
                                 ('Bumper Cave (Top)', 'Dark Death Mountain Healer Fairy'),
                                 ('Bumper Cave Exit (Top)', 'Death Mountain Return Ledge'),
                                 ('Bumper Cave Exit (Bottom)', 'Light World'),
                                 ('Death Mountain Return Cave (West)', 'Bumper Cave'),
                                 ('Death Mountain Return Cave (East)', 'Death Mountain Return Cave'),
                                 ('Death Mountain Return Cave Exit (West)', 'Death Mountain'),
                                 ('Death Mountain Return Cave Exit (East)', 'Death Mountain'),
                                 ('Hookshot Cave Exit (South)', 'Dark Death Mountain'),
                                 ('Superbunny Cave Exit (Top)', 'Dark Death Mountain'),
                                 ('Pyramid Exit', 'Light World'),
                                 ('Inverted Pyramid Entrance', 'Bottom of Pyramid')]

# non shuffled dungeons
default_dungeon_connections = [('Desert Palace Entrance (South)', 'Desert Palace Main (Inner)'),
                               ('Desert Palace Entrance (West)', 'Desert Palace Main (Outer)'),
                               ('Desert Palace Entrance (North)', 'Desert Palace North'),
                               ('Desert Palace Entrance (East)', 'Desert Palace Main (Outer)'),
                               ('Desert Palace Exit (South)', 'Desert Palace Stairs'),
                               ('Desert Palace Exit (West)', 'Desert Ledge'),
                               ('Desert Palace Exit (East)', 'Desert Palace Lone Stairs'),
                               ('Desert Palace Exit (North)', 'Desert Palace Entrance (North) Spot'),

                               ('Eastern Palace', 'Eastern Palace'),
                               ('Eastern Palace Exit', 'Light World'),
                               ('Tower of Hera', 'Tower of Hera (Bottom)'),
                               ('Tower of Hera Exit', 'Death Mountain (Top)'),

                               ('Hyrule Castle Entrance (South)', 'Hyrule Castle'),
                               ('Hyrule Castle Entrance (West)', 'Hyrule Castle'),
                               ('Hyrule Castle Entrance (East)', 'Hyrule Castle'),
                               ('Hyrule Castle Exit (South)', 'Hyrule Castle Courtyard'),
                               ('Hyrule Castle Exit (West)', 'Hyrule Castle Ledge'),
                               ('Hyrule Castle Exit (East)', 'Hyrule Castle Ledge'),
                               ('Agahnims Tower', 'Agahnims Tower'),
                               ('Agahnims Tower Exit', 'Hyrule Castle Ledge'),

                               ('Thieves Town', 'Thieves Town (Entrance)'),
                               ('Thieves Town Exit', 'West Dark World'),
                               ('Skull Woods First Section Hole (East)', 'Skull Woods First Section (Right)'),
                               ('Skull Woods First Section Hole (West)', 'Skull Woods First Section (Left)'),
                               ('Skull Woods First Section Hole (North)', 'Skull Woods First Section (Top)'),
                               ('Skull Woods First Section Door', 'Skull Woods First Section'),
                               ('Skull Woods First Section Exit', 'Skull Woods Forest'),
                               ('Skull Woods Second Section Hole', 'Skull Woods Second Section (Drop)'),
                               ('Skull Woods Second Section Door (East)', 'Skull Woods Second Section'),
                               ('Skull Woods Second Section Door (West)', 'Skull Woods Second Section'),
                               ('Skull Woods Second Section Exit (East)', 'Skull Woods Forest'),
                               ('Skull Woods Second Section Exit (West)', 'Skull Woods Forest (West)'),
                               ('Skull Woods Final Section', 'Skull Woods Final Section (Entrance)'),
                               ('Skull Woods Final Section Exit', 'Skull Woods Forest (West)'),
                               ('Ice Palace', 'Ice Palace (Entrance)'),
                               ('Ice Palace Exit', 'Dark Lake Hylia Central Island'),
                               ('Misery Mire', 'Misery Mire (Entrance)'),
                               ('Misery Mire Exit', 'Dark Desert'),
                               ('Palace of Darkness', 'Palace of Darkness (Entrance)'),
                               ('Palace of Darkness Exit', 'East Dark World'),
                               ('Swamp Palace', 'Swamp Palace (Entrance)'),  # requires additional patch for flooding moat if moved
                               ('Swamp Palace Exit', 'South Dark World'),

                               ('Turtle Rock', 'Turtle Rock (Entrance)'),
                               ('Turtle Rock Exit (Front)', 'Dark Death Mountain (Top)'),
                               ('Turtle Rock Ledge Exit (West)', 'Dark Death Mountain Ledge'),
                               ('Turtle Rock Ledge Exit (East)', 'Dark Death Mountain Ledge'),
                               ('Dark Death Mountain Ledge (West)', 'Turtle Rock (Second Section)'),
                               ('Dark Death Mountain Ledge (East)', 'Turtle Rock (Big Chest)'),
                               ('Turtle Rock Isolated Ledge Exit', 'Dark Death Mountain Isolated Ledge'),
                               ('Turtle Rock Isolated Ledge Entrance', 'Turtle Rock (Eye Bridge)'),

                               ('Ganons Tower', 'Ganons Tower (Entrance)'),
                               ('Ganons Tower Exit', 'Dark Death Mountain (Top)')
                              ]

inverted_default_dungeon_connections = [('Desert Palace Entrance (South)', 'Desert Palace Main (Inner)'),
                                        ('Desert Palace Entrance (West)', 'Desert Palace Main (Outer)'),
                                        ('Desert Palace Entrance (North)', 'Desert Palace North'),
                                        ('Desert Palace Entrance (East)', 'Desert Palace Main (Outer)'),
                                        ('Desert Palace Exit (South)', 'Desert Palace Stairs'),
                                        ('Desert Palace Exit (West)', 'Desert Ledge'),
                                        ('Desert Palace Exit (East)', 'Desert Palace Lone Stairs'),
                                        ('Desert Palace Exit (North)', 'Desert Palace Entrance (North) Spot'),
                                        ('Eastern Palace', 'Eastern Palace'),
                                        ('Eastern Palace Exit', 'Light World'),
                                        ('Tower of Hera', 'Tower of Hera (Bottom)'),
                                        ('Tower of Hera Exit', 'Death Mountain (Top)'),
                                        ('Hyrule Castle Entrance (South)', 'Hyrule Castle'),
                                        ('Hyrule Castle Entrance (West)', 'Hyrule Castle'),
                                        ('Hyrule Castle Entrance (East)', 'Hyrule Castle'),
                                        ('Hyrule Castle Exit (South)', 'Light World'),
                                        ('Hyrule Castle Exit (West)', 'Hyrule Castle Ledge'),
                                        ('Hyrule Castle Exit (East)', 'Hyrule Castle Ledge'),
                                        ('Thieves Town', 'Thieves Town (Entrance)'),
                                        ('Thieves Town Exit', 'West Dark World'),
                                        ('Skull Woods First Section Hole (East)', 'Skull Woods First Section (Right)'),
                                        ('Skull Woods First Section Hole (West)', 'Skull Woods First Section (Left)'),
                                        ('Skull Woods First Section Hole (North)', 'Skull Woods First Section (Top)'),
                                        ('Skull Woods First Section Door', 'Skull Woods First Section'),
                                        ('Skull Woods First Section Exit', 'Skull Woods Forest'),
                                        ('Skull Woods Second Section Hole', 'Skull Woods Second Section (Drop)'),
                                        ('Skull Woods Second Section Door (East)', 'Skull Woods Second Section'),
                                        ('Skull Woods Second Section Door (West)', 'Skull Woods Second Section'),
                                        ('Skull Woods Second Section Exit (East)', 'Skull Woods Forest'),
                                        ('Skull Woods Second Section Exit (West)', 'Skull Woods Forest (West)'),
                                        ('Skull Woods Final Section', 'Skull Woods Final Section (Entrance)'),
                                        ('Skull Woods Final Section Exit', 'Skull Woods Forest (West)'),
                                        ('Ice Palace', 'Ice Palace (Entrance)'),
                                        ('Misery Mire', 'Misery Mire (Entrance)'),
                                        ('Misery Mire Exit', 'Dark Desert'),
                                        ('Palace of Darkness', 'Palace of Darkness (Entrance)'),
                                        ('Palace of Darkness Exit', 'East Dark World'),
                                        ('Swamp Palace', 'Swamp Palace (Entrance)'),
                                        ('Swamp Palace Exit', 'South Dark World'),
                                        ('Turtle Rock', 'Turtle Rock (Entrance)'),
                                        ('Turtle Rock Ledge Exit (West)', 'Dark Death Mountain Ledge'),
                                        ('Turtle Rock Ledge Exit (East)', 'Dark Death Mountain Ledge'),
                                        ('Dark Death Mountain Ledge (West)', 'Turtle Rock (Second Section)'),
                                        ('Dark Death Mountain Ledge (East)', 'Turtle Rock (Big Chest)'),
                                        ('Turtle Rock Isolated Ledge Exit', 'Dark Death Mountain Isolated Ledge'),
                                        ('Turtle Rock Isolated Ledge Entrance', 'Turtle Rock (Eye Bridge)'),
                                        ('Inverted Ganons Tower', 'Inverted Ganons Tower (Entrance)'),
                                        ('Inverted Ganons Tower Exit', 'Hyrule Castle Ledge'),
                                        ('Inverted Agahnims Tower', 'Inverted Agahnims Tower'),
                                        ('Inverted Agahnims Tower Exit', 'Dark Death Mountain'),
                                        ('Turtle Rock Exit (Front)', 'Dark Death Mountain'),
                                        ('Ice Palace Exit', 'Dark Lake Hylia')]

# format:
# Key=Name
# addr = (door_index, exitdata) # multiexit
#       | ([addr], None)  # holes
# exitdata = (room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2)

# ToDo somehow merge this with creation of the locations
door_addresses = {'Links House': (0x00, (0x0104, 0x2c, 0x0506, 0x0a9a, 0x0832, 0x0ae8, 0x08b8, 0x0b07, 0x08bf, 0x06, 0xfe, 0x0816, 0x0000)),
                  'Inverted Big Bomb Shop': (0x00, (0x0104, 0x2c, 0x0506, 0x0a9a, 0x0832, 0x0ae8, 0x08b8, 0x0b07, 0x08bf, 0x06, 0xfe, 0x0816, 0x0000)),
                  'Desert Palace Entrance (South)': (0x08, (0x0084, 0x30, 0x0314, 0x0c56, 0x00a6, 0x0ca8, 0x0128, 0x0cc3, 0x0133, 0x0a, 0xfa, 0x0000, 0x0000)),
                  'Desert Palace Entrance (West)': (0x0A, (0x0083, 0x30, 0x0280, 0x0c46, 0x0003, 0x0c98, 0x0088, 0x0cb3, 0x0090, 0x0a, 0xfd, 0x0000, 0x0000)),
                  'Desert Palace Entrance (North)': (0x0B, (0x0063, 0x30, 0x0016, 0x0c00, 0x00a2, 0x0c28, 0x0128, 0x0c6d, 0x012f, 0x00, 0x0e, 0x0000, 0x0000)),
                  'Desert Palace Entrance (East)': (0x09, (0x0085, 0x30, 0x02a8, 0x0c4a, 0x0142, 0x0c98, 0x01c8, 0x0cb7, 0x01cf, 0x06, 0xfe, 0x0000, 0x0000)),
                  'Eastern Palace': (0x07, (0x00c9, 0x1e, 0x005a, 0x0600, 0x0ed6, 0x0618, 0x0f50, 0x066d, 0x0f5b, 0x00, 0xfa, 0x0000, 0x0000)),
                  'Tower of Hera': (0x32, (0x0077, 0x03, 0x0050, 0x0014, 0x087c, 0x0068, 0x08f0, 0x0083, 0x08fb, 0x0a, 0xf4, 0x0000, 0x0000)),
                  'Hyrule Castle Entrance (South)': (0x03, (0x0061, 0x1b, 0x0530, 0x0692, 0x0784, 0x06cc, 0x07f8, 0x06ff, 0x0803, 0x0e, 0xfa, 0x0000, 0x87be)),
                  'Hyrule Castle Entrance (West)': (0x02, (0x0060, 0x1b, 0x0016, 0x0600, 0x06ae, 0x0604, 0x0728, 0x066d, 0x0733, 0x00, 0x02, 0x0000, 0x8124)),
                  'Hyrule Castle Entrance (East)': (0x04, (0x0062, 0x1b, 0x004a, 0x0600, 0x0856, 0x0604, 0x08c8, 0x066d, 0x08d3, 0x00, 0xfa, 0x0000, 0x8158)),
                  'Inverted Pyramid Entrance': (0x35, (0x0010, 0x1b, 0x0418, 0x0679, 0x06b4, 0x06c6, 0x0728, 0x06e6, 0x0733, 0x07, 0xf9, 0x0000, 0x0000)),
                  'Agahnims Tower': (0x23, (0x00e0, 0x1b, 0x0032, 0x0600, 0x0784, 0x0634, 0x07f8, 0x066d, 0x0803, 0x00, 0x0a, 0x0000, 0x82be)),
                  'Inverted Ganons Tower': (0x23, (0x00e0, 0x1b, 0x0032, 0x0600, 0x0784, 0x0634, 0x07f8, 0x066d, 0x0803, 0x00, 0x0a, 0x0000, 0x82be)),
                  'Thieves Town': (0x33, (0x00db, 0x58, 0x0b2e, 0x075a, 0x0176, 0x07a8, 0x01f8, 0x07c7, 0x0203, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Skull Woods First Section Door': (0x29, (0x0058, 0x40, 0x0f4c, 0x01f6, 0x0262, 0x0248, 0x02e8, 0x0263, 0x02ef, 0x0a, 0xfe, 0x0000, 0x0000)),
                  'Skull Woods Second Section Door (East)': (0x28, (0x0057, 0x40, 0x0eb8, 0x01e6, 0x01c2, 0x0238, 0x0248, 0x0253, 0x024f, 0x0a, 0xfe, 0x0000, 0x0000)),
                  'Skull Woods Second Section Door (West)': (0x27, (0x0056, 0x40, 0x0c8e, 0x01a6, 0x0062, 0x01f8, 0x00e8, 0x0213, 0x00ef, 0x0a, 0x0e, 0x0000, 0x0000)),
                  'Skull Woods Final Section': (0x2A, (0x0059, 0x40, 0x0282, 0x0066, 0x0016, 0x00b8, 0x0098, 0x00d3, 0x00a3, 0x0a, 0xfa, 0x0000, 0x0000)),
                  'Ice Palace': (0x2C, (0x000e, 0x75, 0x0bc6, 0x0d6a, 0x0c3e, 0x0db8, 0x0cb8, 0x0dd7, 0x0cc3, 0x06, 0xf2, 0x0000, 0x0000)),
                  'Misery Mire': (0x26, (0x0098, 0x70, 0x0414, 0x0c79, 0x00a6, 0x0cc7, 0x0128, 0x0ce6, 0x0133, 0x07, 0xfa, 0x0000, 0x0000)),
                  'Palace of Darkness': (0x25, (0x004a, 0x5e, 0x005a, 0x0600, 0x0ed6, 0x0628, 0x0f50, 0x066d, 0x0f5b, 0x00, 0xfa, 0x0000, 0x0000)),
                  'Swamp Palace': (0x24, (0x0028, 0x7b, 0x049e, 0x0e8c, 0x06f2, 0x0ed8, 0x0778, 0x0ef9, 0x077f, 0x04, 0xfe, 0x0000, 0x0000)),
                  'Turtle Rock': (0x34, (0x00d6, 0x47, 0x0712, 0x00da, 0x0e96, 0x0128, 0x0f08, 0x0147, 0x0f13, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Dark Death Mountain Ledge (West)': (0x14, (0x0023, 0x45, 0x07ca, 0x0103, 0x0c46, 0x0157, 0x0cb8, 0x0172, 0x0cc3, 0x0b, 0x0a, 0x0000, 0x0000)),
                  'Dark Death Mountain Ledge (East)': (0x18, (0x0024, 0x45, 0x07e0, 0x0103, 0x0d00, 0x0157, 0x0d78, 0x0172, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Turtle Rock Isolated Ledge Entrance': (0x17, (0x00d5, 0x45, 0x0ad4, 0x0164, 0x0ca6, 0x01b8, 0x0d18, 0x01d3, 0x0d23, 0x0a, 0xfa, 0x0000, 0x0000)),
                  'Hyrule Castle Secret Entrance Stairs': (0x31, (0x0055, 0x1b, 0x044a, 0x067a, 0x0854, 0x06c8, 0x08c8, 0x06e7, 0x08d3, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Kakariko Well Cave': (0x38, (0x002f, 0x18, 0x0386, 0x0665, 0x0032, 0x06b7, 0x00b8, 0x06d2, 0x00bf, 0x0b, 0xfe, 0x0000, 0x0000)),
                  'Bat Cave Cave': (0x10, (0x00e3, 0x22, 0x0412, 0x087a, 0x048e, 0x08c8, 0x0508, 0x08e7, 0x0513, 0x06, 0x02, 0x0000, 0x0000)),
                  'Elder House (East)': (0x0D, (0x00f3, 0x18, 0x02c4, 0x064a, 0x0222, 0x0698, 0x02a8, 0x06b7, 0x02af, 0x06, 0xfe, 0x05d4, 0x0000)),
                  'Elder House (West)': (0x0C, (0x00f2, 0x18, 0x02bc, 0x064c, 0x01e2, 0x0698, 0x0268, 0x06b9, 0x026f, 0x04, 0xfe, 0x05cc, 0x0000)),
                  'North Fairy Cave': (0x37, (0x0008, 0x15, 0x0088, 0x0400, 0x0a36, 0x0448, 0x0aa8, 0x046f, 0x0ab3, 0x00, 0x0a, 0x0000, 0x0000)),
                  'Lost Woods Hideout Stump': (0x2B, (0x00e1, 0x00, 0x0f4e, 0x01f6, 0x0262, 0x0248, 0x02e8, 0x0263, 0x02ef, 0x0a, 0x0e, 0x0000, 0x0000)),
                  'Lumberjack Tree Cave': (0x11, (0x00e2, 0x02, 0x0118, 0x0015, 0x04c6, 0x0067, 0x0548, 0x0082, 0x0553, 0x0b, 0xfa, 0x0000, 0x0000)),
                  'Two Brothers House (East)': (0x0F, (0x00f5, 0x29, 0x0880, 0x0b07, 0x0200, 0x0b58, 0x0238, 0x0b74, 0x028d, 0x09, 0x00, 0x0b86, 0x0000)),
                  'Two Brothers House (West)': (0x0E, (0x00f4, 0x28, 0x08a0, 0x0b06, 0x0100, 0x0b58, 0x01b8, 0x0b73, 0x018d, 0x0a, 0x00, 0x0bb6, 0x0000)),
                  'Sanctuary': (0x01, (0x0012, 0x13, 0x001c, 0x0400, 0x06de, 0x0414, 0x0758, 0x046d, 0x0763, 0x00, 0x02, 0x0000, 0x01aa)),
                  'Old Man Cave (West)': (0x05, (0x00f0, 0x0a, 0x03a0, 0x0264, 0x0500, 0x02b8, 0x05a8, 0x02d3, 0x058d, 0x0a, 0x00, 0x0000, 0x0000)),
                  'Old Man Cave (East)': (0x06, (0x00f1, 0x03, 0x1402, 0x0294, 0x0604, 0x02e8, 0x0678, 0x0303, 0x0683, 0x0a, 0xfc, 0x0000, 0x0000)),
                  'Old Man House (Bottom)': (0x2F, (0x00e4, 0x03, 0x181a, 0x031e, 0x06b4, 0x03a7, 0x0728, 0x038d, 0x0733, 0x00, 0x0c, 0x0000, 0x0000)),
                  'Old Man House (Top)': (0x30, (0x00e5, 0x03, 0x10c6, 0x0224, 0x0814, 0x0278, 0x0888, 0x0293, 0x0893, 0x0a, 0x0c, 0x0000, 0x0000)),
                  'Death Mountain Return Cave (East)': (0x2E, (0x00e7, 0x03, 0x0d82, 0x01c4, 0x0600, 0x0218, 0x0648, 0x0233, 0x067f, 0x0a, 0x00, 0x0000, 0x0000)),
                  'Death Mountain Return Cave (West)': (0x2D, (0x00e6, 0x0a, 0x00a0, 0x0205, 0x0500, 0x0257, 0x05b8, 0x0272, 0x058d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Spectacle Rock Cave Peak': (0x22, (0x00ea, 0x03, 0x092c, 0x0133, 0x0754, 0x0187, 0x07c8, 0x01a2, 0x07d3, 0x0b, 0xfc, 0x0000, 0x0000)),
                  'Spectacle Rock Cave': (0x21, (0x00fa, 0x03, 0x0eac, 0x01e3, 0x0754, 0x0237, 0x07c8, 0x0252, 0x07d3, 0x0b, 0xfc, 0x0000, 0x0000)),
                  'Spectacle Rock Cave (Bottom)': (0x20, (0x00f9, 0x03, 0x0d9c, 0x01c3, 0x06d4, 0x0217, 0x0748, 0x0232, 0x0753, 0x0b, 0xfc, 0x0000, 0x0000)),
                  'Paradox Cave (Bottom)': (0x1D, (0x00ff, 0x05, 0x0ee0, 0x01e3, 0x0d00, 0x0237, 0x0da8, 0x0252, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Paradox Cave (Middle)': (0x1E, (0x00ef, 0x05, 0x17e0, 0x0304, 0x0d00, 0x0358, 0x0dc8, 0x0373, 0x0d7d, 0x0a, 0x00, 0x0000, 0x0000)),
                  'Paradox Cave (Top)': (0x1F, (0x00df, 0x05, 0x0460, 0x0093, 0x0d00, 0x00e7, 0x0db8, 0x0102, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Fairy Ascension Cave (Bottom)': (0x19, (0x00fd, 0x05, 0x0dd4, 0x01c4, 0x0ca6, 0x0218, 0x0d18, 0x0233, 0x0d23, 0x0a, 0xfa, 0x0000, 0x0000)),
                  'Fairy Ascension Cave (Top)': (0x1A, (0x00ed, 0x05, 0x0ad4, 0x0163, 0x0ca6, 0x01b7, 0x0d18, 0x01d2, 0x0d23, 0x0b, 0xfa, 0x0000, 0x0000)),
                  'Spiral Cave': (0x1C, (0x00ee, 0x05, 0x07c8, 0x0108, 0x0c46, 0x0158, 0x0cb8, 0x0177, 0x0cc3, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Spiral Cave (Bottom)': (0x1B, (0x00fe, 0x05, 0x0cca, 0x01a3, 0x0c56, 0x01f7, 0x0cc8, 0x0212, 0x0cd3, 0x0b, 0xfa, 0x0000, 0x0000)),
                  'Bumper Cave (Bottom)': (0x15, (0x00fb, 0x4a, 0x03a0, 0x0263, 0x0500, 0x02b7, 0x05a8, 0x02d2, 0x058d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Bumper Cave (Top)': (0x16, (0x00eb, 0x4a, 0x00a0, 0x020a, 0x0500, 0x0258, 0x05b8, 0x0277, 0x058d, 0x06, 0x00, 0x0000, 0x0000)),
                  'Superbunny Cave (Top)': (0x13, (0x00e8, 0x45, 0x0460, 0x0093, 0x0d00, 0x00e7, 0x0db8, 0x0102, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000)),
                  'Superbunny Cave (Bottom)': (0x12, (0x00f8, 0x45, 0x0ee0, 0x01e4, 0x0d00, 0x0238, 0x0d78, 0x0253, 0x0d7d, 0x0a, 0x00, 0x0000, 0x0000)),
                  'Hookshot Cave': (0x39, (0x003c, 0x45, 0x04da, 0x00a3, 0x0cd6, 0x0107, 0x0d48, 0x0112, 0x0d53, 0x0b, 0xfa, 0x0000, 0x0000)),
                  'Hookshot Cave Back Entrance': (0x3A, (0x002c, 0x45, 0x004c, 0x0000, 0x0c56, 0x0038, 0x0cc8, 0x006f, 0x0cd3, 0x00, 0x0a, 0x0000, 0x0000)),
                  'Ganons Tower': (0x36, (0x000c, 0x43, 0x0052, 0x0000, 0x0884, 0x0028, 0x08f8, 0x006f, 0x0903, 0x00, 0xfc, 0x0000, 0x0000)),
                  'Inverted Agahnims Tower': (0x36, (0x000c, 0x43, 0x0052, 0x0000, 0x0884, 0x0028, 0x08f8, 0x006f, 0x0903, 0x00, 0xfc, 0x0000, 0x0000)),
                  'Pyramid Entrance': (0x35, (0x0010, 0x5b, 0x0b0e, 0x075a, 0x0674, 0x07a8, 0x06e8, 0x07c7, 0x06f3, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Skull Woods First Section Hole (West)': ([0xDB84D, 0xDB84E], None),
                  'Skull Woods First Section Hole (East)': ([0xDB84F, 0xDB850], None),
                  'Skull Woods First Section Hole (North)': ([0xDB84C], None),
                  'Skull Woods Second Section Hole': ([0xDB851, 0xDB852], None),
                  'Pyramid Hole': ([0xDB854, 0xDB855, 0xDB856], None),
                  'Inverted Pyramid Hole': ([0xDB854, 0xDB855, 0xDB856, 0x180340], None),
                  'Waterfall of Wishing': (0x5B, (0x0114, 0x0f, 0x0080, 0x0200, 0x0e00, 0x0207, 0x0e60, 0x026f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000)),
                  'Dam': (0x4D, (0x010b, 0x3b, 0x04a0, 0x0e8a, 0x06fa, 0x0ed8, 0x0778, 0x0ef7, 0x077f, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Blinds Hideout': (0x60, (0x0119, 0x18, 0x02b2, 0x064a, 0x0186, 0x0697, 0x0208, 0x06b7, 0x0213, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Hyrule Castle Secret Entrance Drop': ([0xDB858], None),
                  'Bonk Fairy (Light)': (0x76, (0x0126, 0x2b, 0x00a0, 0x0a0a, 0x0700, 0x0a67, 0x0788, 0x0a77, 0x0785, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Lake Hylia Fairy': (0x5D, (0x0115, 0x2e, 0x0016, 0x0a00, 0x0cb6, 0x0a37, 0x0d28, 0x0a6d, 0x0d33, 0x00, 0x00, 0x0000, 0x0000)),
                  'Light Hype Fairy': (0x6B, (0x0115, 0x34, 0x00a0, 0x0c04, 0x0900, 0x0c58, 0x0988, 0x0c73, 0x0985, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Desert Fairy': (0x71, (0x0115, 0x3a, 0x0000, 0x0e00, 0x0400, 0x0e26, 0x0468, 0x0e6d, 0x0485, 0x00, 0x00, 0x0000, 0x0000)),
                  'Kings Grave': (0x5A, (0x0113, 0x14, 0x0320, 0x0456, 0x0900, 0x04a6, 0x0998, 0x04c3, 0x097d, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Tavern North': (0x42, (0x0103, 0x18, 0x1440, 0x08a7, 0x0206, 0x08f9, 0x0288, 0x0914, 0x0293, 0xf7, 0x09, 0xFFFF, 0x0000)),  # do not use, buggy
                  'Chicken House': (0x4A, (0x0108, 0x18, 0x1120, 0x0837, 0x0106, 0x0888, 0x0188, 0x08a4, 0x0193, 0x07, 0xf9, 0x1530, 0x0000)),
                  'Aginahs Cave': (0x70, (0x010a, 0x30, 0x0656, 0x0cc6, 0x02aa, 0x0d18, 0x0328, 0x0d33, 0x032f, 0x08, 0xf8, 0x0000, 0x0000)),
                  'Sahasrahlas Hut': (0x44, (0x0105, 0x1e, 0x0610, 0x06d4, 0x0c76, 0x0727, 0x0cf0, 0x0743, 0x0cfb, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Cave Shop (Lake Hylia)': (0x57, (0x0112, 0x35, 0x0022, 0x0c00, 0x0b1a, 0x0c26, 0x0b98, 0x0c6d, 0x0b9f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Capacity Upgrade': (0x5C, (0x0115, 0x35, 0x0a46, 0x0d36, 0x0c2a, 0x0d88, 0x0ca8, 0x0da3, 0x0caf, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Kakariko Well Drop': ([0xDB85C, 0xDB85D], None),
                  'Blacksmiths Hut': (0x63, (0x0121, 0x22, 0x010c, 0x081a, 0x0466, 0x0868, 0x04d8, 0x0887, 0x04e3, 0x06, 0xfa, 0x041A, 0x0000)),
                  'Bat Cave Drop': ([0xDB859, 0xDB85A], None),
                  'Sick Kids House': (0x3F, (0x0102, 0x18, 0x10be, 0x0826, 0x01f6, 0x0877, 0x0278, 0x0893, 0x0283, 0x08, 0xf8, 0x14CE, 0x0000)),
                  'North Fairy Cave Drop': ([0xDB857], None),
                  'Lost Woods Gamble': (0x3B, (0x0100, 0x00, 0x004e, 0x0000, 0x0272, 0x0008, 0x02f0, 0x006f, 0x02f7, 0x00, 0x00, 0x0000, 0x0000)),
                  'Fortune Teller (Light)': (0x64, (0x0122, 0x11, 0x060e, 0x04b4, 0x027d, 0x0508, 0x02f8, 0x0523, 0x0302, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Snitch Lady (East)': (0x3D, (0x0101, 0x18, 0x0ad8, 0x074a, 0x02c6, 0x0798, 0x0348, 0x07b7, 0x0353, 0x06, 0xfa, 0x0DE8, 0x0000)),
                  'Snitch Lady (West)': (0x3E, (0x0101, 0x18, 0x0788, 0x0706, 0x0046, 0x0758, 0x00c8, 0x0773, 0x00d3, 0x08, 0xf8, 0x0B98, 0x0000)),
                  'Bush Covered House': (0x43, (0x0103, 0x18, 0x1156, 0x081a, 0x02b6, 0x0868, 0x0338, 0x0887, 0x0343, 0x06, 0xfa, 0x1466, 0x0000)),
                  'Tavern (Front)': (0x41, (0x0103, 0x18, 0x1842, 0x0916, 0x0206, 0x0967, 0x0288, 0x0983, 0x0293, 0x08, 0xf8, 0x1C50, 0x0000)),
                  'Light World Bomb Hut': (0x49, (0x0107, 0x18, 0x1800, 0x0916, 0x0000, 0x0967, 0x0068, 0x0983, 0x008d, 0x08, 0xf8, 0x9C0C, 0x0000)),
                  'Kakariko Shop': (0x45, (0x011f, 0x18, 0x16a8, 0x08e7, 0x0136, 0x0937, 0x01b8, 0x0954, 0x01c3, 0x07, 0xf9, 0x1AB6, 0x0000)),
                  'Lost Woods Hideout Drop': ([0xDB853], None),
                  'Lumberjack Tree Tree': ([0xDB85B], None),
                  'Cave 45': (0x50, (0x011b, 0x32, 0x0680, 0x0cc9, 0x0400, 0x0d16, 0x0438, 0x0d36, 0x0485, 0x07, 0xf9, 0x0000, 0x0000)),
                  'Graveyard Cave': (0x51, (0x011b, 0x14, 0x0016, 0x0400, 0x08a2, 0x0446, 0x0918, 0x046d, 0x091f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Checkerboard Cave': (0x7D, (0x0126, 0x30, 0x00c8, 0x0c0a, 0x024a, 0x0c67, 0x02c8, 0x0c77, 0x02cf, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Mini Moldorm Cave': (0x7C, (0x0123, 0x35, 0x1480, 0x0e96, 0x0a00, 0x0ee8, 0x0a68, 0x0f03, 0x0a85, 0x08, 0xf8, 0x0000, 0x0000)),
                  'Long Fairy Cave': (0x54, (0x011e, 0x2f, 0x06a0, 0x0aca, 0x0f00, 0x0b18, 0x0fa8, 0x0b37, 0x0f85, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Good Bee Cave': (0x6A, (0x0120, 0x37, 0x0084, 0x0c00, 0x0e26, 0x0c36, 0x0e98, 0x0c6f, 0x0ea3, 0x00, 0x00, 0x0000, 0x0000)),
                  '20 Rupee Cave': (0x7A, (0x0125, 0x37, 0x0200, 0x0c23, 0x0e00, 0x0c86, 0x0e68, 0x0c92, 0x0e7d, 0x0d, 0xf3, 0x0000, 0x0000)),
                  '50 Rupee Cave': (0x78, (0x0124, 0x3a, 0x0790, 0x0eea, 0x047a, 0x0f47, 0x04f8, 0x0f57, 0x04ff, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Ice Rod Cave': (0x7F, (0x0120, 0x37, 0x0080, 0x0c00, 0x0e00, 0x0c37, 0x0e48, 0x0c6f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000)),
                  'Bonk Rock Cave': (0x79, (0x0124, 0x13, 0x0280, 0x044a, 0x0600, 0x04a7, 0x0638, 0x04b7, 0x067d, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Library': (0x48, (0x0107, 0x29, 0x0100, 0x0a14, 0x0200, 0x0a67, 0x0278, 0x0a83, 0x0285, 0x0a, 0xf6, 0x040E, 0x0000)),
                  'Potion Shop': (0x4B, (0x0109, 0x16, 0x070a, 0x04e6, 0x0c56, 0x0538, 0x0cc8, 0x0553, 0x0cd3, 0x08, 0xf8, 0x0A98, 0x0000)),
                  'Sanctuary Grave': ([0xDB85E], None),
                  'Hookshot Fairy': (0x4F, (0x010c, 0x05, 0x0ee0, 0x01e3, 0x0d00, 0x0236, 0x0d78, 0x0252, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000)),
                  'Pyramid Fairy': (0x62, (0x0116, 0x5b, 0x0b1e, 0x0754, 0x06fa, 0x07a7, 0x0778, 0x07c3, 0x077f, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'East Dark World Hint': (0x68, (0x010e, 0x6f, 0x06a0, 0x0aca, 0x0f00, 0x0b18, 0x0fa8, 0x0b37, 0x0f85, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Palace of Darkness Hint': (0x67, (0x011a, 0x5e, 0x0c24, 0x0794, 0x0d12, 0x07e8, 0x0d90, 0x0803, 0x0d97, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Dark Lake Hylia Fairy': (0x6C, (0x0115, 0x6e, 0x0016, 0x0a00, 0x0cb6, 0x0a36, 0x0d28, 0x0a6d, 0x0d33, 0x00, 0x00, 0x0000, 0x0000)),
                  'Dark Lake Hylia Ledge Fairy': (0x80, (0x0115, 0x77, 0x0080, 0x0c00, 0x0e00, 0x0c37, 0x0e48, 0x0c6f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000)),
                  'Dark Lake Hylia Ledge Spike Cave': (0x7B, (0x0125, 0x77, 0x0200, 0x0c27, 0x0e00, 0x0c86, 0x0e68, 0x0c96, 0x0e7d, 0x09, 0xf7, 0x0000, 0x0000)),
                  'Dark Lake Hylia Ledge Hint': (0x69, (0x010e, 0x77, 0x0084, 0x0c00, 0x0e26, 0x0c36, 0x0e98, 0x0c6f, 0x0ea3, 0x00, 0x00, 0x0000, 0x0000)),
                  'Hype Cave': (0x3C, (0x011e, 0x74, 0x00a0, 0x0c0a, 0x0900, 0x0c58, 0x0988, 0x0c77, 0x097d, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Bonk Fairy (Dark)': (0x77, (0x0126, 0x6b, 0x00a0, 0x0a05, 0x0700, 0x0a66, 0x0788, 0x0a72, 0x0785, 0x0b, 0xf5, 0x0000, 0x0000)),
                  'Brewery': (0x47, (0x0106, 0x58, 0x16a8, 0x08e4, 0x013e, 0x0938, 0x01b8, 0x0953, 0x01c3, 0x0a, 0xf6, 0x1AB6, 0x0000)),
                  'C-Shaped House': (0x53, (0x011c, 0x58, 0x09d8, 0x0744, 0x02ce, 0x0797, 0x0348, 0x07b3, 0x0353, 0x0a, 0xf6, 0x0DE8, 0x0000)),
                  'Chest Game': (0x46, (0x0106, 0x58, 0x078a, 0x0705, 0x004e, 0x0758, 0x00c8, 0x0774, 0x00d3, 0x09, 0xf7, 0x0B98, 0x0000)),
                  'Dark World Hammer Peg Cave': (0x7E, (0x0127, 0x62, 0x0894, 0x091e, 0x0492, 0x09a6, 0x0508, 0x098b, 0x050f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Red Shield Shop': (0x74, (0x0110, 0x5a, 0x079a, 0x06e8, 0x04d6, 0x0738, 0x0548, 0x0755, 0x0553, 0x08, 0xf8, 0x0AA8, 0x0000)),
                  'Dark Sanctuary Hint': (0x59, (0x0112, 0x53, 0x001e, 0x0400, 0x06e2, 0x0446, 0x0758, 0x046d, 0x075f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Inverted Dark Sanctuary': (0x59, (0x0112, 0x53, 0x001e, 0x0400, 0x06e2, 0x0446, 0x0758, 0x046d, 0x075f, 0x00, 0x00, 0x0000, 0x0000)),
                  'Fortune Teller (Dark)': (0x65, (0x0122, 0x51, 0x0610, 0x04b4, 0x027e, 0x0507, 0x02f8, 0x0523, 0x0303, 0x0a, 0xf6, 0x091E, 0x0000)),
                  'Village of Outcasts Shop': (0x5F, (0x010f, 0x58, 0x1058, 0x0814, 0x02be, 0x0868, 0x0338, 0x0883, 0x0343, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Dark World Lumberjack Shop': (0x56, (0x010f, 0x42, 0x041c, 0x0074, 0x04e2, 0x00c7, 0x0558, 0x00e3, 0x055f, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Dark World Potion Shop': (0x6E, (0x010f, 0x56, 0x080e, 0x04f4, 0x0c66, 0x0548, 0x0cd8, 0x0563, 0x0ce3, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Archery Game': (0x58, (0x0111, 0x69, 0x069e, 0x0ac4, 0x02ea, 0x0b18, 0x0368, 0x0b33, 0x036f, 0x0a, 0xf6, 0x09AC, 0x0000)),
                  'Mire Shed': (0x5E, (0x010d, 0x70, 0x0384, 0x0c69, 0x001e, 0x0cb6, 0x0098, 0x0cd6, 0x00a3, 0x07, 0xf9, 0x0000, 0x0000)),
                  'Dark Desert Hint': (0x61, (0x0114, 0x70, 0x0654, 0x0cc5, 0x02aa, 0x0d16, 0x0328, 0x0d32, 0x032f, 0x09, 0xf7, 0x0000, 0x0000)),
                  'Dark Desert Fairy': (0x55, (0x0115, 0x70, 0x03a8, 0x0c6a, 0x013a, 0x0cb7, 0x01b8, 0x0cd7, 0x01bf, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Spike Cave': (0x40, (0x0117, 0x43, 0x0ed4, 0x01e4, 0x08aa, 0x0236, 0x0928, 0x0253, 0x092f, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Cave Shop (Dark Death Mountain)': (0x6D, (0x0112, 0x45, 0x0ee0, 0x01e3, 0x0d00, 0x0236, 0x0daa, 0x0252, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000)),
                  'Dark Death Mountain Fairy': (0x6F, (0x0115, 0x43, 0x1400, 0x0294, 0x0600, 0x02e8, 0x0678, 0x0303, 0x0685, 0x0a, 0xf6, 0x0000, 0x0000)),
                  'Mimic Cave': (0x4E, (0x010c, 0x05, 0x07e0, 0x0103, 0x0d00, 0x0156, 0x0d78, 0x0172, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000)),
                  'Big Bomb Shop': (0x52, (0x011c, 0x6c, 0x0506, 0x0a9a, 0x0832, 0x0ae7, 0x08b8, 0x0b07, 0x08bf, 0x06, 0xfa, 0x0816, 0x0000)),
                  'Inverted Links House': (0x52, (0x011c, 0x6c, 0x0506, 0x0a9a, 0x0832, 0x0ae7, 0x08b8, 0x0b07, 0x08bf, 0x06, 0xfa, 0x0816, 0x0000)),
                  'Dark Lake Hylia Shop': (0x73, (0x010f, 0x75, 0x0380, 0x0c6a, 0x0a00, 0x0cb8, 0x0a58, 0x0cd7, 0x0a85, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Lumberjack House': (0x75, (0x011f, 0x02, 0x049c, 0x0088, 0x04e6, 0x00d8, 0x0558, 0x00f7, 0x0563, 0x08, 0xf8, 0x07AA, 0x0000)),
                  'Lake Hylia Fortune Teller': (0x72, (0x0122, 0x35, 0x0380, 0x0c6a, 0x0a00, 0x0cb8, 0x0a58, 0x0cd7, 0x0a85, 0x06, 0xfa, 0x0000, 0x0000)),
                  'Kakariko Gamble Game': (0x66, (0x0118, 0x29, 0x069e, 0x0ac4, 0x02ea, 0x0b18, 0x0368, 0x0b33, 0x036f, 0x0a, 0xf6, 0x09AC, 0x0000))}

# format:
# Key=Name
# value = entrance #
#        | (entrance #, exit #)
exit_ids = {'Links House Exit': (0x01, 0x00),
            'Inverted Links House Exit': (0x01, 0x00),
            'Chris Houlihan Room Exit': (None, 0x3D),
            'Desert Palace Exit (South)': (0x09, 0x0A),
            'Desert Palace Exit (West)': (0x0B, 0x0C),
            'Desert Palace Exit (East)': (0x0A, 0x0B),
            'Desert Palace Exit (North)': (0x0C, 0x0D),
            'Eastern Palace Exit': (0x08, 0x09),
            'Tower of Hera Exit': (0x33, 0x2D),
            'Hyrule Castle Exit (South)': (0x04, 0x03),
            'Hyrule Castle Exit (West)': (0x03, 0x02),
            'Hyrule Castle Exit (East)': (0x05, 0x04),
            'Agahnims Tower Exit': (0x24, 0x25),
            'Inverted Agahnims Tower Exit': (0x24, 0x25),
            'Thieves Town Exit': (0x34, 0x35),
            'Skull Woods First Section Exit': (0x2A, 0x2B),
            'Skull Woods Second Section Exit (East)': (0x29, 0x2A),
            'Skull Woods Second Section Exit (West)': (0x28, 0x29),
            'Skull Woods Final Section Exit': (0x2B, 0x2C),
            'Ice Palace Exit': (0x2D, 0x2E),
            'Misery Mire Exit': (0x27, 0x28),
            'Palace of Darkness Exit': (0x26, 0x27),
            'Swamp Palace Exit': (0x25, 0x26),
            'Turtle Rock Exit (Front)': (0x35, 0x34),
            'Turtle Rock Ledge Exit (West)': (0x15, 0x16),
            'Turtle Rock Ledge Exit (East)': (0x19, 0x1A),
            'Turtle Rock Isolated Ledge Exit': (0x18, 0x19),
            'Hyrule Castle Secret Entrance Exit': (0x32, 0x33),
            'Kakariko Well Exit': (0x39, 0x3A),
            'Bat Cave Exit': (0x11, 0x12),
            'Elder House Exit (East)': (0x0E, 0x0F),
            'Elder House Exit (West)': (0x0D, 0x0E),
            'North Fairy Cave Exit': (0x38, 0x39),
            'Lost Woods Hideout Exit': (0x2C, 0x36),
            'Lumberjack Tree Exit': (0x12, 0x13),
            'Two Brothers House Exit (East)': (0x10, 0x11),
            'Two Brothers House Exit (West)': (0x0F, 0x10),
            'Sanctuary Exit': (0x02, 0x01),
            'Old Man Cave Exit (East)': (0x07, 0x08),
            'Old Man Cave Exit (West)': (0x06, 0x07),
            'Old Man House Exit (Bottom)': (0x30, 0x31),
            'Old Man House Exit (Top)': (0x31, 0x32),
            'Death Mountain Return Cave Exit (West)': (0x2E, 0x2F),
            'Death Mountain Return Cave Exit (East)': (0x2F, 0x30),
            'Spectacle Rock Cave Exit': (0x21, 0x22),
            'Spectacle Rock Cave Exit (Top)': (0x22, 0x23),
            'Spectacle Rock Cave Exit (Peak)': (0x23, 0x24),
            'Paradox Cave Exit (Bottom)': (0x1E, 0x1F),
            'Paradox Cave Exit (Middle)': (0x1F, 0x20),
            'Paradox Cave Exit (Top)': (0x20, 0x21),
            'Fairy Ascension Cave Exit (Bottom)': (0x1A, 0x1B),
            'Fairy Ascension Cave Exit (Top)': (0x1B, 0x1C),
            'Spiral Cave Exit': (0x1C, 0x1D),
            'Spiral Cave Exit (Top)': (0x1D, 0x1E),
            'Bumper Cave Exit (Top)': (0x17, 0x18),
            'Bumper Cave Exit (Bottom)': (0x16, 0x17),
            'Superbunny Cave Exit (Top)': (0x14, 0x15),
            'Superbunny Cave Exit (Bottom)': (0x13, 0x14),
            'Hookshot Cave Exit (South)': (0x3A, 0x3B),
            'Hookshot Cave Exit (North)': (0x3B, 0x3C),
            'Ganons Tower Exit': (0x37, 0x38),
            'Inverted Ganons Tower Exit': (0x37, 0x38),
            'Pyramid Exit': (0x36, 0x37),
            'Waterfall of Wishing': 0x5C,
            'Dam': 0x4E,
            'Blinds Hideout': 0x61,
            'Lumberjack House': 0x6B,
            'Bonk Fairy (Light)': 0x71,
            'Bonk Fairy (Dark)': 0x71,
            'Lake Hylia Healer Fairy': 0x5E,
            'Swamp Healer Fairy': 0x5E,
            'Desert Healer Fairy': 0x5E,
            'Dark Lake Hylia Healer Fairy': 0x5E,
            'Dark Lake Hylia Ledge Healer Fairy': 0x5E,
            'Dark Desert Healer Fairy': 0x5E,
            'Dark Death Mountain Healer Fairy': 0x5E,
            'Fortune Teller (Light)': 0x65,
            'Lake Hylia Fortune Teller': 0x65,
            'Kings Grave': 0x5B,
            'Tavern': 0x43,
            'Chicken House': 0x4B,
            'Aginahs Cave': 0x4D,
            'Sahasrahlas Hut': 0x45,
            'Cave Shop (Lake Hylia)': 0x58,
            'Cave Shop (Dark Death Mountain)': 0x58,
            'Capacity Upgrade': 0x5D,
            'Blacksmiths Hut': 0x64,
            'Sick Kids House': 0x40,
            'Lost Woods Gamble': 0x3C,
            'Snitch Lady (East)': 0x3E,
            'Snitch Lady (West)': 0x3F,
            'Bush Covered House': 0x44,
            'Tavern (Front)': 0x42,
            'Light World Bomb Hut': 0x4A,
            'Kakariko Shop': 0x46,
            'Cave 45': 0x51,
            'Graveyard Cave': 0x52,
            'Checkerboard Cave': 0x72,
            'Mini Moldorm Cave': 0x6C,
            'Long Fairy Cave': 0x55,
            'Good Bee Cave': 0x56,
            '20 Rupee Cave': 0x6F,
            '50 Rupee Cave': 0x6D,
            'Ice Rod Cave': 0x84,
            'Bonk Rock Cave': 0x6E,
            'Library': 0x49,
            'Kakariko Gamble Game': 0x67,
            'Potion Shop': 0x4C,
            'Hookshot Fairy': 0x50,
            'Pyramid Fairy': 0x63,
            'East Dark World Hint': 0x69,
            'Palace of Darkness Hint': 0x68,
            'Big Bomb Shop': 0x53,
            'Inverted Big Bomb Shop': 0x53,
            'Village of Outcasts Shop': 0x60,
            'Dark Lake Hylia Shop': 0x60,
            'Dark World Lumberjack Shop': 0x60,
            'Dark World Potion Shop': 0x60,
            'Dark Lake Hylia Ledge Spike Cave': 0x70,
            'Dark Lake Hylia Ledge Hint': 0x6A,
            'Hype Cave': 0x3D,
            'Brewery': 0x48,
            'C-Shaped House': 0x54,
            'Chest Game': 0x47,
            'Dark World Hammer Peg Cave': 0x83,
            'Red Shield Shop': 0x57,
            'Dark Sanctuary Hint': 0x5A,
            'Inverted Dark Sanctuary': 0x5A,
            'Fortune Teller (Dark)': 0x66,
            'Archery Game': 0x59,
            'Mire Shed': 0x5F,
            'Dark Desert Hint': 0x62,
            'Spike Cave': 0x41,
            'Mimic Cave': 0x4F,
            'Kakariko Well (top)': 0x80,
            'Hyrule Castle Secret Entrance': 0x7D,
            'Bat Cave (right)': 0x7E,
            'North Fairy Cave': 0x7C,
            'Lost Woods Hideout (top)': 0x7A,
            'Lumberjack Tree (top)': 0x7F,
            'Sewer Drop': 0x81,
            'Skull Woods Second Section (Drop)': 0x79,
            'Skull Woods First Section (Left)': 0x77,
            'Skull Woods First Section (Right)': 0x78,
            'Skull Woods First Section (Top)': 0x76,
            'Pyramid': 0x7B}

exit_id_to_name = {}
for name, addresses in exit_ids.items():
    if type(addresses) == int:
        exit_id_to_name[addresses] = name
    else:
        for address in addresses:
            exit_id_to_name[address] = name
