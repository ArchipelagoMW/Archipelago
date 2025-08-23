# This file was generated using jinja2 from a template. If this file needs
# to be changed, either change the template, or the code leveraging the template.
from typing import List, NamedTuple, Dict
from worlds.gstla.GameData import ElementType, ItemType
from BaseClasses import ItemClassification
from .ItemNames import name_by_item_id

class InternalItemData(NamedTuple):
    id: int
    name: str
    progression: ItemClassification
    addr: int
    type: ItemType
    # TODO: The event type is really a property of the locations, not of the items
    # event_type:int = 131
    is_mimic: bool =  False
    is_rare: bool = False

class InternalDjinnItemData(InternalItemData):
    element: ElementType
    vanilla_id: int
    stats_addr: int
    stats: List[int]

    def __new__(cls, id: int, name: str, addr: int, element: ElementType, stats_addr: int, stats: List[int]):
        self = super(InternalItemData, cls).__new__(cls, (addr, name, ItemClassification.progression_skip_balancing, addr, ItemType.Djinn))
        self.element = element
        self.stats_addr = stats_addr
        self.stats = stats
        self.vanilla_id = id
        return self

    def get_rando_flag(self):
        return 0x30 + self.element * 20 + self.vanilla_id

class InternalEventItemData(InternalItemData):
    flag: int
    location: str

    def __new__(cls, event_id: int, flag: int, location: str, name: str):
        self = super(InternalItemData, cls).__new__(cls, (event_id, name, ItemClassification.progression, 0, ItemType.Event, 0))
        self.location = location
        self.flag = flag
        return self

summon_list: List[InternalItemData] = [
    InternalItemData(3840, name_by_item_id[3840], ItemClassification.useful, 791824, ItemType.Summon),
    InternalItemData(3841, name_by_item_id[3841], ItemClassification.useful, 791832, ItemType.Summon),
    InternalItemData(3842, name_by_item_id[3842], ItemClassification.useful, 791840, ItemType.Summon),
    InternalItemData(3843, name_by_item_id[3843], ItemClassification.useful, 791848, ItemType.Summon),
    InternalItemData(3844, name_by_item_id[3844], ItemClassification.useful, 791856, ItemType.Summon),
    InternalItemData(3845, name_by_item_id[3845], ItemClassification.useful, 791864, ItemType.Summon),
    InternalItemData(3846, name_by_item_id[3846], ItemClassification.useful, 791872, ItemType.Summon),
    InternalItemData(3847, name_by_item_id[3847], ItemClassification.useful, 791880, ItemType.Summon),
    InternalItemData(3848, name_by_item_id[3848], ItemClassification.useful, 791888, ItemType.Summon),
    InternalItemData(3849, name_by_item_id[3849], ItemClassification.useful, 791896, ItemType.Summon),
    InternalItemData(3850, name_by_item_id[3850], ItemClassification.useful, 791904, ItemType.Summon),
    InternalItemData(3851, name_by_item_id[3851], ItemClassification.useful, 791912, ItemType.Summon),
    InternalItemData(3852, name_by_item_id[3852], ItemClassification.useful, 791920, ItemType.Summon),
    InternalItemData(3853, name_by_item_id[3853], ItemClassification.useful, 791928, ItemType.Summon),
    InternalItemData(3854, name_by_item_id[3854], ItemClassification.useful, 791936, ItemType.Summon),
    InternalItemData(3855, name_by_item_id[3855], ItemClassification.useful, 791944, ItemType.Summon),
    InternalItemData(3856, name_by_item_id[3856], ItemClassification.useful, 791952, ItemType.Summon),
    InternalItemData(3857, name_by_item_id[3857], ItemClassification.useful, 791960, ItemType.Summon),
    InternalItemData(3858, name_by_item_id[3858], ItemClassification.useful, 791968, ItemType.Summon),
    InternalItemData(3859, name_by_item_id[3859], ItemClassification.useful, 791976, ItemType.Summon),
    InternalItemData(3860, name_by_item_id[3860], ItemClassification.useful, 791984, ItemType.Summon),
    InternalItemData(3861, name_by_item_id[3861], ItemClassification.useful, 791992, ItemType.Summon),
    InternalItemData(3862, name_by_item_id[3862], ItemClassification.useful, 792000, ItemType.Summon),
    InternalItemData(3863, name_by_item_id[3863], ItemClassification.useful, 792008, ItemType.Summon),
    InternalItemData(3864, name_by_item_id[3864], ItemClassification.useful, 792016, ItemType.Summon),
    InternalItemData(3865, name_by_item_id[3865], ItemClassification.useful, 792024, ItemType.Summon),
    InternalItemData(3866, name_by_item_id[3866], ItemClassification.useful, 792032, ItemType.Summon),
    InternalItemData(3867, name_by_item_id[3867], ItemClassification.useful, 792040, ItemType.Summon),
    InternalItemData(3868, name_by_item_id[3868], ItemClassification.useful, 792048, ItemType.Summon),
    
]

psyenergy_list: List[InternalItemData] = [
    InternalItemData(3596, name_by_item_id[3596], ItemClassification.progression, 3596, ItemType.Psyenergy),
    InternalItemData(3662, name_by_item_id[3662], ItemClassification.progression, 3662, ItemType.Psyenergy),
    InternalItemData(3722, name_by_item_id[3722], ItemClassification.progression, 3722, ItemType.Psyenergy),
    InternalItemData(3723, name_by_item_id[3723], ItemClassification.progression, 3723, ItemType.Psyenergy),
    InternalItemData(3725, name_by_item_id[3725], ItemClassification.progression, 3725, ItemType.Psyenergy),
    InternalItemData(3728, name_by_item_id[3728], ItemClassification.progression, 3728, ItemType.Psyenergy),
    InternalItemData(3738, name_by_item_id[3738], ItemClassification.progression, 3738, ItemType.Psyenergy),
    
]

psyenergy_as_item_list: List[InternalItemData] = [
    InternalItemData(133 + 0xE00, name_by_item_id[133 + 0xE00], ItemClassification.progression, 738668, ItemType.PsyenergyItem),
    InternalItemData(134 + 0xE00, name_by_item_id[134 + 0xE00], ItemClassification.progression, 738712, ItemType.PsyenergyItem),
    InternalItemData(142 + 0xE00, name_by_item_id[142 + 0xE00], ItemClassification.progression, 738756, ItemType.PsyenergyItem),
    InternalItemData(33 + 0xE00, name_by_item_id[33 + 0xE00], ItemClassification.progression, 738800, ItemType.PsyenergyItem),
    InternalItemData(24 + 0xE00, name_by_item_id[24 + 0xE00], ItemClassification.progression, 738844, ItemType.PsyenergyItem),
    InternalItemData(143 + 0xE00, name_by_item_id[143 + 0xE00], ItemClassification.progression, 738888, ItemType.PsyenergyItem),
    InternalItemData(145 + 0xE00, name_by_item_id[145 + 0xE00], ItemClassification.progression, 738932, ItemType.PsyenergyItem),
    InternalItemData(146 + 0xE00, name_by_item_id[146 + 0xE00], ItemClassification.progression, 738976, ItemType.PsyenergyItem),
    InternalItemData(147 + 0xE00, name_by_item_id[147 + 0xE00], ItemClassification.progression, 739020, ItemType.PsyenergyItem),
    InternalItemData(148 + 0xE00, name_by_item_id[148 + 0xE00], ItemClassification.progression, 739064, ItemType.PsyenergyItem),
    InternalItemData(135 + 0xE00, name_by_item_id[135 + 0xE00], ItemClassification.progression, 739108, ItemType.PsyenergyItem),
    InternalItemData(136 + 0xE00, name_by_item_id[136 + 0xE00], ItemClassification.progression, 739152, ItemType.PsyenergyItem),
    InternalItemData(137 + 0xE00, name_by_item_id[137 + 0xE00], ItemClassification.progression, 739196, ItemType.PsyenergyItem),
    InternalItemData(151 + 0xE00, name_by_item_id[151 + 0xE00], ItemClassification.progression, 739328, ItemType.PsyenergyItem),
    InternalItemData(152 + 0xE00, name_by_item_id[152 + 0xE00], ItemClassification.progression, 739372, ItemType.PsyenergyItem),
    InternalItemData(153 + 0xE00, name_by_item_id[153 + 0xE00], ItemClassification.progression, 739416, ItemType.PsyenergyItem),
    InternalItemData(156 + 0xE00, name_by_item_id[156 + 0xE00], ItemClassification.progression, 739504, ItemType.PsyenergyItem),
    
]

