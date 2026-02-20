"""Tests for WebHost world filter (get_webhost_worlds) and tutorial_landing."""

import unittest

from worlds.AutoWorld import AutoWorldRegister
from WebHostLib.misc import get_webhost_worlds

from . import TestBase


class TestGetWebhostWorlds(unittest.TestCase):
    """Tests for get_webhost_worlds() filter."""

    def test_returns_only_worlds_with_tutorials(self) -> None:
        webhost_worlds = get_webhost_worlds()
        for game, world in webhost_worlds.items():
            with self.subTest(game=game):
                self.assertTrue(
                    hasattr(world.web, "tutorials"),
                    f"{game} in get_webhost_worlds() must have .web.tutorials",
                )

    def test_is_subset_of_all_worlds(self) -> None:
        all_worlds = AutoWorldRegister.world_types
        webhost_worlds = get_webhost_worlds()
        all_keys = set(all_worlds)
        webhost_keys = set(webhost_worlds)
        self.assertTrue(
            webhost_keys <= all_keys,
            f"get_webhost_worlds() should be a subset of get_all_worlds(); "
            f"extra keys: {webhost_keys - all_keys!r}",
        )
        for game in webhost_keys:
            self.assertIs(webhost_worlds[game], all_worlds[game], f"{game} should be same class ref")

    def test_all_worlds_not_filtered_globally(self) -> None:
        """After using get_webhost_worlds(), get_all_worlds() still returns the full set (no world_types reassignment)."""
        get_webhost_worlds()
        all_worlds = AutoWorldRegister.world_types
        webhost_worlds = get_webhost_worlds()
        self.assertGreaterEqual(
            len(all_worlds),
            len(webhost_worlds),
            "get_all_worlds() should return at least as many worlds as get_webhost_worlds()",
        )


class TestTutorialLanding(TestBase):
    """Tests for the /tutorial/ route that uses get_webhost_worlds()."""

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

