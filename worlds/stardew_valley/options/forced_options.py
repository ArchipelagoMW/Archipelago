import logging

import Options as ap_options
from . import options
from .jojapocalypse_options import Jojapocalypse, JojaAreYouSure
from ..mods.mod_data import ModNames, mod_combination_is_valid, get_invalid_mod_combination
from ..options.settings import StardewSettings
from ..strings.ap_names.ap_option_names import EatsanityOptionName, HatsanityOptionName

logger = logging.getLogger(__name__)


def prevent_illegal_mod_combinations(world_options: options.StardewValleyOptions, player: int, player_name: str):
    if not mod_combination_is_valid(world_options.mods):
        invalid_mod_combination = get_invalid_mod_combination(world_options.mods)
        message = f"The combination of mods '{invalid_mod_combination}' cannot be used together. Generation Aborted."
        logger.error(message)
        raise ap_options.OptionError(message)


def force_change_options_if_banned(world_options: options.StardewValleyOptions, settings: StardewSettings, player: int, player_name: str) -> None:
    message_template = f"for Player {player} [{player_name}] disallowed from host.yaml."
    if not settings.allow_allsanity and world_options.goal == options.Goal.option_allsanity:
        message = f"Allsanity Goal {message_template} Generation Aborted."
        logger.error(message)
        raise ap_options.OptionError(message)
    if not settings.allow_perfection and world_options.goal == options.Goal.option_perfection:
        message = f"Perfection Goal {message_template} Generation Aborted."
        logger.error(message)
        raise ap_options.OptionError(message)
    if not settings.allow_max_bundles and world_options.bundle_price == options.BundlePrice.option_maximum:
        world_options.bundle_price.value = options.BundlePrice.option_very_expensive
        message = f"Max Bundles Price {message_template} Replaced with 'Very Expensive'"
        logger.warning(message)
    if not settings.allow_chaos_er and world_options.entrance_randomization == options.EntranceRandomization.option_chaos:
        world_options.entrance_randomization.value = options.EntranceRandomization.option_buildings
        message = f"Chaos Entrance Randomization {message_template} Replaced with 'Buildings'"
        logger.warning(message)
    if not settings.allow_shipsanity_everything and world_options.shipsanity == options.Shipsanity.option_everything:
        world_options.shipsanity.value = options.Shipsanity.option_full_shipment_with_fish
        message = f"Shipsanity Everything {message_template} Replaced with 'Full Shipment With Fish'"
        logger.warning(message)
    if not settings.allow_hatsanity_perfection:
        removed_one = False
        if HatsanityOptionName.near_perfection in world_options.hatsanity.value:
            world_options.hatsanity.value.remove(HatsanityOptionName.near_perfection)
            removed_one = True
        if HatsanityOptionName.post_perfection in world_options.hatsanity.value:
            world_options.hatsanity.value.remove(HatsanityOptionName.post_perfection)
            removed_one = True
        if removed_one and HatsanityOptionName.difficult not in world_options.hatsanity.value:
            world_options.hatsanity.value.add(HatsanityOptionName.difficult)
            message = f"Hatsanity Near or Post Perfection {message_template} Hatsanity setting reduced."
            logger.warning(message)
    if not settings.allow_jojapocalypse and world_options.jojapocalypse >= options.Jojapocalypse.option_allowed:
        world_options.jojapocalypse.value = options.Jojapocalypse.option_disabled
        message = f"Jojapocalypse {message_template} Disabled."
        logger.warning(message)
    if not settings.allow_sve and ModNames.sve in options.Mods:
        world_options.mods.value.remove(ModNames.sve)
        message = f"Stardew Valley Expanded {message_template} Removed from Mods."
        logger.warning(message)
    prevent_illegal_mod_combinations(world_options, player, player_name)


