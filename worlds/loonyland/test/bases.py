from test.bases import WorldTestBase
from worlds.loonyland import LoonylandWorld


class LoonylandTestBase(WorldTestBase):
    game = "Loonyland"
    world: LoonylandWorld
