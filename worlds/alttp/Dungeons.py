from __future__ import annotations

import typing
from typing import List, Optional

from BaseClasses import CollectionState, Region, MultiWorld
from Fill import fill_restrictive

from .Bosses import BossFactory, Boss
from .Items import ItemFactory
from .Regions import lookup_boss_drops, key_drop_data
from .Options import smallkey_shuffle

if typing.TYPE_CHECKING:
    from .SubClasses import ALttPLocation, ALttPItem
    from . import ALTTPWorld


class Dungeon:
    def __init__(self, name: str, regions: List[Region], big_key: ALttPItem, small_keys: List[ALttPItem],
                 dungeon_items: List[ALttPItem], player: int):
        self.name = name
        self.regions = regions
        self.big_key = big_key
        self.small_keys = small_keys
        self.dungeon_items = dungeon_items
        self.bosses = dict()
        self.player = player
        self.multiworld = None

    @property
    def boss(self) -> Optional[Boss]:
        return self.bosses.get(None, None)

    @boss.setter
    def boss(self, value: Optional[Boss]):
        self.bosses[None] = value

    @property
    def keys(self) -> List[ALttPItem]:
        return self.small_keys + ([self.big_key] if self.big_key else [])

    @property
    def all_items(self) -> List[ALttPItem]:
        return self.dungeon_items + self.keys

    def is_dungeon_item(self, item: ALttPItem) -> bool:
        return item.player == self.player and item.name in (dungeon_item.name for dungeon_item in self.all_items)

    def __eq__(self, other: Dungeon) -> bool:
        if not other:
            return False
        return self.name == other.name and self.player == other.player

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.multiworld.get_name_string_for_object(self) if self.multiworld \
            else f'{self.name} (Player {self.player})'


