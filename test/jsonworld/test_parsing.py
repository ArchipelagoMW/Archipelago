from unittest import TestCase
from BaseClasses import ItemClassification
from rule_builder.rules import HasAll, Or
from worlds import json_world


class TestItemDatapackage(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"item_name_to_id": "explicit"},
            "item_name_to_id": {
                "item": 1
            }
        }
        parsed = json_world.build_item_datapackage(data)
        self.assertEqual(parsed, {"item": 1})


class TestLocationDatapackage(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"location_name_to_id": "explicit"},
            "location_name_to_id": {
                "location": 1
            }
        }
        parsed = json_world.build_location_datapackage(data)
        self.assertEqual(parsed, {"location": 1})


class TestItemGroups(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"item_name_groups": "explicit"},
            "item_name_groups": {
                "group": ["item"]
            }
        }
        parsed = json_world.build_item_groups(data)
        self.assertEqual(parsed, {"group": {"item"}})

    def test_empty(self):
        data = {
            "formats": {"item_name_groups": "explicit"},
        }
        parsed = json_world.build_item_groups(data)
        self.assertEqual(parsed, {})


class TestLocationGroups(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"location_name_groups": "explicit"},
            "location_name_groups": {
                "group": ["location"]
            }
        }
        parsed = json_world.build_location_groups(data)
        self.assertEqual(parsed, {"group": {"location"}})

    def test_empty(self):
        data = {
            "formats": {"location_name_groups": "explicit"},
        }
        parsed = json_world.build_location_groups(data)
        self.assertEqual(parsed, {})


class TestRule(TestCase):
    def test_dnf(self):
        data = [["one", "two"], ["three"]]
        parsed = json_world.create_rule(data, rule_format="dnf_items")
        self.assertEqual(parsed, Or(HasAll("one", "two"), HasAll("three")))

    def test_serialised(self):
        data = Or(HasAll("one", "two"), HasAll("three")).to_dict()
        parsed = json_world.create_rule(data, rule_format="serialized")
        self.assertEqual(parsed, Or(HasAll("one", "two"), HasAll("three")))


class TestRegionData(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"region_map": "explicit"},
            "region_map": {
                "Main": {
                    "Treehouse": None
                }
            }
        }
        region_list, region_map = json_world.build_region_data(data)
        with self.subTest("region_list"):
            self.assertEqual(region_list, ["Main", "Treehouse"])
        with self.subTest("region_map"):
            self.assertEqual(region_map, {"Main": {"Treehouse": None}})


class TestLocationMap(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"location_map": "explicit"},
            "location_map": {
                "Treehouse": {
                    "Open Treehouse": None
                }
            }
        }
        parsed = json_world.build_location_map(data)
        self.assertEqual(parsed, {"Treehouse": {"Open Treehouse": None}})


class TestEventMap(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"event_map": "explicit"},
            "event_map": {
                "Treehouse": [
                    ["Treehouse Orb", "Find Orb", None]
                ]
            }
        }
        parsed = json_world.build_event_map(data)
        self.assertEqual(parsed, {"Treehouse": [("Treehouse Orb", "Find Orb", None,)]})

    def test_empty(self):
        data = {
            "formats": {}
        }
        parsed = json_world.build_event_map(data)
        self.assertEqual(parsed, {})


class TestItemList(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"item_list": "explicit"},
            "item_list": [
                "item",
                "item"
            ]
        }
        parsed = json_world.build_item_list(data)
        self.assertEqual(parsed, ["item", "item"])

    def test_counter(self):
        data = {
            "formats": {"item_list": "counter"},
            "item_count": {
                "item": 2
            }
        }
        parsed = json_world.build_item_list(data)
        self.assertEqual(parsed, ["item", "item"])


class TestCompletionRule(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"rule": "dnf_items"},
            "completion_rule": [["one", "two"], ["three"]]
        }
        parsed = json_world.build_completion_rule(data)
        self.assertEqual(parsed, Or(HasAll("one", "two"), HasAll("three")))

    def test_empty(self):
        data = {
            "formats": {"rule": "dnf_items"},
            "completion_rule": None
        }
        with self.assertRaises(Exception):
            parsed = json_world.build_completion_rule(data)


class TestClassificationLookup(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"classification_lookup": "explicit"},
            "classification_lookup": {
                "item": "progression"
            }
        }
        parsed = json_world.build_classification_lookup(data)
        self.assertEqual(parsed, {"item": ItemClassification.progression})

    def test_reverse_lookup(self):
        data = {
            "formats": {"classification_lookup": "reverse_lookup"},
            "classification_lookup": {
                "progression": [
                    "item"
                ]
            }
        }
        parsed = json_world.build_classification_lookup(data)
        self.assertEqual(parsed, {"item": ItemClassification.progression})


class TestFillerWeights(TestCase):
    def test_explicit(self):
        data = {
            "formats": {"filler_weights": "explicit"},
            "filler_weights": {
                "item": 1
            }
        }
        parsed = json_world.build_filler_weights(data)
        self.assertEqual(parsed, {"item": 1})

    def test_single(self):
        data = {
            "formats": {"filler_weights": "single"},
            "filler_item": "item"
        }
        parsed = json_world.build_filler_weights(data)
        self.assertEqual(parsed, {"item": 1})
