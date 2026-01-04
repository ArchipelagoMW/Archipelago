from test.bases import WorldTestBase

class WindWakerTestBase(WorldTestBase):
    game = "The Wind Waker"
    glitches_item_name = "Glitched"

    def enable_glitched_item(self):
        """
        Enable the use of the glitched/sequence breaking item for unit test purposes.

        Also automatically award the item for convenience sake.
        """
        self.collect(self.world.create_item("Glitched"))
