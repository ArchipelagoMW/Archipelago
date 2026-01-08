import orjson
import pkgutil

from typing import Any, List, ClassVar

from BaseClasses import CollectionState, Item, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import SohItem, item_data_table, item_table, item_name_groups, progressive_items
from .Locations import location_table, location_name_groups
from .Options import SohOptions, soh_option_groups
from .Regions import create_regions_and_locations, place_locked_items, dungeon_reward_item_mapping
from .Enums import *
from .ItemPool import create_item_pool, create_filler_item_pool, create_triforce_pieces, get_filler_item
from . import RegionAgeAccess
from .ShopItems import fill_shop_items, generate_scrub_prices, set_price_rules, all_shop_locations
from Fill import fill_restrictive
from .Presets import oot_soh_options_presets
from .UniversalTracker import setup_options_from_slot_data
from settings import Group, Bool
from Options import OptionError

import logging
logger = logging.getLogger("SOH_OOT")


class SohWebWorld(WebWorld):
    theme = "ice"
    options_presets = oot_soh_options_presets

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


class SohSettings(Group):
    class AllowTrueNoLogic(Bool):
        """
        Allows SoH players to enable the true_no_logic hidden option, which makes every region and logically accessible.
        Do not enable this if you are not ready to use /send, !getitem, or similar commands.
        Do not enable this if you don't trust the players using it to play responsibly.
        """

    allow_true_no_logic: AllowTrueNoLogic | bool = False


