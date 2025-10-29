from .. import SohWorld
from ..Items import Items
from .bases import SohTestBase


class TestHearts(SohTestBase):
    world: SohWorld

    def test_heart_counts(self):
        # note that tests don't care if something is progression, since we manually collect
        # it doesn't actually matter whether the heart pieces are useful or prog for this test
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 3)  # type: ignore

        self.collect(self.world.create_item(Items.HEART_CONTAINER))
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 4)  # type: ignore

        for _ in range(3):
            self.collect(self.world.create_item(Items.PIECE_OF_HEART))
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 4)  # type: ignore

        heart = self.world.create_item(Items.HEART_CONTAINER)
        self.collect(heart)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 5)  # type: ignore

        heart_piece = self.world.create_item(Items.PIECE_OF_HEART)
        self.collect(heart_piece)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 6)  # type: ignore

        self.remove(heart_piece)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 5)  # type: ignore

        self.remove(heart)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 4)  # type: ignore
