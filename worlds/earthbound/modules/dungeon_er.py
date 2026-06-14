import struct
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from ..game_data.local_data import item_id_table
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from ..game_data.local_data import item_id_table
if TYPE_CHECKING:
    from .. import EarthBoundWorld
    from ..Rom import LocalRom


@dataclass
class EBDungeonDoor:
    address: int
    copyaddress: int
    direction: int
    is_script: bool = False # Script warps invert the x and y coordinate


def shuffle_dungeons(world: "EarthBoundWorld") -> None:
    # Is the dept. store a dungeon
    single_exit_dungeons = [
        "Giant Step",
        "Happy-Happy HQ",
        "Lilliput Steps",
        "Milky Well",
        "Gold Mine",
        "Moonside",
        "Monotoli Building",
        "Magnet Hill",
        "Pink Cloud",
        "Dungeon Man",
        "Stonehenge Base",
        "Lumine Hall",
        "Fire Spring",
        "Sea of Eden"
    ]

    double_exit_dungeons = [
        "Arcade",
        "Brickroad Maze",
        "Rainy Circle",
        "Belch's Factory",
        "Pyramid"
        ]

    world.dungeon_connections = {
        "Arcade": "Arcade",
        "Giant Step": "Giant Step",
        "Happy-Happy HQ": "Happy-Happy HQ",
        "Lilliput Steps": "Lilliput Steps",
        "Belch's Factory": "Belch's Factory",
        "Milky Well": "Milky Well",
        "Gold Mine": "Gold Mine",
        "Moonside": "Moonside",
        "Monotoli Building": "Monotoli Building",
        "Magnet Hill": "Magnet Hill",
        "Pink Cloud": "Pink Cloud",
        "Dungeon Man": "Dungeon Man",
        "Stonehenge Base": "Stonehenge Base",
        "Brickroad Maze": "Brickroad Maze",
        "Rainy Circle": "Rainy Circle",
        "Pyramid": "Pyramid",
        "Lumine Hall": "Lumine Hall",
        "Fire Spring": "Fire Spring",
        "Sea of Eden": "Sea of Eden"
    }
    if world.options.magicant_mode:
        # Don't shuffle Magicant when it's important
        single_exit_dungeons.remove("Sea of Eden")

    shuffled_single_dungeons = single_exit_dungeons.copy()
    shuffled_double_dungeons = double_exit_dungeons.copy()

    if world.options.dungeon_shuffle:
        world.random.shuffle(shuffled_single_dungeons)
        world.random.shuffle(shuffled_double_dungeons)

    for index, entrance in enumerate(single_exit_dungeons):
        world.dungeon_connections[entrance] = shuffled_single_dungeons[index]

    for index, entrance in enumerate(double_exit_dungeons):
        world.dungeon_connections[entrance] = shuffled_double_dungeons[index]


