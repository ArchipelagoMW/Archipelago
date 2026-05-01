from typing import TYPE_CHECKING

from ..CheckIds import brush_check_id, container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames
from ..Rules import night_time_check_rule
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SHINSHU_FIELD: [
        ExitData("Cross Cave to Agata Forest", RegionNames.SHINSHU_FIELD_AGATA_CAVE, needs_long_swim=True),
        ExitData("Enter Tama's house", RegionNames.TAMA_HOUSE),
        ExitData("To Moon Cave Entrance",RegionNames.MOON_CAVE_OUTSIDE)],
    RegionNames.SHINSHU_FIELD_AGATA_CAVE: [ExitData('To Cursed Agata Forest', RegionNames.CURSED_AGATA_FOREST,
                                                    has_events=["Shinshu Field - Open Entrance to Agata Forest"])]
}
events = {
    RegionNames.SHINSHU_FIELD_AGATA_CAVE: {
        "Shinshu Field - Open Entrance to Agata Forest": EventData(cherry_bomb_level=1)
    }
}
locations = {
    RegionNames.SHINSHU_FIELD: {
        "Shinshu Field - Buried chest near Guardian Sapling": LocData(container_check_id(0xF02, 7), type=LocationType.BURIED_CHEST),
        "Shinshu Field - Freestanding chest behind Guardian Sapling": LocData(container_check_id(0xF02, 11)),
        "Shinshu Field - Buried chest near Tama's house": LocData(container_check_id(0xF02, 26), type=LocationType.BURIED_CHEST),
        "Shinshu Field - Buried chest near Lake": LocData(container_check_id(0xF02, 30), type=LocationType.BURIED_CHEST),
        "Shinshu Field - Chest Under Bombable ground near Agata Forest": LocData(container_check_id(0xF02, 36), cherry_bomb_level=1,
                                                                                 required_brush_techniques=[
                                                                                     BrushTechniques.GREENSPROUT_BLOOM]),
        "Shinshu Field - Buried chest near Dojo": LocData(container_check_id(0xF02, 42), type=LocationType.BURIED_CHEST),
        "Shinshu Field - Chest after devil gate": LocData(container_check_id(0xF02, 47), mandatory_enemies=[OkamiEnemies.GREEN_IMP,
                                                                                 OkamiEnemies.RED_IMP,
                                                                                 OkamiEnemies.YELLOW_IMP]),
        # Probably should find a better name for this one
        "Shinshu Field - Buried chest on ledge": LocData(container_check_id(0xF02, 50), type=LocationType.BURIED_CHEST),
        "Shinshu Field - Buried chest near Ovens": LocData(container_check_id(0xF02, 78), type=LocationType.BURIED_CHEST),
        # This is the cherry bomb tutorial. Need to check what happens if you blow the wall before doing the tutorial.
        "Shinshu Field - In Bombable cave near Tama's house": LocData(container_check_id(0xF02, 82), cherry_bomb_level=1),
        "Shinshu Field - In Bombable cave near cat statue": LocData(container_check_id(0xF02, 83), cherry_bomb_level=1),
        "Shinshu Field - Buried Chest in leaf pile near Tama's house": LocData(container_check_id(0xF02, 86),
                                                                               type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Shinshu Field - Chest on Big Torii": LocData(container_check_id(0xF02, 89), required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Shinshu Field - Freestanding chest in front of guardian sapling": LocData(container_check_id(0xF02, 95)),
        "Shinshu Field - Freestanding chest near Agata Forest Cave": LocData(container_check_id(0xF02, 96)),
        "Shinshu Field - Freestanding chest near Tama's house": LocData(container_check_id(0xF02, 117)),
        "Shinshu Field - Buried Chest in burning leaf pile behind Dojo": LocData(container_check_id(0xF02, 118), type=LocationType.BURIED_UNDER_LEAF_PILE)
    },

    RegionNames.TAMA_HOUSE: {
        "Shinshu Field - Bakigami": LocData(brush_check_id(25),type=LocationType.CONSTELLATION,special_rule=lambda s,w:night_time_check_rule(s,w))  # bit 25
    }
}

# These are added separately and conditionally created based on RandomizeShops option
shop_locations = {
    RegionNames.SHINSHU_FIELD: {
        "Shinshu Field - Shop Slot 1": LocData(shop_check_id(18, 0), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 2": LocData(shop_check_id(18, 1), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 3": LocData(shop_check_id(18, 2), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 4": LocData(shop_check_id(18, 3), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 5": LocData(shop_check_id(18, 4), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 6": LocData(shop_check_id(18, 5), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 7": LocData(shop_check_id(18, 6), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 8": LocData(shop_check_id(18, 7), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 9": LocData(shop_check_id(18, 8), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 10": LocData(shop_check_id(18, 9), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 11": LocData(shop_check_id(18, 10), type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 12": LocData(shop_check_id(18, 11), type=LocationType.SHOP),
    }
}
