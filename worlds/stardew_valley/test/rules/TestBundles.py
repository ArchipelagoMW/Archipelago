from ... import options
from ...options import BundleRandomization
from ...strings.bundle_names import BundleName
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


class TestRemixedBundlesLogic(SVTestBase):
    options = {
        options.BundleRandomization: BundleRandomization.option_remixed,
        options.BundlePrice: options.BundlePrice.default,
        options.BundlePlando: frozenset({BundleName.sticky})
    }

    def test_sticky_bundle_has_grind_rules(self):
        self.assertFalse(self.world.logic.region.can_reach_location("Sticky Bundle")(self.multiworld.state))

        self.collect_all_the_money()
        self.assertTrue(self.world.logic.region.can_reach_location("Sticky Bundle")(self.multiworld.state))
