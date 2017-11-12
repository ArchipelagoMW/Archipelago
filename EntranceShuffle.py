import random

# ToDo: With shuffle_ganon option, prevent gtower from linking to an exit only location through a 2 entrance cave.


def link_entrances(world):
    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname)

    # if we do not shuffle, set default connections
    if world.shuffle == 'vanilla':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)
        for exitname, regionname in default_dungeon_connections:
            connect_simple(world, exitname, regionname)

    elif world.shuffle == 'dungeonssimple':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)

        simple_shuffle_dungeons(world)

    elif world.shuffle == 'dungeonsfull':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)

        skull_woods_shuffle(world)

        dungeon_exits = list(Dungeon_Exits)
        lw_entrances = list(LW_Dungeon_Entrances)
        dw_entrances = list(DW_Dungeon_Entrances)

        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
        else:
            dungeon_exits.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
        else:
            dw_entrances.append('Ganons Tower')
            dungeon_exits.append('Ganons Tower Exit')

        if world.mode == 'standard':
            # rest of hyrule castle must be in light world to avoid fake darkworld stuff, so it has to be the one connected to east exit of desert
            connect_mandatory_exits(world, lw_entrances, [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')], list(LW_Dungeon_Entrances_Must_Exit))
        else:
            connect_mandatory_exits(world, lw_entrances, dungeon_exits, list(LW_Dungeon_Entrances_Must_Exit))
        connect_mandatory_exits(world, dw_entrances, dungeon_exits, list(DW_Dungeon_Entrances_Must_Exit))
        connect_caves(world, lw_entrances, [], list(LW_Dungeon_Exits))  # Agahnim must be light world
        connect_caves(world, lw_entrances, dw_entrances, dungeon_exits)

    elif world.shuffle == 'simple':
        simple_shuffle_dungeons(world)

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
        random.shuffle(two_door_caves)
        random.shuffle(caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1)
            connect_two_way(world, entrance2, exit2)

        # now the remaining pairs
        two_door_caves = list(Two_Door_Caves)
        random.shuffle(two_door_caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1)
            connect_two_way(world, entrance2, exit2)

        # at this point only Light World death mountain entrances remain
        # place old man, has limited options
        remaining_entrances = ['Old Man Cave (West)', 'Old Man House (Bottom)', 'Death Mountain Return Cave (West)', 'Paradox Cave (Bottom)', 'Paradox Cave (Middle)', 'Paradox Cave (Top)',
                               'Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave (Top)', 'Spiral Cave', 'Spiral Cave (Bottom)']
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        remaining_entrances.extend(old_man_entrances)
        random.shuffle(remaining_entrances)
        old_man_entrance = remaining_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')

        # add old man house to ensure it is alwayxs somewhere on light death mountain
        caves.append(('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)'))
        caves.extend(list(three_exit_caves))

        # connect rest
        connect_caves(world, remaining_entrances, [], caves)

        # scramble holes
        scramble_holes(world)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)

    elif world.shuffle == 'restricted':
        simple_shuffle_dungeons(world)

        lw_entrances = list(LW_Entrances)
        dw_entrances = list(DW_Entrances)
        dw_must_exits = list(DW_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances)
        caves = list(Cave_Exits)
        three_exit_caves = list(Cave_Three_Exits)
        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # only use two exit caves to do mandatory dw connections
        connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)
        # add three exit doors to pool for remainder
        caves.extend(three_exit_caves)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        lw_entrances.extend(old_man_entrances)
        random.shuffle(lw_entrances)
        old_man_entrance = lw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')

        # place Old Man House in Light World, so using the s&q point does not cause fake dark world
        connect_caves(world, lw_entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')])

        # connect rest. There's 2 dw entrances remaining, so we will not run into parity issue placing caves
        connect_caves(world, lw_entrances, dw_entrances, caves)

        # scramble holes
        scramble_holes(world)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)

    elif world.shuffle == 'full':
        skull_woods_shuffle(world)

        lw_entrances = list(LW_Entrances + LW_Dungeon_Entrances)
        dw_entrances = list(DW_Entrances + DW_Dungeon_Entrances)
        dw_must_exits = list(DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit)
        lw_must_exits = list(LW_Dungeon_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances)
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits)  # don't need to consider three exit caves, have one exit caves to avoid parity issues
        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
        else:
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
        else:
            dw_entrances.append('Ganons Tower')
            caves.append('Ganons Tower Exit')

        # we randomize which world requirements we fulfill first so we get better dungeon distribution
        if random.randint(0, 1) == 0:
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits)
            connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)
        else:
            connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits)
            connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits)
        if world.mode == 'standard':
            # rest of hyrule castle must be in light world to avoid fake darkworld stuff
            connect_caves(world, lw_entrances, [], [('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')])
        connect_caves(world, lw_entrances, [], list(LW_Dungeon_Exits))  # Agahnim must be light world

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        lw_entrances.extend(old_man_entrances)
        random.shuffle(lw_entrances)
        old_man_entrance = lw_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)')
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)')

        # place Old Man House in Light World, so using the s&q point does not cause fake dark world
        connect_caves(world, lw_entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')])

        # now scramble the rest
        connect_caves(world, lw_entrances, dw_entrances, caves)

        # scramble holes
        scramble_holes(world)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)

    elif world.shuffle == 'madness':
        # here lie dragons, connections are no longer two way
        lw_entrances = list(LW_Entrances + LW_Dungeon_Entrances)
        dw_entrances = list(DW_Entrances + DW_Dungeon_Entrances)
        dw_entrances_must_exits = list(DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit)

        lw_doors = list(LW_Entrances + LW_Dungeon_Entrances + LW_Dungeon_Entrances_Must_Exit) + ['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump',
                                                                                                 'Lumberjack Tree Cave', 'Hyrule Castle Secret Entrance Stairs'] + list(Old_Man_Entrances)
        dw_doors = list(DW_Entrances + DW_Dungeon_Entrances + DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit) + ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)']

        random.shuffle(lw_doors)
        random.shuffle(dw_doors)

        dw_entrances_must_exits.append('Skull Woods Second Section Door (West)')
        dw_entrances.append('Skull Woods Second Section Door (East)')
        dw_entrances.append('Skull Woods First Section Door')

        lw_entrances.extend(['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Entrance (South)'])

        lw_entrances_must_exits = list(LW_Dungeon_Entrances_Must_Exit)
        old_man_entrances = list(Old_Man_Entrances)

        mandatory_light_world = ['Old Man House Exit (Bottom)', 'Old Man House Exit (Top)']
        mandatory_dark_world = []
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits)

        # shuffle up holes

        lw_hole_entrances = ['Kakariko Well Drop', 'Bat Cave Drop', 'North Fairy Cave Drop', 'Lost Woods Hideout Drop', 'Lumberjack Tree Tree', 'Sanctuary Grave']
        dw_hole_entrances = ['Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole']

        hole_targets = [('Kakariko Well Exit', 'Kakariko Well (top)'),
                        ('Bat Cave Exit', 'Bat Cave (right)'),
                        ('North Fairy Cave Exit', 'North Fairy Cave'),
                        ('Lost Woods Hideout Exit', 'Lost Woods Hideout (top)'),
                        ('Lumberjack Tree Exit', 'Lumberjack Tree (top)'),
                        (('Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)'), 'Skull Woods Second Section')]

        if world.mode == 'standard':
            # cannot move uncle cave
            connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance')
            connect_exit(world, 'Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance Stairs')
            connect_entrance(world, lw_doors.pop(), 'Hyrule Castle Secret Entrance Exit')
        else:
            lw_hole_entrances.append('Hyrule Castle Secret Entrance Drop')
            hole_targets.append(('Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance'))
            lw_entrances.append('Hyrule Castle Secret Entrance Stairs')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
            connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit')
            connect_entrance(world, 'Pyramid Hole', 'Pyramid')
        else:
            dw_entrances.append('Ganons Tower')
            caves.append('Ganons Tower Exit')
            dw_hole_entrances.append('Pyramid Hole')
            hole_targets.append(('Pyramid Exit', 'Pyramid'))
            dw_entrances_must_exits.append('Pyramid Entrance')
            dw_doors.extend(['Ganons Tower', 'Pyramid Entrance'])

        random.shuffle(lw_hole_entrances)
        random.shuffle(dw_hole_entrances)
        random.shuffle(hole_targets)

        # decide if skull woods first section should be in light or dark world
        sw_light = random.randint(0, 1) == 0
        if sw_light:
            sw_hole_pool = lw_hole_entrances
            mandatory_light_world.append('Skull Woods First Section Exit')
        else:
            sw_hole_pool = dw_hole_entrances
            mandatory_dark_world.append('Skull Woods First Section Exit')
        for target in ['Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)']:
            connect_entrance(world, sw_hole_pool.pop(), target)

        # sanctuary has to be in light world
        connect_entrance(world, lw_hole_entrances.pop(), 'Sewer Drop')
        mandatory_light_world.append('Sanctuary Exit')

        # fill up remaining holes
        for hole in dw_hole_entrances:
            exits, target = hole_targets.pop()
            mandatory_dark_world.append(exits)
            connect_entrance(world, hole, target)

        for hole in lw_hole_entrances:
            exits, target = hole_targets.pop()
            mandatory_light_world.append(exits)
            connect_entrance(world, hole, target)

        # hyrule castle handling
        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_entrance(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
            random.shuffle(lw_entrances)
            connect_exit(world, 'Hyrule Castle Exit (South)', lw_entrances.pop())
            mandatory_light_world.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            lw_doors.append('Hyrule Castle Entrance (South)')
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))

        # now let's deal with mandatory reachable stuff
        def extract_reachable_exit(cavelist):
            random.shuffle(cavelist)
            candidate = None
            for cave in cavelist:
                if isinstance(cave, tuple) and len(cave) > 1:
                    # special handling: TRock and Spectracle Rock cave have two entries that we should consider entrance only
                    # ToDo this should be handled in a more sensible manner
                    if cave[0] in ['Turtle Rock Exit (Front)', 'Spectacle Rock Cave Exit (Peak)'] and len(cave) == 2:
                        continue
                    candidate = cave
                    break
            if candidate is None:
                raise RuntimeError('No suitable cave.')
            cavelist.remove(candidate)
            return candidate

        def connect_reachable_exit(entrance, general, worldspecific, worldoors):
            # select which one is the primary option
            if random.randint(0, 1) == 0:
                primary = general
                secondary = worldspecific
            else:
                primary = worldspecific
                secondary = general

            try:
                cave = extract_reachable_exit(primary)
            except RuntimeError:
                cave = extract_reachable_exit(secondary)

            exit = cave[-1]
            cave = cave[:-1]
            connect_exit(world, exit, entrance)
            connect_entrance(world, worldoors.pop(), exit)
            # rest of cave now is forced to be in this world
            worldspecific.append(cave)

        # we randomize which world requirements we fulfill first so we get better dungeon distribution
        if random.randint(0, 1) == 0:
            for entrance in lw_entrances_must_exits:
                connect_reachable_exit(entrance, caves, mandatory_light_world, lw_doors)
            for entrance in dw_entrances_must_exits:
                connect_reachable_exit(entrance, caves, mandatory_dark_world, dw_doors)
        else:
            for entrance in dw_entrances_must_exits:
                connect_reachable_exit(entrance, caves, mandatory_dark_world, dw_doors)
            for entrance in lw_entrances_must_exits:
                connect_reachable_exit(entrance, caves, mandatory_light_world, lw_doors)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        lw_entrances.extend(old_man_entrances)
        random.shuffle(lw_entrances)

        connect_exit(world, 'Old Man Cave Exit (East)', old_man_exit)
        connect_entrance(world, lw_doors.pop(), 'Old Man Cave Exit (East)')
        mandatory_light_world.append('Old Man Cave Exit (West)')

        # we connect up the mandatory associations we have found
        for mandatory in mandatory_light_world:
            if not isinstance(mandatory, tuple):
                mandatory = (mandatory,)
            for exit in mandatory:
                # point out somewhere
                connect_exit(world, exit, lw_entrances.pop())
                # point in from somewhere
                connect_entrance(world, lw_doors.pop(), exit)

        for mandatory in mandatory_dark_world:
            if not isinstance(mandatory, tuple):
                mandatory = (mandatory,)
            for exit in mandatory:
                # point out somewhere
                connect_exit(world, exit, dw_entrances.pop())
                # point in from somewhere
                connect_entrance(world, dw_doors.pop(), exit)

        # handle remaining caves
        while caves:
            # connect highest exit count caves first, prevent issue where we have 2 or 3 exits accross worlds left to fill
            cave_candidate = (None, 0)
            for i, cave in enumerate(caves):
                if isinstance(cave, str):
                    cave = (cave,)
                if len(cave) > cave_candidate[1]:
                    cave_candidate = (i, len(cave))
            cave = caves.pop(cave_candidate[0])

            place_lightworld = random.randint(0, 1) == 0
            if place_lightworld:
                target_doors = lw_doors
                target_entrances = lw_entrances
            else:
                target_doors = dw_doors
                target_entrances = dw_entrances

            if isinstance(cave, str):
                cave = (cave,)

            # check if we can still fit the cave into our target group
            if len(target_doors) < len(cave):
                if not place_lightworld:
                    target_doors = lw_doors
                    target_entrances = lw_entrances
                else:
                    target_doors = dw_doors
                    target_entrances = dw_entrances

            for exit in cave:
                connect_exit(world, exit, target_entrances.pop())
                connect_entrance(world, target_doors.pop(), exit)

        # handle simple doors

        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)

    elif world.shuffle == 'insanity':
        # beware ye who enter here

        entrances = LW_Entrances + LW_Dungeon_Entrances + DW_Entrances + DW_Dungeon_Entrances + ['Skull Woods Second Section Door (East)', 'Skull Woods First Section Door', 'Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Entrance (South)']
        entrances_must_exits = DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + LW_Dungeon_Entrances_Must_Exit + ['Skull Woods Second Section Door (West)']

        doors = LW_Entrances + LW_Dungeon_Entrances + LW_Dungeon_Entrances_Must_Exit + ['Kakariko Well Cave', 'Bat Cave Cave', 'North Fairy Cave', 'Sanctuary', 'Lost Woods Hideout Stump', 'Lumberjack Tree Cave', 'Hyrule Castle Secret Entrance Stairs'] + Old_Man_Entrances +\
                DW_Entrances + DW_Dungeon_Entrances + DW_Entrances_Must_Exit + DW_Dungeon_Entrances_Must_Exit + ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)']

        random.shuffle(doors)

        old_man_entrances = list(Old_Man_Entrances)

        caves = Cave_Exits + Dungeon_Exits + Cave_Three_Exits + ['Old Man House Exit (Bottom)', 'Old Man House Exit (Top)', 'Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)',
                                                                 'Kakariko Well Exit', 'Bat Cave Exit', 'North Fairy Cave Exit', 'Lost Woods Hideout Exit', 'Lumberjack Tree Exit', 'Sanctuary Exit']

        # shuffle up holes

        hole_entrances = ['Kakariko Well Drop', 'Bat Cave Drop', 'North Fairy Cave Drop', 'Lost Woods Hideout Drop', 'Lumberjack Tree Tree', 'Sanctuary Grave',
                          'Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole']

        hole_targets = ['Kakariko Well (top)', 'Bat Cave (right)', 'North Fairy Cave', 'Lost Woods Hideout (top)', 'Lumberjack Tree (top)', 'Sewer Drop', 'Skull Woods Second Section',
                        'Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)']

        if world.mode == 'standard':
            # cannot move uncle cave
            connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance')
            connect_exit(world, 'Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance Stairs')
            connect_entrance(world, doors.pop(), 'Hyrule Castle Secret Entrance Exit')
        else:
            hole_entrances.append('Hyrule Castle Secret Entrance Drop')
            hole_targets.append('Hyrule Castle Secret Entrance')
            entrances.append('Hyrule Castle Secret Entrance Stairs')
            caves.append('Hyrule Castle Secret Entrance Exit')

        if not world.shuffle_ganon:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
            connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit')
            connect_entrance(world, 'Pyramid Hole', 'Pyramid')
        else:
            entrances.append('Ganons Tower')
            caves.extend(['Ganons Tower Exit', 'Pyramid Exit'])
            hole_entrances.append('Pyramid Hole')
            hole_targets.append('Pyramid')
            entrances_must_exits.append('Pyramid Entrance')
            doors.extend(['Ganons Tower', 'Pyramid Entrance'])

        random.shuffle(hole_entrances)
        random.shuffle(hole_targets)
        random.shuffle(entrances)

        # fill up holes
        for hole in hole_entrances:
            connect_entrance(world, hole, hole_targets.pop())

        # hyrule castle handling
        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            connect_entrance(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
            connect_exit(world, 'Hyrule Castle Exit (South)', entrances.pop())
            caves.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            doors.append('Hyrule Castle Entrance (South)')
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))

        # now let's deal with mandatory reachable stuff
        def extract_reachable_exit(cavelist):
            random.shuffle(cavelist)
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
                raise RuntimeError('No suitable cave.')
            cavelist.remove(candidate)
            return candidate

        def connect_reachable_exit(entrance, caves, doors):
            cave = extract_reachable_exit(caves)

            exit = cave[-1]
            cave = cave[:-1]
            connect_exit(world, exit, entrance)
            connect_entrance(world, doors.pop(), exit)
            # rest of cave now is forced to be in this world
            caves.append(cave)

        # connect mandatory exits
        for entrance in entrances_must_exits:
            connect_reachable_exit(entrance, caves, doors)

        # place old man, has limited options
        # exit has to come from specific set of doors, the entrance is free to move about
        random.shuffle(old_man_entrances)
        old_man_exit = old_man_entrances.pop()
        entrances.extend(old_man_entrances)
        random.shuffle(entrances)

        connect_exit(world, 'Old Man Cave Exit (East)', old_man_exit)
        connect_entrance(world, doors.pop(), 'Old Man Cave Exit (East)')
        caves.append('Old Man Cave Exit (West)')

        # handle remaining caves
        for cave in caves:
            if isinstance(cave, str):
                cave = (cave,)

            for exit in cave:
                connect_exit(world, exit, entrances.pop())
                connect_entrance(world, doors.pop(), exit)

        # handle simple doors

        single_doors = list(Single_Cave_Doors)
        bomb_shop_doors = list(Bomb_Shop_Single_Cave_Doors)
        blacksmith_doors = list(Blacksmith_Single_Cave_Doors)
        door_targets = list(Single_Cave_Targets)

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut')
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        connect_entrance(world, bomb_shop, 'Big Bomb Shop')
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        connect_doors(world, ['Tavern North'], ['Tavern'])

        # place remaining doors
        connect_doors(world, single_doors, door_targets)

    else:
        raise NotImplementedError('Shuffling not supported yet')

    # check for swamp palace fix
    if world.get_entrance('Dam').connected_region.name != 'Dam' or world.get_entrance('Swamp Palace').connected_region.name != 'Swamp Palace (Entrance)':
        world.swamp_patch_required = True

    # check for ganon location
    if world.get_entrance('Pyramid Hole').connected_region.name != 'Pyramid':
        world.ganon_at_pyramid = False


