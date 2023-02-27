from argparse import Namespace

from BaseClasses import MultiWorld
from test.TestBase import WorldTestBase, gen_steps
from worlds import AutoWorldRegister
from worlds.AutoWorld import call_all


class LTTPOptionsTestBase(WorldTestBase):
    game = "A Link to the Past"

    def setUp(self) -> None:
        for option in self.options:
            if option not in AutoWorldRegister.world_types[self.game].option_definitions:
                self.setup_lttp_multiworld()
                break
        else:
            super().setUp()

    def setup_lttp_multiworld(self):
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = self.game
        self.multiworld.player_name = {1: "Tester"}
        args = Namespace()
        for name, option in AutoWorldRegister.world_types[self.game].option_definitions.items():
            setattr(args, name, {1: option.from_any(self.options.get(name, getattr(option, "default")))})
        self.multiworld.set_options(args)
        self.multiworld.set_default_common_options()
        for name, option in {name: option for name, option in self.options.items()
                             if name not in AutoWorldRegister.world_types[self.game].option_definitions}.items():
            setattr(self.multiworld, name, {1: option})
        for step in gen_steps:
            call_all(self.multiworld, step)
