from ... import options
from ...strings.ap_names.ap_option_names import EatsanityOptionName


def default_6_x_x():
    return {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.default,
        options.BackpackProgression.internal_name: options.BackpackProgression.default,
        options.BackpackSize.internal_name: options.BackpackSize.option_12,
        options.Booksanity.internal_name: options.Booksanity.default,
        options.BuildingProgression.internal_name: options.BuildingProgression.default,
        options.BundlePrice.internal_name: options.BundlePrice.default,
        options.BundleRandomization.internal_name: options.BundleRandomization.default,
        options.Chefsanity.internal_name: options.Chefsanity.default,
        options.Cooksanity.internal_name: options.Cooksanity.default,
        options.Craftsanity.internal_name: options.Craftsanity.default,
        options.Cropsanity.internal_name: options.Cropsanity.default,
        options.Eatsanity.internal_name: options.Eatsanity.preset_none,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.default,
        options.EnabledFillerBuffs.internal_name: options.EnabledFillerBuffs.default,
        options.EntranceRandomization.internal_name: options.EntranceRandomization.default,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.default,
        options.FarmType.internal_name: options.FarmType.default,
        options.FestivalLocations.internal_name: options.FestivalLocations.default,
        options.Fishsanity.internal_name: options.Fishsanity.default,
        options.Friendsanity.internal_name: options.Friendsanity.default,
        options.FriendsanityHeartSize.internal_name: options.FriendsanityHeartSize.default,
        options.Goal.internal_name: options.Goal.default,
        options.Hatsanity.internal_name: options.Hatsanity.preset_none,
        options.IncludeEndgameLocations.internal_name: options.IncludeEndgameLocations.option_false,
        options.Mods.internal_name: options.Mods.default,
        options.Monstersanity.internal_name: options.Monstersanity.default,
        options.Moviesanity.internal_name: options.Moviesanity.option_none,
        options.Museumsanity.internal_name: options.Museumsanity.default,
        options.NumberOfMovementBuffs.internal_name: options.NumberOfMovementBuffs.default,
        options.QuestLocations.internal_name: options.QuestLocations.default,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.default,
        options.Secretsanity.internal_name: options.Secretsanity.preset_none,
        options.Shipsanity.internal_name: options.Shipsanity.default,
        options.SkillProgression.internal_name: options.SkillProgression.default,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.default,
        options.ToolProgression.internal_name: options.ToolProgression.default,
        options.TrapDifficulty.internal_name: options.TrapDifficulty.default,
        options.Walnutsanity.internal_name: options.Walnutsanity.default,
    }


def allsanity_no_mods_6_x_x():
    return {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
        options.BackpackSize.internal_name: options.BackpackSize.option_12,
        options.Booksanity.internal_name: options.Booksanity.option_all,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.BundlePrice.internal_name: options.BundlePrice.option_expensive,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_thematic,
        options.Chefsanity.internal_name: options.Chefsanity.preset_all,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Eatsanity.internal_name: options.Eatsanity.preset_none,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive,
        options.EnabledFillerBuffs.internal_name: options.EnabledFillerBuffs.preset_all,
        options.EntranceRandomization.internal_name: options.EntranceRandomization.option_disabled,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
        options.FarmType.internal_name: options.FarmType.option_standard,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_hard,
        options.Fishsanity.internal_name: options.Fishsanity.option_all,
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 1,
        options.Goal.internal_name: options.Goal.option_perfection,
        options.Hatsanity.internal_name: options.Hatsanity.preset_none,
        options.IncludeEndgameLocations.internal_name: options.IncludeEndgameLocations.option_false,
        options.Mods.internal_name: frozenset(),
        options.Monstersanity.internal_name: options.Monstersanity.option_progressive_goals,
        options.Moviesanity.internal_name: options.Moviesanity.option_none,
        options.Museumsanity.internal_name: options.Museumsanity.option_all,
        options.NumberOfMovementBuffs.internal_name: 12,
        options.QuestLocations.internal_name: 56,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
        options.Secretsanity.internal_name: options.Secretsanity.preset_none,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive_with_masteries,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.TrapDifficulty.internal_name: options.TrapDifficulty.option_nightmare,
        options.Walnutsanity.internal_name: options.Walnutsanity.preset_all,
    }


def allsanity_mods_6_x_x_exclude_disabled():
    allsanity = allsanity_no_mods_6_x_x()
    allsanity.update({options.Mods.internal_name: frozenset(options.enabled_mods_except_invalid_combinations)})
    return allsanity


def allsanity_mods_6_x_x():
    allsanity = allsanity_no_mods_6_x_x()
    allsanity.update({options.Mods.internal_name: frozenset(options.all_mods_except_invalid_combinations)})
    return allsanity


