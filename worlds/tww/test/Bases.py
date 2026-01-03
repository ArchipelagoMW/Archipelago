from test.bases import WorldTestBase
from ..Constants import GAME_NAME, GLITCHED_ITEM

class WindWakerTestBase(WorldTestBase):
    game = GAME_NAME
    glitches_item_name = GLITCHED_ITEM

    def enable_glitched_item(self):
        """
        Enable the use of the glitched/sequence breaking item for unit test purposes.

        Also automatically award the item for convenience sake.
        """
        self.collect(self.world.create_item(GLITCHED_ITEM))
