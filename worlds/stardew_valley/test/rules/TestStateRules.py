from .. import SVTestBase
from ..options.presets import allsanity_mods_6_x_x
from ...stardew_rule import HasProgressionPercent


class TestHasProgressionPercentWithVictory(SVTestBase):
    options = allsanity_mods_6_x_x()

    def test_has_100_progression_percent_is_false_while_items_are_missing(self):
        has_100_progression_percent = HasProgressionPercent(1, 100)

        for i, item in enumerate([i for i in self.multiworld.get_items() if i.advancement and i.code][1:]):
            if item.name != "Victory":
                self.collect(item)
            self.assertFalse(has_100_progression_percent(self.multiworld.state),
                             f"Rule became true after {i} items, total_progression_items is {self.world.total_progression_items}")

    def test_has_100_progression_percent_account_for_victory_not_being_collected(self):
        has_100_progression_percent = HasProgressionPercent(1, 100)

        self.collect_all_except("Victory")

        self.assert_rule_true(has_100_progression_percent, self.multiworld.state)
