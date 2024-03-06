from typing import Dict, Set

from . import ZorkGrandInquisitorTestBase

from ..data_funcs import location_names_to_location, locations_with_tag
from ..enums import ZorkGrandInquisitorLocations, ZorkGrandInquisitorTags


class LocationsTestNoDeathsanity(ZorkGrandInquisitorTestBase):
    options = {
        "deathsanity": "false",
    }

    def test_correct_locations_exist(self) -> None:
        expected_locations: Set[ZorkGrandInquisitorLocations] = locations_with_tag(
            ZorkGrandInquisitorTags.CORE
        )

        self._assert_expected_locations_exist(expected_locations)

    def _assert_expected_locations_exist(self, expected_locations: Set[ZorkGrandInquisitorLocations]) -> None:
        location_name_to_location: Dict[str, ZorkGrandInquisitorLocations] = location_names_to_location()

        for location_object in self.multiworld.get_locations(1):
            location: ZorkGrandInquisitorLocations = location_name_to_location.get(
                location_object.name
            )

            if location is None:
                continue

            self.assertIn(location, expected_locations)

            expected_locations.remove(location)

        self.assertEqual(0, len(expected_locations))


class LocationsTestDeathsanity(LocationsTestNoDeathsanity):
    options = {
        "deathsanity": "true",
    }

    def test_correct_locations_exist(self) -> None:
        expected_locations: Set[ZorkGrandInquisitorLocations] = (
            locations_with_tag(ZorkGrandInquisitorTags.CORE) | locations_with_tag(ZorkGrandInquisitorTags.DEATHSANITY)
        )

        self._assert_expected_locations_exist(expected_locations)
