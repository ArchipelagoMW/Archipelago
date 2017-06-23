from Items import ItemFactory
import random
from BaseClasses import CollectionState


def fill_dungeons(world):
    ES = (['Hyrule Castle'], None, [ItemFactory('Small Key (Escape)')], [ItemFactory('Map (Escape)')])
    EP = (['Eastern Palace'], ItemFactory('Big Key (Eastern Palace)'), [], ItemFactory(['Map (Eastern Palace)', 'Compass (Eastern Palace)']))
    DP = (['Desert Palace Main', 'Desert Palace East', 'Desert Palace North'], ItemFactory('Big Key (Desert Palace)'), [ItemFactory('Small Key (Desert Palace)')], ItemFactory(['Map (Desert Palace)', 'Compass (Desert Palace)']))
    ToH = (['Tower of Hera (Bottom)', 'Tower of Hera (Basement)', 'Tower of Hera (Top)'], ItemFactory('Big Key (Tower of Hera)'), [ItemFactory('Small Key (Tower of Hera)')], ItemFactory(['Map (Tower of Hera)', 'Compass (Tower of Hera)']))
    AT = (['Agahnims Tower', 'Agahnim 1'], None, ItemFactory(['Small Key (Agahnims Tower)'] * 2), [])
    PoD = (['Dark Palace (Entrance)', 'Dark Palace (Center)', 'Dark Palace (Big Key Chest)', 'Dark Palace (Bonk Section)', 'Dark Palace (North)', 'Dark Palace (Maze)', 'Dark Palace (Spike Statue Room)', 'Dark Palace (Final Section)'], ItemFactory('Big Key (Palace of Darkness)'), ItemFactory(['Small Key (Palace of Darkness)'] * 6), ItemFactory(['Map (Palace of Darkness)', 'Compass (Palace of Darkness)']))
    TT = (['Thieves Town (Entrance)', 'Thieves Town (Deep)', 'Blind Fight'], ItemFactory('Big Key (Thieves Town)'), [ItemFactory('Small Key (Thieves Town)')], ItemFactory(['Map (Thieves Town)', 'Compass (Thieves Town)']))
    SW = (['Skull Woods First Section', 'Skull Woods Second Section', 'Skull Woods Final Section (Entrance)', 'Skull Woods Final Section (Mothula)'], ItemFactory('Big Key (Skull Woods)'), ItemFactory(['Small Key (Skull Woods)'] * 2), ItemFactory(['Map (Skull Woods)', 'Compass (Skull Woods)']))
    SP = (['Swamp Palace (Entrance)', 'Swamp Palace (First Room)', 'Swamp Palace (Starting Area)', 'Swamp Palace (Center)', 'Swamp Palace (North)'], ItemFactory('Big Key (Swamp Palace)'), [ItemFactory('Small Key (Swamp Palace)')], ItemFactory(['Map (Swamp Palace)', 'Compass (Swamp Palace)']))
    IP = (['Ice Palace (Entrance)', 'Ice Palace (Main)', 'Ice Palace (East)', 'Ice Palace (East Top)', 'Ice Palace (Kholdstare)'], ItemFactory('Big Key (Ice Palace)'), ItemFactory(['Small Key (Ice Palace)'] * 2), ItemFactory(['Map (Ice Palace)', 'Compass (Ice Palace)']))
    MM = (['Misery Mire (Entrance)', 'Misery Mire (Main)', 'Misery Mire (West)', 'Misery Mire (Final Area)', 'Misery Mire (Vitreous)'], ItemFactory('Big Key (Misery Mire)'), ItemFactory(['Small Key (Misery Mire)'] * 3), ItemFactory(['Map (Misery Mire)', 'Compass (Misery Mire)']))
    TR = (['Turtle Rock (Entrance)', 'Turtle Rock (First Section)', 'Turtle Rock (Chain Chomp Room)', 'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Turtle Rock (Roller Switch Room)', 'Turtle Rock (Dark Room)', 'Turtle Rock (Eye Bridge)', 'Turtle Rock (Trinexx)'], ItemFactory('Big Key (Turtle Rock)'), ItemFactory(['Small Key (Turtle Rock)'] * 4), ItemFactory(['Map (Turtle Rock)', 'Compass (Turtle Rock)']))
    GT = (['Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)', 'Ganons Tower (Compass Room)', 'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)', 'Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)', 'Ganons Tower (Top)', 'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)', 'Agahnim 2'], ItemFactory('Big Key (Ganons Tower)'), ItemFactory(['Small Key (Ganons Tower)'] * 4), ItemFactory(['Map (Ganons Tower)', 'Compass (Ganons Tower)']))

    freebes = ['[dungeon-A2-1F] Ganons Tower - Map Room', '[dungeon-D1-1F] Dark Palace - Spike Statue Room', '[dungeon-D1-1F] Dark Palace - Big Key Room', '[dungeon-D7-B1] Turtle Rock - Big Key Room']

    all_state_base = world.get_all_state()

    # this key is in a fixed location (for now)
    mandatory_sw_key_location = random.choice(['[dungeon-D3-B1] Skull Woods - South of Big Chest'] if world.shuffle != 'vanilla' else ['[dungeon-D3-B1] Skull Woods - South of Big Chest', '[dungeon-D3-B1] Skull Woods - Push Statue Room', '[dungeon-D3-B1] Skull Woods - Compass Room'])

    world.push_item(world.get_location(mandatory_sw_key_location), ItemFactory('Small Key (Skull Woods)'), False)
    world.get_location(mandatory_sw_key_location).event = True

    for dungeon_regions, big_key, small_keys, dungeon_items in [TR, ES, EP, DP, ToH, AT, PoD, TT, SW, SP, IP, MM, GT]:
        # this is what we need to fill
        dungeon_locations = [location for location in world.get_unfilled_locations() if location.parent_region.name in dungeon_regions]
        random.shuffle(dungeon_locations)

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
            dungeon_locations.remove(bk_location)
            all_state._clear_cache()

        # next place small keys
        for small_key in small_keys:
            all_state.sweep_for_events()
            sk_location = None
            for location in dungeon_locations:
                if location.name in freebes or location.can_reach(all_state):
                    sk_location = location
                    break

            if sk_location is None:
                raise RuntimeError('No suitable location for %s' % small_key)

            world.push_item(sk_location, small_key, False)
            sk_location.event = True
            dungeon_locations.remove(sk_location)
            all_state._clear_cache()

        # next place dungeon items
        if world.place_dungeon_items:
            for dungeon_item in dungeon_items:
                di_location = dungeon_locations.pop()
                world.push_item(di_location, dungeon_item, False)

    world.state._clear_cache()

    return ''


dungeon_music_addresses = {'Armos - Pendant': [0x1559A],
                           'Lanmolas - Pendant': [0x1559B, 0x1559C, 0x1559D, 0x1559E],
                           'Moldorm - Pendant': [0x155C5, 0x1107A, 0x10B8C],
                           'Helmasaur - Crystal': [0x155B8],
                           'Arrghus - Crystal': [0x155B7],
                           'Blind - Crystal': [0x155C6],
                           'Mothula - Crystal': [0x155BA, 0x155BB, 0x155BC, 0x155BD, 0x15608, 0x15609, 0x1560A, 0x1560B],
                           'Kholdstare - Crystal': [0x155BF],
                           'Vitreous - Crystal': [0x155B9],
                           'Trinexx - Crystal': [0x155C7, 0x155A7, 0x155AA, 0x155AB]}
