import os
import os.path
import unittest
from io import StringIO
from tempfile import TemporaryDirectory, TemporaryFile
from typing import Any, Dict, List, cast

import Utils
from settings import Group, Settings, ServerOptions


class TestIDs(unittest.TestCase):
    yaml_options: Dict[Any, Any]

    @classmethod
    def setUpClass(cls) -> None:
        with TemporaryFile("w+", encoding="utf-8") as f:
            Settings(None).dump(f)
            f.seek(0, os.SEEK_SET)
            yaml_options = Utils.parse_yaml(f.read())
            assert isinstance(yaml_options, dict)
            cls.yaml_options = yaml_options

    def test_utils_in_yaml(self) -> None:
        """Tests that the auto generated host.yaml has default settings in it"""
        for option_key, option_set in Settings(None).items():
            with self.subTest(option_key):
                self.assertIn(option_key, self.yaml_options)
                for sub_option_key in option_set:
                    self.assertIn(sub_option_key, self.yaml_options[option_key])

    def test_yaml_in_utils(self) -> None:
        """Tests that the auto generated host.yaml shows up in reference calls"""
        utils_options = Settings(None)
        for option_key, option_set in self.yaml_options.items():
            with self.subTest(option_key):
                self.assertIn(option_key, utils_options)
                for sub_option_key in option_set:
                    self.assertIn(sub_option_key, utils_options[option_key])


class TestSettingsDumper(unittest.TestCase):
    def test_string_format(self) -> None:
        """Test that dumping a string will yield the expected output"""
        # By default, pyyaml has automatic line breaks in strings and quoting is optional.
        # What we want for consistency instead is single-line strings and always quote them.
        # Line breaks have to become \n in that quoting style.
        class AGroup(Group):
            key: str = " ".join(["x"] * 60) + "\n"  # more than 120 chars, contains spaces and a line break

        with StringIO() as writer:
            AGroup().dump(writer, 0)
            expected_value = AGroup.key.replace("\n", "\\n")
            self.assertEqual(writer.getvalue(), f"key: \"{expected_value}\"\n",
                             "dumped string has unexpected formatting")

    def test_indentation(self) -> None:
        """Test that dumping items will add indentation"""
        # NOTE: we don't care how many spaces there are, but it has to be a multiple of level
        class AList(List[Any]):
            __doc__ = None  # make sure we get no doc string

        class AGroup(Group):
            key: AList = cast(AList, ["a", "b", [1]])

        for level in range(3):
            with StringIO() as writer:
                AGroup().dump(writer, level)
                lines = writer.getvalue().split("\n", 5)
                key_line = lines[0]
                key_spaces = len(key_line) - len(key_line.lstrip(" "))
                value_lines = lines[1:-1]
                value_spaces = [len(value_line) - len(value_line.lstrip(" ")) for value_line in value_lines]
                if level == 0:
                    self.assertEqual(key_spaces, 0)
                else:
                    self.assertGreaterEqual(key_spaces, level)
                    self.assertEqual(key_spaces % level, 0)
                self.assertGreaterEqual(value_spaces[0], key_spaces)  # a
                self.assertEqual(value_spaces[1], value_spaces[0])  # b
                self.assertEqual(value_spaces[2], value_spaces[0])  # start of sub-list
                self.assertGreater(value_spaces[3], value_spaces[0],
                                   f"{value_lines[3]} should have more indentation than {value_lines[0]} in {lines}")


class TestSettingsSave(unittest.TestCase):
    def test_save(self) -> None:
        """Test that saving and updating works"""
        with TemporaryDirectory() as d:
            filename = os.path.join(d, "host.yaml")
            new_release_mode = ServerOptions.ReleaseMode("enabled")
            # create default host.yaml
            settings = Settings(None)
            settings.save(filename)
            self.assertTrue(os.path.exists(filename),
                            "Default settings could not be saved")
            self.assertNotEqual(settings.server_options.release_mode, new_release_mode,
                                "Unexpected default release mode")
            # update host.yaml
            settings.server_options.release_mode = new_release_mode
            settings.save(filename)
            self.assertFalse(os.path.exists(filename + ".tmp"),
                             "Temp file was not removed during save")
            # read back host.yaml
            settings = Settings(filename)
            self.assertEqual(settings.server_options.release_mode, new_release_mode,
                             "Settings were not overwritten")