def default_7_x_x():
    return {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.default,
        options.BackpackProgression.internal_name: options.BackpackProgression.default,
        options.BackpackSize.internal_name: options.BackpackSize.default,
        options.Booksanity.internal_name: options.Booksanity.default,
        options.BuildingProgression.internal_name: options.BuildingProgression.default,
        options.BundlePerRoom.internal_name: options.BundlePerRoom.default,
        options.BundlePrice.internal_name: options.BundlePrice.default,
        options.BundleRandomization.internal_name: options.BundleRandomization.default,
        options.Chefsanity.internal_name: options.Chefsanity.default,
        options.Cooksanity.internal_name: options.Cooksanity.default,
        options.Craftsanity.internal_name: options.Craftsanity.default,
        options.Cropsanity.internal_name: options.Cropsanity.default,
        options.Eatsanity.internal_name: options.Eatsanity.default,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.default,
        options.EnabledFillerBuffs.internal_name: options.EnabledFillerBuffs.default,
        options.EntranceRandomization.internal_name: options.EntranceRandomization.default,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.default,
        options.FestivalLocations.internal_name: options.FestivalLocations.default,
        options.Fishsanity.internal_name: options.Fishsanity.default,
        options.Friendsanity.internal_name: options.Friendsanity.default,
        options.FriendsanityHeartSize.internal_name: options.FriendsanityHeartSize.default,
        options.Goal.internal_name: options.Goal.default,
        options.Hatsanity.internal_name: options.Hatsanity.default,
        options.IncludeEndgameLocations.internal_name: options.IncludeEndgameLocations.default,
        options.Mods.internal_name: options.Mods.default,
        options.Monstersanity.internal_name: options.Monstersanity.default,
        options.Moviesanity.internal_name: options.Moviesanity.option_none,
        options.Museumsanity.internal_name: options.Museumsanity.default,
        options.NumberOfMovementBuffs.internal_name: options.NumberOfMovementBuffs.default,
        options.QuestLocations.internal_name: options.QuestLocations.default,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.default,
        options.Secretsanity.internal_name: options.Secretsanity.default,
        options.Shipsanity.internal_name: options.Shipsanity.default,
        options.SkillProgression.internal_name: options.SkillProgression.default,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.default,
        options.ToolProgression.internal_name: options.ToolProgression.default,
        options.TrapDifficulty.internal_name: options.TrapDifficulty.default,
        options.Walnutsanity.internal_name: options.Walnutsanity.default,
    }


def allsanity_no_mods_7_x_x():
    return {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
        options.BackpackSize.internal_name: options.BackpackSize.option_1,
        options.Booksanity.internal_name: options.Booksanity.option_all,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.BundlePerRoom.internal_name: options.BundlePerRoom.option_two_extra,
        options.BundlePrice.internal_name: options.BundlePrice.option_expensive,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_thematic,
        options.Chefsanity.internal_name: options.Chefsanity.preset_all,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Eatsanity.internal_name: options.Eatsanity.preset_all,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive,
        options.EnabledFillerBuffs.internal_name: options.EnabledFillerBuffs.preset_all,
        options.EntranceRandomization.internal_name: options.EntranceRandomization.option_disabled,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false,
        options.FarmType.internal_name: options.FarmType.option_beach,  # There is one extra fishing secret on the beach farm
        options.FestivalLocations.internal_name: options.FestivalLocations.option_hard,
        options.Fishsanity.internal_name: options.Fishsanity.option_all,
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 1,
        options.Goal.internal_name: options.Goal.option_perfection,
        options.Hatsanity.internal_name: options.Hatsanity.preset_all,
        options.IncludeEndgameLocations.internal_name: options.IncludeEndgameLocations.option_true,
        options.Mods.internal_name: frozenset(),
        options.Monstersanity.internal_name: options.Monstersanity.option_progressive_goals,
        options.Moviesanity.internal_name: options.Moviesanity.option_all_movies_and_all_loved_snacks,
        options.Museumsanity.internal_name: options.Museumsanity.option_all,
        options.NumberOfMovementBuffs.internal_name: 12,
        options.QuestLocations.internal_name: 56,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
        options.Secretsanity.internal_name: options.Secretsanity.preset_all,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive_with_masteries,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.StartWithout.internal_name: options.StartWithout.preset_all,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.TrapDifficulty.internal_name: options.TrapDifficulty.option_nightmare,
        options.Walnutsanity.internal_name: options.Walnutsanity.preset_all,
    }


def allsanity_mods_7_x_x():
    allsanity = allsanity_no_mods_7_x_x()
    allsanity.update({options.Mods.internal_name: frozenset(options.all_mods_except_invalid_combinations)})
    return allsanity


def allsanity_mods_7_x_x_exclude_disabled():
    allsanity = allsanity_no_mods_7_x_x()
    allsanity.update({options.Mods.internal_name: frozenset(options.enabled_mods_except_invalid_combinations)})
    return allsanity


