from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: typing.Optional[str]
    number: typing.Optional[int]
    progression: bool = False
    never_exclude: bool = True
    quantity: int = 1


class StarcraftWoLItem(Item):
    game: str = "Starcraft 2 Wings of Liberty"

    def __init__(self, name, advancement: bool = False, code: int = None, player: int = None):
        super(StarcraftWoLItem, self).__init__(name, advancement, code, player)


def get_full_item_list():
    return item_table


SC2WOL_ITEM_ID_OFFSET = 1000

item_table = {
    "Marine": ItemData(0+SC2WOL_ITEM_ID_OFFSET, "Unit", 0, progression=True),
    "Medic": ItemData(1+SC2WOL_ITEM_ID_OFFSET, "Unit", 1, progression=True),
    "Firebat": ItemData(2+SC2WOL_ITEM_ID_OFFSET, "Unit", 2, progression=True),
    "Marauder": ItemData(3+SC2WOL_ITEM_ID_OFFSET, "Unit", 3, progression=True),
    "Reaper": ItemData(4+SC2WOL_ITEM_ID_OFFSET, "Unit", 4, progression=True),
    "Hellion": ItemData(5+SC2WOL_ITEM_ID_OFFSET, "Unit", 5, progression=True),
    "Vulture": ItemData(6+SC2WOL_ITEM_ID_OFFSET, "Unit", 6, progression=True),
    "Goliath": ItemData(7+SC2WOL_ITEM_ID_OFFSET, "Unit", 7, progression=True),
    "Diamondback": ItemData(8+SC2WOL_ITEM_ID_OFFSET, "Unit", 8, progression=True),
    "Siege Tank": ItemData(9+SC2WOL_ITEM_ID_OFFSET, "Unit", 9, progression=True),
    "Medivac": ItemData(10+SC2WOL_ITEM_ID_OFFSET, "Unit", 10, progression=True),
    "Wraith": ItemData(11+SC2WOL_ITEM_ID_OFFSET, "Unit", 11, progression=True),
    "Viking": ItemData(12+SC2WOL_ITEM_ID_OFFSET, "Unit", 12, progression=True),
    "Banshee": ItemData(13+SC2WOL_ITEM_ID_OFFSET, "Unit", 13, progression=True),
    "Battlecruiser": ItemData(14+SC2WOL_ITEM_ID_OFFSET, "Unit", 14, progression=True),
    "Ghost": ItemData(15+SC2WOL_ITEM_ID_OFFSET, "Unit", 15, progression=True),
    "Spectre": ItemData(16+SC2WOL_ITEM_ID_OFFSET, "Unit", 16, progression=True),
    "Thor": ItemData(17+SC2WOL_ITEM_ID_OFFSET, "Unit", 17, progression=True),

    "Progressive Infantry Weapon": ItemData (100+SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, quantity=3),
    "Progressive Infantry Armor": ItemData (102+SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, quantity=3),
    "Progressive Vehicle Weapon": ItemData (103+SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, quantity=3),
    "Progressive Vehicle Armor": ItemData (104+SC2WOL_ITEM_ID_OFFSET, "Upgrade", 6, quantity=3),
    "Progressive Ship Weapon": ItemData (105+SC2WOL_ITEM_ID_OFFSET, "Upgrade", 8, quantity=3),
    "Progressive Ship Armor": ItemData (106+SC2WOL_ITEM_ID_OFFSET, "Upgrade", 10, quantity=3),

    "Projectile Accelerator (Bunker)": ItemData (200+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 0),
    "Neosteel Bunker (Bunker)": ItemData (201+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 1),
    "Titanium Housing (Missile Turret)": ItemData (202+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 2),
    "Hellstorm Batteries (Missile Turret)": ItemData (203+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 3),
    "Advanced Construction (SCV)": ItemData (204+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 4),
    "Dual-Fusion Welders (SCV)": ItemData (205+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 5),
    "Fire-Suppression System (Building)": ItemData (206+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 6),
    "Orbital Command (Building)": ItemData (207+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 7),
    "Stimpack (Marine)": ItemData (208+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 8),
    "Combat Shield (Marine)": ItemData (209+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 9),
    "Advanced Medic Facilities (Medic)": ItemData (210+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 10),
    "Stabilizer Medpacks (Medic)": ItemData (211+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 11),
    "Incinerator Gauntlets (Firebat)": ItemData (212+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 12, never_exclude=False),
    "Juggernaut Plating (Firebat)": ItemData (213+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 13),
    "Concussive Shells (Marauder)": ItemData (214+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 14),
    "Kinetic Foam (Marauder)": ItemData (215+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 15),
    "U-238 Rounds (Reaper)": ItemData (216+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 16),
    "G-4 Clusterbomb (Reaper)": ItemData (217+SC2WOL_ITEM_ID_OFFSET, "Armory 1", 17, never_exclude=False),

    "Twin-Linked Flamethrower (Hellion)": ItemData(300+SC2WOL_ITEM_ID_OFFSET, "Armory 2", 0, never_exclude=False),
    "Thermite Filaments (Hellion)": ItemData(301+SC2WOL_ITEM_ID_OFFSET, "Armory 2", 1),
    "Cerberus Mine (Vulture)": ItemData(302 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 2),
    "Replenishable Magazine (Vulture)": ItemData(303 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 3),
    "Multi-Lock Weapons System (Goliath)": ItemData(304 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 4),
    "Ares-Class Targeting System (Goliath)": ItemData(305 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 5),
    "Tri-Lithium Power Cell (Diamondback)": ItemData(306 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 6, never_exclude=False),
    "Shaped Hull (Diamondback)": ItemData(307 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 7, never_exclude=False),
    "Maelstrom Rounds (Siege Tank)": ItemData(308 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 8),
    "Shaped Blast (Siege Tank)": ItemData(309 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 9),
    "Rapid Deployment Tube (Medivac)": ItemData(310 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 10, never_exclude=False),
    "Advanced Healing AI (Medivac)": ItemData(311 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 11),
    "Tomahawk Power Cells (Wraith)": ItemData(312 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 12, never_exclude=False),
    "Displacement Field (Wraith)": ItemData(313 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 13),
    "Ripwave Missiles (Viking)": ItemData(314 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 14),
    "Phobos-Class Weapons System (Viking)": ItemData(315 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 15),
    "Cross-Spectrum Dampeners (Banshee)": ItemData(316 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 16, never_exclude=False),
    "Shockwave Missile Battery (Banshee)": ItemData(317 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 17),
    "Missile Pods (Battlecruiser)": ItemData(318 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 18, never_exclude=False),
    "Defensive Matrix (Battlecruiser)": ItemData(319 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 19, never_exclude=False),
    "Ocular Implants (Ghost)": ItemData(320 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 20),
    "Crius Suit (Ghost)": ItemData(321 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 21),
    "Psionic Lash (Spectre)": ItemData(322 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 22),
    "Nyx-Class Cloaking Module (Spectre)": ItemData(323 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 23),
    "330mm Barrage Cannon (Thor)": ItemData(324 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 24, never_exclude=False),
    "Immortality Protocol (Thor)": ItemData(325 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 25, never_exclude=False),

    "Bunker": ItemData (400+SC2WOL_ITEM_ID_OFFSET, "Building", 0, progression=True),
    "Missile Turret": ItemData (401+SC2WOL_ITEM_ID_OFFSET, "Building", 1, progression=True),
    "Sensor Tower": ItemData (402+SC2WOL_ITEM_ID_OFFSET, "Building", 2),

    "War Pigs": ItemData (500 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 0),
    "Devil Dogs": ItemData(501 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 1, never_exclude=False),
    "Hammer Securities": ItemData(502 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 2),
    "Spartan Company": ItemData(503 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 3),
    "Siege Breakers": ItemData(504 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 4),
    "Hel's Angel": ItemData(505 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 5),
    "Dusk Wings": ItemData(506 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 6),
    "Jackson's Revenge": ItemData(507 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 7),

    "Ultra-Capacitors": ItemData(600 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 0),
    "Vanadium Plating": ItemData(601 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 1),
    "Orbital Depots": ItemData(602 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 2),
    "Micro-Filtering": ItemData(603 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 3),
    "Automated Refinery": ItemData(604 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 4),
    "Command Center Reactor": ItemData(605 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 5),
    "Raven": ItemData(606 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 6),
    "Science Vessel": ItemData(607 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 7, progression=True),
    "Tech Reactor": ItemData(608 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 8),
    "Orbital Strike": ItemData(609 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 9),
    "Shrike Turret": ItemData(610 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 10),
    "Fortified Bunker": ItemData(611 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 11),
    "Planetary Fortress": ItemData(612 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 12),
    "Perdition Turret": ItemData(613 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 13),
    "Predator": ItemData(614 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 14, never_exclude=False),
    "Hercules": ItemData(615 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 15, progression=True),
    "Cellular Reactor": ItemData(616 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 16, never_exclude=False),
    "Regenerative Bio-Steel": ItemData(617 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 17, never_exclude=False),
    "Hive Mind Emulator": ItemData(618 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 18),
    "Psi Disrupter": ItemData(619 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 19, never_exclude=False),

    "Zealot": ItemData(700 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 0, progression=True),
    "Stalker": ItemData(701 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 1, progression=True),
    "High Templar": ItemData(702 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 2, progression=True),
    "Dark Templar": ItemData(703 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 3, progression=True),
    "Immortal": ItemData(704 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 4, progression=True),
    "Colossus": ItemData(705 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 5, progression=True),
    "Phoenix": ItemData(706 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 6, progression=True),
    "Void Ray": ItemData(707 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 7, progression=True),
    "Carrier": ItemData(708 + SC2WOL_ITEM_ID_OFFSET, "Protoss", 8, progression=True),

    "+15 Starting Minerals": ItemData(800+SC2WOL_ITEM_ID_OFFSET, "Minerals", 15, quantity=0, never_exclude=False),
    "+15 Starting Vespene": ItemData(801+SC2WOL_ITEM_ID_OFFSET, "Vespene", 15, quantity=0, never_exclude=False),
    "+2 Starting Supply": ItemData(802+SC2WOL_ITEM_ID_OFFSET, "Supply", 2, quantity=0, never_exclude=False),
}

basic_unit: typing.Tuple[str, ...] = (
    'Marine',
    'Marauder',
    'Firebat',
    'Hellion',
    'Vulture'
)


item_name_groups = {}
for item, data in item_table.items():
    item_name_groups.setdefault(data.type, []).append(item)
item_name_groups["Missions"] = ["Beat Liberation Day", "Beat The Outlaws", "Beat Zero Hour", "Beat Evacuation",
                         "None Outbreak", "Beat Safe Haven", "Beat Haven's Fall", "Beat Smash and Grab", "Beat The Dig",
                         "Beat The Moebius Factor", "Beat Supernova", "Beat Maw of the Void", "Beat Devil's Playground",
                         "Beat Welcome to the Jungle", "Beat Breakout", "Beat Ghost of a Chance",
                         "Beat The Great Train Robbery", "Beat Cutthroat", "Beat Engine of Destruction",
                         "Beat Media Blitz", "Beat Piercing the Shroud"]

filler_items: typing.Tuple[str, ...] = (
    '+15 Starting Minerals',
    '+15 Starting Vespene'
)

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in get_full_item_list().items() if data.code}