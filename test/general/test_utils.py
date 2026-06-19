import subprocess
import unittest
from unittest import mock

import Utils


class TestLinuxFileDialogFallback(unittest.TestCase):
    """The Linux native file dialogs (kdialog/zenity) must honor the helper's exit code.

    Exit code 0 -> a path was chosen; exit code 1 -> the user cancelled (no fallback);
    any other exit code -> the helper errored, so we must fall back to the next backend
    instead of silently treating the failure as a cancellation (issue #5991).
    """

    FILETYPES = (("Patch", (".aptest",)),)

    def _which(self, tool: str) -> str:
        return f"/usr/bin/{tool}"

    def test_kdialog_success_returns_path_without_fallback(self) -> None:
        """A successful kdialog selection is returned and zenity is never consulted."""
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="/home/user/file.aptest\n", stderr="")
        with mock.patch.object(Utils, "is_linux", True), \
                mock.patch.object(Utils, "env_cleared_lib_path", return_value={}), \
                mock.patch("shutil.which", side_effect=self._which) as which_mock, \
                mock.patch("subprocess.run", return_value=completed) as run_mock:
            result = Utils.open_filename("title", self.FILETYPES)

        self.assertEqual(result, "/home/user/file.aptest")
        # Only kdialog should have been run; zenity must not be invoked once kdialog handled it.
        self.assertEqual(run_mock.call_count, 1)
        self.assertIn("kdialog", run_mock.call_args.args[0][0])
        which_mock.assert_called_once_with("kdialog")

    def test_user_cancel_returns_none_without_fallback(self) -> None:
        """Exit code 1 (user cancel) returns None and must NOT fall back to another backend."""
        cancelled = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
        with mock.patch.object(Utils, "is_linux", True), \
                mock.patch.object(Utils, "env_cleared_lib_path", return_value={}), \
                mock.patch("shutil.which", side_effect=self._which), \
                mock.patch("subprocess.run", return_value=cancelled) as run_mock:
            result = Utils.save_filename("title", self.FILETYPES)

        self.assertIsNone(result)
        # A cancel is conclusive: only the first backend (kdialog) runs, no zenity fallback.
        self.assertEqual(run_mock.call_count, 1)
        self.assertIn("kdialog", run_mock.call_args.args[0][0])

    def test_tool_error_falls_back_to_next_backend(self) -> None:
        """Exit code 2 (tool error) must fall back to zenity, which then succeeds."""
        errored = subprocess.CompletedProcess(args=[], returncode=2, stdout="", stderr="boom")
        success = subprocess.CompletedProcess(args=[], returncode=0, stdout="/srv/games\n", stderr="")
        with mock.patch.object(Utils, "is_linux", True), \
                mock.patch.object(Utils, "env_cleared_lib_path", return_value={}), \
                mock.patch("shutil.which", side_effect=self._which), \
                mock.patch("subprocess.run", side_effect=[errored, success]) as run_mock:
            result = Utils.open_directory("title")

        self.assertEqual(result, "/srv/games")
        # kdialog errors (rc 2), so we must invoke zenity as the next backend.
        self.assertEqual(run_mock.call_count, 2)
        self.assertIn("kdialog", run_mock.call_args_list[0].args[0][0])
        self.assertIn("zenity", run_mock.call_args_list[1].args[0][0])


if __name__ == "__main__":
    unittest.main()
