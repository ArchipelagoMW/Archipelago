from BaseClasses import Dungeon
from Bosses import BossFactory
from Fill import fill_restrictive
from Items import ItemFactory
from Regions import lookup_boss_drops


def create_dungeons(world, player):
    def make_dungeon(name, default_boss, dungeon_regions, big_key, small_keys, dungeon_items):
        dungeon = Dungeon(name, dungeon_regions, big_key, [] if world.keyshuffle[player] == "universal" else small_keys,
                          dungeon_items, player)
        dungeon.boss = BossFactory(default_boss, player) if default_boss else None
        for region in dungeon.regions:
            world.get_region(region, player).dungeon = dungeon
            dungeon.world = world
        return dungeon

    ES = make_dungeon('Hyrule Castle', None, ['Hyrule Castle', 'Sewers', 'Sewer Drop', 'Sewers (Dark)', 'Sanctuary'],
                      None, [ItemFactory('Small Key (Hyrule Castle)', player)],
                      [ItemFactory('Map (Hyrule Castle)', player)])
    EP = make_dungeon('Eastern Palace', 'Armos Knights', ['Eastern Palace'],
                      ItemFactory('Big Key (Eastern Palace)', player), [],
                      ItemFactory(['Map (Eastern Palace)', 'Compass (Eastern Palace)'], player))
    DP = make_dungeon('Desert Palace', 'Lanmolas', ['Desert Palace North', 'Desert Palace Main (Inner)', 'Desert Palace Main (Outer)', 'Desert Palace East'], ItemFactory('Big Key (Desert Palace)', player), [ItemFactory('Small Key (Desert Palace)', player)], ItemFactory(['Map (Desert Palace)', 'Compass (Desert Palace)'], player))
    ToH = make_dungeon('Tower of Hera', 'Moldorm', ['Tower of Hera (Bottom)', 'Tower of Hera (Basement)', 'Tower of Hera (Top)'], ItemFactory('Big Key (Tower of Hera)', player), [ItemFactory('Small Key (Tower of Hera)', player)], ItemFactory(['Map (Tower of Hera)', 'Compass (Tower of Hera)'], player))
    PoD = make_dungeon('Palace of Darkness', 'Helmasaur King', ['Palace of Darkness (Entrance)', 'Palace of Darkness (Center)', 'Palace of Darkness (Big Key Chest)', 'Palace of Darkness (Bonk Section)', 'Palace of Darkness (North)', 'Palace of Darkness (Maze)', 'Palace of Darkness (Harmless Hellway)', 'Palace of Darkness (Final Section)'], ItemFactory('Big Key (Palace of Darkness)', player), ItemFactory(['Small Key (Palace of Darkness)'] * 6, player), ItemFactory(['Map (Palace of Darkness)', 'Compass (Palace of Darkness)'], player))
    TT = make_dungeon('Thieves Town', 'Blind', ['Thieves Town (Entrance)', 'Thieves Town (Deep)', 'Blind Fight'], ItemFactory('Big Key (Thieves Town)', player), [ItemFactory('Small Key (Thieves Town)', player)], ItemFactory(['Map (Thieves Town)', 'Compass (Thieves Town)'], player))
    SW = make_dungeon('Skull Woods', 'Mothula', ['Skull Woods Final Section (Entrance)', 'Skull Woods First Section', 'Skull Woods Second Section', 'Skull Woods Second Section (Drop)', 'Skull Woods Final Section (Mothula)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)'], ItemFactory('Big Key (Skull Woods)', player), ItemFactory(['Small Key (Skull Woods)'] * 3, player), ItemFactory(['Map (Skull Woods)', 'Compass (Skull Woods)'], player))
    SP = make_dungeon('Swamp Palace', 'Arrghus', ['Swamp Palace (Entrance)', 'Swamp Palace (First Room)', 'Swamp Palace (Starting Area)', 'Swamp Palace (Center)', 'Swamp Palace (North)'], ItemFactory('Big Key (Swamp Palace)', player), [ItemFactory('Small Key (Swamp Palace)', player)], ItemFactory(['Map (Swamp Palace)', 'Compass (Swamp Palace)'], player))
    IP = make_dungeon('Ice Palace', 'Kholdstare', ['Ice Palace (Entrance)', 'Ice Palace (Main)', 'Ice Palace (East)', 'Ice Palace (East Top)', 'Ice Palace (Kholdstare)'], ItemFactory('Big Key (Ice Palace)', player), ItemFactory(['Small Key (Ice Palace)'] * 2, player), ItemFactory(['Map (Ice Palace)', 'Compass (Ice Palace)'], player))
    MM = make_dungeon('Misery Mire', 'Vitreous', ['Misery Mire (Entrance)', 'Misery Mire (Main)', 'Misery Mire (West)', 'Misery Mire (Final Area)', 'Misery Mire (Vitreous)'], ItemFactory('Big Key (Misery Mire)', player), ItemFactory(['Small Key (Misery Mire)'] * 3, player), ItemFactory(['Map (Misery Mire)', 'Compass (Misery Mire)'], player))
    TR = make_dungeon('Turtle Rock', 'Trinexx', ['Turtle Rock (Entrance)', 'Turtle Rock (First Section)', 'Turtle Rock (Chain Chomp Room)', 'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Turtle Rock (Crystaroller Room)', 'Turtle Rock (Dark Room)', 'Turtle Rock (Eye Bridge)', 'Turtle Rock (Trinexx)'], ItemFactory('Big Key (Turtle Rock)', player), ItemFactory(['Small Key (Turtle Rock)'] * 4, player), ItemFactory(['Map (Turtle Rock)', 'Compass (Turtle Rock)'], player))

    if world.mode[player] != 'inverted':
        AT = make_dungeon('Agahnims Tower', 'Agahnim', ['Agahnims Tower', 'Agahnim 1'], None, ItemFactory(['Small Key (Agahnims Tower)'] * 2, player), [])
        GT = make_dungeon('Ganons Tower', 'Agahnim2', ['Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)', 'Ganons Tower (Compass Room)', 'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)', 'Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)', 'Ganons Tower (Top)', 'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)', 'Agahnim 2'], ItemFactory('Big Key (Ganons Tower)', player), ItemFactory(['Small Key (Ganons Tower)'] * 4, player), ItemFactory(['Map (Ganons Tower)', 'Compass (Ganons Tower)'], player))
    else:
        AT = make_dungeon('Inverted Agahnims Tower', 'Agahnim', ['Inverted Agahnims Tower', 'Agahnim 1'], None, ItemFactory(['Small Key (Agahnims Tower)'] * 2, player), [])
        GT = make_dungeon('Inverted Ganons Tower', 'Agahnim2', ['Inverted Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)', 'Ganons Tower (Compass Room)', 'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)', 'Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)', 'Ganons Tower (Top)', 'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)', 'Agahnim 2'], ItemFactory('Big Key (Ganons Tower)', player), ItemFactory(['Small Key (Ganons Tower)'] * 4, player), ItemFactory(['Map (Ganons Tower)', 'Compass (Ganons Tower)'], player))

    GT.bosses['bottom'] = BossFactory('Armos Knights', player)
    GT.bosses['middle'] = BossFactory('Lanmolas', player)
    GT.bosses['top'] = BossFactory('Moldorm', player)

    world.dungeons += [ES, EP, DP, ToH, AT, PoD, TT, SW, SP, IP, MM, TR, GT]

