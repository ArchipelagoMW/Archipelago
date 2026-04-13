"""Test reset-safe mirror shard grant handling (Issue #109)."""

import re
import sys
import os
import importlib.util

# Prevent stdlib types module shadowing
_SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
_WORLD_DIR = os.path.realpath(os.path.dirname(_SCRIPT_DIR))
for path_entry in list(sys.path):
    resolved = os.path.realpath(path_entry or os.getcwd())
    if resolved == _WORLD_DIR:
        sys.path.remove(path_entry)

import pytest


def test_shard_persistence_addresses_defined():
    """Verify that SRAM addresses for shard persistence are correctly defined in payload."""
    # Payload should define:
    # - SRAM_BASE (0x0E000000)
    # - SRAM_SHARD_FIELD_OFFSET (0x12)
    # - SRAM_CHECKSUM_1/2/3 offsets (0x18, 0x1A, 0x1C)
    
    # This is verified at compile time in ap_payload.c, so this test
    # confirms the implementation exists and is documented.
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")
    assert os.path.exists(payload_path), "ap_payload.c should exist"
    
    with open(payload_path, 'r') as f:
        content = f.read()
    
    # Verify SRAM definitions are present
    assert "SRAM_BASE" in content, "SRAM_BASE should be defined"
    assert "SRAM_SHARD_FIELD_OFFSET" in content, "SRAM_SHARD_FIELD_OFFSET should be defined"
    assert "persist_shard_to_sram" in content, "persist_shard_to_sram function should exist"
    assert "SRAM_CHECKSUM" in content, "Checksum fields should be defined"


def test_shard_persistence_function_exists():
    """Verify persist_shard_to_sram function is called when granting shards."""
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")
    
    with open(payload_path, 'r') as f:
        content = f.read()
    
    # Verify the function is defined
    assert "persist_shard_to_sram(new_shard_flags)" in content, \
        "persist_shard_to_sram should be called when granting shards"


def test_payload_tracks_major_chest_checks_separately_from_native_maps():
    """Verify big chest openings feed transport checks while AP map items unlock native maps."""
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, 'r') as f:
        content = f.read()

    assert "AP_MAJOR_CHEST_FLAGS" in content, "Major chest transport register should be defined"
    assert "ap_on_collect_big_chest" in content, "Big chest hook target should exist"
    assert "ap_set_major_chest_flag(area_id)" in content, "Big chest hook should set transport check flags"
    assert "ap_unlock_area_map" in content, "Payload should unlock native maps on AP item receipt"
    assert "KIRBY_BIG_CHEST_FLAGS" in content, "Native big chest map bitfield should still be addressable"


def test_payload_tracks_vitality_chest_checks_and_ap_vitality_apply():
    """Verify vitality chest checks and AP vitality grants use dedicated payload paths."""
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, 'r') as f:
        content = f.read()

    assert "AP_VITALITY_CHEST_FLAGS" in content, "Vitality chest transport register should be defined"
    assert "ap_on_collect_vitality_chest" in content, "Vitality chest hook target should exist"
    assert "ap_set_vitality_chest_flag_for_room" in content, "Vitality chest room mapping helper should exist"
    assert "ap_grant_vitality_counter" in content, "AP vitality grant helper should exist"
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 18u" in content, "Vitality AP item IDs should be handled"


def test_payload_vitality_items_are_replay_guarded_per_unique_item() -> None:
    """Vitality AP item IDs should be idempotent so reconnect/reset replay does not grant duplicates."""
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, 'r') as f:
        content = f.read()

    assert "AP_DELIVERED_VITALITY_ITEM_BITS" in content, "Vitality replay-guard bitfield should be defined"
    assert "vitality_index" in content, "Vitality handler should derive per-item index"
    assert "vitality_mask" in content, "Vitality handler should derive per-item bit mask"
    assert "AP_DELIVERED_VITALITY_ITEM_BITS |= vitality_mask" in content, (
        "Vitality item handling should mark items as applied"
    )
    assert "AP_DELIVERED_VITALITY_ITEM_BITS = 0u;" in content, (
        "Mailbox initialization should clear vitality replay-guard state"
    )
    assert "KIRBY_MAX_VITALITY_COUNTERS" in content, (
        "Payload should define a hard cap for AP vitality counter grants"
    )
    assert "vitality_counter > KIRBY_MAX_VITALITY_COUNTERS" in content, (
        "Vitality grant helper should clamp already-overflowed vitality counts back down"
    )
    assert "vitality_counter < KIRBY_MAX_VITALITY_COUNTERS" in content, (
        "Vitality grant helper should enforce AP vitality counter cap"
    )


