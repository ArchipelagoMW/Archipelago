from collections import Counter

from . import SVTestBase
from .. import options
from ..locations import locations_by_tag, LocationTags, location_table
from ..strings.animal_names import Animal
from ..strings.animal_product_names import AnimalProduct
from ..strings.artisan_good_names import ArtisanGood
from ..strings.crop_names import Vegetable
from ..strings.entrance_names import Entrance
from ..strings.food_names import Meal
from ..strings.ingredient_names import Ingredient
from ..strings.machine_names import Machine
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.seed_names import Seed


class TestProgressiveToolsLogic(SVTestBase):
    options = {
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
    }

    def setUp(self):
        super().setUp()
        self.multiworld.state.prog_items = {1: Counter()}

    def test_sturgeon(self):
        self.assertFalse(self.world.logic.has("Sturgeon")(self.multiworld.state))

        summer = self.world.create_item("Summer")
        self.multiworld.state.collect(summer, event=True)
        self.assertFalse(self.world.logic.has("Sturgeon")(self.multiworld.state))

        fishing_rod = self.world.create_item("Progressive Fishing Rod")
        self.multiworld.state.collect(fishing_rod, event=True)
        self.multiworld.state.collect(fishing_rod, event=True)
        self.assertFalse(self.world.logic.has("Sturgeon")(self.multiworld.state))

        fishing_level = self.world.create_item("Fishing Level")
        self.multiworld.state.collect(fishing_level, event=True)
        self.assertFalse(self.world.logic.has("Sturgeon")(self.multiworld.state))

        self.multiworld.state.collect(fishing_level, event=True)
        self.multiworld.state.collect(fishing_level, event=True)
        self.multiworld.state.collect(fishing_level, event=True)
        self.multiworld.state.collect(fishing_level, event=True)
        self.multiworld.state.collect(fishing_level, event=True)
        self.assertTrue(self.world.logic.has("Sturgeon")(self.multiworld.state))

        self.remove(summer)
        self.assertFalse(self.world.logic.has("Sturgeon")(self.multiworld.state))

        winter = self.world.create_item("Winter")
        self.multiworld.state.collect(winter, event=True)
        self.assertTrue(self.world.logic.has("Sturgeon")(self.multiworld.state))

        self.remove(fishing_rod)
        self.assertFalse(self.world.logic.has("Sturgeon")(self.multiworld.state))

    def test_old_master_cannoli(self):
        self.multiworld.state.collect(self.world.create_item("Progressive Axe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Progressive Axe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Summer"), event=True)

        self.assertFalse(self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state))

        fall = self.world.create_item("Fall")
        self.multiworld.state.collect(fall, event=True)
        self.assertFalse(self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state))

        tuesday = self.world.create_item("Traveling Merchant: Tuesday")
        self.multiworld.state.collect(tuesday, event=True)
        self.assertFalse(self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state))

        rare_seed = self.world.create_item("Rare Seed")
        self.multiworld.state.collect(rare_seed, event=True)
        self.assertTrue(self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state))

        self.remove(fall)
        self.assertFalse(self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state))
        self.remove(tuesday)

        green_house = self.world.create_item("Greenhouse")
        self.multiworld.state.collect(green_house, event=True)
        self.assertFalse(self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state))

        friday = self.world.create_item("Traveling Merchant: Friday")
        self.multiworld.state.collect(friday, event=True)
        self.assertTrue(self.multiworld.get_location("Old Master Cannoli", 1).access_rule(self.multiworld.state))

        self.remove(green_house)
        self.assertFalse(self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state))
        self.remove(friday)


class TestBundlesLogic(SVTestBase):
    options = {
    }

    def test_vault_2500g_bundle(self):
        self.assertTrue(self.world.logic.can_reach_location("2,500g Bundle")(self.multiworld.state))


