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

    def test_both_side_of_the_same_connection_has_matching_groups(self):
        checked_connections = set()
        connections_by_name = {c.name: c for c in connections_by_content[self.content]}

        for connection in connections_by_content[self.content]:
            if connection.name in checked_connections or RandomizationFlag.IS_ONE_WAY in connection.flag or connection.group == GroupFlag.TO_ANY:
                continue

            opposite_connection = connection.destination_entrance_name
            checked_connections.add(opposite_connection)

            with self.subTest(connection=connection.name):
                if GroupFlag.LEFT in connection.group:
                    self.assertIn(GroupFlag.RIGHT, connections_by_name[opposite_connection].group)
                elif GroupFlag.RIGHT in connection.group:
                    self.assertIn(GroupFlag.LEFT, connections_by_name[opposite_connection].group)
                elif GroupFlag.UP in connection.group:
                    self.assertIn(GroupFlag.DOWN, connections_by_name[opposite_connection].group)
                elif GroupFlag.LADDER in connection.group:
                    self.assertIn(GroupFlag.DOOR, connections_by_name[opposite_connection].group)
                elif GroupFlag.DOOR in connection.group:
                    self.assertIn(connections_by_name[opposite_connection].group & GroupFlag.DIR_MASK, (GroupFlag.DOWN, GroupFlag.LADDER))
                elif GroupFlag.DOWN in connection.group:
                    self.assertIn(connections_by_name[opposite_connection].group & GroupFlag.DIR_MASK, (GroupFlag.DOOR, GroupFlag.UP))

                if GroupFlag.IN_TO_IN in connection.group:
                    self.assertIn(GroupFlag.IN_TO_IN, connections_by_name[opposite_connection].group)
                elif GroupFlag.OUT_TO_OUT in connection.group:
                    self.assertIn(GroupFlag.OUT_TO_OUT, connections_by_name[opposite_connection].group)
                elif GroupFlag.IN_TO_OUT in connection.group:
                    self.assertIn(GroupFlag.OUT_TO_IN, connections_by_name[opposite_connection].group)
                elif GroupFlag.OUT_TO_IN in connection.group:
                    self.assertIn(GroupFlag.IN_TO_OUT, connections_by_name[opposite_connection].group)

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
