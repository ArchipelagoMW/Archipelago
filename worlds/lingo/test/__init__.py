from typing import ClassVar

from argparse import Namespace
from BaseClasses import MultiWorld
from test.TestBase import WorldTestBase
from test.general import gen_steps
from .. import LingoWorld
from worlds.AutoWorld import AutoWorldRegister, call_all


class LingoTestBase(WorldTestBase):
    game = "Lingo"
    world: LingoWorld
    player: ClassVar[int] = 1

    def world_setup(self, *args, **kwargs):
        # Most of this is copied from the superclass, because we want to run some code in the middle of generation.
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = self.game
        self.multiworld.player_name = {1: "Tester"}
        self.multiworld.set_seed(None)
        args = Namespace()
        for name, option in AutoWorldRegister.world_types[self.game].option_definitions.items():
            setattr(args, name, {
                1: option.from_any(self.options.get(name, getattr(option, "default")))
            })
        self.multiworld.set_options(args)
        self.multiworld.set_default_common_options()

        # Test specific stuff.
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]
            self.world.test_options.disable_forced_good_item = True

        # Actual generation.
        for step in gen_steps:
            call_all(self.multiworld, step)

    @property
    def run_default_tests(self) -> bool:
        # world_setup is overridden, so it'd always run default tests when importing SVTestBase
        return type(self) is not LingoTestBase and super().run_default_tests
