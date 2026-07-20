import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import unittest
from unittest import mock

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
CHECKSMATE_TOOLS = REPOSITORY_ROOT / "worlds" / "checksmate" / "tools"
BUILD_SCRIPT = CHECKSMATE_TOOLS / "build_apmw_projector.py"
BUILD_REQUIREMENTS = CHECKSMATE_TOOLS / "apmw_projector_build_requirements.txt"
TEST_OUTPUT = REPOSITORY_ROOT / "build" / "test-apmw-projector-manifest"
EXPECTED_PROJECTOR_METADATA = {
    "runtime_semantic_version": "0.1.0",
    "protocol_version": 1,
    "contract_hash": "f1456e916285bf79dd4be6f4c8c6e5798ed7bb1eebd2f6e1f81075f39e8ffc15",
}


def load_builder():
    specification = importlib.util.spec_from_file_location(
        "build_apmw_projector", BUILD_SCRIPT
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class TestApmwProjectorBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_builder()

    def setUp(self):
        shutil.rmtree(TEST_OUTPUT, ignore_errors=True)
        TEST_OUTPUT.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(TEST_OUTPUT, ignore_errors=True)

    def test_manifest_has_stable_metadata_and_executable_checksum(self):
        executable = TEST_OUTPUT / self.builder.projector_executable_name()
        executable.write_bytes(b"APMW standalone projector fixture")

        manifest_path = self.builder.write_manifest(executable, TEST_OUTPUT)
        manifest = json.loads(manifest_path.read_text(encoding="ascii"))

        self.assertEqual(EXPECTED_PROJECTOR_METADATA, self.builder.projector_metadata())
        self.assertEqual(
            {
                "schema",
                "version",
                "runtime_semantic_version",
                "protocol_version",
                "contract_hash",
                "target_platform",
                "target_architecture",
                "executable_relative_path",
                "executable_sha256",
            },
            set(manifest),
        )
        self.assertEqual(self.builder.BUILD_MANIFEST_SCHEMA, manifest["schema"])
        self.assertEqual(self.builder.BUILD_MANIFEST_VERSION, manifest["version"])
        self.assertEqual(
            EXPECTED_PROJECTOR_METADATA,
            {key: manifest[key] for key in EXPECTED_PROJECTOR_METADATA},
        )
        self.assertEqual(RUNTIME_SEMANTIC_VERSION, manifest["runtime_semantic_version"])
        self.assertEqual(PROTOCOL_VERSION, manifest["protocol_version"])
        self.assertEqual(FROZEN_CONTRACT_HASH, manifest["contract_hash"])
        self.assertEqual(executable.name, manifest["executable_relative_path"])
        self.assertEqual(
            hashlib.sha256(executable.read_bytes()).hexdigest(),
            manifest["executable_sha256"],
        )

    def test_platform_and_architecture_names_are_stable_release_ids(self):
        self.assertEqual("windows", self.builder.normalize_platform("Windows"))
        self.assertEqual("macos", self.builder.normalize_platform("Darwin"))
        self.assertEqual("x86", self.builder.normalize_architecture("i686"))
        self.assertEqual("x64", self.builder.normalize_architecture("amd64"))
        self.assertEqual("x64", self.builder.normalize_architecture("x86_64"))
        self.assertEqual("arm64", self.builder.normalize_architecture("aarch64"))
        with self.assertRaisesRegex(ValueError, "unsupported projector architecture"):
            self.builder.normalize_architecture("sparc")

    def test_missing_cx_freeze_fails_without_installing_dependencies(self):
        with mock.patch.dict(sys.modules, {"cx_Freeze": None}):
            with self.assertRaisesRegex(RuntimeError, "cx_Freeze 8.0.0 is required"):
                self.builder._load_cx_freeze()

    def test_projector_tooling_is_scoped_to_checksmate(self):
        self.assertEqual(CHECKSMATE_TOOLS, BUILD_SCRIPT.parent)
        self.assertEqual(CHECKSMATE_TOOLS / "apmw_projector.py", self.builder.ENTRY_SCRIPT)
        self.assertFalse((REPOSITORY_ROOT / "apmw_projector.py").exists())
        for filename in (
            "build_apmw_projector.py",
            "smoke_apmw_projector.py",
            "create_apmw_projector_release_manifest.py",
            "apmw_projector_build_requirements.txt",
        ):
            self.assertFalse((REPOSITORY_ROOT / "tools" / filename).exists())

    def test_build_dependencies_are_pinned_and_hashed(self):
        requirements = BUILD_REQUIREMENTS.read_text(encoding="ascii")
        requirement_starts = [
            line for line in requirements.splitlines()
            if line and not line.startswith(("#", " "))
        ]
        self.assertTrue(requirement_starts)
        self.assertTrue(all("==" in line for line in requirement_starts))
        self.assertEqual(requirements.count("--hash=sha256:"), 13)


if __name__ == "__main__":
    unittest.main()
