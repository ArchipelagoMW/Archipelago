from enum import IntEnum


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

    def __init__(self, name: str, item_type: str, item_id: int):
        self.name = name
        self.type = item_type
        self.id = item_id


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
    LocationData('Great Crevice', 'Peak', 17, PeaksOfYoreRegion.FUNDAMENTALS),
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
    LocationData('St Haelga', 'Peak', 34, PeaksOfYoreRegion.ADVANCED),
    LocationData("Ymir's Shadow", 'Peak', 35, PeaksOfYoreRegion.ADVANCED),
    LocationData('Great Bulwark', 'Peak', 36, PeaksOfYoreRegion.EXPERT),
    LocationData('Solemn Tempest', 'Peak', 37, PeaksOfYoreRegion.EXPERT),
    LocationData('Walters Crag: Rope (Co-Climb)', 'Rope', 100, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Walkers Pillar: Rope (Co-Climb)', 'Rope', 101, PeaksOfYoreRegion.ADVANCED),
    LocationData('Great Gaol: Rope (Encounter)', 'Rope', 102, PeaksOfYoreRegion.ADVANCED),
    LocationData('St Haelga: Rope (Encounter)', 'Rope', 103, PeaksOfYoreRegion.ADVANCED),
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
    LocationData('Hat 1', 'Artefact', 200, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Hat 2', 'Artefact', 201, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Helmet', 'Artefact', 202, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Shoe', 'Artefact', 203, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Shovel', 'Artefact', 204, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Sleepingbag', 'Artefact', 205, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Backpack', 'Artefact', 206, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Coffebox 1', 'Artefact', 207, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Coffebox 2', 'Artefact', 208, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Chalkbox 1', 'Artefact', 209, PeaksOfYoreRegion.ADVANCED),
    LocationData('Chalkbox 2', 'Artefact', 210, PeaksOfYoreRegion.ADVANCED),
    LocationData('Climber Statue 1', 'Artefact', 211, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Climber Statue 2', 'Artefact', 212, PeaksOfYoreRegion.ADVANCED),
    LocationData('Climber Statue 3', 'Artefact', 213, PeaksOfYoreRegion.EXPERT),
    LocationData('Photograph 1', 'Artefact', 214, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Photograph 2', 'Artefact', 215, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Photograph 3', 'Artefact', 216, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Photograph 4', 'Artefact', 217, PeaksOfYoreRegion.ADVANCED),
    LocationData('Photograph Frame', 'Artefact', 218, PeaksOfYoreRegion.ADVANCED),
    LocationData('Climber Statue 0', 'Artefact', 219, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Extra Seed 1', 'Bird Seed', 400, PeaksOfYoreRegion.FUNDAMENTALS),
    LocationData('Extra Seed 2', 'Bird Seed', 401, PeaksOfYoreRegion.INTERMEDIATE),
    LocationData('Extra Seed 3', 'Bird Seed', 402, PeaksOfYoreRegion.ADVANCED),
    LocationData('Extra Seed 4', 'Bird Seed', 403, PeaksOfYoreRegion.ADVANCED),
    LocationData('Extra Seed 5', 'Bird Seed', 404, PeaksOfYoreRegion.ADVANCED)
]

full_item_list: list[ItemData] = [
    ItemData('Walters Crag: Rope (Co-Climb)', 'Rope', 100),
    ItemData('Walkers Pillar: Rope (Co-Climb)', 'Rope', 101),
    ItemData('Great Gaol: Rope (Encounter)', 'Rope', 102),
    ItemData('St Haelga: Rope (Encounter)', 'Rope', 103),
    ItemData('Rope (Old Man Of Sjor)', 'Rope', 104),
    ItemData('Hangman\'s Leap: Rope', 'Rope', 105),
    ItemData('Ugsome Storr: Rope', 'Rope', 106),
    ItemData('Eldenhorn: Rope', 'Rope', 107),
    ItemData('Ymir\'s Shadow: Rope', 'Rope', 108),
    ItemData('Wuthering Crest: Rope', 'Rope', 109),
    ItemData('Great Gaol: Rope', 'Rope', 110),
    ItemData('Walter\'s Crag: Rope', 'Rope', 111),
    ItemData('Land\'s End: Rope', 'Rope', 112),
    ItemData('Evergreen\'s End: Rope', 'Rope', 113),
    ItemData('Great Crevice: Rope', 'Rope', 114),
    ItemData('Old Hagger Rope', 'Rope', 115),
    ItemData('Hat 1', 'Artefact', 200),
    ItemData('Hat 2', 'Artefact', 201),
    ItemData('Helmet', 'Artefact', 202),
    ItemData('Shoe', 'Artefact', 203),
    ItemData('Shovel', 'Artefact', 204),
    ItemData('Sleepingbag', 'Artefact', 205),
    ItemData('Backpack', 'Artefact', 206),
    ItemData('Coffebox 1', 'Artefact', 207),
    ItemData('Coffebox 2', 'Artefact', 208),
    ItemData('Chalkbox 1', 'Artefact', 209),
    ItemData('Chalkbox 2', 'Artefact', 210),
    ItemData('Climber Statue 1', 'Artefact', 211),
    ItemData('Climber Statue 2', 'Artefact', 212),
    ItemData('Climber Statue 3', 'Artefact', 213),
    ItemData('Photograph 1', 'Artefact', 214),
    ItemData('Photograph 2', 'Artefact', 215),
    ItemData('Photograph 3', 'Artefact', 216),
    ItemData('Photograph 4', 'Artefact', 217),
    ItemData('Photograph Frame', 'Artefact', 218),
    ItemData('Climber Statue 0', 'Artefact', 219),
    ItemData('Fundamentals Book', 'Book', 300),
    ItemData('Intermediate Book', 'Book', 301),
    ItemData('Advanced Book', 'Book', 302),
    ItemData('Expert Book', 'Book', 303),
    ItemData('Extra Seed 1', 'Bird Seed', 400),
    ItemData('Extra Seed 2', 'Bird Seed', 401),
    ItemData('Extra Seed 3', 'Bird Seed', 402),
    ItemData('Extra Seed 4', 'Bird Seed', 403),
    ItemData('Extra Seed 5', 'Bird Seed', 404),
    ItemData('Pipe', 'Tool', 500),
    ItemData('Rope Length Upgrade', 'Tool', 501),
    ItemData('Barometer', 'Tool', 502),
    ItemData('Progressive Crampons', 'Tool', 503),
    ItemData('Monocular', 'Tool', 504),
    ItemData('Phonograph', 'Tool', 505),
    ItemData('Pocketwatch', 'Tool', 506),
    ItemData('Chalkbag', 'Tool', 507),
    ItemData('Rope Unlock', 'Tool', 508),
    ItemData('Extra Rope', 'Extra Item', 600),
    ItemData('Extra Chalk', 'Extra Item', 601),
    ItemData('Extra Coffee', 'Extra Item', 602),
    ItemData('Extra Seed', 'Extra Item', 603)
]
