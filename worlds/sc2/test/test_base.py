from typing import *

from test.TestBase import WorldTestBase
from .. import SC2World
from .. import Client

class Sc2TestBase(WorldTestBase):
    game = Client.SC2Context.game
    world: SC2World
    player: ClassVar[int] = 1
    skip_long_tests: bool = True
