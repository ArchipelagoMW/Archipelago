from . import KirbyAmTestBase
from ..data import load_json_data


def test_region_json_excludes_debug_events_from_dimension_mirror() -> None:
    regions = load_json_data("regions/areas.json")
    dim_region = regions.get("REGION_DIMENSION_MIRROR/MAIN", {})
    events = dim_region.get("events", [])

    assert all(not str(event_name).startswith("EVENT_DEBUG_") for event_name in events)


class TestKirbyAmNoDebugEventLocations(KirbyAmTestBase):
    def test_generated_world_has_no_debug_event_locations(self) -> None:
        location_names = {location.name for location in self.multiworld.get_locations(self.player)}
        assert "EVENT_DEBUG_LOCATION" not in location_names
