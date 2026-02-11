import orjson
import pkgutil

from typing import Any, ClassVar

from BaseClasses import CollectionState, Item, Tutorial, ItemClassification, Location
from worlds.AutoWorld import WebWorld, World
from .location_access.overworld.castle_grounds import LocalEvents
from .Items import SohItem, item_data_table, item_table, item_name_groups, progressive_items
from .Locations import location_table, location_name_groups, token_amounts, SohLocData, location_data_table
from .Options import SohOptions, soh_option_groups
from .Regions import create_regions_and_locations, place_locked_items
from .Enums import *
from .ItemPool import create_item_pool, create_filler_item_pool, create_triforce_pieces, get_filler_item
from . import RegionAgeAccess
from .DungeonRewardShuffle import pre_fill_dungeon, get_pre_fill_rewards
from .KeyShuffle import pre_fill_keys, get_pre_fill_keys
from .SongShuffle import pre_fill_songs, get_prefill_songs
from .ShopItems import fill_shop_items, generate_shop_prices, generate_scrub_prices, generate_merchant_prices, set_price_rules
from .Presets import oot_soh_options_presets
from .UniversalTracker import setup_options_from_slot_data
from settings import Group, Bool
from Options import OptionError
from .LogicHelpers import wallet_capacities

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
    """A PC Port of Ocarina of Time. The Legend of Zelda: Ocarina of Time is a 3D action/adventure game. Travel through Hyrule in two time periods, learn magical ocarina songs, and explore twelve dungeons on your quest. Use Link's many items and abilities to rescue the Seven Sages, and then confront Ganondorf to save Hyrule! """

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
    glitches_item_name = Items.GLITCHED
    using_ut: bool  # so we can check if we're using UT only once
    passthrough: dict[str, Any]  # slot data that got passed through
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.item_pool = list[SohItem]()
        self.included_locations = dict[str, SohLocData]()
        self.shop_prices = dict[str, int]()
        self.shop_vanilla_items = dict[str, str]()
        self.scrub_prices = dict[str, int]()
        self.merchant_prices = dict[str, int]()
        self.triforce_pieces_required: int = 0
        self.vanilla_progressive_skulltula_count: int = 0
        self.randomized_progressive_skulltula_count: int = 0
        self.pre_fill_pool = list[Items]()

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

        # If door of time is set to closed and dungeon rewards aren't shuffled or ocarinas aren't shuffled, force child spawn
        if self.options.door_of_time.value == 0 and (
                self.options.shuffle_dungeon_rewards.value == 0 or self.options.shuffle_ocarinas == 0 or self.options.shuffle_songs == "off"):
            self.options.starting_age.value = 0

        # If the door of time is set to song only, and the songs aren't shuffled, force child spawn
        if self.options.door_of_time == 1 and (self.options.shuffle_songs == "off"):
            self.options.starting_age.value = 0

        # Check if Tycoon Wallet is shuffled and if price settings are above what Giants Wallet can hold. Max/Min Prices need to be adjusted to fit in Giants Wallet.
        if not self.options.shuffle_tycoon_wallet.value:
            for option in (self.options.shuffle_shops_minimum_price, self.options.shuffle_shops_maximum_price, self.options.shuffle_scrubs_minimum_price, self.options.shuffle_scrubs_maximum_price, self.options.shuffle_merchants_minimum_price, self.options.shuffle_merchants_maximum_price):
                if option.value > wallet_capacities[Items.GIANT_WALLET]:
                    option.value = wallet_capacities[Items.GIANT_WALLET]

        # If maximum price is below minimum, set max to minimum.
        if self.options.shuffle_shops_minimum_price.value > self.options.shuffle_shops_maximum_price.value:
            self.options.shuffle_shops_maximum_price.value = self.options.shuffle_shops_minimum_price.value

        if self.options.shuffle_scrubs_minimum_price.value > self.options.shuffle_scrubs_maximum_price.value:
            self.options.shuffle_scrubs_maximum_price.value = self.options.shuffle_scrubs_minimum_price.value

        if self.options.shuffle_merchants_minimum_price.value > self.options.shuffle_merchants_maximum_price.value:
            self.options.shuffle_merchants_maximum_price.value = self.options.shuffle_merchants_minimum_price.value

        # Figure out how many Skulltula tokens need to be progressive
        # Max amount from KAK turn ins
        turn_in_amount: int = 0

        if self.options.shuffle_100_gs_reward:
            turn_in_amount = 100
        elif self.options.accessibility == "full":
            turn_in_amount = 50
        else:
            for location, amount in token_amounts.items():
                if str(location) not in self.options.exclude_locations:
                    turn_in_amount = amount
                    break

        progressive_skulltula_count: int = max(self.options.rainbow_bridge_skull_tokens_required.value if self.options.rainbow_bridge.value == 6 else 0,
                                               self.options.ganons_castle_boss_key_skull_tokens_required.value if self.options.ganons_castle_boss_key.value == 7 else 0, turn_in_amount)

        if self.options.shuffle_skull_tokens:
            self.randomized_progressive_skulltula_count = progressive_skulltula_count

            if self.options.shuffle_skull_tokens == "dungeon":
                self.vanilla_progressive_skulltula_count = max(
                    self.randomized_progressive_skulltula_count - TokenCounts.OVERWORLD.value, 0)

            if self.options.shuffle_skull_tokens == "overworld":
                self.vanilla_progressive_skulltula_count = max(
                    self.randomized_progressive_skulltula_count - TokenCounts.DUNGEON.value, 0)
        else:
            self.vanilla_progressive_skulltula_count = progressive_skulltula_count

        # Figure out Keyring Situation
        key_ring_options: list = [self.options.gerudo_fortress_key_ring, self.options.forest_temple_key_ring, self.options.fire_temple_key_ring, self.options.water_temple_key_ring,
                                  self.options.spirit_temple_key_ring, self.options.shadow_temple_key_ring, self.options.bottom_of_the_well_key_ring, self.options.gerudo_training_ground_key_ring, self.options.ganons_castle_key_ring]

        if self.options.key_rings != "selection":
            for option in key_ring_options:
                option.value = False

        if self.options.key_rings == "count":
            # Fix count if Gerudo Fortress Keys aren't allowed
            if self.options.fortress_carpenters == "normal" and self.options.gerudo_fortress_key_shuffle == "vanilla":
                if self.options.key_rings_count.value > 8:
                    self.options.key_rings_count.value = 8
                key_ring_options.remove(self.options.gerudo_fortress_key_ring)

            self.random.shuffle(key_ring_options)

            # Set only the chosen
            for index in range(self.options.key_rings_count.value):
                key_ring_options[index].value = True
        elif self.options.key_rings == "selection" and self.options.fortress_carpenters == "normal" and self.options.gerudo_fortress_key_shuffle == "vanilla":
            self.options.gerudo_fortress_key_ring.value = False

        # generate the prefill pool
        self.pre_fill_pool += get_pre_fill_rewards(self)
        self.pre_fill_pool += get_prefill_songs(self)
        for key_shuffle in get_pre_fill_keys(self).values():
            self.pre_fill_pool += key_shuffle
        self.pre_fill_pool += ShopItems.get_vanilla_shop_pool(self)

        if self.using_ut:   # can't this get moved to 'UniversalTracker.py' ?
            self.options.gerudo_fortress_key_ring.value = self.passthrough[
                "gerudo_fortress_key_ring"]
            self.options.forest_temple_key_ring.value = self.passthrough["forest_temple_key_ring"]
            self.options.fire_temple_key_ring.value = self.passthrough["fire_temple_key_ring"]
            self.options.water_temple_key_ring.value = self.passthrough["water_temple_key_ring"]
            self.options.spirit_temple_key_ring.value = self.passthrough["spirit_temple_key_ring"]
            self.options.shadow_temple_key_ring.value = self.passthrough["shadow_temple_key_ring"]
            self.options.bottom_of_the_well_key_ring.value = self.passthrough[
                "bottom_of_the_well_key_ring"]
            self.options.gerudo_training_ground_key_ring.value = self.passthrough[
                "gerudo_training_ground_key_ring"]
            self.options.ganons_castle_key_ring.value = self.passthrough["ganons_castle_key_ring"]

    def create_regions(self) -> None:
        create_regions_and_locations(self)
        place_locked_items(self)
        self.reserve_prefill_locations()
        for location in self.get_locations():
            location.name = str(location.name)
        for region in self.get_regions():
            region.name = str(region.name)

    def reserve_prefill_locations(self) -> None:
        DungeonRewardShuffle.reserve_dungeon_reward_locations(self)
        SongShuffle.reserve_song_locations(self)
        # Currently no reservations for key shuffle, 
        # we can't know for sure what locations will get used and reserving everything is too restrictive
        ShopItems.reserve_vanilla_shop_locations(self)

    def create_item(self, name: str, create_as_event: bool = False, classification: ItemClassification = None) -> SohItem:
        item_entry = Items(name)
        return SohItem(str(name), item_data_table[item_entry].classification if classification == None else classification,
                       None if create_as_event else item_data_table[item_entry].item_id, self.player)

    def get_pre_fill_items(self) -> list[Item]:
        return [self.create_item(item) for item in self.pre_fill_pool]

    def get_filler_item_name(self) -> str:
        return get_filler_item(self)

    def set_completion_rule(self) -> None:
        if not self.options.true_no_logic:
            # Actual completion condition.
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                Events.GAME_COMPLETED.value, self.player)

    def get_empty_locations_from_list_shuffled(self, location_list: list[Locations]) -> list[Location]:
        locations = []
        for location in location_list:
            loc = self.get_location(str(location))
            if loc.item != None or loc.locked:
                continue
            locations.append(loc)
        self.random.shuffle(locations)

        return locations

    def get_pre_fill_state(self) -> CollectionState:
        prefill_state = CollectionState(self.multiworld)
        for item in self.item_pool:
            prefill_state.collect(item, True)
        for item in self.pre_fill_pool:
            prefill_state.collect(self.create_item(item), True)
        prefill_state.sweep_for_advancements()
        return prefill_state
    
    def set_rules(self) -> None:
        # Set price rules in advance
        generate_shop_prices(self)
        generate_scrub_prices(self)
        generate_merchant_prices(self)
        set_price_rules(self)

        # disregard all rules if no logic is in effect
        if self.options.true_no_logic:
            for entrance in self.get_entrances():
                entrance.access_rule = lambda state: True
            for location in self.get_locations():
                location.access_rule = lambda state: True

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

        # Pre-Collect Extra Fire Temple Small Key
        if self.options.small_key_shuffle in ("vanilla", "own_dungeon"):
            self.multiworld.push_precollected(
                self.create_item(str(Items.FIRE_TEMPLE_SMALL_KEY), True))

        create_item_pool(self)

        if self.options.triforce_hunt:
            create_triforce_pieces(self)

        create_filler_item_pool(self)

        self.set_completion_rule()

    def pre_fill(self) -> None:
        original_completion_goal = self.multiworld.completion_condition[self.player]

        pre_fill_dungeon(self)
        pre_fill_songs(self)
        pre_fill_keys(self)
        fill_shop_items(self)

        self.multiworld.completion_condition[self.player] = original_completion_goal

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
            # type: ignore
            if state.soh_piece_of_heart_count[self.player] == 4:
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
            # type: ignore
            if state.soh_piece_of_heart_count[self.player] == -1:
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
            "shuffle_songs": self.options.shuffle_songs.value,
            "shuffle_skull_tokens": self.options.shuffle_skull_tokens.value,
            "skulls_sun_song": self.options.skulls_sun_song.value,
            "shuffle_kokiri_sword": self.options.shuffle_kokiri_sword.value,
            "shuffle_master_sword": self.options.shuffle_master_sword.value,
            "shuffle_childs_wallet": self.options.shuffle_childs_wallet.value,
            "shuffle_tycoon_wallet": self.options.shuffle_tycoon_wallet.value,
            "shuffle_ocarinas": self.options.shuffle_ocarina_buttons.value,
            "shuffle_ocarina_buttons": self.options.shuffle_ocarina_buttons.value,
            "shuffle_swim": self.options.shuffle_swim.value,
            "shuffle_gerudo_membership_card": self.options.shuffle_gerudo_membership_card.value,
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
            "merchant_prices": self.merchant_prices,
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
            "small_key_shuffle": self.options.small_key_shuffle.value,
            "gerudo_fortress_key_shuffle": self.options.gerudo_fortress_key_shuffle.value,
            "boss_key_shuffle": self.options.boss_key_shuffle.value,
            "key_rings": self.options.key_rings.value,
            "key_rings_count": self.options.key_rings_count.value,
            "gerudo_fortress_key_ring": self.options.gerudo_fortress_key_ring.value,
            "forest_temple_key_ring": self.options.forest_temple_key_ring.value,
            "fire_temple_key_ring": self.options.fire_temple_key_ring.value,
            "water_temple_key_ring": self.options.water_temple_key_ring.value,
            "spirit_temple_key_ring": self.options.spirit_temple_key_ring.value,
            "shadow_temple_key_ring": self.options.shadow_temple_key_ring.value,
            "bottom_of_the_well_key_ring": self.options.bottom_of_the_well_key_ring.value,
            "gerudo_training_ground_key_ring": self.options.gerudo_training_ground_key_ring.value,
            "ganons_castle_key_ring": self.options.ganons_castle_key_ring.value,
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
            "rocs_feather": self.options.rocs_feather.value,
            "infinite_upgrades": self.options.infinite_upgrades.value,
            "skeleton_key": self.options.skeleton_key.value,
            "slingbow_break_beehives": self.options.slingbow_break_beehives.value,
            "starting_age": self.options.starting_age.value,
            "shuffle_100_gs_reward": self.options.shuffle_100_gs_reward.value,
            "ice_trap_count": self.options.ice_trap_count.value,
            "ice_trap_filler_replacement": self.options.ice_trap_filler_replacement.value,
            "no_logic": self.options.true_no_logic.value,
            "apworld_version": self.apworld_version,
            "enable_all_tricks": self.options.enable_all_tricks.value,
            "tricks_in_logic": self.options.tricks_in_logic.value
        }
