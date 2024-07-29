import random
import asyncio
import worlds._bizhawk as bizhawk
from typing import TYPE_CHECKING
from .Items import trap_table, base_item_id, item_table
from collections import namedtuple

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


trap_id_to_name = {value.index - base_item_id: key for key, value in trap_table.items()}

# Fall Damage and Ice Floor By: Forat Negre


class TrapData:
    def __init__(self, trap_name: str, trap_active: bool, received_position: int, start_time: int):
        self.trap_name = trap_name
        self.trap_active = trap_active
        self.received_position = received_position
        self.start_time = start_time
        self.trap_ended = False
        self.trap_announce = False


async def apply_trap(ctx: "BizHawkClientContext", trap_name: str) -> str:
    trap_value = 0
    trap_data = item_table[trap_name]
    return_string = ""

    if "Ice" in trap_name:
        await apply_ice_floor(ctx)
    elif "Fall" in trap_name:
        await apply_fall_damage(ctx)
    elif "Axe" in trap_name:
        await apply_axe_lord(ctx)
    elif "max" in trap_name:
        if "Half" in trap_name:
            trap_value = 0.5
        elif "80%" in trap_name:
            trap_value = 0.8

        max_value = await read_int(ctx, trap_data.address, 4, "MainRAM")
        new_value = int(max_value * trap_value)
        await bizhawk.write(ctx.bizhawk_ctx, [(trap_data.address, new_value.to_bytes(4, "little"), "MainRAM")])
        cur_value = await read_int(ctx, trap_data.address - 4, 4, "MainRAM")
        if cur_value > new_value:
            await bizhawk.write(ctx.bizhawk_ctx, [(trap_data.address - 4, new_value.to_bytes(4, "little"), "MainRAM")])
    elif "subtract" in trap_name:
        if "10" in trap_name:
            trap_value = 10
        elif "50" in trap_name:
            trap_value = 50

        cur_value = await read_int(ctx, trap_data.address, 4, "MainRAM")
        new_value = cur_value - trap_value
        if new_value < 0:
            new_value = 1
        await bizhawk.write(ctx.bizhawk_ctx, [(trap_data.address, new_value.to_bytes(4, "little"), "MainRAM")])
    elif "stone" in trap_name:
        await bizhawk.write(ctx.bizhawk_ctx, [(trap_data.address, b'\x0b', "MainRAM")])
        await bizhawk.write(ctx.bizhawk_ctx, [(trap_data.address + 2, b'\x00', "MainRAM")])
    elif "Teleport" in trap_name:
        await bizhawk.write(ctx.bizhawk_ctx, [(trap_data.address, b'\x00', "MainRAM")])
    elif "Close" in trap_name:
        return_string = await close_teleport(ctx)

    return return_string


async def close_teleport(ctx: "BizHawkClientContext") -> str:
    teleport = namedtuple("teleport", ["name", "map_address", "map_bit"])

    teleport_dict = {
        1: teleport("Abandoned Mine", 0x6be3c, 0),
        2: teleport("Outer Wall", 0x6bc92, 0),
        3: teleport("Castle Keep", 0x6bc3e, 6),
        4: teleport("Olrox's Quarters", 0x6bccd, 4),
        8: teleport("Reverse Entrance", 0x6c110, 6),
        9: teleport("Cave", 0x6c0ab, 6),
        10: teleport("Reverse Outer Wall", 0x6c255, 6),
        11: teleport("Reverse Castle Keep", 0x6c2a9, 0),
        12: teleport("Death Wing's Lair", 0x6c21a, 2),
    }
    # Castle entrance never close game mechanic
    # 0: teleport("Castle Entrance", 0x6bdd7, 0),

    teleport = await read_int(ctx, 0x03bebc, 2, "MainRAM")
    if teleport == 0 or teleport == 1:
        return "No suitable teleport to close"

    teleport_list = list(teleport_dict.keys())
    random.shuffle(teleport_list)

    while teleport_list:
        check_teleport = teleport_list.pop()
        if teleport & (1 << check_teleport):
            teleport = teleport & ~(1 << check_teleport)
            teleport_data = teleport_dict[check_teleport]
            await bizhawk.write(ctx.bizhawk_ctx,
                                [(0x03bebc, teleport.to_bytes(2, "little"), "MainRAM")])
            map_byte = await read_int(ctx, teleport_data.map_address, 1, "MainRAM")
            map_byte = map_byte & ~(1 << teleport_data.map_bit)
            await bizhawk.write(
                ctx.bizhawk_ctx, [(teleport_data.map_address, map_byte.to_bytes(1, "little"), "MainRAM")])
            return f"Closing teleport in: {teleport_data.name}"
    return ""


