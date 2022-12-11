def load_tests(loader, standard_tests, pattern):
    import os
    import unittest
    from ..TestBase import file_path
    from worlds.AutoWorld import AutoWorldRegister

    suite = unittest.TestSuite()
    suite.addTests(standard_tests)
    folders = [os.path.join(os.path.split(world.__file__)[0], "test")
               for world in AutoWorldRegister.world_types.values()]
    for folder in folders:
        if os.path.exists(folder):
            suite.addTests(loader.discover(folder, top_level_dir=file_path))
    return suite
