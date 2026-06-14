from random import Random
from typing import List

from BaseClasses import Item, ItemClassification
from .filters import remove_excluded, remove_limited_amount_resource_packs, remove_already_included
from .item_data import items_by_group, Group, ItemData, StardewItemFactory, item_table
from ..content.game_content import StardewContent
from ..options import StardewValleyOptions, FestivalLocations
from ..strings.ap_names.ap_option_names import BuffOptionName, AllowedFillerOptionName
from ..strings.ap_names.buff_names import Buff

AllowedFillerTypesMap = {
    AllowedFillerOptionName.farming: Group.FILLER_FARMING,
    AllowedFillerOptionName.fishing: Group.FILLER_FISHING,
    AllowedFillerOptionName.fruit_trees: Group.FILLER_FRUIT_TREES,
    AllowedFillerOptionName.food: Group.FILLER_FOOD,
    AllowedFillerOptionName.buff_food: Group.FILLER_BUFF_FOOD,
    AllowedFillerOptionName.consumables: Group.FILLER_CONSUMABLE,
    AllowedFillerOptionName.machines: Group.FILLER_MACHINE,
    AllowedFillerOptionName.storage: Group.FILLER_STORAGE,
    AllowedFillerOptionName.quality_of_life: Group.FILLER_QUALITY_OF_LIFE,
    AllowedFillerOptionName.materials: Group.FILLER_MATERIALS,
    AllowedFillerOptionName.currencies: Group.FILLER_CURRENCY,
    AllowedFillerOptionName.money: Group.FILLER_MONEY,
    AllowedFillerOptionName.hats: Group.FILLER_HAT,
    AllowedFillerOptionName.decorations: Group.FILLER_DECORATION,
    AllowedFillerOptionName.rings: Group.FILLER_RING,
}


def generate_filler_choice_pool(options: StardewValleyOptions, content: StardewContent) -> list[str]:
    available_filler = get_all_filler_items(options)
    available_filler = remove_excluded(available_filler, content, options)
    available_filler = remove_limited_amount_resource_packs(available_filler)

    return [item.name for item in available_filler]


def get_all_filler_items(options: StardewValleyOptions) -> list[ItemData]:
    all_filler_items = []
    allowed_filler_types = sorted(list(options.allowed_filler_items.value))
    for allowed_filler_type in allowed_filler_types:
        allowed_filler_group = AllowedFillerTypesMap[allowed_filler_type]
        all_filler_items.extend([pack for pack in items_by_group[allowed_filler_group]])
    all_filler_items.extend(items_by_group[Group.TRASH])
    all_filler_items.extend(get_player_buffs(options))
    all_filler_items.extend(get_traps(options))

    return all_filler_items


def get_filler_weights(options: StardewValleyOptions, all_filler_packs: list[ItemData]) -> list[int]:
    weights = []
    for filler in all_filler_packs:
        if filler.name in options.trap_distribution:
            num = options.trap_distribution[filler.name]
        else:
            num = options.trap_distribution.default_weight
        weights.append(num)
    return weights


def generate_unique_filler_items(item_factory: StardewItemFactory, content: StardewContent, options: StardewValleyOptions, random: Random,
                                 available_item_slots: int) -> list[Item]:
    items = create_filler_festival_rewards(item_factory, content, options)

    if len(items) > available_item_slots:
        items = random.sample(items, available_item_slots)
    return items


def create_filler_festival_rewards(item_factory: StardewItemFactory, content: StardewContent, options: StardewValleyOptions) -> list[Item]:
    if options.festival_locations == FestivalLocations.option_disabled:
        return []
    filler_rewards = [item for item in items_by_group[Group.FESTIVAL] if item.classification == ItemClassification.filler]
    filler_rewards = remove_excluded(filler_rewards, content, options)
    return [item_factory(item) for item in filler_rewards]


