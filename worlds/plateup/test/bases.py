from test.bases import WorldTestBase
from ..World import PlateUpWorld


class PlateUpTestBase(WorldTestBase):
    game = "plateup"
    world: PlateUpWorld
