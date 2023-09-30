def load_tests(loader, standard_tests, pattern):
    import os
    import unittest
    import Utils
    import typing
    import zipfile
    import importlib
    import inspect

    from worlds.AutoWorld import AutoWorldRegister

    suite = unittest.TestSuite()
    suite.addTests(standard_tests)
    folders = [(os.path.join(os.path.split(world.__file__)[0], "test"), world.zip_path)
               for world in AutoWorldRegister.world_types.values()]

    all_tests: typing.List[unittest.TestCase] = [
    ]

    for folder, zip_path in folders:
        if os.path.exists(folder) and not zip_path:
            all_tests.extend(
                test_case
                for test_collection in loader.discover(folder, top_level_dir=Utils.local_path("."))
                for test_suite in test_collection
                for test_case in test_suite
            )
        elif zip_path and os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path) as zf:
                for zip_info in zf.infolist():
                    if "__pycache__" in zip_info.filename:
                        continue
                    if "test" in zip_info.filename and zip_info.filename.endswith((".py", ".pyc", ".pyo")):
                        import_path = "worlds." + os.path.splitext(zip_info.filename)[0].replace("/", ".")
                        module = importlib.import_module(import_path)
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, unittest.TestCase):
                                all_tests.extend(obj(method_name) for method_name in loader.getTestCaseNames(obj))

    assert all_tests, "No custom tests found, when it was expected to find them."
    suite.addTests(sorted(all_tests, key=lambda test: test.__module__))
    return suite
