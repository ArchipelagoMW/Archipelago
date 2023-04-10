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

    "Progressive Infantry Weapon": ItemData(100 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, quantity=3),
    "Progressive Infantry Armor": ItemData(102 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, quantity=3),
    "Progressive Vehicle Weapon": ItemData(103 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, quantity=3),
    "Progressive Vehicle Armor": ItemData(104 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 6, quantity=3),
    "Progressive Ship Weapon": ItemData(105 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 8, quantity=3),
    "Progressive Ship Armor": ItemData(106 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 10, quantity=3),

    "Projectile Accelerator (Bunker)": ItemData(200 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 0, parent_item="Bunker"),
    "Neosteel Bunker (Bunker)": ItemData(201 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 1, parent_item="Bunker"),
    "Titanium Housing (Missile Turret)": ItemData(202 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 2, classification=ItemClassification.filler, parent_item="Missile Turret"),
    "Hellstorm Batteries (Missile Turret)": ItemData(203 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 3, parent_item="Missile Turret"),
    "Advanced Construction (SCV)": ItemData(204 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 4, parent_item="SCV"),
    "Dual-Fusion Welders (SCV)": ItemData(205 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 5, parent_item="SCV"),
    "Fire-Suppression System (Building)": ItemData(206 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 6, classification=ItemClassification.filler),
    "Orbital Command (Building)": ItemData(207 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 7),
    "Stimpack (Marine)": ItemData(208 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 8, parent_item="Marine"),
    "Combat Shield (Marine)": ItemData(209 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 9, classification=ItemClassification.progression, parent_item="Marine"),
    "Advanced Medic Facilities (Medic)": ItemData(210 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 10, classification=ItemClassification.progression, parent_item="Medic"),
    "Stabilizer Medpacks (Medic)": ItemData(211 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 11, classification=ItemClassification.progression, parent_item="Medic"),
    "Incinerator Gauntlets (Firebat)": ItemData(212 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 12, classification=ItemClassification.filler, parent_item="Firebat"),
    "Juggernaut Plating (Firebat)": ItemData(213 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 13, parent_item="Firebat"),
    "Concussive Shells (Marauder)": ItemData(214 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 14, parent_item="Marauder"),
    "Kinetic Foam (Marauder)": ItemData(215 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 15, parent_item="Marauder"),
    "U-238 Rounds (Reaper)": ItemData(216 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 16, parent_item="Reaper"),
    "G-4 Clusterbomb (Reaper)": ItemData(217 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 17, classification=ItemClassification.progression, parent_item="Reaper"),

    "Twin-Linked Flamethrower (Hellion)": ItemData(300 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 0, classification=ItemClassification.filler, parent_item="Hellion"),
    "Thermite Filaments (Hellion)": ItemData(301 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 1, parent_item="Hellion"),
    "Cerberus Mine (Vulture)": ItemData(302 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 2, classification=ItemClassification.filler, parent_item="Vulture"),
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
    "Cross-Spectrum Dampeners (Banshee)": ItemData(316 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 16, classification=ItemClassification.filler, parent_item="Banshee"),
    "Shockwave Missile Battery (Banshee)": ItemData(317 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 17, parent_item="Banshee"),
    "Missile Pods (Battlecruiser)": ItemData(318 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 18, classification=ItemClassification.filler, parent_item="Battlecruiser"),
    "Defensive Matrix (Battlecruiser)": ItemData(319 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 19, classification=ItemClassification.filler, parent_item="Battlecruiser"),
    "Ocular Implants (Ghost)": ItemData(320 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 20, parent_item="Ghost"),
    "Crius Suit (Ghost)": ItemData(321 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 21, parent_item="Ghost"),
    "Psionic Lash (Spectre)": ItemData(322 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 22, classification=ItemClassification.progression, parent_item="Spectre"),
    "Nyx-Class Cloaking Module (Spectre)": ItemData(323 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 23, parent_item="Spectre"),
    "330mm Barrage Cannon (Thor)": ItemData(324 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 24, classification=ItemClassification.filler, parent_item="Thor"),
    "Immortality Protocol (Thor)": ItemData(325 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 25, classification=ItemClassification.filler, parent_item="Thor"),

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
    "Shrike Turret": ItemData(610 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 10, parent_item="Bunker"),
    "Fortified Bunker": ItemData(611 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 11, parent_item="Bunker"),
    "Planetary Fortress": ItemData(612 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 12, classification=ItemClassification.progression),
    "Perdition Turret": ItemData(613 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 13, classification=ItemClassification.progression),
    "Predator": ItemData(614 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 14, classification=ItemClassification.filler),
    "Hercules": ItemData(615 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 15, classification=ItemClassification.progression),
    "Cellular Reactor": ItemData(616 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 16, classification=ItemClassification.filler),
    "Regenerative Bio-Steel": ItemData(617 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 17, classification=ItemClassification.filler),
    "Hive Mind Emulator": ItemData(618 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 18, ItemClassification.progression),
    "Psi Disrupter": ItemData(619 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 19, classification=ItemClassification.progression),

    "Zealot": ItemData(700 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 0, classification=ItemClassification.progression),
    "Stalker": ItemData(701 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 1, classification=ItemClassification.progression),
    "High Templar": ItemData(702 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 2, classification=ItemClassification.progression),
    "Dark Templar": ItemData(703 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 3, classification=ItemClassification.progression),
    "Immortal": ItemData(704 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 4, classification=ItemClassification.progression),
    "Colossus": ItemData(705 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 5, classification=ItemClassification.progression),
    "Phoenix": ItemData(706 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 6, classification=ItemClassification.progression),
    "Void Ray": ItemData(707 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 7, classification=ItemClassification.progression),
    "Carrier": ItemData(708 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 8, classification=ItemClassification.progression),

    "+15 Starting Minerals": ItemData(800 + SC2WOL_ITEM_ID_OFFSET, "Minerals", 15, quantity=0, classification=ItemClassification.filler),
    "+15 Starting Vespene": ItemData(801 + SC2WOL_ITEM_ID_OFFSET, "Vespene", 15, quantity=0, classification=ItemClassification.filler),
    "+2 Starting Supply": ItemData(802 + SC2WOL_ITEM_ID_OFFSET, "Supply", 2, quantity=0, classification=ItemClassification.filler),

    # "Keystone Piece": ItemData(850 + SC2WOL_ITEM_ID_OFFSET, "Goal", 0, quantity=0, classification=ItemClassification.progression_skip_balancing)
}


basic_units = {
    'Marine',
    'Marauder',
    'Firebat',
    'Hellion',
    'Vulture'
}

advanced_basic_units = basic_units.union({
    'Reaper',
    'Goliath',
    'Diamondback',
    'Viking'
})


def get_basic_units(multiworld: MultiWorld, player: int) -> typing.Set[str]:
    if get_option_value(multiworld, player, 'required_tactics') > 0:
        return advanced_basic_units
    else:
        return basic_units


item_name_groups = {}
for item, data in item_table.items():
    item_name_groups.setdefault(data.type, []).append(item)
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

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in get_full_item_list().items() if
                                            data.code}
# Map type to expected int
type_flaggroups: typing.Dict[str, int] = {
    "Unit": 0,
    "Upgrade": 1,
    "Armory 1": 2,
    "Armory 2": 3,
    "Building": 4,
    "Mercenary": 5,
    "Laboratory": 6,
    "Protoss": 7,
    "Minerals": 8,
    "Vespene": 9,
    "Supply": 10,
    "Goal": 11
}
