from test.bases import WorldTestBase
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.world import RaC3World


class RAC3TestBase(WorldTestBase):
    game = RAC3OPTION.GAME_TITLE_FULL
    world: RaC3World
