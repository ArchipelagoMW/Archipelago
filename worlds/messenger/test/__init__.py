import unittest

from test.bases import WorldTestBase
from .. import MessengerWorld


class MessengerTestBase(WorldTestBase):
    game = "The Messenger"
    world: MessengerWorld

    @classmethod
    def setUpClass(cls) -> None:
        if cls is MessengerTestBase:
            raise unittest.SkipTest("No running tests on MessengerTestBase import.")
        super().setUpClass()
