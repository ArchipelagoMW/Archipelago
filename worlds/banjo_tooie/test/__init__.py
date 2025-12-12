from test.bases import WorldTestBase
from .. import BanjoTooieWorld


class BanjoTooieTestBase(WorldTestBase):
    game = "Banjo-Tooie"
    world: BanjoTooieWorld