def connect_simple(world, exitname, regionname):
    world.get_entrance(exitname).connect(world.get_region(regionname))


def connect_entrance(world, entrancename, exitname):
    entrance = world.get_entrance(entrancename)
    # check if we got an entrance or a region to connect to
    try:
        region = world.get_region(exitname)
        exit = None
    except RuntimeError:
        exit = world.get_entrance(exitname)
        region = exit.parent_region

    # if this was already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)

    target = exit_ids[exit.name][0] if exit is not None else exit_ids.get(region.name, None)
    addresses = door_addresses[entrance.name][0][0] if exit is not None else door_addresses[entrance.name][0]
    try:
        vanilla_ref = door_addresses[entrance.name][1]
        vanilla = exit_ids[vanilla_ref]
    except IndexError:
        vanilla = None

    entrance.connect(region, addresses, target, vanilla)
    world.spoiler.set_entrance(entrance.name, exit.name if exit is not None else region.name, 'entrance')


def connect_exit(world, exitname, entrancename):
    entrance = world.get_entrance(entrancename)
    exit = world.get_entrance(exitname)

    # if this was already connected somewhere, remove the backreference
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    exit.connect(entrance.parent_region, door_addresses[entrance.name][0][1], exit_ids[exit.name][1])
    world.spoiler.set_entrance(entrance.name, exit.name, 'exit')