def force_change_options_if_incompatible(world_options: options.StardewValleyOptions, player: int, player_name: str) -> None:
    force_no_jojapocalypse_without_being_sure(world_options, player, player_name)
    force_eatsanity_no_enzymes_if_no_other_eatsanity(world_options, player, player_name)
    force_hatsanity_when_goal_is_mad_hatter(world_options, player, player_name)
    force_eatsanity_when_goal_is_ultimate_foodie(world_options, player, player_name)
    force_ginger_island_inclusion_when_goal_is_ginger_island_related(world_options, player, player_name)
    force_walnutsanity_deactivation_when_ginger_island_is_excluded(world_options, player, player_name)
    force_qi_special_orders_deactivation_when_ginger_island_is_excluded(world_options, player, player_name)
    force_accessibility_to_full_when_goal_requires_all_locations(player, player_name, world_options)


def force_no_jojapocalypse_without_being_sure(world_options: options.StardewValleyOptions, player: int, player_name: str) -> None:
    has_jojapocalypse = world_options.jojapocalypse.value >= Jojapocalypse.option_allowed
    is_sure = world_options.joja_are_you_sure == JojaAreYouSure.option_true

    if has_jojapocalypse and not is_sure:
        world_options.jojapocalypse.value = Jojapocalypse.option_disabled
        logger.warning(f"Jojapocalypse requires affirmative consent to be enabled. "
                       f"Jojapocalypse option forced to '{world_options.jojapocalypse}' for player {player} ({player_name})")

    start_price = world_options.joja_start_price.value
    end_price = world_options.joja_end_price.value
    if end_price <= start_price:
        end_price = start_price + 1
        world_options.joja_end_price.value = end_price
        logger.warning(f"Jojapocalypse End price must be higher than the start price. "
                       f"Jojapocalypse End Price forced to '{world_options.joja_end_price}' for player {player} ({player_name})")


def force_eatsanity_no_enzymes_if_no_other_eatsanity(world_options: options.StardewValleyOptions, player: int, player_name: str) -> None:
    has_eatsanity_enzymes = EatsanityOptionName.lock_effects in world_options.eatsanity
    valid_eatsanity_locations_for_enzymes = [EatsanityOptionName.crops, EatsanityOptionName.fish, EatsanityOptionName.cooking]
    has_enough_eatsanity_locations_for_enzymes = any([option in world_options.eatsanity for option in valid_eatsanity_locations_for_enzymes])

    if has_eatsanity_enzymes and not has_enough_eatsanity_locations_for_enzymes:
        world_options.eatsanity.value.remove(EatsanityOptionName.lock_effects)
        logger.warning(f"Eatsanity 'Lock Effects' requires more eatsanity locations to be active. "
                       f"Eatsanity option forced to '{world_options.eatsanity}' for player {player} ({player_name})")


def force_hatsanity_when_goal_is_mad_hatter(world_options: options.StardewValleyOptions, player: int, player_name: str) -> None:
    if world_options.exclude_ginger_island.value and HatsanityOptionName.post_perfection in world_options.hatsanity:
        world_options.hatsanity.value.remove(HatsanityOptionName.post_perfection)
        logger.warning(f"Hatsanity '{HatsanityOptionName.post_perfection}' requires ginger island. "
                       f"'{HatsanityOptionName.post_perfection}' force-removed from Hatsanity")

    goal_is_mad_hatter = world_options.goal == options.Goal.option_mad_hatter
    hatsanity_is_disabled = world_options.hatsanity == options.Hatsanity.preset_none

    if goal_is_mad_hatter and hatsanity_is_disabled:
        world_options.hatsanity.value = options.Hatsanity.preset_simple
        goal_name = world_options.goal.current_option_name
        logger.warning(f"Goal '{goal_name}' requires Hatsanity. "
                       f"Hatsanity option forced to 'Easy+Tailoring' for player {player} ({player_name})")