def get_minsanity_options():
    return {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
        options.BackpackSize.internal_name: options.BackpackSize.option_12,
        options.Booksanity.internal_name: options.Booksanity.option_none,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla,
        options.BundlePerRoom.internal_name: options.BundlePerRoom.option_two_fewer,
        options.BundlePrice.internal_name: options.BundlePrice.option_very_cheap,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_vanilla,
        options.Chefsanity.internal_name: options.Chefsanity.preset_none,
        options.Cooksanity.internal_name: options.Cooksanity.option_none,
        options.Craftsanity.internal_name: options.Craftsanity.option_none,
        options.Cropsanity.internal_name: options.Cropsanity.option_disabled,
        options.Eatsanity.internal_name: options.Eatsanity.preset_none,
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_vanilla,
        options.EnabledFillerBuffs.internal_name: options.EnabledFillerBuffs.preset_none,
        options.EntranceRandomization.internal_name: options.EntranceRandomization.option_disabled,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.FarmType.internal_name: options.FarmType.option_meadowlands,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_disabled,
        options.Fishsanity.internal_name: options.Fishsanity.option_none,
        options.Friendsanity.internal_name: options.Friendsanity.option_none,
        options.FriendsanityHeartSize.internal_name: 8,
        options.Goal.internal_name: options.Goal.option_bottom_of_the_mines,
        options.IncludeEndgameLocations.internal_name: options.IncludeEndgameLocations.option_false,
        options.Mods.internal_name: frozenset(),
        options.Monstersanity.internal_name: options.Monstersanity.option_none,
        options.Moviesanity.internal_name: options.Moviesanity.option_none,
        options.Museumsanity.internal_name: options.Museumsanity.option_none,
        options.NumberOfMovementBuffs.internal_name: 0,
        options.QuestLocations.internal_name: -1,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_disabled,
        options.Secretsanity.internal_name: options.Secretsanity.preset_none,
        options.Shipsanity.internal_name: options.Shipsanity.option_none,
        options.SkillProgression.internal_name: options.SkillProgression.option_vanilla,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_vanilla,
        options.ToolProgression.internal_name: options.ToolProgression.option_vanilla,
        options.TrapDifficulty.internal_name: options.TrapDifficulty.option_no_traps,
        options.Walnutsanity.internal_name: options.Walnutsanity.preset_none,
    }


def minimal_locations_maximal_items():
    min_max_options = {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_disabled,
        options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
        options.BackpackSize.internal_name: options.BackpackSize.option_12,
        options.Booksanity.internal_name: options.Booksanity.option_none,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla,
        options.BundlePerRoom.internal_name: options.BundlePerRoom.option_two_fewer,
        options.BundlePrice.internal_name: options.BundlePrice.option_expensive,
        options.BundleRandomization.internal_name: options.BundleRandomization.option_shuffled,
        options.Chefsanity.internal_name: options.Chefsanity.preset_none,
        options.Cooksanity.internal_name: options.Cooksanity.option_none,
        options.Craftsanity.internal_name: options.Craftsanity.option_none,
        options.Cropsanity.internal_name: options.Cropsanity.option_disabled,
        options.Eatsanity.internal_name: frozenset([EatsanityOptionName.lock_effects]),
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_vanilla,
        options.EnabledFillerBuffs.internal_name: options.EnabledFillerBuffs.preset_all,
        options.EntranceRandomization.internal_name: options.EntranceRandomization.option_disabled,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.FarmType.internal_name: options.FarmType.option_meadowlands,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_disabled,
        options.Fishsanity.internal_name: options.Fishsanity.option_none,
        options.Friendsanity.internal_name: options.Friendsanity.option_none,
        options.FriendsanityHeartSize.internal_name: 8,
        options.Goal.internal_name: options.Goal.option_craft_master,
        options.IncludeEndgameLocations.internal_name: options.IncludeEndgameLocations.option_false,
        options.Mods.internal_name: frozenset(),
        options.Monstersanity.internal_name: options.Monstersanity.option_none,
        options.Moviesanity.internal_name: options.Moviesanity.option_none,
        options.Museumsanity.internal_name: options.Museumsanity.option_none,
        options.NumberOfMovementBuffs.internal_name: 12,
        options.QuestLocations.internal_name: -1,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_randomized,
        options.Secretsanity.internal_name: options.Secretsanity.preset_none,
        options.Shipsanity.internal_name: options.Shipsanity.option_none,
        options.SkillProgression.internal_name: options.SkillProgression.option_vanilla,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_vanilla,
        options.StartWithout.internal_name: options.StartWithout.preset_all,
        options.ToolProgression.internal_name: options.ToolProgression.option_vanilla,
        options.TrapDifficulty.internal_name: options.TrapDifficulty.option_nightmare,
        options.Walnutsanity.internal_name: options.Walnutsanity.preset_none,
    }
    return min_max_options


def minimal_locations_maximal_items_with_island():
    min_max_options = minimal_locations_maximal_items()
    min_max_options.update({options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false})
    return min_max_options
