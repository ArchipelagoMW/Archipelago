"""Item table for Donkey Kong 64."""

import math
import typing

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from types import SimpleNamespace
from typing import TYPE_CHECKING

from archipelago.Options import Goal, ShopPrices, HelmDoor1Item, HelmDoor2Item
from randomizer.Enums.Levels import Levels
from randomizer.Lists import Item as DK64RItem
from randomizer.Enums.Items import Items as DK64RItems
from randomizer.Enums.Settings import WinConditionComplex
from randomizer.Enums.Types import Types as DK64RTypes, BarrierItems
import randomizer.ItemPool as DK64RItemPoolUtility
import copy

if TYPE_CHECKING:
    from .. import DK64World

BASE_ID = 0xD64000


class ItemData(typing.NamedTuple):
    """Data for an item."""

    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


class DK64Item(Item):
    """A DK64 item."""

    game: str = "Donkey Kong 64"


# Separate tables for each type of item.
junk_table = {}

collectable_table = {}

event_table = {
    "Victory": ItemData(0xD64000, True),  # Temp
}


def use_original_name_or_trap_name(item: DK64RItem.Item) -> str:
    """Determine whether to use the original donk name or a renamed ice trap name."""
    if item.type == DK64RTypes.FakeItem:
        # Rename traps to be easier for trap link
        parts = item.name.split("(")

        main_part = parts[0]
        trap_word = main_part.strip().split(" ")[-1]

        subtype = parts[1].split(")")[0]
        if "-" in subtype:
            if "GB" not in subtype.split("-")[1].strip():
                return item.name  # Don't mess with these. We'll deal with them if we decide to add fake Beans/Keys to AP.
            subtype = subtype.split("-")[0].strip()

        return f"{subtype} {trap_word}"
    else:
        return item.name


# Complete item table
full_item_table: dict[str, ItemData] = {use_original_name_or_trap_name(item): ItemData(int(BASE_ID + index), item.playthrough) for index, item in DK64RItem.ItemList.items()}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in full_item_table.items() if data.code}

full_item_table.update(event_table)  # Temp for generating goal item


def random_starting_moves(world: "DK64World") -> typing.List[str]:
    """Handle starting move alterations here."""
    starting_moves = []

    all_eligible_starting_moves = DK64RItemPoolUtility.AllKongMoves()
    all_eligible_starting_moves.extend(DK64RItemPoolUtility.TrainingBarrelAbilities())
    all_eligible_starting_moves.extend(DK64RItemPoolUtility.JunkSharedMoves)
    all_eligible_starting_moves.append(DK64RItems.Camera)
    all_eligible_starting_moves.append(DK64RItems.Shockwave)

    # Either include Climbing as an eligible starting move or place it in the starting inventory
    if world.options.climbing_shuffle:
        all_eligible_starting_moves.extend(DK64RItemPoolUtility.ClimbingAbilities())
    world.random.shuffle(all_eligible_starting_moves)
    while len(starting_moves) < world.options.starting_move_count:
        if len(all_eligible_starting_moves) == 0:
            break
        move_id = all_eligible_starting_moves.pop()
        move = DK64RItem.ItemList[move_id]
        # We don't want to pick anything we're already starting with. As an aside, the starting inventory move name may or may not have spaces in it.
        if move.name in world.options.start_inventory:
            # If we were to choose a move we're forcibly starting with, pick another
            continue
        starting_moves.append(move.name)

    return starting_moves


