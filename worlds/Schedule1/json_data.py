"""
Centralized data loader for Schedule1 world.
Loads and parses items.json and locations.json into structured objects for easy access.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import orjson

from BaseClasses import ItemClassification

@dataclass
class ItemData:
    """Represents item data from items.json"""
    name: str
    modern_id: int
    classification: ItemClassification
    tags: List[str]


@dataclass
class LocationData:
    """Represents location data from locations.json"""
    name: str
    region: str
    requirements: Dict[str, int]
    requirements_alt: Dict[str, int]
    modern_id: int
    tags: List[str]

@dataclass
class EventData:
    """Represents event data from events.json"""
    region: str
    itemName: str
    locationName : str
    requirements: Dict[str, int]
    requirements_alt: Dict[str, int]
    tags: List[str]

class Schedule1ItemData:
    """Container for all Schedule1 game data loaded from JSON files"""
    
    def __init__(self):
        # Load items.json
        items_json_path = Path(__file__).parent / "data" / "items.json"
        with open(items_json_path, "rb") as f:
            items_raw = orjson.loads(f.read())
        
        # Mapping from JSON classification strings to ItemClassification flags
        classification_map = {
            "USEFUL": ItemClassification.useful,
            "PROGRESSION": ItemClassification.progression,
            "FILLER": ItemClassification.filler,
            "PROGRESSION_SKIP_BALANCING": ItemClassification.progression_skip_balancing
        }
        
        # Parse items into ItemData objects
        self.items: Dict[str, ItemData] = {}
        for item_name, item_info in items_raw.items():
            # Convert classification from JSON to ItemClassification flags
            classification_data = item_info["classification"]
            if isinstance(classification_data, list):
                # Multiple classifications - combine with bitwise OR
                classification = classification_map[classification_data[0]]
                for class_name in classification_data[1:]:
                    classification |= classification_map[class_name]
            else:
                # Single classification
                classification = classification_map[classification_data]
            
            self.items[item_name] = ItemData(
                name=item_name,
                modern_id=item_info["modern_id"],
                classification=classification,
                tags=item_info["tags"]
            )


class Schedule1LocationData:
    """Container for all Schedule1 location data loaded from JSON files"""
    
    def __init__(self):
        # Load locations.json
        locations_json_path = Path(__file__).parent / "data" / "locations.json"
        with open(locations_json_path, "rb") as f:
            locations_raw = orjson.loads(f.read())
        
        # Parse locations into LocationData objects
        self.locations: Dict[str, LocationData] = {}
        for location_name, location_info in locations_raw.items():
            self.locations[location_name] = LocationData(
                name=location_name,
                region=location_info["region"],
                requirements=location_info["requirements"],
                requirements_alt=location_info["requirements_alt"],
                tags=location_info["tags"],
                modern_id=location_info["modern_id"]
            )

class Schedule1EventData:
    """Container for all Schedule1 event data loaded from JSON files"""
    
    def __init__(self):
        # Load events.json
        events_json_path = Path(__file__).parent / "data" / "events.json"
        with open(events_json_path, "rb") as f:
            events_raw = orjson.loads(f.read())
        
        # Parse events into LocationData objects
        self.events: Dict[str, EventData] = {}
        for event_name, event_info in events_raw.items():
            self.events[event_name] = EventData(
                itemName=event_info["itemName"],
                locationName=event_info["locationName"],
                region=event_info["region"],
                requirements=event_info["requirements"],
                requirements_alt=event_info["requirements_alt"],
                tags=event_info["tags"]
            )
# Create singleton instances for easy import
schedule1_item_data = Schedule1ItemData()
schedule1_location_data = Schedule1LocationData()
schedule1_event_data = Schedule1EventData()