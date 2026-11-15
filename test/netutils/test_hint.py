import pickle
import unittest
from types import SimpleNamespace

from NetUtils import Hint, HintStatus
from Utils import restricted_loads


class TestHintPickling(unittest.TestCase):
    hint = Hint(1, 2, 100, 200, False, "Test Entrance", 1, HintStatus.HINT_PRIORITY)

    def test_save_roundtrip_preserves_concealment(self):
        for hidden, item_hidden in ((False, False), (True, False), (False, True), (True, True)):
            hint = self.hint._replace(hidden=hidden, item_hidden=item_hidden)
            savedata = {"hints": {(0, 1): {hint}}}
            with self.subTest(hidden=hidden, item_hidden=item_hidden):
                loaded = restricted_loads(pickle.dumps(savedata))
                self.assertEqual(loaded, savedata)
                self.assertIsInstance(next(iter(loaded["hints"][0, 1])), Hint)


class TestHintRendering(unittest.TestCase):
    hint = Hint(1, 2, 100, 200, False, "Test Entrance", 1, HintStatus.HINT_PRIORITY)

    def test_rendering_conceals_requested_details(self):
        for hidden, item_hidden in ((False, False), (True, False), (False, True)):
            with self.subTest(hidden=hidden, item_hidden=item_hidden):
                message = self.hint._replace(hidden=hidden, item_hidden=item_hidden).as_network_message()
                types = {part.get("type") for part in message["data"]}
                self.assertEqual("location_id" in types, not hidden)
                self.assertEqual("entrance_name" in types, not hidden)
                self.assertEqual("item_id" in types, not item_hidden)
                self.assertIn("hint_status", types)
                if item_hidden:
                    self.assertIn("progression", "".join(str(part["text"]) for part in message["data"]))

    def test_checked_location_reveals_both_flags(self):
        context = SimpleNamespace(location_checks={(0, self.hint.finding_player): {self.hint.location}})
        checked = self.hint._replace(hidden=True, item_hidden=True).re_check(context, 0)
        self.assertTrue(checked.found)
        self.assertEqual(checked.status, HintStatus.HINT_FOUND)
        self.assertFalse(checked.hidden)
        self.assertFalse(checked.item_hidden)
