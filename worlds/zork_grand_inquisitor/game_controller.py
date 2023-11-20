import collections

from .data.item_data import item_data
from .data.location_data import location_data

from .data_funcs import game_id_to_items, items_with_tag

from .enums import (
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorTags,
)

from .game_state_manager import GameStateManager


### PROBLEMS / TODO
# Need Repro: Dying in Old Scratch caused Plants are mans best friend to be completed and game crash
#   Maybe only when done on the surface without dalboz? Not reproduced in DML

# 2 Ropes sometimes... after messing with sword + rope? Minor?

# Subway token conditionals are not working properly
# Still a problem with hungus lard and plug in out states. It disappears after plugging it and taking it ouj
# Possible to do messy stuff with sword / map that are supposed to disappear after glass breaks. Clicking fast on them
# Map needs duplication prevention

# Detect when the game is not running and prompt to /zork again

class GameController:
    def __init__(self, logger=None):
        self.logger = logger

        self.game_state_manager = GameStateManager()

        self.received_items = set()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.game_id_to_items = game_id_to_items()

        self.possible_inventory_items = (
            items_with_tag(ZorkGrandInquisitorTags.INVENTORY_ITEM)
            | items_with_tag(ZorkGrandInquisitorTags.SPELL)
            | items_with_tag(ZorkGrandInquisitorTags.TOTEM)
        )

        self.available_inventory_slots = set()

        self.goal_completed = False

        self.option_goal = None
        self.option_deathsanity = False

    def log(self, message):
        if self.logger:
            self.logger.info(message)

    def open_process_handle(self):
        return self.game_state_manager.open_process_handle()

    def close_process_handle(self):
        return self.game_state_manager.close_process_handle()

    def update(self):
        if self.game_state_manager.is_process_running:
            self.game_state_manager.refresh_game_location()

            self._apply_permanent_game_state()
            self._apply_conditional_game_state()

            self._check_for_completed_locations()
            self._manage_items()

            self._apply_conditional_teleports()

            self._check_for_victory()

    def _apply_permanent_game_state(self):
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
        self._write_game_state_value_for(12896, 0)  # Change Machine Full
        self._write_game_state_value_for(12533, 1)  # Ice Cream Sandwitch Taken
        self._write_game_state_value_for(12840, 0)  # Zork Rocks in Perma-Suck Machine
        self._write_game_state_value_for(11886, 1)  # Student ID Taken
        self._write_game_state_value_for(16279, 1)  # Prozork Tablet Taken
        self._write_game_state_value_for(13414, 1)  # Letter Opener Taken
        self._write_game_state_value_for(13279, 1)  # Moss of Mareilon Taken
        self._write_game_state_value_for(13260, 1)  # GOLGATEM Scroll Taken
        self._write_game_state_value_for(4834, 1)  # Flatheadia Fudge Taken
        self._write_game_state_value_for(4746, 1)  # Jar of Hotbugs Taken
        self._write_game_state_value_for(4755, 1)  # Hungus Lard Taken
        self._write_game_state_value_for(4758, 1)  # Mug Taken
        self._write_game_state_value_for(4321, 1)  # Quelbee Honeycomb Taken
        self._write_game_state_value_for(3716, 1)  # NARWILE Scroll Taken
        self._write_game_state_value_for(2495, 1)  # GLORF Scroll Taken
        self._write_game_state_value_for(2986, 1)  # Envelope Taken
        self._write_game_state_value_for(17147, 1)  # Lucy Totem Taken
        self._write_game_state_value_for(9818, 1)  # Middle Telegraph Hammer Taken

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

        # Subway Destinations
        subway_destination = max(
            (
                self._read_game_state_value_for(13825),  # Crossroads Platform
                self._read_game_state_value_for(13307),  # Flood Control Dam Platform
                self._read_game_state_value_for(13496),  # Hades Platform
                self._read_game_state_value_for(13635),  # Monastery Platform
            )
        )

        if subway_destination == 6 and self._player_doesnt_have(
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM
        ):
            self._write_game_state_value_for(13825, 0)
            self._write_game_state_value_for(13307, 0)
            self._write_game_state_value_for(13496, 0)
            self._write_game_state_value_for(13635, 0)
        elif subway_destination == 11 and self._player_doesnt_have(
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY
        ):
            self._write_game_state_value_for(13825, 0)
            self._write_game_state_value_for(13307, 0)
            self._write_game_state_value_for(13496, 0)
            self._write_game_state_value_for(13635, 0)
        elif subway_destination == 8 and self._player_doesnt_have(
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES
        ):
            self._write_game_state_value_for(13825, 0)
            self._write_game_state_value_for(13307, 0)
            self._write_game_state_value_for(13496, 0)
            self._write_game_state_value_for(13635, 0)

        # Pouch of Zorkmids
        if self._player_has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS):
            self._write_game_state_value_for(5827, 1)
        else:
            self._write_game_state_value_for(5827, 0)

        # Blank Scroll Box Access
        if self._player_has(ZorkGrandInquisitorItems.UNLOCKED_BLANK_SCROLL_BOX_ACCESS):
            self._write_game_state_value_for(12095, 0)
        else:
            self._write_game_state_value_for(12095, 1)

        # Brog's Time Tunnel Items
        if self._player_has(ZorkGrandInquisitorItems.REVEALED_BROGS_TIME_TUNNEL_ITEMS):
            self._write_game_state_value_for(15065, 0)
            self._write_game_state_value_for(15088, 0)
            self._write_game_state_value_for(2628, 0)
        else:
            self._write_game_state_value_for(15065, 1)
            self._write_game_state_value_for(15088, 1)
            self._write_game_state_value_for(2628, 4)

        # Griff's Time Tunnel Items
        if self._player_has(ZorkGrandInquisitorItems.REVEALED_GRIFFS_TIME_TUNNEL_ITEMS):
            self._write_game_state_value_for(1340, 0)
            self._write_game_state_value_for(1341, 0)
            self._write_game_state_value_for(1477, 0)
            self._write_game_state_value_for(1814, 0)
        else:
            self._write_game_state_value_for(1340, 1)
            self._write_game_state_value_for(1341, 1)
            self._write_game_state_value_for(1477, 1)
            self._write_game_state_value_for(1814, 1)

        # Lucy's Time Tunnel Items
        if self._player_has(ZorkGrandInquisitorItems.REVEALED_LUCYS_TIME_TUNNEL_ITEMS):
            self._write_game_state_value_for(15405, 5)
        else:
            self._write_game_state_value_for(15405, 0)

        # Sword and Map Taken After Glass Broken
        if self._read_game_state_value_for(12931) == 1:
            self._write_game_state_value_for(12933, 1)
            self._write_game_state_value_for(12932, 1)

        # Snapdragon Taken After Prozorked
        if self._read_game_state_value_for(4115) == 1:
            self._write_game_state_value_for(4114, 1)

    def _check_for_completed_locations(self):
        for location, data in location_data.items():
            if (
                location in self.completed_locations
                or type(location) != ZorkGrandInquisitorLocations
            ):
                continue

            is_location_completed = True

            for trigger, value in data.game_state_trigger:
                if trigger == "location":
                    if not self._player_is_at(value):
                        is_location_completed = False
                        break
                elif type(trigger) == int:
                    if type(value) == int:
                        if self._read_game_state_value_for(trigger) != value:
                            is_location_completed = False
                            break
                    elif type(value) == tuple:
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
                self.completed_locations_queue.append(location)

    def _manage_items(self):
        # Process Queue
        while len(self.received_items_queue) > 0:
            item = self.received_items_queue.popleft()

            if ZorkGrandInquisitorTags.FILLER in item_data[item].tags:
                continue

            self.received_items.add(item)
        # Manage Inventory Items
        if self._player_is_afgncaap():
            self.available_inventory_slots = self._determine_available_inventory_slots()

            received_inventory_items = self.received_items & self.possible_inventory_items
            received_inventory_items = self._filter_received_inventory_items(
                received_inventory_items
            )

            game_state_inventory_items = self._determine_game_state_inventory()

            inventory_items_to_add = received_inventory_items - game_state_inventory_items
            inventory_items_to_remove = game_state_inventory_items - received_inventory_items

            for item in inventory_items_to_add:
                self._add_to_inventory(item)

            for item in inventory_items_to_remove:
                self._remove_from_inventory(item)

    def _apply_conditional_teleports(self):
        if self._player_is_at("uw1k") and self._read_game_state_value_for(13938) == 0:
            self.game_state_manager.set_game_location("pc10", 250)

        if self._player_is_at("ej10"):
            self.game_state_manager.set_game_location("uc10", 1200)

    def _check_for_victory(self):
        if self.option_goal == ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
            coconut_is_placed = self._read_game_state_value_for(2200) == 1
            cube_is_placed = self._read_game_state_value_for(2322) == 1
            skull_is_placed = self._read_game_state_value_for(2321) == 1

            self.goal_completed = coconut_is_placed and cube_is_placed and skull_is_placed

    def _determine_game_state_inventory(self):
        game_state_inventory = set()

        # Item on Cursor
        item_on_cursor = self._read_game_state_value_for(9)

        if item_on_cursor != 0:
            if item_on_cursor in self.game_id_to_items:
                game_state_inventory.add(self.game_id_to_items[item_on_cursor])

        # Item in Inspector
        item_in_inspector = self._read_game_state_value_for(4512)

        if item_in_inspector != 0:
            if item_in_inspector in self.game_id_to_items:
                game_state_inventory.add(self.game_id_to_items[item_in_inspector])

        # Items in Inventory Slots
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

    def _add_to_inventory(self, item):
        if item == ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS:
            return None

        data = item_data[item]

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            inventory_slot = self.available_inventory_slots.pop()
            self._write_game_state_value_for(inventory_slot, data.game_state_keys[0])
        elif ZorkGrandInquisitorTags.SPELL in data.tags:
            self._write_game_state_value_for(data.game_state_keys[0], 1)
        elif ZorkGrandInquisitorTags.TOTEM in data.tags:
            self._write_game_state_value_for(data.game_state_keys[0], 1)

    def _remove_from_inventory(self, item):
        if item == ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS:
            return None

        data = item_data[item]

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            inventory_slot = self._inventory_slot_for(item)

            if inventory_slot is None:
                return None

            self._write_game_state_value_for(inventory_slot, 0)

            if inventory_slot != 9:
                self.available_inventory_slots.add(inventory_slot)
        elif ZorkGrandInquisitorTags.SPELL in data.tags:
            self._write_game_state_value_for(data.game_state_keys[0], 0)
        elif ZorkGrandInquisitorTags.TOTEM in data.tags:
            self._write_game_state_value_for(data.game_state_keys[0], 0)

    def _determine_available_inventory_slots(self):
        available_inventory_slots = set()

        for i in range(151, 171):
            if self._read_game_state_value_for(i) == 0:
                available_inventory_slots.add(i)

        return available_inventory_slots

    def _inventory_slot_for(self, item):
        data = item_data[item]

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            for i in range(151, 171):
                if self._read_game_state_value_for(i) == data.game_state_keys[0]:
                    return i

        if self._read_game_state_value_for(9) == data.game_state_keys[0]:
            return 9

        if self._read_game_state_value_for(4512) == data.game_state_keys[0]:
            return 4512

        return None

    def _filter_received_inventory_items(self, received_inventory_items):
        to_filter_inventory_items = set()

        inventory_item_values = set()

        for i in range(151, 171):
            inventory_item_values.add(self._read_game_state_value_for(i))

        cursor_item_value = self._read_game_state_value_for(9)
        inspector_item_value = self._read_game_state_value_for(4512)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.FLATHEADIA_FUDGE:
                if self._read_game_state_value_for(4766) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.HUNGUS_LARD:
                if self._read_game_state_value_for(4870) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4309) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.JAR_OF_HOTBUGS:
                if self._read_game_state_value_for(4750) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LANTERN:
                if self._read_game_state_value_for(10477) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(5221) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER:
                if self._read_game_state_value_for(9491) == 3:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MEAD_LIGHT:
                if self._read_game_state_value_for(17620) > 0:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4034) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MOSS_OF_MAREILON:
                if self._read_game_state_value_for(4763) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MUG:
                if self._read_game_state_value_for(4772) == 1:
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
            elif item == ZorkGrandInquisitorItems.SNAPDRAGON:
                if self._read_game_state_value_for(4199) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.STUDENT_ID:
                if self._read_game_state_value_for(11838) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SUBWAY_TOKEN:
                if self._read_game_state_value_for(13163) == 2:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SWORD:
                if 22 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif 100 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif 111 in inventory_item_values:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.ZIMDOR_SCROLL:
                if self._read_game_state_value_for(17620) == 3:
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

    def _read_game_state_value_for(self, key):
        try:
            return self.game_state_manager.read_game_state_value_for(key)[0]
        except Exception as e:
            self.log(f"Exception: {e} while trying to read {key}")

        return False

    def _write_game_state_value_for(self, key, value):
        try:
            return self.game_state_manager.write_game_state_value_for(key, value)
        except Exception as e:
            self.log(f"Exception: {e} while trying to write {key} = {value}")

        return False

    def _player_has(self, item):
        return item in self.received_items

    def _player_doesnt_have(self, item):
        return item not in self.received_items

    def _player_is_at(self, game_location):
        return self.game_state_manager.game_location == game_location

    def _player_is_afgncaap(self):
        return self._read_game_state_value_for(1596) == 1
