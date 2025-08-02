from .bases import SVTestBase
from .. import options, item_table, Group

max_iterations = 2000


class TestItemLinksEverythingIncluded(SVTestBase):
    options = {options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
               options.TrapDifficulty.internal_name: options.TrapDifficulty.option_medium}

    def test_filler_of_all_types_generated(self):
        max_number_filler = 114
        filler_generated = []
        at_least_one_trap = False
        at_least_one_island = False
        for i in range(0, max_iterations):
            filler = self.multiworld.worlds[1].get_filler_item_name()
            if filler in filler_generated:
                continue
            filler_generated.append(filler)
            self.assertNotIn(Group.MAXIMUM_ONE, item_table[filler].groups)
            self.assertNotIn(Group.AT_LEAST_TWO, item_table[filler].groups)
            if Group.TRAP in item_table[filler].groups:
                at_least_one_trap = True
            if Group.GINGER_ISLAND in item_table[filler].groups:
                at_least_one_island = True
            if len(filler_generated) >= max_number_filler:
                break
        self.assertTrue(at_least_one_trap)
        self.assertTrue(at_least_one_island)
        self.assertGreaterEqual(len(filler_generated), max_number_filler)


class TestItemLinksNoIsland(SVTestBase):
    options = {options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
               options.TrapDifficulty.internal_name: options.TrapDifficulty.option_medium}

    def test_filler_has_no_island_but_has_traps(self):
        max_number_filler = 109
        filler_generated = []
        at_least_one_trap = False
        for i in range(0, max_iterations):
            filler = self.multiworld.worlds[1].get_filler_item_name()
            if filler in filler_generated:
                continue
            filler_generated.append(filler)
            self.assertNotIn(Group.GINGER_ISLAND, item_table[filler].groups)
            self.assertNotIn(Group.MAXIMUM_ONE, item_table[filler].groups)
            self.assertNotIn(Group.AT_LEAST_TWO, item_table[filler].groups)
            if Group.TRAP in item_table[filler].groups:
                at_least_one_trap = True
            if len(filler_generated) >= max_number_filler:
                break
        self.assertTrue(at_least_one_trap)
        self.assertGreaterEqual(len(filler_generated), max_number_filler)


class TestItemLinksNoTraps(SVTestBase):
    options = {options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
               options.TrapDifficulty.internal_name: options.TrapDifficulty.option_no_traps}

    def test_filler_has_no_traps_but_has_island(self):
        max_number_filler = 99
        filler_generated = []
        at_least_one_island = False
        for i in range(0, max_iterations):
            filler = self.multiworld.worlds[1].get_filler_item_name()
            if filler in filler_generated:
                continue
            filler_generated.append(filler)
            self.assertNotIn(Group.TRAP, item_table[filler].groups)
            self.assertNotIn(Group.MAXIMUM_ONE, item_table[filler].groups)
            self.assertNotIn(Group.AT_LEAST_TWO, item_table[filler].groups)
            if Group.GINGER_ISLAND in item_table[filler].groups:
                at_least_one_island = True
            if len(filler_generated) >= max_number_filler:
                break
        self.assertTrue(at_least_one_island)
        self.assertGreaterEqual(len(filler_generated), max_number_filler)


class TestItemLinksNoTrapsAndIsland(SVTestBase):
    options = {options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
               options.TrapDifficulty.internal_name: options.TrapDifficulty.option_no_traps}

    def test_filler_generated_without_island_or_traps(self):
        max_number_filler = 94
        filler_generated = []
        for i in range(0, max_iterations):
            filler = self.multiworld.worlds[1].get_filler_item_name()
            if filler in filler_generated:
                continue
            filler_generated.append(filler)
            self.assertNotIn(Group.GINGER_ISLAND, item_table[filler].groups)
            self.assertNotIn(Group.TRAP, item_table[filler].groups)
            self.assertNotIn(Group.MAXIMUM_ONE, item_table[filler].groups)
            self.assertNotIn(Group.AT_LEAST_TWO, item_table[filler].groups)
            if len(filler_generated) >= max_number_filler:
                break
        self.assertGreaterEqual(len(filler_generated), max_number_filler)
