from typing import List, Dict

from BaseClasses import Dungeon, Item, MultiWorld, Boss, Region
from Fill import fill_restrictive

from .Regions import lookup_boss_drops
from .Options import smallkey_shuffle
from .Bosses import boss_factory


class ALttpDungeon(Dungeon):
    big_key: Item = None
    small_keys: List[Item] = []

    def __init__(self, name: str, regions: List[str], big_key: Item, small_keys: List[Item],
                 dungeon_items: List[Item], player: int):
        super().__init__(name, regions, player, dungeon_items)
        self.big_key = big_key
        self.small_keys = small_keys


def create_dungeons(world: MultiWorld, player: int):
    def make_dungeon(name: str, default_boss: str, dungeon_regions: List[str], big_key: Item,
                     small_keys: List[Item], dungeon_items: List[Item]):
        dungeon = ALttpDungeon(name, dungeon_regions, big_key,
                          [] if world.smallkey_shuffle[player] == smallkey_shuffle.option_universal else small_keys,
                          dungeon_items, player)
        for item in dungeon.all_items:
            item.dungeon = dungeon
            item.world = world
        dungeon.boss = boss_factory(default_boss, player) if default_boss else None
        for region in dungeon.regions:
            world.get_region(region, player).dungeon = dungeon
            dungeon.world = world
        return dungeon

    ES = make_dungeon('Hyrule Castle', None, ['Hyrule Castle', 'Sewers', 'Sewer Drop', 'Sewers (Dark)', 'Sanctuary'],
                      None, [world.create_item('Small Key (Hyrule Castle)', player)],
                      [world.create_item('Map (Hyrule Castle)', player)])
    EP = make_dungeon('Eastern Palace', 'Armos Knights', ['Eastern Palace'],
                      world.create_item('Big Key (Eastern Palace)', player), [],
                      [world.create_item('Map (Eastern Palace)', player), world.create_item('Compass (Eastern Palace)', player)])
    DP = make_dungeon('Desert Palace', 'Lanmolas',
                      ['Desert Palace North', 'Desert Palace Main (Inner)', 'Desert Palace Main (Outer)',
                       'Desert Palace East'], world.create_item('Big Key (Desert Palace)', player),
                      [world.create_item('Small Key (Desert Palace)', player)],
                      [world.create_item('Map (Desert Palace)', player), world.create_item('Compass (Desert Palace)', player)])
    ToH = make_dungeon('Tower of Hera', 'Moldorm',
                       ['Tower of Hera (Bottom)', 'Tower of Hera (Basement)', 'Tower of Hera (Top)'],
                       world.create_item('Big Key (Tower of Hera)', player),
                       [world.create_item('Small Key (Tower of Hera)', player)],
                       [world.create_item('Map (Tower of Hera)', player), world.create_item('Compass (Tower of Hera)', player)])
    PoD = make_dungeon('Palace of Darkness', 'Helmasaur King',
                       ['Palace of Darkness (Entrance)', 'Palace of Darkness (Center)',
                        'Palace of Darkness (Big Key Chest)', 'Palace of Darkness (Bonk Section)',
                        'Palace of Darkness (North)', 'Palace of Darkness (Maze)',
                        'Palace of Darkness (Harmless Hellway)', 'Palace of Darkness (Final Section)'],
                       world.create_item('Big Key (Palace of Darkness)', player),
                       [world.create_item('Small Key (Palace of Darkness)', player)] * 6,
                       [world.create_item('Map (Palace of Darkness)', player), world.create_item('Compass (Palace of Darkness)', player)])
    TT = make_dungeon('Thieves Town', 'Blind', ['Thieves Town (Entrance)', 'Thieves Town (Deep)', 'Blind Fight'],
                      world.create_item('Big Key (Thieves Town)', player), [world.create_item('Small Key (Thieves Town)', player)],
                      [world.create_item('Map (Thieves Town)', player), world.create_item('Compass (Thieves Town)', player)])
    SW = make_dungeon('Skull Woods', 'Mothula', ['Skull Woods Final Section (Entrance)', 'Skull Woods First Section',
                                                 'Skull Woods Second Section', 'Skull Woods Second Section (Drop)',
                                                 'Skull Woods Final Section (Mothula)',
                                                 'Skull Woods First Section (Right)',
                                                 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)'],
                      world.create_item('Big Key (Skull Woods)', player),
                      [world.create_item('Small Key (Skull Woods)', player)] * 3,
                      [world.create_item('Map (Skull Woods)', player), world.create_item('Compass (Skull Woods)', player)])
    SP = make_dungeon('Swamp Palace', 'Arrghus',
                      ['Swamp Palace (Entrance)', 'Swamp Palace (First Room)', 'Swamp Palace (Starting Area)',
                       'Swamp Palace (Center)', 'Swamp Palace (North)'], world.create_item('Big Key (Swamp Palace)', player),
                      [world.create_item('Small Key (Swamp Palace)', player)],
                      [world.create_item('Map (Swamp Palace)', player), world.create_item('Compass (Swamp Palace)', player)])
    IP = make_dungeon('Ice Palace', 'Kholdstare',
                      ['Ice Palace (Entrance)', 'Ice Palace (Main)', 'Ice Palace (East)', 'Ice Palace (East Top)',
                       'Ice Palace (Kholdstare)'], world.create_item('Big Key (Ice Palace)', player),
                      [world.create_item('Small Key (Ice Palace)', player)] * 2,
                      [world.create_item('Map (Ice Palace)', player), world.create_item('Compass (Ice Palace)', player)])
    MM = make_dungeon('Misery Mire', 'Vitreous',
                      ['Misery Mire (Entrance)', 'Misery Mire (Main)', 'Misery Mire (West)', 'Misery Mire (Final Area)',
                       'Misery Mire (Vitreous)'], world.create_item('Big Key (Misery Mire)', player),
                      [world.create_item('Small Key (Misery Mire)', player)] * 3,
                      [world.create_item('Map (Misery Mire)', player), world.create_item('Compass (Misery Mire)', player)])
    TR = make_dungeon('Turtle Rock', 'Trinexx',
                      ['Turtle Rock (Entrance)', 'Turtle Rock (First Section)', 'Turtle Rock (Chain Chomp Room)',
                       'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Turtle Rock (Crystaroller Room)',
                       'Turtle Rock (Dark Room)', 'Turtle Rock (Eye Bridge)', 'Turtle Rock (Trinexx)'],
                      world.create_item('Big Key (Turtle Rock)', player),
                      [world.create_item('Small Key (Turtle Rock)', player)] * 4,
                      [world.create_item('Map (Turtle Rock)', player), world.create_item('Compass (Turtle Rock)', player)])

    if world.mode[player] != 'inverted':
        AT = make_dungeon('Agahnims Tower', 'Agahnim', ['Agahnims Tower', 'Agahnim 1'], None,
                          [world.create_item('Small Key (Agahnims Tower)', player)] * 2, [])
        GT = make_dungeon('Ganons Tower', 'Agahnim2',
                          ['Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)', 'Ganons Tower (Compass Room)',
                           'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)', 'Ganons Tower (Firesnake Room)',
                           'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)', 'Ganons Tower (Top)',
                           'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)', 'Agahnim 2'],
                          world.create_item('Big Key (Ganons Tower)', player),
                          [world.create_item('Small Key (Ganons Tower)', player)] * 4,
                          [world.create_item('Map (Ganons Tower)', player), world.create_item('Compass (Ganons Tower)', player)])
    else:
        AT = make_dungeon('Inverted Agahnims Tower', 'Agahnim', ['Inverted Agahnims Tower', 'Agahnim 1'], None,
                          [world.create_item('Small Key (Agahnims Tower)', player)] * 2, [])
        GT = make_dungeon('Inverted Ganons Tower', 'Agahnim2',
                          ['Inverted Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)',
                           'Ganons Tower (Compass Room)', 'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)',
                           'Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)',
                           'Ganons Tower (Top)', 'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)',
                           'Agahnim 2'], world.create_item('Big Key (Ganons Tower)', player),
                          [world.create_item('Small Key (Ganons Tower)', player)] * 4,
                          [world.create_item('Map (Ganons Tower)', player), world.create_item('Compass (Ganons Tower)', player)])

    GT.bosses['bottom'] = boss_factory('Armos Knights', player)
    GT.bosses['middle'] = boss_factory('Lanmolas', player)
    GT.bosses['top'] = boss_factory('Moldorm', player)

    for dungeon in [ES, EP, DP, ToH, AT, PoD, TT, SW, SP, IP, MM, TR, GT]:
        world.dungeons[dungeon.name, dungeon.player] = dungeon


