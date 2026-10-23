import unittest
from types import SimpleNamespace

from ..music import default_music, music_pointers, randomize_map_music
from ..regions import map_ids
from ..rom_addresses import rom_addresses


class RecordingWriter:
    def __init__(self) -> None:
        self.writes = {}

    def __call__(self, address: int, data) -> None:
        self.writes[address] = data


class ReverseShuffleRandom:
    def shuffle(self, sequence) -> None:
        sequence.reverse()


class FirstThenSecondChoiceRandom:
    def __init__(self) -> None:
        self.calls = 0

    def choice(self, sequence):
        self.calls += 1
        return sequence[0] if self.calls == 1 else sequence[1]


def make_world(mode: str, rng) -> SimpleNamespace:
    return SimpleNamespace(
        options=SimpleNamespace(randomize_map_music=mode),
        random=rng,
    )


def read_pointer(song_table: bytes, map_name: str) -> int:
    map_id = map_ids[map_name]
    return int.from_bytes(song_table[map_id * 2:(map_id * 2) + 2], byteorder="big")


class TestMapMusicRandomization(unittest.TestCase):
    def test_vanilla_music_leaves_rom_data_untouched(self) -> None:
        writer = RecordingWriter()

        randomize_map_music(make_world("vanilla", ReverseShuffleRandom()), writer)

        self.assertEqual({}, writer.writes)

    def test_shuffle_remaps_music_by_default_track_groups(self) -> None:
        writer = RecordingWriter()

        randomize_map_music(make_world("shuffle", ReverseShuffleRandom()), writer)
        song_table = bytes(writer.writes[rom_addresses["Map_Songs"]])

        shuffled_tracks = list(music_pointers.keys())
        shuffled_tracks.reverse()
        expected_mapping = dict(zip(music_pointers.keys(), shuffled_tracks))
        actual_pointers = {
            map_name: read_pointer(song_table, map_name)
            for map_name in default_music
        }
        expected_pointers = {
            map_name: music_pointers[expected_mapping[default_track]]
            for map_name, default_track in default_music.items()
        }

        self.assertEqual(expected_pointers, actual_pointers)

    def test_randomize_picks_music_per_map_instead_of_per_default_track(self) -> None:
        rng = FirstThenSecondChoiceRandom()
        writer = RecordingWriter()

        randomize_map_music(make_world("randomize", rng), writer)
        song_table = bytes(writer.writes[rom_addresses["Map_Songs"]])

        first_pointer, second_pointer = list(music_pointers.values())[:2]

        self.assertEqual(len(default_music), rng.calls)
        self.assertEqual(first_pointer, read_pointer(song_table, "Pallet Town"))
        self.assertEqual(second_pointer, read_pointer(song_table, "Viridian City"))
        self.assertEqual(second_pointer, read_pointer(song_table, "Player's House 1F"))
        self.assertNotEqual(
            read_pointer(song_table, "Pallet Town"),
            read_pointer(song_table, "Player's House 1F"),
        )

    def test_chaos_mode_enables_option_and_writes_full_pointer_table(self) -> None:
        writer = RecordingWriter()

        randomize_map_music(make_world("chaos", ReverseShuffleRandom()), writer)

        self.assertEqual([0, 0], writer.writes[rom_addresses["Option_Chaos_Music"]])
        self.assertEqual(len(music_pointers), writer.writes[rom_addresses["Chaos_Music_Quantity"]])

        song_table = bytes(writer.writes[rom_addresses["Map_Songs"]])
        expected_prefix = b"".join(
            pointer.to_bytes(2, byteorder="big")
            for pointer in music_pointers.values()
        )

        self.assertEqual(0x1EE, len(song_table))
        self.assertTrue(song_table.startswith(expected_prefix))
        self.assertEqual(bytes(len(song_table) - len(expected_prefix)), song_table[len(expected_prefix):])
