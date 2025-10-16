from typing import Dict, Any

from BaseClasses import CollectionState, Item, Tutorial
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from .Items import SohItem, item_data_table, item_table, item_name_groups, progressive_items
from .Locations import location_table
from .Options import SohOptions, soh_option_groups
from .Regions import create_regions_and_locations, place_locked_items, dungeon_reward_item_mapping
from .Enums import *
from .ItemPool import create_item_pool, get_filler_item
from .LogicHelpers import increment_current_count
from . import RegionAgeAccess
from .ShopItems import fill_shop_items, all_shop_locations
from Fill import fill_restrictive

import logging
logger = logging.getLogger("SOH_OOT")

class SohWebWorld(WebWorld):
    theme = "ice"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Ship of Harkinian.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["aMannus"]
    )
    
    tutorials = [setup_en]
    game_info_languages = ["en"]
    option_groups = soh_option_groups


class SohWorld(World):
    """A PC Port of Ocarina of Time"""

    game = "Ship of Harkinian"
    web = SohWebWorld()
    options: SohOptions
    options_dataclass = SohOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    item_name_groups = item_name_groups

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.item_pool = list[SohItem]()
        self.included_locations = dict[str, int]()
        self.shop_prices = dict[str, int]()
        self.shop_vanilla_items = dict[str, str]()
        self.scrub_prices = dict[str, int]()

    def generate_early(self) -> None:
        # If door of time is set to closed and dungeon rewards aren't shuffled, force child spawn
        if self.options.door_of_time.value == 0 and self.options.shuffle_dungeon_rewards.value == 0:
            self.options.starting_age.value = 0

    def create_item(self, name: str) -> SohItem:
        item_entry = Items(name)
        return SohItem(name, item_data_table[item_entry].classification, item_data_table[item_entry].item_id, self.player)

    def create_items(self) -> None:
        # these are for making the progressive items collect/remove work properly
        # when adding another progressive item that is option-dependent like these,
        # be sure to also update LogicHelpers.increment_current_count with it too
        if not self.options.shuffle_swim:
            self.push_precollected(self.create_item(Items.BRONZE_SCALE))
        if not self.options.shuffle_deku_stick_bag:
            self.push_precollected(self.create_item(Items.DEKU_STICK_BAG))
        if not self.options.shuffle_deku_nut_bag:
            self.push_precollected(self.create_item(Items.DEKU_NUT_BAG))
        if not self.options.bombchu_bag:
            self.push_precollected(self.create_item(Items.BOMBCHU_BAG))
        
        create_item_pool(self)

    def create_regions(self) -> None: 
        create_regions_and_locations(self)
        place_locked_items(self)

    def set_rules(self) -> None:
        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: state.has(Events.GAME_COMPLETED.value, self.player)

    def pre_fill(self) -> None:
        # Prefill Dungeon Rewards. Need to collect the item pool and vanilla shop items before doing so.
        if self.options.shuffle_dungeon_rewards.value == 1:
            # Create a filled copy of the state so the multiworld can place the dungeon rewards using logic
            prefill_state = CollectionState(self.multiworld)
            for item in self.item_pool:
                prefill_state.collect(item, False)
            for region, shop in all_shop_locations:
                for slot, item in shop.items():
                    prefill_state.collect(self.create_item(item), False)
            prefill_state.sweep_for_advancements()

            dungeon_reward_locations = [self.get_location(location.value) for location in dungeon_reward_item_mapping.keys()]
            dungeon_reward_items = [self.create_item(item.value) for item in dungeon_reward_item_mapping.values()]

            # Place dungeon rewards
            fill_restrictive(self.multiworld, prefill_state, dungeon_reward_locations, dungeon_reward_items, single_player_placement=True, lock=True)

        fill_shop_items(self)

        open_location_count: int = sum(1 for loc in self.get_locations() if not loc.locked)
        filler_item_count: int = open_location_count - len(self.item_pool)

        # Ice Trap Count
        for _ in range(min(filler_item_count, self.options.ice_trap_count.value)):
            self.item_pool += [self.create_item(Items.ICE_TRAP)]
            filler_item_count -= 1

        # Ice Trap Filler Replacement
        places_to_fill: int = int(filler_item_count * (self.options.ice_trap_filler_replacement.value * .01))
        for _ in range(places_to_fill):
            self.item_pool += [self.create_item(Items.ICE_TRAP)]
            filler_item_count -= 1

        # Add junk items to fill remaining locations
        for _ in range(filler_item_count):
            self.item_pool += [self.create_item(get_filler_item(self))]

        self.multiworld.itempool += self.item_pool

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "closed_forest": self.options.closed_forest.value,
            "kakariko_gate": self.options.kakariko_gate.value,
            "door_of_time": self.options.door_of_time.value,
            "zoras_fountain": self.options.zoras_fountain.value,
            "sleeping_waterfall": self.options.sleeping_waterfall.value,
            "jabu_jabu": self.options.jabu_jabu.value,
            "lock_overworld_doors": self.options.lock_overworld_doors.value,
            "fortress_carpenters": self.options.fortress_carpenters.value,
            "rainbow_bridge": self.options.rainbow_bridge.value,
            "rainbow_bridge_greg_modifier": self.options.rainbow_bridge_greg_modifier.value,
            "rainbow_bridge_stones_required": self.options.rainbow_bridge_stones_required.value,
            "rainbow_bridge_medallions_required": self.options.rainbow_bridge_medallions_required.value,
            "rainbow_bridge_dungeon_rewards_required": self.options.rainbow_bridge_dungeon_rewards_required.value,
            "rainbow_bridge_dungeons_required": self.options.rainbow_bridge_dungeons_required.value,
            "rainbow_bridge_skull_tokens_required": self.options.rainbow_bridge_skull_tokens_required.value,
            "skip_ganons_trials": self.options.skip_ganons_trials.value,
            "triforce_hunt": self.options.triforce_hunt.value,
            "triforce_hunt_required_pieces": self.options.triforce_hunt_required_pieces.value,
            "triforce_hunt_extra_pieces_percentage": self.options.triforce_hunt_extra_pieces_percentage.value,
            "shuffle_skull_tokens": self.options.shuffle_skull_tokens.value,
            "skull_sun_song": self.options.skull_sun_song.value,
            "shuffle_master_sword": self.options.shuffle_master_sword.value,
            "shuffle_childs_wallet": self.options.shuffle_childs_wallet.value,
            "shuffle_ocarina_buttons": self.options.shuffle_ocarina_buttons.value,
            "shuffle_swim": self.options.shuffle_swim.value,
            "shuffle_weird_egg": self.options.shuffle_weird_egg.value,
            "shuffle_fishing_pole": self.options.shuffle_fishing_pole.value,
            "shuffle_deku_stick_bag": self.options.shuffle_deku_stick_bag.value,
            "shuffle_deku_nut_bag": self.options.shuffle_deku_nut_bag.value,
            "shuffle_freestanding_items": self.options.shuffle_freestanding_items.value,
            "shuffle_shops": self.options.shuffle_shops.value,
            "shuffle_fish": self.options.shuffle_fish.value,
            "shuffle_scrubs": self.options.shuffle_scrubs.value,
            "shuffle_beehives": self.options.shuffle_beehives.value,
            "shuffle_cows": self.options.shuffle_cows.value,
            "shuffle_pots": self.options.shuffle_pots.value,
            "shuffle_crates": self.options.shuffle_crates.value,
            "shuffle_trees": self.options.shuffle_trees.value,
            "shuffle_merchants": self.options.shuffle_merchants.value,
            "shuffle_frog_song_rupees": self.options.shuffle_frog_song_rupees.value,
            "shuffle_adult_trade_items": self.options.shuffle_adult_trade_items.value,
            "shuffle_boss_souls": self.options.shuffle_boss_souls.value,
            "shuffle_fountain_fairies": self.options.shuffle_fountain_fairies.value,
            "shuffle_stone_fairies": self.options.shuffle_stone_fairies.value,
            "shuffle_bean_fairies": self.options.shuffle_bean_fairies.value,
            "shuffle_song_fairies": self.options.shuffle_song_fairies.value,
            "shuffle_grass": self.options.shuffle_grass.value,
            "shuffle_dungeon_rewards": self.options.shuffle_dungeon_rewards.value,
            "maps_and_compasses": self.options.maps_and_compasses.value,
            "ganons_castle_boss_key": self.options.ganons_castle_boss_key.value,
            "ganons_castle_boss_key_greg_modifier": self.options.ganons_castle_boss_key_greg_modifier.value,
            "ganons_castle_boss_key_stones_required": self.options.ganons_castle_boss_key_stones_required.value,
            "ganons_castle_boss_key_medallions_required": self.options.ganons_castle_boss_key_medallions_required.value,
            "ganons_castle_boss_key_dungeon_rewards_required": self.options.ganons_castle_boss_key_dungeon_rewards_required.value,
            "ganons_castle_boss_key_dungeons_required": self.options.ganons_castle_boss_key_dungeons_required.value,
            "ganons_castle_boss_key_skull_tokens_required": self.options.ganons_castle_boss_key_skull_tokens_required.value,
            "key_rings": self.options.key_rings.value,
            "big_poe_target_count": self.options.big_poe_target_count.value,
            "skip_child_zelda": self.options.skip_child_zelda.value,
            "skip_epona_race": self.options.skip_epona_race.value,
            "complete_mask_quest": self.options.complete_mask_quest.value,
            "skip_scarecrows_song": self.options.skip_scarecrows_song.value,
            "full_wallets": self.options.full_wallets.value,
            "bombchu_bag": self.options.bombchu_bag.value,
            "bombchu_drops": self.options.bombchu_drops.value,
            "blue_fire_arrows": self.options.blue_fire_arrows.value,
            "sunlight_arrows": self.options.sunlight_arrows.value,
            "infinite_upgrades": self.options.infinite_upgrades.value,
            "skeleton_key": self.options.skeleton_key.value,
            "slingbow_break_beehives": self.options.slingbow_break_beehives.value,
            "starting_age": self.options.starting_age.value,
            "shuffle_100_gs_reward": self.options.shuffle_100_gs_reward.value,
            "ice_trap_count": self.options.ice_trap_count.value,
            "ice_trap_filler_replacement": self.options.ice_trap_filler_replacement.value,
            "shop_prices": self.shop_prices,
            "shop_vanilla_items": self.shop_vanilla_items,
            "scrub_prices": self.scrub_prices,
        }

    def collect(self, state: CollectionState, item: Item) -> bool:
        state._soh_stale[self.player] = True # type: ignore

        if item.name in progressive_items:
            current_count = state.prog_items[self.player][item.name] + 1
            current_count = increment_current_count(self, item, current_count)
            for non_prog_version in progressive_items[item.name]:
                state.prog_items[self.player][non_prog_version] = 1
                current_count -= 1
                if not current_count:
                    break

        return super().collect(state, item)
    
    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if changed:
            state._soh_invalidate(self.player) # type: ignore

        if item.name in progressive_items:
            current_count = state.prog_items[self.player][item.name]
            current_count = increment_current_count(self, item, current_count)
            for i, non_prog_version in enumerate(progressive_items[item.name]):
                if i + 1 > current_count:
                    state.prog_items[self.player][non_prog_version] = 0

        return changed

    def generate_output(self, output_directory: str):
    
        visualize_regions(self.multiworld.get_region(self.origin_region_name, self.player), f"SOH-Player{self.player}.puml",
                        show_entrance_names=True,
                        regions_to_highlight=self.multiworld.get_all_state().reachable_regions[
                            self.player])
