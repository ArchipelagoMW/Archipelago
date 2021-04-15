from test.minecraft.TestMinecraft import TestMinecraft

# Format: 
# [location, expected_result, given_items, [excluded_items]]
# Every advancement has its own test, named by its internal ID number. 
class TestAdvancements(TestMinecraft):

    def test_42000(self):
        self.run_location_tests([
            ["Who is Cutting Onions?", False, []], 
            ["Who is Cutting Onions?", False, [], ['Ingot Crafting']], 
            ["Who is Cutting Onions?", False, [], ['Flint and Steel']], 
            ["Who is Cutting Onions?", False, [], ['Progressive Tools']], 
            ["Who is Cutting Onions?", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Who is Cutting Onions?", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["Who is Cutting Onions?", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42001(self):
        self.run_location_tests([
            ["Oh Shiny", False, []], 
            ["Oh Shiny", False, [], ['Ingot Crafting']], 
            ["Oh Shiny", False, [], ['Flint and Steel']], 
            ["Oh Shiny", False, [], ['Progressive Tools']], 
            ["Oh Shiny", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Oh Shiny", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["Oh Shiny", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42002(self):
        self.run_location_tests([
            ["Suit Up", False, []],
            ["Suit Up", False, [], ["Progressive Armor"]],
            ["Suit Up", False, [], ["Ingot Crafting"]],
            ["Suit Up", False, [], ["Progressive Tools"]],
            ["Suit Up", True, ["Progressive Armor", "Ingot Crafting", "Progressive Tools"]],
            ])

    def test_42003(self):
        self.run_location_tests([
            ["Very Very Frightening", False, []],
            ["Very Very Frightening", False, [], ['Channeling Book']],
            ["Very Very Frightening", False, [], ['Resource Blocks']],
            ["Very Very Frightening", False, [], ['Ingot Crafting']],
            ["Very Very Frightening", False, [], ['Enchanting']],
            ["Very Very Frightening", False, [], ['Progressive Tools']],
            ["Very Very Frightening", True, ['Channeling Book', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Enchanting', 'Ingot Crafting', 'Resource Blocks']],
            ])

    def test_42004(self):
        self.run_location_tests([
            ["Hot Stuff", False, []], 
            ["Hot Stuff", False, [], ["Bucket"]],
            ["Hot Stuff", False, [], ["Ingot Crafting"]],
            ["Hot Stuff", False, [], ["Progressive Tools"]],
            ["Hot Stuff", True, ["Bucket", "Ingot Crafting", "Progressive Tools"]],  
            ])

    def test_42005(self):
        self.run_location_tests([
            ["The End", False, []],
            ])

    def test_42006(self): 
        self.run_location_tests([
            ["A Furious Cocktail", False, []], 
            ["A Furious Cocktail", False, [], ['Ingot Crafting']], 
            ["A Furious Cocktail", False, [], ['Flint and Steel']], 
            ["A Furious Cocktail", False, [], ['Progressive Tools']], 
            ["A Furious Cocktail", False, [], ['Progressive Weapons']], 
            ["A Furious Cocktail", False, [], ['Progressive Armor']], 
            ["A Furious Cocktail", False, [], ['Brewing']], 
            ["A Furious Cocktail", False, [], ['Bottles']], 
            ["A Furious Cocktail", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["A Furious Cocktail", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']], 
            ["A Furious Cocktail", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']],
            ])

    def test_42007(self):
        self.run_location_tests([
            ["Best Friends Forever", True, []],
            ])

    def test_42008(self):
        self.run_location_tests([
            ["Bring Home the Beacon", False, []],
            ])

    def test_42009(self):
        self.run_location_tests([
            ["Not Today, Thank You", False, []], 
            ["Not Today, Thank You", False, [], ["Shield"]], 
            ["Not Today, Thank You", False, [], ["Ingot Crafting"]], 
            ["Not Today, Thank You", False, [], ["Progressive Tools"]], 
            ["Not Today, Thank You", True, ["Shield", "Ingot Crafting", "Progressive Tools"]], 
            ])

    def test_42010(self):
        self.run_location_tests([
            ["Isn't It Iron Pick", False, []], 
            ["Isn't It Iron Pick", True, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]], 
            ["Isn't It Iron Pick", False, [], ["Progressive Tools", "Progressive Tools"]], 
            ["Isn't It Iron Pick", False, [], ["Ingot Crafting"]], 
            ["Isn't It Iron Pick", False, ["Progressive Tools", "Ingot Crafting"]], 
            ["Isn't It Iron Pick", True, ["Progressive Tools", "Progressive Tools", "Ingot Crafting"]], 
            ])

    def test_42011(self): 
        self.run_location_tests([
            ["Local Brewery", False, []], 
            ["Local Brewery", False, [], ['Ingot Crafting']], 
            ["Local Brewery", False, [], ['Flint and Steel']], 
            ["Local Brewery", False, [], ['Progressive Tools']], 
            ["Local Brewery", False, [], ['Progressive Weapons']], 
            ["Local Brewery", False, [], ['Progressive Armor']], 
            ["Local Brewery", False, [], ['Brewing']], 
            ["Local Brewery", False, [], ['Bottles']],
            ["Local Brewery", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Local Brewery", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']], 
            ["Local Brewery", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor', 'Brewing', 'Bottles']],
            ])

    def test_42012(self):
        self.run_location_tests([
            ["The Next Generation", False, []],
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
            ["Hot Tourist Destinations", False, [], ['Ingot Crafting']], 
            ["Hot Tourist Destinations", False, [], ['Flint and Steel']], 
            ["Hot Tourist Destinations", False, [], ['Progressive Tools']], 
            ["Hot Tourist Destinations", False, [], ['Fishing Rod']],
            ["Hot Tourist Destinations", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Hot Tourist Destinations", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Fishing Rod']], 
            ["Hot Tourist Destinations", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Fishing Rod']],
            ])

    def test_42015(self):
        self.run_location_tests([
            ["This Boat Has Legs", False, []], 
            ["This Boat Has Legs", False, [], ['Ingot Crafting']], 
            ["This Boat Has Legs", False, [], ['Flint and Steel']], 
            ["This Boat Has Legs", False, [], ['Progressive Tools']], 
            ["This Boat Has Legs", False, [], ['Fishing Rod']],
            ["This Boat Has Legs", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["This Boat Has Legs", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Fishing Rod']], 
            ["This Boat Has Legs", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Fishing Rod']],
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
            ["Nether", False, [], ['Ingot Crafting']], 
            ["Nether", False, [], ['Flint and Steel']], 
            ["Nether", False, [], ['Progressive Tools']], 
            ["Nether", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Nether", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["Nether", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42018(self):
        self.run_location_tests([
            ["Great View From Up Here", False, []],
            ])

    def test_42019(self):
        self.run_location_tests([
            ["How Did We Get Here?", False, []],
            ])

    def test_42020(self):
        self.run_location_tests([
            ["Bullseye", False, []],
            ["Bullseye", False, [], ['Archery']],
            ["Bullseye", False, [], ['Ingot Crafting']],
            ["Bullseye", False, [], ['Progressive Tools']],
            ["Bullseye", True, ['Progressive Tools', 'Progressive Tools', 'Ingot Crafting', 'Archery']],
            ])

    def test_42021(self):
        self.run_location_tests([
            ["Spooky Scary Skeleton", False, []], 
            ["Spooky Scary Skeleton", False, [], ['Ingot Crafting']], 
            ["Spooky Scary Skeleton", False, [], ['Flint and Steel']], 
            ["Spooky Scary Skeleton", False, [], ['Progressive Tools']], 
            ["Spooky Scary Skeleton", False, [], ['Progressive Weapons']], 
            ["Spooky Scary Skeleton", False, [], ['Progressive Armor']], 
            ["Spooky Scary Skeleton", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Spooky Scary Skeleton", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor']], 
            ["Spooky Scary Skeleton", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor']],
            ])

    def test_42022(self):
        self.run_location_tests([
            ["Two by Two", False, []],
            ])

    def test_42023(self):
        self.run_location_tests([
            ["Stone Age", True, []],
            ])

    def test_42024(self):
        self.run_location_tests([
            ["Two Birds, One Arrow", False, []],
            ])

    def test_42025(self):
        self.run_location_tests([
            ["We Need to Go Deeper", False, []], 
            ["We Need to Go Deeper", False, [], ['Ingot Crafting']], 
            ["We Need to Go Deeper", False, [], ['Flint and Steel']], 
            ["We Need to Go Deeper", False, [], ['Progressive Tools']], 
            ["We Need to Go Deeper", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["We Need to Go Deeper", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["We Need to Go Deeper", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42026(self):
        self.run_location_tests([
            ["Who's the Pillager Now?", False, []],
            ["Who's the Pillager Now?", False, [], ['Archery']],
            ["Who's the Pillager Now?", False, [], ['Ingot Crafting']],
            ["Who's the Pillager Now?", False, [], ['Progressive Tools']],
            ["Who's the Pillager Now?", False, [], ['Progressive Weapons']],
            ["Who's the Pillager Now?", True, ['Archery', 'Progressive Tools', 'Progressive Weapons', 'Ingot Crafting']],
            ])

    def test_42027(self):
        self.run_location_tests([
            ["Getting an Upgrade", False, []],
            ["Getting an Upgrade", True, ["Progressive Tools"]],
            ])

    def test_42028(self):
        self.run_location_tests([
            ["Tactical Fishing", False, []],
            ["Tactical Fishing", False, [], ['Ingot Crafting']],
            ["Tactical Fishing", False, [], ['Progressive Tools']],
            ["Tactical Fishing", False, [], ['Bucket']],
            ["Tactical Fishing", True, ['Ingot Crafting', 'Progressive Tools', 'Bucket']],
            ])

    def test_42029(self):
        self.run_location_tests([
            ["Zombie Doctor", False, []],
            ])

    def test_42030(self):
        self.run_location_tests([
            ["The City at the End of the Game", False, []],
            ])

    def test_42031(self):
        self.run_location_tests([
            ["Ice Bucket Challenge", False, []], 
            ["Ice Bucket Challenge", False, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]],
            ["Ice Bucket Challenge", False, [], ["Ingot Crafting"]],
            ["Ice Bucket Challenge", True, ["Progressive Tools", "Progressive Tools", "Progressive Tools", "Ingot Crafting"]],
            ])

    def test_42032(self):
        self.run_location_tests([
            ["Remote Getaway", False, []],
            ])

    def test_42033(self):
        self.run_location_tests([
            ["Into Fire", False, []], 
            ["Into Fire", False, [], ['Ingot Crafting']], 
            ["Into Fire", False, [], ['Flint and Steel']], 
            ["Into Fire", False, [], ['Progressive Tools']], 
            ["Into Fire", False, [], ['Progressive Weapons']], 
            ["Into Fire", False, [], ['Progressive Armor']], 
            ["Into Fire", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Into Fire", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket', 'Progressive Weapons', 'Progressive Armor']], 
            ["Into Fire", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools', 'Progressive Weapons', 'Progressive Armor']],
            ])

    def test_42034(self):
        self.run_location_tests([
            ["War Pigs", False, []], 
            ["War Pigs", False, [], ['Ingot Crafting']], 
            ["War Pigs", False, [], ['Flint and Steel']], 
            ["War Pigs", False, [], ['Progressive Tools']], 
            ["War Pigs", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["War Pigs", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["War Pigs", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
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
            ["Total Beelocation", False, [], ['Resource Blocks']],
            ["Total Beelocation", False, [], ['Ingot Crafting']],
            ["Total Beelocation", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Total Beelocation", True, ['Enchanting', 'Silk Touch Book', 'Resource Blocks', 'Ingot Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42037(self):
        self.run_location_tests([
            ["Arbalistic", False, []],
            ["Arbalistic", False, [], ['Enchanting']],
            ["Arbalistic", False, [], ['Piercing IV Book']],
            ["Arbalistic", False, [], ['Resource Blocks']],
            ["Arbalistic", False, [], ['Ingot Crafting']],
            ["Arbalistic", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Arbalistic", False, [], ['Archery']], 
            ["Arbalistic", True, ['Enchanting', 'Piercing IV Book', 'Resource Blocks', 'Ingot Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Archery']],
            ])

    def test_42038(self): 
        self.run_location_tests([
            ["The End... Again...", False, []],
            ])

    def test_42039(self):
        self.run_location_tests([
            ["Acquire Hardware", False, []], 
            ["Acquire Hardware", False, [], ["Progressive Tools"]],
            ["Acquire Hardware", False, [], ["Ingot Crafting"]],
            ["Acquire Hardware", True, ["Progressive Tools", "Ingot Crafting"]],
            ])

    def test_42040(self):
        self.run_location_tests([
            ["Not Quite \"Nine\" Lives", False, []], 
            ["Not Quite \"Nine\" Lives", False, [], ['Ingot Crafting']], 
            ["Not Quite \"Nine\" Lives", False, [], ['Flint and Steel']], 
            ["Not Quite \"Nine\" Lives", False, [], ['Progressive Tools']], 
            ["Not Quite \"Nine\" Lives", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Not Quite \"Nine\" Lives", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["Not Quite \"Nine\" Lives", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42041(self):
        self.run_location_tests([
            ["Cover Me With Diamonds", False, []],
            ["Cover Me With Diamonds", False, ['Progressive Armor'], ['Progressive Armor']],
            ["Cover Me With Diamonds", False, ['Progressive Tools'], ['Progressive Tools', 'Progressive Tools']],
            ["Cover Me With Diamonds", False, [], ['Ingot Crafting']],
            ["Cover Me With Diamonds", True, ['Ingot Crafting', 'Progressive Tools', 'Progressive Tools', 'Progressive Armor', 'Progressive Armor']],
            ])

    def test_42042(self):
        self.run_location_tests([
            ["Sky's the Limit", False, []],
            ])

    def test_42043(self):
        self.run_location_tests([
            ["Hired Help", False, []],
            ["Hired Help", False, [], ['Resource Blocks']],
            ["Hired Help", False, [], ['Ingot Crafting']],
            ["Hired Help", False, [], ['Progressive Tools']],
            ["Hired Help", True, ['Progressive Tools', 'Ingot Crafting', 'Resource Blocks']],
            ])

    def test_42044(self):
        self.run_location_tests([
            ["Return to Sender", False, []], 
            ["Return to Sender", False, [], ['Ingot Crafting']], 
            ["Return to Sender", False, [], ['Flint and Steel']], 
            ["Return to Sender", False, [], ['Progressive Tools']], 
            ["Return to Sender", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Return to Sender", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["Return to Sender", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42045(self):
        self.run_location_tests([
            ["Sweet Dreams", False, []],
            ["Sweet Dreams", True, ['Bed']],
            ["Sweet Dreams", False, [], ['Bed', 'Progressive Weapons']],
            ["Sweet Dreams", False, [], ['Bed', 'Ingot Crafting', 'Campfire']],
            ["Sweet Dreams", True, ['Progressive Weapons', 'Ingot Crafting'], ['Bed', 'Campfire']],
            ["Sweet Dreams", True, ['Progressive Weapons', 'Campfire'], ['Bed', 'Ingot Crafting']],
            ])

    def test_42046(self):
        self.run_location_tests([
            ["You Need a Mint", False, []],
            ])

    def test_42047(self):
        self.run_location_tests([
            ["Adventure", True, []],
            ])

    def test_42048(self):
        self.run_location_tests([
            ["Monsters Hunted", False, []],
            ])

    def test_42049(self):
        self.run_location_tests([
            ["Enchanter", False, []],
            ["Enchanter", False, [], ['Enchanting']],
            ["Enchanter", False, ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']],
            ["Enchanter", False, [], ['Ingot Crafting']],
            ["Enchanter", True, ['Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Enchanting', 'Ingot Crafting']],
            ])

    def test_42050(self):
        self.run_location_tests([
            ["Voluntary Exile", False, []],
            ["Voluntary Exile", False, [], ['Progressive Weapons']],
            ["Voluntary Exile", False, [], ['Campfire', 'Ingot Crafting']],
            ["Voluntary Exile", True, ['Progressive Weapons', 'Campfire']],
            ["Voluntary Exile", True, ['Progressive Weapons', 'Ingot Crafting']],
            ])

    def test_42051(self):
        self.run_location_tests([
            ["Eye Spy", False, []],
            ])

    def test_42052(self):
        self.run_location_tests([
            ["The End", False, []],
            ])

    def test_42053(self):
        self.run_location_tests([
            ["Serious Dedication", False, []],
            ])

    def test_42054(self):
        self.run_location_tests([
            ["Postmortal", False, []],
            ])

    def test_42055(self):
        self.run_location_tests([
            ["Monster Hunter", True, []],
            ])

    def test_42056(self):
        self.run_location_tests([
            ["Adventuring Time", False, []],
            ["Adventuring Time", False, [], ['Progressive Weapons']],
            ["Adventuring Time", False, [], ['Campfire', 'Ingot Crafting']],
            ["Adventuring Time", True, ['Progressive Weapons', 'Campfire']],
            ["Adventuring Time", True, ['Progressive Weapons', 'Ingot Crafting']],
            ])

    def test_42057(self):
        self.run_location_tests([
            ["A Seedy Place", True, []],
            ])

    def test_42058(self):
        self.run_location_tests([
            ["Those Were the Days", False, []], 
            ["Those Were the Days", False, [], ['Ingot Crafting']], 
            ["Those Were the Days", False, [], ['Flint and Steel']], 
            ["Those Were the Days", False, [], ['Progressive Tools']], 
            ["Those Were the Days", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Those Were the Days", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["Those Were the Days", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42059(self):
        self.run_location_tests([
            ["Hero of the Village", False, []],
            ])

    def test_42060(self):
        self.run_location_tests([
            ["Hidden in the Depths", False, []],
            ])

    def test_42061(self):
        self.run_location_tests([
            ["Beaconator", False, []],
            ])

    def test_42062(self):
        self.run_location_tests([
            ["Withering Heights", False, []],
            ])

    def test_42063(self):
        self.run_location_tests([
            ["A Balanced Diet", False, []],
            ])

    def test_42064(self):
        self.run_location_tests([
            ["Subspace Bubble", False, []], 
            ["Subspace Bubble", False, [], ['Ingot Crafting']], 
            ["Subspace Bubble", False, [], ['Flint and Steel']], 
            ["Subspace Bubble", False, [], ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']], 
            ["Subspace Bubble", True, ['Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Flint and Steel', 'Ingot Crafting']], 
            ])

    def test_42065(self):
        self.run_location_tests([
            ["Husbandry", True, []],
            ])

    def test_42066(self):
        self.run_location_tests([
            ["Country Lode, Take Me Home", False, []],
            ])

    def test_42067(self):
        self.run_location_tests([
            ["Bee Our Guest", False, []],
            ["Bee Our Guest", False, [], ['Campfire']],
            ["Bee Our Guest", False, [], ['Bottles']],
            ["Bee Our Guest", False, [], ['Ingot Crafting']],
            ["Bee Our Guest", True, ['Campfire', 'Bottles', 'Ingot Crafting']],
            ])

    def test_42068(self):
        self.run_location_tests([
            ["What a Deal!", False, []],
            ["What a Deal!", False, [], ['Progressive Weapons']],
            ["What a Deal!", False, [], ['Campfire', 'Ingot Crafting']],
            ["What a Deal!", True, ['Progressive Weapons', 'Campfire']],
            ["What a Deal!", True, ['Progressive Weapons', 'Ingot Crafting']],
            ])

    def test_42069(self):
        self.run_location_tests([
            ["Uneasy Alliance", False, []], 
            ["Uneasy Alliance", False, [], ['Ingot Crafting']], 
            ["Uneasy Alliance", False, [], ['Flint and Steel']], 
            ["Uneasy Alliance", False, [], ['Progressive Tools', 'Progressive Tools'], ['Progressive Tools']], 
            ["Uneasy Alliance", True, ['Progressive Tools', 'Progressive Tools', 'Progressive Tools', 'Flint and Steel', 'Ingot Crafting']], 
            ])

    def test_42070(self):
        self.run_location_tests([
            ["Diamonds!", False, []], 
            ["Diamonds!", True, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]], 
            ["Diamonds!", False, [], ["Progressive Tools", "Progressive Tools"]], 
            ["Diamonds!", False, [], ["Ingot Crafting"]], 
            ["Diamonds!", False, ["Progressive Tools", "Ingot Crafting"]], 
            ["Diamonds!", True, ["Progressive Tools", "Progressive Tools", "Ingot Crafting"]], 
            ])

    def test_42071(self):
        self.run_location_tests([
            ["A Terrible Fortress", False, []], 
            ["A Terrible Fortress", False, [], ['Ingot Crafting']], 
            ["A Terrible Fortress", False, [], ['Flint and Steel']], 
            ["A Terrible Fortress", False, [], ['Progressive Tools']], 
            ["A Terrible Fortress", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["A Terrible Fortress", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Bucket']], 
            ["A Terrible Fortress", True, ['Ingot Crafting', 'Progressive Tools', 'Flint and Steel', 'Progressive Tools', 'Progressive Tools']],
            ])

    def test_42072(self):
        self.run_location_tests([
            ["A Throwaway Joke", True, []],
            ])

    def test_42073(self):
        self.run_location_tests([
            ["Minecraft", True, []],
            ])

    def test_42074(self):
        self.run_location_tests([
            ["Sticky Situation", False, []],
            ["Sticky Situation", False, [], ['Bottles']],
            ["Sticky Situation", False, [], ['Ingot Crafting']],
            ["Sticky Situation", True, ['Bottles', 'Ingot Crafting']],
            ])

    def test_42075(self):
        self.run_location_tests([
            ["Ol' Betsy", False, []],
            ["Ol' Betsy", False, [], ['Archery']],
            ["Ol' Betsy", False, [], ['Ingot Crafting']],
            ["Ol' Betsy", False, [], ['Progressive Tools']],
            ["Ol' Betsy", True, ['Archery', 'Ingot Crafting', 'Progressive Tools']],
            ])

    def test_42076(self):
        self.run_location_tests([
            ["Cover Me in Debris", False, []],
            ])

    def test_42077(self):
        self.run_location_tests([
            ["The End?", False, []],
            ])

    def test_42078(self):
        self.run_location_tests([
            ["The Parrots and the Bats", True, []],
            ])

    def test_42079(self):
        self.run_location_tests([
            ["A Complete Catalogue", False, []],
            ["A Complete Catalogue", False, [], ['Progressive Weapons']],
            ["A Complete Catalogue", False, [], ['Campfire', 'Ingot Crafting']],
            ["A Complete Catalogue", True, ['Progressive Weapons', 'Campfire']],
            ["A Complete Catalogue", True, ['Progressive Weapons', 'Ingot Crafting']],
            ])

