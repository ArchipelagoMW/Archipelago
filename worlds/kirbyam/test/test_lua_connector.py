"""Regression tests for the KirbyAM BizHawk Lua connector entrypoint."""

from pathlib import Path


CONNECTOR_PATH = Path(__file__).resolve().parents[3] / "data" / "lua" / "connector_kirbyam_bizhawk.lua"


def test_kirbyam_lua_connector_exists() -> None:
    assert CONNECTOR_PATH.exists()


def test_kirbyam_lua_connector_delegates_to_generic_transport() -> None:
    content = CONNECTOR_PATH.read_text(encoding="utf-8")

    assert "connector_bizhawk_generic.lua" in content
    assert "Expected GBA system" in content
    assert "ROM validation OK" in content
    assert "TODO(issue 51)" in content