def setup_items(world: "DK64World") -> typing.List[DK64Item]:
    """Set up the item table for the world."""
    item_table = []
    starting_moves = random_starting_moves(world)

    # Determine helm door requirements upfront
    helm_door_required_types = set()
    if world.options.crown_door_item.value >= 2:  # Any requirement (random or specific)
        helm_door_required_types.add(world.spoiler.settings.crown_door_item)
    if world.options.coin_door_item.value >= 2:  # Any requirement (random or specific)
        helm_door_required_types.add(world.spoiler.settings.coin_door_item)

    # Handle vanilla helm door requirements
    if world.options.crown_door_item.value == HelmDoor1Item.option_vanilla:
        helm_door_required_types.add(BarrierItems.Crown)
    if world.options.coin_door_item.value == HelmDoor2Item.option_vanilla:
        helm_door_required_types.add(BarrierItems.CompanyCoin)

    for item_id, dk64r_item in DK64RItem.ItemList.items():
        name = use_original_name_or_trap_name(dk64r_item)
        # Edit the progression on an item-by-item basis.
        ap_item = DK64Item(name, ItemClassification.progression, full_item_table[name].code, world.player)
        match dk64r_item.type:
            case DK64RTypes.Banana:
                if world.options.snide_turnins_to_pool:
                    num_bananas = 201
                else:
                    num_bananas = 161
                if world.options.goal != Goal.option_golden_bananas and BarrierItems.GoldenBanana not in helm_door_required_types:
                    ap_item.classification = ItemClassification.progression_deprioritized
                for _ in range(num_bananas):
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Shop | DK64RTypes.TrainingBarrel | DK64RTypes.Shockwave:
                if name == "Camera and Shockwave":
                    continue
                # Skip JunkSharedMoves if no_consumable_upgrades is enabled
                if item_id in DK64RItemPoolUtility.JunkSharedMoves and world.spoiler.settings.no_consumable_upgrades:
                    continue
                if item_id in DK64RItemPoolUtility.JunkSharedMoves:
                    ap_item.classification = ItemClassification.useful
                num_moves = 1  # Track the number of each potion, default 1
                if item_id == DK64RItems.ProgressiveAmmoBelt:
                    num_moves = 2
                elif item_id == DK64RItems.ProgressiveInstrumentUpgrade or item_id == DK64RItems.ProgressiveSlam:
                    num_moves = 3
                if name in world.options.start_inventory:
                    num_moves -= world.options.start_inventory[name]
                if name in starting_moves:
                    for _ in range(starting_moves.count(name)):
                        world.multiworld.push_precollected(copy.copy(ap_item))
                        num_moves -= 1
                for _ in range(num_moves):
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Blueprint:
                # Need to remove the old blueprints
                if item_id >= DK64RItems.DonkeyBlueprint and item_id <= DK64RItems.ChunkyBlueprint:
                    if BarrierItems.Blueprint in helm_door_required_types:
                        # Helm door requires blueprints
                        ap_item.classification = ItemClassification.progression_skip_balancing
                    elif world.options.goal in {Goal.option_blueprints, Goal.option_krools_challenge}:
                        ap_item.classification = ItemClassification.progression
                    else:
                        ap_item.classification = ItemClassification.progression_deprioritized
                    # Add 8 of each generic blueprint (8 per kong = 40 total)
                    for _ in range(8):
                        item_table.append(copy.copy(ap_item))
            case DK64RTypes.Fairy:
                num_fairies = 20
                if BarrierItems.Fairy in helm_door_required_types or world.options.goal == Goal.option_fairies:
                    # Helm door requires fairies
                    ap_item.classification = ItemClassification.progression_skip_balancing
                elif not world.options.goal == Goal.option_fairies:
                    ap_item.classification = ItemClassification.progression_deprioritized
                for _ in range(num_fairies):
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Key:
                # Keys are weird because there's a lot of possibilities based on settings.
                level_keys = {"Key 1", "Key 2", "Key 4", "Key 5", "Key 6", "Key 7"}
                mcguffin_keys = {"Key 3", "Key 8"}

                if name in level_keys:
                    if world.options.open_lobbies:
                        ap_item.classification = ItemClassification.progression_skip_balancing
                if name in mcguffin_keys:
                    ap_item.classification = ItemClassification.progression_skip_balancing

                if item_id in world.spoiler.settings.starting_key_list:
                    world.multiworld.push_precollected(copy.copy(ap_item))
                elif item_id == DK64RItemPoolUtility.getHelmKey(world.spoiler.settings) and world.spoiler.settings.key_8_helm:
                    world.multiworld.get_location("The End of Helm", world.player).place_locked_item(copy.copy(ap_item))
                    world.spoiler.settings.location_pool_size -= 1
                else:
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Crown:
                num_crowns = 10
                if world.options.goal not in {Goal.option_crowns, Goal.option_treasure_hurry} and BarrierItems.Crown not in helm_door_required_types and not world.options.enable_chaos_blockers:
                    ap_item.classification = ItemClassification.filler
                elif (world.options.goal in {Goal.option_crowns, Goal.option_treasure_hurry} or BarrierItems.Crown in helm_door_required_types) and not world.options.enable_chaos_blockers:
                    ap_item.classification = ItemClassification.progression_skip_balancing
                for _ in range(num_crowns):
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Kong:
                kong = DK64RItemPoolUtility.GetKongForItem(item_id)
                if kong in world.spoiler.settings.starting_kong_list:
                    world.multiworld.push_precollected(copy.copy(ap_item))
                else:
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Medal:
                num_medals = 40
                if BarrierItems.Medal in helm_door_required_types:
                    # Helm door requires medals
                    ap_item.classification = ItemClassification.progression_skip_balancing
                elif not world.options.goal == Goal.option_medals:
                    ap_item.classification = ItemClassification.progression_deprioritized
                for _ in range(num_medals):
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Bean:
                if BarrierItems.Bean in helm_door_required_types or world.options.goal == Goal.option_bean:
                    # Helm door or win condition requires bean
                    ap_item.classification = ItemClassification.progression_skip_balancing
                item_table.append(copy.copy(ap_item))
            case DK64RTypes.Pearl:
                num_pearls = 5
                if BarrierItems.Pearl in helm_door_required_types or world.options.goal == Goal.option_pearls:
                    # Helm door requires pearls
                    ap_item.classification = ItemClassification.progression_skip_balancing
                elif not world.options.goal == Goal.option_pearls:
                    ap_item.classification = ItemClassification.progression_deprioritized
                for _ in range(num_pearls):
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.RainbowCoin:
                num_coins = 16
                if BarrierItems.RainbowCoin in helm_door_required_types or world.options.goal == Goal.option_rainbow_coins:
                    ap_item.classification = ItemClassification.progression_skip_balancing
                elif world.options.shop_prices != ShopPrices.option_free:
                    ap_item.classification = ItemClassification.progression_deprioritized
                elif not world.options.enable_chaos_blockers:
                    ap_item.classification = ItemClassification.filler
                else:
                    ap_item.classification = ItemClassification.progression_skip_balancing
                for _ in range(num_coins):
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Climbing:
                if name in starting_moves or not world.options.climbing_shuffle:
                    world.multiworld.push_precollected(copy.copy(ap_item))
                elif name in world.options.start_inventory:
                    continue
                else:
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.Hint:
                if not world.options.hints_in_item_pool:
                    continue
                else:
                    ap_item.classification = ItemClassification.useful
                    item_table.append(copy.copy(ap_item))
            case DK64RTypes.NintendoCoin | DK64RTypes.RarewareCoin:
                if not (world.options.goal in {Goal.option_company_coins, Goal.option_treasure_hurry} or BarrierItems.CompanyCoin in helm_door_required_types or world.options.enable_chaos_blockers):
                    ap_item.classification = ItemClassification.filler
                elif (
                    world.options.goal in {Goal.option_company_coins, Goal.option_treasure_hurry} or BarrierItems.CompanyCoin in helm_door_required_types
                ) and not world.options.enable_chaos_blockers:
                    ap_item.classification = ItemClassification.progression_skip_balancing
                item_table.append(copy.copy(ap_item))
            case DK64RTypes.Cranky | DK64RTypes.Funky | DK64RTypes.Candy | DK64RTypes.Snide:
                if not world.options.shopowners_in_pool:
                    continue
                if name in world.options.start_inventory:
                    continue
                else:
                    item_table.append(copy.copy(ap_item))
            case (
                DK64RTypes.BlueprintBanana
                | DK64RTypes.Constant
                | DK64RTypes.NoItem
                | DK64RTypes.FakeItem
                | DK64RTypes.RaceBanana
                | DK64RTypes.GauntletBanana
                | DK64RTypes.JunkItem
                | DK64RTypes.CrateItem
                | DK64RTypes.Enemies
                | DK64RTypes.IslesMedal
                | DK64RTypes.ProgressiveHint
                | DK64RTypes.ArchipelagoItem
                | DK64RTypes.BoulderItem
                | DK64RTypes.FillerPearl
                | DK64RTypes.FillerBanana
                | DK64RTypes.FillerFairy
                | DK64RTypes.FillerCrown
                | DK64RTypes.FillerMedal
                | DK64RTypes.HelmMedal
                | DK64RTypes.HelmKey
                | DK64RTypes.EnemyPhoto
                | DK64RTypes.HalfMedal
            ):
                # Items that should not be added to the pool at all
                continue

    # Raise an error if we have too many items
    available_slots = world.spoiler.settings.location_pool_size - 1  # minus 1 for Banana Hoard
    if len(item_table) > available_slots:
        raise Exception(f"Too many DK64 items to be placed in too few DK64 locations: {len(item_table)} items for {available_slots} slots (excess: {len(item_table) - available_slots})")

    # If there's too many locations and not enough items, add some junk
    filler_item_count: int = world.spoiler.settings.location_pool_size - len(item_table) - 1  # The last 1 is for the Banana Hoard

    trap_weights = []
    trap_weights += [DK64RItems.IceTrapBubble] * world.options.bubble_trap_weight.value
    trap_weights += [DK64RItems.IceTrapReverse] * world.options.reverse_trap_weight.value
    trap_weights += [DK64RItems.IceTrapSlow] * world.options.slow_trap_weight.value
    trap_weights += [DK64RItems.IceTrapDisableA] * world.options.disable_a_trap_weight.value
    trap_weights += [DK64RItems.IceTrapDisableB] * world.options.disable_b_trap_weight.value
    trap_weights += [DK64RItems.IceTrapDisableZ] * world.options.disable_z_trap_weight.value
    trap_weights += [DK64RItems.IceTrapDisableCU] * world.options.disable_c_trap_weight.value
    trap_weights += [DK64RItems.IceTrapGetOutGB] * world.options.get_out_trap_weight.value
    trap_weights += [DK64RItems.IceTrapDryGB] * world.options.dry_trap_weight.value
    trap_weights += [DK64RItems.IceTrapFlipGB] * world.options.flip_trap_weight.value
    trap_weights += [DK64RItems.IceTrapIceFloorGB] * world.options.ice_floor_weight.value
    trap_weights += [DK64RItems.IceTrapPaperGB] * world.options.paper_weight.value
    trap_weights += [DK64RItems.IceTrapSlipGB] * world.options.slip_weight.value
    trap_weights += [DK64RItems.IceTrapAnimalGB] * world.options.animal_trap_weight.value
    trap_weights += [DK64RItems.IceTrapRockfallGB] * world.options.rockfall_trap_weight.value
    trap_weights += [DK64RItems.IceTrapDisableTagGB] * world.options.disabletag_trap_weight.value

    trap_count = 0 if (len(trap_weights) == 0) else math.ceil(filler_item_count * (world.options.trap_fill_percentage.value / 100.0))
    filler_item_count -= trap_count

    # Build filler weights based on options
    filler_weights = []
    filler_weights += [DK64RItems.JunkMelon] * world.options.junk_filler_weight.value
    filler_weights += [DK64RItems.FillerBanana] * world.options.banana_filler_weight.value
    filler_weights += [DK64RItems.FillerCrown] * world.options.crown_filler_weight.value
    filler_weights += [DK64RItems.FillerFairy] * world.options.fairy_filler_weight.value
    filler_weights += [DK64RItems.FillerMedal] * world.options.medal_filler_weight.value
    filler_weights += [DK64RItems.FillerPearl] * world.options.pearl_filler_weight.value
    filler_weights += [DK64RItems.FillerRainbowCoin] * world.options.rainbowcoin_filler_weight.value

    # If no filler weights are set, default to junk
    if not filler_weights:
        filler_weights = [DK64RItems.JunkMelon]

    for _ in range(filler_item_count):
        junk_enum = world.random.choice(filler_weights)
        junk_item = DK64RItem.ItemList[junk_enum]
        item_table.append(DK64Item(junk_item.name, ItemClassification.filler, full_item_table[junk_item.name].code, world.player))

    for _ in range(trap_count):
        trap_enum = world.random.choice(trap_weights)
        trap_item = DK64RItem.ItemList[trap_enum]
        trap_name = use_original_name_or_trap_name(trap_item)
        item_table.append(DK64Item(trap_name, ItemClassification.trap, full_item_table[trap_name].code, world.player))

    return item_table
