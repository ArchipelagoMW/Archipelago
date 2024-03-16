import collections
import functools
import logging

from typing import Dict, Optional, Set, Tuple, Union

from .data.item_data import item_data, ZorkGrandInquisitorItemData
from .data.location_data import location_data, ZorkGrandInquisitorLocationData

from .data.missable_location_grant_conditions_data import (
    missable_location_grant_conditions_data,
    ZorkGrandInquisitorMissableLocationGrantConditionsData,
)

from .data_funcs import game_id_to_items, items_with_tag, locations_with_tag

from .enums import (
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorTags,
)

from .game_state_manager import GameStateManager


class GameController:
    logger: Optional[logging.Logger]

    game_state_manager: GameStateManager

    received_items: Set[ZorkGrandInquisitorItems]
    completed_locations: Set[ZorkGrandInquisitorLocations]

    completed_locations_queue: collections.deque
    received_items_queue: collections.deque

    all_hotspot_items: Set[ZorkGrandInquisitorItems]

    game_id_to_items: Dict[int, ZorkGrandInquisitorItems]

    possible_inventory_items: Set[ZorkGrandInquisitorItems]

    available_inventory_slots: Set[int]

    goal_completed: bool

    option_goal: Optional[ZorkGrandInquisitorGoals]
    option_deathsanity: Optional[bool]
    option_grant_missable_location_checks: Optional[bool]

    def __init__(self, logger=None) -> None:
        self.logger = logger

        self.game_state_manager = GameStateManager()

        self.received_items = set()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.all_hotspot_items = (
            items_with_tag(ZorkGrandInquisitorTags.HOTSPOT)
            | items_with_tag(ZorkGrandInquisitorTags.SUBWAY_DESTINATION)
            | items_with_tag(ZorkGrandInquisitorTags.TOTEMIZER_DESTINATION)
        )

        self.game_id_to_items = game_id_to_items()

        self.possible_inventory_items = (
            items_with_tag(ZorkGrandInquisitorTags.INVENTORY_ITEM)
            | items_with_tag(ZorkGrandInquisitorTags.SPELL)
            | items_with_tag(ZorkGrandInquisitorTags.TOTEM)
        )

        self.available_inventory_slots = set()

        self.goal_completed = False

        self.option_goal = None
        self.option_deathsanity = None
        self.option_grant_missable_location_checks = None

    @functools.cached_property
    def brog_items(self) -> Set[ZorkGrandInquisitorItems]:
        return {
            ZorkGrandInquisitorItems.BROGS_BICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_GRUE_EGG,
            ZorkGrandInquisitorItems.BROGS_PLANK,
        }

    @functools.cached_property
    def griff_items(self) -> Set[ZorkGrandInquisitorItems]:
        return {
            ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP,
            ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN,
        }

    @functools.cached_property
    def lucy_items(self) -> Set[ZorkGrandInquisitorItems]:
        return {
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4,
        }

    @property
    def totem_items(self) -> Set[ZorkGrandInquisitorItems]:
        return self.brog_items | self.griff_items | self.lucy_items

    @functools.cached_property
    def missable_locations(self) -> Set[ZorkGrandInquisitorLocations]:
        return locations_with_tag(ZorkGrandInquisitorTags.MISSABLE)

    def log(self, message) -> None:
        if self.logger:
            self.logger.info(message)

    def log_debug(self, message) -> None:
        if self.logger:
            self.logger.debug(message)

    def open_process_handle(self) -> bool:
        return self.game_state_manager.open_process_handle()

    def close_process_handle(self) -> bool:
        return self.game_state_manager.close_process_handle()

    def is_process_running(self) -> bool:
        return self.game_state_manager.is_process_running

    def list_received_brog_items(self) -> None:
        self.log("Received Brog Items:")

        self._process_received_items()
        received_brog_items: Set[ZorkGrandInquisitorItems] = self.received_items & self.brog_items

        if not len(received_brog_items):
            self.log("    Nothing")
            return

        for item in sorted(i.value for i in received_brog_items):
            self.log(f"    {item}")

    def list_received_griff_items(self) -> None:
        self.log("Received Griff Items:")

        self._process_received_items()
        received_griff_items: Set[ZorkGrandInquisitorItems] = self.received_items & self.griff_items

        if not len(received_griff_items):
            self.log("    Nothing")
            return

        for item in sorted(i.value for i in received_griff_items):
            self.log(f"    {item}")

    def list_received_lucy_items(self) -> None:
        self.log("Received Lucy Items:")

        self._process_received_items()
        received_lucy_items: Set[ZorkGrandInquisitorItems] = self.received_items & self.lucy_items

        if not len(received_lucy_items):
            self.log("    Nothing")
            return

        for item in sorted(i.value for i in received_lucy_items):
            self.log(f"    {item}")

    def list_received_hotspots(self) -> None:
        self.log("Received Hotspots:")

        self._process_received_items()

        hotspot_items: Set[ZorkGrandInquisitorItems] = items_with_tag(ZorkGrandInquisitorTags.HOTSPOT)
        received_hotspots: Set[ZorkGrandInquisitorItems] = self.received_items & hotspot_items

        if not len(received_hotspots):
            self.log("    Nothing")
            return

        for item in sorted(i.value for i in received_hotspots):
            self.log(f"    {item}")

    def update(self) -> None:
        if self.game_state_manager.is_process_still_running():
            try:
                self.game_state_manager.refresh_game_location()

                self._apply_permanent_game_state()
                self._apply_conditional_game_state()

                self._apply_permanent_game_flags()

                self._check_for_completed_locations()

                if self.option_grant_missable_location_checks:
                    self._check_for_missable_locations_to_grant()

                self._process_received_items()

                self._manage_hotspots()
                self._manage_items()

                self._apply_conditional_teleports()

                self._check_for_victory()
            except Exception as e:
                self.log_debug(e)

    def _apply_permanent_game_state(self) -> None:
        self._write_game_state_value_for(10934, 1)  # Rope Taken
        self._write_game_state_value_for(10418, 1)  # Mead Light Taken
        self._write_game_state_value_for(10275, 0)  # Lantern in Crate
        self._write_game_state_value_for(13929, 1)  # Great Underground Door Open
        self._write_game_state_value_for(13968, 1)  # Subway Token Taken
        self._write_game_state_value_for(12930, 1)  # Hammer Taken
        self._write_game_state_value_for(12935, 1)  # Griff Totem Taken
        self._write_game_state_value_for(12948, 1)  # ZIMDOR Scroll Taken
        self._write_game_state_value_for(4058, 1)  # Shovel Taken
        self._write_game_state_value_for(4059, 1)  # THROCK Scroll Taken
        self._write_game_state_value_for(11758, 1)  # KENDALL Scroll Taken
        self._write_game_state_value_for(16959, 1)  # Old Scratch Card Taken
        self._write_game_state_value_for(12840, 0)  # Zork Rocks in Perma-Suck Machine
        self._write_game_state_value_for(11886, 1)  # Student ID Taken
        self._write_game_state_value_for(16279, 1)  # Prozork Tablet Taken
        self._write_game_state_value_for(13260, 1)  # GOLGATEM Scroll Taken
        self._write_game_state_value_for(4834, 1)  # Flatheadia Fudge Taken
        self._write_game_state_value_for(4746, 1)  # Jar of Hotbugs Taken
        self._write_game_state_value_for(4755, 1)  # Hungus Lard Taken
        self._write_game_state_value_for(4758, 1)  # Mug Taken
        self._write_game_state_value_for(3716, 1)  # NARWILE Scroll Taken
        self._write_game_state_value_for(17147, 1)  # Lucy Totem Taken
        self._write_game_state_value_for(9818, 1)  # Middle Telegraph Hammer Taken
        self._write_game_state_value_for(3766, 0)  # ANS Scroll in Window
        self._write_game_state_value_for(4980, 0)  # ANS Scroll in Window
        self._write_game_state_value_for(3768, 0)  # GIV Scroll in Window
        self._write_game_state_value_for(4978, 0)  # GIV Scroll in Window
        self._write_game_state_value_for(3765, 0)  # SNA Scroll in Window
        self._write_game_state_value_for(4979, 0)  # SNA Scroll in Window
        self._write_game_state_value_for(3767, 0)  # VIG Scroll in Window
        self._write_game_state_value_for(4977, 0)  # VIG Scroll in Window
        self._write_game_state_value_for(15065, 1)  # Brog's Bickering Torch Taken
        self._write_game_state_value_for(15088, 1)  # Brog's Flickering Torch Taken
        self._write_game_state_value_for(2628, 4)  # Brog's Grue Eggs Taken
        self._write_game_state_value_for(2971, 1)  # Brog's Plank Taken
        self._write_game_state_value_for(1340, 1)  # Griff's Inflatable Sea Captain Taken
        self._write_game_state_value_for(1341, 1)  # Griff's Inflatable Raft Taken
        self._write_game_state_value_for(1477, 1)  # Griff's Air Pump Taken
        self._write_game_state_value_for(1814, 1)  # Griff's Dragon Tooth Taken
        self._write_game_state_value_for(15403, 0)  # Lucy's Cards Taken
        self._write_game_state_value_for(15404, 1)  # Lucy's Cards Taken
        self._write_game_state_value_for(15405, 4)  # Lucy's Cards Taken
        self._write_game_state_value_for(5222, 1)  # User Has Spell Book
        self._write_game_state_value_for(13930, 1)  # Skip Well Cutscenes
        self._write_game_state_value_for(19057, 1)  # Skip Well Cutscenes
        self._write_game_state_value_for(13934, 1)  # Skip Well Cutscenes
        self._write_game_state_value_for(13935, 1)  # Skip Well Cutscenes
        self._write_game_state_value_for(13384, 1)  # Skip Meanwhile... Cutscene
        self._write_game_state_value_for(8620, 1)  # First Coin Paid to Charon
        self._write_game_state_value_for(8731, 1)  # First Coin Paid to Charon

    def _apply_conditional_game_state(self):
        # Can teleport to Dungeon Master's Lair
        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR):
            self._write_game_state_value_for(2203, 1)
        else:
            self._write_game_state_value_for(2203, 0)

        # Can teleport to GUE Tech
        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH):
            self._write_game_state_value_for(7132, 1)
        else:
            self._write_game_state_value_for(7132, 0)

        # Can Teleport to Spell Lab
        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB):
            self._write_game_state_value_for(16545, 1)
        else:
            self._write_game_state_value_for(16545, 0)

        # Can Teleport to Hades
        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES):
            self._write_game_state_value_for(7119, 1)
        else:
            self._write_game_state_value_for(7119, 0)

        # Can Teleport to Monastery Station
        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY):
            self._write_game_state_value_for(7148, 1)
        else:
            self._write_game_state_value_for(7148, 0)

        # Initial Totemizer Destination
        should_force_initial_totemizer_destination: bool = True

        if self._player_has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION):
            should_force_initial_totemizer_destination = False
        elif self._player_has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL):
            should_force_initial_totemizer_destination = False
        elif self._player_has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY):
            should_force_initial_totemizer_destination = False
        elif self._player_has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ):
            should_force_initial_totemizer_destination = False

        if should_force_initial_totemizer_destination:
            self._write_game_state_value_for(9617, 2)

        # Pouch of Zorkmids
        if self._player_has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS):
            self._write_game_state_value_for(5827, 1)
        else:
            self._write_game_state_value_for(5827, 0)

        # Brog Torches
        if self._player_is_brog() and self._player_has(ZorkGrandInquisitorItems.BROGS_BICKERING_TORCH):
            self._write_game_state_value_for(10999, 1)
        else:
            self._write_game_state_value_for(10999, 0)

        if self._player_is_brog() and self._player_has(ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH):
            self._write_game_state_value_for(10998, 1)
        else:
            self._write_game_state_value_for(10998, 0)

        # Monastery Rope
        if ZorkGrandInquisitorLocations.I_HOPE_YOU_CAN_CLIMB_UP_THERE in self.completed_locations:
            self._write_game_state_value_for(9637, 1)

    def _apply_permanent_game_flags(self) -> None:
        self._write_game_flags_value_for(9437, 2)  # Monastery Exhibit Door to Outside
        self._write_game_flags_value_for(3074, 2)  # White House Door
        self._write_game_flags_value_for(13005, 2)  # Map
        self._write_game_flags_value_for(13006, 2)  # Sword
        self._write_game_flags_value_for(13007, 2)  # Sword
        self._write_game_flags_value_for(13389, 2)  # Moss of Mareilon
        self._write_game_flags_value_for(4301, 2)  # Quelbee Honeycomb
        self._write_game_flags_value_for(12895, 2)  # Change Machine Money
        self._write_game_flags_value_for(4150, 2)  # Prozorked Snapdragon
        self._write_game_flags_value_for(13413, 2)  # Letter Opener
        self._write_game_flags_value_for(15403, 2)  # Lucy's Cards

    def _check_for_completed_locations(self) -> None:
        location: ZorkGrandInquisitorLocations
        data: ZorkGrandInquisitorLocationData
        for location, data in location_data.items():
            if location in self.completed_locations or not isinstance(
                location, ZorkGrandInquisitorLocations
            ):
                continue

            is_location_completed: bool = True

            trigger: [Union[str, int]]
            value: Union[str, int, Tuple[int, ...]]
            for trigger, value in data.game_state_trigger:
                if trigger == "location":
                    if not self._player_is_at(value):
                        is_location_completed = False
                        break
                elif isinstance(trigger, int):
                    if isinstance(value, int):
                        if self._read_game_state_value_for(trigger) != value:
                            is_location_completed = False
                            break
                    elif isinstance(value, tuple):
                        if self._read_game_state_value_for(trigger) not in value:
                            is_location_completed = False
                            break
                    else:
                        is_location_completed = False
                        break
                else:
                    is_location_completed = False
                    break

            if is_location_completed:
                self.completed_locations.add(location)
                self.completed_locations_queue.append(location)

    def _check_for_missable_locations_to_grant(self) -> None:
        missable_location: ZorkGrandInquisitorLocations
        for missable_location in self.missable_locations:
            if missable_location in self.completed_locations:
                continue

            data: ZorkGrandInquisitorLocationData = location_data[missable_location]

            if ZorkGrandInquisitorTags.DEATHSANITY in data.tags and not self.option_deathsanity:
                continue

            condition_data: ZorkGrandInquisitorMissableLocationGrantConditionsData = (
                missable_location_grant_conditions_data.get(missable_location)
            )

            if condition_data is None:
                self.log_debug(f"Missable Location {missable_location.value} has no grant conditions")
                continue

            if condition_data.location_condition in self.completed_locations:
                grant_location: bool = True

                item: ZorkGrandInquisitorItems
                for item in condition_data.item_conditions or tuple():
                    if self._player_doesnt_have(item):
                        grant_location = False
                        break

                if grant_location:
                    self.completed_locations_queue.append(missable_location)

    def _process_received_items(self) -> None:
        while len(self.received_items_queue) > 0:
            item: ZorkGrandInquisitorItems = self.received_items_queue.popleft()
            data: ZorkGrandInquisitorItemData = item_data[item]

            if ZorkGrandInquisitorTags.FILLER in data.tags:
                continue

            self.received_items.add(item)

    def _manage_hotspots(self) -> None:
        hotspot_item: ZorkGrandInquisitorItems
        for hotspot_item in self.all_hotspot_items:
            data: ZorkGrandInquisitorItemData = item_data[hotspot_item]

            if hotspot_item not in self.received_items:
                key: int
                for key in data.statemap_keys:
                    self._write_game_flags_value_for(key, 2)
            else:
                if hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_666_MAILBOX:
                    if self.game_state_manager.game_location == "hp5g":
                        if self._read_game_state_value_for(9113) == 0:
                            self._write_game_flags_value_for(9116, 0)
                        else:
                            self._write_game_flags_value_for(9116, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS:
                    if self.game_state_manager.game_location == "qb2g":
                        if self._read_game_state_value_for(15433) == 0:
                            self._write_game_flags_value_for(15434, 0)
                        else:
                            self._write_game_flags_value_for(15434, 2)

                        if self._read_game_state_value_for(15435) == 0:
                            self._write_game_flags_value_for(15436, 0)
                        else:
                            self._write_game_flags_value_for(15436, 2)

                        if self._read_game_state_value_for(15437) == 0:
                            self._write_game_flags_value_for(15438, 0)
                        else:
                            self._write_game_flags_value_for(15438, 2)

                        if self._read_game_state_value_for(15439) == 0:
                            self._write_game_flags_value_for(15440, 0)
                        else:
                            self._write_game_flags_value_for(15440, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX:
                    if self.game_state_manager.game_location == "tp2g":
                        if self._read_game_state_value_for(12095) == 1:
                            self._write_game_flags_value_for(9115, 2)
                        else:
                            self._write_game_flags_value_for(9115, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_BLINDS:
                    if self.game_state_manager.game_location == "dv1e":
                        if self._read_game_state_value_for(4743) == 0:
                            self._write_game_flags_value_for(4799, 0)
                        else:
                            self._write_game_flags_value_for(4799, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS:
                    if self.game_state_manager.game_location == "tr5g":
                        key: int
                        for key in data.statemap_keys:
                            self._write_game_flags_value_for(key, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT:
                    if self.game_state_manager.game_location == "tr5g":
                        self._write_game_flags_value_for(12702, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT:
                    if self.game_state_manager.game_location == "tr5m":
                        self._write_game_flags_value_for(12909, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT:
                    if self.game_state_manager.game_location == "tr5j":
                        if self._read_game_state_value_for(12892) == 0:
                            self._write_game_flags_value_for(12900, 0)
                        else:
                            self._write_game_flags_value_for(12900, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR:
                    if self.game_state_manager.game_location == "dw1e":
                        if self._read_game_state_value_for(4983) == 0:
                            self._write_game_flags_value_for(5010, 0)
                        else:
                            self._write_game_flags_value_for(5010, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT:
                    if self.game_state_manager.game_location == "me2j":
                        if self._read_game_state_value_for(9491) == 2:
                            self._write_game_flags_value_for(9539, 0)
                        else:
                            self._write_game_flags_value_for(9539, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER:
                    if self.game_state_manager.game_location == "me2j":
                        if self._read_game_state_value_for(9546) == 2 or self._read_game_state_value_for(9419) == 1:
                            self._write_game_flags_value_for(19712, 2)
                        else:
                            self._write_game_flags_value_for(19712, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT:
                    if self.game_state_manager.game_location == "sg1f":
                        self._write_game_flags_value_for(2586, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER:
                    if self.game_state_manager.game_location == "th3j":
                        five_is_open: bool = self._read_game_state_value_for(11847) == 1
                        six_is_open: bool = self._read_game_state_value_for(11840) == 1
                        seven_is_open: bool = self._read_game_state_value_for(11841) == 1
                        eight_is_open: bool = self._read_game_state_value_for(11848) == 1

                        rocks_in_six: bool = self._read_game_state_value_for(11769) == 1
                        six_blasted: bool = self._read_game_state_value_for(11770) == 1

                        if five_is_open or six_is_open or seven_is_open or eight_is_open or rocks_in_six or six_blasted:
                            self._write_game_flags_value_for(11878, 2)
                        else:
                            self._write_game_flags_value_for(11878, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND:
                    if self.game_state_manager.game_location == "te5e":
                        if self._read_game_state_value_for(11747) == 0:
                            self._write_game_flags_value_for(11751, 0)
                        else:
                            self._write_game_flags_value_for(11751, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH:
                    if self.game_state_manager.game_location == "pe2e":
                        self._write_game_flags_value_for(15147, 0)
                        self._write_game_flags_value_for(15153, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW:
                    if self.game_state_manager.game_location == "cd70":
                        self._write_game_flags_value_for(1705, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS:
                    if self.game_state_manager.game_location == "cd3h":
                        raft_in_left: bool = self._read_game_state_value_for(1301) == 1
                        raft_in_right: bool = self._read_game_state_value_for(1304) == 1
                        raft_inflated: bool = self._read_game_state_value_for(1379) == 1

                        captain_in_left: bool = self._read_game_state_value_for(1374) == 1
                        captain_in_right: bool = self._read_game_state_value_for(1381) == 1
                        captain_inflated: bool = self._read_game_state_value_for(1378) == 1

                        left_inflated: bool = (raft_in_left and raft_inflated) or (captain_in_left and captain_inflated)

                        right_inflated: bool = (raft_in_right and raft_inflated) or (
                                captain_in_right and captain_inflated
                        )

                        if left_inflated:
                            self._write_game_flags_value_for(1425, 2)
                        else:
                            self._write_game_flags_value_for(1425, 0)

                        if right_inflated:
                            self._write_game_flags_value_for(1426, 2)
                        else:
                            self._write_game_flags_value_for(1426, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE:
                    if self.game_state_manager.game_location == "uc3e":
                        if self._read_game_state_value_for(13060) == 0:
                            self._write_game_flags_value_for(13106, 0)
                        else:
                            self._write_game_flags_value_for(13106, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS:
                    if self.game_state_manager.game_location == "ue1e":
                        if self._read_game_state_value_for(14318) == 0:
                            self._write_game_flags_value_for(13219, 0)
                            self._write_game_flags_value_for(13220, 0)
                            self._write_game_flags_value_for(13221, 0)
                            self._write_game_flags_value_for(13222, 0)
                        else:
                            self._write_game_flags_value_for(13219, 2)
                            self._write_game_flags_value_for(13220, 2)
                            self._write_game_flags_value_for(13221, 2)
                            self._write_game_flags_value_for(13222, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS:
                    if self.game_state_manager.game_location == "ue1e":
                        if self._read_game_state_value_for(14318) == 0:
                            self._write_game_flags_value_for(14327, 0)
                            self._write_game_flags_value_for(14332, 0)
                            self._write_game_flags_value_for(14337, 0)
                            self._write_game_flags_value_for(14342, 0)
                        else:
                            self._write_game_flags_value_for(14327, 2)
                            self._write_game_flags_value_for(14332, 2)
                            self._write_game_flags_value_for(14337, 2)
                            self._write_game_flags_value_for(14342, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT:
                    if self.game_state_manager.game_location == "tr5e":
                        self._write_game_flags_value_for(12528, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS:
                    if self.game_state_manager.game_location == "tr5e":
                        if self._read_game_state_value_for(12220) == 0:
                            self._write_game_flags_value_for(12523, 2)
                            self._write_game_flags_value_for(12524, 2)
                            self._write_game_flags_value_for(12525, 2)
                        else:
                            self._write_game_flags_value_for(12523, 0)
                            self._write_game_flags_value_for(12524, 0)
                            self._write_game_flags_value_for(12525, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE:
                    if self.game_state_manager.game_location == "uc1g":
                        if self._read_game_state_value_for(12931) == 1 or self._read_game_state_value_for(12929) == 1:
                            self._write_game_flags_value_for(13002, 2)
                        else:
                            self._write_game_flags_value_for(13002, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL:
                    if self.game_state_manager.game_location == "pe5e":
                        if self._read_game_state_value_for(10277) == 0:
                            self._write_game_flags_value_for(10726, 0)
                        else:
                            self._write_game_flags_value_for(10726, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR:
                    if self.game_state_manager.game_location == "tr1k":
                        if self._read_game_state_value_for(12212) == 0:
                            self._write_game_flags_value_for(12280, 0)
                        else:
                            self._write_game_flags_value_for(12280, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_GRASS:
                    if self.game_state_manager.game_location in ("te10", "te1g", "te20", "te30", "te40"):
                        key: int
                        for key in data.statemap_keys:
                            self._write_game_flags_value_for(key, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS:
                    if self.game_state_manager.game_location == "hp1e":
                        if self._read_game_state_value_for(8431) == 1:
                            key: int
                            for key in data.statemap_keys:
                                self._write_game_flags_value_for(key, 0)
                        else:
                            key: int
                            for key in data.statemap_keys:
                                self._write_game_flags_value_for(key, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER:
                    if self.game_state_manager.game_location == "hp1e":
                        if self._read_game_state_value_for(8431) == 1:
                            self._write_game_flags_value_for(8446, 2)
                        else:
                            self._write_game_flags_value_for(8446, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HARRY:
                    if self.game_state_manager.game_location == "dg4e":
                        if self._read_game_state_value_for(4237) == 1 and self._read_game_state_value_for(4034) == 1:
                            self._write_game_flags_value_for(4260, 2)
                        else:
                            self._write_game_flags_value_for(4260, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY:
                    if self.game_state_manager.game_location == "dg4h":
                        if self._read_game_state_value_for(4279) == 1:
                            self._write_game_flags_value_for(18026, 2)
                        else:
                            self._write_game_flags_value_for(18026, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH:
                    if self.game_state_manager.game_location == "dg4g":
                        if self._read_game_state_value_for(4034) == 1:
                            self._write_game_flags_value_for(17623, 2)
                        else:
                            self._write_game_flags_value_for(17623, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR:
                    if self.game_state_manager.game_location == "uc4e":
                        if self._read_game_state_value_for(13062) == 1:
                            self._write_game_flags_value_for(13140, 2)
                        else:
                            self._write_game_flags_value_for(13140, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR:
                    if self.game_state_manager.game_location == "pe1e":
                        if self._read_game_state_value_for(10451) == 1:
                            self._write_game_flags_value_for(10441, 2)
                        else:
                            self._write_game_flags_value_for(10441, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_LOUDSPEAKER_VOLUME_BUTTONS:
                    if self.game_state_manager.game_location == "pe2j":
                        self._write_game_flags_value_for(19632, 0)
                        self._write_game_flags_value_for(19627, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR:
                    if self.game_state_manager.game_location == "sw4e":
                        if self._read_game_state_value_for(2989) == 1:
                            self._write_game_flags_value_for(3025, 2)
                        else:
                            self._write_game_flags_value_for(3025, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG:
                    if self.game_state_manager.game_location == "sw4e":
                        self._write_game_flags_value_for(3036, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MIRROR:
                    if self.game_state_manager.game_location == "dw1f":
                        self._write_game_flags_value_for(5031, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MONASTERY_VENT:
                    if self.game_state_manager.game_location == "um1e":
                        if self._read_game_state_value_for(9637) == 0:
                            self._write_game_flags_value_for(13597, 0)
                        else:
                            self._write_game_flags_value_for(13597, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE:
                    if self.game_state_manager.game_location == "ue2g":
                        if self._read_game_state_value_for(13278) == 0:
                            self._write_game_flags_value_for(13390, 0)
                        else:
                            self._write_game_flags_value_for(13390, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR:
                    if self.game_state_manager.game_location == "qe1e":
                        if self._player_is_brog():
                            self._write_game_flags_value_for(2447, 0)
                        elif self._player_is_griff():
                            self._write_game_flags_value_for(2455, 0)
                        elif self._player_is_lucy():
                            if self._read_game_state_value_for(2457) == 0:
                                self._write_game_flags_value_for(2455, 0)
                            else:
                                self._write_game_flags_value_for(2455, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS:
                    if self.game_state_manager.game_location == "tr3h":
                        if self._read_game_state_value_for(11777) == 1:
                            self._write_game_flags_value_for(12389, 2)
                        else:
                            self._write_game_flags_value_for(12389, 0)

                        self._write_game_state_value_for(12390, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE:
                    if self.game_state_manager.game_location == "dg4f":
                        if self._read_game_state_value_for(4241) == 1:
                            self._write_game_flags_value_for(4302, 2)
                        else:
                            self._write_game_flags_value_for(4302, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE:
                    if self.game_state_manager.game_location == "tp1e":
                        if self._read_game_state_value_for(16342) == 1:
                            self._write_game_flags_value_for(16383, 2)
                            self._write_game_flags_value_for(16384, 2)
                        else:
                            self._write_game_flags_value_for(16383, 0)
                            self._write_game_flags_value_for(16384, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE:
                    if self.game_state_manager.game_location == "sg6e":
                        if self._read_game_state_value_for(15715) == 1:
                            self._write_game_flags_value_for(2769, 2)
                        else:
                            self._write_game_flags_value_for(2769, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON:
                    if self.game_state_manager.game_location == "dg2f":
                        if self._read_game_state_value_for(4114) == 1 or self._read_game_state_value_for(4115) == 1:
                            self._write_game_flags_value_for(4149, 2)
                        else:
                            self._write_game_flags_value_for(4149, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS:
                    if self.game_state_manager.game_location == "tr5f":
                        self._write_game_flags_value_for(12584, 0)
                        self._write_game_flags_value_for(12585, 0)
                        self._write_game_flags_value_for(12586, 0)
                        self._write_game_flags_value_for(12587, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT:
                    if self.game_state_manager.game_location == "tr5f":
                        self._write_game_flags_value_for(12574, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT:
                    if self.game_state_manager.game_location == "ue2j":
                        if self._read_game_state_value_for(13408) == 1:
                            self._write_game_flags_value_for(13412, 2)
                        else:
                            self._write_game_flags_value_for(13412, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER:
                    if self.game_state_manager.game_location == "tp4g":
                        self._write_game_flags_value_for(12170, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM:
                    if self.game_state_manager.game_location == "tp1e":
                        if self._read_game_state_value_for(16342) == 1 and self._read_game_state_value_for(16374) == 0:
                            self._write_game_flags_value_for(16382, 0)
                        else:
                            self._write_game_flags_value_for(16382, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM:
                    if self.game_state_manager.game_location == "dg3e":
                        self._write_game_flags_value_for(4209, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE:
                    if self.game_state_manager.game_location == "th3r":
                        self._write_game_flags_value_for(11973, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT:
                    if self.game_state_manager.game_location == "uc6e":
                        self._write_game_flags_value_for(13168, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY:
                    if self.game_state_manager.game_location == "qb2e":
                        if self._read_game_state_value_for(15395) == 1:
                            self._write_game_flags_value_for(15396, 2)
                        else:
                            self._write_game_flags_value_for(15396, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH:
                    if self.game_state_manager.game_location == "mt2e":
                        self._write_game_flags_value_for(9706, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS:
                    if self.game_state_manager.game_location == "mt2g":
                        self._write_game_flags_value_for(9728, 0)
                        self._write_game_flags_value_for(9729, 0)
                        self._write_game_flags_value_for(9730, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_WELL:
                    if self.game_state_manager.game_location == "pc1e":
                        self._write_game_flags_value_for(10314, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM:
                    if self.game_state_manager.game_location == "us2e":
                        self._write_game_flags_value_for(13757, 0)
                    elif self.game_state_manager.game_location == "ue2e":
                        self._write_game_flags_value_for(13297, 0)
                    elif self.game_state_manager.game_location == "uh2e":
                        self._write_game_flags_value_for(13486, 0)
                    elif self.game_state_manager.game_location == "um2e":
                        self._write_game_flags_value_for(13625, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES:
                    if self.game_state_manager.game_location == "us2e":
                        self._write_game_flags_value_for(13758, 0)
                    elif self.game_state_manager.game_location == "ue2e":
                        self._write_game_flags_value_for(13309, 0)
                    elif self.game_state_manager.game_location == "uh2e":
                        self._write_game_flags_value_for(13498, 0)
                    elif self.game_state_manager.game_location == "um2e":
                        self._write_game_flags_value_for(13637, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY:
                    if self.game_state_manager.game_location == "us2e":
                        self._write_game_flags_value_for(13759, 0)
                    elif self.game_state_manager.game_location == "ue2e":
                        self._write_game_flags_value_for(13316, 0)
                    elif self.game_state_manager.game_location == "uh2e":
                        self._write_game_flags_value_for(13505, 0)
                    elif self.game_state_manager.game_location == "um2e":
                        self._write_game_flags_value_for(13644, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION:
                    if self.game_state_manager.game_location == "mt1f":
                        self._write_game_flags_value_for(9660, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY:
                    if self.game_state_manager.game_location == "mt1f":
                        self._write_game_flags_value_for(9666, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL:
                    if self.game_state_manager.game_location == "mt1f":
                        self._write_game_flags_value_for(9668, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ:
                    if self.game_state_manager.game_location == "mt1f":
                        self._write_game_flags_value_for(9662, 0)

    def _manage_items(self) -> None:
        if self._player_is_afgncaap():
            self.available_inventory_slots = self._determine_available_inventory_slots()

            received_inventory_items: Set[ZorkGrandInquisitorItems]
            received_inventory_items = self.received_items & self.possible_inventory_items

            received_inventory_items = self._filter_received_inventory_items(received_inventory_items)
        elif self._player_is_totem():
            self.available_inventory_slots = self._determine_available_inventory_slots(is_totem=True)

            received_inventory_items: Set[ZorkGrandInquisitorItems]

            if self._player_is_brog():
                received_inventory_items = self.received_items & self.brog_items
                received_inventory_items = self._filter_received_brog_inventory_items(received_inventory_items)
            elif self._player_is_griff():
                received_inventory_items = self.received_items & self.griff_items
                received_inventory_items = self._filter_received_griff_inventory_items(received_inventory_items)
            elif self._player_is_lucy():
                received_inventory_items = self.received_items & self.lucy_items
                received_inventory_items = self._filter_received_lucy_inventory_items(received_inventory_items)
            else:
                return None
        else:
            return None

        game_state_inventory_items: Set[ZorkGrandInquisitorItems] = self._determine_game_state_inventory()

        inventory_items_to_remove: Set[ZorkGrandInquisitorItems]
        inventory_items_to_remove = game_state_inventory_items - received_inventory_items

        inventory_items_to_add: Set[ZorkGrandInquisitorItems]
        inventory_items_to_add = received_inventory_items - game_state_inventory_items

        item: ZorkGrandInquisitorItems
        for item in inventory_items_to_remove:
            self._remove_from_inventory(item)

        item: ZorkGrandInquisitorItems
        for item in inventory_items_to_add:
            self._add_to_inventory(item)

        # Item Deduplication (Just in Case)
        seen_items: Set[int] = set()

        i: int
        for i in range(151, 171):
            item: int = self._read_game_state_value_for(i)

            if item in seen_items:
                self._write_game_state_value_for(i, 0)
            else:
                seen_items.add(item)

    def _apply_conditional_teleports(self) -> None:
        if self._player_is_at("uw1x"):
            self.game_state_manager.set_game_location("uw10", 0)

        if self._player_is_at("uw1k") and self._read_game_state_value_for(13938) == 0:
            self.game_state_manager.set_game_location("pc10", 250)

        if self._player_is_at("ue1q"):
            self.game_state_manager.set_game_location("ue1e", 0)

        if self._player_is_at("ej10"):
            self.game_state_manager.set_game_location("uc10", 1200)

        if self._read_game_state_value_for(9) == 224:
            self._write_game_state_value_for(9, 0)
            self.game_state_manager.set_game_location("uc10", 1200)

    def _check_for_victory(self) -> None:
        if self.option_goal == ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
            coconut_is_placed = self._read_game_state_value_for(2200) == 1
            cube_is_placed = self._read_game_state_value_for(2322) == 1
            skull_is_placed = self._read_game_state_value_for(2321) == 1

            self.goal_completed = coconut_is_placed and cube_is_placed and skull_is_placed

    def _determine_game_state_inventory(self) -> Set[ZorkGrandInquisitorItems]:
        game_state_inventory: Set[ZorkGrandInquisitorItems] = set()

        # Item on Cursor
        item_on_cursor: int = self._read_game_state_value_for(9)

        if item_on_cursor != 0:
            if item_on_cursor in self.game_id_to_items:
                game_state_inventory.add(self.game_id_to_items[item_on_cursor])

        # Item in Inspector
        item_in_inspector: int = self._read_game_state_value_for(4512)

        if item_in_inspector != 0:
            if item_in_inspector in self.game_id_to_items:
                game_state_inventory.add(self.game_id_to_items[item_in_inspector])

        # Items in Inventory Slots
        i: int
        for i in range(151, 171):
            if self._read_game_state_value_for(i) != 0:
                if self._read_game_state_value_for(i) in self.game_id_to_items:
                    game_state_inventory.add(
                        self.game_id_to_items[self._read_game_state_value_for(i)]
                    )

        # Pouch of Zorkmids
        if self._read_game_state_value_for(5827) == 1:
            game_state_inventory.add(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS)

        # Spells
        i: int
        for i in range(191, 203):
            if self._read_game_state_value_for(i) == 1:
                if i in self.game_id_to_items:
                    game_state_inventory.add(self.game_id_to_items[i])

        # Totems
        if self._read_game_state_value_for(4853) == 1:
            game_state_inventory.add(ZorkGrandInquisitorItems.TOTEM_BROG)

        if self._read_game_state_value_for(4315) == 1:
            game_state_inventory.add(ZorkGrandInquisitorItems.TOTEM_GRIFF)

        if self._read_game_state_value_for(5223) == 1:
            game_state_inventory.add(ZorkGrandInquisitorItems.TOTEM_LUCY)

        return game_state_inventory

    def _add_to_inventory(self, item: ZorkGrandInquisitorItems) -> None:
        if item == ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS:
            return None

        data: ZorkGrandInquisitorItemData = item_data[item]

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            if len(self.available_inventory_slots):  # Inventory slot overflow protection
                inventory_slot: int = self.available_inventory_slots.pop()
                self._write_game_state_value_for(inventory_slot, data.statemap_keys[0])
        elif ZorkGrandInquisitorTags.SPELL in data.tags:
            self._write_game_state_value_for(data.statemap_keys[0], 1)
        elif ZorkGrandInquisitorTags.TOTEM in data.tags:
            self._write_game_state_value_for(data.statemap_keys[0], 1)

    def _remove_from_inventory(self, item: ZorkGrandInquisitorItems) -> None:
        if item == ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS:
            return None

        data: ZorkGrandInquisitorItemData = item_data[item]

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            inventory_slot: Optional[int] = self._inventory_slot_for(item)

            if inventory_slot is None:
                return None

            self._write_game_state_value_for(inventory_slot, 0)

            if inventory_slot != 9:
                self.available_inventory_slots.add(inventory_slot)
        elif ZorkGrandInquisitorTags.SPELL in data.tags:
            self._write_game_state_value_for(data.statemap_keys[0], 0)
        elif ZorkGrandInquisitorTags.TOTEM in data.tags:
            self._write_game_state_value_for(data.statemap_keys[0], 0)

    def _determine_available_inventory_slots(self, is_totem: bool = False) -> Set[int]:
        available_inventory_slots: Set[int] = set()

        inventory_slot_range_end: int = 171

        if is_totem:
            if self._player_is_brog():
                inventory_slot_range_end = 161
            elif self._player_is_griff():
                inventory_slot_range_end = 160
            elif self._player_is_lucy():
                inventory_slot_range_end = 157

        i: int
        for i in range(151, inventory_slot_range_end):
            if self._read_game_state_value_for(i) == 0:
                available_inventory_slots.add(i)

        return available_inventory_slots

    def _inventory_slot_for(self, item) -> Optional[int]:
        data: ZorkGrandInquisitorItemData = item_data[item]

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            i: int
            for i in range(151, 171):
                if self._read_game_state_value_for(i) == data.statemap_keys[0]:
                    return i

        if self._read_game_state_value_for(9) == data.statemap_keys[0]:
            return 9

        if self._read_game_state_value_for(4512) == data.statemap_keys[0]:
            return 4512

        return None

    def _filter_received_inventory_items(
        self, received_inventory_items: Set[ZorkGrandInquisitorItems]
    ) -> Set[ZorkGrandInquisitorItems]:
        to_filter_inventory_items: Set[ZorkGrandInquisitorItems] = self.totem_items

        inventory_item_values: Set[int] = set()

        i: int
        for i in range(151, 171):
            inventory_item_values.add(self._read_game_state_value_for(i))

        cursor_item_value: int = self._read_game_state_value_for(9)
        inspector_item_value: int = self._read_game_state_value_for(4512)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        item: ZorkGrandInquisitorItems
        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.FLATHEADIA_FUDGE:
                if self._read_game_state_value_for(4766) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4869) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.HUNGUS_LARD:
                if self._read_game_state_value_for(4870) == 1:
                    to_filter_inventory_items.add(item)
                elif (
                    self._read_game_state_value_for(4244) == 1
                    and self._read_game_state_value_for(4309) == 0
                ):
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.JAR_OF_HOTBUGS:
                if self._read_game_state_value_for(4750) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4869) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LANTERN:
                if self._read_game_state_value_for(10477) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(5221) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER:
                if self._read_game_state_value_for(9491) == 3:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MAP:
                if self._read_game_state_value_for(16618) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MEAD_LIGHT:
                if 105 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(17620) > 0:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4034) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MOSS_OF_MAREILON:
                if self._read_game_state_value_for(4763) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4869) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MUG:
                if self._read_game_state_value_for(4772) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4869) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.OLD_SCRATCH_CARD:
                if 32 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(12892) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.PERMA_SUCK_MACHINE:
                if self._read_game_state_value_for(12218) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER:
                if self._read_game_state_value_for(15150) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(10421) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.PROZORK_TABLET:
                if self._read_game_state_value_for(4115) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.QUELBEE_HONEYCOMB:
                if self._read_game_state_value_for(4769) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4869) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.ROPE:
                if 22 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif 111 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif (
                    self._read_game_state_value_for(10304) == 1
                    and not self._read_game_state_value_for(13938) == 1
                ):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15150) == 83:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS:
                if 41 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif 98 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(201) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV:
                if 48 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif 98 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(201) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SNAPDRAGON:
                if self._read_game_state_value_for(4199) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.STUDENT_ID:
                if self._read_game_state_value_for(11838) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SUBWAY_TOKEN:
                if self._read_game_state_value_for(13167) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SWORD:
                if 22 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif 100 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif 111 in inventory_item_values:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.ZIMDOR_SCROLL:
                if 105 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(17620) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4034) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.ZORK_ROCKS:
                if self._read_game_state_value_for(12486) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(12487) == 1:
                    to_filter_inventory_items.add(item)
                elif 52 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(11769) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(11840) == 1:
                    to_filter_inventory_items.add(item)

        return received_inventory_items - to_filter_inventory_items

    def _filter_received_brog_inventory_items(
        self, received_inventory_items: Set[ZorkGrandInquisitorItems]
    ) -> Set[ZorkGrandInquisitorItems]:
        to_filter_inventory_items: Set[ZorkGrandInquisitorItems] = set()

        inventory_item_values: Set[int] = set()

        i: int
        for i in range(151, 161):
            inventory_item_values.add(self._read_game_state_value_for(i))

        cursor_item_value: int = self._read_game_state_value_for(9)
        inspector_item_value: int = self._read_game_state_value_for(2194)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        item: ZorkGrandInquisitorItems
        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.BROGS_BICKERING_TORCH:
                if 103 in inventory_item_values:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH:
                if 104 in inventory_item_values:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.BROGS_GRUE_EGG:
                if self._read_game_state_value_for(2577) == 1:
                    to_filter_inventory_items.add(item)
                elif 71 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(2641) == 1:
                    to_filter_inventory_items.add(item)

        return received_inventory_items - to_filter_inventory_items

    def _filter_received_griff_inventory_items(
        self, received_inventory_items: Set[ZorkGrandInquisitorItems]
    ) -> Set[ZorkGrandInquisitorItems]:
        to_filter_inventory_items: Set[ZorkGrandInquisitorItems] = set()

        inventory_item_values: Set[int] = set()

        i: int
        for i in range(151, 160):
            inventory_item_values.add(self._read_game_state_value_for(i))

        cursor_item_value: int = self._read_game_state_value_for(9)
        inspector_item_value: int = self._read_game_state_value_for(4512)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        item: ZorkGrandInquisitorItems
        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT:
                if self._read_game_state_value_for(1301) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(1304) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(16562) == 1:
                    to_filter_inventory_items.add(item)
            if item == ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN:
                if self._read_game_state_value_for(1374) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(1381) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(16562) == 1:
                    to_filter_inventory_items.add(item)

        return received_inventory_items - to_filter_inventory_items

    def _filter_received_lucy_inventory_items(
        self, received_inventory_items: Set[ZorkGrandInquisitorItems]
    ) -> Set[ZorkGrandInquisitorItems]:
        to_filter_inventory_items: Set[ZorkGrandInquisitorItems] = set()

        inventory_item_values: Set[int] = set()

        i: int
        for i in range(151, 157):
            inventory_item_values.add(self._read_game_state_value_for(i))

        cursor_item_value: int = self._read_game_state_value_for(9)
        inspector_item_value: int = self._read_game_state_value_for(2198)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        item: ZorkGrandInquisitorItems
        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1:
                if 120 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15433) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15435) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15437) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15439) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15472) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2:
                if 121 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15433) == 2:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15435) == 2:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15437) == 2:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15439) == 2:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15472) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3:
                if 122 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15433) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15435) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15437) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15439) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15472) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4:
                if 123 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15433) in (4, 5):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15435) in (4, 5):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15437) in (4, 5):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15439) in (4, 5):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15472) == 1:
                    to_filter_inventory_items.add(item)

        return received_inventory_items - to_filter_inventory_items

    def _read_game_state_value_for(self, key: int) -> Optional[int]:
        try:
            return self.game_state_manager.read_game_state_value_for(key)
        except Exception as e:
            self.log_debug(f"Exception: {e} while trying to read game state key '{key}'")
            raise e

    def _write_game_state_value_for(self, key: int, value: int) -> Optional[bool]:
        try:
            return self.game_state_manager.write_game_state_value_for(key, value)
        except Exception as e:
            self.log_debug(f"Exception: {e} while trying to write '{key} = {value}' to game state")
            raise e

    def _read_game_flags_value_for(self, key: int) -> Optional[int]:
        try:
            return self.game_state_manager.read_game_flags_value_for(key)
        except Exception as e:
            self.log_debug(f"Exception: {e} while trying to read game flags key '{key}'")
            raise e

    def _write_game_flags_value_for(self, key: int, value: int) -> Optional[bool]:
        try:
            return self.game_state_manager.write_game_flags_value_for(key, value)
        except Exception as e:
            self.log_debug(f"Exception: {e} while trying to write '{key} = {value}' to game flags")
            raise e

    def _player_has(self, item: ZorkGrandInquisitorItems) -> bool:
        return item in self.received_items

    def _player_doesnt_have(self, item: ZorkGrandInquisitorItems) -> bool:
        return item not in self.received_items

    def _player_is_at(self, game_location: str) -> bool:
        return self.game_state_manager.game_location == game_location

    def _player_is_afgncaap(self) -> bool:
        return self._read_game_state_value_for(1596) == 1

    def _player_is_totem(self) -> bool:
        return self._player_is_brog() or self._player_is_griff() or self._player_is_lucy()

    def _player_is_brog(self) -> bool:
        return self._read_game_state_value_for(1520) == 1

    def _player_is_griff(self) -> bool:
        return self._read_game_state_value_for(1296) == 1

    def _player_is_lucy(self) -> bool:
        return self._read_game_state_value_for(1524) == 1
