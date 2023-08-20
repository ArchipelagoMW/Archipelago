from BaseClasses import Item, ItemClassification, MultiWorld
import typing

from .Options import get_option_value
from .MissionTables import vanilla_mission_req_table


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: typing.Optional[str]
    number: typing.Optional[int]
    classification: ItemClassification = ItemClassification.useful
    quantity: int = 1
    parent_item: str = None
    origin: typing.Set[str] = {"wol"}


class StarcraftWoLItem(Item):
    game: str = "Starcraft 2 Wings of Liberty"


def get_full_item_list():
    return item_table


SC2WOL_ITEM_ID_OFFSET = 1000

item_table = {
    "Marine": ItemData(0 + SC2WOL_ITEM_ID_OFFSET, "Unit", 0, classification=ItemClassification.progression),
    "Medic": ItemData(1 + SC2WOL_ITEM_ID_OFFSET, "Unit", 1, classification=ItemClassification.progression),
    "Firebat": ItemData(2 + SC2WOL_ITEM_ID_OFFSET, "Unit", 2, classification=ItemClassification.progression),
    "Marauder": ItemData(3 + SC2WOL_ITEM_ID_OFFSET, "Unit", 3, classification=ItemClassification.progression),
    "Reaper": ItemData(4 + SC2WOL_ITEM_ID_OFFSET, "Unit", 4, classification=ItemClassification.progression),
    "Hellion": ItemData(5 + SC2WOL_ITEM_ID_OFFSET, "Unit", 5, classification=ItemClassification.progression),
    "Vulture": ItemData(6 + SC2WOL_ITEM_ID_OFFSET, "Unit", 6, classification=ItemClassification.progression),
    "Goliath": ItemData(7 + SC2WOL_ITEM_ID_OFFSET, "Unit", 7, classification=ItemClassification.progression),
    "Diamondback": ItemData(8 + SC2WOL_ITEM_ID_OFFSET, "Unit", 8, classification=ItemClassification.progression),
    "Siege Tank": ItemData(9 + SC2WOL_ITEM_ID_OFFSET, "Unit", 9, classification=ItemClassification.progression),
    "Medivac": ItemData(10 + SC2WOL_ITEM_ID_OFFSET, "Unit", 10, classification=ItemClassification.progression),
    "Wraith": ItemData(11 + SC2WOL_ITEM_ID_OFFSET, "Unit", 11, classification=ItemClassification.progression),
    "Viking": ItemData(12 + SC2WOL_ITEM_ID_OFFSET, "Unit", 12, classification=ItemClassification.progression),
    "Banshee": ItemData(13 + SC2WOL_ITEM_ID_OFFSET, "Unit", 13, classification=ItemClassification.progression),
    "Battlecruiser": ItemData(14 + SC2WOL_ITEM_ID_OFFSET, "Unit", 14, classification=ItemClassification.progression),
    "Ghost": ItemData(15 + SC2WOL_ITEM_ID_OFFSET, "Unit", 15, classification=ItemClassification.progression),
    "Spectre": ItemData(16 + SC2WOL_ITEM_ID_OFFSET, "Unit", 16, classification=ItemClassification.progression),
    "Thor": ItemData(17 + SC2WOL_ITEM_ID_OFFSET, "Unit", 17, classification=ItemClassification.progression),
    # EE units
    "Liberator": ItemData(18 + SC2WOL_ITEM_ID_OFFSET, "Unit", 18, classification=ItemClassification.progression, origin={"nco", "ext"}),
    "Valkyrie": ItemData(19 + SC2WOL_ITEM_ID_OFFSET, "Unit", 19, classification=ItemClassification.progression, origin={"bw"}),
    "Widow Mine": ItemData(20 + SC2WOL_ITEM_ID_OFFSET, "Unit", 20, classification=ItemClassification.progression, origin={"ext"}),
    "Cyclone": ItemData(21 + SC2WOL_ITEM_ID_OFFSET, "Unit", 21, classification=ItemClassification.progression, origin={"ext"}),

    # Some other items are moved to Upgrade group because of the way how the bot message is parsed
    "Progressive Infantry Weapon": ItemData(100 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, quantity=3),
    "Progressive Infantry Armor": ItemData(102 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, quantity=3),
    "Progressive Vehicle Weapon": ItemData(103 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, quantity=3),
    "Progressive Vehicle Armor": ItemData(104 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 6, quantity=3),
    "Progressive Ship Weapon": ItemData(105 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 8, quantity=3),
    "Progressive Ship Armor": ItemData(106 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 10, quantity=3),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    "Progressive Weapon Upgrade": ItemData(107 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, quantity=3),
    "Progressive Armor Upgrade": ItemData(108 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 1, quantity=3),
    "Progressive Infantry Upgrade": ItemData(109 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, quantity=3),
    "Progressive Vehicle Upgrade": ItemData(110 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 3, quantity=3),
    "Progressive Ship Upgrade": ItemData(111 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, quantity=3),
    "Progressive Weapon/Armor Upgrade": ItemData(112 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 5, quantity=3),

    "Projectile Accelerator (Bunker)": ItemData(200 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 0, parent_item="Bunker"),
    "Neosteel Bunker (Bunker)": ItemData(201 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 1, parent_item="Bunker"),
    "Titanium Housing (Missile Turret)": ItemData(202 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 2, classification=ItemClassification.filler, parent_item="Missile Turret"),
    "Hellstorm Batteries (Missile Turret)": ItemData(203 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 3, parent_item="Missile Turret"),
    "Advanced Construction (SCV)": ItemData(204 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 4),
    "Dual-Fusion Welders (SCV)": ItemData(205 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 5),
    "Fire-Suppression System (Building)": ItemData(206 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 6),
    "Orbital Command (Building)": ItemData(207 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 7),
    "Progressive Stimpack (Marine)": ItemData(208 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 0, parent_item="Marine", quantity=2),
    "Combat Shield (Marine)": ItemData(209 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 9, classification=ItemClassification.progression, parent_item="Marine"),
    "Advanced Medic Facilities (Medic)": ItemData(210 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 10, classification=ItemClassification.filler, parent_item="Medic"),
    "Stabilizer Medpacks (Medic)": ItemData(211 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 11, classification=ItemClassification.progression, parent_item="Medic"),
    "Incinerator Gauntlets (Firebat)": ItemData(212 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 12, classification=ItemClassification.filler, parent_item="Firebat"),
    "Juggernaut Plating (Firebat)": ItemData(213 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 13, parent_item="Firebat"),
    "Concussive Shells (Marauder)": ItemData(214 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 14, parent_item="Marauder"),
    "Kinetic Foam (Marauder)": ItemData(215 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 15, parent_item="Marauder"),
    "U-238 Rounds (Reaper)": ItemData(216 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 16, parent_item="Reaper"),
    "G-4 Clusterbomb (Reaper)": ItemData(217 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 17, classification=ItemClassification.progression, parent_item="Reaper"),
    # Items from EE
    "Mag-Field Accelerators (Cyclone)": ItemData(218 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 18, parent_item="Cyclone", origin={"ext"}),
    "Mag-Field Launchers (Cyclone)": ItemData(219 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 19, parent_item="Cyclone", origin={"ext"}),
    # Items from new mod
    "Laser Targeting System (Marine)": ItemData(220 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 8, classification=ItemClassification.filler, parent_item="Marine", origin={"nco"}), # Freed slot from Stimpack
    "Magrail Munitions (Marine)": ItemData(221 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 20, parent_item="Marine", origin={"nco"}),
    "Optimized Logistics (Marine)": ItemData(222 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 21, classification=ItemClassification.filler, parent_item="Marine", origin={"nco"}),
    "Restoration (Medic)": ItemData(223 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 22, classification=ItemClassification.filler, parent_item="Medic", origin={"bw"}),
    "Optical Flare (Medic)": ItemData(224 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 23, classification=ItemClassification.filler, parent_item="Medic", origin={"bw"}),
    "Optimized Logistics (Medic)": ItemData(225 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 24, classification=ItemClassification.filler, parent_item="Medic", origin={"bw"}),
    "Progressive Stimpack (Firebat)": ItemData(226 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 6, parent_item="Firebat", quantity=2, origin={"bw"}),
    "Optimized Logistics (Firebat)": ItemData(227 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 25, parent_item="Firebat", origin={"bw"}),
    "Progressive Stimpack (Marauder)": ItemData(228 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 8, parent_item="Marauder", quantity=2, origin={"nco"}),
    "Laser Targeting System (Marauder)": ItemData(229 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 26, classification=ItemClassification.filler, parent_item="Marauder", origin={"nco"}),
    "Magrail Munitions (Marauder)": ItemData(230 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 27, classification=ItemClassification.filler, parent_item="Marauder", origin={"nco"}),
    "Internal Tech Module (Marauder)": ItemData(231 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 28, classification=ItemClassification.filler, parent_item="Marauder", origin={"nco"}),

    # Items from new mod
    "Progressive Stimpack (Reaper)": ItemData(250 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 10, parent_item="Reaper", quantity=2, origin={"nco"}),
    "Laser Targeting System (Reaper)": ItemData(251 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 0, classification=ItemClassification.filler, parent_item="Reaper", origin={"nco"}),
    "Advanced Cloaking Field (Reaper)": ItemData(252 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 1, parent_item="Reaper", origin={"nco"}),
    "Spider Mines (Reaper)": ItemData(253 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 2, classification=ItemClassification.filler, parent_item="Reaper", origin={"nco"}),
    "Combat Drugs (Reaper)": ItemData(254 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 3, classification=ItemClassification.filler, parent_item="Reaper", origin={"ext"}),
    "Hellbat Aspect (Hellion)": ItemData(255 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 4, parent_item="Hellion", origin={"nco"}),
    "Smart Servos (Hellion)": ItemData(256 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 5, parent_item="Hellion", origin={"nco"}),
    "Optimized Logistics (Hellion)": ItemData(257 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 6, classification=ItemClassification.filler, parent_item="Hellion", origin={"nco"}),
    "Jump Jets (Hellion)": ItemData(258 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 7, classification=ItemClassification.filler, parent_item="Hellion", origin={"nco"}),
    "Progressive Stimpack (Hellion)": ItemData(259 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 12, parent_item="Hellion", quantity=2, origin={"nco"}),
    "Ion Thrusters (Vulture)": ItemData(260 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 8, classification=ItemClassification.filler, parent_item="Vulture", origin={"bw"}),
    "Auto Launchers (Vulture)": ItemData(261 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 9, parent_item="Vulture", origin={"bw"}),
    "High Explosive Munition (Spider Mine)": ItemData(262 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 10, origin={"bw"}),
    "Jump Jets (Goliath)": ItemData(263 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 11, classification=ItemClassification.filler, parent_item="Goliath", origin={"nco"}),
    "Optimized Logistics (Goliath)": ItemData(264 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 12, classification=ItemClassification.filler, parent_item="Goliath", origin={"nco"}),
    "Hyperfluxor (Diamondback)": ItemData(265 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 13, parent_item="Diamondback", origin={"ext"}),
    "Burst Capacitors (Diamondback)": ItemData(266 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 14, classification=ItemClassification.filler, parent_item="Diamondback", origin={"ext"}),
    "Optimized Logistics (Diamondback)": ItemData(267 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 15, parent_item="Diamondback", origin={"ext"}),
    "Jump Jets (Siege Tank)": ItemData(268 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 16, parent_item="Siege Tank", origin={"nco"}),
    "Spider Mines (Siege Tank)": ItemData(269 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 17, classification=ItemClassification.filler, parent_item="Siege Tank", origin={"nco"}),
    "Smart Servos (Siege Tank)": ItemData(270 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 18, classification=ItemClassification.filler, parent_item="Siege Tank", origin={"nco"}),
    "Graduating Range (Siege Tank)": ItemData(271 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 19, classification=ItemClassification.progression, parent_item="Siege Tank", origin={"ext"}),
    "Laser Targeting System (Siege Tank)": ItemData(272 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 20, parent_item="Siege Tank", origin={"nco"}),
    "Advanced Siege Tech (Siege Tank)": ItemData(273 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 21, parent_item="Siege Tank", origin={"ext"}),
    "Internal Tech Module (Siege Tank)": ItemData(274 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 22, classification=ItemClassification.filler, parent_item="Siege Tank", origin={"nco"}),
    "Optimized Logistics (Predator)": ItemData(275 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 23, classification=ItemClassification.filler, parent_item="Predator", origin={"ext"}),
    "Expanded Hull (Medivac)": ItemData(276 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 24, classification=ItemClassification.filler, parent_item="Medivac", origin={"ext"}),
    "Afterburners (Medivac)": ItemData(277 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 25, classification=ItemClassification.filler, parent_item="Medivac", origin={"ext"}),
    "Advanced Laser Technology (Wraith)": ItemData(278 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 26, classification=ItemClassification.progression, parent_item="Wraith", origin={"ext"}),
    "Smart Servos (Viking)": ItemData(279 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 27, parent_item="Viking", origin={"ext"}),
    "Magrail Munitions (Viking)": ItemData(280 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 28, parent_item="Viking", origin={"ext"}),

    "Twin-Linked Flamethrower (Hellion)": ItemData(300 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 0, classification=ItemClassification.filler, parent_item="Hellion"),
    "Thermite Filaments (Hellion)": ItemData(301 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 1, parent_item="Hellion"),
    "Cerberus Mine (Spider Mine)": ItemData(302 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 2, classification=ItemClassification.filler),
    "Replenishable Magazine (Vulture)": ItemData(303 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 3, classification=ItemClassification.filler, parent_item="Vulture"),
    "Multi-Lock Weapons System (Goliath)": ItemData(304 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 4, parent_item="Goliath"),
    "Ares-Class Targeting System (Goliath)": ItemData(305 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 5, parent_item="Goliath"),
    "Tri-Lithium Power Cell (Diamondback)": ItemData(306 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 6, classification=ItemClassification.filler, parent_item="Diamondback"),
    "Shaped Hull (Diamondback)": ItemData(307 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 7, classification=ItemClassification.filler, parent_item="Diamondback"),
    "Maelstrom Rounds (Siege Tank)": ItemData(308 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 8, classification=ItemClassification.progression, parent_item="Siege Tank"),
    "Shaped Blast (Siege Tank)": ItemData(309 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 9, parent_item="Siege Tank"),
    "Rapid Deployment Tube (Medivac)": ItemData(310 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 10, classification=ItemClassification.filler, parent_item="Medivac"),
    "Advanced Healing AI (Medivac)": ItemData(311 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 11, classification=ItemClassification.filler, parent_item="Medivac"),
    "Tomahawk Power Cells (Wraith)": ItemData(312 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 12, classification=ItemClassification.filler, parent_item="Wraith"),
    "Displacement Field (Wraith)": ItemData(313 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 13, classification=ItemClassification.filler, parent_item="Wraith"),
    "Ripwave Missiles (Viking)": ItemData(314 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 14, parent_item="Viking"),
    "Phobos-Class Weapons System (Viking)": ItemData(315 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 15, parent_item="Viking"),
    "Progressive Cross-Spectrum Dampeners (Banshee)": ItemData(316 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 2, classification=ItemClassification.filler, parent_item="Banshee", quantity=2),
    "Shockwave Missile Battery (Banshee)": ItemData(317 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 17, parent_item="Banshee"),
    "Missile Pods (Battlecruiser)": ItemData(318 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 18, classification=ItemClassification.filler, parent_item="Battlecruiser"),
    "Defensive Matrix (Battlecruiser)": ItemData(319 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 19, classification=ItemClassification.filler, parent_item="Battlecruiser"),
    "Ocular Implants (Ghost)": ItemData(320 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 20, parent_item="Ghost"),
    "Crius Suit (Ghost)": ItemData(321 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 21, parent_item="Ghost"),
    "Psionic Lash (Spectre)": ItemData(322 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 22, classification=ItemClassification.progression, parent_item="Spectre"),
    "Nyx-Class Cloaking Module (Spectre)": ItemData(323 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 23, parent_item="Spectre"),
    "330mm Barrage Cannon (Thor)": ItemData(324 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 24, classification=ItemClassification.filler, parent_item="Thor"),
    "Immortality Protocol (Thor)": ItemData(325 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 25, classification=ItemClassification.filler, parent_item="Thor"),
    # Items from EE
    "Advanced Ballistics (Liberator)": ItemData(326 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 26, parent_item="Liberator", origin={"ext"}),
    "Raid Artillery (Liberator)": ItemData(327 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 27, classification=ItemClassification.progression, parent_item="Liberator", origin={"nco"}),
    "Drilling Claws (Widow Mine)": ItemData(328 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 28, classification=ItemClassification.filler, parent_item="Widow Mine", origin={"ext"}),
    "Concealment (Widow Mine)": ItemData(329 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 29, classification=ItemClassification.progression, parent_item="Widow Mine", origin={"ext"}),

    #Items from new mod
    "Hyperflight Rotors (Banshee)": ItemData(350 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 0, classification=ItemClassification.filler, parent_item="Banshee", origin={"ext"}),
    "Laser Targeting System (Banshee)": ItemData(351 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 1, classification=ItemClassification.filler, parent_item="Banshee", origin={"nco"}),
    "Internal Tech Module (Banshee)": ItemData(352 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 2, classification=ItemClassification.filler, parent_item="Banshee", origin={"nco"}),
    "Tactical Jump (Battlecruiser)": ItemData(353 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 3, parent_item="Battlecruiser", origin={"nco", "ext"}),
    "Cloak (Battlecruiser)": ItemData(354 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 4, parent_item="Battlecruiser", origin={"nco"}),
    "ATX Laser Battery (Battlecruiser)": ItemData(355 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 5, classification=ItemClassification.progression, parent_item="Battlecruiser", origin={"nco"}),
    "Optimized Logistics (Battlecruiser)": ItemData(356 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 6, classification=ItemClassification.filler, parent_item="Battlecruiser", origin={"ext"}),
    "Internal Tech Module (Battlecruiser)": ItemData(357 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 7, classification=ItemClassification.filler, parent_item="Battlecruiser", origin={"nco"}),
    "EMP Rounds (Ghost)": ItemData(358 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 8, parent_item="Ghost", origin={"ext"}),
    "Lockdown (Ghost)": ItemData(359 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 9, parent_item="Ghost", origin={"bw"}),
    "Impaler Rounds (Spectre)": ItemData(360 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 10, parent_item="Spectre", origin={"ext"}),
    "Progressive High Impact Payload (Thor)": ItemData(361 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 14, parent_item="Thor", quantity=2, origin={"ext"}),  # L2 is Smart Servos
    "Bio Mechanical Repair Drone (Raven)": ItemData(363 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 13, parent_item="Raven", origin={"nco"}),
    "Spider Mines (Raven)": ItemData(364 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 14, parent_item="Raven", origin={"nco"}),
    "Railgun Turret (Raven)": ItemData(365 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 15, parent_item="Raven", origin={"nco"}),
    "Hunter-Seeker Weapon (Raven)": ItemData(366 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 16, parent_item="Raven", origin={"nco"}),
    "Interference Matrix (Raven)": ItemData(367 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 17, parent_item="Raven", origin={"ext"}),
    "Anti-Armor Missile (Raven)": ItemData(368 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 18, classification=ItemClassification.filler, parent_item="Raven", origin={"ext"}),
    "Internal Tech Module (Raven)": ItemData(369 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 19, classification=ItemClassification.filler, parent_item="Raven", origin={"nco"}),
    "EMP Shockwave (Science Vessel)": ItemData(370 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 20, parent_item="Science Vessel", origin={"bw"}),
    "Defensive Matrix (Science Vessel)": ItemData(371 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 21, parent_item="Science Vessel", origin={"bw"}),
    "Targeting Optics (Cyclone)": ItemData(372 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 22, parent_item="Cyclone", origin={"ext"}),
    "Rapid Fire Launchers (Cyclone)": ItemData(373 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 23, parent_item="Cyclone", origin={"ext"}),
    "Cloak (Liberator)": ItemData(374 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 24, classification=ItemClassification.filler, parent_item="Liberator", origin={"nco"}),
    "Laser Targeting System (Liberator)": ItemData(375 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 25, classification=ItemClassification.filler, parent_item="Liberator", origin={"ext"}),
    "Optimized Logistics (Liberator)": ItemData(376 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 26, classification=ItemClassification.filler, parent_item="Liberator", origin={"nco"}),
    "Black Market Launchers (Widow Mine)": ItemData(377 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 27, classification=ItemClassification.filler, parent_item="Widow Mine", origin={"ext"}),
    "Executioner Missiles (Widow Mine)": ItemData(378 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 28, parent_item="Widow Mine", origin={"ext"}),

    # Just lazy to create a new group for one unit
    "Enhanced Cluster Launchers (Valkyrie)": ItemData(379 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 17, parent_item="Valkyrie", origin={"ext"}),
    "Shaped Hull (Valkyrie)": ItemData(380 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 20, classification=ItemClassification.filler, parent_item="Valkyrie", origin={"ext"}),
    "Burst Lasers (Valkyrie)": ItemData(381 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 21, parent_item="Valkyrie", origin={"ext"}),
    "Afterburners (Valkyrie)": ItemData(382 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 22, classification=ItemClassification.filler, parent_item="Valkyrie", origin={"ext"}),

    "Bunker": ItemData(400 + SC2WOL_ITEM_ID_OFFSET, "Building", 0, classification=ItemClassification.progression),
    "Missile Turret": ItemData(401 + SC2WOL_ITEM_ID_OFFSET, "Building", 1, classification=ItemClassification.progression),
    "Sensor Tower": ItemData(402 + SC2WOL_ITEM_ID_OFFSET, "Building", 2),

    "War Pigs": ItemData(500 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 0, classification=ItemClassification.progression),
    "Devil Dogs": ItemData(501 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 1, classification=ItemClassification.filler),
    "Hammer Securities": ItemData(502 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 2),
    "Spartan Company": ItemData(503 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 3, classification=ItemClassification.progression),
    "Siege Breakers": ItemData(504 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 4),
    "Hel's Angel": ItemData(505 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 5, classification=ItemClassification.progression),
    "Dusk Wings": ItemData(506 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 6),
    "Jackson's Revenge": ItemData(507 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 7),

    "Ultra-Capacitors": ItemData(600 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 0),
    "Vanadium Plating": ItemData(601 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 1),
    "Orbital Depots": ItemData(602 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 2),
    "Micro-Filtering": ItemData(603 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 3),
    "Automated Refinery": ItemData(604 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 4),
    "Command Center Reactor": ItemData(605 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 5),
    "Raven": ItemData(606 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 6),
    "Science Vessel": ItemData(607 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 7, classification=ItemClassification.progression),
    "Tech Reactor": ItemData(608 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 8),
    "Orbital Strike": ItemData(609 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 9),
    "Shrike Turret (Bunker)": ItemData(610 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 10, parent_item="Bunker"),
    "Fortified Bunker (Bunker)": ItemData(611 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 11, parent_item="Bunker"),
    "Planetary Fortress": ItemData(612 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 12, classification=ItemClassification.progression),
    "Perdition Turret": ItemData(613 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 13, classification=ItemClassification.progression),
    "Predator": ItemData(614 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 14, classification=ItemClassification.filler),
    "Hercules": ItemData(615 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 15, classification=ItemClassification.progression),
    "Cellular Reactor": ItemData(616 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 16),
    "Progressive Regenerative Bio-Steel": ItemData(617 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 4, quantity=2),
    "Hive Mind Emulator": ItemData(618 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 18, ItemClassification.progression),
    "Psi Disrupter": ItemData(619 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 19, classification=ItemClassification.progression),

    "Zealot": ItemData(700 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 0, classification=ItemClassification.progression),
    "Stalker": ItemData(701 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 1, classification=ItemClassification.progression),
    "High Templar": ItemData(702 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 2, classification=ItemClassification.progression),
    "Dark Templar": ItemData(703 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 3, classification=ItemClassification.progression),
    "Immortal": ItemData(704 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 4, classification=ItemClassification.progression),
    "Colossus": ItemData(705 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 5),
    "Phoenix": ItemData(706 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 6, classification=ItemClassification.filler),
    "Void Ray": ItemData(707 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 7, classification=ItemClassification.progression),
    "Carrier": ItemData(708 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 8, classification=ItemClassification.progression),

    # Filler items to fill remaining spots
    "+15 Starting Minerals": ItemData(800 + SC2WOL_ITEM_ID_OFFSET, "Minerals", 15, quantity=0, classification=ItemClassification.filler),
    "+15 Starting Vespene": ItemData(801 + SC2WOL_ITEM_ID_OFFSET, "Vespene", 15, quantity=0, classification=ItemClassification.filler),
    # This Filler item isn't placed by the generator yet unless plando'd
    "+2 Starting Supply": ItemData(802 + SC2WOL_ITEM_ID_OFFSET, "Supply", 2, quantity=0, classification=ItemClassification.filler),
    # This item is used to "remove" location from the game. Never placed unless plando'd
    "Nothing": ItemData(803 + SC2WOL_ITEM_ID_OFFSET, "Nothing Group", 2, quantity=0, classification=ItemClassification.trap),

    # "Keystone Piece": ItemData(850 + SC2WOL_ITEM_ID_OFFSET, "Goal", 0, quantity=0, classification=ItemClassification.progression_skip_balancing)
}

