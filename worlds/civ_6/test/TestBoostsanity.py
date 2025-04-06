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
