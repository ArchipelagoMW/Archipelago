from typing import ClassVar

import Options
from test.bases import WorldTestBase
from .. import CMWorld


class CMTestBase(WorldTestBase):
    game = "ChecksMate"
    world: CMWorld
    player: ClassVar[int] = 1
    options = {
        "accessibility": "minimal",
        "min_material": 42,
        "locked_items": {"Progressive Major Piece": 5}
    }

    def world_setup(self, *args, **kwargs):
        super().world_setup(*args, **kwargs)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]  # noqa
            self.multiworld.accessibility[self.player] = Options.Accessibility.option_minimal
