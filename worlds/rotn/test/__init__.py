from test.bases import WorldTestBase
from .. import RotNWorld
from typing import cast

class RotNTestBase(WorldTestBase):
    game = "Rift of the Necrodancer"

    def get_world(self) -> RotNWorld:
        return cast(RotNWorld, self.multiworld.worlds[1])