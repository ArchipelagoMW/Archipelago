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
  * Processed-items count persists in spare save bytes (u16 0x800D1C4E,
    memcard-persisted, savestate-coherent) - reconnects/restarts no longer
    re-apply grants. First connect on a pre-scheme save applies everything
    once (count reads 0), then stabilizes. Wrong-save protection: seed/slot
    stamp byte at 0x800D1C50 (see OFF_STAMP) halts checks+grants on a save
    stamped for a different seed/slot.
  * Pickup checks are dual-path: save-struct bits (vanilla/v2 discs, hybrid)
    or the stub's mailbox ring (proto v3+ discs, where vanilla pickup effects
    are suppressed and save bits never set themselves). Ring records are
    consumed only after the server confirms the location.
  * Tanks: locations + ring detection + grants (u16 0x1C7E bits 12-15) done.
    Armor capsules: locations exist but detection/grants are TODO (spec
    item 6 hook not built yet).
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
SAVE_LEN = 0xA0               # extended to cover launch score/flags/countdown
OFF_MAX_HP_X = 0x0D1C47 - SAVE_BASE
OFF_MAX_HP_Z = 0x0D1C48 - SAVE_BASE
OFF_WEAPONS = 0x0D1C4C - SAVE_BASE      # vanilla weapons/boss-beaten record
OFF_AP_WEAPONS = 0x0D1C4D - SAVE_BASE   # AP-owned capability byte (patched disc)
# Processed-items count, u16 LE in spare memcard-persisted save bytes
# (0x1C4D-0x1C50 run, never written by the game). Survives client restarts,
# rides the memory card, and rewinds coherently with savestates - fixing the
# reconnect re-grant drift (hearts +2 each on every fresh session).
OFF_PROCESSED = 0x0D1C4E - SAVE_BASE
# Seed/slot stamp in the LAST spare persisted byte (0x1C4D weapons,
# 0x1C4E/4F processed count, 0x1C50 stamp): 1-byte hash of seed+slot,
# 0 = unstamped. A sane save stamped for a DIFFERENT seed/slot halts both
# checks and grants (wrong-save protection, A3). Adopted (written) with the
# first grant batch on an unstamped save.
OFF_STAMP = 0x0D1C50 - SAVE_BASE
OFF_INTRO = 0x0D1C79 - SAVE_BASE
OFF_TANKS = 0x0D1C7F - SAVE_BASE
OFF_HEARTS = 0x0D1C80 - SAVE_BASE
# Launch machinery (overlay-findings 11). Score = 2*sum(0x1CC2..C5) + 0x1CCA;
# on the patched disc the roll is `li v1,0`, so success <=> score > 0. The
# client PINS these every cycle from AP part-item state - vanilla accrual
# must never decide a launch. 0x1CCB bit7 = launch-success flag (victory
# marker for the launch goal). 0x1CAC u32 = collision countdown in frames.
OFF_SCORE_ACC = 0x0D1CC2 - SAVE_BASE   # 4 accumulator bytes
OFF_SCORE_MOD = 0x0D1CCA - SAVE_BASE   # additive modifier byte
OFF_LAUNCH_FLAGS = 0x0D1CCB - SAVE_BASE
OFF_COUNTDOWN = 0x0D1CAC - SAVE_BASE
COUNTDOWN_FROZEN = 8 * 0x34BC0         # 8 hours, pinned (design answer 5)
GOAL_LAUNCH = 1

# AP disc-patch detection: the first stage-load weapon-repopulation site.
# Vanilla: lbu $v0,0x4C($a1) = 90 A2 00 4C; AP patch changes the offset byte
# to 0x4D so capability derives from the AP byte while 0x1C4C keeps
# recording kills (story chapters advance on its popcount - never suppress).
PATCH_PROBE_ADDR = 0x03C324
PATCH_PROBE_VANILLA = bytes.fromhex("4C00A290")
PATCH_PROBE_PATCHED = bytes.fromhex("4D00A290")

