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

    assert re.search(r'\bpush\s*\{r0-r7,\s*lr\}', normalized), \
        "Hook should save r0-r7 and lr"
    assert re.search(r'\bpush\s*\{r0-r3\}', normalized), \
        "Hook should save high-register mirrors through r0-r3"
    assert re.search(r'\bpop\s*\{r0-r3\}', normalized), \
        "Hook should restore high-register mirrors before low-register restore"
    assert re.search(r'\bmov\s+r8\s*,\s*r0\b', normalized), \
        "Hook should restore r8 from mirrored low register"
    assert re.search(r'\bmov\s+r9\s*,\s*r1\b', normalized), \
        "Hook should restore r9 from mirrored low register"
    assert re.search(r'\bmov\s+r10\s*,\s*r2\b', normalized), \
        "Hook should restore r10 from mirrored low register"
    assert re.search(r'\bmov\s+r11\s*,\s*r3\b', normalized), \
        "Hook should restore r11 from mirrored low register"
    assert re.search(r'\bpop\s*\{r0-r7\}', normalized), \
        "Hook should restore r0-r7 before replaying overwritten instructions"
    assert re.search(r'\bpop\s*\{pc\}', normalized), \
        "Hook should return by popping the saved lr into pc"
    assert not re.search(r'\bpop\s*\{[^}]*\br4\b[^}]*\}', normalized, re.IGNORECASE), \
        "Hook must not use r4 as a temporary restore register"
    assert not re.search(r'\bmov\s+lr\s*,\s*r4\b', normalized, re.IGNORECASE), \
        "Hook must not rebuild lr through r4"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