class TestBuildingLogic(SVTestBase):
    options = {
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive_early_shipping_bin
    }

    def test_coop_blueprint(self):
        self.assertFalse(self.world.logic.can_reach_location("Coop Blueprint")(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.assertTrue(self.world.logic.can_reach_location("Coop Blueprint")(self.multiworld.state))

    def test_big_coop_blueprint(self):
        self.assertFalse(self.world.logic.can_reach_location("Big Coop Blueprint")(self.multiworld.state),
            f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.assertFalse(self.world.logic.can_reach_location("Big Coop Blueprint")(self.multiworld.state),
            f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=True)
        self.assertTrue(self.world.logic.can_reach_location("Big Coop Blueprint")(self.multiworld.state),
            f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

    def test_deluxe_coop_blueprint(self):
        self.assertFalse(self.world.logic.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.assertFalse(self.world.logic.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=True)
        self.assertFalse(self.world.logic.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=True)
        self.assertTrue(self.world.logic.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

    def test_big_shed_blueprint(self):
        self.assertFalse(self.world.logic.can_reach_location("Big Shed Blueprint")(self.multiworld.state),
            f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.assertFalse(self.world.logic.can_reach_location("Big Shed Blueprint")(self.multiworld.state),
            f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.world.create_item("Progressive Shed"), event=True)
        self.assertTrue(self.world.logic.can_reach_location("Big Shed Blueprint")(self.multiworld.state),
            f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")


class TestArcadeMachinesLogic(SVTestBase):
    options = {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
    }

    def test_prairie_king(self):
        self.assertFalse(self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))

        boots = self.world.create_item("JotPK: Progressive Boots")
        gun = self.world.create_item("JotPK: Progressive Gun")
        ammo = self.world.create_item("JotPK: Progressive Ammo")
        life = self.world.create_item("JotPK: Extra Life")
        drop = self.world.create_item("JotPK: Increased Drop Rate")

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
        self.remove(boots)
        self.remove(gun)

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(boots, event=True)
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
        self.remove(boots)
        self.remove(boots)

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(ammo, event=True)
        self.multiworld.state.collect(life, event=True)
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
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
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state))
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state))
        self.assertFalse(self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
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
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state))
        self.assertTrue(self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state))
        self.assertTrue(self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state))
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
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_mine(self):
        self.collect(self.world.create_item("Adventurer's Guild"))
        self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=True)
        self.collect([self.world.create_item("Combat Level")] * 10)
        self.collect([self.world.create_item("Progressive Mine Elevator")] * 24)
        self.multiworld.state.collect(self.world.create_item("Bus Repair"), event=True)
        self.multiworld.state.collect(self.world.create_item("Skull Key"), event=True)

        self.GiveItemAndCheckReachableMine("Rusty Sword", 1)
        self.GiveItemAndCheckReachableMine("Wooden Blade", 1)
        self.GiveItemAndCheckReachableMine("Elf Blade", 1)

        self.GiveItemAndCheckReachableMine("Silver Saber", 2)
        self.GiveItemAndCheckReachableMine("Crystal Dagger", 2)

        self.GiveItemAndCheckReachableMine("Claymore", 3)
        self.GiveItemAndCheckReachableMine("Obsidian Edge", 3)
        self.GiveItemAndCheckReachableMine("Bone Sword", 3)

        self.GiveItemAndCheckReachableMine("The Slammer", 4)
        self.GiveItemAndCheckReachableMine("Lava Katana", 4)

        self.GiveItemAndCheckReachableMine("Galaxy Sword", 5)
        self.GiveItemAndCheckReachableMine("Galaxy Hammer", 5)
        self.GiveItemAndCheckReachableMine("Galaxy Dagger", 5)

    def GiveItemAndCheckReachableMine(self, item_name: str, reachable_level: int):
        item = self.multiworld.create_item(item_name, self.player)
        self.multiworld.state.collect(item, event=True)
        if reachable_level > 0:
            self.assertTrue(self.world.logic.can_mine_in_the_mines_floor_1_40()(self.multiworld.state))
        else:
            self.assertFalse(self.world.logic.can_mine_in_the_mines_floor_1_40()(self.multiworld.state))

        if reachable_level > 1:
            self.assertTrue(self.world.logic.can_mine_in_the_mines_floor_41_80()(self.multiworld.state))
        else:
            self.assertFalse(self.world.logic.can_mine_in_the_mines_floor_41_80()(self.multiworld.state))

        if reachable_level > 2:
            self.assertTrue(self.world.logic.can_mine_in_the_mines_floor_81_120()(self.multiworld.state))
        else:
            self.assertFalse(self.world.logic.can_mine_in_the_mines_floor_81_120()(self.multiworld.state))

        if reachable_level > 3:
            self.assertTrue(self.world.logic.can_mine_in_the_skull_cavern()(self.multiworld.state))
        else:
            self.assertFalse(self.world.logic.can_mine_in_the_skull_cavern()(self.multiworld.state))

        if reachable_level > 4:
            self.assertTrue(self.world.logic.can_mine_perfectly_in_the_skull_cavern()(self.multiworld.state))
        else:
            self.assertFalse(self.world.logic.can_mine_perfectly_in_the_skull_cavern()(self.multiworld.state))

        self.remove(item)