# Pickup-stub detection (proto v3+ discs): the jump-table entry for pickup
# kind 0 at 0x80011068 either holds the vanilla heart handler or the shared
# check-record stub at 0x800776A0 (patch spec item 2).
STUB_PROBE_ADDR = 0x011068
STUB_PROBE_VANILLA = bytes.fromhex("A0400580")   # 0x800540A0 LE
STUB_PROBE_STUBBED = bytes.fromhex("A0760780")   # 0x800776A0 LE

# Mailbox check-record ring, written by the stub on every randomized pickup:
# 16 slots of {stage u8, kind u8, id u8, seq u8} at 0x801FA020, monotonic
# pickup count u32 at 0x801FA080. seq bit7 marks a valid record (a zeroed
# slot is never one); the client consumes a record by zeroing its seq byte.
# The whole region is plain RAM: savestates wipe it, which only loses
# records in the sub-second window between pickup and this poll.
RING_ADDR = 0x1FA020
RING_SLOTS = 16
RING_COUNT_ADDR = 0x1FA080

# Ring record stage byte (0x800D1C41) -> stage name, verified stage-id order.
STAGE_ID_TO_NAME = {
    1: names.GRIZZLY, 2: names.NECROBAT, 3: names.WHALE, 4: names.DINOREX,
    5: names.KRAKEN, 6: names.FIREFLY, 7: names.ROSERED, 8: names.PEGASUS,
}

# Ring record (kind, id) -> tank location stage. Placement harvest 2026-07-31:
# sub-tanks are kind 9 with globally-unique ids; W/EX tanks are unique kinds.
TANK_RECORD_TO_STAGE = {
    (0x9, 0x27): names.GRIZZLY,    # Sub-Tank #1
    (0x9, 0x28): names.NECROBAT,   # Sub-Tank #2
    (0xA, 0x29): names.PEGASUS,    # W-Tank
    (0xB, 0x2A): names.FIREFLY,    # EX-Tank
}

# Tank bits in save u16 0x800D1C7E live in the HIGH byte 0x1C7F (bits 12-15
# of the u16 = bits 4-7 of the byte): sub1/sub2/W/EX.
TANK_ITEM_BYTE_BITS = {names.W_TANK: 0x40, names.EX_TANK: 0x80}
SUB_TANK_BYTE_BITS = [0x10, 0x20]  # first, second received Sub-Tank

# NOTE: 0x0D4F5x "enables" bytes proved stage-specific (00 during Izzy Glow
# gameplay) - NOT usable as a gameplay gate. Since we only write the persistent
# save struct, the write-safety condition is just "save struct initialized":
# max HP within its legal range (base 0x20 .. capped 0x40, 0x10 safety floor).

# Weapon bit order in 0x0D1C4C (bits 0, 1, 5 verified in-game; rest inferred
# from ammo-slot order — see RAM notes).
WEAPON_BITS = [names.CSHOT, names.DARK_HOLD, names.GOO_SHAVER, names.GROUND_FIRE,
               names.TRI_THUNDER, names.F_LASER, names.SPIKE_BALL, names.WING_SPIRAL]
WEAPON_TO_BIT = {name: i for i, name in enumerate(WEAPON_BITS)}

