# from itertools import chain, combinations

# from worlds.tmc import TMCEvent
from worlds.tmc.constants import TMCItem, TMCLocation
from worlds.tmc.options import DungeonItem, DungeonWarp, ShuffleElements
from worlds.tmc.test import MinishCapTestBase


class TestElementsVanilla(MinishCapTestBase):
    options = {
        "shuffle_elements": ShuffleElements.option_vanilla,
    }

    def test_elements_vanilla(self) -> None:
        """Test that each of the elements gets placed in its vanilla location"""
        prize_names = [
            TMCLocation.DEEPWOOD_PRIZE,
            TMCLocation.COF_PRIZE,
            TMCLocation.DROPLETS_PRIZE,
            TMCLocation.PALACE_PRIZE,
        ]
        prizes = [TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT]
        locations = [self.multiworld.get_location(prize_name, self.player) for prize_name in prize_names]
        for (location, prize) in zip(locations, prizes):
            self.assertEqual(location.item.name, prize)


class TestElementsPrizes(MinishCapTestBase):
    options = {
        "shuffle_elements": ShuffleElements.option_dungeon_prize
    }

    def test_elements_prizes(self) -> None:
        """Test that each of the elements is placed into a prize location"""
        locations = {
            TMCLocation.DEEPWOOD_PRIZE,
            TMCLocation.COF_PRIZE,
            TMCLocation.FORTRESS_PRIZE,
            TMCLocation.DROPLETS_PRIZE,
            TMCLocation.CRYPT_PRIZE,
            TMCLocation.PALACE_PRIZE,
        }
        prizes = {TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT}
        for prize in prizes:
            placements = self.multiworld.find_item_locations(prize, self.player)
            self.assertEqual(len(placements), 1, "Multiple of the same element was placed")
            self.assertIn(placements[0].name, locations, "Element was placed outside a prize location")


class TestElementsAnywhere(MinishCapTestBase):
    """Stub test to ensure generation succeeds when ElementShuffle == anywhere"""
    options = {
        "shuffle_elements": ShuffleElements.option_anywhere
    }


class TestSmallKeysDungeon(MinishCapTestBase):
    options = {
        "dungeon_small_keys": DungeonItem.option_own_dungeon
    }


class TestBigKeysDungeon(MinishCapTestBase):
    options = {
        "dungeon_big_keys": DungeonItem.option_own_dungeon
    }


class TestWindCrests(MinishCapTestBase):
    options = {
        "wind_crest_crenel": 1,
        "wind_crest_falls": 1,
        "wind_crest_clouds": 1,
        "wind_crest_castor": 1,
        "wind_crest_south_field": 1,
        "wind_crest_minish_woods": 1,
    }