djinn_items: List[InternalDjinnItemData] = [
    InternalDjinnItemData(0, name_by_item_id[16384000], 16384000, ElementType(0), 814004, [8, 4, 3, 0, 0, 0]),
    InternalDjinnItemData(1, name_by_item_id[16384002], 16384002, ElementType(0), 814016, [9, 0, 0, 2, 2, 1]),
    InternalDjinnItemData(2, name_by_item_id[16384004], 16384004, ElementType(0), 814028, [10, 3, 0, 0, 3, 0]),
    InternalDjinnItemData(3, name_by_item_id[16384006], 16384006, ElementType(0), 814040, [12, 4, 0, 3, 0, 1]),
    InternalDjinnItemData(4, name_by_item_id[16384008], 16384008, ElementType(0), 814052, [10, 0, 3, 0, 0, 1]),
    InternalDjinnItemData(5, name_by_item_id[16384010], 16384010, ElementType(0), 814064, [9, 3, 0, 0, 3, 0]),
    InternalDjinnItemData(6, name_by_item_id[16384012], 16384012, ElementType(0), 814076, [12, 0, 4, 0, 0, 0]),
    InternalDjinnItemData(7, name_by_item_id[16384014], 16384014, ElementType(0), 814088, [9, 4, 3, 0, 0, 0]),
    InternalDjinnItemData(8, name_by_item_id[16384016], 16384016, ElementType(0), 814100, [11, 0, 0, 2, 3, 0]),
    InternalDjinnItemData(9, name_by_item_id[16384018], 16384018, ElementType(0), 814112, [9, 0, 4, 2, 0, 1]),
    InternalDjinnItemData(10, name_by_item_id[16384020], 16384020, ElementType(0), 814124, [10, 4, 0, 0, 3, 0]),
    InternalDjinnItemData(11, name_by_item_id[16384022], 16384022, ElementType(0), 814136, [12, 4, 0, 0, 0, 0]),
    InternalDjinnItemData(12, name_by_item_id[16384024], 16384024, ElementType(0), 814148, [9, 0, 0, 0, 4, 1]),
    InternalDjinnItemData(13, name_by_item_id[16384026], 16384026, ElementType(0), 814160, [11, 0, 0, 3, 0, 0]),
    InternalDjinnItemData(14, name_by_item_id[16384028], 16384028, ElementType(0), 814172, [9, 5, 0, 0, 0, 1]),
    InternalDjinnItemData(15, name_by_item_id[16384030], 16384030, ElementType(0), 814184, [12, 0, 6, 0, 0, 0]),
    InternalDjinnItemData(16, name_by_item_id[16384032], 16384032, ElementType(0), 814196, [8, 0, 4, 0, 2, 1]),
    InternalDjinnItemData(17, name_by_item_id[16384034], 16384034, ElementType(0), 814208, [10, 5, 0, 2, 0, 0]),
    InternalDjinnItemData(0, name_by_item_id[16384036], 16384036, ElementType(1), 814244, [9, 4, 0, 3, 0, 0]),
    InternalDjinnItemData(1, name_by_item_id[16384038], 16384038, ElementType(1), 814256, [12, 0, 3, 0, 0, 1]),
    InternalDjinnItemData(2, name_by_item_id[16384040], 16384040, ElementType(1), 814268, [11, 0, 4, 0, 0, 0]),
    InternalDjinnItemData(3, name_by_item_id[16384042], 16384042, ElementType(1), 814280, [8, 4, 0, 0, 3, 0]),
    InternalDjinnItemData(4, name_by_item_id[16384044], 16384044, ElementType(1), 814292, [9, 0, 4, 0, 0, 1]),
    InternalDjinnItemData(5, name_by_item_id[16384046], 16384046, ElementType(1), 814304, [8, 3, 0, 2, 0, 2]),
    InternalDjinnItemData(6, name_by_item_id[16384048], 16384048, ElementType(1), 814316, [13, 4, 0, 0, 4, 0]),
    InternalDjinnItemData(7, name_by_item_id[16384050], 16384050, ElementType(1), 814328, [9, 0, 0, 2, 2, 1]),
    InternalDjinnItemData(8, name_by_item_id[16384052], 16384052, ElementType(1), 814340, [8, 4, 3, 0, 0, 0]),
    InternalDjinnItemData(9, name_by_item_id[16384054], 16384054, ElementType(1), 814352, [11, 5, 0, 0, 0, 0]),
    InternalDjinnItemData(10, name_by_item_id[16384056], 16384056, ElementType(1), 814364, [9, 0, 0, 3, 0, 2]),
    InternalDjinnItemData(11, name_by_item_id[16384058], 16384058, ElementType(1), 814376, [10, 3, 0, 2, 0, 0]),
    InternalDjinnItemData(12, name_by_item_id[16384060], 16384060, ElementType(1), 814388, [10, 0, 5, 0, 0, 0]),
    InternalDjinnItemData(13, name_by_item_id[16384062], 16384062, ElementType(1), 814400, [10, 6, 0, 0, 0, 0]),
    InternalDjinnItemData(14, name_by_item_id[16384064], 16384064, ElementType(1), 814412, [9, 0, 5, 0, 2, 0]),
    InternalDjinnItemData(15, name_by_item_id[16384066], 16384066, ElementType(1), 814424, [9, 0, 0, 0, 3, 2]),
    InternalDjinnItemData(16, name_by_item_id[16384068], 16384068, ElementType(1), 814436, [13, 4, 0, 0, 0, 0]),
    InternalDjinnItemData(17, name_by_item_id[16384070], 16384070, ElementType(1), 814448, [12, 0, 3, 0, 0, 0]),
    InternalDjinnItemData(0, name_by_item_id[16384072], 16384072, ElementType(2), 814484, [10, 0, 2, 0, 2, 2]),
    InternalDjinnItemData(1, name_by_item_id[16384074], 16384074, ElementType(2), 814496, [8, 0, 3, 0, 2, 0]),
    InternalDjinnItemData(2, name_by_item_id[16384076], 16384076, ElementType(2), 814508, [12, 3, 0, 3, 0, 1]),
    InternalDjinnItemData(3, name_by_item_id[16384078], 16384078, ElementType(2), 814520, [8, 0, 3, 0, 0, 0]),
    InternalDjinnItemData(4, name_by_item_id[16384080], 16384080, ElementType(2), 814532, [9, 4, 0, 2, 2, 0]),
    InternalDjinnItemData(5, name_by_item_id[16384082], 16384082, ElementType(2), 814544, [14, 3, 0, 2, 0, 0]),
    InternalDjinnItemData(6, name_by_item_id[16384084], 16384084, ElementType(2), 814556, [9, 0, 3, 0, 0, 1]),
    InternalDjinnItemData(7, name_by_item_id[16384086], 16384086, ElementType(2), 814568, [10, 0, 3, 0, 0, 0]),
    InternalDjinnItemData(8, name_by_item_id[16384088], 16384088, ElementType(2), 814580, [11, 6, 0, 0, 0, 0]),
    InternalDjinnItemData(9, name_by_item_id[16384090], 16384090, ElementType(2), 814592, [8, 0, 5, 0, 0, 1]),
    InternalDjinnItemData(10, name_by_item_id[16384092], 16384092, ElementType(2), 814604, [9, 0, 2, 0, 2, 1]),
    InternalDjinnItemData(11, name_by_item_id[16384094], 16384094, ElementType(2), 814616, [11, 3, 0, 0, 3, 0]),
    InternalDjinnItemData(12, name_by_item_id[16384096], 16384096, ElementType(2), 814628, [9, 0, 0, 3, 0, 2]),
    InternalDjinnItemData(13, name_by_item_id[16384098], 16384098, ElementType(2), 814640, [8, 0, 4, 2, 0, 0]),
    InternalDjinnItemData(14, name_by_item_id[16384100], 16384100, ElementType(2), 814652, [12, 5, 0, 0, 0, 0]),
    InternalDjinnItemData(15, name_by_item_id[16384102], 16384102, ElementType(2), 814664, [9, 0, 3, 3, 2, 0]),
    InternalDjinnItemData(16, name_by_item_id[16384104], 16384104, ElementType(2), 814676, [12, 4, 0, 0, 0, 0]),
    InternalDjinnItemData(17, name_by_item_id[16384106], 16384106, ElementType(2), 814688, [11, 4, 0, 2, 0, 0]),
    InternalDjinnItemData(0, name_by_item_id[16384108], 16384108, ElementType(3), 814724, [9, 0, 2, 0, 2, 0]),
    InternalDjinnItemData(1, name_by_item_id[16384110], 16384110, ElementType(3), 814736, [12, 5, 0, 2, 0, 1]),
    InternalDjinnItemData(2, name_by_item_id[16384112], 16384112, ElementType(3), 814748, [11, 3, 0, 0, 2, 1]),
    InternalDjinnItemData(3, name_by_item_id[16384114], 16384114, ElementType(3), 814760, [9, 0, 3, 0, 0, 0]),
    InternalDjinnItemData(4, name_by_item_id[16384116], 16384116, ElementType(3), 814772, [8, 4, 0, 0, 3, 0]),
    InternalDjinnItemData(5, name_by_item_id[16384118], 16384118, ElementType(3), 814784, [10, 0, 5, 0, 0, 0]),
    InternalDjinnItemData(6, name_by_item_id[16384120], 16384120, ElementType(3), 814796, [11, 5, 0, 2, 0, 1]),
    InternalDjinnItemData(7, name_by_item_id[16384122], 16384122, ElementType(3), 814808, [9, 0, 0, 3, 4, 0]),
    InternalDjinnItemData(8, name_by_item_id[16384124], 16384124, ElementType(3), 814820, [10, 4, 3, 0, 0, 0]),
    InternalDjinnItemData(9, name_by_item_id[16384126], 16384126, ElementType(3), 814832, [8, 4, 0, 0, 3, 2]),
    InternalDjinnItemData(10, name_by_item_id[16384128], 16384128, ElementType(3), 814844, [11, 0, 4, 0, 0, 0]),
    InternalDjinnItemData(11, name_by_item_id[16384130], 16384130, ElementType(3), 814856, [10, 0, 0, 2, 3, 2]),
    InternalDjinnItemData(12, name_by_item_id[16384132], 16384132, ElementType(3), 814868, [9, 3, 5, 0, 0, 0]),
    InternalDjinnItemData(13, name_by_item_id[16384134], 16384134, ElementType(3), 814880, [11, 0, 0, 0, 3, 2]),
    InternalDjinnItemData(14, name_by_item_id[16384136], 16384136, ElementType(3), 814892, [9, 0, 4, 2, 0, 0]),
    InternalDjinnItemData(15, name_by_item_id[16384138], 16384138, ElementType(3), 814904, [12, 5, 0, 0, 0, 0]),
    InternalDjinnItemData(16, name_by_item_id[16384140], 16384140, ElementType(3), 814916, [11, 6, 0, 0, 0, 0]),
    InternalDjinnItemData(17, name_by_item_id[16384142], 16384142, ElementType(3), 814928, [10, 0, 0, 0, 5, 3]),
    
]

