from Fill import distribute_items_restrictive
from ..Data import get_boosts_data
from . import CivVITestBase


class TestBoostsanityIncluded(CivVITestBase):
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "boostsanity": "true",
        "progression_style": "none",
        "shuffle_goody_hut_rewards": "false",
    }

    def test_boosts_get_included(self) -> None:
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        locations = self.multiworld.get_locations(self.player)
        found_locations = 0
        for location in locations:
            if "BOOST" in location.name:
                found_locations += 1
        num_boost_locations = len(get_boosts_data())
        self.assertEqual(found_locations, num_boost_locations)

    def test_boosts_require_prereqs_no_progressives(self) -> None:
        self.world_setup()
        location = "BOOST_TECH_ADVANCED_BALLISTICS"
        items_to_give = ["Refining", "Electricity", "Apprenticeship", "Industrialization"]
        self.assertFalse(self.can_reach_location(location))

        for prereq in items_to_give:
            self.collect_by_name(prereq)
            is_last_prereq = prereq == items_to_give[-1]
            self.assertEqual(self.can_reach_location(location), is_last_prereq)


class TestBoostsanityIncludedNoProgressiveDistricts(CivVITestBase):
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "boostsanity": "true",
        "progression_style": "districts_only",
        "shuffle_goody_hut_rewards": "false",
    }

    def test_boosts_get_included(self) -> None:
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        locations = self.multiworld.get_locations(self.player)
        found_locations = 0
        for location in locations:
            if "BOOST" in location.name:
                found_locations += 1
        num_boost_locations = len(get_boosts_data())
        self.assertEqual(found_locations, num_boost_locations)


class TestBoostsanityPrereqsWithProgressiveDistricts(CivVITestBase):
    options = {
        "progressive_eras": "true",
        "boostsanity": "true",
        "progression_style": "districts_only",
        "shuffle_goody_hut_rewards": "false",
    }

    def test_boosts_require_progressive_prereqs_optional(self) -> None:
        location = "BOOST_TECH_NUCLEAR_FUSION"
        items_to_give = ["Progressive Industrial Zone", "Progressive Industrial Zone"]

        self.assertFalse(self.can_reach_location(location))
        for prereq in items_to_give:
            self.collect_by_name(prereq)
            is_last_prereq = prereq == items_to_give[-1]
            self.assertEqual(self.can_reach_location(location), is_last_prereq)

    def tests_boosts_require_correct_progressive_district_count(self) -> None:
        location = "BOOST_TECH_RIFLING"
        items_to_give = ["Mining", "Progressive Encampment", "Progressive Encampment"]

        self.assertFalse(self.can_reach_location(location))
        for prereq in items_to_give:
            self.collect_by_name(prereq)
            is_last_prereq = prereq == items_to_give[-1]
            self.assertEqual(self.can_reach_location(location), is_last_prereq)


class TestBoostsanityExcluded(CivVITestBase):
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "boostsanity": "false",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "false",
    }

    def test_boosts_are_not_included(self) -> None:
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        locations = self.multiworld.get_locations(self.player)
        found_locations = 0
        for location in locations:
            if "BOOST" in location.name:
                found_locations += 1
        self.assertEqual(found_locations, 0)


class TestBoostsanityEraRequired(CivVITestBase):
    options = {
        "boostsanity": "true",
        "progression_style": "none",
        "shuffle_goody_hut_rewards": "false",
    }

    def test_era_required_boosts_not_accessible_early(self) -> None:
        # BOOST_CIVIC_FEUDALISM has EraRequired=True and ERA_CLASSICAL
        # It should NOT be accessible in Ancient era
        self.assertFalse(self.can_reach_location("BOOST_CIVIC_FEUDALISM"))

        # BOOST_CIVIC_URBANIZATION has EraRequired=True and ERA_INDUSTRIAL
        # It should NOT be accessible in Ancient era
        self.assertFalse(self.can_reach_location("BOOST_CIVIC_URBANIZATION"))

        # BOOST_CIVIC_SPACE_RACE has EraRequired=True and ERA_ATOMIC
        # It should NOT be accessible in Ancient era
        self.assertFalse(self.can_reach_location("BOOST_CIVIC_SPACE_RACE"))

        # Regular boosts without EraRequired should be accessible
        self.assertTrue(self.can_reach_location("BOOST_TECH_SAILING"))
        self.assertTrue(self.can_reach_location("BOOST_CIVIC_MILITARY_TRADITION"))

    def test_era_required_boosts_accessible_in_correct_era(self) -> None:
        # Collect items to reach Classical era
        self.collect_by_name(["Mining", "Bronze Working", "Astrology", "Writing",
                              "Irrigation", "Sailing", "Animal Husbandry",
                              "State Workforce", "Foreign Trade"])

        # BOOST_CIVIC_FEUDALISM should now be accessible in Classical era
        self.assertTrue(self.can_reach_location("BOOST_CIVIC_FEUDALISM"))

        # BOOST_CIVIC_URBANIZATION still not accessible (requires Industrial)
        self.assertFalse(self.can_reach_location("BOOST_CIVIC_URBANIZATION"))

        # Collect more items to reach Industrial era
        self.collect_all_but(["TECH_ROCKETRY"])

        # Now BOOST_CIVIC_URBANIZATION should be accessible
        self.assertTrue(self.can_reach_location("BOOST_CIVIC_URBANIZATION"))


class TestBoostsanityEraRequiredWithProgression(CivVITestBase):
    options = {
        "boostsanity": "true",
        "progression_style": "eras_and_districts",
        "shuffle_goody_hut_rewards": "false",
    }

    def test_era_required_with_progressive_eras(self) -> None:
        # Collect all items except Progressive Era
        self.collect_all_but(["Progressive Era"])

        # Even with all other items, era-required boosts should not be accessible
        self.assertFalse(self.can_reach_location("BOOST_CIVIC_FEUDALISM"))
        self.assertFalse(self.can_reach_location("BOOST_CIVIC_URBANIZATION"))

        # Collect enough Progressive Era items to reach Classical (needs 2)
        self.collect(self.get_item_by_name("Progressive Era"))
        self.collect(self.get_item_by_name("Progressive Era"))

        # BOOST_CIVIC_FEUDALISM should now be accessible
        self.assertTrue(self.can_reach_location("BOOST_CIVIC_FEUDALISM"))

        # But BOOST_CIVIC_URBANIZATION still requires Industrial era (needs 5 total)
        self.assertFalse(self.can_reach_location("BOOST_CIVIC_URBANIZATION"))

        # Collect 3 more Progressive Era items to reach Industrial
        self.collect_by_name(["Progressive Era", "Progressive Era", "Progressive Era"])

        # Now BOOST_CIVIC_URBANIZATION should be accessible
        self.assertTrue(self.can_reach_location("BOOST_CIVIC_URBANIZATION"))
