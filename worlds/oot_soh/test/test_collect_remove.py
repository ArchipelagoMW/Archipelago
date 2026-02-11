from .. import SohWorld
from ..Items import progressive_items, Items
from .bases import SohTestBase


class TestCollectRemoveAllOff(SohTestBase):
    options = {"shuffle_childs_wallet": False, "shuffle_swim": False, "shuffle_deku_stick_bag": False,
               "shuffle_deku_nut_bag": False, "bombchu_bag": "none", "shuffle_ocarinas": True}
    world: SohWorld
    optional_prog_item_set = {Items.PROGRESSIVE_SCALE, Items.PROGRESSIVE_WALLET, Items.PROGRESSIVE_STICK_CAPACITY,
                              Items.PROGRESSIVE_NUT_CAPACITY, Items.BOMBCHU_BAG}

    def test_single_of_each(self):
        """
        Checking if we collect 1 of each progressive item, or 0 in the case of ones that aren't shuffled, that we have
        the first "rank" of each item.
        """
        for item_name, prog_items in progressive_items.items():
            if item_name not in self.optional_prog_item_set:
                item = SohWorld.create_item(self.world, item_name)
                self.collect(item)
            self.assertTrue(self.multiworld.state.has(prog_items[0], self.player),
                            f"Failed for {item_name}, we do not have {prog_items[0]}")
            if len(prog_items) > 1:
                self.assertFalse(self.multiworld.state.has(prog_items[1], self.player))

    def test_one_collect_of_optional_ones(self):
        """
        Checking if we have rank 2 of the ones that are not shuffled
        """
        for item_name, prog_items in progressive_items.items():
            if item_name in self.optional_prog_item_set:
                item = SohWorld.create_item(self.world, item_name)
                self.collect(item)
                index_to_check = 1
                if len(prog_items) == 1:
                    # if there's only 1 item in the list, we just want to make sure that it doesn't break
                    index_to_check = 0
                self.assertTrue(self.multiworld.state.has(prog_items[index_to_check], self.player))
                if len(prog_items) > 1:
                    self.assertFalse(self.multiworld.state.has(prog_items[index_to_check + 1], self.player))

    def test_full_collect_and_remove_of_all(self):
        """
        Checking that we have every one of the non-progressive event versions of the items after collecting enough.
        Easy way to do that: just collect 4 of each progressive item.
        """
        full_list_of_items = []
        for item_name, prog_items in progressive_items.items():
            for _ in range(4):
                item = SohWorld.create_item(self.world, item_name)
                full_list_of_items.append(item)
                self.collect(item)

        # check that we have all the non-progressive event versions of items
        for prog_items in progressive_items.values():
            for i in range(len(prog_items)):
                self.assertTrue(self.multiworld.state.has(prog_items[i], self.player))

        # remove the progressive items
        for item in full_list_of_items:
            self.multiworld.state.remove(item)

        for item_name, prog_items in progressive_items.items():
            for i in range(len(prog_items)):
                if i == 0 and item_name in self.optional_prog_item_set:
                    self.assertTrue(self.multiworld.state.has(prog_items[i], self.player))
                else:
                    self.assertFalse(self.multiworld.state.has(prog_items[i], self.player))


class TestCollectRemoveAllOn(SohTestBase):
    options = {"shuffle_childs_wallet": True, "shuffle_swim": True, "shuffle_deku_stick_bag": True,
               "shuffle_deku_nut_bag": True, "bombchu_bag": "single_bag", "shuffle_ocarinas": True}
    world: SohWorld

    def test_single_of_each(self):
        """
        Checking if we collect 1 of each progressive item that we have the first "rank" of each item.
        """
        for item_name, prog_items in progressive_items.items():
            item = SohWorld.create_item(self.world, item_name)
            self.collect(item)
            self.assertTrue(self.multiworld.state.has(prog_items[0], self.player),
                            f"Failed for {item_name}, we do not have {prog_items[0]}")
            if len(prog_items) > 1:
                self.assertFalse(self.multiworld.state.has(prog_items[1], self.player))

    def test_full_collect_and_remove_of_all(self):
        """
        Checking that we have every one of the non-progressive event versions of the items after collecting enough.
        Easy way to do that: just collect 4 of each progressive item.
        """
        full_list_of_items = []
        for item_name, prog_items in progressive_items.items():
            for _ in range(4):
                item = SohWorld.create_item(self.world, item_name)
                full_list_of_items.append(item)
                self.collect(item)

        # check that we have all the non-progressive event versions of items
        for prog_items in progressive_items.values():
            for i in range(len(prog_items)):
                self.assertTrue(self.multiworld.state.has(prog_items[i], self.player))

        # remove the progressive items
        for item in full_list_of_items:
            self.multiworld.state.remove(item)

        for item_name, prog_items in progressive_items.items():
            for i in range(len(prog_items)):
                self.assertFalse(self.multiworld.state.has(prog_items[i], self.player))
