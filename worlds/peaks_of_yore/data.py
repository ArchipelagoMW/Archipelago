from __future__ import annotations

from enum import IntEnum
from typing import Callable, NamedTuple

from .options import PeaksOfYoreOptions
from BaseClasses import ItemClassification

peak_offset: int = 1
rope_offset: int = 1000
artefact_offset: int = 2000
book_offset: int = 3000
bird_seed_offset: int = 4000
tool_offset: int = 5000
extra_item_offset: int = 6000
free_solo_peak_offset: int = 7000
time_attack_time_offset: int = 8000
time_attack_ropes_offset: int = 9000
time_attack_holds_offset: int = 10000

# To whoever is reviewing this, just know that I pray for you
# I basically rewrote this entire file from scratch, so don't go looking at the differences

class POYItemLocationType(IntEnum):
    PEAK = 1
    ROPE = 1000
    ARTEFACT = 2000
    BOOK = 3000
    BIRDSEED = 4000
    TOOL = 5000
    EXTRA = 6000
    FREESOLO = 7000
    TIMEATTACK_TIME = 8000
    TIMEATTACK_HOLDS = 9000
    TIMEATTACK_ROPES = 10000


class ItemData:
    """
    ItemData is an internal class for me to specify items
    is_starter_item, is_enabled and is_early are all called later to determine how to handle the item
    based on the current options
    """
    name: str
    type: POYItemLocationType
    id: int
    classification: ItemClassification
    is_starter_item: Callable[[PeaksOfYoreOptions], bool]
    is_enabled: Callable[[PeaksOfYoreOptions], bool]
    is_early: Callable[[PeaksOfYoreOptions], bool]

    def __init__(self, name: str, item_id: int, classification: ItemClassification, item_type: POYItemLocationType,
                 is_starter_item: Callable[[PeaksOfYoreOptions], bool] = lambda opts: False,
                 is_enabled: Callable[[PeaksOfYoreOptions], bool] = lambda opts: True,
                 is_early: Callable[[PeaksOfYoreOptions], bool] = lambda opts: False):
        self.name = name
        self.type = item_type
        self.id = item_id
        self.classification = classification
        self.is_starter_item = is_starter_item
        self.is_enabled = is_enabled
        self.is_early = is_early

# very simple class for location information
class LocationData(NamedTuple):
    name: str
    type: POYItemLocationType
    id: int

    def get_id(self):
        return self.id + self.type

class POYRegion:
    """
    POYRegion is used later to define Regions, allowing me to define the regions in this file
    with entry_requirements being a dict of item: count, to define entty requirements
    enable_reqirements is called later in regions.py to determine whether to include the region based on the user's options
    e.g. not including the time attack regions if Time Attack is disabled
    """
    name: str
    entry_requirements: dict[str, int]  # name: count
    enable_requirements: Callable[[PeaksOfYoreOptions], bool]
    subregions: list[POYRegion]
    locations: list[LocationData]
    is_peak: bool
    is_book: bool

    def __init__(self, name: str, entry_requirements=None, subregions=None, locations=None,
                 enable_requirements: Callable[[PeaksOfYoreOptions], bool] = lambda opts: True, is_book: bool = False):
        if subregions is None:
            subregions = []
        if entry_requirements is None:
            entry_requirements = {}
        if locations is None:
            locations = []

        self.name = name
        self.entry_requirements = entry_requirements
        self.subregions = subregions
        self.locations = locations
        self.enable_requirements = enable_requirements
        self.is_book = is_book
        self.is_peak = False

    def get_all_locations_dict(self) -> dict[str, int]:
        """
        Get all locations in the region AND its subregions
        {name: id}
        """
        v = self.get_locations_dict()
        for r in self.subregions:
            v.update(r.get_all_locations_dict())
        return v

    def get_locations_dict(self) -> dict[str, int]:
        """
        Get all location in the region, not it's subregions
        {name: id}
        """
        return {i.name: i.get_id() for i in self.locations}


