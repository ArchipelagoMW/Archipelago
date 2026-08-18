from collections.abc import Iterable
from typing import ClassVar
from unittest import TestCase

from test.param import classvar_matrix

from ... import options
from ...data.regions import ConnectionData, GroupFlag, ginger_island_connections, vanilla_connections
from ...mods.region_data import region_data_by_content_pack
from ...regions.entrance_rando import get_target_groups


@classvar_matrix(er_behavior=options.EntranceRandomizationBehavior.valid_keys)
class TestSameTypeEntranceRandomization(TestCase):
    er_behavior: ClassVar[str]

    def test_group_can_connect_to_self(self):

        groups = get_target_groups(options.EntranceRandomizationBehavior({self.er_behavior}))
        for group, allowed_groups in groups.items():
            with self.subTest(group=group):
                self.assertIn(group, allowed_groups)


connections_by_content: dict[str, Iterable[ConnectionData]] = dict(
    [("Vanilla", vanilla_connections), *((content_pack, data.connections) for content_pack, data in region_data_by_content_pack.items())]
)


@classvar_matrix(content=connections_by_content.keys())
class TestRegionsHasMatchingAmountOfTargetGroups(TestCase):
    content: ClassVar[str]

    def test_content_has_matching_amount_of_connection_for_each_group(self):
        matching_groups: list[tuple[Iterable[GroupFlag], Iterable[GroupFlag]]] = [
            ((GroupFlag.RIGHT,), (GroupFlag.LEFT,)),
            ((GroupFlag.UP, GroupFlag.DOOR), (GroupFlag.DOWN, GroupFlag.LADDER)),
            ((GroupFlag.OUT_TO_OUT,), (GroupFlag.OUT_TO_OUT,)),
            ((GroupFlag.IN_TO_IN,), (GroupFlag.IN_TO_IN,)),
            ((GroupFlag.OUT_TO_IN,), (GroupFlag.IN_TO_OUT,)),
        ]

        connections = connections_by_content[self.content]

        for matching_group in matching_groups:
            with self.subTest(matching_group=matching_group):
                first_group, second_group = matching_group
                connections_in_first_group = sum(1 for connection in connections if any(group in connection.group for group in first_group))
                connections_in_second_group = sum(1 for connection in connections if any(group in connection.group for group in second_group))

                self.assertEqual(connections_in_first_group, connections_in_second_group)
