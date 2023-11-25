from .Items import SongData, AlbumData
from typing import Dict, List, Set, Optional
from collections import ChainMap


def load_text_file(name: str) -> str:
    import pkgutil
    return pkgutil.get_data(__name__, name).decode()


class MuseDashCollections:
    """Contains all the data of Muse Dash, loaded from MuseDashData.txt."""
    STARTING_CODE = 2900000

    MUSIC_SHEET_NAME: str = "Music Sheet"
    MUSIC_SHEET_CODE: int = STARTING_CODE

    FREE_ALBUMS: List[str] = [
        "Default Music",
        "Budget Is Burning: Nano Core",
        "Budget Is Burning Vol.1",
    ]

    MUSE_PLUS_DLC: str = "Muse Plus"
    DLC: List[str] = [
        # MUSE_PLUS_DLC, # To be included when OptionSets are rendered as part of basic settings.
        # "maimai DX Limited-time Suite", # Part of Muse Plus. Goes away 31st Jan 2026.
        "Miku in Museland", # Paid DLC not included in Muse Plus
        "MSR Anthology", # Part of Muse Plus. Goes away 20th Jan 2024.
    ]

    DIFF_OVERRIDES: List[str] = [
        "MuseDash ka nanika hi",
        "Rush-Hour",
        "Find this Month's Featured Playlist",
        "PeroPero in the Universe",
    ]

    album_items: Dict[str, AlbumData] = {}
    album_locations: Dict[str, int] = {}
    song_items: Dict[str, SongData] = {}
    song_locations: Dict[str, int] = {}

    vfx_trap_items: Dict[str, int] = {
        "Bad Apple Trap": STARTING_CODE + 1,
        "Pixelate Trap": STARTING_CODE + 2,
        "Ripple Trap": STARTING_CODE + 3,
        "Vignette Trap": STARTING_CODE + 4,
        "Chromatic Aberration Trap": STARTING_CODE + 5,
        "Background Freeze Trap": STARTING_CODE + 6,
        "Gray Scale Trap": STARTING_CODE + 7,
    }

    sfx_trap_items: Dict[str, int] = {
        "Nyaa SFX Trap": STARTING_CODE + 8,
        "Error SFX Trap": STARTING_CODE + 9,
    }

    item_names_to_id: ChainMap = ChainMap({}, sfx_trap_items, vfx_trap_items)
    location_names_to_id: ChainMap = ChainMap(song_locations, album_locations)

    def __init__(self) -> None:
        self.item_names_to_id[self.MUSIC_SHEET_NAME] = self.MUSIC_SHEET_CODE

        item_id_index = self.STARTING_CODE + 50
        full_file = load_text_file("MuseDashData.txt")
        seen_albums = set()
        for line in full_file.splitlines():
            line = line.strip()
            sections = line.split("|")

            album = sections[2]
            if album not in seen_albums:
                seen_albums.add(album)
                self.album_items[album] = AlbumData(item_id_index)
                item_id_index += 1

            # Data is in the format 'Song|UID|Album|StreamerMode|EasyDiff|HardDiff|MasterDiff|SecretDiff'
            song_name = sections[0]
            # [1] is used in the client copy to make sure item id's match.
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

            self.song_items[song_name] = SongData(item_id_index, album, steamer_mode,
                                                  diff_of_easy, diff_of_hard, diff_of_master)
            item_id_index += 1

        self.item_names_to_id.update({name: data.code for name, data in self.song_items.items()})
        self.item_names_to_id.update({name: data.code for name, data in self.album_items.items()})

        location_id_index = self.STARTING_CODE
        for name in self.album_items.keys():
            self.album_locations[f"{name}-0"] = location_id_index
            self.album_locations[f"{name}-1"] = location_id_index + 1
            location_id_index += 2

        for name in self.song_items.keys():
            self.song_locations[f"{name}-0"] = location_id_index
            self.song_locations[f"{name}-1"] = location_id_index + 1
            location_id_index += 2

    def get_songs_with_settings(self, dlc_songs: Set[str], streamer_mode_active: bool,
                                diff_lower: int, diff_higher: int) -> List[str]:
        """Gets a list of all songs that match the filter settings. Difficulty thresholds are inclusive."""
        filtered_list = []

        for songKey, songData in self.song_items.items():
            if not self.song_matches_dlc_filter(songData, dlc_songs):
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

    def song_matches_dlc_filter(self, song: SongData, dlc_songs: Set[str]) -> bool:
        if song.album in self.FREE_ALBUMS:
            return True

        if song.album in dlc_songs:
            return True

        # Muse Plus provides access to any DLC not included as a seperate pack
        if song.album not in self.DLC and self.MUSE_PLUS_DLC in dlc_songs:
            return True

        return False

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
