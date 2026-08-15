from typing import ClassVar
from unittest import TestCase

from test.param import classvar_matrix

from ... import options
from ...regions.entrance_rando import get_target_groups


@classvar_matrix(er_behavior=options.EntranceRandomizationBehavior.valid_keys)
class TestSameTypeEntranceRandomization(TestCase):
    er_behavior: ClassVar[str]

    def test_group_can_connect_to_self(self):

        groups = get_target_groups(options.EntranceRandomizationBehavior({self.er_behavior}))
        for group, allowed_groups in groups.items():
            with self.subTest(group=group):
                self.assertIn(group, allowed_groups)