def connect_two_way(world, entrancename, exitname):
    entrance = world.get_entrance(entrancename)
    exit = world.get_entrance(exitname)

    # if these were already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    entrance.connect(exit.parent_region, door_addresses[entrance.name][0][0], exit_ids[exit.name][0])
    exit.connect(entrance.parent_region, door_addresses[entrance.name][0][1], exit_ids[exit.name][1])
    world.spoiler.set_entrance(entrance.name, exit.name, 'both')


def scramble_holes(world):
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
        connect_two_way(world, 'Pyramid Entrance', 'Pyramid Exit')
        connect_entrance(world, 'Pyramid Hole', 'Pyramid')
    else:
        hole_targets.append(('Pyramid Exit', 'Pyramid'))

    if world.mode == 'standard':
        # cannot move uncle cave
        connect_two_way(world, 'Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Exit')
        connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance')
    else:
        hole_entrances.append(('Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Drop'))
        hole_targets.append(('Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance'))

    # do not shuffle sanctuary into pyramid hole
    if world.shuffle_ganon:
        random.shuffle(hole_targets)
        exit, target = hole_targets.pop()
        connect_two_way(world, 'Pyramid Entrance', exit)
        connect_entrance(world, 'Pyramid Hole', target)
    hole_targets.append(('Sanctuary Exit', 'Sewer Drop'))

    random.shuffle(hole_targets)
    for entrance, drop in hole_entrances:
        exit, target = hole_targets.pop()
        connect_two_way(world, entrance, exit)
        connect_entrance(world, drop, target)


def connect_random(world, exitlist, targetlist, two_way=False):
    targetlist = list(targetlist)
    random.shuffle(targetlist)

    for exit, target in zip(exitlist, targetlist):
        if two_way:
            connect_two_way(world, exit, target)
        else:
            connect_entrance(world, exit, target)