events: List[InternalEventItemData] = [
    InternalEventItemData(5001, 1912, "Mars Lighthouse - Doom Dragon", "Doom Dragon Defeated"),
    InternalEventItemData(5002, 2219, "Alhafra Briggs", "Briggs defeated"),
    InternalEventItemData(5003, 2431, "Alhafra Prison Briggs", "Briggs escaped"),
    InternalEventItemData(5004, 2303, "Gabomba Statue Ritual", "Gabomba Statue Completed"),
    InternalEventItemData(5005, 2542, "Gaia Rock - Serpent", "Serpent defeated"),
    InternalEventItemData(5006, 1637, "Sea of Time - Poseidon", "Poseidon defeated"),
    InternalEventItemData(5007, 2367, "Lemurian Ship - Aqua Hydra", "Aqua Hydra defeated"),
    InternalEventItemData(5008, 2381, "Shaman Village - Moapa", "Moapa defeated"),
    InternalEventItemData(5009, 2593, "Jupiter_Lighthouse Aeri - Agatio and Karst", "Jupiter Beacon Lit"),
    InternalEventItemData(5010, 2635, "Mars Lighthouse - Flame Dragons", "Flame Dragons - defeated"),
    InternalEventItemData(5011, 2270, "Lemurian Ship - Engine Room", "Ship"),
    InternalEventItemData(5012, 2271, "Contigo - Wings of Anemos", "Wings of Anemos"),
    InternalEventItemData(5013, 1610, "Kandorean Temple - Chestbeaters", "Chestbeaters defeated"),
    InternalEventItemData(5014, 1613, "Yampi Desert - King Scorpion", "King Scorpion defeated"),
    InternalEventItemData(5015, 1634, "Champa - Avimander", "Avimander defeated"),
    InternalEventItemData(5016, 1700, "Treasure Isle - Star Magician", "Star Magician defeated"),
    InternalEventItemData(5017, 1757, "Islet Cave - Sentinel", "Sentinel defeated"),
    InternalEventItemData(5018, 1745, "Yampi Desert Cave - Valukar", "Valukar defeated"),
    InternalEventItemData(5019, 1754, "Anemos Inner Sanctum - Dullahan", "Dullahan defeated"),
    InternalEventItemData(5020, 2593, "Contigo - Reunion", "Reunion"),
    InternalEventItemData(5021, 1, "Victory Event", "Victory"),
    InternalEventItemData(5022, 2655, "Loho - Ship Cannon", "Ship Cannon"),
    InternalEventItemData(5023, 2608, "Mars Lighthouse - Heated", "Mars Lighthouse Heated"),
    
]

characters: List[InternalItemData] = [
    InternalItemData(3328, name_by_item_id[3328], ItemClassification.progression, 16384384, ItemType.Character),
    InternalItemData(3329, name_by_item_id[3329], ItemClassification.progression, 16384386, ItemType.Character),
    InternalItemData(3330, name_by_item_id[3330], ItemClassification.progression, 16384388, ItemType.Character),
    InternalItemData(3331, name_by_item_id[3331], ItemClassification.progression, 16384390, ItemType.Character),
    InternalItemData(3333, name_by_item_id[3333], ItemClassification.progression, 16384392, ItemType.Character),
    InternalItemData(3334, name_by_item_id[3334], ItemClassification.progression, 16384394, ItemType.Character),
    InternalItemData(3335, name_by_item_id[3335], ItemClassification.progression, 16384396, ItemType.Character),
    
]

mimics: List[InternalItemData] = [
InternalItemData(2561, name_by_item_id[2561], ItemClassification.trap, 991872, ItemType.Mimic, True),
InternalItemData(2562, name_by_item_id[2562], ItemClassification.trap, 992520, ItemType.Mimic, True),
InternalItemData(2563, name_by_item_id[2563], ItemClassification.trap, 992852, ItemType.Mimic, True),
InternalItemData(2564, name_by_item_id[2564], ItemClassification.trap, 993268, ItemType.Mimic, True),
InternalItemData(2565, name_by_item_id[2565], ItemClassification.trap, 993476, ItemType.Mimic, True),
InternalItemData(2566, name_by_item_id[2566], ItemClassification.trap, 994268, ItemType.Mimic, True),
InternalItemData(2567, name_by_item_id[2567], ItemClassification.trap, 994388, ItemType.Mimic, True),
InternalItemData(2568, name_by_item_id[2568], ItemClassification.trap, 994536, ItemType.Mimic, True),
InternalItemData(2569, name_by_item_id[2569], ItemClassification.trap, 994644, ItemType.Mimic, True),

]

other_progression: List[InternalItemData] = [
InternalItemData(65, name_by_item_id[65], ItemClassification.progression, 732816, ItemType.Weapon, False),
InternalItemData(222, name_by_item_id[222], ItemClassification.progression, 739724, ItemType.KeyItem, False),
InternalItemData(242, name_by_item_id[242], ItemClassification.progression, 740604, ItemType.Consumable, False),
InternalItemData(243, name_by_item_id[243], ItemClassification.progression, 740648, ItemType.Consumable, False),
InternalItemData(244, name_by_item_id[244], ItemClassification.progression, 740692, ItemType.Consumable, False),
InternalItemData(326, name_by_item_id[326], ItemClassification.progression, 744300, ItemType.Trident, False),
InternalItemData(439, name_by_item_id[439], ItemClassification.progression, 749272, ItemType.Consumable, False),
InternalItemData(440, name_by_item_id[440], ItemClassification.progression, 749316, ItemType.Consumable, False),
InternalItemData(441, name_by_item_id[441], ItemClassification.progression, 749360, ItemType.Consumable, False),
InternalItemData(448, name_by_item_id[448], ItemClassification.progression, 749668, ItemType.Consumable, False),
InternalItemData(451, name_by_item_id[451], ItemClassification.progression, 749800, ItemType.Consumable, False),
InternalItemData(452, name_by_item_id[452], ItemClassification.progression, 749844, ItemType.Consumable, False),
InternalItemData(453, name_by_item_id[453], ItemClassification.progression, 749888, ItemType.Consumable, False),
InternalItemData(454, name_by_item_id[454], ItemClassification.progression, 749932, ItemType.Consumable, False),
InternalItemData(455, name_by_item_id[455], ItemClassification.progression, 749976, ItemType.Consumable, False),
InternalItemData(456, name_by_item_id[456], ItemClassification.progression, 750020, ItemType.Consumable, False),
InternalItemData(458, name_by_item_id[458], ItemClassification.progression, 750108, ItemType.Consumable, False),
InternalItemData(459, name_by_item_id[459], ItemClassification.progression, 750152, ItemType.Consumable, False),
InternalItemData(460, name_by_item_id[460], ItemClassification.progression, 750196, ItemType.Consumable, False),

]

