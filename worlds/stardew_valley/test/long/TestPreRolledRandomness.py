import unittest

from BaseClasses import get_seed
from .. import SVTestCase
from ..assertion import WorldAssertMixin
from ... import options


class TestGeneratePreRolledRandomness(WorldAssertMixin, SVTestCase):
    def test_given_pre_rolled_difficult_randomness_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            raise unittest.SkipTest("Long tests disabled")

        choices = {
            options.EntranceRandomization.internal_name: options.EntranceRandomization.option_buildings,
            options.BundleRandomization.internal_name: options.BundleRandomization.option_remixed,
            options.BundlePrice.internal_name: options.BundlePrice.option_maximum
        }

        num_tests = 1000
        for i in range(num_tests):
            seed = get_seed()  # Put seed in parameter to test
            with self.solo_world_sub_test(f"Entrance Randomizer and Remixed Bundles",
                                          choices,
                                          seed=seed,
                                          world_caching=False) \
                    as (multiworld, _):
                self.assert_basic_checks(multiworld)