def connect_mandatory_exits(world, entrances, caves, must_be_exits):
    """This works inplace"""
    random.shuffle(entrances)
    random.shuffle(caves)
    while must_be_exits:
        exit = must_be_exits.pop()
        # find multi exit cave
        cave = None
        for candidate in caves:
            if not isinstance(candidate, str):
                cave = candidate
                break

        if cave is None:
            raise RuntimeError('No more caves left. Should not happen!')
        else:
            caves.remove(cave)

        # all caves are sorted so that the last exit is always reachable
        for i in range(len(cave) - 1):
            entrance = entrances.pop()

            # ToDo Better solution, this is a hot fix. Do not connect both sides of trock ledge to each other
            if entrance == 'Dark Death Mountain Ledge (West)':
                new_entrance = entrances.pop()
                entrances.append(entrance)
                entrance = new_entrance

            connect_two_way(world, entrance, cave[i])
        connect_two_way(world, exit, cave[-1])


def connect_caves(world, lw_entrances, dw_entrances, caves):
    """This works inplace"""
    random.shuffle(lw_entrances)
    random.shuffle(dw_entrances)
    random.shuffle(caves)
    while caves:
        # connect highest exit count caves first, prevent issue where we have 2 or 3 exits accross worlds left to fill
        cave_candidate = (None, 0)
        for i, cave in enumerate(caves):
            if isinstance(cave, str):
                cave = (cave,)
            if len(cave) > cave_candidate[1]:
                cave_candidate = (i, len(cave))
        cave = caves.pop(cave_candidate[0])

        target = lw_entrances if random.randint(0, 1) == 0 else dw_entrances
        if isinstance(cave, str):
            cave = (cave,)

        # check if we can still fit the cave into our target group
        if len(target) < len(cave):
            # need to use other set
            target = lw_entrances if target is dw_entrances else dw_entrances

        for exit in cave:
            connect_two_way(world, target.pop(), exit)


def connect_doors(world, doors, targets):
    """This works inplace"""
    random.shuffle(doors)
    random.shuffle(targets)
    while doors:
        door = doors.pop()
        target = targets.pop()
        connect_entrance(world, door, target)


def skull_woods_shuffle(world):
    connect_random(world, ['Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole'],
                   ['Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)', 'Skull Woods Second Section'])
    connect_random(world, ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)'],
                   ['Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)'], True)


def simple_shuffle_dungeons(world):
    skull_woods_shuffle(world)

    dungeon_entrances = ['Eastern Palace', 'Tower of Hera', 'Thieves Town', 'Skull Woods Final Section', 'Palace of Darkness', 'Ice Palace', 'Misery Mire', 'Swamp Palace']
    dungeon_exits = ['Eastern Palace Exit', 'Tower of Hera Exit', 'Thieves Town Exit', 'Skull Woods Final Section Exit', 'Palace of Darkness Exit', 'Ice Palace Exit', 'Misery Mire Exit', 'Swamp Palace Exit']

    if not world.shuffle_ganon:
        connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit')
    else:
        dungeon_entrances.append('Ganons Tower')
        dungeon_exits.append('Ganons Tower Exit')

    # shuffle up single entrance dungeons
    connect_random(world, dungeon_entrances, dungeon_exits, True)

    # mix up 4 door dungeons
    multi_dungeons = ['Desert', 'Turtle Rock']
    if world.mode == 'open':
        multi_dungeons.append('Hyrule Castle')
    random.shuffle(multi_dungeons)

    dp_target = multi_dungeons[0]
    tr_target = multi_dungeons[1]
    if world.mode != 'open':
        # place hyrule castle as intended
        hc_target = 'Hyrule Castle'
    else:
        hc_target = multi_dungeons[2]

    # ToDo improve this?
    if hc_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)')
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Hyrule Castle Exit (East)')
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Hyrule Castle Exit (West)')
        connect_two_way(world, 'Agahnims Tower', 'Agahnims Tower Exit')
    elif hc_target == 'Desert':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Hyrule Castle Exit (South)')
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Hyrule Castle Exit (East)')
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Hyrule Castle Exit (West)')
        connect_two_way(world, 'Desert Palace Entrance (North)', 'Agahnims Tower Exit')
    elif hc_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Hyrule Castle Exit (South)')
        connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Hyrule Castle Exit (East)')
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Hyrule Castle Exit (West)')
        connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Agahnims Tower Exit')

    if dp_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Desert Palace Exit (South)')
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Desert Palace Exit (East)')
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Desert Palace Exit (West)')
        connect_two_way(world, 'Agahnims Tower', 'Desert Palace Exit (North)')
    elif dp_target == 'Desert':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Desert Palace Exit (South)')
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Desert Palace Exit (East)')
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Desert Palace Exit (West)')
        connect_two_way(world, 'Desert Palace Entrance (North)', 'Desert Palace Exit (North)')
    elif dp_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Desert Palace Exit (South)')
        connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Desert Palace Exit (East)')
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Desert Palace Exit (West)')
        connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Desert Palace Exit (North)')

    if tr_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Turtle Rock Exit (Front)')
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Turtle Rock Ledge Exit (East)')
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Turtle Rock Ledge Exit (West)')
        connect_two_way(world, 'Agahnims Tower', 'Turtle Rock Isolated Ledge Exit')
    elif tr_target == 'Desert':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Turtle Rock Exit (Front)')
        connect_two_way(world, 'Desert Palace Entrance (North)', 'Turtle Rock Ledge Exit (East)')
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Turtle Rock Ledge Exit (West)')
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Turtle Rock Isolated Ledge Exit')
    elif tr_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Turtle Rock Exit (Front)')
        connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Turtle Rock Isolated Ledge Exit')
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Turtle Rock Ledge Exit (West)')
        connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Turtle Rock Ledge Exit (East)')


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

LW_Dungeon_Exits = []

Dungeon_Exits = [('Desert Palace Exit (South)', 'Desert Palace Exit (West)', 'Desert Palace Exit (East)'),
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
                 ('Turtle Rock Exit (Front)', 'Turtle Rock Ledge Exit (East)', 'Turtle Rock Ledge Exit (West)', 'Turtle Rock Isolated Ledge Exit')]

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

Cave_Exits = [('Elder House Exit (East)', 'Elder House Exit (West)'),
              ('Two Brothers House Exit (East)', 'Two Brothers House Exit (West)'),
              ('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave Exit (East)'),
              ('Fairy Ascension Cave Exit (Bottom)', 'Fairy Ascension Cave Exit (Top)'),
              ('Spiral Cave Exit (Top)', 'Spiral Cave Exit'),
              ('Bumper Cave Exit (Top)', 'Bumper Cave Exit (Bottom)'),
              ('Superbunny Cave Exit (Bottom)', 'Superbunny Cave Exit (Top)'),
              ('Hookshot Cave Exit (South)', 'Hookshot Cave Exit (North)')]

Cave_Three_Exits = [('Spectacle Rock Cave Exit (Peak)', 'Spectacle Rock Cave Exit (Top)', 'Spectacle Rock Cave Exit'),
                    ('Paradox Cave Exit (Top)', 'Paradox Cave Exit (Middle)', 'Paradox Cave Exit (Bottom)')]

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

Blacksmith_Single_Cave_Doors = ['Blinds Hideout',
                                'Lake Hylia Fairy',
                                'Swamp Fairy',
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
                               'Dark World Shop',
                               'Dark World Lumberjack Shop',
                               'Dark World Potion Shop',
                               'Archery Game',
                               'Mire Shed',
                               'Dark Desert Hint',
                               'Dark Desert Fairy',
                               'Spike Cave',
                               'Cave Shop (Dark Death Mountain)',
                               'Dark Death Mountain Fairy',
                               'Mimic Cave Mirror Spot',
                               'Big Bomb Shop',
                               'Dark Lake Hylia Shop']

