"""
Centralized data loader for Schedule1 world.
Loads and parses items.json, locations.json, and regions.json into structured objects for easy access.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pkgutil
from typing import Any, Dict, List, Union

import orjson

def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))

@dataclass
class ItemData:
    """Represents item data from items.json"""
    name: str
    modern_id: int
    classification: Union[str, List[str], Dict[str, Union[str, List[str]]]]
    tags: List[str]


@dataclass
class LocationData:
    """Represents location data from locations.json"""
    name: str
    region: str
    requirements: Union[bool, Dict[str, Any]]
    tags: List[str]
    modern_id: int

@dataclass
class RegionData:
    """Represents region data from regions.json"""
    name: str
    connections: Dict[str, Union[bool, Dict[str, Any]]]

class Schedule1ItemData:
    """Container for all Schedule1 game data loaded from JSON files"""
    
    def __init__(self):
        items_raw = load_json_data("items.json")
        
        # Parse items into ItemData objects
        # Classification is stored raw - resolution happens in items.py based on world options
        self.items: Dict[str, ItemData] = {}
        for item_name, item_info in items_raw.items():
            self.items[item_name] = ItemData(
                name=item_name,
                modern_id=item_info["modern_id"],
                classification=item_info["classification"],
                tags=item_info["tags"]
            )


class Schedule1LocationData:
    """Container for all Schedule1 location data loaded from JSON files"""
    
    def __init__(self):
        locations_raw = load_json_data("locations.json")
        
        # Parse locations into LocationData objects
        self.locations: Dict[str, LocationData] = {}
        for location_name, location_info in locations_raw.items():
            self.locations[location_name] = LocationData(
                name=location_name,
                region=location_info["region"],
                requirements=location_info["requirements"],
                tags=location_info["tags"],
                modern_id=location_info["modern_id"]
            )

class Schedule1RegionData:
    """Container for all Schedule1 region data loaded from JSON files"""
    
    def __init__(self):
        regions_raw = load_json_data("regions.json")
        
        # Parse regions into RegionData objects
        self.regions: Dict[str, RegionData] = {}
        for region_name, region_info in regions_raw.items():
            self.regions[region_name] = RegionData(
                name=region_name,
                connections=region_info["connections"]
            )


class Schedule1VictoryData:
    """Container for victory conditions loaded from victory.json"""
    
    def __init__(self):
        # victory.json is structured as {option_name: {method: value, ...}, ...}
        # This is the same structure as requirements in locations/regions
        self.requirements: Dict[str, Any] = load_json_data("victory.json")


# Create singleton instances for easy import
schedule1_item_data = Schedule1ItemData()
schedule1_location_data = Schedule1LocationData()
schedule1_region_data = Schedule1RegionData()
schedule1_victory_data = Schedule1VictoryData()