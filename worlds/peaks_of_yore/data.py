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
    name: str  # I'm storing them both in a single class
    id: int
    classification: ItemClassification

    def __init__(self, name: str, index: int, classification: ItemClassification = ItemClassification.filler):
        self.name = name
        self.id = index
        self.classification = classification

    def offset(self, offset: int, name: str = ""):
        if name == "":
            name = self.name
        return ItemOrLocation(name, self.id + offset, self.classification)


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

peaks_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [
        ItemOrLocation("Greenhorn's Top", 0 + peak_offset),
        ItemOrLocation('Paltry Peak', 1 + peak_offset),
        ItemOrLocation('Old Mill', 2 + peak_offset),
        ItemOrLocation('Gray Gully', 3 + peak_offset),
        ItemOrLocation('Lighthouse', 4 + peak_offset),
        ItemOrLocation('Old Man Of Sjór', 5 + peak_offset),
        ItemOrLocation('Giants Shelf', 6 + peak_offset),
        ItemOrLocation("Evergreen's End", 7 + peak_offset),
        ItemOrLocation('The Twins', 8 + peak_offset),
        ItemOrLocation("Old Grove's Skelf", 9 + peak_offset),
        ItemOrLocation("Land's End", 10 + peak_offset),
        ItemOrLocation("Hangman's Leap", 11 + peak_offset),
        ItemOrLocation('Old Langr', 12 + peak_offset),
        ItemOrLocation('Aldr Grotto', 13 + peak_offset),
        ItemOrLocation('Three Brothers', 14 + peak_offset),
        ItemOrLocation("Walter's Crag", 15 + peak_offset),
        ItemOrLocation('The Great Crevice', 16 + peak_offset),
        ItemOrLocation('Old Hagger', 17 + peak_offset),
        ItemOrLocation('Ugsome Storr', 18 + peak_offset),
        ItemOrLocation('Wuthering Crest', 19 + peak_offset)
    ],
    PeaksOfYoreRegion.INTERMEDIATE: [
        ItemOrLocation("Porter's Boulders", 20 + peak_offset),
        ItemOrLocation("Jotunn's Thumb", 21 + peak_offset),
        ItemOrLocation('Old Skerry', 22 + peak_offset),
        ItemOrLocation('Hamarr Stone', 23 + peak_offset),
        ItemOrLocation("Giant's Nose", 24 + peak_offset),
        ItemOrLocation("Walter's Boulder", 25 + peak_offset),
        ItemOrLocation('Sundered Sons', 26 + peak_offset),
        ItemOrLocation("Old Weald's Boulder", 27 + peak_offset),
        ItemOrLocation('Leaning Spire', 28 + peak_offset),
        ItemOrLocation('Cromlech', 29 + peak_offset),
    ],
    PeaksOfYoreRegion.ADVANCED: [
        ItemOrLocation("Walker's Pillar", 30 + peak_offset),
        ItemOrLocation('Eldenhorn', 31 + peak_offset),
        ItemOrLocation('Great Gaol', 32 + peak_offset),
        ItemOrLocation('St. Haelga', 33 + peak_offset),
        ItemOrLocation("Ymir's Shadow", 34 + peak_offset),
    ],
    PeaksOfYoreRegion.EXPERT: [
        ItemOrLocation('Great Bulwark', 35 + peak_offset),
        ItemOrLocation('Solemn Tempest', 36 + peak_offset),
    ],
    PeaksOfYoreRegion.NONE: []
}

