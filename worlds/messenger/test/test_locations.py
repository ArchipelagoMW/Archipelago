from . import MessengerTestBase
from ..subclasses import MessengerLocation


class LocationsTest(MessengerTestBase):
    options = {
        "shuffle_shards": "true",
    }

    @property
    def run_default_tests(self) -> bool:
        return False

    def test_locations_exist(self) -> None:
        for location in self.multiworld.worlds[1].location_name_to_id:
            self.assertIsInstance(self.multiworld.get_location(location, self.player), MessengerLocation)
