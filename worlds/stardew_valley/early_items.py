from random import Random

from .options import BuildingProgression, StardewValleyOptions, BackpackProgression, ExcludeGingerIsland, SeasonRandomization, SpecialOrderLocations, \
    Monstersanity, ToolProgression, SkillProgression, Cooksanity, Chefsanity

early_candidate_rate = 4
always_early_candidates = ["Greenhouse", "Desert Obelisk", "Rusty Key"]
seasons = ["Spring", "Summer", "Fall", "Winter"]


def setup_early_items(multiworld, options: StardewValleyOptions, player: int, random: Random):
    early_forced = []
    early_candidates = []
    early_candidates.extend(always_early_candidates)

    add_seasonal_candidates(early_candidates, options)

    if options.building_progression & BuildingProgression.option_progressive:
        early_forced.append("Shipping Bin")
        early_candidates.append("Progressive Coop")
        early_candidates.append("Progressive Barn")

    if options.backpack_progression == BackpackProgression.option_early_progressive:
        early_forced.append("Progressive Backpack")

    if options.tool_progression & ToolProgression.option_progressive:
        early_forced.append("Progressive Fishing Rod")
        early_forced.append("Progressive Pickaxe")

    if options.skill_progression == SkillProgression.option_progressive:
        early_forced.append("Fishing Level")

    if options.quest_locations >= 0:
        early_candidates.append("Magnifying Glass")

    if options.special_order_locations & SpecialOrderLocations.option_board:
        early_candidates.append("Special Order Board")

    if options.cooksanity != Cooksanity.option_none | options.chefsanity & Chefsanity.option_queen_of_sauce:
        early_candidates.append("The Queen of Sauce")

    if options.monstersanity == Monstersanity.option_none:
        early_candidates.append("Progressive Weapon")
    else:
        early_candidates.append("Progressive Sword")

    if options.exclude_ginger_island == ExcludeGingerIsland.option_false:
        early_candidates.append("Island Obelisk")

    early_forced.extend(random.sample(early_candidates, len(early_candidates) // early_candidate_rate))

    for item_name in early_forced:
        if item_name in multiworld.early_items[player]:
            continue
        multiworld.early_items[player][item_name] = 1


def add_seasonal_candidates(early_candidates, options):
    if options.season_randomization == SeasonRandomization.option_progressive:
        early_candidates.extend(["Progressive Season"] * 3)
        return
    if options.season_randomization == SeasonRandomization.option_disabled:
        return

    early_candidates.extend(seasons)
