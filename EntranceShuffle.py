import random


def link_entrances(world):
    ret = []
    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname)

    # if we do not shuffle, set default connections
    if world.shuffle == 'default':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)
        for exitname, regionname in default_dungeon_connections:
            connect_simple(world, exitname, regionname)

    elif world.shuffle == 'dungeonssimple':
        ret.append('Mixed Entrances:\n\n')

        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)

        ret.append(simple_shuffle_dungeons(world))

    elif world.shuffle == 'dungeonsfull':
        ret.append('Mixed Entrances:\n\n')

        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)

        ret.append(skull_woods_shuffle(world))

        dungeon_exits = list(Dungeon_Exits)
        lw_entrances = list(LW_Dungeon_Entrances)
        dw_entrances = list(DW_Dungeon_Entrances)

        if world.mode == 'standard':
            # must connect front of hyrule castle to do escape
            ret.append(connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)'))
            dungeon_exits.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            dungeon_exits.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        ret.append(connect_mandatory_exits(world, lw_entrances, dungeon_exits, list(LW_Dungeon_Entrances_Must_Exit)))
        ret.append(connect_mandatory_exits(world, dw_entrances, dungeon_exits, list(DW_Dungeon_Entrances_Must_Exit)))
        ret.append(connect_caves(world, lw_entrances, [], list(LW_Dungeon_Exits)))  # Aghanim must be light world
        ret.append(connect_caves(world, lw_entrances, dw_entrances, dungeon_exits))

    elif world.shuffle == 'simple':
        ret.append('Mixed Entrances:\n\n')

        ret.append(simple_shuffle_dungeons(world))

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
        ret.append(connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits))
        # add three exit doors to pool for remainder
        caves.extend(three_exit_caves)

        # place old man, has limited options
        ret.append(connect_caves(world, old_man_entrances, [], [('Old Man Cave Exit (West)', 'Old Man Cave Exit (East)')]))
        # merge with remainder of lw entrances
        lw_entrances.extend(old_man_entrances)

        # place Old Man House in Light World, so using the s&q point does not cause fake dark world
        ret.append(connect_caves(world, lw_entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')]))

        # connect rest. There's 2 dw entrances remaining, so we will not run into parity issue placing caves
        ret.append(connect_caves(world, lw_entrances, dw_entrances, caves))

        # scramble holes
        ret.append(scramble_holes(world))

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        ret.append(connect_one_way(world, blacksmith_hut, 'Blacksmiths Hut'))
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        # ToDo Dam might be behind fat fairy if we later check for this when placing crystal 5 and 6
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        ret.append(connect_one_way(world, bomb_shop, 'Big Bomb Shop'))
        dam = bomb_shop_doors.pop()
        ret.append(connect_one_way(world, dam, 'Dam'))
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        ret.append(connect_doors(world, ['Tavern North'], ['Tavern']))

        # place remaining doors
        ret.append(connect_doors(world, single_doors, door_targets))

    elif world.shuffle == 'full':
        ret.append('Mixed Entrances:\n\n')

        ret.append(skull_woods_shuffle(world))

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
            ret.append(connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)'))
            caves.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
            lw_entrances.append('Hyrule Castle Entrance (South)')

        ret.append(connect_mandatory_exits(world, lw_entrances, caves, lw_must_exits))
        ret.append(connect_mandatory_exits(world, dw_entrances, caves, dw_must_exits))
        ret.append(connect_caves(world, lw_entrances, [], list(LW_Dungeon_Exits)))  # Aghanim must be light world

        # place old man, has limited options
        ret.append(connect_caves(world, old_man_entrances, [], [('Old Man Cave Exit (West)', 'Old Man Cave Exit (East)')]))
        # merge with remainder of lw entrances
        lw_entrances.extend(old_man_entrances)

        # place Old Man House in Light World, so using the s&q point does not cause fake dark world
        ret.append(connect_caves(world, lw_entrances, [], [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')]))

        # now scramble the rest
        ret.append(connect_caves(world, lw_entrances, dw_entrances, caves))

        # scramble holes
        ret.append(scramble_holes(world))

        # place blacksmith, has limited options
        random.shuffle(blacksmith_doors)
        blacksmith_hut = blacksmith_doors.pop()
        ret.append(connect_one_way(world, blacksmith_hut, 'Blacksmiths Hut'))
        bomb_shop_doors.extend(blacksmith_doors)

        # place dam and pyramid fairy, have limited options
        # ToDo Dam might be behind fat fairy if we later check for this when placing crystal 5 and 6
        random.shuffle(bomb_shop_doors)
        bomb_shop = bomb_shop_doors.pop()
        ret.append(connect_one_way(world, bomb_shop, 'Big Bomb Shop'))
        dam = bomb_shop_doors.pop()
        ret.append(connect_one_way(world, dam, 'Dam'))
        single_doors.extend(bomb_shop_doors)

        # tavern back door cannot be shuffled yet
        ret.append(connect_doors(world, ['Tavern North'], ['Tavern']))

        # place remaining doors
        ret.append(connect_doors(world, single_doors, door_targets))

    else:
        raise NotImplementedError('Shuffling not supported yet')

    if world.aghanim_fix_required:
        # need to swap contents of Mimic Cave and TRock Ledge Right so Aghanim 1 is in Light World!
        ret.append('Fix to prevent Aghanim Softlock: Swap Contents of Turtle Rock Ledge (East) and Mimic Cave:')
        mimic_cave_target = world.get_entrance('Mimic Cave Mirror Spot').connected_region
        ret.append(connect_one_way(world, 'Dark Death Mountain Ledge (East)', mimic_cave_target))
        ret.append(connect_one_way(world, 'Mimic Cave Mirror Spot', 'Aghanims Tower'))

    # check for swamp palace fix
    if world.get_entrance('Dam').connected_region.name != 'Dam' or world.get_entrance('Swamp Palace').connected_region.name != 'Swamp Palace (Entrance)':
        world.swamp_patch_required = True

    return '\n'.join(ret) + '\n\n'


def connect_simple(world, exitname, regionname):
    world.get_entrance(exitname).connect(world.get_region(regionname))


def connect_one_way(world, exitname, regionname):
    entrance = world.get_entrance(exitname)
    region = world.get_region(regionname)
    target = cave_codes.get(region.name, None)
    entrance.connect(region, target)
    return '%s => %s' % (entrance.name, region.name)


def connect_two_way(world, entrancename, exitname):
    entrance = world.get_entrance(entrancename)
    exit = world.get_entrance(exitname)
    entrance.connect(exit.parent_region, exit_ids[exit.name])
    exit.connect(entrance.parent_region)
    return '%s <=> %s' % (entrance.name, exit.name)


def scramble_holes(world):
    ret = []
    hole_entrances = [('Kakariko Well Cave', 'Kakariko Well Drop'),
                      ('Bat Cave Cave', 'Bat Cave Drop'),
                      ('North Fairy Cave', 'North Fairy Cave Drop'),
                      ('Thieves Forest Hideout Stump', 'Thieves Forest Hideout Drop'),
                      ('Lumberjack Tree Cave', 'Lumberjack Tree Tree'),
                      ('Sanctuary', 'Sanctuary Grave')]

    hole_targets = [('Kakariko Well Exit', 'Kakariko Well (top)'),
                    ('Bat Cave Exit', 'Bat Cave (right)'),
                    ('North Fairy Cave Exit', 'North Fairy Cave'),
                    ('Thieves Forest Hideout Exit', 'Thieves Forest Hideout (top)'),
                    ('Lumberjack Tree Exit', 'Lumberjack Tree (top)'),
                    ('Sanctuary Exit', 'Sewer Drop')]

    if world.mode == 'standard':
        # cannot move uncle cave
        ret.append(connect_two_way(world, 'Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Exit'))
        ret.append(connect_one_way(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance'))
    else:
        hole_entrances.append(('Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Drop'))
        hole_targets.append(('Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance'))

    random.shuffle(hole_targets)
    for entrance, drop in hole_entrances:
        exit, target = hole_targets.pop()
        ret.append(connect_two_way(world, entrance, exit))
        ret.append(connect_one_way(world, drop, target))

    return '\n'.join(ret)


def connect_random(world, exitlist, targetlist, two_way=False):
    targetlist = list(targetlist)
    random.shuffle(targetlist)

    ret = []

    for exit, target in zip(exitlist, targetlist):
        if two_way:
            ret.append(connect_two_way(world, exit, target))
        else:
            ret.append(connect_one_way(world, exit, target))

    return '\n'.join(ret)


def connect_mandatory_exits(world, entrances, caves, must_be_exits):
    """This works inplace"""
    ret = []
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

            ret.append(connect_two_way(world, entrance, cave[i]))
        ret.append(connect_two_way(world, exit, cave[-1]))

    return '\n'.join(ret)


def connect_caves(world, lw_entrances, dw_entrances, caves):
    """This works inplace"""
    ret = []
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
            ret.append(connect_two_way(world, target.pop(), exit))

    return '\n'.join(ret)


def connect_doors(world, doors, targets):
    """This works inplace"""
    ret = []
    random.shuffle(doors)
    random.shuffle(targets)
    while doors:
        door = doors.pop()
        target = targets.pop()
        ret.append(connect_one_way(world, door, target))

    return '\n'.join(ret)


def skull_woods_shuffle(world):
    ret = connect_random(world, ['Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole'],
                         ['Skull Woods First Section (Left)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Top)', 'Skull Woods Second Section'])
    return ret + '\n' + connect_random(world, ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)'],
                                       ['Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)'], True)


def simple_shuffle_dungeons(world):
    ret = []

    ret.append(skull_woods_shuffle(world))

    # shuffle up single entrance dungeons
    ret.append(connect_random(world, ['Eastern Palace', 'Tower of Hera', 'Thieves Town', 'Skull Woods Final Section', 'Palace of Darkness', 'Ice Palace', 'Misery Mire', 'Swamp Palace'],
                   ['Eastern Palace Exit', 'Tower of Hera Exit', 'Thieves Town Exit', 'Skull Woods Final Section Exit', 'Dark Palace Exit', 'Ice Palace Exit', 'Misery Mire Exit', 'Swamp Palace Exit'], True))

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
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)'))
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Hyrule Castle Exit (East)'))
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Hyrule Castle Exit (West)'))
        ret.append(connect_two_way(world, 'Aghanims Tower', 'Aghanims Tower Exit'))
    elif hc_target == 'Desert':
        ret.append(connect_two_way(world, 'Desert Palace Entrance (South)', 'Hyrule Castle Exit (South)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (East)', 'Hyrule Castle Exit (East)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (West)', 'Hyrule Castle Exit (West)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (North)', 'Aghanims Tower Exit'))
    elif hc_target == 'Turtle Rock':
        ret.append(connect_two_way(world, 'Turtle Rock', 'Hyrule Castle Exit (South)'))
        ret.append(connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Hyrule Castle Exit (East)'))
        ret.append(connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Hyrule Castle Exit (West)'))
        ret.append(connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Aghanims Tower Exit'))
        world.aghanim_fix_required = True  # need this for now

    if dp_target == 'Hyrule Castle':
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Desert Palace Exit (South)'))
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Desert Palace Exit (East)'))
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Desert Palace Exit (West)'))
        ret.append(connect_two_way(world, 'Aghanims Tower', 'Desert Palace Exit (North)'))
    elif dp_target == 'Desert':
        ret.append(connect_two_way(world, 'Desert Palace Entrance (South)', 'Desert Palace Exit (South)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (East)', 'Desert Palace Exit (East)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (West)', 'Desert Palace Exit (West)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (North)', 'Desert Palace Exit (North)'))
    elif dp_target == 'Turtle Rock':
        ret.append(connect_two_way(world, 'Turtle Rock', 'Desert Palace Exit (South)'))
        ret.append(connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Desert Palace Exit (East)'))
        ret.append(connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Desert Palace Exit (West)'))
        ret.append(connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Desert Palace Exit (North)'))

    if tr_target == 'Hyrule Castle':
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Turtle Rock Exit (Front)'))
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Turtle Rock Ledge Exit (East)'))
        ret.append(connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Turtle Rock Ledge Exit (West)'))
        ret.append(connect_two_way(world, 'Aghanims Tower', 'Turtle Rock Isolated Ledge Exit'))
    elif tr_target == 'Desert':
        ret.append(connect_two_way(world, 'Desert Palace Entrance (South)', 'Turtle Rock Exit (Front)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (North)', 'Turtle Rock Ledge Exit (East)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (West)', 'Turtle Rock Ledge Exit (West)'))
        ret.append(connect_two_way(world, 'Desert Palace Entrance (East)', 'Turtle Rock Isolated Ledge Exit'))
    elif tr_target == 'Turtle Rock':
        ret.append(connect_two_way(world, 'Turtle Rock', 'Turtle Rock Exit (Front)'))
        ret.append(connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Turtle Rock Isolated Ledge Exit'))
        ret.append(connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Turtle Rock Ledge Exit (West)'))
        ret.append(connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Turtle Rock Ledge Exit (East)'))

    return '\n'.join(ret)


LW_Dungeon_Entrances = ['Desert Palace Entrance (South)',
                        'Desert Palace Entrance (West)',
                        'Desert Palace Entrance (North)',
                        'Eastern Palace',
                        'Tower of Hera',
                        'Hyrule Castle Entrance (West)',
                        'Hyrule Castle Entrance (East)',
                        'Aghanims Tower']

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

LW_Dungeon_Exits = ['Aghanims Tower Exit']

Dungeon_Exits = [('Desert Palace Exit (South)', 'Desert Palace Exit (West)', 'Desert Palace Exit (East)'),
                 'Desert Palace Exit (North)',
                 'Eastern Palace Exit',
                 'Tower of Hera Exit',
                 'Thieves Town Exit',
                 'Skull Woods Final Section Exit',
                 'Ice Palace Exit',
                 'Misery Mire Exit',
                 'Dark Palace Exit',
                 'Swamp Palace Exit',
                 ('Turtle Rock Exit (Front)', 'Turtle Rock Ledge Exit (East)', 'Turtle Rock Ledge Exit (West)', 'Turtle Rock Isolated Ledge Exit')]

DW_Entrances_Must_Exit = ['Bumper Cave (Top)', 'Hookshot Cave Back Entrance']

Old_Man_Entrances = ['Old Man Cave (East)',
                     'Old Man House (Top)',
                     'Death Mountain Return Cave (East)',
                     'Spectacle Rock Cave',
                     'Spectacle Rock Cave Peak',
                     'Spectacle Rock Cave (Bottom)']

Cave_Exits = [('Elder House Exit (East)', 'Elder House Exit (West)'),
              ('Two Brothers House Exit (East)', 'Two Brothers House Exit (West)'),
              ('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave Exit (East)'),
              ('Death Mountain Fairy Drop Cave Exit (Bottom)', 'Death Mountain Fairy Drop Cave Exit (Top)'),
              ('Spiral Cave Exit (Top)', 'Spiral Cave Exit'),
              ('Bumper Cave Exit (Top)', 'Bumper Cave Exit (Bottom)'),
              ('Dark Death Mountain Climb Exit (Bottom)', 'Dark Death Mountain Climb Exit (Top)'),
              ('Hookshot Cave Exit (South)', 'Hookshot Cave Exit (North)')]

Cave_Three_Exits = [('Spectacle Rock Cave Exit (Peak)', 'Spectacle Rock Cave Exit (Top)', 'Spectacle Rock Cave Exit'),
                    ('Death Mountain Climb Exit (Top)', 'Death Mountain Climb Exit (Middle)', 'Death Mountain Climb Exit (Bottom)')]

LW_Entrances = ['Elder House (East)',
                'Elder House (West)',
                'Two Brothers House (East)',
                'Two Brothers House (West)',
                'Old Man Cave (West)',
                'Old Man House (Bottom)',
                'Death Mountain Return Cave (West)',
                'Death Mountain Climb (Bottom)',
                'Death Mountain Climb (Middle)',
                'Death Mountain Climb (Top)',
                'Death Mountain Fairy Drop Cave (Bottom)',
                'Death Mountain Fairy Drop Cave (Top)',
                'Spiral Cave',
                'Spiral Cave (Bottom)']

DW_Entrances = ['Bumper Cave (Bottom)',
                'Dark Death Mountain Climb (Top)',
                'Dark Death Mountain Climb (Bottom)',
                'Hookshot Cave']

Blacksmith_Single_Cave_Doors = ['Thiefs Hut',
                                'Bonk Fairy (Light)',
                                'Lake Hylia Fairy',
                                'Swamp Fairy',
                                'Desert Fairy',
                                'Kings Grave',
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
                                'Cave South of Haunted Grove',
                                'Graveyard Cave',
                                'Desert Cave',
                                'Lake Hylia Cave',
                                'Long Fairy Cave',
                                'Good Bee Cave',
                                '20 Rupee Cave',
                                '50 Rupee Cave',
                                'Ice Cave',
                                'Bonk Rock Cave',
                                'Library',
                                'Witch Hut',
                                'Hookshot Fairy',
                                'Waterfall of Wishing',
                                'Capacity Upgrade',
                                'Dam']

Bomb_Shop_Single_Cave_Doors = ['East Dark World Hint',
                               'Palace of Darkness Hint',
                               'Dark Lake Hylia Fairy',
                               'Dark Lake Hylia Ledge Fairy',
                               'Dark Lake Hylia Ledge Spike Cave',
                               'Dark Lake Hylia Ledge Hint',
                               'Dark Swamp Cave',
                               'Bonk Fairy (Dark)',
                               'Doorless Hut',
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
                               'Dark Desert Cave',
                               'Dark Desert Hint',
                               'Dark Desert Fairy',
                               'Spike Cave',
                               'Cave Shop (Dark Death Mountain)',
                               'Dark Death Mountain Fairy',
                               'Mimic Cave Mirror Spot',
                               'Big Bomb Shop',
                               'Dark Lake Hylia Shop',
                               'Lumberjack House',
                               'Lake Hylia Fortune Teller',
                               'Kakariko Gamble Game']

Single_Cave_Doors = ['Pyramid Fairy']

Single_Cave_Targets = ['Thiefs Hut',
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
                       'Cave South of Haunted Grove',
                       'Graveyard Cave',
                       'Desert Cave',
                       'Lake Hylia Cave',
                       'Long Fairy Cave',
                       'Good Bee Cave',
                       '20 Rupee Cave',
                       '50 Rupee Cave',
                       'Ice Cave',
                       'Bonk Rock Cave',
                       'Library',
                       'Witch Hut',
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
                       'Dark Swamp Cave',
                       'Bonk Fairy',
                       'Doorless Hut',
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
                       'Dark Desert Cave',
                       'Dark Desert Hint',
                       'Healer Fairy',
                       'Spike Cave',
                       'Cave Shop',
                       'Healer Fairy',
                       'Mimic Cave',
                       'Dark World Shop',
                       'Lumberjack House',
                       'Fortune Teller (Light)',
                       'Kakariko Gamble Game']

# these are connections that cannot be shuffled and always exist. They link together separate parts of the world we need to divide into regions
mandatory_connections = [('Links House', 'Links House'),  # unshuffled. For now
                         ('Links House Exit', 'Light World'),

                         ('Zoras River', 'Zoras River'),
                         ('Kakariko Well (top to bottom)', 'Kakariko Well (bottom)'),
                         ('Master Sword Meadow', 'Master Sword Meadow'),
                         ('Hobo Bridge', 'Hobo Bridge'),
                         ('Desert Palace East Wing', 'Desert Palace East'),
                         ('Bat Cave Drop Ledge', 'Bat Cave Drop Ledge'),
                         ('Bat Cave Door', 'Bat Cave (left)'),
                         ('Thieves Forest Hideout (top to bottom)', 'Thieves Forest Hideout (bottom)'),
                         ('Lumberjack Tree (top to bottom)', 'Lumberjack Tree (bottom)'),
                         ('Desert Palace Stairs', 'Desert Palace Stairs'),
                         ('Desert Palace Stairs Drop', 'Light World'),
                         ('Desert Palace Entrance (North) Rocks', 'Desert Palace Entrance (North) Spot'),
                         ('Desert Ledge Return Rocks', 'Desert Ledge'),
                         ('Throne Room', 'Sewers (Dark)'),
                         ('Sewers Door', 'Sewers'),
                         ('Sanctuary Push Door', 'Sanctuary'),
                         ('Sewer Drop', 'Sewers'),
                         ('Sewers Back Door', 'Sewers (Dark)'),
                         ('Aghanim 1', 'Aghanim 1'),
                         ('Flute Spot 1', 'Death Mountain'),
                         ('Spectacle Rock Cave Drop', 'Spectacle Rock Cave (Bottom)'),
                         ('Spectacle Rock Cave Peak Drop', 'Spectacle Rock Cave (Bottom)'),
                         ('Spectacle Rock Cave (Bottom)', 'Spectacle Rock Cave (Bottom)'),
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
                         ('Death Mountain Climb Push Block Reverse', 'Death Mountain Climb Cave Chest Area'),
                         ('Death Mountain Climb Push Block', 'Death Mountain Climb Cave Front'),
                         ('Death Mountain Climb Bomb Jump', 'Death Mountain Climb Cave'),
                         ('Death Mountain Climb Drop', 'Death Mountain Climb Cave Chest Area'),
                         ('Death Mountain Fairy Drop Area Rocks', 'Death Mountain Fairy Drop Area'),
                         ('Death Mountain Fairy Drop Area Mirror Spot', 'Death Mountain Fairy Drop Area'),
                         ('Death Mountain Fairy Drop Area Drop', 'East Death Mountain (Bottom)'),
                         ('Death Mountain Fairy Drop Ledge Drop', 'Death Mountain Fairy Drop Area'),
                         ('Death Mountain Fairy Drop Ledge', 'Death Mountain Fairy Drop Ledge'),
                         ('Spectacle Rock Mirror Spot', 'Spectacle Rock'),
                         ('Dark Death Mountain Drop (East)', 'Dark Death Mountain (East Bottom)'),
                         ('Dark Death Mountain Drop (West)', 'Dark Death Mountain (West Bottom)'),
                         ('East Death Mountain (Top) Mirror Spot', 'East Death Mountain (Top)'),
                         ('Turtle Rock Teleporter', 'Turtle Rock (Top)'),
                         ('Turtle Rock Drop', 'Dark Death Mountain (Top)'),
                         ('Floating Island Drop', 'Dark Death Mountain (Top)'),
                         ('East Death Mountain Teleporter', 'Dark Death Mountain (East Bottom)'),
                         ('Isolated Ledge Mirror Spot', 'Death Mountain Fairy Drop Ledge'),
                         ('Spiral Cave Mirror Spot', 'Spiral Cave Ledge'),

                         ('Swamp Palace Moat', 'Swamp Palace (First Room)'),
                         ('Swamp Palace Small Key Door', 'Swamp Palace (Starting Area)'),
                         ('Swamp Palace (Center)', 'Swamp Palace (Center)'),
                         ('Swamp Palace (North)', 'Swamp Palace (North)'),
                         ('Thieves Town Big Key Door', 'Thieves Town (Deep)'),
                         ('Skull Woods Torch Room', 'Skull Woods Final Section (Mothula)'),
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
                         ('Turtle Rock Big Key Door', 'Turtle Rock (Roller Switch Room)'),
                         ('Turtle Rock Dark Room Staircase', 'Turtle Rock (Dark Room)'),
                         ('Turtle Rock (Dark Room) (North)', 'Turtle Rock (Roller Switch Room)'),
                         ('Turtle Rock (Dark Room) (South)', 'Turtle Rock (Eye Bridge)'),
                         ('Turtle Rock Dark Room (South)', 'Turtle Rock (Dark Room)'),
                         ('Turtle Rock (Trinexx)', 'Turtle Rock (Trinexx)'),
                         ('Dark Palace Bridge Room', 'Dark Palace (Center)'),
                         ('Dark Palace Bonk Wall', 'Dark Palace (Bonk Section)'),
                         ('Dark Palace Big Key Chest Staircase', 'Dark Palace (Big Key Chest)'),
                         ('Dark Palace (North)', 'Dark Palace (North)'),
                         ('Dark Palace Big Key Door', 'Dark Palace (Final Section)'),
                         ('Dark Palace Hammer Peg Drop', 'Dark Palace (Center)'),
                         ('Dark Palace Spike Statue Room Door', 'Dark Palace (Spike Statue Room)'),
                         ('Dark Palace Maze Door', 'Dark Palace (Maze)'),
                         ('Ganons Tower', 'Ganons Tower (Entrance)'),  # not shuffled, for now
                         ('Ganons Tower Exit', 'Dark Death Mountain (Top)'),
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
                         ('Ganons Tower Moldorm Gap', 'Aghanim 2'),
                         ('Pyramid Hole', 'Pyramid')  # not shuffled, for now
                         ]

# non-shuffled entrance links
default_connections = [('Waterfall of Wishing', 'Waterfall of Wishing'),
                       ("Thiefs Hut", "Thiefs Hut"),
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
                       ('Thieves Forest Hideout Drop', 'Thieves Forest Hideout (top)'),
                       ('Thieves Forest Hideout Stump', 'Thieves Forest Hideout (bottom)'),
                       ('Thieves Forest Hideout Exit', 'Light World'),
                       ('Lumberjack Tree Tree', 'Lumberjack Tree (top)'),
                       ('Lumberjack Tree Cave', 'Lumberjack Tree (bottom)'),
                       ('Lumberjack Tree Exit', 'Light World'),
                       ('Cave South of Haunted Grove', 'Cave South of Haunted Grove'),
                       ('Graveyard Cave', 'Graveyard Cave'),
                       ('Desert Cave', 'Desert Cave'),
                       ('Lake Hylia Cave', 'Lake Hylia Cave'),
                       ('Long Fairy Cave', 'Long Fairy Cave'),  # near East Light World Teleporter
                       ('Good Bee Cave', 'Good Bee Cave'),
                       ('20 Rupee Cave', '20 Rupee Cave'),
                       ('50 Rupee Cave', '50 Rupee Cave'),
                       ('Ice Cave', 'Ice Cave'),
                       ('Bonk Rock Cave', 'Bonk Rock Cave'),
                       ('Library', 'Library'),
                       ('Kakariko Gamble Game', 'Kakariko Gamble Game'),
                       ('Witch Hut', 'Witch Hut'),
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
                       ('Spectacle Rock Cave', 'Spectacle Rock Cave (Top)'),
                       ('Spectacle Rock Cave Exit', 'Death Mountain'),
                       ('Spectacle Rock Cave Exit (Top)', 'Death Mountain'),
                       ('Spectacle Rock Cave Exit (Peak)', 'Death Mountain'),
                       ('Death Mountain Climb (Bottom)', 'Death Mountain Climb Cave Front'),
                       ('Death Mountain Climb (Middle)', 'Death Mountain Climb Cave'),
                       ('Death Mountain Climb (Top)', 'Death Mountain Climb Cave'),
                       ('Death Mountain Climb Exit (Bottom)', 'East Death Mountain (Bottom)'),
                       ('Death Mountain Climb Exit (Middle)', 'East Death Mountain (Bottom)'),
                       ('Death Mountain Climb Exit (Top)', 'East Death Mountain (Top)'),
                       ('Hookshot Fairy', 'Hookshot Fairy'),
                       ('Death Mountain Fairy Drop Cave (Bottom)', 'Death Mountain Fairy Drop Cave'),
                       ('Death Mountain Fairy Drop Cave (Top)', 'Death Mountain Fairy Drop Cave'),
                       ('Death Mountain Fairy Drop Cave Exit (Bottom)', 'Death Mountain Fairy Drop Area'),
                       ('Death Mountain Fairy Drop Cave Exit (Top)', 'Death Mountain Fairy Drop Ledge'),
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
                       ('Dark Swamp Cave', 'Dark Swamp Cave'),
                       ('Bonk Fairy (Dark)', 'Bonk Fairy'),
                       ('Doorless Hut', 'Doorless Hut'),
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
                       ('Dark Desert Cave', 'Dark Desert Cave'),
                       ('Dark Desert Hint', 'Dark Desert Hint'),
                       ('Dark Desert Fairy', 'Healer Fairy'),
                       ('Spike Cave', 'Spike Cave'),
                       ('Hookshot Cave', 'Hookshot Cave'),
                       ('Dark Death Mountain Climb (Top)', 'Dark Death Mountain Climb'),
                       ('Cave Shop (Dark Death Mountain)', 'Cave Shop'),
                       ('Dark Death Mountain Fairy', 'Healer Fairy'),
                       ('Dark Death Mountain Climb (Bottom)', 'Dark Death Mountain Climb'),
                       ('Dark Death Mountain Climb Exit (Top)', 'Dark Death Mountain (Top)'),
                       ('Dark Death Mountain Climb Exit (Bottom)', 'Dark Death Mountain (East Bottom)'),
                       ('Hookshot Cave Exit (South)', 'Dark Death Mountain (Top)'),
                       ('Hookshot Cave Exit (North)', 'Death Mountain Floating Island'),
                       ('Hookshot Cave Back Entrance', 'Hookshot Cave'),
                       ('Mimic Cave Mirror Spot', 'Mimic Cave')
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
                               ('Aghanims Tower', 'Aghanims Tower'),
                               ('Aghanims Tower Exit', 'Hyrule Castle Ledge'),

                               ('Thieves Town', 'Thieves Town (Entrance)'),
                               ('Thieves Town Exit', 'West Dark World'),
                               ('Skull Woods First Section Hole (East)', 'Skull Woods First Section (Right)'),
                               ('Skull Woods First Section Hole (West)', 'Skull Woods First Section (Left)'),
                               ('Skull Woods First Section Hole (North)', 'Skull Woods First Section (Top)'),
                               ('Skull Woods First Section (Right)', 'Skull Woods First Section'),   # exist only for unique hole reference points
                               ('Skull Woods First Section (Left)', 'Skull Woods First Section'),
                               ('Skull Woods First Section (Top)', 'Skull Woods First Section'),
                               ('Skull Woods First Section Door', 'Skull Woods First Section'),
                               ('Skull Woods First Section Exit', 'Skull Woods Forest'),
                               ('Skull Woods Second Section Hole', 'Skull Woods Second Section'),
                               ('Skull Woods Second Section Door (East)', 'Skull Woods Second Section'),
                               ('Skull Woods Second Section Door (West)', 'Skull Woods Second Section'),
                               ('Skull Woods Second Section Exit (East)', 'Skull Woods Forest'),
                               ('Skull Woods Second Section Exit (West)', 'Skull Woods Forest'),
                               ('Skull Woods Final Section', 'Skull Woods Final Section (Entrance)'),
                               ('Skull Woods Final Section Exit', 'Skull Woods Forest'),
                               ('Ice Palace', 'Ice Palace (Entrance)'),
                               ('Ice Palace Exit', 'Light World'),  # this is kind of wrong, but completely unimportantly so
                               ('Misery Mire', 'Misery Mire (Entrance)'),
                               ('Misery Mire Exit', 'Dark Desert'),
                               ('Palace of Darkness', 'Dark Palace (Entrance)'),
                               ('Dark Palace Exit', 'East Dark World'),
                               ('Swamp Palace', 'Swamp Palace (Entrance)'),  # requires additional patch for flooding moat if moved
                               ('Swamp Palace Exit', 'South Dark World'),

                               ('Turtle Rock', 'Turtle Rock (Entrance)'),
                               ('Turtle Rock Exit (Front)', 'Dark Death Mountain (Top)'),
                               ('Turtle Rock Ledge Exit (West)', 'Dark Death Mountain Ledge'),
                               ('Turtle Rock Ledge Exit (East)', 'Dark Death Mountain Ledge'),
                               ('Dark Death Mountain Ledge (West)', 'Turtle Rock (Second Section)'),
                               ('Dark Death Mountain Ledge (East)', 'Turtle Rock (Big Chest)'),
                               ('Turtle Rock Isolated Ledge Exit', 'Dark Death Mountain Isolated Ledge'),
                               ('Turtle Rock Isolated Ledge Entrance', 'Turtle Rock (Eye Bridge)')

                               ]


# ToDo somehow merge this with creation of the locations
door_addresses = {'Desert Palace Entrance (South)': (0xDBB7B, 0x15B02),
                  'Desert Palace Entrance (West)': (0xDBB7D, 0x15B06),
                  'Desert Palace Entrance (North)': (0xDBB7E, 0x15B08),
                  'Desert Palace Entrance (East)': (0xDBB7C, 0x15B04),
                  'Eastern Palace': (0xDBB7A, 0x15B00),
                  'Tower of Hera': (0xDBBA5, 0x15B48),
                  'Hyrule Castle Entrance (South)': (0xDBB76, 0x15AF4),
                  'Hyrule Castle Entrance (West)': (0xDBB75, 0x15AF2),
                  'Hyrule Castle Entrance (East)': (0xDBB77, 0x15AF6),
                  'Aghanims Tower': (0xDBB96, 0x15B38),
                  'Thieves Town': (0xDBBA6, 0x15B58),
                  'Skull Woods First Section Door': (0xDBB9C, 0x15B44),
                  'Skull Woods Second Section Door (East)': (0xDBB9B, 0x15B42),
                  'Skull Woods Second Section Door (West)': (0xDBB9A, 0x15B40),
                  'Skull Woods Final Section': (0xDBB9D, 0x15B46),
                  'Ice Palace': (0xDBB9F, 0x15B4A),
                  'Misery Mire': (0xDBB99, 0x15B3E),
                  'Palace of Darkness': (0xDBB98, 0x15B3C),
                  'Swamp Palace': (0xDBB97, 0x15B3A),
                  'Turtle Rock': (0xDBBA7, 0x15B56),
                  'Dark Death Mountain Ledge (West)': (0xDBB87, 0x15B1A),
                  'Dark Death Mountain Ledge (East)': (0xDBB8B, 0x15B22),
                  'Turtle Rock Isolated Ledge Entrance': (0xDBB8A, 0x15B20),
                  'Hyrule Castle Secret Entrance Stairs': (0xDBBA4, 0x15B54),
                  'Kakariko Well Cave': (0xDBBAB, 0x15B62),
                  'Bat Cave Cave': (0xDBB83, 0x15B12),
                  'Elder House (East)': (0xDBB80, 0x15B0C),
                  'Elder House (West)': (0xDBB7F, 0x15B0A),
                  'North Fairy Cave': (0xDBBAA, 0x15B60),
                  'Thieves Forest Hideout Stump': (0xDBB9E, 0x15B5A),
                  'Lumberjack Tree Cave': (0xDBB84, 0x15B14),
                  'Two Brothers House (East)': (0xDBB82, 0x15B10),
                  'Two Brothers House (West)': (0xDBB81, 0x15B0E),
                  'Sanctuary': (0xDBB74, 0x15AF0),
                  'Old Man Cave (West)': (0xDBB78, 0x15AFC),
                  'Old Man Cave (East)': (0xDBB79, 0x15AFE),
                  'Old Man House (Bottom)': (0xDBBA2, 0x15B50),
                  'Old Man House (Top)': (0xDBBA3, 0x15B52),
                  'Death Mountain Return Cave (East)': (0xDBBA1, 0x15B4E),
                  'Death Mountain Return Cave (West)': (0xDBBA0, 0x15B4C),
                  'Spectacle Rock Cave Peak': (0xDBB95, 0x15B36),
                  'Spectacle Rock Cave': (0xDBB94, 0x15B34),
                  'Spectacle Rock Cave (Bottom)': (0xDBB93, 0x15B32),
                  'Death Mountain Climb (Bottom)': (0xDBB90, 0x15B2C),
                  'Death Mountain Climb (Middle)': (0xDBB91, 0x15B2E),
                  'Death Mountain Climb (Top)': (0xDBB92, 0x15B30),
                  'Death Mountain Fairy Drop Cave (Bottom)': (0xDBB8C, 0x15B24),
                  'Death Mountain Fairy Drop Cave (Top)': (0xDBB8D, 0x15B26),
                  'Spiral Cave': (0xDBB8F, 0x15B2A),
                  'Spiral Cave (Bottom)': (0xDBB8E, 0x15B28),
                  'Bumper Cave (Bottom)': (0xDBB88, 0x15B1C),
                  'Bumper Cave (Top)': (0xDBB89, 0x15B1E),
                  'Dark Death Mountain Climb (Top)': (0xDBB86, 0x15B18),
                  'Dark Death Mountain Climb (Bottom)': (0xDBB85, 0x15B16),
                  'Hookshot Cave': (0xDBBAC, 0x15B64),
                  'Hookshot Cave Back Entrance': (0xDBBAD, 0x15B66)}

exit_ids = {'Desert Palace Exit (South)': (0x09, 0x84),
            'Desert Palace Exit (West)': (0x0B, 0x83),
            'Desert Palace Exit (East)': (0x0A, 0x85),
            'Desert Palace Exit (North)': (0x0C, 0x63),
            'Eastern Palace Exit': (0x08, 0xC9),
            'Tower of Hera Exit': (0x33, 0x77),
            'Hyrule Castle Exit (South)': (0x04, 0x61),
            'Hyrule Castle Exit (West)': (0x03, 0x60),
            'Hyrule Castle Exit (East)': (0x05, 0x62),
            'Aghanims Tower Exit': (0x24, 0xE0),
            'Thieves Town Exit': (0x34, 0xDB),
            'Skull Woods First Section Exit': (0x2A, 0x58),
            'Skull Woods Second Section Exit (East)': (0x29, 0x57),
            'Skull Woods Second Section Exit (West)': (0x28, 0x56),
            'Skull Woods Final Section Exit': (0x2B, 0x59),
            'Ice Palace Exit': (0x2D, 0x0E),
            'Misery Mire Exit': (0x27, 0x98),
            'Dark Palace Exit': (0x26, 0x4A),
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
            'Thieves Forest Hideout Exit': (0x2C, 0xE1),
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
            'Death Mountain Climb Exit (Bottom)': (0x1E, 0xFF),
            'Death Mountain Climb Exit (Middle)': (0x1F, 0xEF),
            'Death Mountain Climb Exit (Top)': (0x20, 0xDF),
            'Death Mountain Fairy Drop Cave Exit (Bottom)': (0x1A, 0xFD),
            'Death Mountain Fairy Drop Cave Exit (Top)': (0x1B, 0xED),
            'Spiral Cave Exit': (0x1C, 0xFE),
            'Spiral Cave Exit (Top)': (0x1D, 0xEE),
            'Bumper Cave Exit (Top)': (0x17, 0xEB),
            'Bumper Cave Exit (Bottom)': (0x16, 0xFB),
            'Dark Death Mountain Climb Exit (Top)': (0x13, 0xF8),
            'Dark Death Mountain Climb Exit (Bottom)': (0x14, 0xE8),
            'Hookshot Cave Exit (South)': (0x3A, 0x3C),
            'Hookshot Cave Exit (North)': (0x3B, 0x2C)}

single_doors = {'Skull Woods First Section Hole (East)': (0xDB84D, 0xDB84E),
                'Skull Woods First Section Hole (West)': (0xDB84F, 0xDB850),
                'Skull Woods First Section Hole (North)': 0xDB84C,
                'Skull Woods Second Section Hole': (0xDB851, 0xDB852),
                'Waterfall of Wishing': 0xDBBCE,
                'Dam': 0xDBBC0,
                'Thiefs Hut': 0xDBBD3,
                'Hyrule Castle Secret Entrance Drop': 0xDB858,
                'Bonk Fairy (Light)': 0xDBBE9,
                'Lake Hylia Fairy': 0xDBBD0,
                'Swamp Fairy': 0xDBBDE,
                'Desert Fairy': 0xDBBE4,
                'Kings Grave': 0xDBBCD,
                'Tavern North': 0xDBBB5,   # do not use, buggy
                'Chicken House': 0xDBBBD,
                'Aginahs Cave': 0xDBBE3,
                'Sahasrahlas Hut': 0xDBBB7,
                'Cave Shop (Lake Hylia)': 0xDBBCA,
                'Capacity Upgrade': 0xDBBCF,
                'Kakariko Well Drop': (0xDB85C, 0xDB85D),
                'Blacksmiths Hut': 0xDBBD6,
                'Bat Cave Drop': (0xDB859, 0xDB85A),
                'Sick Kids House': 0xDBBB2,
                'North Fairy Cave Drop': 0xDB857,
                'Lost Woods Gamble': 0xDBBAE,
                'Fortune Teller (Light)': 0xDBBD7,
                'Snitch Lady (East)': 0xDBBB0,
                'Snitch Lady (West)': 0xDBBB1,
                'Bush Covered House': 0xDBBB6,
                'Tavern (Front)': 0xDBBB4,
                'Light World Bomb Hut': 0xDBBBC,
                'Kakariko Shop': 0xDBBB8,
                'Thieves Forest Hideout Drop': 0xDB853,
                'Lumberjack Tree Tree': 0xDB85B,
                'Cave South of Haunted Grove': 0xDBBC3,
                'Graveyard Cave': 0xDBBC4,
                'Desert Cave': 0xDBBF0,
                'Lake Hylia Cave': 0xDBBEF,
                'Long Fairy Cave': 0xDBBC7,
                'Good Bee Cave': 0xDBBDD,
                '20 Rupee Cave': 0xDBBED,
                '50 Rupee Cave': 0xDBBEB,
                'Ice Cave': 0xDBBF2,
                'Bonk Rock Cave': 0xDBBEC,
                'Library': 0xDBBBB,
                'Witch Hut': 0xDBBBE,
                'Sanctuary Grave': 0xDB85E,
                'Hookshot Fairy': 0xDBBC2,
                'Pyramid Fairy': 0xDBBD5,
                'East Dark World Hint': 0xDBBDB,
                'Palace of Darkness Hint': 0xDBBDA,
                'Dark Lake Hylia Fairy': 0xDBBDF,
                'Dark Lake Hylia Ledge Fairy': 0xDBBF3,
                'Dark Lake Hylia Ledge Spike Cave': 0xDBBEE,
                'Dark Lake Hylia Ledge Hint': 0xDBBDC,
                'Dark Swamp Cave': 0xDBBAF,
                'Bonk Fairy (Dark)': 0xDBBEA,
                'Doorless Hut': 0xDBBBA,
                'C-Shaped House': 0xDBBC6,
                'Chest Game': 0xDBBB9,
                'Dark World Hammer Peg Cave': 0xDBBF1,
                'Red Shield Shop': 0xDBBE7,
                'Dark Sanctuary Hint': 0xDBBCC,
                'Fortune Teller (Dark)': 0xDBBD8,
                'Dark World Shop': 0xDBBD2,
                'Dark World Lumberjack Shop': 0xDBBC9,
                'Dark World Potion Shop': 0xDBBE1,
                'Archery Game': 0xDBBCB,
                'Dark Desert Cave': 0xDBBD1,
                'Dark Desert Hint': 0xDBBD4,
                'Dark Desert Fairy': 0xDBBC8,
                'Spike Cave': 0xDBBB3,
                'Cave Shop (Dark Death Mountain)': 0xDBBE0,
                'Dark Death Mountain Fairy': 0xDBBE2,
                'Mimic Cave Mirror Spot': 0xDBBC1,
                'Big Bomb Shop': 0xDBBC5,
                'Dark Lake Hylia Shop': 0xDBBE6,
                'Lumberjack House': 0xDBBE8,
                'Lake Hylia Fortune Teller': 0xDBBE5,
                'Kakariko Gamble Game': 0xDBBD9}


cave_codes = {'Waterfall of Wishing': 0x5C,
              'Dam': 0x4E,
              'Thiefs Hut': 0x61,
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
              'Cave South of Haunted Grove': 0x51,
              'Graveyard Cave': 0x52,
              'Desert Cave': 0x72,
              'Lake Hylia Cave': 0x6C,
              'Long Fairy Cave': 0x55,
              'Good Bee Cave': 0x56,
              '20 Rupee Cave': 0x6F,
              '50 Rupee Cave': 0x6D,
              'Ice Cave': 0x84,
              'Bonk Rock Cave': 0x6E,
              'Library': 0x49,
              'Kakariko Gamble Game': 0x67,
              'Witch Hut': 0x4C,
              'Hookshot Fairy': 0x50,
              'Pyramid Fairy': 0x63,
              'East Dark World Hint': 0x69,
              'Palace of Darkness Hint': 0x68,
              'Big Bomb Shop': 0x53,
              'Dark World Shop': 0x60,
              'Dark Lake Hylia Ledge Spike Cave': 0x70,
              'Dark Lake Hylia Ledge Hint': 0x6A,
              'Dark Swamp Cave': 0x3D,
              'Doorless Hut': 0x48,
              'C-Shaped House': 0x54,
              'Chest Game': 0x47,
              'Dark World Hammer Peg Cave': 0x83,
              'Red Shield Shop': 0x57,
              'Dark Sanctuary Hint': 0x5A,
              'Fortune Teller (Dark)': 0x66,
              'Archery Game': 0x59,
              'Dark Desert Cave': 0x5F,
              'Dark Desert Hint': 0x62,
              'Spike Cave': 0x41,
              'Mimic Cave': 0x4F,
              'Kakariko Well (top)': 0x80,
              'Hyrule Castle Secret Entrance': 0x7D,
              'Bat Cave (right)': 0x7E,
              'North Fairy Cave': 0x7C,
              'Thieves Forest Hideout (top)': 0x7A,
              'Lumberjack Tree (top)': 0x7F,
              'Sewer Drop': 0x81,
              'Skull Woods Second Section': 0x79,
              'Skull Woods First Section (Left)': 0x77,
              'Skull Woods First Section (Right)': 0x78,
              'Skull Woods First Section (Top)': 0x76}
