import typing
from BaseClasses import ItemClassification
from ...AutoWorld import call_all
from ..Options import HintClarity, RandomizeBKMoveList, RandomizeBTMoveList, \
    RandomizeSignposts, SignpostHints, AddSignpostHintsToArchipelagoHints
from . import BanjoTooieTestBase
from ..Items import moves_table, bk_moves_table, progressive_ability_table, all_item_table
from Fill import distribute_items_restrictive


class TestSignpostsHints(BanjoTooieTestBase):
    run_default_tests = False

    # fill_slot_data needs to be run for these tests to properly run.
    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        super(BanjoTooieTestBase, self).world_setup(seed)
        if not hasattr(self, "multiworld"):
            return
        distribute_items_restrictive(self.multiworld)
        call_all(self.multiworld, "post_fill")
        call_all(self.multiworld, "fill_slot_data")

    def test_hint_count(self) -> None:
        assert len(self.world.hints) == 61

        non_joke_hints = len([hint_data for hint_data in self.world.hints.values() if hint_data.location_id])
        assert non_joke_hints == self.world.options.signpost_hints.value

    def test_move_hint_count(self) -> None:
        move_names = [
            *[move_name for move_name in moves_table.keys()],
            *[move_name for move_name in bk_moves_table.keys()],
            *[move_name for move_name in progressive_ability_table.keys()],
        ]

        move_hints = 0
        for hint_data in self.world.hints.values():
            if hint_data.location_id is None:
                continue

            hinted_location = self.world.get_location(self.world.location_id_to_name[hint_data.location_id])
            print(hinted_location, hinted_location.item.name)
            if hinted_location.item.name in move_names:
                move_hints += 1

        # There can be more if slow locations are also hinted.
        possible_moves = 0
        if self.world.options.randomize_bt_moves.value:
            possible_moves += 24
        if self.world.options.randomize_bk_moves.value == RandomizeBKMoveList.option_all:
            possible_moves += 16

        assert move_hints >= min(self.world.options.signpost_move_hints.value, possible_moves,
                                 self.world.options.signpost_hints.value)


class TestClearSignpostsHints(TestSignpostsHints):
    options = {
        "hint_clarity": HintClarity.option_clear
    }

    def test_accurate_hint_text(self) -> None:
        for hint_data in self.world.hints.values():
            if not hint_data.location_id:
                continue
            hinted_location = [
                location for location in self.world.get_locations()
                if location.address == hint_data.location_id
            ][0]

            text = hint_data.text

            location = hinted_location.name
            item = hinted_location.item.name

            assert 'Your' in text
            assert location in text
            assert 'your' in text
            assert item in text


class TestClearSignpostsHintsAddAllHints(TestSignpostsHints):
    options = {
        "hint_clarity": HintClarity.option_clear,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_always
    }

    def test_should_add_hint(self) -> None:
        for hint_data in self.world.hints.values():
            if not hint_data.location_id:
                assert not hint_data.should_add_hint
            else:
                assert hint_data.should_add_hint


class TestClearSignpostsHintsAddAllProgressionHints(TestSignpostsHints):
    options = {
        "hint_clarity": HintClarity.option_clear,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_progression
    }

    def test_should_add_hint(self) -> None:
        for hint_data in self.world.hints.values():
            if not hint_data.location_id:
                assert not hint_data.should_add_hint
                continue
            hinted_location = [
                location for location in self.world.get_locations()
                if location.address == hint_data.location_id
            ][0]

            if hinted_location.item.advancement:
                assert hint_data.should_add_hint
            else:
                assert not hint_data.should_add_hint


class TestCrypticSignpostsHints(TestSignpostsHints):
    options = {
        "hint_clarity": HintClarity.option_cryptic,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_always
    }

    def test_accurate_hint_text(self) -> None:
        for hint_data in self.world.hints.values():
            if not hint_data.location_id:
                continue
            hinted_location = [
                location for location in self.world.get_locations()
                if location.address == hint_data.location_id
                and location.player == hint_data.location_player_id
            ][0]

            location = hinted_location.name

            classification_keywords = {
                ItemClassification.progression: [
                    "wonderful", "legendary one-of-a-kind", "Wahay of the Duo", "Wahay of the Archipelago"],
                ItemClassification.progression_deprioritized_skip_balancing: [
                    "Wahay of the Duo", "Wahay of the Archipelago", "great"],
                ItemClassification.useful: ["good"],
                ItemClassification.filler: ["useless"],
                ItemClassification.trap: ["bad"],
            }
            keywords = classification_keywords[hinted_location.item.classification]

            assert 'Your' in hint_data.text
            assert location in hint_data.text
            assert any([keyword in hint_data.text for keyword in keywords]), f"Item {hinted_location.item.name}\
                    should be one of these: {keywords} but was hinted: here's the full text: {hint_data.text}."
            assert not hint_data.should_add_hint


class TestClearSignpostsNoHints(TestClearSignpostsHints):
    options = {
        **TestClearSignpostsHints.options,
        "signpost_hints": 0,
        "signpost_move_hints": 0
    }


class TestClearSignpostsAllHintsHalfMoves(TestClearSignpostsHints):
    options = {
        **TestClearSignpostsHints.options,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "signpost_hints": SignpostHints.range_end,
        "signpost_move_hints": 30,
        "randomize_signposts": RandomizeSignposts.option_true
    }


class TestCrypticSignpostsNoHints(TestCrypticSignpostsHints):
    options = {
        **TestCrypticSignpostsHints.options,
        "signpost_hints": 0,
        "signpost_move_hints": 0
    }


class TestCrypticSignpostsAllHintsHalfMoves(TestCrypticSignpostsHints):
    options = {
        **TestCrypticSignpostsHints.options,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "signpost_hints": SignpostHints.range_end,
        "signpost_move_hints": 30,
        "randomize_signposts": RandomizeSignposts.option_true
    }
