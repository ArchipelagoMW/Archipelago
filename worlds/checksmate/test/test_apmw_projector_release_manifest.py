import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import stat
import sys
import tempfile
from types import ModuleType
import unittest
from unittest.mock import patch
import zipfile

if __package__:
    from ..apmw_projection import (
        FROZEN_CONTRACT_HASH,
        PROTOCOL_VERSION,
        RUNTIME_SEMANTIC_VERSION,
    )
else:
    CHECKSMATE_ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(CHECKSMATE_ROOT))
    from apmw_projection import (
        FROZEN_CONTRACT_HASH,
        PROTOCOL_VERSION,
        RUNTIME_SEMANTIC_VERSION,
    )


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RELEASE_SCRIPT = (
    REPOSITORY_ROOT
    / "worlds"
    / "checksmate"
    / "tools"
    / "create_apmw_projector_release_manifest.py"
)
SOURCE_COMMIT = "0123456789abcdef0123456789abcdef01234567"
SOURCE_REPOSITORY = "chesslogic/Archipelago"
EXPECTED_PROJECTOR_METADATA = {
    "runtime_semantic_version": "0.1.0",
    "protocol_version": 1,
    "contract_hash": "91cf4323ae53663d1e3a7ea8facb449c74fdcd5093fa1620337f51cc5cdbe00c",
    "minimum_client_version": "0.4.0",
}


