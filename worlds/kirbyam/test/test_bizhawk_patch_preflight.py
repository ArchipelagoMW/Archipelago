"""Tests for KirbyAM Open Patch preflight validation hooks."""

from unittest.mock import Mock, patch

from worlds._bizhawk import context as bizhawk_context


class _KirbyRomFile(str):
    validate_calls: list[str] = []
    browse_result: str | None = None

    @classmethod
    def validate(cls, path: str) -> None:
        cls.validate_calls.append(path)
        if path == "bad.gba":
            raise ValueError("hash mismatch")

    def browse(self):
        return self.__class__.browse_result


class _KirbySettings:
    KirbyAmRomFile = _KirbyRomFile

    def __init__(self, rom_file: str):
        self.rom_file = rom_file


class _RootSettings:
    def __init__(self, rom_file: str):
        self.kirby_am_settings = _KirbySettings(rom_file)
        self._save = Mock()

    def save(self) -> None:
        self._save()


def test_kirby_preflight_noop_for_non_kirby_patch() -> None:
    _KirbyRomFile.validate_calls = []
    root = _RootSettings("bad.gba")

    with patch("worlds._bizhawk.context.settings.get_settings", return_value=root):
        bizhawk_context._ensure_kirbyam_base_rom_valid("test.apz5")

    assert _KirbyRomFile.validate_calls == []
    root._save.assert_not_called()


def test_kirby_preflight_reprompts_and_saves_on_hash_mismatch() -> None:
    _KirbyRomFile.validate_calls = []
    _KirbyRomFile.browse_result = "good.gba"
    root = _RootSettings("bad.gba")

    with patch("worlds._bizhawk.context.settings.get_settings", return_value=root), \
         patch("worlds._bizhawk.context.settings.no_gui", False):
        bizhawk_context._ensure_kirbyam_base_rom_valid("test.apkirbyam")

    assert _KirbyRomFile.validate_calls == ["bad.gba", "good.gba"]
    assert root.kirby_am_settings.rom_file == "good.gba"
    root._save.assert_called_once()
