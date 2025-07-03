from worlds.stardew_valley import BackpackProgression, ToolProgression
from worlds.stardew_valley.mods.mod_data import ModNames
from worlds.stardew_valley.options import BackpackSize, Mods, QuestLocations, SkillProgression, Secretsanity, Museumsanity
from worlds.stardew_valley.strings.ap_names.ap_option_names import SecretsanityOptionName
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


class TestSecretFishingRequiresFishingLevelsForDistance(SVTestBase):
    options = {
        SkillProgression: SkillProgression.option_progressive_with_masteries,
        ToolProgression: ToolProgression.option_progressive_no_tool_start,
        Secretsanity: frozenset([SecretsanityOptionName.fishing]),
    }

    def test_pyramid_decal_requires_level_1(self):
        pyramid_decal_location = "Pyramid Decal"
        items_required = ["Progressive Fishing Rod", "Shipping Bin"] * 5
        self.collect_by_name(items_required)
        items_to_test = [self.create_item(item) for item in ["Bus Repair", "Fishing Level"]]
        self.collect(items_to_test)
        self.assert_can_reach_location(pyramid_decal_location)
        for item in items_to_test:
            with self.subTest(f"{pyramid_decal_location} Requires {item.name}"):
                self.remove(item)
                self.assert_cannot_reach_location(pyramid_decal_location)
                self.collect(item)
                self.assert_can_reach_location(pyramid_decal_location)

    def test_foliage_print_requires_level_4(self):
        foliage_print_location = "Foliage Print"
        items_required = ["Progressive Fishing Rod", "Shipping Bin"] * 5
        items_required.extend(["Fishing Level"] * 3)
        self.collect_by_name(items_required)
        items_to_test = [self.create_item(item) for item in ["Boat Repair", "Island North Turtle", "Fishing Level"]]
        self.collect(items_to_test)
        self.assert_can_reach_location(foliage_print_location)
        for item in items_to_test:
            with self.subTest(f"I{foliage_print_location} Requires {item.name}"):
                self.remove(item)
                self.assert_cannot_reach_location(foliage_print_location)
                self.collect(item)
                self.assert_can_reach_location(foliage_print_location)

    def test_iridium_krobus_requires_level_15(self):
        iridium_krobus_location = "Iridium Krobus"
        items_required = ["Progressive Sword", "Progressive Pickaxe", "Progressive Boots", "Combat Level",
                          "Mining Level", "Progressive Watering Can", "Progressive Fishing Rod", "50 Qi Gems", "Shipping Bin"] * 10
        items_required.append("Spring")
        items_required.extend(["Fishing Level"] * 9)
        self.collect_by_name(items_required)
        items_to_test = [self.create_item(item) for item in ["Bus Repair", "Boat Repair", "Island North Turtle", "Qi Walnut Room", "Fishing Level"]]
        self.collect(items_to_test)
        self.assert_can_reach_location(iridium_krobus_location)
        for item in items_to_test:
            with self.subTest(f"{iridium_krobus_location} Requires {item.name}"):
                self.remove(item)
                self.assert_cannot_reach_location(iridium_krobus_location)
                self.collect(item)
                self.assert_can_reach_location(iridium_krobus_location)


class TestArtifactSpotDonationsRequireHoe(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive_no_tool_start,
        Museumsanity: Museumsanity.option_all,
    }

    def test_pyramid_decal_requires_level_1(self):
        artifact_spot_artifacts = ["Chipped Amphora", "Ancient Doll", "Rusty Spoon", "Chicken Statue", "Prehistoric Tool"]
        self.collect_lots_of_money(0.5)
        hoe = self.collect("Progressive Hoe")
        for artifact in artifact_spot_artifacts:
            with self.subTest(f"Artifact: {artifact}"):
                artifact_location = f"Museumsanity: {artifact}"
                self.assert_cannot_reach_location(artifact_location)
                self.collect(hoe)
                self.assert_can_reach_location(artifact_location)
                self.remove(hoe)
