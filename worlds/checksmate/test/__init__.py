from typing import ClassVar

from test.bases import WorldTestBase
from .. import CMWorld


class CMTestBase(WorldTestBase):
    game = "ChecksMate"
    world: CMWorld
    player: ClassVar[int] = 1

    def world_setup(self, *args, **kwargs):
        self.options["accessibility"] = "minimal"
        self.options["min_material"] = 40
        super().world_setup(*args, **kwargs)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]  # noqa
