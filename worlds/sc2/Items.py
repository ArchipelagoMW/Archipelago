import inspect
from pydoc import describe

from BaseClasses import Item, ItemClassification, MultiWorld
import typing

from .Options import get_option_value, RequiredTactics
from .MissionTables import SC2Mission, SC2Race, SC2Campaign, campaign_mission_table
from . import ItemNames
from worlds.AutoWorld import World


class ItemData(typing.NamedTuple):
    code: int
    type: str
    number: int  # Important for bot commands to send the item into the game
    race: SC2Race
    classification: ItemClassification = ItemClassification.useful
    quantity: int = 1
    parent_item: typing.Optional[str] = None
    origin: typing.Set[str] = {"wol"}
    important_for_filtering: bool = False

    def is_important_for_filtering(self):
        return self.important_for_filtering \
            or self.classification == ItemClassification.progression \
            or self.classification == ItemClassification.progression_skip_balancing


class StarcraftItem(Item):
    game: str = "Starcraft 2"


def get_full_item_list():
    return item_table


SC2WOL_ITEM_ID_OFFSET = 1000
SC2HOTS_ITEM_ID_OFFSET = SC2WOL_ITEM_ID_OFFSET + 1000
SC2LOTV_ITEM_ID_OFFSET = SC2HOTS_ITEM_ID_OFFSET + 1000