useful_consumables = [
    
        InternalItemData(186, name_by_item_id[186], ItemClassification.useful, 738140, ItemType.Consumable, False, True),
        InternalItemData(189, name_by_item_id[189], ItemClassification.useful, 738272, ItemType.Consumable, False, True),
        InternalItemData(190, name_by_item_id[190], ItemClassification.useful, 738316, ItemType.Consumable, False, True),
        InternalItemData(183, name_by_item_id[183], ItemClassification.useful, 738008, ItemType.Consumable, False, True),
]

forge_materials = [
    
        InternalItemData(429, name_by_item_id[429], ItemClassification.useful, 748832, ItemType.Consumable, False, True),
        InternalItemData(430, name_by_item_id[430], ItemClassification.useful, 748876, ItemType.Consumable, False, True),
        InternalItemData(431, name_by_item_id[431], ItemClassification.useful, 748920, ItemType.Consumable, False, True),
        InternalItemData(432, name_by_item_id[432], ItemClassification.useful, 748964, ItemType.Consumable, False, True),
        InternalItemData(433, name_by_item_id[433], ItemClassification.useful, 749008, ItemType.Consumable, False, True),
        InternalItemData(434, name_by_item_id[434], ItemClassification.useful, 749052, ItemType.Consumable, False, True),
        InternalItemData(435, name_by_item_id[435], ItemClassification.useful, 749096, ItemType.Consumable, False, True),
        InternalItemData(436, name_by_item_id[436], ItemClassification.useful, 749140, ItemType.Consumable, False, True),
        InternalItemData(437, name_by_item_id[437], ItemClassification.useful, 749184, ItemType.Consumable, False, True),
]

class_change_items = [
    
        InternalItemData(443, name_by_item_id[443], ItemClassification.useful, 749448, ItemType.Class, False, True),
        InternalItemData(444, name_by_item_id[444], ItemClassification.useful, 749492, ItemType.Class, False, True),
        InternalItemData(445, name_by_item_id[445], ItemClassification.useful, 749536, ItemType.Class, False, True),
]



rusty_items = [
    
        InternalItemData(417, name_by_item_id[417], ItemClassification.useful, 748304, ItemType.Weapon, False, True),
        InternalItemData(418, name_by_item_id[418], ItemClassification.useful, 748348, ItemType.Weapon, False, True),
        InternalItemData(419, name_by_item_id[419], ItemClassification.useful, 748392, ItemType.Weapon, False, True),
        InternalItemData(420, name_by_item_id[420], ItemClassification.useful, 748436, ItemType.Weapon, False, True),
        InternalItemData(421, name_by_item_id[421], ItemClassification.useful, 748480, ItemType.Weapon, False, True),
        InternalItemData(422, name_by_item_id[422], ItemClassification.useful, 748524, ItemType.Weapon, False, True),
        InternalItemData(423, name_by_item_id[423], ItemClassification.useful, 748568, ItemType.Weapon, False, True),
        InternalItemData(424, name_by_item_id[424], ItemClassification.useful, 748612, ItemType.Weapon, False, True),
        InternalItemData(425, name_by_item_id[425], ItemClassification.useful, 748656, ItemType.Weapon, False, True),
        InternalItemData(426, name_by_item_id[426], ItemClassification.useful, 748700, ItemType.Weapon, False, True),
        InternalItemData(427, name_by_item_id[427], ItemClassification.useful, 748744, ItemType.Weapon, False, True),
]

stat_boosters = [
    
        InternalItemData(192, name_by_item_id[192], ItemClassification.filler, 738404, ItemType.Consumable, False, True),
        InternalItemData(193, name_by_item_id[193], ItemClassification.filler, 738448, ItemType.Consumable, False, True),
        InternalItemData(194, name_by_item_id[194], ItemClassification.filler, 738492, ItemType.Consumable, False, True),
        InternalItemData(195, name_by_item_id[195], ItemClassification.filler, 738536, ItemType.Consumable, False, True),
        InternalItemData(196, name_by_item_id[196], ItemClassification.filler, 738580, ItemType.Consumable, False, True),
        InternalItemData(191, name_by_item_id[191], ItemClassification.filler, 738360, ItemType.Consumable, False, True),
]



useful_remainder = [
    
        InternalItemData(384, name_by_item_id[384], ItemClassification.useful, 746852, ItemType.Helm, False, True),
        InternalItemData(259, name_by_item_id[259], ItemClassification.useful, 741352, ItemType.Boots, False, True),
        InternalItemData(388, name_by_item_id[388], ItemClassification.useful, 747028, ItemType.Helm, False, True),
        InternalItemData(7, name_by_item_id[7], ItemClassification.useful, 730264, ItemType.Weapon, False, True),
        InternalItemData(10, name_by_item_id[10], ItemClassification.useful, 730396, ItemType.Weapon, False, True),
        InternalItemData(266, name_by_item_id[266], ItemClassification.useful, 741660, ItemType.Ring, False, True),
        InternalItemData(394, name_by_item_id[394], ItemClassification.useful, 747292, ItemType.Helm, False, True),
        InternalItemData(279, name_by_item_id[279], ItemClassification.useful, 742232, ItemType.Weapon, False, True),
        InternalItemData(281, name_by_item_id[281], ItemClassification.useful, 742320, ItemType.Weapon, False, True),
        InternalItemData(26, name_by_item_id[26], ItemClassification.useful, 731100, ItemType.Weapon, False, True),
        InternalItemData(283, name_by_item_id[283], ItemClassification.useful, 742408, ItemType.Weapon, False, True),
        InternalItemData(414, name_by_item_id[414], ItemClassification.useful, 748172, ItemType.Ring, False, True),
        InternalItemData(287, name_by_item_id[287], ItemClassification.useful, 742584, ItemType.Weapon, False, True),
        InternalItemData(290, name_by_item_id[290], ItemClassification.useful, 742716, ItemType.Weapon, False, True),
        InternalItemData(291, name_by_item_id[291], ItemClassification.useful, 742760, ItemType.Weapon, False, True),
        InternalItemData(292, name_by_item_id[292], ItemClassification.useful, 742804, ItemType.Weapon, False, True),
        InternalItemData(300, name_by_item_id[300], ItemClassification.useful, 743156, ItemType.Weapon, False, True),
        InternalItemData(301, name_by_item_id[301], ItemClassification.useful, 743200, ItemType.Weapon, False, True),
        InternalItemData(309, name_by_item_id[309], ItemClassification.useful, 743552, ItemType.Weapon, False, True),
        InternalItemData(311, name_by_item_id[311], ItemClassification.useful, 743640, ItemType.Weapon, False, True),
        InternalItemData(319, name_by_item_id[319], ItemClassification.useful, 743992, ItemType.Weapon, False, True),
        InternalItemData(333, name_by_item_id[333], ItemClassification.useful, 744608, ItemType.Armor, False, True),
        InternalItemData(334, name_by_item_id[334], ItemClassification.useful, 744652, ItemType.Armor, False, True),
        InternalItemData(336, name_by_item_id[336], ItemClassification.useful, 744740, ItemType.Armor, False, True),
        InternalItemData(340, name_by_item_id[340], ItemClassification.useful, 744916, ItemType.Armor, False, True),
        InternalItemData(343, name_by_item_id[343], ItemClassification.useful, 745048, ItemType.Armor, False, True),
        InternalItemData(344, name_by_item_id[344], ItemClassification.useful, 745092, ItemType.Armor, False, True),
        InternalItemData(349, name_by_item_id[349], ItemClassification.useful, 745312, ItemType.Armor, False, True),
        InternalItemData(351, name_by_item_id[351], ItemClassification.useful, 745400, ItemType.Armor, False, True),
        InternalItemData(358, name_by_item_id[358], ItemClassification.useful, 745708, ItemType.Shield, False, True),
        InternalItemData(366, name_by_item_id[366], ItemClassification.useful, 746060, ItemType.Shield, False, True),
        InternalItemData(370, name_by_item_id[370], ItemClassification.useful, 746236, ItemType.Shield, False, True),
        InternalItemData(371, name_by_item_id[371], ItemClassification.useful, 746280, ItemType.Shield, False, True),
        InternalItemData(378, name_by_item_id[378], ItemClassification.useful, 746588, ItemType.Helm, False, True),
        InternalItemData(383, name_by_item_id[383], ItemClassification.useful, 746808, ItemType.Helm, False, True),
]

