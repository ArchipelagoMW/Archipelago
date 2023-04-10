from BaseClasses import ItemClassification
from . import SVTestBase
from .. import locations, items, location_table, options
from ..items import items_by_group, Group
from ..locations import LocationTags


class TestBaseItemGeneration(SVTestBase):

    def test_all_progression_items_are_added_to_the_pool(self):
        for classification in [ItemClassification.progression, ItemClassification.useful]:
            with self.subTest(classification=classification):

                all_classified_items = {self.world.create_item(item)
                                        for item in items.items_by_group[items.Group.COMMUNITY_REWARD]
                                        if item.classification is classification}

                for item in all_classified_items:
                    assert item in self.multiworld.itempool

    def test_creates_as_many_item_as_non_event_locations(self):
        non_event_locations = [location for location in self.multiworld.get_locations(self.player) if
                               not location.event]

        assert len(non_event_locations), len(self.multiworld.itempool)


class TestGivenProgressiveBackpack(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive}

    def test_when_generate_world_then_two_progressive_backpack_are_added(self):
        assert self.multiworld.itempool.count(self.world.create_item("Progressive Backpack")) == 2

    def test_when_generate_world_then_backpack_locations_are_added(self):
        created_locations = {location.name for location in self.multiworld.get_locations(1)}
        assert all(location.name in created_locations for location in locations.locations_by_tag[LocationTags.BACKPACK])


class TestRemixedMineRewards(SVTestBase):
    def test_when_generate_world_then_one_reward_is_added_per_chest(self):
        # assert self.world.create_item("Rusty Sword") in self.multiworld.itempool
        assert any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_10])
        assert any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_20])
        assert self.world.create_item("Slingshot") in self.multiworld.itempool
        assert any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_50])
        assert any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_60])
        assert self.world.create_item("Master Slingshot") in self.multiworld.itempool
        assert any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_80])
        assert any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_90])
        assert self.world.create_item("Stardrop") in self.multiworld.itempool
        assert any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_110])
        assert self.world.create_item("Skull Key") in self.multiworld.itempool

    # This test as 1 over 90,000 changes to fail... Sorry in advance
    def test_when_generate_world_then_rewards_are_not_all_vanilla(self):
        assert not all(self.world.create_item(item) in self.multiworld.itempool
                       for item in
                       ["Leather Boots", "Steel Smallsword", "Tundra Boots", "Crystal Dagger", "Firewalker Boots",
                        "Obsidian Edge", "Space Boots"])


class TestProgressiveElevator(SVTestBase):
    options = {
        options.TheMinesElevatorsProgression.internal_name: options.TheMinesElevatorsProgression.option_progressive,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_given_access_to_floor_115_when_find_another_elevator_then_has_access_to_floor_120(self):
        self.collect([self.get_item_by_name("Progressive Pickaxe")] * 2)
        self.collect([self.get_item_by_name("Progressive Mine Elevator")] * 22)
        self.collect(self.multiworld.create_item("Bone Sword", self.player))
        self.collect([self.get_item_by_name("Combat Level")] * 4)
        self.collect(self.get_item_by_name("Adventurer's Guild"))

        assert not self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state)

        self.collect(self.get_item_by_name("Progressive Mine Elevator"))

        assert self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state)

    def test_given_access_to_floor_115_when_find_another_pickaxe_and_sword_then_has_access_to_floor_120(self):
        self.collect([self.get_item_by_name("Progressive Pickaxe")] * 2)
        self.collect([self.get_item_by_name("Progressive Mine Elevator")] * 22)
        self.collect(self.multiworld.create_item("Bone Sword", self.player))
        self.collect([self.get_item_by_name("Combat Level")] * 4)
        self.collect(self.get_item_by_name("Adventurer's Guild"))

        assert not self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state)

        self.collect(self.get_item_by_name("Progressive Pickaxe"))
        self.collect(self.multiworld.create_item("Steel Falchion", self.player))
        self.collect(self.get_item_by_name("Combat Level"))
        self.collect(self.get_item_by_name("Combat Level"))

        assert self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state)


class TestLocationGeneration(SVTestBase):

    def test_all_location_created_are_in_location_table(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event:
                assert location.name in location_table


class TestLocationAndItemCount(SVTestBase):
    options = {
        options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
        options.ToolProgression.internal_name: options.ToolProgression.option_vanilla,
        options.TheMinesElevatorsProgression.internal_name: options.TheMinesElevatorsProgression.option_vanilla,
        options.SkillProgression.internal_name: options.SkillProgression.option_vanilla,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla,
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled,
        options.HelpWantedLocations.internal_name: 0,
        options.NumberOfPlayerBuffs.internal_name: 12,
    }

    def test_minimal_location_maximal_items_still_valid(self):
        assert len(self.multiworld.get_locations()) >= len(self.multiworld.get_items())
