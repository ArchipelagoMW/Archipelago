from collections import Counter

from . import SVTestBase
from .. import options, HasProgressionPercent
from ..data.craftable_data import all_crafting_recipes_by_name
from ..locations import locations_by_tag, LocationTags, location_table
from ..options import ToolProgression, BuildingProgression, ExcludeGingerIsland, Chefsanity, Craftsanity, Shipsanity, SeasonRandomization, Friendsanity, \
    FriendsanityHeartSize, BundleRandomization, SkillProgression
from ..strings.entrance_names import Entrance
from ..strings.region_names import Region
from ..strings.tool_names import Tool, ToolMaterial


class TestProgressiveToolsLogic(SVTestBase):
    options = {
        ToolProgression.internal_name: ToolProgression.option_progressive,
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
    }

    def test_sturgeon(self):
        self.multiworld.state.prog_items = {1: Counter()}

        sturgeon_rule = self.world.logic.has("Sturgeon")
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        summer = self.world.create_item("Summer")
        self.multiworld.state.collect(summer, event=False)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        fishing_rod = self.world.create_item("Progressive Fishing Rod")
        self.multiworld.state.collect(fishing_rod, event=False)
        self.multiworld.state.collect(fishing_rod, event=False)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        fishing_level = self.world.create_item("Fishing Level")
        self.multiworld.state.collect(fishing_level, event=False)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        self.multiworld.state.collect(fishing_level, event=False)
        self.multiworld.state.collect(fishing_level, event=False)
        self.multiworld.state.collect(fishing_level, event=False)
        self.multiworld.state.collect(fishing_level, event=False)
        self.multiworld.state.collect(fishing_level, event=False)
        self.assert_rule_true(sturgeon_rule, self.multiworld.state)

        self.remove(summer)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        winter = self.world.create_item("Winter")
        self.multiworld.state.collect(winter, event=False)
        self.assert_rule_true(sturgeon_rule, self.multiworld.state)

        self.remove(fishing_rod)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

    def test_old_master_cannoli(self):
        self.multiworld.state.prog_items = {1: Counter()}

        self.multiworld.state.collect(self.world.create_item("Progressive Axe"), event=False)
        self.multiworld.state.collect(self.world.create_item("Progressive Axe"), event=False)
        self.multiworld.state.collect(self.world.create_item("Summer"), event=False)
        self.collect_lots_of_money()

        rule = self.world.logic.region.can_reach_location("Old Master Cannoli")
        self.assert_rule_false(rule, self.multiworld.state)

        fall = self.world.create_item("Fall")
        self.multiworld.state.collect(fall, event=False)
        self.assert_rule_false(rule, self.multiworld.state)

        tuesday = self.world.create_item("Traveling Merchant: Tuesday")
        self.multiworld.state.collect(tuesday, event=False)
        self.assert_rule_false(rule, self.multiworld.state)

        rare_seed = self.world.create_item("Rare Seed")
        self.multiworld.state.collect(rare_seed, event=False)
        self.assert_rule_true(rule, self.multiworld.state)

        self.remove(fall)
        self.assert_rule_false(rule, self.multiworld.state)
        self.remove(tuesday)

        green_house = self.world.create_item("Greenhouse")
        self.multiworld.state.collect(green_house, event=False)
        self.assert_rule_false(rule, self.multiworld.state)

        friday = self.world.create_item("Traveling Merchant: Friday")
        self.multiworld.state.collect(friday, event=False)
        self.assertTrue(self.multiworld.get_location("Old Master Cannoli", 1).access_rule(self.multiworld.state))

        self.remove(green_house)
        self.assert_rule_false(rule, self.multiworld.state)
        self.remove(friday)


class TestBundlesLogic(SVTestBase):
    options = {
        BundleRandomization.internal_name: BundleRandomization.option_vanilla
    }

    def test_vault_2500g_bundle(self):
        self.assertFalse(self.world.logic.region.can_reach_location("2,500g Bundle")(self.multiworld.state))

        self.collect_lots_of_money()
        self.assertTrue(self.world.logic.region.can_reach_location("2,500g Bundle")(self.multiworld.state))


class TestBuildingLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive
    }

    def test_coop_blueprint(self):
        self.assertFalse(self.world.logic.region.can_reach_location("Coop Blueprint")(self.multiworld.state))

        self.collect_lots_of_money()
        self.assertTrue(self.world.logic.region.can_reach_location("Coop Blueprint")(self.multiworld.state))

    def test_big_coop_blueprint(self):
        big_coop_blueprint_rule = self.world.logic.region.can_reach_location("Big Coop Blueprint")
        self.assertFalse(big_coop_blueprint_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

        self.collect_lots_of_money()
        self.assertFalse(big_coop_blueprint_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.world.create_item("Can Construct Buildings"), event=True)
        self.assertFalse(big_coop_blueprint_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=False)
        self.assertTrue(big_coop_blueprint_rule(self.multiworld.state),
                        f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

    def test_deluxe_coop_blueprint(self):
        self.assertFalse(self.world.logic.region.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.collect_lots_of_money()
        self.multiworld.state.collect(self.world.create_item("Can Construct Buildings"), event=True)
        self.assertFalse(self.world.logic.region.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=True)
        self.assertFalse(self.world.logic.region.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=True)
        self.assertTrue(self.world.logic.region.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

    def test_big_shed_blueprint(self):
        big_shed_rule = self.world.logic.region.can_reach_location("Big Shed Blueprint")
        self.assertFalse(big_shed_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")

        self.collect_lots_of_money()
        self.assertFalse(big_shed_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.world.create_item("Can Construct Buildings"), event=True)
        self.assertFalse(big_shed_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.world.create_item("Progressive Shed"), event=True)
        self.assertTrue(big_shed_rule(self.multiworld.state),
                        f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")


class TestArcadeMachinesLogic(SVTestBase):
    options = {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
    }

    def test_prairie_king(self):
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))

        boots = self.world.create_item("JotPK: Progressive Boots")
        gun = self.world.create_item("JotPK: Progressive Gun")
        ammo = self.world.create_item("JotPK: Progressive Ammo")
        life = self.world.create_item("JotPK: Extra Life")
        drop = self.world.create_item("JotPK: Increased Drop Rate")

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
        self.remove(boots)
        self.remove(gun)

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(boots, event=True)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
        self.remove(boots)
        self.remove(boots)

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(ammo, event=True)
        self.multiworld.state.collect(life, event=True)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
        self.remove(boots)
        self.remove(gun)
        self.remove(ammo)
        self.remove(life)

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(ammo, event=True)
        self.multiworld.state.collect(ammo, event=True)
        self.multiworld.state.collect(life, event=True)
        self.multiworld.state.collect(drop, event=True)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
        self.remove(boots)
        self.remove(gun)
        self.remove(gun)
        self.remove(ammo)
        self.remove(ammo)
        self.remove(life)
        self.remove(drop)

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(ammo, event=True)
        self.multiworld.state.collect(ammo, event=True)
        self.multiworld.state.collect(ammo, event=True)
        self.multiworld.state.collect(life, event=True)
        self.multiworld.state.collect(drop, event=True)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
        self.remove(boots)
        self.remove(boots)
        self.remove(gun)
        self.remove(gun)
        self.remove(gun)
        self.remove(gun)
        self.remove(ammo)
        self.remove(ammo)
        self.remove(ammo)
        self.remove(life)
        self.remove(drop)


class TestWeaponsLogic(SVTestBase):
    options = {
        ToolProgression.internal_name: ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_mine(self):
        self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=True)
        self.collect([self.world.create_item("Combat Level")] * 10)
        self.collect([self.world.create_item("Mining Level")] * 10)
        self.collect([self.world.create_item("Progressive Mine Elevator")] * 24)
        self.multiworld.state.collect(self.world.create_item("Bus Repair"), event=True)
        self.multiworld.state.collect(self.world.create_item("Skull Key"), event=True)

        self.GiveItemAndCheckReachableMine("Progressive Sword", 1)
        self.GiveItemAndCheckReachableMine("Progressive Dagger", 1)
        self.GiveItemAndCheckReachableMine("Progressive Club", 1)

        self.GiveItemAndCheckReachableMine("Progressive Sword", 2)
        self.GiveItemAndCheckReachableMine("Progressive Dagger", 2)
        self.GiveItemAndCheckReachableMine("Progressive Club", 2)

        self.GiveItemAndCheckReachableMine("Progressive Sword", 3)
        self.GiveItemAndCheckReachableMine("Progressive Dagger", 3)
        self.GiveItemAndCheckReachableMine("Progressive Club", 3)

        self.GiveItemAndCheckReachableMine("Progressive Sword", 4)
        self.GiveItemAndCheckReachableMine("Progressive Dagger", 4)
        self.GiveItemAndCheckReachableMine("Progressive Club", 4)

        self.GiveItemAndCheckReachableMine("Progressive Sword", 5)
        self.GiveItemAndCheckReachableMine("Progressive Dagger", 5)
        self.GiveItemAndCheckReachableMine("Progressive Club", 5)

    def GiveItemAndCheckReachableMine(self, item_name: str, reachable_level: int):
        item = self.multiworld.create_item(item_name, self.player)
        self.multiworld.state.collect(item, event=True)
        rule = self.world.logic.mine.can_mine_in_the_mines_floor_1_40()
        if reachable_level > 0:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)

        rule = self.world.logic.mine.can_mine_in_the_mines_floor_41_80()
        if reachable_level > 1:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)

        rule = self.world.logic.mine.can_mine_in_the_mines_floor_81_120()
        if reachable_level > 2:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)

        rule = self.world.logic.mine.can_mine_in_the_skull_cavern()
        if reachable_level > 3:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)

        rule = self.world.logic.ability.can_mine_perfectly_in_the_skull_cavern()
        if reachable_level > 4:
            self.assert_rule_true(rule, self.multiworld.state)
        else:
            self.assert_rule_false(rule, self.multiworld.state)


class TestRecipeLearnLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        Chefsanity.internal_name: Chefsanity.option_none,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_learn_qos_recipe(self):
        location = "Cook Radish Salad"
        rule = self.world.logic.region.can_reach_location(location)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Progressive House"), event=False)
        self.multiworld.state.collect(self.world.create_item("Radish Seeds"), event=False)
        self.multiworld.state.collect(self.world.create_item("Spring"), event=False)
        self.multiworld.state.collect(self.world.create_item("Summer"), event=False)
        self.collect_lots_of_money()
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("The Queen of Sauce"), event=False)
        self.assert_rule_true(rule, self.multiworld.state)


class TestRecipeReceiveLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        Chefsanity.internal_name: Chefsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_learn_qos_recipe(self):
        location = "Cook Radish Salad"
        rule = self.world.logic.region.can_reach_location(location)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Progressive House"), event=False)
        self.multiworld.state.collect(self.world.create_item("Radish Seeds"), event=False)
        self.multiworld.state.collect(self.world.create_item("Summer"), event=False)
        self.collect_lots_of_money()
        self.assert_rule_false(rule, self.multiworld.state)

        spring = self.world.create_item("Spring")
        qos = self.world.create_item("The Queen of Sauce")
        self.multiworld.state.collect(spring, event=False)
        self.multiworld.state.collect(qos, event=False)
        self.assert_rule_false(rule, self.multiworld.state)
        self.multiworld.state.remove(spring)
        self.multiworld.state.remove(qos)

        self.multiworld.state.collect(self.world.create_item("Radish Salad Recipe"), event=False)
        self.assert_rule_true(rule, self.multiworld.state)

    def test_get_chefsanity_check_recipe(self):
        location = "Radish Salad Recipe"
        rule = self.world.logic.region.can_reach_location(location)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Spring"), event=False)
        self.collect_lots_of_money()
        self.assert_rule_false(rule, self.multiworld.state)

        seeds = self.world.create_item("Radish Seeds")
        summer = self.world.create_item("Summer")
        house = self.world.create_item("Progressive House")
        self.multiworld.state.collect(seeds, event=False)
        self.multiworld.state.collect(summer, event=False)
        self.multiworld.state.collect(house, event=False)
        self.assert_rule_false(rule, self.multiworld.state)
        self.multiworld.state.remove(seeds)
        self.multiworld.state.remove(summer)
        self.multiworld.state.remove(house)

        self.multiworld.state.collect(self.world.create_item("The Queen of Sauce"), event=False)
        self.assert_rule_true(rule, self.multiworld.state)


class TestCraftsanityLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        Craftsanity.internal_name: Craftsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_craft_recipe(self):
        location = "Craft Marble Brazier"
        rule = self.world.logic.region.can_reach_location(location)
        self.collect([self.world.create_item("Progressive Pickaxe")] * 4)
        self.collect([self.world.create_item("Progressive Fishing Rod")] * 4)
        self.collect([self.world.create_item("Progressive Sword")] * 4)
        self.collect([self.world.create_item("Progressive Mine Elevator")] * 24)
        self.collect([self.world.create_item("Mining Level")] * 10)
        self.collect([self.world.create_item("Combat Level")] * 10)
        self.collect([self.world.create_item("Fishing Level")] * 10)
        self.collect_all_the_money()
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Marble Brazier Recipe"), event=False)
        self.assert_rule_true(rule, self.multiworld.state)

    def test_can_learn_crafting_recipe(self):
        location = "Marble Brazier Recipe"
        rule = self.world.logic.region.can_reach_location(location)
        self.assert_rule_false(rule, self.multiworld.state)

        self.collect_lots_of_money()
        self.assert_rule_true(rule, self.multiworld.state)

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.world.create_item("Pumpkin Seeds"), event=False)
        self.multiworld.state.collect(self.world.create_item("Torch Recipe"), event=False)
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Fall"), event=False)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Jack-O-Lantern Recipe"), event=False)
        self.assert_rule_true(rule, self.multiworld.state)


class TestCraftsanityWithFestivalsLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_easy,
        Craftsanity.internal_name: Craftsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.world.create_item("Pumpkin Seeds"), event=False)
        self.multiworld.state.collect(self.world.create_item("Fall"), event=False)
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Jack-O-Lantern Recipe"), event=False)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Torch Recipe"), event=False)
        self.assert_rule_true(rule, self.multiworld.state)


class TestNoCraftsanityLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        SeasonRandomization.internal_name: SeasonRandomization.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_disabled,
        Craftsanity.internal_name: Craftsanity.option_none,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_craft_recipe(self):
        recipe = all_crafting_recipes_by_name["Wood Floor"]
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_true(rule, self.multiworld.state)

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.world.create_item("Pumpkin Seeds"), event=False)
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        result = rule(self.multiworld.state)
        self.assertFalse(result)

        self.collect([self.world.create_item("Progressive Season")] * 2)
        self.assert_rule_true(rule, self.multiworld.state)


class TestNoCraftsanityWithFestivalsLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_easy,
        Craftsanity.internal_name: Craftsanity.option_none,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.world.create_item("Pumpkin Seeds"), event=False)
        self.multiworld.state.collect(self.world.create_item("Fall"), event=False)
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Jack-O-Lantern Recipe"), event=False)
        self.assert_rule_true(rule, self.multiworld.state)


