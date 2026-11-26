import random
import sys
import unittest
from unittest import mock

from . import bases
from . import test_apmw_projector_build as projector_tests


class TestTestStateIsolation(unittest.TestCase):
    def test_world_fixture_restores_global_random_state_on_success_and_errors(self):
        self.addCleanup(random.setstate, random.getstate())

        class FixtureError(RuntimeError):
            pass

        class Fixture(bases.CMTestBase):
            def world_setup(self):
                super().world_setup(seed=37)

            def setUp(self):
                super().setUp()
                if failure_phase == "setup":
                    raise FixtureError("expected setup failure")

            def runTest(self):
                self.assertEqual(37, self.multiworld.seed)
                if failure_phase == "test":
                    raise FixtureError("expected test failure")

            def tearDown(self):
                super().tearDown()
                if failure_phase == "teardown":
                    raise FixtureError("expected teardown failure")

        for failure_phase in (None, "setup", "test", "teardown"):
            with self.subTest(failure_phase=failure_phase):
                random.seed(91)
                before = random.getstate()
                result = unittest.TestResult()

                unittest.TestSuite([Fixture()]).run(result)

                self.assertEqual(1, result.testsRun)
                self.assertEqual([], result.failures)
                if failure_phase is None:
                    self.assertEqual([], result.errors)
                else:
                    self.assertEqual(1, len(result.errors))
                    self.assertIn(
                        f"FixtureError: expected {failure_phase} failure",
                        result.errors[0][1],
                    )
                self.assertEqual(before, random.getstate())
                self.assertEqual(random.Random(91).random(), random.random())

    def test_projector_fixture_restores_import_path_on_success_and_error(self):
        class FixtureError(RuntimeError):
            pass

        class Fixture(projector_tests.TestApmwProjectorBuild):
            def setUp(self):
                super().setUp()
                if failure_phase == "setup":
                    self.test_manifest_has_stable_metadata_and_executable_checksum()
                    raise FixtureError("expected projector setup failure")

            def runTest(self):
                self.test_manifest_has_stable_metadata_and_executable_checksum()
                if failure_phase == "test":
                    raise FixtureError("expected projector test failure")

        checksmate_root = str(projector_tests.BUILD_SCRIPT.parents[1])
        for failure_phase in (None, "setup", "test"):
            with self.subTest(failure_phase=failure_phase), mock.patch.object(
                sys, "path",
                [entry for entry in sys.path if entry != checksmate_root],
            ):
                original_path = sys.path
                before = original_path.copy()
                result = unittest.TestResult()
                fixture = Fixture()

                unittest.TestSuite([fixture]).run(result)

                self.assertEqual(1, result.testsRun)
                self.assertEqual([], result.failures)
                if failure_phase is not None:
                    self.assertEqual(1, len(result.errors))
                    self.assertIn(
                        f"FixtureError: expected projector {failure_phase} failure",
                        result.errors[0][1],
                    )
                else:
                    self.assertEqual([], result.errors)
                self.assertIs(original_path, sys.path)
                self.assertEqual(before, sys.path)
                self.assertEqual(before, original_path)
                self.assertFalse(fixture.test_output.exists())
