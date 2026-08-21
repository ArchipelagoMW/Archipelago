from test.bases import WorldTestBase

from .. import SM64World


class SM64TestBase(WorldTestBase):
    game = "Super Mario 64"
    world: SM64World
