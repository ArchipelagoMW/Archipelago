import unittest

from BaseClasses import ItemClassification
from ..assertion import get_all_location_names
from ..bases import skip_long_tests, SVTestCase, solo_multiworld
from ..options.presets import setting_mins_and_maxes, allsanity_no_mods_7_x_x, get_minsanity_options, default_7_x_x
from ...items import Group, item_table
from ...items.item_data import FILLER_GROUPS

if skip_long_tests():
    raise unittest.SkipTest("Long tests disabled")


def get_real_item_count(multiworld):
    number_items = len([item for item in multiworld.itempool
                        if all(filler_group not in item_table[item.name].groups for filler_group in FILLER_GROUPS) and Group.TRAP not in item_table[
                            item.name].groups and (item.classification & ItemClassification.progression)])
    return number_items


class TestCountsPerSetting(SVTestCase):

    def test_items_locations_counts_per_setting_with_ginger_island(self):
        option_mins_and_maxes = setting_mins_and_maxes()

        for name in option_mins_and_maxes:
            values = option_mins_and_maxes[name]
            if not isinstance(values, list):
                continue
            with self.subTest(f"{name}"):
                highest_variance_items = -1
                highest_variance_locations = -1
                for preset in [allsanity_no_mods_7_x_x, default_7_x_x, get_minsanity_options]:
                    lowest_items = 9999
                    lowest_locations = 9999
                    highest_items = -1
                    highest_locations = -1
                    for value in values:
                        world_options = preset()
                        world_options[name] = value
                        with solo_multiworld(world_options, world_caching=False) as (multiworld, _):
                            num_locations = len([loc for loc in get_all_location_names(multiworld) if not loc.startswith("Traveling Merchant")])
                            num_items = get_real_item_count(multiworld)
                            if num_items > highest_items:
                                highest_items = num_items
                            if num_items < lowest_items:
                                lowest_items = num_items
                            if num_locations > highest_locations:
                                highest_locations = num_locations
                            if num_locations < lowest_locations:
                                lowest_locations = num_locations

                    variance_items = highest_items - lowest_items
                    variance_locations = highest_locations - lowest_locations
                    if variance_locations > highest_variance_locations:
                        highest_variance_locations = variance_locations
                    if variance_items > highest_variance_items:
                        highest_variance_items = variance_items
                if highest_variance_locations > highest_variance_items:
                    print(f"Options `{name}` can create up to {highest_variance_locations - highest_variance_items} filler ({highest_variance_locations} locations and up to {highest_variance_items} items)")
                if highest_variance_locations < highest_variance_items:
                    print(f"Options `{name}` can create up to {highest_variance_items - highest_variance_locations} orphan ({highest_variance_locations} locations and up to {highest_variance_items} items)")