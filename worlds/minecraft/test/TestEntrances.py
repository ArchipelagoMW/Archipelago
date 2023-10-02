from . import MCTestBase


class TestEntrances(MCTestBase): 
    options = {
        "shuffle_structures": False,
        "structure_compasses": False
    }

    def testPortals(self): 
        self.run_entrance_tests([
            ['Nether Portal', False, []],
            ['Nether Portal', False, [], ['Flint and Steel']],
            ['Nether Portal', False, [], ['Progressive Resource Crafting']],
            ['Nether Portal', False, [], ['Progressive Tools']],
            ['Nether Portal', False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ['Nether Portal', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Bucket']],
            ['Nether Portal', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools']],

            ['End Portal', False, []],
            ['End Portal', False, [], ['Brewing']],
            ['End Portal', False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ['End Portal', False, [], ['Flint and Steel']],
            ['End Portal', False, [], ['Progressive Resource Crafting']],
            ['End Portal', False, [], ['Progressive Tools']],
            ['End Portal', False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ['End Portal', False, [], ['Progressive Weapons']],
            ['End Portal', False, [], ['Progressive Armor', 'Shield']],
            ['End Portal', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Bucket', 
                                  'Progressive Weapons', 'Progressive Armor', 
                                  'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']], 
            ['End Portal', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Bucket', 
                                  'Progressive Weapons', 'Shield', 
                                  'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']], 
            ['End Portal', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 
                                  'Progressive Weapons', 'Progressive Armor', 
                                  'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']], 
            ['End Portal', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 
                                  'Progressive Weapons', 'Shield', 
                                  'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']], 
            ])

    def testStructures(self): 
        self.run_entrance_tests([ # Structures 1 and 2 should be logically equivalent
            ['Overworld Structure 1', False, []],
            ['Overworld Structure 1', False, [], ['Progressive Weapons']],
            ['Overworld Structure 1', False, [], ['Progressive Resource Crafting', 'Campfire']],
            ['Overworld Structure 1', True, ['Progressive Weapons', 'Progressive Resource Crafting']],
            ['Overworld Structure 1', True, ['Progressive Weapons', 'Campfire']],

            ['Overworld Structure 2', False, []],
            ['Overworld Structure 2', False, [], ['Progressive Weapons']],
            ['Overworld Structure 2', False, [], ['Progressive Resource Crafting', 'Campfire']],
            ['Overworld Structure 2', True, ['Progressive Weapons', 'Progressive Resource Crafting']],
            ['Overworld Structure 2', True, ['Progressive Weapons', 'Campfire']],

            ['Nether Structure 1', False, []],
            ['Nether Structure 1', False, [], ['Flint and Steel']],
            ['Nether Structure 1', False, [], ['Progressive Resource Crafting']],
            ['Nether Structure 1', False, [], ['Progressive Tools']],
            ['Nether Structure 1', False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ['Nether Structure 1', False, [], ['Progressive Weapons']],
            ['Nether Structure 1', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Bucket', 'Progressive Weapons']],
            ['Nether Structure 1', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons']],

            ['Nether Structure 2', False, []],
            ['Nether Structure 2', False, [], ['Flint and Steel']],
            ['Nether Structure 2', False, [], ['Progressive Resource Crafting']],
            ['Nether Structure 2', False, [], ['Progressive Tools']],
            ['Nether Structure 2', False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ['Nether Structure 2', False, [], ['Progressive Weapons']],
            ['Nether Structure 2', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Bucket', 'Progressive Weapons']],
            ['Nether Structure 2', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons']],

            ['The End Structure', False, []],
            ['The End Structure', False, [], ['Brewing']],
            ['The End Structure', False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ['The End Structure', False, [], ['Flint and Steel']],
            ['The End Structure', False, [], ['Progressive Resource Crafting']],
            ['The End Structure', False, [], ['Progressive Tools']],
            ['The End Structure', False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ['The End Structure', False, [], ['Progressive Weapons']],
            ['The End Structure', False, [], ['Progressive Armor', 'Shield']],
            ['The End Structure', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Bucket', 
                                  'Progressive Weapons', 'Progressive Armor', 
                                  'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']], 
            ['The End Structure', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Bucket', 
                                  'Progressive Weapons', 'Shield', 
                                  'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']], 
            ['The End Structure', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 
                                  'Progressive Weapons', 'Progressive Armor', 
                                  'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']], 
            ['The End Structure', True, ['Flint and Steel', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 
                                  'Progressive Weapons', 'Shield', 
                                  'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']], 

            ])