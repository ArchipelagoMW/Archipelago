import dolphin_memory_engine

from .Locations import NodeID
from .ClientUtils import KEY_TO_OFFSET  # type: ignore

ACTIVE_SLOT_OFFSET = 0x958


def check_flag(flag: int, address: int) -> bool:
    result = dolphin_memory_engine.read_byte(address)
    return (result & flag) != 0


def check_item_count(item_name: str, base_addr: int) -> int:
    """Checks the save data for if the item / number of items is in the inventory"""
    match (item_name):
        case "Progressive Master Sword":
            if check_flag(0x2, base_addr + 0xD6):  # Light Sword
                return 4
            if check_flag(0x2, base_addr + 0xD2):  # Master Sword
                return 3
            if check_flag(0x1, base_addr + 0xD2):  # Ordon Sword
                return 2
            if check_flag(0x80, base_addr + 0xD0):  # Wooden Sword
                return 1
            return 0

        case "Ordon Shield":
            if check_flag(0x4, base_addr + 0xD2):
                return 1
            return 0

        case "Hylian Shield":
            if check_flag(0x10, base_addr + 0xD2):
                return 1
            return 0

        case "Magic Armor":
            if check_flag(0x1, base_addr + 0xD1):
                return 1
            return 0

        case "Zora Armor":
            if check_flag(0x2, base_addr + 0xD1):
                return 1
            return 0

        case "Shadow Crystal":
            if check_flag(0x4, base_addr + 0xD1):
                return 1
            return 0

        case "Progressive Wallet":
            if check_flag(0x40, base_addr + 0xD1):  # Giant Wallet
                return 2
            if check_flag(0x20, base_addr + 0xD1):  # Big Wallet
                return 1
            return 0

        case "Hawkeye":
            if check_flag(0x40, base_addr + 0xD0):
                return 1
            return 0

        case "Gale Boomerang":
            if check_flag(0x1, base_addr + 0xD7):
                return 1
            return 0

        case "Spinner":
            if check_flag(0x2, base_addr + 0xD7):
                return 1
            return 0

        case "Ball and Chain":
            if check_flag(0x4, base_addr + 0xD7):
                return 1
            return 0

        case "Progressive Hero's Bow":
            if check_flag(0x40, base_addr + 0xD5):  # Giant Quiver
                return 3
            if check_flag(0x20, base_addr + 0xD5):  # Big Quiver
                return 2
            if check_flag(0x8, base_addr + 0xD7):  # Hero's Bow
                return 1
            return 0

        case "Progressive Clawshot":
            if check_flag(0x80, base_addr + 0xD7):  # Double Clawshot
                return 2
            if check_flag(0x10, base_addr + 0xD7):  # Clawshot
                return 1
            return 0

        case "Iron Boots":
            if check_flag(0x20, base_addr + 0xD7):
                return 1
            return 0

        case "Progressive Dominion Rod":
            if check_flag(0x40, base_addr + 0xD7):  # Dominion Rod
                return 2
            if check_flag(0x10, base_addr + 0xD6):  # Powerless Dominion Rod
                return 1
            return 0

        case "Lantern":
            if check_flag(0x1, base_addr + 0xD6):
                return 1
            return 0

        case "Progressive Fishing Rod":
            if check_flag(0x20, base_addr + 0xD0):  # Coral Earing
                return 2
            if check_flag(0x8, base_addr + 0xD6):  # Fishing Rod
                return 1
            return 0

        case "Slingshot":
            if check_flag(0x1, base_addr + 0xD8):
                return 1
            return 0

        case "Bomb Bag":
            if dolphin_memory_engine.read_byte(base_addr + 0xAD) != 0xFF:  # Bomb Bag 3
                return 3
            if dolphin_memory_engine.read_byte(base_addr + 0xAC) != 0xFF:  # Bomb Bag 2
                return 2
            if dolphin_memory_engine.read_byte(base_addr + 0xAB) != 0xFF:  # Bomb Bag 1
                return 1
            return 0

        case "Horse Call":
            if check_flag(0x10, base_addr + 0xDF):
                return 1
            return 0

        case "Auru's Memo":
            if check_flag(0x1, base_addr + 0xDD):
                return 1
            return 0

        case "Ashei's Sketch":
            if check_flag(0x2, base_addr + 0xDD):
                return 1
            return 0

        case "Progressive Mirror Shard":
            if check_flag(0x8, base_addr + 0x10A):  # City Shard
                return 4
            if check_flag(0x4, base_addr + 0x10A):  # Temple of Time Shard
                return 3
            if check_flag(0x2, base_addr + 0x10A):  # Snowpeak Shard
                return 2
            if check_flag(0x1, base_addr + 0x10A):  # Arbiters Shard
                return 1
            return 0

        case "Progressive Fused Shadow":
            if check_flag(0x4, base_addr + 0x109):  # Lakebed Shadow
                return 3
            if check_flag(0x2, base_addr + 0x109):  # Goron Shadow
                return 2
            if check_flag(0x1, base_addr + 0x109):  # Forest Shadow
                return 1
            return 0

        case "Progressive Hidden Skill":
            if check_flag(0x20, base_addr + 0x81A):  # Great Spin
                return 7
            if check_flag(0x40, base_addr + 0x81A):  # Jump Strike
                return 6
            if check_flag(0x80, base_addr + 0x81A):  # Mortal Draw
                return 5
            if check_flag(0x1, base_addr + 0x819):  # Helm Splitter
                return 4
            if check_flag(0x2, base_addr + 0x819):  # Backslice
                return 3
            if check_flag(0x8, base_addr + 0x819):  # Shield Attack
                return 2
            if check_flag(0x4, base_addr + 0x819):  # Ending Blow
                return 1
            return 0

        case "Giant Bomb Bag":
            if check_flag(0x80, base_addr + 0xD6):
                return 1
            return 0

        case "Male Beetle":
            if check_flag(0x1, base_addr + 0xE7):
                return 1
            return 0

        case "Female Beetle":
            if check_flag(0x2, base_addr + 0xE7):
                return 1
            return 0

        case "Male Butterfly":
            if check_flag(0x4, base_addr + 0xE7):
                return 1
            return 0

        case "Female Butterfly":
            if check_flag(0x8, base_addr + 0xE7):
                return 1
            return 0

        case "Male Stag Beetle":
            if check_flag(0x10, base_addr + 0xE7):
                return 1
            return 0

        case "Female Stag Beetle":
            if check_flag(0x20, base_addr + 0xE7):
                return 1
            return 0

        case "Male Grasshopper":
            if check_flag(0x40, base_addr + 0xE7):
                return 1
            return 0

        case "Female Grasshopper":
            if check_flag(0x80, base_addr + 0xE7):
                return 1
            return 0

        case "Male Phasmid":
            if check_flag(0x1, base_addr + 0xE6):
                return 1
            return 0

        case "Female Phasmid":
            if check_flag(0x2, base_addr + 0xE6):
                return 1
            return 0

        case "Male Pill Bug":
            if check_flag(0x4, base_addr + 0xE6):
                return 1
            return 0

        case "Female Pill Bug":
            if check_flag(0x8, base_addr + 0xE6):
                return 1
            return 0

        case "Male Mantis":
            if check_flag(0x10, base_addr + 0xE6):
                return 1
            return 0

        case "Female Mantis":
            if check_flag(0x20, base_addr + 0xE6):
                return 1
            return 0

        case "Male Ladybug":
            if check_flag(0x40, base_addr + 0xE6):
                return 1
            return 0

        case "Female Ladybug":
            if check_flag(0x80, base_addr + 0xE6):
                return 1
            return 0

        case "Male Snail":
            if check_flag(0x1, base_addr + 0xE5):
                return 1
            return 0

        case "Female Snail":
            if check_flag(0x2, base_addr + 0xE5):
                return 1
            return 0

        case "Male Dragonfly":
            if check_flag(0x4, base_addr + 0xE5):
                return 1
            return 0

        case "Female Dragonfly":
            if check_flag(0x8, base_addr + 0xE5):
                return 1
            return 0

        case "Male Ant":
            if check_flag(0x10, base_addr + 0xE5):
                return 1
            return 0

        case "Female Ant":
            if check_flag(0x20, base_addr + 0xE5):
                return 1
            return 0

        case "Male Dayfly":
            if check_flag(0x40, base_addr + 0xE5):
                return 1
            return 0

        case "Female Dayfly":
            if check_flag(0x80, base_addr + 0xE5):
                return 1
            return 0

        case "Poe Soul":
            return dolphin_memory_engine.read_byte(base_addr + 0x10C)

        case "Empty Bottle (Fishing Hole)":
            if dolphin_memory_engine.read_byte(base_addr + 0xAA) != 255:
                return 4
            elif dolphin_memory_engine.read_byte(base_addr + 0xA9) != 255:
                return 3
            elif dolphin_memory_engine.read_byte(base_addr + 0xA8) != 255:
                return 2
            elif dolphin_memory_engine.read_byte(base_addr + 0xA7) != 255:
                return 1
            else:
                return 0


        case _:
            if item_name in KEY_TO_OFFSET:
                key_offset = save_file_addr + 0x901 + KEY_TO_OFFSET[item_name]
                return dolphin_memory_engine.read_byte(key_offset)

            assert False, f"[Twilight Princess Client] could not handle  {item_name=} "


