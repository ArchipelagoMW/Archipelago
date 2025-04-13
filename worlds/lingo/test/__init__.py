from typing import ClassVar

from test.bases import WorldTestBase


class LingoTestBase(WorldTestBase):
    game = "Lingo"
    player: ClassVar[int] = 1
