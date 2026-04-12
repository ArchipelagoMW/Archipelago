from test.bases import WorldTestBase
from ..world import NothingWorld

class NothingTestBase(NothingWorld):
    game = "nothing_archipelago"
    world: NothingWorld