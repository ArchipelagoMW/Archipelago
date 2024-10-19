from BaseClasses import ItemClassification
from Fill import distribute_items_restrictive
from ..Enum import CivVICheckType
from . import CivVITestBase


class TestStartingHints(CivVITestBase):
    run_default_tests = False  # type: ignore
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "pre_hint_items": {"Progression", "Useful", "Filler"},
    }

    def test_all_tech_civic_items_are_hinted_default(self) -> None:
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        self.world.post_fill()
        start_location_hints = self.world.options.start_location_hints.value
        for location_name, location_data in self.world.location_table.items():
            if location_data.location_type == CivVICheckType.CIVIC or location_data.location_type == CivVICheckType.TECH:
                self.assertIn(location_name, start_location_hints)
            else:
                self.assertNotIn(location_name, start_location_hints)


class TestOnlyProgressionItemsHinted(CivVITestBase):
    run_default_tests = False  # type: ignore
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "pre_hint_items": {"Progression"},
    }

    def test_only_progression_items_are_hinted(self) -> None:
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        self.world.post_fill()
        start_location_hints = self.world.options.start_location_hints.value
        self.assertTrue(len(start_location_hints) > 0)
        for hint in start_location_hints:
            location_data = self.world.get_location(hint)
            if location_data.item:
                self.assertTrue(location_data.item.classification == ItemClassification.progression)
            else:
                self.assertTrue(False, "Location has no item")


class TestNoJunkItemsHinted(CivVITestBase):
    run_default_tests = False  # type: ignore
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "pre_hint_items": {"Progression", "Useful"},
    }

    def test_no_junk_items_are_hinted(self) -> None:
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        self.world.post_fill()
        start_location_hints = self.world.options.start_location_hints.value
        self.assertTrue(len(start_location_hints) > 0)
        for hint in start_location_hints:
            location_data = self.world.get_location(hint)
            if location_data.item:
                self.assertTrue(location_data.item.classification == ItemClassification.progression or location_data.item.classification == ItemClassification.useful)
            else:
                self.assertTrue(False, "Location has no item")


class TestNoItemsHinted(CivVITestBase):
    run_default_tests = False  # type: ignore
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "death_link": "true",
        "death_link_effect": "unit_killed",
        "progressive_districts": "true",
        "pre_hint_items": {},
    }

    def test_no_items_are_hinted(self) -> None:
        self.world_setup()
        distribute_items_restrictive(self.multiworld)
        self.world.post_fill()
        start_location_hints = self.world.options.start_location_hints.value
        self.assertEqual(len(start_location_hints), 0)
