import typing
from argparse import Namespace

from BaseClasses import MultiWorld, PlandoOptions, CollectionState
from test.TestBase import WorldTestBase
from test.general import gen_steps
from worlds import AutoWorld
from worlds.AutoWorld import call_all


class KDL3TestBase(WorldTestBase):
    game = "Kirby's Dream Land 3"

    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        if type(self) is WorldTestBase or \
                (hasattr(WorldTestBase, self._testMethodName)
                 and not self.run_default_tests and
                 getattr(self, self._testMethodName).__code__ is
                 getattr(WorldTestBase, self._testMethodName, None).__code__):
            return  # setUp gets called for tests defined in the base class. We skip world_setup here.
        if not hasattr(self, "game"):
            raise NotImplementedError("didn't define game name")
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = self.game
        self.multiworld.player_name = {1: "Tester"}
        self.multiworld.set_seed(seed)
        self.multiworld.state = CollectionState(self.multiworld)
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].options_dataclass.type_hints.items():
            setattr(args, name, {
                1: option.from_any(self.options.get(name, getattr(option, "default")))
            })
        self.multiworld.set_options(args)
        self.multiworld.plando_options = PlandoOptions.connections
        self.multiworld.plando_connections = self.options["plando_connections"] if "plando_connections" in self.options.keys() else []
        for step in gen_steps:
            call_all(self.multiworld, step)