def get_item_table(multiworld: MultiWorld, player: int):
    return item_table

basic_units = {
    'Marine',
    'Marauder',
    'Goliath',
    'Hellion',
    'Vulture'
}

advanced_basic_units = basic_units.union({
    'Reaper',
    'Diamondback',
    'Viking'
})


def get_basic_units(multiworld: MultiWorld, player: int) -> typing.Set[str]:
    if get_option_value(multiworld, player, 'required_tactics') > 0:
        return advanced_basic_units
    else:
        return basic_units


item_name_groups = {}
for item, data in get_full_item_list().items():
    item_name_groups.setdefault(data.type, []).append(item)
    if data.type in ("Armory 1", "Armory 2") and '(' in item:
        short_name = item[:item.find(' (')]
        item_name_groups[short_name] = [item]
item_name_groups["Missions"] = ["Beat " + mission_name for mission_name in vanilla_mission_req_table]


# Items that can be placed before resources if not already in
# General upgrades and Mercs
second_pass_placeable_items: typing.Tuple[str, ...] = (
    # Buildings without upgrades
    "Sensor Tower",
    "Hive Mind Emulator",
    "Psi Disrupter",
    "Perdition Turret",
    # General upgrades without any dependencies
    "Advanced Construction (SCV)",
    "Dual-Fusion Welders (SCV)",
    "Fire-Suppression System (Building)",
    "Orbital Command (Building)",
    "Ultra-Capacitors",
    "Vanadium Plating",
    "Orbital Depots",
    "Micro-Filtering",
    "Automated Refinery",
    "Command Center Reactor",
    "Tech Reactor",
    "Planetary Fortress",
    "Cellular Reactor",
    "Progressive Regenerative Bio-Steel",  # Place only L1
    # Mercenaries
    "War Pigs",
    "Devil Dogs",
    "Hammer Securities",
    "Spartan Company",
    "Siege Breakers",
    "Hel's Angel",
    "Dusk Wings",
    "Jackson's Revenge"
)