async def apply_ice_floor(ctx: "BizHawkClientContext"):
    await bizhawk.write(ctx.bizhawk_ctx ,[(0x10E39C, b'\xA4\xD9\x04\x08\x00\x00\x00\x00', "MainRAM"),
                                         (0x136690, b'\x14\x00\xa3\x94\x01\x00\x02\x34\x02\x00\x62\x14\x00\x00\x00'
                                                    b'\x00\x23\x20\x04\x00\xC3\x20\x04\x00\xC3\x20\x04\x00\x20\x20'
                                                    b'\x84\x00\x08\x00\xA6\x8C\x00\x00\x00\x00\x20\x20\x86\x00\xEC'
                                                    b'\x38\x04\x08', "MainRAM"),
                                         (0x10E1F4, b'\x08\x00\xE0\x03', "MainRAM"),
                                         (0x10E800, b'\x21\x00\x04\x3C', "MainRAM"),
                                         (0x10E484, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10E588, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10E7F4, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10E8AC, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10E9D0, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10ED70, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10FB38, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10FB7C, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10FC08, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10FC64, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10FCCC, b'\x00\x00\x00\x00', "MainRAM"),
                                         (0x10FD38, b'\x00\x00\x00\x00', "MainRAM")])


async def apply_fall_damage(ctx: "BizHawkClientContext"):
    await bizhawk.write(ctx.bizhawk_ctx, [
        (0x0FF0B8, b'\x09\x80\x15\x3C\xF4\x73\xB5\x92\x09\x80\x09\x3C\x04\x74\x35\xA1\x09\x80\x15\x3C\xF5\x73'
                   b'\xB5\x92\x09\x80\x09\x3C\x05\x74\x35\xA1\x08\x00\xE0\x03', "MainRAM"),
        (0x10E800, b'\x2E\xFC\x03\x0C\x00\x00\x00\x00', "MainRAM"),
        (0x10E8D8, b'\x2E\xFC\x03\x0C\x00\x00\x00\x00', "MainRAM"),
        (0x10E780, b'\x2E\xFC\x03\x0C\x00\x00\x00\x00', "MainRAM"),
        (0x10FDD8, b'\x2E\xFC\x03\x0C\x00\x00\x00\x00', "MainRAM"),
        (0x10EA34, b'\x2E\xFC\x03\x0C\x00\x00\x00\x00', "MainRAM"),
        (0x11E298, b'\x2E\xFC\x03\x0C\x00\x00\x00\x00', "MainRAM"),
        (0x111D10, b'\x2E\xFC\x03\x0C\x00\x00\x00\x00', "MainRAM"),
        (0x11007C, b'\x09\x80\x15\x3C\xF5\x73\xB5\x92\x09\x80\x10\x3F\xF4\x73\x10\x92\x09\x80\x16\x3C\x05\x74\xD6'
                   b'\x92\x09\x80\x18\x3C\x04\x74\x18\x93\xFF\x00\x05\x34\x18\x00\xB5\x00\x12\xA8\x00\x00\x21\xA8'
                   b'\x15\x02\x18\x00\xB6\x00\x12\xB0\x00\x00\x21\xB0\x16\x03\x63\xA8\xB6\x02\x20\x20\xA4\x02\x5F'
                   b'\x4F\x04\x0C\x00\x00\x00\x00\x09\x80\x0C\x3F\xA0\x7B\x8C\x91\x00\x00\x00\x00\x04\x00\x80\x1D'
                   b'\x10\x00\x06\x34\x07\x80\x09\x3C\x04\x34\x26\xA1\x5B\x40\x04\x08', "MainRAM"),
        (0x110068, b'\x1F\x00\x40\x10', "MainRAM")])

    # Remove poison and curse instructions
    await bizhawk.write(ctx.bizhawk_ctx, [(0x80114534, b'\x00\x00\x10\x21', "System Bus")])
    await bizhawk.write(ctx.bizhawk_ctx, [(0x801144ec, b'\x00\x00\x10\x21', "System Bus")])


# Thanks Skudd for Axe Lord trap idea
async def apply_axe_lord(ctx: "BizHawkClientContext"):
    # Prevent changing equipment during the trap
    await bizhawk.write(ctx.bizhawk_ctx, [(0x3c9a8, b'\x01', "MainRAM")])
    await bizhawk.write(ctx.bizhawk_ctx, [(0x800fa1ae, b'\x00\x00', "System Bus")])
    await bizhawk.write(ctx.bizhawk_ctx, [(0x800fa0d2, b'\x00\x00', "System Bus")])
    # Force open pause. Thanks for eldri7ch and bismurphy from Long Library discord for all info on that
    # Open pause to unload weapon
    await bizhawk.lock(ctx.bizhawk_ctx)
    await bizhawk.write(ctx.bizhawk_ctx, [(0x3c9a4, b'\x02', "MainRAM")])
    await bizhawk.write(ctx.bizhawk_ctx, [(0x978f8, b'\x00', "MainRAM")])
    await bizhawk.unlock(ctx.bizhawk_ctx)
    menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
    while menu_step[0] != b'\x10':
        menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
    # Remove hands and equip Axe Lord Armor
    await bizhawk.write(ctx.bizhawk_ctx, [(0x97c00, b'\x00', "MainRAM")])
    await bizhawk.write(ctx.bizhawk_ctx, [(0x97c04, b'\x00', "MainRAM")])
    await bizhawk.write(ctx.bizhawk_ctx, [(0x97c0c, b'\x19', "MainRAM")])
    # Close pause
    await bizhawk.write(ctx.bizhawk_ctx, [(0x978f8, b'\x03', "MainRAM")])


