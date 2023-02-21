import unittest
from argparse import Namespace
from typing import get_type_hints

from BaseClasses import MultiWorld, CollectionState
from worlds import AutoWorldRegister


class LTTPTestBase(unittest.TestCase):
    def world_setup(self):
        self.multiworld = MultiWorld(1)
        self.multiworld.state = CollectionState(self.multiworld)
        args = Namespace()
        for name, option in get_type_hints(AutoWorldRegister.world_types["A Link to the Past"].options_dataclass).items():
            setattr(args, name, {1: option.from_any(getattr(option, "default"))})
        self.multiworld.set_options(args)
