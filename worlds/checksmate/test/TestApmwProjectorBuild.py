import hashlib
import importlib.util
import json
from pathlib import Path
import re
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
BUILD_SCRIPT = REPOSITORY_ROOT / "tools" / "build_apmw_projector.py"
BUILD_REQUIREMENTS = REPOSITORY_ROOT / "tools" / "apmw_projector_build_requirements.txt"
RELEASE_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "apmw-projector-release.yml"
TEST_OUTPUT = REPOSITORY_ROOT / "build" / "test-apmw-projector-manifest"


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

    def test_release_build_uses_immutable_actions_and_hashed_dependencies(self):
        workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        action_references = re.findall(r"^\s*uses:\s*[^@\s]+@([^\s#]+)", workflow, re.MULTILINE)

        self.assertTrue(action_references)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", value) for value in action_references))
        self.assertIn("--require-hashes", workflow)
        self.assertIn("tools\\apmw_projector_build_requirements.txt", workflow)

        requirements = BUILD_REQUIREMENTS.read_text(encoding="ascii")
        requirement_starts = [
            line for line in requirements.splitlines()
            if line and not line.startswith(("#", " "))
        ]
        self.assertTrue(requirement_starts)
        self.assertTrue(all("==" in line for line in requirement_starts))
        self.assertEqual(requirements.count("--hash=sha256:"), 13)

    def test_release_rechecks_tag_identity_immediately_before_publication(self):
        workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        publish_step = workflow.index("- name: Publish immutable GitHub release")
        publish_script = workflow[publish_step:]

        self.assertIn('git fetch --force origin "refs/tags/${RELEASE_TAG}:refs/tags/${RELEASE_TAG}"', publish_script)
        self.assertIn('current_tag_commit="$(git rev-list -n 1 "${RELEASE_TAG}^{commit}")"', publish_script)
        self.assertIn('needs.prepare.outputs.source_commit', publish_script)
        self.assertLess(publish_script.index("git fetch --force"), publish_script.index("gh release create"))


if __name__ == "__main__":
    unittest.main()
