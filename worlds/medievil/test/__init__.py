import unittest
from argparse import Namespace

from BaseClasses import MultiWorld, CollectionState
from worlds import AutoWorldRegister


class MedievilTestBase(unittest.TestCase):
    def world_setup(self):
        from worlds.medievil.Options import GoalOptions, ExcludeAntCaves
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = "Medievil"
        self.multiworld.set_seed(None)
        args = Namespace()
        for name, option in AutoWorldRegister.world_types["Medievil"].options_dataclass.type_hints.items():
            setattr(args, name, {1: option.from_any(getattr(option, "default"))})
        self.multiworld.set_options(args)
        self.multiworld.state = CollectionState(self.multiworld)
        self.world = self.multiworld.worlds[1]
        # by default medallion access is randomized, for unittests we set it to vanilla
        self.world.options.goal = GoalOptions.DEFEAT_ZAROK
        self.world.options.goal = ExcludeAntCaves(1)
