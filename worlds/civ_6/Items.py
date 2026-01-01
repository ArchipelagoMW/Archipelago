from enum import Enum
from typing import Dict, Optional, TYPE_CHECKING, List
from BaseClasses import Item, ItemClassification
from .Data import (
    GoodyHutRewardData,
    get_era_required_items_data,
    get_existing_civics_data,
    get_existing_techs_data,
    get_goody_hut_rewards_data,
    get_progressive_districts_data,
)
from .Enum import CivVICheckType, EraType
from .ProgressiveDistricts import get_flat_progressive_districts

if TYPE_CHECKING:
    from . import CivVIWorld


CIV_VI_AP_ITEM_ID_BASE = 5041000

NON_PROGRESSION_DISTRICTS = ["PROGRESSIVE_PRESERVE", "PROGRESSIVE_NEIGHBORHOOD"]


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
    "PROGRESSIVE_PRESERVE",
]


class FillerItemRarity(Enum):
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"


FILLER_DISTRIBUTION: Dict[FillerItemRarity, float] = {
    FillerItemRarity.RARE: 0.025,
    FillerItemRarity.UNCOMMON: 0.2,
    FillerItemRarity.COMMON: 0.775,
}


class FillerItemData:
    name: str
    type: str
    rarity: FillerItemRarity
    civ_name: str

    def __init__(self, data: GoodyHutRewardData):
        self.name = data["Name"]
        self.rarity = FillerItemRarity(data["Rarity"])
        self.civ_name = data["Type"]


filler_data: Dict[str, FillerItemData] = {
    item["Name"]: FillerItemData(item) for item in get_goody_hut_rewards_data()
}


class CivVIItemData:
    civ_vi_id: int
    classification: ItemClassification
    name: str
    code: int
    cost: int
    item_type: CivVICheckType
    progressive_name: Optional[str]
    civ_name: Optional[str]
    era: Optional[EraType]

    def __init__(
        self,
        name: str,
        civ_vi_id: int,
        cost: int,
        item_type: CivVICheckType,
        id_offset: int,
        classification: ItemClassification,
        progressive_name: Optional[str],
        civ_name: Optional[str] = None,
        era: Optional[EraType] = None,
    ):
        self.classification = classification
        self.civ_vi_id = civ_vi_id
        self.name = name
        self.code = civ_vi_id + CIV_VI_AP_ITEM_ID_BASE + id_offset
        self.cost = cost
        self.item_type = item_type
        self.progressive_name = progressive_name
        self.civ_name = civ_name
        self.era = era


class CivVIEvent(Item):
    game: str = "Civilization VI"


class CivVIItem(Item):
    game: str = "Civilization VI"
    civ_vi_id: int
    item_type: CivVICheckType

    def __init__(
        self,
        item: CivVIItemData,
        player: int,
        classification: Optional[ItemClassification] = None,
    ):
        super().__init__(
            item.name, classification or item.classification, item.code, player
        )
        self.civ_vi_id = item.civ_vi_id
        self.item_type = item.item_type


def format_item_name(name: str) -> str:
    name_parts = name.split("_")
    return " ".join([part.capitalize() for part in name_parts])


_items_by_civ_name: Dict[str, CivVIItemData] = {}


def get_item_by_civ_name(
    item_name: str, item_table: Dict[str, "CivVIItemData"]
) -> "CivVIItemData":
    """Gets the names of the items in the item_table"""
    if not _items_by_civ_name:
        for item in item_table.values():
            if item.civ_name:
                _items_by_civ_name[item.civ_name] = item

    try:
        return _items_by_civ_name[item_name]
    except KeyError as e:
        raise KeyError(f"Item {item_name} not found in item_table") from e


def _generate_tech_items(
    id_base: int, required_items: List[str], progressive_items: Dict[str, str]
) -> Dict[str, CivVIItemData]:
    # Generate Techs
    existing_techs = get_existing_techs_data()
    tech_table: Dict[str, CivVIItemData] = {}

    tech_id = 0
    for tech in existing_techs:
        classification = ItemClassification.useful
        name = tech["Name"]
        civ_name = tech["Type"]
        if civ_name in required_items:
            classification = ItemClassification.progression
        progressive_name = None
        check_type = CivVICheckType.TECH
        if civ_name in progressive_items.keys():
            progressive_name = format_item_name(progressive_items[civ_name])

        tech_table[name] = CivVIItemData(
            name=name,
            civ_vi_id=tech_id,
            cost=tech["Cost"],
            item_type=check_type,
            id_offset=id_base,
            classification=classification,
            progressive_name=progressive_name,
            civ_name=civ_name,
            era=EraType(tech["EraType"]),
        )

        tech_id += 1

    return tech_table


