from typing import cast

from test.bases import WorldTestBase
from worlds.gstla import GSTLAWorld


class GSTestBase(WorldTestBase):
    game = 'Golden Sun The Lost Age'

    def get_world(self) -> GSTLAWorld:
        # Can't just retype world in this class
        return cast(GSTLAWorld, self.world)