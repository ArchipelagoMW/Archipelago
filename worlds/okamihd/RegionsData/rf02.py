from typing import TYPE_CHECKING

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
        "Shinshu Field - Buried chest near Guardian Sapling": LocData(1883559, type=LocationType.BURIED_CHEST),
        "Shinshu Field - Freestanding chest behind Guardian Sapling": LocData(1883563),
        "Shinshu Field - Buried chest near Tama's house": LocData(1883578, type=LocationType.BURIED_CHEST),
        "Shinshu Field - Buried chest near Lake": LocData(1883582, type=LocationType.BURIED_CHEST),
        "Shinshu Field - Chest Under Bombable ground near Agata Forest": LocData(1883588, cherry_bomb_level=1,
                                                                                 required_brush_techniques=[
                                                                                     BrushTechniques.GREENSPROUT_BLOOM]),
        "Shinshu Field - Buried chest near Dojo": LocData(1883594, type=LocationType.BURIED_CHEST),
        "Shinshu Field - Chest after devil gate": LocData(1883599, mandatory_enemies=[OkamiEnemies.GREEN_IMP,
                                                                                 OkamiEnemies.RED_IMP,
                                                                                 OkamiEnemies.YELLOW_IMP]),
        # Probably should find a better name for this one
        "Shinshu Field - Buried chest on ledge": LocData(1883602, type=LocationType.BURIED_CHEST),
        "Shinshu Field - Buried chest near Ovens": LocData(1883630, type=LocationType.BURIED_CHEST),
        # This is the cherry bomb tutorial. Need to check what happens if you blow the wall before doing the tutorial.
        "Shinshu Field - In Bombable cave near Tama's house": LocData(1883634, cherry_bomb_level=1),
        "Shinshu Field - In Bombable cave near cat statue": LocData(1883635, cherry_bomb_level=1),
        "Shinshu Field - Buried Chest in leaf pile near Tama's house": LocData(1883638,
                                                                               type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Shinshu Field - Chest on Big Torii": LocData(1883641, required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Shinshu Field - Freestanding chest in front of guardian sapling": LocData(1883647),
        "Shinshu Field - Freestanding chest near Agata Forest Cave": LocData(1883648),
        "Shinshu Field - Freestanding chest near Tama's house": LocData(1883669),
        "Shinshu Field - Buried Chest in burning leaf pile behind Dojo": LocData(1883670, type=LocationType.BURIED_UNDER_LEAF_PILE)
    },

    RegionNames.TAMA_HOUSE: {
        "Shinshu Field - Bakigami": LocData(200025,type=LocationType.CONSTELLATION,special_rule=lambda s,w:night_time_check_rule(s,w))  # bit 25
    }
}

# Shop locations (shopId=18): 300000 + 18*1000 + slot = 318000 + slot
# These are added separately and conditionally created based on RandomizeShops option
shop_locations = {
    RegionNames.SHINSHU_FIELD: {
        "Shinshu Field - Shop Slot 1": LocData(318000, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 2": LocData(318001, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 3": LocData(318002, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 4": LocData(318003, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 5": LocData(318004, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 6": LocData(318005, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 7": LocData(318006, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 8": LocData(318007, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 9": LocData(318008, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 10": LocData(318009, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 11": LocData(318010, type=LocationType.SHOP),
        "Shinshu Field - Shop Slot 12": LocData(318011, type=LocationType.SHOP),
    }
}
