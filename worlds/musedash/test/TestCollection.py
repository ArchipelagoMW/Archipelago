import unittest
from ..MuseDashCollection import MuseDashCollections


class CollectionsTest(unittest.TestCase):
    def test_all_names_are_ascii(self) -> None:
        bad_names = list()
        collection = MuseDashCollections()
        for name in collection.song_items.keys():
            for c in name:
                # This is taken directly from OoT. Represents the generally excepted characters.
                if 0x20 <= ord(c) < 0x7e:
                    continue

                bad_names.append(name)
                break

        self.assertEqual(len(bad_names), 0,
                         f"Muse Dash has {len(bad_names)} songs with non-ASCII characters.\n{bad_names}")

    def test_ids_dont_change(self) -> None:
        collection = MuseDashCollections()
        items_before = {name: code for name, code in collection.item_names_to_id.items()}
        locations_before = {name: code for name, code in collection.location_names_to_id.items()}

        collection.__init__()
        items_after = {name: code for name, code in collection.item_names_to_id.items()}
        locations_after = {name: code for name, code in collection.location_names_to_id.items()}

        self.assertDictEqual(items_before, items_after, "Item ID changed after secondary init.")
        self.assertDictEqual(locations_before, locations_after, "Location ID changed after secondary init.")

    def test_free_dlc_included_in_base_songs(self) -> None:
        collection = MuseDashCollections()
        songs = collection.get_songs_with_settings(set(), False, 0, 12)

        self.assertIn("Glimmer", songs, "Budget Is Burning Vol.1 is not being included in base songs")
        self.assertIn("Out of Sense", songs, "Budget Is Burning: Nano Core is not being included in base songs")

    def test_dlcs(self) -> None:
        collection = MuseDashCollections()
        free_song_count = len(collection.get_songs_with_settings(set(), False, 0, 12))
        known_mp_song = "The Happycore Idol"

        for dlc in collection.DLC:
            songs_with_dlc = collection.get_songs_with_settings({dlc}, False, 0, 12)
            self.assertGreater(len(songs_with_dlc), free_song_count, f"DLC {dlc} did not include extra songs.")
            if dlc == collection.MUSE_PLUS_DLC:
                self.assertIn(known_mp_song, songs_with_dlc, f"Muse Plus missing muse plus song.")
            else:
                self.assertNotIn(known_mp_song, songs_with_dlc, f"DLC {dlc} includes Muse Plus songs.")

    def test_remove_songs_are_not_generated(self) -> None:
        collection = MuseDashCollections()
        songs = collection.get_songs_with_settings({x for x in collection.DLC}, False, 0, 12)

        for song_name in collection.REMOVED_SONGS:
            self.assertNotIn(song_name, songs, f"Song '{song_name}' wasn't removed correctly.")
