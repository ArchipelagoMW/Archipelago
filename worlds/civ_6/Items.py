from enum import Enum
import json
import os
import pkgutil
import random
from typing import Dict, List, Optional
import typing
from BaseClasses import Item, ItemClassification
from .Data import get_era_required_items_data, get_existing_civics_data, get_existing_techs_data, get_goody_hut_rewards_data, get_progressive_districts_data
from .Enum import CivVICheckType, EraType
from .ProgressiveDistricts import get_flat_progressive_districts
CIV_VI_AP_ITEM_ID_BASE = 5041000

NON_PROGRESSION_DISTRICTS = [
    "PROGRESSIVE_PRESERVE",
    "PROGRESSIVE_NEIGHBORHOOD"
]


# Items required as progression for boostsanity mode
BOOSTSANITY_PROGRESSION_ITEMS = [
    "TECH_THE_WHEEL",
    "TECH_MASONRY",
    "TECH_ARCHERY",
    "TECH_ENGINEERING",
    "TECH_CONSTRUCTION",
    "TECH_GUNPOWDER",
    "TECH_MACHINERY",
    "TECH_SIEGE_TACTICS",
    "TECH_STIRRUPS",
    "TECH_ASTRONOMY",
    "TECH_BALLISTICS",
    "TECH_STEAM_POWER",
    "TECH_SANITATION",
    "TECH_COMPUTERS",
    "TECH_COMBUSTION",
    "TECH_TELECOMMUNICATIONS",
    "TECH_ROBOTICS",
    "CIVIC_FEUDALISM",
    "CIVIC_GUILDS",
    "CIVIC_THE_ENLIGHTENMENT",
    "CIVIC_MERCANTILISM",
    "CIVIC_CONSERVATION",
    "CIVIC_CIVIL_SERVICE",
    "CIVIC_GLOBALIZATION",
    "CIVIC_COLD_WAR",
    "CIVIC_URBANIZATION",
    "CIVIC_NATIONALISM",
    "CIVIC_MOBILIZATION",
    "PROGRESSIVE_NEIGHBORHOOD",
    "PROGRESSIVE_PRESERVE"
]


class FillerItemRarity(Enum):
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"


FILLER_DISTRIBUTION: Dict[FillerItemRarity, float] = {
    FillerItemRarity.RARE: 0.025,
    FillerItemRarity.UNCOMMON: .2,
    FillerItemRarity.COMMON: 0.775,
}


class FillerItemData:
    name: str
    type: str
    rarity: FillerItemRarity
    civ_name: str

    def __init__(self, data: Dict[str, str]):
        self.name = data["Name"]
        self.rarity = FillerItemRarity(data["Rarity"])
        self.civ_name = data["Type"]


def get_filler_item_data() -> Dict[str, FillerItemData]:
    """
    Returns a dictionary of filler items with their data
    """
    goody_huts: List[Dict[str, str]] = get_goody_hut_rewards_data()
    # Create a FillerItemData object for each item
    cached_filler_items = {item["Name"]: FillerItemData(item) for item in goody_huts}

    return cached_filler_items


class CivVIItemData:
    civ_vi_id: int
    classification: ItemClassification
    name: str
    code: int
    cost: int
    item_type: CivVICheckType
    progression_name: Optional[str]
    civ_name: Optional[str]

    def __init__(self, name, civ_vi_id: int, cost: int,  item_type: CivVICheckType, id_offset: int, classification: ItemClassification, progression_name: Optional[str], civ_name: Optional[str] = None):
        self.classification = classification
        self.civ_vi_id = civ_vi_id
        self.name = name
        self.code = civ_vi_id + CIV_VI_AP_ITEM_ID_BASE + id_offset
        self.cost = cost
        self.item_type = item_type
        self.progression_name = progression_name
        self.civ_name = civ_name


class CivVIItem(Item):
    game: str = "Civilization VI"
    civ_vi_id: int
    item_type: CivVICheckType

    def __init__(self, item: CivVIItemData, player: int, classification: ItemClassification = None):
        super().__init__(item.name, classification or item.classification, item.code, player)
        self.civ_vi_id = item.civ_vi_id
        self.item_type = item.item_type


def format_item_name(name: str) -> str:
    name_parts = name.split("_")
    return " ".join([part.capitalize() for part in name_parts])


def get_item_by_civ_name(item_name: typing.List[str], item_table: typing.Dict[str, 'CivVIItemData']) -> 'CivVIItemData':
    """Gets the names of the items in the item_table"""
    for item in item_table.values():
        if item_name == item.civ_name:
            return item

    raise Exception(f"Item {item_name} not found in item_table")


