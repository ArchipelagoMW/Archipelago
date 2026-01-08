from dataclasses import dataclass
from enum import Enum
from typing import Dict, NamedTuple, List, cast, Optional
from BaseClasses import Location, LocationProgressType

PLAY_TABLE_START_ID = 300
LEVEL_START_ID = 200
CARD_OPEN_START_ID = 1000
CARD_SELL_START_ID = 500
SELL_CHECK_START_ID=3000


class TCGSimulatorLocation(Location):
    game: str = "TCG Card Shop Simulator"


class LocData(NamedTuple):
    code: Optional[int]
    region: Optional[str]


@dataclass
class ShopLocation:
    code: int

@dataclass
class NamedItem:
    name: str
    id: int
    locData: LocData


pg1_locations: dict[str,ShopLocation] = {
    "Basic Card Pack": ShopLocation(190),#game id 0
    "Basic Card Box": ShopLocation(1),
    "Rare Card Pack": ShopLocation(2),
    "Rare Card Box": ShopLocation(3),
    "Epic Card Pack": ShopLocation(4),
    "Epic Card Box": ShopLocation(5),
    "Legendary Card Pack": ShopLocation(6),
    "Legendary Card Box": ShopLocation(7),
    "Basic Destiny Pack": ShopLocation(8),
    "Basic Destiny Box": ShopLocation(9),
    "Rare Destiny Pack": ShopLocation(10),
    "Rare Destiny Box": ShopLocation(11),
    "Epic Destiny Pack": ShopLocation(12),
    "Epic Destiny Box": ShopLocation(13),
    "Legendary Destiny Pack": ShopLocation(14),
    "Legendary Destiny Box": ShopLocation(15),
    "Fire Battle Deck": ShopLocation(55),
    "Earth Battle Deck": ShopLocation(56),
    "Water Battle Deck": ShopLocation(57),
    "Wind Battle Deck": ShopLocation(58),
    "Fire Destiny Deck": ShopLocation(59),
    "Earth Destiny Deck": ShopLocation(60),
    "Water Destiny Deck": ShopLocation(61),
    "Wind Destiny Deck": ShopLocation(62),
}
pg2_locations: dict[str,ShopLocation] = {
    "Cleanser": ShopLocation(23),
    "Card Sleeves (Clear)": ShopLocation(63),
    "Card Sleeves (Tetramon)": ShopLocation(64),
    "D20 Dice Red": ShopLocation(29),
    "D20 Dice Blue": ShopLocation(30),
    "D20 Dice Black": ShopLocation(31),
    "D20 Dice White": ShopLocation(32),
    "Card Sleeves (Fire)": ShopLocation(65),
    "Card Sleeves (Earth)": ShopLocation(66),
    "Card Sleeves (Water)": ShopLocation(67),
    "Card Sleeves (Wind)": ShopLocation(68),
    "Deck Box Red": ShopLocation(24),
    "Deck Box Green": ShopLocation(25),
    "Deck Box Blue": ShopLocation(26),
    "Deck Box Yellow": ShopLocation(27),
    "Collection Book": ShopLocation(28),
    "Premium Collection Book": ShopLocation(54),
    "Playmat (Drilceros)": ShopLocation(71),
    "Playmat (Clamigo)": ShopLocation(69),
    "Playmat (Wispo)": ShopLocation(75),
    "Playmat (Lunight)": ShopLocation(83),
    "Playmat (Kyrone)": ShopLocation(78),
    "Playmat (Duel)": ShopLocation(70),
    "Playmat (Dracunix1)": ShopLocation(74),
    "Playmat (The Four Dragons)": ShopLocation(73),
    "Playmat (Drakon)": ShopLocation(72),
    "Playmat (GigatronX Evo)": ShopLocation(76),
    "Playmat (Fire)": ShopLocation(79),
    "Playmat (Earth)": ShopLocation(80),
    "Playmat (Water)": ShopLocation(82),
    "Playmat (Wind)": ShopLocation(81),
    "Playmat (Tetramon)": ShopLocation(77),
    "Playmat (Dracunix2)": ShopLocation(109),
    "Playmat (GigatronX)": ShopLocation(110),
    "Playmat (Katengu Black)": ShopLocation(111),
    "Playmat (Katengu White)": ShopLocation(112),
    "Manga 1": ShopLocation(95),
    "Manga 2": ShopLocation(96),
    "Manga 3": ShopLocation(97),
    "Manga 4": ShopLocation(98),
    "Manga 5": ShopLocation(99),
    "Manga 6": ShopLocation(100),
    "Manga 7": ShopLocation(101),
    "Manga 8": ShopLocation(102),
    "Manga 9": ShopLocation(103),
    "Manga 10": ShopLocation(104),
    "Manga 11": ShopLocation(105),
    "Manga 12": ShopLocation(106),
}
pg3_locations: dict[str,ShopLocation] = {
    "Pigni Plushie": ShopLocation(33),
    "Nanomite Plushie": ShopLocation(34),
    "Minstar Plushie": ShopLocation(35),
    "Nocti Plushie": ShopLocation(36),
    "Burpig Figurine": ShopLocation(39),
    "Decimite Figurine": ShopLocation(42),
    "Trickstar Figurine": ShopLocation(45),
    "Lunight Figurine": ShopLocation(48),
    "Inferhog Figurine": ShopLocation(40),
    "Meganite Figurine": ShopLocation(43),
    "Princestar Figurine": ShopLocation(46),
    "Vampicant Figurine": ShopLocation(49),
    "Blazoar Plushie": ShopLocation(41),
    "Giganite Statue": ShopLocation(44),
    "Kingstar Plushie": ShopLocation(47),
    "Dracunix Figurine": ShopLocation(50),
    "Bonfiox Plushie": ShopLocation(52),
    "Drilceros Action Figure": ShopLocation(51),
    "ToonZ Plushie": ShopLocation(53),
}
tt_locations: dict[str,ShopLocation] = {
    "Penny Sleeves": ShopLocation(118),
    "Tower Deckbox": ShopLocation(124),
    "Magnetic Holder": ShopLocation(113),
    "Toploader": ShopLocation(117),
    "Card Preserver": ShopLocation(114),
    "Playmat Gray": ShopLocation(119),
    "Playmat Green": ShopLocation(120),
    "Playmat Purple": ShopLocation(121),
    "Playmat Yellow": ShopLocation(122),
    "Pocket Pages": ShopLocation(115),
    "Card Holder": ShopLocation(116),
    "Collectors Album": ShopLocation(123),
    "System Gate #1": ShopLocation(87),
    "System Gate #2": ShopLocation(88),
    "Mafia Works": ShopLocation(86),
    "Necromonsters": ShopLocation(84),
    "Claim!": ShopLocation(85),
}

