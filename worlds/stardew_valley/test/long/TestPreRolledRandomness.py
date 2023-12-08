from random import random
from ..checks.world_checks import basic_checks
from .. import setup_solo_multiworld, SVTestCase
from ...options import EntranceRandomization, BundleRandomization, BundlePrice


class TestGeneratePreRolledRandomness(SVTestCase):
    def test_given_pre_rolled_difficult_randomness_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        choices = {EntranceRandomization.internal_name: EntranceRandomization.option_buildings,
                   BundleRandomization.internal_name: BundleRandomization.option_remixed,
                   BundlePrice.internal_name: BundlePrice.option_maximum}
        num_tests = 1000
        for i in range(num_tests):
            seed = int(random() * pow(10, 18) - 1)
            # seed = 738592514038774912
            with self.subTest(f"Entrance Randomizer and Remixed Bundles [SEED: {seed}]"):
                multiworld = setup_solo_multiworld(choices, seed)
                basic_checks(self, multiworld)