from test.bases import WorldTestBase
from ..Items import Items

class SohTestBase(WorldTestBase):
    game = "Ship of Harkinian"
    glitches_item_name = Items.GLITCHED

    def enable_glitched_item(self):
        """
        Enable the use of the glitched/sequence breaking item for unit test purposes.

        Also automatically award the item for convenience sake.
        """
        self.collect(self.world.create_item(Items.GLITCHED))