def get_sell_loc(key):
    for d in (tt_locations, pg1_locations, pg2_locations, pg3_locations):
        if key in d:
            return d[key]
    return None

def get_shop_locations(world):
    return [pg1_locations.copy(), pg2_locations.copy(), pg3_locations.copy(), tt_locations.copy()]

def get_license_checks(world,item_key:str ,loc: ShopLocation, is_starting_item:bool = False):
    if item_key is None or loc is None:
        return {}
    return get_license_checks_internal(world.options.sell_check_amount.value,world.options.extra_starting_item_checks.value,
                                item_key, loc, is_starting_item)

def get_license_checks_internal(check_amount, starting_num, item_key:str ,loc: ShopLocation, is_starting_item:bool = False):
    sell_item_locs = {}
    for n in range(1, check_amount + (starting_num if is_starting_item else 0) + 1):
        sell_item_locs[f"Sell {n} {"Boxes" if n>1 else "Box"} of {item_key}"] = SELL_CHECK_START_ID + (loc.code * 16) + (n-1)
    return sell_item_locs

def is_sell_excluded(name,loc_id):
    if not loc_id:
        return False
    if loc_id < SELL_CHECK_START_ID:
        return False
    if name.startswith("Sell ") and " Boxes" in name:
        try:
            # Remove "Sell " prefix and " Boxes" suffix, then convert to int
            n_str = name[len("Sell "):name.index(" Boxes")]
            n = int(n_str)
            if n > 8:
                return True
        except ValueError:
            # If conversion fails, skip
            pass
    return False


def get_play_table_checks(world):
    return get_play_table_checks_internal(world.options.play_table_checks.value)

def get_play_table_checks_internal(game_check_count: int):
    play_table_locs = {}
    if game_check_count > 0:
        for i in range(game_check_count):
            name = f"Customer Play Games #{i + 1}"
            hex_id = PLAY_TABLE_START_ID + i
            play_table_locs[name] = hex_id

    return play_table_locs

