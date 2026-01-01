import unittest
from typing import ClassVar

from BaseClasses import get_seed
from test.param import classvar_matrix
from ..assertion import WorldAssertMixin
from ..bases import skip_long_tests, SVTestCase, solo_multiworld
from ... import options

if skip_long_tests():
    raise unittest.SkipTest("Long tests disabled")

player_options = {
    options.EntranceRandomization.internal_name: options.EntranceRandomization.option_buildings,
    options.BundleRandomization.internal_name: options.BundleRandomization.option_remixed,
    options.BundlePrice.internal_name: options.BundlePrice.option_maximum
}


@classvar_matrix(n=range(1000))
class TestGeneratePreRolledRandomness(WorldAssertMixin, SVTestCase):
    n: ClassVar[int]

    def test_given_pre_rolled_difficult_randomness_when_generate_then_basic_checks(self):
        seed = get_seed()

        print(f"Generating solo multiworld with seed {seed} for Stardew Valley...")
        with solo_multiworld(player_options, seed=seed, world_caching=False) as (multiworld, _):
            self.assert_basic_checks(multiworld)
