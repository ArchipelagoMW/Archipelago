import unittest


class TestWorldImports(unittest.TestCase):
    def test_world_import(self):
        """Tests that every game currently in /worlds can be imported."""
        import worlds
        self.assertEqual([], worlds.failed_world_loads)
