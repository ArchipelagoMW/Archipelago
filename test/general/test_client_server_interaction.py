import unittest

from Utils import get_intended_text, get_input_text_from_response


class TestClient(unittest.TestCase):
    def test_autofill_hint_from_fuzzy_hint(self) -> None:
        tests = (
            ("item", ["item1", "item2"]),  # Multiple close matches
            ("itm", ["item1", "item21"]),  # No close match, multiple option
            ("item", ["item1"]),  # No close match, single option
            ("item", ["\"item\" 'item' (item)"]),  # Testing different special characters
        )

        for input_text, possible_answers in tests:
            item_name, usable, response = get_intended_text(input_text, possible_answers)
            self.assertFalse(usable, "This test must be updated, it seems get_fuzzy_results behavior changed")

            hint_command = get_input_text_from_response(response, "!hint")
            self.assertIsNotNone(hint_command,
                                 "The response to fuzzy hints is no longer recognized by the hint autofill")
            self.assertEqual(hint_command, f"!hint {item_name}",
                             "The hint command autofilled by the response is not correct")
