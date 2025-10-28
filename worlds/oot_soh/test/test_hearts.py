from .. import SohWorld
from ..Items import Items
from .bases import SohTestBase


class TestHearts(SohTestBase):
    world: SohWorld

    def test_heart_counts(self):
        # pieces of heart are not progression, so we do not need to test them here
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 3)  # type: ignore

        heart = self.world.create_item(Items.HEART_CONTAINER)
        self.collect(heart)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 4)  # type: ignore

        self.remove(heart)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 3)  # type: ignore