def get_level_checks(world, region_level, final_region: bool = False):
    return get_level_checks_internal(world.options.all_level_checks.value, region_level, final_region, world.options.goal.value)

def get_level_checks_internal(all_level_checks, region_level, final_region: bool = False, goal = 3):
    level_locs = {}
    if final_region:
        if goal == 0:
            level_locs[f"Level {region_level}"] = None
        else:
            level_locs[f"Level {region_level}"] = LEVEL_START_ID+region_level-1
        return level_locs

    end_level = region_level + 1

    if all_level_checks:
        end_level = region_level+5
        if region_level == 1:
            end_level = 5

    if region_level == 100:
        end_level = 101
    for l in range(region_level, end_level):
        if l == 1:
            continue
        level_locs[f"Level {l}"] = LEVEL_START_ID+l-1
    return level_locs

class Rarity(Enum):
    Common = 1
    Rare = 2
    Epic = 3
    Legendary = 4


class MonsterData(NamedTuple):
    name: str
    rarity: Rarity


class Expansion(Enum):
    Tetramon = 0
    Destiny = 1


class Border(Enum):
    Base = 0
    FirstEdition = 1
    Silver = 2
    Gold = 3
    EX = 4
    FullArt = 5


class Foil(Enum):
    NonFoil = 0
    Foil = 1


