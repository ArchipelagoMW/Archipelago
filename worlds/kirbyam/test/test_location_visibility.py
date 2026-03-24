from . import KirbyAmTestBase
from .. import KirbyAmWorld


_GOAL_LOCATION_NAMES = {"Defeat Dark Mind", "100% Save File"}


def test_goal_locations_are_excluded_from_datapackage_location_ids() -> None:
    assert _GOAL_LOCATION_NAMES.isdisjoint(KirbyAmWorld.location_name_to_id)


def test_goal_locations_are_excluded_from_datapackage_location_groups() -> None:
    for group_locations in KirbyAmWorld.location_name_groups.values():
        assert _GOAL_LOCATION_NAMES.isdisjoint(group_locations)


class TestKirbyAmGoalLocationsRemainRuntimeEvents(KirbyAmTestBase):
    def test_goal_locations_still_exist_as_runtime_events(self) -> None:
        for goal_name in _GOAL_LOCATION_NAMES:
            location = self.multiworld.get_location(goal_name, self.player)
            assert location.address is None
            assert location.item is not None
            assert location.item.name == goal_name