def create_dungeons(world: "ALTTPWorld"):
    multiworld = world.multiworld
    player = world.player

    def make_dungeon(name, default_boss, dungeon_regions, big_key, small_keys, dungeon_items):
        dungeon = Dungeon(name, dungeon_regions, big_key,
                          [] if multiworld.smallkey_shuffle[player] == smallkey_shuffle.option_universal else small_keys,
                          dungeon_items, player)
        for item in dungeon.all_items:
            item.dungeon = dungeon
        dungeon.boss = BossFactory(default_boss, player) if default_boss else None
        regions = []
        for region_name in dungeon.regions:
            region = multiworld.get_region(region_name, player)
            region.dungeon = dungeon
            regions.append(region)
            dungeon.multiworld = multiworld
        dungeon.regions = regions
        return dungeon

    ES = make_dungeon('Hyrule Castle', None, ['Hyrule Castle', 'Sewers', 'Sewer Drop', 'Sewers (Dark)', 'Sanctuary'],
                      ItemFactory('Big Key (Hyrule Castle)', player),
                      ItemFactory(['Small Key (Hyrule Castle)'] * 4, player),
                      [ItemFactory('Map (Hyrule Castle)', player)])
    EP = make_dungeon('Eastern Palace', 'Armos Knights', ['Eastern Palace'],
                      ItemFactory('Big Key (Eastern Palace)', player),
                      ItemFactory(['Small Key (Eastern Palace)'] * 2, player),
                      ItemFactory(['Map (Eastern Palace)', 'Compass (Eastern Palace)'], player))
    DP = make_dungeon('Desert Palace', 'Lanmolas',
                      ['Desert Palace North', 'Desert Palace Main (Inner)', 'Desert Palace Main (Outer)',
                       'Desert Palace East'], ItemFactory('Big Key (Desert Palace)', player),
                      ItemFactory(['Small Key (Desert Palace)'] * 4, player),
                      ItemFactory(['Map (Desert Palace)', 'Compass (Desert Palace)'], player))
    ToH = make_dungeon('Tower of Hera', 'Moldorm',
                       ['Tower of Hera (Bottom)', 'Tower of Hera (Basement)', 'Tower of Hera (Top)'],
                       ItemFactory('Big Key (Tower of Hera)', player),
                       [ItemFactory('Small Key (Tower of Hera)', player)],
                       ItemFactory(['Map (Tower of Hera)', 'Compass (Tower of Hera)'], player))
    PoD = make_dungeon('Palace of Darkness', 'Helmasaur King',
                       ['Palace of Darkness (Entrance)', 'Palace of Darkness (Center)',
                        'Palace of Darkness (Big Key Chest)', 'Palace of Darkness (Bonk Section)',
                        'Palace of Darkness (North)', 'Palace of Darkness (Maze)',
                        'Palace of Darkness (Harmless Hellway)', 'Palace of Darkness (Final Section)'],
                       ItemFactory('Big Key (Palace of Darkness)', player),
                       ItemFactory(['Small Key (Palace of Darkness)'] * 6, player),
                       ItemFactory(['Map (Palace of Darkness)', 'Compass (Palace of Darkness)'], player))
    TT = make_dungeon('Thieves Town', 'Blind', ['Thieves Town (Entrance)', 'Thieves Town (Deep)', 'Blind Fight'],
                      ItemFactory('Big Key (Thieves Town)', player),
                      ItemFactory(['Small Key (Thieves Town)'] * 3, player),
                      ItemFactory(['Map (Thieves Town)', 'Compass (Thieves Town)'], player))
    SW = make_dungeon('Skull Woods', 'Mothula', ['Skull Woods Final Section (Entrance)', 'Skull Woods First Section',
                                                 'Skull Woods Second Section', 'Skull Woods Second Section (Drop)',
                                                 'Skull Woods Final Section (Mothula)',
                                                 'Skull Woods First Section (Right)',
                                                 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)'],
                      ItemFactory('Big Key (Skull Woods)', player),
                      ItemFactory(['Small Key (Skull Woods)'] * 5, player),
                      ItemFactory(['Map (Skull Woods)', 'Compass (Skull Woods)'], player))
    SP = make_dungeon('Swamp Palace', 'Arrghus',
                      ['Swamp Palace (Entrance)', 'Swamp Palace (First Room)', 'Swamp Palace (Starting Area)',
                       'Swamp Palace (West)', 'Swamp Palace (Center)', 'Swamp Palace (North)'],
                      ItemFactory('Big Key (Swamp Palace)', player),
                      ItemFactory(['Small Key (Swamp Palace)'] * 6, player),
                      ItemFactory(['Map (Swamp Palace)', 'Compass (Swamp Palace)'], player))
    IP = make_dungeon('Ice Palace', 'Kholdstare',
                      ['Ice Palace (Entrance)', 'Ice Palace (Second Section)', 'Ice Palace (Main)', 'Ice Palace (East)',
                       'Ice Palace (East Top)', 'Ice Palace (Kholdstare)'], ItemFactory('Big Key (Ice Palace)', player),
                      ItemFactory(['Small Key (Ice Palace)'] * 6, player),
                      ItemFactory(['Map (Ice Palace)', 'Compass (Ice Palace)'], player))
    MM = make_dungeon('Misery Mire', 'Vitreous',
                      ['Misery Mire (Entrance)', 'Misery Mire (Main)', 'Misery Mire (West)', 'Misery Mire (Final Area)',
                       'Misery Mire (Vitreous)'], ItemFactory('Big Key (Misery Mire)', player),
                      ItemFactory(['Small Key (Misery Mire)'] * 6, player),
                      ItemFactory(['Map (Misery Mire)', 'Compass (Misery Mire)'], player))
    TR = make_dungeon('Turtle Rock', 'Trinexx',
                      ['Turtle Rock (Entrance)', 'Turtle Rock (First Section)', 'Turtle Rock (Chain Chomp Room)',
                       'Turtle Rock (Pokey Room)',
                       'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Turtle Rock (Crystaroller Room)',
                       'Turtle Rock (Dark Room)', 'Turtle Rock (Eye Bridge)', 'Turtle Rock (Trinexx)'],
                      ItemFactory('Big Key (Turtle Rock)', player),
                      ItemFactory(['Small Key (Turtle Rock)'] * 6, player),
                      ItemFactory(['Map (Turtle Rock)', 'Compass (Turtle Rock)'], player))

    if multiworld.mode[player] != 'inverted':
        AT = make_dungeon('Agahnims Tower', 'Agahnim', ['Agahnims Tower', 'Agahnim 1'], None,
                          ItemFactory(['Small Key (Agahnims Tower)'] * 4, player), [])
        GT = make_dungeon('Ganons Tower', 'Agahnim2',
                          ['Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)', 'Ganons Tower (Compass Room)',
                           'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)', 'Ganons Tower (Firesnake Room)',
                           'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)', 'Ganons Tower (Top)',
                           'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)', 'Agahnim 2'],
                          ItemFactory('Big Key (Ganons Tower)', player),
                          ItemFactory(['Small Key (Ganons Tower)'] * 8, player),
                          ItemFactory(['Map (Ganons Tower)', 'Compass (Ganons Tower)'], player))
    else:
        AT = make_dungeon('Inverted Agahnims Tower', 'Agahnim', ['Inverted Agahnims Tower', 'Agahnim 1'], None,
                          ItemFactory(['Small Key (Agahnims Tower)'] * 4, player), [])
        GT = make_dungeon('Inverted Ganons Tower', 'Agahnim2',
                          ['Inverted Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)',
                           'Ganons Tower (Compass Room)', 'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)',
                           'Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)',
                           'Ganons Tower (Top)', 'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)',
                           'Agahnim 2'], ItemFactory('Big Key (Ganons Tower)', player),
                          ItemFactory(['Small Key (Ganons Tower)'] * 8, player),
                          ItemFactory(['Map (Ganons Tower)', 'Compass (Ganons Tower)'], player))

    GT.bosses['bottom'] = BossFactory('Armos Knights', player)
    GT.bosses['middle'] = BossFactory('Lanmolas', player)
    GT.bosses['top'] = BossFactory('Moldorm', player)

    for dungeon in [ES, EP, DP, ToH, AT, PoD, TT, SW, SP, IP, MM, TR, GT]:
        world.dungeons[dungeon.name] = dungeon


