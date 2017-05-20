from Items import *
import random
from BaseClasses import CollectionState


def fill_dungeons(world):
    ES = (['Hyrule Castle'], None, [ESSmallKey()], [ESMap()])
    EP = (['Eastern Palace'], EPBigKey(), [], [EPMap(), EPCompass()])
    DP = (['Desert Palace Main', 'Desert Palace East', 'Desert Palace North'], DPBigKey(), [DPSmallKey()], [DPCompass(), DPMap()])
    ToH = (['Tower of Hera (Bottom)', 'Tower of Hera (Basement)', 'Tower of Hera (Top)'], THBigKey(), [THSmallKey()], [THCompass(), THMap()])
    AT = (['Aghanims Tower', 'Aghanim 1'], None, [ATSmallKey(), ATSmallKey()], [])
    PoD = (['Dark Palace (Entrance)', 'Dark Palace (Center)', 'Dark Palace (Big Key Chest)', 'Dark Palace (Bonk Section)', 'Dark Palace (North)', 'Dark Palace (Maze)', 'Dark Palace (Spike Statue Room)', 'Dark Palace (Final Section)'], PDBigKey(), [PDSmallKey(), PDSmallKey(), PDSmallKey(), PDSmallKey(), PDSmallKey(), PDSmallKey()], [PDCompass(), PDMap()])
    TT = (['Thieves Town (Entrance)', 'Thieves Town (Deep)', 'Blind Fight'], TTBigKey(), [TTSmallKey()], [TTCompass(), TTMap()])
    SW = (['Skull Woods First Section', 'Skull Woods Second Section', 'Skull Woods Final Section (Entrance)', 'Skull Woods Final Section (Mothula)'], SWBigKey(), [SWSmallKey(), SWSmallKey()], [SWCompass(), SWMap()])
    SP = (['Swamp Palace (Entrance)', 'Swamp Palace (First Room)', 'Swamp Palace (Starting Area)', 'Swamp Palace (Center)', 'Swamp Palace (North)'], SPBigKey(), [SPSmallKey()], [SPMap(), SPCompass()])
    IP = (['Ice Palace (Entrance)', 'Ice Palace (Main)', 'Ice Palace (East)', 'Ice Palace (East Top)', 'Ice Palace (Kholdstare)'], IPBigKey(), [IPSmallKey(), IPSmallKey()], [IPMap(), IPCompass()])
    MM = (['Misery Mire (Entrance)', 'Misery Mire (Main)', 'Misery Mire (West)', 'Misery Mire (Final Area)', 'Misery Mire (Vitreous)'], MMBigKey(), [MMSmallKey(), MMSmallKey(), MMSmallKey()], [MMCompass(), MMMap()])
    TR = (['Turtle Rock (Entrance)', 'Turtle Rock (First Section)', 'Turtle Rock (Chain Chomp Room)', 'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Turtle Rock (Roller Switch Room)', 'Turtle Rock (Dark Room)', 'Turtle Rock (Eye Bridge)', 'Turtle Rock (Trinexx)'], TRBigKey(), [TRSmallKey(), TRSmallKey(), TRSmallKey(), TRSmallKey()], [TRMap(), TRCompass()])
    GT = (['Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)', 'Ganons Tower (Compass Room)', 'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)', 'Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)', 'Ganons Tower (Top)', 'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)', 'Aghanim 2'], GTBigKey(), [GTSmallKey(), GTSmallKey(), GTSmallKey(), GTSmallKey()], [GTMap(), GTCompass()])

    freebes = ['[dungeon-A2-1F] Ganons Tower - Map Room', '[dungeon-D1-1F] Dark Palace - Spike Statue Room', '[dungeon-D1-1F] Dark Palace - Big Key Room']

    # this key is in a fixed location (for now)
    world.push_item(world.get_location('[dungeon - D3 - B1] Skull Woods - South of Big Chest'), SWSmallKey(), False)

    for dungeon_regions, big_key, small_keys, dungeon_items in [TR, ES, EP, DP, ToH, AT, PoD, TT, SW, SP, IP, MM, GT]:
        # this is what we need to fill
        dungeon_locations = [location for location in world.get_unfilled_locations() if location.parent_region.name in dungeon_regions]
        random.shuffle(dungeon_locations)

        all_state = CollectionState(world, True)

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
            dungeon_locations.remove(bk_location)
            all_state._clear_cache()

        # next place small keys
        for small_key in small_keys:
            sk_location = None
            for location in dungeon_locations:
                if location.name in freebes or location.can_reach(all_state):
                    sk_location = location
                    break

            if sk_location is None:
                raise RuntimeError('No suitable location for %s' % small_key)

            world.push_item(sk_location, small_key, False)
            dungeon_locations.remove(sk_location)
            all_state._clear_cache()

        # next place dungeon items
        if world.place_dungeon_items:
            for dungeon_item in dungeon_items:
                di_location = dungeon_locations.pop()
                world.push_item(di_location, dungeon_item, False)

    world.state._clear_cache()