async def restore_ram(ctx: "BizHawkClientContext", trap_name: str):
    if "Fall damage" in trap_name:
        await bizhawk.write(ctx.bizhawk_ctx, [
            (0x0FF0B8, b'\xE8\xFF\xBD\x27\x10\x00\xB0\xAF\x21\x80\x00\x00\x14\x00\xBF\xAF\x28\xFC\x03\x0C\x21\x20'
                       b'\x00\x02\x01\x00\x10\x26\x10\x00\x02\x2A\xFB\xFF\x40\x14', "MainRAM"),
            (0x10E800, b'\x01\x00\x42\x30\x05\x00\x40\x10', "MainRAM"),
            (0x10E8D8, b'\x01\x00\x02\x34\x07\x00\x62\x14', "MainRAM"),
            (0x10E780, b'\x02\x00\x02\x34\x03\x00\x62\x14', "MainRAM"),
            (0x10FDD8, b'\x07\x80\x01\x3C\x66\x2F\x20\xA4', "MainRAM"),
            (0x10EA34, b'\x92\x36\x04\x0C\x21\x00\x04\x34', "MainRAM"),
            (0x11E298, b'\xDD\x78\x04\x08\x00\x00\x00\x00', "MainRAM"),
            (0x111D10, b'\x21\x30\x00\x00\x10\x00\xBF\x8F', "MainRAM"),
            (0x11007C, b'\x06\x00\x62\x10\x04\x00\x02\x34\x07\x80\x03\x3C\x04\x34\x63\x94\x00\x00\x00\x00\x08\x00\x62'
                       b'\x14\x00\x00\x00\x00\x07\x80\x05\x3C\xE0\x33\xA5\x8C\x03\x00\x04\x34\xC2\x17\x05\x00\x21\x28'
                       b'\xA2\x00\x2F\x40\x04\x08\x43\x28\x05\x00\x01\x00\x04\x34\x21\x28\x00\x00\x1C\x39\x04\x0C\x00'
                       b'\x00\x00\x00\xFE\xD1\x04\x0C\x47\x06\x04\x34\x07\x80\x04\x3C\xB8\xC3\x84\x8C\x70\x40\x04\x08'
                       b'\x21\x28\x00\x00\x07\x80\x02\x3C\x64\x2F\x42\x94\x00\x00\x00\x00', "MainRAM"),
            (0x110068, b'\x1C\x00\x40\x10', "MainRAM")])

        # Restore poison and curse instructions
        await bizhawk.write(ctx.bizhawk_ctx, [(0x80114534, b'\x00\x2f\x22\xa4', "System Bus")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x801144ec, b'\x02\x2f\x22\xa4', "System Bus")])
    elif "Ice floor" in trap_name:
        await bizhawk.write(ctx.bizhawk_ctx, [(0x10E39C, b'\x14\x00\xA3\x94\x01\x00\x02\x34', "MainRAM"),
                                              (0x136690, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                                         b'\x00\x00\x00', "MainRAM"),
                                              (0x10E1F4, b'\x00\x00\x00\x00', "MainRAM"),
                                              (0x10E800, b'\x01\x00\x42\x30', "MainRAM"),
                                              (0x10E484, b'\xE0\x33\x25\xAC', "MainRAM"),
                                              (0x10E588, b'\x00\x00\x24\xAE', "MainRAM"),
                                              (0x10E7F4, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10E8AC, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10E9D0, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10ED70, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10FB38, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10FB7C, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10FC08, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10FC64, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10FCCC, b'\xE0\x33\x20\xAC', "MainRAM"),
                                              (0x10FD38, b'\xE0\x33\x20\xAC', "MainRAM")])
    elif "Axe Lord" in trap_name:
        await bizhawk.lock(ctx.bizhawk_ctx)
        await bizhawk.write(ctx.bizhawk_ctx, [(0x800fa1ae, b'\xe2\xac', "System Bus")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x800fa0d2, b'\xe2\xac', "System Bus")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x3c9a4, b'\x02', "MainRAM")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x978f8, b'\x00', "MainRAM")])
        await bizhawk.unlock(ctx.bizhawk_ctx)
        # Unequip chest
        menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
        while menu_step[0] != b'\x10':
            menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x97c0c, b'\x00', "MainRAM")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x978f8, b'\x03', "MainRAM")])
    elif "Axe menu" in trap_name:
        await bizhawk.write(ctx.bizhawk_ctx, [(0x800fa1ae, b'\xe2\xac', "System Bus")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x800fa0d2, b'\xe2\xac', "System Bus")])


async def read_int(ctx: "BizHawkClientContext", address: int, size: int, domain: str) -> int:
    return int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address, size, domain)]))[0], "little")