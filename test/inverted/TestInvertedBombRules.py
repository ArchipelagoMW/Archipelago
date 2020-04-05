import unittest

from BaseClasses import World
from Dungeons import create_dungeons
from EntranceShuffle import connect_entrance, Inverted_LW_Entrances, Inverted_LW_Dungeon_Entrances, Inverted_LW_Single_Cave_Doors, Inverted_Old_Man_Entrances, Inverted_DW_Entrances, Inverted_DW_Dungeon_Entrances, Inverted_DW_Single_Cave_Doors, \
    Inverted_LW_Entrances_Must_Exit, Inverted_LW_Dungeon_Entrances_Must_Exit, Inverted_Bomb_Shop_Multi_Cave_Doors, Inverted_Bomb_Shop_Single_Cave_Doors, Inverted_Blacksmith_Single_Cave_Doors, Inverted_Blacksmith_Multi_Cave_Doors
from InvertedRegions import create_inverted_regions
from ItemList import difficulties
from Rules import set_inverted_big_bomb_rules


class TestInvertedBombRules(unittest.TestCase):

    def setUp(self):
        self.world = World(1, 'vanilla', 'noglitches', 'inverted', 'random', 'normal', 'normal', 'none', 'on', 'ganon', 'balanced',
                           True, False, False, False, False, False, False, False, False, None,
                           'none', False)
        self.world.difficulty_requirements = difficulties['normal']
        create_inverted_regions(self.world, 1)
        create_dungeons(self.world, 1)

    #TODO: Just making sure I haven't missed an entrance.  It would be good to test the rules make sense as well.
    def testInvertedBombRulesAreComplete(self):
        entrances = list(Inverted_LW_Entrances + Inverted_LW_Dungeon_Entrances + Inverted_LW_Single_Cave_Doors + Inverted_Old_Man_Entrances + Inverted_DW_Entrances + Inverted_DW_Dungeon_Entrances + Inverted_DW_Single_Cave_Doors)
        must_exits = list(Inverted_LW_Entrances_Must_Exit + Inverted_LW_Dungeon_Entrances_Must_Exit)
        for entrance_name in (entrances + must_exits):
            if entrance_name not in ['Desert Palace Entrance (East)', 'Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']:
                entrance = self.world.get_entrance(entrance_name, 1)
                connect_entrance(self.world, entrance, 'Inverted Big Bomb Shop', 1)
                set_inverted_big_bomb_rules(self.world, 1)
                entrance.connected_region.entrances.remove(entrance)
                entrance.connected_region = None

    def testInvalidEntrancesAreNotUsed(self):
        entrances = list(Inverted_Blacksmith_Multi_Cave_Doors + Inverted_Blacksmith_Single_Cave_Doors + Inverted_Bomb_Shop_Multi_Cave_Doors + Inverted_Bomb_Shop_Single_Cave_Doors)
        invalid_entrances = ['Desert Palace Entrance (East)', 'Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)', 'Pyramid Fairy']
        for invalid_entrance in invalid_entrances:
            self.assertNotIn(invalid_entrance, entrances)

    def testInvalidEntrances(self):
        for entrance_name in ['Desert Palace Entrance (East)', 'Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']:
            entrance = self.world.get_entrance(entrance_name, 1)
            connect_entrance(self.world, entrance, 'Inverted Big Bomb Shop', 1)
            with self.assertRaises(Exception):
                set_inverted_big_bomb_rules(self.world, 1)
            entrance.connected_region.entrances.remove(entrance)
            entrance.connected_region = None
