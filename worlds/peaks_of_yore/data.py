from enum import IntEnum
from BaseClasses import ItemClassification


class PeaksOfYoreRegion(IntEnum):
    FUNDAMENTALS = 0
    INTERMEDIATE = 1
    ADVANCED = 2
    EXPERT = 3
    NONE = 4


class PeaksOfYoreItemLocationType(IntEnum):
    PEAK = 0
    ROPE = 1
    ARTEFACT = 2
    BOOK = 3
    BIRDSEED = 4
    TOOL = 5
    EXTRA = 6
    FREESOLO = 7
    TIMEATTACK_TIME = 8
    TIMEATTACK_HOLDS = 9
    TIMEATTACK_ROPES = 10


class LocationData:
    name: str
    type: str
    id: int
    region: PeaksOfYoreRegion

    def __init__(self, name: str, location_type: str, location_id: int, region: PeaksOfYoreRegion):
        self.name = name
        self.type = location_type
        self.id = location_id
        self.region = region


class ItemData:
    name: str
    type: str
    id: int
    classification: ItemClassification

    def __init__(self, name: str, item_type: str, item_id: int, classification: ItemClassification):
        self.name = name
        self.type = item_type
        self.id = item_id
        self.classification = classification


class ItemOrLocation:  # since a good 50% of locations are also items and the other way around
    name: str          # I'm storing them both in a single class
    id: int
    classification: ItemClassification

    def __init__(self, name: str, index: int, classification: ItemClassification = ItemClassification.filler):
        self.name = name
        self.id = index
        self.classification = classification


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

