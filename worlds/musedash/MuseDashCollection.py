import os

from BaseClasses import ItemClassification
from .Items import MuseDashFixedItem, SongData, AlbumData
from typing import Dict

class MuseDashCollections:
    AlbumItems: Dict[str, AlbumData] = {}
    AlbumLocations: Dict[str, int] = {}

    BaseSongItems: Dict[str, SongData] = {}
    BaseSongLocations: Dict[str, int] = {}

    SongItems: Dict[str, SongData] = {}
    SongLocations: Dict[str, int] = {}

    def __init__(self, startItemID: int, itemsPerLocation: int):
        currentItemId = startItemID
        currentLocationID = startItemID

        albumPath = os.path.join(os.path.dirname(__file__), "Albums.txt")
        with open(albumPath, "r", encoding="utf-8") as file:
            for line in file.readlines():
                line = line.strip()
                self.AlbumItems[line] = AlbumData(currentItemId)
                currentItemId += 1

        for i in range(0, itemsPerLocation):
            for name in self.AlbumItems.keys():
                newName = "%s-%i" % (name, i)
                self.AlbumLocations[newName] = currentLocationID
                currentLocationID += 1

        songPath = os.path.join(os.path.dirname(__file__), "Songs.txt")
        with open(songPath, "r", encoding="utf-8") as file:
            for line in file.readlines():
                line = line.strip()
                sections = line.split("|")
                self.SongItems[sections[0]] = SongData(currentItemId, sections[1], sections[2], sections[3], sections[4])
                currentItemId += 1

        for i in range(0, itemsPerLocation):
            for name in self.SongItems.keys():
                newName = "%s-%i" % (name, i)
                self.SongLocations[newName] = currentLocationID
                currentLocationID += 1

        #Prepare information for songs outside the Just as Planned DLC
        songPath = os.path.join(os.path.dirname(__file__), "BaseSongs.txt")
        with open(songPath, "r", encoding="utf-8") as file:
            for line in file.readlines():
                line = line.strip()
                sections = line.split("|")
                self.BaseSongItems[sections[0]] = self.SongItems[sections[0]]

        for i in range(0, itemsPerLocation):
            for name in self.BaseSongItems.keys():
                newName = "%s-%i" % (name, i)
                self.BaseSongLocations[newName] = self.SongLocations[newName]

        self.VictoryItemID = currentItemId
        self.EmptyItemID = currentItemId + 1

    def create_empty_item(self, player) -> MuseDashFixedItem:
        return MuseDashFixedItem("Nothing", ItemClassification.filler, player, self.EmptyItemID)

    def create_victory_item(self, player) -> MuseDashFixedItem:
        return MuseDashFixedItem("Victory", ItemClassification.progression, player, self.VictoryItemID)
