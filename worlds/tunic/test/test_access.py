from . import TunicTestBase
from .. import options


class TestAccess(TunicTestBase):
    options = {options.CombatLogic.internal_name: options.CombatLogic.option_off}

    # test whether you can get into the temple without laurels
    def test_temple_access(self) -> None:
        self.collect_all_but(["Hero's Laurels", "Lantern"])
        self.assertFalse(self.can_reach_location("Sealed Temple - Page Pickup"))
        self.collect_by_name(["Lantern"])
        self.assertTrue(self.can_reach_location("Sealed Temple - Page Pickup"))

    # test that the wells function properly. Since fairies is written the same way, that should succeed too
    def test_wells(self) -> None:
        self.collect_all_but(["Golden Coin"])
        self.assertFalse(self.can_reach_location("Coins in the Well - 3 Coins"))
        self.collect_by_name(["Golden Coin"])
        self.assertTrue(self.can_reach_location("Coins in the Well - 3 Coins"))


class TestStandardShuffle(TunicTestBase):
    options = {options.AbilityShuffling.internal_name: options.AbilityShuffling.option_true}

    # test that you need to get holy cross to open the hc door in overworld
    def test_hc_door(self) -> None:
        self.assertFalse(self.can_reach_location("Fountain Cross Door - Page Pickup"))
        self.collect_by_name("Pages 42-43 (Holy Cross)")
        self.assertTrue(self.can_reach_location("Fountain Cross Door - Page Pickup"))


class TestHexQuestShuffle(TunicTestBase):
    options = {options.HexagonQuest.internal_name: options.HexagonQuest.option_true,
               options.AbilityShuffling.internal_name: options.AbilityShuffling.option_true}

    # test that you need the gold questagons to open the hc door in overworld
    def test_hc_door_hex_shuffle(self) -> None:
        self.assertFalse(self.can_reach_location("Fountain Cross Door - Page Pickup"))
        self.collect_by_name("Gold Questagon")
        self.assertTrue(self.can_reach_location("Fountain Cross Door - Page Pickup"))


class TestHexQuestNoShuffle(TunicTestBase):
    options = {options.HexagonQuest.internal_name: options.HexagonQuest.option_true,
               options.AbilityShuffling.internal_name: options.AbilityShuffling.option_false}

    # test that you can get the item behind the overworld hc door with nothing and no ability shuffle
    def test_hc_door_no_shuffle(self) -> None:
        self.assertTrue(self.can_reach_location("Fountain Cross Door - Page Pickup"))


class TestNormalGoal(TunicTestBase):
    options = {options.HexagonQuest.internal_name: options.HexagonQuest.option_false}

    # test that you need the three colored hexes to reach the Heir in standard
    def test_normal_goal(self) -> None:
        location = ["The Heir"]
        items = [["Red Questagon", "Blue Questagon", "Green Questagon"]]
        self.assertAccessDependency(location, items)


class TestER(TunicTestBase):
    options = {options.EntranceRando.internal_name: options.EntranceRando.option_yes,
               options.AbilityShuffling.internal_name: options.AbilityShuffling.option_true,
               options.HexagonQuest.internal_name: options.HexagonQuest.option_false,
               options.CombatLogic.internal_name: options.CombatLogic.option_off,
               options.FixedShop.internal_name: options.FixedShop.option_true}

    def test_overworld_hc_chest(self) -> None:
        # test to see that static connections are working properly -- this chest requires holy cross and is in Overworld
        self.assertFalse(self.can_reach_location("Overworld - [Southwest] Flowers Holy Cross"))
        self.collect_by_name(["Pages 42-43 (Holy Cross)"])
        self.assertTrue(self.can_reach_location("Overworld - [Southwest] Flowers Holy Cross"))


class TestERSpecial(TunicTestBase):
    options = {options.EntranceRando.internal_name: options.EntranceRando.option_yes,
               options.AbilityShuffling.internal_name: options.AbilityShuffling.option_true,
               options.HexagonQuest.internal_name: options.HexagonQuest.option_false,
               options.FixedShop.internal_name: options.FixedShop.option_false,
               options.IceGrappling.internal_name: options.IceGrappling.option_easy,
               "plando_connections": [
                   {
                       "entrance": "Stick House Entrance",
                       "exit": "Ziggurat Portal Room Entrance"
                   },
                   {
                       "entrance": "Ziggurat Lower to Ziggurat Tower",
                       "exit": "Secret Gathering Place Exit"
                   }
               ]}
    # with these plando connections, you need to ice grapple from the back of lower zig to the front to get laurels


# ensure that ladder storage connections connect to the outlet region, not the portal's region
class TestLadderStorage(TunicTestBase):
    options = {options.EntranceRando.internal_name: options.EntranceRando.option_yes,
               options.AbilityShuffling.internal_name: options.AbilityShuffling.option_true,
               options.HexagonQuest.internal_name: options.HexagonQuest.option_false,
               options.FixedShop.internal_name: options.FixedShop.option_false,
               options.LadderStorage.internal_name: options.LadderStorage.option_hard,
               options.LadderStorageWithoutItems.internal_name: options.LadderStorageWithoutItems.option_false,
               "plando_connections": [
                   {
                       "entrance": "Fortress Courtyard Shop",
                       # "exit": "Ziggurat Portal Room Exit"
                       "exit": "Spawn to Far Shore"
                   },
                   {
                       "entrance": "Fortress Courtyard to Beneath the Vault",
                       "exit": "Stick House Exit"
                   },
                   {
                       "entrance": "Stick House Entrance",
                       "exit": "Fortress Courtyard to Overworld"
                   },
                   {
                       "entrance": "Old House Waterfall Entrance",
                       "exit": "Ziggurat Portal Room Entrance"
                   },
               ]}

    def test_ls_to_shop_entrance(self) -> None:
        self.collect_by_name(["Magic Orb"])
        self.assertFalse(self.can_reach_location("Fortress Courtyard - Page Near Cave"))
        self.collect_by_name(["Pages 24-25 (Prayer)"])
        self.assertTrue(self.can_reach_location("Fortress Courtyard - Page Near Cave"))
