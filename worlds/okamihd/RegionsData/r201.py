from typing import TYPE_CHECKING

from ..CheckIds import container_check_id, brush_check_id
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SEIAN_CITY_COMMONERS_DRY:[
        ExitData(RegionNames.SEIAN_CITY_COMMONERS,has_events="Inside the Emperor - Defeat Blight")
    ],
    RegionNames.SEIAN_CITY_COMMONERS:[
        ExitData(RegionNames.SEIAN_CITY_YAMA),
        ExitData(RegionNames.SEIAN_CITY_FLOWERS),
        ExitData(RegionNames.SEIAN_CITY_SOUTHWEST,has_events=["Sei-an City - Blow up wall to southwest building"])
    ]
}
events = {
    #FIXME: temporary placed here to ensure everything is acessible
    RegionNames.SEIAN_CITY_COMMONERS_DRY:{
        "Inside the Emperor - Defeat Blight":EventData()
    },

    RegionNames.SEIAN_CITY_COMMONERS:{
        "Sei-an City - Blow up wall to southwest building": EventData(cherry_bomb_level=1)
    },
    RegionNames.SEIAN_CITY_YAMA: {
        "Sei-an City (Commoner's Quarter) - Give golden mushroom to Yama": EventData(
            required_items_events=["Golden Mushroom"])
    }
}
locations = {
    # TODO: Make some names clearer
    # Always mark chests in Canal as underwater in case the water has been returned.
    RegionNames.SEIAN_CITY_COMMONERS_DRY: {
        "Sei-an City (Commoner's quarter) - Chest in Canal near Yellow Kimono lady": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 0), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal near Naguri": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 1), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal near empty Ferry Stop": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 3), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal near bridge": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 4), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal under balcony": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 5), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal near west bridge": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 6), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal in northwest corner": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 7), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal near southeast bridge": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 8), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal near stairs": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 10), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Buried chest Chest near bridge": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 11), type=LocationType.BURIED_CHEST),
        "Sei-an City (Commoner's quarter) - Buried chest near east wall": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 12), type=LocationType.BURIED_CHEST),
        "Sei-an City (Commoner's quarter) - Freestanding chest near Ryoshima entrance": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 13)),
        "Sei-an City (Commoner's quarter) - Buried Chest behind Mr. Flower's house": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 14),type=LocationType.BURIED_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Canal near Mr. Flower's house": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 15),type=LocationType.BURIED_CHEST),
        "Sei-an City (Commoner's quarter) - Freestanding Chest behind building": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 16)),
        "Sei-an City (Commoner's quarter) - Freestanding Chest near Ryoshima entrance 2": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 17)),
    },
    RegionNames.SEIAN_CITY_YAMA: {
        "Sei-an City (Commoner's quarter) - Chest after learning Fireburst": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 2),
            required_items_events=["Sei-an City (Commoner's Quarter) - Give golden mushroom to Yama"]),
        "Sei-an City (Commoner's quarter) - Moegami(Fireburst)": LocData(brush_check_id(11), required_items_events=[
            "Sei-an City (Commoner's Quarter) - Give golden mushroom to Yama"])

    },
    RegionNames.SEIAN_CITY_FLOWERS:{
        "Sei-an City (Commoner's quarter) - Chest Buried in Mr Flower's house": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 9), type=LocationType.BURIED_CHEST),
    }
}
shop_locations = {
}