Single_Cave_Doors = ['Pyramid Fairy']

Single_Cave_Targets = ['Blinds Hideout',
                       'Bonk Fairy',
                       'Healer Fairy',
                       'Healer Fairy',
                       'Healer Fairy',
                       'Kings Grave',
                       'Chicken House',
                       'Aginahs Cave',
                       'Sahasrahlas Hut',
                       'Cave Shop',
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
                       'Healer Fairy',
                       'Healer Fairy',
                       'Dark Lake Hylia Ledge Spike Cave',
                       'Dark Lake Hylia Ledge Hint',
                       'Hype Cave',
                       'Bonk Fairy',
                       'Brewery',
                       'C-Shaped House',
                       'Chest Game',
                       'Dark World Hammer Peg Cave',
                       'Red Shield Shop',
                       'Dark Sanctuary Hint',
                       'Fortune Teller (Dark)',
                       'Dark World Shop',
                       'Dark World Shop',
                       'Dark World Shop',
                       'Archery Game',
                       'Mire Shed',
                       'Dark Desert Hint',
                       'Healer Fairy',
                       'Spike Cave',
                       'Cave Shop',
                       'Healer Fairy',
                       'Mimic Cave',
                       'Dark World Shop',
                       'Lumberjack House',
                       'Fortune Teller (Light)',
                       'Kakariko Gamble Game',
                       'Dam']

