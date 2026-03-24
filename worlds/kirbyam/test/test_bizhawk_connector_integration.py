"""Protocol-level integration tests for BizHawk transport and KirbyAM ROM validation."""

from __future__ import annotations

import base64
from types import SimpleNamespace

import pytest

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import AutoBizHawkClientRegister
from worlds.kirbyam.client import (
    EXPECTED_ROM_GAME_CODE,
    EXPECTED_ROM_HEADER_TITLE,
    EXPECTED_ROM_MAKER_CODE,
    KirbyAmClient,
)
from worlds.kirbyam.data import data
from worlds.kirbyam.rom import KirbyAmProcedurePatch

from .support.fake_bizhawk_connector import FakeBizHawkConnector


def _normalize_gba_rom_address(value: int) -> int:
    if 0x08000000 <= value < 0x0A000000:
        return value - 0x08000000
    if 0x0A000000 <= value < 0x0C000000:
        return value - 0x0A000000
    return value


def _seed_kirby_rom_header(connector: FakeBizHawkConnector) -> None:
    connector.set_bytes("ROM", 0xA0, EXPECTED_ROM_HEADER_TITLE.upper().encode("ascii"))
    connector.set_bytes("ROM", 0xAC, EXPECTED_ROM_GAME_CODE.upper().encode("ascii"))
    connector.set_bytes("ROM", 0xB0, EXPECTED_ROM_MAKER_CODE.encode("ascii"))


@pytest.mark.asyncio
async def test_fake_connector_selects_kirby_handler_and_sets_auth(monkeypatch: pytest.MonkeyPatch) -> None:
    auth_addr = data.rom_addresses.get("gArchipelagoInfo")
    assert isinstance(auth_addr, int)
    auth_addr = _normalize_gba_rom_address(auth_addr)
    auth_raw = bytes(range(1, 17))

    connector = FakeBizHawkConnector(system="GBA", rom_hash="issue367-patched")
    _seed_kirby_rom_header(connector)
    connector.set_bytes("ROM", auth_addr, auth_raw)
    await connector.start()

    monkeypatch.setattr(bizhawk, "BIZHAWK_SOCKET_PORT_RANGE_START", connector.port)
    monkeypatch.setattr(bizhawk, "BIZHAWK_SOCKET_PORT_RANGE_SIZE", 1)

    ctx = bizhawk.BizHawkContext()
    try:
        assert await bizhawk.connect(ctx)
        await bizhawk.ping(ctx)
        assert await bizhawk.get_system(ctx) == "GBA"

        client_ctx = SimpleNamespace(bizhawk_ctx=ctx, rom_hash=await bizhawk.get_hash(ctx))
        handler = await AutoBizHawkClientRegister.get_handler(client_ctx, "GBA")

        assert isinstance(handler, KirbyAmClient)
        assert client_ctx.game == "Kirby & The Amazing Mirror"

        await handler.set_auth(client_ctx)
        assert client_ctx.auth == base64.b64encode(auth_raw).decode("ascii")
        assert any(
            req.get("type") == "READ" and req.get("address") == auth_addr and req.get("size") == 16
            for req in connector.request_log
        )
    finally:
        bizhawk.disconnect(ctx)
        await connector.close()


@pytest.mark.asyncio
async def test_fake_connector_rejects_unpatched_base_rom_hash(monkeypatch: pytest.MonkeyPatch) -> None:
    auth_addr = data.rom_addresses.get("gArchipelagoInfo")
    assert isinstance(auth_addr, int)
    auth_addr = _normalize_gba_rom_address(auth_addr)

    connector = FakeBizHawkConnector(system="GBA", rom_hash=KirbyAmProcedurePatch.hash)
    _seed_kirby_rom_header(connector)
    connector.set_bytes("ROM", auth_addr, bytes(range(1, 17)))
    await connector.start()

    monkeypatch.setattr(bizhawk, "BIZHAWK_SOCKET_PORT_RANGE_START", connector.port)
    monkeypatch.setattr(bizhawk, "BIZHAWK_SOCKET_PORT_RANGE_SIZE", 1)

    ctx = bizhawk.BizHawkContext()
    try:
        assert await bizhawk.connect(ctx)
        client_ctx = SimpleNamespace(bizhawk_ctx=ctx, rom_hash=await bizhawk.get_hash(ctx))
        handler = await AutoBizHawkClientRegister.get_handler(client_ctx, "GBA")
        assert handler is None
    finally:
        bizhawk.disconnect(ctx)
        await connector.close()