ropes_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [
        ItemOrLocation('Walters Crag: Rope (Co-Climb)', 0 + rope_offset),
        # the in game ropes are shuffled around a bit,
        # this is also why they are in this weird order here
        ItemOrLocation('Old Man Of Sjór: Rope', 4 + rope_offset),
        ItemOrLocation('Hangman\'s Leap: Rope', 5 + rope_offset),
        ItemOrLocation('Ugsome Storr: Rope', 6 + rope_offset),
        ItemOrLocation('Wuthering Crest: Rope', 9 + rope_offset),
        ItemOrLocation('Walter\'s Crag: Rope', 11 + rope_offset),
        ItemOrLocation('Land\'s End: Rope', 12 + rope_offset),
        ItemOrLocation('Evergreen\'s End: Rope', 13 + rope_offset),
        ItemOrLocation('The Great Crevice: Rope', 14 + rope_offset),
        ItemOrLocation('Old Hagger Rope', 15 + rope_offset),
    ],
    PeaksOfYoreRegion.INTERMEDIATE: [],
    PeaksOfYoreRegion.ADVANCED: [
        ItemOrLocation('Walkers Pillar: Rope (Co-Climb)', 1 + rope_offset),
        ItemOrLocation('Great Gaol: Rope (Encounter)', 2 + rope_offset),
        ItemOrLocation('St. Haelga: Rope (Encounter)', 3 + rope_offset),
        ItemOrLocation('Eldenhorn: Rope', 7 + rope_offset),
        ItemOrLocation('Ymir\'s Shadow: Rope', 8 + rope_offset),
        ItemOrLocation('Great Gaol: Rope', 10 + rope_offset),
    ],
    PeaksOfYoreRegion.EXPERT: [],
    PeaksOfYoreRegion.NONE: []
}

artefacts_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [
        ItemOrLocation('Old Mill: Hat', 0 + artefact_offset),
        ItemOrLocation('Evergreen\'s End: Fisherman\'s Cap', 1 + artefact_offset),
        ItemOrLocation('Old Grove\'s Skelf: Safety Helmet', 2 + artefact_offset),
        ItemOrLocation('Old Man Of Sjór: Climbing Shoe', 3 + artefact_offset),
        ItemOrLocation('Three Brothers: Shovel', 4 + artefact_offset),
        ItemOrLocation('Giant\'s Shelf: Sleeping Bag', 5 + artefact_offset),
        ItemOrLocation('Aldr Grotto: Backpack', 6 + artefact_offset),
        ItemOrLocation('Old Langr: Coffee Box', 7 + artefact_offset, ItemClassification.useful),
        ItemOrLocation('Wuthering Crest: Coffee Box', 8 + artefact_offset, ItemClassification.useful),
        ItemOrLocation('Gray Gully: Picture Piece #1', 14 + artefact_offset),
        ItemOrLocation('Land\'s End: Picture Piece #2', 15 + artefact_offset),
        ItemOrLocation('The Great Crevice: Picture Piece #3', 16 + artefact_offset),
        ItemOrLocation('Walter\'s Crag: Fundamentals Trophy', 19 + artefact_offset),
    ],
    PeaksOfYoreRegion.INTERMEDIATE: [
        ItemOrLocation('Leaning Spire: Intermediate Trophy', 11 + artefact_offset),
    ],
    PeaksOfYoreRegion.ADVANCED: [
        ItemOrLocation('Walker\'s Pillar: Chalk Box', 9 + artefact_offset, ItemClassification.useful),
        ItemOrLocation('Eldenhorn: Chalk Box', 10 + artefact_offset, ItemClassification.useful),
        ItemOrLocation('Ymir\'s Shadow: Advanced Trophy', 12 + artefact_offset),
        ItemOrLocation('St. Haelga: Picture Piece #4', 17 + artefact_offset),
        ItemOrLocation('Great Gaol: Picture Frame', 18 + artefact_offset),
    ],
    PeaksOfYoreRegion.EXPERT: [
        ItemOrLocation('The Great Bulwark: Expert Trophy', 13 + artefact_offset),
    ],
    PeaksOfYoreRegion.NONE: []
}

books_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [],
    PeaksOfYoreRegion.INTERMEDIATE: [],
    PeaksOfYoreRegion.ADVANCED: [],
    PeaksOfYoreRegion.EXPERT: [],
    PeaksOfYoreRegion.NONE: [
        ItemOrLocation('Fundamentals Book', 0 + book_offset, ItemClassification.progression),
        ItemOrLocation('Intermediate Book', 1 + book_offset, ItemClassification.progression),
        ItemOrLocation('Advanced Book', 2 + book_offset, ItemClassification.progression),
        ItemOrLocation('Expert Book', 3 + book_offset, ItemClassification.progression),
    ]
}

