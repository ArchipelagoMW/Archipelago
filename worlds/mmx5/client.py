"""BizHawkClient for Mega Man X5 (PS1, SLUS-01334, NTSC-U).

Working core:
  * validates the game via the boot-EXE signature at 0x80010000
  * detects checks from the persistent save struct (weapons, heart tanks, intro)
  * grants received weapons and heart tanks by writing the save struct
All addresses verified in the research notes (mmx5-ram-notes.md, in
worlds/mmx5/docs/ on the author's fork: github.com/Shinnuu/Archipelago,
branch mmx5-apworld).

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
  * Armor capsules (proto v9+): the capsule stub records {stage, kind 0x20,
    id} to the ring and suppresses the vanilla part grant; the disc patch
    also makes randomized capsules (ids 0-7) always spawn, so granted armor
    parts never hide an unchecked capsule. Grants OR part bits into 0x1CA1;
    set-completion flags (0x1C4A) follow at the next results screen
    (vanilla logic). No capsule detection on vanilla discs (0x1CA1 bits
    would conflate AP grants with local pickups).
  * Victory detection: sigma goal fires on the ending mode bytes
    (0x800D1C00 walks 0x10 -> 0x11/credits after the final blow — allow the
    ~78 s cutscene gap); launch goal fires on the launch-success flag
    (0x1CCB bit 7) once all 8 parts are in hand. Both observed live.
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
OFF_ARMOR = 0x0D1CA1 - SAVE_BASE       # armor parts byte (Falcon 0-3, Gaea 4-7)
# Launch machinery (overlay-findings 11). Score = 2*sum(0x1CC2..C5) + 0x1CCA;
# on the patched disc the roll is `li v1,0`, so success <=> score > 0. The
# client PINS these every cycle from AP part-item state - vanilla accrual
# must never decide a launch. 0x1CCB bit7 = launch-success flag (victory
# marker for the launch goal). 0x1CAC u32 = collision countdown in frames.
OFF_SCORE_ACC = 0x0D1CC2 - SAVE_BASE   # 4 accumulator bytes
OFF_SCORE_MOD = 0x0D1CCA - SAVE_BASE   # additive modifier byte
OFF_LAUNCH_FLAGS = 0x0D1CCB - SAVE_BASE
OFF_COUNTDOWN = 0x0D1CAC - SAVE_BASE
# Countdown pin, in HOURS, per the boss_difficulty option. The hours remaining
# set the BOSS LEVEL BASE (mmx5-ram-notes.md "Boss Level formula"):
#   16-17 -> 1, 14-15 -> 3, 12-13 -> 5, 10-11 -> 7, 8-9 -> 9,
#    6-7  -> 11, 4-5 -> 13, 2-3 -> 15, 0-1 -> 17
# Level 4+ unlocks the Life/Energy Up choice, 8+ the Life+/Energy+ tier with an
# equippable Part. Pinning fixes only the BASE; +1 per Maverick and +1 per
# weapon still accumulate, so bosses keep scaling across a run.
#
# HISTORY: this used to be a bare `8 * 0x34BC0` attributed to "design answer
# 5". That answer only said "frozen" - it specified no value - so the 8 was an
# undocumented implementer's choice made before the boss-level formula was
# known, i.e. before anyone realised the number sets difficulty. It happens to
# land well (base 9 clears both reward thresholds); that was luck. Now explicit.
#
# Never pin at 0: the colony crash triggers on the countdown expiring.
COUNTDOWN_HOURS_BY_DIFFICULTY = {
    0: 17,   # relaxed  -> base 1
    1: 8,    # standard -> base 9   (the old hardcoded value)
    2: 1,    # intense  -> base 17
}
COUNTDOWN_HOURS_DEFAULT = 8


def countdown_frozen_value(ctx) -> int:
    """Pinned countdown in FRAMES for this seed's boss_difficulty option."""
    difficulty = (ctx.slot_data or {}).get("boss_difficulty", 1)
    hours = COUNTDOWN_HOURS_BY_DIFFICULTY.get(difficulty, COUNTDOWN_HOURS_DEFAULT)
    return hours * 0x34BC0
GOAL_SIGMA = 0
GOAL_LAUNCH = 1