def get_dungeon_item_pool(multiworld: MultiWorld) -> typing.List[ALttPItem]:
    return [item
            for world in multiworld.get_game_worlds("A Link to the Past")
            for item in get_dungeon_item_pool_player(world)]


def get_dungeon_item_pool_player(world) -> typing.List[ALttPItem]:
    return [item
            for dungeon in world.dungeons.values()
            for item in dungeon.all_items]


def get_unfilled_dungeon_locations(multiworld: MultiWorld) -> typing.List[ALttPLocation]:
    return [location
            for world in multiworld.get_game_worlds("A Link to the Past")
            for dungeon in world.dungeons.values()
            for region in dungeon.regions
            for location in region.locations if not location.item]


def fill_dungeons_restrictive(multiworld: MultiWorld):
    """Places dungeon-native items into their dungeons, places nothing if everything is shuffled outside."""
    localized: set = set()
    dungeon_specific: set = set()
    for subworld in multiworld.get_game_worlds("A Link to the Past"):
        player = subworld.player
        if player not in multiworld.groups:
            localized |= {(player, item_name) for item_name in
                          subworld.dungeon_local_item_names}
            dungeon_specific |= {(player, item_name) for item_name in
                                 subworld.dungeon_specific_item_names}

    if localized:
        in_dungeon_items = [item for item in get_dungeon_item_pool(multiworld) if (item.player, item.name) in localized]
        if in_dungeon_items:
            restricted_players = {player for player, restricted in multiworld.restrict_dungeon_item_on_boss.items() if
                                  restricted}
            locations: typing.List["ALttPLocation"] = [
                location for location in get_unfilled_dungeon_locations(multiworld)
                # filter boss
                if not (location.player in restricted_players and location.name in lookup_boss_drops)]
            if dungeon_specific:
                for location in locations:
                    dungeon = location.parent_region.dungeon
                    orig_rule = location.item_rule
                    location.item_rule = lambda item, dungeon=dungeon, orig_rule=orig_rule: \
                        (not (item.player, item.name) in dungeon_specific or item.dungeon is dungeon) and orig_rule(item)

            multiworld.random.shuffle(locations)
            # Dungeon-locked items have to be placed first, to not run out of spaces for dungeon-locked items
            # subsort in the order Big Key, Small Key, Other before placing dungeon items

            sort_order = {"BigKey": 3, "SmallKey": 2}
            in_dungeon_items.sort(
                key=lambda item: sort_order.get(item.type, 1) +
                                 (5 if (item.player, item.name) in dungeon_specific else 0))

            # Construct a partial all_state which contains only the items from get_pre_fill_items,
            # which aren't in_dungeon
            in_dungeon_player_ids = {item.player for item in in_dungeon_items}
            all_state_base = CollectionState(multiworld)
            for item in multiworld.itempool:
                multiworld.worlds[item.player].collect(all_state_base, item)
            pre_fill_items = []
            for player in in_dungeon_player_ids:
                pre_fill_items += multiworld.worlds[player].get_pre_fill_items()
            for item in in_dungeon_items:
                try:
                    pre_fill_items.remove(item)
                except ValueError:
                    # pre_fill_items should be a subset of in_dungeon_items, but just in case
                    pass
            for item in pre_fill_items:
                multiworld.worlds[item.player].collect(all_state_base, item)
            all_state_base.sweep_for_events()

            # Remove completion condition so that minimal-accessibility worlds place keys properly
            for player in {item.player for item in in_dungeon_items}:
                if all_state_base.has("Triforce", player):
                    all_state_base.remove(multiworld.worlds[player].create_item("Triforce"))

            for (player, key_drop_shuffle) in multiworld.key_drop_shuffle.items():
                if not key_drop_shuffle and player not in multiworld.groups:
                    for key_loc in key_drop_data:
                        key_data = key_drop_data[key_loc]
                        all_state_base.remove(ItemFactory(key_data[3], player))
                        loc = multiworld.get_location(key_loc, player)

                        if loc in all_state_base.events:
                            all_state_base.events.remove(loc)
            fill_restrictive(multiworld, all_state_base, locations, in_dungeon_items, True, True,
                             name="LttP Dungeon Items")


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