bird_seeds_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [
        ItemOrLocation('Three Brothers: Bird Seed', 0 + bird_seed_offset),
    ],
    PeaksOfYoreRegion.INTERMEDIATE: [
        ItemOrLocation('Old Skerry: Bird Seed', 1 + bird_seed_offset),
    ],
    PeaksOfYoreRegion.ADVANCED: [
        ItemOrLocation('Great Gaol: Bird Seed', 2 + bird_seed_offset),
        ItemOrLocation('Eldenhorn: Bird Seed', 3 + bird_seed_offset),
    ],
    PeaksOfYoreRegion.EXPERT: [],
    PeaksOfYoreRegion.NONE: []
}

tools_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [],
    PeaksOfYoreRegion.INTERMEDIATE: [],
    PeaksOfYoreRegion.ADVANCED: [],
    PeaksOfYoreRegion.EXPERT: [],
    PeaksOfYoreRegion.NONE: [
        ItemOrLocation('Pipe', 0 + tool_offset, ItemClassification.useful),
        ItemOrLocation('Rope Length Upgrade', 1 + tool_offset, ItemClassification.progression),
        ItemOrLocation('Barometer', 2 + tool_offset, ItemClassification.useful),
        ItemOrLocation('Progressive Crampons', 3 + tool_offset, ItemClassification.progression),
        ItemOrLocation('Monocular', 4 + tool_offset, ItemClassification.useful),
        ItemOrLocation('Phonograph', 5 + tool_offset, ItemClassification.filler),
        ItemOrLocation('Pocketwatch', 6 + tool_offset, ItemClassification.progression),
        ItemOrLocation('Chalkbag', 7 + tool_offset, ItemClassification.useful),
        ItemOrLocation('Rope Unlock', 8 + tool_offset, ItemClassification.progression),
        ItemOrLocation('Coffee Unlock', 9 + tool_offset, ItemClassification.useful),
        ItemOrLocation('Oil Lamp', 10 + tool_offset, ItemClassification.useful),
        ItemOrLocation('Left Hand', 11 + tool_offset, ItemClassification.progression),
        ItemOrLocation('Right Hand', 12 + tool_offset, ItemClassification.progression),
    ]
}

extra_items_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [],
    PeaksOfYoreRegion.INTERMEDIATE: [],
    PeaksOfYoreRegion.ADVANCED: [],
    PeaksOfYoreRegion.EXPERT: [],
    PeaksOfYoreRegion.NONE: [
        ItemOrLocation('Extra Rope', 0 + extra_item_offset, ItemClassification.filler),
        ItemOrLocation('Extra Chalk', 1 + extra_item_offset, ItemClassification.filler),
        ItemOrLocation('Extra Coffee', 2 + extra_item_offset, ItemClassification.filler),
        ItemOrLocation('Extra Seed', 3 + extra_item_offset, ItemClassification.filler)
    ]
}

# item lists below are generated based on previous lists
free_solo_peak_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [],
    PeaksOfYoreRegion.INTERMEDIATE: [],
    PeaksOfYoreRegion.ADVANCED: [p.offset(free_solo_peak_offset - peak_offset, p.name + " (Free Solo)") for p in
                                 peaks_list[PeaksOfYoreRegion.ADVANCED]],
    PeaksOfYoreRegion.EXPERT: [p.offset(free_solo_peak_offset - peak_offset, p.name + " (Free Solo)") for p in
                               peaks_list[PeaksOfYoreRegion.EXPERT]],
    PeaksOfYoreRegion.NONE: []
}

time_attack_time_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [p.offset(time_attack_time_offset - peak_offset, p.name + ": Time record") for p
                                     in peaks_list[PeaksOfYoreRegion.FUNDAMENTALS]],
    PeaksOfYoreRegion.INTERMEDIATE: [p.offset(time_attack_time_offset - peak_offset, p.name + ": Time record") for p
                                     in peaks_list[PeaksOfYoreRegion.INTERMEDIATE]],
    PeaksOfYoreRegion.ADVANCED: [p.offset(time_attack_time_offset - peak_offset, p.name + ": Time record") for p in
                                 peaks_list[PeaksOfYoreRegion.ADVANCED]],
    PeaksOfYoreRegion.EXPERT: [],
    PeaksOfYoreRegion.NONE: []
}

