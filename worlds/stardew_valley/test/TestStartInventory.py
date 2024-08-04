from . import SVTestBase
from .assertion import WorldAssertMixin
from .. import options


class TestStartInventoryAllsanity(WorldAssertMixin, SVTestBase):
    options = {
        "accessibility": "items",
        options.Goal.internal_name: options.Goal.option_allsanity,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_remixed,
        options.BundlePrice.internal_name: options.BundlePrice.option_minimum,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive_very_cheap,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive_from_previous_floor,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive_very_cheap,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_easy,
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board,
        options.QuestLocations.internal_name: -1,
        options.Fishsanity.internal_name: options.Fishsanity.option_only_easy_fish,
        options.Museumsanity.internal_name: options.Museumsanity.option_randomized,
        options.Monstersanity.internal_name: options.Monstersanity.option_one_per_category,
        options.Shipsanity.internal_name: options.Shipsanity.option_crops,
        options.Cooksanity.internal_name: options.Cooksanity.option_queen_of_sauce,
        options.Chefsanity.internal_name: 0b1001,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Friendsanity.internal_name: options.Friendsanity.option_bachelors,
        options.FriendsanityHeartSize.internal_name: 3,
        options.NumberOfMovementBuffs.internal_name: 10,
        options.EnabledFillerBuffs.internal_name: options.EnabledFillerBuffs.preset_all,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
        options.Mods.internal_name: ["Tractor Mod", "Bigger Backpack", "Luck Skill", "Magic", "Socializing Skill", "Archaeology", "Cooking Skill",
                                     "Binning Skill"],
        "start_inventory": {"Progressive Pickaxe": 2}
    }

    def test_start_inventory_progression_items_does_not_break_progression_percent(self):
        self.assert_basic_checks_with_subtests(self.multiworld)
        self.assert_can_win(self.multiworld)
