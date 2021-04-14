from test.minecraft.TestMinecraft import TestMinecraft

# Format: 
# [location, expected_result, given_items, [excluded_items]]
class TestStoryAdvancements(TestMinecraft):

    def test_advancements(self):
        self.run_location_tests([
            ["Minecraft", True, []],

            ["Stone Age", True, []],

            ["Getting an Upgrade", False, []],
            ["Getting an Upgrade", True, ["Progressive Tools"]],

            ["Acquire Hardware", False, []], 
            ["Acquire Hardware", False, [], ["Progressive Tools"]],
            ["Acquire Hardware", False, [], ["Ingot Crafting"]],
            ["Acquire Hardware", True, ["Progressive Tools", "Ingot Crafting"]],

            ["Suit Up", False, []],
            ["Suit Up", False, [], ["Progressive Armor"]],
            ["Suit Up", False, [], ["Ingot Crafting"]],
            ["Suit Up", False, [], ["Progressive Tools"]],
            ["Suit Up", True, ["Progressive Armor", "Ingot Crafting", "Progressive Tools"]],

            ["Hot Stuff", False, []], 
            ["Hot Stuff", False, [], ["Bucket"]],
            ["Hot Stuff", False, [], ["Ingot Crafting"]],
            ["Hot Stuff", False, [], ["Progressive Tools"]],
            ["Hot Stuff", True, ["Bucket", "Ingot Crafting", "Progressive Tools"]],  

            ["Isn't It Iron Pick", False, []], 
            ["Isn't It Iron Pick", True, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]], 
            ["Isn't It Iron Pick", False, [], ["Progressive Tools", "Progressive Tools"]], 
            ["Isn't It Iron Pick", False, [], ["Ingot Crafting"]], 
            ["Isn't It Iron Pick", False, ["Progressive Tools", "Ingot Crafting"]], 
            ["Isn't It Iron Pick", True, ["Progressive Tools", "Progressive Tools", "Ingot Crafting"]], 

            ["Not Today, Thank You", False, []], 
            ["Not Today, Thank You", False, [], ["Shield"]], 
            ["Not Today, Thank You", False, [], ["Ingot Crafting"]], 
            ["Not Today, Thank You", False, [], ["Progressive Tools"]], 
            ["Not Today, Thank You", True, ["Shield", "Ingot Crafting", "Progressive Tools"]], 

            ["Ice Bucket Challenge", False, []], 
            ["Ice Bucket Challenge", False, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]],
            ["Ice Bucket Challenge", False, [], ["Ingot Crafting"]],
            ["Ice Bucket Challenge", True, ["Progressive Tools", "Progressive Tools", "Progressive Tools", "Ingot Crafting"]],

            ["Diamonds!", False, []], 
            ["Diamonds!", True, ["Progressive Tools", "Progressive Tools"], ["Progressive Tools"]], 
            ["Diamonds!", False, [], ["Progressive Tools", "Progressive Tools"]], 
            ["Diamonds!", False, [], ["Ingot Crafting"]], 
            ["Diamonds!", False, ["Progressive Tools", "Ingot Crafting"]], 
            ["Diamonds!", True, ["Progressive Tools", "Progressive Tools", "Ingot Crafting"]], 

            ["We Need to Go Deeper", False, []], 

            ["Cover Me With Diamonds", False, []], 

            ["Enchanter", False, []], 

            ["Zombie Doctor", False, []], 

            ["Eye Spy", False, []], 

            ["The End?", False, []]

        ])