other_useful: List[InternalItemData] = useful_remainder  + useful_consumables  + forge_materials  + class_change_items 

shop_only: List[InternalItemData] = [
InternalItemData(1, name_by_item_id[1], ItemClassification.filler, 730000, ItemType.Weapon, False, False),
InternalItemData(2, name_by_item_id[2], ItemClassification.filler, 730044, ItemType.Weapon, False, False),
InternalItemData(3, name_by_item_id[3], ItemClassification.filler, 730088, ItemType.Weapon, False, False),
InternalItemData(4, name_by_item_id[4], ItemClassification.filler, 730132, ItemType.Weapon, False, False),
InternalItemData(5, name_by_item_id[5], ItemClassification.useful, 730176, ItemType.Weapon, False, True),
InternalItemData(6, name_by_item_id[6], ItemClassification.useful, 730220, ItemType.Weapon, False, True),
InternalItemData(16, name_by_item_id[16], ItemClassification.filler, 730660, ItemType.Weapon, False, False),
InternalItemData(17, name_by_item_id[17], ItemClassification.filler, 730704, ItemType.Weapon, False, False),
InternalItemData(18, name_by_item_id[18], ItemClassification.filler, 730748, ItemType.Weapon, False, False),
InternalItemData(19, name_by_item_id[19], ItemClassification.filler, 730792, ItemType.Weapon, False, False),
InternalItemData(20, name_by_item_id[20], ItemClassification.useful, 730836, ItemType.Weapon, False, True),
InternalItemData(21, name_by_item_id[21], ItemClassification.useful, 730880, ItemType.Weapon, False, True),
InternalItemData(31, name_by_item_id[31], ItemClassification.filler, 731320, ItemType.Weapon, False, False),
InternalItemData(32, name_by_item_id[32], ItemClassification.filler, 731364, ItemType.Weapon, False, False),
InternalItemData(33, name_by_item_id[33], ItemClassification.filler, 731408, ItemType.Weapon, False, False),
InternalItemData(34, name_by_item_id[34], ItemClassification.useful, 731452, ItemType.Weapon, False, True),
InternalItemData(43, name_by_item_id[43], ItemClassification.filler, 731848, ItemType.Weapon, False, False),
InternalItemData(44, name_by_item_id[44], ItemClassification.filler, 731892, ItemType.Weapon, False, False),
InternalItemData(45, name_by_item_id[45], ItemClassification.filler, 731936, ItemType.Weapon, False, False),
InternalItemData(46, name_by_item_id[46], ItemClassification.filler, 731980, ItemType.Weapon, False, False),
InternalItemData(47, name_by_item_id[47], ItemClassification.useful, 732024, ItemType.Weapon, False, True),
InternalItemData(55, name_by_item_id[55], ItemClassification.filler, 732376, ItemType.Weapon, False, False),
InternalItemData(56, name_by_item_id[56], ItemClassification.useful, 732420, ItemType.Weapon, False, True),
InternalItemData(57, name_by_item_id[57], ItemClassification.useful, 732464, ItemType.Weapon, False, True),
InternalItemData(58, name_by_item_id[58], ItemClassification.useful, 732508, ItemType.Weapon, False, True),
InternalItemData(59, name_by_item_id[59], ItemClassification.useful, 732552, ItemType.Weapon, False, True),
InternalItemData(60, name_by_item_id[60], ItemClassification.useful, 732596, ItemType.Weapon, False, True),
InternalItemData(61, name_by_item_id[61], ItemClassification.useful, 732640, ItemType.Weapon, False, True),
InternalItemData(62, name_by_item_id[62], ItemClassification.useful, 732684, ItemType.Weapon, False, True),
InternalItemData(63, name_by_item_id[63], ItemClassification.useful, 732728, ItemType.Weapon, False, True),
InternalItemData(75, name_by_item_id[75], ItemClassification.filler, 733256, ItemType.Armor, False, False),
InternalItemData(76, name_by_item_id[76], ItemClassification.filler, 733300, ItemType.Armor, False, False),
InternalItemData(77, name_by_item_id[77], ItemClassification.filler, 733344, ItemType.Armor, False, False),
InternalItemData(78, name_by_item_id[78], ItemClassification.filler, 733388, ItemType.Armor, False, False),
InternalItemData(79, name_by_item_id[79], ItemClassification.filler, 733432, ItemType.Armor, False, False),
InternalItemData(80, name_by_item_id[80], ItemClassification.filler, 733476, ItemType.Armor, False, False),
InternalItemData(89, name_by_item_id[89], ItemClassification.filler, 733872, ItemType.Armor, False, False),
InternalItemData(90, name_by_item_id[90], ItemClassification.filler, 733916, ItemType.Armor, False, False),
InternalItemData(92, name_by_item_id[92], ItemClassification.filler, 734004, ItemType.Armor, False, False),
InternalItemData(94, name_by_item_id[94], ItemClassification.filler, 734092, ItemType.Armor, False, False),
InternalItemData(103, name_by_item_id[103], ItemClassification.filler, 734488, ItemType.Armor, False, False),
InternalItemData(104, name_by_item_id[104], ItemClassification.filler, 734532, ItemType.Armor, False, False),
InternalItemData(105, name_by_item_id[105], ItemClassification.filler, 734576, ItemType.Armor, False, False),
InternalItemData(107, name_by_item_id[107], ItemClassification.filler, 734664, ItemType.Armor, False, False),
InternalItemData(109, name_by_item_id[109], ItemClassification.useful, 734752, ItemType.Armor, False, True),
InternalItemData(110, name_by_item_id[110], ItemClassification.useful, 734796, ItemType.Armor, False, True),
InternalItemData(111, name_by_item_id[111], ItemClassification.useful, 734840, ItemType.Armor, False, True),
InternalItemData(118, name_by_item_id[118], ItemClassification.filler, 735148, ItemType.Shield, False, False),
InternalItemData(119, name_by_item_id[119], ItemClassification.filler, 735192, ItemType.Shield, False, False),
InternalItemData(120, name_by_item_id[120], ItemClassification.filler, 735236, ItemType.Shield, False, False),
InternalItemData(121, name_by_item_id[121], ItemClassification.filler, 735280, ItemType.Shield, False, False),
InternalItemData(122, name_by_item_id[122], ItemClassification.useful, 735324, ItemType.Shield, False, True),
InternalItemData(127, name_by_item_id[127], ItemClassification.filler, 735544, ItemType.Shield, False, False),
InternalItemData(128, name_by_item_id[128], ItemClassification.filler, 735588, ItemType.Shield, False, False),
InternalItemData(129, name_by_item_id[129], ItemClassification.filler, 735632, ItemType.Shield, False, False),
InternalItemData(131, name_by_item_id[131], ItemClassification.useful, 735720, ItemType.Shield, False, True),
InternalItemData(136, name_by_item_id[136], ItemClassification.filler, 735940, ItemType.Shield, False, False),
InternalItemData(137, name_by_item_id[137], ItemClassification.filler, 735984, ItemType.Shield, False, False),
InternalItemData(138, name_by_item_id[138], ItemClassification.filler, 736028, ItemType.Shield, False, False),
InternalItemData(139, name_by_item_id[139], ItemClassification.filler, 736072, ItemType.Shield, False, False),
InternalItemData(140, name_by_item_id[140], ItemClassification.useful, 736116, ItemType.Shield, False, True),
InternalItemData(145, name_by_item_id[145], ItemClassification.filler, 736336, ItemType.Helm, False, False),
InternalItemData(146, name_by_item_id[146], ItemClassification.filler, 736380, ItemType.Helm, False, False),
InternalItemData(147, name_by_item_id[147], ItemClassification.filler, 736424, ItemType.Helm, False, False),
InternalItemData(148, name_by_item_id[148], ItemClassification.filler, 736468, ItemType.Helm, False, False),
InternalItemData(149, name_by_item_id[149], ItemClassification.filler, 736512, ItemType.Helm, False, False),
InternalItemData(150, name_by_item_id[150], ItemClassification.filler, 736556, ItemType.Helm, False, False),
InternalItemData(156, name_by_item_id[156], ItemClassification.filler, 736820, ItemType.Helm, False, False),
InternalItemData(157, name_by_item_id[157], ItemClassification.filler, 736864, ItemType.Helm, False, False),
InternalItemData(158, name_by_item_id[158], ItemClassification.filler, 736908, ItemType.Helm, False, False),
InternalItemData(159, name_by_item_id[159], ItemClassification.useful, 736952, ItemType.Helm, False, True),
InternalItemData(166, name_by_item_id[166], ItemClassification.filler, 737260, ItemType.Helm, False, False),
InternalItemData(167, name_by_item_id[167], ItemClassification.filler, 737304, ItemType.Helm, False, False),
InternalItemData(168, name_by_item_id[168], ItemClassification.filler, 737348, ItemType.Helm, False, False),
InternalItemData(169, name_by_item_id[169], ItemClassification.filler, 737392, ItemType.Helm, False, False),
InternalItemData(402, name_by_item_id[402], ItemClassification.useful, 747644, ItemType.Boots, False, False),
InternalItemData(404, name_by_item_id[404], ItemClassification.useful, 747732, ItemType.Boots, False, True),

]

