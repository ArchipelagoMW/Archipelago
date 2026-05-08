from typing import TYPE_CHECKING

from rule_builder.rules import Or, Has, HasAll
from ..CheckIds import shop_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Types import LocData, EventData, ExitData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CITY_CHECKPOINT_TAKA: [
        ExitData("Enter the Drawbridge", RegionNames.CITY_CHECKPOINT_DRAWBRIDGE,
                 has_events=["City Checkpoint - Activate the Drawbridge"]),
        # Setup this connection only bc it is always both ways. ignore the fact that you can go down to the river from the other side.
        ExitData("Use ramp to go down to the river", RegionNames.CITY_CHECKPOINT_RIVER)
    ],
    RegionNames.CITY_CHECKPOINT_DRAWBRIDGE: [
        ExitData("Exit the Drawbridge", RegionNames.CITY_CHECKPOINT_RYOSHIMA)
    ]
}
events = {
    RegionNames.CITY_CHECKPOINT_TAKA: {
        # Not setting any logic for this event yet, as we'll probably handle it in a specific way.
        "City Checkpoint - Activate the Drawbridge": EventData()
    },
    RegionNames.CITY_CHECKPOINT_RYOSHIMA: {
        "City Checkpoint - Restore Cursed Patches on Ryoshima side": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM])
    }
}
locations = {

    RegionNames.CITY_CHECKPOINT_TAKA: {
        "City Checkpoint - Buried chest behind merchant": LocData(container_check_id(MapIds.CITY_CHECKPOINT, 6),
                                                                  type=LocationType.BURIED_CHEST),

        "City Checkpoint - Chest under ramp": LocData(container_check_id(MapIds.CITY_CHECKPOINT, 7)),

    },

    RegionNames.CITY_CHECKPOINT_DRAWBRIDGE: {
        "City Checkpoint - Chest inside torches circle": LocData(container_check_id(MapIds.CITY_CHECKPOINT, 1),
                                                                 required_brush_techniques=[
                                                                     BrushTechniques.GREENSPROUT_VINE]),
        "City Checkpoint - Chest on top of rock": LocData(container_check_id(MapIds.CITY_CHECKPOINT, 2),
                                                          required_brush_techniques=[
                                                              BrushTechniques.GREENSPROUT_VINE]),
    },
    RegionNames.CITY_CHECKPOINT_RYOSHIMA: {
        "City Checkpoint - Buried Chest on Ryoshima side after cursed patches": LocData(
            container_check_id(MapIds.CITY_CHECKPOINT, 13), type=LocationType.BURIED_CHEST),
    },
    RegionNames.CITY_CHECKPOINT_RIVER: {
        "City Checkpoint - Southernmost buried chest on river's edge ": LocData(
            container_check_id(MapIds.CITY_CHECKPOINT, 8)),
        "City Checkpoint - Buried chest on river's edge South near waterfall ": LocData(
            container_check_id(MapIds.CITY_CHECKPOINT, 9)),
        "City Checkpoint - Burning chest on river's edge South near waterfall ": LocData(
            container_check_id(MapIds.CITY_CHECKPOINT, 12), type=LocationType.BURNING_CHEST),
        # Special Rule for the river access - You need either Water Tablet or (Waterlily and Gaelstrom)
        "City Checkpoint - Buired Chest on River Northern Island": LocData(
            container_check_id(MapIds.CITY_CHECKPOINT, 16), special_rule=Or(Has("Water Tablet"), HasAll(
                BrushTechniques.GREENSPROUT_WATERLILY, BrushTechniques.GALESTORM)))
    }
}

shop_locations = {
    RegionNames.CITY_CHECKPOINT_TAKA: {
        "City Checkpoint - Shop Slot 1": LocData(shop_check_id(2, 0), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 2": LocData(shop_check_id(2, 1), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 3": LocData(shop_check_id(2, 2), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 4": LocData(shop_check_id(2, 3), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 5": LocData(shop_check_id(2, 4), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 6": LocData(shop_check_id(2, 5), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 7": LocData(shop_check_id(2, 6), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 8": LocData(shop_check_id(2, 7), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 9": LocData(shop_check_id(2, 8), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 10": LocData(shop_check_id(2, 9), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 11": LocData(shop_check_id(2, 10), type=LocationType.SHOP),
        "City Checkpoint - Shop Slot 12": LocData(shop_check_id(2, 11), type=LocationType.SHOP),
    }
}
