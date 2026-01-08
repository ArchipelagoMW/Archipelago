from BaseClasses import ItemClassification

from . import CrossCodeTestBase
from ..types.items import CrossCodeItem
from ..types.condition import *
from ..types.locations import CrossCodeLocation

class TestItemConditions(CrossCodeTestBase):
    def assertIsValidItemCondition(self, cond: ItemCondition):
        """
        This method provides an *exhaustive* check as to whether an item condition is valid, using a wide variety of
        methods.

        This may take a while, but I deem each step worth it as they test different aspects of whether the condition is
        well-formed.
        """

        # first check if this item's data can be loaded.
        try:
            item_data = self.world_data.items_by_full_name[cond.item_name]
        except:
            self.fail(f"ItemData could not be loaded for item with full name {cond.item_name}")

        # next, make sure the item is progressive
        self.assertEqual(
            item_data.item.classification,
            ItemClassification.progression,
            f"ItemData for item with full name {cond.item_name} is not progressive"
        )

        # check if the multiworld actually contains all the items this condition wants.
        self.assertGreaterEqual(
            self.multiworld.get_all_state(True).count(cond.item_name, self.player),
            item_data.amount,
            f"Cannot find {item_data.amount} instances of {cond.item_name} in item pool"
        )

    def assertIsValidCondition(self, cond: Condition):
        if isinstance(cond, ItemCondition):
            self.assertIsValidItemCondition(cond)

    def assertIsValidConditionList(self, conds: list[Condition]):
        for cond in conds:
            self.assertIsValidCondition(cond)

    def test_conditions_on_locations(self):
        for name, location in self.multiworld.regions.location_cache[self.player].items():
            if location.address == None:
                continue
            if not isinstance(location, CrossCodeLocation):
                self.fail(f"location {location.name} is not a CrossCodeLocation")
            cond = location.data.access.cond
            if cond is not None:
                self.assertIsValidConditionList(cond)

    # def test_conditions_on_regions(self):
    #     for mode in modes:
    #         for connection in region_packs[mode].region_connections:
    #             for item, _ in connection.cond.items:
    #                 assert(item in single_items_dict)

'''class TestLocationConditions(CrossCodeTestBase):
    auto_construct = False
    locations_dict = {location.name: location for location in [*locations_data, *events_data]}

    def test_location_conditions_on_locations(self):
        for data in locations_data:
            for location in data.cond.locations:
                assert(location in self.locations_dict)

    def test_region_conditions_on_locations(self):
        for data in locations_data:
            for mode, regions in data.cond.regions.items():
                for region in regions:
                    assert(region in region_packs[mode].region_list)

    def test_location_conditions_on_regions(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                for location in connection.cond.locations:
                    assert(location in self.locations_dict)

    def test_region_conditions_on_regions(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                if mode not in connection.cond.regions:
                    continue
                for region in connection.cond.regions[mode]:
                    assert(region in region_packs[mode].region_list)
'''
