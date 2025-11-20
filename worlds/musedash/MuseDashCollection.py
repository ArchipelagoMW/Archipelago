from .Items import SongData
from .MuseDashData import SONG_DATA
from typing import Dict, List, Set
from collections import ChainMap


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

    # Ordering matters for webhost. Order goes: Muse Plus, Time Limited Muse Plus Dlcs, Paid Dlcs
    DLC: List[str] = [
        MUSE_PLUS_DLC,
        "CHUNITHM COURSE MUSE",  # Part of Muse Plus. Goes away 22nd May 2027.
        "maimai DX Limited-time Suite",  # Part of Muse Plus. Goes away 31st Jan 2026.
        "MSR Anthology",  # Goes away January 26, 2026. 
        "Miku in Museland",  # Paid DLC not included in Muse Plus
        "Rin Len's Mirrorland",  # Paid DLC not included in Muse Plus
        "MSR Anthology_Vol.02", # Goes away January 26, 2026. 
    ]

    REMOVED_SONGS = [
        "CHAOS Glitch",
        "FM 17314 SUGAR RADIO",
        "Yume Ou Mono Yo Secret",
        "Echo over you... Secret",
        "Tsukuyomi Ni Naru Replaced",
        "Heart Message feat. Aoi Tokimori Secret",
        "Meow Rock feat. Chun Ge, Yuan Shen",
    ]

    song_items = SONG_DATA
    song_locations: Dict[str, int] = {}

    trap_items: Dict[str, int] = {
        "Bad Apple Trap": STARTING_CODE + 1,
        "Pixelate Trap": STARTING_CODE + 2,
        "Ripple Trap": STARTING_CODE + 3,
        "Vignette Trap": STARTING_CODE + 4,
        "Chromatic Aberration Trap": STARTING_CODE + 5,
        "Background Freeze Trap": STARTING_CODE + 6,
        "Gray Scale Trap": STARTING_CODE + 7,
        "Nyaa SFX Trap": STARTING_CODE + 8,
        "Error SFX Trap": STARTING_CODE + 9,
        "Focus Line Trap": STARTING_CODE + 10,
        "Beefcake SFX Trap": STARTING_CODE + 11,
    }

    sfx_trap_items: List[str] = [
        "Nyaa SFX Trap",
        "Error SFX Trap",
        "Beefcake SFX Trap",
    ]

    filler_items: Dict[str, int] = {
        "Great To Perfect (10 Pack)": STARTING_CODE + 30,
        "Miss To Great (5 Pack)": STARTING_CODE + 31,
        "Extra Life": STARTING_CODE + 32,
    }

    filler_item_weights: Dict[str, int] = {
        "Great To Perfect (10 Pack)": 10,
        "Miss To Great (5 Pack)": 3,
        "Extra Life": 1,
    }

    item_names_to_id: ChainMap = ChainMap({k: v.code for k, v in SONG_DATA.items()}, filler_items, trap_items)
    location_names_to_id: ChainMap = ChainMap(song_locations)

    def __init__(self) -> None:
        self.item_names_to_id[self.MUSIC_SHEET_NAME] = self.MUSIC_SHEET_CODE

        location_id_index = self.STARTING_CODE
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

            if songKey in self.REMOVED_SONGS:
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

    def filter_songs_to_dlc(self, song_list: List[str], dlc_songs: Set[str]) -> List[str]:
        return [song for song in song_list if self.song_matches_dlc_filter(self.song_items[song], dlc_songs)]

    def song_matches_dlc_filter(self, song: SongData, dlc_songs: Set[str]) -> bool:
        if song.album in self.FREE_ALBUMS:
            return True

        if song.album in dlc_songs:
            return True

        # Muse Plus provides access to any DLC not included as a seperate pack
        if song.album not in self.DLC and self.MUSE_PLUS_DLC in dlc_songs:
            return True

        return False
