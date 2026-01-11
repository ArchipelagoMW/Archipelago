from test.bases import WorldTestBase
from .. import FF4FEWorld


class FF4FETestBase(WorldTestBase):
    game = "Final Fantasy IV Free Enterprise"
    world: FF4FEWorld
