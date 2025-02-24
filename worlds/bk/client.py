import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from typing import TYPE_CHECKING, List

from .Items import moves_table, ItemData
from .Locations import (jiggy_table, honeycomb_table, mumbo_token_table, mole_hill_table, witch_switch_table, puzzle_table,
                        note_door_table)

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object


class BKClient(BizHawkClient):
    game = "Banjo-Kazooie"
    system = "N64"

    def __init__(self) -> None:
        super().__init__()
        self.once = False
        self.checked_locations = []

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        print("DEBUG: Running BK client")
        ctx.game = self.game
        ctx.items_handling = 0b011
        ctx.want_slot_data = True
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not self.once:
            self.once = True
            unlocked_read = await bizhawk.read(ctx.bizhawk_ctx, [(0x37c3a0, 4, "RDRAM")])
            unlocked = int.from_bytes(unlocked_read[0], "big")
        await self.check_locations(ctx)

    async def check_locations(self, ctx: "BizHawkClientContext") -> None:
        collected_jiggies = await bizhawk.read(ctx.bizhawk_ctx, [(0x3832c0, 7, "RDRAM")])
        jiggies = int.from_bytes(collected_jiggies[0], "big")
        collected_hc = await bizhawk.read(ctx.bizhawk_ctx, [(0x3832e0, 4, "RDRAM")])
        hc = int.from_bytes(collected_hc[0], "big")
        mole_hill = await bizhawk.read(ctx.bizhawk_ctx, [(0x37c3a0, 4, "RDRAM")])
        mh = int.from_bytes(mole_hill[0], "big")
        mumbo_token = await bizhawk.read(ctx.bizhawk_ctx, [(0x3832f0, 4, "RDRAM")])
        mt = int.from_bytes(mumbo_token[0], "big")
        witch_switch = await bizhawk.read(ctx.bizhawk_ctx, [(0x3831ab, 2, "RDRAM")])
        ws = int.from_bytes(witch_switch[0], "big")
        jigsaw_puzzle = await bizhawk.read(ctx.bizhawk_ctx, [(0x3831b0, 4, "RDRAM")])
        jp = int.from_bytes(jigsaw_puzzle[0], "big")
        note_door = await bizhawk.read(ctx.bizhawk_ctx, [(0x3831af, 1, "RDRAM")])
        nd = int.from_bytes(note_door[0], "big")

        for k, v in jiggy_table.items():
            if k not in self.checked_locations:
                if jiggies & (1 << (55 - v.game_code)):
                    print(f"New check: {k}")
                    self.checked_locations.append(k)

        for k, v in mumbo_token_table.items():
            if k not in self.checked_locations:
                if mt & (1 << (31 - v.game_code)):
                    print(f"New check: {k}")
                    self.checked_locations.append(k)

        for k, v in honeycomb_table.items():
            if k not in self.checked_locations:
                if hc & (1 << (31 - v.game_code)):
                    print(f"New check: {k}")
                    self.checked_locations.append(k)

        for k, v in mole_hill_table.items():
            if k not in self.checked_locations:
                if mh & (1 << (31 - v.game_code)):
                    print(f"New check: {k}")
                    self.checked_locations.append(k)

        for k, v in witch_switch_table.items():
            if k not in self.checked_locations:
                if ws & (1 << (15 - v.game_code)):
                    print(f"New check: {k}")
                    self.checked_locations.append(k)

        for k, v in puzzle_table.items():
            if k not in self.checked_locations:
                checked: bool = False
                if v.game_address == 0x00:
                    if jp & (1 << (31 - v.game_code)):
                        checked = True
                else:
                    value = await bizhawk.read(ctx.bizhawk_ctx, [(v.game_address, 4, "RDRAM")])
                    value_int = int.from_bytes(value[0], "big")
                    if value_int & v.bit_mask == v.bit_mask:
                        checked = True

                if checked:
                    print(f"New check: {k}")
                    self.checked_locations.append(k)

        for k, v in note_door_table.items():
            if k not in self.checked_locations:
                if nd & (1 << (7 - v.game_code)):
                    print(f"New check: {k}")
                    self.checked_locations.append(k)


    @staticmethod
    async def update_abilities(ctx: "BizHawkClientContext", unlocked: List) -> None:
        result: int = 0x04  # Start with camera controls unlocked

        for ability in unlocked:
            try:
                item: ItemData = moves_table[ability]
                result |= 1 << item.game_code
            except KeyError:
                pass

        unlocked_read = await bizhawk.read(ctx.bizhawk_ctx, [(0x37c3a0, 4, "RDRAM")])

        result_bytes = int.to_bytes(result, 4, "big")

        if unlocked_read[0] != result_bytes:
            await bizhawk.write(ctx.bizhawk_ctx, [(0x37c3a0, result_bytes, "RDRAM")])


