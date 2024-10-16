from . import content_packs
from .feature import cropsanity, friendsanity, fishsanity, booksanity, skill_progression
from .game_content import ContentPack, StardewContent, StardewFeatures
from .unpacking import unpack_content
from .. import options


def create_content(player_options: options.StardewValleyOptions) -> StardewContent:
    active_packs = choose_content_packs(player_options)
    features = choose_features(player_options)
    return unpack_content(features, active_packs)


def choose_content_packs(player_options: options.StardewValleyOptions):
    active_packs = [content_packs.pelican_town, content_packs.the_desert, content_packs.the_farm, content_packs.the_mines]

    if player_options.exclude_ginger_island == options.ExcludeGingerIsland.option_false:
        active_packs.append(content_packs.ginger_island_content_pack)

        if player_options.special_order_locations & options.SpecialOrderLocations.value_qi:
            active_packs.append(content_packs.qi_board_content_pack)

    for mod in player_options.mods.value:
        active_packs.append(content_packs.by_mod[mod])

    return active_packs


def choose_features(player_options: options.StardewValleyOptions) -> StardewFeatures:
    return StardewFeatures(
        choose_booksanity(player_options.booksanity),
        choose_cropsanity(player_options.cropsanity),
        choose_fishsanity(player_options.fishsanity),
        choose_friendsanity(player_options.friendsanity, player_options.friendsanity_heart_size),
        choose_skill_progression(player_options.skill_progression),
    )


booksanity_by_option = {
    options.Booksanity.option_none: booksanity.BooksanityDisabled(),
    options.Booksanity.option_power: booksanity.BooksanityPower(),
    options.Booksanity.option_power_skill: booksanity.BooksanityPowerSkill(),
    options.Booksanity.option_all: booksanity.BooksanityAll(),
}


def choose_booksanity(booksanity_option: options.Booksanity) -> booksanity.BooksanityFeature:
    booksanity_feature = booksanity_by_option.get(booksanity_option)

    if booksanity_feature is None:
        raise ValueError(f"No booksanity feature mapped to {str(booksanity_option.value)}")

    return booksanity_feature


cropsanity_by_option = {
    options.Cropsanity.option_disabled: cropsanity.CropsanityDisabled(),
    options.Cropsanity.option_enabled: cropsanity.CropsanityEnabled(),
}


def choose_cropsanity(cropsanity_option: options.Cropsanity) -> cropsanity.CropsanityFeature:
    cropsanity_feature = cropsanity_by_option.get(cropsanity_option)

    if cropsanity_feature is None:
        raise ValueError(f"No cropsanity feature mapped to {str(cropsanity_option.value)}")

    return cropsanity_feature


fishsanity_by_option = {
    options.Fishsanity.option_none: fishsanity.FishsanityNone(),
    options.Fishsanity.option_legendaries: fishsanity.FishsanityLegendaries(),
    options.Fishsanity.option_special: fishsanity.FishsanitySpecial(),
    options.Fishsanity.option_randomized: fishsanity.FishsanityAll(randomization_ratio=0.4),
    options.Fishsanity.option_all: fishsanity.FishsanityAll(),
    options.Fishsanity.option_exclude_legendaries: fishsanity.FishsanityExcludeLegendaries(),
    options.Fishsanity.option_exclude_hard_fish: fishsanity.FishsanityExcludeHardFish(),
    options.Fishsanity.option_only_easy_fish: fishsanity.FishsanityOnlyEasyFish(),
}


def choose_fishsanity(fishsanity_option: options.Fishsanity) -> fishsanity.FishsanityFeature:
    fishsanity_feature = fishsanity_by_option.get(fishsanity_option)

    if fishsanity_feature is None:
        raise ValueError(f"No fishsanity feature mapped to {str(fishsanity_option.value)}")

    return fishsanity_feature


def choose_friendsanity(friendsanity_option: options.Friendsanity, heart_size: options.FriendsanityHeartSize) -> friendsanity.FriendsanityFeature:
    if friendsanity_option == options.Friendsanity.option_none:
        return friendsanity.FriendsanityNone()

    if friendsanity_option == options.Friendsanity.option_bachelors:
        return friendsanity.FriendsanityBachelors(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_starting_npcs:
        return friendsanity.FriendsanityStartingNpc(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_all:
        return friendsanity.FriendsanityAll(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_all_with_marriage:
        return friendsanity.FriendsanityAllWithMarriage(heart_size.value)

    raise ValueError(f"No friendsanity feature mapped to {str(friendsanity_option.value)}")


skill_progression_by_option = {
    options.SkillProgression.option_vanilla: skill_progression.SkillProgressionVanilla(),
    options.SkillProgression.option_progressive: skill_progression.SkillProgressionProgressive(),
    options.SkillProgression.option_progressive_with_masteries: skill_progression.SkillProgressionProgressiveWithMasteries(),
}


def choose_skill_progression(skill_progression_option: options.SkillProgression) -> skill_progression.SkillProgressionFeature:
    skill_progression_feature = skill_progression_by_option.get(skill_progression_option)

    if skill_progression_feature is None:
        raise ValueError(f"No skill progression feature mapped to {str(skill_progression_option.value)}")

    return skill_progression_feature