def fill_dungeons(world):
    #All chests on the freebes list locked behind a key in room with no other exit
    freebes = ['Ganons Tower - Map Chest', 'Palace of Darkness - Harmless Hellway', 'Palace of Darkness - Big Key Chest', 'Turtle Rock - Big Key Chest']

    all_state_base = world.get_all_state()

    dungeons = [(list(dungeon.regions), dungeon.big_key, list(dungeon.small_keys), list(dungeon.dungeon_items)) for dungeon in world.dungeons]

    loopcnt = 0
    while dungeons:
        loopcnt += 1
        dungeon_regions, big_key, small_keys, dungeon_items = dungeons.pop(0)
        # this is what we need to fill
        dungeon_locations = [location for location in world.get_unfilled_locations() if location.parent_region.name in dungeon_regions]
        world.random.shuffle(dungeon_locations)

        all_state = all_state_base.copy()

        # first place big key
        if big_key is not None:
            bk_location = None
            for location in dungeon_locations:
                if location.item_rule(big_key):
                    bk_location = location
                    break

            if bk_location is None:
                raise RuntimeError('No suitable location for %s' % big_key)

            world.push_item(bk_location, big_key, False)
            bk_location.event = True
            bk_location.locked = True
            dungeon_locations.remove(bk_location)
            big_key = None

        # next place small keys
        while small_keys:
            small_key = small_keys.pop()
            all_state.sweep_for_events()
            sk_location = None
            for location in dungeon_locations:
                if location.name in freebes or (location.can_reach(all_state) and location.item_rule(small_key)):
                    sk_location = location
                    break

            if sk_location is None:
                # need to retry this later
                small_keys.append(small_key)
                dungeons.append((dungeon_regions, big_key, small_keys, dungeon_items))
                # infinite regression protection
                if loopcnt < (30 * world.players):
                    break
                else:
                    raise RuntimeError('No suitable location for %s' % small_key)

            world.push_item(sk_location, small_key, False)
            sk_location.event = True
            sk_location.locked = True
            dungeon_locations.remove(sk_location)

        if small_keys:
            # key placement not finished, loop again
            continue

        # next place dungeon items
        for dungeon_item in dungeon_items:
            di_location = dungeon_locations.pop()
            world.push_item(di_location, dungeon_item, False)


