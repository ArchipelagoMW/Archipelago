import unittest
from ..MuseDashCollection import MuseDashCollections


class NamesTest(unittest.TestCase):
    def test_all_names_are_ascii(self) -> None:
        bad_names = list()
        collection = MuseDashCollections(0, 1)
        for name in collection.SongItems.keys():
            for c in name:
                if (0 <= ord(c) <= 127):
                    continue

                bad_names.append(name)
                break

        assert len(bad_names) == 0, f"Muse Dash has {len(bad_names)} songs with non-ASCII characters.\n{bad_names}"