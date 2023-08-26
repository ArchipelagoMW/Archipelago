import unittest
from ..MuseDashCollection import MuseDashCollections


class CollectionsTest(unittest.TestCase):
    REMOVED_SONGS = [
        "CHAOS Glitch",
        "FM 17314 SUGAR RADIO"
    ]

    def test_all_names_are_ascii(self) -> None:
        bad_names = list()
        collection = MuseDashCollections()
        for name in collection.song_items.keys():
            for c in name:
                # This is taken directly from OoT. Represents the generally excepted characters.
                if (0x20 <= ord(c) < 0x7e):
                    continue

                bad_names.append(name)
                break

        assert len(bad_names) == 0, f"Muse Dash has {len(bad_names)} songs with non-ASCII characters.\n{bad_names}"

    def test_ids_dont_change(self) -> None:
        collection = MuseDashCollections()
        items = {name: code for name, code in collection.item_names_to_id.items()}
        locations = {name: code for name, code in collection.location_names_to_id.items()}

        collection.__init__()

        for key in items.keys():
            assert items[key] == collection.item_names_to_id[key], "Item ID changed after secondary init."
        for key in locations.keys():
            assert locations[key] == collection.location_names_to_id[key], "Item ID changed after secondary init."

    def test_free_dlc_included_in_base_songs(self) -> None:
        collection = MuseDashCollections()
        songs = collection.get_songs_with_settings(False, False, 0, 11)
        assert "Glimmer" in songs, "Budget Is Burning Vol.1 is not being included in base songs"
        assert "Out of Sense" in songs, "Budget Is Burning: Nano Core is not being included in base songs"

    def test_remove_songs_are_not_generated(self) -> None:
        collection = MuseDashCollections()
        songs = collection.get_songs_with_settings(True, False, 0, 11)

        for song_name in self.REMOVED_SONGS:
            assert song_name not in songs, f"Song '{song_name}' wasn't removed correctly."
