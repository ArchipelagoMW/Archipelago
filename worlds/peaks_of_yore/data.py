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
    LocationData('Walters Crag: Rope (Co-Climb)', 'Rope', 100, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Walkers Pillar: Rope (Co-Climb)', 'Rope', 101, PeaksOfYoreRegion.ADVANCED),
    LocationData('Great Gaol: Rope (Encounter)', 'Rope', 102, PeaksOfYoreRegion.ADVANCED),
    LocationData('St. Haelga: Rope (Encounter)', 'Rope', 103, PeaksOfYoreRegion.ADVANCED),
    LocationData('Rope (Old Man Of Sjor)', 'Rope', 104, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Hangman\'s Leap: Rope', 'Rope', 105, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Ugsome Storr: Rope', 'Rope', 106, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Eldenhorn: Rope', 'Rope', 107, PeaksOfYoreRegion.ADVANCED),
    LocationData('Ymir\'s Shadow: Rope', 'Rope', 108, PeaksOfYoreRegion.ADVANCED),
    LocationData('Wuthering Crest: Rope', 'Rope', 109, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Great Gaol: Rope', 'Rope', 110, PeaksOfYoreRegion.ADVANCED),
    LocationData('Walter\'s Crag: Rope', 'Rope', 111, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Land\'s End: Rope', 'Rope', 112, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Evergreen\'s End: Rope', 'Rope', 113, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Great Crevice: Rope', 'Rope', 114, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Old Hagger Rope', 'Rope', 115, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Hat', 'Artefact', 200, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Fisherman\'s Cap', 'Artefact', 201, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Safety Helmet', 'Artefact', 202, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Climbing Shoe', 'Artefact', 203, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Shovel', 'Artefact', 204, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Sleeping Bag', 'Artefact', 205, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Backpack', 'Artefact', 206, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Coffee Box (Old Langr)', 'Artefact', 207, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Coffee Box (Wuthering Crest)', 'Artefact', 208, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Chalk Box (Walker\'s Pillar)', 'Artefact', 209, PeaksOfYoreRegion.ADVANCED),
    LocationData('Chalk Box (Eldenhorn)', 'Artefact', 210, PeaksOfYoreRegion.ADVANCED),
    LocationData('Intermediate Trophy', 'Artefact', 211, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Advanced Trophy', 'Artefact', 212, PeaksOfYoreRegion.ADVANCED),
    LocationData('Expert Trophy', 'Artefact', 213, PeaksOfYoreRegion.EXPERT),
    LocationData('Picture Piece #1 (Gray Gully)', 'Artefact', 214, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Picture Piece #2 (Land\'s End)', 'Artefact', 215, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Picture Piece #3 (The Great Crevice)', 'Artefact', 216, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Picture Piece #4 (St. Haelga)', 'Artefact', 217, PeaksOfYoreRegion.ADVANCED),
    LocationData('Picture Frame', 'Artefact', 218, PeaksOfYoreRegion.ADVANCED),
    LocationData('Fundamentals Trophy', 'Artefact', 219, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Bird Seed (Three Brothers)', 'Bird Seed', 400, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Bird Seed (Old Skerry)', 'Bird Seed', 401, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Bird Seed (Great Gaol)', 'Bird Seed', 402, PeaksOfYoreRegion.ADVANCED),
    LocationData('Bird Seed (Eldenhorn)', 'Bird Seed', 403, PeaksOfYoreRegion.ADVANCED),
    LocationData('Bird Seed (Ymir\'s Shadow)', 'Bird Seed', 404, PeaksOfYoreRegion.ADVANCED)
]

full_item_list: list[ItemData] = [
    ItemData('Walters Crag: Rope (Co-Climb)', 'Rope', 100, ItemClassification.filler),
    ItemData('Walkers Pillar: Rope (Co-Climb)', 'Rope', 101, ItemClassification.filler),
    ItemData('Great Gaol: Rope (Encounter)', 'Rope', 102, ItemClassification.filler),
    ItemData('St. Haelga: Rope (Encounter)', 'Rope', 103, ItemClassification.filler),
    ItemData('Rope (Old Man Of Sjor)', 'Rope', 104, ItemClassification.filler),
    ItemData('Hangman\'s Leap: Rope', 'Rope', 105, ItemClassification.filler),
    ItemData('Ugsome Storr: Rope', 'Rope', 106, ItemClassification.filler),
    ItemData('Eldenhorn: Rope', 'Rope', 107, ItemClassification.filler),
    ItemData('Ymir\'s Shadow: Rope', 'Rope', 108, ItemClassification.filler),
    ItemData('Wuthering Crest: Rope', 'Rope', 109, ItemClassification.filler),
    ItemData('Great Gaol: Rope', 'Rope', 110, ItemClassification.filler),
    ItemData('Walter\'s Crag: Rope', 'Rope', 111, ItemClassification.filler),
    ItemData('Land\'s End: Rope', 'Rope', 112, ItemClassification.filler),
    ItemData('Evergreen\'s End: Rope', 'Rope', 113, ItemClassification.filler),
    ItemData('Great Crevice: Rope', 'Rope', 114, ItemClassification.filler),
    ItemData('Old Hagger Rope', 'Rope', 115, ItemClassification.filler),
    ItemData('Hat', 'Artefact', 200, ItemClassification.filler),
    ItemData('Fisherman\'s Cap', 'Artefact', 201, ItemClassification.filler),
    ItemData('Safety Helmet', 'Artefact', 202, ItemClassification.filler),
    ItemData('Climbing Shoe', 'Artefact', 203, ItemClassification.filler),
    ItemData('Shovel', 'Artefact', 204, ItemClassification.filler),
    ItemData('Sleeping Bag', 'Artefact', 205, ItemClassification.filler),
    ItemData('Backpack', 'Artefact', 206, ItemClassification.filler),
    ItemData('Coffee Box (Old Langr)', 'Artefact', 207, ItemClassification.useful),
    ItemData('Coffee Box (Wuthering Crest)', 'Artefact', 208, ItemClassification.useful),
    ItemData('Chalk Box (Walker\'s Pillar)', 'Artefact', 209, ItemClassification.useful),
    ItemData('Chalk Box (Eldenhorn)', 'Artefact', 210, ItemClassification.useful),
    ItemData('Intermediate Trophy', 'Artefact', 211, ItemClassification.filler),
    ItemData('Advanced Trophy', 'Artefact', 212, ItemClassification.filler),
    ItemData('Expert Trophy', 'Artefact', 213, ItemClassification.filler),
    ItemData('Picture Piece #1 (Gray Gully)', 'Artefact', 214, ItemClassification.filler),
    ItemData('Picture Piece #2 (Land\'s End)', 'Artefact', 215, ItemClassification.filler),
    ItemData('Picture Piece #3 (The Great Crevice)', 'Artefact', 216, ItemClassification.filler),
    ItemData('Picture Piece #4 (St. Haelga)', 'Artefact', 217, ItemClassification.filler),
    ItemData('Picture Frame', 'Artefact', 218, ItemClassification.filler),
    ItemData('Fundamentals Trophy', 'Artefact', 219, ItemClassification.filler),
    ItemData('Fundamentals Book', 'Book', 300, ItemClassification.progression),
    ItemData('Intermediate Book', 'Book', 301, ItemClassification.progression),
    ItemData('Advanced Book', 'Book', 302, ItemClassification.progression),
    ItemData('Expert Book', 'Book', 303, ItemClassification.progression),
    ItemData('Bird Seed (Three Brothers)', 'Bird Seed', 400, ItemClassification.filler),
    ItemData('Bird Seed (Old Skerry)', 'Bird Seed', 401, ItemClassification.filler),
    ItemData('Bird Seed (Great Gaol)', 'Bird Seed', 402, ItemClassification.filler),
    ItemData('Bird Seed (Eldenhorn)', 'Bird Seed', 403, ItemClassification.filler),
    ItemData('Bird Seed (Ymir\'s Shadow)', 'Bird Seed', 404, ItemClassification.filler),
    ItemData('Pipe', 'Tool', 500, ItemClassification.useful),
    ItemData('Rope Length Upgrade', 'Tool', 501, ItemClassification.progression),
    ItemData('Barometer', 'Tool', 502, ItemClassification.useful),
    ItemData('Progressive Crampons', 'Tool', 503, ItemClassification.progression),
    ItemData('Monocular', 'Tool', 504, ItemClassification.useful),
    ItemData('Phonograph', 'Tool', 505, ItemClassification.filler),
    ItemData('Pocketwatch', 'Tool', 506, ItemClassification.useful),
    ItemData('Chalkbag', 'Tool', 507, ItemClassification.useful),
    ItemData('Rope Unlock', 'Tool', 508, ItemClassification.progression),
    ItemData('Coffee Unlock', 'Tool', 509, ItemClassification.useful),
    ItemData('Oil Lamp', 'Tool', 510, ItemClassification.useful),
    ItemData('Extra Rope', 'Extra Item', 600, ItemClassification.filler),
    ItemData('Extra Chalk', 'Extra Item', 601, ItemClassification.filler),
    ItemData('Extra Coffee', 'Extra Item', 602, ItemClassification.filler),
    ItemData('Extra Seed', 'Extra Item', 603, ItemClassification.filler)
]
