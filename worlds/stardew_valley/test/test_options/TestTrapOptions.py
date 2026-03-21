from ...items import items_by_group, Group
from ...options import TrapDifficulty
from ...test.bases import SVTestCase, solo_multiworld
from ...test.options.presets import allsanity_mods_7_x_x, allsanity_no_mods_7_x_x


class TestTraps(SVTestCase):
    def test_given_no_traps_when_generate_then_no_trap_in_pool(self):
        world_options = allsanity_no_mods_7_x_x().copy()
        world_options[TrapDifficulty.internal_name] = TrapDifficulty.option_no_traps
        with solo_multiworld(world_options) as (multi_world, _):
            trap_items = [item_data.name for item_data in items_by_group[Group.TRAP]]
            multiworld_items = [item.name for item in multi_world.get_items()]

            for item in trap_items:
                with self.subTest(f"{item}"):
                    self.assertNotIn(item, multiworld_items)

    def test_given_traps_when_generate_then_all_traps_in_pool(self):
        trap_option = TrapDifficulty
        world_options = allsanity_mods_7_x_x()
        world_options.update({TrapDifficulty.internal_name: trap_option.option_easy})
        with solo_multiworld(world_options) as (multi_world, _):
            trap_items = [item_data.name for item_data in items_by_group[Group.TRAP] if Group.DEPRECATED not in item_data.groups]
            multiworld_items = [item.name for item in multi_world.get_items()]
            for item in trap_items:
                with self.subTest(f"Item: {item}"):
                    self.assertIn(item, multiworld_items)