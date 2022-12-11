# Tests for Generate.py (ArchipelagoGenerate.exe)

import unittest
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import os.path
import os
import ModuleUpdate
ModuleUpdate.update_ran = True  # don't upgrade
import Generate


class TestGenerateMain(unittest.TestCase):
    """This tests Generate.py (ArchipelagoGenerate.exe) main"""

    generate_dir = Path(Generate.__file__).parent
    run_dir = generate_dir / "test"  # reproducible cwd that's neither __file__ nor Generate.__file__
    abs_input_dir = Path(__file__).parent / 'data' / 'OnePlayer'
    rel_input_dir = abs_input_dir.relative_to(run_dir)  # directly supplied relative paths are relative to cwd
    yaml_input_dir = abs_input_dir.relative_to(generate_dir)  # yaml paths are relative to user_path

    def assertOutput(self, output_dir: str):
        output_path = Path(output_dir)
        output_files = list(output_path.glob('*.zip'))
        if len(output_files) == 1:
            return True
        self.fail(f"Expected {output_dir} to contain one zip, but has {len(output_files)}: "
                  f"{list(output_path.glob('*'))}")

    def setUp(self):
        self.original_argv = sys.argv.copy()
        self.original_cwd = os.getcwd()
        self.original_local_path = Generate.Utils.local_path.cached_path
        self.original_user_path = Generate.Utils.user_path.cached_path

        # Force both user_path and local_path to a specific path. They have independent caches.
        Generate.Utils.user_path.cached_path = Generate.Utils.local_path.cached_path = str(self.generate_dir)
        os.chdir(self.run_dir)
        self.output_tempdir = TemporaryDirectory(prefix='AP_out_')

    def tearDown(self):
        self.output_tempdir.cleanup()
        os.chdir(self.original_cwd)
        sys.argv = self.original_argv
        Generate.Utils.local_path.cached_path = self.original_local_path
        Generate.Utils.user_path.cached_path = self.original_user_path

    def test_paths(self):
        self.assertTrue(os.path.exists(self.generate_dir))
        self.assertTrue(os.path.exists(self.run_dir))
        self.assertTrue(os.path.exists(self.abs_input_dir))
        self.assertTrue(os.path.exists(self.rel_input_dir))
        self.assertFalse(os.path.exists(self.yaml_input_dir))  # relative to user_path, not cwd

    def test_generate_absolute(self):
        sys.argv = [sys.argv[0], '--seed', '0',
                    '--player_files_path', str(self.abs_input_dir),
                    '--outputpath', self.output_tempdir.name]
        print(f'Testing Generate.py {sys.argv} in {os.getcwd()}')
        Generate.main()

        self.assertOutput(self.output_tempdir.name)

    def test_generate_relative(self):
        sys.argv = [sys.argv[0], '--seed', '0',
                    '--player_files_path', str(self.rel_input_dir),
                    '--outputpath', self.output_tempdir.name]
        print(f'Testing Generate.py {sys.argv} in {os.getcwd()}')
        Generate.main()

        self.assertOutput(self.output_tempdir.name)

    def test_generate_yaml(self):
        # override host.yaml
        defaults = Generate.Utils.get_options()["generator"]
        defaults["player_files_path"] = str(self.yaml_input_dir)
        defaults["players"] = 0

        sys.argv = [sys.argv[0], '--seed', '0',
                    '--outputpath', self.output_tempdir.name]
        print(f'Testing Generate.py {sys.argv} in {os.getcwd()}, player_files_path={self.yaml_input_dir}')
        Generate.main()

        self.assertOutput(self.output_tempdir.name)
