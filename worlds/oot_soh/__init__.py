from typing import Dict, Any
from collections import deque

from BaseClasses import CollectionState, Item, Tutorial, MultiWorld
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World, LogicMixin
from .Items import SohItem, item_data_table, item_table, item_name_groups
from .Locations import location_table
from .Options import SohOptions
from .RegionAgeAccess import reset_age_access, update_age_access
from .Regions import create_regions_and_locations, place_locked_items
from .Enums import *
from .ItemPool import create_item_pool

import logging
import copy
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

class SohState(LogicMixin):
    def init_mixin(self, parent: MultiWorld):
        self._soh_stale = {player: True for player in parent.worlds.keys()
                            if parent.worlds[player].game == SohWorld.game}
        players = parent.get_game_groups(SohWorld.game) + parent.get_game_players(SohWorld.game)
        self._soh_child_reachable_regions = {player: set() for player in players}
        self._soh_adult_reachable_regions = {player: set() for player in players}
        self._soh_child_blocked_regions = {player: set() for player in players}
        self._soh_adult_blocked_regions = {player: set() for player in players}
        self._soh_age = {player: Ages.null for player in players}

    def copy_mixin(self, ret) -> CollectionState:
        ret._soh_stale = {player: stale for player, stale in self._soh_stale.items()}
        ret._soh_child_reachable_regions = {player: copy.copy(regions) for player, regions in self._soh_child_reachable_regions.items()}
        ret._soh_adult_reachable_regions = {player: copy.copy(regions) for player, regions in self._soh_adult_reachable_regions.items()}
        ret._soh_child_blocked_regions = {player: copy.copy(regions) for player, regions in self._soh_child_blocked_regions.items()}
        ret._soh_adult_blocked_regions = {player: copy.copy(regions) for player, regions in self._soh_adult_blocked_regions.items()}
        ret._soh_age = {player: age for player, age in self._soh_age.items()}
        return ret
    
    def _soh_invalidate(self, player):
        self._soh_child_reachable_regions[player] = set()
        self._soh_adult_reachable_regions[player] = set()
        self._soh_child_blocked_regions[player] = set()
        self._soh_adult_blocked_regions[player] = set()
        self._soh_stale[player] = True

    def _soh_update_age_reachable_regions(self, player):
        self._soh_stale[player] = False
        for age in [Ages.CHILD, Ages.ADULT]:
            self._soh_age[player] = age
            start = self.multiworld.get_region(Regions.ROOT, player)
            
            if age == Ages.CHILD:
                reachable = self._soh_child_reachable_regions[player]
                blocked = self._soh_child_blocked_regions[player]
                queue = deque(self._soh_child_blocked_regions[player])
            else:
                reachable = self._soh_adult_reachable_regions[player]
                blocked = self._soh_adult_blocked_regions[player]
                queue = deque(self._soh_adult_blocked_regions[player])

            # init on first call
            if start not in reachable:
                reachable.add(start)
                blocked.update(start.exits)
                queue.extend(start.exits)

            # run breadth first search
            while queue:
                connection = queue.popleft()
                new_region = connection.connected_region
                if new_region is None:
                    continue
                if new_region in reachable:
                    blocked.remove(connection)
                elif connection.can_reach(self):
                    reachable.add(new_region)
                    blocked.remove(connection)
                    blocked.update(new_region.exits)
                    queue.extend(new_region.exits)
                    self.path[new_region] = (new_region.name, self.path.get(connection, None))
    
    def _soh_can_reach_as_age(self, region: Regions, age: Ages, player: int): # Todo, type safety to age enum
        if self._soh_age[player] is Ages.null:
            # first layer of recursion
            self._soh_age[player] = age
            can_reach = self.multiworld.get_region(region.value, player).can_reach(self)
            self._soh_age[player] = Ages.null
            return can_reach
        return self._soh_age[player] == age



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
        self.included_locations = dict[str, int]()

    def generate_early(self) -> None:
        #input("\033[33m WARNING: Ship of Harkinian currently only supports SOME LOGIC! There may still be impossible generations. If you're OK with this, press Enter to continue. \033[0m")
        pass

    def create_item(self, name: str) -> SohItem:
        item_entry = Items(name)
        return SohItem(name, item_data_table[item_entry].classification, item_data_table[item_entry].item_id, self.player)

    def create_items(self) -> None:
        create_item_pool(self)

    def create_regions(self) -> None: 
        create_regions_and_locations(self)
        place_locked_items(self)

    def set_rules(self) -> None:
        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: state.has(Events.GAME_COMPLETED.value, self.player)

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
            "rainbow_bridge_stones_required": self.options.rainbow_bridge_stones_required.value,
            "rainbow_bridge_medallions_required": self.options.rainbow_bridge_medallions_required.value,
            "rainbow_bridge_dungeon_rewards_required": self.options.rainbow_bridge_dungeon_rewards_required.value,
            "rainbow_bridge_dungeons_required": self.options.rainbow_bridge_dungeons_required.value,
            "rainbow_bridge_skull_tokens_required": self.options.rainbow_bridge_skull_tokens_required.value,
            "ganons_trials_required": self.options.ganons_trials_required.value,
            "triforce_hunt": self.options.triforce_hunt.value,
            "triforce_hunt_required_pieces": self.options.triforce_hunt_required_pieces.value,
            "triforce_hunt_extra_pieces_percentage": self.options.triforce_hunt_extra_pieces_percentage.value,
            "shuffle_skull_tokens": self.options.shuffle_skull_tokens.value,
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
            "shuffle_merchants": self.options.shuffle_merchants.value,
            "shuffle_frog_song_rupees": self.options.shuffle_frog_song_rupees.value,
            "shuffle_adult_trade_items": self.options.shuffle_adult_trade_items.value,
            "shuffle_boss_souls": self.options.shuffle_boss_souls.value,
            "shuffle_fairies": self.options.shuffle_fairies.value,
            "shuffle_grass": self.options.shuffle_grass.value,
            "shuffle_dungeon_rewards": self.options.shuffle_dungeon_rewards.value,
            "maps_and_compasses": self.options.maps_and_compasses.value,
            "ganons_castle_boss_key": self.options.ganons_castle_boss_key.value,
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
        }
    
    def collect(self, state: CollectionState, item: Item) -> bool:
        # Temporarily disabled because logic is in progress
        #update_age_access(self, state)
        state._soh_stale[self.player] = True
        return super().collect(state, item)
    
    def remove(self, state: CollectionState, item: Item) -> bool:
        # Temporarily disabled because logic is in progress
        changed = super().remove(state, item)
        if changed:
            state._soh_invalidate(self.player)
        return changed

    def generate_output(self, output_directory: str):
    
        visualize_regions(self.multiworld.get_region(self.origin_region_name, self.player), f"SOH-Player{self.player}.puml",
                        show_entrance_names=True,
                        regions_to_highlight=self.multiworld.get_all_state().reachable_regions[
                            self.player])