from . import MessengerTestBase
from ..SubClasses import MessengerLocation


class LocationsTest(MessengerTestBase):
    options = {
        "shuffle_shards": "true",
    }

    @property
    def run_default_tests(self) -> bool:
        return False
    
    def testLocationsExist(self):
        for location in self.multiworld.worlds[1].location_name_to_id:
            self.assertIsInstance(self.multiworld.get_location(location, self.player), MessengerLocation)
