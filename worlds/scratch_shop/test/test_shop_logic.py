from test.bases import WorldTestBase


class ScratchShopTestBase(WorldTestBase):
    """
    The core base setup for all Scratch Shop tests. 
    This tells the testing framework which game we are evaluating.
    """
    game = "Scratch Shop"


class TestScratchShopStandard(ScratchShopTestBase):
    """
    This class automatically runs the core Archipelago checks using default options:
    1. Can everything be reached if we have all items?
    2. Can at least something be reached with no items?
    3. Can the multiworld generate and fill successfully?
    """
    pass


class TestScratchShopRules(ScratchShopTestBase):
    """
    Explicitly tests your logic rules to ensure item requirements are enforced.
    """

    def test_shop_1_is_free(self) -> None:
        """Shop 1 has no access rules in __init__.py, so it must be reachable immediately."""
        self.assertTrue(self.can_reach_location("Shop 1"))

    def test_coin_progression_gates(self) -> None:
        """Verify that shops require their specific coins and block players without them."""
        
        # A dictionary mapping locations to their strict coin requirements based on your __init__.py
        progression_map = {
            "Shop 2": "Red Coin",
            "Shop 3": "Blue Coin",
            "Shop 4": "Orange Coin",
            "Shop 11": "Gold Coin",
            "Shop 12": "Silver Coin",
            "Shop 15": "Copper Coin",
        }

        for location, required_coin in progression_map.items():
            # 1. Assert that without the coin, the location is unreachable
            self.assertFalse(
                self.can_reach_location(location),
                f"{location} should be locked if the player does not have a {required_coin}!"
            )

            # 2. Give the player the specific coin
            self.collect_by_name(required_coin)

            # 3. Assert that with the coin, the location is now unlocked
            self.assertTrue(
                self.can_reach_location(location),
                f"{location} failed to unlock even though the player collected a {required_coin}!"
            )

            # 4. Reset the item pool state back to empty for the next loop iteration
            #self.remove_from_pool(required_coin)


class TestScratchShopOptions(ScratchShopTestBase):
    """
    Tests that changes to user options don't break generation.
    """
    options = {
        "useless_toggle": 1  # 1 represents 'True' or Enabled for Toggle options
    }

    def test_toggle_generation(self) -> None:
        """Verifies that enabling the useless_toggle doesn't break basic logic flow."""
        self.assertTrue(self.can_reach_location("Shop 1"))