forge_only: List[InternalItemData] = [
InternalItemData(272, name_by_item_id[272], ItemClassification.useful, 741924, ItemType.Weapon, False, True),
InternalItemData(273, name_by_item_id[273], ItemClassification.useful, 741968, ItemType.Weapon, False, True),
InternalItemData(274, name_by_item_id[274], ItemClassification.useful, 742012, ItemType.Weapon, False, True),
InternalItemData(275, name_by_item_id[275], ItemClassification.useful, 742056, ItemType.Weapon, False, True),
InternalItemData(276, name_by_item_id[276], ItemClassification.useful, 742100, ItemType.Weapon, False, True),
InternalItemData(277, name_by_item_id[277], ItemClassification.useful, 742144, ItemType.Weapon, False, True),
InternalItemData(278, name_by_item_id[278], ItemClassification.useful, 742188, ItemType.Weapon, False, True),
InternalItemData(285, name_by_item_id[285], ItemClassification.useful, 742496, ItemType.Weapon, False, True),
InternalItemData(286, name_by_item_id[286], ItemClassification.useful, 742540, ItemType.Weapon, False, True),
InternalItemData(288, name_by_item_id[288], ItemClassification.useful, 742628, ItemType.Weapon, False, True),
InternalItemData(289, name_by_item_id[289], ItemClassification.useful, 742672, ItemType.Weapon, False, True),
InternalItemData(295, name_by_item_id[295], ItemClassification.useful, 742936, ItemType.Weapon, False, True),
InternalItemData(296, name_by_item_id[296], ItemClassification.useful, 742980, ItemType.Weapon, False, True),
InternalItemData(297, name_by_item_id[297], ItemClassification.useful, 743024, ItemType.Weapon, False, True),
InternalItemData(298, name_by_item_id[298], ItemClassification.useful, 743068, ItemType.Weapon, False, True),
InternalItemData(299, name_by_item_id[299], ItemClassification.useful, 743112, ItemType.Weapon, False, True),
InternalItemData(305, name_by_item_id[305], ItemClassification.useful, 743376, ItemType.Weapon, False, True),
InternalItemData(306, name_by_item_id[306], ItemClassification.useful, 743420, ItemType.Weapon, False, True),
InternalItemData(307, name_by_item_id[307], ItemClassification.useful, 743464, ItemType.Weapon, False, True),
InternalItemData(308, name_by_item_id[308], ItemClassification.useful, 743508, ItemType.Weapon, False, True),
InternalItemData(313, name_by_item_id[313], ItemClassification.useful, 743728, ItemType.Weapon, False, True),
InternalItemData(314, name_by_item_id[314], ItemClassification.useful, 743772, ItemType.Weapon, False, True),
InternalItemData(315, name_by_item_id[315], ItemClassification.useful, 743816, ItemType.Weapon, False, True),
InternalItemData(316, name_by_item_id[316], ItemClassification.useful, 743860, ItemType.Weapon, False, True),
InternalItemData(317, name_by_item_id[317], ItemClassification.useful, 743904, ItemType.Weapon, False, True),
InternalItemData(318, name_by_item_id[318], ItemClassification.useful, 743948, ItemType.Weapon, False, True),
InternalItemData(328, name_by_item_id[328], ItemClassification.useful, 744388, ItemType.Armor, False, True),
InternalItemData(329, name_by_item_id[329], ItemClassification.useful, 744432, ItemType.Armor, False, True),
InternalItemData(330, name_by_item_id[330], ItemClassification.useful, 744476, ItemType.Armor, False, True),
InternalItemData(331, name_by_item_id[331], ItemClassification.useful, 744520, ItemType.Armor, False, True),
InternalItemData(332, name_by_item_id[332], ItemClassification.useful, 744564, ItemType.Armor, False, True),
InternalItemData(338, name_by_item_id[338], ItemClassification.useful, 744828, ItemType.Armor, False, True),
InternalItemData(339, name_by_item_id[339], ItemClassification.useful, 744872, ItemType.Armor, False, True),
InternalItemData(347, name_by_item_id[347], ItemClassification.useful, 745224, ItemType.Armor, False, True),
InternalItemData(348, name_by_item_id[348], ItemClassification.useful, 745268, ItemType.Armor, False, True),
InternalItemData(353, name_by_item_id[353], ItemClassification.useful, 745488, ItemType.Shield, False, True),
InternalItemData(354, name_by_item_id[354], ItemClassification.useful, 745532, ItemType.Shield, False, True),
InternalItemData(355, name_by_item_id[355], ItemClassification.useful, 745576, ItemType.Shield, False, True),
InternalItemData(356, name_by_item_id[356], ItemClassification.useful, 745620, ItemType.Shield, False, True),
InternalItemData(357, name_by_item_id[357], ItemClassification.useful, 745664, ItemType.Shield, False, True),
InternalItemData(361, name_by_item_id[361], ItemClassification.useful, 745840, ItemType.Shield, False, True),
InternalItemData(362, name_by_item_id[362], ItemClassification.useful, 745884, ItemType.Shield, False, True),
InternalItemData(363, name_by_item_id[363], ItemClassification.useful, 745928, ItemType.Shield, False, True),
InternalItemData(368, name_by_item_id[368], ItemClassification.useful, 746148, ItemType.Shield, False, True),
InternalItemData(369, name_by_item_id[369], ItemClassification.useful, 746192, ItemType.Shield, False, True),
InternalItemData(374, name_by_item_id[374], ItemClassification.useful, 746412, ItemType.Helm, False, True),
InternalItemData(375, name_by_item_id[375], ItemClassification.useful, 746456, ItemType.Helm, False, True),
InternalItemData(376, name_by_item_id[376], ItemClassification.useful, 746500, ItemType.Helm, False, True),
InternalItemData(377, name_by_item_id[377], ItemClassification.useful, 746544, ItemType.Helm, False, True),
InternalItemData(382, name_by_item_id[382], ItemClassification.useful, 746764, ItemType.Helm, False, True),
InternalItemData(390, name_by_item_id[390], ItemClassification.useful, 747116, ItemType.Helm, False, True),
InternalItemData(391, name_by_item_id[391], ItemClassification.useful, 747160, ItemType.Helm, False, True),
InternalItemData(392, name_by_item_id[392], ItemClassification.useful, 747204, ItemType.Helm, False, True),
InternalItemData(393, name_by_item_id[393], ItemClassification.useful, 747248, ItemType.Helm, False, True),
InternalItemData(403, name_by_item_id[403], ItemClassification.useful, 747688, ItemType.Boots, False, True),
InternalItemData(409, name_by_item_id[409], ItemClassification.useful, 747952, ItemType.Ring, False, True),
InternalItemData(410, name_by_item_id[410], ItemClassification.useful, 747996, ItemType.Ring, False, True),

]