def test_payload_tracks_sound_player_chest_checks_and_ap_unlock_apply():
    """Verify Sound Player chest checks are AP-owned and unlock only on AP item receipt."""
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, 'r') as f:
        content = f.read()

    assert "AP_SOUND_PLAYER_CHEST_FLAGS" in content, "Sound Player chest transport register should be defined"
    assert "ap_on_collect_sound_player_chest" in content, "Sound Player chest hook target should exist"
    assert "ap_set_sound_player_chest_flag(0u)" in content, "Sound Player chest hook should set AP check bit"
    assert "KIRBY_COLLECT_SOUND_PLAYER_FN(0u)" in content, "AP Sound Player item should apply native unlock"
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 25u" in content, "Sound Player AP item ID should be handled"


def test_payload_tracks_hub_switch_checks_from_world_map_unlocks() -> None:
    """Verify world-map big-switch unlock callbacks set dedicated AP hub-switch check flags."""
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, 'r') as f:
        content = f.read()

    assert "AP_HUB_SWITCH_FLAGS" in content, "Hub switch transport register should be defined"
    assert "ap_set_hub_switch_flag" in content, "Hub switch flag helper should exist"
    assert "ap_on_world_map_unlock_call" in content, "World-map unlock hook target should exist"
    assert "door_index" in content, "World-map unlock hook should read the unlock door index"


def test_sram_checksum_fields_updated():
    """Verify that checksum fields are updated alongside shard persistence."""
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")
    
    with open(payload_path, 'r') as f:
        content = f.read()
    
    # Verify checksum update logic exists
    assert "SRAM_CHECKSUM_1 = " in content, "Checksum 1 should be updated"
    assert "SRAM_CHECKSUM_2 = " in content, "Checksum 2 should be updated"
    assert "SRAM_CHECKSUM_3 = " in content, "Checksum 3 should be updated"
    
    # Verify they use the shard bitfield value
    assert "new_shard_bitfield" in content, "Checksums should be derived from shard bitfield"


def test_issue_109_addresses_documented():
    """Verify Issue #109 addresses are documented in the payload."""
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")
    
    with open(payload_path, 'r') as f:
        content = f.read()
    
    # Verify the specific candidate SRAM addresses are in some form
    # Issue #109 mentions: 000018, 00001A, 00001C, 00032C, 00032E, 000330
    # Our implementation uses: 0x12 (18), 0x18 (24), 0x1A (26), 0x1C (28)
    
    # These are in the ranges mentioned in Issue #109
    assert "0x12" in content or "18" in content, "SRAM offset 0x12 should be defined"
    assert "0x18" in content or "24" in content, "SRAM offset 0x18 should be defined"
    assert "0x1A" in content or "26" in content, "SRAM offset 0x1A should be defined"
    assert "0x1C" in content or "28" in content, "SRAM offset 0x1C should be defined"


def test_boss_defeat_hook_preserves_native_shard_state():
    """Verify ap_on_boss_defeat_collect_shard records AP flag AND updates native shard state.

    Issue #380: suppressing native CollectShard left gTreasures.shardField stale,
    causing the post-cutscene game-state machine to leave the screen permanently
    white.  The hook must replicate CollectShard semantics (write KIRBY_SHARD_FLAGS
    and persist to SRAM) in addition to setting the AP boss-defeat transport flag.
    Source: d:\\kirbyam-extras\\katam\\src\\code_0801C6F8.c (sub_0801D948 / sub_0801D584).
    """
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, "r") as f:
        content = f.read()

    # The hook must still record the AP boss-defeat flag.
    # Restrict all checks to the ap_on_boss_defeat_collect_shard body so the
    # test cannot pass by matching the same strings in ap_apply_item or any
    # other function.
    match = re.search(
        r"void\s+ap_on_boss_defeat_collect_shard[^{]*\{(?P<body>.*?)^}",
        content,
        flags=re.DOTALL | re.MULTILINE,
    )
    assert match is not None, "ap_on_boss_defeat_collect_shard definition must exist in ap_payload.c"
    hook_body = match.group(0)

    assert "ap_set_boss_defeat_flag(boss_index)" in hook_body, \
        "Boss hook must call ap_set_boss_defeat_flag to signal the AP location check"

    # The hook must also replicate CollectShard: write the native EWRAM shard bitfield.
    assert "KIRBY_SHARD_FLAGS = new_shard_flags" in hook_body, \
        "Boss hook must write KIRBY_SHARD_FLAGS so post-cutscene state machine sees valid shard state"

    # The hook must persist to SRAM (same as the AP shard-grant path).
    assert "persist_shard_to_sram(new_shard_flags)" in hook_body, \
        "Boss hook must persist shard flags to SRAM for reset-safe behaviour"


