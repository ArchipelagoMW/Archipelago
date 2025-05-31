from random import Random

from BaseClasses import Item, ItemClassification
from .filters import filter_excluded, filter_limited_amount_resource_packs, filter_already_included_maximum_one
from .item_data import items_by_group, Group, ItemData, StardewItemFactory, item_table
from ..options import StardewValleyOptions, FestivalLocations
from ..strings.ap_names.ap_option_names import BuffOptionName
from ..strings.ap_names.buff_names import Buff


def generate_filler_choice_pool(options: StardewValleyOptions) -> list[str]:
    available_filler = get_all_resource_packs_and_traps(options)
    available_filler = filter_excluded(available_filler, options)
    available_filler = filter_limited_amount_resource_packs(available_filler)

    return [item.name for item in available_filler]


def get_all_resource_packs_and_traps(options: StardewValleyOptions) -> list[ItemData]:
    all_filler_items = [pack for pack in items_by_group[Group.RESOURCE_PACK]]
    all_filler_items.extend(items_by_group[Group.TRASH])
    all_filler_items.extend(get_traps(options))

    return all_filler_items


def get_filler_weights(options: StardewValleyOptions, all_filler_packs: list[ItemData]) -> list[int]:
    weights = []
    for filler in all_filler_packs:
        if filler.name in options.trap_distribution:
            weights.append(options.trap_distribution[filler.name])
        else:
            weights.append(options.trap_distribution.default_weight)
    return weights


def generate_unique_filler_items(item_factory: StardewItemFactory, options: StardewValleyOptions, random: Random,
                                 available_item_slots: int) -> list[Item]:
    items = create_filler_festival_rewards(item_factory, options)

    if len(items) > available_item_slots:
        items = random.sample(items, available_item_slots)
    return items


def create_filler_festival_rewards(item_factory: StardewItemFactory, options: StardewValleyOptions) -> list[Item]:
    if options.festival_locations == FestivalLocations.option_disabled:
        return []

    return [
        item_factory(item)
        for item in items_by_group[Group.FESTIVAL]
        if item.classification == ItemClassification.filler
    ]


def generate_resource_packs_and_traps(item_factory: StardewItemFactory,
                                      options: StardewValleyOptions,
                                      random: Random,
                                      already_added_items: list[Item],
                                      available_item_slots: int) -> list[Item]:
    def filler_factory(item: ItemData) -> Item:
        # Yes some fillers are progression. We add multiple fruit tree saplings for instance.
        if ItemClassification.progression in item.classification:
            return item_factory(item,
                                classification_pre_fill=ItemClassification.filler,
                                classification_post_fill=ItemClassification.progression_skip_balancing)
        return item_factory(item)

    already_added_items_names = {item.name for item in already_added_items}

    priority_fillers = get_priority_resource_packs_buffs_and_traps(options)
    priority_fillers = filter_excluded(priority_fillers, options)
    priority_fillers = filter_already_included_maximum_one(priority_fillers, already_added_items_names)

    if available_item_slots < len(priority_fillers):
        return [filler_factory(priority_filler) for priority_filler in random.sample(priority_fillers, available_item_slots)]

    chosen_fillers = []
    chosen_fillers.extend([filler_factory(priority_filler) for priority_filler in priority_fillers])
    available_item_slots -= len(priority_fillers)
    already_added_items_names |= {priority_item.name for priority_item in priority_fillers}

    all_fillers = get_all_resource_packs_and_traps(options)
    all_fillers.extend(get_player_buffs(options))
    all_fillers = filter_excluded(all_fillers, options)
    all_fillers = filter_already_included_maximum_one(all_fillers, already_added_items_names)

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


def get_priority_resource_packs_buffs_and_traps(options: StardewValleyOptions) -> list[ItemData]:
    useful_resource_packs = items_by_group[Group.RESOURCE_PACK_USEFUL]
    buffs = get_player_buffs(options)
    traps = get_traps(options)

    return useful_resource_packs + buffs + traps


def get_player_buffs(options: StardewValleyOptions) -> list[ItemData]:
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
        if options.trap_distribution.get(trap.name, 0) > 0
    ]
