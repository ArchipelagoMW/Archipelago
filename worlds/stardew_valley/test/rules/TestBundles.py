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


class TestRaccoonBundlesLogic(SVTestBase):
    options = {
        options.BundleRandomization: BundleRandomization.option_vanilla,
        options.BundlePrice: options.BundlePrice.option_normal,
        options.Craftsanity: options.Craftsanity.option_all,
    }
    seed = 2  # Magic seed that does what I want. Might need to get changed if we change the randomness behavior of raccoon bundles

    def test_raccoon_bundles_rely_on_previous_ones(self):
        # The first raccoon bundle is a fishing one
        raccoon_rule_1 = self.world.logic.region.can_reach_location("Raccoon Request 1")

        # The 3th raccoon bundle is a foraging one
        raccoon_rule_3 = self.world.logic.region.can_reach_location("Raccoon Request 3")
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

        self.assertFalse(raccoon_rule_1(self.multiworld.state))
        self.assertFalse(raccoon_rule_3(self.multiworld.state))

        self.collect("Fish Smoker Recipe")

        self.assertTrue(raccoon_rule_1(self.multiworld.state))
        self.assertTrue(raccoon_rule_3(self.multiworld.state))