class TestDonationLogicAll(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_all
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        railroad_item = "Railroad Boulder Removed"
        swap_museum_and_bathhouse(self.multiworld, self.player)
        collect_all_except(self.multiworld, railroad_item)

        for donation in locations_by_tag[LocationTags.MUSEUM_DONATIONS]:
            self.assertFalse(self.world.logic.region.can_reach_location(donation.name)(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item(railroad_item), event=False)

        for donation in locations_by_tag[LocationTags.MUSEUM_DONATIONS]:
            self.assertTrue(self.world.logic.region.can_reach_location(donation.name)(self.multiworld.state))


class TestDonationLogicRandomized(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_randomized
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        railroad_item = "Railroad Boulder Removed"
        swap_museum_and_bathhouse(self.multiworld, self.player)
        collect_all_except(self.multiworld, railroad_item)
        donation_locations = [location for location in self.multiworld.get_locations() if
                              not location.event and LocationTags.MUSEUM_DONATIONS in location_table[location.name].tags]

        for donation in donation_locations:
            self.assertFalse(self.world.logic.region.can_reach_location(donation.name)(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item(railroad_item), event=False)

        for donation in donation_locations:
            self.assertTrue(self.world.logic.region.can_reach_location(donation.name)(self.multiworld.state))


class TestDonationLogicMilestones(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_milestones
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        railroad_item = "Railroad Boulder Removed"
        swap_museum_and_bathhouse(self.multiworld, self.player)
        collect_all_except(self.multiworld, railroad_item)

        for donation in locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            self.assertFalse(self.world.logic.region.can_reach_location(donation.name)(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item(railroad_item), event=False)

        for donation in locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            self.assertTrue(self.world.logic.region.can_reach_location(donation.name)(self.multiworld.state))


def swap_museum_and_bathhouse(multiworld, player):
    museum_region = multiworld.get_region(Region.museum, player)
    bathhouse_region = multiworld.get_region(Region.bathhouse_entrance, player)
    museum_entrance = multiworld.get_entrance(Entrance.town_to_museum, player)
    bathhouse_entrance = multiworld.get_entrance(Entrance.enter_bathhouse_entrance, player)
    museum_entrance.connect(bathhouse_region)
    bathhouse_entrance.connect(museum_region)


class TestToolVanillaRequiresBlacksmith(SVTestBase):
    options = {
        options.EntranceRandomization: options.EntranceRandomization.option_buildings,
        options.ToolProgression: options.ToolProgression.option_vanilla,
    }
    seed = 4111845104987680262

    # Seed is hardcoded to make sure the ER is a valid roll that actually lock the blacksmith behind the Railroad Boulder Removed.

    def test_cannot_get_any_tool_without_blacksmith_access(self):
        railroad_item = "Railroad Boulder Removed"
        place_region_at_entrance(self.multiworld, self.player, Region.blacksmith, Entrance.enter_bathhouse_entrance)
        collect_all_except(self.multiworld, railroad_item)

        for tool in [Tool.pickaxe, Tool.axe, Tool.hoe, Tool.trash_can, Tool.watering_can]:
            for material in [ToolMaterial.copper, ToolMaterial.iron, ToolMaterial.gold, ToolMaterial.iridium]:
                self.assert_rule_false(self.world.logic.tool.has_tool(tool, material), self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item(railroad_item), event=False)

        for tool in [Tool.pickaxe, Tool.axe, Tool.hoe, Tool.trash_can, Tool.watering_can]:
            for material in [ToolMaterial.copper, ToolMaterial.iron, ToolMaterial.gold, ToolMaterial.iridium]:
                self.assert_rule_true(self.world.logic.tool.has_tool(tool, material), self.multiworld.state)

    def test_cannot_get_fishing_rod_without_willy_access(self):
        railroad_item = "Railroad Boulder Removed"
        place_region_at_entrance(self.multiworld, self.player, Region.fish_shop, Entrance.enter_bathhouse_entrance)
        collect_all_except(self.multiworld, railroad_item)

        for fishing_rod_level in [3, 4]:
            self.assert_rule_false(self.world.logic.tool.has_fishing_rod(fishing_rod_level), self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item(railroad_item), event=False)

        for fishing_rod_level in [3, 4]:
            self.assert_rule_true(self.world.logic.tool.has_fishing_rod(fishing_rod_level), self.multiworld.state)


def place_region_at_entrance(multiworld, player, region, entrance):
    region_to_place = multiworld.get_region(region, player)
    entrance_to_place_region = multiworld.get_entrance(entrance, player)

    entrance_to_switch = region_to_place.entrances[0]
    region_to_switch = entrance_to_place_region.connected_region
    entrance_to_switch.connect(region_to_switch)
    entrance_to_place_region.connect(region_to_place)


def collect_all_except(multiworld, item_to_not_collect: str):
    for item in multiworld.get_items():
        if item.name != item_to_not_collect:
            multiworld.state.collect(item)


class TestFriendsanityDatingRules(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized_not_winter,
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize.internal_name: 3
    }

    def test_earning_dating_heart_requires_dating(self):
        self.collect_all_the_money()
        self.multiworld.state.collect(self.world.create_item("Fall"), event=False)
        self.multiworld.state.collect(self.world.create_item("Beach Bridge"), event=False)
        self.multiworld.state.collect(self.world.create_item("Progressive House"), event=False)
        for i in range(3):
            self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=False)
            self.multiworld.state.collect(self.world.create_item("Progressive Weapon"), event=False)
            self.multiworld.state.collect(self.world.create_item("Progressive Axe"), event=False)
            self.multiworld.state.collect(self.world.create_item("Progressive Barn"), event=False)
        for i in range(10):
            self.multiworld.state.collect(self.world.create_item("Foraging Level"), event=False)
            self.multiworld.state.collect(self.world.create_item("Farming Level"), event=False)
            self.multiworld.state.collect(self.world.create_item("Mining Level"), event=False)
            self.multiworld.state.collect(self.world.create_item("Combat Level"), event=False)
            self.multiworld.state.collect(self.world.create_item("Progressive Mine Elevator"), event=False)
            self.multiworld.state.collect(self.world.create_item("Progressive Mine Elevator"), event=False)

        npc = "Abigail"
        heart_name = f"{npc} <3"
        step = 3

        self.assert_can_reach_heart_up_to(npc, 3, step)
        self.multiworld.state.collect(self.world.create_item(heart_name), event=False)
        self.assert_can_reach_heart_up_to(npc, 6, step)
        self.multiworld.state.collect(self.world.create_item(heart_name), event=False)
        self.assert_can_reach_heart_up_to(npc, 8, step)
        self.multiworld.state.collect(self.world.create_item(heart_name), event=False)
        self.assert_can_reach_heart_up_to(npc, 10, step)
        self.multiworld.state.collect(self.world.create_item(heart_name), event=False)
        self.assert_can_reach_heart_up_to(npc, 14, step)

    def assert_can_reach_heart_up_to(self, npc: str, max_reachable: int, step: int):
        prefix = "Friendsanity: "
        suffix = " <3"
        for i in range(1, max_reachable + 1):
            if i % step != 0 and i != 14:
                continue
            location = f"{prefix}{npc} {i}{suffix}"
            can_reach = self.world.logic.region.can_reach_location(location)(self.multiworld.state)
            self.assertTrue(can_reach, f"Should be able to earn relationship up to {i} hearts")
        for i in range(max_reachable + 1, 14 + 1):
            if i % step != 0 and i != 14:
                continue
            location = f"{prefix}{npc} {i}{suffix}"
            can_reach = self.world.logic.region.can_reach_location(location)(self.multiworld.state)
            self.assertFalse(can_reach, f"Should not be able to earn relationship up to {i} hearts")


class TestShipsanityNone(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_none
    }

    def test_no_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event:
                self.assertFalse("Shipsanity" in location.name)
                self.assertNotIn(LocationTags.SHIPSANITY, location_table[location.name].tags)


class TestShipsanityCrops(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_crops
    }

    def test_only_crop_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                self.assertIn(LocationTags.SHIPSANITY_CROP, location_table[location.name].tags)


class TestShipsanityFish(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_fish
    }

    def test_only_fish_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                self.assertIn(LocationTags.SHIPSANITY_FISH, location_table[location.name].tags)


class TestShipsanityFullShipment(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_full_shipment
    }

    def test_only_full_shipment_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                self.assertIn(LocationTags.SHIPSANITY_FULL_SHIPMENT, location_table[location.name].tags)
                self.assertNotIn(LocationTags.SHIPSANITY_FISH, location_table[location.name].tags)


class TestShipsanityFullShipmentWithFish(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_full_shipment_with_fish
    }

    def test_only_full_shipment_and_fish_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                self.assertTrue(LocationTags.SHIPSANITY_FULL_SHIPMENT in location_table[location.name].tags or
                                LocationTags.SHIPSANITY_FISH in location_table[location.name].tags)


class TestShipsanityEverything(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_everything,
        BuildingProgression.internal_name: BuildingProgression.option_progressive
    }

    def test_all_shipsanity_locations_require_shipping_bin(self):
        bin_name = "Shipping Bin"
        collect_all_except(self.multiworld, bin_name)
        shipsanity_locations = [location for location in self.multiworld.get_locations() if
                                not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags]
        bin_item = self.world.create_item(bin_name)
        for location in shipsanity_locations:
            with self.subTest(location.name):
                self.remove(bin_item)
                self.assertFalse(self.world.logic.region.can_reach_location(location.name)(self.multiworld.state))
                self.multiworld.state.collect(bin_item, event=False)
                shipsanity_rule = self.world.logic.region.can_reach_location(location.name)
                self.assert_rule_true(shipsanity_rule, self.multiworld.state)
                self.remove(bin_item)


class TestVanillaSkillLogicSimplification(SVTestBase):
    options = {
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_progressive,
    }

    def test_skill_logic_has_level_only_uses_one_has_progression_percent(self):
        rule = self.multiworld.worlds[1].logic.skill.has_level("Farming", 8)
        self.assertEqual(1, sum(1 for i in rule.current_rules if type(i) == HasProgressionPercent))
