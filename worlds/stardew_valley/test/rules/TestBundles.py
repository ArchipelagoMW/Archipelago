from ... import options
from ...options import BundleRandomization
from ...test import SVTestBase


class TestBundlesLogic(SVTestBase):
    options = {
        options.BundleRandomization: BundleRandomization.option_vanilla,
        options.BundlePrice: options.BundlePrice.default,
    }

    def test_vault_2500g_bundle(self):
        self.assertFalse(self.world.logic.region.can_reach_location("2,500g Bundle")(self.multiworld.state))

        self.collect_lots_of_money()
        self.assertTrue(self.world.logic.region.can_reach_location("2,500g Bundle")(self.multiworld.state))
