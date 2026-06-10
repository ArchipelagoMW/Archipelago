"""
Async helpers for reading/writing Aria of Sorrow live memory through BizHawk.

``AoSRAM`` wraps a ``BizHawkContext`` (the ``ctx.bizhawk_ctx`` the client already
holds) with typed get/set primitives plus a few semantic accessors over the
addresses in ``addresses.py``. Each primitive is one BizHawk round-trip; the
``game_watcher`` can still batch raw reads via the address constants when it wants
a single request per tick.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import worlds._bizhawk as bizhawk

from . import addresses as addr
from .addresses import EWRAM
from .structures import EQUIPPED_GEAR_SIZE, VITALS_SIZE, EquippedGear, PlayerVitals

if TYPE_CHECKING:
    from worlds._bizhawk import BizHawkContext


class AoSRAM:
    """
    Typed accessor over AoS live memory for one BizHawk connection.
    """

    def __init__(self, bizhawk_ctx: "BizHawkContext") -> None:
        self.ctx = bizhawk_ctx

    # --- typed primitives ---------------------------------------------------
    async def read(self, offset: int, size: int, domain: str = EWRAM) -> bytes:
        return (await bizhawk.read(self.ctx, [(offset, size, domain)]))[0]

    async def read_u8(self, offset: int, domain: str = EWRAM) -> int:
        return (await self.read(offset, 1, domain))[0]

    async def read_u16(self, offset: int, domain: str = EWRAM) -> int:
        return int.from_bytes(await self.read(offset, 2, domain), "little")

    async def read_u32(self, offset: int, domain: str = EWRAM) -> int:
        return int.from_bytes(await self.read(offset, 4, domain), "little")

    async def write(self, offset: int, data: Sequence[int], domain: str = EWRAM) -> None:
        await bizhawk.write(self.ctx, [(offset, list(data), domain)])

    async def write_u8(self, offset: int, value: int, domain: str = EWRAM) -> None:
        await self.write(offset, [value & 0xFF], domain)

    async def write_u16(self, offset: int, value: int, domain: str = EWRAM) -> None:
        await self.write(offset, list((value & 0xFFFF).to_bytes(2, "little")), domain)

    async def write_u32(self, offset: int, value: int, domain: str = EWRAM) -> None:
        await self.write(offset, list((value & 0xFFFFFFFF).to_bytes(4, "little")), domain)

    async def guarded_write(self, offset: int, data: Sequence[int], expected: Sequence[int],
                            domain: str = EWRAM) -> bool:
        """
        Writes ``data`` at ``offset`` only if the bytes there still equal ``expected``.

        Returns False if the guard failed (the value changed underneath us);
        the caller should retry next tick rather than advancing any counter.
        """
        return await bizhawk.guarded_write(
            self.ctx, [(offset, list(data), domain)], [(offset, list(expected), domain)])

    # --- gameplay state -----------------------------------------------------
    async def is_in_gameplay(self) -> bool:
        """
        True only when it is safe to read checks / inject items: normal in-room
        gameplay, not paused / transitioning / in a menu / game-over (sec. 5b).
        """
        state, menu = await bizhawk.read(self.ctx, [
            (addr.GAME_STATE, 1, EWRAM),
            (addr.MENU_STATE, 1, EWRAM),
        ])
        return state[0] == addr.GameState.INGAME and menu[0] == addr.MENU_STATE_NORMAL

    # --- location detection -------------------------------------------------
    async def read_pickup_flags(self) -> bytes:
        return await self.read(addr.PICKUP_FLAGS, addr.PICKUP_FLAGS_LEN)

    @staticmethod
    def _flag_id(byte_index: int, bit: int) -> int:
        """
        The collected-pickup flag id for ``bit`` of byte ``byte_index`` of the 0x02000360
        bitfield -- the single home of the bit-numbering convention. LSB-first within each byte
        (byte 0 = ids 0-7, bit 0 = the 0x01 bit). VERIFIED against cvaos-decomp: the game
        tests these flags as ``unk_360[id >> 5] & (1 << (id & 0x1F))`` (src/code_0800F1FC.c), i.e.
        LSB-first little-endian u32 -- identical to this per-byte form. For MSB-first, change to
        ``byte_index * 8 + (7 - bit)``.
        """
        return byte_index * 8 + bit

    @staticmethod
    def pickup_flag_ids(flag_bytes: bytes) -> set[int]:
        """
        Set of collected-pickup flag ids whose bit is set. Maps each id through
        ``flag_offset -> ptr_address`` to get AP location ids; bit-numbering lives in ``_flag_id``.
        """
        ids: set[int] = set()
        for byte_index, value in enumerate(flag_bytes):
            for bit in range(8):
                if value & (1 << bit):
                    ids.add(AoSRAM._flag_id(byte_index, bit))
        return ids

    # --- typed structs ------------------------------------------
    async def get_vitals(self) -> PlayerVitals:
        """
        The full HP/MP block, typed (read ``.current_hp.value`` etc.).
        """
        return PlayerVitals.from_bytes(await self.read(addr.CURRENT_HP, VITALS_SIZE))

    async def get_equipped_gear(self) -> EquippedGear:
        """
        Currently-equipped weapon/souls/armor/accessory indices, typed.
        """
        return EquippedGear.from_bytes(await self.read(addr.EQUIPPED_WEAPON, EQUIPPED_GEAR_SIZE))

    async def get_current_hp(self) -> int:
        """
        Lean single-field read for the DeathLink poll. See `get_vitals` for the
        whole typed block.
        """
        return await self.read_u16(addr.CURRENT_HP)

    async def get_max_hp(self) -> int:
        """
        Lean single-field read for the DeathLink poll. See `get_vitals` for the
        whole typed block.
        """
        return await self.read_u16(addr.MAX_HP)

    async def kill_player(self) -> None:
        """
        Sets current HP to zero. Used to apply an incoming DeathLink.
        """
        await self.write_u16(addr.CURRENT_HP, 0)

    # --- goal flags ---------------------------------------------------------
    async def get_boss_flags(self) -> int:
        return await self.read_u16(addr.BOSS_FLAGS)

    async def get_global_flags(self) -> int:
        return await self.read_u32(addr.GLOBAL_FLAGS)

    async def has_defeated(self, boss_flag: int) -> bool:
        """
        ``boss_flag`` is one of the ``addr.BOSS_FLAG_*`` bit masks.
        """
        return bool(await self.get_boss_flags() & boss_flag)

    async def has_good_ending(self) -> bool:
        return bool(await self.get_global_flags() & addr.GLOBAL_FLAG_GOOD_ENDING)

    async def get_received_count(self) -> int:
        return await self.read_u16(addr.AP_RECEIVED_COUNT)

    async def set_received_count(self, count: int, expected: int) -> bool:
        """
        Advances the saved received-items counter to ``count``, guarded on its prior value
        ``expected`` so the client never blind-stomps the word. The counter lives on a verified-dead
        saved byte that only the client writes (see addr.AP_RECEIVED_COUNT), so the guard is
        belt-and-suspenders: returns ``False`` only if the word changed underneath us, in which case
        the caller re-reads and retries next tick instead of advancing.
        """
        return await self.guarded_write(
            addr.AP_RECEIVED_COUNT,
            list((count & 0xFFFF).to_bytes(2, "little")),
            list((expected & 0xFFFF).to_bytes(2, "little")))

    # --- giving items -------------------------------------------------------
    async def give_item(self, category: str, index: int, *, cap: int = 9) -> bool:
        """
        Increments the owned-count for one item, race-safely.

        ``category`` is an item_info category string (``"consumable"``,
        ``"weapon"``, ``"blue_soul"``, ...) and ``index`` is the item's id within
        that category (its ``item_info`` id, i.e. the EWRAM array index; this is NOT
        the pickup ``var_b`` for souls). AoS caps every owned-count -- consumables,
        equipment, and souls alike -- at ``cap`` (9); the game accepts a pickup at the
        cap but won't count it past 9, and we mirror that. A received item that would
        exceed the cap is dropped and logged (still returns ``True`` so the counter
        advances). Returns ``True`` on success/at-cap, or ``False`` if the guarded write
        lost a race -- retry next tick and do **not** advance the received counter.
        """
        array = addr.INVENTORY[category]
        if not 0 <= index < array.length:
            raise ValueError(f"{category} index {index} out of range (0..{array.length - 1})")

        if array.nibble_packed:
            byte_off = array.base + (index // 2)
            current = await self.read_u8(byte_off)
            high = index % 2 == 1
            count = (current >> 4) & 0x0F if high else current & 0x0F
            new = min(count + 1, cap)
            new_byte = (current & 0x0F) | (new << 4) if high else (current & 0xF0) | new
        else:
            byte_off = array.base + index
            current = await self.read_u8(byte_off)
            new_byte = min(current + 1, cap)

        if new_byte == current:
            # Already at the cap: AoS accepts the pickup but won't count it past 9, so a received copy
            # has nowhere to go. Log it (a real drop, not a race) rather than swallow it silently, then
            # report success so the received-counter still advances.
            from CommonClient import logger
            logger.warning("CVAoS: %s slot %d already at cap %d; received item dropped.",
                           category, index, cap)
            return True
        return await self.guarded_write(byte_off, [new_byte], [current])

    async def add_gold(self, amount: int) -> bool:
        """
        Adds ``amount`` to the player's gold (subtype-1 'money' pickups),
        race-safely. The caller resolves the money item to its gold value.
        """
        current = await self.read(addr.CURRENT_GOLD, 4)
        new_value = min(int.from_bytes(current, "little") + amount, 0xFFFFFFFF)
        return await self.guarded_write(
            addr.CURRENT_GOLD, list(new_value.to_bytes(4, "little")), list(current))
    
    async def set_flag_bit(self, offset: int, bit: int, value: int) -> bool:
        """
        Sets (``value`` truthy) or clears bit ``bit`` (0-7) of the EWRAM byte at ``offset``,
        race-safely. Returns ``True`` on success or no-op, ``False`` if the guarded write lost a
        race (retry next tick without advancing the received-counter).
        """
        current = await self.read_u8(offset)
        mask = 1 << bit
        new = current | mask if value else current & ~mask & 0xFF
        if new == current:
            return True
        return await self.guarded_write(offset, [new], [current])
