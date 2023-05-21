from test.TestBase import WorldTestBase
from worlds.pokemon_emerald.util import location_name_to_label
from worlds.pokemon_emerald.options import NormanRequirement
from Options import Toggle

class TestBasic(WorldTestBase):
    game = "Pokemon Emerald"

    def testAlwaysAccessible(self):
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_102_POTION")))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_SUPER_POTION")))


class TestSurf(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "npc_gifts": Toggle.option_true
    }

    def testInaccessibleWithNoSurf(self):
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_PETALBURG_CITY_ETHER")))
        self.assertFalse(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))
        self.assertFalse(self.can_reach_entrance("REGION_ROUTE118/WATER -> REGION_ROUTE118/EAST"))
        self.assertFalse(self.can_reach_entrance("REGION_ROUTE119/UPPER -> REGION_FORTREE_CITY/MAIN"))
        self.assertFalse(self.can_reach_entrance("MAP_FORTREE_CITY:3/MAP_FORTREE_CITY_MART:0"))

    def testAccessibleWithSurfOnly(self):
        self.collect_by_name(["HM03 Surf", "Balance Badge"])
        self.multiworld.state.sweep_for_events()
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_PETALBURG_CITY_ETHER")))
        self.assertTrue(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))
        self.assertTrue(self.can_reach_entrance("REGION_ROUTE118/WATER -> REGION_ROUTE118/EAST"))
        self.assertTrue(self.can_reach_entrance("REGION_ROUTE119/UPPER -> REGION_FORTREE_CITY/MAIN"))
        self.assertTrue(self.can_reach_entrance("MAP_FORTREE_CITY:3/MAP_FORTREE_CITY_MART:0"))
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_4")))


class TestFerry(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "npc_gifts": Toggle.option_true,
        "enable_ferry": Toggle.option_true
    }

    def testInaccessibleWithNoItems(self):
        self.assertFalse(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))

    def testInaccessibleWithOnlySlateportAccess(self):
        self.collect_by_name(["HM06 Rock Smash", "Dynamo Badge", "Acro Bike"])
        self.assertTrue(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))

    def testAccessibleWithSlateportAccessAndTicket(self):
        self.collect_by_name(["HM06 Rock Smash", "Dynamo Badge", "Acro Bike", "S.S. Ticket"])
        self.assertTrue(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))


class TestExtraBouldersOn(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "extra_boulders": Toggle.option_true
    }

    def testInaccessibleWithNoItems(self):
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))

    def testInaccessibleWithSurfOnly(self):
        self.collect_by_name(["HM03 Surf", "Balance Badge"])
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))

    def testAccessibleWithSurfAndStrength(self):
        self.collect_by_name(["HM03 Surf", "Balance Badge", "HM04 Strength", "Heat Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))


class TestExtraBouldersOff(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "extra_boulders": Toggle.option_false
    }

    def testInaccessibleWithNoItems(self):
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))

    def testAccessibleWithSurfOnly(self):
        self.collect_by_name(["HM03 Surf", "Balance Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))


class TestNormanRequirement1(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "norman_requirement": NormanRequirement.option_badges,
        "norman_count": 0
    }

    def testAccessibleWithNoItems(self):
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_5")))


class TestNormanRequirement2(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "norman_requirement": NormanRequirement.option_badges,
        "norman_count": 4
    }

    def testInaccessibleWithNoItems(self):
        self.assertFalse(self.can_reach_location(location_name_to_label("BADGE_5")))

    def testAccessibleWithEnoughBadges(self):
        self.collect_by_name(["Stone Badge", "Knuckle Badge", "Feather Badge", "Balance Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_5")))


class TestNormanRequirement3(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "norman_requirement": NormanRequirement.option_gyms,
        "norman_count": 0
    }

    def testAccessibleWithNoItems(self):
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_5")))


class TestNormanRequirement4(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "norman_requirement": NormanRequirement.option_gyms,
        "norman_count": 4
    }

    def testInaccessibleWithNoItems(self):
        self.assertFalse(self.can_reach_location(location_name_to_label("BADGE_5")))

    def testAccessibleWithReachableGyms(self):
        self.collect_by_name(["HM03 Surf", "Balance Badge"]) # Reaches Roxanne, Brawley, Wattson, and Flannery
        self.multiworld.state.sweep_for_events()
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_5")))


class TestVictoryRoad(WorldTestBase):
    game = "Pokemon Emerald"
    options = {
        "elite_four_requirement": NormanRequirement.option_badges,
        "elite_four_count": 0,
        "remove_roadblocks": {"Lilycove City Wailmer"}
    }

    def testAccessibleWithSpecificHMs(self):
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM03 Surf", "Balance Badge"])
        self.multiworld.state.sweep_for_events()
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM07 Waterfall", "Rain Badge"])
        self.multiworld.state.sweep_for_events()
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM04 Strength", "Heat Badge"])
        self.multiworld.state.sweep_for_events()
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM06 Rock Smash", "Dynamo Badge"])
        self.multiworld.state.sweep_for_events()
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM05 Flash", "Knuckle Badge"])
        self.multiworld.state.sweep_for_events()
        self.assertTrue(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
