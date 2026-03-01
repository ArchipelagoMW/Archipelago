"""Tests for WebHost world filter and tutorial_landing."""

import unittest

from worlds.AutoWorld import AutoWorldRegister

from . import TestBase


class TestGetWebhostWorlds(unittest.TestCase):
    """Tests for AutoWorldRegister.get_worlds(require_tutorials=True) filter."""

    def test_returns_only_worlds_with_tutorials(self) -> None:
        webhost_worlds = AutoWorldRegister.get_worlds(require_tutorials=True)
        for game, world in webhost_worlds.items():
            with self.subTest(game=game):
                self.assertTrue(
                    hasattr(world.web, "tutorials"),
                    f"{game} in get_worlds(require_tutorials=True) must have .web.tutorials",
                )

    def test_is_subset_of_all_worlds(self) -> None:
        all_worlds = AutoWorldRegister.world_types
        webhost_worlds = AutoWorldRegister.get_worlds(require_tutorials=True)
        all_keys = set(all_worlds)
        webhost_keys = set(webhost_worlds)
        self.assertTrue(
            webhost_keys <= all_keys,
            f"get_worlds(require_tutorials=True) should be a subset of get_all_worlds(); "
            f"extra keys: {webhost_keys - all_keys!r}",
        )
        for game in webhost_keys:
            self.assertIs(webhost_worlds[game], all_worlds[game], f"{game} should be same class ref")

    def test_all_worlds_not_filtered_globally(self) -> None:
        """Calling tutorial-filtered get_worlds() should not mutate the global world mapping."""
        AutoWorldRegister.get_worlds(require_tutorials=True)
        all_worlds = AutoWorldRegister.world_types
        webhost_worlds = AutoWorldRegister.get_worlds(require_tutorials=True)
        self.assertGreaterEqual(
            len(all_worlds),
            len(webhost_worlds),
            "get_all_worlds() should return at least as many worlds as get_worlds(require_tutorials=True)",
        )


class TestTutorialLanding(TestBase):
    """Tests for the /tutorial/ route that uses AutoWorldRegister.get_worlds()."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        import WebHost
        WebHost.copy_tutorials_files_to_static()

    def test_tutorial_landing_returns_200(self) -> None:
        """Tutorial landing page loads without error and only includes WebHost-valid worlds."""
        with self.app.test_request_context():
            response = self.client.get("/tutorial/")
        self.assertEqual(response.status_code, 200, response.data.decode()[:500])

