from test.bases import WorldTestBase

from ..Rules import mix_in_universal_tracker_logic

class WindWakerTestBase(WorldTestBase):
    game = "The Wind Waker"
    glitches_item_name = "Glitched"

    def enable_glitched_item(self):
        """
        Enable the use of the glitched/sequence breaking item for unit test purposes.

        Also automatically award the item for convenience sake.
        """
        # Mix in Universal Tracker logic so glitched item checks work
        mix_in_universal_tracker_logic()

        self.collect(self.world.create_item("Glitched"))
