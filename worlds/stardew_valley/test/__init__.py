from test.TestBase import WorldTestBase
from .. import StardewValleyWorld


class SVTestBase(WorldTestBase):
    game = "Stardew Valley"
    world: StardewValleyWorld

    def world_setup(self, *args, **kwargs):
        super().world_setup(*args, **kwargs)
        self.world = self.multiworld.worlds[self.player]
