from worlds.alttp.Dungeons import create_dungeons
from worlds.alttp.EntranceShuffle import connect_entrance, Inverted_LW_Entrances, Inverted_LW_Dungeon_Entrances, Inverted_LW_Single_Cave_Doors, Inverted_Old_Man_Entrances, Inverted_DW_Entrances, Inverted_DW_Dungeon_Entrances, Inverted_DW_Single_Cave_Doors, \
    Inverted_LW_Entrances_Must_Exit, Inverted_LW_Dungeon_Entrances_Must_Exit, Inverted_Bomb_Shop_Multi_Cave_Doors, Inverted_Bomb_Shop_Single_Cave_Doors, Blacksmith_Single_Cave_Doors, Inverted_Blacksmith_Multi_Cave_Doors
from worlds.alttp.InvertedRegions import create_inverted_regions
from worlds.alttp.ItemPool import difficulties
from worlds.alttp.Rules import set_inverted_big_bomb_rules
from worlds.alttp.test import LTTPTestBase


class TestInvertedBombRules(LTTPTestBase):

    def setUp(self):
        self.world_setup()
        self.multiworld.mode[1] = "inverted"
        self.multiworld.difficulty_requirements[1] = difficulties['normal']
        create_inverted_regions(self.multiworld, 1)
        self.multiworld.worlds[1].create_dungeons()

    #TODO: Just making sure I haven't missed an entrance.  It would be good to test the rules make sense as well.
    def testInvertedBombRulesAreComplete(self):
        entrances = list(Inverted_LW_Entrances + Inverted_LW_Dungeon_Entrances + Inverted_LW_Single_Cave_Doors + Inverted_Old_Man_Entrances + Inverted_DW_Entrances + Inverted_DW_Dungeon_Entrances + Inverted_DW_Single_Cave_Doors)
        must_exits = list(Inverted_LW_Entrances_Must_Exit + Inverted_LW_Dungeon_Entrances_Must_Exit)
        for entrance_name in (entrances + must_exits):
            if entrance_name not in ['Desert Palace Entrance (East)', 'Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']:
                entrance = self.multiworld.get_entrance(entrance_name, 1)
                connect_entrance(self.multiworld, entrance_name, 'Inverted Big Bomb Shop', 1)
                set_inverted_big_bomb_rules(self.multiworld, 1)
                entrance.connected_region.entrances.remove(entrance)
                entrance.connected_region = None

    def testInvalidEntrancesAreNotUsed(self):
        entrances = list(Inverted_Blacksmith_Multi_Cave_Doors + Blacksmith_Single_Cave_Doors + Inverted_Bomb_Shop_Multi_Cave_Doors + Inverted_Bomb_Shop_Single_Cave_Doors)
        invalid_entrances = ['Desert Palace Entrance (East)', 'Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)', 'Pyramid Fairy']
        for invalid_entrance in invalid_entrances:
            self.assertNotIn(invalid_entrance, entrances)

    def testInvalidEntrances(self):
        for entrance_name in ['Desert Palace Entrance (East)', 'Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']:
            entrance = self.multiworld.get_entrance(entrance_name, 1)
            connect_entrance(self.multiworld, entrance_name, 'Inverted Big Bomb Shop', 1)
            with self.assertRaises(Exception):
                set_inverted_big_bomb_rules(self.multiworld, 1)
            entrance.connected_region.entrances.remove(entrance)
            entrance.connected_region = None
