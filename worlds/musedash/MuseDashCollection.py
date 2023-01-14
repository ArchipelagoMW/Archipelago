import os

from BaseClasses import ItemClassification
from .Items import MuseDashFixedItem, SongData, AlbumData
from typing import Dict, Optional

class MuseDashCollections:
    """Contains all the data of Muse Dash, loaded from MuseDashData.txt."""

    AlbumItems: Dict[str, AlbumData] = {}
    AlbumLocations: Dict[str, int] = {}

    SongItems: Dict[str, SongData] = {}
    SongLocations: Dict[str, int] = {}

    def __init__(self, startItemID: int, itemsPerLocation: int):
        currentItemId = startItemID
        currentLocationID = startItemID

        dataPath = os.path.join(os.path.dirname(__file__), "MuseDashData.txt")
        with open(dataPath, "r", encoding="utf-8") as file:
            for line in file.readlines():
                line = line.strip()
                sections = line.split("|")

                if (sections[1] not in self.AlbumItems):
                    self.AlbumItems[sections[1]] = AlbumData(currentItemId)
                    currentItemId += 1

                # Data is 'Song|Album|StreamerMode|EasyDiff|HardDiff|MasterDiff|SecretDiff'
                itemName = "%s[%s]" % (sections[0], sections[1])
                song_is_default = sections[1] == "Default Music" # All DLC songs have a different album
                steamer_mode = sections[2] == "True"

                easyDiff = self.parse_song_difficulty(sections[3])
                hardDiff = self.parse_song_difficulty(sections[4])
                masterDiff = self.parse_song_difficulty(sections[5])

                self.SongItems[itemName] = SongData(currentItemId, song_is_default, steamer_mode, easyDiff, hardDiff, masterDiff)
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

        self.VictoryItemID = currentItemId
        self.EmptyItemID = currentItemId + 1


    def get_all_songs_with_settings(self, dlcSongs: bool, streamerModeActive: bool, lowerDiffThreshold : int, higherDiffThreshold : int) -> list[str]:
        """Returns all song keys that fit the settings provided."""
        songList = list()

        for songKey, songData in self.SongItems.items():
            if (dlcSongs and not songData.default_song):
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

    def create_empty_item(self, player) -> MuseDashFixedItem:
        return MuseDashFixedItem("Nothing", ItemClassification.filler, player, self.EmptyItemID)


    def create_victory_item(self, player) -> MuseDashFixedItem:
        return MuseDashFixedItem("Victory", ItemClassification.progression, player, self.VictoryItemID)