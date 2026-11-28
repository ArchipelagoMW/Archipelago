from .. import options
from ..mods.mod_data import ModNames
from .assertion import WorldAssertMixin
from .bases import SVTestBase


class TestStartInventoryAllsanity(WorldAssertMixin, SVTestBase):
    options = {  # noqa: RUF012
        "accessibility": "items",
        options.Goal: options.Goal.option_allsanity,
        options.BundleRandomization: options.BundleRandomization.option_remixed,
        options.BundlePrice: options.BundlePrice.option_minimum,
        options.SeasonRandomization: options.SeasonRandomization.option_randomized,
        options.Cropsanity: options.Cropsanity.option_enabled,
        options.ToolProgression: options.ToolProgression.option_progressive_very_cheap,
        options.ElevatorProgression: options.ElevatorProgression.option_progressive_from_previous_floor,
        options.SkillProgression: options.SkillProgression.option_progressive,
        options.BuildingProgression: options.BuildingProgression.option_progressive_very_cheap,
        options.FestivalLocations: options.FestivalLocations.option_easy,
        options.JourneyOfThePrairieKing: options.JourneyOfThePrairieKing.option_disabled,
        options.JunimoKart: options.JunimoKart.option_disabled,
        options.SpecialOrderLocations: options.SpecialOrderLocations.option_board,
        options.QuestLocations: -1,
        options.Fishsanity: options.Fishsanity.option_only_easy_fish,
        options.Museumsanity: options.Museumsanity.option_randomized,
        options.Monstersanity: options.Monstersanity.option_one_per_category,
        options.Shipsanity: options.Shipsanity.option_crops,
        options.Cooksanity: options.Cooksanity.option_queen_of_sauce,
        options.Chefsanity: options.Chefsanity.preset_all,
        options.Craftsanity: options.Craftsanity.option_all,
        options.Friendsanity: options.Friendsanity.option_bachelors,
        options.FriendsanityHeartSize: 3,
        options.NumberOfMovementBuffs: 10,
        options.EnabledFillerBuffs: options.EnabledFillerBuffs.preset_all,
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
        options.Mods: [
            ModNames.tractor,
            ModNames.big_backpack,
            ModNames.luck_skill,
            # ModNames.magic,
            ModNames.socializing_skill,
            ModNames.archaeology,
            # ModNames.cooking_skill,
            ModNames.binning_skill,
        ],
        "start_inventory": {"Progressive Pickaxe": 2},
    }

    def test_start_inventory_progression_items_does_not_break_progression_percent(self):
        self.assert_basic_checks_with_subtests(self.multiworld)
        self.assert_can_win(self.multiworld)
