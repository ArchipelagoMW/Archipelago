from BaseClasses import ItemClassification
from . import SVTestBase
from .. import locations, items, location_table, options
from ..data.villagers_data import all_villagers_by_name
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
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
        options.SeedShuffle.internal_name: options.SeedShuffle.option_shuffled,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
        options.ToolProgression.internal_name: options.ToolProgression.option_vanilla,
        options.SkillProgression.internal_name: options.SkillProgression.option_vanilla,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla,
        options.TheMinesElevatorsProgression.internal_name: options.TheMinesElevatorsProgression.option_vanilla,
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled,
        options.HelpWantedLocations.internal_name: 0,
        options.Fishsanity.internal_name: options.Fishsanity.option_none,
        options.Museumsanity.internal_name: options.Museumsanity.option_none,
        options.Friendsanity.internal_name: options.Museumsanity.option_none,
        options.NumberOfPlayerBuffs.internal_name: 12,
    }

    def test_minimal_location_maximal_items_still_valid(self):
        assert len(self.multiworld.get_locations()) >= len(self.multiworld.get_items())


class TestFriendsanityNone(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_none,
    }

    def test_no_friendsanity_items(self):
        for item in self.multiworld.get_items():
            assert not item.name.endswith(": 1 <3")

    def test_no_friendsanity_locations(self):
        for location in self.multiworld.get_locations():
            assert not location.name.startswith("Friendsanity")


class TestFriendsanityBachelors(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_bachelors,
    }
    bachelors = {"Harvey", "Elliott", "Sam", "Alex", "Shane", "Sebastian", "Emily", "Haley", "Leah", "Abigail", "Penny",
                 "Maru"}

    def test_friendsanity_only_bachelor_items(self):
        suffix = ": 1 <3"
        for item in self.multiworld.get_items():
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                assert villager_name in self.bachelors

    def test_friendsanity_only_bachelor_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location in self.multiworld.get_locations():
            if location.name.startswith(prefix):
                name_no_prefix = location.name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                assert name in self.bachelors
                assert int(hearts) <= 8


class TestFriendsanityStartingNpcs(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_starting_npcs,
    }
    excluded_npcs = {"Leo", "Krobus", "Dwarf", "Sandy", "Kent"}

    def test_friendsanity_only_starting_npcs_items(self):
        suffix = ": 1 <3"
        for item in self.multiworld.get_items():
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                assert villager_name not in self.excluded_npcs

    def test_friendsanity_only_starting_npcs_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location in self.multiworld.get_locations():
            if location.name.startswith(prefix):
                name_no_prefix = location.name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                assert name not in self.excluded_npcs
                assert name in all_villagers_by_name or name == "Pet"
                if name == "Pet":
                    assert int(hearts) <= 5
                elif all_villagers_by_name[name].bachelor:
                    assert int(hearts) <= 8
                else:
                    assert int(hearts) <= 10


class TestFriendsanityAllNpcs(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all,
    }

    def test_friendsanity_all_items(self):
        suffix = ": 1 <3"
        for item in self.multiworld.get_items():
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                assert villager_name in all_villagers_by_name or villager_name == "Pet"

    def test_friendsanity_all_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location in self.multiworld.get_locations():
            if location.name.startswith(prefix):
                name_no_prefix = location.name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                assert name in all_villagers_by_name or name == "Pet"
                if name == "Pet":
                    assert int(hearts) <= 5
                elif all_villagers_by_name[name].bachelor:
                    assert int(hearts) <= 8
                else:
                    assert int(hearts) <= 10


class TestFriendsanityAllNpcsWithMarriage(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = ": 1 <3"
        for item in self.multiworld.get_items():
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                assert villager_name in all_villagers_by_name or villager_name == "Pet"

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location in self.multiworld.get_locations():
            if location.name.startswith(prefix):
                name_no_prefix = location.name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                assert name in all_villagers_by_name or name == "Pet"
                if name == "Pet":
                    assert int(hearts) <= 5
                elif all_villagers_by_name[name].bachelor:
                    assert int(hearts) <= 14
                else:
                    assert int(hearts) <= 10
