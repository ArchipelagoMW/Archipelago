from test.bases import WorldTestBase
from .. import MessengerWorld


class MessengerTestBase(WorldTestBase):
    game = "The Messenger"
    world: MessengerWorld