def _generate_tech_items(id_base: int, required_items: List[str], progressive_items: Dict[str, str]) -> List[CivVIItemData]:
    # Generate Techs
    existing_techs = get_existing_techs_data()
    tech_table = {}

    tech_id = 0
    for tech in existing_techs:
        classification = ItemClassification.useful
        name = tech["Name"]
        civ_name = tech["Type"]
        if civ_name in required_items:
            classification = ItemClassification.progression
        progression_name = None
        check_type = CivVICheckType.TECH
        if civ_name in progressive_items.keys():
            progression_name = format_item_name(progressive_items[civ_name])

        tech_table[name] = CivVIItemData(
            name=name,
            civ_vi_id=tech_id,
            cost=tech["Cost"],
            item_type=check_type,
            id_offset=id_base,
            classification=classification,
            progression_name=progression_name,
            civ_name=civ_name
        )

        tech_id += 1

    return tech_table


def _generate_civics_items(id_base: int, required_items: List[str], progressive_items: Dict[str, str]) -> List[CivVIItemData]:
    civic_id = 0
    civic_table = {}
    existing_civics = get_existing_civics_data()

    for civic in existing_civics:
        name = civic["Name"]
        civ_name = civic["Type"]
        progression_name = None
        check_type = CivVICheckType.CIVIC

        if civ_name in progressive_items.keys():
            progression_name = format_item_name(progressive_items[civ_name])

        classification = ItemClassification.useful
        if civ_name in required_items:
            classification = ItemClassification.progression

        civic_table[name] = CivVIItemData(
            name=name,
            civ_vi_id=civic_id,
            cost=civic["Cost"],
            item_type=check_type,
            id_offset=id_base,
            classification=classification,
            progression_name=progression_name,
            civ_name=civ_name
        )

        civic_id += 1

    return civic_table


def _generate_progressive_district_items(id_base: int) -> List[CivVIItemData]:
    progressive_table = {}
    progressive_id_base = 0
    progressive_items = get_progressive_districts_data()
    for item_name in progressive_items.keys():
        progression = ItemClassification.progression
        if item_name in NON_PROGRESSION_DISTRICTS:
            progression = ItemClassification.useful
        name = format_item_name(item_name)
        progressive_table[name] = CivVIItemData(
            name=name,
            civ_vi_id=progressive_id_base,
            cost=0,
            item_type=CivVICheckType.PROGRESSIVE_DISTRICT,
            id_offset=id_base,
            classification=progression,
            progression_name=None,
            civ_name=item_name
        )
        progressive_id_base += 1
    return progressive_table


def _generate_progressive_era_items(id_base: int) -> List[CivVIItemData]:
    """Generates the single progressive district item"""
    era_table = {}
    # Generate progressive eras
    progressive_era_name = format_item_name("PROGRESSIVE_ERA")
    era_table[progressive_era_name] = CivVIItemData(
        name=progressive_era_name,
        civ_vi_id=0,
        cost=0,
        item_type=CivVICheckType.ERA,
        id_offset=id_base,
        classification=ItemClassification.progression,
        progression_name=None,
        civ_name="PROGRESSIVE_ERA"
    )
    return era_table


def _generate_goody_hut_items(id_base: int) -> List[CivVIItemData]:
    # Generate goody hut items
    goody_huts = get_filler_item_data()
    goody_table = {}
    goody_base = 0
    for value in goody_huts.values():
        goody_table[value.name] = CivVIItemData(
            name=value.name,
            civ_vi_id=goody_base,
            cost=0,
            item_type=CivVICheckType.GOODY,
            id_offset=id_base,
            classification=ItemClassification.filler,
            progression_name=None,
            civ_name=value.civ_name
        )
        goody_base += 1
    return goody_table


def generate_item_table() -> Dict[str, CivVIItemData]:
    era_required_items = get_era_required_items_data()
    required_items: List[str] = []
    for key, value in era_required_items.items():
        required_items += value

    progressive_items = get_flat_progressive_districts()

    item_table = {}

    def get_id_base():
        return len(item_table.keys())

    item_table = {**item_table, **_generate_tech_items(get_id_base(), required_items, progressive_items)}
    item_table = {**item_table, **_generate_civics_items(get_id_base(), required_items, progressive_items)}
    item_table = {**item_table, **_generate_progressive_district_items(get_id_base())}
    item_table = {**item_table, **_generate_progressive_era_items(get_id_base())}
    item_table = {**item_table, **_generate_goody_hut_items(get_id_base())}

    return item_table


def get_items_by_type(item_type: CivVICheckType, item_table: Dict[str, CivVIItemData]) -> List[CivVIItemData]:
    """
    Returns a list of items that match the given item type
    """
    return [item for item in item_table.values() if item.item_type == item_type]


def get_random_filler_by_rarity(rarity: FillerItemRarity, item_table: Dict[str, CivVIItemData]) -> CivVIItemData:
    """
    Returns a random filler item by rarity
    """
    items = [item for item in get_filler_item_data().values() if item.rarity == rarity]
    return items[random.randint(0, len(items) - 1)]
