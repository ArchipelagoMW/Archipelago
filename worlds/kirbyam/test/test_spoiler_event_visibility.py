from . import KirbyAmTestBase
from ..data import load_json_data


def test_region_json_excludes_debug_events_from_dimension_mirror() -> None:
    regions = load_json_data("regions/areas.json")
    assert "REGION_DIMENSION_MIRROR/MAIN" in regions
    dim_region = regions["REGION_DIMENSION_MIRROR/MAIN"]
    assert "events" in dim_region
    events = dim_region["events"]
    assert "Defeat Dark Meta Knight (Dimension Mirror)" in events

    assert all(not str(event_name).startswith("EVENT_DEBUG_") for event_name in events)


class TestKirbyAmNoDebugEventLocations(KirbyAmTestBase):
    def test_generated_world_has_no_debug_event_locations(self) -> None:
        location_names = {location.name for location in self.multiworld.get_locations(self.player)}
        assert all(not str(name).startswith("EVENT_DEBUG_") for name in location_names)
