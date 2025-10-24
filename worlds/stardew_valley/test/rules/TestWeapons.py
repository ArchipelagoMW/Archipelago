from ..bases import SVTestBase
from ... import options
from ...options import ToolProgression


class TestWeaponsLogic(SVTestBase):
    options = {
        ToolProgression.internal_name: ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_mine(self):
        self.multiworld.state.collect(self.create_item("Progressive Pickaxe"))
        self.multiworld.state.collect(self.create_item("Progressive Pickaxe"))
        self.multiworld.state.collect(self.create_item("Progressive Pickaxe"))
        self.multiworld.state.collect(self.create_item("Progressive Pickaxe"))
        self.multiworld.state.collect(self.create_item("Progressive House"))
        self.collect([self.create_item("Combat Level")] * 10)
        self.collect([self.create_item("Mining Level")] * 10)
        self.collect([self.create_item("Progressive Mine Elevator")] * 24)
        self.multiworld.state.collect(self.create_item("Bus Repair"))
        self.multiworld.state.collect(self.create_item("Skull Key"))

        self.give_item_and_check_reachable_mine("Progressive Sword", 1)
        self.give_item_and_check_reachable_mine("Progressive Dagger", 1)
        self.give_item_and_check_reachable_mine("Progressive Club", 1)

        self.give_item_and_check_reachable_mine("Progressive Sword", 2)
        self.give_item_and_check_reachable_mine("Progressive Dagger", 2)
        self.give_item_and_check_reachable_mine("Progressive Club", 2)

        self.give_item_and_check_reachable_mine("Progressive Sword", 3)
        self.give_item_and_check_reachable_mine("Progressive Dagger", 3)
        self.give_item_and_check_reachable_mine("Progressive Club", 3)

        self.give_item_and_check_reachable_mine("Progressive Sword", 4)
        self.give_item_and_check_reachable_mine("Progressive Dagger", 4)
        self.give_item_and_check_reachable_mine("Progressive Club", 4)

        self.give_item_and_check_reachable_mine("Progressive Sword", 5)
        self.give_item_and_check_reachable_mine("Progressive Dagger", 5)
        self.give_item_and_check_reachable_mine("Progressive Club", 5)

    def give_item_and_check_reachable_mine(self, item_name: str, reachable_level: int):
        item = self.multiworld.create_item(item_name, self.player)
        self.multiworld.state.collect(item)
        rule = self.world.logic.mine.can_mine_in_the_mines_floor_1_40()
        if reachable_level > 0:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)

        rule = self.world.logic.mine.can_mine_in_the_mines_floor_41_80()
        if reachable_level > 1:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)

        rule = self.world.logic.mine.can_mine_in_the_mines_floor_81_120()
        if reachable_level > 2:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)

        rule = self.world.logic.mine.can_mine_in_the_skull_cavern()
        if reachable_level > 3:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)

        rule = self.world.logic.ability.can_mine_perfectly_in_the_skull_cavern()
        if reachable_level > 4:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)
