import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import stat
import sys
import unittest
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
RELEASE_SCRIPT = REPOSITORY_ROOT / "tools" / "create_apmw_projector_release_manifest.py"
TEST_OUTPUT = REPOSITORY_ROOT / "build" / "test-apmw-projector-release-manifest"
SOURCE_COMMIT = "0123456789abcdef0123456789abcdef01234567"
SOURCE_REPOSITORY = "chesslogic/Archipelago"


def load_release_builder():
    specification = importlib.util.spec_from_file_location(
        "create_apmw_projector_release_manifest", RELEASE_SCRIPT
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class TestApmwProjectorReleaseManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.release_builder = load_release_builder()

    def setUp(self):
        shutil.rmtree(TEST_OUTPUT, ignore_errors=True)
        TEST_OUTPUT.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(TEST_OUTPUT, ignore_errors=True)

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
            manifest, TEST_OUTPUT / "release.json"
        )

        self.assertEqual(
            self.release_builder.RELEASE_MANIFEST_SCHEMA, manifest["schema"]
        )
        self.assertEqual(
            self.release_builder.RELEASE_MANIFEST_VERSION, manifest["version"]
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
            TEST_OUTPUT / "missing.json", x86.archive
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
        build_manifest = TEST_OUTPUT / f"{stem}.json"
        archive = TEST_OUTPUT / f"{stem}.zip"
        build_manifest.write_text(
            json.dumps(
                {
                    "schema": "apmw_projector_build_manifest",
                    "version": 1,
                    "runtime_semantic_version": RUNTIME_SEMANTIC_VERSION,
                    "protocol_version": PROTOCOL_VERSION,
                    "contract_hash": FROZEN_CONTRACT_HASH,
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