card_rarity: List[MonsterData] = [
    MonsterData("Pigni", Rarity.Common),
    MonsterData("Burpig", Rarity.Rare),
    MonsterData("Inferhog", Rarity.Epic),
    MonsterData("Blazoar", Rarity.Legendary),
    MonsterData("Kidsune", Rarity.Common),
    MonsterData("Bonfiox", Rarity.Rare),
    MonsterData("Honobi", Rarity.Epic),
    MonsterData("Kyuenbi", Rarity.Legendary),
    MonsterData("Nanomite", Rarity.Common),
    MonsterData("Decimite", Rarity.Rare),
    MonsterData("Meganite", Rarity.Epic),
    MonsterData("Giganite", Rarity.Legendary),
    MonsterData("Sapoling", Rarity.Common),
    MonsterData("Forush", Rarity.Rare),
    MonsterData("Timbro", Rarity.Epic),
    MonsterData("Mammotree", Rarity.Legendary),
    MonsterData("Minstar", Rarity.Common),
    MonsterData("Trickstar", Rarity.Rare),
    MonsterData("Princestar", Rarity.Epic),
    MonsterData("Kingstar", Rarity.Legendary),
    MonsterData("Shellow", Rarity.Common),
    MonsterData("Clamigo", Rarity.Rare),
    MonsterData("Aquariff", Rarity.Epic),
    MonsterData("Fistronk", Rarity.Legendary),
    MonsterData("Wurmgle", Rarity.Common),
    MonsterData("Pupazz", Rarity.Rare),
    MonsterData("Mothini", Rarity.Epic),
    MonsterData("Royalama", Rarity.Legendary),
    MonsterData("Nocti", Rarity.Common),
    MonsterData("Lunight", Rarity.Rare),
    MonsterData("Vampicant", Rarity.Epic),
    MonsterData("Dracunix", Rarity.Legendary),
    MonsterData("Minotos", Rarity.Rare),
    MonsterData("Drilceros", Rarity.Epic),
    MonsterData("Grizzaw", Rarity.Epic),
    MonsterData("Jelicleen", Rarity.Rare),
    MonsterData("Wispo", Rarity.Rare),
    MonsterData("Mummog", Rarity.Rare),
    MonsterData("Helio", Rarity.Common),
    MonsterData("Pixy", Rarity.Rare),
    MonsterData("Flory", Rarity.Epic),
    MonsterData("Magnoria", Rarity.Legendary),
    MonsterData("Werboo", Rarity.Common),
    MonsterData("Flami", Rarity.Common),
    MonsterData("Angez", Rarity.Rare),
    MonsterData("Moskit", Rarity.Epic),
    MonsterData("Kyrone", Rarity.Common),
    MonsterData("Twofrost", Rarity.Rare),
    MonsterData("Threeze", Rarity.Epic),
    MonsterData("Hydroid", Rarity.Legendary),
    MonsterData("Drakon", Rarity.Legendary),
    MonsterData("Bogon", Rarity.Legendary),
    MonsterData("Hydron", Rarity.Legendary),
    MonsterData("Raizon", Rarity.Legendary),
    MonsterData("Tortugor", Rarity.Epic),
    MonsterData("Lupup", Rarity.Common),
    MonsterData("Luphire", Rarity.Rare),
    MonsterData("Lucinder", Rarity.Epic),
    MonsterData("Lucadence", Rarity.Legendary),
    MonsterData("Gupi", Rarity.Common),
    MonsterData("Sharfin", Rarity.Rare),
    MonsterData("Gilgabass", Rarity.Epic),
    MonsterData("Jigajawr", Rarity.Legendary),
    MonsterData("Batrang", Rarity.Common),
    MonsterData("Dusko", Rarity.Rare),
    MonsterData("Wolgin", Rarity.Epic),
    MonsterData("Jacktern", Rarity.Legendary),
    MonsterData("Tetron", Rarity.Common),
    MonsterData("Raxx", Rarity.Rare),
    MonsterData("Gannon", Rarity.Epic),
    MonsterData("GigatronX", Rarity.Legendary),
    MonsterData("Clawop", Rarity.Common),
    MonsterData("Clawdos", Rarity.Rare),
    MonsterData("Clawaken", Rarity.Epic),
    MonsterData("Clawcifear", Rarity.Legendary),
    MonsterData("Sunflork", Rarity.Common),
    MonsterData("Scarlios", Rarity.Rare),
    MonsterData("Scarkgorus", Rarity.Epic),
    MonsterData("Crobib", Rarity.Common),
    MonsterData("Crosilisk", Rarity.Rare),
    MonsterData("Crorathian", Rarity.Epic),
    MonsterData("Nimblis", Rarity.Common),
    MonsterData("Nimboculo", Rarity.Rare),
    MonsterData("Nimbustrike", Rarity.Epic),
    MonsterData("Esmeri", Rarity.Common),
    MonsterData("Esmerock", Rarity.Rare),
    MonsterData("Esmerdios", Rarity.Epic),
    MonsterData("Litspire", Rarity.Epic),
    MonsterData("Voltrex", Rarity.Legendary),
    MonsterData("Crablox", Rarity.Rare),
    MonsterData("Clawvenger", Rarity.Epic),
    MonsterData("Flambrolly", Rarity.Legendary),
    MonsterData("Lumie", Rarity.Rare),
    MonsterData("Seedant", Rarity.Common),
    MonsterData("Budwing", Rarity.Rare),
    MonsterData("Buzzeed", Rarity.Epic),
    MonsterData("Beakai", Rarity.Rare), #should be common, bad game
    MonsterData("Talontsu", Rarity.Epic), #should be rare bad game
    MonsterData("Talonika", Rarity.Epic),
    MonsterData("Talonryu", Rarity.Legendary),
    MonsterData("Kataryu", Rarity.Epic),
    MonsterData("Katengu", Rarity.Legendary),
    MonsterData("Mufflin", Rarity.Common),
    MonsterData("Muffleur", Rarity.Rare),
    MonsterData("Mufflimax", Rarity.Epic),
    MonsterData("Anguifish", Rarity.Common),
    MonsterData("Amneshark", Rarity.Rare),
    MonsterData("Amnesilla", Rarity.Epic),
    MonsterData("Frizard", Rarity.Rare),
    MonsterData("Gekoflare", Rarity.Epic),
    MonsterData("Terradrakon", Rarity.Legendary),
    MonsterData("Flamchik", Rarity.Common),
    MonsterData("Pyropeck", Rarity.Rare),
    MonsterData("Poseia", Rarity.Common),
    MonsterData("Posteed", Rarity.Rare),
    MonsterData("Poseigon", Rarity.Epic),
    MonsterData("Poseidrake", Rarity.Legendary),
    MonsterData("Sludglop", Rarity.Common),
    MonsterData("Sludgetox", Rarity.Rare),
    MonsterData("Toxigoop", Rarity.Epic),
    MonsterData("Toximuck", Rarity.Legendary),
]
int_to_card_region = {
    0:"Basic Card Pack",
    1:"Rare Card Pack",
    2:"Epic Card Pack",
    3:"Legendary Card Pack",
    4:"Destiny Basic Card Pack",
    5:"Destiny Rare Card Pack",
    6:"Destiny Epic Card Pack",
    7:"Destiny Legendary Card Pack"
}
def decode_card(num):
    if not num:
        return None
    if (num & 0x10000) == 0:
        return None

    # Extract values
    expansion = (num >> 12) & 0xF
    border = (num >> 8) & 0xF
    foil = (num >> 7) & 0x1
    index = (num & 0x7F) - 1

    return expansion, border, foil, index

