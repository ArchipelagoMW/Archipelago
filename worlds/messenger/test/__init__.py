from test.bases import WorldTestBase
from .. import MessengerWorld


class MessengerTestBase(WorldTestBase):
    game = "The Messenger"
    player: int = 1
    world: MessengerWorld
    
    def setUp(self) -> None:
        super().setUp()
        self.world = self.multiworld.worlds[self.player]