# these are connections that cannot be shuffled and always exist. They link together separate parts of the world we need to divide into regions
mandatory_connections = [('Links House', 'Links House'),  # unshuffled. For now
                         ('Links House Exit', 'Light World'),

                         ('Lake Hylia Central Island Pier', 'Lake Hylia Central Island'),
                         ('Lake Hylia Central Island Teleporter', 'Dark Lake Hylia Central Island'),
                         ('Zoras River', 'Zoras River'),
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
                         ('Throne Room', 'Sewers (Dark)'),
                         ('Sewers Door', 'Sewers'),
                         ('Sanctuary Push Door', 'Sanctuary'),
                         ('Sewer Drop', 'Sewers'),
                         ('Sewers Back Door', 'Sewers (Dark)'),
                         ('Agahnim 1', 'Agahnim 1'),
                         ('Flute Spot 1', 'Death Mountain'),
                         ('Spectacle Rock Cave Drop', 'Spectacle Rock Cave (Bottom)'),
                         ('Spectacle Rock Cave Peak Drop', 'Spectacle Rock Cave (Bottom)'),
                         ('Death Mountain Return Ledge Drop', 'Light World'),
                         ('Broken Bridge (West)', 'East Death Mountain (Bottom)'),
                         ('Broken Bridge (East)', 'Death Mountain'),
                         ('East Death Mountain Drop', 'East Death Mountain (Bottom)'),
                         ('Spiral Cave Ledge Access', 'Spiral Cave Ledge'),
                         ('Spiral Cave Ledge Drop', 'East Death Mountain (Bottom)'),
                         ('Spiral Cave (top to bottom)', 'Spiral Cave (Bottom)'),
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
                         ('Bat Cave Drop Ledge Mirror Spot', 'Bat Cave Drop Ledge'),
                         ('East Dark World River Pier', 'East Dark World'),
                         ('West Dark World Gap', 'West Dark World'),
                         ('Bumper Cave Ledge Drop', 'West Dark World'),
                         ('Bumper Cave Ledge Mirror Spot', 'Death Mountain Return Ledge'),
                         ('Skull Woods Forest', 'Skull Woods Forest'),
                         ('Desert Ledge Mirror Spot', 'Desert Ledge'),
                         ('Desert Ledge (West) Mirror Spot', 'Desert Ledge (West)'),
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
                         ('Fairy Ascension Rocks', 'Fairy Ascension Plateau'),
                         ('Fairy Ascension Mirror Spot', 'Fairy Ascension Plateau'),
                         ('Fairy Ascension Drop', 'East Death Mountain (Bottom)'),
                         ('Fairy Ascension Ledge Drop', 'Fairy Ascension Plateau'),
                         ('Fairy Ascension Ledge', 'Fairy Ascension Ledge'),
                         ('Spectacle Rock Mirror Spot', 'Spectacle Rock'),
                         ('Dark Death Mountain Drop (East)', 'Dark Death Mountain (East Bottom)'),
                         ('Dark Death Mountain Drop (West)', 'Dark Death Mountain (West Bottom)'),
                         ('East Death Mountain (Top) Mirror Spot', 'East Death Mountain (Top)'),
                         ('Turtle Rock Teleporter', 'Turtle Rock (Top)'),
                         ('Turtle Rock Drop', 'Dark Death Mountain (Top)'),
                         ('Floating Island Drop', 'Dark Death Mountain (Top)'),
                         ('East Death Mountain Teleporter', 'Dark Death Mountain (East Bottom)'),
                         ('Isolated Ledge Mirror Spot', 'Fairy Ascension Ledge'),
                         ('Spiral Cave Mirror Spot', 'Spiral Cave Ledge'),

                         ('Swamp Palace Moat', 'Swamp Palace (First Room)'),
                         ('Swamp Palace Small Key Door', 'Swamp Palace (Starting Area)'),
                         ('Swamp Palace (Center)', 'Swamp Palace (Center)'),
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
                         ('Blind Fight', 'Blind Fight'),
                         ('Ice Palace Entrance Room', 'Ice Palace (Main)'),
                         ('Ice Palace (East)', 'Ice Palace (East)'),
                         ('Ice Palace (East Top)', 'Ice Palace (East Top)'),
                         ('Ice Palace (Kholdstare)', 'Ice Palace (Kholdstare)'),
                         ('Misery Mire Entrance Gap', 'Misery Mire (Main)'),
                         ('Misery Mire (West)', 'Misery Mire (West)'),
                         ('Misery Mire Big Key Door', 'Misery Mire (Final Area)'),
                         ('Misery Mire (Vitreous)', 'Misery Mire (Vitreous)'),
                         ('Turtle Rock Entrance Gap', 'Turtle Rock (First Section)'),
                         ('Turtle Rock Entrance Gap Reverse', 'Turtle Rock (Entrance)'),
                         ('Turtle Rock Pokey Room', 'Turtle Rock (Chain Chomp Room)'),
                         ('Turtle Rock (Chain Chomp Room) (North)', 'Turtle Rock (Second Section)'),
                         ('Turtle Rock (Chain Chomp Room) (South)', 'Turtle Rock (First Section)'),
                         ('Turtle Rock Chain Chomp Staircase', 'Turtle Rock (Chain Chomp Room)'),
                         ('Turtle Rock (Big Chest) (North)', 'Turtle Rock (Second Section)'),
                         ('Turtle Rock Big Key Door', 'Turtle Rock (Crystaroller Room)'),
                         ('Turtle Rock Big Key Door Reverse', 'Turtle Rock (Second Section)'),
                         ('Turtle Rock Dark Room Staircase', 'Turtle Rock (Dark Room)'),
                         ('Turtle Rock (Dark Room) (North)', 'Turtle Rock (Crystaroller Room)'),
                         ('Turtle Rock (Dark Room) (South)', 'Turtle Rock (Eye Bridge)'),
                         ('Turtle Rock Dark Room (South)', 'Turtle Rock (Dark Room)'),
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

# non-shuffled entrance links
default_connections = [('Waterfall of Wishing', 'Waterfall of Wishing'),
                       ("Blinds Hideout", "Blinds Hideout"),
                       ('Dam', 'Dam'),
                       ('Lumberjack House', 'Lumberjack House'),
                       ("Hyrule Castle Secret Entrance Drop", "Hyrule Castle Secret Entrance"),
                       ("Hyrule Castle Secret Entrance Stairs", "Hyrule Castle Secret Entrance"),
                       ("Hyrule Castle Secret Entrance Exit", "Light World"),
                       ('Bonk Fairy (Light)', 'Bonk Fairy'),
                       ('Lake Hylia Fairy', 'Healer Fairy'),
                       ('Lake Hylia Fortune Teller', 'Fortune Teller (Light)'),
                       ('Swamp Fairy', 'Healer Fairy'),
                       ('Desert Fairy', 'Healer Fairy'),
                       ('Kings Grave', 'Kings Grave'),
                       ('Tavern North', 'Tavern'),
                       ('Chicken House', 'Chicken House'),
                       ('Aginahs Cave', 'Aginahs Cave'),
                       ('Sahasrahlas Hut', 'Sahasrahlas Hut'),
                       ('Cave Shop (Lake Hylia)', 'Cave Shop'),
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
                       ('Old Man Cave Exit (West)', 'Death Mountain'),
                       ('Old Man Cave Exit (East)', 'Light World'),
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
                       ('Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave'),
                       ('Fairy Ascension Cave (Top)', 'Fairy Ascension Cave'),
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
                       ('Dark Lake Hylia Shop', 'Dark World Shop'),
                       ('Dark Lake Hylia Fairy', 'Healer Fairy'),
                       ('Dark Lake Hylia Ledge Fairy', 'Healer Fairy'),
                       ('Dark Lake Hylia Ledge Spike Cave', 'Dark Lake Hylia Ledge Spike Cave'),
                       ('Dark Lake Hylia Ledge Hint', 'Dark Lake Hylia Ledge Hint'),
                       ('Hype Cave', 'Hype Cave'),
                       ('Bonk Fairy (Dark)', 'Bonk Fairy'),
                       ('Brewery', 'Brewery'),
                       ('C-Shaped House', 'C-Shaped House'),
                       ('Chest Game', 'Chest Game'),
                       ('Dark World Hammer Peg Cave', 'Dark World Hammer Peg Cave'),
                       ('Bumper Cave (Bottom)', 'Bumper Cave'),
                       ('Bumper Cave (Top)', 'Bumper Cave'),
                       ('Red Shield Shop', 'Red Shield Shop'),
                       ('Dark Sanctuary Hint', 'Dark Sanctuary Hint'),
                       ('Fortune Teller (Dark)', 'Fortune Teller (Dark)'),
                       ('Dark World Shop', 'Dark World Shop'),
                       ('Dark World Lumberjack Shop', 'Dark World Shop'),
                       ('Dark World Potion Shop', 'Dark World Shop'),
                       ('Archery Game', 'Archery Game'),
                       ('Bumper Cave Exit (Top)', 'Bumper Cave Ledge'),
                       ('Bumper Cave Exit (Bottom)', 'West Dark World'),
                       ('Mire Shed', 'Mire Shed'),
                       ('Dark Desert Hint', 'Dark Desert Hint'),
                       ('Dark Desert Fairy', 'Healer Fairy'),
                       ('Spike Cave', 'Spike Cave'),
                       ('Hookshot Cave', 'Hookshot Cave'),
                       ('Superbunny Cave (Top)', 'Superbunny Cave'),
                       ('Cave Shop (Dark Death Mountain)', 'Cave Shop'),
                       ('Dark Death Mountain Fairy', 'Healer Fairy'),
                       ('Superbunny Cave (Bottom)', 'Superbunny Cave'),
                       ('Superbunny Cave Exit (Top)', 'Dark Death Mountain (Top)'),
                       ('Superbunny Cave Exit (Bottom)', 'Dark Death Mountain (East Bottom)'),
                       ('Hookshot Cave Exit (South)', 'Dark Death Mountain (Top)'),
                       ('Hookshot Cave Exit (North)', 'Death Mountain Floating Island'),
                       ('Hookshot Cave Back Entrance', 'Hookshot Cave'),
                       ('Mimic Cave Mirror Spot', 'Mimic Cave'),

                       ('Pyramid Hole', 'Pyramid'),
                       ('Pyramid Exit', 'Pyramid Ledge'),
                       ('Pyramid Entrance', 'Bottom of Pyramid')
                       ]

# non shuffled dungeons
default_dungeon_connections = [('Desert Palace Entrance (South)', 'Desert Palace Main'),
                               ('Desert Palace Entrance (West)', 'Desert Palace Main'),
                               ('Desert Palace Entrance (North)', 'Desert Palace North'),
                               ('Desert Palace Entrance (East)', 'Desert Palace Main'),
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
                               ('Agahnims Tower', 'Agahnims Tower'),
                               ('Agahnims Tower Exit', 'Hyrule Castle Ledge'),

                               ('Thieves Town', 'Thieves Town (Entrance)'),
                               ('Thieves Town Exit', 'West Dark World'),
                               ('Skull Woods First Section Hole (East)', 'Skull Woods First Section (Right)'),
                               ('Skull Woods First Section Hole (West)', 'Skull Woods First Section (Left)'),
                               ('Skull Woods First Section Hole (North)', 'Skull Woods First Section (Top)'),
                               ('Skull Woods First Section Door', 'Skull Woods First Section'),
                               ('Skull Woods First Section Exit', 'Skull Woods Forest'),
                               ('Skull Woods Second Section Hole', 'Skull Woods Second Section'),
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


# ToDo somehow merge this with creation of the locations
door_addresses = {'Desert Palace Entrance (South)': ((0xDBB7B, 0x15B02),),
                  'Desert Palace Entrance (West)': ((0xDBB7D, 0x15B06),),
                  'Desert Palace Entrance (North)': ((0xDBB7E, 0x15B08),),
                  'Desert Palace Entrance (East)': ((0xDBB7C, 0x15B04),),
                  'Eastern Palace': ((0xDBB7A, 0x15B00),),
                  'Tower of Hera': ((0xDBBA5, 0x15B48),),
                  'Hyrule Castle Entrance (South)': ((0xDBB76, 0x15AF4),),
                  'Hyrule Castle Entrance (West)': ((0xDBB75, 0x15AF2),),
                  'Hyrule Castle Entrance (East)': ((0xDBB77, 0x15AF6),),
                  'Agahnims Tower': ((0xDBB96, 0x15B38),),
                  'Thieves Town': ((0xDBBA6, 0x15B58),),
                  'Skull Woods First Section Door': ((0xDBB9C, 0x15B44),),
                  'Skull Woods Second Section Door (East)': ((0xDBB9B, 0x15B42),),
                  'Skull Woods Second Section Door (West)': ((0xDBB9A, 0x15B40),),
                  'Skull Woods Final Section': ((0xDBB9D, 0x15B46),),
                  'Ice Palace': ((0xDBB9F, 0x15B4A),),
                  'Misery Mire': ((0xDBB99, 0x15B3E),),
                  'Palace of Darkness': ((0xDBB98, 0x15B3C),),
                  'Swamp Palace': ((0xDBB97, 0x15B3A),),
                  'Turtle Rock': ((0xDBBA7, 0x15B56),),
                  'Dark Death Mountain Ledge (West)': ((0xDBB87, 0x15B1A),),
                  'Dark Death Mountain Ledge (East)': ((0xDBB8B, 0x15B22),),
                  'Turtle Rock Isolated Ledge Entrance': ((0xDBB8A, 0x15B20),),
                  'Hyrule Castle Secret Entrance Stairs': ((0xDBBA4, 0x15B54),),
                  'Kakariko Well Cave': ((0xDBBAB, 0x15B62),),
                  'Bat Cave Cave': ((0xDBB83, 0x15B12),),
                  'Elder House (East)': ((0xDBB80, 0x15B0C),),
                  'Elder House (West)': ((0xDBB7F, 0x15B0A),),
                  'North Fairy Cave': ((0xDBBAA, 0x15B60),),
                  'Lost Woods Hideout Stump': ((0xDBB9E, 0x15B5A),),
                  'Lumberjack Tree Cave': ((0xDBB84, 0x15B14),),
                  'Two Brothers House (East)': ((0xDBB82, 0x15B10),),
                  'Two Brothers House (West)': ((0xDBB81, 0x15B0E),),
                  'Sanctuary': ((0xDBB74, 0x15AF0),),
                  'Old Man Cave (West)': ((0xDBB78, 0x15AFC),),
                  'Old Man Cave (East)': ((0xDBB79, 0x15AFE),),
                  'Old Man House (Bottom)': ((0xDBBA2, 0x15B50),),
                  'Old Man House (Top)': ((0xDBBA3, 0x15B52),),
                  'Death Mountain Return Cave (East)': ((0xDBBA1, 0x15B4E),),
                  'Death Mountain Return Cave (West)': ((0xDBBA0, 0x15B4C),),
                  'Spectacle Rock Cave Peak': ((0xDBB95, 0x15B36),),
                  'Spectacle Rock Cave': ((0xDBB94, 0x15B34),),
                  'Spectacle Rock Cave (Bottom)': ((0xDBB93, 0x15B32),),
                  'Paradox Cave (Bottom)': ((0xDBB90, 0x15B2C),),
                  'Paradox Cave (Middle)': ((0xDBB91, 0x15B2E),),
                  'Paradox Cave (Top)': ((0xDBB92, 0x15B30),),
                  'Fairy Ascension Cave (Bottom)': ((0xDBB8C, 0x15B24),),
                  'Fairy Ascension Cave (Top)': ((0xDBB8D, 0x15B26),),
                  'Spiral Cave': ((0xDBB8F, 0x15B2A),),
                  'Spiral Cave (Bottom)': ((0xDBB8E, 0x15B28),),
                  'Bumper Cave (Bottom)': ((0xDBB88, 0x15B1C),),
                  'Bumper Cave (Top)': ((0xDBB89, 0x15B1E),),
                  'Superbunny Cave (Top)': ((0xDBB86, 0x15B18),),
                  'Superbunny Cave (Bottom)': ((0xDBB85, 0x15B16),),
                  'Hookshot Cave': ((0xDBBAC, 0x15B64),),
                  'Hookshot Cave Back Entrance': ((0xDBBAD, 0x15B66),),
                  'Ganons Tower': ((0xDBBA9, 0x15B5E),),
                  'Pyramid Entrance': ((0xDBBA8, 0x15B5C),),
                  'Skull Woods First Section Hole (East)': ((0xDB84D, 0xDB84E),),
                  'Skull Woods First Section Hole (West)': ((0xDB84F, 0xDB850),),
                  'Skull Woods First Section Hole (North)': (0xDB84C,),
                  'Skull Woods Second Section Hole': ((0xDB851, 0xDB852),),
                  'Pyramid Hole': ((0xDB854, 0xDB855, 0xDB856),),
                  'Waterfall of Wishing': (0xDBBCE, 'Waterfall of Wishing'),
                  'Dam': (0xDBBC0, 'Dam'),
                  'Blinds Hideout': (0xDBBD3, 'Blinds Hideout'),
                  'Hyrule Castle Secret Entrance Drop': (0xDB858,),
                  'Bonk Fairy (Light)': (0xDBBE9, 'Bonk Fairy'),
                  'Lake Hylia Fairy': (0xDBBD0, 'Healer Fairy'),
                  'Swamp Fairy': (0xDBBDE, 'Healer Fairy'),
                  'Desert Fairy': (0xDBBE4, 'Healer Fairy'),
                  'Kings Grave': (0xDBBCD, 'Kings Grave'),
                  'Tavern North': (0xDBBB5, 'Tavern'),  # do not use, buggy
                  'Chicken House': (0xDBBBD, 'Chicken House'),
                  'Aginahs Cave': (0xDBBE3, 'Aginahs Cave'),
                  'Sahasrahlas Hut': (0xDBBB7, 'Sahasrahlas Hut'),
                  'Cave Shop (Lake Hylia)': (0xDBBCA, 'Cave Shop'),
                  'Capacity Upgrade': (0xDBBCF, 'Capacity Upgrade'),
                  'Kakariko Well Drop': ((0xDB85C, 0xDB85D),),
                  'Blacksmiths Hut': (0xDBBD6, 'Blacksmiths Hut'),
                  'Bat Cave Drop': ((0xDB859, 0xDB85A),),
                  'Sick Kids House': (0xDBBB2, 'Sick Kids House'),
                  'North Fairy Cave Drop': (0xDB857,),
                  'Lost Woods Gamble': (0xDBBAE, 'Lost Woods Gamble'),
                  'Fortune Teller (Light)': (0xDBBD7, 'Fortune Teller (Light)'),
                  'Snitch Lady (East)': (0xDBBB0, 'Snitch Lady (East)'),
                  'Snitch Lady (West)': (0xDBBB1, 'Snitch Lady (West)'),
                  'Bush Covered House': (0xDBBB6, 'Bush Covered House'),
                  'Tavern (Front)': (0xDBBB4, 'Tavern (Front)'),
                  'Light World Bomb Hut': (0xDBBBC, 'Light World Bomb Hut'),
                  'Kakariko Shop': (0xDBBB8, 'Kakariko Shop'),
                  'Lost Woods Hideout Drop': (0xDB853,),
                  'Lumberjack Tree Tree': (0xDB85B,),
                  'Cave 45': (0xDBBC3, 'Cave 45'),
                  'Graveyard Cave': (0xDBBC4, 'Graveyard Cave'),
                  'Checkerboard Cave': (0xDBBF0, 'Checkerboard Cave'),
                  'Mini Moldorm Cave': (0xDBBEF, 'Mini Moldorm Cave'),
                  'Long Fairy Cave': (0xDBBC7, 'Long Fairy Cave'),
                  'Good Bee Cave': (0xDBBDD, 'Good Bee Cave'),
                  '20 Rupee Cave': (0xDBBED, '20 Rupee Cave'),
                  '50 Rupee Cave': (0xDBBEB, '50 Rupee Cave'),
                  'Ice Rod Cave': (0xDBBF2, 'Ice Rod Cave'),
                  'Bonk Rock Cave': (0xDBBEC, 'Bonk Rock Cave'),
                  'Library': (0xDBBBB, 'Library'),
                  'Potion Shop': (0xDBBBE, 'Potion Shop'),
                  'Sanctuary Grave': (0xDB85E,),
                  'Hookshot Fairy': (0xDBBC2, 'Hookshot Fairy'),
                  'Pyramid Fairy': (0xDBBD5, 'Pyramid Fairy'),
                  'East Dark World Hint': (0xDBBDB, 'East Dark World Hint'),
                  'Palace of Darkness Hint': (0xDBBDA, 'Palace of Darkness Hint'),
                  'Dark Lake Hylia Fairy': (0xDBBDF, 'Healer Fairy'),
                  'Dark Lake Hylia Ledge Fairy': (0xDBBF3, 'Healer Fairy'),
                  'Dark Lake Hylia Ledge Spike Cave': (0xDBBEE, 'Dark Lake Hylia Ledge Spike Cave'),
                  'Dark Lake Hylia Ledge Hint': (0xDBBDC, 'Dark Lake Hylia Ledge Hint'),
                  'Hype Cave': (0xDBBAF, 'Hype Cave'),
                  'Bonk Fairy (Dark)': (0xDBBEA, 'Bonk Fairy'),
                  'Brewery': (0xDBBBA, 'Brewery'),
                  'C-Shaped House': (0xDBBC6, 'C-Shaped House'),
                  'Chest Game': (0xDBBB9, 'Chest Game'),
                  'Dark World Hammer Peg Cave': (0xDBBF1, 'Dark World Hammer Peg Cave'),
                  'Red Shield Shop': (0xDBBE7, 'Red Shield Shop'),
                  'Dark Sanctuary Hint': (0xDBBCC, 'Dark Sanctuary Hint'),
                  'Fortune Teller (Dark)': (0xDBBD8, 'Fortune Teller (Dark)'),
                  'Dark World Shop': (0xDBBD2, 'Dark World Shop'),
                  'Dark World Lumberjack Shop': (0xDBBC9, 'Dark World Shop'),
                  'Dark World Potion Shop': (0xDBBE1, 'Dark World Shop'),
                  'Archery Game': (0xDBBCB, 'Archery Game'),
                  'Mire Shed': (0xDBBD1, 'Mire Shed'),
                  'Dark Desert Hint': (0xDBBD4, 'Dark Desert Hint'),
                  'Dark Desert Fairy': (0xDBBC8, 'Healer Fairy'),
                  'Spike Cave': (0xDBBB3, 'Spike Cave'),
                  'Cave Shop (Dark Death Mountain)': (0xDBBE0, 'Cave Shop'),
                  'Dark Death Mountain Fairy': (0xDBBE2, 'Healer Fairy'),
                  'Mimic Cave Mirror Spot': (0xDBBC1, 'Mimic Cave'),
                  'Big Bomb Shop': (0xDBBC5, 'Big Bomb Shop'),
                  'Dark Lake Hylia Shop': (0xDBBE6, 'Dark World Shop'),
                  'Lumberjack House': (0xDBBE8, 'Lumberjack House'),
                  'Lake Hylia Fortune Teller': (0xDBBE5, 'Fortune Teller (Light)'),
                  'Kakariko Gamble Game': (0xDBBD9, 'Kakariko Gamble Game')}

exit_ids = {'Desert Palace Exit (South)': (0x09, 0x84),
            'Desert Palace Exit (West)': (0x0B, 0x83),
            'Desert Palace Exit (East)': (0x0A, 0x85),
            'Desert Palace Exit (North)': (0x0C, 0x63),
            'Eastern Palace Exit': (0x08, 0xC9),
            'Tower of Hera Exit': (0x33, 0x77),
            'Hyrule Castle Exit (South)': (0x04, 0x61),
            'Hyrule Castle Exit (West)': (0x03, 0x60),
            'Hyrule Castle Exit (East)': (0x05, 0x62),
            'Agahnims Tower Exit': (0x24, 0xE0),
            'Thieves Town Exit': (0x34, 0xDB),
            'Skull Woods First Section Exit': (0x2A, 0x58),
            'Skull Woods Second Section Exit (East)': (0x29, 0x57),
            'Skull Woods Second Section Exit (West)': (0x28, 0x56),
            'Skull Woods Final Section Exit': (0x2B, 0x59),
            'Ice Palace Exit': (0x2D, 0x0E),
            'Misery Mire Exit': (0x27, 0x98),
            'Palace of Darkness Exit': (0x26, 0x4A),
            'Swamp Palace Exit': (0x25, 0x28),
            'Turtle Rock Exit (Front)': (0x35, 0xD6),
            'Turtle Rock Ledge Exit (West)': (0x15, 0x23),
            'Turtle Rock Ledge Exit (East)': (0x19, 0x24),
            'Turtle Rock Isolated Ledge Exit': (0x18, 0xD5),
            'Hyrule Castle Secret Entrance Exit': (0x32, 0x55),
            'Kakariko Well Exit': (0x39, 0x2F),
            'Bat Cave Exit': (0x11, 0xE3),
            'Elder House Exit (East)': (0x0E, 0xF3),
            'Elder House Exit (West)': (0x0D, 0xF2),
            'North Fairy Cave Exit': (0x38, 0x08),
            'Lost Woods Hideout Exit': (0x2C, 0xE1),
            'Lumberjack Tree Exit': (0x12, 0xE2),
            'Two Brothers House Exit (East)': (0x10, 0xF5),
            'Two Brothers House Exit (West)': (0x0F, 0xF4),
            'Sanctuary Exit': (0x02, 0x12),
            'Old Man Cave Exit (East)': (0x07, 0xF1),
            'Old Man Cave Exit (West)': (0x06, 0xF0),
            'Old Man House Exit (Bottom)': (0x30, 0xE4),
            'Old Man House Exit (Top)': (0x31, 0xE5),
            'Death Mountain Return Cave Exit (West)': (0x2E, 0xE6),
            'Death Mountain Return Cave Exit (East)': (0x2F, 0xE7),
            'Spectacle Rock Cave Exit': (0x21, 0xF9),
            'Spectacle Rock Cave Exit (Top)': (0x22, 0xFA),
            'Spectacle Rock Cave Exit (Peak)': (0x23, 0xEA),
            'Paradox Cave Exit (Bottom)': (0x1E, 0xFF),
            'Paradox Cave Exit (Middle)': (0x1F, 0xEF),
            'Paradox Cave Exit (Top)': (0x20, 0xDF),
            'Fairy Ascension Cave Exit (Bottom)': (0x1A, 0xFD),
            'Fairy Ascension Cave Exit (Top)': (0x1B, 0xED),
            'Spiral Cave Exit': (0x1C, 0xFE),
            'Spiral Cave Exit (Top)': (0x1D, 0xEE),
            'Bumper Cave Exit (Top)': (0x17, 0xEB),
            'Bumper Cave Exit (Bottom)': (0x16, 0xFB),
            'Superbunny Cave Exit (Top)': (0x14, 0xE8),
            'Superbunny Cave Exit (Bottom)': (0x13, 0xF8),
            'Hookshot Cave Exit (South)': (0x3A, 0x3C),
            'Hookshot Cave Exit (North)': (0x3B, 0x2C),
            'Ganons Tower Exit': (0x37, 0x0C),
            'Pyramid Exit': (0x36, 0x10),
            'Waterfall of Wishing': 0x5C,
            'Dam': 0x4E,
            'Blinds Hideout': 0x61,
            'Lumberjack House': 0x6B,
            'Bonk Fairy': 0x71,
            'Healer Fairy': 0x5E,
            'Fortune Teller (Light)': 0x65,
            'Kings Grave': 0x5B,
            'Tavern': 0x43,
            'Chicken House': 0x4B,
            'Aginahs Cave': 0x4D,
            'Sahasrahlas Hut': 0x45,
            'Cave Shop': 0x58,
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
            'Dark World Shop': 0x60,
            'Dark Lake Hylia Ledge Spike Cave': 0x70,
            'Dark Lake Hylia Ledge Hint': 0x6A,
            'Hype Cave': 0x3D,
            'Brewery': 0x48,
            'C-Shaped House': 0x54,
            'Chest Game': 0x47,
            'Dark World Hammer Peg Cave': 0x83,
            'Red Shield Shop': 0x57,
            'Dark Sanctuary Hint': 0x5A,
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
            'Skull Woods Second Section': 0x79,
            'Skull Woods First Section (Left)': 0x77,
            'Skull Woods First Section (Right)': 0x78,
            'Skull Woods First Section (Top)': 0x76,
            'Pyramid': 0x7B}