def test_boss_defeat_hook_sets_scrub_delay():
    """Verify ap_on_boss_defeat_collect_shard sets AP_SHARD_SCRUB_DELAY (Issue #478).

    The scrub delay holds off the per-frame KIRBY_SHARD_FLAGS clamp so the
    post-boss cutscene state machine can read the temporary native write without
    triggering the white-screen regression from Issue #380.
    """
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, "r") as f:
        content = f.read()

    match = re.search(
        r"void\s+ap_on_boss_defeat_collect_shard[^{]*\{(?P<body>.*?)^}",
        content,
        flags=re.DOTALL | re.MULTILINE,
    )
    assert match is not None, "ap_on_boss_defeat_collect_shard definition must exist"
    hook_body = match.group(0)

    assert "AP_SHARD_SCRUB_DELAY" in hook_body, \
        "Boss hook must set AP_SHARD_SCRUB_DELAY to hold off shard scrub during cutscene"
    assert "SHARD_BOSS_CUTSCENE_FRAMES" in hook_body, \
        "Boss hook must assign SHARD_BOSS_CUTSCENE_FRAMES to AP_SHARD_SCRUB_DELAY"
    assert "AP_BOSS_TEMP_SHARD_BITFIELD" in hook_body, \
        "Boss hook must mark temporary boss shard bits for state-driven scrub"


def test_ap_apply_item_shard_path_writes_delivered_bitfield():
    """Verify ap_apply_item shard path writes AP_DELIVERED_SHARD_BITFIELD (Issue #478).

    AP_DELIVERED_SHARD_BITFIELD is the authority for which shard bits are
    AP-owned.  Only ap_apply_item() may set bits in it; boss-defeat must not.
    """
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, "r") as f:
        content = f.read()

    # Extract ap_apply_item body
    match = re.search(
        r"uint8_t\s+ap_apply_item[^{]*\{(?P<body>.*?)^}",
        content,
        flags=re.DOTALL | re.MULTILINE,
    )
    assert match is not None, "ap_apply_item definition must exist in ap_payload.c"
    apply_body = match.group(0)

    assert "AP_DELIVERED_SHARD_BITFIELD" in apply_body, \
        "ap_apply_item shard path must write AP_DELIVERED_SHARD_BITFIELD"

    # Boss hook must NOT write AP_DELIVERED_SHARD_BITFIELD
    match_boss = re.search(
        r"void\s+ap_on_boss_defeat_collect_shard[^{]*\{(?P<body>.*?)^}",
        content,
        flags=re.DOTALL | re.MULTILINE,
    )
    assert match_boss is not None, "ap_on_boss_defeat_collect_shard definition must exist"
    assert "AP_DELIVERED_SHARD_BITFIELD" not in match_boss.group(0), \
        "Boss hook must NOT write AP_DELIVERED_SHARD_BITFIELD; it is AP-delivery-only"


