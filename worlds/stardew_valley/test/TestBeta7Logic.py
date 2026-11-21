from worlds.stardew_valley import BackpackProgression, ToolProgression, SeasonRandomization
from worlds.stardew_valley.mods.mod_data import ModNames
from worlds.stardew_valley.options import BackpackSize, Mods, QuestLocations, SkillProgression, Secretsanity, Museumsanity, Booksanity, Hatsanity, Cropsanity, \
    StartWithout
from worlds.stardew_valley.strings.ap_names.ap_option_names import SecretsanityOptionName, StartWithoutOptionName
from worlds.stardew_valley.test.bases import SVTestBase


class TestAvailableBackpacksSize1(SVTestBase):
    options = {
        SeasonRandomization: SeasonRandomization.option_disabled,
        Cropsanity: Cropsanity.option_disabled,
        BackpackProgression: BackpackProgression.option_progressive,
        BackpackSize: 1,
        StartWithout: frozenset({StartWithoutOptionName.backpack}),
        Mods: frozenset({ModNames.big_backpack}),
    }

    def test_can_purchase_correct_number_of_backpacks(self):
        backpack_names = ["Small Pack", "Large Pack", "Deluxe Pack", "Premium Pack"]
        backpack_location_names = []
        for backpack_name in backpack_names:
            for i in range(1, 13):
                backpack_location_names.append(f"{backpack_name} {i}")

        items_required = ["Shipping Bin", "Progressive Hoe", "Progressive Watering Can"]
        for item in items_required:
            self.collect(item)
        self.collect_lots_of_money(0.15)
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
        SeasonRandomization: SeasonRandomization.option_disabled,
        Cropsanity: Cropsanity.option_disabled,
        BackpackProgression: BackpackProgression.option_progressive,
        BackpackSize: 4,
        StartWithout: frozenset({StartWithoutOptionName.backpack}),
        Mods: frozenset({ModNames.big_backpack}),
    }

    def test_can_purchase_correct_number_of_backpacks(self):
        backpack_names = ["Small Pack", "Large Pack", "Deluxe Pack", "Premium Pack"]
        backpack_location_names = []
        for backpack_name in backpack_names:
            for i in range(1, 4):
                backpack_location_names.append(f"{backpack_name} {i}")

        items_required = ["Shipping Bin", "Progressive Hoe", "Progressive Watering Can"]
        for item in items_required:
            self.collect(item)
        self.collect_lots_of_money(0.15)

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
        StartWithout: StartWithout.preset_none,
    }

    def test_beach_bridge_requires_axe(self):
        beach_bridge_location = "Beach Bridge Repair"
        self.assert_can_reach_location(beach_bridge_location)


class TestBeachBridgeWithoutStartingToolsRequiresAxe(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
        StartWithout: frozenset({StartWithoutOptionName.tools}),
    }

    def test_beach_bridge_requires_axe(self):
        beach_bridge_location = "Beach Bridge Repair"
        self.assert_cannot_reach_location(beach_bridge_location)
        self.collect("Progressive Axe")
        self.assert_can_reach_location(beach_bridge_location)


class TestGrimReaperWithStartingToolsRequiresQuarryAndWeapon(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
        StartWithout: StartWithout.preset_none,
    }

    def test_grim_reaper_requires_two_weapons(self):
        grim_reaper_location = "Grim Reaper Statue"
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Landslide Removed")
        self.collect("Bridge Repair")
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Progressive Weapon")
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Progressive Weapon")
        self.assert_can_reach_location(grim_reaper_location)


class TestGrimRepairWithoutStartingToolsRequiresQuarryAndPickaxeAndWeapon(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
        StartWithout: frozenset({StartWithoutOptionName.tools}),
    }

    def test_grim_reaper_requires_weapon_and_pickaxe(self):
        grim_reaper_location = "Grim Reaper Statue"
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Mountain Shortcuts")
        self.collect("Bridge Repair")
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Progressive Weapon")
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Progressive Weapon")
        self.assert_cannot_reach_location(grim_reaper_location)
        self.collect("Progressive Pickaxe")
        self.assert_can_reach_location(grim_reaper_location)


class TestGatheringQuestsWithStartingToolsRequiresMinesAccess(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
        StartWithout: frozenset({StartWithoutOptionName.landslide}),
        QuestLocations: 7,
    }

    def test_gathering_quest_requires_landslide(self):
        gathering_location = "Help Wanted: Gathering 1"
        self.assert_cannot_reach_location(gathering_location)
        self.collect("Landslide Removed")
        self.assert_can_reach_location(gathering_location)


class TestGatheringQuestsWithoutStartingToolsRequiresMinesAndAxeAndPickaxe(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
        StartWithout: frozenset({StartWithoutOptionName.tools, StartWithoutOptionName.landslide}),
        QuestLocations: 7,
    }

    def test_gathering_quest_requires_landslide_axe_and_pickaxe(self):
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