# Sigma victory detection (live-captured 2026-08-01, five RAM dumps bracketing
# a real Sigma kill; see mmx5-ram-notes.md "Endgame / Zero Space").
# Endgame bosses do NOT route through the 0x0C results screen, so the patchless
# maverick kill detect (mode 0x0C + sortie id 1-8) can never see Sigma. What
# the mode byte 0x800D1C00 does after the final blow is:
#     0x0A -> 0x13 -> 0x14 -> 0x10 -> 0x11(credits)
# The X-vs-Zero duel produces 0x13 -> 0x14 as well, so those two are generic
# story-cutscene modes and are NOT usable alone. 0x10 and 0x11 appeared only
# after Sigma, and 0x11 persists through the credits. 0x0D is the death /
# game-over screen (seen oscillating during failed attempts) - deliberately
# excluded.
ENDING_MODES = frozenset({0x10, 0x11})
SIGMA_STAGE_ID = 0x0C                  # read live on entry; endgame ids are
                                       # NOT contiguous (ZS1=0x10, duel=0x12)

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

# Capsule ring records carry the SYNTHETIC kind byte 0x20 (written by the
# capsule stub only - real dispatcher kinds stop well below it). The stage
# byte identifies the location; the id (0-7) is part of the de-dupe key.
CAPSULE_KIND = 0x20
# Armor part item -> 0x1CA1 bit, taken from the game's own capsule mask table
# at 0x8007C370 (selftested in the disc builder). The table is a PERMUTATION,
# not 1<<i - it swaps body/arm within each set, so the old `1 << i` guess
# mislabelled 4 of the 8 parts on the status screen.
#
# Derivation (live capture 2026-08-01): capsule id == part index. Two ground
# truths, each a capsule whose id we read off the live object while its known
# vanilla part is documented - Tidal Whale = id 1 = Falcon Body = ARMOR_PARTS[1],
# Dark Necrobat = id 4 = Gaea Head = ARMOR_PARTS[4]. So part i is granted by
# capsule i, which ORs maskTable[i].
#
# Nibble membership (0x0F Falcon / 0xF0 Gaea) is what the results overlay
# checks for set completion, so this only affects which part the status screen
# shows - but it now matches the game instead of guessing.
ARMOR_MASK_TABLE = (0x01, 0x04, 0x02, 0x08, 0x10, 0x40, 0x20, 0x80)
ARMOR_ITEM_BITS = {name: ARMOR_MASK_TABLE[i]
                   for i, name in enumerate(names.ARMOR_PARTS)}

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
    # Registers ".apmmx5" with the BizHawk Client launcher component
    # (worlds/_bizhawk/client.py reads this attribute). WITHOUT it the
    # Launcher's Open Patch dialog does not list the extension and
    # "open with -> Archipelago Launcher" cannot route the file to a
    # handler, so the player is never prompted for their disc image -
    # reported by a tester on the v0.1.0 release.
    patch_suffix = ".apmmx5"

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
            logger.debug(f"MMX5: disc mode undetermined at boot (probe {probe.hex()}) - will re-probe in-game")

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items, own-world items, starting inventory
        ctx.want_slot_data = True
        self.items_processed = 0
        self.hearts_applied = 0
        return True

    @staticmethod
    def _classify_probe(probe: bytes):
        if probe == PATCH_PROBE_PATCHED:
            logger.debug("MMX5: disc mode = AP-PATCHED (capability byte 0x1C4D)")
            return True
        if probe == PATCH_PROBE_VANILLA:
            logger.debug("MMX5: disc mode = vanilla (hybrid grants)")
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
            logger.debug("MMX5: pickup stub RESIDENT - checks come from the mailbox ring")
            return True
        if probe == STUB_PROBE_VANILLA:
            logger.debug("MMX5: pickup stub absent - pickup checks from save-struct bits")
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
            # ---- Sigma goal: victory on the post-Sigma ending modes ----
            # Deliberately BEFORE the save-struct gate below: the ending modes
            # are neither gameplay (0x0A) nor results (0x0C), so that gate is
            # False all the way through the credits and would swallow the goal.
            # Sequence after the final blow (live-captured): 0A -> 13 -> 14 ->
            # 10 -> 11. 0x13/0x14 also fire for the X-vs-Zero duel, so only
            # 0x10/0x11 are treated as the ending.
            if not self.victory_sent \
                    and (ctx.slot_data or {}).get("goal", GOAL_SIGMA) == GOAL_SIGMA \
                    and mode[0] in ENDING_MODES:
                self.victory_sent = True
                await ctx.send_msgs([{"cmd": "StatusUpdate",
                                      "status": ClientStatus.CLIENT_GOAL}])
                logger.info(f"MMX5: ending reached (mode {mode[0]:02X}) - GOAL complete!")

            # Grants are safe whenever the save struct is live: gameplay or
            # results mode, plus a sanity floor on max HP against garbage states.
            save_sane = 0x10 <= save[OFF_MAX_HP_X] <= 0x40
            in_gameplay = mode[0] in (0x0A, 0x0C) and save_sane
            if in_gameplay != self.last_gate_state:
                logger.debug(f"MMX5: save-struct gate -> {in_gameplay} (maxhp: {save[OFF_MAX_HP_X]:02X})")
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
                    logger.debug("MMX5: save stamp OK - resuming")

            # ---- Check detection ----
            new_checks = []

            def check(location_name: str, condition: bool) -> None:
                loc_id = location_table[location_name]
                if condition and loc_id not in ctx.checked_locations:
                    new_checks.append(loc_id)

            # Save-struct reads are meaningful ONLY once a save is actually
            # resident. Before that - boot, title, training mode - the region
            # holds stale bytes from the previous session, and reading them
            # anyway fired a phantom "Intro Stage - Clear" on a tester's
            # machine while max HP still read 0x00 (the save-struct gate was
            # logging False at that very moment). An earlier comment here
            # claimed detection was "safe from any state because the save
            # struct persists"; that is true of a LOADED save, not of the
            # window before one exists. Recovery on connect is unaffected: a
            # loaded save reads sane in menus and the hub, not just in-stage.
            # The mailbox ring below is deliberately NOT gated - it lives in
            # its own free-RAM block and carries a per-record validity bit.
            def save_check(location_name: str, condition: bool) -> None:
                check(location_name, condition and save_sane)

            save_check(names.INTRO_CLEAR, save[OFF_INTRO] != 0)

            weapons_owned = save[OFF_WEAPONS]
            for bit, weapon in enumerate(WEAPON_BITS):
                stage = next(s for s, w in names.BOSS_WEAPON.items() if w == weapon)
                beaten = bool(weapons_owned & (1 << bit))
                save_check(names.boss_location(stage), beaten)
                # The DNA reward check rides the BOSS KILL, not the reward
                # prompt. Alia offers the choice only for a boss of level 4+,
                # and bosses do NOT respawn (live: entering a cleared boss room
                # just ends the stage), so keying off the prompt would make
                # this check permanently MISSABLE. Two ways that would have
                # bitten, both now moot:
                #   - a Maverick killed early, before the level-4 threshold;
                #   - EASY MODE, which locks every boss at level 1 => no
                #     Life/Energy Up prompt EVER => all 8 checks unobtainable
                #     for the whole run.
                # Keying off the kill is immune to boss level, difficulty,
                # the countdown pin, and whether the player noticed the prompt.
                # The vanilla stat gain still happens when the prompt appears -
                # it is simply no longer what we detect.
                # (Boss level formula: mmx5-ram-notes.md.)
                save_check(names.dna_location(stage), beaten)
                # Third reward from the same kill: the equippable Part granted
                # with the level-8+ Life+/Energy+ tier (DNA parts u32
                # 0x800D1C84). Also keyed on the kill rather than the Part
                # actually dropping - Parts require boss level 8+, so on
                # `relaxed` difficulty (base 1) early bosses grant none and a
                # grant-based check would be permanently missable.
                save_check(names.dna_part_location(stage), beaten)

            hearts = save[OFF_HEARTS]
            for bit in range(8):
                if hearts & (1 << bit):
                    stage = HEART_BIT_TO_STAGE.get(bit)
                    if stage is not None:
                        save_check(names.heart_location(stage), True)
                    # Unmapped bits: intentionally unsent until verified.

            # NOTE: the DNA reward locations are checked with the boss kill
            # above, NOT from the reward bits in 0x800D1C80 (Life-Up bits
            # 8-15 / Energy-Up bits 24-31, applier ~0x800EFB40). Detecting the
            # actual reward was tried and rejected: the prompt only appears
            # for a boss of level 4+ and bosses never respawn, so it would
            # make the check permanently missable. Those bits remain useful
            # for RESEARCH - Scripts/mmx5_dna_watch.lua decodes them - but the
            # client no longer depends on them, which is also what frees
            # the countdown pin from being load-bearing - it is now a plain
            # difficulty knob (see the boss_difficulty option).

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
                    # NOTE: there is deliberately NO kind-1 branch here. It
                    # used to map kind 1 / ids 0x10-0x17 to an "Energy Up"
                    # pickup location; those pickups do not exist. Across
                    # every logged session the stub has recorded only kinds
                    # 0 (heart), 6, 0xB (EX-Tank) and 0x20 (capsule) - kind 1
                    # never once fired. DNA rewards are detected from the save
                    # struct above, not from the ring.
                    elif (kind, rec_id) in TANK_RECORD_TO_STAGE:
                        loc_name = names.tank_location(TANK_RECORD_TO_STAGE[(kind, rec_id)])
                    elif kind == CAPSULE_KIND and stage is not None and rec_id <= 7:
                        # Armor capsule (proto v9 stub): one per stage.
                        loc_name = names.capsule_location(stage)

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
                            logger.debug(f"MMX5: unmapped pickup record stage={stage_id} "
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
                frozen = countdown_frozen_value(ctx)
                if countdown != frozen:
                    pin.append((SAVE_BASE + OFF_COUNTDOWN,
                                list(frozen.to_bytes(4, "little")), "MainRAM"))
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
                        # weapons/tanks/armor handled cumulatively below;
                        # TODO: filler energy once designed

                    writes = []
                    # Weapons: OR ALL received bits into the capability byte
                    # (idempotent). AP-patched disc: 0x1C4D (0x1C4C keeps
                    # recording kills - story chapters advance on its
                    # popcount). Vanilla disc: hybrid mode, write 0x1C4C.
                    wep_off = OFF_AP_WEAPONS if self.ap_patched else OFF_WEAPONS
                    capability = save[wep_off]
                    all_received_weapon_bits = 0
                    tank_bits = 0
                    armor_bits = 0
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
                        elif item_name in ARMOR_ITEM_BITS:
                            armor_bits |= ARMOR_ITEM_BITS[item_name]
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

                    # Armor parts: idempotent OR into 0x1CA1 (memcard-
                    # persisted). Individual parts do nothing in X5 until a
                    # set completes; the results overlay sets the completion
                    # flags (0x1C4A |= 2/4) at the next results screen, which
                    # unlocks the armor at character select. On the v9+ disc
                    # this can never hide an unchecked capsule: randomized
                    # capsules always spawn (spawn-gate retarget).
                    merged_armor = save[OFF_ARMOR] | armor_bits
                    if merged_armor != save[OFF_ARMOR]:
                        writes.append((SAVE_BASE + OFF_ARMOR, [merged_armor], "MainRAM"))

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
                    logger.debug(f"MMX5: grants {'applied' if success else 'guard-failed, retrying'}: "
                                f"items {processed}->{total}, "
                                f"weapons({'AP' if self.ap_patched else 'vanilla'})={merged:02X} "
                                f"tanks={merged_tanks:02X} armor={merged_armor:02X} "
                                f"hearts+={new_hearts}")
                    if success:
                        self.items_processed = total
                        self.hearts_applied += new_hearts

            # Sigma victory detection now lives at the top of this method
            # (ending modes 0x10/0x11) - it must run outside the save-struct
            # gate, which is False during the credits.
            # TODO: DeathLink via damage/death flag 0x800D1C1C - CAUTION, that
            # byte went 00 -> 01 across BOTH the X-vs-Zero duel and the Sigma
            # fight, so it is not obviously "player died"; disambiguate before
            # wiring it up.

        except bizhawk.RequestFailedError:
            pass
