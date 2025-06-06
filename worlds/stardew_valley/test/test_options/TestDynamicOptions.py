from typing import ClassVar

from test.param import classvar_matrix
from ...test.assertion import WorldAssertMixin
from ...test.bases import SVTestCase, solo_multiworld
from ...test.options.option_names import all_option_choices


@classvar_matrix(option_and_choice=all_option_choices)
class TestGenerateDynamicOptions(WorldAssertMixin, SVTestCase):
    option_and_choice: ClassVar[tuple[str, str]]

    def test_given_option_and_choice_when_generate_then_basic_checks(self):
        option, choice = self.option_and_choice
        world_options = {option: choice}
        with solo_multiworld(world_options) as (multiworld, stardew_world):
            self.assert_basic_checks(multiworld)