def get_dungeon_item_pool(world) -> List:
    return [item for dungeon in world.dungeons.values() for item in dungeon.all_items]


def get_dungeon_item_pool_player(world, player) -> List:
    return [item for dungeon in world.world.dungeons.values() if dungeon.player == player for item in dungeon.all_items]


def fill_dungeons_restrictive(world):
    """Places dungeon-native items into their dungeons, places nothing if everything is shuffled outside."""
    localized: set = set()
    dungeon_specific: set = set()
    for subworld in world.get_game_worlds("A Link to the Past"):
        player = subworld.player
        localized |= {(player, item_name) for item_name in
                      subworld.dungeon_local_item_names}
        dungeon_specific |= {(player, item_name) for item_name in
                             subworld.dungeon_specific_item_names}

    if localized:
        in_dungeon_items = [item for item in get_dungeon_item_pool(world) if (item.player, item.name) in localized]
        if in_dungeon_items:
            restricted_players = {player for player, restricted in world.restrict_dungeon_item_on_boss.items() if
                                  restricted}
            locations = [location for location in world.get_unfilled_dungeon_locations()
                         # filter boss
                         if not (location.player in restricted_players and location.name in lookup_boss_drops)]
            if dungeon_specific:
                for location in locations:
                    dungeon = location.parent_region.dungeon
                    orig_rule = location.item_rule
                    location.item_rule = lambda item, dungeon=dungeon, orig_rule=orig_rule: \
                        (not (item.player, item.name) in dungeon_specific or item.dungeon is dungeon) and orig_rule(item)

            world.random.shuffle(locations)
            all_state_base = world.get_all_state(use_cache=True)
            # Dungeon-locked items have to be placed first, to not run out of spaces for dungeon-locked items
            # subsort in the order Big Key, Small Key, Other before placing dungeon items

            sort_order = {"BigKey": 3, "SmallKey": 2}
            in_dungeon_items.sort(
                key=lambda item: sort_order.get(item.type, 1) +
                                 (5 if (item.player, item.name) in dungeon_specific else 0))
            for item in in_dungeon_items:
                all_state_base.remove(item)
            fill_restrictive(world, all_state_base, locations, in_dungeon_items, True, True)


dungeon_music_addresses = {'Eastern Palace - Prize': [0x1559A],
                           'Desert Palace - Prize': [0x1559B, 0x1559C, 0x1559D, 0x1559E],
                           'Tower of Hera - Prize': [0x155C5, 0x1107A, 0x10B8C],
                           'Palace of Darkness - Prize': [0x155B8],
                           'Swamp Palace - Prize': [0x155B7],
                           'Thieves\' Town - Prize': [0x155C6],
                           'Skull Woods - Prize': [0x155BA, 0x155BB, 0x155BC, 0x155BD, 0x15608, 0x15609, 0x1560A,
                                                   0x1560B],
                           'Ice Palace - Prize': [0x155BF],
                           'Misery Mire - Prize': [0x155B9],
                           'Turtle Rock - Prize': [0x155C7, 0x155A7, 0x155AA, 0x155AB]}
