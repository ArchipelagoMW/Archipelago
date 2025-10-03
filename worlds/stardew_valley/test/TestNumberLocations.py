from BaseClasses import ItemClassification
from .bases import SVTestBase
from .options.presets import default_7_x_x, allsanity_no_mods_7_x_x, get_minsanity_options, \
    minimal_locations_maximal_items, minimal_locations_maximal_items_with_island, allsanity_mods_7_x_x_exclude_disabled
from .. import location_table
from ..items import Group, item_table
from ..items.item_data import FILLER_GROUPS


class TestLocationGeneration(SVTestBase):

    def test_all_location_created_are_in_location_table(self):
        for location in self.get_real_locations():
            self.assertIn(location.name, location_table)


class TestMinLocationAndMaxItem(SVTestBase):
    options = minimal_locations_maximal_items()

    def test_minimal_location_maximal_items_still_valid(self):
        valid_locations = self.get_real_locations()
        number_locations = len(valid_locations)
        number_items = len([item for item in self.multiworld.itempool
                            if all(filler_group not in item_table[item.name].groups for filler_group in FILLER_GROUPS) and Group.TRAP not in item_table[item.name].groups])
        print(f"Stardew Valley - Minimum Locations: {number_locations}, Maximum Items: {number_items} [ISLAND EXCLUDED]")
        self.assertGreaterEqual(number_locations, number_items)


class TestMinLocationAndMaxItemWithIsland(SVTestBase):
    options = minimal_locations_maximal_items_with_island()

    def test_minimal_location_maximal_items_with_island_still_valid(self):
        valid_locations = self.get_real_locations()
        number_locations = len(valid_locations)
        number_items = len([item for item in self.multiworld.itempool
                            if all(filler_group not in item_table[item.name].groups for filler_group in FILLER_GROUPS) and Group.TRAP not in item_table[item.name].groups and (item.classification & ItemClassification.progression)])
        print(f"Stardew Valley - Minimum Locations: {number_locations}, Maximum Items: {number_items} [ISLAND INCLUDED]")
        self.assertGreaterEqual(number_locations, number_items)


class TestMinSanityHasAllExpectedLocations(SVTestBase):
    options = get_minsanity_options()

    def test_minsanity_has_few_locations(self):
        fewest_allowed_locations = 90
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        print(f"Stardew Valley - Minsanity Locations: {number_locations}")
        self.assertGreaterEqual(number_locations, fewest_allowed_locations)
        if number_locations < fewest_allowed_locations:
            print(f"\tMinsanity too many locations detected"
                  f"\n\tPlease update test_minsanity_has_fewer_than_locations"
                  f"\n\t\tMinimum: {fewest_allowed_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestDefaultSettingsHasAllExpectedLocations(SVTestBase):
    options = default_7_x_x()

    def test_default_settings_has_exactly_locations(self):
        expected_locations = 475
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        print(f"Stardew Valley - Default options locations: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_default_settings_has_exactly_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestAllSanitySettingsHasAllExpectedLocations(SVTestBase):
    options = allsanity_no_mods_7_x_x()

    def test_allsanity_without_mods_has_at_least_locations(self):
        expected_locations = 2821
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        print(f"Stardew Valley - Allsanity Locations without mods: {number_locations}")
        self.assertGreaterEqual(number_locations, expected_locations)
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_without_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestAllSanityWithModsSettingsHasAllExpectedLocations(SVTestBase):
    options = allsanity_mods_7_x_x_exclude_disabled()

    def test_allsanity_with_mods_has_at_least_locations(self):
        expected_locations = 3189  # It was before disabling SVE 3473
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        print(f"Stardew Valley - Allsanity Locations with all mods: {number_locations}")
        self.assertGreaterEqual(number_locations, expected_locations)
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_with_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")