class TestPrizeTicketAndHelpWanted(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
        StartWithout: frozenset({StartWithoutOptionName.tools, StartWithoutOptionName.landslide}),
        QuestLocations: 7,
        Booksanity: Booksanity.option_all,
        Hatsanity: Hatsanity.preset_all,
    }

    def test_prize_tickets_requires_all_help_wanteds_help_wanted(self):
        locations = ["Wear Sports Cap", "Wear Chicken Mask", "Wear Polka Bow"]  # , "Read Friendship 101"] # Friendship 101's bookseller source messes this up
        items_required = ["Shipping Bin", "Progressive Fishing Rod", "Spring", "Progressive Mine Elevator", "Progressive Hoe", "Progressive Watering Can"]
        for item in items_required:
            self.collect(item)
        self.collect_lots_of_money(0.75)
        items_to_test = [self.create_item(item) for item in ["Progressive Fishing Rod", "Landslide Removed", "Progressive Axe",
                                                             "Progressive Pickaxe", "Progressive Weapon"]]
        self.collect(items_to_test)
        for location in locations:
            with self.subTest(f"{location} can be accessed with all help wanted items"):
                self.assert_can_reach_location(location)
            for item in items_to_test:
                self.remove(item)
                with self.subTest(f"{location} Requires {item.name}"):
                    self.assert_cannot_reach_location(location)
                self.collect(item)
                self.assert_can_reach_location(location)


class TestSecretFishingRequiresFishingLevelsForDistance(SVTestBase):
    options = {
        SkillProgression: SkillProgression.option_progressive_with_masteries,
        ToolProgression: ToolProgression.option_progressive,
        StartWithout: frozenset({StartWithoutOptionName.tools}),
        Secretsanity: frozenset([SecretsanityOptionName.fishing]),
    }

    def test_pyramid_decal_requires_level_1(self):
        pyramid_decal_location = "Fishing Secret: Pyramid Decal"
        items_required = ["Progressive Fishing Rod", "Shipping Bin"] * 5
        for item in items_required:
            self.collect(item)
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
        foliage_print_location = "Fishing Secret: Foliage Print"
        items_required = ["Progressive Fishing Rod", "Shipping Bin"] * 5
        items_required.extend(["Fishing Level"] * 3)
        for item in items_required:
            self.collect(item)
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
        iridium_krobus_location = "Fishing Secret: Iridium Krobus"
        items_required = ["Progressive Sword", "Progressive Pickaxe", "Progressive Footwear", "Combat Level", "Progressive House", "Landslide Removed", "Progressive Mine Elevator",
                          "Mining Level", "Progressive Watering Can", "Progressive Hoe", "Progressive Fishing Rod", "50 Qi Gems", "Shipping Bin"] * 10
        self.remove_one_by_name("Spring")
        items_required.extend(["Summer", "Fall", "Winter"])
        items_required.extend(["Fishing Level"] * 9)
        for item in items_required:
            self.collect(item)
        self.collect_lots_of_money(0.6)
        groups_of_items_to_test = {"Quality Seafoam Pudding": [self.create_item(item) for item in
                                                               ["Fish Pond", "Qi Walnut Room", "Boat Repair", "Island West Turtle", "Fishing Level"]],
                                   "Enchanted Rod and Seafoam Pudding": [self.create_item(item) for item in
                                                                         ["Bus Repair", "Fish Pond", "Boat Repair", "Island North Turtle", "Fishing Level",
                                                                          "Skull Key"]],
                                   "Desert Chef and Escargot": [self.create_item(item) for item in
                                                                ["Bus Repair", "Fishing Level", "Garlic Seeds", "Spring"]],
                                   }
        for item_group_to_test in groups_of_items_to_test:
            items_to_test = groups_of_items_to_test[item_group_to_test]
            with self.subTest(f"{iridium_krobus_location} Requires {item_group_to_test}"):
                self.collect(items_to_test)
                self.assert_can_reach_location(iridium_krobus_location)
            for item in items_to_test:
                with self.subTest(f"{iridium_krobus_location} Requires {item_group_to_test} [{item.name}]"):
                    self.remove(item)
                    self.assert_cannot_reach_location(iridium_krobus_location)
                    self.collect(item)
                    self.assert_can_reach_location(iridium_krobus_location)
            self.remove(items_to_test)


class TestArtifactSpotDonationsRequireHoe(SVTestBase):
    options = {
        ToolProgression: ToolProgression.option_progressive,
        StartWithout: frozenset({StartWithoutOptionName.tools}),
        Museumsanity: Museumsanity.option_all,
    }

    def test_artifact_spot_requires_hoe(self):
        artifact_spot_artifacts = ["Chipped Amphora", "Ancient Doll", "Rusty Spoon", "Chicken Statue", "Prehistoric Tool"]
        self.collect_lots_of_money(0.5)
        self.collect("Traveling Merchant Metal Detector", 2)
        hoe = self.create_item("Progressive Hoe")
        for artifact in artifact_spot_artifacts:
            with self.subTest(f"Artifact: {artifact}"):
                artifact_location = f"Museumsanity: {artifact}"
                self.assert_cannot_reach_location(artifact_location)
                self.collect(hoe)
                self.assert_can_reach_location(artifact_location)
                self.remove(hoe)
