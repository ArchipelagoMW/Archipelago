import loguru
from test.bases import WorldTestBase
from ..Options import LogicType, RandomizeBTMoveList
from . import BanjoTooieTestBase
from .. import all_item_table

class AdvMovesEnabled(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true
    }

    def test_item_pool(self) -> None:
        adv_move_count = len(self.world.item_name_groups["Moves"])
        adv_count = 0

        item_pool_item_names = [item.name for item in self.world.multiworld.itempool]
        for adv_move in self.world.item_name_groups["Moves"]:
            if adv_move in item_pool_item_names:
                adv_count += 1

        assert adv_move_count == adv_count


class AdvMovesDisabled(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_false
    }

    def test_disabled_item_pool(self) -> None:
        adv_count = 0

        for adv_move in self.world.item_name_groups["Moves"]:
            for item in self.world.multiworld.itempool:
                if adv_move == item.name:
                    loguru.logger.error(f"Item: {adv_move} Should be here!")
                    adv_count += 1

        assert 0 == adv_count

    def test_prefills(self) -> None:
        adv_items = 0
        placed_correctly = 0
        for name in self.world.item_name_groups["Moves"]:
            adv_items += 1
            banjoItem = all_item_table[name]
            try:
                location_item = self.multiworld.get_location(banjoItem.default_location, self.player).item.name
                if location_item == name:
                    placed_correctly += 1
            except Exception:
                loguru.logger.error(f"Issue with Item: {name} Please Investigate")
                placed_correctly += 0
        assert adv_items == placed_correctly


class TestAdvMovesEnabledIntended(AdvMovesEnabled):
    options = {
        **AdvMovesEnabled.options,
        "logic_type": LogicType.option_intended,
    }


class TestAdvMovesEnabledEasyTricks(AdvMovesEnabled):
    options = {
        **AdvMovesEnabled.options,
        "logic_type": LogicType.option_easy_tricks,
    }


class TestAdvMovesEnabledHardTricks(AdvMovesEnabled):
    options = {
        **AdvMovesEnabled.options,
        "logic_type": LogicType.option_hard_tricks,
    }


class TestAdvMovesEnabledGlitchesTricks(AdvMovesEnabled):
    options = {
        **AdvMovesEnabled.options,
        "logic_type": LogicType.option_glitches,
    }


class TestAdvMovesDisabledIntended(AdvMovesDisabled):
    options = {
        **AdvMovesDisabled.options,
        "logic_type": LogicType.option_intended,
    }


class TestAdvMovesDisabledEasyTricks(AdvMovesDisabled):
    options = {
        **AdvMovesDisabled.options,
        "logic_type": LogicType.option_easy_tricks,
    }


class TestAdvMovesDisabledHardTricks(AdvMovesDisabled):
    options = {
        **AdvMovesDisabled.options,
        "logic_type": LogicType.option_hard_tricks,
    }


class TestAdvMovesDisabledGlitchesTricks(AdvMovesDisabled):
    options = {
        **AdvMovesDisabled.options,
        "logic_type": LogicType.option_glitches,
    }
