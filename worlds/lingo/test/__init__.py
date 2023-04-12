from typing import ClassVar

from test.TestBase import WorldTestBase
from .. import LingoWorld


class LingoTestBase(WorldTestBase):
    game = "Lingo"
    world: LingoWorld
    player: ClassVar[int] = 1

    def world_setup(self, *args, **kwargs):
        super().world_setup(*args, **kwargs)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]

    @property
    def run_default_tests(self) -> bool:
        # world_setup is overridden, so it'd always run default tests when importing SVTestBase
        return type(self) is not LingoTestBase and super().run_default_tests
