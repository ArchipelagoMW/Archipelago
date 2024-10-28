from io import BytesIO, StringIO

from . import GSTestBase
from .. import LocationType


class TestRandoFormat(GSTestBase):

    def test_file_structure(self):
        world = self.get_world()
        rando_content = BytesIO()
        debug_content = StringIO()
        world._generate_rando_data(rando_content, debug_content)
        data = rando_content.getvalue()
        loc_count = 0
        for loc in world.multiworld.get_locations(world.player):
            if loc.item is not None and loc.location_data.loc_type != LocationType.Event:
                loc_count += 1
        expected_length = 1 + 16 + 16 + len(self.world.player_name) + 1 + loc_count * 4 + 4
        self.assertEqual(expected_length, len(data))

        rando_content.seek(0)
        version = int.from_bytes(rando_content.read(1), byteorder='little')
        self.assertEqual(1, version)

        rando_content.seek(33)
        name = rando_content.read(len(self.world.player_name) + 1).decode('ascii')
        self.assertEqual(self.world.player_name + "\n", name)