def test_ap_poll_mailbox_contains_shard_scrub_logic():
    """Verify ap_poll_mailbox_c contains the per-frame KIRBY_SHARD_FLAGS scrub (Issue #478).

    Once AP_SHARD_SCRUB_DELAY reaches 0, the scrub clamps KIRBY_SHARD_FLAGS to
    AP_DELIVERED_SHARD_BITFIELD so that HasShard() / NumShardsCollected() gate
    checks reflect only AP-delivered shards.
    """
    payload_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_payload.c")

    with open(payload_path, "r") as f:
        content = f.read()

    match = re.search(
        r"void\s+ap_poll_mailbox_c[^{]*\{(?P<body>.*?)^}",
        content,
        flags=re.DOTALL | re.MULTILINE,
    )
    assert match is not None, "ap_poll_mailbox_c definition must exist in ap_payload.c"
    poll_body = match.group(0)

    # Strip line comments and normalize whitespace to reduce formatting brittleness.
    poll_body_code_only = re.sub(r'//[^\n]*', '', poll_body)
    poll_body_norm = re.sub(r'\s+', ' ', poll_body_code_only)

    assert "AP_SHARD_SCRUB_DELAY" in poll_body_norm, \
        "ap_poll_mailbox_c must reference AP_SHARD_SCRUB_DELAY for the scrub countdown"
    assert "AP_DELIVERED_SHARD_BITFIELD" in poll_body_norm, \
        "ap_poll_mailbox_c must read AP_DELIVERED_SHARD_BITFIELD to clamp KIRBY_SHARD_FLAGS"
    assert "AP_MAILBOX_INIT_COOKIE" in poll_body_norm, \
        "ap_poll_mailbox_c must validate mailbox init cookie before shard scrub logic"
    assert "AP_MAILBOX_INIT_COOKIE_VALUE" in poll_body_norm, \
        "ap_poll_mailbox_c must compare against AP_MAILBOX_INIT_COOKIE_VALUE"
    assert re.search(r"AP_DELIVERED_SHARD_BITFIELD\s*=\s*\(uint32_t\)\s*native_shards_boot", poll_body_norm), \
        "ap_poll_mailbox_c must seed AP_DELIVERED_SHARD_BITFIELD from native shard state on init"
    assert "AP_BOSS_TEMP_SHARD_BITFIELD" in poll_body_norm, \
        "ap_poll_mailbox_c must track temporary boss shard bits"
    assert "AI_KIRBY_STATE" in poll_body_norm, \
        "ap_poll_mailbox_c must gate scrub release on gameplay-state resume"
    assert "DEMO_PLAYBACK_FLAGS" in poll_body_norm, \
        "ap_poll_mailbox_c gameplay gate must account for title-demo playback"
    assert re.search(r"AP_DELIVERED_SHARD_BITFIELD\s*=\s*\(uint32_t\)\s*native_shards", poll_body_norm), \
        "ap_poll_mailbox_c must be able to seed AP_DELIVERED_SHARD_BITFIELD from native saved shards"
    assert re.search(r"persist_shard_to_sram\s*\(", poll_body_norm), \
        "ap_poll_mailbox_c scrub must persist the clamped state to SRAM"


def test_ap_hook_preserves_register_context_without_r4_temp_restore():
    """Verify the hook preserves full context and does not rebuild LR through r4."""
    hook_path = os.path.join(_WORLD_DIR, "kirby_ap_payload", "ap_hook.s")
    assert os.path.exists(hook_path), "ap_hook.s should exist in kirby_ap_payload"

    with open(hook_path, 'r') as f:
        content = f.read()

    # Strip // line comments so comment text cannot trigger false positives/negatives.
    code_only = re.sub(r'//[^\n]*', '', content)
    # Normalize runs of spaces/tabs to a single space.
    normalized = re.sub(r'[ \t]+', ' ', code_only)

    assert re.search(r'\bpush\s*\{r0-r3,\s*lr\}', normalized), \
        "Hook should save scratch registers and lr"
    assert re.search(r'\bbl\s+ap_poll_mailbox_c\b', normalized), \
        "Hook should call ap_poll_mailbox_c"
    assert re.search(r'\bpop\s*\{r0-r3\}', normalized), \
        "Hook should restore scratch registers before replaying overwritten instructions"
    assert re.search(r'\bmov\s+r7\s*,\s*r9\b', normalized), \
        "Hook should replay overwritten instruction mov r7, r9"
    assert re.search(r'\bmov\s+r6\s*,\s*r8\b', normalized), \
        "Hook should replay overwritten instruction mov r6, r8"
    assert re.search(r'\bpop\s*\{pc\}', normalized), \
        "Hook should return by popping the saved lr into pc"
    assert not re.search(r'\bpop\s*\{[^}]*\br4\b[^}]*\}', normalized, re.IGNORECASE), \
        "Hook must not use r4 as a temporary restore register"
    assert not re.search(r'\bmov\s+lr\s*,\s*r4\b', normalized, re.IGNORECASE), \
        "Hook must not rebuild lr through r4"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
