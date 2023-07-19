import unittest
from argparse import Namespace

from BaseClasses import MultiWorld, CollectionState
from worlds import AutoWorldRegister


class LTTPTestBase(unittest.TestCase):
    def world_setup(self):
        self.multiworld = MultiWorld(1)
        self.multiworld.state = CollectionState(self.multiworld)
        self.multiworld.set_seed(None)
        args = Namespace()
        for name, option in AutoWorldRegister.world_types["A Link to the Past"].options_dataclass.type_hints.items():
            setattr(args, name, {1: option.from_any(getattr(option, "default"))})
        self.multiworld.set_options(args)
