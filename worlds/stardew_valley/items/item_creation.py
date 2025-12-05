import logging
from random import Random
from typing import List

from BaseClasses import Item, ItemClassification
from .fillers import generate_resource_packs_and_traps, generate_unique_filler_items
from .filters import remove_excluded
from .item_data import StardewItemFactory, items_by_group, Group, item_table, ItemData
from ..content.feature import friendsanity
from ..content.game_content import StardewContent
from ..content.vanilla.ginger_island import ginger_island_content_pack
from ..content.vanilla.qi_board import qi_board_content_pack
from ..data.game_item import ItemTag
from ..mods.mod_data import ModNames
from ..options import StardewValleyOptions, FestivalLocations, SpecialOrderLocations, SeasonRandomization, Museumsanity, \
    ElevatorProgression, BackpackProgression, ArcadeMachineLocations, Monstersanity, Goal, \
    Chefsanity, Craftsanity, BundleRandomization, EntranceRandomization, Shipsanity, Walnutsanity, Moviesanity
from ..options.options import IncludeEndgameLocations, Friendsanity
from ..strings.ap_names.ap_option_names import WalnutsanityOptionName, SecretsanityOptionName, EatsanityOptionName, ChefsanityOptionName, StartWithoutOptionName
from ..strings.ap_names.ap_weapon_names import APWeapon
from ..strings.ap_names.buff_names import Buff
from ..strings.ap_names.community_upgrade_names import CommunityUpgrade, Bookseller
from ..strings.ap_names.mods.mod_items import SVEQuestItem
from ..strings.backpack_tiers import Backpack
from ..strings.building_names import Building
from ..strings.currency_names import Currency
from ..strings.tool_names import Tool
from ..strings.wallet_item_names import Wallet

logger = logging.getLogger(__name__)


def create_items(item_factory: StardewItemFactory, locations_count: int, items_to_exclude: List[Item],
                 options: StardewValleyOptions, content: StardewContent, random: Random) -> List[Item]:
    items = []
    unique_items = create_unique_items(item_factory, options, content, random)

    remove_items(items_to_exclude, unique_items)

    remove_items_if_no_room_for_them(unique_items, locations_count, random)

    items += unique_items
    logger.debug(f"Created {len(unique_items)} unique items")

    unique_filler_items = generate_unique_filler_items(item_factory, content, options, random, locations_count - len(items))
    items += unique_filler_items
    logger.debug(f"Created {len(unique_filler_items)} unique filler items")

    resource_pack_items = generate_resource_packs_and_traps(item_factory, options, content, random, items + items_to_exclude, locations_count - len(items))
    items += resource_pack_items
    logger.debug(f"Created {len(resource_pack_items)} resource packs")

    return items


def remove_items(items_to_remove: List[Item], items: List[Item]):
    for item_to_remove in items_to_remove:
        for i, item_candidate in enumerate(items):
            if item_to_remove != item_candidate:
                continue
            if item_to_remove.classification == item_candidate.classification and item_to_remove.advancement == item_candidate.advancement:
                items.pop(i)
                break


def remove_items_if_no_room_for_them(unique_items: List[Item], locations_count: int, random: Random):
    if len(unique_items) <= locations_count:
        return

    number_of_items_to_remove = len(unique_items) - locations_count
    removable_items = [item for item in unique_items if item.classification == ItemClassification.filler or item.classification == ItemClassification.trap]
    if len(removable_items) < number_of_items_to_remove:
        logger.debug(f"Player has more items than locations, trying to remove {number_of_items_to_remove} random non-progression items")
        removable_items = [item for item in unique_items if not item.classification & ItemClassification.progression]
    else:
        logger.debug(f"Player has more items than locations, trying to remove {number_of_items_to_remove} random filler items")
    count = len(unique_items)
    assert len(removable_items) >= number_of_items_to_remove, \
        f"There should be at least as many locations [{locations_count}] as there are mandatory items [{count - len(removable_items)}]"
    items_to_remove = random.sample(removable_items, number_of_items_to_remove)
    remove_items(items_to_remove, unique_items)


