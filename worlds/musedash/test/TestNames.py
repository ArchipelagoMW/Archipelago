import unittest
from ..MuseDashCollection import MuseDashCollections


class NamesTest(unittest.TestCase):
    def test_all_names_are_ascii(self) -> None:
        bad_names = list()
        collection = MuseDashCollections(0, 1)
        for name in collection.song_items.keys():
            for c in name:
                # This is taken directly from OoT. This represents probably the minimum set of characters before a game handles their own text.
                if (0x20 <= ord(c) < 0x7e):
                    continue

                bad_names.append(name)
                break

        assert len(bad_names) == 0, f"Muse Dash has {len(bad_names)} songs with non-ASCII characters.\n{bad_names}"