def get_dungeon_item_pool(world):
    return [item for dungeon in world.dungeons for item in dungeon.all_items]

def fill_dungeons_restrictive(world):
    """Places dungeon-native items into their dungeons, places nothing if everything is shuffled outside."""
    restricted_players = {player for player, restricted in world.restrict_dungeon_item_on_boss.items() if restricted}

    locations = [location for location in world.get_unfilled_dungeon_locations()
                 if not (location.player in restricted_players and location.name in lookup_boss_drops)] # filter boss

    world.random.shuffle(locations)
    all_state_base = world.get_all_state()

    # with shuffled dungeon items they are distributed as part of the normal item pool
    for item in world.get_items():
        if (item.smallkey and world.keyshuffle[item.player]) or (item.bigkey and world.bigkeyshuffle[item.player]):
            all_state_base.collect(item, True)
            item.advancement = True
        elif (item.map and world.mapshuffle[item.player]) or (item.compass and world.compassshuffle[item.player]):
            item.priority = True

    dungeon_items = [item for item in get_dungeon_item_pool(world) if (((item.smallkey and not world.keyshuffle[item.player])
                                                                       or (item.bigkey and not world.bigkeyshuffle[item.player])
                                                                       or (item.map and not world.mapshuffle[item.player])
                                                                       or (item.compass and not world.compassshuffle[item.player])
                                                                        ) and world.goal[item.player] != 'icerodhunt')]  #
    if dungeon_items:
        # sort in the order Big Key, Small Key, Other before placing dungeon items
        sort_order = {"BigKey": 3, "SmallKey": 2}
        dungeon_items.sort(key=lambda item: sort_order.get(item.type, 1))
        fill_restrictive(world, all_state_base, locations, dungeon_items, True, True)


dungeon_music_addresses = {'Eastern Palace - Prize': [0x1559A],
                           'Desert Palace - Prize': [0x1559B, 0x1559C, 0x1559D, 0x1559E],
                           'Tower of Hera - Prize': [0x155C5, 0x1107A, 0x10B8C],
                           'Palace of Darkness - Prize': [0x155B8],
                           'Swamp Palace - Prize': [0x155B7],
                           'Thieves\' Town - Prize': [0x155C6],
                           'Skull Woods - Prize': [0x155BA, 0x155BB, 0x155BC, 0x155BD, 0x15608, 0x15609, 0x1560A, 0x1560B],
                           'Ice Palace - Prize': [0x155BF],
                           'Misery Mire - Prize': [0x155B9],
                           'Turtle Rock - Prize': [0x155C7, 0x155A7, 0x155AA, 0x155AB]}
