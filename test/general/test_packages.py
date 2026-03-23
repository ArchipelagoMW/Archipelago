import unittest
import os


class TestPackages(unittest.TestCase):
    def test_packages_have_init(self):
        """Test that all world folders containing .py files also have a __init__.py file,
        to indicate full package rather than namespace package."""
        import Utils

        # Ignore directories with these names.
        ignore_dirs = {".github"}

        worlds_path = Utils.local_path("worlds")
        for dirpath, dirnames, filenames in os.walk(worlds_path):
            # Drop ignored directories from dirnames, excluding them from walking.
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            with self.subTest(directory=dirpath):
                self.assertEqual("__init__.py" in filenames, any(file.endswith(".py") for file in filenames))