class PeakRegion(POYRegion):
    """
    PeakRegion is a descendant of POYRegion, and simply helps me by doing the necessary setup by:
     - Adding a location for the peak itself
     - Creating a subregion for Time attack locations (only accessible with the pocketwatch)
     - creating a location for Free Soloing the peak
    """
    peak_id: int
    generate_time_attack: bool

    def __init__(self, name: str, peak_id: int, entry_requirements=None, subregions=None, locations=None,
                 enable_requirements: Callable[[PeaksOfYoreOptions], bool] = lambda opts: True,
                 generate_time_attack: bool = True):
        self.peak_id = peak_id
        self.generate_time_attack = generate_time_attack
        super(PeakRegion, self).__init__(name, entry_requirements, subregions, locations, enable_requirements)
        self.prepare_peak_region()
        self.is_peak = True
        self.is_book = False

    def prepare_peak_region(self):
        self.entry_requirements.update({self.name: 1})
        self.locations.append(LocationData(self.name, POYItemLocationType.PEAK, self.peak_id))
        if self.peak_id >= 30:
            self.locations.append(LocationData(self.name + ": Free Solo", POYItemLocationType.FREESOLO,
                                               self.peak_id))
        if self.generate_time_attack:
            self.subregions.append(POYRegion(
                self.name + " Time Attack", entry_requirements={"Pocketwatch": 1}, locations=[
                    LocationData(self.name + ": Time Record", POYItemLocationType.TIMEATTACK_TIME, self.peak_id),
                    LocationData(self.name + ": Ropes Record", POYItemLocationType.TIMEATTACK_ROPES, self.peak_id),
                    LocationData(self.name + ": Holds Record", POYItemLocationType.TIMEATTACK_HOLDS, self.peak_id),
                ], enable_requirements=lambda options: options.include_time_attack))


