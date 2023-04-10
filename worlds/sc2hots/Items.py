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


class StarcraftHotSItem(Item):
    game: str = "Starcraft 2 Heart of the Swarm"


def get_full_item_list():
    return item_table


SC2HOTS_ITEM_ID_OFFSET = 4000

item_table = {
    "Zergling": ItemData(0 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 0, classification=ItemClassification.progression),
    "Swarm Queen": ItemData(1 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 1, classification=ItemClassification.progression),
    "Roach": ItemData(2 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 2, classification=ItemClassification.progression),
    "Hydralisk": ItemData(3 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 3, classification=ItemClassification.progression),
    "Baneling": ItemData(4 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 4, classification=ItemClassification.progression),
    "Aberration": ItemData(5 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 5, classification=ItemClassification.progression),
    "Mutalisk": ItemData(6 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 6, classification=ItemClassification.progression),
    "Swarm Host": ItemData(7 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 7, classification=ItemClassification.progression),
    "Infestor": ItemData(8 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 8, classification=ItemClassification.progression),
    "Ultralisk": ItemData(9 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 9, classification=ItemClassification.progression),
    "Spore Crawler": ItemData(10 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 10, classification=ItemClassification.progression),
    "Spine Crawler": ItemData(11 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 11, classification=ItemClassification.progression),
    # "Marine": ItemData(0 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 0, classification=ItemClassification.progression),
    # "Medic": ItemData(1 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 1, classification=ItemClassification.progression),
    # "Firebat": ItemData(2 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 2, classification=ItemClassification.progression),
    # "Marauder": ItemData(3 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 3, classification=ItemClassification.progression),
    # "Reaper": ItemData(4 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 4, classification=ItemClassification.progression),
    # "Hellion": ItemData(5 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 5, classification=ItemClassification.progression),
    # "Vulture": ItemData(6 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 6, classification=ItemClassification.progression),
    # "Goliath": ItemData(7 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 7, classification=ItemClassification.progression),
    # "Diamondback": ItemData(8 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 8, classification=ItemClassification.progression),
    # "Siege Tank": ItemData(9 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 9, classification=ItemClassification.progression),
    # "Medivac": ItemData(10 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 10, classification=ItemClassification.progression),
    # "Wraith": ItemData(11 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 11, classification=ItemClassification.progression),
    # "Viking": ItemData(12 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 12, classification=ItemClassification.progression),
    # "Banshee": ItemData(13 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 13, classification=ItemClassification.progression),
    # "Battlecruiser": ItemData(14 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 14, classification=ItemClassification.progression),
    # "Ghost": ItemData(15 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 15, classification=ItemClassification.progression),
    # "Spectre": ItemData(16 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 16, classification=ItemClassification.progression),
    # "Thor": ItemData(17 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 17, classification=ItemClassification.progression),

    "Progressive Melee Attack": ItemData(100 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 0, quantity=3),
    "Progressive Missile Attack": ItemData(101 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 2, quantity=3),
    "Progressive Ground Carapace": ItemData(102 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 4, quantity=3),
    "Progressive Flyer Attack": ItemData(103 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 6, quantity=3),
    "Progressive Flyer Carapace": ItemData(104 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 8, quantity=3),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    "Progressive Weapon Upgrade": ItemData(105 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 0, quantity=3),
    "Progressive Armor Upgrade": ItemData(106 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 1, quantity=3),
    "Progressive Ground Upgrade": ItemData(107 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 2, quantity=3),
    "Progressive Flyer Upgrade": ItemData(108 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 3, quantity=3),
    "Progressive Upgrade": ItemData(109 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 4, quantity=3),
    # "Progressive Infantry Weapon": ItemData(100 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 0, quantity=3),
    # "Progressive Infantry Armor": ItemData(102 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 2, quantity=3),
    # "Progressive Vehicle Weapon": ItemData(103 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 4, quantity=3),
    # "Progressive Vehicle Armor": ItemData(104 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 6, quantity=3),
    # "Progressive Ship Weapon": ItemData(105 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 8, quantity=3),
    # "Progressive Ship Armor": ItemData(106 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 10, quantity=3),

    "Hardened Carapace (Zergling)": ItemData(200 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 0, parent_item="Zergling"),
    "Adrenal Overload (Zergling)": ItemData(201 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 1, parent_item="Zergling"),
    "Metabolic Boost (Zergling)": ItemData(202 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 2, parent_item="Zergling", classification=ItemClassification.filler),
    "Hydriodic Bile (Roach)": ItemData(203 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 3, parent_item="Roach"),
    "Adaptive Plating (Roach)": ItemData(204 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 4, parent_item="Roach"),
    "Tunneling Claws (Roach)": ItemData(205 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 5, parent_item="Roach", classification=ItemClassification.filler),
    "Frenzy (Hydralisk)": ItemData(206 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 6, parent_item="Hydralisk"),
    "Ancillary Carapace (Hydralisk)": ItemData(207 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 7, parent_item="Hydralisk", classification=ItemClassification.filler),
    "Grooved Spines (Hydralisk)": ItemData(208 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 8, parent_item="Hydralisk"),
    "Corrosive Acid (Baneling)": ItemData(209 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 9, parent_item="Baneling"),
    "Rupture (Baneling)": ItemData(210 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 10, parent_item="Baneling", classification=ItemClassification.filler),
    "Regenerative Acid (Baneling)": ItemData(211 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 11, parent_item="Baneling", classification=ItemClassification.filler),
    "Vicious Glave (Mutalisk)": ItemData(212 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 12, parent_item="Mutalisk"),
    "Rapid Regeneration (Mutalisk)": ItemData(213 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 13, parent_item="Mutalisk"),
    "Sundering Glave (Mutalisk)": ItemData(214 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 14, parent_item="Mutalisk"),
    "Burrow (Swarm Host)": ItemData(215 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 15, parent_item="Swarm Host", classification=ItemClassification.filler),
    "Rapid Incubation (Swarm Host)": ItemData(216 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 16, parent_item="Swarm Host"),
    "Pressurized Glands (Swarm Host)": ItemData(217 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 17, parent_item="Swarm Host", classification=ItemClassification.progression),
    "Burrow Charge (Ultralisk)": ItemData(218 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 18, parent_item="Ultralisk"),
    "Tissue Animation (Ultralisk)": ItemData(219 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 19, parent_item="Ultralisk"),
    "Monarch Blades (Ultralisk)": ItemData(220 + SC2HOTS_ITEM_ID_OFFSET, "Mutation", 20, parent_item="Ultralisk"),
    # "Projectile Accelerator (Bunker)": ItemData(200 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 0, parent_item="Bunker"),
    # "Neosteel Bunker (Bunker)": ItemData(201 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 1, parent_item="Bunker"),
    # "Titanium Housing (Missile Turret)": ItemData(202 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 2, classification=ItemClassification.filler, parent_item="Missile Turret"),
    # "Hellstorm Batteries (Missile Turret)": ItemData(203 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 3, parent_item="Missile Turret"),
    # "Advanced Construction (SCV)": ItemData(204 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 4, parent_item="SCV"),
    # "Dual-Fusion Welders (SCV)": ItemData(205 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 5, parent_item="SCV"),
    # "Fire-Suppression System (Building)": ItemData(206 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 6, classification=ItemClassification.filler),
    # "Orbital Command (Building)": ItemData(207 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 7),
    # "Stimpack (Marine)": ItemData(208 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 8, parent_item="Marine"),
    # "Combat Shield (Marine)": ItemData(209 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 9, classification=ItemClassification.progression, parent_item="Marine"),
    # "Advanced Medic Facilities (Medic)": ItemData(210 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 10, classification=ItemClassification.progression, parent_item="Medic"),
    # "Stabilizer Medpacks (Medic)": ItemData(211 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 11, classification=ItemClassification.progression, parent_item="Medic"),
    # "Incinerator Gauntlets (Firebat)": ItemData(212 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 12, classification=ItemClassification.filler, parent_item="Firebat"),
    # "Juggernaut Plating (Firebat)": ItemData(213 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 13, parent_item="Firebat"),
    # "Concussive Shells (Marauder)": ItemData(214 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 14, parent_item="Marauder"),
    # "Kinetic Foam (Marauder)": ItemData(215 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 15, parent_item="Marauder"),
    # "U-238 Rounds (Reaper)": ItemData(216 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 16, parent_item="Reaper"),
    # "G-4 Clusterbomb (Reaper)": ItemData(217 + SC2HOTS_ITEM_ID_OFFSET, "Armory 1", 17, classification=ItemClassification.progression, parent_item="Reaper"),

    "Raptor Strain (Zergling)": ItemData(300 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 0, parent_item="Zergling"),
    "Swarmling Strain (Zergling)": ItemData(301 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 1, parent_item="Zergling"),
    "Vile Strain (Roach)": ItemData(302 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 2, parent_item="Roach"),
    "Corpser Strain (Roach)": ItemData(303 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 3, parent_item="Roach"),
    "Impaler Strain (Hydralisk)": ItemData(304 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 4, parent_item="Hydralisk", classification=ItemClassification.progression),
    "Lurker Strain (Hydralisk)": ItemData(305 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 5, parent_item="Hydralisk", classification=ItemClassification.progression),
    "Splitter Strain (Baneling)": ItemData(306 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 6, parent_item="Baneling"),
    "Hunter Strain (Baneling)": ItemData(307 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 7, parent_item="Baneling"),
    "Brood Lord Strain (Mutalisk)": ItemData(308 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 8, parent_item="Mutalisk", classification=ItemClassification.progression),
    "Viper Strain (Mutalisk)": ItemData(309 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 9, parent_item="Mutalisk", classification=ItemClassification.progression),
    "Carrion Strain (Swarm Host)": ItemData(310 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 10, parent_item="Swarm Host"),
    "Creeper Strain (Swarm Host)": ItemData(311 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 11, parent_item="Swarm Host", classification=ItemClassification.filler),
    "Noxious Strain (Ultralisk)": ItemData(312 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 12, parent_item="Ultralisk", classification=ItemClassification.filler),
    "Torrasque Strain (Ultralisk)": ItemData(313 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 13, parent_item="Ultralisk"),
    # "Twin-Linked Flamethrower (Hellion)": ItemData(300 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 0, classification=ItemClassification.filler, parent_item="Hellion"),
    # "Thermite Filaments (Hellion)": ItemData(301 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 1, parent_item="Hellion"),
    # "Cerberus Mine (Vulture)": ItemData(302 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 2, classification=ItemClassification.filler, parent_item="Vulture"),
    # "Replenishable Magazine (Vulture)": ItemData(303 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 3, classification=ItemClassification.filler, parent_item="Vulture"),
    # "Multi-Lock Weapons System (Goliath)": ItemData(304 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 4, parent_item="Goliath"),
    # "Ares-Class Targeting System (Goliath)": ItemData(305 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 5, parent_item="Goliath"),
    # "Tri-Lithium Power Cell (Diamondback)": ItemData(306 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 6, classification=ItemClassification.filler, parent_item="Diamondback"),
    # "Shaped Hull (Diamondback)": ItemData(307 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 7, classification=ItemClassification.filler, parent_item="Diamondback"),
    # "Maelstrom Rounds (Siege Tank)": ItemData(308 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 8, classification=ItemClassification.progression, parent_item="Siege Tank"),
    # "Shaped Blast (Siege Tank)": ItemData(309 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 9, parent_item="Siege Tank"),
    # "Rapid Deployment Tube (Medivac)": ItemData(310 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 10, classification=ItemClassification.filler, parent_item="Medivac"),
    # "Advanced Healing AI (Medivac)": ItemData(311 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 11, classification=ItemClassification.filler, parent_item="Medivac"),
    # "Tomahawk Power Cells (Wraith)": ItemData(312 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 12, classification=ItemClassification.filler, parent_item="Wraith"),
    # "Displacement Field (Wraith)": ItemData(313 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 13, classification=ItemClassification.filler, parent_item="Wraith"),
    # "Ripwave Missiles (Viking)": ItemData(314 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 14, parent_item="Viking"),
    # "Phobos-Class Weapons System (Viking)": ItemData(315 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 15, parent_item="Viking"),
    # "Cross-Spectrum Dampeners (Banshee)": ItemData(316 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 16, classification=ItemClassification.filler, parent_item="Banshee"),
    # "Shockwave Missile Battery (Banshee)": ItemData(317 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 17, parent_item="Banshee"),
    # "Missile Pods (Battlecruiser)": ItemData(318 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 18, classification=ItemClassification.filler, parent_item="Battlecruiser"),
    # "Defensive Matrix (Battlecruiser)": ItemData(319 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 19, classification=ItemClassification.filler, parent_item="Battlecruiser"),
    # "Ocular Implants (Ghost)": ItemData(320 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 20, parent_item="Ghost"),
    # "Crius Suit (Ghost)": ItemData(321 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 21, parent_item="Ghost"),
    # "Psionic Lash (Spectre)": ItemData(322 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 22, classification=ItemClassification.progression, parent_item="Spectre"),
    # "Nyx-Class Cloaking Module (Spectre)": ItemData(323 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 23, parent_item="Spectre"),
    # "330mm Barrage Cannon (Thor)": ItemData(324 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 24, classification=ItemClassification.filler, parent_item="Thor"),
    # "Immortality Protocol (Thor)": ItemData(325 + SC2HOTS_ITEM_ID_OFFSET, "Armory 2", 25, classification=ItemClassification.filler, parent_item="Thor"),

    "Kinetic Blast (Kerrigan Tier 1)": ItemData(400 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 0, classification=ItemClassification.progression),
    "Heroic Fortitude (Kerrigan Tier 1)": ItemData(401 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 1, classification=ItemClassification.progression),
    "Leaping Strike (Kerrigan Tier 1)": ItemData(402 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 2, classification=ItemClassification.progression),
    "Crushing Grip (Kerrigan Tier 2)": ItemData(403 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 3, classification=ItemClassification.progression),
    "Chain Reaction (Kerrigan Tier 2)": ItemData(404 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 4, classification=ItemClassification.progression),
    "Psionic Shift (Kerrigan Tier 2)": ItemData(405 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 5, classification=ItemClassification.progression),
    "Zergling Reconstitution (Kerrigan Tier 3)": ItemData(406 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 6, classification=ItemClassification.filler),
    "Improved Overlords (Kerrigan Tier 3)": ItemData(407 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 7),
    "Automated Extractors (Kerrigan Tier 3)": ItemData(408 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 8),
    "Wild Mutation (Kerrigan Tier 4)": ItemData(409 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 9, classification=ItemClassification.progression),
    "Spawn Banelings (Kerrigan Tier 4)": ItemData(410 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 10, classification=ItemClassification.progression),
    "Mend (Kerrigan Tier 4)": ItemData(411 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 11, classification=ItemClassification.progression),
    "Twin Drones (Kerrigan Tier 5)": ItemData(412 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 12),
    "Malignant Creep (Kerrigan Tier 5)": ItemData(413 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 13),
    "Vespene Efficiency (Kerrigan Tier 5)": ItemData(414 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 14),
    "Infest Broodlings (Kerrigan Tier 6)": ItemData(415 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 15, classification=ItemClassification.progression),
    "Fury (Kerrigan Tier 6)": ItemData(416 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 16, classification=ItemClassification.progression),
    "Ability Efficiency (Kerrigan Tier 6)": ItemData(417 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 17),
    "Apocalypse (Kerrigan Tier 7)": ItemData(418 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 18, classification=ItemClassification.progression),
    "Spawn Leviathan (Kerrigan Tier 7)": ItemData(419 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 19, classification=ItemClassification.progression),
    "Drop-Pods (Kerrigan Tier 7)": ItemData(420 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 20, classification=ItemClassification.progression),
    # Handled separately from other abilities
    "Primal Form (Kerrigan)": ItemData(421 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 0),
    # "Bunker": ItemData(400 + SC2HOTS_ITEM_ID_OFFSET, "Building", 0, classification=ItemClassification.progression),
    # "Missile Turret": ItemData(401 + SC2HOTS_ITEM_ID_OFFSET, "Building", 1, classification=ItemClassification.progression),
    # "Sensor Tower": ItemData(402 + SC2HOTS_ITEM_ID_OFFSET, "Building", 2),

    "10 Kerrigan Levels": ItemData(500 + SC2HOTS_ITEM_ID_OFFSET, "Level", 10, quantity=0),
    "9 Kerrigan Levels": ItemData(501 + SC2HOTS_ITEM_ID_OFFSET, "Level", 9, quantity=0),
    "8 Kerrigan Levels": ItemData(502 + SC2HOTS_ITEM_ID_OFFSET, "Level", 8, quantity=0),
    "7 Kerrigan Levels": ItemData(503 + SC2HOTS_ITEM_ID_OFFSET, "Level", 7, quantity=0),
    "6 Kerrigan Levels": ItemData(504 + SC2HOTS_ITEM_ID_OFFSET, "Level", 6, quantity=0),
    "5 Kerrigan Levels": ItemData(505 + SC2HOTS_ITEM_ID_OFFSET, "Level", 5, quantity=0),
    "4 Kerrigan Levels": ItemData(506 + SC2HOTS_ITEM_ID_OFFSET, "Level", 4, quantity=0, classification=ItemClassification.filler),
    "3 Kerrigan Levels": ItemData(507 + SC2HOTS_ITEM_ID_OFFSET, "Level", 3, quantity=0, classification=ItemClassification.filler),
    "2 Kerrigan Levels": ItemData(508 + SC2HOTS_ITEM_ID_OFFSET, "Level", 2, quantity=0, classification=ItemClassification.filler),
    "1 Kerrigan Level": ItemData(509 + SC2HOTS_ITEM_ID_OFFSET, "Level", 1, quantity=0, classification=ItemClassification.filler),
    "14 Kerrigan Levels": ItemData(510 + SC2HOTS_ITEM_ID_OFFSET, "Level", 14, quantity=0),
    "35 Kerrigan Levels": ItemData(511 + SC2HOTS_ITEM_ID_OFFSET, "Level", 35, quantity=0),
    "70 Kerrigan Levels": ItemData(512 + SC2HOTS_ITEM_ID_OFFSET, "Level", 70, quantity=0),
    # "War Pigs": ItemData(500 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 0, classification=ItemClassification.progression),
    # "Devil Dogs": ItemData(501 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 1, classification=ItemClassification.filler),
    # "Hammer Securities": ItemData(502 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 2),
    # "Spartan Company": ItemData(503 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 3, classification=ItemClassification.progression),
    # "Siege Breakers": ItemData(504 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 4),
    # "Hel's Angel": ItemData(505 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 5, classification=ItemClassification.progression),
    # "Dusk Wings": ItemData(506 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 6),
    # "Jackson's Revenge": ItemData(507 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 7),

    # "Ultra-Capacitors": ItemData(600 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 0),
    # "Vanadium Plating": ItemData(601 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 1),
    # "Orbital Depots": ItemData(602 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 2),
    # "Micro-Filtering": ItemData(603 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 3),
    # "Automated Refinery": ItemData(604 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 4),
    # "Command Center Reactor": ItemData(605 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 5),
    # "Raven": ItemData(606 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 6),
    # "Science Vessel": ItemData(607 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 7, classification=ItemClassification.progression),
    # "Tech Reactor": ItemData(608 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 8),
    # "Orbital Strike": ItemData(609 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 9),
    # "Shrike Turret": ItemData(610 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 10, parent_item="Bunker"),
    # "Fortified Bunker": ItemData(611 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 11, parent_item="Bunker"),
    # "Planetary Fortress": ItemData(612 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 12, classification=ItemClassification.progression),
    # "Perdition Turret": ItemData(613 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 13, classification=ItemClassification.progression),
    # "Predator": ItemData(614 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 14, classification=ItemClassification.filler),
    # "Hercules": ItemData(615 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 15, classification=ItemClassification.progression),
    # "Cellular Reactor": ItemData(616 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 16, classification=ItemClassification.filler),
    # "Regenerative Bio-Steel": ItemData(617 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 17, classification=ItemClassification.filler),
    # "Hive Mind Emulator": ItemData(618 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 18, ItemClassification.progression),
    # "Psi Disrupter": ItemData(619 + SC2HOTS_ITEM_ID_OFFSET, "Laboratory", 19, classification=ItemClassification.progression),

    # "Zealot": ItemData(700 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 0, classification=ItemClassification.progression),
    # "Stalker": ItemData(701 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 1, classification=ItemClassification.progression),
    # "High Templar": ItemData(702 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 2, classification=ItemClassification.progression),
    # "Dark Templar": ItemData(703 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 3, classification=ItemClassification.progression),
    # "Immortal": ItemData(704 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 4, classification=ItemClassification.progression),
    # "Colossus": ItemData(705 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 5, classification=ItemClassification.progression),
    # "Phoenix": ItemData(706 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 6, classification=ItemClassification.progression),
    # "Void Ray": ItemData(707 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 7, classification=ItemClassification.progression),
    # "Carrier": ItemData(708 + SC2HOTS_ITEM_ID_OFFSET, "Protoss", 8, classification=ItemClassification.progression),

    "+15 Starting Minerals": ItemData(800 + SC2HOTS_ITEM_ID_OFFSET, "Minerals", 15, quantity=0, classification=ItemClassification.filler),
    "+15 Starting Vespene": ItemData(801 + SC2HOTS_ITEM_ID_OFFSET, "Vespene", 15, quantity=0, classification=ItemClassification.filler),
    "+2 Starting Supply": ItemData(802 + SC2HOTS_ITEM_ID_OFFSET, "Supply", 2, quantity=0, classification=ItemClassification.filler),

    "Transmission Trap": ItemData(803 + SC2HOTS_ITEM_ID_OFFSET, "Trap", 0, quantity=0, classification=ItemClassification.trap)

    # "Keystone Piece": ItemData(850 + SC2HOTS_ITEM_ID_OFFSET, "Goal", 0, quantity=0, classification=ItemClassification.progression_skip_balancing)
}