def generate_resource_packs_and_traps(item_factory: StardewItemFactory,
                                      options: StardewValleyOptions,
                                      content: StardewContent,
                                      random: Random,
                                      already_added_items: list[Item],
                                      available_item_slots: int) -> list[Item]:
    def filler_factory(item: ItemData):
        # Yes some fillers are progression. We add multiple fruit tree saplings for instance.
        if ItemClassification.progression in item.classification:
            return item_factory(item,
                                classification_pre_fill=ItemClassification.filler,
                                classification_post_fill=ItemClassification.progression_skip_balancing)
        return item_factory(item)

    already_added_items_names = {item.name for item in already_added_items}

    priority_fillers = get_priority_fillers(options)
    priority_fillers = remove_excluded(priority_fillers, content, options)
    priority_fillers = remove_already_included(priority_fillers, already_added_items_names)

    if available_item_slots < len(priority_fillers):
        return [filler_factory(priority_filler)
                for priority_filler in random.sample(priority_fillers, available_item_slots)]

    chosen_fillers = []
    chosen_fillers.extend([filler_factory(priority_filler) for priority_filler in priority_fillers])
    available_item_slots -= len(priority_fillers)
    already_added_items_names |= {priority_item.name for priority_item in priority_fillers}

    all_fillers = get_all_filler_items(options)
    all_fillers = remove_excluded(all_fillers, content, options)
    all_fillers = remove_already_included(all_fillers, already_added_items_names)

    filler_weights = get_filler_weights(options, all_fillers)

    while available_item_slots > 0:
        resource_pack = random.choices(all_fillers, weights=filler_weights, k=1)[0]

        exactly_2 = Group.AT_LEAST_TWO in resource_pack.groups
        while exactly_2 and available_item_slots == 1:
            # We roll another filler since there is no place for the second one
            resource_pack = random.choices(all_fillers, weights=filler_weights, k=1)[0]
            exactly_2 = Group.AT_LEAST_TWO in resource_pack.groups

        chosen_fillers.append(filler_factory(resource_pack))
        available_item_slots -= 1
        if exactly_2:
            chosen_fillers.append(filler_factory(resource_pack))
            available_item_slots -= 1

        if resource_pack.has_limited_amount():
            index = all_fillers.index(resource_pack)
            all_fillers.pop(index)
            filler_weights.pop(index)

    return chosen_fillers


def get_priority_fillers(options: StardewValleyOptions) -> list[ItemData]:
    buffs = get_player_buffs(options)
    traps = get_traps(options)

    return buffs + traps


def get_player_buffs(options: StardewValleyOptions) -> List[ItemData]:
    buff_option = options.enabled_filler_buffs
    allowed_buffs = []
    if BuffOptionName.luck in buff_option:
        allowed_buffs.append(item_table[Buff.luck])
    if BuffOptionName.damage in buff_option:
        allowed_buffs.append(item_table[Buff.damage])
    if BuffOptionName.defense in buff_option:
        allowed_buffs.append(item_table[Buff.defense])
    if BuffOptionName.immunity in buff_option:
        allowed_buffs.append(item_table[Buff.immunity])
    if BuffOptionName.health in buff_option:
        allowed_buffs.append(item_table[Buff.health])
    if BuffOptionName.energy in buff_option:
        allowed_buffs.append(item_table[Buff.energy])
    if BuffOptionName.bite in buff_option:
        allowed_buffs.append(item_table[Buff.bite_rate])
    if BuffOptionName.fish_trap in buff_option:
        allowed_buffs.append(item_table[Buff.fish_trap])
    if BuffOptionName.fishing_bar in buff_option:
        allowed_buffs.append(item_table[Buff.fishing_bar])
    if BuffOptionName.quality in buff_option:
        allowed_buffs.append(item_table[Buff.quality])
    if BuffOptionName.glow in buff_option:
        allowed_buffs.append(item_table[Buff.glow])
    return allowed_buffs


def get_traps(options: StardewValleyOptions) -> list[ItemData]:
    if not options.trap_difficulty.include_traps():
        return []

    return [
        trap
        for trap in items_by_group[Group.TRAP]
        if trap.name not in options.trap_distribution or options.trap_distribution[trap.name] > 0
    ]