lucky_only: List[InternalItemData] = [
InternalItemData(250, name_by_item_id[250], ItemClassification.useful, 740956, ItemType.Shirt, False, True),
InternalItemData(251, name_by_item_id[251], ItemClassification.useful, 741000, ItemType.Shirt, False, True),
InternalItemData(252, name_by_item_id[252], ItemClassification.useful, 741044, ItemType.Shirt, False, True),
InternalItemData(256, name_by_item_id[256], ItemClassification.useful, 741220, ItemType.Boots, False, True),
InternalItemData(257, name_by_item_id[257], ItemClassification.useful, 741264, ItemType.Boots, False, True),
InternalItemData(258, name_by_item_id[258], ItemClassification.useful, 741308, ItemType.Boots, False, True),
InternalItemData(262, name_by_item_id[262], ItemClassification.useful, 741484, ItemType.Ring, False, True),
InternalItemData(263, name_by_item_id[263], ItemClassification.useful, 741528, ItemType.Ring, False, True),
InternalItemData(264, name_by_item_id[264], ItemClassification.useful, 741572, ItemType.Ring, False, True),
InternalItemData(280, name_by_item_id[280], ItemClassification.useful, 742276, ItemType.Weapon, False, True),
InternalItemData(302, name_by_item_id[302], ItemClassification.useful, 743244, ItemType.Weapon, False, True),
InternalItemData(320, name_by_item_id[320], ItemClassification.useful, 744036, ItemType.Weapon, False, True),
InternalItemData(335, name_by_item_id[335], ItemClassification.useful, 744696, ItemType.Armor, False, True),
InternalItemData(341, name_by_item_id[341], ItemClassification.useful, 744960, ItemType.Armor, False, True),
InternalItemData(342, name_by_item_id[342], ItemClassification.useful, 745004, ItemType.Armor, False, True),
InternalItemData(359, name_by_item_id[359], ItemClassification.useful, 745752, ItemType.Shield, False, True),
InternalItemData(364, name_by_item_id[364], ItemClassification.useful, 745972, ItemType.Shield, False, True),
InternalItemData(380, name_by_item_id[380], ItemClassification.useful, 746676, ItemType.Helm, False, True),
InternalItemData(387, name_by_item_id[387], ItemClassification.useful, 746984, ItemType.Helm, False, True),
InternalItemData(395, name_by_item_id[395], ItemClassification.useful, 747336, ItemType.Helm, False, True),

]

non_vanilla: List[InternalItemData] = [
InternalItemData(8, name_by_item_id[8], ItemClassification.useful, 730308, ItemType.Weapon, False, True),
InternalItemData(9, name_by_item_id[9], ItemClassification.useful, 730352, ItemType.Weapon, False, True),
InternalItemData(11, name_by_item_id[11], ItemClassification.useful, 730440, ItemType.Weapon, False, True),
InternalItemData(15, name_by_item_id[15], ItemClassification.filler, 730616, ItemType.Weapon, False, False),
InternalItemData(22, name_by_item_id[22], ItemClassification.useful, 730924, ItemType.Weapon, False, True),
InternalItemData(23, name_by_item_id[23], ItemClassification.useful, 730968, ItemType.Weapon, False, True),
InternalItemData(24, name_by_item_id[24], ItemClassification.useful, 731012, ItemType.Weapon, False, True),
InternalItemData(25, name_by_item_id[25], ItemClassification.useful, 731056, ItemType.Weapon, False, True),
InternalItemData(27, name_by_item_id[27], ItemClassification.useful, 731144, ItemType.Weapon, False, True),
InternalItemData(35, name_by_item_id[35], ItemClassification.useful, 731496, ItemType.Weapon, False, True),
InternalItemData(36, name_by_item_id[36], ItemClassification.useful, 731540, ItemType.Weapon, False, True),
InternalItemData(37, name_by_item_id[37], ItemClassification.useful, 731584, ItemType.Weapon, False, True),
InternalItemData(38, name_by_item_id[38], ItemClassification.useful, 731628, ItemType.Weapon, False, True),
InternalItemData(48, name_by_item_id[48], ItemClassification.useful, 732068, ItemType.Weapon, False, True),
InternalItemData(49, name_by_item_id[49], ItemClassification.useful, 732112, ItemType.Weapon, False, True),
InternalItemData(50, name_by_item_id[50], ItemClassification.useful, 732156, ItemType.Weapon, False, True),
InternalItemData(64, name_by_item_id[64], ItemClassification.useful, 732772, ItemType.Weapon, False, True),
InternalItemData(81, name_by_item_id[81], ItemClassification.useful, 733520, ItemType.Armor, False, True),
InternalItemData(82, name_by_item_id[82], ItemClassification.useful, 733564, ItemType.Armor, False, True),
InternalItemData(83, name_by_item_id[83], ItemClassification.useful, 733608, ItemType.Armor, False, True),
InternalItemData(84, name_by_item_id[84], ItemClassification.useful, 733652, ItemType.Armor, False, True),
InternalItemData(85, name_by_item_id[85], ItemClassification.useful, 733696, ItemType.Armor, False, True),
InternalItemData(91, name_by_item_id[91], ItemClassification.filler, 733960, ItemType.Armor, False, False),
InternalItemData(93, name_by_item_id[93], ItemClassification.useful, 734048, ItemType.Armor, False, True),
InternalItemData(95, name_by_item_id[95], ItemClassification.useful, 734136, ItemType.Armor, False, True),
InternalItemData(96, name_by_item_id[96], ItemClassification.useful, 734180, ItemType.Armor, False, True),
InternalItemData(97, name_by_item_id[97], ItemClassification.useful, 734224, ItemType.Armor, False, True),
InternalItemData(98, name_by_item_id[98], ItemClassification.useful, 734268, ItemType.Armor, False, True),
InternalItemData(106, name_by_item_id[106], ItemClassification.useful, 734620, ItemType.Armor, False, True),
InternalItemData(108, name_by_item_id[108], ItemClassification.useful, 734708, ItemType.Armor, False, True),
InternalItemData(112, name_by_item_id[112], ItemClassification.useful, 734884, ItemType.Armor, False, True),
InternalItemData(113, name_by_item_id[113], ItemClassification.useful, 734928, ItemType.Armor, False, True),
InternalItemData(123, name_by_item_id[123], ItemClassification.useful, 735368, ItemType.Shield, False, True),
InternalItemData(124, name_by_item_id[124], ItemClassification.useful, 735412, ItemType.Shield, False, True),
InternalItemData(130, name_by_item_id[130], ItemClassification.useful, 735676, ItemType.Shield, False, True),
InternalItemData(132, name_by_item_id[132], ItemClassification.useful, 735764, ItemType.Shield, False, True),
InternalItemData(133, name_by_item_id[133], ItemClassification.useful, 735808, ItemType.Shield, False, True),
InternalItemData(134, name_by_item_id[134], ItemClassification.useful, 735852, ItemType.Shield, False, True),
InternalItemData(141, name_by_item_id[141], ItemClassification.useful, 736160, ItemType.Shield, False, True),
InternalItemData(142, name_by_item_id[142], ItemClassification.useful, 736204, ItemType.Shield, False, True),
InternalItemData(151, name_by_item_id[151], ItemClassification.useful, 736600, ItemType.Helm, False, True),
InternalItemData(152, name_by_item_id[152], ItemClassification.useful, 736644, ItemType.Helm, False, True),
InternalItemData(160, name_by_item_id[160], ItemClassification.useful, 736996, ItemType.Helm, False, True),
InternalItemData(161, name_by_item_id[161], ItemClassification.useful, 737040, ItemType.Helm, False, True),
InternalItemData(162, name_by_item_id[162], ItemClassification.useful, 737084, ItemType.Helm, False, True),
InternalItemData(163, name_by_item_id[163], ItemClassification.useful, 737128, ItemType.Helm, False, True),
InternalItemData(164, name_by_item_id[164], ItemClassification.useful, 737172, ItemType.Helm, False, True),
InternalItemData(170, name_by_item_id[170], ItemClassification.useful, 737436, ItemType.Helm, False, True),
InternalItemData(171, name_by_item_id[171], ItemClassification.useful, 737480, ItemType.Helm, False, True),
InternalItemData(265, name_by_item_id[265], ItemClassification.useful, 741616, ItemType.Ring, False, True),
InternalItemData(267, name_by_item_id[267], ItemClassification.useful, 741704, ItemType.Ring, False, True),
InternalItemData(268, name_by_item_id[268], ItemClassification.useful, 741748, ItemType.Ring, False, True),
InternalItemData(282, name_by_item_id[282], ItemClassification.useful, 742364, ItemType.Weapon, False, True),
InternalItemData(293, name_by_item_id[293], ItemClassification.useful, 742848, ItemType.Weapon, False, True),
InternalItemData(303, name_by_item_id[303], ItemClassification.useful, 743288, ItemType.Weapon, False, True),
InternalItemData(310, name_by_item_id[310], ItemClassification.useful, 743596, ItemType.Weapon, False, True),
InternalItemData(321, name_by_item_id[321], ItemClassification.useful, 744080, ItemType.Weapon, False, True),
InternalItemData(322, name_by_item_id[322], ItemClassification.useful, 744124, ItemType.Weapon, False, True),
InternalItemData(323, name_by_item_id[323], ItemClassification.useful, 744168, ItemType.Weapon, False, True),
InternalItemData(324, name_by_item_id[324], ItemClassification.useful, 744212, ItemType.Weapon, False, True),
InternalItemData(345, name_by_item_id[345], ItemClassification.useful, 745136, ItemType.Armor, False, True),
InternalItemData(350, name_by_item_id[350], ItemClassification.useful, 745356, ItemType.Armor, False, True),
InternalItemData(365, name_by_item_id[365], ItemClassification.useful, 746016, ItemType.Shield, False, True),
InternalItemData(372, name_by_item_id[372], ItemClassification.useful, 746324, ItemType.Shield, False, True),
InternalItemData(379, name_by_item_id[379], ItemClassification.useful, 746632, ItemType.Helm, False, True),
InternalItemData(385, name_by_item_id[385], ItemClassification.useful, 746896, ItemType.Helm, False, True),
InternalItemData(386, name_by_item_id[386], ItemClassification.useful, 746940, ItemType.Helm, False, True),
InternalItemData(396, name_by_item_id[396], ItemClassification.useful, 747380, ItemType.Helm, False, True),
InternalItemData(398, name_by_item_id[398], ItemClassification.useful, 747468, ItemType.Shirt, False, True),
InternalItemData(399, name_by_item_id[399], ItemClassification.useful, 747512, ItemType.Shirt, False, True),
InternalItemData(400, name_by_item_id[400], ItemClassification.useful, 747556, ItemType.Shirt, False, True),
InternalItemData(401, name_by_item_id[401], ItemClassification.useful, 747600, ItemType.Shirt, False, True),
InternalItemData(405, name_by_item_id[405], ItemClassification.useful, 747776, ItemType.Boots, False, True),
InternalItemData(406, name_by_item_id[406], ItemClassification.useful, 747820, ItemType.Boots, False, True),
InternalItemData(407, name_by_item_id[407], ItemClassification.useful, 747864, ItemType.Boots, False, True),
InternalItemData(408, name_by_item_id[408], ItemClassification.useful, 747908, ItemType.Boots, False, True),
InternalItemData(411, name_by_item_id[411], ItemClassification.useful, 748040, ItemType.Ring, False, True),
InternalItemData(412, name_by_item_id[412], ItemClassification.useful, 748084, ItemType.Ring, False, True),
InternalItemData(413, name_by_item_id[413], ItemClassification.useful, 748128, ItemType.Ring, False, True),
InternalItemData(415, name_by_item_id[415], ItemClassification.useful, 748216, ItemType.Ring, False, True),

]

