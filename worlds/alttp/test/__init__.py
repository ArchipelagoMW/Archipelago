import unittest
from argparse import Namespace

from BaseClasses import MultiWorld, CollectionState
from worlds import AutoWorldRegister


class LTTPTestBase(unittest.TestCase):
    def world_setup(self):
        from worlds.alttp.Options import Medallion
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = "A Link to the Past"
        self.multiworld.state = CollectionState(self.multiworld)
        self.multiworld.set_seed(None)
        args = Namespace()
        for name, option in AutoWorldRegister.world_types["A Link to the Past"].options_dataclass.type_hints.items():
            setattr(args, name, {1: option.from_any(getattr(option, "default"))})
        self.multiworld.set_options(args)
        self.world = self.multiworld.worlds[1]
        # by default medallion access is randomized, for unittests we set it to vanilla
        self.world.options.misery_mire_medallion.value = Medallion.option_ether
        self.world.options.turtle_rock_medallion.value = Medallion.option_quake