class SohWorld(World):
    """A PC Port of Ocarina of Time"""

    game = "Ship of Harkinian"
    web = SohWebWorld()
    options: SohOptions
    options_dataclass = SohOptions
    settings: ClassVar[SohSettings]
    location_name_to_id = location_table
    item_name_to_id = item_table
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    # Universal Tracker stuff, does not do anything in normal gen
    using_ut: bool  # so we can check if we're using UT only once
    passthrough: dict[str, Any]  # slot data that got passed through
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.item_pool = list[SohItem]()
        self.included_locations = dict[str, int]()
        self.shop_prices = dict[str, int]()
        self.shop_vanilla_items = dict[str, str]()
        self.scrub_prices = dict[str, int]()
        self.triforce_pieces_required: int = 0

        apworld_manifest = orjson.loads(pkgutil.get_data(
            __name__, "archipelago.json").decode("utf-8"))
        self.apworld_version: str = apworld_manifest["world_version"]
        # The version is stored on Worlds, so when we're ready to bump our min AP version to 0.6.4, we can use this directly in our slot data:
        # slot_data["apworld_version"] = self.world_version

    def generate_early(self) -> None:
        # for use with Universal Tracker, doesn't do anything otherwise
        setup_options_from_slot_data(self)

        if self.options.true_no_logic and not self.settings.allow_true_no_logic:
            raise OptionError(f"Player {self.player_name} enabled True No Logic, but the corresponding host.yaml "
                              "setting has not been enabled. Either have them disable that option, or enable it in "
                              "your host.yaml settings.")

        # If door of time is set to closed and dungeon rewards aren't shuffled, force child spawn
        if self.options.door_of_time.value == 0 and self.options.shuffle_dungeon_rewards.value == 0:
            self.options.starting_age.value = 0

        # If maximum price is below minimum, set max to minimum.
        if self.options.shuffle_shops_minimum_price.value > self.options.shuffle_shops_maximum_price.value:
            self.options.shuffle_shops_maximum_price.value = self.options.shuffle_shops_minimum_price.value

        if self.options.shuffle_scrubs_minimum_price.value > self.options.shuffle_scrubs_maximum_price.value:
            self.options.shuffle_scrubs_maximum_price.value = self.options.shuffle_scrubs_minimum_price.value

    def create_regions(self) -> None:
        create_regions_and_locations(self)
        place_locked_items(self)
        generate_scrub_prices(self)
        for location in self.get_locations():
            location.name = str(location.name)
        for region in self.get_regions():
            region.name = str(region.name)

        if self.options.true_no_logic:
            for entrance in self.get_entrances():
                entrance.access_rule = lambda state: True
            for location in self.get_locations():
                location.access_rule = lambda state: True

    def create_item(self, name: str, create_as_event: bool = False) -> SohItem:
        item_entry = Items(name)
        return SohItem(str(name), item_data_table[item_entry].classification,
                       None if create_as_event else item_data_table[item_entry].item_id, self.player)

    def get_filler_item_name(self) -> str:
        return get_filler_item(self)

    def create_items(self) -> None:
        # these are for making the progressive items collect/remove work properly
        if not self.options.shuffle_swim:
            self.push_precollected(self.create_item(
                Items.PROGRESSIVE_SCALE, create_as_event=True))
        if not self.options.shuffle_deku_stick_bag:
            self.push_precollected(self.create_item(
                Items.PROGRESSIVE_STICK_CAPACITY, create_as_event=True))
        if not self.options.shuffle_deku_nut_bag:
            self.push_precollected(self.create_item(
                Items.PROGRESSIVE_NUT_CAPACITY, create_as_event=True))
        if not self.options.shuffle_childs_wallet:
            self.push_precollected(self.create_item(
                Items.PROGRESSIVE_WALLET, create_as_event=True))

        create_item_pool(self)

        if self.options.triforce_hunt:
            create_triforce_pieces(self)

        create_filler_item_pool(self)

    def set_rules(self) -> None:
        if self.options.true_no_logic:
            return

        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            Events.GAME_COMPLETED.value, self.player)

        # UT doesn't run pre_fill, so we're doing this here instead
        if self.using_ut:
            self.shop_prices = self.passthrough["shop_prices"]
            self.shop_vanilla_items = self.passthrough["shop_vanilla_items"]
            set_price_rules(self)

    def get_pre_fill_items(self) -> List["Item"]:
        pre_fill_items = []

        if self.options.shuffle_dungeon_rewards == "dungeons":
            dungeon_reward_items = [self.create_item(
                item.value) for item in dungeon_reward_item_mapping.values()]
            pre_fill_items.extend(dungeon_reward_items)

        for region, shop in all_shop_locations:
            for slot, item in shop.items():
                pre_fill_items.append(self.create_item(item))

        return pre_fill_items

    def pre_fill(self):
        # Prefill Dungeon Rewards. Need to collect the item pool and vanilla shop items before doing so.
        if self.options.shuffle_dungeon_rewards == "dungeons":
            # Create a filled copy of the state so the multiworld can place the dungeon rewards using logic
            prefill_state = CollectionState(self.multiworld)
            for item in self.item_pool:
                prefill_state.collect(item, True)
            for region, shop in all_shop_locations:
                for slot, item in shop.items():
                    prefill_state.collect(self.create_item(item), True)
            prefill_state.sweep_for_advancements()

            dungeon_reward_locations = [self.get_location(location.value)
                                        for location in dungeon_reward_item_mapping.keys()]
            dungeon_reward_items = [self.create_item(
                item.value) for item in dungeon_reward_item_mapping.values()]
            self.multiworld.random.shuffle(dungeon_reward_items)

            # Place dungeon rewards
            fill_restrictive(self.multiworld, prefill_state, dungeon_reward_locations,
                             dungeon_reward_items, single_player_placement=True, lock=True)

        fill_shop_items(self)

        # if UT ever does start running pre_fill, this will stop it from overwriting the shop price rules
        if self.using_ut or self.options.true_no_logic:
            return

        set_price_rules(self)

    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        state._soh_stale[self.player] = True  # type: ignore

        if item.name in progressive_items:
            current_count = state.prog_items[self.player][item.name]
            for non_prog_version in progressive_items[item.name]:
                state.prog_items[self.player][non_prog_version] = 1
                current_count -= 1
                if not current_count:
                    break

        if item.name == Items.HEART_CONTAINER:
            state.soh_heart_count[self.player] += 1  # type: ignore

        if item.name in (Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER):
            state.soh_piece_of_heart_count[self.player] += 1  # type: ignore
            if state.soh_piece_of_heart_count[self.player] == 4:  # type: ignore
                state.soh_piece_of_heart_count[self.player] = 0  # type: ignore
                state.soh_heart_count[self.player] += 1  # type: ignore

        return changed

    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if changed:
            state._soh_invalidate(self.player)  # type: ignore

        if item.name in progressive_items:
            current_count = state.prog_items[self.player][item.name]
            for i, non_prog_version in enumerate(progressive_items[item.name]):
                if i + 1 > current_count:
                    state.prog_items[self.player][non_prog_version] = 0

        if item.name == Items.HEART_CONTAINER:
            state.soh_heart_count[self.player] -= 1  # type: ignore

        if item.name in (Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER):
            state.soh_piece_of_heart_count[self.player] -= 1  # type: ignore
            if state.soh_piece_of_heart_count[self.player] == -1:  # type: ignore
                state.soh_piece_of_heart_count[self.player] = 3  # type: ignore
                state.soh_heart_count[self.player] -= 1  # type: ignore

        return changed

    # For debugging purposes
    # def generate_output(self, output_directory: str):
    #    from Utils import visualize_regions
    #    visualize_regions(self.get_region(self.origin_region_name), f"SOH-Player{self.player}.puml",
    #                      show_entrance_names=True,
    #                      regions_to_highlight=self.multiworld.get_all_state().reachable_regions[self.player])

    def fill_slot_data(self) -> dict[str, Any]:
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
            "triforce_hunt_pieces_total": self.options.triforce_hunt_pieces_total.value,
            "triforce_hunt_pieces_required": self.triforce_pieces_required,
            "shuffle_skull_tokens": self.options.shuffle_skull_tokens.value,
            "skulls_sun_song": self.options.skulls_sun_song.value,
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
            "shuffle_shops_item_amount": self.options.shuffle_shops_item_amount.value,
            "shop_prices": self.shop_prices,
            "shop_vanilla_items": self.shop_vanilla_items,
            "shuffle_fish": self.options.shuffle_fish.value,
            "shuffle_scrubs": self.options.shuffle_scrubs.value,
            "scrub_prices": self.scrub_prices,
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
            "no_logic": self.options.true_no_logic.value,
            "apworld_version": self.apworld_version,
        }
