from test.bases import WorldTestBase

from .. import ShellipelagoWorld


class ShellipelagoTestBase(WorldTestBase):
    game = "Shellipelago"
    world: ShellipelagoWorld
