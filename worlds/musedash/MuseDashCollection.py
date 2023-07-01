from .Items import SongData, AlbumData
from typing import Dict, List, Optional


def load_text_file(name: str) -> str:
    import pkgutil
    return pkgutil.get_data(__name__, name).decode()


class MuseDashCollections:
    """Contains all the data of Muse Dash, loaded from MuseDashData.txt."""

    MUSIC_SHEET_CODE: int

    FREE_ALBUMS = [
        "Default Music",
        "Budget Is Burning: Nano Core",
        "Budget is Burning Vol.1"
    ]

    DIFF_OVERRIDES = [
        "MuseDash ka nanika hi",
        "Rush-Hour",
        "Find this Month's Featured Playlist",
        "PeroPero in the Universe"
    ]

    album_items: Dict[str, AlbumData] = {}
    album_locations: Dict[str, int] = {}
    song_items: Dict[str, SongData] = {}
    song_locations: Dict[str, int] = {}

    vfx_trap_items: Dict[str, int] = {
        "Bad Apple Trap": 1,
        "Pixelate Trap": 2,
        "Random Wave Trap": 3,
        "Shadow Edge Trap": 4,
        "Chromatic Aberration Trap": 5,
        "Background Freeze Trap": 6,
        "Gray Scale Trap": 7,
    }

    sfx_trap_items: Dict[str, int] = {
        "Nyaa SFX Trap": 8,
        "Error SFX Trap": 9,
    }

    def __init__(self, start_item_id: int, items_per_location: int):
        self.MUSIC_SHEET_CODE = start_item_id

        self.vfx_trap_items = {k: (v + start_item_id) for (k, v) in self.vfx_trap_items.items()}
        self.sfx_trap_items = {k: (v + start_item_id) for (k, v) in self.sfx_trap_items.items()}

        item_id_index = start_item_id + 50
        location_id_index = start_item_id

        full_file = load_text_file("MuseDashData.txt")

        for line in full_file.splitlines():
            line = line.strip()
            sections = line.split("|")

            if sections[2] not in self.album_items:
                self.album_items[sections[2]] = AlbumData(item_id_index)
                item_id_index += 1

            # Data is in the format 'Song|UID|Album|StreamerMode|EasyDiff|HardDiff|MasterDiff|SecretDiff'
            song_name = sections[0]
            # [1] is used in the client copy to make sure item id's match.
            song_is_free = sections[2] in self.FREE_ALBUMS
            steamer_mode = sections[3] == "True"

            if song_name in self.DIFF_OVERRIDES:
                # Note: These difficulties may not actually be representative of these songs.
                # The game does not provide these difficulties so they have to be filled in.
                diff_of_easy = 4
                diff_of_hard = 7
                diff_of_master = 10
            else:
                diff_of_easy = self.parse_song_difficulty(sections[4])
                diff_of_hard = self.parse_song_difficulty(sections[5])
                diff_of_master = self.parse_song_difficulty(sections[6])

            self.song_items[song_name] = SongData(item_id_index, song_is_free, steamer_mode,
                                                  diff_of_easy, diff_of_hard, diff_of_master)
            item_id_index += 1

        for name in self.album_items.keys():
            for i in range(0, items_per_location):
                new_name = f"{name}-{i}"
                self.album_locations[new_name] = location_id_index
                location_id_index += 1

        for name in self.song_items.keys():
            for i in range(0, items_per_location):
                new_name = f"{name}-{i}"
                self.song_locations[new_name] = location_id_index
                location_id_index += 1

    def get_songs_with_settings(self, dlc_songs: bool, streamer_mode_active: bool,
                                diff_lower: int, diff_higher: int) -> List[str]:
        """Gets a list of all songs that match the filter settings. Difficulty thresholds are inclusive."""
        filtered_list = []

        for songKey, songData in self.song_items.items():
            if not dlc_songs and not songData.song_is_free:
                continue

            if streamer_mode_active and not songData.streamer_mode:
                continue

            if songData.easy is not None and diff_lower <= songData.easy <= diff_higher:
                filtered_list.append(songKey)
                continue

            if songData.hard is not None and diff_lower <= songData.hard <= diff_higher:
                filtered_list.append(songKey)
                continue

            if songData.master is not None and diff_lower <= songData.master <= diff_higher:
                filtered_list.append(songKey)
                continue

        return filtered_list

    def parse_song_difficulty(self, difficulty: str) -> Optional[int]:
        """Attempts to parse the song difficulty."""
        if len(difficulty) <= 0 or difficulty == "?" or difficulty == "¿":
            return None

        # 0 is used as a filler and no songs actually have a 0 difficulty song.
        if difficulty == "0":
            return None

        # Curse the 2023 april fools update. Used on 3rd Avenue.
        if difficulty == "〇":
            return 10

        return int(difficulty)
