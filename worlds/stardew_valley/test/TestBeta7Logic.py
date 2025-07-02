from worlds.stardew_valley import BackpackProgression, ToolProgression
from worlds.stardew_valley.mods.mod_data import ModNames
from worlds.stardew_valley.options import BackpackSize, Mods, QuestLocations
from worlds.stardew_valley.test.bases import SVTestBase


class TestAvailableBackpacks(SVTestBase):
    options = {
        BackpackProgression: BackpackProgression.option_progressive,
        BackpackSize: 1,
        ToolProgression: ToolProgression.option_progressive_no_tool_start,
        Mods: frozenset({ModNames.big_backpack}),
    }

    def test_can_purchase_correct_number_of_backpacks(self):
        backpack_names = ["Small Pack", "Large Pack", "Premium Pack", "Deluxe Pack"]
        backpack_location_names = []
        for backpack_name in backpack_names:
            for i in range(1, 13):
                backpack_location_names.append(f"{backpack_name} {i}")

        number_owned_backpacks = self.multiworld.state.prog_items[self.player]["Progressive Backpack"]
        while number_owned_backpacks < 48:
            number_available = number_owned_backpacks + 1
            with self.subTest(f"Can Purchase {number_available} backpacks when you own {number_owned_backpacks} backpacks"):
                for i in range(0, len(backpack_location_names)):
                    if i < number_available:
                        self.assert_can_reach_location(backpack_location_names[i])
                    else:
                        self.assert_cannot_reach_location(backpack_location_names[i])
            self.collect("Progressive Backpack")
            number_owned_backpacks = self.multiworld.state.prog_items[self.player]["Progressive Backpack"]


class TestAvailableBackpacksSize4(SVTestBase):
    options = {
        BackpackProgression: BackpackProgression.option_progressive,
        BackpackSize: 4,
        ToolProgression: ToolProgression.option_progressive_no_tool_start,
        Mods: frozenset({ModNames.big_backpack}),
    }

    def test_can_purchase_correct_number_of_backpacks(self):
        backpack_names = ["Small Pack", "Large Pack", "Premium Pack", "Deluxe Pack"]
        backpack_location_names = []
        for backpack_name in backpack_names:
            for i in range(1, 4):
                backpack_location_names.append(f"{backpack_name} {i}")

        number_owned_backpacks = self.multiworld.state.prog_items[self.player]["Progressive Backpack"]
        while number_owned_backpacks * 4 < 48:
            number_available = number_owned_backpacks + 1
            with self.subTest(f"Can Purchase {number_available} backpacks when you own {number_owned_backpacks} backpacks"):
                for i in range(0, len(backpack_location_names)):
                    if i < number_available:
                        self.assert_can_reach_location(backpack_location_names[i])
                    else:
                        self.assert_cannot_reach_location(backpack_location_names[i])
            self.collect("Progressive Backpack")
            number_owned_backpacks = self.multiworld.state.prog_items[self.player]["Progressive Backpack"]


class TestBeachBridgeWithStartingToolsRequiresNothing(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
    }

    def test_beach_bridge_requires_axe(self):
        beach_bridge_location = "Beach Bridge Repair"
        self.assert_can_reach_location(beach_bridge_location)


class TestBeachBridgeWithoutStartingToolsRequiresAxe(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive_no_tool_start,
    }

    def test_beach_bridge_requires_axe(self):
        beach_bridge_location = "Beach Bridge Repair"
        self.assert_cannot_reach_location(beach_bridge_location)
        self.collect("Progressive Axe")
        self.assert_can_reach_location(beach_bridge_location)


class TestGrimReaperWithStartingToolsRequiresQuarryAndWeapon(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
    }

    def test_beach_bridge_requires_axe(self):
        grim_reaper_location = "Grim Reaper statue"
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Bridge Repair")
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Progressive Weapon")
        self.assert_can_reach_location(grim_reaper_location)


class TestGrimRepairWithoutStartingToolsRequiresQuarryAndPickaxeAndWeapon(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive_no_tool_start,
    }

    def test_beach_bridge_requires_axe(self):
        grim_reaper_location = "Grim Reaper statue"
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Bridge Repair")
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Progressive Weapon")
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Progressive Pickaxe")
        self.assert_can_reach_location(grim_reaper_location)


class TestGatheringQuestsWithStartingToolsRequiresMinesAccess(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
        QuestLocations: 7,
    }

    def test_beach_bridge_requires_axe(self):
        gathering_location = "Help Wanted: Gathering 1"
        self.assert_cannot_reach_location(gathering_location)
        self.collect("Landslide Removed")
        self.assert_can_reach_location(gathering_location)


class TestGatheringQuestsWithoutStartingToolsRequiresMinesAndAxeAndPickaxe(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive_no_tool_start,
        QuestLocations: 7,
    }

    def test_beach_bridge_requires_axe(self):
        gathering_location = "Help Wanted: Gathering 1"
        axe = self.create_item("Progressive Axe")
        self.assert_cannot_reach_location(gathering_location)
        self.collect("Landslide Removed")
        self.assert_cannot_reach_location(gathering_location)
        self.collect(axe)
        self.assert_cannot_reach_location(gathering_location)
        self.collect("Progressive Pickaxe")
        self.assert_can_reach_location(gathering_location)
        self.remove(axe)
        self.assert_cannot_reach_location(gathering_location)