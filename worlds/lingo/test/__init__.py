from test.bases import WorldTestBase
from typing import ClassVar


class LingoTestBase(WorldTestBase):
    game = "Lingo"
    player: ClassVar[int] = 1