def create_unique_items(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, random: Random) -> List[Item]:
    items = []

    items.extend(item_factory(item) for item in items_by_group[Group.COMMUNITY_REWARD])
    items.append(item_factory(CommunityUpgrade.movie_theater))  # It is a community reward, but we need two of them
    create_raccoons(item_factory, options, items)
    items.append(item_factory(Wallet.metal_detector))  # Always offer at least one metal detector

    create_backpack_items(item_factory, options, content, items)
    create_weapons(item_factory, options, content, items)
    items.append(item_factory("Skull Key"))
    create_elevators(item_factory, options, content, items)
    create_tools(item_factory, content, items)
    create_skills(item_factory, content, items)
    create_wizard_buildings(item_factory, options, content, items)
    create_carpenter_buildings(item_factory, options, content, items)
    items.append(item_factory("Railroad Boulder Removed"))
    items.append(item_factory(CommunityUpgrade.fruit_bats))
    items.append(item_factory(CommunityUpgrade.mushroom_boxes))
    items.append(item_factory("Beach Bridge"))
    create_tv_channels(item_factory, options, items)
    create_quest_rewards(item_factory, options, content, items)
    create_stardrops(item_factory, options, content, items)
    create_museum_items(item_factory, options, items)
    create_arcade_machine_items(item_factory, options, items)
    create_movement_buffs(item_factory, options, items)
    create_traveling_merchant_items(item_factory, items)
    items.append(item_factory("Return Scepter"))
    create_seasons(item_factory, options, items)
    create_seeds(item_factory, content, items)
    create_friendsanity_items(item_factory, options, content, items, random)
    create_festival_rewards(item_factory, options, items)
    create_special_order_board_rewards(item_factory, options, items)
    create_special_order_qi_rewards(item_factory, options, content, items)
    create_walnuts(item_factory, options, content, items)
    create_walnut_purchase_rewards(item_factory, content, items)
    create_crafting_recipes(item_factory, options, content, items)
    create_cooking_recipes(item_factory, options, content, items)
    create_shipsanity_items(item_factory, options, items)
    create_booksanity_items(item_factory, options, content, items)
    create_movie_items(item_factory, options, items)
    create_secrets_items(item_factory, content, options, items)
    create_eatsanity_enzyme_items(item_factory, options, items)
    create_endgame_locations_items(item_factory, options, items)

    create_goal_items(item_factory, options, items)
    items.append(item_factory("Golden Egg"))
    items.append(item_factory(CommunityUpgrade.mr_qi_plane_ride))

    items.append(item_factory(Wallet.mens_locker_key))
    items.append(item_factory(Wallet.womens_locker_key))

    create_sve_special_items(item_factory, content, items)
    create_magic_mod_spells(item_factory, content, items)
    create_deepwoods_pendants(item_factory, content, items)
    create_archaeology_items(item_factory, content, items)

    return items