def force_eatsanity_when_goal_is_ultimate_foodie(world_options: options.StardewValleyOptions, player: int, player_name: str) -> None:
    goal_is_foodie = world_options.goal == options.Goal.option_ultimate_foodie
    eatsanity_options_that_dont_add_locations = [EatsanityOptionName.lock_effects, EatsanityOptionName.poisonous]
    eatsanity_options_that_add_locations = options.Eatsanity.preset_all.difference(eatsanity_options_that_dont_add_locations)
    eatsanity_relevant_values = world_options.eatsanity.value.difference(eatsanity_options_that_dont_add_locations)
    eatsanity_is_disabled = len(eatsanity_relevant_values) <= 0

    if goal_is_foodie and eatsanity_is_disabled:
        world_options.eatsanity.value = world_options.eatsanity.value.union(eatsanity_options_that_add_locations)
        goal_name = world_options.goal.current_option_name
        logger.warning(f"Goal '{goal_name}' requires Eatsanity. "
                       f"Eatsanity option forced to 'All' for player {player} ({player_name})")


def force_ginger_island_inclusion_when_goal_is_ginger_island_related(world_options: options.StardewValleyOptions, player: int, player_name: str) -> None:
    goal_is_walnut_hunter = world_options.goal == options.Goal.option_greatest_walnut_hunter
    goal_is_perfection = world_options.goal == options.Goal.option_perfection
    goal_is_island_related = goal_is_walnut_hunter or goal_is_perfection
    ginger_island_is_excluded = world_options.exclude_ginger_island == options.ExcludeGingerIsland.option_true

    if goal_is_island_related and ginger_island_is_excluded:
        world_options.exclude_ginger_island.value = options.ExcludeGingerIsland.option_false
        goal_name = world_options.goal.current_option_name
        logger.warning(f"Goal '{goal_name}' requires Ginger Island. "
                       f"Exclude Ginger Island option forced to 'False' for player {player} ({player_name})")


def force_walnutsanity_deactivation_when_ginger_island_is_excluded(world_options: options.StardewValleyOptions, player: int, player_name: str):
    ginger_island_is_excluded = world_options.exclude_ginger_island == options.ExcludeGingerIsland.option_true
    walnutsanity_is_active = world_options.walnutsanity != options.Walnutsanity.preset_none

    if ginger_island_is_excluded and walnutsanity_is_active:
        world_options.walnutsanity.value = options.Walnutsanity.preset_none
        logger.warning(f"Walnutsanity requires Ginger Island. "
                       f"Ginger Island was excluded from {player} ({player_name})'s world, so walnutsanity was force disabled")


def force_qi_special_orders_deactivation_when_ginger_island_is_excluded(world_options: options.StardewValleyOptions, player: int, player_name: str):
    ginger_island_is_excluded = world_options.exclude_ginger_island == options.ExcludeGingerIsland.option_true
    qi_board_is_active = world_options.special_order_locations.value & options.SpecialOrderLocations.value_qi

    if ginger_island_is_excluded and qi_board_is_active:
        original_option_name = world_options.special_order_locations.current_option_name
        world_options.special_order_locations.value -= options.SpecialOrderLocations.value_qi
        logger.warning(f"Mr. Qi's Special Orders requires Ginger Island. "
                       f"Ginger Island was excluded from {player} ({player_name})'s world, so Special Order Locations was changed from {original_option_name} to {world_options.special_order_locations.current_option_name}")


def force_accessibility_to_full_when_goal_requires_all_locations(player, player_name, world_options):
    goal_is_allsanity = world_options.goal == options.Goal.option_allsanity
    goal_is_perfection = world_options.goal == options.Goal.option_perfection
    goal_requires_all_locations = goal_is_allsanity or goal_is_perfection
    accessibility_is_minimal = world_options.accessibility == ap_options.Accessibility.option_minimal

    if goal_requires_all_locations and accessibility_is_minimal:
        world_options.accessibility.value = ap_options.Accessibility.option_full
        goal_name = world_options.goal.current_option_name
        logger.warning(f"Goal '{goal_name}' requires full accessibility. "
                       f"Accessibility option forced to 'Full' for player {player} ({player_name})")
