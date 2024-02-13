from random import random

from .. import setup_solo_multiworld, SVTestCase
from ..assertion import WorldAssertMixin
from ... import options


class TestGeneratePreRolledRandomness(WorldAssertMixin, SVTestCase):
    def test_given_pre_rolled_difficult_randomness_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        choices = {
            options.EntranceRandomization.internal_name: options.EntranceRandomization.option_buildings,
            options.BundleRandomization.internal_name: options.BundleRandomization.option_remixed,
            options.BundlePrice.internal_name: options.BundlePrice.option_maximum
        }

        num_tests = 1000
        for i in range(num_tests):
            seed = int(random() * pow(10, 18) - 1)
            # seed = 738592514038774912
            with self.subTest(f"Entrance Randomizer and Remixed Bundles [SEED: {seed}]"):
                multiworld = setup_solo_multiworld(choices, seed)
                self.assert_basic_checks(multiworld)