# Heart-tank bitfield stage mapping — complete via placement-record harvest
# 2026-07-31 (Scripts/mmx5_placement_dump.lua); bits 2 and 6 also live-verified.
# NOT stage-id order: the bit is the placement record's id byte.
HEART_BIT_TO_STAGE = {
    0: names.GRIZZLY,
    1: names.KRAKEN,    # Squid Adler
    2: names.FIREFLY,   # Izzy Glow — live-verified (pickup, 0x40->0x44)
    3: names.WHALE,     # Duff McWhalen
    4: names.PEGASUS,   # The Skiver
    5: names.ROSERED,   # Axle the Red (unique ungated record + elimination)
    6: names.NECROBAT,  # Dark Dizzy — live-verified 2026-07-30
    7: names.DINOREX,   # Mattrex
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
        self.ap_patched = False
        self.stub_present = False
        self.unknown_records_logged = set()
        self.stamp_warned = False
        self.victory_sent = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            sig, probe, stub_probe = await bizhawk.read(ctx.bizhawk_ctx, [
                (EXE_SIG_ADDR, len(EXE_SIG), "MainRAM"),
                (PATCH_PROBE_ADDR, 4, "MainRAM"),
                (STUB_PROBE_ADDR, 4, "MainRAM"),
            ])
            if sig != EXE_SIG:
                return False
        except bizhawk.RequestFailedError:
            return False

        # Hybrid-mode fallback on vanilla discs stays supported during
        # development; the AP disc patch decouples weapon capability.
        # None = undetermined (validate can race the EXE still streaming in
        # from disc - the probe reads zeros during boot); game_watcher
        # re-probes before granting anything.
        self.ap_patched = self._classify_probe(probe)
        self.stub_present = self._classify_stub_probe(stub_probe)
        if self.ap_patched is None:
            logger.info(f"MMX5: disc mode undetermined at boot (probe {probe.hex()}) - will re-probe in-game")

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items, own-world items, starting inventory
        ctx.want_slot_data = True
        self.items_processed = 0
        self.hearts_applied = 0
        return True

    @staticmethod
    def _classify_probe(probe: bytes):
        if probe == PATCH_PROBE_PATCHED:
            logger.info("MMX5: disc mode = AP-PATCHED (capability byte 0x1C4D)")
            return True
        if probe == PATCH_PROBE_VANILLA:
            logger.info("MMX5: disc mode = vanilla (hybrid grants)")
            return False
        return None

    @staticmethod
    def _seed_stamp(ctx: "BizHawkClientContext") -> int:
        # Deterministic 1-byte hash of seed+slot (never 0 = unstamped).
        # Python's hash() is salted per-process - roll our own.
        h = 0
        for ch in f"{ctx.seed_name}:{ctx.auth}":
            h = (h * 31 + ord(ch)) & 0xFF
        return h or 1

    @staticmethod
    def _classify_stub_probe(probe: bytes):
        if probe == STUB_PROBE_STUBBED:
            logger.info("MMX5: pickup stub RESIDENT - checks come from the mailbox ring")
            return True
        if probe == STUB_PROBE_VANILLA:
            logger.info("MMX5: pickup stub absent - pickup checks from save-struct bits")
            return False
        return None

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.slot is None:
            return

        try:
            mode, save, ring = await bizhawk.read(ctx.bizhawk_ctx, [
                (0x0D1C00, 1, "MainRAM"),  # game-mode controller: 0x0A gameplay / 0x0C results
                (SAVE_BASE, SAVE_LEN, "MainRAM"),
                (RING_ADDR, RING_SLOTS * 4, "MainRAM"),  # pickup-stub check records
            ])
            # Grants are safe whenever the save struct is live: gameplay or
            # results mode, plus a sanity floor on max HP against garbage states.
            save_sane = 0x10 <= save[OFF_MAX_HP_X] <= 0x40
            in_gameplay = mode[0] in (0x0A, 0x0C) and save_sane
            if in_gameplay != self.last_gate_state:
                logger.info(f"MMX5: save-struct gate -> {in_gameplay} (maxhp: {save[OFF_MAX_HP_X]:02X})")
                self.last_gate_state = in_gameplay
                # Savestates restore ALL of RAM including the loaded EXE, so
                # the disc mode can CHANGE mid-session. Re-probe on EVERY
                # gate transition (stage entry AND exit-to-hub).
                self.ap_patched = None
                self.stub_present = None

            # Resolve the probes whenever unresolved - NOT just in-stage.
            # Launches happen at the HUB (modes 0x13-0x15); the old
            # in-gameplay-only resolution left ap_patched unresolved on a
            # boot-to-hub path and score pinning silently no-oped (live
            # 2026-08-01: an unpinned Enigma launch succeeded off vanilla
            # accrual + the zeroed roll). During boot the EXE reads as
            # zeros -> classify returns None -> retried next cycle.
            if self.ap_patched is None or self.stub_present is None:
                probe, stub_probe = await bizhawk.read(ctx.bizhawk_ctx, [
                    (PATCH_PROBE_ADDR, 4, "MainRAM"),
                    (STUB_PROBE_ADDR, 4, "MainRAM"),
                ])
                self.ap_patched = self._classify_probe(probe)
                self.stub_present = self._classify_stub_probe(stub_probe)

            # ---- Wrong-save protection (A3): a sane save stamped for a
            # DIFFERENT seed/slot halts checks AND grants - its bits belong
            # to another game. Swap saves, or deliberately reuse this one by
            # zeroing 0x1C4D-0x1C50 in the Lua console. Unstamped saves (0)
            # pass and get stamped with their first grant batch. ----
            if save_sane and ctx.seed_name:
                if save[OFF_STAMP] not in (0, self._seed_stamp(ctx)):
                    if not self.stamp_warned:
                        self.stamp_warned = True
                        logger.warning(
                            f"MMX5: save is stamped {save[OFF_STAMP]:02X} but this seed/slot "
                            f"expects {self._seed_stamp(ctx):02X} - WRONG SAVE, checks and "
                            f"grants held (zero 0x1C4D-0x1C50 via Lua to deliberately reuse it)")
                    return
                if self.stamp_warned:
                    self.stamp_warned = False
                    logger.info("MMX5: save stamp OK - resuming")

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

            # ---- Pickup-stub ring (stub discs only): the stub suppresses
            # vanilla pickup effects, so heart/tank save bits never set
            # themselves - the ring records ARE the checks there. ----
            if self.stub_present:
                ack_writes, ack_guards = [], []
                for slot in range(RING_SLOTS):
                    rec = ring[slot * 4:slot * 4 + 4]
                    stage_id, kind, rec_id, seq = rec
                    if not seq & 0x80:
                        continue  # empty/consumed slot
                    stage = STAGE_ID_TO_NAME.get(stage_id)
                    loc_name = None
                    if kind == 0x0 and stage is not None \
                            and HEART_BIT_TO_STAGE.get(rec_id) == stage:
                        loc_name = names.heart_location(stage)
                    elif kind == 0x1 and stage is not None and 0x10 <= rec_id <= 0x17:
                        # Energy-Ups: one per stage; the stage byte alone
                        # identifies the location (ids are globally unique
                        # bits but their stage map is still being harvested).
                        loc_name = names.energy_up_location(stage)
                    elif (kind, rec_id) in TANK_RECORD_TO_STAGE:
                        loc_name = names.tank_location(TANK_RECORD_TO_STAGE[(kind, rec_id)])

                    if loc_name is not None:
                        check(loc_name, True)
                        # Consume only once the server has confirmed the
                        # location; until then the record persists and the
                        # (idempotent) check is simply re-sent each poll.
                        consume = location_table[loc_name] in ctx.checked_locations
                    else:
                        # Kind-0 stage mismatches are Axle's armor-gated
                        # decoy heart records; anything else is unmapped.
                        # Either way: log once, consume, don't send.
                        rec_key = (stage_id, kind, rec_id)
                        if rec_key not in self.unknown_records_logged:
                            self.unknown_records_logged.add(rec_key)
                            logger.info(f"MMX5: unmapped pickup record stage={stage_id} "
                                        f"kind={kind:X} id={rec_id:02X} - ignored")
                        consume = True
                    if consume:
                        # Zero the seq byte, guarded on the whole slot so a
                        # concurrent stub overwrite loses cleanly (retry next poll).
                        ack_writes.append((RING_ADDR + slot * 4 + 3, [0], "MainRAM"))
                        ack_guards.append((RING_ADDR + slot * 4, rec, "MainRAM"))
                if ack_writes:
                    await bizhawk.guarded_write(ctx.bizhawk_ctx, ack_writes, ack_guards)

            # ---- Launch control (patched discs only): pin the score bytes
            # so launches succeed exactly when AP part state allows (the
            # disc patch turns the roll into `li v1,0`, so success <=>
            # score > 0), freeze the countdown (design answer 5), and
            # detect launch-goal victory (0x1CCB bit7). Pinning runs every
            # cycle - vanilla accrual must never decide a launch. ----
            if self.ap_patched and save_sane:
                lookup = ctx.item_names.lookup_in_game
                enigma = sum(1 for i in ctx.items_received if lookup(i.item) == names.ENIGMA_PART)
                shuttle = sum(1 for i in ctx.items_received if lookup(i.item) == names.SHUTTLE_PART)
                goal = (ctx.slot_data or {}).get("goal", 0)
                if goal == GOAL_LAUNCH:
                    # Launch goal: nothing fires until every part is in hand.
                    powered = enigma >= 4 and shuttle >= 4
                else:
                    # Story flavor: power whichever launcher the chapter
                    # offers (shuttle era begins at 6 recorded kills).
                    kills = bin(save[OFF_WEAPONS]).count("1")
                    powered = (shuttle >= 4) if kills >= 6 else (enigma >= 4)
                pin = []
                if save[OFF_SCORE_ACC:OFF_SCORE_ACC + 4] != b"\x00\x00\x00\x00":
                    pin.append((SAVE_BASE + OFF_SCORE_ACC, [0, 0, 0, 0], "MainRAM"))
                want_mod = 1 if powered else 0
                if save[OFF_SCORE_MOD] != want_mod:
                    pin.append((SAVE_BASE + OFF_SCORE_MOD, [want_mod], "MainRAM"))
                countdown = int.from_bytes(save[OFF_COUNTDOWN:OFF_COUNTDOWN + 4], "little")
                if countdown != COUNTDOWN_FROZEN:
                    pin.append((SAVE_BASE + OFF_COUNTDOWN,
                                list(COUNTDOWN_FROZEN.to_bytes(4, "little")), "MainRAM"))
                if pin:
                    await bizhawk.write(ctx.bizhawk_ctx, pin)
                if goal == GOAL_LAUNCH and not self.victory_sent \
                        and save[OFF_LAUNCH_FLAGS] & 0x80:
                    self.victory_sent = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    logger.info("MMX5: launch succeeded - GOAL complete!")

            if new_checks:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])

            # ---- Item grants (only while the save struct is live) ----
            if in_gameplay:
                # Resolve disc mode if boot raced the EXE load; in gameplay
                # the EXE is fully resident, so this settles on first cycle.
                # Probes resolve at the top of every cycle now; in-stage the
                # EXE is fully resident so an unresolved probe here is
                # genuinely abnormal - hold grants.
                if self.ap_patched is None:
                    logger.warning("MMX5: disc mode unresolved in-game - grants held")
                    return
                # Source of truth for "how many received items are already
                # applied to THIS save" lives IN the save (u16 at 0x1C4E):
                # memcard-persisted, savestate-coherent, restart-proof.
                # The old in-memory counter re-applied everything each
                # session (the +2-max-HP-per-heart reconnect drift).
                processed = save[OFF_PROCESSED] | (save[OFF_PROCESSED + 1] << 8)
                total = len(ctx.items_received)
                if processed > total:
                    # More applied than the server knows: rewound-to-newer
                    # save vs older seed state, or a foreign save. Clamp and
                    # warn; proper wrong-save protection = seed stamp (A3).
                    logger.warning(f"MMX5: save says {processed} items applied but server sent {total} - clamping")
                    processed = total

                if processed < total:
                    new_hearts = 0
                    for item in ctx.items_received[processed:]:
                        item_name = ctx.item_names.lookup_in_game(item.item)
                        if item_name == names.HEART_TANK:
                            new_hearts += 1
                        # weapons handled cumulatively below; TODO: armor,
                        # tanks, filler energy once their state is AP-owned

                    writes = []
                    # Weapons: OR ALL received bits into the capability byte
                    # (idempotent). AP-patched disc: 0x1C4D (0x1C4C keeps
                    # recording kills - story chapters advance on its
                    # popcount). Vanilla disc: hybrid mode, write 0x1C4C.
                    wep_off = OFF_AP_WEAPONS if self.ap_patched else OFF_WEAPONS
                    capability = save[wep_off]
                    all_received_weapon_bits = 0
                    tank_bits = 0
                    sub_tanks_received = 0
                    for item in ctx.items_received:
                        item_name = ctx.item_names.lookup_in_game(item.item)
                        if item_name in WEAPON_TO_BIT:
                            all_received_weapon_bits |= 1 << WEAPON_TO_BIT[item_name]
                        elif item_name == names.SUB_TANK and sub_tanks_received < 2:
                            tank_bits |= SUB_TANK_BYTE_BITS[sub_tanks_received]
                            sub_tanks_received += 1
                        elif item_name in TANK_ITEM_BYTE_BITS:
                            tank_bits |= TANK_ITEM_BYTE_BITS[item_name]
                    merged = capability | all_received_weapon_bits
                    if merged != capability:
                        writes.append((SAVE_BASE + wep_off, [merged], "MainRAM"))

                    # Tanks: same idempotent OR into the u16 0x1C7E high byte
                    # (bits 12-15: sub1/sub2/W/EX - engine-honored, appear in
                    # the pause menu immediately). Granted sub-tanks start
                    # empty, exactly like a vanilla save-reload after pickup.
                    merged_tanks = save[OFF_TANKS] | tank_bits
                    if merged_tanks != save[OFF_TANKS]:
                        writes.append((SAVE_BASE + OFF_TANKS, [merged_tanks], "MainRAM"))

                    if new_hearts:
                        # BOTH characters (design decision 2026-08-01):
                        # vanilla hearts only boost the collector, but an AP
                        # heart item shouldn't shortchange whoever's benched.
                        new_max_x = min(0x40, save[OFF_MAX_HP_X] + HP_PER_HEART * new_hearts)
                        new_max_z = min(0x40, save[OFF_MAX_HP_Z] + HP_PER_HEART * new_hearts)
                        writes.append((SAVE_BASE + OFF_MAX_HP_X, [new_max_x, new_max_z], "MainRAM"))

                    # Adopt an unstamped save on its first grant batch.
                    if ctx.seed_name and save[OFF_STAMP] == 0:
                        writes.append((SAVE_BASE + OFF_STAMP,
                                       [self._seed_stamp(ctx)], "MainRAM"))

                    # Commit the new processed-count in the SAME guarded
                    # batch as the effects it accounts for.
                    writes.append((SAVE_BASE + OFF_PROCESSED,
                                   [total & 0xFF, (total >> 8) & 0xFF], "MainRAM"))

                    # Guard on the count we based the batch on: retries
                    # cleanly if anything moved between read and write.
                    success = await bizhawk.guarded_write(
                        ctx.bizhawk_ctx, writes,
                        [(SAVE_BASE + OFF_PROCESSED,
                          bytes([processed & 0xFF, (processed >> 8) & 0xFF]), "MainRAM")],
                    )
                    logger.info(f"MMX5: grants {'applied' if success else 'guard-failed, retrying'}: "
                                f"items {processed}->{total}, "
                                f"weapons({'AP' if self.ap_patched else 'vanilla'})={merged:02X} "
                                f"tanks={merged_tanks:02X} hearts+={new_hearts}")
                    if success:
                        self.items_processed = total
                        self.hearts_applied += new_hearts

            # TODO: victory detection (Sigma defeat address unknown) ->
            #   await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            # TODO: DeathLink via damage/death flag 0x800D1C1C once tested.

        except bizhawk.RequestFailedError:
            pass