# basic_units = {
#     'Marine',
#     'Marauder',
#     'Firebat',
#     'Hellion',
#     'Vulture'
# }
basic_units = {
    'Zergling',
    'Swarm Queen',
    'Roach',
    'Hydralisk'
}

# advanced_basic_units = basic_units.union({
#     'Reaper',
#     'Goliath',
#     'Diamondback',
#     'Viking'
# })
advanced_basic_units = basic_units.union({
    'Infestor',
    'Aberration'
})


def get_basic_units(multiworld: MultiWorld, player: int) -> typing.Set[str]:
    if get_option_value(multiworld, player, 'required_tactics') > 0:
        return advanced_basic_units
    else:
        return basic_units


item_name_groups = {}
for item, data in item_table.items():
    item_name_groups.setdefault(data.type, []).append(item)
    if data.type in ("Mutation", "Strain", "Ability") and '(' in item:
        short_name = item[:item.find(' (')]
        item_name_groups[short_name] = [item]
item_name_groups["Missions"] = ["Beat " + mission_name for mission_name in vanilla_mission_req_table]

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
    "Vulture": 2
}
zerg_defense_ratings = {
    "Perdition Turret": 2,
    # Bunker w/ Firebat: 2,
    "Hive Mind Emulator": 3,
    "Psi Disruptor": 3
}

