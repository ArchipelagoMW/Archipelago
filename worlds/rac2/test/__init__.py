from typing import ClassVar

from BaseClasses import get_seed
from test.bases import WorldTestBase

DEFAULT_TEST_SEED = get_seed(1)


class Rac2TestBase(WorldTestBase):
    game = "Ratchet & Clank 2"
    player: ClassVar[int] = 1

    seed = DEFAULT_TEST_SEED

    def world_setup(self, *args, **kwargs):
        super().world_setup(seed=self.seed)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]
