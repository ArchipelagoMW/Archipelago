from typing import ClassVar

from test.bases import WorldTestBase
from .. import LingoTestOptions


class LingoTestBase(WorldTestBase):
    game = "Lingo"
    player: ClassVar[int] = 1

    def world_setup(self, *args, **kwargs):
        LingoTestOptions.disable_forced_good_item = True
        super().world_setup(*args, **kwargs)