time_attack_holds_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [p.offset(time_attack_holds_offset - peak_offset, p.name + ": Holds record") for p
                                     in peaks_list[PeaksOfYoreRegion.FUNDAMENTALS]],
    PeaksOfYoreRegion.INTERMEDIATE: [p.offset(time_attack_holds_offset - peak_offset, p.name + ": Holds record") for p
                                     in peaks_list[PeaksOfYoreRegion.INTERMEDIATE]],
    PeaksOfYoreRegion.ADVANCED: [p.offset(time_attack_holds_offset - peak_offset, p.name + ": Holds record") for p in
                                 peaks_list[PeaksOfYoreRegion.ADVANCED]],
    PeaksOfYoreRegion.EXPERT: [],
    PeaksOfYoreRegion.NONE: []
}

time_attack_ropes_list: dict[PeaksOfYoreRegion, list[ItemOrLocation]] = {
    PeaksOfYoreRegion.FUNDAMENTALS: [p.offset(time_attack_ropes_offset - peak_offset, p.name + ": Ropes record") for p
                                     in peaks_list[PeaksOfYoreRegion.FUNDAMENTALS]],
    PeaksOfYoreRegion.INTERMEDIATE: [p.offset(time_attack_ropes_offset - peak_offset, p.name + ": Ropes record") for p
                                     in peaks_list[PeaksOfYoreRegion.INTERMEDIATE]],
    PeaksOfYoreRegion.ADVANCED: [p.offset(time_attack_ropes_offset - peak_offset, p.name + ": Ropes record") for p in
                                 peaks_list[PeaksOfYoreRegion.ADVANCED]],
    PeaksOfYoreRegion.EXPERT: [],
    PeaksOfYoreRegion.NONE: []
}


def get_all_items_or_locations(d: dict[PeaksOfYoreRegion: list[ItemOrLocation]]) -> list[ItemOrLocation]:
    # the unholy double unpack making me reap what I sow
    return [*d[PeaksOfYoreRegion.FUNDAMENTALS], *d[PeaksOfYoreRegion.INTERMEDIATE], *d[PeaksOfYoreRegion.ADVANCED]
            , *d[PeaksOfYoreRegion.EXPERT], *d[PeaksOfYoreRegion.NONE]]


def create_full_location_table() -> dict[str: ItemOrLocation]:
    ropes = {i.name: i for i in get_all_items_or_locations(ropes_list)}
    artefacts = {i.name: i for i in get_all_items_or_locations(artefacts_list)}
    bird_seeds = {i.name: i for i in get_all_items_or_locations(bird_seeds_list)}

    peaks = {i.name: i for i in get_all_items_or_locations(peaks_list)}
    free_solo_peaks = {i.name: i for i in get_all_items_or_locations(free_solo_peak_list)}
    time_attack_time = {i.name: i for i in get_all_items_or_locations(time_attack_time_list)}
    time_attack_ropes = {i.name: i for i in get_all_items_or_locations(time_attack_ropes_list)}
    time_attack_holds = {i.name: i for i in get_all_items_or_locations(time_attack_holds_list)}

    return {**artefacts, **bird_seeds, **peaks, **free_solo_peaks, **time_attack_time, **time_attack_ropes,
            **time_attack_holds, **ropes}


def create_full_item_table() -> dict[str:ItemOrLocation]:
    ropes = {i.name: i for i in get_all_items_or_locations(ropes_list)}
    artefacts = {i.name: i for i in get_all_items_or_locations(artefacts_list)} # remove peak name from Artefact name
    books = {i.name: i for i in get_all_items_or_locations(books_list)}
    bird_seeds = {i.name: i for i in get_all_items_or_locations(bird_seeds_list)}
    tools = {i.name: i for i in get_all_items_or_locations(tools_list)}
    extra_items = {i.name: i for i in get_all_items_or_locations(extra_items_list)}

    return {**ropes, **artefacts, **books, **bird_seeds, **tools, **extra_items}


full_item_table: dict[str, ItemOrLocation] = create_full_item_table()
full_location_table: dict[str, ItemOrLocation] = create_full_location_table()
