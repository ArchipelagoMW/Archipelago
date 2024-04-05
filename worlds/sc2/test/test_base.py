from test.TestBase import WorldTestBase
from typing import *

from .. import Client, SC2World


class Sc2TestBase(WorldTestBase):
    game = Client.SC2Context.game
    world: SC2World
    player: ClassVar[int] = 1
    skip_long_tests: bool = True