# 'number' values of upgrades for upgrade bundle items
upgrade_numbers = [
    {0, 2, 6}, # Weapon
    {4, 8}, # Armor
    {0, 2, 4}, # Ground
    {6, 8}, # Flyer
    {0, 2, 4, 6, 8} # All
]
# Names of upgrades to be included for different options
upgrade_included_names = [
    { # Individual Items
        "Progressive Melee Attack",
        "Progressive Missile Attack",
        "Progressive Ground Carapace",
        "Progressive Flyer Attack",
        "Progressive Flyer Carapace"
    },
    { # Bundle Weapon And Armor
        "Progressive Weapon Upgrade",
        "Progressive Armor Upgrade"
    },
    { # Bundle Ground And Flyer
        "Progressive Ground Upgrade",
        "Progressive Flyer Upgrade"
    },
    { # Bundle All
        "Progressive Upgrade"
    }
]

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in get_full_item_list().items() if
                                            data.code}
# Map type to expected int
type_flaggroups: typing.Dict[str, int] = {
    "Unit": 0,
    "Upgrade": 1,
    "Mutation": 2,
    "Strain": 3,
    "Ability": 4,
    "Level": 5,
    # "Armory 1": 2,
    # "Armory 2": 3,
    # "Building": 4,
    # "Mercenary": 5,
    # "Laboratory": 6,
    # "Protoss": 7,
    "Minerals": 6,
    "Vespene": 7,
    "Supply": 8,
    "Goal": 9,
    "Trap": 10
}
