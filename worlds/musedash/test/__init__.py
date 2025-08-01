from test.bases import WorldTestBase
from .. import MuseDashWorld
from typing import cast

class MuseDashTestBase(WorldTestBase):
    game = "Muse Dash"

    def get_world(self) -> MuseDashWorld:
        return cast(MuseDashWorld, self.multiworld.worlds[1])

