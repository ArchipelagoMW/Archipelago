from typing import *
import unittest
import random
from argparse import Namespace
from BaseClasses import MultiWorld, CollectionState, PlandoOptions
from Generate import get_seed_name
from worlds import AutoWorld
from test.general import gen_steps, call_all

from test.bases import WorldTestBase
from .. import SC2World, SC2Campaign
from .. import client
from .. import options

class Sc2TestBase(WorldTestBase):
    game = client.SC2Context.game
    world: SC2World
    player: ClassVar[int] = 1
    skip_long_tests: bool = True


class Sc2SetupTestBase(unittest.TestCase):
    """
    A custom sc2-specific test base class that provides an explicit function to generate the world from options.
    This allows potentially generating multiple worlds in one test case, useful for tracking down a rare / sporadic
    crash.
    """
    ALL_CAMPAIGNS = {
        'enabled_campaigns': options.EnabledCampaigns.valid_keys,
    }
    TERRAN_CAMPAIGNS = {
        'enabled_campaigns': {SC2Campaign.WOL.campaign_name, SC2Campaign.NCO.campaign_name,}
    }
    ZERG_CAMPAIGNS = {
        'enabled_campaigns': {SC2Campaign.HOTS.campaign_name,}
    }
    PROTOSS_CAMPAIGNS = {
        'enabled_campaigns': {SC2Campaign.PROPHECY.campaign_name, SC2Campaign.PROLOGUE.campaign_name, SC2Campaign.LOTV.campaign_name,}
    }
    seed: Optional[int] = None
    game = SC2World.game
    player = 1
    def generate_world(self, options: Dict[str, Any]) -> None:
        self.multiworld = MultiWorld(1)
        self.multiworld.game[self.player] = self.game
        self.multiworld.player_name = {self.player: "Tester"}
        self.multiworld.set_seed(self.seed)
        random.seed(self.multiworld.seed)
        self.multiworld.seed_name = get_seed_name(random)  # only called to get same RNG progression as Generate.py
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].options_dataclass.type_hints.items():
            new_option = option.from_any(options.get(name, option.default))
            new_option.verify(SC2World, "Tester", PlandoOptions.items|PlandoOptions.connections|PlandoOptions.texts|PlandoOptions.bosses)
            setattr(args, name, {
                1: new_option
            })
        self.multiworld.set_options(args)
        self.world: SC2World = cast(SC2World, self.multiworld.worlds[self.player])
        self.multiworld.state = CollectionState(self.multiworld)
        try:
            for step in gen_steps:
                call_all(self.multiworld, step)
        except Exception as ex:
            ex.add_note(f"Seed: {self.multiworld.seed}")
            raise
