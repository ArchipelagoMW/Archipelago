from ... import StardewItem
from ...options import (
    BuildingProgression,
    ElevatorProgression,
    EntranceRandomization,
    ExcludeGingerIsland,
    Fishsanity,
    Mods,
    SeasonRandomization,
    SkillProgression,
    SpecialOrderLocations,
    StartWithout,
    ToolProgression,
)
from ...options.options import CustomLogic, DataRandomization, DataRandomizationBehavior, Shipsanity
from ...strings.ap_names.ap_option_names import CustomLogicOptionName, DataRandomizationOptionName, StartWithoutOptionName
from ...strings.ap_names.transport_names import Transportation
from ...strings.fish_names import Fish
from ...strings.tv_channel_names import Channel
from ..bases import SVTestBase


class TestNeedRegionToCatchFish(SVTestBase):
    options = {
        StartWithout: frozenset({StartWithoutOptionName.landslide, StartWithoutOptionName.community_center}),
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_progressive,
        Fishsanity.internal_name: Fishsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi, }

    def test_catch_fish_requires_region_unlock(self):
        fish_and_items: dict[str, list[str | list[str]]] = {
            Fish.crimsonfish: [["Beach Bridge", "Town To Tide Pools Shortcut"]],
            Fish.void_salmon: ["Railroad Boulder Removed", "Dark Talisman"],
            Fish.woodskip: ["Progressive Axe", "Progressive Axe"],
            Fish.mutant_carp: ["Rusty Key"],
            Fish.slimejack: ["Railroad Boulder Removed", "Rusty Key"],
            Fish.lionfish: [[Transportation.boat_repair, "Island Obelisk"]],
            Fish.blue_discus: ["Wizard Invitation", "Island Obelisk", ["Island West Turtle", "Parrot Express"]],
            Fish.stingray: [Transportation.boat_repair, "Island Resort"],
            Fish.ghostfish: [["Landslide Removed", "Mountain Shortcuts"], "Progressive Weapon"],
            Fish.stonefish: [["Landslide Removed", "Mountain Shortcuts"], "Progressive Weapon"],
            Fish.ice_pip: [["Landslide Removed", "Mountain Shortcuts"], "Progressive Weapon", "Progressive Weapon", "Progressive Pickaxe"],
            Fish.lava_eel: [["Landslide Removed", "Mountain Shortcuts"], "Progressive Weapon", "Progressive Weapon", "Progressive Weapon",
                            "Progressive Pickaxe", "Progressive Pickaxe"],
            Fish.sandfish: [Transportation.bus_repair],
            Fish.scorpion_carp: ["Wizard Invitation", "Desert Obelisk"],

            Fish.son_of_crimsonfish: [Transportation.boat_repair, ["Island West Turtle", "Parrot Express"], "Qi Walnut Room", ["Beach Bridge", "Town To Tide Pools Shortcut"]],
            Fish.radioactive_carp: ["Rusty Key", Transportation.boat_repair, ["Island West Turtle", "Parrot Express"], "Qi Walnut Room"],
            Fish.glacierfish_jr: [Transportation.boat_repair, ["Island West Turtle", "Parrot Express"], "Qi Walnut Room"],
            Fish.legend_ii: ["Wizard Invitation", "Island Obelisk", ["Island West Turtle", "Parrot Express"], "Qi Walnut Room"],
            Fish.ms_angler: ["Wizard Invitation", "Island Obelisk", ["Island West Turtle", "Parrot Express"], "Qi Walnut Room"], }
        self.collect("Progressive Fishing Rod", 4)
        self.collect_all_the_money()
        for fish in fish_and_items:
            with self.subTest(f"Region rules for {fish}"):
                item_names = fish_and_items[fish]
                location = f"Fishsanity: {fish}"
                self.assert_cannot_reach_location(location)
                items = [
                    (self.create_item(item_name) if isinstance(item_name, str) else [self.create_item(itn) for itn in item_name]) for item_name in item_names]
                for item in items:
                    self.collect(item)
                with self.subTest(f"{fish} can be reached with {item_names}"):
                    self.assert_can_reach_location(location)
                for items_required in items:
                    if isinstance(items_required, StardewItem):
                        item_required = items_required
                        with self.subTest(f"{fish} requires {item_required.name}"):
                            self.remove(item_required)
                            self.assert_cannot_reach_location(location)
                            self.collect(item_required)
                            self.assert_can_reach_location(location)
                    else:
                        with self.subTest(f"{fish} requires {' or '.join((item_required.name for item_required in items_required))}"):
                            self.remove(items_required)
                            self.assert_cannot_reach_location(location)
                            self.collect(items_required)
                            self.assert_can_reach_location(location)
                for item in items:
                    self.remove(item)


class TestNeedLevelsToCatchFish(SVTestBase):
    options = {
        StartWithout: frozenset({StartWithoutOptionName.landslide, StartWithoutOptionName.community_center}),
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_progressive,
        ToolProgression.internal_name: ToolProgression.option_progressive,
        Fishsanity.internal_name: Fishsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
        DataRandomization.internal_name: frozenset(DataRandomization.preset_all - {DataRandomizationOptionName.fish_catch_method}),
        DataRandomizationBehavior.internal_name: DataRandomizationBehavior.option_weighted_randomized,
    }

    def test_catch_fish_requires_minimum_level(self):
        fish_and_levels: dict[str, int] = {
            Fish.angler: 3,
            Fish.crimsonfish: 5,
            Fish.glacierfish: 6,
            Fish.legend: 10,

            Fish.ms_angler: 3,
            Fish.son_of_crimsonfish: 5,
            Fish.glacierfish_jr: 6,
            Fish.legend_ii: 10,
        }
        self.collect("Progressive Fishing Rod", 4)
        region_items = ["Beach Bridge", "Town To Tide Pools Shortcut", "Rusty Key", "Beach Bridge",
                        "Wizard Invitation", "Island Obelisk", "Island West Turtle", "Qi Walnut Room" ]
        collected_items = [self.collect(item) for item in region_items]
        self.collect_all_the_money()
        for fish in fish_and_levels:
            with self.subTest(f"Level rules for {fish}"):
                level = fish_and_levels[fish]
                location = f"Fishsanity: {fish}"
                items = [self.create_item(item_name) for item_name in (["Fishing Level"] * level)]
                for item in items:
                    self.assert_cannot_reach_location(location)
                    self.collect(item)
                for item in items:
                    self.remove(item)


