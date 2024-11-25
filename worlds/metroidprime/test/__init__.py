from typing import ClassVar

from BaseClasses import get_seed
from test.bases import WorldTestBase
from .. import MetroidPrimeWorld

DEFAULT_TEST_SEED = get_seed(1)


class MetroidPrimeTestBase(WorldTestBase):
    game = "Metroid Prime"
    player: ClassVar[int] = 1
    world: "MetroidPrimeWorld"

    seed = DEFAULT_TEST_SEED

    def world_setup(self, *args, **kwargs):  # type: ignore
        super().world_setup(seed=self.seed)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]  # type: ignore
