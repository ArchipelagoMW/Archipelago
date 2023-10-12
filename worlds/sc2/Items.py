from BaseClasses import Item, ItemClassification, MultiWorld
import typing

from .Options import get_option_value, RequiredTactics
from .MissionTables import SC2Mission, SC2Race, SC2Campaign, campaign_mission_table
from . import ItemNames

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: str
    number: int
    race: SC2Race
    classification: ItemClassification = ItemClassification.useful
    quantity: int = 1
    parent_item: typing.Optional[str] = None
    origin: typing.Set[str] = {"wol"}


class StarcraftItem(Item):
    game: str = "Starcraft 2"


def get_full_item_list():
    return item_table


SC2WOL_ITEM_ID_OFFSET = 1000
SC2HOTS_ITEM_ID_OFFSET = SC2WOL_ITEM_ID_OFFSET + 900

item_table = {
    # WoL
    ItemNames.Marine: ItemData(0 + SC2WOL_ITEM_ID_OFFSET, "Unit", 0, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Medic: ItemData(1 + SC2WOL_ITEM_ID_OFFSET, "Unit", 1, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Firebat: ItemData(2 + SC2WOL_ITEM_ID_OFFSET, "Unit", 2, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Marauder: ItemData(3 + SC2WOL_ITEM_ID_OFFSET, "Unit", 3, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Reaper: ItemData(4 + SC2WOL_ITEM_ID_OFFSET, "Unit", 4, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Hellion: ItemData(5 + SC2WOL_ITEM_ID_OFFSET, "Unit", 5, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Vulture: ItemData(6 + SC2WOL_ITEM_ID_OFFSET, "Unit", 6, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Goliath: ItemData(7 + SC2WOL_ITEM_ID_OFFSET, "Unit", 7, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Diamondback: ItemData(8 + SC2WOL_ITEM_ID_OFFSET, "Unit", 8, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Siege_Tank: ItemData(9 + SC2WOL_ITEM_ID_OFFSET, "Unit", 9, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Medivac: ItemData(10 + SC2WOL_ITEM_ID_OFFSET, "Unit", 10, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Wraith: ItemData(11 + SC2WOL_ITEM_ID_OFFSET, "Unit", 11, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Viking: ItemData(12 + SC2WOL_ITEM_ID_OFFSET, "Unit", 12, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Banshee: ItemData(13 + SC2WOL_ITEM_ID_OFFSET, "Unit", 13, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Battlecruiser: ItemData(14 + SC2WOL_ITEM_ID_OFFSET, "Unit", 14, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Ghost: ItemData(15 + SC2WOL_ITEM_ID_OFFSET, "Unit", 15, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Spectre: ItemData(16 + SC2WOL_ITEM_ID_OFFSET, "Unit", 16, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Thor: ItemData(17 + SC2WOL_ITEM_ID_OFFSET, "Unit", 17, SC2Race.TERRAN, classification=ItemClassification.progression),
    # EE units
    ItemNames.Liberator: ItemData(18 + SC2WOL_ITEM_ID_OFFSET, "Unit", 18, SC2Race.TERRAN, classification=ItemClassification.progression, origin={"nco", "ext"}),
    ItemNames.Valkyrie: ItemData(19 + SC2WOL_ITEM_ID_OFFSET, "Unit", 19, SC2Race.TERRAN, classification=ItemClassification.progression, origin={"bw"}),
    ItemNames.Widow_Mine: ItemData(20 + SC2WOL_ITEM_ID_OFFSET, "Unit", 20, SC2Race.TERRAN, classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.Cyclone: ItemData(21 + SC2WOL_ITEM_ID_OFFSET, "Unit", 21, SC2Race.TERRAN, classification=ItemClassification.progression, origin={"ext"}),

    # Some other items are moved to Upgrade group because of the way how the bot message is parsed
    ItemNames.Progressive_Terran_Infantry_Weapon: ItemData(100 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Infantry_Armor: ItemData(102 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Vehicle_Weapon: ItemData(103 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Vehicle_Armor: ItemData(104 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Ship_Weapon: ItemData(105 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Ship_Armor: ItemData(106 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 10, SC2Race.TERRAN, quantity=3),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    ItemNames.Progressive_Terran_Weapon_Upgrade: ItemData(107 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Armor_Upgrade: ItemData(108 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 1, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Infantry_Upgrade: ItemData(109 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Vehicle_Upgrade: ItemData(110 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 3, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Ship_Upgrade: ItemData(111 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.TERRAN, quantity=3),
    ItemNames.Progressive_Terran_Weapon_Armor_Upgrade: ItemData(112 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 5, SC2Race.TERRAN, quantity=3),

    ItemNames.Bunker_Projectile_Accelerator: ItemData(200 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 0, SC2Race.TERRAN, parent_item="Bunker"),
    ItemNames.Bunker_Neosteel_Bunker: ItemData(201 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 1, SC2Race.TERRAN, parent_item="Bunker"),
    ItemNames.Missile_Turret_Titanium_Housing: ItemData(202 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 2, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Missile Turret"),
    ItemNames.Missile_Turret_Hellstorm_Batteries: ItemData(203 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 3, SC2Race.TERRAN, parent_item="Missile Turret"),
    ItemNames.SCV_Advanced_Construction: ItemData(204 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 4, SC2Race.TERRAN),
    ItemNames.SCV_Dual_Fusion_Welders: ItemData(205 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 5, SC2Race.TERRAN),
    ItemNames.Building_Fire_Suppression_System: ItemData(206 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 6, SC2Race.TERRAN),
    ItemNames.Building_Orbital_Command: ItemData(207 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 7, SC2Race.TERRAN),
    ItemNames.Marine_Progressive_Stimpack: ItemData(208 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 0, SC2Race.TERRAN, parent_item="Marine", quantity=2),
    ItemNames.Marine_Combat_Shield: ItemData(209 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 9, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Marine"),
    ItemNames.Medic_Advanced_Medic_Facilities: ItemData(210 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 10, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Medic"),
    ItemNames.Medic_Stabilizer_Medpacks: ItemData(211 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 11, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Medic"),
    ItemNames.Firebat_Incinerator_Gauntlets: ItemData(212 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 12, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Firebat"),
    ItemNames.Firebat_Juggernaut_Plating: ItemData(213 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 13, SC2Race.TERRAN, parent_item="Firebat"),
    ItemNames.Marauder_Concussive_Shells: ItemData(214 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 14, SC2Race.TERRAN, parent_item="Marauder"),
    ItemNames.Marauder_Kinetic_Foam: ItemData(215 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 15, SC2Race.TERRAN, parent_item="Marauder"),
    ItemNames.Reaper_U238_Rounds: ItemData(216 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 16, SC2Race.TERRAN, parent_item="Reaper"),
    ItemNames.Reaper_G4_Clusterbomb: ItemData(217 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 17, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Reaper"),
    # Items from EE
    ItemNames.Cyclone_Mag_Field_Accelerators: ItemData(218 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 18, SC2Race.TERRAN, parent_item="Cyclone", origin={"ext"}),
    ItemNames.Cyclone_Mag_Field_Launchers: ItemData(219 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 19, SC2Race.TERRAN, parent_item="Cyclone", origin={"ext"}),
    # Items from new mod
    ItemNames.Marine_Laser_Targeting_System: ItemData(220 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 8, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Marine", origin={"nco"}), # Freed slot from Stimpack
    ItemNames.Marine_Magrail_Munitions: ItemData(221 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 20, SC2Race.TERRAN, parent_item="Marine", origin={"nco"}),
    ItemNames.Marine_Optimized_Logistics: ItemData(222 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 21, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Marine", origin={"nco"}),
    ItemNames.Medic_Restoration: ItemData(223 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 22, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Medic", origin={"bw"}),
    ItemNames.Medic_Optical_Flare: ItemData(224 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 23, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Medic", origin={"bw"}),
    ItemNames.Medic_Optimized_Logistics: ItemData(225 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 24, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Medic", origin={"bw"}),
    ItemNames.Firebat_Progressive_Stimpack: ItemData(226 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 6, SC2Race.TERRAN, parent_item="Firebat", quantity=2, origin={"bw"}),
    ItemNames.Firebat_Optimized_Logistics: ItemData(227 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 25, SC2Race.TERRAN, parent_item="Firebat", origin={"bw"}),
    ItemNames.Marauder_Progressive_Stimpack: ItemData(228 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 8, SC2Race.TERRAN, parent_item="Marauder", quantity=2, origin={"nco"}),
    ItemNames.Marauder_Laser_Targeting_System: ItemData(229 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 26, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Marauder", origin={"nco"}),
    ItemNames.Marauder_Magrail_Munitions: ItemData(230 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 27, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Marauder", origin={"nco"}),
    ItemNames.Marauder_Internal_Tech_Module: ItemData(231 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 28, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Marauder", origin={"nco"}),

    # Items from new mod
    ItemNames.Reaper_Progressive_Stimpack: ItemData(250 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 10, SC2Race.TERRAN, parent_item="Reaper", quantity=2, origin={"nco"}),
    ItemNames.Reaper_Laser_Targeting_System: ItemData(251 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 0, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Reaper", origin={"nco"}),
    ItemNames.Reaper_Advanced_Cloaking_Field: ItemData(252 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 1, SC2Race.TERRAN, parent_item="Reaper", origin={"nco"}),
    ItemNames.Reaper_Spider_Mines: ItemData(253 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 2, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Reaper", origin={"nco"}),
    ItemNames.Reaper_Combat_Drugs: ItemData(254 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 3, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Reaper", origin={"ext"}),
    ItemNames.Hellion_Hellbat_Aspect: ItemData(255 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 4, SC2Race.TERRAN, parent_item="Hellion", origin={"nco"}),
    ItemNames.Hellion_Smart_Servos: ItemData(256 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 5, SC2Race.TERRAN, parent_item="Hellion", origin={"nco"}),
    ItemNames.Hellion_Optimized_Logistics: ItemData(257 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 6, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Hellion", origin={"nco"}),
    ItemNames.Hellion_Jump_Jets: ItemData(258 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 7, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Hellion", origin={"nco"}),
    ItemNames.Hellion_Progressive_Stimpack: ItemData(259 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 12, SC2Race.TERRAN, parent_item="Hellion", quantity=2, origin={"nco"}),
    ItemNames.Vulture_Ion_Thrusters: ItemData(260 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 8, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Vulture", origin={"bw"}),
    ItemNames.Vulture_Auto_Launchers: ItemData(261 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 9, SC2Race.TERRAN, parent_item="Vulture", origin={"bw"}),
    ItemNames.Spider_Mine_High_Explosive_Munition: ItemData(262 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 10, SC2Race.TERRAN, origin={"bw"}),
    ItemNames.Goliath_Jump_Jets: ItemData(263 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 11, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Goliath", origin={"nco"}),
    ItemNames.Goliath_Optimized_Logistics: ItemData(264 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 12, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Goliath", origin={"nco"}),
    ItemNames.Diamondback_Hyperfluxor: ItemData(265 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 13, SC2Race.TERRAN, parent_item="Diamondback", origin={"ext"}),
    ItemNames.Diamondback_Burst_Capacitors: ItemData(266 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 14, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Diamondback", origin={"ext"}),
    ItemNames.Diamondback_Optimized_Logistics: ItemData(267 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 15, SC2Race.TERRAN, parent_item="Diamondback", origin={"ext"}),
    ItemNames.Siege_Tank_Jump_Jets: ItemData(268 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 16, SC2Race.TERRAN, parent_item="Siege Tank", origin={"nco"}),
    ItemNames.Siege_Tank_Spider_Mines: ItemData(269 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 17, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Siege Tank", origin={"nco"}),
    ItemNames.Siege_Tank_Smart_Servos: ItemData(270 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 18, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Siege Tank", origin={"nco"}),
    ItemNames.Siege_Tank_Graduating_Range: ItemData(271 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 19, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Siege Tank", origin={"ext"}),
    ItemNames.Siege_Tank_Laser_Targeting_System: ItemData(272 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 20, SC2Race.TERRAN, parent_item="Siege Tank", origin={"nco"}),
    ItemNames.Siege_Tank_Advanced_Siege_Tech: ItemData(273 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 21, SC2Race.TERRAN, parent_item="Siege Tank", origin={"ext"}),
    ItemNames.Siege_Tank_Internal_Tech_Module: ItemData(274 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 22, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Siege Tank", origin={"nco"}),
    ItemNames.Predator_Optimized_Logistics: ItemData(275 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 23, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Predator", origin={"ext"}),
    ItemNames.Medivac_Expanded_Hull: ItemData(276 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 24, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Medivac", origin={"ext"}),
    ItemNames.Medivac_Afterburners: ItemData(277 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 25, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Medivac", origin={"ext"}),
    ItemNames.Wraith_Advanced_Laser_Technology: ItemData(278 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 26, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Wraith", origin={"ext"}),
    ItemNames.Viking_Smart_Servos: ItemData(279 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 27, SC2Race.TERRAN, parent_item="Viking", origin={"ext"}),
    ItemNames.Viking_Magrail_Munitions: ItemData(280 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 28, SC2Race.TERRAN, parent_item="Viking", origin={"ext"}),

    ItemNames.Hellion_Twin_Linked_Flamethrower: ItemData(300 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 0, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Hellion"),
    ItemNames.Hellion_Thermite_Filaments: ItemData(301 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 1, SC2Race.TERRAN, parent_item="Hellion"),
    ItemNames.Spider_Mine_Cerberus_Mine: ItemData(302 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 2, SC2Race.TERRAN, classification=ItemClassification.filler),
    ItemNames.Vulture_Replenishable_Magazine: ItemData(303 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 3, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Vulture"),
    ItemNames.Goliath_Multi_Lock_Weapons_System: ItemData(304 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 4, SC2Race.TERRAN, parent_item="Goliath"),
    ItemNames.Goliath_Ares_Class_Targeting_System: ItemData(305 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 5, SC2Race.TERRAN, parent_item="Goliath"),
    ItemNames.Diamondback_Tri_Lithium_Power_Cell: ItemData(306 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 6, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Diamondback"),
    ItemNames.Diamondback_Shaped_Hull: ItemData(307 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 7, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Diamondback"),
    ItemNames.Siege_Tank_Maelstrom_Rounds: ItemData(308 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 8, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Siege Tank"),
    ItemNames.Siege_Tank_Shaped_Blast: ItemData(309 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 9, SC2Race.TERRAN, parent_item="Siege Tank"),
    ItemNames.Medivac_Rapid_Deployment_Tube: ItemData(310 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 10, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Medivac"),
    ItemNames.Medivac_Advanced_Healing_AI: ItemData(311 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 11, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Medivac"),
    ItemNames.Wraith_Tomahawk_Power_Cells: ItemData(312 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 12, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Wraith"),
    ItemNames.Wraith_Displacement_Field: ItemData(313 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 13, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Wraith"),
    ItemNames.Viking_Ripwave_Missiles: ItemData(314 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 14, SC2Race.TERRAN, parent_item="Viking"),
    ItemNames.Viking_Phobos_Class_Weapons_System: ItemData(315 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 15, SC2Race.TERRAN, parent_item="Viking"),
    ItemNames.Banshee_Progressive_Cross_Spectrum_Dampeners: ItemData(316 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 2, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Banshee", quantity=2),
    ItemNames.Banshee_Shockwave_Missile_Battery: ItemData(317 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 17, SC2Race.TERRAN, parent_item="Banshee"),
    ItemNames.Battlecruiser_Missile_Pods: ItemData(318 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 18, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Battlecruiser"),
    ItemNames.Battlecruiser_Defensive_Matrix: ItemData(319 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 19, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Battlecruiser"),
    ItemNames.Ghost_Ocular_Implants: ItemData(320 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 20, SC2Race.TERRAN, parent_item="Ghost"),
    ItemNames.Ghost_Crius_Suit: ItemData(321 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 21, SC2Race.TERRAN, parent_item="Ghost"),
    ItemNames.Spectre_Psionic_Lash: ItemData(322 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 22, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Spectre"),
    ItemNames.Spectre_Nyx_Class_Cloaking_Module: ItemData(323 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 23, SC2Race.TERRAN, parent_item="Spectre"),
    ItemNames.Thor_330mm_Barrage_Cannon: ItemData(324 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 24, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Thor"),
    ItemNames.Thor_Immortality_Protocol: ItemData(325 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 25, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Thor"),
    # Items from EE
    ItemNames.Liberator_Advanced_Ballistics: ItemData(326 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 26, SC2Race.TERRAN, parent_item="Liberator", origin={"ext"}),
    ItemNames.Liberator_Raid_Artillery: ItemData(327 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 27, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Liberator", origin={"nco"}),
    ItemNames.Widow_Mine_Drilling_Claws: ItemData(328 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 28, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Widow Mine", origin={"ext"}),
    ItemNames.Widow_Mine_Concealment: ItemData(329 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 29, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Widow Mine", origin={"ext"}),

    #Items from new mod
    ItemNames.Banshee_Hyperflight_Rotors: ItemData(350 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 0, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Banshee", origin={"ext"}),
    ItemNames.Banshee_Laser_Targeting_System: ItemData(351 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 1, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Banshee", origin={"nco"}),
    ItemNames.Banshee_Internal_Tech_Module: ItemData(352 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 2, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Banshee", origin={"nco"}),
    ItemNames.Battlecruiser_Tactical_Jump: ItemData(353 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 3, SC2Race.TERRAN, parent_item="Battlecruiser", origin={"nco", "ext"}),
    ItemNames.Battlecruiser_Cloak: ItemData(354 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 4, SC2Race.TERRAN, parent_item="Battlecruiser", origin={"nco"}),
    ItemNames.Battlecruiser_ATX_Laser_Battery: ItemData(355 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 5, SC2Race.TERRAN, classification=ItemClassification.progression, parent_item="Battlecruiser", origin={"nco"}),
    ItemNames.Battlecruiser_Optimized_Logistics: ItemData(356 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 6, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Battlecruiser", origin={"ext"}),
    ItemNames.Battlecruiser_Internal_Tech_Module: ItemData(357 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 7, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Battlecruiser", origin={"nco"}),
    ItemNames.Ghost_EMP_Rounds: ItemData(358 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 8, SC2Race.TERRAN, parent_item="Ghost", origin={"ext"}),
    ItemNames.Ghost_Lockdown: ItemData(359 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 9, SC2Race.TERRAN, parent_item="Ghost", origin={"bw"}),
    ItemNames.Spectre_Impaler_Rounds: ItemData(360 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 10, SC2Race.TERRAN, parent_item="Spectre", origin={"ext"}),
    ItemNames.Thor_Progressive_High_Impact_Payload: ItemData(361 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 14, SC2Race.TERRAN, parent_item="Thor", quantity=2, origin={"ext"}),  # L2 is Smart Servos
    ItemNames.Raven_Bio_Mechanical_Repair_Drone: ItemData(363 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 13, SC2Race.TERRAN, parent_item="Raven", origin={"nco"}),
    ItemNames.Raven_Spider_Mines: ItemData(364 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 14, SC2Race.TERRAN, parent_item="Raven", origin={"nco"}),
    ItemNames.Raven_Railgun_Turret: ItemData(365 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 15, SC2Race.TERRAN, parent_item="Raven", origin={"nco"}),
    ItemNames.Raven_Hunter_Seeker_Weapon: ItemData(366 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 16, SC2Race.TERRAN, parent_item="Raven", origin={"nco"}),
    ItemNames.Raven_Interference_Matrix: ItemData(367 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 17, SC2Race.TERRAN, parent_item="Raven", origin={"ext"}),
    ItemNames.Raven_Anti_Armor_Missile: ItemData(368 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 18, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Raven", origin={"ext"}),
    ItemNames.Raven_Internal_Tech_Module: ItemData(369 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 19, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Raven", origin={"nco"}),
    ItemNames.Science_Vessel_EMP_Shockwave: ItemData(370 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 20, SC2Race.TERRAN, parent_item="Science Vessel", origin={"bw"}),
    ItemNames.Science_Vessel_Defensive_Matrix: ItemData(371 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 21, SC2Race.TERRAN, parent_item="Science Vessel", origin={"bw"}),
    ItemNames.Cyclone_Targeting_Optics: ItemData(372 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 22, SC2Race.TERRAN, parent_item="Cyclone", origin={"ext"}),
    ItemNames.Cyclone_Rapid_Fire_Launchers: ItemData(373 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 23, SC2Race.TERRAN, parent_item="Cyclone", origin={"ext"}),
    ItemNames.Liberator_Cloak: ItemData(374 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 24, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Liberator", origin={"nco"}),
    ItemNames.Liberator_Laser_Targeting_System: ItemData(375 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 25, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Liberator", origin={"ext"}),
    ItemNames.Liberator_Optimized_Logistics: ItemData(376 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 26, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Liberator", origin={"nco"}),
    ItemNames.Widow_Mine_Black_Market_Launchers: ItemData(377 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 27, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Widow Mine", origin={"ext"}),
    ItemNames.Widow_Mine_Executioner_Missiles: ItemData(378 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 28, SC2Race.TERRAN, parent_item="Widow Mine", origin={"ext"}),

    # Just lazy to create a new group for one unit
    ItemNames.Valkyrie_Enhanced_Cluster_Launchers: ItemData(379 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 17, SC2Race.TERRAN, parent_item="Valkyrie", origin={"ext"}),
    ItemNames.Valkyrie_Shaped_Hull: ItemData(380 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 20, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Valkyrie", origin={"ext"}),
    ItemNames.Valkyrie_Burst_Lasers: ItemData(381 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 21, SC2Race.TERRAN, parent_item="Valkyrie", origin={"ext"}),
    ItemNames.Valkyrie_Afterburners: ItemData(382 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 22, SC2Race.TERRAN, classification=ItemClassification.filler, parent_item="Valkyrie", origin={"ext"}),

    ItemNames.Bunker: ItemData(400 + SC2WOL_ITEM_ID_OFFSET, "Building", 0, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Missile_Turret: ItemData(401 + SC2WOL_ITEM_ID_OFFSET, "Building", 1, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Sensor_Tower: ItemData(402 + SC2WOL_ITEM_ID_OFFSET, "Building", 2, SC2Race.TERRAN),

    ItemNames.War_Pigs: ItemData(500 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 0, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Devil_Dogs: ItemData(501 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 1, SC2Race.TERRAN, classification=ItemClassification.filler),
    ItemNames.Hammer_Securities: ItemData(502 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 2, SC2Race.TERRAN),
    ItemNames.Spartan_Company: ItemData(503 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 3, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Siege_Breakers: ItemData(504 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 4, SC2Race.TERRAN),
    ItemNames.Hels_Angel: ItemData(505 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 5, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Dusk_Wings: ItemData(506 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 6, SC2Race.TERRAN),
    ItemNames.Jacksons_Revenge: ItemData(507 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 7, SC2Race.TERRAN),

    ItemNames.Ultra_Capacitors: ItemData(600 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 0, SC2Race.TERRAN),
    ItemNames.Vanadium_Plating: ItemData(601 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 1, SC2Race.TERRAN),
    ItemNames.Orbital_Depots: ItemData(602 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 2, SC2Race.TERRAN),
    ItemNames.Micro_Filtering: ItemData(603 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 3, SC2Race.TERRAN),
    ItemNames.Automated_Refinery: ItemData(604 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 4, SC2Race.TERRAN),
    ItemNames.Command_Center_Reactor: ItemData(605 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 5, SC2Race.TERRAN),
    ItemNames.Raven: ItemData(606 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 6, SC2Race.TERRAN),
    ItemNames.Science_Vessel: ItemData(607 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 7, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Tech_Reactor: ItemData(608 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 8, SC2Race.TERRAN),
    ItemNames.Orbital_Strike: ItemData(609 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 9, SC2Race.TERRAN),
    ItemNames.Bunker_Shrike_Turret: ItemData(610 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 10, SC2Race.TERRAN, parent_item="Bunker"),
    ItemNames.Bunker_Fortified_Bunker: ItemData(611 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 11, SC2Race.TERRAN, parent_item="Bunker"),
    ItemNames.Planetary_Fortress: ItemData(612 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 12, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Perdition_Turret: ItemData(613 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 13, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Predator: ItemData(614 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 14, SC2Race.TERRAN, classification=ItemClassification.filler),
    ItemNames.Hercules: ItemData(615 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 15, SC2Race.TERRAN, classification=ItemClassification.progression),
    ItemNames.Cellular_Reactor: ItemData(616 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 16, SC2Race.TERRAN),
    ItemNames.Progressive_Regenerative_Bio_Steel: ItemData(617 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 4, SC2Race.TERRAN, quantity=2),
    ItemNames.Hive_Mind_Emulator: ItemData(618 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 18, SC2Race.TERRAN, ItemClassification.progression),
    ItemNames.Psi_Disrupter: ItemData(619 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 19, SC2Race.TERRAN, classification=ItemClassification.progression),

    ItemNames.Zealot: ItemData(700 + SC2WOL_ITEM_ID_OFFSET, "Unit", 0, SC2Race.PROTOSS, classification=ItemClassification.progression),
    ItemNames.Stalker: ItemData(701 + SC2WOL_ITEM_ID_OFFSET, "Unit", 1, SC2Race.PROTOSS, classification=ItemClassification.progression),
    ItemNames.High_Templar: ItemData(702 + SC2WOL_ITEM_ID_OFFSET, "Unit", 2, SC2Race.PROTOSS, classification=ItemClassification.progression),
    ItemNames.Dark_Templar: ItemData(703 + SC2WOL_ITEM_ID_OFFSET, "Unit", 3, SC2Race.PROTOSS, classification=ItemClassification.progression),
    ItemNames.Immortal: ItemData(704 + SC2WOL_ITEM_ID_OFFSET, "Unit", 4, SC2Race.PROTOSS, classification=ItemClassification.progression),
    ItemNames.Colossus: ItemData(705 + SC2WOL_ITEM_ID_OFFSET, "Unit", 5, SC2Race.PROTOSS),
    ItemNames.Phoenix: ItemData(706 + SC2WOL_ITEM_ID_OFFSET, "Unit", 6, SC2Race.PROTOSS, classification=ItemClassification.filler),
    ItemNames.Void_Ray: ItemData(707 + SC2WOL_ITEM_ID_OFFSET, "Unit", 7, SC2Race.PROTOSS, classification=ItemClassification.progression),
    ItemNames.Carrier: ItemData(708 + SC2WOL_ITEM_ID_OFFSET, "Unit", 8, SC2Race.PROTOSS, classification=ItemClassification.progression),

    # Filler items to fill remaining spots
    ItemNames.Starting_Minerals: ItemData(800 + SC2WOL_ITEM_ID_OFFSET, "Minerals", 15, SC2Race.ANY, quantity=0, classification=ItemClassification.filler),
    ItemNames.Starting_Vespene: ItemData(801 + SC2WOL_ITEM_ID_OFFSET, "Vespene", 15, SC2Race.ANY, quantity=0, classification=ItemClassification.filler),
    # This Filler item isn't placed by the generator yet unless plando'd
    ItemNames.Starting_Supply: ItemData(802 + SC2WOL_ITEM_ID_OFFSET, "Supply", 2, SC2Race.ANY, quantity=0, classification=ItemClassification.filler),
    # This item is used to "remove" location from the game. Never placed unless plando'd
    ItemNames.Nothing: ItemData(803 + SC2WOL_ITEM_ID_OFFSET, "Nothing Group", 2, SC2Race.ANY, quantity=0, classification=ItemClassification.trap),

    # ItemNames.Keystone_Piece: ItemData(850 + SC2WOL_ITEM_ID_OFFSET, "Goal", 0, quantity=0, classification=ItemClassification.progression_skip_balancing)

    # HotS
    ItemNames.Zergling: ItemData(0 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 0, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Swarm_Queen: ItemData(1 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 1, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Roach: ItemData(2 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 2, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Hydralisk: ItemData(3 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 3, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Baneling: ItemData(4 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 4, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Aberration: ItemData(5 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 5, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Mutalisk: ItemData(6 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 6, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Swarm_Host: ItemData(7 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 7, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Infestor: ItemData(8 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 8, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Ultralisk: ItemData(9 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 9, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Spore_Crawler: ItemData(10 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 10, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    ItemNames.Spine_Crawler: ItemData(11 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 11, SC2Race.ZERG, classification=ItemClassification.progression, origin={"hots"}),
    
    ItemNames.Progressive_Zerg_Melee_Attack: ItemData(100 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.Progressive_Zerg_Missile_Attack: ItemData(101 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.Progressive_Zerg_Ground_Carapace: ItemData(102 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.Progressive_Zerg_Flyer_Attack: ItemData(103 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.Progressive_Zerg_Flyer_Carapace: ItemData(104 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.ZERG, quantity=3, origin={"hots"}),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    ItemNames.Progressive_Zerg_Weapon_Upgrade: ItemData(105 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.Progressive_Zerg_Armor_Upgrade: ItemData(106 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 7, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.Progressive_Zerg_Ground_Upgrade: ItemData(107 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.Progressive_Zerg_Flyer_Upgrade: ItemData(108 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 9, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.Progressive_Zerg_Weapon_Armor_Upgrade: ItemData(109 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 10, SC2Race.ZERG, quantity=3, origin={"hots"}),

    ItemNames.Zergling_Hardened_Carapace: ItemData(200 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 0, SC2Race.ZERG, parent_item="Zergling", origin={"hots"}),
    ItemNames.Zergling_Adrenal_Overload: ItemData(201 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 1, SC2Race.ZERG, parent_item="Zergling", origin={"hots"}),
    ItemNames.Zergling_Metabolic_Boost: ItemData(202 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 2, SC2Race.ZERG, parent_item="Zergling", origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Roach_Hydriodic_Bile: ItemData(203 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 3, SC2Race.ZERG, parent_item="Roach", origin={"hots"}),
    ItemNames.Roach_Adaptive_Plating: ItemData(204 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 4, SC2Race.ZERG, parent_item="Roach", origin={"hots"}),
    ItemNames.Roach_Tunneling_Claws: ItemData(205 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 5, SC2Race.ZERG, parent_item="Roach", origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Hydralisk_Frenzy: ItemData(206 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 6, SC2Race.ZERG, parent_item="Hydralisk", origin={"hots"}),
    ItemNames.Hydralisk_Ancillary_Carapace: ItemData(207 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 7, SC2Race.ZERG, parent_item="Hydralisk", origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Hydralisk_Grooved_Spines: ItemData(208 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 8, SC2Race.ZERG, parent_item="Hydralisk", origin={"hots"}),
    ItemNames.Baneling_Corrosive_Acid: ItemData(209 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 9, SC2Race.ZERG, parent_item="Baneling", origin={"hots"}),
    ItemNames.Baneling_Rupture: ItemData(210 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 10, SC2Race.ZERG, parent_item="Baneling", origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Baneling_Regenerative_Acid: ItemData(211 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 11, SC2Race.ZERG, parent_item="Baneling", origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Mutalisk_Vicious_Glave: ItemData(212 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 12, SC2Race.ZERG, parent_item="Mutalisk", origin={"hots"}),
    ItemNames.Mutalisk_Rapid_Regeneration: ItemData(213 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 13, SC2Race.ZERG, parent_item="Mutalisk", origin={"hots"}),
    ItemNames.Mutalisk_Sundering_Glave: ItemData(214 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 14, SC2Race.ZERG, parent_item="Mutalisk", origin={"hots"}),
    ItemNames.Swarm_Host_Burrow: ItemData(215 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 15, SC2Race.ZERG, parent_item="Swarm Host", origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Swarm_Host_Rapid_Incubation: ItemData(216 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 16, SC2Race.ZERG, parent_item="Swarm Host", origin={"hots"}),
    ItemNames.Swarm_Host_Pressurized_Glands: ItemData(217 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 17, SC2Race.ZERG, parent_item="Swarm Host", origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Ultralisk_Burrow_Charge: ItemData(218 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 18, SC2Race.ZERG, parent_item="Ultralisk", origin={"hots"}),
    ItemNames.Ultralisk_Tissue_Animation: ItemData(219 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 19, SC2Race.ZERG, parent_item="Ultralisk", origin={"hots"}),
    ItemNames.Ultralisk_Monarch_Blades: ItemData(220 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 20, SC2Race.ZERG, parent_item="Ultralisk", origin={"hots"}),
    
    ItemNames.Zergling_Raptor_Strain: ItemData(300 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 0, SC2Race.ZERG, parent_item="Zergling", origin={"hots"}),
    ItemNames.Zergling_Swarmling_Strain: ItemData(301 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 1, SC2Race.ZERG, parent_item="Zergling", origin={"hots"}),
    ItemNames.Roach_Vile_Strain: ItemData(302 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 2, SC2Race.ZERG, parent_item="Roach", origin={"hots"}),
    ItemNames.Roach_Corpser_Strain: ItemData(303 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 3, SC2Race.ZERG, parent_item="Roach", origin={"hots"}),
    ItemNames.Hydralisk_Impaler_Strain: ItemData(304 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 4, SC2Race.ZERG, parent_item="Hydralisk", origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Hydralisk_Lurker_Strain: ItemData(305 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 5, SC2Race.ZERG, parent_item="Hydralisk", origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Baneling_Splitter_Strain: ItemData(306 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 6, SC2Race.ZERG, parent_item="Baneling", origin={"hots"}),
    ItemNames.Baneling_Hunter_Strain: ItemData(307 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 7, SC2Race.ZERG, parent_item="Baneling", origin={"hots"}),
    ItemNames.Mutalisk_Brood_Lord_Strain: ItemData(308 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 8, SC2Race.ZERG, parent_item="Mutalisk", origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Mutalisk_Viper_Strain: ItemData(309 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 9, SC2Race.ZERG, parent_item="Mutalisk", origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Swarm_Host_Carrion_Strain: ItemData(310 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 10, SC2Race.ZERG, parent_item="Swarm Host", origin={"hots"}),
    ItemNames.Swarm_Host_Creeper_Strain: ItemData(311 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 11, SC2Race.ZERG, parent_item="Swarm Host", origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Ultralisk_Noxious_Strain: ItemData(312 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 12, SC2Race.ZERG, parent_item="Ultralisk", origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Ultralisk_Torrasque_Strain: ItemData(313 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 13, SC2Race.ZERG, parent_item="Ultralisk", origin={"hots"}),
    
    ItemNames.Kerrigan_Kinetic_Blast: ItemData(400 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 0, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Heroic_Fortitude: ItemData(401 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 1, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Leaping_Strike: ItemData(402 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 2, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Crushing_Grip: ItemData(403 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 3, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Chain_Reaction: ItemData(404 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 4, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Psionic_Shift: ItemData(405 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 5, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Zergling_Reconstitution: ItemData(406 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 6, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.Kerrigan_Improved_Overlords: ItemData(407 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 7, SC2Race.ZERG, origin={"hots"}),
    ItemNames.Kerrigan_Automated_Extractors: ItemData(408 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 8, SC2Race.ZERG, origin={"hots"}),
    ItemNames.Kerrigan_Wild_Mutation: ItemData(409 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 9, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Spawn_Banelings: ItemData(410 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 10, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Mend: ItemData(411 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 11, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Twin_Drones: ItemData(412 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 12, SC2Race.ZERG, origin={"hots"}),
    ItemNames.Kerrigan_Malignant_Creep: ItemData(413 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 13, SC2Race.ZERG, origin={"hots"}),
    ItemNames.Kerrigan_Vespene_Efficiency: ItemData(414 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 14, SC2Race.ZERG, origin={"hots"}),
    ItemNames.Kerrigan_Infest_Broodlings: ItemData(415 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 15, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Fury: ItemData(416 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 16, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Ability_Efficiency: ItemData(417 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 17, SC2Race.ZERG, origin={"hots"}),
    ItemNames.Kerrigan_Apocalypse: ItemData(418 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 18, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Spawn_Leviathan: ItemData(419 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 19, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.Kerrigan_Drop_Pods: ItemData(420 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 20, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    # Handled separately from other abilities
    ItemNames.Kerrigan_Primal_Form: ItemData(421 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 0, SC2Race.ZERG, origin={"hots"}),
    
    ItemNames.Kerrigan_Levels_10: ItemData(500 + SC2HOTS_ITEM_ID_OFFSET, "Level", 10, SC2Race.ZERG, origin={"hots"}, quantity=0),
    ItemNames.Kerrigan_Levels_9: ItemData(501 + SC2HOTS_ITEM_ID_OFFSET, "Level", 9, SC2Race.ZERG, origin={"hots"}, quantity=0),
    ItemNames.Kerrigan_Levels_8: ItemData(502 + SC2HOTS_ITEM_ID_OFFSET, "Level", 8, SC2Race.ZERG, origin={"hots"}, quantity=0),
    ItemNames.Kerrigan_Levels_7: ItemData(503 + SC2HOTS_ITEM_ID_OFFSET, "Level", 7, SC2Race.ZERG, origin={"hots"}, quantity=0),
    ItemNames.Kerrigan_Levels_6: ItemData(504 + SC2HOTS_ITEM_ID_OFFSET, "Level", 6, SC2Race.ZERG, origin={"hots"}, quantity=0),
    ItemNames.Kerrigan_Levels_5: ItemData(505 + SC2HOTS_ITEM_ID_OFFSET, "Level", 5, SC2Race.ZERG, origin={"hots"}, quantity=0),
    ItemNames.Kerrigan_Levels_4: ItemData(506 + SC2HOTS_ITEM_ID_OFFSET, "Level", 4, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.filler),
    ItemNames.Kerrigan_Levels_3: ItemData(507 + SC2HOTS_ITEM_ID_OFFSET, "Level", 3, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.filler),
    ItemNames.Kerrigan_Levels_2: ItemData(508 + SC2HOTS_ITEM_ID_OFFSET, "Level", 2, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.filler),
    ItemNames.Kerrigan_Levels_1: ItemData(509 + SC2HOTS_ITEM_ID_OFFSET, "Level", 1, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.filler),
    ItemNames.Kerrigan_Levels_14: ItemData(510 + SC2HOTS_ITEM_ID_OFFSET, "Level", 14, SC2Race.ZERG, origin={"hots"}, quantity=0),
    ItemNames.Kerrigan_Levels_35: ItemData(511 + SC2HOTS_ITEM_ID_OFFSET, "Level", 35, SC2Race.ZERG, origin={"hots"}, quantity=0),
    ItemNames.Kerrigan_Levels_70: ItemData(512 + SC2HOTS_ITEM_ID_OFFSET, "Level", 70, SC2Race.ZERG, origin={"hots"}, quantity=0),
}

def get_item_table(multiworld: MultiWorld, player: int):
    return item_table

basic_units = {
    SC2Race.TERRAN: {
        ItemNames.Marine,
        ItemNames.Marauder,
        ItemNames.Goliath,
        ItemNames.Hellion,
        ItemNames.Vulture,
    },
    SC2Race.ZERG: {
        ItemNames.Zergling,
        ItemNames.Swarm_Queen,
        ItemNames.Roach,
        ItemNames.Hydralisk,
    },
    # TODO Placeholder for Prophecy
    SC2Race.PROTOSS: {
        ItemNames.Zealot,
        ItemNames.Stalker,
    }
}

advanced_basic_units = {
    SC2Race.TERRAN: basic_units[SC2Race.TERRAN].union({
        ItemNames.Reaper,
        ItemNames.Diamondback,
        ItemNames.Viking,
    }),
    SC2Race.ZERG: basic_units[SC2Race.ZERG].union({
        ItemNames.Infestor,
        ItemNames.Aberration,
    }),
    SC2Race.PROTOSS: basic_units[SC2Race.PROTOSS].union({
        ItemNames.Dark_Templar,
    })
}


def get_basic_units(multiworld: MultiWorld, player: int, race: SC2Race) -> typing.Set[str]:
    if get_option_value(multiworld, player, 'required_tactics') != RequiredTactics.option_standard:
        return advanced_basic_units[race]
    else:
        return basic_units[race]


item_name_group_names = {
    # WoL
    "Armory 1", "Armory 2", "Armory 3",
    "Armory 4", "Laboratory", "Progressive Upgrade",
    # HotS
    "Ability", "Strain", "Mutation"
}
item_name_groups: typing.Dict[str, typing.List[str]] = {}
for item, data in get_full_item_list().items():
    item_name_groups.setdefault(data.type, []).append(item)
    if data.type in item_name_group_names and '(' in item:
        short_name = item[:item.find(' (')]
        item_name_groups[short_name] = [item]
item_name_groups["Missions"] = ["Beat " + mission.mission_name for mission in SC2Mission]
item_name_groups["WoL Missions"] = ["Beat " + mission.mission_name for mission in campaign_mission_table[SC2Campaign.WOL]] + \
                                   ["Beat " + mission.mission_name for mission in campaign_mission_table[SC2Campaign.PROPHECY]]


# Items that can be placed before resources if not already in
# General upgrades and Mercs
# TODO needs zerg items
second_pass_placeable_items: typing.Tuple[str, ...] = (
    # Buildings without upgrades
    ItemNames.Sensor_Tower,
    ItemNames.Hive_Mind_Emulator,
    ItemNames.Psi_Disrupter,
    ItemNames.Perdition_Turret,
    # General upgrades without any dependencies
    ItemNames.SCV_Advanced_Construction,
    ItemNames.SCV_Dual_Fusion_Welders,
    ItemNames.Building_Fire_Suppression_System,
    ItemNames.Building_Orbital_Command,
    ItemNames.Ultra_Capacitors,
    ItemNames.Vanadium_Plating,
    ItemNames.Orbital_Depots,
    ItemNames.Micro_Filtering,
    ItemNames.Automated_Refinery,
    ItemNames.Command_Center_Reactor,
    ItemNames.Tech_Reactor,
    ItemNames.Planetary_Fortress,
    ItemNames.Cellular_Reactor,
    ItemNames.Progressive_Regenerative_Bio_Steel,  # Place only L1
    # Mercenaries
    ItemNames.War_Pigs,
    ItemNames.Devil_Dogs,
    ItemNames.Hammer_Securities,
    ItemNames.Spartan_Company,
    ItemNames.Siege_Breakers,
    ItemNames.Hels_Angel,
    ItemNames.Dusk_Wings,
    ItemNames.Jacksons_Revenge,
)


filler_items: typing.Tuple[str, ...] = (
    ItemNames.Starting_Minerals,
    ItemNames.Starting_Vespene,
)

# Defense rating table
# Commented defense ratings are handled in LogicMixin
defense_ratings = {
    ItemNames.Siege_Tank: 5,
    # "Maelstrom Rounds": 2,
    ItemNames.Planetary_Fortress: 3,
    # Bunker w/ Marine/Marauder: 3,
    ItemNames.Perdition_Turret: 2,
    ItemNames.Missile_Turret: 2,
    ItemNames.Vulture: 2,
    ItemNames.Liberator: 2,
    ItemNames.Widow_Mine: 2,
    # "Concealment (Widow Mine)": 1
}
zerg_defense_ratings = {
    ItemNames.Perdition_Turret: 2,
    # Bunker w/ Firebat: 2,
    ItemNames.Hive_Mind_Emulator: 3,
    ItemNames.Psi_Disrupter: 3,
}

spider_mine_sources = {
    ItemNames.Vulture,
    ItemNames.Reaper_Spider_Mines,
    ItemNames.Siege_Tank_Spider_Mines,
    ItemNames.Raven_Spider_Mines,
}

progressive_if_nco = {
    ItemNames.Marine_Progressive_Stimpack,
    ItemNames.Firebat_Progressive_Stimpack,
    ItemNames.Banshee_Progressive_Cross_Spectrum_Dampeners,
    ItemNames.Progressive_Regenerative_Bio_Steel,
}

kerrigan_actives: typing.List[typing.Set[str]] = [
    {ItemNames.Kerrigan_Kinetic_Blast, ItemNames.Kerrigan_Leaping_Strike},
    {ItemNames.Kerrigan_Crushing_Grip, ItemNames.Kerrigan_Psionic_Shift},
    set(),
    {ItemNames.Kerrigan_Wild_Mutation, ItemNames.Kerrigan_Spawn_Banelings, ItemNames.Kerrigan_Mend},
    set(),
    set(),
    {ItemNames.Kerrigan_Apocalypse, ItemNames.Kerrigan_Spawn_Leviathan, ItemNames.Kerrigan_Drop_Pods},
]

kerrigan_passives: typing.List[typing.Set[str]] = [
    {ItemNames.Kerrigan_Heroic_Fortitude},
    {ItemNames.Kerrigan_Chain_Reaction},
    {ItemNames.Kerrigan_Zergling_Reconstitution, ItemNames.Kerrigan_Improved_Overlords, ItemNames.Kerrigan_Automated_Extractors},
    set(),
    {ItemNames.Kerrigan_Twin_Drones, ItemNames.Kerrigan_Malignant_Creep, ItemNames.Kerrigan_Vespene_Efficiency},
    {ItemNames.Kerrigan_Infest_Broodlings, ItemNames.Kerrigan_Fury, ItemNames.Kerrigan_Ability_Efficiency},
    set(),
]

kerrigan_only_passives = {
    ItemNames.Kerrigan_Heroic_Fortitude, ItemNames.Kerrigan_Chain_Reaction,
    ItemNames.Kerrigan_Infest_Broodlings, ItemNames.Kerrigan_Fury, ItemNames.Kerrigan_Ability_Efficiency,
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
]
# 'upgrade_numbers' indices for all upgrades
upgrade_numbers_all = {
    SC2Race.TERRAN: 5,
    SC2Race.ZERG: 10,
}

# Names of upgrades to be included for different options
upgrade_included_names = [
    { # Individual Items
        ItemNames.Progressive_Terran_Infantry_Weapon,
        ItemNames.Progressive_Terran_Infantry_Armor,
        ItemNames.Progressive_Terran_Vehicle_Weapon,
        ItemNames.Progressive_Terran_Vehicle_Armor,
        ItemNames.Progressive_Terran_Ship_Weapon,
        ItemNames.Progressive_Terran_Ship_Armor,
        ItemNames.Progressive_Zerg_Melee_Attack,
        ItemNames.Progressive_Zerg_Missile_Attack,
        ItemNames.Progressive_Zerg_Ground_Carapace,
        ItemNames.Progressive_Zerg_Flyer_Attack,
        ItemNames.Progressive_Zerg_Flyer_Carapace,
    },
    { # Bundle Weapon And Armor
        ItemNames.Progressive_Terran_Weapon_Upgrade,
        ItemNames.Progressive_Terran_Armor_Upgrade,
        ItemNames.Progressive_Zerg_Weapon_Upgrade,
        ItemNames.Progressive_Zerg_Armor_Upgrade,
    },
    { # Bundle Unit Class
        ItemNames.Progressive_Terran_Infantry_Upgrade,
        ItemNames.Progressive_Terran_Vehicle_Upgrade,
        ItemNames.Progressive_Terran_Ship_Upgrade,
        ItemNames.Progressive_Zerg_Ground_Upgrade,
        ItemNames.Progressive_Zerg_Flyer_Upgrade,
    },
    { # Bundle All
        ItemNames.Progressive_Terran_Weapon_Armor_Upgrade,
        ItemNames.Progressive_Zerg_Weapon_Armor_Upgrade,
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
        "Unit": 0,
        "Upgrade": 1,  # Weapon / Armor upgrades
        "Armory 1": 2,  # Unit upgrades
        "Armory 2": 3,  # Unit upgrades
        "Building": 4,
        "Mercenary": 5,
        "Laboratory": 6,
        "Armory 3": 7,  # Unit upgrades
        "Armory 4": 8,  # Unit upgrades
        "Progressive Upgrade": 9,  # Unit upgrades that exist multiple times (Stimpack / Super Stimpack)
    },
    SC2Race.ZERG: {
        "Unit": 0,
        "Upgrade": 1,
        "Mutation": 2,
        "Strain": 3,
        "Ability": 4,
        "Level": 5,
    },
    SC2Race.PROTOSS: {
        "Unit": 0,
    }
}
