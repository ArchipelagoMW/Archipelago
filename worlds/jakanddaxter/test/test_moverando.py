from .bases import JakAndDaxterTestBase
from ..items import move_item_table


class MoveRandoTest(JakAndDaxterTestBase):
    options = {
        "enable_move_randomizer": True
    }

    def test_move_items_in_pool(self):
        for move in move_item_table:
            self.assertIn(move_item_table[move], {item.name for item in self.multiworld.itempool})
            self.assertNotIn(move_item_table[move],
                             {item.name for item in self.multiworld.precollected_items[self.player]})

    def test_cannot_reach_without_move(self):
        self.assertAccessDependency(
            ["GR: Climb Up The Cliff"],
            [["Double Jump"], ["Crouch"]],
            only_check_listed=True)


class NoMoveRandoTest(JakAndDaxterTestBase):
    options = {
        "enable_move_randomizer": False
    }

    def test_move_items_in_inventory(self):
        for move in move_item_table:
            self.assertNotIn(move_item_table[move], {item.name for item in self.multiworld.itempool})
            self.assertIn(move_item_table[move],
                          {item.name for item in self.multiworld.precollected_items[self.player]})
