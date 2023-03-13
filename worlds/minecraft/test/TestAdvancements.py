from . import MCTestBase


# Format:
# [location, expected_result, given_items, [excluded_items]]
# Every advancement has its own test, named by its internal ID number. 
class TestAdvancements(MCTestBase):
    options = {
        "shuffle_structures": False,
        "structure_compasses": False
    }

    def test_42000(self):
        self.run_location_tests([
            ["Who is Cutting Onions?", False, []], 
            ["Who is Cutting Onions?", False, [], ['Progressive Resource Crafting']], 
            ["Who is Cutting Onions?", False, [], ['Flint and Steel']], 
            ["Who is Cutting Onions?", False, [], ['Progressive Tools']], 
            ["Who is Cutting Onions?", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Who is Cutting Onions?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["Who is Cutting Onions?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42001(self):
        self.run_location_tests([
            ["Oh Shiny", False, []],
            ["Oh Shiny", False, [], ['Progressive Resource Crafting']],
            ["Oh Shiny", False, [], ['Flint and Steel']],
            ["Oh Shiny", False, [], ['Progressive Tools']],
            ["Oh Shiny", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Oh Shiny", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']],
            ["Oh Shiny", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42002(self):
        self.run_location_tests([
            ["Suit Up", False, []],
            ["Suit Up", False, [], ["Progressive Armor"]],
            ["Suit Up", False, [], ["Progressive Resource Crafting"]],
            ["Suit Up", False, [], ["Progressive Tools"]],
            ["Suit Up", True, ["Progressive Armor", "Progressive Resource Crafting", "Progressive Tools"]],
            ])

    def test_42003(self):
        self.run_location_tests([
            ["Very Very Frightening", False, []],
            ["Very Very Frightening", False, [], ['Channeling Book']],
            ["Very Very Frightening", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["Very Very Frightening", False, [], ['Enchanting']],
            ["Very Very Frightening", False, [], ['Progressive Tools']],
            ["Very Very Frightening", False, [], ['Progressive Weapons']],
            ["Very Very Frightening", True, ['Progressive Weapons', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools',
                                             'Enchanting', 'Progressive Resource Crafting', 'Progressive Resource Crafting', 'Channeling Book']],
            ])

    def test_42004(self):
        self.run_location_tests([
            ["Hot Stuff", False, []],
            ["Hot Stuff", False, [], ["Bucket"]],
            ["Hot Stuff", False, [], ["Progressive Resource Crafting"]],
            ["Hot Stuff", False, [], ["Progressive Tools"]],
            ["Hot Stuff", True, ["Bucket", "Progressive Resource Crafting", "Progressive Tools"]],
            ])

    def test_42005(self):
        self.run_location_tests([
            ["Free the End", False, []],
            ["Free the End", False, [], ['Progressive Resource Crafting']],
            ["Free the End", False, [], ['Flint and Steel']],
            ["Free the End", False, [], ['Progressive Tools']],
            ["Free the End", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["Free the End", False, [], ['Progressive Armor']],
            ["Free the End", False, [], ['Brewing']],
            ["Free the End", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Free the End", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["Free the End", False, [], ['Archery']],
            ["Free the End", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                    'Progressive Weapons', 'Progressive Weapons', 'Archery', 'Progressive Armor',
                                    'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Free the End", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                    'Progressive Weapons', 'Progressive Weapons', 'Archery', 'Progressive Armor',
                                    'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42006(self):
        self.run_location_tests([
            ["A Furious Cocktail", False, []],
            ["A Furious Cocktail", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["A Furious Cocktail", False, [], ['Flint and Steel']],
            ["A Furious Cocktail", False, [], ['Progressive Tools']],
            ["A Furious Cocktail", False, [], ['Progressive Weapons']],
            ["A Furious Cocktail", False, [], ['Progressive Armor', 'Shield']],
            ["A Furious Cocktail", False, [], ['Brewing']],
            ["A Furious Cocktail", False, [], ['Bottles']],
            ["A Furious Cocktail", False, [], ['Fishing Rod']],
            ["A Furious Cocktail", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["A Furious Cocktail", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting',
                                             'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                             'Progressive Weapons', 'Progressive Weapons', 'Progressive Weapons',
                                             'Progressive Armor', 'Progressive Armor',
                                             'Enchanting', 'Brewing', 'Bottles', 'Fishing Rod']],
            ])

    def test_42007(self):
        self.run_location_tests([
            ["Best Friends Forever", True, []],
            ])

    def test_42008(self):
        self.run_location_tests([
            ["Bring Home the Beacon", False, []],
            ["Bring Home the Beacon", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["Bring Home the Beacon", False, [], ['Flint and Steel']],
            ["Bring Home the Beacon", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Bring Home the Beacon", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["Bring Home the Beacon", False, ['Progressive Armor'], ['Progressive Armor']],
            ["Bring Home the Beacon", False, [], ['Enchanting']],
            ["Bring Home the Beacon", False, [], ['Brewing']],
            ["Bring Home the Beacon", False, [], ['Bottles']],
            ["Bring Home the Beacon", True, [], ['Bucket']],
            ["Bring Home the Beacon", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting',
                                             'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                             'Progressive Weapons', 'Progressive Weapons', 'Progressive Weapons',
                                             'Progressive Armor', 'Progressive Armor',
                                             'Enchanting', 'Brewing', 'Bottles']],
            ])

    def test_42009(self):
        self.run_location_tests([
            ["Not Today, Thank You", False, []],
            ["Not Today, Thank You", False, [], ["Shield"]],
            ["Not Today, Thank You", False, [], ["Progressive Resource Crafting"]],
            ["Not Today, Thank You", False, [], ["Progressive Tools"]],
            ["Not Today, Thank You", True, ["Shield", "Progressive Resource Crafting", "Progressive Tools"]],
            ])

    def test_42010(self):
        self.run_location_tests([
            ["Isn't It Iron Pick", False, []],
            ["Isn't It Iron Pick", True, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]],
            ["Isn't It Iron Pick", False, [], ["Progressive Tools", "Progressive Tools"]],
            ["Isn't It Iron Pick", False, [], ["Progressive Resource Crafting"]],
            ["Isn't It Iron Pick", False, ["Progressive Tools", "Progressive Resource Crafting"]],
            ["Isn't It Iron Pick", True, ["Progressive Tools", "Progressive Tools", "Progressive Resource Crafting"]],
            ])

    def test_42011(self):
        self.run_location_tests([
            ["Local Brewery", False, []],
            ["Local Brewery", False, [], ['Progressive Resource Crafting']],
            ["Local Brewery", False, [], ['Flint and Steel']],
            ["Local Brewery", False, [], ['Progressive Tools']],
            ["Local Brewery", False, [], ['Progressive Weapons']],
            ["Local Brewery", False, [], ['Progressive Armor', 'Shield']],
            ["Local Brewery", False, [], ['Brewing']],
            ["Local Brewery", False, [], ['Bottles']],
            ["Local Brewery", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Local Brewery", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                     'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']],
            ["Local Brewery", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                     'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']],
            ["Local Brewery", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                     'Progressive Weapons', 'Shield', 'Brewing', 'Bottles']],
            ["Local Brewery", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                     'Progressive Weapons', 'Shield', 'Brewing', 'Bottles']],
            ])

    def test_42012(self):
        self.run_location_tests([
            ["The Next Generation", False, []],
            ["The Next Generation", False, [], ['Progressive Resource Crafting']],
            ["The Next Generation", False, [], ['Flint and Steel']],
            ["The Next Generation", False, [], ['Progressive Tools']],
            ["The Next Generation", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["The Next Generation", False, [], ['Progressive Armor']],
            ["The Next Generation", False, [], ['Brewing']],
            ["The Next Generation", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["The Next Generation", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["The Next Generation", False, [], ['Archery']],
            ["The Next Generation", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                           'Progressive Weapons', 'Progressive Weapons', 'Archery', 'Progressive Armor',
                                           'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The Next Generation", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                           'Progressive Weapons', 'Progressive Weapons', 'Archery', 'Progressive Armor',
                                           'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42013(self):
        self.run_location_tests([
            ["Fishy Business", False, []],
            ["Fishy Business", False, [], ['Fishing Rod']],
            ["Fishy Business", True, ['Fishing Rod']],
            ])

    def test_42014(self):
        self.run_location_tests([
            ["Hot Tourist Destinations", False, []],
            ["Hot Tourist Destinations", False, [], ['Progressive Resource Crafting']],
            ["Hot Tourist Destinations", False, [], ['Flint and Steel']],
            ["Hot Tourist Destinations", False, [], ['Progressive Tools']],
            ["Hot Tourist Destinations", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Hot Tourist Destinations", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']],
            ["Hot Tourist Destinations", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42015(self):
        self.run_location_tests([
            ["This Boat Has Legs", False, []],
            ["This Boat Has Legs", False, [], ['Progressive Resource Crafting']],
            ["This Boat Has Legs", False, [], ['Flint and Steel']],
            ["This Boat Has Legs", False, [], ['Progressive Tools']],
            ["This Boat Has Legs", False, [], ['Progressive Weapons']],
            ["This Boat Has Legs", False, [], ['Progressive Armor', 'Shield']],
            ["This Boat Has Legs", False, [], ['Fishing Rod']],
            ["This Boat Has Legs", False, [], ['Saddle']],
            ["This Boat Has Legs", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["This Boat Has Legs", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor', 'Flint and Steel', 'Bucket', 'Fishing Rod']],
            ["This Boat Has Legs", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Fishing Rod']],
            ["This Boat Has Legs", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Weapons', 'Shield', 'Flint and Steel', 'Bucket', 'Fishing Rod']],
            ["This Boat Has Legs", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Weapons', 'Shield', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Fishing Rod']],
            ])

    def test_42016(self):
        self.run_location_tests([
            ["Sniper Duel", False, []],
            ["Sniper Duel", False, [], ['Archery']],
            ["Sniper Duel", True, ['Archery']],
            ])

    def test_42017(self):
        self.run_location_tests([
            ["Nether", False, []],
            ["Nether", False, [], ['Progressive Resource Crafting']],
            ["Nether", False, [], ['Flint and Steel']],
            ["Nether", False, [], ['Progressive Tools']],
            ["Nether", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Nether", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']],
            ["Nether", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42018(self):
        self.run_location_tests([
            ["Great View From Up Here", False, []],
            ["Great View From Up Here", False, [], ['Progressive Resource Crafting']],
            ["Great View From Up Here", False, [], ['Flint and Steel']],
            ["Great View From Up Here", False, [], ['Progressive Tools']],
            ["Great View From Up Here", False, [], ['Progressive Weapons']],
            ["Great View From Up Here", False, [], ['Progressive Armor', 'Shield']],
            ["Great View From Up Here", False, [], ['Brewing']],
            ["Great View From Up Here", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Great View From Up Here", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["Great View From Up Here", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                               'Progressive Weapons', 'Progressive Armor',
                                               'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Great View From Up Here", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                               'Progressive Weapons', 'Progressive Armor',
                                               'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Great View From Up Here", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                               'Progressive Weapons', 'Shield',
                                               'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Great View From Up Here", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                               'Progressive Weapons', 'Shield',
                                               'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42019(self):
        self.run_location_tests([
            ["How Did We Get Here?", False, []],
            ["How Did We Get Here?", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["How Did We Get Here?", False, [], ['Flint and Steel']],
            ["How Did We Get Here?", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["How Did We Get Here?", False, ['Progressive Weapons', 'Progressive Weapons'], ['Progressive Weapons']],
            ["How Did We Get Here?", False, ['Progressive Armor'], ['Progressive Armor']],
            ["How Did We Get Here?", False, [], ['Shield']],
            ["How Did We Get Here?", False, [], ['Enchanting']],
            ["How Did We Get Here?", False, [], ['Brewing']],
            ["How Did We Get Here?", False, [], ['Bottles']],
            ["How Did We Get Here?", False, [], ['Archery']],
            ["How Did We Get Here?", False, [], ['Fishing Rod']],
            ["How Did We Get Here?", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["How Did We Get Here?", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting', 'Flint and Steel',
                                            'Progressive Tools', 'Progressive Tools', 'Progressive Tools',
                                            'Progressive Weapons', 'Progressive Weapons', 'Progressive Weapons',
                                            'Progressive Armor', 'Progressive Armor', 'Shield',
                                            'Enchanting', 'Brewing', 'Archery', 'Bottles', 'Fishing Rod',
                                            '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42020(self):
        self.run_location_tests([
            ["Bullseye", False, []],
            ["Bullseye", False, [], ['Archery']],
            ["Bullseye", False, [], ['Progressive Resource Crafting']],
            ["Bullseye", False, [], ['Progressive Tools']],
            ["Bullseye", True, ['Progressive Tools', 'Progressive Tools', 'Progressive Resource Crafting', 'Archery']],
            ])

    def test_42021(self):
        self.run_location_tests([
            ["Spooky Scary Skeleton", False, []],
            ["Spooky Scary Skeleton", False, [], ['Progressive Resource Crafting']],
            ["Spooky Scary Skeleton", False, [], ['Flint and Steel']],
            ["Spooky Scary Skeleton", False, [], ['Progressive Tools']],
            ["Spooky Scary Skeleton", False, [], ['Progressive Weapons']],
            ["Spooky Scary Skeleton", False, [], ['Progressive Armor', 'Shield']],
            ["Spooky Scary Skeleton", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Spooky Scary Skeleton", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor']],
            ["Spooky Scary Skeleton", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor']],
            ["Spooky Scary Skeleton", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Shield']],
            ["Spooky Scary Skeleton", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Shield']],
            ])

    def test_42022(self):
        self.run_location_tests([
            ["Two by Two", False, []],
            ["Two by Two", False, [], ['Progressive Resource Crafting']],
            ["Two by Two", False, [], ['Flint and Steel']],
            ["Two by Two", False, [], ['Progressive Tools']],
            ["Two by Two", False, [], ['Progressive Weapons']],
            ["Two by Two", False, [], ['Bucket']],
            ["Two by Two", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Two by Two", False, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons']],
            ["Two by Two", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons']],
            ])

    def test_42023(self):
        self.run_location_tests([
            ["Stone Age", True, []],
            ])

    def test_42024(self):
        self.run_location_tests([
            ["Two Birds, One Arrow", False, []],
            ["Two Birds, One Arrow", False, [], ['Archery']],
            ["Two Birds, One Arrow", False, [], ['Progressive Resource Crafting']],
            ["Two Birds, One Arrow", False, ['Progressive Tools'], ['Progressive Tools', 'Progressive Tools']],
            ["Two Birds, One Arrow", False, [], ['Enchanting']],
            ["Two Birds, One Arrow", True, ['Archery', 'Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Enchanting']],
            ])

    def test_42025(self):
        self.run_location_tests([
            ["We Need to Go Deeper", False, []],
            ["We Need to Go Deeper", False, [], ['Progressive Resource Crafting']],
            ["We Need to Go Deeper", False, [], ['Flint and Steel']],
            ["We Need to Go Deeper", False, [], ['Progressive Tools']],
            ["We Need to Go Deeper", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["We Need to Go Deeper", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']],
            ["We Need to Go Deeper", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42026(self):
        self.run_location_tests([
            ["Who's the Pillager Now?", False, []],
            ["Who's the Pillager Now?", False, [], ['Archery']],
            ["Who's the Pillager Now?", False, [], ['Progressive Resource Crafting']],
            ["Who's the Pillager Now?", False, [], ['Progressive Tools']],
            ["Who's the Pillager Now?", False, [], ['Progressive Weapons']],
            ["Who's the Pillager Now?", True, ['Archery', 'Progressive Tools', 'Progressive Weapons', 'Progressive Resource Crafting']],
            ])

    def test_42027(self):
        self.run_location_tests([
            ["Getting an Upgrade", False, []],
            ["Getting an Upgrade", True, ["Progressive Tools"]],
            ])

    def test_42028(self):
        self.run_location_tests([
            ["Tactical Fishing", False, []],
            ["Tactical Fishing", False, [], ['Progressive Resource Crafting']],
            ["Tactical Fishing", False, [], ['Progressive Tools']],
            ["Tactical Fishing", False, [], ['Bucket']],
            ["Tactical Fishing", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Bucket']],
            ])

    def test_42029(self):
        self.run_location_tests([
            ["Zombie Doctor", False, []],
            ["Zombie Doctor", False, [], ['Progressive Resource Crafting']],
            ["Zombie Doctor", False, [], ['Flint and Steel']],
            ["Zombie Doctor", False, [], ['Progressive Tools']],
            ["Zombie Doctor", False, [], ['Progressive Weapons']],
            ["Zombie Doctor", False, [], ['Progressive Armor', 'Shield']],
            ["Zombie Doctor", False, [], ['Brewing']],
            ["Zombie Doctor", False, [], ['Bottles']],
            ["Zombie Doctor", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Zombie Doctor", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                     'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']],
            ["Zombie Doctor", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                     'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']],
            ["Zombie Doctor", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                     'Progressive Weapons', 'Shield', 'Brewing', 'Bottles']],
            ["Zombie Doctor", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                     'Progressive Weapons', 'Shield', 'Brewing', 'Bottles']],
            ])

    def test_42030(self):
        self.run_location_tests([
            ["The City at the End of the Game", False, []],
            ["The City at the End of the Game", False, [], ['Progressive Resource Crafting']],
            ["The City at the End of the Game", False, [], ['Flint and Steel']],
            ["The City at the End of the Game", False, [], ['Progressive Tools']],
            ["The City at the End of the Game", False, [], ['Progressive Weapons']],
            ["The City at the End of the Game", False, [], ['Progressive Armor', 'Shield']],
            ["The City at the End of the Game", False, [], ['Brewing']],
            ["The City at the End of the Game", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["The City at the End of the Game", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["The City at the End of the Game", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                                       'Progressive Weapons', 'Progressive Armor',
                                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The City at the End of the Game", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                                       'Progressive Weapons', 'Progressive Armor',
                                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The City at the End of the Game", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                                       'Progressive Weapons', 'Shield',
                                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The City at the End of the Game", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                                       'Progressive Weapons', 'Shield',
                                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42031(self):
        self.run_location_tests([
            ["Ice Bucket Challenge", False, []],
            ["Ice Bucket Challenge", False, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]],
            ["Ice Bucket Challenge", False, [], ["Progressive Resource Crafting"]],
            ["Ice Bucket Challenge", True, ["Progressive Tools", "Progressive Tools", "Progressive Tools", "Progressive Resource Crafting"]],
            ])

    def test_42032(self):
        self.run_location_tests([
            ["Remote Getaway", False, []],
            ["Remote Getaway", False, [], ['Progressive Resource Crafting']],
            ["Remote Getaway", False, [], ['Flint and Steel']],
            ["Remote Getaway", False, [], ['Progressive Tools']],
            ["Remote Getaway", False, [], ['Progressive Weapons']],
            ["Remote Getaway", False, [], ['Progressive Armor', 'Shield']],
            ["Remote Getaway", False, [], ['Brewing']],
            ["Remote Getaway", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Remote Getaway", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["Remote Getaway", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                      'Progressive Weapons', 'Progressive Armor',
                                      'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Remote Getaway", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                      'Progressive Weapons', 'Progressive Armor',
                                      'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Remote Getaway", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                      'Progressive Weapons', 'Shield',
                                      'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Remote Getaway", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                      'Progressive Weapons', 'Shield',
                                      'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42033(self):
        self.run_location_tests([
            ["Into Fire", False, []],
            ["Into Fire", False, [], ['Progressive Resource Crafting']],
            ["Into Fire", False, [], ['Flint and Steel']],
            ["Into Fire", False, [], ['Progressive Tools']],
            ["Into Fire", False, [], ['Progressive Weapons']],
            ["Into Fire", False, [], ['Progressive Armor', 'Shield']],
            ["Into Fire", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Into Fire", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor']],
            ["Into Fire", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor']],
            ["Into Fire", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Shield']],
            ["Into Fire", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Shield']],
            ])

    def test_42034(self):
        self.run_location_tests([
            ["War Pigs", False, []],
            ["War Pigs", False, [], ['Progressive Resource Crafting']],
            ["War Pigs", False, [], ['Flint and Steel']],
            ["War Pigs", False, [], ['Progressive Tools']],
            ["War Pigs", False, [], ['Progressive Weapons']],
            ["War Pigs", False, [], ['Progressive Armor', 'Shield']],
            ["War Pigs", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["War Pigs", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Shield']],
            ["War Pigs", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Shield']],
            ])

    def test_42035(self):
        self.run_location_tests([
            ["Take Aim", False, []],
            ["Take Aim", False, [], ['Archery']],
            ["Take Aim", True, ['Archery']],
            ])

    def test_42036(self):
        self.run_location_tests([
            ["Total Beelocation", False, []],
            ["Total Beelocation", False, [], ['Enchanting']],
            ["Total Beelocation", False, [], ['Silk Touch Book']],
            ["Total Beelocation", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["Total Beelocation", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Total Beelocation", True, ['Enchanting', 'Silk Touch Book', 'Progressive Resource Crafting', 'Progressive Resource Crafting',
                                         'Progressive Tools', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42037(self):
        self.run_location_tests([
            ["Arbalistic", False, []],
            ["Arbalistic", False, [], ['Enchanting']],
            ["Arbalistic", False, [], ['Piercing IV Book']],
            ["Arbalistic", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["Arbalistic", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Arbalistic", False, [], ['Archery']],
            ["Arbalistic", True, ['Enchanting', 'Piercing IV Book', 'Progressive Resource Crafting', 'Progressive Resource Crafting',
                                  'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Archery']],
            ])

    def test_42038(self):
        self.run_location_tests([
            ["The End... Again...", False, []],
            ["The End... Again...", False, [], ['Progressive Resource Crafting']],
            ["The End... Again...", False, [], ['Flint and Steel']],
            ["The End... Again...", False, [], ['Progressive Tools']],
            ["The End... Again...", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["The End... Again...", False, [], ['Progressive Armor']],
            ["The End... Again...", False, [], ['Brewing']],
            ["The End... Again...", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["The End... Again...", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["The End... Again...", False, [], ['Archery']],
            ["The End... Again...", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                           'Progressive Weapons', 'Progressive Weapons', 'Archery', 'Progressive Armor',
                                           'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The End... Again...", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                           'Progressive Weapons', 'Progressive Weapons', 'Archery', 'Progressive Armor',
                                           'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42039(self):
        self.run_location_tests([
            ["Acquire Hardware", False, []],
            ["Acquire Hardware", False, [], ["Progressive Tools"]],
            ["Acquire Hardware", False, [], ["Progressive Resource Crafting"]],
            ["Acquire Hardware", True, ["Progressive Tools", "Progressive Resource Crafting"]],
            ])

    def test_42040(self):
        self.run_location_tests([
            ["Not Quite \"Nine\" Lives", False, []],
            ["Not Quite \"Nine\" Lives", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["Not Quite \"Nine\" Lives", False, [], ['Flint and Steel']],
            ["Not Quite \"Nine\" Lives", False, [], ['Progressive Tools']],
            ["Not Quite \"Nine\" Lives", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Not Quite \"Nine\" Lives", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']],
            ["Not Quite \"Nine\" Lives", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42041(self):
        self.run_location_tests([
            ["Cover Me With Diamonds", False, []],
            ["Cover Me With Diamonds", False, ['Progressive Armor'], ['Progressive Armor']],
            ["Cover Me With Diamonds", False, ['Progressive Tools'], ['Progressive Tools', 'Progressive Tools']],
            ["Cover Me With Diamonds", False, [], ['Progressive Resource Crafting']],
            ["Cover Me With Diamonds", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Armor', 'Progressive Armor']],
            ])

    def test_42042(self):
        self.run_location_tests([
            ["Sky's the Limit", False, []],
            ["Sky's the Limit", False, [], ['Progressive Resource Crafting']],
            ["Sky's the Limit", False, [], ['Flint and Steel']],
            ["Sky's the Limit", False, [], ['Progressive Tools']],
            ["Sky's the Limit", False, [], ['Progressive Weapons']],
            ["Sky's the Limit", False, [], ['Progressive Armor', 'Shield']],
            ["Sky's the Limit", False, [], ['Brewing']],
            ["Sky's the Limit", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Sky's the Limit", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["Sky's the Limit", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                       'Progressive Weapons', 'Progressive Armor',
                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Sky's the Limit", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                       'Progressive Weapons', 'Progressive Armor',
                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Sky's the Limit", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                       'Progressive Weapons', 'Shield',
                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["Sky's the Limit", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                       'Progressive Weapons', 'Shield',
                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42043(self):
        self.run_location_tests([
            ["Hired Help", False, []],
            ["Hired Help", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["Hired Help", False, [], ['Progressive Tools']],
            ["Hired Help", True, ['Progressive Tools', 'Progressive Resource Crafting', 'Progressive Resource Crafting']],
            ])

    def test_42044(self):
        self.run_location_tests([
            ["Return to Sender", False, []],
            ["Return to Sender", False, [], ['Progressive Resource Crafting']],
            ["Return to Sender", False, [], ['Flint and Steel']],
            ["Return to Sender", False, [], ['Progressive Tools']],
            ["Return to Sender", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Return to Sender", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']],
            ["Return to Sender", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42045(self):
        self.run_location_tests([
            ["Sweet Dreams", False, []],
            ["Sweet Dreams", True, ['Bed']],
            ["Sweet Dreams", False, [], ['Bed', 'Progressive Weapons']],
            ["Sweet Dreams", False, [], ['Bed', 'Progressive Resource Crafting', 'Campfire']],
            ["Sweet Dreams", True, ['Progressive Weapons', 'Progressive Resource Crafting'], ['Bed', 'Campfire']],
            ["Sweet Dreams", True, ['Progressive Weapons', 'Campfire'], ['Bed', 'Progressive Resource Crafting']],
            ])

    def test_42046(self):
        self.run_location_tests([
            ["You Need a Mint", False, []],
            ["You Need a Mint", False, [], ['Progressive Resource Crafting']],
            ["You Need a Mint", False, [], ['Flint and Steel']],
            ["You Need a Mint", False, [], ['Progressive Tools']],
            ["You Need a Mint", False, [], ['Progressive Weapons']],
            ["You Need a Mint", False, [], ['Progressive Armor', 'Shield']],
            ["You Need a Mint", False, [], ['Brewing']],
            ["You Need a Mint", False, [], ['Bottles']],
            ["You Need a Mint", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["You Need a Mint", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["You Need a Mint", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                       'Progressive Weapons', 'Progressive Armor', 'Brewing',
                                       '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', 'Bottles']],
            ["You Need a Mint", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                       'Progressive Weapons', 'Progressive Armor', 'Brewing',
                                       '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', 'Bottles']],
            ["You Need a Mint", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                       'Progressive Weapons', 'Shield', 'Brewing',
                                       '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', 'Bottles']],
            ["You Need a Mint", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                       'Progressive Weapons', 'Shield', 'Brewing',
                                       '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', 'Bottles']],
            ])

    def test_42047(self):
        self.run_location_tests([
            ["Adventure", True, []],
            ])

    def test_42048(self):
        self.run_location_tests([
            ["Monsters Hunted", False, []],
            ["Monsters Hunted", False, [], ['Progressive Resource Crafting']],
            ["Monsters Hunted", False, [], ['Flint and Steel']],
            ["Monsters Hunted", False, [], ['Progressive Tools']],
            ["Monsters Hunted", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["Monsters Hunted", False, [], ['Progressive Armor']],
            ["Monsters Hunted", False, [], ['Brewing']],
            ["Monsters Hunted", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Monsters Hunted", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["Monsters Hunted", False, [], ['Archery']],
            ["Monsters Hunted", False, [], ['Enchanting']],
            ["Monsters Hunted", False, [], ['Fishing Rod']],
            ["Monsters Hunted", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                       'Progressive Weapons', 'Progressive Weapons', 'Progressive Weapons', 'Archery',
                                       'Progressive Armor', 'Progressive Armor', 'Enchanting',
                                       'Fishing Rod', 'Brewing', 'Bottles', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42049(self):
        self.run_location_tests([
            ["Enchanter", False, []],
            ["Enchanter", False, [], ['Enchanting']],
            ["Enchanter", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Enchanter", False, [], ['Progressive Resource Crafting']],
            ["Enchanter", True, ['Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Enchanting', 'Progressive Resource Crafting']],
            ])

    def test_42050(self):
        self.run_location_tests([
            ["Voluntary Exile", False, []],
            ["Voluntary Exile", False, [], ['Progressive Weapons']],
            ["Voluntary Exile", False, [], ['Progressive Armor', 'Shield']],
            ["Voluntary Exile", False, [], ['Progressive Tools']],
            ["Voluntary Exile", False, [], ['Progressive Resource Crafting']],
            ["Voluntary Exile", True, ['Progressive Tools', 'Progressive Armor', 'Progressive Weapons', 'Progressive Resource Crafting']],
            ["Voluntary Exile", True, ['Progressive Tools', 'Shield', 'Progressive Weapons', 'Progressive Resource Crafting']],
            ])

    def test_42051(self):
        self.run_location_tests([
            ["Eye Spy", False, []],
            ["Eye Spy", False, [], ['Progressive Resource Crafting']],
            ["Eye Spy", False, [], ['Flint and Steel']],
            ["Eye Spy", False, [], ['Progressive Tools']],
            ["Eye Spy", False, [], ['Progressive Weapons']],
            ["Eye Spy", False, [], ['Progressive Armor', 'Shield']],
            ["Eye Spy", False, [], ['Brewing']],
            ["Eye Spy", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Eye Spy", False, [], ['3 Ender Pearls']],
            ["Eye Spy", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                               'Progressive Weapons', 'Progressive Armor', 'Brewing', '3 Ender Pearls']],
            ["Eye Spy", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                               'Progressive Weapons', 'Progressive Armor', 'Brewing', '3 Ender Pearls']],
            ["Eye Spy", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                               'Progressive Weapons', 'Shield', 'Brewing', '3 Ender Pearls']],
            ["Eye Spy", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                               'Progressive Weapons', 'Shield', 'Brewing', '3 Ender Pearls']],
            ])

    def test_42052(self):
        self.run_location_tests([
            ["The End", False, []],
            ["The End", False, [], ['Progressive Resource Crafting']],
            ["The End", False, [], ['Flint and Steel']],
            ["The End", False, [], ['Progressive Tools']],
            ["The End", False, [], ['Progressive Weapons']],
            ["The End", False, [], ['Progressive Armor', 'Shield']],
            ["The End", False, [], ['Brewing']],
            ["The End", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["The End", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["The End", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                               'Progressive Weapons', 'Progressive Armor',
                               'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The End", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                               'Progressive Weapons', 'Progressive Armor',
                               'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The End", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                               'Progressive Weapons', 'Shield',
                               'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The End", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                               'Progressive Weapons', 'Shield',
                               'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42053(self):
        self.run_location_tests([
            ["Serious Dedication", False, []],
            ["Serious Dedication", False, [], ['Progressive Resource Crafting']],
            ["Serious Dedication", False, [], ['Flint and Steel']],
            ["Serious Dedication", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Serious Dedication", False, [], ['Progressive Weapons']],
            ["Serious Dedication", False, [], ['Progressive Armor', 'Shield']],
            ["Serious Dedication", False, [], ['Brewing']],
            ["Serious Dedication", False, [], ['Bottles']],
            ["Serious Dedication", False, [], ['Bed']],
            ["Serious Dedication", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                          'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles', 'Bed']],
            ["Serious Dedication", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                          'Progressive Weapons', 'Shield', 'Brewing', 'Bottles', 'Bed']],
            ])

    def test_42054(self):
        self.run_location_tests([
            ["Postmortal", False, []],
            ["Postmortal", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["Postmortal", False, [], ['Progressive Armor']],
            ["Postmortal", False, [], ['Shield']],
            ["Postmortal", False, [], ['Progressive Resource Crafting']],
            ["Postmortal", False, [], ['Progressive Tools']],
            ["Postmortal", True, ['Progressive Weapons', 'Progressive Weapons', 'Progressive Armor', 'Shield', 'Progressive Resource Crafting', 'Progressive Tools']],
            ])

    def test_42055(self):
        self.run_location_tests([
            ["Monster Hunter", True, []],
            ])

    def test_42056(self):
        self.run_location_tests([
            ["Adventuring Time", False, []],
            ["Adventuring Time", False, [], ['Progressive Weapons']],
            ["Adventuring Time", False, [], ['Campfire', 'Progressive Resource Crafting']],
            ["Adventuring Time", True, ['Progressive Weapons', 'Campfire']],
            ["Adventuring Time", True, ['Progressive Weapons', 'Progressive Resource Crafting']],
            ])

    def test_42057(self):
        self.run_location_tests([
            ["A Seedy Place", True, []],
            ])

    def test_42058(self):
        self.run_location_tests([
            ["Those Were the Days", False, []],
            ["Those Were the Days", False, [], ['Progressive Resource Crafting']],
            ["Those Were the Days", False, [], ['Flint and Steel']],
            ["Those Were the Days", False, [], ['Progressive Tools']],
            ["Those Were the Days", False, [], ['Progressive Weapons']],
            ["Those Were the Days", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Those Were the Days", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons']],
            ["Those Were the Days", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons']],
            ])

    def test_42059(self):
        self.run_location_tests([
            ["Hero of the Village", False, []],
            ["Hero of the Village", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["Hero of the Village", False, [], ['Progressive Armor']],
            ["Hero of the Village", False, [], ['Shield']],
            ["Hero of the Village", False, [], ['Progressive Resource Crafting']],
            ["Hero of the Village", False, [], ['Progressive Tools']],
            ["Hero of the Village", True, ['Progressive Weapons', 'Progressive Weapons', 'Progressive Armor', 'Shield', 'Progressive Resource Crafting', 'Progressive Tools']],
            ])

    def test_42060(self):
        self.run_location_tests([
            ["Hidden in the Depths", False, []],
            ["Hidden in the Depths", False, [], ['Progressive Resource Crafting']],
            ["Hidden in the Depths", False, [], ['Flint and Steel']],
            ["Hidden in the Depths", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Hidden in the Depths", False, [], ['Progressive Weapons']],
            ["Hidden in the Depths", False, [], ['Progressive Armor', 'Shield']],
            ["Hidden in the Depths", False, [], ['Brewing']],
            ["Hidden in the Depths", False, [], ['Bottles']],
            ["Hidden in the Depths", False, [], ['Bed']],
            ["Hidden in the Depths", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                            'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles', 'Bed']],
            ["Hidden in the Depths", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                            'Progressive Weapons', 'Shield', 'Brewing', 'Bottles', 'Bed']],
            ])

    def test_42061(self):
        self.run_location_tests([
            ["Beaconator", False, []],
            ["Beaconator", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["Beaconator", False, [], ['Flint and Steel']],
            ["Beaconator", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Beaconator", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["Beaconator", False, ['Progressive Armor'], ['Progressive Armor']],
            ["Beaconator", False, [], ['Brewing']],
            ["Beaconator", False, [], ['Bottles']],
            ["Beaconator", False, [], ['Enchanting']],
            ["Beaconator", True, [], ['Bucket']],
            ["Beaconator", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting',
                                  'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                  'Progressive Weapons', 'Progressive Weapons', 'Progressive Weapons', 'Progressive Armor', 'Progressive Armor',
                                  'Brewing', 'Bottles', 'Enchanting']],
            ])

    def test_42062(self):
        self.run_location_tests([
            ["Withering Heights", False, []],
            ["Withering Heights", False, [], ['Progressive Resource Crafting']],
            ["Withering Heights", False, [], ['Flint and Steel']],
            ["Withering Heights", False, [], ['Progressive Tools']],
            ["Withering Heights", False, ['Progressive Weapons'], ['Progressive Weapons', 'Progressive Weapons']],
            ["Withering Heights", False, ['Progressive Armor'], ['Progressive Armor']],
            ["Withering Heights", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Withering Heights", False, [], ['Brewing']],
            ["Withering Heights", False, [], ['Bottles']],
            ["Withering Heights", False, [], ['Enchanting']],
            ["Withering Heights", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                         'Progressive Weapons', 'Progressive Weapons', 'Progressive Weapons', 'Progressive Armor', 'Progressive Armor',
                                         'Brewing', 'Bottles', 'Enchanting']],
            ])

    def test_42063(self):
        self.run_location_tests([
            ["A Balanced Diet", False, []],
            ["A Balanced Diet", False, [], ['Bottles']],
            ["A Balanced Diet", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["A Balanced Diet", False, [], ['Flint and Steel']],
            ["A Balanced Diet", False, [], ['Progressive Tools']],
            ["A Balanced Diet", False, [], ['Progressive Weapons']],
            ["A Balanced Diet", False, [], ['Progressive Armor', 'Shield']],
            ["A Balanced Diet", False, [], ['Brewing']],
            ["A Balanced Diet", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["A Balanced Diet", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["A Balanced Diet", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting',
                                       'Progressive Tools', 'Flint and Steel', 'Bucket',
                                       'Progressive Weapons', 'Progressive Armor', 'Bottles',
                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["A Balanced Diet", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting',
                                       'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                       'Progressive Weapons', 'Progressive Armor', 'Bottles',
                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["A Balanced Diet", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting',
                                       'Progressive Tools', 'Flint and Steel', 'Bucket',
                                       'Progressive Weapons', 'Shield', 'Bottles',
                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["A Balanced Diet", True, ['Progressive Resource Crafting', 'Progressive Resource Crafting',
                                       'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                       'Progressive Weapons', 'Shield', 'Bottles',
                                       'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42064(self):
        self.run_location_tests([
            ["Subspace Bubble", False, []],
            ["Subspace Bubble", False, [], ['Progressive Resource Crafting']],
            ["Subspace Bubble", False, [], ['Flint and Steel']],
            ["Subspace Bubble", False, [], ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Subspace Bubble", True, ['Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Flint and Steel', 'Progressive Resource Crafting']],
            ])

    def test_42065(self):
        self.run_location_tests([
            ["Husbandry", True, []],
            ])

    def test_42066(self):
        self.run_location_tests([
            ["Country Lode, Take Me Home", False, []],
            ["Country Lode, Take Me Home", False, [], ['Progressive Resource Crafting']],
            ["Country Lode, Take Me Home", False, [], ['Flint and Steel']],
            ["Country Lode, Take Me Home", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Country Lode, Take Me Home", False, [], ['Progressive Weapons']],
            ["Country Lode, Take Me Home", False, [], ['Progressive Armor', 'Shield']],
            ["Country Lode, Take Me Home", False, [], ['Brewing']],
            ["Country Lode, Take Me Home", False, [], ['Bottles']],
            ["Country Lode, Take Me Home", False, [], ['Bed']],
            ["Country Lode, Take Me Home", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                                  'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles', 'Bed']],
            ["Country Lode, Take Me Home", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                                  'Progressive Weapons', 'Shield', 'Brewing', 'Bottles', 'Bed']],
            ])

    def test_42067(self):
        self.run_location_tests([
            ["Bee Our Guest", False, []],
            ["Bee Our Guest", False, [], ['Campfire']],
            ["Bee Our Guest", False, [], ['Bottles']],
            ["Bee Our Guest", False, [], ['Progressive Resource Crafting']],
            ["Bee Our Guest", True, ['Campfire', 'Bottles', 'Progressive Resource Crafting']],
            ])

    def test_42068(self):
        self.run_location_tests([
            ["What a Deal!", False, []],
            ["What a Deal!", False, [], ['Progressive Weapons']],
            ["What a Deal!", False, [], ['Campfire', 'Progressive Resource Crafting']],
            ["What a Deal!", True, ['Progressive Weapons', 'Campfire']],
            ["What a Deal!", True, ['Progressive Weapons', 'Progressive Resource Crafting']],
            ])

    def test_42069(self):
        self.run_location_tests([
            ["Uneasy Alliance", False, []],
            ["Uneasy Alliance", False, [], ['Progressive Resource Crafting']],
            ["Uneasy Alliance", False, [], ['Flint and Steel']],
            ["Uneasy Alliance", False, [], ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Uneasy Alliance", False, [], ['Fishing Rod']],
            ["Uneasy Alliance", True, ['Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Flint and Steel', 'Progressive Resource Crafting', 'Fishing Rod']],
            ])

    def test_42070(self):
        self.run_location_tests([
            ["Diamonds!", False, []],
            ["Diamonds!", True, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]],
            ["Diamonds!", False, [], ["Progressive Tools", "Progressive Tools"]],
            ["Diamonds!", False, [], ["Progressive Resource Crafting"]],
            ["Diamonds!", False, ["Progressive Tools", "Progressive Resource Crafting"]],
            ["Diamonds!", True, ["Progressive Tools", "Progressive Tools", "Progressive Resource Crafting"]],
            ])

    def test_42071(self):
        self.run_location_tests([
            ["A Terrible Fortress", False, []],
            ["A Terrible Fortress", False, [], ['Progressive Resource Crafting']],
            ["A Terrible Fortress", False, [], ['Flint and Steel']],
            ["A Terrible Fortress", False, [], ['Progressive Tools']],
            ["A Terrible Fortress", False, [], ['Progressive Weapons']],
            ["A Terrible Fortress", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["A Terrible Fortress", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons']],
            ["A Terrible Fortress", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons']],
            ])

    def test_42072(self):
        self.run_location_tests([
            ["A Throwaway Joke", False, []],
            ["A Throwaway Joke", False, [], ['Progressive Weapons']],
            ["A Throwaway Joke", False, [], ['Campfire', 'Progressive Resource Crafting']],
            ["A Throwaway Joke", True, ['Progressive Weapons', 'Campfire']],
            ["A Throwaway Joke", True, ['Progressive Weapons', 'Progressive Resource Crafting']],
            ])

    def test_42073(self):
        self.run_location_tests([
            ["Minecraft", True, []],
            ])

    def test_42074(self):
        self.run_location_tests([
            ["Sticky Situation", False, []],
            ["Sticky Situation", False, [], ['Bottles']],
            ["Sticky Situation", False, [], ['Progressive Resource Crafting']],
            ["Sticky Situation", False, [], ['Campfire']],
            ["Sticky Situation", True, ['Bottles', 'Progressive Resource Crafting', 'Campfire']],
            ])

    def test_42075(self):
        self.run_location_tests([
            ["Ol' Betsy", False, []],
            ["Ol' Betsy", False, [], ['Archery']],
            ["Ol' Betsy", False, [], ['Progressive Resource Crafting']],
            ["Ol' Betsy", False, [], ['Progressive Tools']],
            ["Ol' Betsy", True, ['Archery', 'Progressive Resource Crafting', 'Progressive Tools']],
            ])

    def test_42076(self):
        self.run_location_tests([
            ["Cover Me in Debris", False, []],
            ["Cover Me in Debris", False, [], ['Progressive Resource Crafting']],
            ["Cover Me in Debris", False, [], ['Flint and Steel']],
            ["Cover Me in Debris", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Cover Me in Debris", False, [], ['Progressive Weapons']],
            ["Cover Me in Debris", False, ['Progressive Armor'], ['Progressive Armor']],
            ["Cover Me in Debris", False, [], ['Brewing']],
            ["Cover Me in Debris", False, [], ['Bottles']],
            ["Cover Me in Debris", False, [], ['Bed']],
            ["Cover Me in Debris", False, ['8 Netherite Scrap'], ['8 Netherite Scrap']],
            ["Cover Me in Debris", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                          'Progressive Weapons', 'Progressive Armor', 'Progressive Armor',
                                          'Brewing', 'Bottles', 'Bed', '8 Netherite Scrap', '8 Netherite Scrap']],
            ])

    def test_42077(self):
        self.run_location_tests([
            ["The End?", False, []],
            ["The End?", False, [], ['Progressive Resource Crafting']],
            ["The End?", False, [], ['Flint and Steel']],
            ["The End?", False, [], ['Progressive Tools']],
            ["The End?", False, [], ['Progressive Weapons']],
            ["The End?", False, [], ['Progressive Armor', 'Shield']],
            ["The End?", False, [], ['Brewing']],
            ["The End?", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["The End?", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["The End?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                'Progressive Weapons', 'Progressive Armor',
                                'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The End?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                'Progressive Weapons', 'Progressive Armor',
                                'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The End?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                'Progressive Weapons', 'Shield',
                                'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ["The End?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                'Progressive Weapons', 'Shield',
                                'Brewing', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls']],
            ])

    def test_42078(self):
        self.run_location_tests([
            ["The Parrots and the Bats", True, []],
            ])

    def test_42079(self):
        self.run_location_tests([
            ["A Complete Catalogue", False, []],
            ["A Complete Catalogue", False, [], ['Progressive Weapons']],
            ["A Complete Catalogue", False, [], ['Campfire', 'Progressive Resource Crafting']],
            ["A Complete Catalogue", True, ['Progressive Weapons', 'Campfire']],
            ["A Complete Catalogue", True, ['Progressive Weapons', 'Progressive Resource Crafting']],
            ])

    def test_42080(self):
        self.run_location_tests([
            ["Getting Wood", True, []],
            ])

    def test_42081(self):
        self.run_location_tests([
            ["Time to Mine!", True, []],
            ])

    def test_42082(self):
        self.run_location_tests([
            ["Hot Topic", False, []],
            ["Hot Topic", True, ['Progressive Resource Crafting']],
            ])

    def test_42083(self):
        self.run_location_tests([
            ["Bake Bread", True, []],
            ])

    def test_42084(self):
        self.run_location_tests([
            ["The Lie", False, []],
            ["The Lie", False, [], ['Progressive Resource Crafting']],
            ["The Lie", False, [], ['Bucket']],
            ["The Lie", False, [], ['Progressive Tools']],
            ["The Lie", True, ['Bucket', 'Progressive Resource Crafting', 'Progressive Tools']],
            ])

    def test_42085(self):
        self.run_location_tests([
            ["On a Rail", False, []],
            ["On a Rail", False, [], ['Progressive Resource Crafting']],
            ["On a Rail", False, ['Progressive Tools'], ['Progressive Tools', 'Progressive Tools']],
            ["On a Rail", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42086(self):
        self.run_location_tests([
            ["Time to Strike!", True, []],
            ])

    def test_42087(self):
        self.run_location_tests([
            ["Cow Tipper", True, []],
            ])

    def test_42088(self):
        self.run_location_tests([
            ["When Pigs Fly", False, []],
            ["When Pigs Fly", False, [], ['Progressive Resource Crafting']],
            ["When Pigs Fly", False, [], ['Progressive Tools']],
            ["When Pigs Fly", False, [], ['Progressive Weapons']],
            ["When Pigs Fly", False, [], ['Progressive Armor', 'Shield']],
            ["When Pigs Fly", False, [], ['Fishing Rod']],
            ["When Pigs Fly", False, [], ['Saddle']],
            ["When Pigs Fly", False, ['Progressive Weapons'], ['Flint and Steel', 'Progressive Weapons', 'Progressive Weapons']],
            ["When Pigs Fly", False, ['Progressive Tools', 'Progressive Tools', 'Progressive Weapons'], ['Bucket', 'Progressive Tools', 'Progressive Weapons', 'Progressive Weapons']],
            ["When Pigs Fly", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor', 'Fishing Rod']],
            ["When Pigs Fly", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor', 'Fishing Rod']],
            ["When Pigs Fly", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Shield', 'Fishing Rod']],
            ["When Pigs Fly", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Shield', 'Fishing Rod']],
            ["When Pigs Fly", True, ['Saddle', 'Progressive Weapons', 'Progressive Weapons', 'Progressive Armor', 'Shield', 'Progressive Resource Crafting', 'Progressive Tools', 'Fishing Rod']],
            ])

    def test_42089(self):
        self.run_location_tests([
            ["Overkill", False, []],
            ["Overkill", False, [], ['Progressive Resource Crafting']],
            ["Overkill", False, [], ['Flint and Steel']],
            ["Overkill", False, [], ['Progressive Tools']],
            ["Overkill", False, [], ['Progressive Weapons']],
            ["Overkill", False, [], ['Progressive Armor', 'Shield']],
            ["Overkill", False, [], ['Brewing']],
            ["Overkill", False, [], ['Bottles']],
            ["Overkill", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Overkill", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']],
            ["Overkill", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']],
            ["Overkill", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                'Progressive Weapons', 'Shield', 'Brewing', 'Bottles']],
            ["Overkill", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                'Progressive Weapons', 'Shield', 'Brewing', 'Bottles']],
            ])

    def test_42090(self):
        self.run_location_tests([
            ["Librarian", False, []],
            ["Librarian", True, ['Enchanting']],
            ])

    def test_42091(self):
        self.run_location_tests([
            ["Overpowered", False, []],
            ["Overpowered", False, [], ['Progressive Resource Crafting']],
            ["Overpowered", False, [], ['Flint and Steel']],
            ["Overpowered", False, ['Progressive Tools', 'Progressive Tools', 'Bucket', 'Flint and Steel']],
            ["Overpowered", False, [], ['Progressive Weapons']],
            ["Overpowered", False, [], ['Progressive Armor', 'Shield']],
            ["Overpowered", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor']],
            ["Overpowered", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor']],
            ["Overpowered", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Weapons', 'Shield']],
            ["Overpowered", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Shield']],
            ])

    def test_42092(self):
        self.run_location_tests([
            ["Wax On", False, []],
            ["Wax On", False, [], ["Progressive Tools"]],
            ["Wax On", False, [], ["Campfire"]],
            ["Wax On", False, ["Progressive Resource Crafting"], ["Progressive Resource Crafting"]],
            ["Wax On", True, ["Progressive Tools", "Progressive Resource Crafting", "Progressive Resource Crafting", "Campfire"]],
            ])

    def test_42093(self):
        self.run_location_tests([
            ["Wax Off", False, []],
            ["Wax Off", False, [], ["Progressive Tools"]],
            ["Wax Off", False, [], ["Campfire"]],
            ["Wax Off", False, ["Progressive Resource Crafting"], ["Progressive Resource Crafting"]],
            ["Wax Off", True, ["Progressive Tools", "Progressive Resource Crafting", "Progressive Resource Crafting", "Campfire"]],
            ])

    def test_42094(self):
        self.run_location_tests([
            ["The Cutest Predator", False, []],
            ["The Cutest Predator", False, [], ["Progressive Tools"]],
            ["The Cutest Predator", False, [], ["Progressive Resource Crafting"]],
            ["The Cutest Predator", False, [], ["Bucket"]],
            ["The Cutest Predator", True, ["Progressive Tools", "Progressive Resource Crafting", "Bucket"]],
            ])

    def test_42095(self):
        self.run_location_tests([
            ["The Healing Power of Friendship", False, []],
            ["The Healing Power of Friendship", False, [], ["Progressive Tools"]],
            ["The Healing Power of Friendship", False, [], ["Progressive Resource Crafting"]],
            ["The Healing Power of Friendship", False, [], ["Bucket"]],
            ["The Healing Power of Friendship", True, ["Progressive Tools", "Progressive Resource Crafting", "Bucket"]],
            ])

    def test_42096(self):
        self.run_location_tests([
            ["Is It a Bird?", False, []],
            ["Is It a Bird?", False, [], ["Progressive Weapons"]],
            ["Is It a Bird?", False, [], ["Progressive Tools"]],
            ["Is It a Bird?", False, [], ["Progressive Resource Crafting"]],
            ["Is It a Bird?", False, [], ["Spyglass"]],
            ["Is It a Bird?", True, ["Progressive Weapons", "Progressive Tools", "Progressive Resource Crafting", "Spyglass"]],
            ])

    def test_42097(self):
        self.run_location_tests([
            ["Is It a Balloon?", False, []],
            ["Is It a Balloon?", False, [], ['Progressive Resource Crafting']],
            ["Is It a Balloon?", False, [], ['Flint and Steel']],
            ["Is It a Balloon?", False, [], ['Progressive Tools']],
            ["Is It a Balloon?", False, [], ['Progressive Weapons']],
            ["Is It a Balloon?", False, [], ['Spyglass']],
            ["Is It a Balloon?", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Is It a Balloon?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Spyglass']],
            ["Is It a Balloon?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Spyglass']],
            ])

    def test_42098(self):
        self.run_location_tests([
            ["Is It a Plane?", False, []],
            ["Is It a Plane?", False, [], ['Progressive Resource Crafting']],
            ["Is It a Plane?", False, [], ['Flint and Steel']],
            ["Is It a Plane?", False, [], ['Progressive Tools']],
            ["Is It a Plane?", False, [], ['Progressive Weapons']],
            ["Is It a Plane?", False, [], ['Progressive Armor', 'Shield']],
            ["Is It a Plane?", False, [], ['Brewing']],
            ["Is It a Plane?", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']],
            ["Is It a Plane?", False, ['3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls'], ['3 Ender Pearls']],
            ["Is It a Plane?", False, [], ['Spyglass']],
            ["Is It a Plane?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                    'Progressive Weapons', 'Progressive Armor', 'Brewing',
                                    '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', 'Spyglass']],
            ["Is It a Plane?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                    'Progressive Weapons', 'Progressive Armor', 'Brewing',
                                    '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', 'Spyglass']],
            ["Is It a Plane?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket',
                                    'Progressive Weapons', 'Shield', 'Brewing',
                                    '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', 'Spyglass']],
            ["Is It a Plane?", True, ['Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools',
                                    'Progressive Weapons', 'Shield', 'Brewing',
                                    '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', '3 Ender Pearls', 'Spyglass']],
            ])

    def test_42099(self):
        self.run_location_tests([
            ["Surge Protector", False, []],
            ["Surge Protector", False, [], ['Channeling Book']],
            ["Surge Protector", False, ['Progressive Resource Crafting'], ['Progressive Resource Crafting']],
            ["Surge Protector", False, [], ['Enchanting']],
            ["Surge Protector", False, [], ['Progressive Tools']],
            ["Surge Protector", False, [], ['Progressive Weapons']],
            ["Surge Protector", True, ['Progressive Weapons', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools',
                                             'Enchanting', 'Progressive Resource Crafting', 'Progressive Resource Crafting', 'Channeling Book']],
            ])

    def test_42100(self):
        self.run_location_tests([
            ["Light as a Rabbit", False, []],
            ["Light as a Rabbit", False, [], ["Progressive Weapons"]],
            ["Light as a Rabbit", False, [], ["Progressive Tools"]],
            ["Light as a Rabbit", False, [], ["Progressive Resource Crafting"]],
            ["Light as a Rabbit", False, [], ["Bucket"]],
            ["Light as a Rabbit", True, ["Progressive Weapons", "Progressive Tools", "Progressive Resource Crafting", "Bucket"]],
            ])

    def test_42101(self):
        self.run_location_tests([
            ["Glow and Behold!", False, []],
            ["Glow and Behold!", False, [], ["Progressive Weapons"]],
            ["Glow and Behold!", False, [], ["Progressive Resource Crafting", "Campfire"]],
            ["Glow and Behold!", True, ["Progressive Weapons", "Progressive Resource Crafting"]],
            ["Glow and Behold!", True, ["Progressive Weapons", "Campfire"]],
            ])

    def test_42102(self):
        self.run_location_tests([
            ["Whatever Floats Your Goat!", False, []],
            ["Whatever Floats Your Goat!", False, [], ["Progressive Weapons"]],
            ["Whatever Floats Your Goat!", False, [], ["Progressive Resource Crafting", "Campfire"]],
            ["Whatever Floats Your Goat!", True, ["Progressive Weapons", "Progressive Resource Crafting"]],
            ["Whatever Floats Your Goat!", True, ["Progressive Weapons", "Campfire"]],
            ])

    # bucket, iron pick
    def test_42103(self):
        self.run_location_tests([
            ["Caves & Cliffs", False, []],
            ["Caves & Cliffs", False, [], ["Bucket"]],
            ["Caves & Cliffs", False, [], ["Progressive Tools"]],
            ["Caves & Cliffs", False, [], ["Progressive Resource Crafting"]],
            ["Caves & Cliffs", True, ["Progressive Resource Crafting", "Progressive Tools", "Progressive Tools", "Bucket"]],
            ])

    # bucket, fishing rod, saddle, combat
    def test_42104(self):
        self.run_location_tests([
            ["Feels like home", False, []],
            ["Feels like home", False, [], ['Progressive Resource Crafting']],
            ["Feels like home", False, [], ['Progressive Tools']],
            ["Feels like home", False, [], ['Progressive Weapons']],
            ["Feels like home", False, [], ['Progressive Armor', 'Shield']],
            ["Feels like home", False, [], ['Fishing Rod']],
            ["Feels like home", False, [], ['Saddle']],
            ["Feels like home", False, [], ['Bucket']],
            ["Feels like home", False, [], ['Flint and Steel']],
            ["Feels like home", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor', 'Fishing Rod']],
            ["Feels like home", True, ['Saddle', 'Progressive Resource Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Shield', 'Fishing Rod']],
            ])

    # iron pick, combat
    def test_42105(self):
        self.run_location_tests([
            ["Sound of Music", False, []],
            ["Sound of Music", False, [], ["Progressive Tools"]],
            ["Sound of Music", False, [], ["Progressive Resource Crafting"]],
            ["Sound of Music", False, [], ["Progressive Weapons"]],
            ["Sound of Music", False, [], ["Progressive Armor", "Shield"]],
            ["Sound of Music", True, ["Progressive Tools", "Progressive Tools", "Progressive Resource Crafting", "Progressive Weapons", "Progressive Armor"]],
            ["Sound of Music", True, ["Progressive Tools", "Progressive Tools", "Progressive Resource Crafting", "Progressive Weapons", "Shield"]],
            ])

    # bucket, nether, villager
    def test_42106(self):
        self.run_location_tests([
            ["Star Trader", False, []],
            ["Star Trader", False, [], ["Bucket"]],
            ["Star Trader", False, [], ["Flint and Steel"]],
            ["Star Trader", False, [], ["Progressive Tools"]],
            ["Star Trader", False, [], ["Progressive Resource Crafting"]],
            ["Star Trader", False, [], ["Progressive Weapons"]],
            ["Star Trader", True, ["Bucket", "Flint and Steel", "Progressive Tools", "Progressive Resource Crafting", "Progressive Weapons"]],
            ])

    # bucket, redstone -> iron pick, pillager outpost -> adventure
    def test_42107(self):
        self.run_location_tests([
            ["Birthday Song", False, []],
            ["Birthday Song", False, [], ["Bucket"]],
            ["Birthday Song", False, [], ["Progressive Tools"]],
            ["Birthday Song", False, [], ["Progressive Weapons"]],
            ["Birthday Song", False, [], ["Progressive Resource Crafting"]],
            ["Birthday Song", True, ["Progressive Resource Crafting", "Progressive Tools", "Progressive Tools", "Progressive Weapons", "Bucket"]],
            ])

    # bucket, adventure
    def test_42108(self):
        self.run_location_tests([
            ["Bukkit Bukkit", False, []],
            ["Bukkit Bukkit", False, [], ["Bucket"]],
            ["Bukkit Bukkit", False, [], ["Progressive Tools"]],
            ["Bukkit Bukkit", False, [], ["Progressive Weapons"]],
            ["Bukkit Bukkit", False, [], ["Progressive Resource Crafting"]],
            ["Bukkit Bukkit", True, ["Bucket", "Progressive Tools", "Progressive Weapons", "Progressive Resource Crafting"]],
            ])

    # iron pick, adventure
    def test_42109(self):
        self.run_location_tests([
            ["It Spreads", False, []],
            ["It Spreads", False, [], ["Progressive Tools"]],
            ["It Spreads", False, [], ["Progressive Weapons"]],
            ["It Spreads", False, [], ["Progressive Resource Crafting"]],
            ["It Spreads", True, ["Progressive Tools", "Progressive Tools", "Progressive Weapons", "Progressive Resource Crafting"]],
            ])

    # iron pick, adventure
    def test_42110(self):
        self.run_location_tests([
            ["Sneak 100", False, []],
            ["Sneak 100", False, [], ["Progressive Tools"]],
            ["Sneak 100", False, [], ["Progressive Weapons"]],
            ["Sneak 100", False, [], ["Progressive Resource Crafting"]],
            ["Sneak 100", True, ["Progressive Tools", "Progressive Tools", "Progressive Weapons", "Progressive Resource Crafting"]],
            ])

    # adventure, lead
    def test_42111(self):
        self.run_location_tests([
            ["When the Squad Hops into Town", False, []],
            ["When the Squad Hops into Town", False, [], ["Progressive Weapons"]],
            ["When the Squad Hops into Town", False, [], ["Campfire", "Progressive Resource Crafting"]],
            ["When the Squad Hops into Town", False, [], ["Lead"]],
            ["When the Squad Hops into Town", True, ["Progressive Weapons", "Lead", "Campfire"]],
            ["When the Squad Hops into Town", True, ["Progressive Weapons", "Lead", "Progressive Resource Crafting"]],
            ])

    # adventure, lead, nether
    def test_42112(self):
        self.run_location_tests([
            ["With Our Powers Combined!", False, []],
            ["With Our Powers Combined!", False, [], ["Lead"]],
            ["With Our Powers Combined!", False, [], ["Bucket", "Progressive Tools"]],
            ["With Our Powers Combined!", False, [], ["Flint and Steel"]],
            ["With Our Powers Combined!", False, [], ["Progressive Weapons"]],
            ["With Our Powers Combined!", False, [], ["Progressive Resource Crafting"]],
            ["With Our Powers Combined!", True, ["Lead", "Progressive Weapons", "Progressive Resource Crafting", "Flint and Steel", "Progressive Tools", "Bucket"]],
            ["With Our Powers Combined!", True, ["Lead", "Progressive Weapons", "Progressive Resource Crafting", "Flint and Steel", "Progressive Tools", "Progressive Tools", "Progressive Tools"]],
            ])

    # pillager outpost -> adventure
    def test_42113(self):
        self.run_location_tests([
            ["You've Got a Friend in Me", False, []],
            ["You've Got a Friend in Me", False, [], ["Progressive Weapons"]],
            ["You've Got a Friend in Me", False, [], ["Campfire", "Progressive Resource Crafting"]],
            ["You've Got a Friend in Me", True, ["Progressive Weapons", "Campfire"]],
            ["You've Got a Friend in Me", True, ["Progressive Weapons", "Progressive Resource Crafting"]],
            ])
