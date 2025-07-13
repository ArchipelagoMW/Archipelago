from random import Random

from . import options as stardew_options
from .content import StardewContent
from .strings.ap_names.ap_weapon_names import APWeapon
from .strings.ap_names.transport_names import Transportation
from .strings.building_names import Building
from .strings.region_names import Region
from .strings.season_names import Season
from .strings.skill_names import Skill
from .strings.tv_channel_names import Channel
from .strings.wallet_item_names import Wallet

early_candidate_rate = 4
always_early_candidates = [Region.greenhouse, Transportation.desert_obelisk, Wallet.rusty_key]
seasons = [Season.spring, Season.summer, Season.fall, Season.winter]


def setup_early_items(multiworld, options: stardew_options.StardewValleyOptions, content: StardewContent, player: int, random: Random):
    early_forced = []
    early_candidates = []
    early_candidates.extend(always_early_candidates)

    add_seasonal_candidates(early_candidates, options)

    if content.features.building_progression.is_progressive:
        early_forced.append(Building.shipping_bin)
        if Building.coop not in content.features.building_progression.starting_buildings:
            early_candidates.append("Progressive Coop")
        early_candidates.append("Progressive Barn")

    if options.backpack_progression == stardew_options.BackpackProgression.option_early_progressive:
        early_forced.append("Progressive Backpack")

    if content.features.tool_progression.is_progressive:
        if content.features.fishsanity.is_enabled:
            early_candidates.append("Progressive Fishing Rod")
        early_forced.append("Progressive Pickaxe")

    fishing = content.skills.get(Skill.fishing)
    if fishing is not None and content.features.skill_progression.is_progressive:
        early_forced.append(fishing.level_name)

    if options.quest_locations.has_story_quests():
        early_candidates.append(Wallet.magnifying_glass)

    if options.special_order_locations & stardew_options.SpecialOrderLocations.option_board:
        early_candidates.append("Special Order Board")

    if options.cooksanity != stardew_options.Cooksanity.option_none or options.chefsanity & stardew_options.Chefsanity.option_queen_of_sauce:
        early_candidates.append(Channel.queen_of_sauce)

    if options.craftsanity != stardew_options.Craftsanity.option_none:
        early_candidates.append("Furnace Recipe")

    if options.monstersanity == stardew_options.Monstersanity.option_none:
        early_candidates.append(APWeapon.weapon)
    else:
        early_candidates.append(APWeapon.sword)

    if options.exclude_ginger_island == stardew_options.ExcludeGingerIsland.option_false:
        early_candidates.append(Transportation.island_obelisk)

        if options.walnutsanity.value:
            early_candidates.append("Island North Turtle")
            early_candidates.append("Island West Turtle")

    if options.museumsanity != stardew_options.Museumsanity.option_none or options.shipsanity >= stardew_options.Shipsanity.option_full_shipment:
        early_candidates.append(Wallet.metal_detector)

    early_forced.extend(random.sample(early_candidates, len(early_candidates) // early_candidate_rate))

    for item_name in early_forced:
        if item_name in multiworld.early_items[player]:
            continue
        multiworld.early_items[player][item_name] = 1


def add_seasonal_candidates(early_candidates, options):
    if options.season_randomization == stardew_options.SeasonRandomization.option_progressive:
        early_candidates.extend([Season.progressive] * 3)
        return
    if options.season_randomization == stardew_options.SeasonRandomization.option_disabled:
        return

    early_candidates.extend(seasons)
