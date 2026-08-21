from collections.abc import Iterable
from typing import ClassVar
from unittest import TestCase

from test.param import classvar_matrix

from Options import PlandoConnection

from ... import EntranceRandomizationBehaviorOptionName, options
from ...data.regions import ConnectionData, GroupFlag, RandomizationFlag, vanilla_connections
from ...mods.region_data import region_data_by_content_pack
from ...regions.entrance_rando import get_target_groups
from ...strings.entrance_names import Entrance as EntranceName
from ...strings.region_names import Region as RegionName
from ..bases import SVTestBase

connections_by_content: dict[str, Iterable[ConnectionData]] = dict(
    [("Vanilla", vanilla_connections), *((content_pack, data.connections) for content_pack, data in region_data_by_content_pack.items())]
)


@classvar_matrix(er_behavior=options.EntranceRandomizationBehavior.valid_keys)
class TestSameTypeEntranceRandomization(TestCase):
    er_behavior: ClassVar[str]

    def test_group_can_connect_to_self(self):

        groups = get_target_groups(options.EntranceRandomizationBehavior({self.er_behavior}))
        for group, allowed_groups in groups.items():
            with self.subTest(group=group):
                self.assertIn(group, allowed_groups)

@classvar_matrix(content=connections_by_content.keys())
class TestContentPacksEntranceTargetGroups(TestCase):
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
                connections_in_first_group = sum(
                    1
                    for connection in connections
                    if any(group in connection.group for group in first_group)
                    if RandomizationFlag.IS_ONE_WAY not in connection.flag
                )
                connections_in_second_group = sum(
                    1
                    for connection in connections
                    if any(group in connection.group for group in second_group)
                    if RandomizationFlag.IS_ONE_WAY not in connection.flag
                )

                self.assertEqual(connections_in_first_group, connections_in_second_group)

    def test_all_connections_has_area_group_flag(self):
        connections = connections_by_content[self.content]
        for connection in connections:
            if connection.flag == RandomizationFlag.NOT_RANDOMIZED:
                continue

            with self.subTest(connection=connection.name):
                self.assertNotEqual(GroupFlag.TO_ANY, connection.group & GroupFlag.AREA_MASK)

class TestFarmhouseEntranceCanBePairedMatchWithSomething(SVTestBase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_disabled,
        options.EntranceRandomizationBehavior: {EntranceRandomizationBehaviorOptionName.decoupled},
        options.EntrancePlando: [
            PlandoConnection(EntranceName.farmhouse_to_farm, EntranceName.town_to_sewer, "entrance", 100),
        ],
    }

    def test_can_roll_entrance_rando(self):
        farmhouse_exit = self.world.get_entrance(EntranceName.farmhouse_to_farm)
        self.assertEqual(RegionName.sewer, farmhouse_exit.connected_region.name)