weapons = ["Progressive Weapon"] * 5
fishing_items = ["Beach Bridge", "Rusty Key", "Wizard Invitation", "Island Obelisk", "Bus Repair", "Dark Talisman", "Island Resort",
                "Island West Turtle", "Qi Walnut Room", "Shipping Bin", "Railroad Boulder Removed", "Nexus: Farm Runes", "Nexus: Outpost Runes",
                "Marlon's Boat Paddle", "Fable Reef Portal", "Kittyfish Spell", *weapons ]

class TestNeedFIBSToCatchDRFish(SVTestBase):
    options = {
        EntranceRandomization.internal_name: EntranceRandomization.option_disabled,
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        BuildingProgression.internal_name: BuildingProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_vanilla,
        Fishsanity.internal_name: Fishsanity.option_all,
        Shipsanity.internal_name: Shipsanity.option_everything,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
        DataRandomization.internal_name: frozenset(DataRandomization.preset_all - {DataRandomizationOptionName.shop_currencies}),
        DataRandomizationBehavior.internal_name: DataRandomizationBehavior.option_shuffled,
        Mods.internal_name: frozenset(Mods.valid_keys),
        CustomLogic.internal_name: frozenset({}),
    }

    def test_fish_require_fibs(self):
        collected_items = [self.collect(item) for item in fishing_items]
        content = self.world.content
        self.collect_all_the_money()
        for fish_name in content.fishes:
            fish = content.fishes[fish_name]
            fishsanity_location = f"Fishsanity: {fish_name}"
            shipsanity_location = f"Shipsanity: {fish_name}"
            is_crab_pot = fish.is_crab_pot()
            if is_crab_pot:
                with self.subTest(f"{fish_name} does not require FIBS"):
                    self.assert_can_reach_location(fishsanity_location)
                    self.assert_can_reach_location(shipsanity_location)
            else:
                with self.subTest(f"{fish_name} requires FIBS"):
                    self.assert_cannot_reach_location(fishsanity_location)
                    self.assert_cannot_reach_location(shipsanity_location)

                    fibs = self.create_item(Channel.fibs)
                    self.collect(fibs)

                    self.assert_can_reach_location(fishsanity_location)
                    self.assert_can_reach_location(shipsanity_location)

                    self.remove(fibs)


class TestDontNeedFIBSToCatchDRFishWithCustomLogic(SVTestBase):
    options = {
        EntranceRandomization.internal_name: EntranceRandomization.option_disabled,
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        BuildingProgression.internal_name: BuildingProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_vanilla,
        Fishsanity.internal_name: Fishsanity.option_all,
        Shipsanity.internal_name: Shipsanity.option_everything,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
        DataRandomization.internal_name: frozenset(DataRandomization.preset_all - {DataRandomizationOptionName.shop_currencies}),
        DataRandomizationBehavior.internal_name: DataRandomizationBehavior.option_shuffled,
        Mods.internal_name: frozenset(Mods.valid_keys),
        CustomLogic.internal_name: frozenset({CustomLogicOptionName.no_fibs}),
    }

    def test_fish_require_fibs(self):
        collected_items = [self.collect(item) for item in fishing_items]
        content = self.world.content
        self.collect_all_the_money()
        for fish_name in content.fishes:
            fish = content.fishes[fish_name]
            fishsanity_location = f"Fishsanity: {fish_name}"
            shipsanity_location = f"Shipsanity: {fish_name}"
            is_crab_pot = fish.is_crab_pot()
            with self.subTest(f"{fish_name} does not require FIBS"):
                self.assert_can_reach_location(fishsanity_location)
                self.assert_can_reach_location(shipsanity_location)


class TestDontNeedFIBSToCatchNonDRFish(SVTestBase):
    options = {
        EntranceRandomization.internal_name: EntranceRandomization.option_disabled,
        SeasonRandomization.internal_name: SeasonRandomization.option_disabled,
        ElevatorProgression.internal_name: ElevatorProgression.option_vanilla,
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        BuildingProgression.internal_name: BuildingProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_vanilla,
        Fishsanity.internal_name: Fishsanity.option_all,
        Shipsanity.internal_name: Shipsanity.option_everything,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
        DataRandomization.internal_name: frozenset(DataRandomization.preset_none),
        DataRandomizationBehavior.internal_name: DataRandomizationBehavior.option_shuffled,
        Mods.internal_name: frozenset(Mods.valid_keys),
        CustomLogic.internal_name: frozenset({}),
    }

    def test_fish_require_fibs(self):
        collected_items = [self.collect(item) for item in fishing_items]
        content = self.world.content
        self.collect_all_the_money()
        for fish_name in content.fishes:
            fish = content.fishes[fish_name]
            fishsanity_location = f"Fishsanity: {fish_name}"
            shipsanity_location = f"Shipsanity: {fish_name}"
            is_crab_pot = fish.is_crab_pot()
            with self.subTest(f"{fish_name} does not require FIBS"):
                self.assert_can_reach_location(fishsanity_location)
                self.assert_can_reach_location(shipsanity_location)
