from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from unittest import TestLoader, TestSuite


def load_tests(loader: "TestLoader", standard_tests: "TestSuite", pattern: str):
    import os
    import unittest
    import fnmatch
    from .. import file_path
    from worlds.AutoWorld import AutoWorldRegister

    suite = unittest.TestSuite()
    suite.addTests(standard_tests)

    # pattern hack
    # all tests from within __init__ are always imported, so we need to filter out the folder earlier
    # if the pattern isn't matching a specific world, we don't have much of a solution

    if pattern.startswith("worlds."):
        if pattern.endswith(".py"):
            pattern = pattern[:-3]
        components = pattern.split(".")
        world_glob = f"worlds.{components[1]}"
        pattern = components[-1]

    elif pattern.startswith(f"worlds{os.path.sep}") or pattern.startswith(f"worlds{os.path.altsep}"):
        components = pattern.split(os.path.sep)
        if len(components) == 1:
            components = pattern.split(os.path.altsep)
        world_glob = f"worlds.{components[1]}"
        pattern = components[-1]
    else:
        world_glob = "*"


    folders = [os.path.join(os.path.split(world.__file__)[0], "test")
               for world in AutoWorldRegister.world_types.values()
               if fnmatch.fnmatch(world.__module__, world_glob)]

    all_tests = [
        test_case for folder in folders if os.path.exists(folder)
        for test_collection in loader.discover(folder, top_level_dir=file_path, pattern=pattern)
        for test_suite in test_collection if isinstance(test_suite, unittest.suite.TestSuite)
        for test_case in test_suite
    ]

    suite.addTests(sorted(all_tests, key=lambda test: test.__module__))
    return suite