filler_items: typing.Tuple[str, ...] = (
    '+15 Starting Minerals',
    '+15 Starting Vespene'
)

# Defense rating table
# Commented defense ratings are handled in LogicMixin
defense_ratings = {
    "Siege Tank": 5,
    # "Maelstrom Rounds": 2,
    "Planetary Fortress": 3,
    # Bunker w/ Marine/Marauder: 3,
    "Perdition Turret": 2,
    "Missile Turret": 2,
    "Vulture": 2,
    "Liberator": 2,
    "Widow Mine": 2
    # "Concealment (Widow Mine)": 1
}
zerg_defense_ratings = {
    "Perdition Turret": 2,
    # Bunker w/ Firebat: 2,
    "Hive Mind Emulator": 3,
    "Psi Disruptor": 3
}

spider_mine_sources = {
    "Vulture",
    "Spider Mines (Reaper)",
    "Spider Mines (Siege Tank)",
    "Spider Mines (Raven)"
}

progressive_if_nco = {
    "Progressive Stimpack (Marine)",
    "Progressive Stimpack (Firebat)",
    "Progressive Cross-Spectrum Dampeners (Banshee)",
    "Progressive Regenerative Bio-Steel"
}

# 'number' values of upgrades for upgrade bundle items
upgrade_numbers = [
    {0, 4, 8}, # Weapon
    {2, 6, 10}, # Armor
    {0, 2}, # Infantry
    {4, 6}, # Vehicle
    {8, 10}, # Starship
    {0, 2, 4, 6, 8, 10} # All
]
# Names of upgrades to be included for different options
upgrade_included_names = [
    { # Individual Items
        "Progressive Infantry Weapon",
        "Progressive Infantry Armor",
        "Progressive Vehicle Weapon",
        "Progressive Vehicle Armor",
        "Progressive Ship Weapon",
        "Progressive Ship Armor"
    },
    { # Bundle Weapon And Armor
        "Progressive Weapon Upgrade",
        "Progressive Armor Upgrade"
    },
    { # Bundle Unit Class
        "Progressive Infantry Upgrade",
        "Progressive Vehicle Upgrade",
        "Progressive Starship Upgrade"
    },
    { # Bundle All
        "Progressive Weapon/Armor Upgrade"
    }
]

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in get_full_item_list().items() if
                                            data.code}
# Map type to expected int
type_flaggroups: typing.Dict[str, int] = {
    "Unit": 0,
    "Upgrade": 1,  # Weapon / Armor upgrades
    "Armory 1": 2,  # Unit upgrades
    "Armory 2": 3,  # Unit upgrades
    "Building": 4,
    "Mercenary": 5,
    "Laboratory": 6,
    "Protoss": 7,
    "Minerals": 8,
    "Vespene": 9,
    "Supply": 10,
    "Goal": 11,
    "Armory 3": 12,  # Unit upgrades
    "Armory 4": 13,  # Unit upgrades
    "Progressive Upgrade": 14,  # Unit upgrades that exist multiple times (Stimpack / Super Stimpack)
    "Nothing Group": 15
}
