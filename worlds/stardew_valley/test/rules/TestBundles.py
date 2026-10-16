from ... import SeasonRandomization, StartWithoutOptionName, options
from ...options import BundleRandomization, StartWithout
from ...strings.bundle_names import BundleName
from ..bases import SVTestBase


class TestBundlesLogic(SVTestBase):
    options = {
        StartWithout.internal_name: frozenset({StartWithoutOptionName.community_center, StartWithoutOptionName.buildings}),
        options.SeasonRandomization: SeasonRandomization.option_disabled,
        options.BundleRandomization: BundleRandomization.option_vanilla,
        options.BundlePrice: options.BundlePrice.default,
    }

    def test_vault_2500g_bundle(self):
        self.assert_cannot_reach_location("2,500g Bundle")

        self.collect("Community Center Key")
        self.collect("Forest Magic")
        self.assert_cannot_reach_location("2,500g Bundle")
        self.collect_lots_of_money()
        self.assert_can_reach_location("2,500g Bundle")


class TestRemixedBundlesLogic(SVTestBase):
    options = {
        StartWithout.internal_name: frozenset({StartWithoutOptionName.community_center}),
        options.SeasonRandomization: SeasonRandomization.option_disabled,
        options.BundleRandomization: BundleRandomization.option_remixed,
        options.BundlePrice: options.BundlePrice.default,
        options.BundleWhitelist: frozenset({BundleName.sticky})
    }

    def test_sticky_bundle_has_grind_rules(self):
        self.assert_cannot_reach_location("Sticky Bundle")

        self.collect("Community Center Key")
        self.collect("Forest Magic")
        self.assert_cannot_reach_location("Sticky Bundle")
        self.collect_all_the_money()
        self.assert_can_reach_location("Sticky Bundle")


class TestRaccoonBundlesLogic(SVTestBase):
    options = {
        options.SeasonRandomization: SeasonRandomization.option_disabled,
        options.BundleRandomization: BundleRandomization.option_vanilla,
        options.BundlePrice: options.BundlePrice.option_normal,
        options.Craftsanity: options.Craftsanity.option_all,
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
    }

    def test_raccoon_bundles_dont_rely_on_previous_ones(self):
        self.collect("Forest Magic")
        self.collect("Progressive Raccoon", 8)
        self.collect("Progressive Mine Elevator", 24)
        self.collect("Mining Level", 12)
        self.collect("Combat Level", 12)
        self.collect("Progressive Axe", 4)
        self.collect("Progressive Pickaxe", 4)
        self.collect("Progressive Weapon", 4)
        self.collect("Progressive Fishing Rod", 4)
        self.collect("Fishing Level", 10)
        self.collect("Progressive Coop", 3)
        self.collect("Furnace Recipe")
        self.collect("Dehydrator Recipe")
        self.collect("Mushroom Boxes")

        # The first raccoon bundle is a fishing one
        self.assert_cannot_reach_location("Raccoon Request 1")
        # The third raccoon bundle is a foraging one
        self.assert_can_reach_location("Raccoon Request 3")

        self.collect("Fish Smoker Recipe")

        self.assert_can_reach_location("Raccoon Request 1")
        self.assert_can_reach_location("Raccoon Request 3")
