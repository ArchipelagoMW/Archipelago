import unittest
from ..MuseDashCollection import MuseDashCollections


class CollectionsTest(unittest.TestCase):
    REMOVED_SONGS = [
        "CHAOS Glitch",
        "FM 17314 SUGAR RADIO",
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

        self.assertEqual(len(bad_names), 0, f"Muse Dash has {len(bad_names)} songs with non-ASCII characters.\n{bad_names}")

    def test_ids_dont_change(self) -> None:
        collection = MuseDashCollections()
        itemsBefore = {name: code for name, code in collection.item_names_to_id.items()}
        locationsBefore = {name: code for name, code in collection.location_names_to_id.items()}

        collection.__init__()
        itemsAfter = {name: code for name, code in collection.item_names_to_id.items()}
        locationsAfter = {name: code for name, code in collection.location_names_to_id.items()}

        self.assertDictEqual(itemsBefore, itemsAfter, "Item ID changed after secondary init.")
        self.assertDictEqual(locationsBefore, locationsAfter, "Location ID changed after secondary init.")

    def test_free_dlc_included_in_base_songs(self) -> None:
        collection = MuseDashCollections()
        songs = collection.get_songs_with_settings(False, False, 0, 11)

        self.assertIn("Glimmer", songs, "Budget Is Burning Vol.1 is not being included in base songs")
        self.assertIn("Out of Sense", songs, "Budget Is Burning: Nano Core is not being included in base songs")

    def test_remove_songs_are_not_generated(self) -> None:
        collection = MuseDashCollections()
        songs = collection.get_songs_with_settings(True, False, 0, 11)

        for song_name in self.REMOVED_SONGS:
            self.assertNotIn(song_name, songs, f"Song '{song_name}' wasn't removed correctly.")
