from . import setup_solo_multiworld, SVTestCase
from .checks.world_checks import basic_checks_with_subtests
from .. import Goal
from ..options import SpecialOrderLocations, FestivalLocations, NumberOfMovementBuffs, BundleRandomization, BundlePrice, SeasonRandomization, Cropsanity, \
    ToolProgression, ElevatorProgression, SkillProgression, BuildingProgression, ArcadeMachineLocations, QuestLocations, Fishsanity, Museumsanity, \
    Monstersanity, Shipsanity, Cooksanity, Chefsanity, Craftsanity, Friendsanity, FriendsanityHeartSize, NumberOfLuckBuffs, ExcludeGingerIsland, Mods


class TestStartInventoryAllsanity(SVTestCase):

    def test_start_inventory_movement_speed(self):
        start_inventory = {"Movement Speed Bonus": 2}
        options = {
            "accessibility": "items",
            Goal.internal_name: Goal.option_allsanity,
            BundleRandomization.internal_name: BundleRandomization.option_remixed,
            BundlePrice.internal_name: BundlePrice.option_minimum,
            SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
            Cropsanity.internal_name: Cropsanity.option_enabled,
            ToolProgression.internal_name: ToolProgression.option_progressive_very_cheap,
            ElevatorProgression.internal_name: ElevatorProgression.option_progressive_from_previous_floor,
            SkillProgression.internal_name: SkillProgression.option_progressive,
            BuildingProgression.internal_name: BuildingProgression.option_progressive_very_cheap,
            FestivalLocations.internal_name: FestivalLocations.option_easy,
            ArcadeMachineLocations.internal_name: ArcadeMachineLocations.option_disabled,
            SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_only,
            QuestLocations.internal_name: -1,
            Fishsanity.internal_name: Fishsanity.option_only_easy_fish,
            Museumsanity.internal_name: Museumsanity.option_randomized,
            Monstersanity.internal_name: Monstersanity.option_one_per_category,
            Shipsanity.internal_name: Shipsanity.option_crops,
            Cooksanity.internal_name: Cooksanity.option_queen_of_sauce,
            Chefsanity.internal_name: 0b1001,
            Craftsanity.internal_name: Craftsanity.option_all,
            Friendsanity.internal_name: Friendsanity.option_bachelors,
            FriendsanityHeartSize.internal_name: 3,
            NumberOfMovementBuffs.internal_name: 10,
            NumberOfLuckBuffs.internal_name: 12,
            ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
            Mods.internal_name: ["Tractor Mod", "Bigger Backpack", "Luck Skill", "Magic", "Socializing Skill", "Archaeology", "Cooking Skill", "Binning Skill"],
            "start_inventory": start_inventory
        }

        multiworld = setup_solo_multiworld(options)
        basic_checks_with_subtests(self, multiworld)
        self.assertTrue(multiworld.can_beat_game())
