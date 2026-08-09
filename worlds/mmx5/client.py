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
    also makes randomized capsules (ids 0-7) always spawn. Grants OR part
    bits into 0x1CA1; set-completion flags (0x1C4A) follow at the next
    results screen (vanilla logic). No capsule detection on vanilla discs
    (0x1CA1 bits would conflate AP grants with local pickups).
    NOTE the always-spawn patch is necessary but NOT sufficient: a capsule
    can have a SECOND gate on the route to it. Squid Adler's is opened by
    collecting energy balls, and owning the part it grants hides those balls
    - so the capsule sits there unopenable. See STAGE_CAPSULE_ARMOR_BIT.
  * Victory detection: sigma goal fires on the ending mode bytes
    (0x800D1C00 walks 0x10 -> 0x11/credits after the final blow — allow the
    ~78 s cutscene gap); launch goal fires on the launch-success flag
    (0x1CCB bit 7) once all 8 parts are in hand. Both observed live.
"""
import hashlib
import logging
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

logger = logging.getLogger("Client")

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from . import names, pickups
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
# checks and grants (wrong-save protection, A3). Written at the first
# TRUSTED sight of a fresh (progress-free) save; an unstamped save that
# already HAS progress is held instead (A3b, see game_watcher) - it is
# either another playthrough's save or offline progress, and both need the
# player to say adopting it is deliberate.
OFF_STAMP = 0x0D1C50 - SAVE_BASE
OFF_INTRO = 0x0D1C79 - SAVE_BASE
OFF_CHAR = 0x0D1C44 - SAVE_BASE         # 0 = X, 1 = Zero
# Queued-refill counters the engine drains 1 HP/tick during gameplay
# (FUN_80034140): X at 0x1C76, Zero at 0x1C77. value & 0x7F = pending amount,
# bit 7 = active. Sub-tank and pickup heals go through these, so they are the
# engine-native way to deliver received filler energy.
OFF_REFILL = 0x0D1C76 - SAVE_BASE
SMALL_ENERGY_HEAL = 4                   # matches the small HP capsule (kind 2)

# ---- Boss HP randomization -------------------------------------------------
# 0x800D1CA2 IS boss max HP - live-proven 2026-08-05: pinned to 40, the next
# boss spawned with exactly 40 (its intro fill ramp shortened 73f -> 38f to
# match). It doubles as the Boss-Level accumulator: fn 0x80024594 runs at each
# stage start and does `0x1CA2 = min(0x1CA2 + level_raw, 0x7F)`, which is how
# bosses gain HP over a run.
#
# THAT ACCUMULATION IS WHY WE RESTORE. Overwriting the byte makes OUR value the
# base for the next stage's accumulate, so the multiplier compounds and pins to
# the 0x7F ceiling within a few stages. Instead: write the rolled value on
# gameplay entry, put the vanilla value back on exit, and the game's own
# arithmetic stays exactly vanilla.
#
# One global byte means bosses met during the SAME stage visit (mid-boss and
# stage boss) share that visit's roll. Inherent to the lever, documented in the
# option text.
OFF_BOSS_HP = 0x0D1CA2 - SAVE_BASE
# LOW BOUND IS 0x20, NOT 1 - corrected 2026-08-09 from a tester's corrupt
# lifebars. 0x1CA2 does not only scale HP, it drives the bar GRAPHIC, and the
# two consumers that read it are clamped above and not below:
#
#   0x800259E0  sprite = 0xA3 + (v - 0x20)/2, clamped above at 0xD3
#               (sprites 0xA3..0xD3 cover 32..128 HP, one per 2 HP)
#   0x8002617C  screen coord += (v - 0x20) rounded down to even
#
# Below v = 0x20 the subtraction goes negative: the sprite index runs
# backwards out of the bar artwork and the bar's anchor shifts the wrong way.
# A tester's Izzy Glow rolled 25 and drew a broken bar. The 0x7F ceiling is
# separately load-bearing - `lb` is a SIGNED load, so v >= 0x80 reads
# negative and is far worse.
#
# The floor is applied as min(BOSS_HP_MIN, vanilla), NEVER as a bare
# max(0x20, rolled): 0x1CA2 accumulates from 0, so an early-run vanilla of 16
# under `weak` rolls 6-13, and a bare floor would clamp that UP to 32 - a 2x
# boss buff from the option named "weak". See _boss_hp_roll.
BOSS_HP_MIN, BOSS_HP_MAX = 0x20, 0x7F
# option value -> (low, high) multiplier applied to the game's own value
BOSS_HP_BANDS = {
    1: (0.40, 0.80),    # weak
    2: (0.70, 1.30),    # regular
    3: (1.20, 2.00),    # strong
    4: (0.25, 2.50),    # chaotic
}
# ---- Stage unlocks -------------------------------------------------------
# The hub overlay turns a stage-select cursor slot into a stage id through an
# 8-byte table, then refuses to act on a zero:
#
#   800EFC88  addiu $v0, $v0, 0x5050    ; $v0 = 0x800F5050
#   800EFC90  lbu   $v1, 0x0($v0)       ; stageId = SLOT_TO_STAGE[cursor]
#   800EFC98  sb    $v1, 0xc($s0)       ; 0x800D1C0C = stage id
#   800EFCA4  beqz  $v0, 800EFD40       ; *** id 0 -> do nothing ***
#
# That `beqz` is the whole feature. Zero a slot and confirming its icon is a
# silent no-op; write the real id back and it works again. An exhaustive
# immediate scan of the hub module found this handler to be the table's ONLY
# reader, so zeroing a slot changes nothing else on screen. Details, including
# the slot -> boss layout, in mmx5-ghidra-findings.md §9.14 (research notes,
# fork branch mmx5-apworld - not present on the upstream PR branch).
SLOT_TABLE_ADDR = 0x0F5050
# slot order is the screen's: four icons down the left column, four down the
# right. Slot 8 (the Enigma / Shuttle / Zero Space / Sigma entry) does NOT go
# through this table - it resolves from chapter and ACT - and stays vanilla.
SLOT_TO_STAGE = (1, 5, 6, 3, 8, 7, 2, 4)
# Anchor word proving the hub overlay is the resident module before we write
# into its data: `addiu $v0, $v0, 0x5050` at 0x800EFC88. Every other overlay
# maps different code there, and the table is reloaded from disc on each hub
# entry, so the client must re-assert the lock every time rather than once.
SLOT_TABLE_ANCHOR_ADDR = 0x0EFC88
SLOT_TABLE_ANCHOR = bytes.fromhex("50504224")   # 0x24425050 LE
# 0x800EFC98 stores the id BEFORE the zero test, so a blocked confirm leaves
# 0x800D1C0C reading 0 while the player sits in the hub - a value vanilla never
# writes there, and one that would be committed to the memory card by an
# in-hub save. The client puts the hub's own id back; HUB_STAGE_ID is only the
# fallback for "we have not seen a real one yet" (0x0D in every hub capture).
HUB_STAGE_ID = 0x0D

# Story ACT value Training mode stamps into the save struct (live-captured
# 2026-08-03). The campaign uses a small range - 1 at intro victory, 5 at
# Eurasia, 2 read off a real mid-game save - so 0x0A is out of band and
# identifies the training pseudo-save. See the `training` check below.
TRAINING_ACT = 0x0A
# ACT value the colony resolution writes, and the real ENDGAME GATE: with ACT
# >= this, stage select offers Zero Space; below it, Zero Space is absent.
# Live-verified 2026-08-04 - poking ACT from 5 down to 2 made Zero Space
# disappear from a save that had it. Corroborated by the results tail, which
# tests 0x800D1C79 < 5 for its bonus lines.
#
# This is what actually controls endgame access. The story-chapter ladder does
# NOT: the Enigma/Shuttle menu entries are always present, the shuttle simply
# appears once the Enigma has been used, and a player at 6 kills reached Zero
# Space on a disc whose shuttle-era threshold had been moved to 8. Moving that
# threshold only delays the story ANNOUNCEMENT (and Dynamo).
ENDGAME_ACT = 5
# ACT doubles as the endgame progress counter. The hub's stage-select confirm
# handler picks the Zero Space destination straight off it (0x800EFC0C):
# 5 -> 0x10, 6 -> 0x11, 7 -> 0x12, anything else -> 0x0C (Sigma). So the value
# only advances by clearing the stage it currently points at, and the ACT a
# clear produces is the threshold for that clear's check.
#
# CONFIRMED LIVE 2026-08-06: clearing Zero Space 1 stepped ACT 5 -> 6 on the
# frame the stage ended (`[f323080] savestruct 800D1C79: 05 -> 06`). The ladder
# reads as progress, not just as a destination lookup.
ENDGAME_CLEAR_ACT = {
    names.ZERO_SPACE_1: 6,
    names.ZERO_SPACE_2: 7,
    names.ZERO_SPACE_X_VS_ZERO: 8,
}
# ---- DNA Parts -----------------------------------------------------------
# u32 bitfield, Parts in bits 2..17. Bit numbers read off the game's own Parts
# screen with every bit forced on (2026-08-06); provenance and the full table
# in mmx5-ghidra-findings.md §9.15 (fork branch). Corroborating pattern: 11-16 are
# exactly the six character-locked Parts, X's three then Zero's three.
OFF_PARTS = 0x0D1C84 - SAVE_BASE        # u32
PART_TO_BIT = {
    names.SPEEDSTER: 2, names.JUMPER: 3, names.HYPER_DASH: 4,
    names.W_ENERGY_SAVER: 5, names.SUPER_RECOVER: 6,
    names.ANTI_VIRUS_GUARD: 7, names.BUSTER_PLUS: 8, names.SPEED_SHOT: 9,
    names.VIRUS_BUSTER: 10, names.BURST_SHOTS: 11, names.ULTIMATE_BUSTER: 12,
    names.QUICK_CHARGE: 13, names.Z_SABER_PLUS: 14, names.Z_SABER_EXTEND: 15,
    names.SHOT_ERASER: 16, names.SHOCK_BUFFER: 17,
}
PARTS_MASK = 0x0003FFFC                 # bits 2..17
OFF_TANKS = 0x0D1C7F - SAVE_BASE
OFF_HEARTS = 0x0D1C80 - SAVE_BASE
OFF_ARMOR = 0x0D1CA1 - SAVE_BASE       # armor parts byte (Falcon 0-3, Gaea 4-7)
# Armor SET-COMPLETION flags: bit1 Falcon complete, bit2 Gaea complete.
# Capability comes from a complete set, so this - not the parts byte -
# is what must survive while a part is withheld.
OFF_SETFLAGS = 0x0D1C4A - SAVE_BASE
# Secret armors from the Zero Space capsule (id 8). Its grant code, disasm'd
# 2026-08-01 (overlay-findings 2.x): char 0 (X) -> 0x800D1C4B = 1 (Ultimate),
# otherwise 0x800D1C4A |= 0x10 (Black Zero). Both memcard-persisted, and the
# stage-load character init mirrors 0x1C4B into the live player struct
# (`lbu 0x4B(ctrl); sb 0x14A(player)`), so a grant applies at the next stage
# load exactly like the weapons byte.
#
# Both armors LIVE-CONFIRMED 2026-08-06, and they apply on DIFFERENT schedules:
#   * Ultimate (0x1C4B) needs a stage load. X wore it on the entry AFTER the
#     grant landed, not the stage he was standing in - exactly what the mirror
#     above predicts, since the copy into the player struct happens once at
#     character init.
#   * Black Zero (0x1C4A bit 4) applied IMMEDIATELY - Zero turned black with no
#     further stage entry. No mirror instruction was ever found for this bit,
#     so its consumer evidently reads the save byte live. [INFER on mechanism;
#     the timing itself is observed.]
# Also settled: writing ONLY 0x1C4B is enough for Ultimate. The capsule's
# despawn ladder reads `0x1C4A & 8`, but that is not a second ownership flag.
#
# 0x1C4B IS NOT A BOOLEAN, though. Observed live 2026-08-06: the game moved
# it 01 -> 02 at a results screen, and Ultimate remained selectable at the
# armor picker afterwards. So 1 grants it, but 1 is not the only value that
# means "owned" - possibly a selection index. The grant below therefore
# writes only when the byte is ZERO, which is the one value we know means
# "no Ultimate". Never restore it to 1 from some other non-zero value.
OFF_ULTIMATE = 0x0D1C4B - SAVE_BASE
ULTIMATE_ON = 1
BLACK_ZERO_BIT = 0x10           # into 0x1C4A (OFF_SETFLAGS)
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
# Defeat all 8 Mavericks, THEN Sigma. Distinct from GOAL_SIGMA because vanilla
# does not require the full set: the endgame opens when the colony situation
# resolves, and the story ladder (fn 0x800EEF14, popcount of 0x800D1C4C) hands
# out the Enigma at 2 kills and the shuttle at 6 - so a double failure at 6
# kills opens Zero Space two Mavericks early. AP-granted weapons land in
# 0x1C4D, not 0x1C4C, so received items never advance that ladder; only real
# kills do. See overlay-findings 10.
GOAL_ALL_MAVERICKS = 2

# launch_odds option. `vanilla` puts the game's own roll back (the disc keeps
# its vanilla `andi` at 0x800FA0D4) and the client writes a SCORE in the band
# matching the parts held, rather than the flat 0/1 that deterministic odds
# use. Bands come from the resolution ladder at 0x800FA0D8 (see Rom.py):
#   0x01-0x14 -> 6.25%   0x15-0x28 -> 12.5%
#   0x29-0x3C -> 37.5%   0x3D-0x50 -> 75%
# One representative value per band; the exact number inside a band does not
# matter, only which band it lands in.
LAUNCH_ODDS_VANILLA = 1
LAUNCH_SCORE_6 = 0x0A     # 6.25%
LAUNCH_SCORE_12 = 0x20    # 12.5%
LAUNCH_SCORE_37 = 0x30    # 37.5%
LAUNCH_SCORE_75 = 0x45    # 75%
# Goals that end on the post-Sigma ending modes rather than the launch flag.
ENDING_GOALS = frozenset({GOAL_SIGMA, GOAL_ALL_MAVERICKS})

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

# ---- Boss Rush rematch checks (live session 2026-08-08) --------------------
# A rush rematch runs in the standard boss-HP slot: the bar fills, steps to 0
# on the kill, and the 0 PERSISTS 600+ frames, so polling cannot miss it.
# WHICH boss is fighting comes from the boss module the portal streamed to
# RAM 0x800FA000 (ROCK chunk 29+stage_id): 16 bytes at +0x300 are
# pairwise-distinct across the 8 modules. Sixteen bytes and not a word,
# because a single word there can be a common instruction (`lw $s0,0x10($sp)`)
# and collide with whatever module Sigma's own fights load; the Sigma-fight
# dumps match none of the 8 at 16 bytes. Three fingerprints are live-verified
# (Squid mid-fight; Izzy and Dark Dizzy resident in corridor dumps), five are
# chunk-derived - which is safe because an unknown fingerprint sends NOTHING.
#
# The module PERSISTS after a fight until the next portal replaces it, so a
# matching fingerprint means "most recently loaded", never "in progress".
# Liveness comes from stage+mode+the HP fill, and the kill send additionally
# requires the player alive: after a mid-fight player death the module is
# still resident, and however the engine treats the boss-HP byte across the
# respawn, a zero there must not read as a kill.
#
# The sub-stage byte 0x1C1D is deliberately NOT used: the same Squid rematch
# read 0x05 and 0x06 in different sessions (route-dependent room counter).
# Full derivation: mmx5-ram-notes.md §Boss fights (fork branch).
RUSH_BOSS_HP_ADDR = 0x0920EC
RUSH_FP_ADDR = 0x0FA300
# 256 BYTES, NOT 16 - corrected 2026-08-09 after a tester received rematch
# checks for bosses he never fought (Squid Adler and The Skiver).
#
# The probe ADDRESS was never wrong; the LENGTH was. A 16-byte window at a
# fixed offset is a sample, not an identity, and the old table's own values
# prove it - counted across the whole disc:
#
#   The Skiver   40 occurrences (12 of them in the base EXE, so it is
#                resident in EVERY state including the title screen). Its
#                bytes are `lw $s0,0x10($sp)` / `jr $ra` / `addiu $sp,0x28` /
#                `addiu $sp,-0x20` - a function epilogue followed by the next
#                prologue, i.e. ordinary compiler boilerplate.
#   Squid Adler  11 occurrences, TWO of them inside the Sigma-area module at
#                0x800FA350 and 0x800FA2E0 - the same routine linked 0x50
#                above and 0x20 below this probe, so a different route
#                through that stage lands it exactly on the probe.
#   Izzy Glow     1 occurrence - the only one of the eight that was ever an
#                identity, and the only one that never misfired.
#
# "Pairwise-distinct across the 8 boss modules" was true and irrelevant: the
# competing values are not the other seven modules, they are everything else
# that can be resident at 0x800FA000.
#
# At 256 bytes all eight are unique across the entire disc, zero duplicates
# (unique from 128 already; 256 is margin). Derivation and the full count
# table: ai-docs/plans/2026-08-09_mmx5-tester-bug-triage.md 2a, ram-notes
# section Boss rush. test_rematch_checks.py re-derives this table from the
# disc when one is available and skips when it is not.
RUSH_FP_LEN = 256
# sha256 of the 256 bytes, rather than the bytes themselves: 8 x 512 hex
# characters of boilerplate in the source would be unreadable and unreviewable.
# A torn read of a mid-stream module hashes to nothing in this table, which is
# the safe direction - an unknown module sends NOTHING.
RUSH_FP_TO_STAGE = {
    "07213d14ef50d9015a6765bafb8db0e74207d17ca0ffa6f5781fbbdeb1c613fb":
        names.GRIZZLY,          # ROCK chunk 30, head 060020a1180023ad...
    "8cc2552329764e86ddfd25a7206516b8a839845ea2796f1859647aa70cff2a66":
        names.NECROBAT,         # ROCK chunk 31, head 540002ae0780023c...
    "20f34a69a417bf6a8e39c901f28aaff8edbd260dedd00dbc16efc63860811b8c":
        names.WHALE,            # ROCK chunk 32, head 5e0102240d006214...
    "51e9a73507986e4ae4a139e7aa98b1eb4fd8e69c2bb814391c15e0d029223753":
        names.DINOREX,          # ROCK chunk 33, head 801f053c3000a58c...
    "18b43b831fc1ec46a4222803e867a346180d29e5d96ebf87fd8ac41581e945ed":
        names.KRAKEN,           # ROCK chunk 34, head 0100032402000424...
    "a62d57fc6199e45ac975e8232fa4c340783de559d8d117029406f65ef47cff7b":
        names.FIREFLY,          # ROCK chunk 35, head b8fcc3a404000292...
    "9bb05e09c42291fa06252979b88cea0054968d8dd006f91695bef92dc8670aea":
        names.ROSERED,          # ROCK chunk 36, head 0780023c05000324...
    "7996f8efc130ef48254bd51771bb9b101e132185d6037be8eca7982924550400":
        names.PEGASUS,          # ROCK chunk 37, head 1000b08f0800e003...
}
# Real fights fill to 40+ (Squid 58, Axle 53). The old value of 8 was set
# from "corridor blips reach 6" while ram-notes simultaneously recorded
# "leftover 16 observed at stage entry" - the threshold sat BELOW a
# documented stale value.
RUSH_MIN_PEAK = 24
PLAYER_HP_ADDR = 0x09A0FC       # live player HP; bit7 = just-damaged flag

# ---- Reploid rescue checks (live session 2026-08-08) -----------------------
# A rescue's only footprint is lives (0x0D1C45) += 1, clamped to 9 - no
# persistent record exists (disproven 2026-07-31), so the AP server IS the
# record and detection is live: when lives rise during trusted gameplay in a
# Reploid stage, the player is standing ON the Reploid (rescue requires
# overlap), so the nearest Reploid record to the player names the check.
# Live rescues overlapped their record within ~25px; the radius is generous
# because the CLIENT polls sparsely and the player walks after rescuing.
# Position is also the guard against the other things that raise lives:
# a 1-UP pickup away from any record matches nothing and sends nothing.
# (Izzy and Squid area 0 have no freestanding consumables at all.)
#
# Misses are recoverable: Reploids respawn on every stage re-entry. The one
# blind spot is a rescue AT the 9-life cap (no increment to see) - documented
# in the option text; re-entering under 9 lives redoes it.
# (REPLOID_RECORDS_BY_STAGE is built below STAGE_ID_BY_NAME.)
REPLOID_MATCH_RADIUS = 0x180
OFF_LIVES = 0x0D1C45 - SAVE_BASE
PLAYER_XY_ADDR = 0x09A0AA       # player struct +0x0A: x s16, +0x0E: y s16

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
# Tank already-owned despawn fix (disc rev 12+). The item init at
# 0x800535C8 destroys a pickup you already own; the patch zeroes the sub-tank
# mask word so the test can never fire for tanks. Probing it tells a fixed
# disc from an older one, so the client's own workaround below runs ONLY
# where it is actually needed.
TANK_FIX_PROBE_ADDR = 0x053804
TANK_FIX_VANILLA = bytes.fromhex("00100224")   # addiu v0,zero,0x1000
TANK_FIX_PATCHED = bytes.fromhex("00000224")   # addiu v0,zero,0

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

# Pickupsanity ring (per-seed stub, option-gated): 32 slots of
# {stage u8, kind u8, id u8, seq u8, record_ptr u32} at 0x801FA100, count
# u32 at 0x801FA200. The record pointer is the placement-record address the
# spawner stored at itemObj+0x10 - the only unique identity consumables have
# (their id byte is a TYPE and collides). Resolved via
# pickups.RECORD_TO_LOCATION; list bases are static EXE data so the
# addresses are stable across discs and sessions.
RING2_ADDR = 0x1FA100
RING2_SLOTS = 32
RING2_COUNT_ADDR = 0x1FA200
# Stub-presence probe. Two words, because ONE is not enough any more:
#
#   RING2_STUB_PROBE_ADDR - the stub's own first instruction, in EXE free
#     space. This is the authority. The client never writes here, so it stays
#     true no matter what the dispatch table currently says.
#   RING2_PROBE_ADDR - the kind-2 (small HP) dispatch entry, kept only to tell
#     a real vanilla disc (EXE loaded, table holds the vanilla handler) from
#     boot (everything reads zero).
#
# The dispatch entry ALONE used to be the probe, and that stopped being safe
# the moment _pickup_dispatch_apply started rewriting it: hand a cleared stage
# its vanilla capsules back, walk out, and the gate-transition re-probe would
# read "vanilla" and turn pickupsanity check detection off for the rest of the
# session. Presence of the stub is a property of the DISC; what the table
# points at right now is a property of where the player is standing.
RING2_PROBE_ADDR = 0x011070
RING2_PROBE_VANILLA = bytes.fromhex("64410580")   # 0x80054164 LE
RING2_PROBE_STUBBED = bytes.fromhex("60770780")   # 0x80077760 LE
RING2_STUB_PROBE_ADDR = 0x077760                  # PICKUPSANITY_STUB_ADDR
# The stub's first instruction, used to prove a disc carries the pickupsanity
# stub at all. BOTH generations are accepted on purpose: the v2 stub (0.5.0)
# starts by loading the placement-record pointer so it can tell an enemy drop
# from a placed pickup, while v1 (<= 0.4.2) started by building the ring base.
# Recognising only the current one would make every disc patched before 0.5.0
# read as "not stubbed" and silently turn pickupsanity check detection OFF
# mid-run - a far worse failure than not having the enemy-drop fix.
RING2_STUB_WORD = bytes.fromhex("10002f8e")       # v2: lw $t7, 0x10($s1)
RING2_STUB_WORD_V1 = bytes.fromhex("1f80083c")    # v1: lui $t0, 0x801F
RING2_STUB_WORDS = (RING2_STUB_WORD, RING2_STUB_WORD_V1)

# The whole collect dispatch table, so the client can hand a cleared stage its
# vanilla capsules back (_pickup_dispatch_apply). Kinds and stub address match
# disc.py's CONSUMABLE_KINDS / PICKUPSANITY_STUB_ADDR - the same table it
# patches at build time; these are the runtime override of those same words.
# Vanilla handler addresses read out of the unmodified SLUS_013.34 (2026-08-08);
# kinds 5/6/7 genuinely share one handler.
DISPATCH_TABLE_ADDR = 0x011068
CONSUMABLE_KINDS = (0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8)
PICKUPSANITY_STUB_ADDR = 0x80077760
VANILLA_DISPATCH = {
    0x2: 0x80054164,   # small HP
    0x3: 0x80054198,   # large HP
    0x4: 0x800541D8,   # full HP
    0x5: 0x80054204,   # small weapon
    0x6: 0x80054204,   # large weapon  (same handler)
    0x7: 0x80054204,   # full weapon   (same handler)
    0x8: 0x80054218,   # 1-UP
}

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

# Which tank bit each tank LOCATION's vanilla pickup sets. Used by the
# unpatched-disc workaround: while standing in a stage whose tank location is
# still unchecked, that bit must be clear or the game deletes the pickup.
STAGE_TANK_BIT = {
    names.GRIZZLY: 0x10,    # Sub-Tank #1
    names.NECROBAT: 0x20,   # Sub-Tank #2
    names.PEGASUS: 0x40,    # W-Tank
    names.FIREFLY: 0x80,    # EX-Tank
}
STAGE_ID_BY_NAME = {name: sid for sid, name in STAGE_ID_TO_NAME.items()}

# stage id -> [(x, y, location name)] for the Reploid watcher (see the
# constants block above for the detection rationale).
from .reploids import REPLOIDS as _REPLOIDS  # noqa: E402
REPLOID_RECORDS_BY_STAGE: dict[int, list[tuple[int, int, str]]] = {}
for _stage, _idx, _x, _y, _name in _REPLOIDS:
    REPLOID_RECORDS_BY_STAGE.setdefault(
        STAGE_ID_BY_NAME[_stage], []).append((_x, _y, _name))

# Armor part each stage's CAPSULE grants, as an 0x1CA1 mask. Owning the part
# can suppress the vanilla mechanism that opens its own capsule - live-proven
# 2026-08-03 in Squid Adler: with 0x1CA1 = 00 the jet-bike energy balls that
# gate that capsule are present and collectable; granting Falcon Head (0x01)
# and re-entering makes them vanish. Same family as the tank despawn - an
# AP-granted item hiding the route to its own check - but a SECOND gate on a
# location whose capsule object the v9 spawn-gate patch already forces to
# spawn. The capsule sits there; the thing that opens it does not.
#
# Only Squid Adler is listed because only Squid Adler is proven. The stage ->
# capsule-part map is verified for four stages (Squid Adler = Falcon Head 0x01,
# Duff McWhalen = Falcon Body, Grizzly = Falcon Leg, Dark Dizzy = Gaea Head)
# and unverified for the rest, and a wrong entry here would withhold armor a
# player needs to REACH a capsule - worse than the bug. Add entries only with
# the same kind of live evidence.
STAGE_CAPSULE_ARMOR_BIT = {
    names.KRAKEN: 0x01,     # Squid Adler -> Falcon Armor Head
}

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

# Live (volatile) weapons-owned bitfield, zeroed on death and stage exit and
# repopulated at stage load. Writing the SAVE byte alone is why a weapon used
# to sit unusable until the player left and re-entered the stage (reported by
# a tester 2026-08-08): the save byte is what a stage load reads, not what the
# pause menu reads mid-stage.
#
# The restore is `0x8003C324`: `lbu $v0, 0x4C($a1)` / `sb $v0, 0xC9($s0)` with
# $s0 = the player struct 0x8009A0A0, so $s0+0xC9 IS this address. That store
# is one of the three the AP disc patch retargets 0x4C -> 0x4D, which is why a
# patched disc restores from the AP capability byte rather than the kill
# record. Verified statically 2026-08-08 (ghidra-findings 9.16).
#
# Only ever OR-ed, and only during gameplay: X5 never takes a weapon away, and
# the 0x9Axxx region is garbage outside gameplay.
LIVE_WEAPONS_ADDR = 0x09A169

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
        # None = unknown. validate_rom classifies before the watcher ever
        # runs; False specifically means "probe read the exact vanilla word",
        # and the victory hold below keys on that distinction - a fresh
        # client must not read as "known vanilla".
        self.ap_patched = None
        self.stub_present = False
        self.ring2_present = False
        self.unknown_records_logged = set()
        # Last (vanilla?, stage) the collect dispatch table was set for. None
        # means "unknown", so the first cycle always writes - a savestate or a
        # reload can put the disc's own (stubbed) words back under us.
        self.pickup_dispatch_vanilla = None
        # Boss HP: the vanilla accumulator value the game last computed, and
        # what we last wrote over it. Both in-memory only - see _boss_hp_apply.
        self.boss_hp_vanilla = None
        self.boss_hp_written = None
        self.boss_hp_stage = None
        self.boss_hp_logged = set()
        self.stamp_warned = False
        self.unpatched_warned = False
        self.last_probe_word = None
        # Save-derived checks are believed only while in gameplay AND only
        # once the check-driving bytes repeat across two polls. See the
        # save_trusted block for why save_sane alone is not enough.
        self.last_check_sig = None
        self.last_trust_state = None
        # Whether the PREVIOUS poll's gate was open. Trust requires two
        # consecutive gameplay polls: the stability signature is also
        # recorded on menu polls, and stale RAM never changes, so without
        # this a single poll landing in a gameplay mode (e.g. the 0x0C that
        # appears mid stage-load) would be trusted instantly off a signature
        # the title screen established.
        self.last_in_gameplay = False
        # Set once a 0x0A poll has been trusted this session. 0x0C is only
        # believed AFTER that: results screens always follow real gameplay,
        # but 0x0C also appears in the stage-LOAD mode walk
        # (0A->0B->0C->0E->..., ram-notes), where the struct may still hold
        # the previous session's bytes.
        self.gameplay_anchored = False
        self.unstamped_warned = False
        self.victory_sent = False
        # Boss Rush rematch tracking: which boss the resident module names
        # (None outside the rush / unknown module), and the highest boss HP
        # seen for that boss while the fight conditions held. Peak >=
        # RUSH_MIN_PEAK is what separates a real fight's kill from the
        # corridor's stale-byte blips.
        self.rush_boss = None
        self.rush_peak = 0
        # Arming state, added 2026-08-09. A resident module means "most
        # recently loaded", never "in progress", so identity alone must not
        # arm a kill. Within one arming (one observed module load) we need to
        # SEE the intro fill happen - the bar ramps +1/frame from 1 to max -
        # before a zero may be read as a kill, and we send at most once.
        # This rejects the two no-fight paths the corridor dumps sit in:
        # a stale byte >= the threshold that later drops to 0, and a module
        # resident with the byte already 0.
        self.rush_prev_hp = None
        self.rush_saw_low = False
        self.rush_saw_fill = False
        self.rush_sent = False
        # Reploid watcher: (stage id, lives) from the last poll that was
        # trusted gameplay in a Reploid stage - None anywhere else, so a
        # menu, savestate load or stage change can never fake an increment.
        self.reploid_lives = None
        # Highest Maverick kill count seen while the save read SANE. The
        # all_mavericks goal needs this at the ENDING, where the save-struct
        # gate is False (see the victory block) - so it cannot be read then.
        # Tracked during play instead, and deliberately never sourced from an
        # ungated read: a stale 0xFF would score 8 and hand out a false goal,
        # which is exactly how the phantom intro check happened in 0.1.1.
        self.mavericks_defeated = 0
        self.short_ending_warned = False
        # Endgame withholding (all_mavericks). Remember the last legitimate
        # pre-endgame ACT so it can be restored exactly, rather than guessing a
        # value the story never had.
        self.last_pre_endgame_act = None
        self.act_withheld = False
        self.act_withheld_warned = False
        self.last_training_state = None
        self.tank_fix_present = None    # None = not yet probed
        self.tank_workaround_warned = False
        self.unpowered_launch_warned = False
        self.armor_workaround_warned = False
        self.armor_setflags_pin = None
        self.tanks_withheld = 0         # bits held back this stage visit
        # Stage unlocks: last slot table we wrote, the set of stages we have
        # announced as unlocked, and the last real hub stage id seen.
        self.slot_table_written = None
        self.stages_unlocked_logged = set()
        self.hub_stage_id = None
        # Highest story ACT seen while the save read SANE. A high-water mark
        # rather than a live read, for two reasons: the all_mavericks goal
        # WRITES this byte (it holds the endgame shut by pushing ACT back below
        # 5), and training mode parks 0x0A in it. The withhold only ever lowers
        # ACT, so a peak is immune to it; training is excluded explicitly.
        self.max_act_seen = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            sig, probe, stub_probe, tank_probe = await bizhawk.read(ctx.bizhawk_ctx, [
                (EXE_SIG_ADDR, len(EXE_SIG), "MainRAM"),
                (PATCH_PROBE_ADDR, 4, "MainRAM"),
                (STUB_PROBE_ADDR, 4, "MainRAM"),
                (TANK_FIX_PROBE_ADDR, 4, "MainRAM"),
            ])
            if sig != EXE_SIG:
                return False
        except bizhawk.RequestFailedError:
            return False

        # False = known vanilla; the watcher REFUSES to run on it (hybrid
        # mode is gone - see the unpatched-disc block in game_watcher).
        # None = undetermined (validate can race the EXE still streaming in
        # from disc - the probe reads zeros during boot); game_watcher
        # re-probes before granting anything.
        self.ap_patched = self._classify_probe(probe)
        self.last_probe_word = bytes(probe)
        self.stub_present = self._classify_stub_probe(stub_probe)
        self.tank_fix_present = self._classify_tank_fix(tank_probe)
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
    def _classify_tank_fix(probe: bytes):
        if probe == TANK_FIX_PATCHED:
            return True
        if probe == TANK_FIX_VANILLA:
            return False
        return None      # boot race: EXE not resident yet, re-probe later

    def _tank_bit_to_withhold(self, ctx, stage_name: str) -> int:
        """Tank bit that must stay CLEAR to keep this stage's pickup alive.

        Only meaningful on a disc without the tank fix. Returns 0 once the
        location is checked - at that point the pickup no longer matters and
        the player should have their tank.
        """
        bit = STAGE_TANK_BIT.get(stage_name, 0)
        if not bit:
            return 0
        loc = location_table.get(names.tank_location(stage_name))
        if loc is None or loc in ctx.checked_locations:
            return 0
        return bit

    def _armor_bit_to_withhold(self, ctx, stage_name: str) -> int:
        """Armor bit that must stay CLEAR to keep this stage's capsule openable.

        Returns 0 once the capsule location is checked - after that the route
        no longer matters and the player should have their armor back.
        """
        bit = STAGE_CAPSULE_ARMOR_BIT.get(stage_name, 0)
        if not bit:
            return 0
        loc = location_table.get(names.capsule_location(stage_name))
        if loc is None or loc in ctx.checked_locations:
            return 0
        return bit

    def _boss_hp_roll(self, ctx, stage_id: int, vanilla: int) -> int:
        """Rolled boss HP for this stage visit. Deterministic per
        (seed, slot, stage, vanilla) so a retry is the same fight."""
        band = BOSS_HP_BANDS.get(
            (ctx.slot_data or {}).get("boss_hp_randomization", 0))
        if band is None:
            return vanilla
        if vanilla <= 0:
            # Callers must not reach here (see the current == 0 guard), but a
            # 0 would mean an instant-death boss, so refuse it outright.
            return vanilla
        seed = f"{ctx.seed_name}:{ctx.slot}:{stage_id}:{vanilla}"
        # Stable across sessions and machines - hash() is salted per process.
        digest = hashlib.sha256(seed.encode("utf-8")).digest()
        frac = int.from_bytes(digest[:4], "big") / 0xFFFFFFFF
        lo, hi = band
        rolled = round(vanilla * (lo + frac * (hi - lo)))
        # The floor is min(BOSS_HP_MIN, vanilla), not BOSS_HP_MIN: it must
        # never RAISE a boss above what vanilla would have given, or `weak`
        # becomes a buff wherever vanilla already sits under 0x20 (which it
        # does early in a run - the accumulator starts at 0). Where vanilla is
        # already below the artwork's domain we simply do not make it worse.
        return max(min(BOSS_HP_MIN, vanilla), min(BOSS_HP_MAX, rolled))

    async def _boss_hp_apply(self, ctx, save: bytes, in_gameplay: bool,
                             stage_id: int) -> None:
        """Hold rolled boss HP during gameplay; restore vanilla on the way out.

        The restore is not cosmetic: 0x1CA2 accumulates at each stage start, so
        leaving our value in place would compound the multiplier every stage.
        """
        if not (ctx.slot_data or {}).get("boss_hp_randomization", 0):
            return
        # STAGE 0x0C IS EXCLUDED (2026-08-09). 0x1CA2 scales the lifebar for
        # EVERY boss but sets HP for only SOME. Measured: Axle 53 -> fills 53
        # and Sigma 80 -> fills 80 (both driven by it), but the Squid rematch
        # reads 0x1CA2 = 127 and fills to 58 - rush rematches take their HP
        # somewhere else. Randomizing the byte there therefore does not change
        # the fight at all, it only desynchronizes the bar from the boss's
        # real HP, at ANY roll value - the 0x20 floor does not help. A tester
        # saw exactly that on three rematches ("the Max is low but the HP they
        # get is higher than the max").
        #
        # Cost of this exclusion, accepted deliberately: Sigma himself IS
        # 0x1CA2-driven and lives in this stage, so he stops being
        # randomized. Eight visibly broken rematch bars is the worse trade.
        # Treating the stage as "not gameplay" reuses the restore path below,
        # so entering it hands the game its own number back.
        if stage_id == SIGMA_STAGE_ID:
            in_gameplay = False
        current = save[OFF_BOSS_HP]
        # 0 is never a real baseline. The stage id (0x800D1C0C) changes during
        # the stage load, but the Boss Level function has not necessarily
        # recomputed 0x1CA2 yet, so sampling here can catch a zeroed byte.
        # Adopting that would (a) roll 0 -> 0, and 0 IS the kill-boss value,
        # and (b) make the restore-on-exit write 0 over a legitimate number and
        # poison the game's own accumulator. Wait for a real value instead.
        # Seen live 2026-08-05: "boss HP stage 1: 0 -> 0".
        if current == 0:
            return
        if in_gameplay:
            # Adopt a vanilla baseline ONLY on a stage transition, because the
            # game only recomputes 0x1CA2 at stage start.
            #
            # The obvious "anything I did not write is vanilla" rule is WRONG
            # here: savestates restore 0x1CA2 along with the rest of RAM, so
            # loading a state taken earlier in the same stage hands us a stale
            # value that is not a fresh recompute. Trusting it would reroll
            # from the wrong base, and - worse - that wrong number is what gets
            # restored on the way out, corrupting the game's own accumulator.
            # Keying on the stage id means state loads inside a stage simply
            # get our rolled value re-applied, which is what a player expects.
            if self.boss_hp_stage != stage_id:
                self.boss_hp_stage = stage_id
                self.boss_hp_vanilla = current
                self.boss_hp_written = None
            if self.boss_hp_vanilla is None:
                return
            rolled = self._boss_hp_roll(ctx, stage_id, self.boss_hp_vanilla)
            if current != rolled:
                await bizhawk.write(ctx.bizhawk_ctx,
                                    [(SAVE_BASE + OFF_BOSS_HP, [rolled], "MainRAM")])
                self.boss_hp_written = rolled
            else:
                # Roll landed on the value already there. Remember it as ours
                # so the restore path still hands the game back its own number.
                self.boss_hp_written = rolled
            # Log the DECISION, not just writes: a roll that happens to equal
            # the baseline produces no write, and logging only on writes made
            # a correctly-working feature look inert during testing.
            key = (stage_id, self.boss_hp_vanilla, rolled)
            if key not in self.boss_hp_logged:
                self.boss_hp_logged.add(key)
                logger.info(
                    f"MMX5: boss HP stage {stage_id}: {self.boss_hp_vanilla} "
                    f"-> {rolled}"
                    + (" (unchanged - roll matched)"
                       if rolled == self.boss_hp_vanilla else ""))
        elif self.boss_hp_vanilla is not None and current == self.boss_hp_written:
            # Left gameplay with our value still in place: hand the game back
            # its own number so the next stage accumulates from vanilla.
            await bizhawk.write(ctx.bizhawk_ctx,
                                [(SAVE_BASE + OFF_BOSS_HP,
                                  [self.boss_hp_vanilla], "MainRAM")])
            self.boss_hp_written = None
            # Force a fresh baseline on the next stage entry even if it is the
            # same stage id (re-entering a stage recomputes 0x1CA2).
            self.boss_hp_stage = None

    async def _stage_unlocks_apply(self, ctx, cur_stage_id: int) -> None:
        """Zero the hub's slot -> stage-id entries for stages not yet unlocked.

        Re-asserted every cycle rather than once: the table is overlay data,
        reloaded from disc on every hub entry, and a savestate can swap it under
        us too. Guarded by an instruction anchor so we never write into whatever
        module happens to occupy that address in a stage.
        """
        if not (ctx.slot_data or {}).get("stage_unlocks", 0):
            return
        try:
            anchor, table = await bizhawk.read(ctx.bizhawk_ctx, [
                (SLOT_TABLE_ANCHOR_ADDR, len(SLOT_TABLE_ANCHOR), "MainRAM"),
                (SLOT_TABLE_ADDR, len(SLOT_TO_STAGE), "MainRAM"),
            ])
        except bizhawk.RequestFailedError:
            return
        if anchor != SLOT_TABLE_ANCHOR:
            # Not in the hub - forget what we wrote so the next hub entry is
            # treated as fresh (the reload will have restored vanilla bytes).
            self.slot_table_written = None
            return

        unlocked = {name for name in
                    (ctx.item_names.lookup_in_game(item.item)
                     for item in ctx.items_received)
                    if name in names.ACCESS_ITEMS}
        want = bytes(sid if names.access_item(STAGE_ID_TO_NAME[sid]) in unlocked
                     else 0
                     for sid in SLOT_TO_STAGE)
        if bytes(table) != want:
            await bizhawk.write(ctx.bizhawk_ctx,
                                [(SLOT_TABLE_ADDR, list(want), "MainRAM")])
        if self.slot_table_written != want:
            self.slot_table_written = want
            newly = unlocked - self.stages_unlocked_logged
            if newly:
                self.stages_unlocked_logged |= newly
                logger.info(f"MMX5: stages unlocked ({len(unlocked)}/8): "
                            + ", ".join(sorted(
                                n.removesuffix(" Access Codes") for n in unlocked)))

        # A blocked confirm leaves 0x800D1C0C = 0 (the store at 0x800EFC98
        # happens before the game's own zero test). Vanilla never leaves 0
        # there, and an in-hub save would commit it to the memory card, so put
        # the hub's own id back.
        if cur_stage_id:
            self.hub_stage_id = cur_stage_id
        else:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                0x0D1C0C, [self.hub_stage_id or HUB_STAGE_ID], "MainRAM")])

    async def _live_weapons_apply(self, ctx, save: bytes, in_gameplay: bool) -> None:
        """Mirror granted weapons into the LIVE bitfield so they work now.

        Grants land in the save struct, which is what a stage LOAD reads - so
        before this, a weapon received mid-stage did nothing until the player
        left and came back (tester report, 2026-08-08). The live byte is the
        one the pause menu and the fire button consult.

        Idempotent OR of bits that are already committed to the save struct,
        never a source of truth in its own right: if the save byte does not
        have the bit, neither does this. That keeps the write strictly
        downstream of the grant path's own guards rather than adding a second
        place where an item can be conjured.
        """
        if not in_gameplay:
            # 0x9Axxx is garbage outside gameplay; the stage load will restore
            # this byte from the save struct anyway.
            return
        wep_off = OFF_AP_WEAPONS if self.ap_patched else OFF_WEAPONS
        capability = save[wep_off]
        if not capability:
            return
        try:
            live = await bizhawk.read(ctx.bizhawk_ctx,
                                      [(LIVE_WEAPONS_ADDR, 1, "MainRAM")])
        except bizhawk.RequestFailedError:
            return
        merged = live[0][0] | capability
        if merged != live[0][0]:
            await bizhawk.write(ctx.bizhawk_ctx,
                                [(LIVE_WEAPONS_ADDR, [merged], "MainRAM")])
            logger.debug(f"MMX5: live weapons {live[0][0]:02X} -> {merged:02X} "
                         f"(save {capability:02X})")

    async def _pickup_dispatch_apply(self, ctx, cur_stage_id: int,
                                     in_gameplay: bool) -> None:
        """Let already-cleared stages heal from their capsules again.

        Pickupsanity redirects the collect dispatch table by ITEM KIND, so a
        randomized capsule is inert for the whole run - including on a revisit
        after its check is long since sent. In the Boss Rush that is a real
        cost (tester report, 2026-08-08).

        Only one stage's placement list is live at a time, so per-stage is as
        fine-grained as a kind-indexed table allows: if every pickupsanity
        location in the stage the player is standing in has been CONFIRMED by
        the server, nothing there is left to record and the vanilla handlers
        go back. Anywhere else - and any stage with a check still outstanding,
        including one merely sent and not yet acknowledged - keeps the stub.

        Fails safe in both directions: the stub is the default, the disc's own
        bytes are the stub, and a reload restores them.
        """
        if not (ctx.slot_data or {}).get("pickupsanity", 0):
            return
        if self.ring2_present is not True:
            return

        stage_locs = [location_table[name]
                      for stage, _area, _idx, _iid, name in pickups.PICKUPS
                      if stage == cur_stage_id]
        # Vanilla only where we are certain: in gameplay, in a stage whose
        # every pickup check is confirmed. A stage with no pickup locations at
        # all (Squid Adler, and the intro, whose single capsule is
        # deliberately not a location) qualifies too - suppressing those was
        # never intended.
        vanilla = in_gameplay and all(loc in ctx.checked_locations
                                      for loc in stage_locs)
        if self.pickup_dispatch_vanilla == (vanilla, cur_stage_id):
            return

        writes = [(DISPATCH_TABLE_ADDR + kind * 4,
                   list((VANILLA_DISPATCH[kind] if vanilla
                         else PICKUPSANITY_STUB_ADDR).to_bytes(4, "little")),
                   "MainRAM")
                  for kind in CONSUMABLE_KINDS]
        try:
            await bizhawk.write(ctx.bizhawk_ctx, writes)
        except bizhawk.RequestFailedError:
            return
        self.pickup_dispatch_vanilla = (vanilla, cur_stage_id)
        if vanilla and stage_locs:
            logger.info("MMX5: every pickup check in this stage is collected - "
                        "its capsules restore energy normally again")

    @staticmethod
    def _classify_ring2(stub_probe: bytes, dispatch_probe: bytes):
        """Is this a pickupsanity disc? True / False / None (retry).

        The stub's own bytes decide it, because the client rewrites the
        dispatch table at runtime and so cannot read its own override back as
        evidence about the disc. The dispatch entry only distinguishes a
        loaded vanilla EXE from boot, where everything reads zero.
        """
        if bytes(stub_probe) in RING2_STUB_WORDS:
            return True
        if bytes(dispatch_probe) == RING2_PROBE_VANILLA:
            return False
        return None                    # boot zeros - retry next cycle

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
            # 0x0D1C00..0x0D1C0F in one read: mode at +0, and the spawn
            # engine's stage id at +0x0C (below SAVE_BASE, so it is not in the
            # save block). The tank protection needs to know which stage the
            # player is standing in.
            mode, save, ring, ring2, rush_hp, rush_fp, player_hp, player_xy = \
                await bizhawk.read(ctx.bizhawk_ctx, [
                    (0x0D1C00, 0x10, "MainRAM"),  # game-mode controller: 0x0A gameplay / 0x0C results
                    (SAVE_BASE, SAVE_LEN, "MainRAM"),
                    (RING_ADDR, RING_SLOTS * 4, "MainRAM"),  # pickup-stub check records
                    (RING2_ADDR, RING2_SLOTS * 8, "MainRAM"),  # pickupsanity records
                    (RUSH_BOSS_HP_ADDR, 1, "MainRAM"),    # live boss HP (rush watcher)
                    (RUSH_FP_ADDR, RUSH_FP_LEN, "MainRAM"),  # boss-module fingerprint
                    (PLAYER_HP_ADDR, 1, "MainRAM"),       # player HP (rush kill gate)
                    (PLAYER_XY_ADDR, 8, "MainRAM"),       # player x/y (reploid watcher)
                ])
            # NOT `stage_id`: the mailbox-ring loop below unpacks each record
            # into a local of that name, which would clobber this before the
            # tank protection reads it (it did - the bit silently never got
            # withheld because the last empty ring slot left it 0).
            cur_stage_id = mode[0x0C]
            # ---- Sigma goal: victory on the post-Sigma ending modes ----
            # Deliberately BEFORE the save-struct gate below: the ending modes
            # are neither gameplay (0x0A) nor results (0x0C), so that gate is
            # False all the way through the credits and would swallow the goal.
            # Sequence after the final blow (live-captured): 0A -> 13 -> 14 ->
            # 10 -> 11. 0x13/0x14 also fire for the X-vs-Zero duel, so only
            # 0x10/0x11 are treated as the ending.
            ending_goal = (ctx.slot_data or {}).get("goal", GOAL_SIGMA)
            # `is not False` on purpose: an unpatched disc must not goal
            # (a goal can RELEASE every remaining location in this world,
            # the same blast radius as the phantom-check incident), but an
            # UNREADABLE probe must not swallow a legitimate ending - the
            # credits could clobber the probe region and None means only
            # "retry", never "vanilla".
            if not self.victory_sent \
                    and ending_goal in ENDING_GOALS \
                    and self.ap_patched is not False \
                    and mode[0] in ENDING_MODES:
                # all_mavericks additionally requires the full set of kills.
                # The count comes from play (self.mavericks_defeated), never
                # from a read taken here - the save struct is not sane during
                # the ending.
                if ending_goal == GOAL_ALL_MAVERICKS and self.mavericks_defeated < 8:
                    if not self.short_ending_warned:
                        self.short_ending_warned = True
                        logger.warning(
                            f"MMX5: ending reached with only {self.mavericks_defeated}/8 "
                            f"Mavericks defeated - the all_mavericks goal is NOT complete. "
                            f"Vanilla can open the endgame at 6 kills; this seed's goal "
                            f"needs all 8.")
                else:
                    self.victory_sent = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate",
                                          "status": ClientStatus.CLIENT_GOAL}])
                    logger.info(f"MMX5: ending reached (mode {mode[0]:02X}) - GOAL complete!")

            # TRAINING MODE builds a PSEUDO-SAVE in this very struct. Live
            # capture 2026-08-03: selecting Training writes ACT=0x0A and max
            # HP=0x20 in the SAME frame, so a residency check alone is
            # satisfied and the intro check fires - this is the phantom
            # "Intro Stage - Clear" a tester reported, and the residency gate
            # added in 0.1.1 did NOT stop it. A campaign save never holds ACT
            # 0x0A: the same capture read 0x02 on a real save, and the story
            # writes 1 at the intro and 5 at Eurasia. The kills term is
            # belt-and-braces so no conceivable late-game save can trip this
            # rule - training set NO kill bit across a whole session
            # including a boss kill (0x1C4C stayed 0x00 throughout), while
            # any save deep enough to matter necessarily has some.
            training = (save[OFF_INTRO] == TRAINING_ACT
                        and save[OFF_WEAPONS] == 0)
            # Deliberately folded into save_sane rather than guarded
            # separately: every consumer - check detection, item grants and
            # launch pinning - already keys off this one flag, so training is
            # inert everywhere at once instead of in three places that could
            # drift apart.
            save_sane = 0x10 <= save[OFF_MAX_HP_X] <= 0x40 and not training
            if training != self.last_training_state:
                self.last_training_state = training
                if training:
                    logger.info("MMX5: training mode detected - checks and "
                                "grants suspended until you leave it")
            in_gameplay = mode[0] in (0x0A, 0x0C) and save_sane
            # Recorded HERE, before any early return below, so "was the
            # previous read taken in gameplay" always refers to the previous
            # read of the struct, not the previous poll that got this far.
            was_in_gameplay = self.last_in_gameplay
            self.last_in_gameplay = in_gameplay
            if in_gameplay != self.last_gate_state:
                logger.debug(f"MMX5: save-struct gate -> {in_gameplay} (maxhp: {save[OFF_MAX_HP_X]:02X})")
                self.last_gate_state = in_gameplay
                # Savestates restore ALL of RAM including the loaded EXE, so
                # the disc mode can CHANGE mid-session. Re-probe on EVERY
                # gate transition (stage entry AND exit-to-hub).
                self.ap_patched = None
                self.stub_present = None
                # Savestates restore the EXE, so the tank fix can appear or
                # vanish mid-session exactly like the other two.
                self.tank_fix_present = None
                self.ring2_present = None
                # Same reason: a savestate can put the disc's own (stubbed)
                # dispatch words back under an override we think is still
                # applied. Forget it so the next cycle re-decides.
                self.pickup_dispatch_vanilla = None

            # Resolve the probes whenever unresolved - NOT just in-stage.
            # Launches happen at the HUB (modes 0x13-0x15); the old
            # in-gameplay-only resolution left ap_patched unresolved on a
            # boot-to-hub path and score pinning silently no-oped (live
            # 2026-08-01: an unpinned Enigma launch succeeded off vanilla
            # accrual + the zeroed roll). During boot the EXE reads as
            # zeros -> classify returns None -> retried next cycle.
            if self.ap_patched is None or self.stub_present is None \
                    or self.tank_fix_present is None or self.ring2_present is None:
                probe, stub_probe, tank_probe, ring2_probe, ring2_stub = \
                    await bizhawk.read(ctx.bizhawk_ctx, [
                        (PATCH_PROBE_ADDR, 4, "MainRAM"),
                        (STUB_PROBE_ADDR, 4, "MainRAM"),
                        (TANK_FIX_PROBE_ADDR, 4, "MainRAM"),
                        (RING2_PROBE_ADDR, 4, "MainRAM"),
                        (RING2_STUB_PROBE_ADDR, 4, "MainRAM"),
                    ])
                self.tank_fix_present = self._classify_tank_fix(tank_probe)
                self.ap_patched = self._classify_probe(probe)
                self.last_probe_word = bytes(probe)   # for the refusal message
                self.stub_present = self._classify_stub_probe(stub_probe)
                self.ring2_present = self._classify_ring2(ring2_stub, ring2_probe)

            # ---- UNPATCHED DISC: hold everything ---------------------------
            # Directly after probe resolution, BEFORE every block that writes
            # the save struct or reads it for checks. It used to sit below the
            # boss-HP / DNA-Part / stage-unlock writers, so an unpatched disc
            # still had Parts granted, vanilla Parts suppressed, stages locked
            # and boss HP rerolled - "holds all checks and items" was not
            # actually true. Nothing above this line touches the game.
            #
            # Why refuse at all: the old "hybrid mode" wrote AP-granted
            # weapons into 0x1C4C, which is the VANILLA kill record - the same
            # byte the 24 boss / DNA Reward / DNA Part checks read as ground
            # truth. Every weapon the multiworld sent you therefore marked its
            # boss defeated and fired three checks, releasing items to
            # everyone else. Reported by a tester 2026-08-06 ("it sends all
            # those checks before I even started playing") and reproduced
            # exactly: 8 weapons received, zero bosses beaten, 24 checks sent.
            #
            # Detection is gated too, not just grants, because a save already
            # poisoned by a hybrid session still holds those bits and would
            # fire them again on the next connect. The goal is held separately
            # at the top of this method (an unpatched playthrough must not
            # RELEASE this world's locations either).
            #
            # Hybrid dates from before the disc patch existed; the module
            # header always flagged it as interim. Every supported flow
            # produces a patched disc - the .apmmx5 IS the delivery mechanism -
            # so this is unreachable in correct use and corrupts a multiworld
            # in incorrect use.
            if self.ap_patched is False:
                if not self.unpatched_warned:
                    self.unpatched_warned = True
                    probe_note = (f" (probe read {self.last_probe_word.hex()})"
                                  if self.last_probe_word else "")
                    logger.error(
                        "MMX5: this disc is NOT AP-patched - checks and items are "
                        "HELD. On an unpatched disc the weapons you receive get "
                        "written into the byte the game uses to record boss kills, "
                        "which would send false checks to everyone in your "
                        "multiworld. Patch your disc: open your .apmmx5 with the "
                        "Archipelago Launcher, then load the .cue it produces."
                        + probe_note)
                return

            # ---- Boss HP randomization: hold the rolled value while in a
            # stage, hand the vanilla number back on the way out (0x1CA2
            # accumulates, so leaving ours in place would compound). Runs
            # before the stamp gate deliberately - the restore must happen
            # even on a save we are otherwise refusing to touch, or a
            # mid-session save swap could strand our value in the struct. ----
            if save_sane:
                await self._boss_hp_apply(ctx, save, mode[0] == 0x0A, cur_stage_id)

            # ---- Wrong-save protection (A3): a sane save stamped for a
            # DIFFERENT seed/slot halts checks AND grants - its bits belong
            # to another game. Swap saves, or deliberately reuse this one by
            # zeroing 0x1C4D-0x1C50 in the Lua console. Unstamped saves (0)
            # pass HERE; the A3b hold below decides whether they are fresh
            # (stamp them) or progressed (hold them). ----
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

            # ---- DNA Parts: the AP-granted set, and nothing else -----------
            # One write covers both halves of the feature. Parts the player
            # received are OR-ed in; Parts the GAME granted are cleared, which
            # is the suppression - X5 delivers a Part at the results screen
            # after a level-8+ Maverick kill, and with this option on that
            # reward comes from the multiworld instead.
            #
            # Only bits 2..17 are touched. The rest of the word has no known
            # meaning, and assuming it is spare is exactly the kind of guess
            # this project has been bitten by.
            if save_sane and (ctx.slot_data or {}).get("dna_parts_in_pool", 0):
                want = 0
                for item in ctx.items_received:
                    bit = PART_TO_BIT.get(ctx.item_names.lookup_in_game(item.item))
                    if bit is not None:
                        want |= 1 << bit
                cur = int.from_bytes(save[OFF_PARTS:OFF_PARTS + 4], "little")
                merged = (cur & ~PARTS_MASK) | want
                if merged != cur:
                    await bizhawk.write(ctx.bizhawk_ctx, [(
                        SAVE_BASE + OFF_PARTS,
                        list(merged.to_bytes(4, "little")), "MainRAM")])
                    if (cur & PARTS_MASK) & ~want:
                        logger.debug("MMX5: suppressed a vanilla DNA Part grant")

            # ---- Stage unlocks: hold locked slots at 0 in the hub's
            # slot -> stage-id table. AFTER the stamp gate on purpose - locking
            # is the inverse of granting, so a save belonging to another seed
            # should not have this seed's locks imposed on it either. Safe to
            # skip: the table is overlay data and reloads vanilla on the next
            # hub entry, so bailing out never leaves a stage stuck shut. ----
            if save_sane:
                await self._stage_unlocks_apply(ctx, cur_stage_id)

            # ---- Live weapon mirror, and handing cleared stages their
            # capsules back. Both are conveniences layered on state that is
            # already decided elsewhere: the first only re-states weapon bits
            # the save struct already holds, the second only relaxes
            # suppression for locations the SERVER has already confirmed. Both
            # after the stamp gate, for the same reason stage unlocks are. ----
            if save_sane:
                await self._live_weapons_apply(ctx, save, mode[0] == 0x0A)
                await self._pickup_dispatch_apply(ctx, cur_stage_id,
                                                  mode[0] == 0x0A)

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
            # ---- What it takes to BELIEVE the save struct -------------------
            # `save_sane` alone is far too weak: its only residency test is
            # 0x10 <= maxHP <= 0x40, which RAM left over from a previous game
            # satisfies exactly - and RAM survives a soft reset, so "I started
            # a new save" does not mean the struct held that new save when we
            # read it. A tester's world sent 24 phantom checks to an 8-player
            # multiworld on 2026-08-06; on a patched disc the client cannot
            # have written those bits, so something was read that was not a
            # live save. Rather than guess which, close the class.
            #
            # Four additional requirements, all cheap:
            #
            #  (a) IN GAMEPLAY. Modes 0x0A/0x0C mean a save is definitionally
            #      resident. The title screen, the data-select menu and the
            #      attract demo are not gameplay, and those are exactly where
            #      leftover RAM gets read as progress. Costs nothing: boss
            #      kills commit at the results screen (0x0C), and any check
            #      detected elsewhere fires on the next gameplay cycle anyway,
            #      because detection is level-triggered, not edge-triggered.
            #
            #  (b) STABLE across two consecutive polls. A struct being written
            #      during a load can read as a plausible half-state for a
            #      frame; requiring the check-driving bytes to repeat costs one
            #      poll and removes that whole window.
            #
            #  (c) THE PREVIOUS POLL WAS ALSO GAMEPLAY. (b) alone buys nothing
            #      against stale RAM, because the signature is recorded on
            #      menu polls too and stale RAM never changes - so a single
            #      poll landing in a gameplay mode would be trusted instantly
            #      off a signature the title screen established. Two
            #      consecutive gameplay reads close that.
            #
            #      NB an earlier draft justified (d) by citing a stage-load
            #      mode walk '0A->0B->0C->0E' from ram-notes. That sequence is
            #      NOT the mode byte - it is 0x800D1CB4, the fast per-stage
            #      COUNTER documented there as a known decoy. The only mode
            #      walk actually on record is 0A->13->14 at the Sigma kill.
            #      (c) and (d) are kept anyway, as cheap conservatism, but
            #      they rest on 'we have not mapped this byte', not on
            #      evidence that 0x0C occurs mid-load.
            #
            #  (d) 0x0C ONLY AFTER A TRUSTED 0x0A. A results screen always
            #      follows real gameplay; the 0x0C in the stage-LOAD walk does
            #      not necessarily, and if the loader parks there with the
            #      previous session's struct still in RAM, (b)+(c) could both
            #      pass.
            #      Requiring one trusted gameplay poll first makes 0x0C an
            #      extension of a live session, never the start of one.
            #
            # Deliberately NOT relying on internal consistency (e.g. "8 kills
            # implies ACT >= 5"): the all_mavericks goal makes that briefly
            # false ON PURPOSE by withholding ACT, so it would reject real
            # saves.
            #
            # The signature is WIDER than the bytes save_checks read (tanks
            # and armor feed only the mailbox ring): breadth is deliberate.
            # The signature's job is evidence the struct is not mid-write,
            # and more bytes is more evidence. The cost is that our own grant
            # writes flip it and delay save checks by one poll - accepted.
            check_sig = (save[OFF_INTRO], save[OFF_WEAPONS], save[OFF_HEARTS],
                         save[OFF_TANKS], save[OFF_ARMOR])
            stable = check_sig == self.last_check_sig
            self.last_check_sig = check_sig
            results_ok = mode[0] != 0x0C or self.gameplay_anchored
            save_trusted = in_gameplay and was_in_gameplay and stable and results_ok
            if save_trusted and mode[0] == 0x0A:
                self.gameplay_anchored = True
            if save_trusted != self.last_trust_state:
                self.last_trust_state = save_trusted
                logger.debug(f"MMX5: save trusted -> {save_trusted} "
                             f"(gameplay {in_gameplay}, prev {was_in_gameplay}, "
                             f"stable {stable}, results_ok {results_ok})")

            # ---- Unstamped save with pre-existing progress: hold (A3b) -----
            # Fix B stops STALE RAM; it deliberately trusts a genuinely
            # resident save - and a save with pre-AP progress is exactly that.
            # A vanilla playthrough on a cloned memcard, "Continue" on the
            # wrong slot, or a savestate from before this seed's first
            # connect all read as real progress and would fire every check it
            # contains into the multiworld. The A3 stamp gate above cannot
            # catch them: a save this seed never touched is stamped 0, which
            # passes.
            #
            # So the stamp is now written on the FIRST TRUSTED SIGHT of a
            # fresh save (not with the first grant batch - a player who never
            # receives an item would stay unstamped forever and trip this on
            # their next session), and a save that arrives at its first
            # trusted poll unstamped but already progressed is held until the
            # player says it is deliberate. Trusted, not merely sane, on
            # purpose: evaluating this on stale RAM would hold (and warn
            # about) bytes that are not a save at all.
            if save_trusted and ctx.seed_name and save[OFF_STAMP] == 0:
                # ACT (OFF_INTRO) is deliberately NOT progress here.
                # Including it locked out an ordinary flow: boot the game,
                # start playing, THEN open the client - the moment the intro
                # clears, ACT is 1 and the save was held behind a Lua command.
                # The asymmetry is worth it. ACT alone claims exactly ONE
                # location (Intro Clear); weapons/hearts/tanks/armor are where
                # the 24-check blast radius lives, and those still hold.
                progressed = (save[OFF_WEAPONS] or save[OFF_HEARTS]
                              or save[OFF_TANKS] or save[OFF_ARMOR])
                if progressed:
                    if not self.unstamped_warned:
                        self.unstamped_warned = True
                        logger.error(
                            f"MMX5: this save has progress but has never been used "
                            f"with this seed - checks and grants are HELD so it "
                            f"cannot flood the multiworld. If this is leftover or "
                            f"vanilla progress, start a NEW GAME on a fresh slot. "
                            f"If you really mean to bring this save into this "
                            f"multiworld, run this in BizHawk's Lua console: "
                            f"mainmemory.writebyte(0x{SAVE_BASE + OFF_STAMP:06X}, "
                            f"0x{self._seed_stamp(ctx):02X})")
                    return
                await bizhawk.write(ctx.bizhawk_ctx, [(
                    SAVE_BASE + OFF_STAMP, [self._seed_stamp(ctx)], "MainRAM")])
                logger.debug("MMX5: fresh save adopted (stamped "
                             f"{self._seed_stamp(ctx):02X})")
            if self.unstamped_warned and save_trusted \
                    and save[OFF_STAMP] == self._seed_stamp(ctx):
                self.unstamped_warned = False
                logger.info("MMX5: save adopted into this seed - resuming")

            def save_check(location_name: str, condition: bool) -> None:
                check(location_name, condition and save_trusted)

            save_check(names.INTRO_CLEAR, save[OFF_INTRO] != 0)

            # ---- Zero Space clears -----------------------------------------
            # Latched at a high-water mark, NOT read live. Two things move this
            # byte other than progress: the all_mavericks withhold below pushes
            # it back under 5, and training parks 0x0A in it - which is >= every
            # threshold here and would fire all three checks at once. save_sane
            # already excludes training; the explicit test is belt-and-braces,
            # the same way the Maverick tally guards itself.
            # Latched only from a TRUSTED read - a high-water mark taken from
            # stale RAM would be permanent, and would fire all three Zero
            # Space checks on a save that never cleared them.
            if save_trusted and save[OFF_INTRO] != TRAINING_ACT:
                self.max_act_seen = max(self.max_act_seen, save[OFF_INTRO])
            if (ctx.slot_data or {}).get("endgame_checks", 0):
                for stage, act in ENDGAME_CLEAR_ACT.items():
                    save_check(names.endgame_clear_location(stage),
                               self.max_act_seen >= act)

            # ---- Reploid rescues (client-side watcher) ---------------------
            # A rescue is lives rising during trusted gameplay in a Reploid
            # stage while the player stands on a Reploid record (rescue
            # requires overlap; live rescues matched within ~25px). Position
            # is the discriminator against 1-UP pickups, and the tracker is
            # None outside trusted gameplay so menus, savestate loads and
            # stage transitions can never fake an increment. Two rescues
            # inside one poll window send the two nearest records (the only
            # adjacent pair, Skiver's x=896/984, is 88px apart - well inside
            # one radius).
            if (ctx.slot_data or {}).get("reploid_checks", 0):
                records = REPLOID_RECORDS_BY_STAGE.get(cur_stage_id)
                lives_now = save[OFF_LIVES]
                trusted_here = (save_trusted and mode[0] == 0x0A
                                and records is not None)
                prev = self.reploid_lives
                if trusted_here and prev is not None \
                        and prev[0] == cur_stage_id and lives_now > prev[1]:
                    px = int.from_bytes(player_xy[0:2], "little", signed=True)
                    py = int.from_bytes(player_xy[4:6], "little", signed=True)
                    near = sorted(
                        (max(abs(x - px), abs(y - py)), name)
                        for x, y, name in records
                        if abs(x - px) <= REPLOID_MATCH_RADIUS
                        and abs(y - py) <= REPLOID_MATCH_RADIUS)
                    for _dist, name in near[:lives_now - prev[1]]:
                        check(name, True)
                    if not near:
                        # 1-UP pickup or enemy drop away from any Reploid -
                        # correct silence; logged at debug for diagnosability.
                        logger.debug(
                            f"MMX5: lives +{lives_now - prev[1]} at "
                            f"({px},{py}) with no Reploid record in range - "
                            f"treated as a 1-UP, no check")
                self.reploid_lives = ((cur_stage_id, lives_now)
                                      if trusted_here else None)

            # ---- Boss Rush rematch kills (client-side watcher) -------------
            # Fight state machine per ram-notes §Boss fights. Every condition
            # must hold at the SAME poll:
            #   stage 0x0C + mode 0x0A - the rush, in gameplay.
            #   fingerprint matches    - the resident module names the fight
            #       (256 bytes, disc-unique - see RUSH_FP_LEN for why 16 was
            #       not). An unknown module sends NOTHING.
            #   saw the fill          - the intro bar ramps +1/frame from 1 to
            #       max, so a real fight is VISIBLE as a rise. Required
            #       because identity alone cannot mean "in progress".
            #   peak >= RUSH_MIN_PEAK  - the rise reached fight scale.
            #   boss HP == 0           - the kill. It persists 600+ frames,
            #       so a poll cannot miss it.
            #   player HP > 0          - a player death mid-fight must never
            #       read as a boss kill, whatever the respawn does to the
            #       boss-HP byte (the module stays resident through it).
            #
            # WHY THE FILL AND THE ONE-SEND RULE EXIST (2026-08-09). Two
            # captured corridor states - ramdump_rematch_before_f369766 (Izzy
            # resident) and _after_f372037 (Dizzy resident) - satisfy stage,
            # mode, identity, boss HP 0 and player alive with NO fight
            # happening. Every term except the fill is true while simply
            # walking between portals. Requiring an observed rise inside the
            # current arming rejects both no-fight paths: a stale byte that
            # later drops to 0 (ram-notes records 16 at stage entry), and a
            # resident module with the byte already 0.
            #
            # Deliberately NOT save_trusted: nothing here reads the save
            # struct, and the server is the permanent record - the rush
            # resets on stage re-entry, so a send missed by a disconnect is
            # refightable, the same shape as pickupsanity's ring.
            if (ctx.slot_data or {}).get("rematch_checks", 0):
                in_rush = cur_stage_id == SIGMA_STAGE_ID and mode[0] == 0x0A
                fp_boss = (RUSH_FP_TO_STAGE.get(hashlib.sha256(bytes(rush_fp)).hexdigest())
                           if in_rush else None)
                if fp_boss != self.rush_boss:
                    # Identity changed: a new portal streamed a module in, or
                    # we left the rush. This is the ONLY thing that arms a
                    # fight - a module that has merely stayed resident since
                    # the last kill can never credit again.
                    self.rush_boss = fp_boss
                    self.rush_peak = 0
                    self.rush_prev_hp = None
                    self.rush_saw_low = False
                    self.rush_saw_fill = False
                    self.rush_sent = False
                if fp_boss is not None:
                    if (player_hp[0] & 0x7F) == 0:
                        # Player down mid-fight. Death costs seconds of
                        # non-gameplay modes, but polls are sparse - relying
                        # on catching one of those frames would leave a
                        # window where "boss 0 + player respawned" still
                        # carried the dead fight's peak. Dropping the whole
                        # arming here closes it: the boss must be seen to
                        # fill again before another kill can count.
                        self.rush_peak = 0
                        self.rush_prev_hp = None
                        self.rush_saw_low = False
                        self.rush_saw_fill = False
                    else:
                        hp_now = rush_hp[0]
                        # "The bar was seen to fill" - two ways to establish
                        # it, because polls are far sparser than the ~1s ramp
                        # and one rule alone is either brittle or leaky:
                        #
                        #   a strict rise      - stale bytes do not climb, so
                        #       any increase is the engine filling the bar;
                        #   low THEN >= peak   - covers the common case where
                        #       the ramp completes entirely between two polls;
                        #       the arming poll supplies the low reading, and
                        #       after a kill the byte sits at 0, which is low.
                        #
                        # Neither admits the two no-fight states: a stale byte
                        # at or above the threshold never rises and was never
                        # seen low, and a resident module with the byte at 0
                        # never reaches the threshold.
                        if self.rush_prev_hp is not None and hp_now > self.rush_prev_hp:
                            self.rush_saw_fill = True
                        if hp_now < RUSH_MIN_PEAK:
                            self.rush_saw_low = True
                        elif self.rush_saw_low:
                            self.rush_saw_fill = True
                        self.rush_prev_hp = hp_now
                        self.rush_peak = max(self.rush_peak, hp_now)
                        if (hp_now == 0 and self.rush_saw_fill
                                and self.rush_peak >= RUSH_MIN_PEAK
                                and not self.rush_sent):
                            check(names.rematch_location(fp_boss), True)
                            # One send per arming. Re-arming needs a module
                            # change, i.e. an actual new portal.
                            self.rush_sent = True

            # ---- all_mavericks: hold the endgame shut until 8 kills --------
            # The colony resolution writes ACT = ENDGAME_ACT, which is what
            # opens Zero Space. Under this goal that must not happen early, or
            # a player reaches Sigma short of the full set, kills him, and the
            # goal can never fire - and Sigma does NOT respawn, so the run is
            # over. Withhold the value and hand it back at 8.
            #
            # Client-side on purpose: the disc shuttle-era edit turned out to
            # gate only the story announcement, not access. This gates access.
            if save_sane and (ctx.slot_data or {}).get("goal", GOAL_SIGMA) == GOAL_ALL_MAVERICKS:
                act_now = save[OFF_INTRO]
                kills_for_act = bin(save[OFF_WEAPONS]).count("1")
                if act_now < ENDGAME_ACT and act_now != TRAINING_ACT:
                    self.last_pre_endgame_act = act_now
                if kills_for_act < 8 and act_now >= ENDGAME_ACT:
                    # Restore the exact value the story last legitimately held.
                    restore = (self.last_pre_endgame_act
                               if self.last_pre_endgame_act is not None
                               else ENDGAME_ACT - 1)
                    await bizhawk.write(ctx.bizhawk_ctx,
                                        [(SAVE_BASE + OFF_INTRO, [restore], "MainRAM")])
                    self.act_withheld = True
                    if not self.act_withheld_warned:
                        self.act_withheld_warned = True
                        logger.info(
                            f"MMX5: the colony resolved with only {kills_for_act}/8 "
                            f"Mavericks down - holding the endgame shut until all 8 "
                            f"are defeated. Zero Space opens on the eighth kill.")
                elif kills_for_act >= 8 and self.act_withheld and act_now < ENDGAME_ACT:
                    # Full set: give back what was withheld, or the player
                    # could never reach Sigma at all.
                    await bizhawk.write(ctx.bizhawk_ctx,
                                        [(SAVE_BASE + OFF_INTRO, [ENDGAME_ACT], "MainRAM")])
                    self.act_withheld = False
                    logger.info("MMX5: all 8 Mavericks down - Zero Space is open.")

            weapons_owned = save[OFF_WEAPONS]
            # Maverick tally for the all_mavericks goal. 0x1C4C is the VANILLA
            # kill record - AP grants go to 0x1C4D - so its popcount is real
            # kills and nothing else. Gated on save_sane and monotonic, so a
            # transient bad read can never lower a count already earned.
            # Trusted, not merely sane - this LATCHES, and it decides the
            # all_mavericks goal. A stale 0xFF read would score 8 permanently
            # and hand out a false victory, which no later good read can undo.
            # Same hazard as max_act_seen; both now use the same gate.
            if save_trusted:
                self.mavericks_defeated = max(self.mavericks_defeated,
                                              bin(weapons_owned).count("1"))
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
                        # Capsule id == armor part index, so every capsule
                        # anyone opens reveals one entry of the stage -> part
                        # map. Only four of eight are verified, and that map is
                        # what STAGE_CAPSULE_ARMOR_BIT needs before it can
                        # protect any stage other than Squid Adler. Logging it
                        # here means ordinary play fills the map in for free
                        # rather than anyone hand-testing seven stages.
                        if rec_id < len(names.ARMOR_PARTS):
                            logger.info(
                                f"MMX5: capsule map - {stage} grants "
                                f"{names.ARMOR_PARTS[rec_id]} (capsule id {rec_id})")

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

            # ---- Pickupsanity ring (per-seed stub): consumable pickups.
            # Identity comes from the RECORD POINTER the stub copied out of
            # itemObj+0x10 - the id byte is a type and collides. Same
            # record-until-confirmed/ack discipline as the main ring. ----
            if self.ring2_present and (ctx.slot_data or {}).get("pickupsanity", 0):
                ack_writes, ack_guards = [], []
                for slot in range(RING2_SLOTS):
                    rec = ring2[slot * 8:slot * 8 + 8]
                    stage_id, kind, rec_id, seq = rec[0], rec[1], rec[2], rec[3]
                    if not seq & 0x80:
                        continue  # empty/consumed slot
                    recptr = int.from_bytes(rec[4:8], "little")
                    loc_name = pickups.RECORD_TO_LOCATION.get(recptr)
                    # The stage byte is a corruption check on the pointer, not
                    # the identity: a stale/garbage record whose pointer
                    # happens to hit the map must not send a wrong check.
                    if loc_name is not None \
                            and pickups.LOCATION_STAGE_ID[loc_name] != stage_id:
                        loc_name = None
                    if loc_name is not None:
                        check(loc_name, True)
                        consume = location_table[loc_name] in ctx.checked_locations
                    else:
                        # The intro capsule (deliberately not a location) and
                        # anything unmapped: log once, consume, don't send.
                        # Two keys on purpose. The info line is deduped
                        # WITHOUT the record pointer, because enemy-dropped
                        # consumables come through this same branch with a
                        # different pointer every time - keying on it would
                        # turn an info-level line into a spam firehose. The
                        # debug line keeps the pointer for every record.
                        #
                        # The info line still SHOWS one example pointer, and
                        # that sample is load-bearing: the disc-side fix for
                        # "enemy drops do nothing under pickupsanity" needs to
                        # know what a dropped item carries at obj+0x10 (a zero,
                        # a stale pooled value, or something else), and this is
                        # the only place that value surfaces without an
                        # emulator session. One line per kind per stage.
                        info_key = ("ring2", stage_id, kind, rec_id)
                        if info_key not in self.unknown_records_logged:
                            self.unknown_records_logged.add(info_key)
                            logger.info(
                                f"MMX5: unmapped pickupsanity record stage={stage_id} "
                                f"kind={kind:X} id={rec_id:02X} rec=0x{recptr:08X} "
                                f"- ignored (further records of this kind in this "
                                f"stage are silent)")
                        rec_key = ("ring2ptr", stage_id, kind, rec_id, recptr)
                        if rec_key not in self.unknown_records_logged:
                            self.unknown_records_logged.add(rec_key)
                            logger.debug(
                                f"MMX5: unmapped pickupsanity record stage={stage_id} "
                                f"kind={kind:X} id={rec_id:02X} rec=0x{recptr:08X} - ignored")
                        consume = True
                    if consume:
                        ack_writes.append((RING2_ADDR + slot * 8 + 3, [0], "MainRAM"))
                        ack_guards.append((RING2_ADDR + slot * 8, rec, "MainRAM"))
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
                kills_now = bin(save[OFF_WEAPONS]).count("1")
                if (ctx.slot_data or {}).get("launch_odds", 0) == LAUNCH_ODDS_VANILLA:
                    # Vanilla odds: hand the game a SCORE in the band that
                    # matches the parts held and let its own roll decide.
                    # (Roll ladder in Rom.py; the disc keeps its vanilla andi
                    # under this option, so 0x800FA0D4 is not neutralised.)
                    # The all_mavericks gate still wins: a successful launch
                    # before 8 kills would open the endgame ahead of the goal.
                    if goal == GOAL_ALL_MAVERICKS and kills_now < 8:
                        want_mod = 0
                    elif kills_now >= 6:
                        want_mod = (LAUNCH_SCORE_75 if shuttle >= 3
                                    else LAUNCH_SCORE_37 if shuttle >= 1
                                    else LAUNCH_SCORE_12)
                    else:
                        want_mod = (LAUNCH_SCORE_12 if enigma >= 1
                                    else LAUNCH_SCORE_6)
                    powered = want_mod > 0
                elif goal == GOAL_LAUNCH:
                    # Launch goal: nothing fires until every part is in hand.
                    powered = enigma >= 4 and shuttle >= 4
                else:
                    # Story flavor: power whichever launcher the chapter
                    # offers (shuttle era begins at 6 recorded kills).
                    kills = bin(save[OFF_WEAPONS]).count("1")
                    if goal == GOAL_ALL_MAVERICKS and kills < 8:
                        # A SUCCESSFUL Enigma resolves the colony on its own,
                        # and the Enigma is offered from 2 kills - so lucky
                        # early parts could open the endgame six Mavericks
                        # short, without the shuttle ever being involved. The
                        # disc gate moves the shuttle era to 8; this closes the
                        # other door. Both are needed: neither covers the
                        # other's path.
                        powered = False
                    else:
                        powered = (shuttle >= 4) if kills >= 6 else (enigma >= 4)
                pin = []
                if save[OFF_SCORE_ACC:OFF_SCORE_ACC + 4] != b"\x00\x00\x00\x00":
                    pin.append((SAVE_BASE + OFF_SCORE_ACC, [0, 0, 0, 0], "MainRAM"))
                # Deterministic odds reduce to a flat 0/1, because the disc's
                # roll is neutralised and any score > 0 succeeds. Vanilla odds
                # already chose a banded score above - do not flatten it.
                if (ctx.slot_data or {}).get("launch_odds", 0) != LAUNCH_ODDS_VANILLA:
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
                # Goal requires BOTH a successful launch and the parts that
                # were supposed to power it. The flag alone is not enough:
                # vanilla launches the shuttle by itself once all eight
                # Mavericks are down, which completed the launch goal for a
                # tester holding only 3 of 8 parts. The world's own
                # completion_condition already demands all 8, so firing on the
                # flag alone had the client disagreeing with its own logic.
                if goal == GOAL_LAUNCH and not self.victory_sent \
                        and save[OFF_LAUNCH_FLAGS] & 0x80 and powered:
                    self.victory_sent = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    logger.info("MMX5: launch succeeded with all 8 parts - GOAL complete!")
                elif goal == GOAL_LAUNCH and not self.victory_sent \
                        and save[OFF_LAUNCH_FLAGS] & 0x80 and not self.unpowered_launch_warned:
                    self.unpowered_launch_warned = True
                    logger.info(
                        f"MMX5: a launch succeeded, but this is the story's own launch - "
                        f"you have {enigma}/4 Enigma and {shuttle}/4 Shuttle parts. "
                        f"The goal needs all 8, so keep collecting.")

            if new_checks:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])

            # ---- Item grants (only while the save struct is TRUSTED) ----
            # Same bar as reading it: never write items into a struct we
            # would not believe - a grant landing in stale or mid-load RAM is
            # at best lost and at worst mutates bytes the real load then
            # inherits. Level-triggered like everything else, so the
            # one-poll delay this adds after entering gameplay is invisible;
            # the withhold protections below re-engage on the next trusted
            # poll for the same reason.
            if save_trusted:
                # Resolve disc mode if boot raced the EXE load; in gameplay
                # the EXE is fully resident, so this settles on first cycle.
                # Probes resolve at the top of every cycle now; in-stage the
                # EXE is fully resident so an unresolved probe here is
                # genuinely abnormal - hold grants.
                if self.ap_patched is None:
                    logger.warning("MMX5: disc mode unresolved in-game - grants held")
                    return


                # ---- Tank-pickup protection (discs WITHOUT the tank fix) ----
                # The item init deletes any pickup you already own, so an
                # AP-granted tank bit destroys the vanilla pickup that IS that
                # location's check - permanently, and those locations can hold
                # progression, so it can strand a seed. While the player is in
                # the stage owning an UNCHECKED tank location, hold that one
                # bit clear. The check still lands normally: the pickup stub
                # records it to the ring, so the game and the client never
                # fight over the bit. The tank returns as soon as the location
                # is checked or the player leaves.
                # Runs EVERY cycle, not inside the grant batch below - a
                # player who already received their tank has nothing new to
                # grant, and is exactly the person this protects.
                # Gated on the probe: a patched disc needs none of this, and
                # withholding a tank there would be a pure downgrade.
                stage_name = STAGE_ID_TO_NAME.get(cur_stage_id)
                withhold = 0
                if self.tank_fix_present is False and stage_name:
                    withhold = self._tank_bit_to_withhold(ctx, stage_name)

                # Same protection for armor: owning the part a capsule grants
                # can hide the vanilla route to that capsule (proven for Squid
                # Adler's energy balls). Unlike tanks there is no disc fix yet,
                # so this is unconditional rather than probe-gated.
                #
                # It has to cover the WHOLE stage visit, not just loading.
                # Measured 2026-08-03 by holding the bit clear over different
                # windows: clear across the entire load but restored as
                # gameplay begins -> balls still gone; clear for the first 600
                # frames of gameplay -> balls present. The check runs per ball
                # as the screen scan reaches it, exactly like ordinary item
                # spawns, so there is no load-time window to restore in.
                armor_withhold = 0
                if stage_name:
                    armor_withhold = self._armor_bit_to_withhold(ctx, stage_name)
                if armor_withhold and (save[OFF_ARMOR] & armor_withhold):
                    # Pin the set-completion flags (0x1C4A) while the part
                    # bit is withheld.
                    #
                    # MEASURED 2026-08-03 with a real complete Falcon set: the
                    # game did NOT clear the flag when it saw an incomplete
                    # parts byte (0x1C4A held 03 throughout), so this write is
                    # normally a no-op - it is insurance, not the mechanism.
                    #
                    # WHY THIS COSTS THE PLAYER NOTHING (verified live with a
                    # complete Falcon set): the game decides which armor to
                    # EQUIP from the parts byte when the stage LOADS, while the
                    # energy balls consult ownership during GAMEPLAY. This
                    # withhold runs only inside the in_gameplay branch, so it
                    # lands between the two - X wears the armor and the balls
                    # are present at the same time.
                    #
                    # So do NOT move it earlier. Withholding across stage
                    # loading strips the armor for that stage, and doing it
                    # regardless of stage strips it everywhere: a test harness
                    # made exactly that mistake and lost armor in Grizzly
                    # Slash, a stage this never touches.
                    #
                    # Because the flag survives, the armor returns as soon as
                    # the bit is restored - no results screen needed, nothing
                    # lost permanently. Nothing in that stage requires Falcon
                    # armor to reach, so this costs convenience, not access.
                    writes = [(SAVE_BASE + OFF_ARMOR,
                               [save[OFF_ARMOR] & ~armor_withhold], "MainRAM")]
                    if self.armor_setflags_pin is None:
                        self.armor_setflags_pin = save[OFF_SETFLAGS]
                    if save[OFF_SETFLAGS] != self.armor_setflags_pin:
                        writes.append((SAVE_BASE + OFF_SETFLAGS,
                                       [self.armor_setflags_pin], "MainRAM"))
                    await bizhawk.write(ctx.bizhawk_ctx, writes)
                    if not self.armor_workaround_warned:
                        self.armor_workaround_warned = True
                        logger.info(
                            "MMX5: holding back an armor part while you are in this stage - "
                            "owning it hides the route to that stage's capsule. You get it "
                            "back once the capsule check is collected or you leave.")
                    return   # re-read next cycle with the bit actually clear
                if withhold != self.tanks_withheld:
                    self.tanks_withheld = withhold
                    logger.debug(f"MMX5: tank protection -> withhold {withhold:02X}")
                if withhold and (save[OFF_TANKS] & withhold):
                    await bizhawk.write(ctx.bizhawk_ctx, [(
                        SAVE_BASE + OFF_TANKS,
                        [save[OFF_TANKS] & ~withhold], "MainRAM")])
                    if not self.tank_workaround_warned:
                        self.tank_workaround_warned = True
                        logger.info(
                            "MMX5: this disc predates the tank fix, so a tank is being held "
                            "back to keep its pickup from being deleted. You get it once "
                            "that check is collected. Re-patch with the current apworld to "
                            "remove this entirely.")
                    return   # re-read next cycle with the bit actually clear
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
                    new_energy = 0
                    for item in ctx.items_received[processed:]:
                        item_name = ctx.item_names.lookup_in_game(item.item)
                        if item_name == names.HEART_TANK:
                            new_hearts += 1
                        elif item_name == names.SMALL_ENERGY:
                            new_energy += 1
                        # weapons/tanks/armor handled cumulatively below

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
                    want_ultimate = False
                    want_black_zero = False
                    for item in ctx.items_received:
                        item_name = ctx.item_names.lookup_in_game(item.item)
                        if item_name == names.ULTIMATE_ARMOR:
                            want_ultimate = True
                        elif item_name == names.BLACK_ZERO:
                            want_black_zero = True
                        elif item_name in WEAPON_TO_BIT:
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
                    # `withhold` is computed once per cycle further down (the
                    # unpatched-disc tank protection) and applied here too, so
                    # a grant batch cannot re-set a bit the protection just
                    # cleared.
                    merged_tanks = (save[OFF_TANKS] | tank_bits) & ~withhold
                    if merged_tanks != save[OFF_TANKS]:
                        writes.append((SAVE_BASE + OFF_TANKS, [merged_tanks], "MainRAM"))

                    # Armor parts: idempotent OR into 0x1CA1 (memcard-
                    # persisted). Individual parts do nothing in X5 until a
                    # set completes; the results overlay sets the completion
                    # flags (0x1C4A |= 2/4) at the next results screen, which
                    # unlocks the armor at character select. On the v9+ disc
                    # this can never hide an unchecked capsule: randomized
                    # capsules always spawn (spawn-gate retarget).
                    merged_armor = (save[OFF_ARMOR] | armor_bits) & ~armor_withhold
                    if merged_armor != save[OFF_ARMOR]:
                        writes.append((SAVE_BASE + OFF_ARMOR, [merged_armor], "MainRAM"))

                    # Secret armors: two independent flags, both idempotent.
                    # Black Zero shares 0x1C4A with the Falcon/Gaea
                    # set-completion bits the results overlay owns, so it is
                    # OR-ed in rather than assigned.
                    # Ultimate: grant ONLY from zero. `!= ULTIMATE_ON` was
                    # wrong - the game writes 0x1C4B itself (observed live
                    # 2026-08-06: 01 -> 02 at a results screen, with Ultimate
                    # still selectable afterwards), so this byte is not the
                    # boolean it was taken for. Under the old test every later
                    # item batch would have stomped the game's value back to 1,
                    # and if 0x1C4B is a SELECTION rather than a flag that
                    # silently resets the player's armor choice. Zero is the
                    # only value we know means "no Ultimate", so it is the only
                    # one we overwrite.
                    if want_ultimate and save[OFF_ULTIMATE] == 0:
                        writes.append((SAVE_BASE + OFF_ULTIMATE,
                                       [ULTIMATE_ON], "MainRAM"))
                    if want_black_zero and not (save[OFF_SETFLAGS] & BLACK_ZERO_BIT):
                        writes.append((SAVE_BASE + OFF_SETFLAGS,
                                       [save[OFF_SETFLAGS] | BLACK_ZERO_BIT],
                                       "MainRAM"))

                    if new_hearts:
                        # BOTH characters (design decision 2026-08-01):
                        # vanilla hearts only boost the collector, but an AP
                        # heart item shouldn't shortchange whoever's benched.
                        new_max_x = min(0x40, save[OFF_MAX_HP_X] + HP_PER_HEART * new_hearts)
                        new_max_z = min(0x40, save[OFF_MAX_HP_Z] + HP_PER_HEART * new_hearts)
                        writes.append((SAVE_BASE + OFF_MAX_HP_X, [new_max_x, new_max_z], "MainRAM"))

                    if new_energy:
                        # Filler energy heals via the engine's own queued-
                        # refill counter for the CURRENT character (drained
                        # 1 HP/tick during gameplay, sub-tank style; persists
                        # in the save until drained, so a grant landing at
                        # the hub is delivered at the next stage). value &
                        # 0x7F = pending, bit 7 = active.
                        char = 1 if save[OFF_CHAR] else 0
                        pending = save[OFF_REFILL + char] & 0x7F
                        amount = min(0x7F, pending + SMALL_ENERGY_HEAL * new_energy)
                        writes.append((SAVE_BASE + OFF_REFILL + char,
                                       [amount | 0x80], "MainRAM"))

                    # (Stamping happens at first trusted sight of a fresh
                    # save, up with the unstamped-progress hold - NOT here.
                    # Stamping in the grant batch could land before the first
                    # trusted poll and blind that hold.)

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
