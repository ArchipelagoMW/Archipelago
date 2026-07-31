"""BizHawkClient for Mega Man X5 (PS1, SLUS-01334, NTSC-U).

Skeleton status — working core:
  * validates the game via the boot-EXE signature at 0x80010000
  * detects checks from the persistent save struct (weapons, heart tanks, intro)
  * grants received weapons and heart tanks by writing the save struct
All addresses verified in the workspace RAM notes (Reference/mmx5-ram-notes.md).

Known interim policies (deliberate, revisit before release):
  * HYBRID grants: locally-earned weapon bits are never cleared, so beating a
    boss still awards its vanilla weapon in addition to the AP item at that
    location. Pure randomization needs either a separate boss-defeated record
    or vanilla-grant suppression (ASM/overlay work).
  * Heart tank items are applied incrementally per session (client-side received
    index); totals can drift if reconnecting into an older save. Proper fix:
    persist the processed-count inside spare save-struct bytes once a safe spot
    is verified.
  * Armor capsules/tanks: locations exist but detection/grants are TODO until
    their bit layouts are verified.
  * Victory detection (Sigma) TODO.
"""
import logging
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

logger = logging.getLogger("Client")

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from . import names
from .locations import location_table

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

# --- RAM constants (PS1 address minus 0x80000000 = MainRAM offset) ---
EXE_SIG_ADDR = 0x010000
EXE_SIG = bytes([0x70, 0xE9, 0x0E, 0x80]) + b"\\ROCK_X5.DAT"

SAVE_BASE = 0x0D1C40          # save struct block we read each cycle
SAVE_LEN = 0x60
OFF_MAX_HP_X = 0x0D1C47 - SAVE_BASE
OFF_WEAPONS = 0x0D1C4C - SAVE_BASE
OFF_INTRO = 0x0D1C79 - SAVE_BASE
OFF_TANKS = 0x0D1C7F - SAVE_BASE
OFF_HEARTS = 0x0D1C80 - SAVE_BASE

# NOTE: 0x0D4F5x "enables" bytes proved stage-specific (00 during Izzy Glow
# gameplay) - NOT usable as a gameplay gate. Since we only write the persistent
# save struct, the write-safety condition is just "save struct initialized":
# max HP within its legal range (base 0x20 .. capped 0x40, 0x10 safety floor).

# Weapon bit order in 0x0D1C4C (bits 0-1 verified, 2-7 inferred from ammo-slot
# order — see RAM notes).
WEAPON_BITS = [names.CSHOT, names.DARK_HOLD, names.GOO_SHAVER, names.GROUND_FIRE,
               names.TRI_THUNDER, names.F_LASER, names.SPIKE_BALL, names.WING_SPIRAL]
WEAPON_TO_BIT = {name: i for i, name in enumerate(WEAPON_BITS)}

# Heart-tank bitfield stage mapping — only bit 6 verified so far. Unknown bits
# are logged but not sent as checks until mapped.
HEART_BIT_TO_STAGE = {
    6: names.NECROBAT,  # Dark Dizzy — verified 2026-07-30
}

BASE_MAX_HP = 0x20
HP_PER_HEART = 2


class MMX5Client(BizHawkClient):
    game = "Mega Man X5"
    system = "PSX"

    def __init__(self) -> None:
        super().__init__()
        self.items_processed = 0
        self.hearts_applied = 0
        self.last_gate_state = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            sig = (await bizhawk.read(ctx.bizhawk_ctx, [(EXE_SIG_ADDR, len(EXE_SIG), "MainRAM")]))[0]
            if sig != EXE_SIG:
                return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items, own-world items, starting inventory
        ctx.want_slot_data = True
        self.items_processed = 0
        self.hearts_applied = 0
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.slot is None:
            return

        try:
            save = (await bizhawk.read(ctx.bizhawk_ctx, [
                (SAVE_BASE, SAVE_LEN, "MainRAM"),
            ]))[0]
            in_gameplay = 0x10 <= save[OFF_MAX_HP_X] <= 0x40
            if in_gameplay != self.last_gate_state:
                logger.info(f"MMX5: save-struct gate -> {in_gameplay} (maxhp: {save[OFF_MAX_HP_X]:02X})")
                self.last_gate_state = in_gameplay

            # ---- Check detection (safe to do from any state: save struct
            # persists and only ever gains bits during legitimate play) ----
            new_checks = []

            def check(location_name: str, condition: bool) -> None:
                loc_id = location_table[location_name]
                if condition and loc_id not in ctx.checked_locations:
                    new_checks.append(loc_id)

            check(names.INTRO_CLEAR, save[OFF_INTRO] != 0)

            weapons_owned = save[OFF_WEAPONS]
            for bit, weapon in enumerate(WEAPON_BITS):
                stage = next(s for s, w in names.BOSS_WEAPON.items() if w == weapon)
                check(names.boss_location(stage), bool(weapons_owned & (1 << bit)))

            hearts = save[OFF_HEARTS]
            for bit in range(8):
                if hearts & (1 << bit):
                    stage = HEART_BIT_TO_STAGE.get(bit)
                    if stage is not None:
                        check(names.heart_location(stage), True)
                    # Unmapped bits: intentionally unsent until verified.

            if new_checks:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])

            # ---- Item grants (only while the save struct is live) ----
            if in_gameplay:
                grant_weapons = 0
                new_hearts = 0
                for item in ctx.items_received[self.items_processed:]:
                    item_name = ctx.item_names.lookup_in_game(item.item)
                    if item_name in WEAPON_TO_BIT:
                        grant_weapons |= 1 << WEAPON_TO_BIT[item_name]
                    elif item_name == names.HEART_TANK:
                        new_hearts += 1
                    # TODO: armor parts, tanks, filler energy

                writes = []
                # Weapons: OR received bits into the persistent bitfield
                # (guarded so we only commit against the value we just read).
                all_received_weapon_bits = 0
                for item in ctx.items_received:
                    item_name = ctx.item_names.lookup_in_game(item.item)
                    if item_name in WEAPON_TO_BIT:
                        all_received_weapon_bits |= 1 << WEAPON_TO_BIT[item_name]
                merged = weapons_owned | all_received_weapon_bits
                if merged != weapons_owned:
                    writes.append((SAVE_BASE + OFF_WEAPONS, [merged], "MainRAM"))

                if new_hearts:
                    new_max = min(0x40, save[OFF_MAX_HP_X] + HP_PER_HEART * new_hearts)
                    writes.append((SAVE_BASE + OFF_MAX_HP_X, [new_max], "MainRAM"))

                # Only mark items processed after a successful write, so a
                # failed guard retries next cycle instead of losing grants.
                success = True
                if writes:
                    success = await bizhawk.guarded_write(
                        ctx.bizhawk_ctx, writes,
                        [(SAVE_BASE + OFF_WEAPONS, bytes([weapons_owned]), "MainRAM")],
                    )
                    logger.info(f"MMX5: grants {'applied' if success else 'guard-failed, retrying'}: "
                                f"weapons={merged:02X} hearts+={new_hearts}")
                if success:
                    self.items_processed = len(ctx.items_received)
                    self.hearts_applied += new_hearts

            # TODO: victory detection (Sigma defeat address unknown) ->
            #   await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            # TODO: DeathLink via damage/death flag 0x800D1C1C once tested.

        except bizhawk.RequestFailedError:
            pass
