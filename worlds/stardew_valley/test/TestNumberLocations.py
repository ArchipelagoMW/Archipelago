from . import SVTestBase
from .options.presets import default_6_x_x, allsanity_no_mods_6_x_x, allsanity_mods_6_x_x_exclude_disabled, get_minsanity_options, \
    minimal_locations_maximal_items, minimal_locations_maximal_items_with_island
from .. import location_table
from ..items import Group, item_table


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
                            if Group.RESOURCE_PACK not in item_table[item.name].groups and Group.TRAP not in item_table[item.name].groups])
        print(f"Stardew Valley - Minimum Locations: {number_locations}, Maximum Items: {number_items} [ISLAND EXCLUDED]")
        self.assertGreaterEqual(number_locations, number_items)


class TestMinLocationAndMaxItemWithIsland(SVTestBase):
    options = minimal_locations_maximal_items_with_island()

    def test_minimal_location_maximal_items_with_island_still_valid(self):
        valid_locations = self.get_real_locations()
        number_locations = len(valid_locations)
        number_items = len([item for item in self.multiworld.itempool
                            if Group.RESOURCE_PACK not in item_table[item.name].groups and Group.TRAP not in item_table[item.name].groups])
        print(f"Stardew Valley - Minimum Locations: {number_locations}, Maximum Items: {number_items} [ISLAND INCLUDED]")
        self.assertGreaterEqual(number_locations, number_items)


class TestMinSanityHasAllExpectedLocations(SVTestBase):
    options = get_minsanity_options()

    def test_minsanity_has_fewer_than_locations(self):
        expected_locations = 85
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        print(f"Stardew Valley - Minsanity Locations: {number_locations}")
        self.assertLessEqual(number_locations, expected_locations)
        if number_locations != expected_locations:
            print(f"\tDisappeared Locations Detected!"
                  f"\n\tPlease update test_minsanity_has_fewer_than_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestDefaultSettingsHasAllExpectedLocations(SVTestBase):
    options = default_6_x_x()

    def test_default_settings_has_exactly_locations(self):
        expected_locations = 491
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        print(f"Stardew Valley - Default options locations: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_default_settings_has_exactly_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestAllSanitySettingsHasAllExpectedLocations(SVTestBase):
    options = allsanity_no_mods_6_x_x()

    def test_allsanity_without_mods_has_at_least_locations(self):
        expected_locations = 2256
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
    options = allsanity_mods_6_x_x_exclude_disabled()

    def test_allsanity_with_mods_has_at_least_locations(self):
        expected_locations = 2908
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        print(f"Stardew Valley - Allsanity Locations with all mods: {number_locations}")
        self.assertGreaterEqual(number_locations, expected_locations)
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_with_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")
