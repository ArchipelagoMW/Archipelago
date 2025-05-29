from typing import cast

from Fill import distribute_items_restrictive

from worlds.AutoWorld import call_all
from worlds.witness import WitnessWorld
from worlds.witness.test import WitnessMultiworldTestBase


class TestDisabledAudioLogs(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "shuffle_postgame": False,
            "disable_non_randomized_puzzles": False,
        },
        {
            "shuffle_postgame": False,
            "disable_non_randomized_puzzles": True,
        },
        {
            "shuffle_postgame": True,
            "disable_non_randomized_puzzles": False,
        },
        {
            "shuffle_postgame": True,
            "disable_non_randomized_puzzles": True,
        },
    ]

    common_options = {
        "victory_condition": "mountain_box_short",
        "shuffle_doors": "off",
        "hint_amount": 49,
    }

    def setUp(self) -> None:
        super().setUp()
        distribute_items_restrictive(self.multiworld)
        call_all(self.multiworld, "fill_slot_data")

    def test_disabled_audio_logs(self) -> None:
        worlds = [cast(WitnessWorld, world) for world in self.multiworld.worlds.values()]

        with self.subTest(
            "Check that shuffle_postgame and disable_non_randomized disable the correct amount of Audio Logs and that "
            'the "hint_amount" option was appropriately adjusted'
        ):
            for player, expected_audio_log_amount in zip([0, 1, 2, 3], [36, 32, 49, 45]):
                self.assertEqual(worlds[player].options.hint_amount, expected_audio_log_amount)

        town_obelisk_audio_log = 0x015B7
        monastery_audio_log = 0x3C106
        tunnels_audio_log = 0x3C105

        with self.subTest(
            "Check that disabled Audio Logs had junk hints put on them, and vice versa.",
            options=self.options_per_world[0]
        ):
            self.assertTrue(worlds[0].log_ids_to_hints[town_obelisk_audio_log][0])
            self.assertTrue(worlds[0].log_ids_to_hints[monastery_audio_log][0])
            self.assertFalse(worlds[0].log_ids_to_hints[tunnels_audio_log][0])

        with self.subTest(
            "Check that disabled Audio Logs had junk hints put on them, and vice versa.",
            options=self.options_per_world[1]
        ):
            self.assertTrue(worlds[1].log_ids_to_hints[town_obelisk_audio_log][0])
            self.assertFalse(worlds[1].log_ids_to_hints[monastery_audio_log][0])
            self.assertFalse(worlds[1].log_ids_to_hints[tunnels_audio_log][0])

        with self.subTest(
            "Check that disabled Audio Logs had junk hints put on them, and vice versa.",
            options=self.options_per_world[2]
        ):
            self.assertTrue(worlds[2].log_ids_to_hints[town_obelisk_audio_log][0])
            self.assertTrue(worlds[2].log_ids_to_hints[monastery_audio_log][0])
            self.assertTrue(worlds[2].log_ids_to_hints[tunnels_audio_log][0])

        with self.subTest(
            "Check that disabled Audio Logs had junk hints put on them, and vice versa.",
            options=self.options_per_world[3]
        ):
            self.assertTrue(worlds[3].log_ids_to_hints[town_obelisk_audio_log][0])
            self.assertFalse(worlds[3].log_ids_to_hints[monastery_audio_log][0])
            self.assertTrue(worlds[3].log_ids_to_hints[tunnels_audio_log][0])
