import itertools
import math
import unittest


from BaseClasses import ItemClassification, MultiWorld
from .. import ItemData, StardewValleyWorld
from ..items import Group, ResourcePackData, item_table


class TestItems(unittest.TestCase):
    def test_can_create_item_of_resource_pack(self):
        item_name = "Resource Pack: 500 Money"

        multi_world = MultiWorld(1)
        multi_world.game[1] = "Stardew Valley"
        multi_world.player_name = {1: "Tester"}
        world = StardewValleyWorld(multi_world, 1)
        item = world.create_item(item_name)

        assert item.name == item_name

    def test_items_table_footprint_is_between_717000_and_727000(self):
        item_with_lowest_id = min((item for item in item_table.values() if item.code is not None), key=lambda x: x.code)
        item_with_highest_id = max((item for item in item_table.values() if item.code is not None),
                                   key=lambda x: x.code)

        assert item_with_lowest_id.code >= 717000
        assert item_with_highest_id.code < 727000


class TestResourcePacks:
    def test_can_transform_resource_pack_data_into_idem_data(self):
        resource_pack = ResourcePackData("item name", 1, 1, ItemClassification.filler, frozenset())

        items = resource_pack.as_item_data(itertools.count())

        assert ItemData(0, "Resource Pack: 1 item name", ItemClassification.filler, {Group.RESOURCE_PACK}) in items
        assert ItemData(1, "Resource Pack: 2 item name", ItemClassification.filler, {Group.RESOURCE_PACK}) in items
        assert len(items) == 2

    def test_when_scale_quantity_then_generate_a_possible_quantity_from_minimal_scaling_to_double(self):
        resource_pack = ResourcePackData("item name", default_amount=4, scaling_factor=2)

        quantities = resource_pack.scale_quantity.items()

        assert (50, 2) in quantities
        assert (100, 4) in quantities
        assert (150, 6) in quantities
        assert (200, 8) in quantities
        assert len(quantities) == (4 / 2) * 2

    def test_given_scaling_not_multiple_of_default_amount_when_scale_quantity_then_double_is_added_at_200_scaling(self):
        resource_pack = ResourcePackData("item name", default_amount=5, scaling_factor=3)

        quantities = resource_pack.scale_quantity.items()

        assert (40, 2) in quantities
        assert (100, 5) in quantities
        assert (160, 8) in quantities
        assert (200, 10) in quantities
        assert len(quantities) == math.ceil(5 / 3) * 2

    def test_given_large_default_amount_multiple_of_scaling_factor_when_scale_quantity_then_scaled_amount_multiple(self):
        resource_pack = ResourcePackData("item name", default_amount=500, scaling_factor=50)

        quantities = resource_pack.scale_quantity.items()

        assert (10, 50) in quantities
        assert (20, 100) in quantities
        assert (30, 150) in quantities
        assert (40, 200) in quantities
        assert (50, 250) in quantities
        assert (60, 300) in quantities
        assert (70, 350) in quantities
        assert (80, 400) in quantities
        assert (90, 450) in quantities
        assert (100, 500) in quantities
        assert (110, 550) in quantities
        assert (120, 600) in quantities
        assert (130, 650) in quantities
        assert (140, 700) in quantities
        assert (150, 750) in quantities
        assert (160, 800) in quantities
        assert (170, 850) in quantities
        assert (180, 900) in quantities
        assert (190, 950) in quantities
        assert (200, 1000) in quantities
        assert len(quantities) == math.ceil(500 / 50) * 2

    def test_given_smallest_multiplier_possible_when_generate_resource_pack_name_then_quantity_is_not_0(self):
        resource_pack = ResourcePackData("item name", default_amount=10, scaling_factor=5)

        name = resource_pack.create_name_from_multiplier(1)

        assert name == "Resource Pack: 5 item name"
