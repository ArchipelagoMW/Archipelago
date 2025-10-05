# Tests for build_apworld.py

import importlib
import os
import shutil
import sys
import textwrap
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, AnyStr, ClassVar, Final, Self, Type

import orjson

import Launcher
import build_apworld
from general import TestWorld
from worlds import AutoWorldRegister
from worlds.AutoWorld import World

INIT_CONTENTS: Final[str] = f"from .world import {TestWorld.__name__}"
MANIFEST_CONTENTS: Final[str] = textwrap.dedent(f"""\
	{{
		"game": "{TestWorld.game}"
	}}
""")

LAUNCHER_COMPONENT: Final[str] = "Build APWorlds"


class TestBuildApworld(unittest.TestCase):
	output_tempdir: ClassVar[TemporaryDirectory]
	test_world_cache: ClassVar[dict[Path, type[World]]] = {}

	@classmethod
	def setUpClass(cls: Type[Self]) -> None:
		cls.output_tempdir = TemporaryDirectory(prefix=".AP_out_")
		sys.path.insert(0, cls.output_tempdir.name)

		# Unregister TestWorld imported from this class file
		# Necessary so that build_apworld gets correct paths
		AutoWorldRegister.world_types.pop(TestWorld.game)

	@classmethod
	def tearDownClass(cls: Type[Self]) -> None:
		cls.output_tempdir.cleanup()
		sys.path.remove(cls.output_tempdir.name)

	def tearDown(self: Self) -> None:
		for apworld in Path(self.output_tempdir.name).glob("*.apworld"):
			os.remove(apworld)

		test_world = AutoWorldRegister.world_types.pop(TestWorld.game, None)

		# Re-import will not re-add this World instance to AutoWorldRegister,
		# so keep it in case we need it later
		if test_world:
			self.test_world_cache[Path(test_world.__file__).parent] = test_world

	@classmethod
	def create_apworld_dir(cls: Type[Self], dir_name: AnyStr = "test_world") -> Path:
		apworld_dir = Path(cls.output_tempdir.name, dir_name)

		if apworld_dir.exists():
			AutoWorldRegister.world_types[TestWorld.game] = cls.test_world_cache[apworld_dir.resolve()]
		else:
			apworld_dir.mkdir()
			(apworld_dir / "__init__.py").write_text(INIT_CONTENTS)
			(apworld_dir / build_apworld.MANIFEST_NAME).write_text(MANIFEST_CONTENTS)
			shutil.copyfile(TestWorld.__file__, os.path.join(apworld_dir, "world.py"))

		return apworld_dir

	def test_input_path_absolute(self: Self) -> None:
		input_path = self.create_apworld_dir().resolve()
		output_path = self.output_tempdir.name

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

	def test_input_path_relative(self: Self) -> None:
		input_path = self.create_apworld_dir().relative_to(os.path.abspath(os.curdir), walk_up=True)
		output_path = self.output_tempdir.name

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

	def test_input_path_diacritics(self: Self) -> None:
		apworld_name = "ầþẁöřḻď"
		input_path = self.create_apworld_dir(apworld_name)
		output_path = self.output_tempdir.name

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))
		self.assertEqual(f"{apworld_name}.apworld", os.path.basename(apworld_path))

	def test_output_path_absolute(self: Self) -> None:
		input_path = self.create_apworld_dir()
		output_path = os.path.abspath(self.output_tempdir.name)

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

	def test_output_path_relative(self: Self) -> None:
		input_path = self.create_apworld_dir()
		output_path = os.path.relpath(self.output_tempdir.name, os.curdir)

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

	def test_apworld_name(self: Self) -> None:
		apworld_name = "test"
		input_path = self.create_apworld_dir()
		output_path = self.output_tempdir.name

		apworld_path = build_apworld.main(
			apworld_name=apworld_name,
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))
		self.assertEqual(f"{apworld_name}.apworld", os.path.basename(apworld_path))

	def test_world_type_invalid(self: Self) -> None:
		input_path = self.create_apworld_dir()
		output_path = self.output_tempdir.name

		with self.assertRaises(AssertionError):
			build_apworld.main(
				input_path=input_path,
				output_path=output_path,
				world_type=TestWorld
			)

	def test_world_type_valid(self: Self) -> None:
		input_path = self.create_apworld_dir()
		output_path = self.output_tempdir.name

		importlib.import_module(input_path.name)

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path,
			world_type=AutoWorldRegister.world_types[TestWorld.game]
		)

		self.assertTrue(os.path.exists(apworld_path))

	def test_zipfile_contents(self: Self) -> None:
		apworld_name = "test"
		input_path = self.create_apworld_dir()
		output_path = self.output_tempdir.name

		apworld_path = build_apworld.main(
			apworld_name=apworld_name,
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

		with zipfile.ZipFile(apworld_path) as zf:
			missing_files = set()
			zip_file_paths = zf.namelist()

			for input_file in input_path.iterdir():
				if input_file.name in build_apworld.ZIP_EXCLUDE:
					continue

				zip_file_path = f"{apworld_name}/{input_file.name}"

				if zip_file_path in zip_file_paths:
					zip_file_paths.remove(zip_file_path)
				else:
					missing_files.add(zip_file_path)

			self.assertFalse(missing_files, "Files found in input that were not in apworld")
			self.assertFalse(zip_file_paths, "Files found in apworld that were not in input")

	def test_zipfile_exclusion(self: Self) -> None:
		input_path = self.create_apworld_dir()
		output_path = self.output_tempdir.name

		excluded_file_name = ".DS_STORE"
		excluded_file_path = input_path / excluded_file_name
		excluded_file_path.touch()

		self.assertTrue(excluded_file_path.exists())

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

		with zipfile.ZipFile(apworld_path) as zf:
			self.assertNotIn(f"{input_path.name}/{excluded_file_name}", zf.namelist())

	def test_zipfile_extensionless(self: Self) -> None:
		input_path = self.create_apworld_dir()
		output_path = self.output_tempdir.name

		excluded_file_name = "README"
		excluded_file_path = input_path / excluded_file_name
		excluded_file_path.touch()

		self.assertTrue(excluded_file_path.exists())

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

		with zipfile.ZipFile(apworld_path) as zf:
			self.assertIn(f"{input_path.name}/{excluded_file_name}", zf.namelist())

	def test_zipfile_manifest(self: Self) -> None:
		input_path = self.create_apworld_dir()
		output_path = self.output_tempdir.name

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

		with zipfile.ZipFile(apworld_path) as zf:
			manifest: dict[str, Any] = orjson.loads(zf.read(f"{input_path.name}/{build_apworld.MANIFEST_NAME}"))

			self.assertIn("compatible_version", manifest)
			self.assertIn("version", manifest)

	def test_zipfile_timestamp(self: Self) -> None:
		input_path = self.create_apworld_dir("timestamp")
		output_path = self.output_tempdir.name

		for input_file in os.listdir(input_path):
			os.utime(os.path.join(input_path, input_file), (0, 0))

		apworld_path = build_apworld.main(
			input_path=input_path,
			output_path=output_path
		)

		self.assertTrue(os.path.exists(apworld_path))

	def test_launcher_component_all(self: Self) -> None:
		build_dir = "build"
		# noinspection SpellCheckingInspection
		apworlds_path = os.path.join(build_dir, "apworlds")

		_, component = Launcher.identify(LAUNCHER_COMPONENT)

		Launcher.main({
			"args": {
				"--suppress-open"
			},
			"component": component,
			"update_settings": False
		})

		try:
			self.assertTrue(os.path.exists(apworlds_path))
			self.assertEqual(len(AutoWorldRegister.world_types), len(os.listdir(apworlds_path)))
		finally:
			shutil.rmtree(build_dir, ignore_errors=True)

	def test_launcher_component_single(self: Self) -> None:
		build_dir = "build"
		# noinspection SpellCheckingInspection
		apworlds_path = os.path.join(build_dir, "apworlds")

		_, component = Launcher.identify(LAUNCHER_COMPONENT)

		Launcher.main({
			"args": {
				"--suppress-open",
				"Archipelago"
			},
			"component": component,
			"update_settings": False
		})

		try:
			self.assertTrue(os.path.exists(os.path.join(apworlds_path, "generic.apworld")))
			self.assertEqual(1, len(os.listdir(apworlds_path)))
		finally:
			shutil.rmtree(build_dir, ignore_errors=True)
