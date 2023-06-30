from collections import Counter

from . import SVTestBase
from .. import options


class TestProgressiveToolsLogic(SVTestBase):
    options = {
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
    }

    def setUp(self):
        super().setUp()
        self.multiworld.state.prog_items = Counter()

    def test_sturgeon(self):
        assert not self.world.logic.has("Sturgeon")(self.multiworld.state)

        summer = self.world.create_item("Summer")
        self.multiworld.state.collect(summer, event=True)
        assert not self.world.logic.has("Sturgeon")(self.multiworld.state)

        fishing_rod = self.world.create_item("Progressive Fishing Rod")
        self.multiworld.state.collect(fishing_rod, event=True)
        self.multiworld.state.collect(fishing_rod, event=True)
        assert not self.world.logic.has("Sturgeon")(self.multiworld.state)

        fishing_level = self.world.create_item("Fishing Level")
        self.multiworld.state.collect(fishing_level, event=True)
        assert not self.world.logic.has("Sturgeon")(self.multiworld.state)

        self.multiworld.state.collect(fishing_level, event=True)
        self.multiworld.state.collect(fishing_level, event=True)
        self.multiworld.state.collect(fishing_level, event=True)
        self.multiworld.state.collect(fishing_level, event=True)
        self.multiworld.state.collect(fishing_level, event=True)
        assert self.world.logic.has("Sturgeon")(self.multiworld.state)

        self.remove(summer)
        assert not self.world.logic.has("Sturgeon")(self.multiworld.state)

        winter = self.world.create_item("Winter")
        self.multiworld.state.collect(winter, event=True)
        assert self.world.logic.has("Sturgeon")(self.multiworld.state)

        self.remove(fishing_rod)
        assert not self.world.logic.has("Sturgeon")(self.multiworld.state)

    def test_old_master_cannoli(self):
        self.multiworld.state.collect(self.world.create_item("Progressive Axe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Progressive Axe"), event=True)
        self.multiworld.state.collect(self.world.create_item("Summer"), event=True)

        assert not self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state)

        fall = self.world.create_item("Fall")
        self.multiworld.state.collect(fall, event=True)
        assert not self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state)

        tuesday = self.world.create_item("Traveling Merchant: Tuesday")
        self.multiworld.state.collect(tuesday, event=True)
        assert self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state)

        self.remove(fall)
        assert not self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state)
        self.remove(tuesday)

        green_house = self.world.create_item("Greenhouse")
        self.multiworld.state.collect(green_house, event=True)
        assert not self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state)

        friday = self.world.create_item("Traveling Merchant: Friday")
        self.multiworld.state.collect(friday, event=True)
        assert self.multiworld.get_location("Old Master Cannoli", 1).access_rule(self.multiworld.state)

        self.remove(green_house)
        assert not self.world.logic.can_reach_location("Old Master Cannoli")(self.multiworld.state)
        self.remove(friday)


class TestBundlesLogic(SVTestBase):
    options = {
    }

    def test_vault_2500g_bundle(self):
        assert self.world.logic.can_reach_location("2,500g Bundle")(self.multiworld.state)


class TestBuildingLogic(SVTestBase):
    options = {
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive_early_shipping_bin
    }

    def test_coop_blueprint(self):
        assert not self.world.logic.can_reach_location("Coop Blueprint")(self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        assert self.world.logic.can_reach_location("Coop Blueprint")(self.multiworld.state)

    def test_big_coop_blueprint(self):
        assert not self.world.logic.can_reach_location("Big Coop Blueprint")(self.multiworld.state), \
            f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}"

        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        assert not self.world.logic.can_reach_location("Big Coop Blueprint")(self.multiworld.state), \
            f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}"

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=True)
        assert self.world.logic.can_reach_location("Big Coop Blueprint")(self.multiworld.state), \
            f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}"

    def test_deluxe_coop_blueprint(self):
        assert not self.world.logic.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        assert not self.world.logic.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=True)
        assert not self.world.logic.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Progressive Coop"), event=True)
        assert self.world.logic.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state)

    def test_big_shed_blueprint(self):
        assert not self.world.logic.can_reach_location("Big Shed Blueprint")(self.multiworld.state), \
            f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}"

        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        self.multiworld.state.collect(self.world.create_item("Month End"), event=True)
        assert not self.world.logic.can_reach_location("Big Shed Blueprint")(self.multiworld.state), \
            f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}"

        self.multiworld.state.collect(self.world.create_item("Progressive Shed"), event=True)
        assert self.world.logic.can_reach_location("Big Shed Blueprint")(self.multiworld.state), \
            f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}"


class TestArcadeMachinesLogic(SVTestBase):
    options = {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
    }

    def test_prairie_king(self):
        assert not self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state)
        assert not self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state)
        assert not self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state)
        assert not self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state)

        boots = self.world.create_item("JotPK: Progressive Boots")
        gun = self.world.create_item("JotPK: Progressive Gun")
        ammo = self.world.create_item("JotPK: Progressive Ammo")
        life = self.world.create_item("JotPK: Extra Life")
        drop = self.world.create_item("JotPK: Increased Drop Rate")

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(gun, event=True)
        assert self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state)
        assert not self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state)
        assert not self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state)
        assert not self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state)
        self.remove(boots)
        self.remove(gun)

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(boots, event=True)
        assert self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state)
        assert not self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state)
        assert not self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state)
        assert not self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state)
        self.remove(boots)
        self.remove(boots)

        self.multiworld.state.collect(boots, event=True)
        self.multiworld.state.collect(gun, event=True)
        self.multiworld.state.collect(ammo, event=True)
        self.multiworld.state.collect(life, event=True)
        assert self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state)
        assert self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state)
        assert not self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state)
        assert not self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state)
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
        assert self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state)
        assert self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state)
        assert self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state)
        assert not self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state)
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
        assert self.world.logic.can_reach_region("JotPK World 1")(self.multiworld.state)
        assert self.world.logic.can_reach_region("JotPK World 2")(self.multiworld.state)
        assert self.world.logic.can_reach_region("JotPK World 3")(self.multiworld.state)
        assert self.world.logic.can_reach_location("Journey of the Prairie King Victory")(self.multiworld.state)
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
            assert self.world.logic.can_mine_in_the_mines_floor_1_40()(self.multiworld.state)
        else:
            assert not self.world.logic.can_mine_in_the_mines_floor_1_40()(self.multiworld.state)

        if reachable_level > 1:
            assert self.world.logic.can_mine_in_the_mines_floor_41_80()(self.multiworld.state)
        else:
            assert not self.world.logic.can_mine_in_the_mines_floor_41_80()(self.multiworld.state)

        if reachable_level > 2:
            assert self.world.logic.can_mine_in_the_mines_floor_81_120()(self.multiworld.state)
        else:
            assert not self.world.logic.can_mine_in_the_mines_floor_81_120()(self.multiworld.state)

        if reachable_level > 3:
            assert self.world.logic.can_mine_in_the_skull_cavern()(self.multiworld.state)
        else:
            assert not self.world.logic.can_mine_in_the_skull_cavern()(self.multiworld.state)

        if reachable_level > 4:
            assert self.world.logic.can_mine_perfectly_in_the_skull_cavern()(self.multiworld.state)
        else:
            assert not self.world.logic.can_mine_perfectly_in_the_skull_cavern()(self.multiworld.state)

        self.remove(item)
