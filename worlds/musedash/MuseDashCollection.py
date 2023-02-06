import os

from BaseClasses import ItemClassification
from .Items import MuseDashFixedItem, SongData, AlbumData
from typing import Dict, Optional, Set

def load_text_file(name: str) -> str:
    import pkgutil
    return pkgutil.get_data(__name__, "MuseDashData.txt").decode()

class MuseDashCollections:
    """Contains all the data of Muse Dash, loaded from MuseDashData.txt."""

    AlbumItems: Dict[str, AlbumData] = {}
    AlbumLocations: Dict[str, int] = {}

    SongItems: Dict[str, SongData] = {}
    SongLocations: Dict[str, int] = {}

    FreeAlbums = ["Default Music", "Budget Is Burning: Nano Core", "Budget is Burning Vol.1"]

    MusicSheetID: int

    def __init__(self, startItemID: int, itemsPerLocation: int):
        currentItemId = startItemID
        currentLocationID = startItemID

        full_file = load_text_file("MuseDashData.txt")

        for line in full_file.splitlines():
            line = line.strip()
            sections = line.split("|")

            if (sections[1] not in self.AlbumItems):
                self.AlbumItems[sections[1]] = AlbumData(currentItemId)
                currentItemId += 1

            # Data is 'Song|Album|StreamerMode|EasyDiff|HardDiff|MasterDiff|SecretDiff'
            itemName = sections[0]
            song_is_free = sections[1] in self.FreeAlbums
            steamer_mode = sections[2] == "True"

            easyDiff = self.parse_song_difficulty(sections[3])
            hardDiff = self.parse_song_difficulty(sections[4])
            masterDiff = self.parse_song_difficulty(sections[5])

            self.SongItems[itemName] = SongData(currentItemId, song_is_free, steamer_mode, easyDiff, hardDiff, masterDiff)
            currentItemId += 1

        for name in self.AlbumItems.keys():
            for i in range(0, itemsPerLocation):
                newName = "%s-%i" % (name, i)
                self.AlbumLocations[newName] = currentLocationID
                currentLocationID += 1

        for name in self.SongItems.keys():
            for i in range(0, itemsPerLocation):
                newName = "%s-%i" % (name, i)
                self.SongLocations[newName] = currentLocationID
                currentLocationID += 1

        self.MusicSheetID = currentItemId


    def get_all_songs_with_settings(self, dlcSongs: bool, streamerModeActive: bool, lowerDiffThreshold : int, higherDiffThreshold : int) -> list[str]:
        """Returns all song keys that fit the settings provided."""
        songList = list()

        for songKey, songData in self.SongItems.items():
            if (not dlcSongs and not songData.song_is_free):
                continue

            if (streamerModeActive and not songData.streamer_mode):
                continue

            if (songData.easy is not None and lowerDiffThreshold <= songData.easy <= higherDiffThreshold):
                songList.append(songKey)
                continue

            if (songData.hard is not None and lowerDiffThreshold <= songData.hard <= higherDiffThreshold):
                songList.append(songKey)
                continue

            if (songData.master is not None and lowerDiffThreshold <= songData.master <= higherDiffThreshold):
                songList.append(songKey)
                continue

        return songList


    def parse_song_difficulty(self, difficulty : str) -> Optional[int]:
        if (len(difficulty) <= 0 or difficulty == "?" or difficulty == "¿"):
            return None
        return int(difficulty)