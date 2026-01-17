from collections.abc import Mapping
from random import Random

from BaseClasses import ItemClassification, Location

from . import Items
from . import Rom
from .id_maps import item_name_to_id
from .Options import FF6WCOptions

# NOTE: most of this code is located in WorldsCollide/args/items.py during the process function


def get_item_rewards(options: FF6WCOptions) -> list[str]:
    # Check to see what the Item Rewards are to populate the "dead" checks
    item_rewards: list[str] = []
    # if -ir in flagstring, then user specified item rewards
    if options.Flagstring.has_flag("-ir"):
        # get the item reward string between the -ir flag & the next one
        item_reward_args = options.Flagstring.get_flag("-ir").strip()
        for a_item_id in item_reward_args.split(','):
            # look for strings first
            a_item_id = a_item_id.lower().strip()
            if a_item_id == 'none':
                item_rewards = []
            elif a_item_id == 'standard':
                item_rewards = Items.good_items.copy()
            elif a_item_id == 'stronger':
                item_rewards = Items.stronger_items.copy()
            elif a_item_id == 'premium':
                item_rewards = Items.premium_items.copy()
            # else convert IDs to item names & place into reward list
            else:
                a_item_id = int(a_item_id)
                all_items = list(Rom.item_name_id.keys())
                if a_item_id < len(all_items):
                    item_rewards.append(all_items[a_item_id])
        # remove duplicates and sort
        item_rewards = list(set(item_rewards))
        item_rewards.sort()

        # Remove Atma Weapon is it's not Stronger (-saw flag) and Atma Weapon was added to reward pool
        if not options.Flagstring.has_flag("-saw") and "Atma Weapon" in item_rewards:
            item_rewards.remove("Atma Weapon")

        # Remove excluded items
        # if -nee No PaladinShld specified, remove from rewards list
        if options.no_paladin_shields() and "Paladin Shld" in item_rewards:
            item_rewards.remove("Paladin Shld")
        # if -nee No ExpEgg specified, remove from rewards list
        if options.no_exp_eggs() and "Exp. Egg" in item_rewards:
            item_rewards.remove("Exp. Egg")
        # if -nil No Illumina specified, remove from rewards list
        if options.no_illuminas() and "Illumina" in item_rewards:
            item_rewards.remove("Illumina")
        # if -noshoes No SprintShoes specified, remove from rewards list
        if options.Flagstring.has_flag("-noshoes") and "Sprint Shoes" in item_rewards:
            item_rewards.remove("Sprint Shoes")
        # if -nmc No MoogleCharms specified, remove from rewards list
        if options.Flagstring.has_flag("-nmc") and "Moogle Charm" in item_rewards:
            item_rewards.remove("Moogle Charm")

        # Make dead checks award "empty" if the item reward list is empty
        # (e.g. all items were supposed to be Illuminas and the No Illumina flag is on)
        if len(item_rewards) < 1:
            item_rewards.append("Empty")
    # else no -ir, keep good_items as-is
    else:
        item_rewards = Items.good_items

    return item_rewards


def build_ir_from_placements(wc_event_locations: list[Location]) -> list[str]:
    """ returns the "-ir" flag for the flagstring """
    inventory_item_ap_id_to_name = {item_name_to_id[name]: name for name in Items.items}

    items_in_wc_event_locations: dict[str, int] = {}
    for loc in wc_event_locations:
        if loc.item and loc.item.player == loc.player:
            ap_item_id = loc.item.code
            if ap_item_id in inventory_item_ap_id_to_name:
                wc_item_id = Rom.item_name_id[inventory_item_ap_id_to_name[ap_item_id]]
                items_in_wc_event_locations[loc.name] = wc_item_id

    items_in_wc_event_locations_list = sorted(set(items_in_wc_event_locations.values()))
    if len(items_in_wc_event_locations_list):
        item_str = ",".join(str(i_id) for i_id in items_in_wc_event_locations_list)
        return ["-ir", item_str]
    else:
        return []


def item_qualities() -> Mapping[int, int]:
    """ to be able to sort items by quality """
    from . import FF6WCWorld
    with FF6WCWorld.wc_ready:
        # hack to deal with global state in WC
        from .WorldsCollide import args
        setattr(args, "stronger_atma_weapon", False)
        from .WorldsCollide.data.chest_item_tiers import tiers
        delattr(args, "stronger_atma_weapon")

        sort_keys = [10, 8, 6, 4, 2,  9, 7, 5, 3, 1]
        assert len(sort_keys) == len(tiers), f"{len(tiers)=} {sort_keys=}"
        assert 239 in tiers[4], f"{tiers[4]=} should be Megalixir"
        assert 254 in tiers[3], f"{tiers[3]=} should have Dried Meat"
        qualities: dict[int, int] = {}
        for item_tier, key in zip(tiers, sort_keys, strict=True):
            for wc_id in item_tier:
                qualities[wc_id] = key
        return qualities


def limit_event_items(wc_event_locations: list[Location], random: Random) -> None:
    """
    make sure there are not too many different inventory items in the major locations

    (because there's limited space in rom for dialogs to give the items)
    """
    inventory_item_ap_id_to_name = {item_name_to_id[name]: name for name in Items.items}

    items_in_wc_event_locations: dict[str, int] = {}
    locations_by_name: dict[str, Location] = {}
    for loc in wc_event_locations:
        if loc.item and loc.item.player == loc.player:
            ap_item_id = loc.item.code
            if ap_item_id in inventory_item_ap_id_to_name:
                wc_item_id = Rom.item_name_id[inventory_item_ap_id_to_name[ap_item_id]]
                items_in_wc_event_locations[loc.name] = wc_item_id
                locations_by_name[loc.name] = loc

    qualities = item_qualities()

    def sort_key(wc_item_id: int) -> int:
        return qualities[wc_item_id]

    items_by_quality = sorted(set(items_in_wc_event_locations.values()), key=sort_key)

    # I think we start with 50 dialogs.
    # 8 might be used for the Auction House.
    # I don't know what else might use them - should leave some room for error.
    smaller_set = items_by_quality[:32]

    # print(f"{[Rom.item_id_name_weight[i_id][0] for i_id in smaller_set]=}")

    for loc_name, loc in locations_by_name.items():
        wc_item_id = items_in_wc_event_locations[loc_name]
        if wc_item_id not in smaller_set:
            replacement = random.choice(smaller_set)
            replacement_name = Rom.item_id_name_weight[replacement][0]
            replacement_code = item_name_to_id[replacement_name]
            assert loc.item, f"{loc=}"
            loc.item.name = replacement_name
            loc.item.code = replacement_code
            loc.item.classification = ItemClassification.useful
            loc.locked = True
