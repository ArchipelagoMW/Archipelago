from typing import *

from BaseClasses import ItemClassification
import typing

from ..mission_tables import SC2Mission, SC2Race, SC2Campaign
from ..item import parent_names, ItemData, TerranItemType, FactionlessItemType, ProtossItemType, ZergItemType
from ..mission_order.presets_static import get_used_layout_names
from . import item_names



def get_full_item_list():
    return item_table


SC2WOL_ITEM_ID_OFFSET = 1000
SC2HOTS_ITEM_ID_OFFSET = SC2WOL_ITEM_ID_OFFSET + 1000
SC2LOTV_ITEM_ID_OFFSET = SC2HOTS_ITEM_ID_OFFSET + 1000
SC2_KEY_ITEM_ID_OFFSET = SC2LOTV_ITEM_ID_OFFSET + 1000
# Reserve this many IDs for missions, layouts, campaigns, and generic keys each
SC2_KEY_ITEM_SECTION_SIZE = 1000

WEAPON_ARMOR_UPGRADE_MAX_LEVEL = 5


# The items are sorted by their IDs. The IDs shall be kept for compatibility with older games.
item_table = {
    # WoL
    item_names.MARINE:
        ItemData(0 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.MEDIC:
        ItemData(1 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.FIREBAT:
        ItemData(2 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 2, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.MARAUDER:
        ItemData(3 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.REAPER:
        ItemData(4 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.HELLION:
        ItemData(5 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.VULTURE:
        ItemData(6 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.GOLIATH:
        ItemData(7 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.DIAMONDBACK:
        ItemData(8 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.SIEGE_TANK:
        ItemData(9 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.MEDIVAC:
        ItemData(10 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.WRAITH:
        ItemData(11 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 11, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.VIKING:
        ItemData(12 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.BANSHEE:
        ItemData(13 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.BATTLECRUISER:
        ItemData(14 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 14, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.GHOST:
        ItemData(15 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.SPECTRE:
        ItemData(16 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 16, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.THOR:
        ItemData(17 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    # EE units
    item_names.LIBERATOR:
        ItemData(18 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 18, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.VALKYRIE:
        ItemData(19 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 19, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.WIDOW_MINE:
        ItemData(20 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.CYCLONE:
        ItemData(21 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 21, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.HERC:
        ItemData(22 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 26, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.WARHOUND:
        ItemData(23 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 27, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.DOMINION_TROOPER:
        ItemData(24 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    # Elites, currently disabled for balance
    item_names.PRIDE_OF_AUGUSTRGRAD:
        ItemData(50 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 28, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.SKY_FURY:
        ItemData(51 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 29, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.SHOCK_DIVISION:
        ItemData(52 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.BLACKHAMMER:
        ItemData(53 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.AEGIS_GUARD:
        ItemData(54 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 2, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.EMPERORS_SHADOW:
        ItemData(55 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.SON_OF_KORHAL:
        ItemData(56 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.BULWARK_COMPANY:
        ItemData(57 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.FIELD_RESPONSE_THETA:
        ItemData(58 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.EMPERORS_GUARDIAN:
        ItemData(59 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NIGHT_HAWK:
        ItemData(60 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NIGHT_WOLF:
        ItemData(61 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit_2, 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression),

    # Some other items are moved to Upgrade group because of the way how the bot message is parsed
    item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON: ItemData(100 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, 0, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.INFANTRY_WEAPON_UNITS),
    item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR: ItemData(102 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, 4, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.INFANTRY_UNITS),
    item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON: ItemData(103 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, 8, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.VEHICLE_WEAPON_UNITS),
    item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR: ItemData(104 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, 12, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.VEHICLE_UNITS),
    item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON: ItemData(105 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, 16, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.STARSHIP_WEAPON_UNITS),
    item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR: ItemData(106 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, 20, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.STARSHIP_UNITS),
    # Bundles
    item_names.PROGRESSIVE_TERRAN_WEAPON_UPGRADE: ItemData(107 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, -1, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE: ItemData(108 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, -1, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE: ItemData(109 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, -1, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.INFANTRY_UNITS),
    item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE: ItemData(110 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, -1, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.VEHICLE_UNITS),
    item_names.PROGRESSIVE_TERRAN_SHIP_UPGRADE: ItemData(111 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, -1, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.STARSHIP_UNITS),
    item_names.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE: ItemData(112 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Upgrade, -1, SC2Race.TERRAN, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),

    # Unit and structure upgrades
    item_names.BUNKER_PROJECTILE_ACCELERATOR:
        ItemData(200 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 0, SC2Race.TERRAN,
                 parent=item_names.BUNKER),
    item_names.BUNKER_NEOSTEEL_BUNKER:
        ItemData(201 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 1, SC2Race.TERRAN,
                 parent=item_names.BUNKER),
    item_names.MISSILE_TURRET_TITANIUM_HOUSING:
        ItemData(202 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 2, SC2Race.TERRAN,
                 parent=item_names.MISSILE_TURRET),
    item_names.MISSILE_TURRET_HELLSTORM_BATTERIES:
        ItemData(203 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 3, SC2Race.TERRAN,
                 parent=item_names.MISSILE_TURRET),
    item_names.SCV_ADVANCED_CONSTRUCTION:
        ItemData(204 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 4, SC2Race.TERRAN),
    item_names.SCV_DUAL_FUSION_WELDERS:
        ItemData(205 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 5, SC2Race.TERRAN),
    item_names.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM:
        ItemData(206 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 24, SC2Race.TERRAN,
                 quantity=2),
    item_names.PROGRESSIVE_ORBITAL_COMMAND:
        ItemData(207 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.Deprecated, -1, SC2Race.TERRAN,
                 quantity=0, classification=ItemClassification.progression),
    item_names.MARINE_PROGRESSIVE_STIMPACK:
        ItemData(208 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.MARINE, quantity=2),
    item_names.MARINE_COMBAT_SHIELD:
        ItemData(209 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.MARINE),
    item_names.MEDIC_ADVANCED_MEDIC_FACILITIES:
        ItemData(210 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 10, SC2Race.TERRAN,
                 parent=item_names.MEDIC),
    item_names.MEDIC_STABILIZER_MEDPACKS:
        ItemData(211 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 11, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.MEDIC),
    item_names.FIREBAT_INCINERATOR_GAUNTLETS:
        ItemData(212 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 12, SC2Race.TERRAN,
                 parent=item_names.FIREBAT),
    item_names.FIREBAT_JUGGERNAUT_PLATING:
        ItemData(213 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.FIREBAT),
    item_names.MARAUDER_CONCUSSIVE_SHELLS:
        ItemData(214 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 14, SC2Race.TERRAN,
                 parent=item_names.MARAUDER),
    item_names.MARAUDER_KINETIC_FOAM:
        ItemData(215 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 15, SC2Race.TERRAN,
                 parent=item_names.MARAUDER),
    item_names.REAPER_U238_ROUNDS:
        ItemData(216 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 16, SC2Race.TERRAN,
                 parent=item_names.REAPER),
    item_names.REAPER_G4_CLUSTERBOMB:
        ItemData(217 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.REAPER),
    item_names.CYCLONE_MAG_FIELD_ACCELERATORS:
        ItemData(218 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 18, SC2Race.TERRAN,
                 parent=item_names.CYCLONE),
    item_names.CYCLONE_MAG_FIELD_LAUNCHERS:
        ItemData(219 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 19, SC2Race.TERRAN,
                 parent=item_names.CYCLONE),
    item_names.MARINE_LASER_TARGETING_SYSTEM:
        ItemData(220 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.MARINE),
    item_names.MARINE_MAGRAIL_MUNITIONS:
        ItemData(221 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.MARINE),
    item_names.MARINE_OPTIMIZED_LOGISTICS:
        ItemData(222 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 21, SC2Race.TERRAN,
                 parent=item_names.MARINE),
    item_names.MEDIC_RESTORATION:
        ItemData(223 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 22, SC2Race.TERRAN,
                 parent=item_names.MEDIC),
    item_names.MEDIC_OPTICAL_FLARE:
        ItemData(224 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 23, SC2Race.TERRAN,
                 parent=item_names.MEDIC),
    item_names.MEDIC_RESOURCE_EFFICIENCY:
        ItemData(225 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 24, SC2Race.TERRAN,
                 parent=item_names.MEDIC),
    item_names.FIREBAT_PROGRESSIVE_STIMPACK:
        ItemData(226 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.FIREBAT, quantity=2),
    item_names.FIREBAT_RESOURCE_EFFICIENCY:
        ItemData(227 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 25, SC2Race.TERRAN,
                 parent=item_names.FIREBAT),
    item_names.MARAUDER_PROGRESSIVE_STIMPACK:
        ItemData(228 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 8, SC2Race.TERRAN,
                 parent=item_names.MARAUDER, quantity=2),
    item_names.MARAUDER_LASER_TARGETING_SYSTEM:
        ItemData(229 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 26, SC2Race.TERRAN,
                 parent=item_names.MARAUDER),
    item_names.MARAUDER_MAGRAIL_MUNITIONS:
        ItemData(230 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 27, SC2Race.TERRAN,
                 parent=item_names.MARAUDER),
    item_names.MARAUDER_INTERNAL_TECH_MODULE:
        ItemData(231 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 28, SC2Race.TERRAN,
                 parent=item_names.MARAUDER),
    item_names.SCV_HOSTILE_ENVIRONMENT_ADAPTATION:
        ItemData(232 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 29, SC2Race.TERRAN),
    item_names.MEDIC_ADAPTIVE_MEDPACKS:
        ItemData(233 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.MEDIC),
    item_names.MEDIC_NANO_PROJECTOR:
        ItemData(234 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 1, SC2Race.TERRAN,
                 parent=item_names.MEDIC),
    item_names.FIREBAT_INFERNAL_PRE_IGNITER:
        ItemData(235 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 2, SC2Race.TERRAN,
                 parent=item_names.FIREBAT),
    item_names.FIREBAT_KINETIC_FOAM:
        ItemData(236 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 3, SC2Race.TERRAN,
                 parent=item_names.FIREBAT),
    item_names.FIREBAT_NANO_PROJECTORS:
        ItemData(237 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.FIREBAT),
    item_names.MARAUDER_JUGGERNAUT_PLATING:
        ItemData(238 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 5, SC2Race.TERRAN,
                 parent=item_names.MARAUDER),
    item_names.REAPER_JET_PACK_OVERDRIVE:
        ItemData(239 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing, parent=item_names.REAPER),
    item_names.HELLION_INFERNAL_PLATING:
        ItemData(240 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 7, SC2Race.TERRAN,
                 parent=item_names.HELLION),
    item_names.VULTURE_JERRYRIGGED_PATCHUP:
        ItemData(241 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 8, SC2Race.TERRAN,
                 parent=item_names.VULTURE),
    item_names.GOLIATH_SHAPED_HULL:
        ItemData(242 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 9, SC2Race.TERRAN,
                 parent=item_names.GOLIATH),
    item_names.GOLIATH_RESOURCE_EFFICIENCY:
        ItemData(243 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 10, SC2Race.TERRAN,
                 parent=item_names.GOLIATH),
    item_names.GOLIATH_INTERNAL_TECH_MODULE:
        ItemData(244 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 11, SC2Race.TERRAN,
                 parent=item_names.GOLIATH),
    item_names.SIEGE_TANK_SHAPED_HULL:
        ItemData(245 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 12, SC2Race.TERRAN,
                 parent=item_names.SIEGE_TANK),
    item_names.SIEGE_TANK_RESOURCE_EFFICIENCY:
        ItemData(246 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 13, SC2Race.TERRAN,
                 parent=item_names.SIEGE_TANK),
    item_names.PREDATOR_CLOAK:
        ItemData(247 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 14, SC2Race.TERRAN,
                 parent=item_names.PREDATOR),
    item_names.PREDATOR_CHARGE:
        ItemData(248 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 15, SC2Race.TERRAN,
                 parent=item_names.PREDATOR),
    item_names.MEDIVAC_SCATTER_VEIL:
        ItemData(249 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 16, SC2Race.TERRAN,
                 parent=item_names.MEDIVAC),
    item_names.REAPER_PROGRESSIVE_STIMPACK:
        ItemData(250 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 10, SC2Race.TERRAN,
                 parent=item_names.REAPER, quantity=2),
    item_names.REAPER_LASER_TARGETING_SYSTEM:
        ItemData(251 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 17, SC2Race.TERRAN,
                 parent=item_names.REAPER),
    item_names.REAPER_ADVANCED_CLOAKING_FIELD:
        ItemData(252 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 18, SC2Race.TERRAN,
                 parent=item_names.REAPER),
    item_names.REAPER_SPIDER_MINES:
        ItemData(253 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 19, SC2Race.TERRAN,
                 parent=item_names.REAPER,
                 important_for_filtering=True),
    item_names.REAPER_COMBAT_DRUGS:
        ItemData(254 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 20, SC2Race.TERRAN,
                 parent=item_names.REAPER),
    item_names.HELLION_HELLBAT:
        ItemData(255 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 21, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.HELLION),
    item_names.HELLION_SMART_SERVOS:
        ItemData(256 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 22, SC2Race.TERRAN,
                 parent=item_names.HELLION),
    item_names.HELLION_OPTIMIZED_LOGISTICS:
        ItemData(257 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 23, SC2Race.TERRAN,
                 parent=item_names.HELLION),
    item_names.HELLION_JUMP_JETS:
        ItemData(258 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 24, SC2Race.TERRAN,
                 parent=item_names.HELLION),
    item_names.HELLION_PROGRESSIVE_STIMPACK:
        ItemData(259 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 12, SC2Race.TERRAN,
                 parent=item_names.HELLION, quantity=2),
    item_names.VULTURE_ION_THRUSTERS:
        ItemData(260 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 25, SC2Race.TERRAN,
                 parent=item_names.VULTURE),
    item_names.VULTURE_AUTO_LAUNCHERS:
        ItemData(261 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 26, SC2Race.TERRAN,
                 parent=item_names.VULTURE),
    item_names.SPIDER_MINE_HIGH_EXPLOSIVE_MUNITION:
        ItemData(262 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 27, SC2Race.TERRAN,
            parent=parent_names.SPIDER_MINE_SOURCE),
    item_names.GOLIATH_JUMP_JETS:
        ItemData(263 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 28, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.GOLIATH),
    item_names.GOLIATH_OPTIMIZED_LOGISTICS:
        ItemData(264 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_2, 29, SC2Race.TERRAN,
                 parent=item_names.GOLIATH),
    item_names.DIAMONDBACK_HYPERFLUXOR:
        ItemData(265 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 0, SC2Race.TERRAN,
                 parent=item_names.DIAMONDBACK),
    item_names.DIAMONDBACK_BURST_CAPACITORS:
        ItemData(266 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 1, SC2Race.TERRAN,
                 parent=item_names.DIAMONDBACK),
    item_names.DIAMONDBACK_RESOURCE_EFFICIENCY:
        ItemData(267 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 2, SC2Race.TERRAN,
                 parent=item_names.DIAMONDBACK),
    item_names.SIEGE_TANK_JUMP_JETS:
        ItemData(268 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.SIEGE_TANK),
    item_names.SIEGE_TANK_SPIDER_MINES:
        ItemData(269 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 4, SC2Race.TERRAN,
                 parent=item_names.SIEGE_TANK,
                 important_for_filtering=True),
    item_names.SIEGE_TANK_SMART_SERVOS:
        ItemData(270 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.SIEGE_TANK),
    item_names.SIEGE_TANK_GRADUATING_RANGE:
        ItemData(271 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.SIEGE_TANK),
    item_names.SIEGE_TANK_LASER_TARGETING_SYSTEM:
        ItemData(272 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 7, SC2Race.TERRAN,
                 parent=item_names.SIEGE_TANK),
    item_names.SIEGE_TANK_ADVANCED_SIEGE_TECH:
        ItemData(273 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 8, SC2Race.TERRAN,
                 parent=item_names.SIEGE_TANK),
    item_names.SIEGE_TANK_INTERNAL_TECH_MODULE:
        ItemData(274 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 9, SC2Race.TERRAN,
                 parent=item_names.SIEGE_TANK),
    item_names.PREDATOR_RESOURCE_EFFICIENCY:
        ItemData(275 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.PREDATOR),
    item_names.MEDIVAC_EXPANDED_HULL:
        ItemData(276 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 11, SC2Race.TERRAN,
                 parent=item_names.MEDIVAC),
    item_names.MEDIVAC_AFTERBURNERS:
        ItemData(277 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 12, SC2Race.TERRAN,
                 parent=item_names.MEDIVAC),
    item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY:
        ItemData(278 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.WRAITH),
    item_names.VIKING_SMART_SERVOS:
        ItemData(279 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 14, SC2Race.TERRAN,
                 parent=item_names.VIKING),
    item_names.VIKING_ANTI_MECHANICAL_MUNITION:
        ItemData(280 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 15, SC2Race.TERRAN,
                 parent=item_names.VIKING),
    item_names.DIAMONDBACK_MAGLEV_PROPULSION:
        ItemData(281 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 21, SC2Race.TERRAN,
                 parent=item_names.DIAMONDBACK),
    item_names.WARHOUND_RESOURCE_EFFICIENCY:
        ItemData(282 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 13, SC2Race.TERRAN,
                 parent=item_names.WARHOUND),
    item_names.WARHOUND_AXIOM_PLATING:
        ItemData(283 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 14, SC2Race.TERRAN,
                 parent=item_names.WARHOUND),
    item_names.HERC_RESOURCE_EFFICIENCY:
        ItemData(284 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 15, SC2Race.TERRAN,
                 parent=item_names.HERC),
    item_names.HERC_JUGGERNAUT_PLATING:
        ItemData(285 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 16, SC2Race.TERRAN,
                 parent=item_names.HERC),
    item_names.HERC_KINETIC_FOAM:
        ItemData(286 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 17, SC2Race.TERRAN,
                 parent=item_names.HERC),
    item_names.REAPER_RESOURCE_EFFICIENCY:
        ItemData(287 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 18, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.REAPER),
    item_names.REAPER_BALLISTIC_FLIGHTSUIT:
        ItemData(288 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 19, SC2Race.TERRAN,
                 parent=item_names.REAPER),
    item_names.SIEGE_TANK_PROGRESSIVE_TRANSPORT_HOOK:
        ItemData(289 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive_2, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=parent_names.SIEGE_TANK_AND_TRANSPORT, quantity=2),
    item_names.SIEGE_TANK_ALLTERRAIN_TREADS :
        ItemData(290 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 20, SC2Race.TERRAN,
                 parent=item_names.SIEGE_TANK),
    item_names.MEDIVAC_RAPID_REIGNITION_SYSTEMS:
        ItemData(291 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 21, SC2Race.TERRAN,
                 parent=item_names.MEDIVAC),
    item_names.BATTLECRUISER_BEHEMOTH_REACTOR:
        ItemData(292 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 22, SC2Race.TERRAN,
                 parent=item_names.BATTLECRUISER),
    item_names.THOR_RAPID_RELOAD:
        ItemData(293 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 23, SC2Race.TERRAN,
                 parent=item_names.THOR),
    item_names.LIBERATOR_GUERILLA_MISSILES:
        ItemData(294 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 24, SC2Race.TERRAN,
                 parent=item_names.LIBERATOR),
    item_names.WIDOW_MINE_RESOURCE_EFFICIENCY:
        ItemData(295 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 25, SC2Race.TERRAN,
                 parent=item_names.WIDOW_MINE),
    item_names.HERC_GRAPPLE_PULL:
        ItemData(296 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 26, SC2Race.TERRAN,
                 parent=item_names.HERC),
    item_names.COMMAND_CENTER_SCANNER_SWEEP:
        ItemData(297 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 27, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.COMMAND_CENTER_MULE:
        ItemData(298 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 28, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.COMMAND_CENTER_EXTRA_SUPPLIES:
        ItemData(299 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 29, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.HELLION_TWIN_LINKED_FLAMETHROWER:
        ItemData(300 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 16, SC2Race.TERRAN,
                 parent=item_names.HELLION),
    item_names.HELLION_THERMITE_FILAMENTS:
        ItemData(301 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 17, SC2Race.TERRAN,
                 parent=item_names.HELLION),
    item_names.SPIDER_MINE_CERBERUS_MINE:
        ItemData(302 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 18, SC2Race.TERRAN,
                 parent=parent_names.SPIDER_MINE_SOURCE),
    item_names.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE:
        ItemData(303 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 16, SC2Race.TERRAN,
                 parent=item_names.VULTURE, quantity=2),
    item_names.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM:
        ItemData(304 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 19, SC2Race.TERRAN,
                 parent=item_names.GOLIATH),
    item_names.GOLIATH_ARES_CLASS_TARGETING_SYSTEM:
        ItemData(305 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 20, SC2Race.TERRAN,
                 parent=item_names.GOLIATH),
    item_names.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL:
        ItemData(306 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive_2, 4, SC2Race.TERRAN,
                 parent=item_names.DIAMONDBACK, quantity=2),
    item_names.DIAMONDBACK_SHAPED_HULL:
        ItemData(307 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 22, SC2Race.TERRAN,
                 parent=item_names.DIAMONDBACK),
    item_names.SIEGE_TANK_MAELSTROM_ROUNDS:
        ItemData(308 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.SIEGE_TANK),
    item_names.SIEGE_TANK_SHAPED_BLAST:
        ItemData(309 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 24, SC2Race.TERRAN,
                 parent=item_names.SIEGE_TANK),
    item_names.MEDIVAC_RAPID_DEPLOYMENT_TUBE:
        ItemData(310 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 25, SC2Race.TERRAN,
                 parent=item_names.MEDIVAC),
    item_names.MEDIVAC_ADVANCED_HEALING_AI:
        ItemData(311 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 26, SC2Race.TERRAN,
                 parent=item_names.MEDIVAC),
    item_names.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS:
        ItemData(312 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 18, SC2Race.TERRAN,
                 parent=item_names.WRAITH, quantity=2),
    item_names.WRAITH_DISPLACEMENT_FIELD:
        ItemData(313 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 27, SC2Race.TERRAN,
                 parent=item_names.WRAITH),
    item_names.VIKING_RIPWAVE_MISSILES:
        ItemData(314 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 28, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.VIKING),
    item_names.VIKING_PHOBOS_CLASS_WEAPONS_SYSTEM:
        ItemData(315 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_3, 29, SC2Race.TERRAN,
                 parent=item_names.VIKING),
    item_names.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS:
        ItemData(316 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 2, SC2Race.TERRAN,
                 parent=item_names.BANSHEE, quantity=2),
    item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY:
        ItemData(317 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.BANSHEE),
    item_names.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS:
        ItemData(318 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive_2, 2, SC2Race.TERRAN,
                 parent=item_names.BATTLECRUISER, quantity=2),
    item_names.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX:
        ItemData(319 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.BATTLECRUISER, quantity=2),
    item_names.GHOST_OCULAR_IMPLANTS:
        ItemData(320 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 2, SC2Race.TERRAN,
                 parent=item_names.GHOST),
    item_names.GHOST_CRIUS_SUIT:
        ItemData(321 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 3, SC2Race.TERRAN,
                 parent=item_names.GHOST),
    item_names.SPECTRE_PSIONIC_LASH:
        ItemData(322 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.SPECTRE),
    item_names.SPECTRE_NYX_CLASS_CLOAKING_MODULE:
        ItemData(323 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 5, SC2Race.TERRAN,
                 parent=item_names.SPECTRE),
    item_names.THOR_330MM_BARRAGE_CANNON:
        ItemData(324 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 6, SC2Race.TERRAN,
                 parent=item_names.THOR),
    item_names.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL:
        ItemData(325 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 22, SC2Race.TERRAN,
                 parent=item_names.THOR, quantity=2),
    item_names.LIBERATOR_ADVANCED_BALLISTICS:
        ItemData(326 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 7, SC2Race.TERRAN,
                 parent=item_names.LIBERATOR),
    item_names.LIBERATOR_RAID_ARTILLERY:
        ItemData(327 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.LIBERATOR),
    item_names.WIDOW_MINE_DRILLING_CLAWS:
        ItemData(328 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 9, SC2Race.TERRAN,
                 parent=item_names.WIDOW_MINE),
    item_names.WIDOW_MINE_CONCEALMENT:
        ItemData(329 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.WIDOW_MINE),
    item_names.MEDIVAC_ADVANCED_CLOAKING_FIELD:
        ItemData(330 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 11, SC2Race.TERRAN,
                 parent=item_names.MEDIVAC),
    item_names.WRAITH_TRIGGER_OVERRIDE:
        ItemData(331 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 12, SC2Race.TERRAN,
                 parent=item_names.WRAITH),
    item_names.WRAITH_INTERNAL_TECH_MODULE:
        ItemData(332 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 13, SC2Race.TERRAN,
                 parent=item_names.WRAITH),
    item_names.WRAITH_RESOURCE_EFFICIENCY:
        ItemData(333 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 14, SC2Race.TERRAN,
                 parent=item_names.WRAITH),
    item_names.VIKING_SHREDDER_ROUNDS:
        ItemData(334 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.VIKING),
    item_names.VIKING_WILD_MISSILES:
        ItemData(335 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 16, SC2Race.TERRAN,
                 parent=item_names.VIKING),
    item_names.BANSHEE_SHAPED_HULL:
        ItemData(336 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.BANSHEE),
    item_names.BANSHEE_ADVANCED_TARGETING_OPTICS:
        ItemData(337 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 18, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.BANSHEE),
    item_names.BANSHEE_DISTORTION_BLASTERS:
        ItemData(338 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 19, SC2Race.TERRAN,
                 parent=item_names.BANSHEE),
    item_names.BANSHEE_ROCKET_BARRAGE:
        ItemData(339 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.BANSHEE),
    item_names.GHOST_RESOURCE_EFFICIENCY:
        ItemData(340 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 21, SC2Race.TERRAN,
                 parent=item_names.GHOST),
    item_names.SPECTRE_RESOURCE_EFFICIENCY:
        ItemData(341 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 22, SC2Race.TERRAN,
                 parent=item_names.SPECTRE),
    item_names.THOR_BUTTON_WITH_A_SKULL_ON_IT:
        ItemData(342 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.THOR),
    item_names.THOR_LASER_TARGETING_SYSTEM:
        ItemData(343 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 24, SC2Race.TERRAN,
                 parent=item_names.THOR),
    item_names.THOR_LARGE_SCALE_FIELD_CONSTRUCTION:
        ItemData(344 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 25, SC2Race.TERRAN,
                 parent=item_names.THOR),
    item_names.RAVEN_RESOURCE_EFFICIENCY:
        ItemData(345 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 26, SC2Race.TERRAN,
                 parent=item_names.RAVEN),
    item_names.RAVEN_DURABLE_MATERIALS:
        ItemData(346 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 27, SC2Race.TERRAN,
                 parent=item_names.RAVEN),
    item_names.SCIENCE_VESSEL_IMPROVED_NANO_REPAIR:
        ItemData(347 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 28, SC2Race.TERRAN,
                 parent=item_names.SCIENCE_VESSEL),
    item_names.SCIENCE_VESSEL_MAGELLAN_COMPUTATION_SYSTEMS:
        ItemData(348 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 29, SC2Race.TERRAN,
                 parent=item_names.SCIENCE_VESSEL),
    item_names.CYCLONE_RESOURCE_EFFICIENCY:
        ItemData(349 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 0, SC2Race.TERRAN,
                 parent=item_names.CYCLONE),
    item_names.BANSHEE_HYPERFLIGHT_ROTORS:
        ItemData(350 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 1, SC2Race.TERRAN,
                 parent=item_names.BANSHEE),
    item_names.BANSHEE_LASER_TARGETING_SYSTEM:
        ItemData(351 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 2, SC2Race.TERRAN,
                 parent=item_names.BANSHEE),
    item_names.BANSHEE_INTERNAL_TECH_MODULE:
        ItemData(352 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 3, SC2Race.TERRAN,
                 parent=item_names.BANSHEE),
    item_names.BATTLECRUISER_TACTICAL_JUMP:
        ItemData(353 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 4, SC2Race.TERRAN,
                 parent=item_names.BATTLECRUISER),
    item_names.BATTLECRUISER_CLOAK:
        ItemData(354 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 5, SC2Race.TERRAN,
                 parent=item_names.BATTLECRUISER),
    item_names.BATTLECRUISER_ATX_LASER_BATTERY:
        ItemData(355 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.BATTLECRUISER),
    item_names.BATTLECRUISER_OPTIMIZED_LOGISTICS:
        ItemData(356 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 7, SC2Race.TERRAN,
                 parent=item_names.BATTLECRUISER),
    item_names.BATTLECRUISER_INTERNAL_TECH_MODULE:
        ItemData(357 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 8, SC2Race.TERRAN,
                 parent=item_names.BATTLECRUISER),
    item_names.GHOST_EMP_ROUNDS:
        ItemData(358 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.GHOST),
    item_names.GHOST_LOCKDOWN:
        ItemData(359 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.GHOST),
    item_names.SPECTRE_IMPALER_ROUNDS:
        ItemData(360 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 11, SC2Race.TERRAN,
                 parent=item_names.SPECTRE),
    item_names.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD:
        ItemData(361 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 14, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.THOR, quantity=2),
    item_names.RAVEN_BIO_MECHANICAL_REPAIR_DRONE:
        ItemData(363 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.RAVEN),
    item_names.RAVEN_SPIDER_MINES:
        ItemData(364 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 13, SC2Race.TERRAN,
                 parent=item_names.RAVEN, important_for_filtering=True),
    item_names.RAVEN_RAILGUN_TURRET:
        ItemData(365 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 14, SC2Race.TERRAN,
                 parent=item_names.RAVEN),
    item_names.RAVEN_HUNTER_SEEKER_WEAPON:
        ItemData(366 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.RAVEN),
    item_names.RAVEN_INTERFERENCE_MATRIX:
        ItemData(367 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 16, SC2Race.TERRAN,
                 parent=item_names.RAVEN),
    item_names.RAVEN_ANTI_ARMOR_MISSILE:
        ItemData(368 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 17, SC2Race.TERRAN,
                 parent=item_names.RAVEN),
    item_names.RAVEN_INTERNAL_TECH_MODULE:
        ItemData(369 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 18, SC2Race.TERRAN,
                 parent=item_names.RAVEN),
    item_names.SCIENCE_VESSEL_EMP_SHOCKWAVE:
        ItemData(370 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 19, SC2Race.TERRAN,
                 parent=item_names.SCIENCE_VESSEL),
    item_names.SCIENCE_VESSEL_DEFENSIVE_MATRIX:
        ItemData(371 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 20, SC2Race.TERRAN,
                 parent=item_names.SCIENCE_VESSEL),
    item_names.CYCLONE_TARGETING_OPTICS:
        ItemData(372 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 21, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.CYCLONE),
    item_names.CYCLONE_RAPID_FIRE_LAUNCHERS:
        ItemData(373 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 22, SC2Race.TERRAN,
                 parent=item_names.CYCLONE),
    item_names.LIBERATOR_CLOAK:
        ItemData(374 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 23, SC2Race.TERRAN,
                 parent=item_names.LIBERATOR),
    item_names.LIBERATOR_LASER_TARGETING_SYSTEM:
        ItemData(375 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 24, SC2Race.TERRAN,
                 parent=item_names.LIBERATOR),
    item_names.LIBERATOR_OPTIMIZED_LOGISTICS:
        ItemData(376 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 25, SC2Race.TERRAN,
                 parent=item_names.LIBERATOR),
    item_names.WIDOW_MINE_BLACK_MARKET_LAUNCHERS:
        ItemData(377 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 26, SC2Race.TERRAN,
                 parent=item_names.WIDOW_MINE),
    item_names.WIDOW_MINE_EXECUTIONER_MISSILES:
        ItemData(378 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 27, SC2Race.TERRAN,
                 parent=item_names.WIDOW_MINE),
    item_names.VALKYRIE_ENHANCED_CLUSTER_LAUNCHERS:
        ItemData(379 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 28,  SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.VALKYRIE),
    item_names.VALKYRIE_SHAPED_HULL:
        ItemData(380 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_5, 29, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.VALKYRIE),
    item_names.VALKYRIE_FLECHETTE_MISSILES:
        ItemData(381 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.VALKYRIE),
    item_names.VALKYRIE_AFTERBURNERS:
        ItemData(382 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.VALKYRIE),
    item_names.CYCLONE_INTERNAL_TECH_MODULE:
        ItemData(383 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 2, SC2Race.TERRAN,
                 parent=item_names.CYCLONE),
    item_names.LIBERATOR_SMART_SERVOS:
        ItemData(384 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.LIBERATOR),
    item_names.LIBERATOR_RESOURCE_EFFICIENCY:
        ItemData(385 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 4, SC2Race.TERRAN,
                 parent=item_names.LIBERATOR),
    item_names.HERCULES_INTERNAL_FUSION_MODULE:
        ItemData(386 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 5, SC2Race.TERRAN,
                 parent=item_names.HERCULES),
    item_names.HERCULES_TACTICAL_JUMP:
        ItemData(387 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 6, SC2Race.TERRAN,
                 parent=item_names.HERCULES),
    item_names.PLANETARY_FORTRESS_PROGRESSIVE_AUGMENTED_THRUSTERS:
        ItemData(388 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 28, SC2Race.TERRAN,
                 parent=item_names.PLANETARY_FORTRESS, quantity=2),
    item_names.PLANETARY_FORTRESS_IBIKS_TRACKING_SCANNERS:
        ItemData(389 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.PLANETARY_FORTRESS),
    item_names.VALKYRIE_LAUNCHING_VECTOR_COMPENSATOR:
        ItemData(390 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 8, SC2Race.TERRAN,
                 parent=item_names.VALKYRIE),
    item_names.VALKYRIE_RESOURCE_EFFICIENCY:
        ItemData(391 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 9, SC2Race.TERRAN,
                 parent=item_names.VALKYRIE),
    item_names.PREDATOR_VESPENE_SYNTHESIS:
        ItemData(392 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 10, SC2Race.TERRAN,
                 parent=item_names.PREDATOR),
    item_names.BATTLECRUISER_BEHEMOTH_PLATING:
        ItemData(393 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 11, SC2Race.TERRAN,
                 parent=item_names.BATTLECRUISER),
    item_names.BATTLECRUISER_MOIRAI_IMPULSE_DRIVE:
        ItemData(394 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_6, 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.BATTLECRUISER),
    item_names.PLANETARY_FORTRESS_ORBITAL_MODULE:
        ItemData(395 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_4, 1, SC2Race.TERRAN,
                 parent=parent_names.ORBITAL_COMMAND_AND_PLANETARY),
    item_names.DEVASTATOR_TURRET_CONCUSSIVE_GRENADES:
        ItemData(396 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 0, SC2Race.TERRAN,
                 parent=item_names.DEVASTATOR_TURRET),
    item_names.DEVASTATOR_TURRET_ANTI_ARMOR_MUNITIONS:
        ItemData(397 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 1, SC2Race.TERRAN,
                 parent=item_names.DEVASTATOR_TURRET),
    item_names.DEVASTATOR_TURRET_RESOURCE_EFFICIENCY:
        ItemData(398 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 2, SC2Race.TERRAN,
                 parent=item_names.DEVASTATOR_TURRET),
    item_names.MISSILE_TURRET_RESOURCE_EFFICENCY:
        ItemData(399 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 3, SC2Race.TERRAN,
                 parent=item_names.MISSILE_TURRET),
    # Note(mm): WoL ID 400 collides with buildings; jump forward to leave buildings room

    #Buildings
    item_names.BUNKER:
        ItemData(400 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Building, 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.MISSILE_TURRET:
        ItemData(401 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Building, 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.SENSOR_TOWER:
        ItemData(402 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Building, 2, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.DEVASTATOR_TURRET:
        ItemData(403 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Building, 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression),

    item_names.WAR_PIGS:
        ItemData(500 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.DEVIL_DOGS:
        ItemData(501 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.HAMMER_SECURITIES:
        ItemData(502 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 2, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.SPARTAN_COMPANY:
        ItemData(503 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.SIEGE_BREAKERS:
        ItemData(504 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.HELS_ANGELS:
        ItemData(505 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.DUSK_WINGS:
        ItemData(506 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.JACKSONS_REVENGE:
        ItemData(507 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.SKIBIS_ANGELS:
        ItemData(508 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.DEATH_HEADS:
        ItemData(509 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.WINGED_NIGHTMARES:
        ItemData(510 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.MIDNIGHT_RIDERS:
        ItemData(511 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 11, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.BRYNHILDS:
        ItemData(512 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),
    item_names.JOTUN:
        ItemData(513 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Mercenary, 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression_skip_balancing),

    item_names.ULTRA_CAPACITORS:
        ItemData(600 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 0, SC2Race.TERRAN),
    item_names.VANADIUM_PLATING:
        ItemData(601 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 1, SC2Race.TERRAN),
    item_names.ORBITAL_DEPOTS:
        ItemData(602 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 2, SC2Race.TERRAN, classification=ItemClassification.progression),
    item_names.MICRO_FILTERING:
        ItemData(603 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 3, SC2Race.TERRAN, classification=ItemClassification.progression),
    item_names.AUTOMATED_REFINERY:
        ItemData(604 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 4, SC2Race.TERRAN, classification=ItemClassification.progression),
    item_names.COMMAND_CENTER_COMMAND_CENTER_REACTOR:
        ItemData(605 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 5, SC2Race.TERRAN, classification=ItemClassification.progression),
    item_names.RAVEN:
        ItemData(606 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 22, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.SCIENCE_VESSEL:
        ItemData(607 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.TECH_REACTOR:
        ItemData(608 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 6, SC2Race.TERRAN, classification=ItemClassification.progression),
    item_names.ORBITAL_STRIKE:
        ItemData(609 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 7, SC2Race.TERRAN,
                parent=parent_names.INFANTRY_UNITS),
    item_names.BUNKER_SHRIKE_TURRET:
        ItemData(610 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 6, SC2Race.TERRAN,
                 parent=item_names.BUNKER),
    item_names.BUNKER_FORTIFIED_BUNKER:
        ItemData(611 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_1, 7, SC2Race.TERRAN,
                 parent=item_names.BUNKER),
    item_names.PLANETARY_FORTRESS:
        ItemData(612 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Building, 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.PERDITION_TURRET:
        ItemData(613 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Building, 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.PREDATOR:
        ItemData(614 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 24, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.HERCULES:
        ItemData(615 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Unit, 25, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.CELLULAR_REACTOR:
        ItemData(616 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 8, SC2Race.TERRAN),
    item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL:
        ItemData(617 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive, 4, SC2Race.TERRAN, quantity=3,
                 classification= ItemClassification.progression),
    item_names.HIVE_MIND_EMULATOR:
        ItemData(618 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 21, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.PSI_DISRUPTER:
        ItemData(619 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 18, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.STRUCTURE_ARMOR:
        ItemData(620 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 9, SC2Race.TERRAN),
    item_names.HI_SEC_AUTO_TRACKING:
        ItemData(621 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 10, SC2Race.TERRAN),
    item_names.ADVANCED_OPTICS:
        ItemData(622 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 11, SC2Race.TERRAN),
    item_names.ROGUE_FORCES:
        ItemData(623 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 12, SC2Race.TERRAN, classification=ItemClassification.progression, parent=parent_names.TERRAN_MERCENARIES),
    item_names.MECHANICAL_KNOW_HOW:
        ItemData(624 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 13, SC2Race.TERRAN),
    item_names.MERCENARY_MUNITIONS:
        ItemData(625 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 14, SC2Race.TERRAN),
    item_names.PROGRESSIVE_FAST_DELIVERY:
        ItemData(626 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive_2, 8, SC2Race.TERRAN, quantity=2, classification=ItemClassification.progression, parent=parent_names.TERRAN_MERCENARIES),
    item_names.RAPID_REINFORCEMENT:
        ItemData(627 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 16, SC2Race.TERRAN, classification=ItemClassification.progression, parent=parent_names.TERRAN_MERCENARIES),
    item_names.FUSION_CORE_FUSION_REACTOR:
        ItemData(628 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 17, SC2Race.TERRAN),
    item_names.SONIC_DISRUPTER:
        ItemData(629 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 19, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.PSI_SCREEN:
        ItemData(630 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.ARGUS_AMPLIFIER:
        ItemData(631 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 22, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.PSI_INDOCTRINATOR:
        ItemData(632 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.SIGNAL_BEACON:
        ItemData(633 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Laboratory, 24, SC2Race.TERRAN, parent=parent_names.TERRAN_MERCENARIES),

    # WoL Protoss takes SC2WOL + 700~708

    item_names.SCIENCE_VESSEL_TACTICAL_JUMP:
        ItemData(750 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 4, SC2Race.TERRAN,
                 parent=item_names.SCIENCE_VESSEL),
    item_names.LIBERATOR_UED_MISSILE_TECHNOLOGY:
        ItemData(751 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 5, SC2Race.TERRAN,
                 parent=item_names.LIBERATOR),
    item_names.BATTLECRUISER_FIELD_ASSIST_TARGETING_SYSTEM:
        ItemData(752 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 6, SC2Race.TERRAN,
                 parent=item_names.BATTLECRUISER),
    item_names.PREDATOR_ADAPTIVE_DEFENSES:
        ItemData(753 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.PREDATOR),
    item_names.VIKING_AESIR_TURBINES:
        ItemData(754 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 8, SC2Race.TERRAN,
                 parent=item_names.VIKING),
    item_names.MEDIVAC_RESOURCE_EFFICIENCY:
        ItemData(755 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 9, SC2Race.TERRAN,
                 parent=item_names.MEDIVAC),
    item_names.EMPERORS_SHADOW_SOVEREIGN_TACTICAL_MISSILES:
        ItemData(756 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 10, SC2Race.TERRAN,
                 parent=item_names.EMPERORS_SHADOW),
    item_names.DOMINION_TROOPER_B2_HIGH_CAL_LMG:
        ItemData(757 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 11, SC2Race.TERRAN,
                 parent=item_names.DOMINION_TROOPER, important_for_filtering=True),
    item_names.DOMINION_TROOPER_HAILSTORM_LAUNCHER:
        ItemData(758 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 12, SC2Race.TERRAN,
                 parent=item_names.DOMINION_TROOPER, important_for_filtering=True),
    item_names.DOMINION_TROOPER_CPO7_SALAMANDER_FLAMETHROWER:
        ItemData(759 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 13, SC2Race.TERRAN,
                 parent=item_names.DOMINION_TROOPER, important_for_filtering=True),
    item_names.DOMINION_TROOPER_ADVANCED_ALLOYS:
        ItemData(760 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 14, SC2Race.TERRAN,
                 parent=parent_names.DOMINION_TROOPER_WEAPONS),
    item_names.DOMINION_TROOPER_OPTIMIZED_LOGISTICS:
        ItemData(761 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 15, SC2Race.TERRAN,
                 parent=item_names.DOMINION_TROOPER),
    item_names.SCV_CONSTRUCTION_JUMP_JETS:
        ItemData(762 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 16, SC2Race.TERRAN),
    item_names.WIDOW_MINE_DEMOLITION_PAYLOAD:
        ItemData(763 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent=item_names.WIDOW_MINE),
    item_names.SENSOR_TOWER_ASSISTIVE_TARGETING:
        ItemData(764 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 18, SC2Race.TERRAN,
                 parent=item_names.SENSOR_TOWER),
    item_names.SENSOR_TOWER_MUILTISPECTRUM_DOPPLER:
        ItemData(765 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 19, SC2Race.TERRAN,
                 parent=item_names.SENSOR_TOWER),
    item_names.WARHOUND_DEPLOY_TURRET:
        ItemData(766 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 20, SC2Race.TERRAN,
                 parent=item_names.WARHOUND),
    item_names.GHOST_BARGAIN_BIN_PRICES:
        ItemData(767 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 21, SC2Race.TERRAN,
                 parent=item_names.GHOST),
    item_names.SPECTRE_BARGAIN_BIN_PRICES:
        ItemData(768 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Armory_7, 22, SC2Race.TERRAN,
                 parent=item_names.SPECTRE),

    # Filler items to fill remaining spots
    item_names.STARTING_MINERALS:
        ItemData(800 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.Minerals, -1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    item_names.STARTING_VESPENE:
        ItemData(801 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.Vespene, -1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    item_names.STARTING_SUPPLY:
        ItemData(802 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.Supply, -1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    # This item is used to "remove" location from the game. Never placed unless plando'd
    item_names.NOTHING:
        ItemData(803 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.Nothing, -1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.trap),
    item_names.MAX_SUPPLY:
        ItemData(804 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.MaxSupply, -1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    item_names.SHIELD_REGENERATION:
        ItemData(805 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.ShieldRegeneration, 1, SC2Race.PROTOSS, quantity=0,
                 classification=ItemClassification.filler),
    item_names.BUILDING_CONSTRUCTION_SPEED:
        ItemData(806 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.BuildingSpeed, 1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    item_names.UPGRADE_RESEARCH_SPEED:
        ItemData(807 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.ResearchSpeed, 1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    item_names.UPGRADE_RESEARCH_COST:
        ItemData(808 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.ResearchCost, 1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),

    # Trap Filler
    item_names.REDUCED_MAX_SUPPLY:
        ItemData(850 + SC2WOL_ITEM_ID_OFFSET, FactionlessItemType.MaxSupplyTrap, -1, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.trap),


    # Nova gear
    item_names.NOVA_GHOST_VISOR:
        ItemData(900 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 0, SC2Race.TERRAN, classification=ItemClassification.progression),
    item_names.NOVA_RANGEFINDER_OCULUS:
        ItemData(901 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 1, SC2Race.TERRAN),
    item_names.NOVA_DOMINATION:
        ItemData(902 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 2, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_BLINK:
        ItemData(903 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE:
        ItemData(904 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Progressive_2, 0, SC2Race.TERRAN, quantity=2,
                 classification=ItemClassification.progression),
    item_names.NOVA_ENERGY_SUIT_MODULE:
        ItemData(905 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_ARMORED_SUIT_MODULE:
        ItemData(906 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_JUMP_SUIT_MODULE:
        ItemData(907 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_C20A_CANISTER_RIFLE:
        ItemData(908 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_HELLFIRE_SHOTGUN:
        ItemData(909 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_PLASMA_RIFLE:
        ItemData(910 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_MONOMOLECULAR_BLADE:
        ItemData(911 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_BLAZEFIRE_GUNBLADE:
        ItemData(912 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 11, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_STIM_INFUSION:
        ItemData(913 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_PULSE_GRENADES:
        ItemData(914 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_FLASHBANG_GRENADES:
        ItemData(915 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 14, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_IONIC_FORCE_FIELD:
        ItemData(916 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_HOLO_DECOY:
        ItemData(917 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 16, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    item_names.NOVA_NUKE:
        ItemData(918 + SC2WOL_ITEM_ID_OFFSET, TerranItemType.Nova_Gear, 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression),

    # HotS
    item_names.ZERGLING:
        ItemData(0 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 0, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.SWARM_QUEEN:
        ItemData(1 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 1, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.ROACH:
        ItemData(2 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 2, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.HYDRALISK:
        ItemData(3 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 3, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.ZERGLING_BANELING_ASPECT:
        ItemData(4 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 5, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_ZERGLING),
    item_names.ABERRATION:
        ItemData(5 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 5, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.MUTALISK:
        ItemData(6 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 6, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.SWARM_HOST:
        ItemData(7 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 7, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.INFESTOR:
        ItemData(8 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 8, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.ULTRALISK:
        ItemData(9 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 9, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.SPORE_CRAWLER:
        ItemData(10 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 10, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.SPINE_CRAWLER:
        ItemData(11 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 11, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.CORRUPTOR:
        ItemData(12 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 12, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.SCOURGE:
        ItemData(13 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 13, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.BROOD_QUEEN:
        ItemData(14 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 4, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.DEFILER:
        ItemData(15 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 14, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.INFESTED_MARINE:
        ItemData(16 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 15, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.INFESTED_BUNKER:
        ItemData(17 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 16, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.NYDUS_WORM:
        ItemData(18 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 17, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.ECHIDNA_WORM:
        ItemData(19 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 18, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.INFESTED_SIEGE_TANK:
        ItemData(20 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 19, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.INFESTED_DIAMONDBACK:
        ItemData(21 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 20, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.INFESTED_BANSHEE:
        ItemData(22 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 21, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.INFESTED_LIBERATOR:
        ItemData(23 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 22, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.INFESTED_MISSILE_TURRET:
        ItemData(24 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 23, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.PYGALISK:
        ItemData(25 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 24, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.BILE_LAUNCHER:
        ItemData(26 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 25, SC2Race.ZERG,
                 classification=ItemClassification.progression),
    item_names.BULLFROG:
        ItemData(27 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Unit, 26, SC2Race.ZERG,
                 classification=ItemClassification.progression),

    item_names.PROGRESSIVE_ZERG_MELEE_ATTACK: ItemData(100 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, 0, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.ZERG_MELEE_ATTACKER),
    item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK: ItemData(101 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, 4, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.ZERG_MISSILE_ATTACKER),
    item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE: ItemData(102 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, 8, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.ZERG_CARAPACE_UNIT),
    item_names.PROGRESSIVE_ZERG_FLYER_ATTACK: ItemData(103 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, 12, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.ZERG_FLYING_UNIT),
    item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE: ItemData(104 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, 16, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.ZERG_FLYING_UNIT),
    # Bundles
    item_names.PROGRESSIVE_ZERG_WEAPON_UPGRADE: ItemData(105 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, -1, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_ZERG_ARMOR_UPGRADE: ItemData(106 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, -1, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_ZERG_GROUND_UPGRADE: ItemData(107 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, -1, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.ZERG_CARAPACE_UNIT),
    item_names.PROGRESSIVE_ZERG_FLYER_UPGRADE: ItemData(108 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, -1, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL, parent=parent_names.ZERG_FLYING_UNIT),
    item_names.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE: ItemData(109 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Upgrade, -1, SC2Race.ZERG, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),

    item_names.ZERGLING_HARDENED_CARAPACE:
        ItemData(200 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 0, SC2Race.ZERG, parent=item_names.ZERGLING),
    item_names.ZERGLING_ADRENAL_OVERLOAD:
        ItemData(201 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 1, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ZERGLING),
    item_names.ZERGLING_METABOLIC_BOOST:
        ItemData(202 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 2, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ZERGLING),
    item_names.ROACH_HYDRIODIC_BILE:
        ItemData(203 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 3, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ROACH),
    item_names.ROACH_ADAPTIVE_PLATING:
        ItemData(204 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 4, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ROACH),
    item_names.ROACH_TUNNELING_CLAWS:
        ItemData(205 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 5, SC2Race.ZERG, parent=item_names.ROACH),
    item_names.HYDRALISK_FRENZY:
        ItemData(206 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 6, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.HYDRALISK),
    item_names.HYDRALISK_ANCILLARY_CARAPACE:
        ItemData(207 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 7, SC2Race.ZERG, parent=item_names.HYDRALISK),
    item_names.HYDRALISK_GROOVED_SPINES:
        ItemData(208 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 8, SC2Race.ZERG, parent=item_names.HYDRALISK),
    item_names.BANELING_CORROSIVE_ACID:
        ItemData(209 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 9, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=parent_names.BANELING_SOURCE),
    item_names.BANELING_RUPTURE:
        ItemData(210 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 10, SC2Race.ZERG,
                 parent=parent_names.BANELING_SOURCE),
    item_names.BANELING_REGENERATIVE_ACID:
        ItemData(211 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 11, SC2Race.ZERG,
                 parent=parent_names.BANELING_SOURCE),
    item_names.MUTALISK_VICIOUS_GLAIVE:
        ItemData(212 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 12, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.MUTALISK),
    item_names.MUTALISK_RAPID_REGENERATION:
        ItemData(213 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 13, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.MUTALISK),
    item_names.MUTALISK_SUNDERING_GLAIVE:
        ItemData(214 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 14, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.MUTALISK),
    item_names.SWARM_HOST_BURROW:
        ItemData(215 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 15, SC2Race.ZERG, parent=item_names.SWARM_HOST),
    item_names.SWARM_HOST_RAPID_INCUBATION:
        ItemData(216 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 16, SC2Race.ZERG, parent=item_names.SWARM_HOST),
    item_names.SWARM_HOST_PRESSURIZED_GLANDS:
        ItemData(217 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 17, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.SWARM_HOST),
    item_names.ULTRALISK_BURROW_CHARGE:
        ItemData(218 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 18, SC2Race.ZERG, parent=item_names.ULTRALISK),
    item_names.ULTRALISK_TISSUE_ASSIMILATION:
        ItemData(219 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 19, SC2Race.ZERG, parent=item_names.ULTRALISK),
    item_names.ULTRALISK_MONARCH_BLADES:
        ItemData(220 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 20, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ULTRALISK),
    item_names.CORRUPTOR_CAUSTIC_SPRAY:
        ItemData(221 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 21, SC2Race.ZERG, parent=item_names.CORRUPTOR),
    item_names.CORRUPTOR_CORRUPTION:
        ItemData(222 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 22, SC2Race.ZERG, parent=item_names.CORRUPTOR),
    item_names.SCOURGE_VIRULENT_SPORES:
        ItemData(223 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 23, SC2Race.ZERG, parent=item_names.SCOURGE),
    item_names.SCOURGE_RESOURCE_EFFICIENCY:
        ItemData(224 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 24, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.SCOURGE),
    item_names.SCOURGE_SWARM_SCOURGE:
        ItemData(225 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 25, SC2Race.ZERG, parent=item_names.SCOURGE),
    item_names.ZERGLING_SHREDDING_CLAWS:
        ItemData(226 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 26, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ZERGLING),
    item_names.ROACH_GLIAL_RECONSTITUTION:
        ItemData(227 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 27, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ROACH),
    item_names.ROACH_ORGANIC_CARAPACE:
        ItemData(228 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 28, SC2Race.ZERG, parent=item_names.ROACH),
    item_names.HYDRALISK_MUSCULAR_AUGMENTS:
        ItemData(229 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_1, 29, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.HYDRALISK),
    item_names.HYDRALISK_RESOURCE_EFFICIENCY:
        ItemData(230 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 0, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.HYDRALISK),
    item_names.BANELING_CENTRIFUGAL_HOOKS:
        ItemData(231 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 1, SC2Race.ZERG,
                 parent=parent_names.BANELING_SOURCE),
    item_names.BANELING_TUNNELING_JAWS:
        ItemData(232 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 2, SC2Race.ZERG,
                 parent=parent_names.BANELING_SOURCE),
    item_names.BANELING_RAPID_METAMORPH:
        ItemData(233 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 3, SC2Race.ZERG,
                 parent=item_names.ZERGLING_BANELING_ASPECT),
    item_names.MUTALISK_SEVERING_GLAIVE:
        ItemData(234 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 4, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.MUTALISK),
    item_names.MUTALISK_AERODYNAMIC_GLAIVE_SHAPE:
        ItemData(235 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 5, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.MUTALISK),
    item_names.SWARM_HOST_LOCUST_METABOLIC_BOOST:
        ItemData(236 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 6, SC2Race.ZERG, parent=item_names.SWARM_HOST),
    item_names.SWARM_HOST_ENDURING_LOCUSTS:
        ItemData(237 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 7, SC2Race.ZERG, parent=item_names.SWARM_HOST),
    item_names.SWARM_HOST_ORGANIC_CARAPACE:
        ItemData(238 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 8, SC2Race.ZERG, parent=item_names.SWARM_HOST),
    item_names.SWARM_HOST_RESOURCE_EFFICIENCY:
        ItemData(239 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 9, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing, parent=item_names.SWARM_HOST),
    item_names.ULTRALISK_ANABOLIC_SYNTHESIS:
        ItemData(240 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 10, SC2Race.ZERG, parent=item_names.ULTRALISK),
    item_names.ULTRALISK_CHITINOUS_PLATING:
        ItemData(241 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 11, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ULTRALISK),
    item_names.ULTRALISK_ORGANIC_CARAPACE:
        ItemData(242 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 12, SC2Race.ZERG, parent=item_names.ULTRALISK),
    item_names.ULTRALISK_RESOURCE_EFFICIENCY:
        ItemData(243 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 13, SC2Race.ZERG, parent=item_names.ULTRALISK),
    item_names.DEVOURER_CORROSIVE_SPRAY:
        ItemData(244 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 14, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT),
    item_names.DEVOURER_GAPING_MAW:
        ItemData(245 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 15, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT),
    item_names.DEVOURER_IMPROVED_OSMOSIS:
        ItemData(246 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 16, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT),
    item_names.DEVOURER_PRESCIENT_SPORES:
        ItemData(247 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 17, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT,
                 classification=ItemClassification.progression),
    item_names.GUARDIAN_PROLONGED_DISPERSION:
        ItemData(248 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 18, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT),
    item_names.GUARDIAN_PRIMAL_ADAPTATION:
        ItemData(249 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 19, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT,
                 classification=ItemClassification.progression),
    item_names.GUARDIAN_SORONAN_ACID:
        ItemData(250 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 20, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT),
    item_names.IMPALER_ADAPTIVE_TALONS:
        ItemData(251 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 21, SC2Race.ZERG,
                 parent=item_names.HYDRALISK_IMPALER_ASPECT),
    item_names.IMPALER_SECRETION_GLANDS:
        ItemData(252 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 22, SC2Race.ZERG,
                 parent=item_names.HYDRALISK_IMPALER_ASPECT),
    item_names.IMPALER_SUNKEN_SPINES:
        ItemData(253 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 23, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=item_names.HYDRALISK_IMPALER_ASPECT),
    item_names.LURKER_SEISMIC_SPINES:
        ItemData(254 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 24, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=item_names.HYDRALISK_LURKER_ASPECT),
    item_names.LURKER_ADAPTED_SPINES:
        ItemData(255 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 25, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=item_names.HYDRALISK_LURKER_ASPECT),
    item_names.RAVAGER_POTENT_BILE:
        ItemData(256 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 26, SC2Race.ZERG,
                 parent=item_names.ROACH_RAVAGER_ASPECT),
    item_names.RAVAGER_BLOATED_BILE_DUCTS:
        ItemData(257 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 27, SC2Race.ZERG,
                 parent=item_names.ROACH_RAVAGER_ASPECT),
    item_names.RAVAGER_DEEP_TUNNEL:
        ItemData(258 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 28, SC2Race.ZERG,
                 classification=ItemClassification.progression_skip_balancing, parent=item_names.ROACH_RAVAGER_ASPECT),
    item_names.VIPER_PARASITIC_BOMB:
        ItemData(259 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_2, 29, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT,
                 classification=ItemClassification.progression),
    item_names.VIPER_PARALYTIC_BARBS:
        ItemData(260 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 0, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT),
    item_names.VIPER_VIRULENT_MICROBES:
        ItemData(261 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 1, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT),
    item_names.BROOD_LORD_POROUS_CARTILAGE:
        ItemData(262 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 2, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT),
    item_names.BROOD_LORD_BEHEMOTH_STELLARSKIN:
        ItemData(263 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 3, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT),
    item_names.BROOD_LORD_SPLITTER_MITOSIS:
        ItemData(264 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 4, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT),
    item_names.BROOD_LORD_RESOURCE_EFFICIENCY:
        ItemData(265 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 5, SC2Race.ZERG,
                 parent=item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT),
    item_names.INFESTOR_INFESTED_TERRAN:
        ItemData(266 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 6, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.INFESTOR),
    item_names.INFESTOR_MICROBIAL_SHROUD:
        ItemData(267 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 7, SC2Race.ZERG, parent=item_names.INFESTOR),
    item_names.SWARM_QUEEN_SPAWN_LARVAE:
        ItemData(268 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 8, SC2Race.ZERG, parent=item_names.SWARM_QUEEN),
    item_names.SWARM_QUEEN_DEEP_TUNNEL:
        ItemData(269 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 9, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing, parent=item_names.SWARM_QUEEN),
    item_names.SWARM_QUEEN_ORGANIC_CARAPACE:
        ItemData(270 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 10, SC2Race.ZERG, parent=item_names.SWARM_QUEEN),
    item_names.SWARM_QUEEN_BIO_MECHANICAL_TRANSFUSION:
        ItemData(271 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 11, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.SWARM_QUEEN),
    item_names.SWARM_QUEEN_RESOURCE_EFFICIENCY:
        ItemData(272 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 12, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.SWARM_QUEEN),
    item_names.SWARM_QUEEN_INCUBATOR_CHAMBER:
        ItemData(273 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 13, SC2Race.ZERG, parent=item_names.SWARM_QUEEN),
    item_names.BROOD_QUEEN_FUNGAL_GROWTH:
        ItemData(274 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 14, SC2Race.ZERG, parent=item_names.BROOD_QUEEN),
    item_names.BROOD_QUEEN_ENSNARE:
        ItemData(275 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 15, SC2Race.ZERG, parent=item_names.BROOD_QUEEN),
    item_names.BROOD_QUEEN_ENHANCED_MITOCHONDRIA:
        ItemData(276 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 16, SC2Race.ZERG, parent=item_names.BROOD_QUEEN),
    item_names.DEFILER_PATHOGEN_PROJECTORS:
        ItemData(277 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 17, SC2Race.ZERG, parent=item_names.DEFILER),
    item_names.DEFILER_TRAPDOOR_ADAPTATION:
        ItemData(278 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 18, SC2Race.ZERG, parent=item_names.DEFILER),
    item_names.DEFILER_PREDATORY_CONSUMPTION:
        ItemData(279 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 19, SC2Race.ZERG, parent=item_names.DEFILER),
    item_names.DEFILER_COMORBIDITY:
        ItemData(280 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 20, SC2Race.ZERG, parent=item_names.DEFILER),
    item_names.ABERRATION_MONSTROUS_RESILIENCE:
        ItemData(281 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 21, SC2Race.ZERG, parent=item_names.ABERRATION),
    item_names.ABERRATION_CONSTRUCT_REGENERATION:
        ItemData(282 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 22, SC2Race.ZERG, parent=item_names.ABERRATION),
    item_names.ABERRATION_BANELING_INCUBATION:
        ItemData(283 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 23, SC2Race.ZERG, parent=item_names.ABERRATION),
    item_names.ABERRATION_PROTECTIVE_COVER:
        ItemData(284 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 24, SC2Race.ZERG, parent=item_names.ABERRATION),
    item_names.ABERRATION_RESOURCE_EFFICIENCY:
        ItemData(285 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 25, SC2Race.ZERG, parent=item_names.ABERRATION),
    item_names.CORRUPTOR_MONSTROUS_RESILIENCE:
        ItemData(286 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 26, SC2Race.ZERG, parent=item_names.CORRUPTOR),
    item_names.CORRUPTOR_CONSTRUCT_REGENERATION:
        ItemData(287 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 27, SC2Race.ZERG, parent=item_names.CORRUPTOR),
    item_names.CORRUPTOR_SCOURGE_INCUBATION:
        ItemData(288 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 28, SC2Race.ZERG, parent=item_names.CORRUPTOR),
    item_names.CORRUPTOR_RESOURCE_EFFICIENCY:
        ItemData(289 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_3, 29, SC2Race.ZERG, parent=item_names.CORRUPTOR),
    item_names.PRIMAL_IGNITER_CONCENTRATED_FIRE:
        ItemData(290 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 0, SC2Race.ZERG, parent=item_names.ROACH_PRIMAL_IGNITER_ASPECT),
    item_names.PRIMAL_IGNITER_PRIMAL_TENACITY:
        ItemData(291 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 1, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ROACH_PRIMAL_IGNITER_ASPECT),
    item_names.INFESTED_SCV_BUILD_CHARGES:
        ItemData(292 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 2, SC2Race.ZERG, parent=parent_names.INFESTED_UNITS),
    item_names.INFESTED_MARINE_PLAGUED_MUNITIONS:
        ItemData(293 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 3, SC2Race.ZERG, parent=item_names.INFESTED_MARINE),
    item_names.INFESTED_MARINE_RETINAL_AUGMENTATION:
        ItemData(294 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 4, SC2Race.ZERG, parent=item_names.INFESTED_MARINE),
    item_names.INFESTED_BUNKER_CALCIFIED_ARMOR:
        ItemData(295 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 6, SC2Race.ZERG, parent=item_names.INFESTED_BUNKER),
    item_names.INFESTED_BUNKER_REGENERATIVE_PLATING:
        ItemData(296 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 5, SC2Race.ZERG, parent=item_names.INFESTED_BUNKER),
    item_names.INFESTED_BUNKER_ENGORGED_BUNKERS:
        ItemData(297 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 7, SC2Race.ZERG, parent=item_names.INFESTED_BUNKER),
    item_names.INFESTED_MISSILE_TURRET_BIOELECTRIC_PAYLOAD:
        ItemData(298 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 6, SC2Race.ZERG, parent=item_names.INFESTED_MISSILE_TURRET),
    item_names.INFESTED_MISSILE_TURRET_ACID_SPORE_VENTS:
        ItemData(299 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 7, SC2Race.ZERG, parent=item_names.INFESTED_MISSILE_TURRET),

    item_names.ZERGLING_RAPTOR_STRAIN:
        ItemData(300 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 0, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ZERGLING),
    item_names.ZERGLING_SWARMLING_STRAIN:
        ItemData(301 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 1, SC2Race.ZERG, parent=item_names.ZERGLING),
    item_names.ROACH_VILE_STRAIN:
        ItemData(302 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 2, SC2Race.ZERG, parent=item_names.ROACH),
    item_names.ROACH_CORPSER_STRAIN:
        ItemData(303 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 3, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ROACH),
    item_names.HYDRALISK_IMPALER_ASPECT:
        ItemData(304 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 0, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_HYDRALISK),
    item_names.HYDRALISK_LURKER_ASPECT:
        ItemData(305 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 1, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_HYDRALISK),
    item_names.BANELING_SPLITTER_STRAIN:
        ItemData(306 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 6, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.BANELING_SOURCE),
    item_names.BANELING_HUNTER_STRAIN:
        ItemData(307 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 7, SC2Race.ZERG, parent=parent_names.BANELING_SOURCE),
    item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT:
        ItemData(308 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 2, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_AIR),
    item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT:
        ItemData(309 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 3, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_AIR),
    item_names.SWARM_HOST_CARRION_STRAIN:
        ItemData(310 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 10, SC2Race.ZERG, parent=item_names.SWARM_HOST),
    item_names.SWARM_HOST_CREEPER_STRAIN:
        ItemData(311 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 11, SC2Race.ZERG, parent=item_names.SWARM_HOST),
    item_names.ULTRALISK_NOXIOUS_STRAIN:
        ItemData(312 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 12, SC2Race.ZERG, parent=item_names.ULTRALISK),
    item_names.ULTRALISK_TORRASQUE_STRAIN:
        ItemData(313 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Strain, 13, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ULTRALISK),

    item_names.TYRANNOZOR_TYRANTS_PROTECTION:
        ItemData(350 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 8, SC2Race.ZERG, parent=item_names.ULTRALISK_TYRANNOZOR_ASPECT),
    item_names.TYRANNOZOR_BARRAGE_OF_SPIKES:
        ItemData(351 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 9, SC2Race.ZERG, parent=item_names.ULTRALISK_TYRANNOZOR_ASPECT),
    item_names.TYRANNOZOR_IMPALING_STRIKE:
        ItemData(352 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 10, SC2Race.ZERG, parent=item_names.ULTRALISK_TYRANNOZOR_ASPECT),
    item_names.TYRANNOZOR_HEALING_ADAPTATION:
        ItemData(353 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 11, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ULTRALISK_TYRANNOZOR_ASPECT),
    item_names.NYDUS_WORM_ECHIDNA_WORM_SUBTERRANEAN_SCALES:
        ItemData(354 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 12, SC2Race.ZERG, parent=parent_names.ANY_NYDUS_WORM),
    item_names.NYDUS_WORM_ECHIDNA_WORM_JORMUNGANDR_STRAIN:
        ItemData(355 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 13, SC2Race.ZERG, parent=parent_names.ANY_NYDUS_WORM),
    item_names.NYDUS_WORM_ECHIDNA_WORM_RESOURCE_EFFICIENCY:
        ItemData(356 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 14, SC2Race.ZERG, parent=parent_names.ANY_NYDUS_WORM),
    item_names.ECHIDNA_WORM_OUROBOROS_STRAIN:
        ItemData(357 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 15, SC2Race.ZERG, parent=parent_names.ZERG_OUROBOUROS_CONDITION),
    item_names.NYDUS_WORM_RAVENOUS_APPETITE:
        ItemData(358 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 16, SC2Race.ZERG, parent=item_names.NYDUS_WORM),
    item_names.INFESTED_SIEGE_TANK_PROGRESSIVE_AUTOMATED_MITOSIS:
        ItemData(359 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Progressive, 0, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=item_names.INFESTED_SIEGE_TANK, quantity=2),
    item_names.INFESTED_SIEGE_TANK_ACIDIC_ENZYMES:
        ItemData(360 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 17, SC2Race.ZERG, parent=item_names.INFESTED_SIEGE_TANK),
    item_names.INFESTED_SIEGE_TANK_DEEP_TUNNEL:
        ItemData(361 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 18, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing, parent=item_names.INFESTED_SIEGE_TANK),
    item_names.INFESTED_DIAMONDBACK_CAUSTIC_MUCUS:
        ItemData(362 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 19, SC2Race.ZERG, parent=item_names.INFESTED_DIAMONDBACK),
    item_names.INFESTED_DIAMONDBACK_VIOLENT_ENZYMES:
        ItemData(363 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 20, SC2Race.ZERG, parent=item_names.INFESTED_DIAMONDBACK),
    item_names.INFESTED_BANSHEE_BRACED_EXOSKELETON:
        ItemData(364 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 21, SC2Race.ZERG, parent=item_names.INFESTED_BANSHEE),
    item_names.INFESTED_BANSHEE_RAPID_HIBERNATION:
        ItemData(365 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 22, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.INFESTED_BANSHEE),
    item_names.INFESTED_LIBERATOR_CLOUD_DISPERSAL:
        ItemData(366 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 23, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.INFESTED_LIBERATOR),
    item_names.INFESTED_LIBERATOR_VIRAL_CONTAMINATION:
        ItemData(367 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 24, SC2Race.ZERG, parent=item_names.INFESTED_LIBERATOR),
    item_names.GUARDIAN_PROPELLANT_SACS:
        ItemData(368 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 25, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT),
    item_names.GUARDIAN_EXPLOSIVE_SPORES:
        ItemData(369 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 26, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT),
    item_names.GUARDIAN_PRIMORDIAL_FURY:
        ItemData(370 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 27, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT),
    item_names.INFESTED_SIEGE_TANK_SEISMIC_SONAR:
        ItemData(371 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 28, SC2Race.ZERG, parent=item_names.INFESTED_SIEGE_TANK),
    item_names.INFESTED_BANSHEE_FLESHFUSED_TARGETING_OPTICS:
        ItemData(372 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_4, 29, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.INFESTED_BANSHEE),
    item_names.INFESTED_SIEGE_TANK_BALANCED_ROOTS:
        ItemData(373 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 0, SC2Race.ZERG, parent=item_names.INFESTED_SIEGE_TANK),
    item_names.INFESTED_DIAMONDBACK_PROGRESSIVE_FUNGAL_SNARE:
        ItemData(374 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Progressive, 2, SC2Race.ZERG,
                 classification=ItemClassification.progression, parent=item_names.INFESTED_DIAMONDBACK, quantity=2),
    item_names.INFESTED_DIAMONDBACK_CONCENTRATED_SPEW:
        ItemData(375 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 1, SC2Race.ZERG, parent=item_names.INFESTED_DIAMONDBACK),
    item_names.INFESTED_SIEGE_TANK_FRIGHTFUL_FLESHWELDER:
        ItemData(376 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 2, SC2Race.ZERG, parent=item_names.INFESTED_SIEGE_TANK),
    item_names.INFESTED_DIAMONDBACK_FRIGHTFUL_FLESHWELDER:
        ItemData(377 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 3, SC2Race.ZERG, parent=item_names.INFESTED_DIAMONDBACK),
    item_names.INFESTED_BANSHEE_FRIGHTFUL_FLESHWELDER:
        ItemData(378 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 4, SC2Race.ZERG, parent=item_names.INFESTED_BANSHEE),
    item_names.INFESTED_LIBERATOR_FRIGHTFUL_FLESHWELDER:
        ItemData(379 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 5, SC2Race.ZERG, parent=item_names.INFESTED_LIBERATOR),
    item_names.INFESTED_LIBERATOR_DEFENDER_MODE:
        ItemData(380 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 8, SC2Race.ZERG, parent=item_names.INFESTED_LIBERATOR,
                 classification=ItemClassification.progression),
    item_names.ABERRATION_PROGRESSIVE_BANELING_LAUNCH:
        ItemData(381 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Progressive, 4, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.ABERRATION, quantity=2),
    item_names.PYGALISK_STIM:
        ItemData(382 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 9, SC2Race.ZERG, parent=item_names.PYGALISK),
    item_names.PYGALISK_DUCAL_BLADES:
        ItemData(383 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 10, SC2Race.ZERG, parent=item_names.PYGALISK),
    item_names.PYGALISK_COMBAT_CARAPACE:
        ItemData(384 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 11, SC2Race.ZERG, parent=item_names.PYGALISK),
    item_names.BILE_LAUNCHER_ARTILLERY_DUCTS:
        ItemData(385 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 12, SC2Race.ZERG, parent=item_names.BILE_LAUNCHER),
    item_names.BILE_LAUNCHER_RAPID_BOMBARMENT:
        ItemData(386 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 13, SC2Race.ZERG, classification=ItemClassification.progression, parent=item_names.BILE_LAUNCHER),
    item_names.BULLFROG_WILD_MUTATION:
        ItemData(387 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 14, SC2Race.ZERG, parent=item_names.BULLFROG),
    item_names.BULLFROG_BROODLINGS:
        ItemData(388 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 15, SC2Race.ZERG, parent=item_names.BULLFROG),
    item_names.BULLFROG_HARD_IMPACT:
        ItemData(389 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 16, SC2Race.ZERG, parent=item_names.BULLFROG),
    item_names.BULLFROG_RANGE:
        ItemData(390 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 17, SC2Race.ZERG, parent=item_names.BULLFROG),
    item_names.SPORE_CRAWLER_BIO_BONUS: 
        ItemData(391 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mutation_5, 18, SC2Race.ZERG, parent=item_names.SPORE_CRAWLER),

    item_names.KERRIGAN_KINETIC_BLAST: ItemData(400 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 0, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_HEROIC_FORTITUDE: ItemData(401 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 1, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEAPING_STRIKE: ItemData(402 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 2, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_CRUSHING_GRIP: ItemData(403 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 3, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_CHAIN_REACTION: ItemData(404 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 4, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_PSIONIC_SHIFT: ItemData(405 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 5, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.ZERGLING_RECONSTITUTION: ItemData(406 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 0, SC2Race.ZERG, parent=item_names.ZERGLING),
    item_names.OVERLORD_IMPROVED_OVERLORDS: ItemData(407 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 1, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.AUTOMATED_EXTRACTORS: ItemData(408 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 2, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_WILD_MUTATION: ItemData(409 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 6, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_SPAWN_BANELINGS: ItemData(410 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 7, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_MEND: ItemData(411 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 8, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.TWIN_DRONES: ItemData(412 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 3, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.MALIGNANT_CREEP: ItemData(413 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 4, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.VESPENE_EFFICIENCY: ItemData(414 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 5, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_INFEST_BROODLINGS: ItemData(415 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 9, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_FURY: ItemData(416 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 10, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_ABILITY_EFFICIENCY: ItemData(417 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 11, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_APOCALYPSE: ItemData(418 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 12, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_SPAWN_LEVIATHAN: ItemData(419 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 13, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.KERRIGAN_DROP_PODS: ItemData(420 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 14, SC2Race.ZERG, classification=ItemClassification.progression),
    # Handled separately from other abilities
    item_names.KERRIGAN_PRIMAL_FORM: ItemData(421 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Primal_Form, 0, SC2Race.ZERG),
    item_names.KERRIGAN_ASSIMILATION_AURA: ItemData(422 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 15, SC2Race.ZERG),
    item_names.KERRIGAN_IMMOBILIZATION_WAVE: ItemData(423 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Ability, 16, SC2Race.ZERG, classification=ItemClassification.progression),

    item_names.KERRIGAN_LEVELS_10: ItemData(500 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 10, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEVELS_9: ItemData(501 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 9, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEVELS_8: ItemData(502 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 8, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEVELS_7: ItemData(503 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 7, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEVELS_6: ItemData(504 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 6, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEVELS_5: ItemData(505 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 5, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEVELS_4: ItemData(506 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 4, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression_skip_balancing),
    item_names.KERRIGAN_LEVELS_3: ItemData(507 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 3, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression_skip_balancing),
    item_names.KERRIGAN_LEVELS_2: ItemData(508 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 2, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression_skip_balancing),
    item_names.KERRIGAN_LEVELS_1: ItemData(509 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 1, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression_skip_balancing),
    item_names.KERRIGAN_LEVELS_14: ItemData(510 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 14, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEVELS_35: ItemData(511 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 35, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),
    item_names.KERRIGAN_LEVELS_70: ItemData(512 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Level, 70, SC2Race.ZERG, quantity=0, classification=ItemClassification.progression),

    # Zerg Mercs
    item_names.INFESTED_MEDICS: ItemData(600 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 0, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.INFESTED_SIEGE_BREAKERS: ItemData(601 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 1, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.INFESTED_DUSK_WINGS: ItemData(602 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 2, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.DEVOURING_ONES: ItemData(603 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 3, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.HUNTER_KILLERS: ItemData(604 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 4, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.TORRASQUE_MERC: ItemData(605 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 5, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.HUNTERLING: ItemData(606 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 6, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.YGGDRASIL: ItemData(607 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 7, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.CAUSTIC_HORRORS: ItemData(608 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Mercenary, 8, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),


    # Misc Upgrades
    item_names.OVERLORD_VENTRAL_SACS: ItemData(700 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 6, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.OVERLORD_GENERATE_CREEP: ItemData(701 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 7, SC2Race.ZERG, classification=ItemClassification.progression_skip_balancing),
    item_names.OVERLORD_ANTENNAE: ItemData(702 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 8, SC2Race.ZERG),
    item_names.OVERLORD_PNEUMATIZED_CARAPACE: ItemData(703 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 9, SC2Race.ZERG),
    item_names.ZERG_EXCAVATING_CLAWS: ItemData(704 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 11, SC2Race.ZERG, parent=parent_names.ZERG_UPROOTABLE_BUILDINGS),
    item_names.ZERG_CREEP_STOMACH: ItemData(705 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 10, SC2Race.ZERG),
    item_names.HIVE_CLUSTER_MATURATION: ItemData(706 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 12, SC2Race.ZERG),
    item_names.MACROSCOPIC_RECUPERATION: ItemData(707 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 13, SC2Race.ZERG),
    item_names.BIOMECHANICAL_STOCKPILING: ItemData(708 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 14, SC2Race.ZERG, parent=parent_names.INFESTED_FACTORY_OR_STARPORT),
    item_names.BROODLING_SPORE_SATURATION: ItemData(709 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 15, SC2Race.ZERG),
    item_names.CELL_DIVISION: ItemData(710 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 16, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.ZERG_MERCENARIES),
    item_names.SELF_SUFFICIENT: ItemData(711 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 17, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.ZERG_MERCENARIES),
    item_names.UNRESTRICTED_MUTATION: ItemData(712 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 18, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.ZERG_MERCENARIES),
    item_names.EVOLUTIONARY_LEAP: ItemData(713 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Evolution_Pit, 19, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.ZERG_MERCENARIES),

    # Morphs
    item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT: ItemData(800 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 6, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_AIR),
    item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT: ItemData(801 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 7, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_AIR),
    item_names.ROACH_RAVAGER_ASPECT: ItemData(802 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 8, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_ROACH),
    item_names.OVERLORD_OVERSEER_ASPECT: ItemData(803 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 4, SC2Race.ZERG, classification=ItemClassification.progression),
    item_names.ROACH_PRIMAL_IGNITER_ASPECT: ItemData(804 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 9, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_ROACH),
    item_names.ULTRALISK_TYRANNOZOR_ASPECT: ItemData(805 + SC2HOTS_ITEM_ID_OFFSET, ZergItemType.Morph, 10, SC2Race.ZERG, classification=ItemClassification.progression, parent=parent_names.MORPH_SOURCE_ULTRALISK),

    # Protoss Units
    # The first several are in SC2WOL offset for historical reasons (show up in prophecy)
    item_names.ZEALOT:
        ItemData(700 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 0, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.STALKER: 
        ItemData(701 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 1, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression),
    item_names.HIGH_TEMPLAR: 
        ItemData(702 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 2, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression),
    item_names.DARK_TEMPLAR: 
        ItemData(703 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 3, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression),
    item_names.IMMORTAL: 
        ItemData(704 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 4, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.COLOSSUS:
        ItemData(705 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 5, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.PHOENIX:
        ItemData(706 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 6, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.VOID_RAY:
        ItemData(707 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 7, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.CARRIER:
        ItemData(708 + SC2WOL_ITEM_ID_OFFSET, ProtossItemType.Unit, 8, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.OBSERVER:
        ItemData(0 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 9, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.CENTURION:
        ItemData(1 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 10, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.SENTINEL:
        ItemData(2 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 11, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.SUPPLICANT:
        ItemData(3 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 12, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.INSTIGATOR:
        ItemData(4 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 13, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.SLAYER:
        ItemData(5 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 14, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.SENTRY:
        ItemData(6 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 15, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.ENERGIZER:
        ItemData(7 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 16, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.HAVOC:
        ItemData(8 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 17, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.SIGNIFIER:
        ItemData(9 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 18, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.ASCENDANT:
        ItemData(10 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 19, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.AVENGER:
        ItemData(11 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 20, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.BLOOD_HUNTER:
        ItemData(12 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 21, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.DRAGOON:
        ItemData(13 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 22, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.DARK_ARCHON:
        ItemData(14 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 23, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.ADEPT:
        ItemData(15 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 24, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.WARP_PRISM:
        ItemData(16 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 25, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.ANNIHILATOR:
        ItemData(17 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 26, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.VANGUARD:
        ItemData(18 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 27, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.WRATHWALKER:
        ItemData(19 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 28, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.REAVER:
        ItemData(20 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit, 29, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.DISRUPTOR:
        ItemData(21 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 0, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.MIRAGE:
        ItemData(22 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 1, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.CORSAIR:
        ItemData(23 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 2, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.DESTROYER:
        ItemData(24 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 3, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.SCOUT:
        ItemData(25 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 4, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.TEMPEST:
        ItemData(26 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 5, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.MOTHERSHIP:
        ItemData(27 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 6, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.ARBITER:
        ItemData(28 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 7, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.ORACLE:
        ItemData(29 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 8, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.STALWART:
        ItemData(30 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 9, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.PULSAR:
        ItemData(31 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 10, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.DAWNBRINGER:
        ItemData(32 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 11, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.SKYLORD:
        ItemData(33 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 12, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.TRIREME:
        ItemData(34 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 13, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.SKIRMISHER:
        ItemData(35 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 14, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    # 36, 37 reserved for Mothership
    item_names.OPPRESSOR:
        ItemData(38 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 17, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.CALADRIUS:
        ItemData(39 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 18, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.MISTWING:
        ItemData(40 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Unit_2, 19, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),

    # Protoss Upgrades
    item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON: ItemData(100 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, 0, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR: ItemData(101 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, 4, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_PROTOSS_SHIELDS: ItemData(102 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, 8, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON: ItemData(103 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, 12, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR: ItemData(104 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, 16, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    # Bundles
    item_names.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE: ItemData(105 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, -1, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE: ItemData(106 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, -1, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE: ItemData(107 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, -1, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE: ItemData(108 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, -1, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),
    item_names.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE: ItemData(109 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Upgrade, -1, SC2Race.PROTOSS, classification=ItemClassification.progression, quantity=WEAPON_ARMOR_UPGRADE_MAX_LEVEL),

    # Protoss Buildings
    item_names.PHOTON_CANNON: ItemData(200 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Building, 0, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.KHAYDARIN_MONOLITH: ItemData(201 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Building, 1, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SHIELD_BATTERY: ItemData(202 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Building, 2, SC2Race.PROTOSS, classification=ItemClassification.progression),

    # Protoss Unit Upgrades
    item_names.SUPPLICANT_BLOOD_SHIELD: ItemData(300 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 0, SC2Race.PROTOSS, parent=item_names.SUPPLICANT),
    item_names.SUPPLICANT_SOUL_AUGMENTATION: ItemData(301 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 1, SC2Race.PROTOSS, parent=item_names.SUPPLICANT),
    item_names.SUPPLICANT_ENDLESS_SERVITUDE: ItemData(302 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 2, SC2Race.PROTOSS, parent=item_names.SUPPLICANT),
    item_names.ADEPT_SHOCKWAVE: ItemData(303 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 3, SC2Race.PROTOSS, parent=item_names.ADEPT),
    item_names.ADEPT_RESONATING_GLAIVES: ItemData(304 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 4, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.ADEPT),
    item_names.ADEPT_PHASE_BULWARK: ItemData(305 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 5, SC2Race.PROTOSS, parent=item_names.ADEPT),
    item_names.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES: ItemData(306 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 6, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.STALKER_CLASS),
    item_names.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION: ItemData(307 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 7, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.STALKER_CLASS),
    item_names.DRAGOON_CONCENTRATED_ANTIMATTER: ItemData(308 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 8, SC2Race.PROTOSS, parent=item_names.DRAGOON),
    item_names.DRAGOON_TRILLIC_COMPRESSION_SYSTEM: ItemData(309 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 9, SC2Race.PROTOSS, parent=item_names.DRAGOON),
    item_names.DRAGOON_SINGULARITY_CHARGE: ItemData(310 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 10, SC2Race.PROTOSS, parent=item_names.DRAGOON),
    item_names.DRAGOON_ENHANCED_STRIDER_SERVOS: ItemData(311 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 11, SC2Race.PROTOSS, parent=item_names.DRAGOON),
    item_names.SCOUT_COMBAT_SENSOR_ARRAY: ItemData(312 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 12, SC2Race.PROTOSS, parent=parent_names.SCOUT_CLASS),
    item_names.SCOUT_APIAL_SENSORS: ItemData(313 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 13, SC2Race.PROTOSS, parent=item_names.SCOUT),
    item_names.SCOUT_GRAVITIC_THRUSTERS: ItemData(314 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 14, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.SCOUT_CLASS),
    item_names.SCOUT_ADVANCED_PHOTON_BLASTERS: ItemData(315 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 15, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.SCOUT_OR_OPPRESSOR_OR_MISTWING),
    item_names.TEMPEST_TECTONIC_DESTABILIZERS: ItemData(316 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 16, SC2Race.PROTOSS, parent=item_names.TEMPEST),
    item_names.TEMPEST_QUANTIC_REACTOR: ItemData(317 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 17, SC2Race.PROTOSS, parent=item_names.TEMPEST),
    item_names.TEMPEST_GRAVITY_SLING: ItemData(318 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 18, SC2Race.PROTOSS, parent=item_names.TEMPEST),
    item_names.PHOENIX_CLASS_IONIC_WAVELENGTH_FLUX: ItemData(319 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 19, SC2Race.PROTOSS, parent=parent_names.PHOENIX_CLASS),
    item_names.PHOENIX_CLASS_ANION_PULSE_CRYSTALS: ItemData(320 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 20, SC2Race.PROTOSS, parent=parent_names.PHOENIX_CLASS),
    item_names.CORSAIR_STEALTH_DRIVE: ItemData(321 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 21, SC2Race.PROTOSS, parent=item_names.CORSAIR),
    item_names.CORSAIR_ARGUS_JEWEL: ItemData(322 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 22, SC2Race.PROTOSS, parent=item_names.CORSAIR),
    item_names.CORSAIR_SUSTAINING_DISRUPTION: ItemData(323 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 23, SC2Race.PROTOSS, parent=item_names.CORSAIR),
    item_names.CORSAIR_NEUTRON_SHIELDS: ItemData(324 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 24, SC2Race.PROTOSS, parent=item_names.CORSAIR),
    item_names.ORACLE_STEALTH_DRIVE: ItemData(325 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 25, SC2Race.PROTOSS, parent=item_names.ORACLE),
    item_names.ORACLE_SKYWARD_CHRONOANOMALY: ItemData(544 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 26, SC2Race.PROTOSS, parent=item_names.ORACLE),
    item_names.ORACLE_TEMPORAL_ACCELERATION_BEAM: ItemData(327 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 27, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.ORACLE),
    item_names.ARBITER_CHRONOSTATIC_REINFORCEMENT: ItemData(328 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 28, SC2Race.PROTOSS, parent=item_names.ARBITER),
    item_names.ARBITER_KHAYDARIN_CORE: ItemData(329 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_1, 29, SC2Race.PROTOSS, parent=item_names.ARBITER),
    item_names.ARBITER_SPACETIME_ANCHOR: ItemData(330 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 0, SC2Race.PROTOSS, parent=item_names.ARBITER),
    item_names.ARBITER_RESOURCE_EFFICIENCY: ItemData(331 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 1, SC2Race.PROTOSS, parent=item_names.ARBITER),
    item_names.ARBITER_JUDICATORS_VEIL: ItemData(332 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 2, SC2Race.PROTOSS, parent=item_names.ARBITER),
    item_names.CARRIER_TRIREME_GRAVITON_CATAPULT:
        ItemData(333 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 3, SC2Race.PROTOSS, parent=parent_names.CARRIER_OR_TRIREME),
    item_names.CARRIER_SKYLORD_TRIREME_HULL_OF_PAST_GLORIES:
        ItemData(334 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 4, SC2Race.PROTOSS, parent=parent_names.CARRIER_CLASS),
    item_names.VOID_RAY_DESTROYER_PULSAR_DAWNBRINGER_FLUX_VANES:
        ItemData(335 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 5, SC2Race.PROTOSS, parent=parent_names.VOID_RAY_CLASS),
    item_names.DESTROYER_RESOURCE_EFFICIENCY: ItemData(535 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 6, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.DESTROYER),
    item_names.WARP_PRISM_GRAVITIC_DRIVE:
        ItemData(337 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 7, SC2Race.PROTOSS, parent=item_names.WARP_PRISM),
    item_names.WARP_PRISM_PHASE_BLASTER:
        ItemData(338 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 8, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, parent=item_names.WARP_PRISM),
    item_names.WARP_PRISM_WAR_CONFIGURATION: ItemData(339 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 9, SC2Race.PROTOSS, parent=item_names.WARP_PRISM),
    item_names.OBSERVER_GRAVITIC_BOOSTERS: ItemData(340 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 10, SC2Race.PROTOSS, parent=item_names.OBSERVER),
    item_names.OBSERVER_SENSOR_ARRAY: ItemData(341 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 11, SC2Race.PROTOSS, parent=item_names.OBSERVER),
    item_names.REAVER_SCARAB_DAMAGE: ItemData(342 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 12, SC2Race.PROTOSS, parent=item_names.REAVER),
    item_names.REAVER_SOLARITE_PAYLOAD: ItemData(343 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 13, SC2Race.PROTOSS, parent=item_names.REAVER),
    item_names.REAVER_REAVER_CAPACITY: ItemData(344 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 14, SC2Race.PROTOSS, parent=item_names.REAVER),
    item_names.REAVER_RESOURCE_EFFICIENCY: ItemData(345 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 15, SC2Race.PROTOSS, parent=item_names.REAVER),
    item_names.VANGUARD_AGONY_LAUNCHERS: ItemData(346 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 16, SC2Race.PROTOSS, parent=item_names.VANGUARD),
    item_names.VANGUARD_MATTER_DISPERSION: ItemData(347 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 17, SC2Race.PROTOSS, parent=item_names.VANGUARD),
    item_names.IMMORTAL_ANNIHILATOR_SINGULARITY_CHARGE: ItemData(348 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 18, SC2Race.PROTOSS, parent=parent_names.IMMORTAL_OR_ANNIHILATOR),
    item_names.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING: ItemData(349 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 19, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.IMMORTAL_OR_ANNIHILATOR),
    item_names.COLOSSUS_PACIFICATION_PROTOCOL: ItemData(350 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 20, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.COLOSSUS),
    item_names.WRATHWALKER_RAPID_POWER_CYCLING: ItemData(351 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 21, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.WRATHWALKER),
    item_names.WRATHWALKER_EYE_OF_WRATH: ItemData(352 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 22, SC2Race.PROTOSS, parent=item_names.WRATHWALKER),
    item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHROUD_OF_ADUN: ItemData(353 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 23, SC2Race.PROTOSS, parent=parent_names.DARK_TEMPLAR_CLASS),
    item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHADOW_GUARD_TRAINING: ItemData(354 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 24, SC2Race.PROTOSS, parent=parent_names.DARK_TEMPLAR_CLASS),
    item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_BLINK: ItemData(355 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 25, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.DARK_TEMPLAR_CLASS),
    item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_RESOURCE_EFFICIENCY: ItemData(356 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 26, SC2Race.PROTOSS, parent=parent_names.DARK_TEMPLAR_CLASS),
    item_names.DARK_TEMPLAR_DARK_ARCHON_MELD: ItemData(357 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 27, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.DARK_TEMPLAR),
    item_names.HIGH_TEMPLAR_SIGNIFIER_UNSHACKLED_PSIONIC_STORM: ItemData(358 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 28, SC2Race.PROTOSS, parent=parent_names.STORM_CASTER),
    item_names.HIGH_TEMPLAR_SIGNIFIER_HALLUCINATION: ItemData(359 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_2, 29, SC2Race.PROTOSS, parent=parent_names.STORM_CASTER),
    item_names.HIGH_TEMPLAR_SIGNIFIER_KHAYDARIN_AMULET: ItemData(360 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 0, SC2Race.PROTOSS, parent=parent_names.STORM_CASTER),
    item_names.ARCHON_HIGH_ARCHON: ItemData(361 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 1, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.ARCHON_SOURCE),
    item_names.DARK_ARCHON_FEEDBACK: ItemData(362 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 2, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.DARK_ARCHON_SOURCE),
    item_names.DARK_ARCHON_MAELSTROM: ItemData(363 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 3, SC2Race.PROTOSS, parent=parent_names.DARK_ARCHON_SOURCE),
    item_names.DARK_ARCHON_ARGUS_TALISMAN: ItemData(364 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 4, SC2Race.PROTOSS, parent=parent_names.DARK_ARCHON_SOURCE),
    item_names.ASCENDANT_POWER_OVERWHELMING: ItemData(365 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 5, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=parent_names.SUPPLICANT_AND_ASCENDANT),
    item_names.ASCENDANT_CHAOTIC_ATTUNEMENT: ItemData(366 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 6, SC2Race.PROTOSS, parent=item_names.ASCENDANT),
    item_names.ASCENDANT_BLOOD_AMULET: ItemData(367 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 7, SC2Race.PROTOSS, parent=item_names.ASCENDANT),
    item_names.SENTRY_ENERGIZER_HAVOC_CLOAKING_MODULE: ItemData(368 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 8, SC2Race.PROTOSS, parent=parent_names.SENTRY_CLASS),
    item_names.SENTRY_ENERGIZER_HAVOC_SHIELD_BATTERY_RAPID_RECHARGING: ItemData(369 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 9, SC2Race.PROTOSS, parent=parent_names.SENTRY_CLASS_OR_SHIELD_BATTERY),
    item_names.SENTRY_FORCE_FIELD: ItemData(370 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 10, SC2Race.PROTOSS, parent=item_names.SENTRY),
    item_names.SENTRY_HALLUCINATION: ItemData(371 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 11, SC2Race.PROTOSS, parent=item_names.SENTRY),
    item_names.ENERGIZER_RECLAMATION: ItemData(372 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 12, SC2Race.PROTOSS, parent=item_names.ENERGIZER),
    item_names.ENERGIZER_FORGED_CHASSIS: ItemData(373 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 13, SC2Race.PROTOSS, parent=item_names.ENERGIZER),
    item_names.HAVOC_DETECT_WEAKNESS: ItemData(374 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 14, SC2Race.PROTOSS, parent=item_names.HAVOC),
    item_names.HAVOC_BLOODSHARD_RESONANCE: ItemData(375 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 15, SC2Race.PROTOSS, parent=item_names.HAVOC),
    item_names.ZEALOT_SENTINEL_CENTURION_LEG_ENHANCEMENTS: ItemData(376 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 16, SC2Race.PROTOSS, parent=parent_names.ZEALOT_OR_SENTINEL_OR_CENTURION),
    item_names.ZEALOT_SENTINEL_CENTURION_SHIELD_CAPACITY: ItemData(377 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 17, SC2Race.PROTOSS, classification=ItemClassification.progression_skip_balancing, parent=parent_names.ZEALOT_OR_SENTINEL_OR_CENTURION),
    item_names.ORACLE_BOSONIC_CORE: ItemData(378 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 18, SC2Race.PROTOSS, parent=item_names.ORACLE),
    item_names.SCOUT_RESOURCE_EFFICIENCY: ItemData(379 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 19, SC2Race.PROTOSS, parent=item_names.SCOUT),
    item_names.IMMORTAL_ANNIHILATOR_DISRUPTOR_DISPERSION: ItemData(380 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 20, SC2Race.PROTOSS, parent=parent_names.IMMORTAL_OR_ANNIHILATOR),
    item_names.DISRUPTOR_CLOAKING_MODULE: ItemData(381 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 21, SC2Race.PROTOSS, parent=item_names.DISRUPTOR),
    item_names.DISRUPTOR_PERFECTED_POWER:  ItemData(382 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 22, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.DISRUPTOR),
    item_names.DISRUPTOR_RESTRAINED_DESTRUCTION: ItemData(383 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 23, SC2Race.PROTOSS, parent=item_names.DISRUPTOR),
    item_names.TEMPEST_INTERPLANETARY_RANGE: ItemData(384 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 24, SC2Race.PROTOSS, parent=item_names.TEMPEST),
    item_names.DAWNBRINGER_ANTI_SURFACE_COUNTERMEASURES: ItemData(385 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 25, SC2Race.PROTOSS, parent=item_names.DAWNBRINGER),
    item_names.DAWNBRINGER_ENHANCED_SHIELD_GENERATOR: ItemData(386 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 26, SC2Race.PROTOSS, parent=item_names.DAWNBRINGER),
    item_names.STALWART_HIGH_VOLTAGE_CAPACITORS: ItemData(387 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 27, SC2Race.PROTOSS, parent=item_names.STALWART),
    item_names.STALWART_REINTEGRATED_FRAMEWORK: ItemData(388 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 28, SC2Race.PROTOSS, parent=item_names.STALWART),
    item_names.STALWART_STABILIZED_ELECTRODES: ItemData(389 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_3, 29, SC2Race.PROTOSS, parent=item_names.STALWART),
    item_names.STALWART_LATTICED_SHIELDING: ItemData(390 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 0, SC2Race.PROTOSS, parent=item_names.STALWART),
    item_names.ARCHON_TRANSCENDENCE: ItemData(391 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 1, SC2Race.PROTOSS, parent=parent_names.ARCHON_SOURCE),
    item_names.ARCHON_POWER_SIPHON: ItemData(392 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 2, SC2Race.PROTOSS, parent=parent_names.ARCHON_SOURCE),
    item_names.ARCHON_ERADICATE: ItemData(393 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 3, SC2Race.PROTOSS, parent=parent_names.ARCHON_SOURCE),
    item_names.ARCHON_OBLITERATE: ItemData(394 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 4, SC2Race.PROTOSS, parent=parent_names.ARCHON_SOURCE),
    item_names.SUPPLICANT_ZENITH_PITCH: ItemData(395 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 5, SC2Race.PROTOSS, classification=ItemClassification.progression_skip_balancing, parent=item_names.SUPPLICANT),
    item_names.PULSAR_CHRONOCLYSM: ItemData(396 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 6, SC2Race.PROTOSS, parent=item_names.PULSAR),
    item_names.PULSAR_ENTROPIC_REVERSAL: ItemData(397 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 7, SC2Race.PROTOSS, parent=item_names.PULSAR),
    # 398-407 reserved for Mothership
    item_names.OPPRESSOR_ACCELERATED_WARP: ItemData(408 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 18, SC2Race.PROTOSS, parent=item_names.OPPRESSOR),
    item_names.OPPRESSOR_ARMOR_MELTING_BLASTERS: ItemData(409 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 19, SC2Race.PROTOSS, parent=item_names.OPPRESSOR),
    item_names.CALADRIUS_SIDE_MISSILES: ItemData(410 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 20, SC2Race.PROTOSS, parent=item_names.CALADRIUS),
    item_names.CALADRIUS_STRUCTURE_TARGETING: ItemData(411 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 21, SC2Race.PROTOSS, parent=item_names.CALADRIUS),
    item_names.CALADRIUS_SOLARITE_REACTOR: ItemData(412 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 22, SC2Race.PROTOSS, parent=item_names.CALADRIUS),
    item_names.MISTWING_NULL_SHROUD: ItemData(413 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 23, SC2Race.PROTOSS, parent=item_names.MISTWING),
    item_names.MISTWING_PILOT: ItemData(414 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 24, SC2Race.PROTOSS, classification=ItemClassification.progression_skip_balancing, parent=item_names.MISTWING),
    item_names.INSTIGATOR_BLINK_OVERDRIVE: ItemData(415 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 25, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.INSTIGATOR),
    item_names.INSTIGATOR_RECONSTRUCTION: ItemData(416 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 26, SC2Race.PROTOSS, parent=item_names.INSTIGATOR),
    item_names.DARK_TEMPLAR_ARCHON_MERGE: ItemData(417 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 27, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.DARK_TEMPLAR),
    item_names.ASCENDANT_ARCHON_MERGE: ItemData(418 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 28, SC2Race.PROTOSS, classification=ItemClassification.progression_skip_balancing, parent=item_names.ASCENDANT),
    item_names.SCOUT_SUPPLY_EFFICIENCY: ItemData(419 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_4, 29, SC2Race.PROTOSS, parent=item_names.SCOUT),
    item_names.REAVER_BARGAIN_BIN_PRICES: ItemData(420 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Forge_5, 0, SC2Race.PROTOSS, parent=item_names.REAVER),


    # War Council
    item_names.ZEALOT_WHIRLWIND: ItemData(500 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 0, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.ZEALOT),
    item_names.CENTURION_RESOURCE_EFFICIENCY: ItemData(501 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 1, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.CENTURION),
    item_names.SENTINEL_RESOURCE_EFFICIENCY: ItemData(502 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 2, SC2Race.PROTOSS, parent=item_names.SENTINEL),
    item_names.STALKER_PHASE_REACTOR: ItemData(503 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 3, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.STALKER),
    item_names.DRAGOON_PHALANX_SUIT: ItemData(504 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 4, SC2Race.PROTOSS, parent=item_names.DRAGOON),
    item_names.INSTIGATOR_MODERNIZED_SERVOS: ItemData(505 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 5, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.INSTIGATOR),
    item_names.ADEPT_DISRUPTIVE_TRANSFER: ItemData(506 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 6, SC2Race.PROTOSS, parent=item_names.ADEPT),
    item_names.SLAYER_PHASE_BLINK: ItemData(507 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 7, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.SLAYER),
    item_names.AVENGER_KRYHAS_CLOAK: ItemData(508 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 8, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.AVENGER),
    item_names.DARK_TEMPLAR_LESSER_SHADOW_FURY: ItemData(509 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 9, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.DARK_TEMPLAR),
    item_names.DARK_TEMPLAR_GREATER_SHADOW_FURY: ItemData(510 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 10, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.DARK_TEMPLAR),
    item_names.BLOOD_HUNTER_BRUTAL_EFFICIENCY: ItemData(511 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 11, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.BLOOD_HUNTER),
    item_names.SENTRY_DOUBLE_SHIELD_RECHARGE: ItemData(512 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 12, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.SENTRY),
    item_names.ENERGIZER_MOBILE_CHRONO_BEAM: ItemData(513 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 13, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.ENERGIZER),
    item_names.HAVOC_ENDURING_SIGHT: ItemData(514 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 14, SC2Race.PROTOSS, parent=item_names.HAVOC),
    item_names.HIGH_TEMPLAR_PLASMA_SURGE: ItemData(515 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 15, SC2Race.PROTOSS, parent=item_names.HIGH_TEMPLAR),
    item_names.SIGNIFIER_FEEDBACK: ItemData(516 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 16, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.SIGNIFIER),
    item_names.ASCENDANT_BREATH_OF_CREATION: ItemData(517 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 17, SC2Race.PROTOSS, parent=item_names.ASCENDANT),
    item_names.DARK_ARCHON_INDOMITABLE_WILL: ItemData(518 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 18, SC2Race.PROTOSS, parent=parent_names.DARK_ARCHON_SOURCE),
    item_names.IMMORTAL_IMPROVED_BARRIER: ItemData(519 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 19, SC2Race.PROTOSS, parent=item_names.IMMORTAL),
    item_names.VANGUARD_RAPIDFIRE_CANNON: ItemData(520 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 20, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.VANGUARD),
    item_names.VANGUARD_FUSION_MORTARS: ItemData(521 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 21, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.VANGUARD),
    item_names.ANNIHILATOR_TWILIGHT_CHASSIS: ItemData(522 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 22, SC2Race.PROTOSS, parent=item_names.ANNIHILATOR),
    item_names.STALWART_ARC_INDUCERS: ItemData(523 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 23, SC2Race.PROTOSS, parent=item_names.STALWART),
    item_names.COLOSSUS_FIRE_LANCE: ItemData(524 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 24, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.COLOSSUS),
    item_names.WRATHWALKER_AERIAL_TRACKING: ItemData(525 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 25, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.WRATHWALKER),
    item_names.REAVER_KHALAI_REPLICATORS: ItemData(526 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 26, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.REAVER),
    item_names.DISRUPTOR_MOBILITY_PROTOCOLS: ItemData(527 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 27, SC2Race.PROTOSS, parent=item_names.DISRUPTOR),
    item_names.WARP_PRISM_WARP_REFRACTION: ItemData(528 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 28, SC2Race.PROTOSS, parent=item_names.WARP_PRISM),
    item_names.OBSERVER_INDUCE_SCOPOPHOBIA: ItemData(529 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council, 29, SC2Race.PROTOSS, parent=item_names.OBSERVER),
    item_names.PHOENIX_DOUBLE_GRAVITON_BEAM: ItemData(530 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 0, SC2Race.PROTOSS, parent=item_names.PHOENIX),
    item_names.CORSAIR_NETWORK_DISRUPTION: ItemData(531 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 1, SC2Race.PROTOSS, parent=item_names.CORSAIR),
    item_names.MIRAGE_GRAVITON_BEAM: ItemData(532 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 2, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.MIRAGE),
    item_names.SKIRMISHER_PEER_CONTEMPT: ItemData(533 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 3, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.SKIRMISHER),
    item_names.VOID_RAY_PRISMATIC_RANGE: ItemData(534 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 4, SC2Race.PROTOSS, parent=item_names.VOID_RAY),
    item_names.DESTROYER_REFORGED_BLOODSHARD_CORE: ItemData(336 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 5, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.DESTROYER),
    item_names.PULSAR_CHRONO_SHEAR: ItemData(536 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 6, SC2Race.PROTOSS, parent=item_names.PULSAR),
    item_names.DAWNBRINGER_SOLARITE_LENS: ItemData(537 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 7, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.DAWNBRINGER),
    item_names.CARRIER_REPAIR_DRONES: ItemData(538 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 8, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.CARRIER),
    item_names.SKYLORD_JUMP: ItemData(539 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 9, SC2Race.PROTOSS, parent=item_names.SKYLORD),
    item_names.TRIREME_SOLAR_BEAM: ItemData(540 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 10, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.TRIREME),
    item_names.TEMPEST_DISINTEGRATION: ItemData(541 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 11, SC2Race.PROTOSS, parent=item_names.TEMPEST),
    item_names.SCOUT_EXPEDITIONARY_HULL: ItemData(542 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 12, SC2Race.PROTOSS, parent=item_names.SCOUT),
    item_names.ARBITER_VESSEL_OF_THE_CONCLAVE: ItemData(543 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 13, SC2Race.PROTOSS, parent=item_names.ARBITER),
    item_names.ORACLE_STASIS_CALIBRATION: ItemData(326 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 14, SC2Race.PROTOSS, parent=item_names.ORACLE),
    item_names.MOTHERSHIP_INTEGRATED_POWER: ItemData(545 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 15, SC2Race.PROTOSS, parent=item_names.MOTHERSHIP),
    # 546-549 reserved for Mothership
    item_names.OPPRESSOR_VULCAN_BLASTER: ItemData(550 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 20, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.OPPRESSOR),
    item_names.CALADRIUS_CORONA_BEAM: ItemData(551 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 21, SC2Race.PROTOSS, classification=ItemClassification.progression, parent=item_names.CALADRIUS),
    item_names.MISTWING_PHANTOM_DASH: ItemData(552 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 22, SC2Race.PROTOSS, parent=item_names.MISTWING),
    item_names.SUPPLICANT_SACRIFICE: ItemData(553 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.War_Council_2, 23, SC2Race.PROTOSS, parent=item_names.SUPPLICANT),

    # SoA Calldown powers
    item_names.SOA_CHRONO_SURGE: ItemData(700 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 0, SC2Race.PROTOSS),
    item_names.SOA_PROGRESSIVE_PROXY_PYLON: ItemData(701 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Progressive, 0, SC2Race.PROTOSS, quantity=2, classification=ItemClassification.progression),
    item_names.SOA_PYLON_OVERCHARGE: ItemData(702 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 1, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SOA_ORBITAL_STRIKE: ItemData(703 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 2, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SOA_TEMPORAL_FIELD: ItemData(704 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 3, SC2Race.PROTOSS),
    item_names.SOA_SOLAR_LANCE: ItemData(705 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 4, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SOA_MASS_RECALL: ItemData(706 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 5, SC2Race.PROTOSS),
    item_names.SOA_SHIELD_OVERCHARGE: ItemData(707 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 6, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SOA_DEPLOY_FENIX: ItemData(708 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 7, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SOA_PURIFIER_BEAM: ItemData(709 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 8, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SOA_TIME_STOP: ItemData(710 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 9, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SOA_SOLAR_BOMBARDMENT: ItemData(711 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Spear_Of_Adun, 10, SC2Race.PROTOSS, classification=ItemClassification.progression),

    # Generic Protoss Upgrades
    item_names.MATRIX_OVERLOAD:
        ItemData(800 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 0, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.QUATRO:
        ItemData(801 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 1, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.NEXUS_OVERCHARGE:
        ItemData(802 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 2, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, important_for_filtering=True),
    item_names.ORBITAL_ASSIMILATORS:
        ItemData(803 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 3, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.WARP_HARMONIZATION:
        ItemData(804 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 4, SC2Race.PROTOSS, classification=ItemClassification.progression_skip_balancing),
    item_names.GUARDIAN_SHELL:
        ItemData(805 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 5, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.RECONSTRUCTION_BEAM:
        ItemData(806 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 6, SC2Race.PROTOSS,
                 classification=ItemClassification.progression),
    item_names.OVERWATCH:
        ItemData(807 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 7, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.SUPERIOR_WARP_GATES:
        ItemData(808 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 8, SC2Race.PROTOSS),
    item_names.ENHANCED_TARGETING:
        ItemData(809 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 9, SC2Race.PROTOSS, parent=parent_names.PROTOSS_STATIC_DEFENSE),
    item_names.OPTIMIZED_ORDNANCE:
        ItemData(810 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 10, SC2Race.PROTOSS, parent=parent_names.PROTOSS_ATTACKING_BUILDING),
    item_names.KHALAI_INGENUITY:
        ItemData(811 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 11, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.AMPLIFIED_ASSIMILATORS:
        ItemData(812 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 12, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.PROGRESSIVE_WARP_RELOCATE:
        ItemData(813 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Progressive, 2, SC2Race.PROTOSS, quantity=2,
                 classification=ItemClassification.progression),
    item_names.PROBE_WARPIN:
        ItemData(814 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 13, SC2Race.PROTOSS, classification=ItemClassification.progression),
    item_names.ELDER_PROBES:
        ItemData(815 + SC2LOTV_ITEM_ID_OFFSET, ProtossItemType.Solarite_Core, 14, SC2Race.PROTOSS, classification=ItemClassification.progression),
}

# Add keys to item table
# Mission keys (key offset + 0-999)
# Mission IDs start at 1 so the item IDs are moved down a space
mission_key_item_table = {
    item_names._TEMPLATE_MISSION_KEY.format(mission.mission_name):
        ItemData(mission.id - 1 + SC2_KEY_ITEM_ID_OFFSET, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0)
    for mission in SC2Mission
}
# Numbered layout keys (key offset + 1000 - 1999)
numbered_layout_key_item_table = {
    item_names._TEMPLATE_NUMBERED_LAYOUT_KEY.format(number + 1):
        ItemData(number + SC2_KEY_ITEM_ID_OFFSET + SC2_KEY_ITEM_SECTION_SIZE, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0)
    for number in range(len(SC2Mission))
}
# Numbered campaign keys (key offset + 2000 - 2999)
numbered_campaign_key_item_table = {
    item_names._TEMPLATE_NUMBERED_CAMPAIGN_KEY.format(number + 1):
        ItemData(number + SC2_KEY_ITEM_ID_OFFSET + SC2_KEY_ITEM_SECTION_SIZE * 2, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0)
    for number in range(len(SC2Mission))
}
# Flavor keys (key offset + 3000 - 3999)
flavor_key_item_table = {
    item_names._TEMPLATE_FLAVOR_KEY.format(name):
        ItemData(i + SC2_KEY_ITEM_ID_OFFSET + SC2_KEY_ITEM_SECTION_SIZE * 3, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0)
    for (i, name) in enumerate(item_names._flavor_key_names)
}
# Named layout keys (key offset + 4000 - 4999)
campaign_to_layout_names = get_used_layout_names()
named_layout_key_item_table = {
    item_names._TEMPLATE_NAMED_LAYOUT_KEY.format(layout_name, campaign.campaign_name):
        ItemData(layout_start + i + SC2_KEY_ITEM_ID_OFFSET + SC2_KEY_ITEM_SECTION_SIZE * 4, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0)
    for (campaign, (layout_start, layout_names)) in campaign_to_layout_names.items() for (i, layout_name) in enumerate(layout_names)
}
# Named campaign keys (key offset + 5000 - 5999)
campaign_names = [campaign.campaign_name for campaign in SC2Campaign if campaign != SC2Campaign.GLOBAL]
named_campaign_key_item_table = {
    item_names._TEMPLATE_NAMED_CAMPAIGN_KEY.format(campaign_name):
        ItemData(i + SC2_KEY_ITEM_ID_OFFSET + SC2_KEY_ITEM_SECTION_SIZE * 5, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0)
    for (i, campaign_name) in enumerate(campaign_names)
}
# Numbered progressive keys (key offset + 6000 - 6999)
numbered_progressive_keys = {
    item_names._TEMPLATE_PROGRESSIVE_KEY.format(number + 1):
        ItemData(number + SC2_KEY_ITEM_ID_OFFSET + SC2_KEY_ITEM_SECTION_SIZE * 6, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0)
    for number in range(len(SC2Mission))
}
# Special keys (key offset + 7000 - 7999)
special_keys = {
    item_names.PROGRESSIVE_MISSION_KEY:
        ItemData(0 + SC2_KEY_ITEM_ID_OFFSET + SC2_KEY_ITEM_SECTION_SIZE * 7, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0),
    item_names.PROGRESSIVE_QUESTLINE_KEY:
        ItemData(1 + SC2_KEY_ITEM_ID_OFFSET + SC2_KEY_ITEM_SECTION_SIZE * 7, FactionlessItemType.Keys, 0, SC2Race.ANY,
                 classification=ItemClassification.progression, quantity=0),
}
key_item_table = {}
key_item_table.update(mission_key_item_table)
key_item_table.update(numbered_layout_key_item_table)
key_item_table.update(numbered_campaign_key_item_table)
key_item_table.update(flavor_key_item_table)
key_item_table.update(named_layout_key_item_table)
key_item_table.update(named_campaign_key_item_table)
key_item_table.update(numbered_progressive_keys)
key_item_table.update(special_keys)
item_table.update(key_item_table)

def get_item_table():
    return item_table


basic_units = {
    SC2Race.TERRAN: {
        item_names.MARINE,
        item_names.MARAUDER,
        item_names.DOMINION_TROOPER,
        item_names.GOLIATH,
        item_names.HELLION,
        item_names.VULTURE,
        item_names.WARHOUND,
    },
    SC2Race.ZERG: {
        item_names.SWARM_QUEEN,
        item_names.ROACH,
        item_names.HYDRALISK,
    },
    SC2Race.PROTOSS: {
        item_names.ZEALOT,
        item_names.CENTURION,
        item_names.SENTINEL,
        item_names.STALKER,
        item_names.INSTIGATOR,
        item_names.SLAYER,
        item_names.ADEPT,
    }
}

advanced_basic_units = {
    SC2Race.TERRAN: basic_units[SC2Race.TERRAN].union({
        item_names.REAPER,
        item_names.DIAMONDBACK,
        item_names.VIKING,
        item_names.SIEGE_TANK,
        item_names.BANSHEE,
        item_names.THOR,
        item_names.BATTLECRUISER,
        item_names.CYCLONE
    }),
    SC2Race.ZERG: basic_units[SC2Race.ZERG].union({
        item_names.INFESTED_BANSHEE,
        item_names.INFESTED_DIAMONDBACK,
        item_names.INFESTOR,
        item_names.ABERRATION,
    }),
    SC2Race.PROTOSS: basic_units[SC2Race.PROTOSS].union({
        item_names.DARK_TEMPLAR,
        item_names.DRAGOON,
        item_names.AVENGER,
        item_names.IMMORTAL,
        item_names.ANNIHILATOR,
        item_names.VANGUARD,
        item_names.SKIRMISHER,
    })
}

no_logic_basic_units = {
    SC2Race.TERRAN: advanced_basic_units[SC2Race.TERRAN].union({
        item_names.FIREBAT,
        item_names.GHOST,
        item_names.SPECTRE,
        item_names.WRAITH,
        item_names.RAVEN,
        item_names.PREDATOR,
        item_names.LIBERATOR,
        item_names.HERC,
    }),
    SC2Race.ZERG: advanced_basic_units[SC2Race.ZERG].union({
        item_names.ZERGLING,
        item_names.PYGALISK,
        item_names.INFESTED_SIEGE_TANK,
        item_names.ULTRALISK,
        item_names.SWARM_HOST
    }),
    SC2Race.PROTOSS: advanced_basic_units[SC2Race.PROTOSS].union({
        item_names.BLOOD_HUNTER,
        item_names.STALWART,
        item_names.CARRIER,
        item_names.SKYLORD,
        item_names.TRIREME,
        item_names.TEMPEST,
        item_names.VOID_RAY,
        item_names.DESTROYER,
        item_names.PULSAR,
        item_names.DAWNBRINGER,
        item_names.COLOSSUS,
        item_names.WRATHWALKER,
        item_names.SCOUT,
        item_names.OPPRESSOR,
        item_names.MISTWING,
        item_names.HIGH_TEMPLAR,
        item_names.SIGNIFIER,
        item_names.ASCENDANT,
        item_names.DARK_ARCHON,
        item_names.SUPPLICANT,
    })
}

not_balanced_starting_units = {
    item_names.SIEGE_TANK,
    item_names.THOR,
    item_names.BANSHEE,
    item_names.BATTLECRUISER,
    item_names.ULTRALISK,
    item_names.CARRIER,
    item_names.TEMPEST,
}


# Defense rating table
# Commented defense ratings are handled in LogicMixin
tvx_defense_ratings = {
    item_names.SIEGE_TANK: 5,
    # "Graduating Range": 1,
    item_names.PLANETARY_FORTRESS: 3,
    # Bunker w/ Marine/Marauder: 3,
    item_names.PERDITION_TURRET: 2,
    item_names.DEVASTATOR_TURRET: 2,
    item_names.VULTURE: 1,
    item_names.BANSHEE: 1,
    item_names.BATTLECRUISER: 1,
    item_names.LIBERATOR: 4,
    item_names.WIDOW_MINE: 1,
    # "Concealment (Widow Mine)": 1
}
tvz_defense_ratings = {
    item_names.PERDITION_TURRET: 2,
    # Bunker w/ Firebat: 2,
    item_names.LIBERATOR: -2,
    item_names.HIVE_MIND_EMULATOR: 3,
    item_names.PSI_DISRUPTER: 3,
}
tvx_air_defense_ratings = {
    item_names.MISSILE_TURRET: 2,
}
zvx_defense_ratings = {
    # Note that this doesn't include Kerrigan because this is just for race swaps, which doesn't involve her (for now)
    item_names.SPINE_CRAWLER: 3,
    # w/ Twin Drones: 1
    item_names.SWARM_QUEEN: 1,
    item_names.SWARM_HOST: 1,
    # impaler: 3
    #  "Hardened Tentacle Spines (Impaler)": 2
    # lurker: 1
    #  "Seismic Spines (Lurker)": 2
    #  "Adapted Spines (Lurker)": 1
    # brood lord : 2
    # corpser roach: 1
    # creep tumors (swarm queen or overseer): 1
    # w/ malignant creep: 1
    # tanks with ammo: 5
    item_names.INFESTED_BUNKER: 3,
    item_names.BILE_LAUNCHER: 2,
}
# zvz_defense_ratings = {
    # corpser roach: 1
    # primal igniter: 2
    # lurker: 1
    # w/ adapted spines: -1
    # impaler: -1
# }
zvx_air_defense_ratings = {
    item_names.SPORE_CRAWLER: 2,
    # w/ Twin Drones: 1
    item_names.INFESTED_MISSILE_TURRET: 2,
}
pvx_defense_ratings = {
    item_names.PHOTON_CANNON: 2,
    item_names.KHAYDARIN_MONOLITH: 3,
    item_names.SHIELD_BATTERY: 1,
    item_names.NEXUS_OVERCHARGE: 2,
    item_names.SKYLORD: 1,
    item_names.MATRIX_OVERLOAD: 1,
    item_names.COLOSSUS: 1,
    item_names.VANGUARD: 1,
    item_names.REAVER: 1,
}
pvz_defense_ratings = {
    item_names.KHAYDARIN_MONOLITH: -2,
    item_names.COLOSSUS: 1,
}

terran_passive_ratings = {
    item_names.AUTOMATED_REFINERY: 4,
    item_names.COMMAND_CENTER_MULE: 4,
    item_names.ORBITAL_DEPOTS: 2,
    item_names.COMMAND_CENTER_COMMAND_CENTER_REACTOR: 2,
    item_names.COMMAND_CENTER_EXTRA_SUPPLIES: 2,
    item_names.MICRO_FILTERING: 2,
    item_names.TECH_REACTOR: 2
}

zerg_passive_ratings = {
    item_names.TWIN_DRONES: 7,
    item_names.AUTOMATED_EXTRACTORS: 4,
    item_names.VESPENE_EFFICIENCY: 3,
    item_names.OVERLORD_IMPROVED_OVERLORDS: 4,
    item_names.MALIGNANT_CREEP: 2
}

protoss_passive_ratings = {
    item_names.QUATRO: 4,
    item_names.ORBITAL_ASSIMILATORS: 4,
    item_names.AMPLIFIED_ASSIMILATORS: 3,
    item_names.PROBE_WARPIN: 2,
    item_names.ELDER_PROBES: 2,
    item_names.MATRIX_OVERLOAD: 2
}

soa_energy_ratings = {
    item_names.SOA_SOLAR_LANCE: 8,
    item_names.SOA_DEPLOY_FENIX: 7,
    item_names.SOA_TEMPORAL_FIELD: 6,
    item_names.SOA_PROGRESSIVE_PROXY_PYLON: 5,  # Requires Lvl 2 (Warp in Reinforcements)
    item_names.SOA_SHIELD_OVERCHARGE: 5,
    item_names.SOA_ORBITAL_STRIKE: 4
}

soa_passive_ratings = {
    item_names.GUARDIAN_SHELL: 4,
    item_names.OVERWATCH: 2
}

soa_ultimate_ratings = {
    item_names.SOA_TIME_STOP: 4,
    item_names.SOA_PURIFIER_BEAM: 3,
    item_names.SOA_SOLAR_BOMBARDMENT: 3
}

kerrigan_levels = [
    item_name for item_name, item_data in item_table.items()
    if item_data.type == ZergItemType.Level and item_data.race == SC2Race.ZERG
]


spear_of_adun_calldowns = {
    item_names.SOA_CHRONO_SURGE,
    item_names.SOA_PROGRESSIVE_PROXY_PYLON,
    item_names.SOA_PYLON_OVERCHARGE,
    item_names.SOA_ORBITAL_STRIKE,
    item_names.SOA_TEMPORAL_FIELD,
    item_names.SOA_SOLAR_LANCE,
    item_names.SOA_MASS_RECALL,
    item_names.SOA_SHIELD_OVERCHARGE,
    item_names.SOA_DEPLOY_FENIX,
    item_names.SOA_PURIFIER_BEAM,
    item_names.SOA_TIME_STOP,
    item_names.SOA_SOLAR_BOMBARDMENT
}

spear_of_adun_castable_passives = {
    item_names.RECONSTRUCTION_BEAM,
    item_names.OVERWATCH,
    item_names.GUARDIAN_SHELL,
}

nova_equipment = {
    *[item_name for item_name, item_data in get_full_item_list().items()
      if item_data.type == TerranItemType.Nova_Gear],
    item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE
}

upgrade_bundles: Dict[str, List[str]] = {
    # Terran
    item_names.PROGRESSIVE_TERRAN_WEAPON_UPGRADE:
        [
            item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON,
            item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON,
            item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON
        ],
    item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE:
        [
            item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR,
            item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR,
            item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR
        ],
    item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE:
        [
            item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR
        ],
    item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE:
        [
            item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON, item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR
        ],
    item_names.PROGRESSIVE_TERRAN_SHIP_UPGRADE:
        [
            item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR
        ],
    item_names.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE:
        [
            item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR,
            item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON, item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR,
            item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR
        ],
    # Zerg
    item_names.PROGRESSIVE_ZERG_WEAPON_UPGRADE:
        [
            item_names.PROGRESSIVE_ZERG_MELEE_ATTACK,
            item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK,
            item_names.PROGRESSIVE_ZERG_FLYER_ATTACK
        ],
    item_names.PROGRESSIVE_ZERG_ARMOR_UPGRADE:
        [
            item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE, item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE
        ],
    item_names.PROGRESSIVE_ZERG_GROUND_UPGRADE:
        [
            item_names.PROGRESSIVE_ZERG_MELEE_ATTACK,
            item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK,
            item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE
        ],
    item_names.PROGRESSIVE_ZERG_FLYER_UPGRADE:
        [
            item_names.PROGRESSIVE_ZERG_FLYER_ATTACK, item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE
        ],
    item_names.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE:
        [
            item_names.PROGRESSIVE_ZERG_MELEE_ATTACK,
            item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK,
            item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE,
            item_names.PROGRESSIVE_ZERG_FLYER_ATTACK,
            item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE
        ],
    # Protoss
    item_names.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE:
        [
            item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON, item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON
        ],
    item_names.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE:
        [
            item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR, item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR,
            item_names.PROGRESSIVE_PROTOSS_SHIELDS
        ],
    item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE:
        [
            item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON, item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR,
            item_names.PROGRESSIVE_PROTOSS_SHIELDS
        ],
    item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE:
        [
            item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON, item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR,
            item_names.PROGRESSIVE_PROTOSS_SHIELDS
        ],
    item_names.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE:
        [
            item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON, item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR,
            item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON, item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR,
            item_names.PROGRESSIVE_PROTOSS_SHIELDS
        ],
}

# Used for logic
upgrade_bundle_inverted_lookup: Dict[str, List[str]] = dict()
for key, values in upgrade_bundles.items():
    for value in values:
        if upgrade_bundle_inverted_lookup.get(value) is None:
            upgrade_bundle_inverted_lookup[value] = list()
        if (value != item_names.PROGRESSIVE_PROTOSS_SHIELDS
                or key not in [
                    item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE,
                    item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE
                ]
        ):
            # Shield handling is trickier as it's max of Ground/Air group, not their sum
            upgrade_bundle_inverted_lookup[value].append(key)

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in get_full_item_list().items() if
                                            data.code}

upgrade_item_types = (TerranItemType.Upgrade, ZergItemType.Upgrade, ProtossItemType.Upgrade)
