from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Dict, Set, List
from enum import IntEnum


class ItemType(IntEnum):
    technology = 1
    resource = 2
    group = 3


class ItemData(NamedTuple):
    classification: IC
    count: int
    name: str
    tech_type: str
    type: ItemType = ItemType.technology


def make_resource_bundle_data(display_name: str, internal_name: str = "") -> ItemData:
    if not internal_name:
        internal_name = display_name
    return ItemData(IC.filler, 0, display_name, internal_name, ItemType.resource)


item_table: Dict[int, ItemData] = {
    35000: ItemData(IC.useful, 1, "Compass", "Compass"),
    35001: ItemData(IC.progression, 1, "Lightweight High Capacity Tank", "PlasteelTank"),
    35002: ItemData(IC.progression, 1, "Vehicle Upgrade Console", "BaseUpgradeConsole"),
    35003: ItemData(IC.progression, 1, "Ultra Glide Fins", "UltraGlideFins"),
    35004: ItemData(IC.useful, 1, "Cyclops Sonar Upgrade", "CyclopsSonarModule"),
    35005: ItemData(IC.useful, 1, "Reinforced Dive Suit", "ReinforcedDiveSuit"),
    35006: ItemData(IC.useful, 1, "Cyclops Thermal Reactor Module", "CyclopsThermalReactorModule"),
    35007: ItemData(IC.filler, 1, "Water Filtration Suit", "WaterFiltrationSuit"),
    35008: ItemData(IC.progression, 1, "Alien Containment", "BaseWaterPark"),
    35009: ItemData(IC.useful, 1, "Creature Decoy", "CyclopsDecoy"),
    35010: ItemData(IC.useful, 1, "Cyclops Fire Suppression System", "CyclopsFireSuppressionModule"),
    35011: ItemData(IC.useful, 1, "Swim Charge Fins", "SwimChargeFins"),
    35012: ItemData(IC.useful, 1, "Repulsion Cannon", "RepulsionCannon"),
    35013: ItemData(IC.useful, 1, "Cyclops Decoy Tube Upgrade", "CyclopsDecoyModule"),
    35014: ItemData(IC.progression, 1, "Cyclops Shield Generator", "CyclopsShieldModule"),
    35015: ItemData(IC.progression, 1, "Cyclops Depth Module MK1", "CyclopsHullModule1"),
    35016: ItemData(IC.useful, 1, "Cyclops Docking Bay Repair Module", "CyclopsSeamothRepairModule"),
    35017: ItemData(IC.useful, 2, "Battery Charger fragment", "BatteryChargerFragment"),
    35018: ItemData(IC.filler, 2, "Beacon Fragment", "BeaconFragment"),
    35019: ItemData(IC.useful, 2, "Bioreactor Fragment", "BaseBioReactorFragment"),
    35020: ItemData(IC.progression, 4, "Cyclops Bridge Fragment", "CyclopsBridgeFragment"),
    35021: ItemData(IC.progression, 4, "Cyclops Engine Fragment", "CyclopsEngineFragment"),
    35022: ItemData(IC.progression, 4, "Cyclops Hull Fragment", "CyclopsHullFragment"),
    35023: ItemData(IC.filler, 2, "Grav Trap Fragment", "GravSphereFragment"),
    35024: ItemData(IC.progression, 3, "Laser Cutter Fragment", "LaserCutterFragment"),
    35025: ItemData(IC.filler, 2, "Light Stick Fragment", "TechlightFragment"),
    35026: ItemData(IC.progression, 5, "Mobile Vehicle Bay Fragment", "ConstructorFragment"),
    35027: ItemData(IC.progression, 3, "Modification Station Fragment", "WorkbenchFragment"),
    35028: ItemData(IC.progression, 2, "Moonpool Fragment", "MoonpoolFragment"),
    35029: ItemData(IC.useful, 3, "Nuclear Reactor Fragment", "BaseNuclearReactorFragment"),
    35030: ItemData(IC.useful, 2, "Power Cell Charger Fragment", "PowerCellChargerFragment"),
    35031: ItemData(IC.filler, 1, "Power Transmitter Fragment", "PowerTransmitterFragment"),
    35032: ItemData(IC.progression, 6, "Prawn Suit Fragment", "ExosuitFragment"),
    35033: ItemData(IC.useful, 2, "Prawn Suit Drill Arm Fragment", "ExosuitDrillArmFragment"),
    35034: ItemData(IC.useful, 2, "Prawn Suit Grappling Arm Fragment", "ExosuitGrapplingArmFragment"),
    35035: ItemData(IC.useful, 2, "Prawn Suit Propulsion Cannon Fragment", "ExosuitPropulsionArmFragment"),
    35036: ItemData(IC.useful, 2, "Prawn Suit Torpedo Arm Fragment", "ExosuitTorpedoArmFragment"),
    35037: ItemData(IC.useful, 3, "Scanner Room Fragment", "BaseMapRoomFragment"),
    35038: ItemData(IC.progression, 5, "Seamoth Fragment", "SeamothFragment"),
    35039: ItemData(IC.progression, 2, "Stasis Rifle Fragment", "StasisRifleFragment"),
    35040: ItemData(IC.useful, 2, "Thermal Plant Fragment", "ThermalPlantFragment"),
    35041: ItemData(IC.progression, 4, "Seaglide Fragment", "SeaglideFragment"),
    35042: ItemData(IC.progression, 1, "Radiation Suit", "RadiationSuit"),
    35043: ItemData(IC.progression, 2, "Propulsion Cannon Fragment", "PropulsionCannonFragment"),
    35044: ItemData(IC.progression_skip_balancing, 1, "Neptune Launch Platform", "RocketBase"),
    35045: ItemData(IC.progression, 1, "Ion Power Cell", "PrecursorIonPowerCell"),
    35046: ItemData(IC.filler, 2, "Exterior Growbed", "FarmingTray"),
    35047: ItemData(IC.filler, 1, "Picture Frame", "PictureFrameFragment"),
    35048: ItemData(IC.filler, 1, "Bench", "Bench"),
    35049: ItemData(IC.filler, 1, "Basic Plant Pot", "PlanterPotFragment"),
    35050: ItemData(IC.filler, 1, "Interior Growbed", "PlanterBoxFragment"),
    35051: ItemData(IC.filler, 1, "Plant Shelf", "PlanterShelfFragment"),
    35052: ItemData(IC.filler, 1, "Observatory", "BaseObservatory"),
    35053: ItemData(IC.progression, 1, "Multipurpose Room", "BaseRoom"),
    35054: ItemData(IC.useful, 1, "Bulkhead", "BaseBulkhead"),
    35055: ItemData(IC.filler, 1, "Spotlight", "Spotlight"),
    35056: ItemData(IC.filler, 1, "Desk", "StarshipDesk"),
    35057: ItemData(IC.filler, 1, "Swivel Chair", "StarshipChair"),
    35058: ItemData(IC.filler, 1, "Office Chair", "StarshipChair2"),
    35059: ItemData(IC.filler, 1, "Command Chair", "StarshipChair3"),
    35060: ItemData(IC.filler, 1, "Counter", "LabCounter"),
    35061: ItemData(IC.filler, 1, "Single Bed", "NarrowBed"),
    35062: ItemData(IC.filler, 1, "Basic Double Bed", "Bed1"),
    35063: ItemData(IC.filler, 1, "Quilted Double Bed", "Bed2"),
    35064: ItemData(IC.filler, 1, "Coffee Vending Machine", "CoffeeVendingMachine"),
    35065: ItemData(IC.filler, 1, "Trash Can", "Trashcans"),
    35066: ItemData(IC.filler, 1, "Floodlight", "Techlight"),
    35067: ItemData(IC.filler, 1, "Bar Table", "BarTable"),
    35068: ItemData(IC.filler, 1, "Vending Machine", "VendingMachine"),
    35069: ItemData(IC.filler, 1, "Single Wall Shelf", "SingleWallShelf"),
    35070: ItemData(IC.filler, 1, "Wall Shelves", "WallShelves"),
    35071: ItemData(IC.filler, 1, "Round Plant Pot", "PlanterPot2"),
    35072: ItemData(IC.filler, 1, "Chic Plant Pot", "PlanterPot3"),
    35073: ItemData(IC.filler, 1, "Nuclear Waste Disposal", "LabTrashcan"),
    35074: ItemData(IC.filler, 1, "Wall Planter", "BasePlanter"),
    35075: ItemData(IC.progression, 1, "Ion Battery", "PrecursorIonBattery"),
    35076: ItemData(IC.progression_skip_balancing, 1, "Neptune Gantry", "RocketBaseLadder"),
    35077: ItemData(IC.progression_skip_balancing, 1, "Neptune Boosters", "RocketStage1"),
    35078: ItemData(IC.progression_skip_balancing, 1, "Neptune Fuel Reserve", "RocketStage2"),
    35079: ItemData(IC.progression_skip_balancing, 1, "Neptune Cockpit", "RocketStage3"),
    35080: ItemData(IC.filler, 1, "Water Filtration Machine", "BaseFiltrationMachine"),
    35081: ItemData(IC.progression, 1, "Ultra High Capacity Tank", "HighCapacityTank"),
    35082: ItemData(IC.progression, 1, "Large Room", "BaseLargeRoom"),
    # awarded with their rooms, keeping that as-is as they"re cosmetic
    35083: ItemData(IC.filler, 0, "Large Room Glass Dome", "BaseLargeGlassDome"),
    35084: ItemData(IC.filler, 0, "Multipurpose Room Glass Dome", "BaseGlassDome"),
    35085: ItemData(IC.filler, 0, "Partition", "BasePartition"),
    35086: ItemData(IC.filler, 0, "Partition Door", "BasePartitionDoor"),

    # Bundles of items
    # Awards all furniture as a bundle
    35100: ItemData(IC.filler, 0, "Furniture", "AP_Furniture", ItemType.group),
    # Awards all farming blueprints as a bundle
    35101: ItemData(IC.filler, 0, "Farming", "AP_Farming", ItemType.group),

    # Awards multiple resources as a bundle
    35102: ItemData(IC.filler, 0, "Resources Bundle", "AP_Resources", ItemType.group),

    # resource bundles, as convenience/filler

    # ores
    35200: make_resource_bundle_data("Titanium"),
    35201: make_resource_bundle_data("Copper Ore", "Copper"),
    35202: make_resource_bundle_data("Silver Ore", "Silver"),
    35203: make_resource_bundle_data("Gold"),
    35204: make_resource_bundle_data("Lead"),
    35205: make_resource_bundle_data("Diamond"),
    35206: make_resource_bundle_data("Lithium"),
    35207: make_resource_bundle_data("Ruby", "AluminumOxide"),
    35208: make_resource_bundle_data("Nickel Ore", "Nickel"),
    35209: make_resource_bundle_data("Crystalline Sulfur", "Sulphur"),
    35210: make_resource_bundle_data("Salt Deposit", "Salt"),
    35211: make_resource_bundle_data("Kyanite"),
    35212: make_resource_bundle_data("Magnetite"),
    35213: make_resource_bundle_data("Reactor Rod", "ReactorRod"),
}


items_by_type: Dict[ItemType, List[int]] = {item_type: [] for item_type in ItemType}
for item_id, item_data in item_table.items():
    items_by_type[item_data.type].append(item_id)

group_items: Dict[int, Set[int]] = {
    35100: {35025, 35047, 35048, 35056, 35057, 35058, 35059, 35060, 35061, 35062, 35063, 35064, 35065, 35067, 35068,
            35069, 35070, 35073, 35074},
    35101: {35049, 35050, 35051, 35071, 35072, 35074},
    35102: set(items_by_type[ItemType.resource]),
}
