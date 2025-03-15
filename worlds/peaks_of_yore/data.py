from enum import IntEnum
from BaseClasses import ItemClassification


class PeaksOfYoreRegion(IntEnum):
    FUNDAMENTALS = 0
    INTERMEDIATE = 1
    ADVANCED = 2
    EXPERT = 3


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
    LocationData('Bird Seed (Ymir\'s Shadow)', 'Bird Seed', 4004, PeaksOfYoreRegion.ADVANCED)
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
