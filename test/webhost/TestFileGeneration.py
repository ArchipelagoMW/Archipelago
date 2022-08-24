"""Tests for successful generation of WebHost cached files. Can catch some other deeper errors."""

import os
import unittest

import WebHost


class TestFileGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.correct_path = os.path.join(os.path.dirname(WebHost.__file__), "WebHostLib")
        # should not create the folder *here*
        self.incorrect_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], "WebHostLib")

    def testOptions(self):
        WebHost.create_options_files()
        self.assertTrue(os.path.exists(os.path.join(self.correct_path, "static", "generated", "configs")))
        self.assertFalse(os.path.exists(os.path.join(self.incorrect_path, "static", "generated", "configs")))

    def testTutorial(self):
        WebHost.create_ordered_tutorials_file()
        self.assertTrue(os.path.exists(os.path.join(self.correct_path, "static", "generated", "tutorials.json")))
        self.assertFalse(os.path.exists(os.path.join(self.incorrect_path, "static", "generated", "tutorials.json")))
