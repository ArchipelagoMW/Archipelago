from typing import Any, ClassVar, Dict, cast

from BaseClasses import get_seed
from test.bases import WorldTestBase
from .. import MetroidPrimeWorld, MultiworldWithPassthrough

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


class MetroidPrimeUniversalTrackerTestBase(WorldTestBase):
    game = "Metroid Prime"
    player: ClassVar[int] = 1
    world: "MetroidPrimeWorld"

    seed = DEFAULT_TEST_SEED

    def world_setup(self, *args, **kwargs):  # type: ignore
        super().world_setup(seed=self.seed)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]  # type: ignore
            self.tracker_multiworld = cast(MultiworldWithPassthrough, self.multiworld)

    def init_passhthrough(self, slot_data: Dict[Any, str]):
        self.tracker_multiworld.re_gen_passthrough = {self.game: slot_data}
