from argparse import Namespace

from BaseClasses import PlandoOptions
from Generate import handle_option
from . import L2ACTestBase
from ..Options import CustomItemPool


class TestEmpty(L2ACTestBase):
    options = {
        "custom_item_pool": {},
    }

    def test_empty(self) -> None:
        self.assertEqual(0, len(self.get_items_by_name("Dekar blade")))


class TestINeedDekarBlade(L2ACTestBase):
    options = {
        "custom_item_pool": {
            "Dekar blade": 2,
        },
    }

    def test_i_need_dekar_blade(self) -> None:
        self.assertEqual(2, len(self.get_items_by_name("Dekar blade")))


class TestVerifyCount(L2ACTestBase):
    auto_construct = False
    options = {
        "custom_item_pool": {
            "Dekar blade": 26,
        },
    }

    def test_verify_count(self) -> None:
        self.assertRaisesRegex(ValueError,
                               "Number of items in custom_item_pool \\(26\\) is greater than blue_chest_count \\(25\\)",
                               lambda: self.world_setup())


class TestVerifyItemName(L2ACTestBase):
    auto_construct = False
    options = {
        "custom_item_pool": {
            "The car blade": 2,
        },
    }

    def test_verify_item_name(self) -> None:
        self.assertRaisesRegex(Exception,
                               "Item 'The car blade' from option 'CustomItemPool\\(The car blade: 2\\)' is not a "
                               "valid item name from 'Lufia II Ancient Cave'\\. Did you mean 'Dekar blade'",
                               lambda: handle_option(Namespace(game="Lufia II Ancient Cave", name="Player"),
                                                     self.options, "custom_item_pool", CustomItemPool,
                                                     PlandoOptions(0)))
