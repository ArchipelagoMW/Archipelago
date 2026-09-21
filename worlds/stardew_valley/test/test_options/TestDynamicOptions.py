import unittest
from typing import ClassVar

from test.param import classvar_matrix
from ..options.option_names import get_all_option_choices
from ...options import BackpackProgression, BackpackSize, BundlePerRoom, BundlePrice, FarmType
from ...test.assertion import WorldAssertMixin
from ...test.bases import SVTestCase, solo_multiworld, skip_long_tests

if skip_long_tests():
    raise unittest.SkipTest("Long tests disabled")

extra_options_to_ignore = [BackpackProgression.internal_name, BackpackSize.internal_name, BundlePerRoom.internal_name,
                           BundlePrice.internal_name, FarmType.internal_name]


@classvar_matrix(option_and_choice=get_all_option_choices(extra_options_to_ignore))
class TestGenerateDynamicOptions(WorldAssertMixin, SVTestCase):
    option_and_choice: ClassVar[tuple[str, str]]

    def test_given_option_and_choice_when_generate_then_basic_checks(self):
        option, choice = self.option_and_choice
        world_options = {option: choice}
        with solo_multiworld(world_options) as (multiworld, stardew_world):
            self.assert_basic_checks(multiworld)