from typing import ClassVar

from test.bases import WorldTestBase


class CivVITestBase(WorldTestBase):
    game = "Civilization VI"
    player: ClassVar[int] = 1