def write_dungeon_entrances(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    dungeon_entrances = {
        "Arcade": ["Arcade Entrance", "Arcade Exit", "Arcade Back Exit", "Arcade Back Entrance"],
        "Giant Step": ["Giant Step Entrance", "Giant Step Exit"],
        "Happy-Happy HQ": ["Happy-Happy HQ Entrance", "Happy-Happy HQ Exit"],
        "Lilliput Steps": ["Lilliput Steps Entrance", "Lilliput Steps Exit"],
        "Belch's Factory": ["Factory Script Warp", "Factory Exit", "Factory Back Exit", "Factory Back Entrance"],
        "Milky Well": ["Milky Well Entrance", "Milky Well Exit"],
        "Gold Mine": ["Mine Entrance", "Mine Exit"],
        "Monotoli Building": ["Monotoli Entrance", "Monotoli Exit"],
        "Moonside": ["Cafe Entrance", "Cafe Exit"],
        "Brickroad Maze": ["Maze Entrance", "Maze Exit", "Maze Back Exit", "Maze Back Entrance"],
        "Rainy Circle": ["Rainy Entrance", "Rainy Exit", "Rainy Back Exit", "Rainy Back Entrance"],
        "Magnet Hill": ["Sewer Entrance", "Sewer Exit"],
        "Pink Cloud": ["Pink Cloud Entrance", "Pink Cloud Exit"],
        "Pyramid": ["Pyramid Entrance", "Pyramid Exit", "Pyramid Back Exit", "Pyramid Back Entrance"],
        "Dungeon Man": ["D.M. Entrance Script", "D.M. Exit Script"],
        "Stonehenge Base": ["Stonehenge Entrance", "Stonehenge Exit"],
        "Lumine Hall": ["Lumine Entrance", "Lumine Exit"],
        "Fire Spring": ["Fire Spring Entrance", "Fire Spring Exit"],
        "Sea of Eden": ["Sea Entrance Script", "Sea Exit Script"]
    }

    all_dungeon_doors = {
        "Arcade Entrance": EBDungeonDoor(0x0F00CC, 0x321000, 7),
        "Arcade Exit": EBDungeonDoor(0x0F029A, 0x321010, 5),
        "Arcade Back Exit": EBDungeonDoor(0x0F026E, 0x321020, 1),
        "Arcade Back Entrance": EBDungeonDoor(0x0F00C1, 0x321030, 5),
        "Giant Step Entrance": EBDungeonDoor(0x0F0032, 0x321040, 7),
        "Giant Step Exit": EBDungeonDoor(0x0F04B5, 0x321050, 5),
        "Happy-Happy HQ Entrance": EBDungeonDoor(0x0F09E9, 0x321060, 7),
        "Happy-Happy HQ Exit": EBDungeonDoor(0x0F0A99, 0x321070, 5),
        "Lilliput Steps Entrance": EBDungeonDoor(0x0F09F4, 0x321080, 3),
        "Lilliput Steps Exit": EBDungeonDoor(0x0F0B1A, 0x321090, 7),
        "Factory Entrance": EBDungeonDoor(0x0F1277, 0x3210A0, 5),
        "Factory Script Warp": EBDungeonDoor(0x15EECB, 0x3210B0, 5, True),
        "Factory Exit": EBDungeonDoor(0x0F1159, 0x3210C0, 5),
        "Factory Back Exit": EBDungeonDoor(0x0F11BC, 0x3210D0, 5),
        "Factory Back Entrance": EBDungeonDoor(0x0F11FE, 0x3210E0, 3),
        "Milky Well Entrance": EBDungeonDoor(0x0F12E9, 0x3210F0, 3),
        "Milky Well Exit": EBDungeonDoor(0x0F11E8, 0x321100, 5),
        "Mine Entrance": EBDungeonDoor(0x0F1378, 0x321110, 7),
        "Mine Exit": EBDungeonDoor(0x0F1400, 0x321120, 5),
        "Cafe Entrance": EBDungeonDoor(0x0F165D, 0x321150, 3),
        "Cafe Exit": EBDungeonDoor(0x0F1A25, 0x321160, 7),
        "Monotoli Entrance": EBDungeonDoor(0x0F1928, 0x321170, 7),
        "Monotoli Exit": EBDungeonDoor(0x0F1862, 0x321180, 3),
        "Maze Entrance": EBDungeonDoor(0x0F0EB6, 0x321190, 3),
        "Maze Exit": EBDungeonDoor(0x0F0FD8, 0x3211A0, 5),
        "Maze Back Exit": EBDungeonDoor(0x0F0FE3, 0x3211B0, 5),
        "Maze Back Entrance": EBDungeonDoor(0x0F0EC1, 0x3211C0, 7),
        "Rainy Entrance": EBDungeonDoor(0x0F0ED7, 0x3211D0, 7),
        "Rainy Exit": EBDungeonDoor(0x0F1030, 0x3211E0, 5),
        "Rainy Back Exit": EBDungeonDoor(0x0F0FEE, 0x3211F0, 5),
        "Rainy Back Entrance": EBDungeonDoor(0x0F0EAB, 0x321200, 3),
        "Sewer Entrance": EBDungeonDoor(0x0F1A3B, 0x321210, 5),
        "Sewer Exit": EBDungeonDoor(0x0F1A9E, 0x321220, 1),
        "Pink Cloud Entrance": EBDungeonDoor(0x0F1E32, 0x321230, 7),
        "Pink Cloud Exit": EBDungeonDoor(0x0F1EAB, 0x321240, 5),
        "Pyramid Entrance": EBDungeonDoor(0x0F1F3A, 0x321250, 3),
        "Pyramid Exit": EBDungeonDoor(0x0F1FA9, 0x321260, 5),
        "Pyramid Back Exit": EBDungeonDoor(0x0F20E8, 0x321290, 5),
        "Pyramid Back Entrance": EBDungeonDoor(0x0F1F45, 0x3212A0, 3),
        "D.M. Entrance Script": EBDungeonDoor(0x15F0A3, 0x321270, 7, True),
        "D.M. Exit Script": EBDungeonDoor(0x15F0CB, 0x321280, 5, True),
        "Stonehenge Entrance": EBDungeonDoor(0x0F105C, 0x3212B0, 7),
        "Stonehenge Exit": EBDungeonDoor(0x0F1072, 0x3212C0, 3),
        "Lumine Entrance": EBDungeonDoor(0x0F239C, 0x3212D0, 7),
        "Lumine Exit": EBDungeonDoor(0x0F2318, 0x3212E0, 3),
        "Fire Spring Entrance": EBDungeonDoor(0x0F23D4, 0x3212F0, 3),
        "Fire Spring Exit": EBDungeonDoor(0x0F2437, 0x321300, 5),
        "Sea Entrance Script": EBDungeonDoor(0x15F25B, 0x321310, 3, True),
        "Sea Exit Script": EBDungeonDoor(0x15ECEB, 0x321320, 5, True),
        "Post-Nightmare Script": EBDungeonDoor(0x15ED4B, 0x321330, 5, True),
        "Carpainter Failure Script": EBDungeonDoor(0x15EEF3, 0x321340, 7, True)
    }

    paired_doors = {}

    for door in all_dungeon_doors:
        rom.copy_bytes(all_dungeon_doors[door].address, 6, all_dungeon_doors[door].copyaddress)  # Copy 6 bytes at the source of the door to the destination of the door

    for door in world.dungeon_connections:
        for index, entrance in enumerate(dungeon_entrances[door]):
            if "Exit" in entrance:
                paired_doors[dungeon_entrances[world.dungeon_connections[door]][index]] = entrance
            else:
                paired_doors[entrance] = dungeon_entrances[world.dungeon_connections[door]][index]

    paired_doors["Post-Nightmare Script"] = paired_doors["Sea Exit Script"]
    paired_doors["Carpainter Failure Script"] = paired_doors["Happy-Happy HQ Exit"]

    for door in paired_doors:
        destination = all_dungeon_doors[paired_doors[door]]
        source = all_dungeon_doors[door]
        if source.is_script:
            if destination.is_script:
                rom.copy_bytes(destination.copyaddress, 6, source.address)
            else:
                rom.copy_bytes(destination.copyaddress + 2, 2, source.address)
                rom.copy_bytes(destination.copyaddress, 2, source.address + 2)
                rom.write_bytes(source.address + 4, bytearray([destination.direction]))
                rom.copy_bytes(destination.copyaddress + 4, 1, source.address + 5)
        else:
            if destination.is_script:
                rom.copy_bytes(destination.copyaddress + 2, 2, source.address)
                rom.copy_bytes(destination.copyaddress, 2, source.address + 2)
                rom.copy_bytes(destination.copyaddress + 5, 1, source.address + 4)
            else:
                rom.copy_bytes(destination.copyaddress, 5, source.address)

    rom.write_bytes(0x101664, struct.pack("H", 0x041F))  # Flag controlling the Saturn Valley ladder
    rom.write_bytes(0x0F19C7, struct.pack("I", 0xF3104C))  # Replacement for the Moonside deliveryman
    rom.write_bytes(0x0F0A93, struct.pack("I", 0x000000))  # Skip Pokey walking up after HHHQ
    rom.write_bytes(0x086DFC, struct.pack("H", 0x00C7))  # Flag-independent Moonside entry
    rom.write_bytes(0x0F1657, struct.pack("I", 0xF311A7))  # Fourside Cafe Door Script
    rom.write_bytes(0x0F165B, struct.pack("H", 0x8091))  # Lock Cafe
    rom.write_bytes(0x0FC8C6, struct.pack("I", 0xF3120B))  # Everdred script
    rom.write_bytes(0x10784A, struct.pack("H", 0x0000))  # Mook spawn in stonehenge anteroom
    rom.write_bytes(0x0FC51E, bytearray([0x00]))  # Moonside sparkle always active

    rom.write_bytes(0x0FA4D6, bytearray([0xC7, 0x00, 0x01]))

    moonside_reward = world.multiworld.get_location("Fourside - Post-Moonside Delivery", world.player).item
    if (moonside_reward.player != world.player) or world.options.remote_items or moonside_reward.name not in item_id_table:
        rom.write_bytes(0x3310F7, struct.pack("I", 0xF310FB))
