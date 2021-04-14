from test.minecraft.TestMinecraft import TestMinecraft

# Format: 
# [location, expected_result, given_items, [excluded_items]]
class TestNetherAdvancements(TestMinecraft):

    def test_advancements(self):
        self.run_location_tests([
            ["Who is Cutting Onions?", False, []], 
            ["Who is Cutting Onions?", False, [], ['Ingot Crafting']], 
            ["Who is Cutting Onions?", False, [], ['Flint & Steel']], 
            ["Who is Cutting Onions?", False, [], ['Progressive Tools']], 
            ["Who is Cutting Onions?", False, ['Progressive Tools', 'Progressive Tools'], ['Bucket', 'Progressive Tools']], 
            ["Who is Cutting Onions?", True, ['Ingot Crafting', 'Progressive Tools', 'Flint & Steel', 'Bucket']], 
            ["Who is Cutting Onions?", True, ['Ingot Crafting', 'Progressive Tools', 'Flint & Steel', 'Progressive Tools', 'Progressive Tools']]


        ])
