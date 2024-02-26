import os
import unittest
from tempfile import TemporaryFile

from settings import Settings
import Utils


class TestIDs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with TemporaryFile("w+", encoding="utf-8") as f:
            Settings(None).dump(f)
            f.seek(0, os.SEEK_SET)
            cls.yaml_options = Utils.parse_yaml(f.read())

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