def check_card_exclude(world, num):
    decoded = decode_card(num)
    if decoded:
        exp, bord, foil, idx = decoded
        if bord >= Border.Silver.value:
            return True
        if foil:
            return True
        if world.random.random() > 0.5:
            return True
    return False

def generate_card(name, index, border, foil, expansion, rarity):
    return f"{name} {border.name} {'Foil' if foil else 'NonFoil'} {expansion.name}", 0x10000 | (expansion.value << 12) | (border.value << 8) | (foil << 7) | (index + 1)

def get_card_checks(world, card_region: int):
    return get_card_checks_internal(world.options.card_sanity.value, world.options.border_sanity.value, world.options.foil_sanity.value,
                                    world.options.checks_per_pack.value, card_region, True, world)

def get_card_checks_internal(card_sanity, border_sanity, foil_sanity, checks_per_pack, card_region: int, create_hints:bool = False, world = None):
    card_locs = {}
    expansion = Expansion(1 if card_region >= 4 else 0)
    rarity = Rarity((card_region % 4) + 1)

    if card_sanity > 0:
        if card_sanity > card_region:
            for index, data in enumerate(card_rarity):
                data = cast(MonsterData, data)
                if data.rarity != rarity:
                    continue
                for border in Border:
                    if border_sanity < border.value:
                        continue

                    name, code = generate_card(data.name, index, border, 0, expansion, rarity)
                    card_locs[name] = code
                    if create_hints and world:
                        world.hints[code] = f"Card is in {expansion.name} {rarity.name} Packs"
                    if foil_sanity:
                        name, code = generate_card(data.name, index, border, 1, expansion, rarity)
                        card_locs[name] = code
                        if create_hints and world:
                            world.hints[code] = f"Card is in {expansion.name} {rarity.name} Packs"
    else:
        for i in range(checks_per_pack):
            name = f"Open {expansion.name} {rarity.name} cards {i+1}"

            card_locs[name] = CARD_OPEN_START_ID + i + (((rarity.value - 1) + (expansion.value * 4))*30)

    return card_locs

def get_sell_card_checks(world, is_destiny: bool):
    return get_sell_card_checks_internal(world.options.sell_card_check_count.value,is_destiny)

def get_sell_card_checks_internal(sell_card_check_count, is_destiny):
    sell_card_locs = {}
    expansion = Expansion.Destiny if is_destiny else Expansion.Tetramon
    if sell_card_check_count > 0:
        for i in range(sell_card_check_count):
            name = f"Sell {expansion.name} cards #{i + 1}"
            sell_card_locs[name] = CARD_SELL_START_ID + i + expansion.value * 50
    return sell_card_locs


def get_all_locations():
    all_locations = {}

    for card_region_id in range(8):
        all_locations.update(get_card_checks_internal(8, 5, True, 0, card_region_id))
        all_locations.update(get_card_checks_internal(0, 0, False, 30, card_region_id))

    for l in range(0, 105, 5):
        if l == 0:
            all_locations.update(get_level_checks_internal(True, 1))
            continue
        all_locations.update(get_level_checks_internal(True, l))

    all_locations.update(get_play_table_checks_internal(50))
    all_locations.update(get_sell_card_checks_internal(50, False))
    all_locations.update(get_sell_card_checks_internal(50, True))

    for item_key, item_data in pg1_locations.items():
        license_checks = get_license_checks_internal(16, 2, item_key, item_data)
        all_locations.update(license_checks)

    for item_key, item_data in pg2_locations.items():
        license_checks = get_license_checks_internal(16, 2, item_key, item_data)
        all_locations.update(license_checks)

    for item_key, item_data in pg3_locations.items():
        license_checks = get_license_checks_internal(16, 2, item_key, item_data)
        all_locations.update(license_checks)

    for item_key, item_data in tt_locations.items():
        license_checks = get_license_checks_internal(16, 2, item_key, item_data)
        all_locations.update(license_checks)

    return all_locations