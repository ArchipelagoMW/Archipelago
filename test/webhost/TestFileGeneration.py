"""Tests for successful generation of WebHost cached files. Can catch some other deeper errors."""

import os
import unittest

import WebHost


class TestFileGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.correct_path = os.path.join(os.path.dirname(WebHost.__file__), "WebHostLib")
        # should not create the folder *here*
        cls.incorrect_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], "WebHostLib")

    def testOptions(self):
        WebHost.create_options_files()
        target = os.path.join(self.correct_path, "static", "generated", "configs")
        self.assertTrue(os.path.exists(target))
        self.assertFalse(os.path.exists(os.path.join(self.incorrect_path, "static", "generated", "configs")))

        # folder seems fine, so now we try to generate Options based on the default file
        from WebHostLib.check import roll_options
        file: os.DirEntry
        for file in os.scandir(target):
            if file.is_file() and file.name.endswith(".yaml"):
                with self.subTest(file=file.name):
                    with open(file) as f:
                        for value in roll_options({file.name: f.read()})[0].values():
                            self.assertTrue(value is True, f"Default Options for template {file.name} cannot be run.")

    def testTutorial(self):
        WebHost.create_ordered_tutorials_file()
        self.assertTrue(os.path.exists(os.path.join(self.correct_path, "static", "generated", "tutorials.json")))
        self.assertFalse(os.path.exists(os.path.join(self.incorrect_path, "static", "generated", "tutorials.json")))