class TestRecipeLogic(SVTestBase):
    options = {
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_shuffled,
    }

    # I wanted to make a test for different ways to obtain a pizza, but I'm stuck not knowing how to block the immediate purchase from Gus
    # def test_pizza(self):
    #     world = self.world
    #     logic = world.logic
    #     multiworld = self.multiworld
    #
    #     self.assertTrue(logic.has(Ingredient.wheat_flour)(multiworld.state))
    #     self.assertTrue(logic.can_spend_money_at(Region.saloon, 150)(multiworld.state))
    #     self.assertFalse(logic.has(Meal.pizza)(multiworld.state))
    #
    #     self.assertFalse(logic.can_cook()(multiworld.state))
    #     self.collect(world.create_item("Progressive House"))
    #     self.assertTrue(logic.can_cook()(multiworld.state))
    #     self.assertFalse(logic.has(Meal.pizza)(multiworld.state))
    #
    #     self.assertFalse(logic.has(Seed.tomato)(multiworld.state))
    #     self.collect(world.create_item(Seed.tomato))
    #     self.assertTrue(logic.has(Seed.tomato)(multiworld.state))
    #     self.assertFalse(logic.has(Meal.pizza)(multiworld.state))
    #
    #     self.assertFalse(logic.has(Vegetable.tomato)(multiworld.state))
    #     self.collect(world.create_item(Season.summer))
    #     self.assertTrue(logic.has(Vegetable.tomato)(multiworld.state))
    #     self.assertFalse(logic.has(Meal.pizza)(multiworld.state))
    #
    #     self.assertFalse(logic.has(Animal.cow)(multiworld.state))
    #     self.assertFalse(logic.has(AnimalProduct.cow_milk)(multiworld.state))
    #     self.collect(world.create_item("Progressive Barn"))
    #     self.assertTrue(logic.has(Animal.cow)(multiworld.state))
    #     self.assertTrue(logic.has(AnimalProduct.cow_milk)(multiworld.state))
    #     self.assertFalse(logic.has(Meal.pizza)(multiworld.state))
    #
    #     self.assertFalse(logic.has(Machine.cheese_press)(self.multiworld.state))
    #     self.assertFalse(logic.has(ArtisanGood.cheese)(self.multiworld.state))
    #     self.collect(world.create_item(item) for item in ["Farming Level"] * 6)
    #     self.collect(world.create_item(item) for item in ["Progressive Axe"] * 2)
    #     self.assertTrue(logic.has(Machine.cheese_press)(self.multiworld.state))
    #     self.assertTrue(logic.has(ArtisanGood.cheese)(self.multiworld.state))
    #     self.assertTrue(logic.has(Meal.pizza)(self.multiworld.state))


class TestDonationLogicAll(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_all
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        guild_item = "Adventurer's Guild"
        swap_museum_and_guild(self.multiworld, self.player)
        collect_all_except(self.multiworld, guild_item)

        for donation in locations_by_tag[LocationTags.MUSEUM_DONATIONS]:
            self.assertFalse(self.world.logic.can_reach_location(donation.name)(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item(guild_item), event=True)

        for donation in locations_by_tag[LocationTags.MUSEUM_DONATIONS]:
            self.assertTrue(self.world.logic.can_reach_location(donation.name)(self.multiworld.state))


class TestDonationLogicRandomized(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_randomized
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        guild_item = "Adventurer's Guild"
        swap_museum_and_guild(self.multiworld, self.player)
        collect_all_except(self.multiworld, guild_item)
        donation_locations = [location for location in self.multiworld.get_locations() if not location.event and LocationTags.MUSEUM_DONATIONS in location_table[location.name].tags]

        for donation in donation_locations:
            self.assertFalse(self.world.logic.can_reach_location(donation.name)(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item(guild_item), event=True)

        for donation in donation_locations:
            self.assertTrue(self.world.logic.can_reach_location(donation.name)(self.multiworld.state))


class TestDonationLogicMilestones(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_milestones
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        guild_item = "Adventurer's Guild"
        swap_museum_and_guild(self.multiworld, self.player)
        collect_all_except(self.multiworld, guild_item)

        for donation in locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            self.assertFalse(self.world.logic.can_reach_location(donation.name)(self.multiworld.state))

        self.multiworld.state.collect(self.world.create_item(guild_item), event=True)

        for donation in locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            self.assertTrue(self.world.logic.can_reach_location(donation.name)(self.multiworld.state))


def swap_museum_and_guild(multiworld, player):
    museum_region = multiworld.get_region(Region.museum, player)
    guild_region = multiworld.get_region(Region.adventurer_guild, player)
    museum_entrance = multiworld.get_entrance(Entrance.town_to_museum, player)
    guild_entrance = multiworld.get_entrance(Entrance.mountain_to_adventurer_guild, player)
    museum_entrance.connect(guild_region)
    guild_entrance.connect(museum_region)


def collect_all_except(multiworld, item_to_not_collect: str):
    for item in multiworld.get_items():
        if item.name != item_to_not_collect:
            multiworld.state.collect(item)


class TestFriendsanityDatingRules(SVTestBase):
    options = {
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized_not_winter,
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 3
    }

    def test_earning_dating_heart_requires_dating(self):
        month_name = "Month End"
        for i in range(12):
            month_item = self.world.create_item(month_name)
            self.multiworld.state.collect(month_item, event=True)
        self.multiworld.state.collect(self.world.create_item("Beach Bridge"), event=False)
        self.multiworld.state.collect(self.world.create_item("Progressive House"), event=False)
        self.multiworld.state.collect(self.world.create_item("Adventurer's Guild"), event=False)
        self.multiworld.state.collect(self.world.create_item("Galaxy Hammer"), event=False)
        for i in range(3):
            self.multiworld.state.collect(self.world.create_item("Progressive Pickaxe"), event=False)
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
            can_reach = self.world.logic.can_reach_location(location)(self.multiworld.state)
            self.assertTrue(can_reach, f"Should be able to earn relationship up to {i} hearts")
        for i in range(max_reachable + 1, 14 + 1):
            if i % step != 0 and i != 14:
                continue
            location = f"{prefix}{npc} {i}{suffix}"
            can_reach = self.world.logic.can_reach_location(location)(self.multiworld.state)
            self.assertFalse(can_reach, f"Should not be able to earn relationship up to {i} hearts")