def check_dungeon_item_count(item_name: str, base_addr: int, node_number: int) -> int:

    match (item_name):
        case "Forest Temple Compass":
            if node_number == NodeID.Forest_Temple:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Forest_Temple * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "Forest Temple Map":
            if node_number == NodeID.Forest_Temple:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Forest_Temple * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0

        case "Goron Mines Compass":
            if node_number == NodeID.Goron_Mines:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Goron_Mines * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "Goron Mines Map":
            if node_number == NodeID.Goron_Mines:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Goron_Mines * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0

        case "Lakebed Temple Compass":
            if node_number == NodeID.Lakebed_Temple:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Lakebed_Temple * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "Lakebed Temple Map":
            if node_number == NodeID.Lakebed_Temple:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Lakebed_Temple * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0

        case "Arbiters Grounds Compass":
            if node_number == NodeID.Arbiters_Grounds:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Arbiters_Grounds * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "Arbiters Grounds Map":
            if node_number == NodeID.Arbiters_Grounds:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Arbiters_Grounds * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0

        case "Snowpeak Ruins Compass":
            if node_number == NodeID.Snowpeak_Ruins:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Snowpeak_Ruins * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "Snowpeak Ruins Map":
            if node_number == NodeID.Snowpeak_Ruins:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Snowpeak_Ruins * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0

        case "Temple of Time Compass":
            if node_number == NodeID.Temple_of_Time:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Temple_of_Time * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "Temple of Time Map":
            if node_number == NodeID.Temple_of_Time:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Temple_of_Time * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0

        case "City in The Sky Compass":
            if node_number == NodeID.City_in_the_Sky:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.City_in_the_Sky * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "City in The Sky Map":
            if node_number == NodeID.City_in_the_Sky:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.City_in_the_Sky * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0

        case "Palace of Twilight Compass":
            if node_number == NodeID.Palace_of_Twilight:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Palace_of_Twilight * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "Palace of Twilight Map":
            if node_number == NodeID.Palace_of_Twilight:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Palace_of_Twilight * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0

        case "Hyrule Castle Compass":
            if node_number == NodeID.Hyrule_Castle:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Hyrule_Castle * 32) + base_addr + 0x1D

            if check_flag(0x2, addr):
                return 1
            return 0

        case "Hyrule Castle Map":
            if node_number == NodeID.Hyrule_Castle:
                addr = base_addr + 0x1D + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Hyrule_Castle * 32) + base_addr + 0x1D

            if check_flag(0x1, addr):
                return 1
            return 0


