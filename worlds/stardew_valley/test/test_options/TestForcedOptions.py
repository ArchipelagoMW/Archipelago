import itertools
import unittest

import Options as ap_options
from ...options import options
from ...options.forced_options import force_change_options_if_incompatible
from ...test.options.utils import fill_dataclass_with_default


class TestGoalsRequiringAllLocationsOverrideAccessibility(unittest.TestCase):

    def test_given_goal_requiring_all_locations_when_generate_then_accessibility_is_forced_to_full(self):
        """There is a bug with the current victory condition of the perfection goal that can create unwinnable seeds if the accessibility is set to minimal and
        the world gets flooded with progression items through plando. This will increase the amount of collected progression items pass the total amount
        calculated for the world when creating the item pool. This will cause the victory condition to be met before all locations are collected, so some could
        be left inaccessible, which in practice will make the seed unwinnable.
        """

        for goal in [options.Goal.option_perfection, options.Goal.option_allsanity]:
            for accessibility in ap_options.Accessibility.options.keys():
                with self.subTest(f"Goal: {options.Goal.get_option_name(goal)} Accessibility: {accessibility}"):
                    world_options = fill_dataclass_with_default({
                        options.Goal: goal,
                        "accessibility": accessibility
                    })

                    force_change_options_if_incompatible(world_options, 1, "Tester")

                    self.assertEqual(world_options.accessibility.value, ap_options.Accessibility.option_full)


class TestGingerIslandRelatedGoalsOverrideGingerIslandExclusion(unittest.TestCase):

    def test_given_island_related_goal_when_generate_then_override_exclude_ginger_island(self):
        for goal in [options.Goal.option_greatest_walnut_hunter, options.Goal.option_perfection]:
            for exclude_island in options.ExcludeGingerIsland.options:
                with self.subTest(f"Goal: {options.Goal.get_option_name(goal)} Exclude Ginger Island: {exclude_island}"):
                    world_options = fill_dataclass_with_default({
                        options.Goal: goal,
                        options.ExcludeGingerIsland: exclude_island
                    })

                    force_change_options_if_incompatible(world_options, 1, "Tester")

                    self.assertEqual(world_options.exclude_ginger_island.value, options.ExcludeGingerIsland.option_false)


class TestGingerIslandExclusionOverridesWalnutsanity(unittest.TestCase):

    def test_given_ginger_island_excluded_when_generate_then_walnutsanity_is_forced_disabled(self):
        walnutsanity_options = options.Walnutsanity.valid_keys
        for walnutsanity in (
                walnutsanity
                for r in range(len(walnutsanity_options) + 1)
                for walnutsanity in itertools.combinations(walnutsanity_options, r)
        ):
            with self.subTest(f"Walnutsanity: {walnutsanity}"):
                world_options = fill_dataclass_with_default({
                    options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
                    options.Walnutsanity: walnutsanity
                })

                force_change_options_if_incompatible(world_options, 1, "Tester")

                self.assertEqual(world_options.walnutsanity.value, options.Walnutsanity.preset_none)

    def test_given_ginger_island_related_goal_and_ginger_island_excluded_when_generate_then_walnutsanity_is_not_changed(self):
        for goal in [options.Goal.option_greatest_walnut_hunter, options.Goal.option_perfection]:
            walnutsanity_options = options.Walnutsanity.valid_keys
            for original_walnutsanity_choice in (
                    set(walnutsanity)
                    for r in range(len(walnutsanity_options) + 1)
                    for walnutsanity in itertools.combinations(walnutsanity_options, r)
            ):
                with self.subTest(f"Goal: {options.Goal.get_option_name(goal)} Walnutsanity: {original_walnutsanity_choice}"):
                    world_options = fill_dataclass_with_default({
                        options.Goal: goal,
                        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
                        options.Walnutsanity: original_walnutsanity_choice
                    })

                    force_change_options_if_incompatible(world_options, 1, "Tester")

                    self.assertEqual(world_options.walnutsanity.value, original_walnutsanity_choice)


class TestGingerIslandExclusionOverridesQisSpecialOrders(unittest.TestCase):

    def test_given_ginger_island_excluded_when_generate_then_qis_special_orders_are_forced_disabled(self):
        special_order_options = options.SpecialOrderLocations.options
        for special_order in special_order_options.keys():
            with self.subTest(f"Special order: {special_order}"):
                world_options = fill_dataclass_with_default({
                    options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
                    options.SpecialOrderLocations: special_order
                })

                force_change_options_if_incompatible(world_options, 1, "Tester")

                self.assertEqual(world_options.special_order_locations.value & options.SpecialOrderLocations.value_qi, 0)

    def test_given_ginger_island_related_goal_and_ginger_island_excluded_when_generate_then_special_orders_is_not_changed(self):
        for goal in [options.Goal.option_greatest_walnut_hunter, options.Goal.option_perfection]:
            special_order_options = options.SpecialOrderLocations.options
            for special_order, original_special_order_value in special_order_options.items():
                with self.subTest(f"Special order: {special_order}"):
                    world_options = fill_dataclass_with_default({
                        options.Goal: goal,
                        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
                        options.SpecialOrderLocations: special_order
                    })

                    force_change_options_if_incompatible(world_options, 1, "Tester")

                    self.assertEqual(world_options.special_order_locations.value, original_special_order_value)