def _generate_civics_items(
    id_base: int, required_items: List[str], progressive_items: Dict[str, str]
) -> Dict[str, CivVIItemData]:
    civic_id = 0
    civic_table: Dict[str, CivVIItemData] = {}
    existing_civics = get_existing_civics_data()

    for civic in existing_civics:
        name = civic["Name"]
        civ_name = civic["Type"]
        progressive_name = None
        check_type = CivVICheckType.CIVIC

        if civ_name in progressive_items.keys():
            progressive_name = format_item_name(progressive_items[civ_name])

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
            progressive_name=progressive_name,
            civ_name=civ_name,
            era=EraType(civic["EraType"]),
        )

        civic_id += 1

    return civic_table


def _generate_progressive_district_items(id_base: int) -> Dict[str, CivVIItemData]:
    progressive_table: Dict[str, CivVIItemData] = {}
    progressive_id_base = 0
    progressive_items = get_progressive_districts_data()
    for item_name in progressive_items.keys():
        classification = (
            ItemClassification.useful
            if item_name in NON_PROGRESSION_DISTRICTS
            else ItemClassification.progression
        )
        name = format_item_name(item_name)
        progressive_table[name] = CivVIItemData(
            name=name,
            civ_vi_id=progressive_id_base,
            cost=0,
            item_type=CivVICheckType.PROGRESSIVE_DISTRICT,
            id_offset=id_base,
            classification=classification,
            progressive_name=None,
            civ_name=item_name,
        )
        progressive_id_base += 1
    return progressive_table


def _generate_progressive_era_items(id_base: int) -> Dict[str, CivVIItemData]:
    """Generates the single progressive district item"""
    era_table: Dict[str, CivVIItemData] = {}
    # Generate progressive eras
    progressive_era_name = format_item_name("PROGRESSIVE_ERA")
    era_table[progressive_era_name] = CivVIItemData(
        name=progressive_era_name,
        civ_vi_id=0,
        cost=0,
        item_type=CivVICheckType.ERA,
        id_offset=id_base,
        classification=ItemClassification.progression,
        progressive_name=None,
        civ_name="PROGRESSIVE_ERA",
    )
    return era_table


def _generate_goody_hut_items(id_base: int) -> Dict[str, CivVIItemData]:
    # Generate goody hut items
    goody_huts = {
        item["Name"]: FillerItemData(item) for item in get_goody_hut_rewards_data()
    }
    goody_table: Dict[str, CivVIItemData] = {}
    goody_base = 0
    for value in goody_huts.values():
        goody_table[value.name] = CivVIItemData(
            name=value.name,
            civ_vi_id=goody_base,
            cost=0,
            item_type=CivVICheckType.GOODY,
            id_offset=id_base,
            classification=ItemClassification.filler,
            progressive_name=None,
            civ_name=value.civ_name,
        )
        goody_base += 1
    return goody_table


def generate_item_table() -> Dict[str, CivVIItemData]:
    era_required_items = get_era_required_items_data()
    required_items: List[str] = []
    for value in era_required_items.values():
        required_items += value

    progressive_items = get_flat_progressive_districts()

    item_table: Dict[str, CivVIItemData] = {}

    def get_id_base():
        return len(item_table.keys())

    item_table.update(
        **_generate_tech_items(get_id_base(), required_items, progressive_items)
    )
    item_table.update(
        **_generate_civics_items(get_id_base(), required_items, progressive_items)
    )
    item_table.update(**_generate_progressive_district_items(get_id_base()))
    item_table.update(**_generate_progressive_era_items(get_id_base()))
    item_table.update(**_generate_goody_hut_items(get_id_base()))

    return item_table


def get_items_by_type(
    item_type: CivVICheckType, item_table: Dict[str, CivVIItemData]
) -> List[CivVIItemData]:
    """
    Returns a list of items that match the given item type
    """
    return [item for item in item_table.values() if item.item_type == item_type]


fillers_by_rarity: Dict[FillerItemRarity, List[FillerItemData]] = {
    rarity: [item for item in filler_data.values() if item.rarity == rarity]
    for rarity in FillerItemRarity
}


def get_random_filler_by_rarity(
    world: "CivVIWorld", rarity: FillerItemRarity
) -> FillerItemData:
    """
    Returns a random filler item by rarity
    """
    return world.random.choice(fillers_by_rarity[rarity])
