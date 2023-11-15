from Options import Toggle

from . import PokemonEmeraldTestBase
from ..util import location_name_to_label
from ..options import NormanRequirement


class TestBasic(PokemonEmeraldTestBase):
    def test_always_accessible(self) -> None:
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_102_POTION")))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_SUPER_POTION")))


class TestScorchedSlabPond(PokemonEmeraldTestBase):
    options = {
        "enable_ferry": Toggle.option_true,
        "require_flash": Toggle.option_false
    }

    def test_with_neither(self) -> None:
        self.collect_by_name(["S.S. Ticket", "Letter", "Stone Badge", "HM01 Cut"])
        self.assertTrue(self.can_reach_region("REGION_ROUTE120/NORTH"))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_ROUTE_120_NEST_BALL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_SCORCHED_SLAB_TM11")))

    def test_with_surf(self) -> None:
        self.collect_by_name(["S.S. Ticket", "Letter", "Stone Badge", "HM01 Cut", "HM03 Surf", "Balance Badge"])
        self.assertTrue(self.can_reach_region("REGION_ROUTE120/NORTH"))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_ROUTE_120_NEST_BALL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_SCORCHED_SLAB_TM11")))

    def test_with_scope(self) -> None:
        self.collect_by_name(["S.S. Ticket", "Letter", "Stone Badge", "HM01 Cut", "Devon Scope"])
        self.assertTrue(self.can_reach_region("REGION_ROUTE120/NORTH"))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_120_NEST_BALL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_SCORCHED_SLAB_TM11")))

    def test_with_both(self) -> None:
        self.collect_by_name(["S.S. Ticket", "Letter", "Stone Badge", "HM01 Cut", "Devon Scope", "HM03 Surf", "Balance Badge"])
        self.assertTrue(self.can_reach_region("REGION_ROUTE120/NORTH"))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_120_NEST_BALL")))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_SCORCHED_SLAB_TM11")))


class TestSurf(PokemonEmeraldTestBase):
    options = {
        "npc_gifts": Toggle.option_true
    }

    def test_inaccessible_with_no_surf(self) -> None:
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_PETALBURG_CITY_ETHER")))
        self.assertFalse(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))
        self.assertFalse(self.can_reach_entrance("REGION_ROUTE118/WATER -> REGION_ROUTE118/EAST"))
        self.assertFalse(self.can_reach_entrance("REGION_ROUTE119/UPPER -> REGION_FORTREE_CITY/MAIN"))
        self.assertFalse(self.can_reach_entrance("MAP_FORTREE_CITY:3/MAP_FORTREE_CITY_MART:0"))

    def test_accessible_with_surf_only(self) -> None:
        self.collect_by_name(["HM03 Surf", "Balance Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_PETALBURG_CITY_ETHER")))
        self.assertTrue(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))
        self.assertTrue(self.can_reach_entrance("REGION_ROUTE118/WATER -> REGION_ROUTE118/EAST"))
        self.assertTrue(self.can_reach_entrance("REGION_ROUTE119/UPPER -> REGION_FORTREE_CITY/MAIN"))
        self.assertTrue(self.can_reach_entrance("MAP_FORTREE_CITY:3/MAP_FORTREE_CITY_MART:0"))
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_4")))


class TestFreeFly(PokemonEmeraldTestBase):
    options = {
        "npc_gifts": Toggle.option_true,
        "free_fly_location": Toggle.option_true
    }

    def setUp(self) -> None:
        super(PokemonEmeraldTestBase, self).setUp()

        # Swap free fly to Sootopolis
        free_fly_location = self.multiworld.get_location("FREE_FLY_LOCATION", 1)
        free_fly_location.item = None
        free_fly_location.place_locked_item(self.multiworld.worlds[1].create_event("EVENT_VISITED_SOOTOPOLIS_CITY"))

    def test_sootopolis_gift_inaccessible_with_no_surf(self) -> None:
        self.collect_by_name(["HM02 Fly", "Feather Badge"])
        self.assertFalse(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_TM31")))

    def test_sootopolis_gift_accessible_with_surf(self) -> None:
        self.collect_by_name(["HM03 Surf", "Balance Badge", "HM02 Fly", "Feather Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_TM31")))


