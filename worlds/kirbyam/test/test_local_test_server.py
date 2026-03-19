"""Tests for KirbyAM local test server bootstrap helpers."""

from pathlib import Path

from .server.start_test_server import _find_latest_archive


def test_find_latest_archive_selects_newest_zip(tmp_path: Path) -> None:
    older = tmp_path / "older.archipelago"
    newest = tmp_path / "newest.zip"
    older.write_bytes(b"old")
    newest.write_bytes(b"new")

    assert _find_latest_archive(tmp_path) == newest


def test_find_latest_archive_raises_when_missing(tmp_path: Path) -> None:
    try:
        _find_latest_archive(tmp_path)
        raise AssertionError("Expected FileNotFoundError")
    except FileNotFoundError:
        pass