# All of the items in the randomiser are defined here, with functions to define whether they are not enabled,
# starter items, or early
all_items: list[ItemData] = [
    # Tools
    ItemData("Pipe", 0, ItemClassification.useful, POYItemLocationType.TOOL),
    ItemData("Rope Length Upgrade", 1, ItemClassification.useful, POYItemLocationType.TOOL),
    ItemData("Barometer", 2, ItemClassification.useful, POYItemLocationType.TOOL,
             is_starter_item=lambda options: options.start_with_barometer),
    ItemData("Progressive Crampons", 3, ItemClassification.progression, POYItemLocationType.TOOL,
             is_starter_item=lambda options: options.starting_book == 3),
    ItemData("Progressive Crampons", 3, ItemClassification.progression, POYItemLocationType.TOOL),
    # ^2 of these^ (on purpose)
    ItemData("Monocular", 4, ItemClassification.filler, POYItemLocationType.TOOL),
    ItemData("Phonograph", 5, ItemClassification.filler, POYItemLocationType.TOOL),
    ItemData("Pocketwatch", 6, ItemClassification.progression, POYItemLocationType.TOOL),
    ItemData("Chalkbag", 7, ItemClassification.useful, POYItemLocationType.TOOL,
             is_starter_item=lambda options: options.start_with_chalk),
    ItemData("Rope Unlock", 8, ItemClassification.progression, POYItemLocationType.TOOL,
             is_starter_item=lambda options: options.rope_unlock_mode == 0,
             is_early=lambda options: options.rope_unlock_mode == 1),
    ItemData("Coffee Unlock", 9, ItemClassification.useful, POYItemLocationType.TOOL,
             is_starter_item=lambda options: options.start_with_coffee),
    ItemData("Oil Lamp", 10, ItemClassification.progression, POYItemLocationType.TOOL,
             is_starter_item=lambda options: options.start_with_oil_lamp),
    ItemData("Left Hand", 11, ItemClassification.progression, POYItemLocationType.TOOL,
             is_starter_item=lambda options: options.start_with_hands in (0, 1),
             is_early=lambda options: options.early_hands),
    ItemData("Right Hand", 12, ItemClassification.progression, POYItemLocationType.TOOL,
             is_starter_item=lambda options: options.start_with_hands in (0, 2),
             is_early=lambda options: options.early_hands),

    # Books
    ItemData("Fundamentals Book", 0, ItemClassification.progression, POYItemLocationType.BOOK,
             is_starter_item=lambda options: options.starting_book == 0,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 0),
    ItemData("Intermediate Book", 1, ItemClassification.progression, POYItemLocationType.BOOK,
             is_starter_item=lambda options: options.starting_book == 1,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 0),
    ItemData("Advanced Book", 2, ItemClassification.progression, POYItemLocationType.BOOK,
             is_starter_item=lambda options: options.starting_book == 2,
             is_enabled=lambda options: options.enable_advanced and options.game_mode == 0),
    ItemData("Expert Book", 3, ItemClassification.progression, POYItemLocationType.BOOK,
             is_starter_item=lambda options: options.starting_book == 3,
             is_enabled=lambda options: options.enable_expert and options.game_mode == 0),

    # Fundamental Peaks
    ItemData("Greenhorn's Top", 0, ItemClassification.progression, POYItemLocationType.PEAK,
             is_starter_item=lambda options: options.starting_book == 0,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Paltry Peak", 1, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Old Mill", 2, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Gray Gully", 3, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Lighthouse", 4, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Old Man Of Sjór", 5, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Giant's Shelf", 6, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Evergreen's End", 7, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("The Twins", 8, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Old Grove's Skelf", 9, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Land's End", 10, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Hangman's Leap", 11, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Old Langr", 12, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Aldr Grotto", 13, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Three Brothers", 14, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Walter's Crag", 15, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("The Great Crevice", 16, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Old Hagger", 17, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Ugsome Storr", 18, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    ItemData("Wuthering Crest", 19, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_fundamental and options.game_mode == 1),
    # Intermediate Peaks
    ItemData("Porter's Boulder", 20, ItemClassification.progression, POYItemLocationType.PEAK,
             is_starter_item=lambda options: options.starting_book == 1,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Jotunn's Thumb", 21, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Old Skerry", 22, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Hamarr Stone", 23, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Giant's Nose", 24, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Walter's Boulder", 25, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Sundered Sons", 26, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Old Weald's Boulder", 27, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Leaning Spire", 28, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    ItemData("Cromlech", 29, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_intermediate and options.game_mode == 1),
    # Advanced Peaks
    ItemData("Walker's Pillar", 30, ItemClassification.progression, POYItemLocationType.PEAK,
             is_starter_item=lambda options: options.starting_book == 2,
             is_enabled=lambda options: options.enable_advanced and options.game_mode == 1),
    ItemData("Eldenhorn", 31, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_advanced and options.game_mode == 1),
    ItemData("Great Gaol", 32, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_advanced and options.game_mode == 1),
    ItemData("St, Haelga", 33, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_advanced and options.game_mode == 1),
    ItemData("Ymir's Shadow", 34, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_advanced and options.game_mode == 1),
    # Expert Peaks
    ItemData("The Great Bulwark", 35, ItemClassification.progression, POYItemLocationType.PEAK,
             is_starter_item=lambda options: options.starting_book == 3,
             is_enabled=lambda options: options.enable_expert and options.game_mode == 1),
    ItemData("Solemn Tempest", 36, ItemClassification.progression, POYItemLocationType.PEAK,
             is_enabled=lambda options: options.enable_expert and not options.disable_solemn_tempest
                                        and options.game_mode == 1),

    # ropes
    ItemData("Walter's Crag: Rope (Co-Climb)", 0, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Walker's Pillar: Rope (Co-Climb)", 1, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Great Gaol: Rope (Encounter)", 2, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("St Haelga: Rope (Encounter)", 3, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Old Man Of Sjór: Rope", 4, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Hangman's Leap: Rope", 5, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Ugsome Storr: Rope", 6, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Eldenhorn: Rope", 7, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Ymir's Shadow: Rope", 8, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Wuthering Crest: Rope", 9, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Great Gaol: Rope", 10, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Walter's Crag: Rope", 11, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Land's End: Rope", 12, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Evergreen's End: Rope", 13, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("The Great Crevice: Rope", 14, ItemClassification.useful, POYItemLocationType.ROPE),
    ItemData("Old Hagger: Rope", 15, ItemClassification.useful, POYItemLocationType.ROPE),

    # artefacts
    ItemData("Old Mill: Hat", 0, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Evergreen's End: Fisherman's Cap", 1, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Old Grove's Skelf: Safety Helmet", 2, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Old Man Of Sjór: Climbing Shoe", 3, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Three Brothers: Shovel", 4, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Giant's Shelf: Sleeping Bag", 5, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Aldr Grotto: Backpack", 6, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Old Langr: Coffee Box", 7, ItemClassification.useful, POYItemLocationType.ARTEFACT),
    ItemData("Wuthering Crest: Coffee Box", 8, ItemClassification.useful, POYItemLocationType.ARTEFACT),
    ItemData("Walker's Pillar: Chalk Box", 9, ItemClassification.useful, POYItemLocationType.ARTEFACT),
    ItemData("Eldenhorn: Chalk Box", 10, ItemClassification.useful, POYItemLocationType.ARTEFACT),
    ItemData("Leaning Spire: Intermediate Trophy", 11, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Ymir's Shadow: Advanced Trophy", 12, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("The Great Bulwark: Expert Trophy", 13, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Gray Gully: Picture Piece #1", 14, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Land's End: Picture Piece #2", 15, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("The Great Crevice: Picture Piece #3", 16, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("St. Haelga: Picture Piece #4", 17, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Great Gaol: Picture Frame", 18, ItemClassification.filler, POYItemLocationType.ARTEFACT),
    ItemData("Walter's Crag: Fundamentals Trophy", 19, ItemClassification.filler, POYItemLocationType.ARTEFACT),

    # Bird seeds
    ItemData("Three Brothers: Bird Seed", 0, ItemClassification.useful, POYItemLocationType.BIRDSEED),
    ItemData("Old Skerry: Bird Seed", 1, ItemClassification.useful, POYItemLocationType.BIRDSEED),
    ItemData("Great Gaol: Bird Seed", 2, ItemClassification.useful, POYItemLocationType.BIRDSEED),
    ItemData("Eldenhorn: Bird Seed", 3, ItemClassification.useful, POYItemLocationType.BIRDSEED),

    # Extra items
    ItemData("Extra Rope", 0, ItemClassification.filler, POYItemLocationType.EXTRA),
    ItemData("Extra Chalk", 1, ItemClassification.filler, POYItemLocationType.EXTRA),
    ItemData("Extra Coffee", 2, ItemClassification.filler, POYItemLocationType.EXTRA),
    ItemData("Extra Seed", 3, ItemClassification.filler, POYItemLocationType.EXTRA),
    ItemData("Trap", 4, ItemClassification.filler, POYItemLocationType.EXTRA),
]
item_name_to_id: dict[str, int] = {i.name: i.id + i.type for i in all_items}

item_id_to_classification: dict[int, ItemClassification] = {i.id + i.type: i.classification for i in all_items}

# poy_regions defines all the regions, their entry requirements, locations and requirements to be included
poy_regions: POYRegion = POYRegion("Cabin", subregions=[
    POYRegion("Fundamentals", entry_requirements={"Fundamentals Book": 1}, subregions=[
        PeakRegion("Greenhorn's Top", 0),
        PeakRegion("Paltry Peak", 1),
        PeakRegion("Old Mill", 2, locations=[
            LocationData("Old Mill: Hat", POYItemLocationType.ARTEFACT, 0)
        ]),
        PeakRegion("Gray Gully", 3, locations=[
            LocationData("Gray Gully: Picture Piece #1", POYItemLocationType.ARTEFACT, 14),
        ]),
        PeakRegion("Lighthouse", 4),
        PeakRegion("Old Man Of Sjór", 5, locations=[
            LocationData("Old Man Of Sjór: Climbing Shoe", POYItemLocationType.ARTEFACT, 3),
            LocationData("Old Man Of Sjór: Rope: Rope", POYItemLocationType.ROPE, 4)
        ]),
        PeakRegion("Giant's Shelf", 6, locations=[
            LocationData("Giant's Shelf: Sleeping Bag", POYItemLocationType.ARTEFACT, 5),
        ]),
        PeakRegion("Evergreen's End", 7, locations=[
            LocationData("Evergreen's End: Fisherman's Cap", POYItemLocationType.ARTEFACT, 1),
            LocationData("Evergreen's End: Rope", POYItemLocationType.ROPE, 13),
        ]),
        PeakRegion("The Twins", 8),
        PeakRegion("Old Grove's Skelf", 9, locations=[
            LocationData("Old Grove's Skelf: Safety Helmet", POYItemLocationType.ARTEFACT, 2)
        ]),
        PeakRegion("Land's End", 10, locations=[
            LocationData("Land's End: Picture Piece #2", POYItemLocationType.ARTEFACT, 15),
            LocationData("Land's End: Rope", POYItemLocationType.ROPE, 12),
        ]),
        PeakRegion("Hangman's Leap", 11, locations=[
            LocationData("Hangman's Leap: Rope", POYItemLocationType.ROPE, 5),
        ]),
        PeakRegion("Old Langr", 12, locations=[
            LocationData("Old Langr: Coffee Box", POYItemLocationType.ARTEFACT, 7),
        ]),
        PeakRegion("Aldr Grotto", 13, entry_requirements={"Oil Lamp": 1}, locations=[
            LocationData("Aldr Grotto: Backpack", POYItemLocationType.ARTEFACT, 6),
        ]),
        PeakRegion("Three Brothers", 14, locations=[
            LocationData("Three Brothers: Shovel", POYItemLocationType.ARTEFACT, 4),
            LocationData("Three Brothers: Bird Seed", POYItemLocationType.BIRDSEED, 0),
        ]),
        PeakRegion("Walter's Crag", 15, locations=[
            LocationData("Walter's Crag: Fundamentals Trophy", POYItemLocationType.ARTEFACT, 19),
            LocationData("Walter's Crag: Rope (Co-Climb)", POYItemLocationType.ROPE, 0),
            LocationData("Walter's Crag: Rope", POYItemLocationType.ROPE, 11),
        ]),
        PeakRegion("The Great Crevice", 16, locations=[
            LocationData("The Great Crevice: Picture Piece #3", POYItemLocationType.ARTEFACT, 16),
            LocationData("The Great Crevice: Rope", POYItemLocationType.ROPE, 14),
        ]),
        PeakRegion("Old Hagger", 17, locations=[
            LocationData("Old Hagger: Rope", POYItemLocationType.ROPE, 15),
        ]),
        PeakRegion("Ugsome Storr", 18, locations=[
            LocationData("Ugsome Storr: Rope", POYItemLocationType.ROPE, 6),
        ]),
        PeakRegion("Wuthering Crest", 19, locations=[
            LocationData("Wuthering Crest: Coffee Box", POYItemLocationType.ARTEFACT, 8),
            LocationData("Wuthering Crest: Rope", POYItemLocationType.ROPE, 9),
        ]),
    ], enable_requirements=lambda options: options.enable_fundamental, is_book=True),
    POYRegion("Intermediate", entry_requirements={"Intermediate Book": 1}, subregions=[
        PeakRegion("Porter's Boulder", 20),
        PeakRegion("Jotunn's Thumb", 21),
        PeakRegion("Old Skerry", 22, locations=[
            LocationData("Old Skerry: Bird Seed", POYItemLocationType.BIRDSEED, 1),
        ]),
        PeakRegion("Hamarr Stone", 23),
        PeakRegion("Giant's Nose", 24),
        PeakRegion("Walter's Boulder", 25),
        PeakRegion("Sundered Sons", 26),
        PeakRegion("Old Weald's Boulder", 27),
        PeakRegion("Leaning Spire", 28, locations=[
            LocationData("Leaning Spire: Intermediate Trophy", POYItemLocationType.ARTEFACT, 11),
        ]),
        PeakRegion("Cromlech", 29),
    ], enable_requirements=lambda options: options.enable_intermediate, is_book=True),
    POYRegion("Advanced", entry_requirements={"Advanced Book": 1}, subregions=[
        PeakRegion("Walker's Pillar", 30, locations=[
            LocationData("Walker's Pillar: Chalk Box", POYItemLocationType.ARTEFACT, 9),
            LocationData("Walker's Pillar: Rope (Co-Climb)", POYItemLocationType.ROPE, 1),
        ]),
        PeakRegion("Eldenhorn", 31, locations=[
            LocationData("Eldenhorn: Chalk Box", POYItemLocationType.ARTEFACT, 10),
            LocationData("Eldenhorn: Rope", POYItemLocationType.ROPE, 7),
            LocationData("Eldenhorn: Bird Seed", POYItemLocationType.BIRDSEED, 3),
        ]),
        PeakRegion("Great Gaol", 32, locations=[
            LocationData("Great Gaol: Picture Frame", POYItemLocationType.ARTEFACT, 18),
            LocationData("Great Gaol: Rope (Encounter)", POYItemLocationType.ROPE, 2),
            LocationData("Great Gaol: Rope", POYItemLocationType.ROPE, 10),
            LocationData("Great Gaol: Bird Seed", POYItemLocationType.BIRDSEED, 2),
        ]),
        PeakRegion("St, Haelga", 33, locations=[
            LocationData("St Haelga: Rope (Encounter)", POYItemLocationType.ROPE, 3),
            LocationData("St. Haelga: Picture Piece #4", POYItemLocationType.ARTEFACT, 17),
        ]),
        PeakRegion("Ymir's Shadow", 34, locations=[
            LocationData("Ymir's Shadow: Advanced Trophy", POYItemLocationType.ARTEFACT, 12),
            LocationData("Ymir's Shadow: Rope", POYItemLocationType.ROPE, 8),
            LocationData("Ymir's Shadow: Bird Seed", POYItemLocationType.BIRDSEED, 4),
        ]),
    ], enable_requirements=lambda options: options.enable_advanced, is_book=True),
    POYRegion("Expert", entry_requirements={"Progressive Crampons": 1, "Expert Book": 1}, subregions=[
        PeakRegion("The Great Bulwark", 35, locations=[
            LocationData("The Great Bulwark: Expert Trophy", POYItemLocationType.ARTEFACT, 13),
        ], generate_time_attack=False),
        PeakRegion("Solemn Tempest", 36, entry_requirements={"Progressive Crampons": 2},
                   enable_requirements=lambda options: not options.disable_solemn_tempest, generate_time_attack=False),
    ], enable_requirements=lambda options: options.enable_expert, is_book=True),
])
all_locations_to_ids: dict[str, int] = poy_regions.get_all_locations_dict()