#   options = {"wind_crests": WindCrests.default}
#   options_list = [
#       "Mount Crenel",
#       "Veil Falls",
#       "Cloud Tops",
#       "Hyrule Town",
#       # "Lake Hylia",
#       "Castor Wilds",
#       "South Hyrule Field",
#       "Minish Woods",
#   ]
#   default_access_list = [
#       [
#           [TMCItem.CANE_OF_PACCI, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD, TMCItem.SPIN_ATTACK],
#           [TMCItem.CANE_OF_PACCI, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPIN_SCROLL],
#           [TMCItem.CANE_OF_PACCI, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPLIT_SCROLL],
#           [TMCItem.CANE_OF_PACCI, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD, TMCItem.GREATSPIN],
#           [TMCItem.CANE_OF_PACCI, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD, TMCItem.LONG_SPIN],
#           [TMCItem.CANE_OF_PACCI, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.FLIPPERS],
#           [TMCItem.CANE_OF_PACCI, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.ROCS_CAPE],
#           [TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.SPIN_ATTACK],
#           [TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPIN_SCROLL],
#           [TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPLIT_SCROLL],
#           [TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.GREATSPIN],
#           [TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.LONG_SPIN],
#           [TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.BOTTLE, TMCItem.FLIPPERS],
#           [TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.BOTTLE, TMCItem.ROCS_CAPE],
#           [TMCItem.ROCS_CAPE, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD, TMCItem.SPIN_ATTACK],
#           [TMCItem.ROCS_CAPE, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#           TMCItem.FAST_SPIN_SCROLL],
#           [TMCItem.ROCS_CAPE, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPLIT_SCROLL],
#           [TMCItem.ROCS_CAPE, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD, TMCItem.GREATSPIN],
#           [TMCItem.ROCS_CAPE, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD, TMCItem.LONG_SPIN],
#           [TMCItem.ROCS_CAPE, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.FLIPPERS],
#           [TMCItem.ROCS_CAPE, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.ROCS_CAPE],
#           [TMCItem.PROGRESSIVE_BOW, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.SPIN_ATTACK],
#           [TMCItem.PROGRESSIVE_BOW, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPIN_SCROLL],
#           [TMCItem.PROGRESSIVE_BOW, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPLIT_SCROLL],
#           [TMCItem.PROGRESSIVE_BOW, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.GREATSPIN],
#           [TMCItem.PROGRESSIVE_BOW, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.LONG_SPIN],
#           [TMCItem.PROGRESSIVE_BOW, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.FLIPPERS],
#           [TMCItem.PROGRESSIVE_BOW, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.ROCS_CAPE],
#           [TMCItem.PROGRESSIVE_BOOMERANG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE,
#            TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.SPIN_ATTACK],
#           [TMCItem.PROGRESSIVE_BOOMERANG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE,
#            TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPIN_SCROLL],
#           [TMCItem.PROGRESSIVE_BOOMERANG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE,
#            TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPLIT_SCROLL],
#           [TMCItem.PROGRESSIVE_BOOMERANG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE,
#            TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.GREATSPIN],
#           [TMCItem.PROGRESSIVE_BOOMERANG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE,
#            TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.LONG_SPIN],
#           [TMCItem.PROGRESSIVE_BOOMERANG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.FLIPPERS],
#           [TMCItem.PROGRESSIVE_BOOMERANG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.ROCS_CAPE],
#           [TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.SPIN_ATTACK],
#           [TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPIN_SCROLL],
#           [TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.FAST_SPLIT_SCROLL],
#           [TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.GREATSPIN],
#           [TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.PROGRESSIVE_SWORD,
#            TMCItem.LONG_SPIN],
#           [TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.FLIPPERS],
#           [TMCItem.BOMB_BAG, TMCItem.GUST_JAR, TMCItem.GRIP_RING, TMCItem.BOTTLE, TMCItem.ROCS_CAPE],
#       ],
#       [
#           [TMCItem.GRIP_RING, TMCItem.LANTERN, TMCItem.KINSTONE_GOLD_FALLS, TMCItem.BOMB_BAG]
#       ],
#       [
#           [*[TMCItem.KINSTONE_GOLD_CLOUD] * 5, TMCItem.MOLE_MITTS, TMCItem.GRIP_RING, TMCItem.LANTERN,
#            TMCItem.KINSTONE_GOLD_FALLS,
#            TMCItem.BOMB_BAG],
#           [*[TMCItem.KINSTONE_GOLD_CLOUD] * 5, TMCItem.ROCS_CAPE, TMCItem.GRIP_RING, TMCItem.LANTERN,
#            TMCItem.KINSTONE_GOLD_FALLS, TMCItem.BOMB_BAG],
#       ],
#       [
#           [TMCItem.OCARINA],
#           [TMCItem.LONLON_KEY, TMCItem.PROGRESSIVE_SWORD],
#           [TMCItem.LONLON_KEY, TMCItem.LANTERN],
#           [TMCItem.LONLON_KEY, TMCItem.BOMB_BAG],
#           [TMCItem.ROCS_CAPE, TMCItem.PROGRESSIVE_SWORD],
#           [TMCItem.ROCS_CAPE, TMCItem.LANTERN],
#           [TMCItem.ROCS_CAPE, TMCItem.BOMB_BAG],
#           [TMCItem.MOLE_MITTS, TMCItem.FLIPPERS, TMCItem.PROGRESSIVE_SWORD],
#           [TMCItem.MOLE_MITTS, TMCItem.FLIPPERS, TMCItem.LANTERN],
#           [TMCItem.MOLE_MITTS, TMCItem.FLIPPERS, TMCItem.BOMB_BAG],
#       ],
#       [
#           [TMCItem.PEGASUS_BOOTS, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.SPIN_ATTACK],
#           [TMCItem.PEGASUS_BOOTS, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.FAST_SPIN_SCROLL],
#           [TMCItem.PEGASUS_BOOTS, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.FAST_SPLIT_SCROLL],
#           [TMCItem.PEGASUS_BOOTS, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.GREATSPIN],
#           [TMCItem.PEGASUS_BOOTS, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.LONG_SPIN],
#           [TMCItem.ROCS_CAPE, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.SPIN_ATTACK],
#           [TMCItem.ROCS_CAPE, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.FAST_SPIN_SCROLL],
#           [TMCItem.ROCS_CAPE, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.FAST_SPLIT_SCROLL],
#           [TMCItem.ROCS_CAPE, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.GREATSPIN],
#           [TMCItem.ROCS_CAPE, *[TMCItem.PROGRESSIVE_SWORD] * 3, TMCItem.LONG_SPIN],
#       ],
#       [
#           [TMCItem.PROGRESSIVE_SWORD],
#           [TMCItem.LANTERN],
#           [TMCItem.BOMB_BAG],
#       ],
#       [
#           [TMCItem.BOMB_BAG],
#           [TMCItem.PROGRESSIVE_SWORD, TMCEvent.CLEAR_DWS],
#           [TMCItem.LANTERN, TMCEvent.CLEAR_DWS],
#           [TMCItem.OCARINA, TMCEvent.CLEAR_DWS],
#       ],
#   ]
#   location_list = [
#       TMCLocation.CRENEL_UPPER_BLOCK_CHEST,
#       TMCLocation.FALLS_TOP_CAVE_CHEST,
#       TMCLocation.WIND_TRIBE_3F_LEFT_CHEST,  # FUTURE Fusion
#       TMCLocation.LON_LON_PUDDLE_FUSION_BIG_CHEST,  # FUTURE Fusion
#       TMCLocation.SWAMP_BUTTERFLY_FUSION_ITEM,  # FUTURE Fusion
#       TMCLocation.SOUTH_FIELD_FUSION_CHEST,  # FUTURE Fusion
#       TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_1,
#   ]
#
#    def test_crests_combo(self) -> None:
#        """Tests locations near wind crests, checking every combination of settings"""
#
#        options = {1,2,4,5,6}
#        powerset = chain.from_iterable(combinations(options, r) for r in range(len(options) + 1))
#
#        for combo in powerset:
#            if combo == (): continue
#            crests = []
#            for ID in combo:
#                crests.append(self.options_list[ID])
#                self.default_access_list[ID].append([TMCItem.OCARINA])
#            self.options.update({"wind_crests": crests})
#            self.world_setup()
#            for ID in range(7):
#                self.assertAccessDependency([self.location_list[ID]], self.default_access_list[ID], True)
#            self.options.update({"wind_crests": WindCrests.default})
#            for ID in combo:
#                self.default_access_list[ID].remove([TMCItem.OCARINA])

class TestDungeonWarps(MinishCapTestBase):
    options = {
        "dungeon_warp_dws": DungeonWarp.option_both,
        "dungeon_warp_cof": DungeonWarp.option_both,
        "dungeon_warp_fow": DungeonWarp.option_both,
        "dungeon_warp_tod": DungeonWarp.option_both,
        "dungeon_warp_pow": DungeonWarp.option_both,
        "dungeon_warp_dhc": DungeonWarp.option_both,
    }
