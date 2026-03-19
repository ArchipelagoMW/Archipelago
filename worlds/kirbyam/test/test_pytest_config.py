"""Pytest configuration checks for Kirby AM test discovery and async execution."""

from __future__ import annotations


def test_pytest_config_supports_kirbyam_discovery(pytestconfig) -> None:
    """Guard required pytest ini settings used by Kirby AM tests."""
    testpaths = set(pytestconfig.getini("testpaths"))
    assert "worlds" in testpaths
    assert "test" in testpaths
    assert pytestconfig.getini("asyncio_mode") == "auto"
    assert (
        pytestconfig.pluginmanager.hasplugin("pytest_asyncio")
        or pytestconfig.pluginmanager.hasplugin("asyncio")
    )
