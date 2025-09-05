from ..bases import SVTestBase
from ... import options
from ...options import BundleRandomization
from ...strings.bundle_names import BundleName


class TestBundlesLogic(SVTestBase):
    options = {
        options.BundleRandomization: BundleRandomization.option_vanilla,
        options.BundlePrice: options.BundlePrice.default,
    }

    def test_vault_2500g_bundle(self):
        self.assert_cannot_reach_location("2,500g Bundle")

        self.collect_lots_of_money()
        self.assert_can_reach_location("2,500g Bundle")


class TestRemixedBundlesLogic(SVTestBase):
    options = {
        options.BundleRandomization: BundleRandomization.option_remixed,
        options.BundlePrice: options.BundlePrice.default,
        options.BundlePlando: frozenset({BundleName.sticky})
    }

    def test_sticky_bundle_has_grind_rules(self):
        self.assert_cannot_reach_location("Sticky Bundle")

        self.collect_all_the_money()
        self.assert_can_reach_location("Sticky Bundle")


class TestRaccoonBundlesLogic(SVTestBase):
    options = {
        options.BundleRandomization: BundleRandomization.option_vanilla,
        options.BundlePrice: options.BundlePrice.option_normal,
        options.Craftsanity: options.Craftsanity.option_all,
    }
    seed = 2  # Magic seed that does what I want. Might need to get changed if we change the randomness behavior of raccoon bundles

    def test_raccoon_bundles_rely_on_previous_ones(self):
        self.collect("Progressive Raccoon", 6)
        self.collect("Progressive Mine Elevator", 24)
        self.collect("Mining Level", 12)
        self.collect("Combat Level", 12)
        self.collect("Progressive Axe", 4)
        self.collect("Progressive Pickaxe", 4)
        self.collect("Progressive Weapon", 4)
        self.collect("Dehydrator Recipe")
        self.collect("Mushroom Boxes")
        self.collect("Progressive Fishing Rod", 4)
        self.collect("Fishing Level", 10)
        self.collect("Furnace Recipe")

        # The first raccoon bundle is a fishing one
        self.assert_cannot_reach_location("Raccoon Request 1")
        # The third raccoon bundle is a foraging one
        self.assert_cannot_reach_location("Raccoon Request 3")

        self.collect("Fish Smoker Recipe")

        self.assert_can_reach_location("Raccoon Request 1")
        self.assert_can_reach_location("Raccoon Request 3")