def check_dungeon_key_count(item_name: str, base_addr: int, node_number: int) -> int:
    match (item_name):
        case "Forest Temple Small Key":
            if node_number == NodeID.Forest_Temple:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Forest_Temple * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)

        case "Goron Mines Small Key":
            if node_number == NodeID.Goron_Mines:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Goron_Mines * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)

        case "Lakebed Temple Small Key":
            if node_number == NodeID.Lakebed_Temple:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Lakebed_Temple * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)

        case "Arbiters Grounds Small Key":
            if node_number == NodeID.Arbiters_Grounds:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Arbiters_Grounds * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)

        case "Snowpeak Ruins Small Key":
            if node_number == NodeID.Snowpeak_Ruins:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Snowpeak_Ruins * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)

        case "Temple of Time Small Key":
            if node_number == NodeID.Temple_of_Time:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Temple_of_Time * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)

        case "City in The Sky Small Key":
            if node_number == NodeID.City_in_the_Sky:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.City_in_the_Sky * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)

        case "Palace of Twilight Small Key":
            if node_number == NodeID.Palace_of_Twilight:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Palace_of_Twilight * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)

        case "Hyrule Castle Small Key":
            if node_number == NodeID.Hyrule_Castle:
                addr = base_addr + 0x1C + ACTIVE_SLOT_OFFSET
            else:
                addr = (NodeID.Hyrule_Castle * 32) + base_addr + 0x1C

            return dolphin_memory_engine.read_byte(addr)
