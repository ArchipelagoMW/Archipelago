import unittest
import os


class TestBase(unittest.TestCase):
    def test_requirements_file_ends_on_newline(self):
        """Test that all requirements files end on a newline"""
        import Utils
        requirements_files = [Utils.local_path("requirements.txt"),
                              Utils.local_path("WebHostLib", "requirements.txt")]
        worlds_path = Utils.local_path("worlds")
        for entry in os.listdir(worlds_path):
            requirements_path = os.path.join(worlds_path, entry, "requirements.txt")
            if os.path.isfile(requirements_path):
                requirements_files.append(requirements_path)
        for requirements_file in requirements_files:
            with self.subTest(path=requirements_file):
                with open(requirements_file) as f:
                    self.assertEqual(f.read()[-1], "\n")