def create_raccoons(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    number_progressive_raccoons = 9
    if options.bundle_per_room.value < 0:
        number_progressive_raccoons -= options.bundle_per_room.value
    if options.quest_locations.has_no_story_quests():
        number_progressive_raccoons = number_progressive_raccoons - 1

    items.extend(item_factory(item) for item in [CommunityUpgrade.raccoon] * number_progressive_raccoons)


def create_backpack_items(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    if options.backpack_progression == BackpackProgression.option_vanilla:
        return
    num_per_tier = options.backpack_size.count_per_tier()
    backpack_tier_names = Backpack.get_purchasable_tiers(ModNames.big_backpack in content.registered_packs, StartWithoutOptionName.backpack in options.start_without)
    num_backpacks = len(backpack_tier_names) * num_per_tier

    items.extend(item_factory(item) for item in ["Progressive Backpack"] * num_backpacks)


def create_footwear(item_factory: StardewItemFactory, number: int) -> List[Item]:
    return [item_factory(APWeapon.footwear) for _ in range(number)]


def create_weapons(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    weapons = weapons_count(content)
    items.extend(item_factory(item) for item in [APWeapon.slingshot] * 2)
    monstersanity = options.monstersanity

    ring_classification = ItemClassification.progression if options.bundle_randomization == BundleRandomization.option_meme else ItemClassification.useful
    rings_items = [item for item in items_by_group[Group.FILLER_RING] if item.classification is not ItemClassification.filler]

    if monstersanity == Monstersanity.option_none:  # Without monstersanity, might not be enough checks to split the weapons
        items.extend(item_factory(item) for item in [APWeapon.weapon] * weapons)
        items.extend(create_footwear(item_factory, 3))  # 1-2 | 3-4 | 6-7-8
        rings_items = [item for item in rings_items if item.classification is ItemClassification.progression]
        items.extend(item_factory(item, classification_pre_fill=ring_classification) for item in rings_items)
        return

    items.extend(item_factory(item) for item in [APWeapon.sword] * weapons)
    items.extend(item_factory(item) for item in [APWeapon.club] * weapons)
    items.extend(item_factory(item) for item in [APWeapon.dagger] * weapons)
    items.extend(create_footwear(item_factory, 4))  # 1-2 | 3-4 | 6-7-8 | 11-13

    items.extend(item_factory(item, classification_pre_fill=ring_classification) for item in rings_items)
    if monstersanity == Monstersanity.option_goals or monstersanity == Monstersanity.option_one_per_category or \
            monstersanity == Monstersanity.option_short_goals or monstersanity == Monstersanity.option_very_short_goals:
        return


def create_elevators(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    if options.elevator_progression == ElevatorProgression.option_vanilla:
        return

    items.extend([item_factory(item) for item in ["Progressive Mine Elevator"] * 24])
    if ModNames.deepwoods in content.registered_packs:
        items.extend([item_factory(item) for item in ["Progressive Woods Obelisk Sigils"] * 10])
    if ModNames.skull_cavern_elevator in content.registered_packs:
        items.extend([item_factory(item) for item in ["Progressive Skull Cavern Elevator"] * 8])


def create_tools(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    tool_progression = content.features.tool_progression
    for tool, count in tool_progression.tool_distribution.items():
        item = item_table[tool_progression.to_progressive_item_name(tool)]

        # Trash can is only used in tool upgrade logic, so the last trash can is not progression because it basically does not unlock anything.
        if tool == Tool.trash_can:
            count -= 1
            items.append(item_factory(item,
                                      classification_pre_fill=ItemClassification.useful,
                                      classification_post_fill=ItemClassification.progression_skip_balancing))

        items.extend([item_factory(item) for _ in range(count)])


def create_skills(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    skill_progression = content.features.skill_progression
    if not skill_progression.is_progressive:
        return

    for skill in content.skills.values():
        items.extend(item_factory(skill.level_name) for _ in skill_progression.get_randomized_level_names_by_level(skill))

        if skill_progression.is_mastery_randomized(skill):
            items.append(item_factory(skill.mastery_name))

    if skill_progression.are_masteries_shuffled:
        items.append(item_factory(Wallet.mastery_of_the_five_ways))


def create_wizard_buildings(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    useful_buildings_classification = ItemClassification.progression_skip_balancing if goal_is_perfection(options) else ItemClassification.useful
    items.append(item_factory("Earth Obelisk", classification_pre_fill=useful_buildings_classification))
    items.append(item_factory("Water Obelisk", classification_pre_fill=useful_buildings_classification))
    items.append(item_factory("Desert Obelisk"))
    items.append(item_factory("Junimo Hut"))
    items.append(item_factory("Gold Clock", classification_pre_fill=useful_buildings_classification))
    if content.is_enabled(ginger_island_content_pack):
        items.append(item_factory("Island Obelisk"))
    if content.is_enabled(ModNames.deepwoods):
        items.append(item_factory("Woods Obelisk"))


def create_carpenter_buildings(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    building_progression = content.features.building_progression
    if not building_progression.is_progressive:
        return

    for building in content.farm_buildings.values():
        item_name, _ = building_progression.to_progressive_item(building.name)
        if item_name in [Building.stable, Building.well] and options.bundle_randomization != BundleRandomization.option_meme:
            items.append(item_factory(item_name, classification_pre_fill=ItemClassification.useful))
        else:
            items.append(item_factory(item_name))


def create_quest_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    create_special_quest_rewards(item_factory, options, content, items)
    create_help_wanted_quest_rewards(item_factory, options, items)

    create_quest_rewards_sve(item_factory, options, content, items)


def create_special_quest_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    if options.quest_locations.has_no_story_quests():
        return
    # items.append(item_factory("Adventurer's Guild")) # Now unlocked always!
    items.append(item_factory(Wallet.club_card))
    items.append(item_factory(Wallet.magnifying_glass))
    items.append(item_factory(Wallet.magic_ink))
    items.append(item_factory(Wallet.iridium_snake_milk))
    if ModNames.sve in content.registered_packs:
        items.append(item_factory(Wallet.bears_knowledge))
    else:
        items.append(item_factory(Wallet.bears_knowledge, classification_pre_fill=ItemClassification.useful))  # Not necessary outside of SVE
    items.append(item_factory("Dark Talisman"))
    if content.is_enabled(ginger_island_content_pack):
        items.append(item_factory("Fairy Dust Recipe"))


def create_help_wanted_quest_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.quest_locations <= 0:
        return

    number_help_wanted = options.quest_locations.value
    quest_per_prize_ticket = 3
    number_prize_tickets = number_help_wanted // quest_per_prize_ticket
    items.extend(item_factory(item) for item in [Currency.prize_ticket] * number_prize_tickets)


def create_stardrops(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    stardrops_classification = get_stardrop_classification(options)
    items.append(item_factory("Stardrop", classification_pre_fill=stardrops_classification))  # The Mines level 100
    items.append(item_factory("Stardrop", classification_pre_fill=stardrops_classification))  # Krobus Stardrop
    if content.features.fishsanity.is_enabled:
        items.append(item_factory("Stardrop", classification_pre_fill=stardrops_classification))  # Master Angler Stardrop
    if ModNames.deepwoods in content.registered_packs:
        items.append(item_factory("Stardrop", classification_pre_fill=stardrops_classification))  # Petting the Unicorn
    if content.features.friendsanity.is_enabled:
        items.append(item_factory("Stardrop", classification_pre_fill=stardrops_classification))  # Spouse Stardrop
    if SecretsanityOptionName.easy in options.secretsanity:
        # Always Progression as a different secret requires a stardrop
        items.append(item_factory("Stardrop", classification_pre_fill=ItemClassification.progression))  # Old Master Cannoli.


def create_museum_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    items.append(item_factory(Wallet.rusty_key))
    items.append(item_factory(Wallet.dwarvish_translation_guide))
    items.append(item_factory("Ancient Seeds Recipe"))
    items.append(item_factory("Stardrop", classification_pre_fill=get_stardrop_classification(options)))
    if options.museumsanity == Museumsanity.option_none:
        return
    items.extend(item_factory(item) for item in ["Magic Rock Candy"] * 10)
    items.extend(item_factory(item) for item in ["Ancient Seeds"] * 5)
    items.append(item_factory(Wallet.metal_detector))


def create_friendsanity_items(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item], random: Random):
    if not content.features.friendsanity.is_enabled:
        return

    create_babies(item_factory, items, random)

    for villager in content.villagers.values():
        item_name = friendsanity.to_item_name(villager.name)

        for _ in content.features.friendsanity.get_randomized_hearts(villager):
            items.append(item_factory(item_name))

    need_pet = options.goal == Goal.option_grandpa_evaluation
    pet_item_classification = ItemClassification.progression_skip_balancing if need_pet else ItemClassification.useful

    for _ in content.features.friendsanity.get_pet_randomized_hearts():
        items.append(item_factory(friendsanity.pet_heart_item_name, classification_pre_fill=pet_item_classification))


def create_babies(item_factory: StardewItemFactory, items: List[Item], random: Random):
    baby_items = [item for item in items_by_group[Group.BABY]]
    for i in range(2):
        chosen_baby = random.choice(baby_items)
        items.append(item_factory(chosen_baby))


def create_arcade_machine_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.arcade_machine_locations == ArcadeMachineLocations.option_full_shuffling:
        items.append(item_factory("JotPK: Progressive Boots"))
        items.append(item_factory("JotPK: Progressive Boots"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Extra Life"))
        items.append(item_factory("JotPK: Extra Life"))
        items.append(item_factory("JotPK: Increased Drop Rate"))
        items.extend(item_factory(item) for item in ["Junimo Kart: Extra Life"] * 8)


def create_movement_buffs(item_factory, options: StardewValleyOptions, items: List[Item]):
    movement_buffs: int = options.movement_buff_number.value
    items.extend(item_factory(item) for item in [Buff.movement] * movement_buffs)


def create_traveling_merchant_items(item_factory: StardewItemFactory, items: List[Item]):
    items.extend([*(item_factory(item) for item in items_by_group[Group.TRAVELING_MERCHANT_DAY]),
                  *(item_factory(item) for item in ["Traveling Merchant Stock Size"] * 6)])


def create_seasons(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.season_randomization == SeasonRandomization.option_disabled:
        return

    if options.season_randomization == SeasonRandomization.option_progressive:
        items.extend([item_factory(item) for item in ["Progressive Season"] * 3])
        return

    items.extend([item_factory(item) for item in items_by_group[Group.SEASON]])


def create_seeds(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    if not content.features.cropsanity.is_enabled:
        return

    items.extend(item_factory(item_table[seed.name]) for seed in content.find_tagged_items(ItemTag.CROPSANITY_SEED))


def create_festival_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    items.append(item_factory("Deluxe Scarecrow Recipe"))
    if options.festival_locations == FestivalLocations.option_disabled:
        return

    festival_rewards = [item_factory(item) for item in items_by_group[Group.FESTIVAL] if item.classification != ItemClassification.filler]
    items.extend([*festival_rewards, item_factory("Stardrop", classification_pre_fill=get_stardrop_classification(options))])


def create_walnuts(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    walnutsanity = options.walnutsanity
    if not content.is_enabled(ginger_island_content_pack) or walnutsanity == Walnutsanity.preset_none:
        return

    # Give baseline walnuts just to be nice
    num_single_walnuts = 0
    num_triple_walnuts = 2
    num_penta_walnuts = 1
    # https://stardewvalleywiki.com/Golden_Walnut
    # Totals should be accurate, but distribution is slightly offset to make room for baseline walnuts
    if WalnutsanityOptionName.puzzles in walnutsanity:  # 61
        num_single_walnuts += 6  # 6
        num_triple_walnuts += 5  # 15
        num_penta_walnuts += 8  # 40
    if WalnutsanityOptionName.bushes in walnutsanity:  # 25
        num_single_walnuts += 16  # 16
        num_triple_walnuts += 3  # 9
    if WalnutsanityOptionName.dig_spots in walnutsanity:  # 18
        num_single_walnuts += 18  # 18
    if WalnutsanityOptionName.repeatables in walnutsanity:  # 33
        num_single_walnuts += 30  # 30
        num_triple_walnuts += 1  # 3

    items.extend([item_factory(item) for item in ["Golden Walnut"] * num_single_walnuts])
    items.extend([item_factory(item) for item in ["3 Golden Walnuts"] * num_triple_walnuts])
    items.extend([item_factory(item) for item in ["5 Golden Walnuts"] * num_penta_walnuts])


def create_walnut_purchase_rewards(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    if not content.is_enabled(ginger_island_content_pack):
        return

    items.extend([item_factory("Boat Repair"),
                  item_factory("Open Professor Snail Cave"),
                  item_factory("Ostrich Incubator Recipe"),
                  item_factory("Treehouse"),
                  *[item_factory(item) for item in items_by_group[Group.WALNUT_PURCHASE]]])


def create_special_order_board_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.special_order_locations & SpecialOrderLocations.option_board:
        special_order_board_items = [item for item in items_by_group[Group.SPECIAL_ORDER_BOARD]]
        items.extend([item_factory(item) for item in special_order_board_items])


def special_order_board_item_classification(item: ItemData, need_all_recipes: bool) -> ItemClassification:
    if item.classification is ItemClassification.useful:
        return ItemClassification.useful
    if item.name == "Special Order Board":
        return ItemClassification.progression
    if need_all_recipes and "Recipe" in item.name:
        return ItemClassification.progression_skip_balancing
    if item.name == "Monster Musk Recipe":
        return ItemClassification.progression_skip_balancing
    return ItemClassification.useful


def create_special_order_qi_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    if not content.is_enabled(ginger_island_content_pack):
        return
    qi_gem_rewards = []
    if options.bundle_randomization >= BundleRandomization.option_remixed:
        qi_gem_rewards.append("15 Qi Gems")
        qi_gem_rewards.append("15 Qi Gems")

    if content.is_enabled(qi_board_content_pack):
        qi_gem_rewards.extend(["100 Qi Gems", "10 Qi Gems", "40 Qi Gems", "25 Qi Gems", "25 Qi Gems",
                               "40 Qi Gems", "20 Qi Gems", "50 Qi Gems", "40 Qi Gems", "35 Qi Gems"])

    qi_gem_items = [item_factory(reward) for reward in qi_gem_rewards]
    items.extend(qi_gem_items)


def create_tv_channels(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    channels = [channel for channel in items_by_group[Group.TV_CHANNEL]]
    if options.entrance_randomization == EntranceRandomization.option_disabled:
        channels = [channel for channel in channels if channel.name != "The Gateway Gazette"]
    items.extend([item_factory(item) for item in channels])


def create_crafting_recipes(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    has_craftsanity = options.craftsanity == Craftsanity.option_all
    crafting_recipes = []
    crafting_recipes.extend([recipe for recipe in items_by_group[Group.QI_CRAFTING_RECIPE]])
    if has_craftsanity:
        crafting_recipes.extend([recipe for recipe in items_by_group[Group.CRAFTSANITY]])
    crafting_recipes = remove_excluded(crafting_recipes, content, options)
    items.extend([item_factory(item) for item in crafting_recipes])


def create_cooking_recipes(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    chefsanity = options.chefsanity
    if chefsanity == Chefsanity.preset_none:
        return

    chefsanity_recipes_by_name = {recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_STARTER]}  # Dictionary to not make duplicates

    if ChefsanityOptionName.queen_of_sauce in chefsanity:
        chefsanity_recipes_by_name.update({recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_QOS]})
    if ChefsanityOptionName.purchases in chefsanity:
        chefsanity_recipes_by_name.update({recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_PURCHASE]})
    if ChefsanityOptionName.friendship in chefsanity:
        chefsanity_recipes_by_name.update({recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_FRIENDSHIP]})
    if ChefsanityOptionName.skills in chefsanity:
        chefsanity_recipes_by_name.update({recipe.name: recipe for recipe in items_by_group[Group.CHEFSANITY_SKILL]})

    filtered_chefsanity_recipes = remove_excluded(list(chefsanity_recipes_by_name.values()), content, options)
    items.extend([item_factory(item) for item in filtered_chefsanity_recipes])


def create_shipsanity_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    shipsanity = options.shipsanity
    if shipsanity != Shipsanity.option_everything:
        return

    items.append(item_factory(Wallet.metal_detector))


def create_booksanity_items(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    create_bookseller_items(item_factory, options, content, items)
    booksanity = content.features.booksanity
    if not booksanity.is_enabled:
        return

    items.extend(item_factory(item_table[booksanity.to_item_name(book.name)]) for book in content.find_tagged_items(ItemTag.BOOK_POWER))
    progressive_lost_book = item_table[booksanity.progressive_lost_book]
    # We do -1 here because the first lost book spawns freely in the museum
    num_lost_books = len([book for book in content.features.booksanity.get_randomized_lost_books()]) - 1
    items.extend(item_factory(progressive_lost_book) for _ in range(num_lost_books))


def create_bookseller_items(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    needs_books = options.shipsanity == Shipsanity.option_everything or content.features.booksanity.is_enabled or content.features.hatsanity.is_enabled
    book_items = []
    book_items.extend(item_factory(item_table[Bookseller.days]) for _ in range(4 if needs_books else 1))
    if not needs_books:
        book_items.extend(item_factory(item_table[Bookseller.days], classification_pre_fill=ItemClassification.filler) for _ in range(3))
    book_items.extend(item_factory(item_table[Bookseller.stock_rare_books]) for _ in range(2 if needs_books else 1))
    book_items.append(item_factory(item_table[Bookseller.stock_permanent_books]))
    book_items.append(item_factory(item_table[Bookseller.stock_experience_books]))
    if needs_books:
        book_items.extend(item_factory(item_table[Bookseller.stock_experience_books], classification_pre_fill=ItemClassification.filler) for _ in range(2))

    items.extend(book_items)


def create_movie_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.moviesanity.value < Moviesanity.option_all_movies:
        return

    items.extend(item_factory(item) for item in items_by_group[Group.MOVIESANITY])


def create_secrets_items(item_factory: StardewItemFactory, content: StardewContent, options: StardewValleyOptions, items: List[Item]):
    if not options.secretsanity:
        return
    secret_items = []
    if SecretsanityOptionName.easy in options.secretsanity:
        secret_items.extend(items_by_group[Group.EASY_SECRET])
    # if SecretsanityOptionName.fishing in options.secretsanity:
    #     secret_items.extend(items_by_group[Group.FISHING_SECRET]) # There are no longer any of these items, they are now part of FILLER_DECORATION
    # if SecretsanityOptionName.difficult in options.secretsanity:
    #     items.extend(item_factory(item) for item in items_by_group[Group.DIFFICULT_SECRET])
    if SecretsanityOptionName.secret_notes in options.secretsanity:
        secret_items.extend(items_by_group[Group.SECRET_NOTES_SECRET])
        if options.quest_locations.has_no_story_quests():
            secret_items.append(item_table[Wallet.club_card])
            secret_items.append(item_table[Wallet.iridium_snake_milk])
    filtered_secret_items = remove_excluded(list(secret_items), content, options)
    items.extend([item_factory(item) for item in filtered_secret_items])


def create_eatsanity_enzyme_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if EatsanityOptionName.lock_effects not in options.eatsanity:
        return

    # These items unlock progressively stronger ability to digest food items that give the associated buff
    # Upon receiving the enzyme, you also get a temporary buff of whatever the effect is
    # Stamina and Health items can go beyond their original max value, but the buffs cannot.
    items.extend(item_factory(item) for item in ["Stamina Enzyme"]*10)
    items.extend(item_factory(item) for item in ["Health Enzyme"]*10)
    items.extend(item_factory(item) for item in ["Speed Enzyme"]*5)
    items.extend(item_factory(item) for item in ["Luck Enzyme"]*5)
    items.extend(item_factory(item) for item in ["Farming Enzyme"]*5)
    items.extend(item_factory(item) for item in ["Foraging Enzyme"]*5)
    items.extend(item_factory(item) for item in ["Fishing Enzyme"]*5)
    items.extend(item_factory(item) for item in ["Mining Enzyme"]*5)
    items.extend(item_factory(item) for item in ["Magnetism Enzyme"]*2)
    items.extend(item_factory(item) for item in ["Defense Enzyme"]*5)
    items.extend(item_factory(item) for item in ["Attack Enzyme"]*5)
    items.extend(item_factory(item) for item in ["Max Stamina Enzyme"]*3)
    items.extend(item_factory(item) for item in ["Squid Ink Enzyme"])
    items.extend(item_factory(item) for item in ["Monster Musk Enzyme"])
    items.extend(item_factory(item) for item in ["Oil Of Garlic Enzyme"])
    items.extend(item_factory(item) for item in ["Tipsy Enzyme"])


def create_endgame_locations_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    if options.include_endgame_locations == IncludeEndgameLocations.option_false:
        return

    items_to_add = []
    items_to_add.extend(items_by_group[Group.ENDGAME_LOCATION_ITEMS])
    if options.friendsanity != Friendsanity.option_all_with_marriage:
        for portrait in items_by_group[Group.REQUIRES_FRIENDSANITY_MARRIAGE]:
            items_to_add.remove(portrait)
    items.extend(item_factory(item) for item in items_to_add)


def create_goal_items(item_factory: StardewItemFactory, options: StardewValleyOptions, items: List[Item]):
    goal = options.goal
    if goal != Goal.option_perfection and goal != Goal.option_complete_collection:
        return

    items.append(item_factory(Wallet.metal_detector))


def create_archaeology_items(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    if ModNames.archaeology not in content.registered_packs:
        return

    items.append(item_factory(Wallet.metal_detector))


def create_magic_mod_spells(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    if ModNames.magic not in content.registered_packs:
        return
    items.extend([item_factory(item) for item in items_by_group[Group.MAGIC_SPELL]])


def create_deepwoods_pendants(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    if ModNames.deepwoods not in content.registered_packs:
        return
    items.extend([item_factory(item) for item in ["Pendant of Elders", "Pendant of Community", "Pendant of Depths"]])


def create_sve_special_items(item_factory: StardewItemFactory, content: StardewContent, items: List[Item]):
    if ModNames.sve not in content.registered_packs:
        return

    items.extend([item_factory(item) for item in items_by_group[Group.MOD_WARP] if ModNames.sve in item.content_packs])


def create_quest_rewards_sve(item_factory: StardewItemFactory, options: StardewValleyOptions, content: StardewContent, items: List[Item]):
    if not content.is_enabled(ModNames.sve):
        return

    ginger_island_included = content.is_enabled(ginger_island_content_pack)
    items.extend([item_factory(item) for item in SVEQuestItem.sve_always_quest_items])
    if ginger_island_included:
        items.extend([item_factory(item) for item in SVEQuestItem.sve_always_quest_items_ginger_island])

    if options.quest_locations.has_no_story_quests():
        return

    items.extend([item_factory(item) for item in SVEQuestItem.sve_quest_items])
    if not ginger_island_included:
        return
    items.extend([item_factory(item) for item in SVEQuestItem.sve_quest_items_ginger_island])


def weapons_count(content: StardewContent):
    weapon_count = 5
    if ModNames.sve in content.registered_packs:
        weapon_count += 1
    return weapon_count


def get_stardrop_classification(options) -> ItemClassification:
    return ItemClassification.progression_skip_balancing \
        if goal_is_perfection(options) or goal_is_stardrops(options) or EatsanityOptionName.shop in options.eatsanity \
        else ItemClassification.useful


def goal_is_perfection(options) -> bool:
    return options.goal == Goal.option_perfection


def goal_is_stardrops(options) -> bool:
    return options.goal == Goal.option_mystery_of_the_stardrops
