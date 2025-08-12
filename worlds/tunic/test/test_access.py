from .. import options
from .bases import TunicTestBase


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
               options.CombatLogic.internal_name: options.CombatLogic.option_off,
               options.EntranceLayout.internal_name: options.EntranceLayout.option_fixed_shop,
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


# check that it still functions if in decoupled and every single normal entrance leads to a shop
class TestERDecoupledPlando(TunicTestBase):
    options = {options.EntranceRando.internal_name: options.EntranceRando.option_yes,
               options.Decoupled.internal_name: options.Decoupled.option_true,
               "plando_connections": [
                   {"entrance": "Stick House Entrance", "exit": "Shop Portal 1", "direction": "entrance"},
                   {"entrance": "Windmill Entrance", "exit": "Shop Portal 2", "direction": "entrance"},
                   {"entrance": "Well Ladder Entrance", "exit": "Shop Portal 3", "direction": "entrance"},
                   {"entrance": "Entrance to Well from Well Rail", "exit": "Shop Portal 4", "direction": "entrance"},
                   {"entrance": "Old House Door Entrance", "exit": "Shop Portal 5", "direction": "entrance"},
                   {"entrance": "Old House Waterfall Entrance", "exit": "Shop Portal 6", "direction": "entrance"},
                   {"entrance": "Entrance to Furnace from Well Rail", "exit": "Shop Portal 7", "direction": "entrance"},
                   {"entrance": "Entrance to Furnace under Windmill", "exit": "Shop Portal 8", "direction": "entrance"},
                   {"entrance": "Entrance to Furnace near West Garden", "exit": "Shop Portal 9",
                    "direction": "entrance"},
                   {"entrance": "Entrance to Furnace from Beach", "exit": "Shop Portal 10", "direction": "entrance"},
                   {"entrance": "Caustic Light Cave Entrance", "exit": "Shop Portal 11", "direction": "entrance"},
                   {"entrance": "Swamp Upper Entrance", "exit": "Shop Portal 12", "direction": "entrance"},
                   {"entrance": "Swamp Lower Entrance", "exit": "Shop Portal 13", "direction": "entrance"},
                   {"entrance": "Ruined Passage Not-Door Entrance", "exit": "Shop Portal 14", "direction": "entrance"},
                   {"entrance": "Ruined Passage Door Entrance", "exit": "Shop Portal 15", "direction": "entrance"},
                   {"entrance": "Atoll Upper Entrance", "exit": "Shop Portal 16", "direction": "entrance"},
                   {"entrance": "Atoll Lower Entrance", "exit": "Shop Portal 17", "direction": "entrance"},
                   {"entrance": "Special Shop Entrance", "exit": "Shop Portal 18", "direction": "entrance"},
                   {"entrance": "Maze Cave Entrance", "exit": "Shop Portal 19", "direction": "entrance"},
                   {"entrance": "West Garden Entrance near Belltower", "exit": "Shop Portal 20",
                    "direction": "entrance"},
                   {"entrance": "West Garden Entrance from Furnace", "exit": "Shop Portal 21", "direction": "entrance"},
                   {"entrance": "West Garden Laurels Entrance", "exit": "Shop Portal 22", "direction": "entrance"},
                   {"entrance": "Temple Door Entrance", "exit": "Shop Portal 23", "direction": "entrance"},
                   {"entrance": "Temple Rafters Entrance", "exit": "Shop Portal 24", "direction": "entrance"},
                   {"entrance": "Ruined Shop Entrance", "exit": "Shop Portal 25", "direction": "entrance"},
                   {"entrance": "Patrol Cave Entrance", "exit": "Shop Portal 26", "direction": "entrance"},
                   {"entrance": "Hourglass Cave Entrance", "exit": "Shop Portal 27", "direction": "entrance"},
                   {"entrance": "Changing Room Entrance", "exit": "Shop Portal 28", "direction": "entrance"},
                   {"entrance": "Cube Cave Entrance", "exit": "Shop Portal 29", "direction": "entrance"},
                   {"entrance": "Stairs from Overworld to Mountain", "exit": "Shop Portal 30", "direction": "entrance"},
                   {"entrance": "Overworld to Fortress", "exit": "Shop Portal 31", "direction": "entrance"},
                   {"entrance": "Fountain HC Door Entrance", "exit": "Shop Portal 32", "direction": "entrance"},
                   {"entrance": "Southeast HC Door Entrance", "exit": "Shop Portal 33", "direction": "entrance"},
                   {"entrance": "Overworld to Quarry Connector", "exit": "Shop Portal 34", "direction": "entrance"},
                   {"entrance": "Dark Tomb Main Entrance", "exit": "Shop Portal 35", "direction": "entrance"},
                   {"entrance": "Overworld to Forest Belltower", "exit": "Shop Portal 36", "direction": "entrance"},
                   {"entrance": "Town to Far Shore", "exit": "Shop Portal 37", "direction": "entrance"},
                   {"entrance": "Spawn to Far Shore", "exit": "Shop Portal 38", "direction": "entrance"},
                   {"entrance": "Secret Gathering Place Entrance", "exit": "Shop Portal 39", "direction": "entrance"},
                   {"entrance": "Secret Gathering Place Exit", "exit": "Shop Portal 40", "direction": "entrance"},
                   {"entrance": "Windmill Exit", "exit": "Shop Portal 41", "direction": "entrance"},
                   {"entrance": "Windmill Shop", "exit": "Shop Portal 42", "direction": "entrance"},
                   {"entrance": "Old House Door Exit", "exit": "Shop Portal 43", "direction": "entrance"},
                   {"entrance": "Old House to Glyph Tower", "exit": "Shop Portal 44", "direction": "entrance"},
                   {"entrance": "Old House Waterfall Exit", "exit": "Shop Portal 45", "direction": "entrance"},
                   {"entrance": "Glyph Tower Exit", "exit": "Shop Portal 46", "direction": "entrance"},
                   {"entrance": "Changing Room Exit", "exit": "Shop Portal 47", "direction": "entrance"},
                   {"entrance": "Fountain HC Room Exit", "exit": "Shop Portal 48", "direction": "entrance"},
                   {"entrance": "Cube Cave Exit", "exit": "Shop Portal 49", "direction": "entrance"},
                   {"entrance": "Guard Patrol Cave Exit", "exit": "Shop Portal 50", "direction": "entrance"},
                   {"entrance": "Ruined Shop Exit", "exit": "Shop Portal 51", "direction": "entrance"},
                   {"entrance": "Furnace Exit towards Well", "exit": "Shop Portal 52", "direction": "entrance"},
                   {"entrance": "Furnace Exit to Dark Tomb", "exit": "Shop Portal 53", "direction": "entrance"},
                   {"entrance": "Furnace Exit towards West Garden", "exit": "Shop Portal 54", "direction": "entrance"},
                   {"entrance": "Furnace Exit to Beach", "exit": "Shop Portal 55", "direction": "entrance"},
                   {"entrance": "Furnace Exit under Windmill", "exit": "Shop Portal 56", "direction": "entrance"},
                   {"entrance": "Stick House Exit", "exit": "Shop Portal 57", "direction": "entrance"},
                   {"entrance": "Ruined Passage Not-Door Exit", "exit": "Shop Portal 58", "direction": "entrance"},
                   {"entrance": "Ruined Passage Door Exit", "exit": "Shop Portal 59", "direction": "entrance"},
                   {"entrance": "Southeast HC Room Exit", "exit": "Shop Portal 60", "direction": "entrance"},
                   {"entrance": "Caustic Light Cave Exit", "exit": "Shop Portal 61", "direction": "entrance"},
                   {"entrance": "Maze Cave Exit", "exit": "Shop Portal 62", "direction": "entrance"},
                   {"entrance": "Hourglass Cave Exit", "exit": "Shop Portal 63", "direction": "entrance"},
                   {"entrance": "Special Shop Exit", "exit": "Shop Portal 64", "direction": "entrance"},
                   {"entrance": "Temple Rafters Exit", "exit": "Shop Portal 65", "direction": "entrance"},
                   {"entrance": "Temple Door Exit", "exit": "Shop Portal 66", "direction": "entrance"},
                   {"entrance": "Forest Belltower to Fortress", "exit": "Shop Portal 67", "direction": "entrance"},
                   {"entrance": "Forest Belltower to Forest", "exit": "Shop Portal 68", "direction": "entrance"},
                   {"entrance": "Forest Belltower to Overworld", "exit": "Shop Portal 69", "direction": "entrance"},
                   {"entrance": "Forest Belltower to Guard Captain Room", "exit": "Shop Portal 70",
                    "direction": "entrance"},
                   {"entrance": "Forest to Belltower", "exit": "Shop Portal 71", "direction": "entrance"},
                   {"entrance": "Forest Guard House 1 Lower Entrance", "exit": "Shop Portal 72",
                    "direction": "entrance"},
                   {"entrance": "Forest Guard House 1 Gate Entrance", "exit": "Shop Portal 73",
                    "direction": "entrance"},
                   {"entrance": "Forest Dance Fox Outside Doorway", "exit": "Shop Portal 74", "direction": "entrance"},
                   {"entrance": "Forest to Far Shore", "exit": "Shop Portal 75", "direction": "entrance"},
                   {"entrance": "Forest Guard House 2 Lower Entrance", "exit": "Shop Portal 76",
                    "direction": "entrance"},
                   {"entrance": "Forest Guard House 2 Upper Entrance", "exit": "Shop Portal 77",
                    "direction": "entrance"},
                   {"entrance": "Forest Grave Path Lower Entrance", "exit": "Shop Portal 78", "direction": "entrance"},
                   {"entrance": "Forest Grave Path Upper Entrance", "exit": "Shop Portal 79", "direction": "entrance"},
                   {"entrance": "Forest Grave Path Upper Exit", "exit": "Shop Portal 80", "direction": "entrance"},
                   {"entrance": "Forest Grave Path Lower Exit", "exit": "Shop Portal 81", "direction": "entrance"},
                   {"entrance": "East Forest Hero's Grave", "exit": "Shop Portal 82", "direction": "entrance"},
                   {"entrance": "Guard House 1 Dance Fox Exit", "exit": "Shop Portal 83", "direction": "entrance"},
                   {"entrance": "Guard House 1 Lower Exit", "exit": "Shop Portal 84", "direction": "entrance"},
                   {"entrance": "Guard House 1 Upper Forest Exit", "exit": "Shop Portal 85", "direction": "entrance"},
                   {"entrance": "Guard House 1 to Guard Captain Room", "exit": "Shop Portal 86",
                    "direction": "entrance"},
                   {"entrance": "Guard House 2 Lower Exit", "exit": "Shop Portal 87", "direction": "entrance"},
                   {"entrance": "Guard House 2 Upper Exit", "exit": "Shop Portal 88", "direction": "entrance"},
                   {"entrance": "Guard Captain Room Non-Gate Exit", "exit": "Shop Portal 89", "direction": "entrance"},
                   {"entrance": "Guard Captain Room Gate Exit", "exit": "Shop Portal 90", "direction": "entrance"},
                   {"entrance": "Well Ladder Exit", "exit": "Shop Portal 91", "direction": "entrance"},
                   {"entrance": "Well to Well Boss", "exit": "Shop Portal 92", "direction": "entrance"},
                   {"entrance": "Well Exit towards Furnace", "exit": "Shop Portal 93", "direction": "entrance"},
                   {"entrance": "Well Boss to Well", "exit": "Shop Portal 94", "direction": "entrance"},
                   {"entrance": "Checkpoint to Dark Tomb", "exit": "Shop Portal 95", "direction": "entrance"},
                   {"entrance": "Dark Tomb to Overworld", "exit": "Shop Portal 96", "direction": "entrance"},
                   {"entrance": "Dark Tomb to Furnace", "exit": "Shop Portal 97", "direction": "entrance"},
                   {"entrance": "Dark Tomb to Checkpoint", "exit": "Shop Portal 98", "direction": "entrance"},
                   {"entrance": "West Garden Exit near Hero's Grave", "exit": "Shop Portal 99",
                    "direction": "entrance"},
                   {"entrance": "West Garden to Magic Dagger House", "exit": "Shop Portal 100",
                    "direction": "entrance"},
                   {"entrance": "West Garden Exit after Boss", "exit": "Shop Portal 101", "direction": "entrance"},
                   {"entrance": "West Garden Shop", "exit": "Shop Portal 102", "direction": "entrance"},
                   {"entrance": "West Garden Laurels Exit", "exit": "Shop Portal 103", "direction": "entrance"},
                   {"entrance": "West Garden Hero's Grave", "exit": "Shop Portal 104", "direction": "entrance"},
                   {"entrance": "West Garden to Far Shore", "exit": "Shop Portal 105", "direction": "entrance"},
                   {"entrance": "Magic Dagger House Exit", "exit": "Shop Portal 106", "direction": "entrance"},
                   {"entrance": "Fortress Courtyard to Fortress Grave Path Lower", "exit": "Shop Portal 107",
                    "direction": "entrance"},
                   {"entrance": "Fortress Courtyard to Fortress Grave Path Upper", "exit": "Shop Portal 108",
                    "direction": "entrance"},
                   {"entrance": "Fortress Courtyard to Fortress Interior", "exit": "Shop Portal 109",
                    "direction": "entrance"},
                   {"entrance": "Fortress Courtyard to East Fortress", "exit": "Shop Portal 110",
                    "direction": "entrance"},
                   {"entrance": "Fortress Courtyard to Beneath the Vault", "exit": "Shop Portal 111",
                    "direction": "entrance"},
                   {"entrance": "Fortress Courtyard to Forest Belltower", "exit": "Shop Portal 112",
                    "direction": "entrance"},
                   {"entrance": "Fortress Courtyard to Overworld", "exit": "Shop Portal 113", "direction": "entrance"},
                   {"entrance": "Fortress Courtyard Shop", "exit": "Shop Portal 114", "direction": "entrance"},
                   {"entrance": "Beneath the Vault to Fortress Interior", "exit": "Shop Portal 115",
                    "direction": "entrance"},
                   {"entrance": "Beneath the Vault to Fortress Courtyard", "exit": "Shop Portal 116",
                    "direction": "entrance"},
                   {"entrance": "Fortress Interior Main Exit", "exit": "Shop Portal 117", "direction": "entrance"},
                   {"entrance": "Fortress Interior to Beneath the Earth", "exit": "Shop Portal 118",
                    "direction": "entrance"},
                   {"entrance": "Fortress Interior to Siege Engine Arena", "exit": "Shop Portal 119",
                    "direction": "entrance"},
                   {"entrance": "Fortress Interior Shop", "exit": "Shop Portal 120", "direction": "entrance"},
                   {"entrance": "Fortress Interior to East Fortress Upper", "exit": "Shop Portal 121",
                    "direction": "entrance"},
                   {"entrance": "Fortress Interior to East Fortress Lower", "exit": "Shop Portal 122",
                    "direction": "entrance"},
                   {"entrance": "East Fortress to Interior Lower", "exit": "Shop Portal 123", "direction": "entrance"},
                   {"entrance": "East Fortress to Courtyard", "exit": "Shop Portal 124", "direction": "entrance"},
                   {"entrance": "East Fortress to Interior Upper", "exit": "Shop Portal 125", "direction": "entrance"},
                   {"entrance": "Fortress Grave Path Lower Exit", "exit": "Shop Portal 126", "direction": "entrance"},
                   {"entrance": "Fortress Hero's Grave", "exit": "Shop Portal 127", "direction": "entrance"},
                   {"entrance": "Fortress Grave Path Upper Exit", "exit": "Shop Portal 128", "direction": "entrance"},
                   {"entrance": "Fortress Grave Path Dusty Entrance", "exit": "Shop Portal 129",
                    "direction": "entrance"},
                   {"entrance": "Dusty Exit", "exit": "Shop Portal 130", "direction": "entrance"},
                   {"entrance": "Siege Engine Arena to Fortress", "exit": "Shop Portal 131", "direction": "entrance"},
                   {"entrance": "Fortress to Far Shore", "exit": "Shop Portal 132", "direction": "entrance"},
                   {"entrance": "Atoll Upper Exit", "exit": "Shop Portal 133", "direction": "entrance"},
                   {"entrance": "Atoll Lower Exit", "exit": "Shop Portal 134", "direction": "entrance"},
                   {"entrance": "Atoll Shop", "exit": "Shop Portal 135", "direction": "entrance"},
                   {"entrance": "Atoll to Far Shore", "exit": "Shop Portal 136", "direction": "entrance"},
                   {"entrance": "Atoll Statue Teleporter", "exit": "Shop Portal 137", "direction": "entrance"},
                   {"entrance": "Frog Stairs Eye Entrance", "exit": "Shop Portal 138", "direction": "entrance"},
                   {"entrance": "Frog Stairs Mouth Entrance", "exit": "Shop Portal 139", "direction": "entrance"},
                   {"entrance": "Frog Stairs Eye Exit", "exit": "Shop Portal 140", "direction": "entrance"},
                   {"entrance": "Frog Stairs Mouth Exit", "exit": "Shop Portal 141", "direction": "entrance"},
                   {"entrance": "Frog Stairs to Frog's Domain's Entrance", "exit": "Shop Portal 142",
                    "direction": "entrance"},
                   {"entrance": "Frog Stairs to Frog's Domain's Exit", "exit": "Shop Portal 143",
                    "direction": "entrance"},
                   {"entrance": "Frog's Domain Ladder Exit", "exit": "Shop Portal 144", "direction": "entrance"},
                   {"entrance": "Frog's Domain Orb Exit", "exit": "Shop Portal 145", "direction": "entrance"},
                   {"entrance": "Library Exterior Tree", "exit": "Shop Portal 146", "direction": "entrance"},
                   {"entrance": "Library Exterior Ladder", "exit": "Shop Portal 147", "direction": "entrance"},
                   {"entrance": "Library Hall Bookshelf Exit", "exit": "Shop Portal 148", "direction": "entrance"},
                   {"entrance": "Library Hero's Grave", "exit": "Shop Portal 149", "direction": "entrance"},
                   {"entrance": "Library Hall to Rotunda", "exit": "Shop Portal 150", "direction": "entrance"},
                   {"entrance": "Library Rotunda Lower Exit", "exit": "Shop Portal 151", "direction": "entrance"},
                   {"entrance": "Library Rotunda Upper Exit", "exit": "Shop Portal 152", "direction": "entrance"},
                   {"entrance": "Library Lab to Rotunda", "exit": "Shop Portal 153", "direction": "entrance"},
                   {"entrance": "Library to Far Shore", "exit": "Shop Portal 154", "direction": "entrance"},
                   {"entrance": "Library Lab to Librarian Arena", "exit": "Shop Portal 155", "direction": "entrance"},
                   {"entrance": "Librarian Arena Exit", "exit": "Shop Portal 156", "direction": "entrance"},
                   {"entrance": "Stairs to Top of the Mountain", "exit": "Shop Portal 157", "direction": "entrance"},
                   {"entrance": "Mountain to Quarry", "exit": "Shop Portal 158", "direction": "entrance"},
                   {"entrance": "Mountain to Overworld", "exit": "Shop Portal 159", "direction": "entrance"},
                   {"entrance": "Top of the Mountain Exit", "exit": "Shop Portal 160", "direction": "entrance"},
                   {"entrance": "Quarry Connector to Overworld", "exit": "Shop Portal 161", "direction": "entrance"},
                   {"entrance": "Quarry Connector to Quarry", "exit": "Shop Portal 162", "direction": "entrance"},
                   {"entrance": "Quarry to Overworld Exit", "exit": "Shop Portal 163", "direction": "entrance"},
                   {"entrance": "Quarry Shop", "exit": "Shop Portal 164", "direction": "entrance"},
                   {"entrance": "Quarry to Monastery Front", "exit": "Shop Portal 165", "direction": "entrance"},
                   {"entrance": "Quarry to Monastery Back", "exit": "Shop Portal 166", "direction": "entrance"},
                   {"entrance": "Quarry to Mountain", "exit": "Shop Portal 167", "direction": "entrance"},
                   {"entrance": "Quarry to Ziggurat", "exit": "Shop Portal 168", "direction": "entrance"},
                   {"entrance": "Quarry to Far Shore", "exit": "Shop Portal 169", "direction": "entrance"},
                   {"entrance": "Monastery Rear Exit", "exit": "Shop Portal 170", "direction": "entrance"},
                   {"entrance": "Monastery Front Exit", "exit": "Shop Portal 171", "direction": "entrance"},
                   {"entrance": "Monastery Hero's Grave", "exit": "Shop Portal 172", "direction": "entrance"},
                   {"entrance": "Ziggurat Entry Hallway to Ziggurat Upper", "exit": "Shop Portal 173",
                    "direction": "entrance"},
                   {"entrance": "Ziggurat Entry Hallway to Quarry", "exit": "Shop Portal 174", "direction": "entrance"},
                   {"entrance": "Ziggurat Upper to Ziggurat Entry Hallway", "exit": "Shop Portal 175",
                    "direction": "entrance"},
                   {"entrance": "Ziggurat Upper to Ziggurat Tower", "exit": "Shop Portal 176", "direction": "entrance"},
                   {"entrance": "Ziggurat Tower to Ziggurat Upper", "exit": "Shop Portal 177", "direction": "entrance"},
                   {"entrance": "Ziggurat Tower to Ziggurat Lower", "exit": "Shop Portal 178", "direction": "entrance"},
                   {"entrance": "Ziggurat Lower to Ziggurat Tower", "exit": "Shop Portal 179", "direction": "entrance"},
                   {"entrance": "Ziggurat Portal Room Entrance", "exit": "Shop Portal 180", "direction": "entrance"},
                   {"entrance": "Ziggurat Portal Room Exit", "exit": "Shop Portal 181", "direction": "entrance"},
                   {"entrance": "Ziggurat to Far Shore", "exit": "Shop Portal 182", "direction": "entrance"},
                   {"entrance": "Swamp Lower Exit", "exit": "Shop Portal 183", "direction": "entrance"},
                   {"entrance": "Swamp to Cathedral Main Entrance", "exit": "Shop Portal 184", "direction": "entrance"},
                   {"entrance": "Swamp to Cathedral Secret Legend Room Entrance", "exit": "Shop Portal 185",
                    "direction": "entrance"},
                   {"entrance": "Swamp to Gauntlet", "exit": "Shop Portal 186", "direction": "entrance"},
                   {"entrance": "Swamp Shop", "exit": "Shop Portal 187", "direction": "entrance"},
                   {"entrance": "Swamp Upper Exit", "exit": "Shop Portal 188", "direction": "entrance"},
                   {"entrance": "Swamp Hero's Grave", "exit": "Shop Portal 189", "direction": "entrance"},
                   {"entrance": "Cathedral Main Exit", "exit": "Shop Portal 190", "direction": "entrance"},
                   {"entrance": "Cathedral Elevator", "exit": "Shop Portal 191", "direction": "entrance"},
                   {"entrance": "Cathedral Secret Legend Room Exit", "exit": "Shop Portal 192",
                    "direction": "entrance"},
                   {"entrance": "Gauntlet to Swamp", "exit": "Shop Portal 193", "direction": "entrance"},
                   {"entrance": "Gauntlet Elevator", "exit": "Shop Portal 194", "direction": "entrance"},
                   {"entrance": "Gauntlet Shop", "exit": "Shop Portal 195", "direction": "entrance"},
                   {"entrance": "Hero's Grave to Fortress", "exit": "Shop Portal 196", "direction": "entrance"},
                   {"entrance": "Hero's Grave to Monastery", "exit": "Shop Portal 197", "direction": "entrance"},
                   {"entrance": "Hero's Grave to West Garden", "exit": "Shop Portal 198", "direction": "entrance"},
                   {"entrance": "Hero's Grave to East Forest", "exit": "Shop Portal 199", "direction": "entrance"},
                   {"entrance": "Hero's Grave to Library", "exit": "Shop Portal 200", "direction": "entrance"},
                   {"entrance": "Hero's Grave to Swamp", "exit": "Shop Portal 201", "direction": "entrance"},
                   {"entrance": "Far Shore to West Garden", "exit": "Shop Portal 202", "direction": "entrance"},
                   {"entrance": "Far Shore to Library", "exit": "Shop Portal 203", "direction": "entrance"},
                   {"entrance": "Far Shore to Quarry", "exit": "Shop Portal 204", "direction": "entrance"},
                   {"entrance": "Far Shore to East Forest", "exit": "Shop Portal 205", "direction": "entrance"},
                   {"entrance": "Far Shore to Fortress", "exit": "Shop Portal 206", "direction": "entrance"},
                   {"entrance": "Far Shore to Atoll", "exit": "Shop Portal 207", "direction": "entrance"},
                   {"entrance": "Far Shore to Ziggurat", "exit": "Shop Portal 208", "direction": "entrance"},
                   {"entrance": "Far Shore to Heir", "exit": "Shop Portal 209", "direction": "entrance"},
                   {"entrance": "Far Shore to Town", "exit": "Shop Portal 210", "direction": "entrance"},
                   {"entrance": "Far Shore to Spawn", "exit": "Shop Portal 211", "direction": "entrance"},
                   {"entrance": "Heir Arena Exit", "exit": "Shop Portal 212", "direction": "entrance"},
                   {"entrance": "Purgatory Bottom Exit", "exit": "Shop Portal 213", "direction": "entrance"},
                   {"entrance": "Purgatory Top Exit", "exit": "Shop Portal 214", "direction": "entrance"},
                   {"entrance": "Shop Portal 215", "exit": "Shop Portal 216", "direction": "entrance"},
                   {"entrance": "Shop Portal 217", "exit": "Shop Portal 218", "direction": "entrance"},
                   {"entrance": "Shop Portal 219", "exit": "Shop Portal 220", "direction": "entrance"},
                   {"entrance": "Shop Portal 221", "exit": "Shop Portal 222", "direction": "entrance"},
                   {"entrance": "Shop Portal 223", "exit": "Shop Portal 224", "direction": "entrance"},
                   {"entrance": "Shop Portal 225", "exit": "Shop Portal 226", "direction": "entrance"},
                   {"entrance": "Shop Portal 227", "exit": "Shop Portal 228", "direction": "entrance"},
                   {"entrance": "Shop Portal 229", "exit": "Shop Portal 230", "direction": "entrance"},
               ]}