peaks_list: dict[PeaksOfYoreRegion, set[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: {
        ItemOrLocation("Greenhorn's Top", 0),
        ItemOrLocation('Paltry Peak', 1),
        ItemOrLocation('Old Mill', 2),
        ItemOrLocation('Gray Gully', 3),
        ItemOrLocation('Lighthouse', 4),
        ItemOrLocation('Old Man Of Sjor', 5),
        ItemOrLocation('Giants Shelf', 6),
        ItemOrLocation("Evergreen's End", 7),
        ItemOrLocation('The Twins', 8),
        ItemOrLocation("Old Grove's Skelf", 9),
        ItemOrLocation("Land's End", 10),
        ItemOrLocation("Hangman's Leap", 11),
        ItemOrLocation('Old Langr', 12),
        ItemOrLocation('Aldr Grotto', 13),
        ItemOrLocation('Three Brothers', 14),
        ItemOrLocation("Walter's Crag", 15),
        ItemOrLocation('The Great Crevice', 16),
        ItemOrLocation('Old Hagger', 17),
        ItemOrLocation('Ugsome Storr', 18),
        ItemOrLocation('Wuthering Crest', 19)
    },
    PeaksOfYoreRegion.INTERMEDIATE: {
        ItemOrLocation("Porter's Boulders", 20),
        ItemOrLocation("Jotunn's Thumb", 21),
        ItemOrLocation('Old Skerry', 22),
        ItemOrLocation('Hamarr Stone', 23),
        ItemOrLocation("Giant's Nose", 24),
        ItemOrLocation("Walter's Boulder", 25),
        ItemOrLocation('Sundered Sons', 26),
        ItemOrLocation("Old Weald's Boulder", 27),
        ItemOrLocation('Leaning Spire', 28),
        ItemOrLocation('Cromlech', 29),
    },
    PeaksOfYoreRegion.ADVANCED: {
        ItemOrLocation("Walker's Pillar", 30),
        ItemOrLocation('Eldenhorn', 31),
        ItemOrLocation('Great Gaol', 32),
        ItemOrLocation('St. Haelga', 33),
        ItemOrLocation("Ymir's Shadow", 34),
    },
    PeaksOfYoreRegion.EXPERT: {
        ItemOrLocation('Great Bulwark', 35),
        ItemOrLocation('Solemn Tempest', 36),
    },
    PeaksOfYoreRegion.NONE: {}
}

ropes_list: dict[PeaksOfYoreRegion, set[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: {
        ItemOrLocation('Walters Crag: Rope (Co-Climb)', 0),     # the in game ropes are shuffled around a bit,
        ItemOrLocation('Old Man Of Sjor: Rope', 4),             # this is also why they are like this here
        ItemOrLocation('Hangman\'s Leap: Rope', 5),
        ItemOrLocation('Ugsome Storr: Rope', 6),
        ItemOrLocation('Wuthering Crest: Rope', 9),
        ItemOrLocation('Walter\'s Crag: Rope', 11),
        ItemOrLocation('Land\'s End: Rope', 12),
        ItemOrLocation('Evergreen\'s End: Rope', 13),
        ItemOrLocation('Great Crevice: Rope', 14),
        ItemOrLocation('Old Hagger Rope', 15),
    },
    PeaksOfYoreRegion.INTERMEDIATE: {},
    PeaksOfYoreRegion.ADVANCED: {
        ItemOrLocation('Walkers Pillar: Rope (Co-Climb)', 1),
        ItemOrLocation('Great Gaol: Rope (Encounter)', 2),
        ItemOrLocation('St. Haelga: Rope (Encounter)', 3),
        ItemOrLocation('Eldenhorn: Rope', 7),
        ItemOrLocation('Ymir\'s Shadow: Rope', 8),
        ItemOrLocation('Great Gaol: Rope', 10),
    },
    PeaksOfYoreRegion.EXPERT: {},
    PeaksOfYoreRegion.NONE: {}
}

artefacts_list: dict[PeaksOfYoreRegion, set[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: {
        ItemOrLocation('Hat', 0),
        ItemOrLocation('Fisherman\'s Cap', 1),
        ItemOrLocation('Safety Helmet', 2),
        ItemOrLocation('Climbing Shoe', 3),
        ItemOrLocation('Shovel', 4),
        ItemOrLocation('Sleeping Bag', 5),
        ItemOrLocation('Backpack', 6),
        ItemOrLocation('Coffee Box (Old Langr)', 7),
        ItemOrLocation('Coffee Box (Wuthering Crest)', 8),
        ItemOrLocation('Picture Piece #1 (Gray Gully)', 14),
        ItemOrLocation('Picture Piece #2 (Land\'s End)', 15),
        ItemOrLocation('Picture Piece #3 (The Great Crevice)', 16),
        ItemOrLocation('Fundamentals Trophy', 19),
    },
    PeaksOfYoreRegion.INTERMEDIATE: {
        ItemOrLocation('Intermediate Trophy', 11),
    },
    PeaksOfYoreRegion.ADVANCED: {
        ItemOrLocation('Chalk Box (Walker\'s Pillar)', 9),
        ItemOrLocation('Chalk Box (Eldenhorn)', 10),
        ItemOrLocation('Advanced Trophy', 12),
        ItemOrLocation('Picture Piece #4 (St. Haelga)', 17),
        ItemOrLocation('Picture Frame', 18),
    },
    PeaksOfYoreRegion.EXPERT: {
        ItemOrLocation('Expert Trophy', 13),
    },
    PeaksOfYoreRegion.NONE: {}
}

books_list: dict[PeaksOfYoreRegion, set[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: {},
    PeaksOfYoreRegion.INTERMEDIATE: {},
    PeaksOfYoreRegion.ADVANCED: {},
    PeaksOfYoreRegion.EXPERT: {},
    PeaksOfYoreRegion.NONE: {
        ItemOrLocation('Fundamentals Book', 0, ItemClassification.progression),
        ItemOrLocation('Intermediate Book', 1, ItemClassification.progression),
        ItemOrLocation('Advanced Book', 2, ItemClassification.progression),
        ItemOrLocation('Expert Book', 3, ItemClassification.progression),
    }
}

bird_seeds_list: dict[PeaksOfYoreRegion, set[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: {
        ItemOrLocation('Bird Seed (Three Brothers)', 0),
    },
    PeaksOfYoreRegion.INTERMEDIATE: {
        ItemOrLocation('Bird Seed (Old Skerry)', 1),
    },
    PeaksOfYoreRegion.ADVANCED: {
        ItemOrLocation('Bird Seed (Great Gaol)', 2),
        ItemOrLocation('Bird Seed (Eldenhorn)', 3),
    },
    PeaksOfYoreRegion.EXPERT: {},
    PeaksOfYoreRegion.NONE: {}
}

tools_list: dict[PeaksOfYoreRegion, set[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: {},
    PeaksOfYoreRegion.INTERMEDIATE: {},
    PeaksOfYoreRegion.ADVANCED: {},
    PeaksOfYoreRegion.EXPERT: {},
    PeaksOfYoreRegion.NONE: {
        ItemOrLocation('Pipe', 0, ItemClassification.useful),
        ItemOrLocation('Rope Length Upgrade', 1, ItemClassification.progression),
        ItemOrLocation('Barometer', 2, ItemClassification.useful),
        ItemOrLocation('Progressive Crampons', 3, ItemClassification.progression),
        ItemOrLocation('Monocular', 4, ItemClassification.useful),
        ItemOrLocation('Phonograph', 5, ItemClassification.filler),
        ItemOrLocation('Pocketwatch', 6, ItemClassification.useful),
        ItemOrLocation('Chalkbag', 7, ItemClassification.useful),
        ItemOrLocation('Rope Unlock', 8, ItemClassification.progression),
        ItemOrLocation('Coffee Unlock', 9, ItemClassification.useful),
        ItemOrLocation('Oil Lamp', 10, ItemClassification.useful),
        ItemOrLocation('Left Hand', 11, ItemClassification.progression),
        ItemOrLocation('Right Hand', 12, ItemClassification.progression),
    }
}

extra_items_list: dict[PeaksOfYoreRegion, set[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: {},
    PeaksOfYoreRegion.INTERMEDIATE: {},
    PeaksOfYoreRegion.ADVANCED: {},
    PeaksOfYoreRegion.EXPERT: {},
    PeaksOfYoreRegion.NONE: {
        ItemOrLocation('Extra Rope', 0, ItemClassification.filler),
        ItemOrLocation('Extra Chalk', 1, ItemClassification.filler),
        ItemOrLocation('Extra Coffee', 2, ItemClassification.filler),
        ItemOrLocation('Extra Seed', 3, ItemClassification.filler)
    }
}

full_location_list: list[LocationData] = [
    LocationData("Greenhorn's Top", 'Peak', 1, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Paltry Peak', 'Peak', 2, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Old Mill', 'Peak', 3, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Gray Gully', 'Peak', 4, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Lighthouse', 'Peak', 5, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Old Man Of Sjor', 'Peak', 6, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Giants Shelf', 'Peak', 7, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData("Evergreen's End", 'Peak', 8, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('The Twins', 'Peak', 9, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData("Old Grove's Skelf", 'Peak', 10, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData("Land's End", 'Peak', 11, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData("Hangman's Leap", 'Peak', 12, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Old Langr', 'Peak', 13, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Aldr Grotto', 'Peak', 14, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Three Brothers', 'Peak', 15, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData("Walter's Crag", 'Peak', 16, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('The Great Crevice', 'Peak', 17, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Old Hagger', 'Peak', 18, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Ugsome Storr', 'Peak', 19, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Wuthering Crest', 'Peak', 20, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData("Porter's Boulders", 'Peak', 21, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData("Jotunn's Thumb", 'Peak', 22, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Old Skerry', 'Peak', 23, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Hamarr Stone', 'Peak', 24, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData("Giant's Nose", 'Peak', 25, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData("Walter's Boulder", 'Peak', 26, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Sundered Sons', 'Peak', 27, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData("Old Weald's Boulder", 'Peak', 28, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Leaning Spire', 'Peak', 29, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Cromlech', 'Peak', 30, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData("Walker's Pillar", 'Peak', 31, PeaksOfYoreRegion.ADVANCED),
    LocationData('Eldenhorn', 'Peak', 32, PeaksOfYoreRegion.ADVANCED),
    LocationData('Great Gaol', 'Peak', 33, PeaksOfYoreRegion.ADVANCED),
    LocationData('St. Haelga', 'Peak', 34, PeaksOfYoreRegion.ADVANCED),
    LocationData("Ymir's Shadow", 'Peak', 35, PeaksOfYoreRegion.ADVANCED),
    LocationData('Great Bulwark', 'Peak', 36, PeaksOfYoreRegion.EXPERT),
    LocationData('Solemn Tempest', 'Peak', 37, PeaksOfYoreRegion.EXPERT),
    LocationData('Walters Crag: Rope (Co-Climb)', 'Rope', 1000, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Walkers Pillar: Rope (Co-Climb)', 'Rope', 1001, PeaksOfYoreRegion.ADVANCED),
    LocationData('Great Gaol: Rope (Encounter)', 'Rope', 1002, PeaksOfYoreRegion.ADVANCED),
    LocationData('St. Haelga: Rope (Encounter)', 'Rope', 1003, PeaksOfYoreRegion.ADVANCED),
    LocationData('Old Man Of Sjor: Rope', 'Rope', 1004, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Hangman\'s Leap: Rope', 'Rope', 1005, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Ugsome Storr: Rope', 'Rope', 1006, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Eldenhorn: Rope', 'Rope', 1007, PeaksOfYoreRegion.ADVANCED),
    LocationData('Ymir\'s Shadow: Rope', 'Rope', 1008, PeaksOfYoreRegion.ADVANCED),
    LocationData('Wuthering Crest: Rope', 'Rope', 1009, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Great Gaol: Rope', 'Rope', 1010, PeaksOfYoreRegion.ADVANCED),
    LocationData('Walter\'s Crag: Rope', 'Rope', 1011, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Land\'s End: Rope', 'Rope', 1012, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Evergreen\'s End: Rope', 'Rope', 1013, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Great Crevice: Rope', 'Rope', 1014, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Old Hagger Rope', 'Rope', 1015, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Hat', 'Artefact', 2000, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Fisherman\'s Cap', 'Artefact', 2001, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Safety Helmet', 'Artefact', 2002, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Climbing Shoe', 'Artefact', 2003, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Shovel', 'Artefact', 2004, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Sleeping Bag', 'Artefact', 2005, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Backpack', 'Artefact', 2006, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Coffee Box (Old Langr)', 'Artefact', 2007, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Coffee Box (Wuthering Crest)', 'Artefact', 2008, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Chalk Box (Walker\'s Pillar)', 'Artefact', 2009, PeaksOfYoreRegion.ADVANCED),
    LocationData('Chalk Box (Eldenhorn)', 'Artefact', 2010, PeaksOfYoreRegion.ADVANCED),
    LocationData('Intermediate Trophy', 'Artefact', 2011, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Advanced Trophy', 'Artefact', 2012, PeaksOfYoreRegion.ADVANCED),
    LocationData('Expert Trophy', 'Artefact', 2013, PeaksOfYoreRegion.EXPERT),
    LocationData('Picture Piece #1 (Gray Gully)', 'Artefact', 2014, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Picture Piece #2 (Land\'s End)', 'Artefact', 2015, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Picture Piece #3 (The Great Crevice)', 'Artefact', 2016, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Picture Piece #4 (St. Haelga)', 'Artefact', 2017, PeaksOfYoreRegion.ADVANCED),
    LocationData('Picture Frame', 'Artefact', 2018, PeaksOfYoreRegion.ADVANCED),
    LocationData('Fundamentals Trophy', 'Artefact', 2019, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Bird Seed (Three Brothers)', 'Bird Seed', 4000, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Bird Seed (Old Skerry)', 'Bird Seed', 4001, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Bird Seed (Great Gaol)', 'Bird Seed', 4002, PeaksOfYoreRegion.ADVANCED),
    LocationData('Bird Seed (Eldenhorn)', 'Bird Seed', 4003, PeaksOfYoreRegion.ADVANCED),
    LocationData('Bird Seed (Ymir\'s Shadow)', 'Bird Seed', 4004, PeaksOfYoreRegion.ADVANCED),
    LocationData("Walker's Pillar (Free Solo)", 'Free Solo Peak', 7030, PeaksOfYoreRegion.ADVANCED),
    LocationData('Eldenhorn (Free Solo)', 'Free Solo Peak', 7031, PeaksOfYoreRegion.ADVANCED),
    LocationData('Great Gaol (Free Solo)', 'Free Solo Peak', 7032, PeaksOfYoreRegion.ADVANCED),
    LocationData('St. Haelga (Free Solo)', 'Free Solo Peak', 7033, PeaksOfYoreRegion.ADVANCED),
    LocationData("Ymir's Shadow (Free Solo)", 'Free Solo Peak', 7034, PeaksOfYoreRegion.ADVANCED),
    LocationData('Great Bulwark (Free Solo)', 'Free Solo Peak', 7035, PeaksOfYoreRegion.EXPERT),
    LocationData('Solemn Tempest (Free Solo)', 'Free Solo Peak', 7036, PeaksOfYoreRegion.EXPERT),
]

full_item_list: list[ItemData] = [
    ItemData('Walters Crag: Rope (Co-Climb)', 'Rope', 1000, ItemClassification.filler),
    ItemData('Walkers Pillar: Rope (Co-Climb)', 'Rope', 1001, ItemClassification.filler),
    ItemData('Great Gaol: Rope (Encounter)', 'Rope', 1002, ItemClassification.filler),
    ItemData('St. Haelga: Rope (Encounter)', 'Rope', 1003, ItemClassification.filler),
    ItemData('Old Man Of Sjor: Rope', 'Rope', 1004, ItemClassification.filler),
    ItemData('Hangman\'s Leap: Rope', 'Rope', 1005, ItemClassification.filler),
    ItemData('Ugsome Storr: Rope', 'Rope', 1006, ItemClassification.filler),
    ItemData('Eldenhorn: Rope', 'Rope', 1007, ItemClassification.filler),
    ItemData('Ymir\'s Shadow: Rope', 'Rope', 1008, ItemClassification.filler),
    ItemData('Wuthering Crest: Rope', 'Rope', 1009, ItemClassification.filler),
    ItemData('Great Gaol: Rope', 'Rope', 1010, ItemClassification.filler),
    ItemData('Walter\'s Crag: Rope', 'Rope', 1011, ItemClassification.filler),
    ItemData('Land\'s End: Rope', 'Rope', 1012, ItemClassification.filler),
    ItemData('Evergreen\'s End: Rope', 'Rope', 1013, ItemClassification.filler),
    ItemData('Great Crevice: Rope', 'Rope', 1014, ItemClassification.filler),
    ItemData('Old Hagger Rope', 'Rope', 1015, ItemClassification.filler),
    ItemData('Hat', 'Artefact', 2000, ItemClassification.filler),
    ItemData('Fisherman\'s Cap', 'Artefact', 2001, ItemClassification.filler),
    ItemData('Safety Helmet', 'Artefact', 2002, ItemClassification.filler),
    ItemData('Climbing Shoe', 'Artefact', 2003, ItemClassification.filler),
    ItemData('Shovel', 'Artefact', 2004, ItemClassification.filler),
    ItemData('Sleeping Bag', 'Artefact', 2005, ItemClassification.filler),
    ItemData('Backpack', 'Artefact', 2006, ItemClassification.filler),
    ItemData('Coffee Box (Old Langr)', 'Artefact', 2007, ItemClassification.useful),
    ItemData('Coffee Box (Wuthering Crest)', 'Artefact', 2008, ItemClassification.useful),
    ItemData('Chalk Box (Walker\'s Pillar)', 'Artefact', 2009, ItemClassification.useful),
    ItemData('Chalk Box (Eldenhorn)', 'Artefact', 2010, ItemClassification.useful),
    ItemData('Intermediate Trophy', 'Artefact', 2011, ItemClassification.filler),
    ItemData('Advanced Trophy', 'Artefact', 2012, ItemClassification.filler),
    ItemData('Expert Trophy', 'Artefact', 2013, ItemClassification.filler),
    ItemData('Picture Piece #1 (Gray Gully)', 'Artefact', 2014, ItemClassification.filler),
    ItemData('Picture Piece #2 (Land\'s End)', 'Artefact', 2015, ItemClassification.filler),
    ItemData('Picture Piece #3 (The Great Crevice)', 'Artefact', 2016, ItemClassification.filler),
    ItemData('Picture Piece #4 (St. Haelga)', 'Artefact', 2017, ItemClassification.filler),
    ItemData('Picture Frame', 'Artefact', 2018, ItemClassification.filler),
    ItemData('Fundamentals Trophy', 'Artefact', 2019, ItemClassification.filler),
    ItemData('Fundamentals Book', 'Book', 3000, ItemClassification.progression),
    ItemData('Intermediate Book', 'Book', 3001, ItemClassification.progression),
    ItemData('Advanced Book', 'Book', 3002, ItemClassification.progression),
    ItemData('Expert Book', 'Book', 3003, ItemClassification.progression),
    ItemData('Bird Seed (Three Brothers)', 'Bird Seed', 4000, ItemClassification.filler),
    ItemData('Bird Seed (Old Skerry)', 'Bird Seed', 4001, ItemClassification.filler),
    ItemData('Bird Seed (Great Gaol)', 'Bird Seed', 4002, ItemClassification.filler),
    ItemData('Bird Seed (Eldenhorn)', 'Bird Seed', 4003, ItemClassification.filler),
    ItemData('Bird Seed (Ymir\'s Shadow)', 'Bird Seed', 4004, ItemClassification.filler),
    ItemData('Pipe', 'Tool', 5000, ItemClassification.useful),
    ItemData('Rope Length Upgrade', 'Tool', 5001, ItemClassification.progression),
    ItemData('Barometer', 'Tool', 5002, ItemClassification.useful),
    ItemData('Progressive Crampons', 'Tool', 5003, ItemClassification.progression),
    ItemData('Monocular', 'Tool', 5004, ItemClassification.useful),
    ItemData('Phonograph', 'Tool', 5005, ItemClassification.filler),
    ItemData('Pocketwatch', 'Tool', 5006, ItemClassification.useful),
    ItemData('Chalkbag', 'Tool', 5007, ItemClassification.useful),
    ItemData('Rope Unlock', 'Tool', 5008, ItemClassification.progression),
    ItemData('Coffee Unlock', 'Tool', 5009, ItemClassification.useful),
    ItemData('Oil Lamp', 'Tool', 5010, ItemClassification.useful),
    ItemData('Left Hand', 'Tool', 5011, ItemClassification.progression),
    ItemData('Right Hand', 'Tool', 5012, ItemClassification.progression),
    ItemData('Extra Rope', 'Extra Item', 6000, ItemClassification.filler),
    ItemData('Extra Chalk', 'Extra Item', 6001, ItemClassification.filler),
    ItemData('Extra Coffee', 'Extra Item', 6002, ItemClassification.filler),
    ItemData('Extra Seed', 'Extra Item', 6003, ItemClassification.filler)
]

full_item_table: dict[str, ItemData] = {i.name: i for i in full_item_list}
full_location_table: dict[str, LocationData] = {l.name: l for l in full_location_list}
