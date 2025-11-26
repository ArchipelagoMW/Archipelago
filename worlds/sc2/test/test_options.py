import unittest
from typing import Dict

from .. import options
from ..item import item_parents


class TestOptions(unittest.TestCase):

    def test_unit_max_upgrades_matching_items(self) -> None:
        upgrade_group_to_count: Dict[str, int] = {}
        for parent_id, child_list in item_parents.parent_id_to_children.items():
            main_parent = item_parents.parent_present[parent_id].constraint_group
            if main_parent is None:
                continue
            upgrade_group_to_count.setdefault(main_parent, 0)
            upgrade_group_to_count[main_parent] += len(child_list)

        self.assertEqual(options.MAX_UPGRADES_OPTION, max(upgrade_group_to_count.values()))
