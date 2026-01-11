from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import DigimonWorldItem

class DigimonWorldLocationCategory(IntEnum):
    RECRUIT = 0
    MISC = 1
    EVENT = 2
    SKIP = 3,
    PROSPERITY = 4,
    CARD = 5,


class DigimonWorldLocationData(NamedTuple):
    id: int
    name: str
    default_item: str
    category: DigimonWorldLocationCategory


class DigimonWorldLocation(Location):
    game: str = "Digimon World"
    category: DigimonWorldLocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: DigimonWorldLocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category
        self.id = id

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 69000000
        table_offset = 1000

        table_order = [
            "Consumable", "Misc", "Cards", "Start Game", "Prosperity",
            "Digimon"
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))
            output.update({location_data.name: location_data.id for location_data in location_tables[region_name]})
        return output

    def place_locked_item(self, item: DigimonWorldItem):
        self.item = item
        self.locked = True
        item.location = self

location_tables = {
    "Start Game": [
        DigimonWorldLocationData(69003000, "Start Game", "Agumon Soul", DigimonWorldLocationCategory.RECRUIT),
    ],
    "Digimon": [
        DigimonWorldLocationData(69005000, "Agumon", "1000 Bits", DigimonWorldLocationCategory.RECRUIT),    
        DigimonWorldLocationData(69006000, "Betamon", "Betamon Soul", DigimonWorldLocationCategory.RECRUIT),   
        DigimonWorldLocationData(69007000, "Greymon", "Greymon Soul", DigimonWorldLocationCategory.RECRUIT),   
        DigimonWorldLocationData(69008000, "Devimon", "Devimon Soul", DigimonWorldLocationCategory.RECRUIT),   
        DigimonWorldLocationData(69009000, "Airdramon", "Airdramon Soul", DigimonWorldLocationCategory.RECRUIT),   
        DigimonWorldLocationData(69010000, "Tyrannomon", "Tyrannomon Soul", DigimonWorldLocationCategory.RECRUIT),    
        DigimonWorldLocationData(69011000, "Meramon", "Meramon Soul", DigimonWorldLocationCategory.RECRUIT),   
        DigimonWorldLocationData(69012000, "Seadramon", "Seadramon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69013000, "Numemon", "Numemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69014000, "MetalGreymon", "MetalGreymon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69015000, "Mamemon", "Mamemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69016000, "Monzaemon", "Monzaemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69017000, "Gabumon", "Gabumon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69018000, "Elecmon", "Elecmon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69019000, "Kabuterimon", "Kabuterimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69020000, "Angemon", "Angemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69021000, "Birdramon", "Birdramon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69022000, "Garurumon", "Garurumon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69023000, "Frigimon", "Frigimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69024000, "Whamon", "Whamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69025000, "Vegiemon", "Vegiemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69026000, "SkullGreymon", "SkullGreymon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69027000, "MetalMamemon", "MetalMamemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69028000, "Vademon", "Vademon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69029000, "Patamon", "Patamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69030000, "Kunemon", "Kunemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69031000, "Unimon", "Unimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69032000, "Ogremon", "Ogremon Soul", DigimonWorldLocationCategory.RECRUIT),  
        DigimonWorldLocationData(69033000, "Shellmon", "Shellmon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69034000, "Centarumon", "Centarumon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69035000, "Bakemon", "Bakemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69036000, "Drimogemon", "Drimogemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69037000, "Sukamon", "Sukamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69038000, "Andromon", "Andromon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69039000, "Giromon", "Giromon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69040000, "Etemon", "Etemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69041000, "Biyomon", "Biyomon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69042000, "Palmon", "Palmon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69043000, "Monochromon", "Monochromon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69044000, "Leomon", "Leomon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69045000, "Coelamon", "Coelamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69046000, "Kokatorimon", "Kokatorimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69047000, "Kuwagamon", "Kuwagamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69048000, "Mojyamon", "Mojyamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69049000, "Nanimon", "Nanimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69050000, "Megadramon", "Megadramon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69051000, "Piximon", "Piximon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69052000, "Digitamamon", "Digitamamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69053000, "Penguinmon", "Penguinmon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69054000, "Ninjamon", "Ninjamon Soul", DigimonWorldLocationCategory.RECRUIT),
    ],
    "Item Boxes":[

    ],
    "Cards":[
        DigimonWorldLocationData(69002000, "Player Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002001, "Phoenixmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002002, "H-Kabuterimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002003, "MegaSeadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002004, "ShogunGekomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002005, "Myotismon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002006, "MetalGreymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002007, "Mamemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002008, "Monzaemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002009, "SkullGreymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002010, "MetalMamemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002011, "Vademon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002012, "Andromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002013, "Giromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002014, "Etemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002015, "Megadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002016, "Piximon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002017, "Digitamamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002018, "Gekomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002019, "WaruMonzaemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002020, "Jijimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002021, "King of Sukamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002022, "Cherrymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002023, "Guardromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002024, "Hagurumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002025, "Brachiomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002026, "Greymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002027, "Devimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002028, "Airdramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002029, "Tyrannomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002030, "Meramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002031, "Seadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002032, "Kabuterimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002033, "Angemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002034, "Birdramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002035, "Garurumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002036, "Frigimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002037, "Whamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002038, "Unimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002039, "Ogremon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002040, "Shellmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002041, "Centarumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002042, "Bakemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002043, "Drimogemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002044, "Monochromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002045, "Leomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002046, "Coelamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002047, "Kokatorimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002048, "Kuwagamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002049, "Mojyamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002050, "Ninjamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002051, "Penguinmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002052, "Otamamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002053, "Tentomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002054, "Yanmamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002055, "Gotsumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002056, "Darkrizamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002057, "ToyAgumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002058, "DemiMeramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002059, "Tankmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002060, "Goburimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002061, "Numemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002062, "Vegiemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002063, "Sukamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002064, "Nanimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002065, "Machinedramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD), 
    ],
    "Prosperity":
    [
        DigimonWorldLocationData(69004000, "1 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004001, "2 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004002, "3 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004003, "4 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004004, "5 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004005, "6 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004006, "7 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004007, "8 Prosperity", "Various", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004008, "9 Prosperity", "Various", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004009, "10 Prosperity", "Bandage", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004010, "11 Prosperity", "Bandage", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004011, "12 Prosperity", "Medicine", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004012, "13 Prosperity", "Medicine", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004013, "14 Prosperity", "Medicine", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004014, "15 Prosperity", "Torn tatter", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004015, "16 Prosperity", "Koga laws", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004016, "17 Prosperity", "Grey Claws", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004017, "18 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004018, "19 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004019, "20 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004020, "21 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004021, "22 Prosperity", "SM Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004022, "23 Prosperity", "Med Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004023, "24 Prosperity", "Med Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004024, "25 Prosperity", "Med Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004025, "26 Prosperity", "Med Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004026, "27 Prosperity", "Med Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004027, "28 Prosperity", "Med Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004028, "29 Prosperity", "Med Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004029, "30 Prosperity", "Med Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004030, "31 Prosperity", "Lrg Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004031, "32 Prosperity", "Lrg Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004032, "33 Prosperity", "Lrg Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004033, "34 Prosperity", "Lrg Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004034, "35 Prosperity", "Sup Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004035, "36 Prosperity", "Sup Recovery", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004036, "37 Prosperity", "Double flop", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004037, "38 Prosperity", "Double flop", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004038, "39 Prosperity", "Double flop", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004039, "40 Prosperity", "Large MP", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004040, "41 Prosperity", "Large MP", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004041, "42 Prosperity", "Medium MP", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004042, "43 Prosperity", "Medium MP", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004043, "44 Prosperity", "Medium MP", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004044, "45 Prosperity", "Sup.restore", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004045, "46 Prosperity", "Sup.restore", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004046, "47 Prosperity", "Restore", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004047, "48 Prosperity", "Restore", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004048, "49 Prosperity", "Health shoe", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004049, "50 Prosperity", "Port. potty", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004050, "51 Prosperity", "Port. potty", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004051, "52 Prosperity", "Port. potty", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004052, "53 Prosperity", "Port. potty", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004053, "54 Prosperity", "Auto Pilot", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004054, "55 Prosperity", "Auto Pilot", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004055, "56 Prosperity", "Auto Pilot", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004056, "57 Prosperity", "Auto Pilot", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004057, "58 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004058, "59 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004059, "60 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004060, "61 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004061, "62 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004062, "63 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004063, "64 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004064, "65 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004065, "66 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004066, "67 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004067, "68 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004068, "69 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004069, "70 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004070, "71 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004071, "72 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004072, "73 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004073, "74 Prosperity", "5000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004074, "75 Prosperity", "5000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004075, "76 Prosperity", "5000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004076, "77 Prosperity", "5000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004077, "78 Prosperity", "5000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004078, "79 Prosperity", "5000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004079, "80 Prosperity", "5000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004080, "81 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004081, "82 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004082, "83 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004083, "84 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004084, "85 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004085, "86 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004086, "87 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004087, "88 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004088, "89 Prosperity", "1000 Bits", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004089, "90 Prosperity", "Black trout", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004090, "91 Prosperity", "Black trout", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004091, "92 Prosperity", "Chain melon", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004092, "93 Prosperity", "Digiseabass", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004093, "94 Prosperity", "Digiseabass", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004094, "95 Prosperity", "Digiseabass", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004095, "96 Prosperity", "Digiseabass", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004096, "97 Prosperity", "Rain Plant", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004097, "98 Prosperity", "Rain Plant", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004098, "99 Prosperity", "Rain Plant", DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData(69004099, "100 Prosperity", "Rain Plant", DigimonWorldLocationCategory.EVENT),
    ],
    "Consumable": [],
    "Misc": [        
    ],
}
location_dictionary: Dict[str, DigimonWorldLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