# The items are sorted by their IDs. The IDs shall be kept for compatibility with older games.
item_table = {
    # WoL
    ItemNames.MARINE:
        ItemData(0 + SC2WOL_ITEM_ID_OFFSET, "Unit", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.MEDIC:
        ItemData(1 + SC2WOL_ITEM_ID_OFFSET, "Unit", 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.FIREBAT:
        ItemData(2 + SC2WOL_ITEM_ID_OFFSET, "Unit", 2, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.MARAUDER:
        ItemData(3 + SC2WOL_ITEM_ID_OFFSET, "Unit", 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.REAPER:
        ItemData(4 + SC2WOL_ITEM_ID_OFFSET, "Unit", 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.HELLION:
        ItemData(5 + SC2WOL_ITEM_ID_OFFSET, "Unit", 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.VULTURE:
        ItemData(6 + SC2WOL_ITEM_ID_OFFSET, "Unit", 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.GOLIATH:
        ItemData(7 + SC2WOL_ITEM_ID_OFFSET, "Unit", 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.DIAMONDBACK:
        ItemData(8 + SC2WOL_ITEM_ID_OFFSET, "Unit", 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.SIEGE_TANK:
        ItemData(9 + SC2WOL_ITEM_ID_OFFSET, "Unit", 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.MEDIVAC:
        ItemData(10 + SC2WOL_ITEM_ID_OFFSET, "Unit", 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.WRAITH:
        ItemData(11 + SC2WOL_ITEM_ID_OFFSET, "Unit", 11, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.VIKING:
        ItemData(12 + SC2WOL_ITEM_ID_OFFSET, "Unit", 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.BANSHEE:
        ItemData(13 + SC2WOL_ITEM_ID_OFFSET, "Unit", 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.BATTLECRUISER:
        ItemData(14 + SC2WOL_ITEM_ID_OFFSET, "Unit", 14, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.GHOST:
        ItemData(15 + SC2WOL_ITEM_ID_OFFSET, "Unit", 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.SPECTRE:
        ItemData(16 + SC2WOL_ITEM_ID_OFFSET, "Unit", 16, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.THOR:
        ItemData(17 + SC2WOL_ITEM_ID_OFFSET, "Unit", 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    # EE units
    ItemNames.LIBERATOR:
        ItemData(18 + SC2WOL_ITEM_ID_OFFSET, "Unit", 18, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"nco", "ext"}),
    ItemNames.VALKYRIE:
        ItemData(19 + SC2WOL_ITEM_ID_OFFSET, "Unit", 19, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"bw"}),
    ItemNames.WIDOW_MINE:
        ItemData(20 + SC2WOL_ITEM_ID_OFFSET, "Unit", 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.CYCLONE:
        ItemData(21 + SC2WOL_ITEM_ID_OFFSET, "Unit", 21, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.HERC:
        ItemData(22 + SC2WOL_ITEM_ID_OFFSET, "Unit", 26, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.WARHOUND:
        ItemData(23 + SC2WOL_ITEM_ID_OFFSET, "Unit", 27, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"}),

    # Some other items are moved to Upgrade group because of the way how the bot message is parsed
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_WEAPON: ItemData(100 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.TERRAN, quantity=3,),
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_ARMOR: ItemData(102 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_WEAPON: ItemData(103 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_ARMOR: ItemData(104 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_WEAPON: ItemData(105 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_ARMOR: ItemData(106 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 10, SC2Race.TERRAN, quantity=3),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_UPGRADE: ItemData(107 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_ARMOR_UPGRADE: ItemData(108 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 1, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE: ItemData(109 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE: ItemData(110 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 3, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_UPGRADE: ItemData(111 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE: ItemData(112 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 5, SC2Race.TERRAN, quantity=3),

    # Unit and structure upgrades
    ItemNames.BUNKER_PROJECTILE_ACCELERATOR:
        ItemData(200 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 0, SC2Race.TERRAN,
                 parent_item=ItemNames.BUNKER),
    ItemNames.BUNKER_NEOSTEEL_BUNKER:
        ItemData(201 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 1, SC2Race.TERRAN,
                 parent_item=ItemNames.BUNKER),
    ItemNames.MISSILE_TURRET_TITANIUM_HOUSING:
        ItemData(202 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 2, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MISSILE_TURRET),
    ItemNames.MISSILE_TURRET_HELLSTORM_BATTERIES:
        ItemData(203 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 3, SC2Race.TERRAN,
                 parent_item=ItemNames.MISSILE_TURRET),
    ItemNames.SCV_ADVANCED_CONSTRUCTION:
        ItemData(204 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 4, SC2Race.TERRAN),
    ItemNames.SCV_DUAL_FUSION_WELDERS:
        ItemData(205 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 5, SC2Race.TERRAN),
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM:
        ItemData(206 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 24, SC2Race.TERRAN,
                 quantity=2),
    ItemNames.PROGRESSIVE_ORBITAL_COMMAND:
        ItemData(207 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 26, SC2Race.TERRAN,
                 quantity=2, classification=ItemClassification.progression),
    ItemNames.MARINE_PROGRESSIVE_STIMPACK:
        ItemData(208 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MARINE, quantity=2),
    ItemNames.MARINE_COMBAT_SHIELD:
        ItemData(209 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MARINE),
    ItemNames.MEDIC_ADVANCED_MEDIC_FACILITIES:
        ItemData(210 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 10, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC),
    ItemNames.MEDIC_STABILIZER_MEDPACKS:
        ItemData(211 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 11, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MEDIC),
    ItemNames.FIREBAT_INCINERATOR_GAUNTLETS:
        ItemData(212 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 12, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.FIREBAT),
    ItemNames.FIREBAT_JUGGERNAUT_PLATING:
        ItemData(213 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 13, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT),
    ItemNames.MARAUDER_CONCUSSIVE_SHELLS:
        ItemData(214 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.MARAUDER),
    ItemNames.MARAUDER_KINETIC_FOAM:
        ItemData(215 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 15, SC2Race.TERRAN,
                 parent_item=ItemNames.MARAUDER),
    ItemNames.REAPER_U238_ROUNDS:
        ItemData(216 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.REAPER),
    ItemNames.REAPER_G4_CLUSTERBOMB:
        ItemData(217 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.REAPER),
    ItemNames.CYCLONE_MAG_FIELD_ACCELERATORS:
        ItemData(218 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 18, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"}),
    ItemNames.CYCLONE_MAG_FIELD_LAUNCHERS:
        ItemData(219 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 19, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"}),
    ItemNames.MARINE_LASER_TARGETING_SYSTEM:
        ItemData(220 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 8, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARINE, origin={"nco"}),
    ItemNames.MARINE_MAGRAIL_MUNITIONS:
        ItemData(221 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MARINE, origin={"nco"}),
    ItemNames.MARINE_OPTIMIZED_LOGISTICS:
        ItemData(222 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 21, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARINE, origin={"nco"}),
    ItemNames.MEDIC_RESTORATION:
        ItemData(223 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 22, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC, origin={"bw"}),
    ItemNames.MEDIC_OPTICAL_FLARE:
        ItemData(224 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 23, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC, origin={"bw"}),
    ItemNames.MEDIC_RESOURCE_EFFICIENCY:
        ItemData(225 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC, origin={"bw"}),
    ItemNames.FIREBAT_PROGRESSIVE_STIMPACK:
        ItemData(226 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 6, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, quantity=2, origin={"bw"}),
    ItemNames.FIREBAT_RESOURCE_EFFICIENCY:
        ItemData(227 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 25, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, origin={"bw"}),
    ItemNames.MARAUDER_PROGRESSIVE_STIMPACK:
        ItemData(228 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 8, SC2Race.TERRAN,
                 parent_item=ItemNames.MARAUDER, quantity=2, origin={"nco"}),
    ItemNames.MARAUDER_LASER_TARGETING_SYSTEM:
        ItemData(229 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 26, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARAUDER, origin={"nco"}),
    ItemNames.MARAUDER_MAGRAIL_MUNITIONS:
        ItemData(230 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 27, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARAUDER, origin={"nco"}),
    ItemNames.MARAUDER_INTERNAL_TECH_MODULE:
        ItemData(231 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 28, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARAUDER, origin={"nco"}),
    ItemNames.SCV_HOSTILE_ENVIRONMENT_ADAPTATION:
        ItemData(232 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 29, SC2Race.TERRAN,
                 classification=ItemClassification.filler, origin={"bw"}),
    ItemNames.MEDIC_ADAPTIVE_MEDPACKS:
        ItemData(233 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MEDIC, origin={"ext"}),
    ItemNames.MEDIC_NANO_PROJECTOR:
        ItemData(234 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC, origin={"ext"}),
    ItemNames.FIREBAT_INFERNAL_PRE_IGNITER:
        ItemData(235 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 2, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, origin={"bw"}),
    ItemNames.FIREBAT_KINETIC_FOAM:
        ItemData(236 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 3, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, origin={"ext"}),
    ItemNames.FIREBAT_NANO_PROJECTORS:
        ItemData(237 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 4, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, origin={"ext"}),
    ItemNames.MARAUDER_JUGGERNAUT_PLATING:
        ItemData(238 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 5, SC2Race.TERRAN,
                 parent_item=ItemNames.MARAUDER, origin={"ext"}),
    ItemNames.REAPER_JET_PACK_OVERDRIVE:
        ItemData(239 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 6, SC2Race.TERRAN,
                 parent_item=ItemNames.REAPER, origin={"ext"}),
    ItemNames.HELLION_INFERNAL_PLATING:
        ItemData(240 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.HELLION, origin={"ext"}),
    ItemNames.VULTURE_AUTO_REPAIR:
        ItemData(241 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 8, SC2Race.TERRAN,
                 parent_item=ItemNames.VULTURE, origin={"ext"}),
    ItemNames.GOLIATH_SHAPED_HULL:
        ItemData(242 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 9, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.GOLIATH, origin={"nco", "ext"}),
    ItemNames.GOLIATH_RESOURCE_EFFICIENCY:
        ItemData(243 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 10, SC2Race.TERRAN,
                 parent_item=ItemNames.GOLIATH, origin={"nco", "bw"}),
    ItemNames.GOLIATH_INTERNAL_TECH_MODULE:
        ItemData(244 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 11, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.GOLIATH, origin={"nco", "bw"}),
    ItemNames.SIEGE_TANK_SHAPED_HULL:
        ItemData(245 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 12, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.SIEGE_TANK, origin={"nco", "ext"}),
    ItemNames.SIEGE_TANK_RESOURCE_EFFICIENCY:
        ItemData(246 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 13, SC2Race.TERRAN,
                 parent_item=ItemNames.SIEGE_TANK, origin={"bw"}),
    ItemNames.PREDATOR_CLOAK:
        ItemData(247 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 14, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.PREDATOR, origin={"ext"}),
    ItemNames.PREDATOR_CHARGE:
        ItemData(248 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 15, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.PREDATOR, origin={"ext"}),
    ItemNames.MEDIVAC_SCATTER_VEIL:
        ItemData(249 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.MEDIVAC, origin={"ext"}),
    ItemNames.REAPER_PROGRESSIVE_STIMPACK:
        ItemData(250 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 10, SC2Race.TERRAN,
                 parent_item=ItemNames.REAPER, quantity=2, origin={"nco"}),
    ItemNames.REAPER_LASER_TARGETING_SYSTEM:
        ItemData(251 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 17, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.REAPER, origin={"nco"}),
    ItemNames.REAPER_ADVANCED_CLOAKING_FIELD:
        ItemData(252 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 18, SC2Race.TERRAN,
                 parent_item=ItemNames.REAPER, origin={"nco"}),
    ItemNames.REAPER_SPIDER_MINES:
        ItemData(253 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 19, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.REAPER, origin={"nco"},
                 important_for_filtering=True),
    ItemNames.REAPER_COMBAT_DRUGS:
        ItemData(254 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 20, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.REAPER, origin={"ext"}),
    ItemNames.HELLION_HELLBAT_ASPECT:
        ItemData(255 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 21, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.HELLION, origin={"nco"}),
    ItemNames.HELLION_SMART_SERVOS:
        ItemData(256 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 22, SC2Race.TERRAN,
                 parent_item=ItemNames.HELLION, origin={"nco"}),
    ItemNames.HELLION_OPTIMIZED_LOGISTICS:
        ItemData(257 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 23, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.HELLION, origin={"nco"}),
    ItemNames.HELLION_JUMP_JETS:
        ItemData(258 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.HELLION, origin={"nco"}),
    ItemNames.HELLION_PROGRESSIVE_STIMPACK:
        ItemData(259 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 12, SC2Race.TERRAN,
                 parent_item=ItemNames.HELLION, quantity=2, origin={"nco"}),
    ItemNames.VULTURE_ION_THRUSTERS:
        ItemData(260 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 25, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VULTURE, origin={"bw"}),
    ItemNames.VULTURE_AUTO_LAUNCHERS:
        ItemData(261 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 26, SC2Race.TERRAN,
                 parent_item=ItemNames.VULTURE, origin={"bw"}),
    ItemNames.SPIDER_MINE_HIGH_EXPLOSIVE_MUNITION:
        ItemData(262 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 27, SC2Race.TERRAN,
                 origin={"bw"}),
    ItemNames.GOLIATH_JUMP_JETS:
        ItemData(263 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 28, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.GOLIATH, origin={"nco"}),
    ItemNames.GOLIATH_OPTIMIZED_LOGISTICS:
        ItemData(264 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 29, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.GOLIATH, origin={"nco"}),
    ItemNames.DIAMONDBACK_HYPERFLUXOR:
        ItemData(265 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 0, SC2Race.TERRAN,
                 parent_item=ItemNames.DIAMONDBACK, origin={"ext"}),
    ItemNames.DIAMONDBACK_BURST_CAPACITORS:
        ItemData(266 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.DIAMONDBACK, origin={"ext"}),
    ItemNames.DIAMONDBACK_RESOURCE_EFFICIENCY:
        ItemData(267 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 2, SC2Race.TERRAN,
                 parent_item=ItemNames.DIAMONDBACK, origin={"ext"}),
    ItemNames.SIEGE_TANK_JUMP_JETS:
        ItemData(268 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.SIEGE_TANK, origin={"nco"}),
    ItemNames.SIEGE_TANK_SPIDER_MINES:
        ItemData(269 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 4, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.SIEGE_TANK, origin={"nco"},
                 important_for_filtering=True),
    ItemNames.SIEGE_TANK_SMART_SERVOS:
        ItemData(270 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 5, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.SIEGE_TANK, origin={"nco"}),
    ItemNames.SIEGE_TANK_GRADUATING_RANGE:
        ItemData(271 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.SIEGE_TANK, origin={"ext"}),
    ItemNames.SIEGE_TANK_LASER_TARGETING_SYSTEM:
        ItemData(272 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.SIEGE_TANK, origin={"nco"}),
    ItemNames.SIEGE_TANK_ADVANCED_SIEGE_TECH:
        ItemData(273 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 8, SC2Race.TERRAN,
                 parent_item=ItemNames.SIEGE_TANK, origin={"ext"}),
    ItemNames.SIEGE_TANK_INTERNAL_TECH_MODULE:
        ItemData(274 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 9, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.SIEGE_TANK, origin={"nco"}),
    ItemNames.PREDATOR_RESOURCE_EFFICIENCY:
        ItemData(275 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 10, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.PREDATOR, origin={"ext"}),
    ItemNames.MEDIVAC_EXPANDED_HULL:
        ItemData(276 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 11, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIVAC, origin={"ext"}),
    ItemNames.MEDIVAC_AFTERBURNERS:
        ItemData(277 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 12, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIVAC, origin={"ext"}),
    ItemNames.WRAITH_ADVANCED_LASER_TECHNOLOGY:
        ItemData(278 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.WRAITH, origin={"ext"}),
    ItemNames.VIKING_SMART_SERVOS:
        ItemData(279 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING, origin={"ext"}),
    ItemNames.VIKING_ANTI_MECHANICAL_MUNITION:
        ItemData(280 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 15, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING, origin={"ext"}),
    ItemNames.DIAMONDBACK_ION_THRUSTERS:
        ItemData(281 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 21, SC2Race.TERRAN,
                 parent_item=ItemNames.DIAMONDBACK, origin={"ext"}),
    ItemNames.WARHOUND_RESOURCE_EFFICIENCY:
        ItemData(282 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 13, SC2Race.TERRAN,
                 parent_item=ItemNames.WARHOUND, origin={"ext"}),
    ItemNames.WARHOUND_REINFORCED_PLATING:
        ItemData(283 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.WARHOUND, origin={"ext"}),
    ItemNames.HERC_RESOURCE_EFFICIENCY:
        ItemData(284 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 15, SC2Race.TERRAN,
                 parent_item=ItemNames.HERC, origin={"ext"}),
    ItemNames.HERC_JUGGERNAUT_PLATING:
        ItemData(285 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.HERC, origin={"ext"}),
    ItemNames.HERC_KINETIC_FOAM:
        ItemData(286 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 17, SC2Race.TERRAN,
                 parent_item=ItemNames.HERC, origin={"ext"}),

    ItemNames.HELLION_TWIN_LINKED_FLAMETHROWER:
        ItemData(300 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 16, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.HELLION),
    ItemNames.HELLION_THERMITE_FILAMENTS:
        ItemData(301 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 17, SC2Race.TERRAN,
                 parent_item=ItemNames.HELLION),
    ItemNames.SPIDER_MINE_CERBERUS_MINE:
        ItemData(302 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 18, SC2Race.TERRAN,
                 classification=ItemClassification.filler),
    ItemNames.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE:
        ItemData(303 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 16, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VULTURE, quantity=2),
    ItemNames.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM:
        ItemData(304 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 19, SC2Race.TERRAN,
                 parent_item=ItemNames.GOLIATH),
    ItemNames.GOLIATH_ARES_CLASS_TARGETING_SYSTEM:
        ItemData(305 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 20, SC2Race.TERRAN,
                 parent_item=ItemNames.GOLIATH),
    ItemNames.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL:
        ItemData(306 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade 2", 4, SC2Race.TERRAN,
                 parent_item=ItemNames.DIAMONDBACK, quantity=2),
    ItemNames.DIAMONDBACK_SHAPED_HULL:
        ItemData(307 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 22, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.DIAMONDBACK),
    ItemNames.SIEGE_TANK_MAELSTROM_ROUNDS:
        ItemData(308 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.SIEGE_TANK),
    ItemNames.SIEGE_TANK_SHAPED_BLAST:
        ItemData(309 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 24, SC2Race.TERRAN,
                 parent_item=ItemNames.SIEGE_TANK),
    ItemNames.MEDIVAC_RAPID_DEPLOYMENT_TUBE:
        ItemData(310 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 25, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIVAC),
    ItemNames.MEDIVAC_ADVANCED_HEALING_AI:
        ItemData(311 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 26, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIVAC),
    ItemNames.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS:
        ItemData(312 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 18, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WRAITH, quantity=2),
    ItemNames.WRAITH_DISPLACEMENT_FIELD:
        ItemData(313 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 27, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WRAITH),
    ItemNames.VIKING_RIPWAVE_MISSILES:
        ItemData(314 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 28, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING),
    ItemNames.VIKING_PHOBOS_CLASS_WEAPONS_SYSTEM:
        ItemData(315 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 29, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING),
    ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS:
        ItemData(316 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 2, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BANSHEE, quantity=2),
    ItemNames.BANSHEE_SHOCKWAVE_MISSILE_BATTERY:
        ItemData(317 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.BANSHEE),
    ItemNames.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS:
        ItemData(318 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade 2", 2, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, quantity=2),
    ItemNames.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX:
        ItemData(319 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 20, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, quantity=2),
    ItemNames.GHOST_OCULAR_IMPLANTS:
        ItemData(320 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 2, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST),
    ItemNames.GHOST_CRIUS_SUIT:
        ItemData(321 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 3, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST),
    ItemNames.SPECTRE_PSIONIC_LASH:
        ItemData(322 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.SPECTRE),
    ItemNames.SPECTRE_NYX_CLASS_CLOAKING_MODULE:
        ItemData(323 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 5, SC2Race.TERRAN,
                 parent_item=ItemNames.SPECTRE),
    ItemNames.THOR_330MM_BARRAGE_CANNON:
        ItemData(324 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 6, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.THOR),
    ItemNames.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL:
        ItemData(325 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 22, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.THOR, quantity=2),
    ItemNames.LIBERATOR_ADVANCED_BALLISTICS:
        ItemData(326 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.LIBERATOR, origin={"ext"}),
    ItemNames.LIBERATOR_RAID_ARTILLERY:
        ItemData(327 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.LIBERATOR, origin={"nco"}),
    ItemNames.WIDOW_MINE_DRILLING_CLAWS:
        ItemData(328 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 9, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WIDOW_MINE, origin={"ext"}),
    ItemNames.WIDOW_MINE_CONCEALMENT:
        ItemData(329 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.WIDOW_MINE, origin={"ext"}),
    ItemNames.MEDIVAC_ADVANCED_CLOAKING_FIELD:
        ItemData(330 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 11, SC2Race.TERRAN,
                 parent_item=ItemNames.MEDIVAC, origin={"ext"}),
    ItemNames.WRAITH_TRIGGER_OVERRIDE:
        ItemData(331 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 12, SC2Race.TERRAN,
                 parent_item=ItemNames.WRAITH, origin={"ext"}),
    ItemNames.WRAITH_INTERNAL_TECH_MODULE:
        ItemData(332 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 13, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WRAITH, origin={"bw"}),
    ItemNames.WRAITH_RESOURCE_EFFICIENCY:
        ItemData(333 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.WRAITH, origin={"bw"}),
    ItemNames.VIKING_SHREDDER_ROUNDS:
        ItemData(334 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.VIKING, origin={"ext"}),
    ItemNames.VIKING_WILD_MISSILES:
        ItemData(335 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING, origin={"ext"}),
    ItemNames.BANSHEE_SHAPED_HULL:
        ItemData(336 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 17, SC2Race.TERRAN,
                 parent_item=ItemNames.BANSHEE, origin={"ext"}),
    ItemNames.BANSHEE_ADVANCED_TARGETING_OPTICS:
        ItemData(337 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 18, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.BANSHEE, origin={"ext"}),
    ItemNames.BANSHEE_DISTORTION_BLASTERS:
        ItemData(338 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 19, SC2Race.TERRAN,
                 parent_item=ItemNames.BANSHEE, origin={"ext"}),
    ItemNames.BANSHEE_ROCKET_BARRAGE:
        ItemData(339 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 20, SC2Race.TERRAN,
                 parent_item=ItemNames.BANSHEE, origin={"ext"}),
    ItemNames.GHOST_RESOURCE_EFFICIENCY:
        ItemData(340 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 21, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST, origin={"bw"}),
    ItemNames.SPECTRE_RESOURCE_EFFICIENCY:
        ItemData(341 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 22, SC2Race.TERRAN,
                 parent_item=ItemNames.SPECTRE, origin={"ext"}),
    ItemNames.THOR_BUTTON_WITH_A_SKULL_ON_IT:
        ItemData(342 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.THOR, origin={"ext"}),
    ItemNames.THOR_LASER_TARGETING_SYSTEM:
        ItemData(343 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.THOR, origin={"ext"}),
    ItemNames.THOR_LARGE_SCALE_FIELD_CONSTRUCTION:
        ItemData(344 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 25, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.THOR, origin={"ext"}),
    ItemNames.RAVEN_RESOURCE_EFFICIENCY:
        ItemData(345 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 26, SC2Race.TERRAN,
                 parent_item=ItemNames.RAVEN, origin={"ext"}),
    ItemNames.RAVEN_DURABLE_MATERIALS:
        ItemData(346 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 27, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.RAVEN, origin={"ext"}),
    ItemNames.SCIENCE_VESSEL_IMPROVED_NANO_REPAIR:
        ItemData(347 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 28, SC2Race.TERRAN,
                 parent_item=ItemNames.SCIENCE_VESSEL, origin={"ext"}),
    ItemNames.SCIENCE_VESSEL_ADVANCED_AI_SYSTEMS:
        ItemData(348 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 29, SC2Race.TERRAN,
                 parent_item=ItemNames.SCIENCE_VESSEL, origin={"ext"}),
    ItemNames.CYCLONE_RESOURCE_EFFICIENCY:
        ItemData(349 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 0, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"}),
    ItemNames.BANSHEE_HYPERFLIGHT_ROTORS:
        ItemData(350 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BANSHEE, origin={"ext"}),
    ItemNames.BANSHEE_LASER_TARGETING_SYSTEM:
        ItemData(351 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 2, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BANSHEE, origin={"nco"}),
    ItemNames.BANSHEE_INTERNAL_TECH_MODULE:
        ItemData(352 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 3, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BANSHEE, origin={"nco"}),
    ItemNames.BATTLECRUISER_TACTICAL_JUMP:
        ItemData(353 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 4, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, origin={"nco", "ext"}),
    ItemNames.BATTLECRUISER_CLOAK:
        ItemData(354 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 5, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, origin={"nco"}),
    ItemNames.BATTLECRUISER_ATX_LASER_BATTERY:
        ItemData(355 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.BATTLECRUISER, origin={"nco"}),
    ItemNames.BATTLECRUISER_OPTIMIZED_LOGISTICS:
        ItemData(356 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 7, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BATTLECRUISER, origin={"ext"}),
    ItemNames.BATTLECRUISER_INTERNAL_TECH_MODULE:
        ItemData(357 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 8, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BATTLECRUISER, origin={"nco"}),
    ItemNames.GHOST_EMP_ROUNDS:
        ItemData(358 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 9, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST, origin={"ext"}),
    ItemNames.GHOST_LOCKDOWN:
        ItemData(359 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 10, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST, origin={"bw"}),
    ItemNames.SPECTRE_IMPALER_ROUNDS:
        ItemData(360 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 11, SC2Race.TERRAN,
                 parent_item=ItemNames.SPECTRE, origin={"ext"}),
    ItemNames.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD:
        ItemData(361 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.THOR, quantity=2, origin={"ext"}),
    ItemNames.RAVEN_BIO_MECHANICAL_REPAIR_DRONE:
        ItemData(363 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.RAVEN, origin={"nco"}),
    ItemNames.RAVEN_SPIDER_MINES:
        ItemData(364 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 13, SC2Race.TERRAN,
                 parent_item=ItemNames.RAVEN, origin={"nco"}, important_for_filtering=True),
    ItemNames.RAVEN_RAILGUN_TURRET:
        ItemData(365 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.RAVEN, origin={"nco"}),
    ItemNames.RAVEN_HUNTER_SEEKER_WEAPON:
        ItemData(366 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.RAVEN, origin={"nco"}),
    ItemNames.RAVEN_INTERFERENCE_MATRIX:
        ItemData(367 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.RAVEN, origin={"ext"}),
    ItemNames.RAVEN_ANTI_ARMOR_MISSILE:
        ItemData(368 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 17, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.RAVEN, origin={"ext"}),
    ItemNames.RAVEN_INTERNAL_TECH_MODULE:
        ItemData(369 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 18, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.RAVEN, origin={"nco"}),
    ItemNames.SCIENCE_VESSEL_EMP_SHOCKWAVE:
        ItemData(370 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 19, SC2Race.TERRAN,
                 parent_item=ItemNames.SCIENCE_VESSEL, origin={"bw"}),
    ItemNames.SCIENCE_VESSEL_DEFENSIVE_MATRIX:
        ItemData(371 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 20, SC2Race.TERRAN,
                 parent_item=ItemNames.SCIENCE_VESSEL, origin={"bw"}),
    ItemNames.CYCLONE_TARGETING_OPTICS:
        ItemData(372 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 21, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"}),
    ItemNames.CYCLONE_RAPID_FIRE_LAUNCHERS:
        ItemData(373 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 22, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"}),
    ItemNames.LIBERATOR_CLOAK:
        ItemData(374 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 23, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"nco"}),
    ItemNames.LIBERATOR_LASER_TARGETING_SYSTEM:
        ItemData(375 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"ext"}),
    ItemNames.LIBERATOR_OPTIMIZED_LOGISTICS:
        ItemData(376 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 25, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"nco"}),
    ItemNames.WIDOW_MINE_BLACK_MARKET_LAUNCHERS:
        ItemData(377 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 26, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WIDOW_MINE, origin={"ext"}),
    ItemNames.WIDOW_MINE_EXECUTIONER_MISSILES:
        ItemData(378 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 27, SC2Race.TERRAN,
                 parent_item=ItemNames.WIDOW_MINE, origin={"ext"}),
    ItemNames.VALKYRIE_ENHANCED_CLUSTER_LAUNCHERS:
        ItemData(379 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 28,
                 SC2Race.TERRAN, parent_item=ItemNames.VALKYRIE, origin={"ext"}),
    ItemNames.VALKYRIE_SHAPED_HULL:
        ItemData(380 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 29, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VALKYRIE, origin={"ext"}),
    ItemNames.VALKYRIE_FLECHETTE_MISSILES:
        ItemData(381 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 0, SC2Race.TERRAN,
                 parent_item=ItemNames.VALKYRIE, origin={"ext"}),
    ItemNames.VALKYRIE_AFTERBURNERS:
        ItemData(382 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VALKYRIE, origin={"ext"}),
    ItemNames.CYCLONE_INTERNAL_TECH_MODULE:
        ItemData(383 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 2, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.CYCLONE, origin={"ext"}),
    ItemNames.LIBERATOR_SMART_SERVOS:
        ItemData(384 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 3, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"nco"}),
    ItemNames.LIBERATOR_RESOURCE_EFFICIENCY:
        ItemData(385 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 4, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"ext"}),
    ItemNames.HERCULES_INTERNAL_FUSION_MODULE:
        ItemData(386 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 5, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.HERCULES, origin={"ext"}),
    ItemNames.HERCULES_TACTICAL_JUMP:
        ItemData(387 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 6, SC2Race.TERRAN,
                 parent_item=ItemNames.HERCULES, origin={"ext"}),
    ItemNames.PLANETARY_FORTRESS_PROGRESSIVE_AUGMENTED_THRUSTERS:
        ItemData(388 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 28, SC2Race.TERRAN,
                 parent_item=ItemNames.PLANETARY_FORTRESS, origin={"ext"}, quantity=2),
    ItemNames.PLANETARY_FORTRESS_ADVANCED_TARGETING:
        ItemData(389 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.PLANETARY_FORTRESS, origin={"ext"}),
    ItemNames.VALKYRIE_LAUNCHING_VECTOR_COMPENSATOR:
        ItemData(390 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 8, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VALKYRIE, origin={"ext"}),
    ItemNames.VALKYRIE_RESOURCE_EFFICIENCY:
        ItemData(391 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 9, SC2Race.TERRAN,
                 parent_item=ItemNames.VALKYRIE, origin={"ext"}),
    ItemNames.PREDATOR_PREDATOR_S_FURY:
        ItemData(392 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 10, SC2Race.TERRAN,
                 parent_item=ItemNames.PREDATOR, origin={"ext"}),
    ItemNames.BATTLECRUISER_BEHEMOTH_PLATING:
        ItemData(393 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 11, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, origin={"ext"}),
    ItemNames.BATTLECRUISER_COVERT_OPS_ENGINES:
        ItemData(394 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 12, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, origin={"nco"}),

    #Buildings
    ItemNames.BUNKER:
        ItemData(400 + SC2WOL_ITEM_ID_OFFSET, "Building", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.MISSILE_TURRET:
        ItemData(401 + SC2WOL_ITEM_ID_OFFSET, "Building", 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.SENSOR_TOWER:
        ItemData(402 + SC2WOL_ITEM_ID_OFFSET, "Building", 2, SC2Race.TERRAN),

    ItemNames.WAR_PIGS:
        ItemData(500 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.DEVIL_DOGS:
        ItemData(501 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler),
    ItemNames.HAMMER_SECURITIES:
        ItemData(502 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 2, SC2Race.TERRAN),
    ItemNames.SPARTAN_COMPANY:
        ItemData(503 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.SIEGE_BREAKERS:
        ItemData(504 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 4, SC2Race.TERRAN),
    ItemNames.HELS_ANGELS:
        ItemData(505 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.DUSK_WINGS:
        ItemData(506 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 6, SC2Race.TERRAN),
    ItemNames.JACKSONS_REVENGE:
        ItemData(507 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 7, SC2Race.TERRAN),
    ItemNames.SKIBIS_ANGELS:
        ItemData(508 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 8, SC2Race.TERRAN,
                 origin={"ext"}),
    ItemNames.DEATH_HEADS:
        ItemData(509 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 9, SC2Race.TERRAN,
                 origin={"ext"}),
    ItemNames.WINGED_NIGHTMARES:
        ItemData(510 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.MIDNIGHT_RIDERS:
        ItemData(511 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 11, SC2Race.TERRAN,
                 origin={"ext"}),
    ItemNames.BRYNHILDS:
        ItemData(512 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.JOTUN:
        ItemData(513 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 13, SC2Race.TERRAN,
                 origin={"ext"}),

    ItemNames.ULTRA_CAPACITORS:
        ItemData(600 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 0, SC2Race.TERRAN),
    ItemNames.VANADIUM_PLATING:
        ItemData(601 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 1, SC2Race.TERRAN),
    ItemNames.ORBITAL_DEPOTS:
        ItemData(602 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 2, SC2Race.TERRAN),
    ItemNames.MICRO_FILTERING:
        ItemData(603 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 3, SC2Race.TERRAN),
    ItemNames.AUTOMATED_REFINERY:
        ItemData(604 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 4, SC2Race.TERRAN),
    ItemNames.COMMAND_CENTER_REACTOR:
        ItemData(605 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 5, SC2Race.TERRAN),
    ItemNames.RAVEN:
        ItemData(606 + SC2WOL_ITEM_ID_OFFSET, "Unit", 22, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.SCIENCE_VESSEL:
        ItemData(607 + SC2WOL_ITEM_ID_OFFSET, "Unit", 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.TECH_REACTOR:
        ItemData(608 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 6, SC2Race.TERRAN),
    ItemNames.ORBITAL_STRIKE:
        ItemData(609 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 7, SC2Race.TERRAN),
    ItemNames.BUNKER_SHRIKE_TURRET:
        ItemData(610 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 6, SC2Race.TERRAN,
                 parent_item=ItemNames.BUNKER),
    ItemNames.BUNKER_FORTIFIED_BUNKER:
        ItemData(611 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.BUNKER),
    ItemNames.PLANETARY_FORTRESS:
        ItemData(612 + SC2WOL_ITEM_ID_OFFSET, "Building", 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.PERDITION_TURRET:
        ItemData(613 + SC2WOL_ITEM_ID_OFFSET, "Building", 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.PREDATOR:
        ItemData(614 + SC2WOL_ITEM_ID_OFFSET, "Unit", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler),
    ItemNames.HERCULES:
        ItemData(615 + SC2WOL_ITEM_ID_OFFSET, "Unit", 25, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.CELLULAR_REACTOR:
        ItemData(616 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 8, SC2Race.TERRAN),
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL:
        ItemData(617 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 4, SC2Race.TERRAN, quantity=3,
                 classification= ItemClassification.progression),
    ItemNames.HIVE_MIND_EMULATOR:
        ItemData(618 + SC2WOL_ITEM_ID_OFFSET, "Building", 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.PSI_DISRUPTER:
        ItemData(619 + SC2WOL_ITEM_ID_OFFSET, "Building", 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression),
    ItemNames.STRUCTURE_ARMOR:
        ItemData(620 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 9, SC2Race.TERRAN),
    ItemNames.HI_SEC_AUTO_TRACKING:
        ItemData(621 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 10, SC2Race.TERRAN),
    ItemNames.ADVANCED_OPTICS:
        ItemData(622 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 11, SC2Race.TERRAN),
    ItemNames.ROGUE_FORCES:
        ItemData(623 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 12, SC2Race.TERRAN, origin={"ext"}),

    ItemNames.ZEALOT:
        ItemData(700 + SC2WOL_ITEM_ID_OFFSET, "Unit", 0, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.STALKER: 
        ItemData(701 + SC2WOL_ITEM_ID_OFFSET, "Unit", 1, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.HIGH_TEMPLAR: 
        ItemData(702 + SC2WOL_ITEM_ID_OFFSET, "Unit", 2, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.DARK_TEMPLAR: 
        ItemData(703 + SC2WOL_ITEM_ID_OFFSET, "Unit", 3, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.IMMORTAL: 
        ItemData(704 + SC2WOL_ITEM_ID_OFFSET, "Unit", 4, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.COLOSSUS:
        ItemData(705 + SC2WOL_ITEM_ID_OFFSET, "Unit", 5, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.PHOENIX:
        ItemData(706 + SC2WOL_ITEM_ID_OFFSET, "Unit", 6, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.VOID_RAY:
        ItemData(707 + SC2WOL_ITEM_ID_OFFSET, "Unit", 7, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.CARRIER:
        ItemData(708 + SC2WOL_ITEM_ID_OFFSET, "Unit", 8, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"}),

    # Filler items to fill remaining spots
    ItemNames.STARTING_MINERALS:
        ItemData(800 + SC2WOL_ITEM_ID_OFFSET, "Minerals", 15, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    ItemNames.STARTING_VESPENE:
        ItemData(801 + SC2WOL_ITEM_ID_OFFSET, "Vespene", 15, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    ItemNames.STARTING_SUPPLY:
        ItemData(802 + SC2WOL_ITEM_ID_OFFSET, "Supply", 2, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler),
    # This item is used to "remove" location from the game. Never placed unless plando'd
    ItemNames.NOTHING:
        ItemData(803 + SC2WOL_ITEM_ID_OFFSET, "Nothing Group", 2, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.trap),

    # Nova gear
    ItemNames.NOVA_GHOST_VISOR:
        ItemData(900 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 0, SC2Race.TERRAN, origin={"nco"}),
    ItemNames.NOVA_RANGEFINDER_OCULUS:
        ItemData(901 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 1, SC2Race.TERRAN, origin={"nco"}),
    ItemNames.NOVA_DOMINATION:
        ItemData(902 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 2, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_BLINK:
        ItemData(903 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 3, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE:
        ItemData(904 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade 2", 0, SC2Race.TERRAN, quantity=2, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_ENERGY_SUIT_MODULE:
        ItemData(905 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 4, SC2Race.TERRAN, origin={"nco"}),
    ItemNames.NOVA_ARMORED_SUIT_MODULE:
        ItemData(906 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 5, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_JUMP_SUIT_MODULE:
        ItemData(907 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 6, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_C20A_CANISTER_RIFLE:
        ItemData(908 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 7, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_HELLFIRE_SHOTGUN:
        ItemData(909 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 8, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_PLASMA_RIFLE:
        ItemData(910 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 9, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_MONOMOLECULAR_BLADE:
        ItemData(911 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 10, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_BLAZEFIRE_GUNBLADE:
        ItemData(912 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 11, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_STIM_INFUSION:
        ItemData(913 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 12, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_PULSE_GRENADES:
        ItemData(914 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 13, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_FLASHBANG_GRENADES:
        ItemData(915 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 14, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_IONIC_FORCE_FIELD:
        ItemData(916 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 15, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_HOLO_DECOY:
        ItemData(917 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 16, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),
    ItemNames.NOVA_NUKE:
        ItemData(918 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 17, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression),

    # HotS
    ItemNames.ZERGLING:
        ItemData(0 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 0, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.SWARM_QUEEN:
        ItemData(1 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 1, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.ROACH:
        ItemData(2 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 2, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.HYDRALISK:
        ItemData(3 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 3, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.ZERGLING_BANELING_ASPECT:
        ItemData(4 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 5, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.ABERRATION:
        ItemData(5 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 5, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.MUTALISK:
        ItemData(6 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 6, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.SWARM_HOST:
        ItemData(7 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 7, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.INFESTOR:
        ItemData(8 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 8, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.ULTRALISK:
        ItemData(9 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 9, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.SPORE_CRAWLER:
        ItemData(10 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 10, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.SPINE_CRAWLER:
        ItemData(11 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 11, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.CORRUPTOR:
        ItemData(12 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 12, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.SCOURGE:
        ItemData(13 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 13, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"bw", "ext"}),
    ItemNames.BROOD_QUEEN:
        ItemData(14 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 4, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"bw", "ext"}),
    ItemNames.DEFILER:
        ItemData(15 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 14, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"bw"}),

    ItemNames.PROGRESSIVE_ZERG_MELEE_ATTACK: ItemData(100 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_MISSILE_ATTACK: ItemData(101 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_GROUND_CARAPACE: ItemData(102 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_FLYER_ATTACK: ItemData(103 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_FLYER_CARAPACE: ItemData(104 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.ZERG, quantity=3, origin={"hots"}),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    ItemNames.PROGRESSIVE_ZERG_WEAPON_UPGRADE: ItemData(105 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_ARMOR_UPGRADE: ItemData(106 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 7, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_GROUND_UPGRADE: ItemData(107 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_FLYER_UPGRADE: ItemData(108 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 9, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE: ItemData(109 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 10, SC2Race.ZERG, quantity=3, origin={"hots"}),

    ItemNames.ZERGLING_HARDENED_CARAPACE:
        ItemData(200 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 0, SC2Race.ZERG, parent_item=ItemNames.ZERGLING, origin={"hots"}),
    ItemNames.ZERGLING_ADRENAL_OVERLOAD:
        ItemData(201 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 1, SC2Race.ZERG, parent_item=ItemNames.ZERGLING, origin={"hots"}),
    ItemNames.ZERGLING_METABOLIC_BOOST:
        ItemData(202 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 2, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.ROACH_HYDRIODIC_BILE:
        ItemData(203 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 3, SC2Race.ZERG, parent_item=ItemNames.ROACH, origin={"hots"}),
    ItemNames.ROACH_ADAPTIVE_PLATING:
        ItemData(204 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 4, SC2Race.ZERG, parent_item=ItemNames.ROACH, origin={"hots"}),
    ItemNames.ROACH_TUNNELING_CLAWS:
        ItemData(205 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 5, SC2Race.ZERG, parent_item=ItemNames.ROACH,
                 origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.HYDRALISK_FRENZY:
        ItemData(206 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 6, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK, origin={"hots"}),
    ItemNames.HYDRALISK_ANCILLARY_CARAPACE:
        ItemData(207 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 7, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.HYDRALISK_GROOVED_SPINES:
        ItemData(208 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 8, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"hots"}),
    ItemNames.BANELING_CORROSIVE_ACID:
        ItemData(209 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 9, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"}),
    ItemNames.BANELING_RUPTURE:
        ItemData(210 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 10, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"},
                 classification=ItemClassification.filler),
    ItemNames.BANELING_REGENERATIVE_ACID:
        ItemData(211 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 11, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"},
                 classification=ItemClassification.filler),
    ItemNames.MUTALISK_VICIOUS_GLAIVE:
        ItemData(212 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 12, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"hots"}),
    ItemNames.MUTALISK_RAPID_REGENERATION:
        ItemData(213 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 13, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"hots"}),
    ItemNames.MUTALISK_SUNDERING_GLAIVE:
        ItemData(214 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 14, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"hots"}),
    ItemNames.SWARM_HOST_BURROW:
        ItemData(215 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 15, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.SWARM_HOST_RAPID_INCUBATION:
        ItemData(216 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 16, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}),
    ItemNames.SWARM_HOST_PRESSURIZED_GLANDS:
        ItemData(217 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 17, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.ULTRALISK_BURROW_CHARGE:
        ItemData(218 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 18, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}),
    ItemNames.ULTRALISK_TISSUE_ASSIMILATION:
        ItemData(219 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 19, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}),
    ItemNames.ULTRALISK_MONARCH_BLADES:
        ItemData(220 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 20, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}),
    ItemNames.CORRUPTOR_CAUSTIC_SPRAY:
        ItemData(221 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 21, SC2Race.ZERG, parent_item=ItemNames.CORRUPTOR,
                 origin={"ext"}),
    ItemNames.CORRUPTOR_CORRUPTION:
        ItemData(222 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 22, SC2Race.ZERG, parent_item=ItemNames.CORRUPTOR,
                 origin={"ext"}),
    ItemNames.SCOURGE_VIRULENT_SPORES:
        ItemData(223 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 23, SC2Race.ZERG, parent_item=ItemNames.SCOURGE,
                 origin={"ext"}),
    ItemNames.SCOURGE_RESOURCE_EFFICIENCY:
        ItemData(224 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 24, SC2Race.ZERG, parent_item=ItemNames.SCOURGE,
                 origin={"ext"}, classification=ItemClassification.progression),
    ItemNames.SCOURGE_SWARM_SCOURGE:
        ItemData(225 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 25, SC2Race.ZERG, parent_item=ItemNames.SCOURGE,
                 origin={"ext"}),
    ItemNames.ZERGLING_SHREDDING_CLAWS:
        ItemData(226 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 26, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"ext"}),
    ItemNames.ROACH_GLIAL_RECONSTITUTION:
        ItemData(227 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 27, SC2Race.ZERG, parent_item=ItemNames.ROACH,
                 origin={"ext"}),
    ItemNames.ROACH_ORGANIC_CARAPACE:
        ItemData(228 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 28, SC2Race.ZERG, parent_item=ItemNames.ROACH,
                 origin={"ext"}),
    ItemNames.HYDRALISK_MUSCULAR_AUGMENTS:
        ItemData(229 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 29, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"bw"}),
    ItemNames.HYDRALISK_RESOURCE_EFFICIENCY:
        ItemData(230 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 0, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"bw"}),
    ItemNames.BANELING_CENTRIFUGAL_HOOKS:
        ItemData(231 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 1, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"ext"}),
    ItemNames.BANELING_TUNNELING_JAWS:
        ItemData(232 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 2, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"ext"}),
    ItemNames.BANELING_RAPID_METAMORPH:
        ItemData(233 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 3, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"ext"}),
    ItemNames.MUTALISK_SEVERING_GLAIVE:
        ItemData(234 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 4, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"ext"}),
    ItemNames.MUTALISK_AERODYNAMIC_GLAIVE_SHAPE:
        ItemData(235 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 5, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"ext"}),
    ItemNames.SWARM_HOST_LOCUST_METABOLIC_BOOST:
        ItemData(236 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 6, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"ext"}, classification=ItemClassification.filler),
    ItemNames.SWARM_HOST_ENDURING_LOCUSTS:
        ItemData(237 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 7, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"ext"}),
    ItemNames.SWARM_HOST_ORGANIC_CARAPACE:
        ItemData(238 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 8, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"ext"}),
    ItemNames.SWARM_HOST_RESOURCE_EFFICIENCY:
        ItemData(239 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 9, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"ext"}),
    ItemNames.ULTRALISK_ANABOLIC_SYNTHESIS:
        ItemData(240 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 10, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"bw"}, classification=ItemClassification.filler),
    ItemNames.ULTRALISK_CHITINOUS_PLATING:
        ItemData(241 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 11, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"bw"}),
    ItemNames.ULTRALISK_ORGANIC_CARAPACE:
        ItemData(242 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 12, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"ext"}),
    ItemNames.ULTRALISK_RESOURCE_EFFICIENCY:
        ItemData(243 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 13, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"bw"}),
    ItemNames.DEVOURER_CORROSIVE_SPRAY:
        ItemData(244 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 14, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, origin={"ext"}),
    ItemNames.DEVOURER_GAPING_MAW:
        ItemData(245 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 15, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, origin={"ext"}),
    ItemNames.DEVOURER_IMPROVED_OSMOSIS:
        ItemData(246 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 16, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, origin={"ext"},
                 classification=ItemClassification.filler),
    ItemNames.DEVOURER_PRESCIENT_SPORES:
        ItemData(247 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 17, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, origin={"ext"}),
    ItemNames.GUARDIAN_PROLONGED_DISPERSION:
        ItemData(248 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 18, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT, origin={"ext"}),
    ItemNames.GUARDIAN_PRIMAL_ADAPTATION:
        ItemData(249 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 19, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT, origin={"ext"}),
    ItemNames.GUARDIAN_SORONAN_ACID:
        ItemData(250 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 20, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT, origin={"ext"}),
    ItemNames.IMPALER_ADAPTIVE_TALONS:
        ItemData(251 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 21, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_IMPALER_ASPECT, origin={"ext"},
                 classification=ItemClassification.filler),
    ItemNames.IMPALER_SECRETION_GLANDS:
        ItemData(252 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 22, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_IMPALER_ASPECT, origin={"ext"}),
    ItemNames.IMPALER_HARDENED_TENTACLE_SPINES:
        ItemData(253 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 23, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_IMPALER_ASPECT, origin={"ext"}),
    ItemNames.LURKER_SEISMIC_SPINES:
        ItemData(254 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 24, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_LURKER_ASPECT, origin={"ext"}),
    ItemNames.LURKER_ADAPTED_SPINES:
        ItemData(255 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 25, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_LURKER_ASPECT, origin={"ext"}),
    ItemNames.RAVAGER_POTENT_BILE:
        ItemData(256 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 26, SC2Race.ZERG,
                 parent_item=ItemNames.ROACH_RAVAGER_ASPECT, origin={"ext"}),
    ItemNames.RAVAGER_BLOATED_BILE_DUCTS:
        ItemData(257 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 27, SC2Race.ZERG,
                 parent_item=ItemNames.ROACH_RAVAGER_ASPECT, origin={"ext"}),
    ItemNames.RAVAGER_DEEP_TUNNEL:
        ItemData(258 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 28, SC2Race.ZERG,
                 parent_item=ItemNames.ROACH_RAVAGER_ASPECT, origin={"ext"}),
    ItemNames.VIPER_PARASITIC_BOMB:
        ItemData(259 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 29, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT, origin={"ext"}),
    ItemNames.VIPER_PARALYTIC_BARBS:
        ItemData(260 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 0, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT, origin={"ext"}),
    ItemNames.VIPER_VIRULENT_MICROBES:
        ItemData(261 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 1, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT, origin={"ext"}),
    ItemNames.BROOD_LORD_POROUS_CARTILAGE:
        ItemData(262 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 2, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, origin={"ext"}),
    ItemNames.BROOD_LORD_EVOLVED_CARAPACE:
        ItemData(263 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 3, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, origin={"ext"}),
    ItemNames.BROOD_LORD_SPLITTER_MITOSIS:
        ItemData(264 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 4, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, origin={"ext"}),
    ItemNames.BROOD_LORD_RESOURCE_EFFICIENCY:
        ItemData(265 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 5, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, origin={"ext"}),
    ItemNames.INFESTOR_INFESTED_TERRAN:
        ItemData(266 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 6, SC2Race.ZERG, parent_item=ItemNames.INFESTOR,
                 origin={"ext"}),
    ItemNames.INFESTOR_MICROBIAL_SHROUD:
        ItemData(267 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 7, SC2Race.ZERG, parent_item=ItemNames.INFESTOR,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_SPAWN_LARVAE:
        ItemData(268 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 8, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_DEEP_TUNNEL:
        ItemData(269 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 9, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_ORGANIC_CARAPACE:
        ItemData(270 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 10, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}, classification=ItemClassification.filler),
    ItemNames.SWARM_QUEEN_BIO_MECHANICAL_TRANSFUSION:
        ItemData(271 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 11, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_RESOURCE_EFFICIENCY:
        ItemData(272 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 12, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_INCUBATOR_CHAMBER:
        ItemData(273 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 13, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.BROOD_QUEEN_FUNGAL_GROWTH:
        ItemData(274 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 14, SC2Race.ZERG, parent_item=ItemNames.BROOD_QUEEN,
                 origin={"ext"}),
    ItemNames.BROOD_QUEEN_ENSNARE:
        ItemData(275 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 15, SC2Race.ZERG, parent_item=ItemNames.BROOD_QUEEN,
                 origin={"ext"}),
    ItemNames.BROOD_QUEEN_ENHANCED_MITOCHONDRIA:
        ItemData(276 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 16, SC2Race.ZERG, parent_item=ItemNames.BROOD_QUEEN,
                 origin={"ext"}),

    ItemNames.ZERGLING_RAPTOR_STRAIN:
        ItemData(300 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 0, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"hots"}),
    ItemNames.ZERGLING_SWARMLING_STRAIN:
        ItemData(301 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 1, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"hots"}),
    ItemNames.ROACH_VILE_STRAIN:
        ItemData(302 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 2, SC2Race.ZERG, parent_item=ItemNames.ROACH, origin={"hots"}),
    ItemNames.ROACH_CORPSER_STRAIN:
        ItemData(303 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 3, SC2Race.ZERG, parent_item=ItemNames.ROACH, origin={"hots"}),
    ItemNames.HYDRALISK_IMPALER_ASPECT:
        ItemData(304 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 0, SC2Race.ZERG, origin={"hots"},
                 classification=ItemClassification.progression),
    ItemNames.HYDRALISK_LURKER_ASPECT:
        ItemData(305 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 1, SC2Race.ZERG, origin={"hots"},
                 classification=ItemClassification.progression),
    ItemNames.BANELING_SPLITTER_STRAIN:
        ItemData(306 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 6, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"}),
    ItemNames.BANELING_HUNTER_STRAIN:
        ItemData(307 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 7, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"}),
    ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT:
        ItemData(308 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 2, SC2Race.ZERG, origin={"hots"},
                 classification=ItemClassification.progression),
    ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT:
        ItemData(309 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 3, SC2Race.ZERG, origin={"hots"},
                 classification=ItemClassification.progression),
    ItemNames.SWARM_HOST_CARRION_STRAIN:
        ItemData(310 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 10, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}),
    ItemNames.SWARM_HOST_CREEPER_STRAIN:
        ItemData(311 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 11, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.ULTRALISK_NOXIOUS_STRAIN:
        ItemData(312 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 12, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.ULTRALISK_TORRASQUE_STRAIN:
        ItemData(313 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 13, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}),

    ItemNames.KERRIGAN_KINETIC_BLAST: ItemData(400 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 0, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_HEROIC_FORTITUDE: ItemData(401 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 1, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEAPING_STRIKE: ItemData(402 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 2, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_CRUSHING_GRIP: ItemData(403 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 3, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_CHAIN_REACTION: ItemData(404 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 4, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_PSIONIC_SHIFT: ItemData(405 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 5, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_ZERGLING_RECONSTITUTION: ItemData(406 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 0, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.KERRIGAN_IMPROVED_OVERLORDS: ItemData(407 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 1, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_AUTOMATED_EXTRACTORS: ItemData(408 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 2, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_WILD_MUTATION: ItemData(409 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 6, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_SPAWN_BANELINGS: ItemData(410 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 7, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_MEND: ItemData(411 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 8, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_TWIN_DRONES: ItemData(412 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 3, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_MALIGNANT_CREEP: ItemData(413 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 4, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_VESPENE_EFFICIENCY: ItemData(414 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 5, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_INFEST_BROODLINGS: ItemData(415 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 9, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_FURY: ItemData(416 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 10, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_ABILITY_EFFICIENCY: ItemData(417 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 11, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_APOCALYPSE: ItemData(418 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 12, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_SPAWN_LEVIATHAN: ItemData(419 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 13, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_DROP_PODS: ItemData(420 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 14, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    # Handled separately from other abilities
    ItemNames.KERRIGAN_PRIMAL_FORM: ItemData(421 + SC2HOTS_ITEM_ID_OFFSET, "Primal Form", 0, SC2Race.ZERG, origin={"hots"}),

    ItemNames.KERRIGAN_LEVELS_10: ItemData(500 + SC2HOTS_ITEM_ID_OFFSET, "Level", 10, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_9: ItemData(501 + SC2HOTS_ITEM_ID_OFFSET, "Level", 9, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_8: ItemData(502 + SC2HOTS_ITEM_ID_OFFSET, "Level", 8, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_7: ItemData(503 + SC2HOTS_ITEM_ID_OFFSET, "Level", 7, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_6: ItemData(504 + SC2HOTS_ITEM_ID_OFFSET, "Level", 6, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_5: ItemData(505 + SC2HOTS_ITEM_ID_OFFSET, "Level", 5, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_4: ItemData(506 + SC2HOTS_ITEM_ID_OFFSET, "Level", 4, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression_skip_balancing),
    ItemNames.KERRIGAN_LEVELS_3: ItemData(507 + SC2HOTS_ITEM_ID_OFFSET, "Level", 3, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression_skip_balancing),
    ItemNames.KERRIGAN_LEVELS_2: ItemData(508 + SC2HOTS_ITEM_ID_OFFSET, "Level", 2, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression_skip_balancing),
    ItemNames.KERRIGAN_LEVELS_1: ItemData(509 + SC2HOTS_ITEM_ID_OFFSET, "Level", 1, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression_skip_balancing),
    ItemNames.KERRIGAN_LEVELS_14: ItemData(510 + SC2HOTS_ITEM_ID_OFFSET, "Level", 14, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_35: ItemData(511 + SC2HOTS_ITEM_ID_OFFSET, "Level", 35, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_70: ItemData(512 + SC2HOTS_ITEM_ID_OFFSET, "Level", 70, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),

    # Zerg Mercs
    ItemNames.INFESTED_MEDICS: ItemData(600 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 0, SC2Race.ZERG, origin={"ext"}),
    ItemNames.INFESTED_SIEGE_TANKS: ItemData(601 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 1, SC2Race.ZERG, origin={"ext"}),
    ItemNames.INFESTED_BANSHEES: ItemData(602 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 2, SC2Race.ZERG, origin={"ext"}),

    # Misc Upgrades
    ItemNames.OVERLORD_VENTRAL_SACS: ItemData(700 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 6, SC2Race.ZERG, origin={"bw"}),

    # Morphs
    ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT: ItemData(800 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 6, SC2Race.ZERG, origin={"bw"}),
    ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT: ItemData(801 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 7, SC2Race.ZERG, origin={"bw"}),
    ItemNames.ROACH_RAVAGER_ASPECT: ItemData(802 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 8, SC2Race.ZERG, origin={"ext"}),


    # Protoss Units (those that aren't as items in WoL (Prophecy))
    ItemNames.OBSERVER: ItemData(0 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 9, SC2Race.PROTOSS, 
                 classification=ItemClassification.filler, origin={"wol"}),
    ItemNames.CENTURION: ItemData(1 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 10, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SENTINEL: ItemData(2 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 11, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SUPPLICANT: ItemData(3 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 12, SC2Race.PROTOSS, 
                 classification=ItemClassification.filler, important_for_filtering=True, origin={"ext"}),
    ItemNames.INSTIGATOR: ItemData(4 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 13, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.SLAYER: ItemData(5 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 14, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.SENTRY: ItemData(6 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 15, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.ENERGIZER: ItemData(7 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 16, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.HAVOC: ItemData(8 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 17, SC2Race.PROTOSS,
                 origin={"lotv"}, important_for_filtering=True),
    ItemNames.SIGNIFIER: ItemData(9 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 18, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.ASCENDANT: ItemData(10 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 19, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.AVENGER: ItemData(11 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 20, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.BLOOD_HUNTER: ItemData(12 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 21, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.DRAGOON: ItemData(13 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 22, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.DARK_ARCHON: ItemData(14 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 23, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.ADEPT: ItemData(15 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 24, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.WARP_PRISM: ItemData(16 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 25, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.ANNIHILATOR: ItemData(17 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 26, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.VANGUARD: ItemData(18 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 27, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.WRATHWALKER: ItemData(19 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 28, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.REAVER: ItemData(20 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 29, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.DISRUPTOR: ItemData(21 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 0, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.MIRAGE: ItemData(22 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 1, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.CORSAIR: ItemData(23 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 2, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.DESTROYER: ItemData(24 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 3, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SCOUT: ItemData(25 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 4, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.TEMPEST: ItemData(26 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 5, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.MOTHERSHIP: ItemData(27 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 6, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.ARBITER: ItemData(28 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 7, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.ORACLE: ItemData(29 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 8, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"}),

    # Protoss Upgrades
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_WEAPON: ItemData(100 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_ARMOR: ItemData(101 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_SHIELDS: ItemData(102 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_WEAPON: ItemData(103 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_ARMOR: ItemData(104 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE: ItemData(105 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 11, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE: ItemData(106 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 12, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_UPGRADE: ItemData(107 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 13, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_UPGRADE: ItemData(108 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 14, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE: ItemData(109 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 15, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),

    # Protoss Buildings
    ItemNames.PHOTON_CANNON: ItemData(200 + SC2LOTV_ITEM_ID_OFFSET, "Building", 0, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.KHAYDARIN_MONOLITH: ItemData(201 + SC2LOTV_ITEM_ID_OFFSET, "Building", 1, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SHIELD_BATTERY: ItemData(202 + SC2LOTV_ITEM_ID_OFFSET, "Building", 2, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),

    # Protoss Unit Upgrades
    ItemNames.SUPPLICANT_BLOOD_SHIELD: ItemData(300 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 0, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SUPPLICANT),
    ItemNames.SUPPLICANT_SOUL_AUGMENTATION: ItemData(301 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 1, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SUPPLICANT),
    ItemNames.SUPPLICANT_SHIELD_REGENERATION: ItemData(302 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 2, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SUPPLICANT),
    ItemNames.ADEPT_SHOCKWAVE: ItemData(303 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 3, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ADEPT),
    ItemNames.ADEPT_RESONATING_GLAIVES: ItemData(304 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 4, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ADEPT),
    ItemNames.ADEPT_PHASE_BULWARK: ItemData(305 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 5, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ADEPT),
    ItemNames.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES: ItemData(306 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 6, SC2Race.PROTOSS, origin={"ext"}, classification=ItemClassification.progression),
    ItemNames.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION: ItemData(307 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 7, SC2Race.PROTOSS, origin={"ext"}, classification=ItemClassification.progression),
    ItemNames.DRAGOON_HIGH_IMPACT_PHASE_DISRUPTORS: ItemData(308 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 8, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.DRAGOON),
    ItemNames.DRAGOON_TRILLIC_COMPRESSION_SYSTEM: ItemData(309 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 9, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.DRAGOON),
    ItemNames.DRAGOON_SINGULARITY_CHARGE: ItemData(310 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 10, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.DRAGOON),
    ItemNames.DRAGOON_ENHANCED_STRIDER_SERVOS: ItemData(311 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 11, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.DRAGOON),
    ItemNames.SCOUT_COMBAT_SENSOR_ARRAY: ItemData(312 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 12, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.SCOUT),
    ItemNames.SCOUT_APIAL_SENSORS: ItemData(313 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 13, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.SCOUT),
    ItemNames.SCOUT_GRAVITIC_THRUSTERS: ItemData(314 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 14, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.SCOUT),
    ItemNames.SCOUT_ADVANCED_PHOTON_BLASTERS: ItemData(315 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 15, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.SCOUT),
    ItemNames.TEMPEST_TECTONIC_DESTABILIZERS: ItemData(316 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 16, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.TEMPEST),
    ItemNames.TEMPEST_QUANTIC_REACTOR: ItemData(317 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 17, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.TEMPEST),
    ItemNames.TEMPEST_GRAVITY_SLING: ItemData(318 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 18, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.TEMPEST),
    ItemNames.PHOENIX_MIRAGE_IONIC_WAVELENGTH_FLUX: ItemData(319 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 19, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.PHOENIX_MIRAGE_ANION_PULSE_CRYSTALS: ItemData(320 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 20, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.CORSAIR_STEALTH_DRIVE: ItemData(321 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 21, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.CORSAIR),
    ItemNames.CORSAIR_ARGUS_JEWEL: ItemData(322 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 22, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.CORSAIR),
    ItemNames.CORSAIR_SUSTAINING_DISRUPTION: ItemData(323 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 23, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.CORSAIR),
    ItemNames.CORSAIR_NEUTRON_SHIELDS: ItemData(324 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 24, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.CORSAIR),
    ItemNames.ORACLE_STEALTH_DRIVE: ItemData(325 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 25, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ORACLE),
    ItemNames.ORACLE_STASIS_CALIBRATION: ItemData(326 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 26, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ORACLE),
    ItemNames.ORACLE_TEMPORAL_ACCELERATION_BEAM: ItemData(327 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 27, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ORACLE),
    ItemNames.ARBITER_CHRONOSTATIC_REINFORCEMENT: ItemData(328 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 28, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.ARBITER_KHAYDARIN_CORE: ItemData(329 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 29, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.ARBITER_SPACETIME_ANCHOR: ItemData(330 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 0, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.ARBITER_RESOURCE_EFFICIENCY: ItemData(331 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 1, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.ARBITER_ENHANCED_CLOAK_FIELD: ItemData(332 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 2, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.CARRIER_GRAVITON_CATAPULT:
        ItemData(333 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 3, SC2Race.PROTOSS, origin={"wol"},
                 parent_item=ItemNames.CARRIER),
    ItemNames.CARRIER_HULL_OF_PAST_GLORIES:
        ItemData(334 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 4, SC2Race.PROTOSS, origin={"bw"},
                 parent_item=ItemNames.CARRIER),
    ItemNames.VOID_RAY_DESTROYER_FLUX_VANES:
        ItemData(335 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 5, SC2Race.PROTOSS, classification=ItemClassification.filler,
                 origin={"ext"}),
    ItemNames.DESTROYER_REFORGED_BLOODSHARD_CORE:
        ItemData(336 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 6, SC2Race.PROTOSS, origin={"ext"},
                 parent_item=ItemNames.DESTROYER),
    ItemNames.WARP_PRISM_GRAVITIC_DRIVE:
        ItemData(337 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 7, SC2Race.PROTOSS, classification=ItemClassification.filler,
                 origin={"ext"}, parent_item=ItemNames.WARP_PRISM),
    ItemNames.WARP_PRISM_PHASE_BLASTER:
        ItemData(338 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 8, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"ext"}, parent_item=ItemNames.WARP_PRISM),
    ItemNames.WARP_PRISM_WAR_CONFIGURATION: ItemData(339 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 9, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.WARP_PRISM),
    ItemNames.OBSERVER_GRAVITIC_BOOSTERS: ItemData(340 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 10, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.OBSERVER),
    ItemNames.OBSERVER_SENSOR_ARRAY: ItemData(341 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 11, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.OBSERVER),
    ItemNames.REAVER_SCARAB_DAMAGE: ItemData(342 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 12, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.REAVER),
    ItemNames.REAVER_SOLARITE_PAYLOAD: ItemData(343 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 13, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.REAVER),
    ItemNames.REAVER_REAVER_CAPACITY: ItemData(344 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 14, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.REAVER),
    ItemNames.REAVER_RESOURCE_EFFICIENCY: ItemData(345 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 15, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.REAVER),
    ItemNames.VANGUARD_AGONY_LAUNCHERS: ItemData(346 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 16, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.VANGUARD),
    ItemNames.VANGUARD_MATTER_DISPERSION: ItemData(347 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 17, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.VANGUARD),
    ItemNames.IMMORTAL_ANNIHILATOR_SINGULARITY_CHARGE: ItemData(348 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 18, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING_MECHANICS: ItemData(349 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 19, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.COLOSSUS_PACIFICATION_PROTOCOL: ItemData(350 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 20, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.COLOSSUS),
    ItemNames.WRATHWALKER_RAPID_POWER_CYCLING: ItemData(351 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 21, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.WRATHWALKER),
    ItemNames.WRATHWALKER_EYE_OF_WRATH: ItemData(352 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 22, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.WRATHWALKER),
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHROUD_OF_ADUN: ItemData(353 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 23, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHADOW_GUARD_TRAINING: ItemData(354 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 24, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_BLINK: ItemData(355 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 25, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_RESOURCE_EFFICIENCY: ItemData(356 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 26, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.DARK_TEMPLAR_DARK_ARCHON_MELD: ItemData(357 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 27, SC2Race.PROTOSS, origin={"bw"}, important_for_filtering=True ,parent_item=ItemNames.DARK_TEMPLAR),
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_UNSHACKLED_PSIONIC_STORM: ItemData(358 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 28, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_HALLUCINATION: ItemData(359 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 29, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}),
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_KHAYDARIN_AMULET: ItemData(360 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 0, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.ARCHON_HIGH_ARCHON: ItemData(361 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 1, SC2Race.PROTOSS, origin={"ext"}, important_for_filtering=True),
    ItemNames.DARK_ARCHON_FEEDBACK: ItemData(362 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 2, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.DARK_ARCHON_MAELSTROM: ItemData(363 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 3, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.DARK_ARCHON_ARGUS_TALISMAN: ItemData(364 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 4, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.ASCENDANT_POWER_OVERWHELMING: ItemData(365 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 5, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ASCENDANT),
    ItemNames.ASCENDANT_CHAOTIC_ATTUNEMENT: ItemData(366 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 6, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ASCENDANT),
    ItemNames.ASCENDANT_BLOOD_AMULET: ItemData(367 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 7, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ASCENDANT),
    ItemNames.SENTRY_ENERGIZER_HAVOC_CLOAKING_MODULE: ItemData(368 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 8, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.SENTRY_ENERGIZER_HAVOC_SHIELD_BATTERY_RAPID_RECHARGING: ItemData(369 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 9, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.SENTRY_FORCE_FIELD: ItemData(370 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 10, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SENTRY),
    ItemNames.SENTRY_HALLUCINATION: ItemData(371 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 11, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SENTRY),
    ItemNames.ENERGIZER_RECLAMATION: ItemData(372 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 12, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ENERGIZER),
    ItemNames.ENERGIZER_FORGED_CHASSIS: ItemData(373 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 13, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ENERGIZER),
    ItemNames.HAVOC_DETECT_WEAKNESS: ItemData(374 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 14, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.HAVOC),
    ItemNames.HAVOC_BLOODSHARD_RESONANCE: ItemData(375 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 15, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.HAVOC),
    ItemNames.ZEALOT_SENTINEL_CENTURION_LEG_ENHANCEMENTS: ItemData(376 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 16, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.ZEALOT_SENTINEL_CENTURION_SHIELD_CAPACITY: ItemData(377 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 17, SC2Race.PROTOSS, origin={"bw"}),

    # SoA Calldown powers
    ItemNames.SOA_CHRONO_SURGE: ItemData(700 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 0, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_PROGRESSIVE_PROXY_PYLON: ItemData(701 + SC2LOTV_ITEM_ID_OFFSET, "Progressive Upgrade", 0, SC2Race.PROTOSS, origin={"lotv"}, quantity=2),
    ItemNames.SOA_PYLON_OVERCHARGE: ItemData(702 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 1, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.SOA_ORBITAL_STRIKE: ItemData(703 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 2, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_TEMPORAL_FIELD: ItemData(704 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 3, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_SOLAR_LANCE: ItemData(705 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 4, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SOA_MASS_RECALL: ItemData(706 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 5, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_SHIELD_OVERCHARGE: ItemData(707 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 6, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_DEPLOY_FENIX: ItemData(708 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 7, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SOA_PURIFIER_BEAM: ItemData(709 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 8, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_TIME_STOP: ItemData(710 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 9, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SOA_SOLAR_BOMBARDMENT: ItemData(711 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 10, SC2Race.PROTOSS, origin={"lotv"}),

    # Generic Protoss Upgrades
    ItemNames.MATRIX_OVERLOAD:
        ItemData(800 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 0, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.QUATRO:
        ItemData(801 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 1, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.NEXUS_OVERCHARGE:
        ItemData(802 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 2, SC2Race.PROTOSS, origin={"lotv"}, important_for_filtering=True),
    ItemNames.ORBITAL_ASSIMILATORS:
        ItemData(803 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 3, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.WARP_HARMONIZATION:
        ItemData(804 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 4, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.GUARDIAN_SHELL:
        ItemData(805 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 5, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.RECONSTRUCTION_BEAM:
        ItemData(806 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 6, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.OVERWATCH:
        ItemData(807 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 7, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.SUPERIOR_WARP_GATES:
        ItemData(808 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 8, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.ENHANCED_TARGETING:
        ItemData(809 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 9, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.OPTIMIZED_ORDNANCE:
        ItemData(810 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 10, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.KHALAI_INGENUITY:
        ItemData(811 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 11, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.AMPLIFIED_ASSIMILATORS:
        ItemData(812 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 12, SC2Race.PROTOSS, origin={"ext"}),
}


def get_item_table():
    return item_table


basic_units = {
    SC2Race.TERRAN: {
        ItemNames.MARINE,
        ItemNames.MARAUDER,
        ItemNames.GOLIATH,
        ItemNames.HELLION,
        ItemNames.VULTURE,
        ItemNames.WARHOUND,
    },
    SC2Race.ZERG: {
        ItemNames.ZERGLING,
        ItemNames.SWARM_QUEEN,
        ItemNames.ROACH,
        ItemNames.HYDRALISK,
    },
    SC2Race.PROTOSS: {
        ItemNames.ZEALOT,
        ItemNames.CENTURION,
        ItemNames.SENTINEL,
        ItemNames.STALKER,
        ItemNames.INSTIGATOR,
        ItemNames.SLAYER,
        ItemNames.DRAGOON,
        ItemNames.ADEPT,
    }
}

advanced_basic_units = {
    SC2Race.TERRAN: basic_units[SC2Race.TERRAN].union({
        ItemNames.REAPER,
        ItemNames.DIAMONDBACK,
        ItemNames.VIKING,
        ItemNames.SIEGE_TANK,
        ItemNames.BANSHEE,
        ItemNames.THOR,
        ItemNames.BATTLECRUISER,
        ItemNames.CYCLONE
    }),
    SC2Race.ZERG: basic_units[SC2Race.ZERG].union({
        ItemNames.INFESTOR,
        ItemNames.ABERRATION,
    }),
    SC2Race.PROTOSS: basic_units[SC2Race.PROTOSS].union({
        ItemNames.DARK_TEMPLAR,
        ItemNames.BLOOD_HUNTER,
        ItemNames.AVENGER,
        ItemNames.IMMORTAL,
        ItemNames.ANNIHILATOR,
        ItemNames.VANGUARD,
    })
}

no_logic_starting_units = {
    SC2Race.TERRAN: advanced_basic_units[SC2Race.TERRAN].union({
        ItemNames.FIREBAT,
        ItemNames.GHOST,
        ItemNames.SPECTRE,
        ItemNames.WRAITH,
        ItemNames.RAVEN,
        ItemNames.PREDATOR,
        ItemNames.LIBERATOR,
        ItemNames.HERC,
    }),
    SC2Race.ZERG: advanced_basic_units[SC2Race.ZERG].union({
        ItemNames.ULTRALISK,
        ItemNames.SWARM_HOST
    }),
    SC2Race.PROTOSS: advanced_basic_units[SC2Race.PROTOSS].union({
        ItemNames.CARRIER,
        ItemNames.TEMPEST,
        ItemNames.VOID_RAY,
        ItemNames.DESTROYER,
        ItemNames.COLOSSUS,
        ItemNames.WRATHWALKER,
        ItemNames.SCOUT,
        ItemNames.HIGH_TEMPLAR,
        ItemNames.SIGNIFIER,
        ItemNames.ASCENDANT,
        ItemNames.DARK_ARCHON,
        ItemNames.SUPPLICANT,
    })
}

not_balanced_starting_units = {
    ItemNames.SIEGE_TANK,
    ItemNames.THOR,
    ItemNames.BANSHEE,
    ItemNames.BATTLECRUISER,
    ItemNames.ULTRALISK,
    ItemNames.CARRIER,
    ItemNames.TEMPEST,
}


def get_basic_units(world: World, race: SC2Race) -> typing.Set[str]:
    logic_level = get_option_value(world, 'required_tactics')
    if logic_level == RequiredTactics.option_no_logic:
        return no_logic_starting_units[race]
    elif logic_level == RequiredTactics.option_advanced:
        return advanced_basic_units[race]
    else:
        return basic_units[race]


# Items that can be placed before resources if not already in
# General upgrades and Mercs
second_pass_placeable_items: typing.Tuple[str, ...] = (
    # Global weapon/armor upgrades
    ItemNames.PROGRESSIVE_TERRAN_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_UPGRADE,
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_ZERG_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_ZERG_WEAPON_UPGRADE,
    ItemNames.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE,
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_PROTOSS_SHIELDS,
    # Terran Buildings without upgrades
    ItemNames.SENSOR_TOWER,
    ItemNames.HIVE_MIND_EMULATOR,
    ItemNames.PSI_DISRUPTER,
    ItemNames.PERDITION_TURRET,
    # Terran units without upgrades
    ItemNames.HERC,
    ItemNames.WARHOUND,
    # General Terran upgrades without any dependencies
    ItemNames.SCV_ADVANCED_CONSTRUCTION,
    ItemNames.SCV_DUAL_FUSION_WELDERS,
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,
    ItemNames.PROGRESSIVE_ORBITAL_COMMAND,
    ItemNames.ULTRA_CAPACITORS,
    ItemNames.VANADIUM_PLATING,
    ItemNames.ORBITAL_DEPOTS,
    ItemNames.MICRO_FILTERING,
    ItemNames.AUTOMATED_REFINERY,
    ItemNames.COMMAND_CENTER_REACTOR,
    ItemNames.TECH_REACTOR,
    ItemNames.CELLULAR_REACTOR,
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL,  # Place only L1
    ItemNames.STRUCTURE_ARMOR,
    ItemNames.HI_SEC_AUTO_TRACKING,
    ItemNames.ADVANCED_OPTICS,
    ItemNames.ROGUE_FORCES,
    # Mercenaries (All races)
    *[item_name for item_name, item_data in get_full_item_list().items()
      if item_data.type == "Mercenary"],
    # Kerrigan and Nova levels, abilities and generally useful stuff
    *[item_name for item_name, item_data in get_full_item_list().items()
      if item_data.type in ("Level", "Ability", "Evolution Pit", "Nova Gear")],
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE,
    # Zerg static defenses
    ItemNames.SPORE_CRAWLER,
    ItemNames.SPINE_CRAWLER,
    # Defiler, Aberration (no upgrades)
    ItemNames.DEFILER,
    ItemNames.ABERRATION,
    # Spear of Adun Abilities
    ItemNames.SOA_CHRONO_SURGE,
    ItemNames.SOA_PROGRESSIVE_PROXY_PYLON,
    ItemNames.SOA_PYLON_OVERCHARGE,
    ItemNames.SOA_ORBITAL_STRIKE,
    ItemNames.SOA_TEMPORAL_FIELD,
    ItemNames.SOA_SOLAR_LANCE,
    ItemNames.SOA_MASS_RECALL,
    ItemNames.SOA_SHIELD_OVERCHARGE,
    ItemNames.SOA_DEPLOY_FENIX,
    ItemNames.SOA_PURIFIER_BEAM,
    ItemNames.SOA_TIME_STOP,
    ItemNames.SOA_SOLAR_BOMBARDMENT,
    # Protoss generic upgrades
    ItemNames.MATRIX_OVERLOAD,
    ItemNames.QUATRO,
    ItemNames.NEXUS_OVERCHARGE,
    ItemNames.ORBITAL_ASSIMILATORS,
    ItemNames.WARP_HARMONIZATION,
    ItemNames.GUARDIAN_SHELL,
    ItemNames.RECONSTRUCTION_BEAM,
    ItemNames.OVERWATCH,
    ItemNames.SUPERIOR_WARP_GATES,
    ItemNames.KHALAI_INGENUITY,
    ItemNames.AMPLIFIED_ASSIMILATORS,
    # Protoss static defenses
    ItemNames.PHOTON_CANNON,
    ItemNames.KHAYDARIN_MONOLITH,
    ItemNames.SHIELD_BATTERY
)


filler_items: typing.Tuple[str, ...] = (
    ItemNames.STARTING_MINERALS,
    ItemNames.STARTING_VESPENE,
    ItemNames.STARTING_SUPPLY,
)

# Defense rating table
# Commented defense ratings are handled in LogicMixin
defense_ratings = {
    ItemNames.SIEGE_TANK: 5,
    # "Maelstrom Rounds": 2,
    ItemNames.PLANETARY_FORTRESS: 3,
    # Bunker w/ Marine/Marauder: 3,
    ItemNames.PERDITION_TURRET: 2,
    ItemNames.VULTURE: 1,
    ItemNames.BANSHEE: 1,
    ItemNames.BATTLECRUISER: 1,
    ItemNames.LIBERATOR: 4,
    ItemNames.WIDOW_MINE: 1,
    # "Concealment (Widow Mine)": 1
}
zerg_defense_ratings = {
    ItemNames.PERDITION_TURRET: 2,
    # Bunker w/ Firebat: 2,
    ItemNames.LIBERATOR: -2,
    ItemNames.HIVE_MIND_EMULATOR: 3,
    ItemNames.PSI_DISRUPTER: 3,
}
air_defense_ratings = {
    ItemNames.MISSILE_TURRET: 2,
}

kerrigan_levels = [item_name for item_name, item_data in get_full_item_list().items()
                        if item_data.type == "Level" and item_data.race == SC2Race.ZERG]

spider_mine_sources = {
    ItemNames.VULTURE,
    ItemNames.REAPER_SPIDER_MINES,
    ItemNames.SIEGE_TANK_SPIDER_MINES,
    ItemNames.RAVEN_SPIDER_MINES,
}

progressive_if_nco = {
    ItemNames.MARINE_PROGRESSIVE_STIMPACK,
    ItemNames.FIREBAT_PROGRESSIVE_STIMPACK,
    ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS,
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL,
}

progressive_if_ext = {
    ItemNames.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE,
    ItemNames.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS,
    ItemNames.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX,
    ItemNames.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS,
    ItemNames.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL,
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,
    ItemNames.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL
}

kerrigan_actives: typing.List[typing.Set[str]] = [
    {ItemNames.KERRIGAN_KINETIC_BLAST, ItemNames.KERRIGAN_LEAPING_STRIKE},
    {ItemNames.KERRIGAN_CRUSHING_GRIP, ItemNames.KERRIGAN_PSIONIC_SHIFT},
    set(),
    {ItemNames.KERRIGAN_WILD_MUTATION, ItemNames.KERRIGAN_SPAWN_BANELINGS, ItemNames.KERRIGAN_MEND},
    set(),
    set(),
    {ItemNames.KERRIGAN_APOCALYPSE, ItemNames.KERRIGAN_SPAWN_LEVIATHAN, ItemNames.KERRIGAN_DROP_PODS},
]

kerrigan_passives: typing.List[typing.Set[str]] = [
    {ItemNames.KERRIGAN_HEROIC_FORTITUDE},
    {ItemNames.KERRIGAN_CHAIN_REACTION},
    {ItemNames.KERRIGAN_ZERGLING_RECONSTITUTION, ItemNames.KERRIGAN_IMPROVED_OVERLORDS, ItemNames.KERRIGAN_AUTOMATED_EXTRACTORS},
    set(),
    {ItemNames.KERRIGAN_TWIN_DRONES, ItemNames.KERRIGAN_MALIGNANT_CREEP, ItemNames.KERRIGAN_VESPENE_EFFICIENCY},
    {ItemNames.KERRIGAN_INFEST_BROODLINGS, ItemNames.KERRIGAN_FURY, ItemNames.KERRIGAN_ABILITY_EFFICIENCY},
    set(),
]

kerrigan_only_passives = {
    ItemNames.KERRIGAN_HEROIC_FORTITUDE, ItemNames.KERRIGAN_CHAIN_REACTION,
    ItemNames.KERRIGAN_INFEST_BROODLINGS, ItemNames.KERRIGAN_FURY, ItemNames.KERRIGAN_ABILITY_EFFICIENCY,
}

spear_of_adun_calldowns = {
    ItemNames.SOA_CHRONO_SURGE,
    ItemNames.SOA_PROGRESSIVE_PROXY_PYLON,
    ItemNames.SOA_PYLON_OVERCHARGE,
    ItemNames.SOA_ORBITAL_STRIKE,
    ItemNames.SOA_TEMPORAL_FIELD,
    ItemNames.SOA_SOLAR_LANCE,
    ItemNames.SOA_MASS_RECALL,
    ItemNames.SOA_SHIELD_OVERCHARGE,
    ItemNames.SOA_DEPLOY_FENIX,
    ItemNames.SOA_PURIFIER_BEAM,
    ItemNames.SOA_TIME_STOP,
    ItemNames.SOA_SOLAR_BOMBARDMENT
}

spear_of_adun_castable_passives = {
    ItemNames.RECONSTRUCTION_BEAM,
    ItemNames.OVERWATCH,
}

nova_equipment = {
    *[item_name for item_name, item_data in get_full_item_list().items()
      if item_data.type == "Nova Gear"],
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE
}

# 'number' values of upgrades for upgrade bundle items
upgrade_numbers = [
    # Terran
    {0, 4, 8}, # Weapon
    {2, 6, 10}, # Armor
    {0, 2}, # Infantry
    {4, 6}, # Vehicle
    {8, 10}, # Starship
    {0, 2, 4, 6, 8, 10}, # All
    # Zerg
    {0, 2, 6}, # Weapon
    {4, 8}, # Armor
    {0, 2, 4}, # Ground
    {6, 8}, # Flyer
    {0, 2, 4, 6, 8}, # All
    # Protoss
    {0, 6}, # Weapon
    {2, 4, 8}, # Armor
    {0, 2}, # Ground, Shields are handled specially
    {6, 8}, # Air, Shields are handled specially
    {0, 2, 4, 6, 8}, # All
]
# 'upgrade_numbers' indices for all upgrades
upgrade_numbers_all = {
    SC2Race.TERRAN: 5,
    SC2Race.ZERG: 10,
    SC2Race.PROTOSS: 15,
}

# Names of upgrades to be included for different options
upgrade_included_names = [
    { # Individual Items
        ItemNames.PROGRESSIVE_TERRAN_INFANTRY_WEAPON,
        ItemNames.PROGRESSIVE_TERRAN_INFANTRY_ARMOR,
        ItemNames.PROGRESSIVE_TERRAN_VEHICLE_WEAPON,
        ItemNames.PROGRESSIVE_TERRAN_VEHICLE_ARMOR,
        ItemNames.PROGRESSIVE_TERRAN_SHIP_WEAPON,
        ItemNames.PROGRESSIVE_TERRAN_SHIP_ARMOR,
        ItemNames.PROGRESSIVE_ZERG_MELEE_ATTACK,
        ItemNames.PROGRESSIVE_ZERG_MISSILE_ATTACK,
        ItemNames.PROGRESSIVE_ZERG_GROUND_CARAPACE,
        ItemNames.PROGRESSIVE_ZERG_FLYER_ATTACK,
        ItemNames.PROGRESSIVE_ZERG_FLYER_CARAPACE,
        ItemNames.PROGRESSIVE_PROTOSS_GROUND_WEAPON,
        ItemNames.PROGRESSIVE_PROTOSS_GROUND_ARMOR,
        ItemNames.PROGRESSIVE_PROTOSS_SHIELDS,
        ItemNames.PROGRESSIVE_PROTOSS_AIR_WEAPON,
        ItemNames.PROGRESSIVE_PROTOSS_AIR_ARMOR,
    },
    { # Bundle Weapon And Armor
        ItemNames.PROGRESSIVE_TERRAN_WEAPON_UPGRADE,
        ItemNames.PROGRESSIVE_TERRAN_ARMOR_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_WEAPON_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_ARMOR_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE,
    },
    { # Bundle Unit Class
        ItemNames.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE,
        ItemNames.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE,
        ItemNames.PROGRESSIVE_TERRAN_SHIP_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_GROUND_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_FLYER_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_GROUND_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_AIR_UPGRADE,
    },
    { # Bundle All
        ItemNames.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE,
    }
]

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in get_full_item_list().items() if
                                            data.code}

# Map type to expected int
type_flaggroups: typing.Dict[SC2Race, typing.Dict[str, int]] = {
    SC2Race.ANY: {
        "Minerals": 0,
        "Vespene": 1,
        "Supply": 2,
        "Goal": 3,
        "Nothing Group": 4,
    },
    SC2Race.TERRAN: {
        "Armory 1": 0,
        "Armory 2": 1,
        "Armory 3": 2,
        "Armory 4": 3,
        "Armory 5": 4,
        "Armory 6": 5,
        "Progressive Upgrade": 6,  # Unit upgrades that exist multiple times (Stimpack / Super Stimpack)
        "Laboratory": 7,
        "Upgrade": 8,  # Weapon / Armor upgrades
        "Unit": 9,
        "Building": 10,
        "Mercenary": 11,
        "Nova Gear": 12,
        "Progressive Upgrade 2": 13,
    },
    SC2Race.ZERG: {
        "Ability": 0,
        "Mutation 1": 1,
        "Strain": 2,
        "Morph": 3,
        "Upgrade": 4,
        "Mercenary": 5,
        "Unit": 6,
        "Level": 7,
        "Primal Form": 8,
        "Evolution Pit": 9,
        "Mutation 2": 10,
        "Mutation 3": 11
    },
    SC2Race.PROTOSS: {
        "Unit": 0,
        "Unit 2": 1,
        "Upgrade": 2,  # Weapon / Armor upgrades
        "Building": 3,
        "Progressive Upgrade": 4,
        "Spear of Adun": 5,
        "Solarite Core": 6,
        "Forge 1": 7,
        "Forge 2": 8,
        "Forge 3": 9,
    }
}
