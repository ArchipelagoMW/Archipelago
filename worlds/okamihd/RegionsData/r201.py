from typing import TYPE_CHECKING

from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SEIAN_CITY_COMMONERS_DRY: [
        ExitData(RegionNames.SEIAN_CITY_COMMONERS, required_items_events=["Imperial Palace - Defeat Blight"],
                 loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_WEAPON_SHOP, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_TOOL_SHOP, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_FLOWERS),
        ExitData(RegionNames.SEIAN_CITY_BRIDGE_COMMONERS)
    ],
    RegionNames.SEIAN_CITY_COMMONERS: [
        ExitData(RegionNames.SEIAN_CITY_YAMA),
        ExitData(RegionNames.SEIAN_CITY_SOUTHWEST,
                 required_items_events=["Sei-an City (Commoner's Quarter) - Blow up wall to southwest building"]),
        ExitData(RegionNames.SEIAN_CITY_TAO,
                 required_items_events=["Sei-an City (Commoner's Quarter) - Climb to Tao Troopers Headquarters"],
                 one_way=True, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_BLOSSOM),
        ExitData(RegionNames.SEIN_CITY_KIMONO)
    ],
    RegionNames.SEIAN_CITY_TAO: [
        ExitData(RegionNames.SEIAN_CITY_COMMONERS, one_way=True)
    ]
}
events = {

    RegionNames.SEIAN_CITY_COMMONERS_DRY: {
        "Sei-an City (Commoner's Quarter) - Dig water source": EventData(type=LocationType.DIGGING_MINIGAME_LATER),
    },
    RegionNames.SEIAN_CITY_COMMONERS: {
        "Sei-an City (Commoner's Quarter) - Blow up wall to southwest building": EventData(cherry_bomb_level=1),
        "Sei-an City (Commoner's Quarter) - Climb to Tao Troopers Headquarters": EventData(
            required_brush_techniques=[BrushTechniques.WATERSPOUT],required_items_events=["Sei-an City (Commoner's Quarter) - Dig water source"])
    },
    RegionNames.SEIAN_CITY_YAMA: {
        "Sei-an City (Commoner's Quarter) - Give golden mushroom to Yama": EventData(
            required_items_events=["Golden Mushroom"])
    }
}
locations = {
    # Always mark chests in Canal as underwater in case the water has been returned.
    RegionNames.SEIAN_CITY_COMMONERS_DRY: {
        "Sei-an City (Commoner's quarter) - Northern Chest in West Canal": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 0), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in western Canal near water source": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 1), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in eastern Canal empty Ferry Stop": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 3), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Southern Chest in eastern Canal near bridge": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 4), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in eastern canal under balcony": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 5), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in western Canal between bridge and ferry spot": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 6), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in western canal north of ferry spot": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 7), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Southern chest in western Canal": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 8), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in Eastern Canal near stairs to Mr Flower's house": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 10), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Commoner's quarter) - Buried chest Chest near west ferry spot": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 11), type=LocationType.BURIED_CHEST),
        "Sei-an City (Commoner's quarter) - Buried chest near east wall": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 12), type=LocationType.BURIED_CHEST),
        "Sei-an City (Commoner's quarter) - Freestanding chest west of Ryoshima entrance": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 13)),
        "Sei-an City (Commoner's quarter) - Buried Chest behind Mr. Flower's house": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 17),type=LocationType.BURIED_CHEST),
        "Sei-an City (Commoner's quarter) - Chest in canal northeast corner": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 21)),
        "Sei-an City (Commoner's quarter) - Freestanding chest behind Aspiring Carpenter's house": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 22)),
        "Sei-an City (Commoner's quarter) - Chest east of Aristocratic quarters entrance": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 23)),
    },
    RegionNames.SEIAN_CITY_YAMA: {
        "Sei-an City (Commoner's quarter) - Chest after learning Fireburst": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 2),
            required_items_events=["Sei-an City (Commoner's Quarter) - Give golden mushroom to Yama"]),
        "Sei-an City (Commoner's quarter) - Moegami(Fireburst)": LocData(brush_check_id(11), required_items_events=[
            "Sei-an City (Commoner's Quarter) - Give golden mushroom to Yama"])

    },
    RegionNames.SEIAN_CITY_FLOWERS: {
        "Sei-an City (Commoner's quarter) - Chest Buried in Mr Flower's house": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 9), type=LocationType.BURIED_CHEST),
    },
    RegionNames.SEIAN_CITY_SOUTHWEST: {
        "Sei-an City (Commoner's quarter) - Chest in southwest building, 1F southwest Rafters": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 24)),
        "Sei-an City (Commoner's quarter) - Chest in southwest building, GF Freestanding Left": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 25)),
        "Sei-an City (Commoner's quarter) - Chest in southwest building, GF Freestanding Right": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 29)),
        "Sei-an City (Commoner's quarter) - Chest in southwest building, 2F northwest Rafters Left": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 26)),
        "Sei-an City (Commoner's quarter) - Chest in southwest building, 2F northwest Rafters Right": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 27)),
        "Sei-an City (Commoner's quarter) - Chest in southwest building, 2F north Rafters": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 28)),
        "Sei-an City (Commoner's quarter) - Chest in southwest building, GF in Cage": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 30)),
        "Sei-an City (Commoner's quarter) - Chest in southwest building, GF near Cage": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 31)),
    },
    RegionNames.SEIAN_CITY_COMMONERS: {
        "Sei-an City (Commoner's quarter) - Freestanding Chest behind west buildings": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 32)),
        "Sei-an City (Commoner's quarter) - Buried Chest near west buildings": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 33), type=LocationType.BURIED_CHEST),
        "Sei-an City (Commoner's quarter) - Buried Chest near Yama's restaurant": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 34), type=LocationType.BURIED_CHEST),

    },
    RegionNames.SEIAN_CITY_TAO: {
        "Sei-an City (Commoner's quarter) - Freestanding chest behind Tao Troopers headquarters": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 44)),
    },
    RegionNames.SEIAN_CITY_BLOSSOM: {
        "Sei-an City (Commoner's quarter) - Chest in Blossom's house": LocData(
            container_check_id(MapIds.SEIAN_COMMONERS, 45), cherry_bomb_level=1)
    }
}
shop_locations = {
    RegionNames.SEIAN_CITY_TOOL_SHOP: {
        "Sei-an City - Tool Shop Slot 1": LocData(shop_check_id(16, 0), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 2": LocData(shop_check_id(16, 1), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 3": LocData(shop_check_id(16, 2), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 4": LocData(shop_check_id(16, 3), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 5": LocData(shop_check_id(16, 4), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 6": LocData(shop_check_id(16, 5), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 7": LocData(shop_check_id(16, 6), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 8": LocData(shop_check_id(16, 7), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 9": LocData(shop_check_id(16, 8), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 10": LocData(shop_check_id(16, 9), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 11": LocData(shop_check_id(16, 10), type=LocationType.SHOP),
        "Sei-an City - Tool Shop Slot 12": LocData(shop_check_id(16, 11), type=LocationType.SHOP)
    },
    RegionNames.SEIAN_CITY_WEAPON_SHOP: {
        "Sei-an City - Weapon Shop Slot 1": LocData(shop_check_id(17, 0), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 2": LocData(shop_check_id(17, 1), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 3": LocData(shop_check_id(17, 2), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 4": LocData(shop_check_id(17, 3), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 5": LocData(shop_check_id(17, 4), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 6": LocData(shop_check_id(17, 5), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 7": LocData(shop_check_id(17, 6), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 8": LocData(shop_check_id(17, 7), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 9": LocData(shop_check_id(17, 8), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 10": LocData(shop_check_id(17, 9), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 11": LocData(shop_check_id(17, 10), type=LocationType.SHOP),
        "Sei-an City - Weapon Shop Slot 12": LocData(shop_check_id(17, 11), type=LocationType.SHOP),
    }
}