def load_release_builder():
    specification = importlib.util.spec_from_file_location(
        "create_apmw_projector_release_manifest", RELEASE_SCRIPT
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    missing = object()
    previous = sys.modules.get(specification.name, missing)
    # Dataclasses needs this registration while resolving postponed annotations.
    sys.modules[specification.name] = module
    try:
        specification.loader.exec_module(module)
    finally:
        if previous is missing:
            sys.modules.pop(specification.name, None)
        else:
            sys.modules[specification.name] = previous
    return module


class TestApmwProjectorReleaseManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.release_builder = load_release_builder()

    def setUp(self):
        directory = tempfile.TemporaryDirectory(
            prefix="test-apmw-projector-release-manifest-"
        )
        self.addCleanup(directory.cleanup)
        self.test_output = Path(directory.name)

    def test_overlapping_fixture_lifecycles_preserve_each_others_files(self):
        first = self._input("windows", "x86")
        expected = {
            path: path.read_bytes() for path in (first.build_manifest, first.archive)
        }
        second = type(self)()
        self.addCleanup(second.doCleanups)
        second.setUp()
        try:
            with self.subTest(phase="second setup"):
                for path, contents in expected.items():
                    self.assertEqual(contents, path.read_bytes())
            second_input = second._input("windows", "x86")
        finally:
            second.tearDown()
            second.doCleanups()

        with self.subTest(phase="second cleanup"):
            for path, contents in expected.items():
                self.assertEqual(contents, path.read_bytes())
        self.assertFalse(second_input.build_manifest.parent.exists())

    def test_failed_fixture_lifecycle_cleans_up_its_files(self):
        for phase in ("setup", "test"):
            with self.subTest(phase=phase):
                class FailingFixture(TestApmwProjectorReleaseManifest):
                    def setUp(self):
                        super().setUp()
                        self.fixture = self._input("windows", "x86")
                        if phase == "setup":
                            raise RuntimeError("fixture setup failed")

                    def runTest(self):
                        raise RuntimeError("fixture test failed")

                case = FailingFixture()
                self.addCleanup(case.doCleanups)
                result = unittest.TestResult()
                case.run(result)
                self.assertEqual(1, len(result.errors))
                self.assertIn(f"RuntimeError: fixture {phase} failed", result.errors[0][1])
                self.assertFalse(case.fixture.build_manifest.parent.exists())

    def test_release_builder_load_restores_module_registration(self):
        module_name = self.release_builder.__name__
        missing = object()
        original = sys.modules.get(module_name, missing)
        if original is missing:
            self.addCleanup(sys.modules.pop, module_name, None)
        else:
            self.addCleanup(sys.modules.__setitem__, module_name, original)
        dependency = ModuleType("_checksmate_release_builder_test_dependency")
        self.assertNotIn(dependency.__name__, sys.modules)
        self.addCleanup(sys.modules.pop, dependency.__name__, None)
        exec_module = importlib.machinery.SourceFileLoader.exec_module

        for previous in (missing, self.release_builder, None):
            for fails in (False, True):
                with self.subTest(previous=previous, fails=fails):
                    if previous is missing:
                        sys.modules.pop(module_name, None)
                    else:
                        sys.modules[module_name] = previous
                    sys.modules.pop(dependency.__name__, None)

                    def exec_with_dependency(loader, module):
                        if module.__name__ == module_name:
                            self.assertIs(module, sys.modules[module_name])
                            sys.modules[dependency.__name__] = dependency
                            if fails:
                                raise RuntimeError("release builder execution failed")
                        return exec_module(loader, module)

                    with patch.object(
                        importlib.machinery.SourceFileLoader,
                        "exec_module",
                        autospec=True,
                        side_effect=exec_with_dependency,
                    ):
                        if fails:
                            with self.assertRaisesRegex(
                                RuntimeError, "release builder execution failed"
                            ):
                                load_release_builder()
                        else:
                            builder = load_release_builder()
                            self.assertIsNot(builder, previous)

                    if previous is missing:
                        self.assertNotIn(module_name, sys.modules)
                    else:
                        self.assertIs(previous, sys.modules[module_name])
                    self.assertIs(dependency, sys.modules.get(dependency.__name__))

    def test_combines_two_archives_into_canonical_immutable_manifest(self):
        x86 = self._input("windows", "x86")
        x64 = self._input("windows", "x64")

        manifest = self.release_builder.create_release_manifest(
            [x86, x64],
            SOURCE_REPOSITORY,
            SOURCE_COMMIT,
            "apmw-projector-v0.1.0",
        )
        output = self.release_builder.write_release_manifest(
            manifest, self.test_output / "release.json"
        )

        self.assertEqual(
            self.release_builder.RELEASE_MANIFEST_SCHEMA, manifest["schema"]
        )
        self.assertEqual(
            self.release_builder.RELEASE_MANIFEST_VERSION, manifest["version"]
        )
        self.assertEqual(
            EXPECTED_PROJECTOR_METADATA,
            {key: manifest[key] for key in EXPECTED_PROJECTOR_METADATA},
        )
        self.assertEqual(RUNTIME_SEMANTIC_VERSION, manifest["runtime_semantic_version"])
        self.assertEqual(PROTOCOL_VERSION, manifest["protocol_version"])
        self.assertEqual(FROZEN_CONTRACT_HASH, manifest["contract_hash"])
        self.assertEqual(SOURCE_COMMIT, manifest["source_commit"])
        self.assertEqual({"windows-x86", "windows-x64"}, set(manifest["assets"]))
        asset = manifest["assets"]["windows-x64"]
        self.assertEqual("windows-x64.zip", asset["filename"])
        self.assertEqual(
            hashlib.sha256(x64.archive.read_bytes()).hexdigest(), asset["sha256"]
        )
        self.assertEqual(x64.archive.stat().st_size, asset["size"])
        self.assertEqual("ApmwProjector.exe", asset["executable"]["relative_path"])
        self.assertEqual(
            hashlib.sha256(b"fixture").hexdigest(), asset["executable"]["sha256"]
        )
        self.assertEqual(
            self.release_builder.canonical_json(manifest) + "\n",
            output.read_text(encoding="ascii"),
        )
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.release_builder.write_release_manifest(manifest, output)

    def test_rejects_mismatched_metadata_duplicate_architecture_and_bad_identity(self):
        x86 = self._input("windows", "x86")
        x64 = self._input("windows", "x64")
        mismatched = json.loads(x64.build_manifest.read_text(encoding="ascii"))
        mismatched["protocol_version"] = PROTOCOL_VERSION + 1
        x64.build_manifest.write_text(
            json.dumps(mismatched, sort_keys=True, separators=(",", ":")),
            encoding="ascii",
        )
        self._write_archive(
            x64,
            {
                "apmw-projector-manifest.json": x64.build_manifest.read_bytes(),
                "ApmwProjector.exe": b"fixture",
            },
        )
        with self.assertRaisesRegex(ValueError, "mismatched projector metadata"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

        duplicate = self._input("windows", "x86", "duplicate")
        with self.assertRaisesRegex(ValueError, "duplicate projector architecture"):
            self.release_builder.create_release_manifest(
                [x86, duplicate],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )
        with self.assertRaisesRegex(ValueError, "lowercase 40-hex"):
            self.release_builder.create_release_manifest(
                [x86, duplicate],
                SOURCE_REPOSITORY,
                "not-a-commit",
                "apmw-projector-v0.1.0",
            )
        x64 = self._input("windows", "x64", "tag")
        with self.assertRaisesRegex(ValueError, "runtime version"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.2.0",
            )

    def test_rejects_unrequested_or_invalid_input_files(self):
        x86 = self._input("windows", "x86")
        missing = self.release_builder.ReleaseInput(
            self.test_output / "missing.json", x86.archive
        )
        with self.assertRaisesRegex(ValueError, "not a regular file"):
            self.release_builder.create_release_manifest(
                [x86, missing],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

    def test_rejects_duplicate_json_and_untrusted_archive_contents(self):
        x86 = self._input("windows", "x86")
        x64 = self._input("windows", "x64")
        x86.build_manifest.write_text(
            '{"schema":"apmw_projector_build_manifest","schema":"duplicate"}',
            encoding="ascii",
        )
        with self.assertRaisesRegex(ValueError, "duplicate JSON property"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

        x86 = self._input("windows", "x86", "archive")
        x64 = self._input("windows", "x64", "archive")
        self._write_archive(
            x86,
            {
                "apmw-projector-manifest.json": x86.build_manifest.read_bytes(),
                "ApmwProjector.exe": b"fixture",
                "../outside": b"unsafe",
            },
        )
        with self.assertRaisesRegex(ValueError, "unsafe member path"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

        x86 = self._input("windows", "x86", "duplicate-member")
        x64 = self._input("windows", "x64", "duplicate-member")
        with zipfile.ZipFile(x86.archive, "w") as bundle:
            bundle.writestr(
                "apmw-projector-manifest.json", x86.build_manifest.read_bytes()
            )
            bundle.writestr("ApmwProjector.exe", b"fixture")
            bundle.writestr("ApmwProjector.exe", b"fixture")
        with self.assertRaisesRegex(ValueError, "duplicate member path"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

        x86 = self._input("windows", "x86", "link")
        x64 = self._input("windows", "x64", "link")
        with zipfile.ZipFile(x86.archive, "w") as bundle:
            bundle.writestr(
                "apmw-projector-manifest.json", x86.build_manifest.read_bytes()
            )
            bundle.writestr("ApmwProjector.exe", b"fixture")
            link = zipfile.ZipInfo("linked")
            link.external_attr = (stat.S_IFLNK | 0o777) << 16
            bundle.writestr(link, b"target")
        with self.assertRaisesRegex(ValueError, "link-like member"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

        x86 = self._input("windows", "x86", "reparse")
        x64 = self._input("windows", "x64", "reparse")
        with zipfile.ZipFile(x86.archive, "w") as bundle:
            bundle.writestr(
                "apmw-projector-manifest.json", x86.build_manifest.read_bytes()
            )
            bundle.writestr("ApmwProjector.exe", b"fixture")
            reparse = zipfile.ZipInfo("reparse")
            reparse.external_attr = 0x400
            bundle.writestr(reparse, b"target")
        with self.assertRaisesRegex(ValueError, "link-like member"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

    def test_rejects_archive_manifest_and_executable_disagreement(self):
        x86 = self._input("windows", "x86")
        x64 = self._input("windows", "x64")
        self._write_archive(
            x86,
            {
                "apmw-projector-manifest.json": b"{}",
                "ApmwProjector.exe": b"fixture",
            },
        )
        with self.assertRaisesRegex(ValueError, "does not match supplied"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

        x86 = self._input("windows", "x86", "hash")
        x64 = self._input("windows", "x64", "hash")
        document = json.loads(x86.build_manifest.read_text(encoding="ascii"))
        document["executable_sha256"] = "b" * 64
        x86.build_manifest.write_text(
            json.dumps(document, sort_keys=True, separators=(",", ":")),
            encoding="ascii",
        )
        self._write_archive(
            x86,
            {
                "apmw-projector-manifest.json": x86.build_manifest.read_bytes(),
                "ApmwProjector.exe": b"fixture",
            },
        )
        with self.assertRaisesRegex(ValueError, "executable hash"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

        x86 = self._input("windows", "x86", "version")
        x64 = self._input("windows", "x64", "version")
        document = json.loads(x86.build_manifest.read_text(encoding="ascii"))
        document["runtime_semantic_version"] = "01.0.0"
        x86.build_manifest.write_text(
            json.dumps(document, sort_keys=True, separators=(",", ":")),
            encoding="ascii",
        )
        self._write_archive(
            x86,
            {
                "apmw-projector-manifest.json": x86.build_manifest.read_bytes(),
                "ApmwProjector.exe": b"fixture",
            },
        )
        with self.assertRaisesRegex(ValueError, "invalid metadata"):
            self.release_builder.create_release_manifest(
                [x86, x64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

    def test_requires_exact_windows_architecture_pair(self):
        x86 = self._input("windows", "x86")
        arm64 = self._input("windows", "arm64")
        with self.assertRaisesRegex(ValueError, "windows-x86 and windows-x64"):
            self.release_builder.create_release_manifest(
                [x86, arm64],
                SOURCE_REPOSITORY,
                SOURCE_COMMIT,
                "apmw-projector-v0.1.0",
            )

    def _input(self, platform: str, architecture: str, suffix: str = ""):
        stem = f"{platform}-{architecture}{suffix}"
        build_manifest = self.test_output / f"{stem}.json"
        archive = self.test_output / f"{stem}.zip"
        build_manifest.write_text(
            json.dumps(
                {
                    "schema": "apmw_projector_build_manifest",
                    "version": 1,
                    "runtime_semantic_version": RUNTIME_SEMANTIC_VERSION,
                    "protocol_version": PROTOCOL_VERSION,
                    "contract_hash": FROZEN_CONTRACT_HASH,
                    "minimum_client_version": "0.4.0",
                    "target_platform": platform,
                    "target_architecture": architecture,
                    "executable_relative_path": "ApmwProjector.exe",
                    "executable_sha256": hashlib.sha256(b"fixture").hexdigest(),
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            encoding="ascii",
        )
        self._write_archive(
            self.release_builder.ReleaseInput(build_manifest, archive),
            {
                "apmw-projector-manifest.json": build_manifest.read_bytes(),
                "ApmwProjector.exe": b"fixture",
            },
        )
        return self.release_builder.ReleaseInput(build_manifest, archive)

    @staticmethod
    def _write_archive(release_input, entries):
        with zipfile.ZipFile(release_input.archive, "w") as bundle:
            for path, contents in entries.items():
                bundle.writestr(path, contents)


if __name__ == "__main__":
    unittest.main()
