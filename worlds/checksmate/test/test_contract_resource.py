import unittest
from unittest import mock

from ..apmw_projection import resource


class TestContractResource(unittest.TestCase):
    def tearDown(self):
        resource.frozen_contract_text.cache_clear()
        resource.load_frozen_contract.cache_clear()
        resource._frozen_contract_document.cache_clear()
        resource.load_frozen_contract()

    def test_text_and_typed_contract_are_loaded_and_parsed_once(self):
        resource.frozen_contract_text.cache_clear()
        with mock.patch.object(
            resource.resources, "files", wraps=resource.resources.files
        ) as files:
            first_text = resource.frozen_contract_text()
            self.assertIs(first_text, resource.frozen_contract_text())
            self.assertEqual(1, files.call_count)

        resource.load_frozen_contract.cache_clear()
        with (
            mock.patch.object(
                resource, "frozen_contract_text", return_value=first_text
            ) as load_text,
            mock.patch.object(
                resource, "parse_contract", wraps=resource.parse_contract
            ) as parse,
        ):
            first_contract = resource.load_frozen_contract()
            second_contract = resource.load_frozen_contract()

        self.assertIs(first_contract, second_contract)
        self.assertEqual(1, load_text.call_count)
        self.assertEqual(1, parse.call_count)
        with self.assertRaises(TypeError):
            first_contract.expected_material["pawn"] = 0
        with self.assertRaises(TypeError):
            first_contract.effective_item_maxima["common"]["Play as White"] = 0

    def test_documents_are_fresh_copies_of_one_cached_parse(self):
        resource._frozen_contract_document.cache_clear()
        with mock.patch.object(
            resource.json, "loads", wraps=resource.json.loads
        ) as loads:
            first = resource.frozen_contract_document()
            second = resource.frozen_contract_document()

        self.assertEqual(1, loads.call_count)
        self.assertIsNot(first, second)
        self.assertIsNot(first["geometry"], second["geometry"])
        first["geometry"]["base"]["files"] = 99
        self.assertEqual(8, second["geometry"]["base"]["files"])
        self.assertEqual(
            8,
            resource.frozen_contract_document()["geometry"]["base"]["files"],
        )


if __name__ == "__main__":
    unittest.main()