vanilla_coins: List[InternalItemData] = [
InternalItemData(32771, name_by_item_id[32771], ItemClassification.filler, 991840, ItemType.Consumable, False),
InternalItemData(32780, name_by_item_id[32780], ItemClassification.filler, 993540, ItemType.Consumable, False),
InternalItemData(32783, name_by_item_id[32783], ItemClassification.filler, 991976, ItemType.Consumable, False),
InternalItemData(33083, name_by_item_id[33083], ItemClassification.filler, 992128, ItemType.Consumable, False),
InternalItemData(32800, name_by_item_id[32800], ItemClassification.filler, 993192, ItemType.Consumable, False),
InternalItemData(32891, name_by_item_id[32891], ItemClassification.filler, 992324, ItemType.Consumable, False),
InternalItemData(33545, name_by_item_id[33545], ItemClassification.filler, 992360, ItemType.Consumable, False),
InternalItemData(32850, name_by_item_id[32850], ItemClassification.filler, 992388, ItemType.Consumable, False),
InternalItemData(33434, name_by_item_id[33434], ItemClassification.filler, 992644, ItemType.Consumable, False),
InternalItemData(32786, name_by_item_id[32786], ItemClassification.filler, 992712, ItemType.Consumable, False),
InternalItemData(32784, name_by_item_id[32784], ItemClassification.filler, 993048, ItemType.Consumable, False),
InternalItemData(32950, name_by_item_id[32950], ItemClassification.filler, 993180, ItemType.Consumable, False),
InternalItemData(32978, name_by_item_id[32978], ItemClassification.filler, 993632, ItemType.Consumable, False),
InternalItemData(33133, name_by_item_id[33133], ItemClassification.filler, 993788, ItemType.Consumable, False),
InternalItemData(32934, name_by_item_id[32934], ItemClassification.filler, 993960, ItemType.Consumable, False),
InternalItemData(32929, name_by_item_id[32929], ItemClassification.filler, 994108, ItemType.Consumable, False),
InternalItemData(33679, name_by_item_id[33679], ItemClassification.filler, 994208, ItemType.Consumable, False),
InternalItemData(33074, name_by_item_id[33074], ItemClassification.filler, 994412, ItemType.Consumable, False),
InternalItemData(33151, name_by_item_id[33151], ItemClassification.filler, 994460, ItemType.Consumable, False),

]

misc: List[InternalItemData] = [
    InternalItemData(0, name_by_item_id[0], ItemClassification.filler, 729956, ItemType.Consumable, False),
    InternalItemData(231, name_by_item_id[231], ItemClassification.filler, 740120, ItemType.Consumable, False),
    InternalItemData(449, name_by_item_id[449], ItemClassification.filler, 749712, ItemType.Consumable, False),
    
]

remainder: List[InternalItemData] = [
    InternalItemData(180, name_by_item_id[180], ItemClassification.filler, 737876, ItemType.Consumable, False, False),
    InternalItemData(181, name_by_item_id[181], ItemClassification.filler, 737920, ItemType.Consumable, False, False),
    InternalItemData(182, name_by_item_id[182], ItemClassification.filler, 737964, ItemType.Consumable, False, False),
    InternalItemData(187, name_by_item_id[187], ItemClassification.filler, 738184, ItemType.Consumable, False, False),
    InternalItemData(188, name_by_item_id[188], ItemClassification.filler, 738228, ItemType.Consumable, False, False),
    InternalItemData(226, name_by_item_id[226], ItemClassification.filler, 739900, ItemType.Consumable, False, False),
    InternalItemData(227, name_by_item_id[227], ItemClassification.filler, 739944, ItemType.Consumable, False, False),
    InternalItemData(228, name_by_item_id[228], ItemClassification.filler, 739988, ItemType.Consumable, False, True),
    InternalItemData(229, name_by_item_id[229], ItemClassification.filler, 740032, ItemType.Consumable, False, True),
    InternalItemData(233, name_by_item_id[233], ItemClassification.filler, 740208, ItemType.Consumable, False, False),
    InternalItemData(236, name_by_item_id[236], ItemClassification.filler, 740340, ItemType.Consumable, False, False),
    InternalItemData(238, name_by_item_id[238], ItemClassification.filler, 740428, ItemType.Consumable, False, False),
    InternalItemData(239, name_by_item_id[239], ItemClassification.filler, 740472, ItemType.Consumable, False, False),
    InternalItemData(240, name_by_item_id[240], ItemClassification.filler, 740516, ItemType.Consumable, False, False),
    InternalItemData(241, name_by_item_id[241], ItemClassification.filler, 740560, ItemType.Consumable, False, False),
    
]

all_items: List[InternalItemData] = djinn_items + psyenergy_as_item_list + psyenergy_list + summon_list + events + characters + \
    mimics + other_progression + other_useful + shop_only + forge_only + lucky_only + non_vanilla + vanilla_coins + \
    misc  + rusty_items  + stat_boosters  + remainder 
assert len(all_items) == len({x.id for x in all_items})
item_table: Dict[str, InternalItemData] = {item.name: item for item in all_items}
items_by_id: Dict[int, InternalItemData] = {item.id: item for item in all_items}