class TestFerry(PokemonEmeraldTestBase):
    options = {
        "npc_gifts": Toggle.option_true,
        "enable_ferry": Toggle.option_true
    }

    def test_inaccessible_with_no_items(self) -> None:
        self.assertFalse(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))

    def test_inaccessible_with_only_slateport_access(self) -> None:
        self.collect_by_name(["HM06 Rock Smash", "Dynamo Badge", "Acro Bike"])
        self.assertTrue(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))

    def test_accessible_with_slateport_access_and_ticket(self) -> None:
        self.collect_by_name(["HM06 Rock Smash", "Dynamo Badge", "Acro Bike", "S.S. Ticket"])
        self.assertTrue(self.can_reach_location(location_name_to_label("NPC_GIFT_RECEIVED_SOOTHE_BELL")))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))


class TestExtraBouldersOn(PokemonEmeraldTestBase):
    options = {
        "extra_boulders": Toggle.option_true
    }

    def test_inaccessible_with_no_items(self) -> None:
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))

    def test_inaccessible_with_surf_only(self) -> None:
        self.collect_by_name(["HM03 Surf", "Balance Badge"])
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))

    def test_accessible_with_surf_and_strength(self) -> None:
        self.collect_by_name(["HM03 Surf", "Balance Badge", "HM04 Strength", "Heat Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))


class TestExtraBouldersOff(PokemonEmeraldTestBase):
    options = {
        "extra_boulders": Toggle.option_false
    }

    def test_inaccessible_with_no_items(self) -> None:
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))

    def test_accessible_with_surf_only(self) -> None:
        self.collect_by_name(["HM03 Surf", "Balance Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_115_PP_UP")))


class TestNormanRequirement1(PokemonEmeraldTestBase):
    options = {
        "norman_requirement": NormanRequirement.option_badges,
        "norman_count": 0
    }

    def test_accessible_with_no_items(self) -> None:
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_5")))


class TestNormanRequirement2(PokemonEmeraldTestBase):
    options = {
        "norman_requirement": NormanRequirement.option_badges,
        "norman_count": 4
    }

    def test_inaccessible_with_no_items(self) -> None:
        self.assertFalse(self.can_reach_location(location_name_to_label("BADGE_5")))

    def test_accessible_with_enough_badges(self) -> None:
        self.collect_by_name(["Stone Badge", "Knuckle Badge", "Feather Badge", "Balance Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_5")))


class TestNormanRequirement3(PokemonEmeraldTestBase):
    options = {
        "norman_requirement": NormanRequirement.option_gyms,
        "norman_count": 0
    }

    def test_accessible_with_no_items(self) -> None:
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_5")))


class TestNormanRequirement4(PokemonEmeraldTestBase):
    options = {
        "norman_requirement": NormanRequirement.option_gyms,
        "norman_count": 4
    }

    def test_inaccessible_with_no_items(self) -> None:
        self.assertFalse(self.can_reach_location(location_name_to_label("BADGE_5")))

    def test_accessible_with_reachable_gyms(self) -> None:
        self.collect_by_name(["HM03 Surf", "Balance Badge"])  # Reaches Roxanne, Brawley, Wattson, and Flannery
        self.assertTrue(self.can_reach_location(location_name_to_label("BADGE_5")))


class TestVictoryRoad(PokemonEmeraldTestBase):
    options = {
        "elite_four_requirement": NormanRequirement.option_badges,
        "elite_four_count": 0,
        "remove_roadblocks": {"Lilycove City Wailmer"}
    }

    def test_accessible_with_specific_hms(self) -> None:
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM03 Surf", "Balance Badge"])
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM07 Waterfall", "Rain Badge"])
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM04 Strength", "Heat Badge"])
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM06 Rock Smash", "Dynamo Badge"])
        self.assertFalse(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
        self.collect_by_name(["HM05 Flash", "Knuckle Badge"])
        self.assertTrue(self.can_reach_location("EVENT_DEFEAT_CHAMPION"))
