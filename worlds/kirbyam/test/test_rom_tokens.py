"""Tests for KirbyAM ROM token generation behavior."""

from __future__ import annotations

import random
from types import SimpleNamespace

import pytest
import worlds.kirbyam.rom as rom_module

from worlds.Files import APTokenTypes

from ..ability_randomization import build_enemy_copy_ability_policy
from ..options import AbilityRandomizationMode
from ..rom import write_tokens


class _DummyPatch:
    def __init__(self) -> None:
        self.token_writes: list[tuple[int, int, bytes]] = []
        self.files: dict[str, bytes] = {}

    def write_token(self, token_type: int, address: int, payload: bytes) -> None:
        self.token_writes.append((token_type, address, payload))

    def get_token_binary(self) -> bytes:
        return b"dummy-token-binary"

    def write_file(self, name: str, data: bytes) -> None:
        self.files[name] = data


def _make_world(mode: int) -> SimpleNamespace:
    return SimpleNamespace(
        auth=b"0123456789ABCDEF",
        options=SimpleNamespace(
            ability_randomization_mode=SimpleNamespace(value=mode)
        ),
    )


def test_write_tokens_rejects_missing_policy_for_non_vanilla_mode() -> None:
    world = _make_world(AbilityRandomizationMode.option_shuffled)
    patch = _DummyPatch()

    with pytest.raises(ValueError, match="enemy_copy_ability_policy must be initialized"):
        write_tokens(world, patch)


def test_write_tokens_emits_runtime_enemy_writes_for_non_vanilla_mode() -> None:
    world = _make_world(AbilityRandomizationMode.option_shuffled)
    world._enemy_copy_ability_policy = build_enemy_copy_ability_policy(
        random.Random(20260324),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
    )

    patch = _DummyPatch()
    write_tokens(world, patch)

    # Auth token write + many single-byte ability remap writes.
    single_byte_writes = [
        w for w in patch.token_writes
        if w[0] == APTokenTypes.WRITE and len(w[2]) == 1
    ]
    assert single_byte_writes
    assert "token_data.bin" in patch.files


def test_write_tokens_allows_non_vanilla_mode_with_no_runtime_writes(monkeypatch) -> None:
    world = _make_world(AbilityRandomizationMode.option_shuffled)
    world._enemy_copy_ability_policy = build_enemy_copy_ability_policy(
        random.Random(20260324),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
    )
    monkeypatch.setattr(rom_module, "build_enemy_copy_runtime_patch_writes", lambda policy: {})

    patch = _DummyPatch()
    write_tokens(world, patch)

    single_byte_writes = [
        w for w in patch.token_writes
        if w[0] == APTokenTypes.WRITE and len(w[2]) == 1
    ]
    assert not single_byte_writes
    assert "token_data.bin" in patch.files
