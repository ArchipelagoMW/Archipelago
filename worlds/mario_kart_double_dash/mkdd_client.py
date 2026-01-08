import asyncio
import random
import time
import traceback
from typing import TYPE_CHECKING, Any, Optional

import dolphin_memory_engine as dolphin

import Utils
from CommonClient import get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from . import game_data, items, locations, patches, mem_addresses, ar_codes, version, options
from .locations import MkddLocationData
from .items import ItemType, MkddItemData

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import (TrackerCommandProcessor as ClientCommandProcessor,
                                              TrackerGameContext as CommonContext, UT_VERSION)
    tracker_loaded = True
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext


if TYPE_CHECKING:
    import kvui

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a ROM for Mario Kart Double Dash (USA). Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Mario Kart Double Dash is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

class MkddCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for Mario Kart Double Dash client commands.

    This class handles commands specific to Mario Kart Double Dash.
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """Display the current Dolphin emulator connection status."""
        if isinstance(self.ctx, MkddContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")
    
    def _cmd_unlocked(self) -> None:
        """Show list of unlocked items."""
        if isinstance(self.ctx, MkddContext):
            logger.info(f"Trophies: {self.ctx.trophies}/{self.ctx.trophy_goal}")
            logger.info(f"Unlocked characters: {", ".join([game_data.CHARACTERS[c].name for c in self.ctx.unlocked_characters])}")
            logger.info(f"Unlocked karts (upgrades): {", ".join([f"{game_data.KARTS[c].name} ({(
                ", ".join(u.name for u in self.ctx.kart_upgrades[c]))})" for c in self.ctx.unlocked_karts])}")
            logger.info(f"Speed upgrades: {self.ctx.engine_upgrade_level}")
            logger.info(f"Max vehicle class: {["50cc", "100cc", "150cc", "Mirror"][self.ctx.unlocked_vehicle_class]}")
            logger.info(f"Unlocked cups: {", ".join([game_data.CUPS[c] for c in self.ctx.unlocked_cups])}")
            logger.info(f"Unlocked time trial courses: {", ".join([game_data.COURSES[c].name for c in self.ctx.unlocked_courses])}")
            logger.info("Unlocked item box items:")
            if len(self.ctx.global_items) > 0:
                logger.info(f"Everybody: {", ".join([item.name for item in self.ctx.global_items])}")
            for character, items in self.ctx.character_items.items():
                if len(items) > 0:
                   logger.info(f"{character.name}: {", ".join([item.name for item in items])}")


class MkddContext(CommonContext):
    """
    The context for Mario Kart Double Dash client.

    This class manages all interactions with the Dolphin emulator and the Archipelago server for Mario Kart Double Dash.
    """

    command_processor = MkddCommandProcessor
    game: str = "Mario Kart Double Dash"
    items_handling: int = 0b111

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        """
        Initialize the Mkdd context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)
        # Client data.
        self.items_received_2: list[tuple[NetworkItem, int]] = []
        self.last_item_handled: int = -1
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.last_rcvd_index: int = -1
        self.has_send_death: bool = False
        self.victory_sent: bool = False

        self.message_queue: list[str] = []
        self.message_time_left: int = 0

        self.memory_addresses = mem_addresses.MkddMemAddressesUsa

        # Options.
        self.goal: options.Goal
        self.trophy_goal: int
        self.all_cup_tour_length: int
        self.cups_courses: list[list[int]]
        self.mirror_200cc: bool
        self.lap_counts: dict[str, int]

        # Game data.
        self.victory: bool = False
        self.trophies: int = 0

        self.last_race_timer: int = 0
        self.last_in_game: bool = False

        self.race_counter: int = 0
        self.course_changed_time: int = 0

        self.unlocked_vehicle_class: int = 0
        self.last_selected_vehicle_class: int = 0

        self.unlocked_characters: list[int] = []
        self.unlocked_karts: list[int] = []
        self.engine_upgrade_level = 0
        self.kart_upgrades: dict[int, list[game_data.KartUpgrade]] = {i:[] for i, _ in enumerate(game_data.KARTS)}

        self.unlocked_cups: list[int] = []
        self.last_selected_cup: int = 0

        self.unlocked_cup_skips: int = 0
        
        self.unlocked_courses: list[int] = []
        self.last_selected_course: int = 0
        
        self.time_trial_items: int = 0

        # These are per player.
        self.last_selected_character: list[int] = [0 for _ in range(4)]
        self.last_selected_kart: list[int] = [0 for _ in range(4)]

        self.active_characters: list[game_data.Character] = [game_data.CHARACTERS[0], game_data.CHARACTERS[0]]
        self.active_kart: game_data.Kart = game_data.KARTS[0]
        
        self.character_item_total_weights: dict[str, list[int]] = {}
        self.global_items_total_weights: list[int] = []
        self.character_items: dict[game_data.Character, list[game_data.Item]] = {character:[] for character in game_data.CHARACTERS}
        self.global_items: list[game_data.Item] = []

        # Name of the current stage as read from the game's memory. Sent to trackers whenever its value changes to
        # facilitate automatically switching to the map of the current stage.
        self.current_course: game_data.Course = game_data.Course()

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        self.auth = None
        self.current_course = game_data.Course()
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if password_requested and not self.password:
            await super(MkddContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        if cmd == "Connected":
            self.items_received_2 = []
            self.last_rcvd_index = -1
            slot_data: dict = args.get("slot_data")
            if "death_link" in slot_data:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
            
            self.trophy_goal = slot_data.get("trophy_requirement")
            self.cups_courses = slot_data["cups_courses"]
            self.all_cup_tour_length = slot_data.get("all_cup_tour_length", 8)
            self.mirror_200cc = bool(slot_data.get("mirror_200cc"))
            self.lap_counts = slot_data.get("lap_counts")

            self.character_item_total_weights = slot_data.get("character_item_total_weights")
            self.global_items_total_weights = slot_data.get("global_items_total_weights")

            host_version = slot_data.get("version")
            if host_version != version.get_str():
                logger.warning(
                    f"The seed was generated using version {host_version} of MKDDAP.\n" +
                    f"The client is using version {version.get_str()}.\n" +
                    "If there are any issues, consider changing your client to matching version."
                )
            sync_state(self)
        elif cmd == "ReceivedItems":
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_received_2.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_received_2.sort(key=lambda v: v[1])
        elif cmd == "Retrieved":
            requested_keys_dict = args["keys"]
        elif cmd == "PrintJSON":
            if args.get("type") == "ItemSend":
                to_player: int = args["receiving"]
                nw_item: NetworkItem = args["item"]
                from_player: int = nw_item.player
                item_name: str = self.item_names.lookup_in_slot(nw_item.item, to_player)
                if to_player == self.slot and from_player == self.slot:
                    queue_ingame_message(self, f"You found your\n{item_name}")
                elif to_player == self.slot:
                    from_player_name: str = self.player_names[from_player]
                    queue_ingame_message(self, f"{from_player_name} found your\n{item_name}")
                elif from_player == self.slot:
                    to_player_name: str = self.player_names[to_player]
                    queue_ingame_message(self, f"You found {to_player_name}'s\n{item_name}")
        # Relay packages to the tracker also.
        super().on_package(cmd, args)

    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        super().on_deathlink(data)
        _give_death(self)

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for Mario Kart Double Dash client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = f"Archipelago Mario Kart Double Dash Client {version.get_str()}"
        if tracker_loaded:
            ui.base_title += f" | Universal Tracker {UT_VERSION}"
        ui.base_title +=  " | Archipelago v"
        return ui

###### Dolphin connection ######
def _apply_ar_code(code: list[int]):
    for i in range(0, len(code), 2):
        command = (code[i] & 0xFE00_0000) >> 24
        address = (code[i] & 0x01FF_FFFF) | 0x8000_0000
        if command == 0x04:
            dolphin.write_word(address, code[i + 1])


def _apply_dict_patch(code: dict[int, list[int]]):
    for start_address, rows in code.items():
        address = start_address
        for row in rows:
            dolphin.write_word(address, row)
            address += 4


def apply_patch(ctx: MkddContext):
    _apply_dict_patch(patches.patch)
    _apply_ar_code(ar_codes.lap_modifier)
    _apply_ar_code(ar_codes.gp_course_selection)
    logger.info("Patch Applied.")


def sync_state(ctx: MkddContext) -> None:
    """
    Sets game state to match client data about unlocks.

    :param ctx: Mario Kart Double Dash client context.
    """
    for character in range(len(game_data.CHARACTERS)):
        dolphin.write_byte(
            ctx.memory_addresses.available_characters_bx + character,
            int(character in ctx.unlocked_characters)
        )
    for k in range(len(game_data.KARTS)):
        kart = game_data.KARTS[k]
        dolphin.write_byte(
            ctx.memory_addresses.available_karts_bx + kart.unlock_id,
            int(k in ctx.unlocked_karts)
        )
    dolphin.write_word(ctx.memory_addresses.max_vehicle_class_w, ctx.unlocked_vehicle_class)
    dolphin.write_bytes(ctx.memory_addresses.tt_items_bx, game_data.TT_ITEM_TABLE[ctx.time_trial_items])


def _give_death(ctx: MkddContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: Mario Kart Double Dash client context.
    """
    if (
        ctx.slot is not None
        and dolphin.is_hooked()
        and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
        and check_ingame()
    ):
        ctx.has_send_death = True
        # TODO: Add death link.


def _give_item(ctx: MkddContext, item: MkddItemData) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: Mario Kart Double Dash client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    if item.item_type == ItemType.CHARACTER:
        dolphin.write_byte(ctx.memory_addresses.available_characters_bx + item.address, 1)
        ctx.unlocked_characters.append(item.address)
    
    elif item.item_type == ItemType.KART:
        kart = game_data.KARTS[item.address]
        dolphin.write_byte(ctx.memory_addresses.available_karts_bx + kart.unlock_id, 1)
        ctx.unlocked_karts.append(item.address)
    
    elif item.item_type == ItemType.KART_UPGRADE:
        ctx.kart_upgrades[item.address].append(item.meta)
    
    elif item.name == items.PROGRESSIVE_ENGINE:
        ctx.engine_upgrade_level += 1
    
    elif item.item_type == ItemType.CUP:
        ctx.unlocked_cups.append(item.address)
    
    elif item.item_type == ItemType.TT_COURSE:
        ctx.unlocked_courses.append(item.address)
    
    elif item.name == items.PROGRESSIVE_CLASS:
        ctx.unlocked_vehicle_class = min(ctx.unlocked_vehicle_class + 1, 3)
        dolphin.write_word(ctx.memory_addresses.max_vehicle_class_w, ctx.unlocked_vehicle_class)
    
    elif item.name == items.PROGRESSIVE_CUP_SKIP:
        ctx.unlocked_cup_skips = min(ctx.unlocked_cup_skips + 1, 3)
    
    elif item.name == items.PROGRESSIVE_TIME_TRIAL_ITEM:
        ctx.time_trial_items = min(ctx.time_trial_items + 1, len(game_data.TT_ITEM_TABLE) - 1)
        dolphin.write_bytes(ctx.memory_addresses.tt_items_bx, game_data.TT_ITEM_TABLE[ctx.time_trial_items])
    
    elif item.item_type == ItemType.ITEM_UNLOCK:
        if item.meta["character"] == None:
            ctx.global_items.append(item.meta["item"])
        else:
            ctx.character_items[item.meta["character"]].append(item.meta["item"])

    elif item.name == items.TROPHY:
        ctx.trophies += 1
    
    elif item.name == items.VICTORY:
        ctx.victory = True
    
    return True


async def give_items(ctx: MkddContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: Mario Kart Double Dash client context.
    """
    # Loop through items to give.
    for item, idx in ctx.items_received_2:
        # If the item's index is greater than the player's expected index, give the player the item.
        if ctx.last_item_handled < idx:
            # Attempt to give the item and increment the expected index.
            while not _give_item(ctx, items.data_table[item.item]):
                await asyncio.sleep(0.01)

            # Increment the expected index.
            ctx.last_item_handled = idx


async def check_locations(ctx: MkddContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: Mario Kart Double Dash client context.
    """
    new_location_names: set[str] = set()

    if ctx.trophies >= ctx.trophy_goal:
        new_location_names.add(locations.TROPHY_GOAL)
    
    mode: int = dolphin.read_word(ctx.memory_addresses.mode_w)
    cup: str = game_data.CUPS[dolphin.read_word(ctx.memory_addresses.cup_w)]
    menu_course: int = dolphin.read_word(ctx.memory_addresses.menu_course_w)
    vehicle_class: int = dolphin.read_word(ctx.memory_addresses.vehicle_class_w)
    current_lap: int = dolphin.read_word(ctx.memory_addresses.current_lap_wx)
    # Get placement and modify it to be 0-based for less confusion (rankings are also 0-based).
    in_race_placement: int = dolphin.read_word(ctx.memory_addresses.in_race_placement_wx) - 1
    current_course_ranking: int = dolphin.read_word(ctx.memory_addresses.current_course_ranking_w)
    total_ranking: int = dolphin.read_word(ctx.memory_addresses.total_ranking_w)
    total_points: int = dolphin.read_word(ctx.memory_addresses.total_points_wx)
    game_ticks: int = dolphin.read_word(ctx.memory_addresses.game_ticks_w)
    race_timer: int = dolphin.read_word(ctx.memory_addresses.race_timer_w)
    # Remove 181 frame headstart and convert to seconds.
    # Close enough (to 1/10th of a second), altough probably exact formula should be investigated.
    race_timer_s: float = (race_timer - 181) / 60

    # Some ways to check what state is the game in. In game in particular has to have one frame
    # leeway in case we read finishing state after the last frame advance has happened.
    new_in_game: bool = race_timer - ctx.last_race_timer > 0 # From countdown to finish.
    in_game: bool = new_in_game or ctx.last_in_game
    ctx.last_in_game = new_in_game
    course_loaded: bool = game_ticks > ctx.course_changed_time + 60 # Don't give checks in menus etc.
    ctx.last_race_timer = race_timer

    # Course finishing related locations.
    # For Time Trials check against default lap counts.
    if in_game and current_lap >= ctx.current_course.laps:
        if mode == game_data.Modes.TIMETRIAL:
            new_location_names.add(locations.get_loc_name_finish(ctx.current_course.name))
            if race_timer_s < ctx.current_course.good_time:
                new_location_names.add(locations.get_loc_name_good_time(ctx.current_course))
            if race_timer_s < ctx.current_course.staff_time:
                new_location_names.add(locations.get_loc_name_ghost(ctx.current_course.name))

    # For Grand Prix use possible custom lap counts.
    if in_game and current_lap >= ctx.lap_counts.get(ctx.current_course.name, 3):
        if mode == game_data.Modes.GRANDPRIX:
            new_location_names.add(locations.get_loc_name_finish(ctx.current_course.name))
            if in_race_placement == 0:
                new_location_names.add(locations.get_loc_name_first(ctx.current_course.name))

                # Win with default character pairs.
                character1 = min(c.id for c in ctx.active_characters)
                character2 = max(c.id for c in ctx.active_characters)
                if character1 % 2 == 0 and character1 + 1 == character2:
                    new_location_names.add(locations.get_loc_name_win_characters(
                        game_data.CHARACTERS[character1].name, game_data.CHARACTERS[character2].name
                    ))

                # Win with default character + kart combination.
                for character in ctx.active_characters:
                    kart = game_data.KARTS[character.default_kart]
                    if ctx.active_kart == kart:
                        new_location_names.add(locations.get_loc_name_win_char_kart(character.name, kart.name))
                
                # Win with course owner.
                owner_count = 0
                for character in ctx.current_course.owners:
                    if game_data.CHARACTERS[character] in ctx.active_characters:
                        owner_count += 1
                    if owner_count == len(ctx.current_course.owners):
                        new_location_names.add(locations.get_loc_name_win_course_char(ctx.current_course))
            
    if mode == game_data.Modes.GRANDPRIX and current_lap > 0 and in_race_placement == 0 and in_game:
        new_location_names.add(locations.get_loc_name_lead(ctx.current_course.name))

    # Cup related locations.
    if mode == game_data.Modes.CEREMONY:
        if cup == game_data.CUPS[game_data.CUP_ALL_CUP_TOUR]:
            if total_ranking == 0:
                new_location_names.add(locations.WIN_ALL_CUP_TOUR)
        else:
            new_location_names.add(locations.get_loc_name_finish(cup))
            # Bronze or better. Add all variants that are considered easier than current (ie. 50 bronze for 150 gold finish).
            if total_ranking <= 2:
                for r in range(2, total_ranking - 1, -1):
                    for c in range(vehicle_class + 1):
                        new_location_names.add(locations.get_loc_name_cup(cup, r, c))
                        if r == 0:
                            new_location_names.add(locations.get_loc_name_trophy(cup, c))
            # Gold for various vehicles.
            if total_ranking == 0:
                if ctx.active_kart.weight == 0:
                    new_location_names.add(locations.GOLD_LIGHT)
                elif ctx.active_kart.weight == 1:
                    new_location_names.add(locations.GOLD_MEDIUM)
                elif ctx.active_kart.weight == 2:
                    new_location_names.add(locations.GOLD_HEAVY)
                elif ctx.active_kart.weight == -1:
                    new_location_names.add(locations.GOLD_PARADE)
            
            if total_points == 40:
                new_location_names.add(locations.get_loc_name_perfect(cup))
        
    new_locations = {locations.name_to_id.get(loc_name) for loc_name in new_location_names}
    new_locations.discard(None)
    ctx.locations_checked.update(new_locations)
    # Send the list of newly-checked locations to the server.
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


def check_finished(ctx: MkddContext) -> bool:
    current_race: int = dolphin.read_word(ctx.memory_addresses.race_counter_w)
    if current_race > ctx.race_counter:
        ctx.race_counter = current_race
        return True
    else:
        return False


def update_game(ctx: MkddContext) -> None:
    """
    Update game state such as controlling character selection.

    :param ctx: Mario Kart Double Dash client context.
    """
    _apply_ar_code(ar_codes.unlock_everything)
    
    text_s: list[str] = ["" for _ in range(ctx.memory_addresses.text_amount)]
    text_x: list[int] = [0 for _ in range(ctx.memory_addresses.text_amount)]
    text_y: list[int] = [0 for _ in range(ctx.memory_addresses.text_amount)]
    text_j: list[int] = [1 for _ in range(ctx.memory_addresses.text_amount)]

    menu_pointer = dolphin.read_word(ctx.memory_addresses.menu_pointer)
    if menu_pointer != 0:
        driver = dolphin.read_word(menu_pointer + ctx.memory_addresses.menu_driver_w_offset)
        rider = dolphin.read_word(menu_pointer + ctx.memory_addresses.menu_rider_w_offset)
        # Save active selections for printing info.
        p1_character: game_data.Character | None = None
        p2_character: game_data.Character | None = None
        p1_kart: game_data.Kart | None = None
        # Save selections for later use (when menu pointer becomes invalid).
        if driver >= 0 and driver < len(game_data.CHARACTERS):
            ctx.active_characters[0] = game_data.CHARACTERS[driver]
            p1_character = ctx.active_characters[0]
        if rider >= 0 and rider < len(game_data.CHARACTERS):
            ctx.active_characters[1] = game_data.CHARACTERS[rider]
            p2_character = ctx.active_characters[1]
        
        for player in range(4):
            player_offset = player * ctx.memory_addresses.menu_player_struct_size
            character: int = int(dolphin.read_word(menu_pointer + ctx.memory_addresses.menu_character_w_offset + player_offset))
            kart: int = int(dolphin.read_word(menu_pointer + ctx.memory_addresses.menu_kart_w_offset + player_offset))
            
            if character >= 0 and character < len(game_data.CHARACTERS):
                if player == 0:
                    if not p1_character:
                        # Player 1 is choosing the driver.
                        p1_character = game_data.CHARACTERS[character]
                    else:
                        # Player 1 is choosing the rider.
                        p2_character = game_data.CHARACTERS[character]
                elif player == 1:
                    # Player 2 can choose only the rider.
                    p2_character = game_data.CHARACTERS[character]

                # Force character selection.
                if not character in ctx.unlocked_characters:
                    direction: int = character - ctx.last_selected_character[player]
                    direction = 1 if direction == 0 or direction == 1 else -1
                    for i in range(20):
                        character = wrap(character + direction, len(game_data.CHARACTERS))
                        if character in ctx.unlocked_characters:
                            break
                    dolphin.write_word(menu_pointer + ctx.memory_addresses.menu_character_w_offset + player_offset, character)

            ctx.last_selected_character[player] = character
            
            if kart >= 0 and kart < len(game_data.KARTS):
                # Force kart selection.
                weight = max(ctx.active_characters[0].weight, ctx.active_characters[1].weight)
                direction: int = kart - ctx.last_selected_kart[player]
                direction = 1 if direction == 0 else int(direction / abs(direction))
                for i in range(21):
                    if kart in ctx.unlocked_karts and (game_data.KARTS[kart].weight == weight or game_data.KARTS[kart].weight == -1):
                        break
                    kart = wrap(kart + direction, len(game_data.KARTS))
                dolphin.write_word(menu_pointer + ctx.memory_addresses.menu_kart_w_offset + player_offset, kart)

                if player == 0:
                    ctx.active_kart = game_data.KARTS[kart]
                    p1_kart = ctx.active_kart
            ctx.last_selected_kart[player] = kart

        # Print selected kart or characters and their items.
        if p1_kart:
            text_s[0] = p1_kart.name + " " + ", ".join(u.short_name for u in ctx.kart_upgrades[p1_kart.id])
            text_x[0] = 92
            text_y[0] = 215
        elif p1_character:
            p1_items: list[game_data.Item] = ctx.character_items.get(p1_character, []).copy()
            p1_items.extend(ctx.global_items)
            if p2_character:
                p2_items: list[game_data.Item] = ctx.character_items.get(p2_character, []).copy()
                p2_items.extend(ctx.global_items)
                # Check for synergy (default character combo).
                character1 = min(p1_character.id, p2_character.id)
                character2 = max(p1_character.id, p2_character.id)
                if character1 % 2 == 0 and character1 + 1 == character2 or character1 >= 16 and character2 >= 16:
                    p1_items = p2_items
                    if len(p2_items) > 0:
                        text_x[2] = 92
                        text_y[2] = 265
                        text_s[2] = "Item synergy"
                text_x[1] = 92
                text_y[1] = 240
                if len(p2_items) > 0:
                    text_s[1] = f"{p2_character.name}: {", ".join([item.name for item in p2_items])}"
                    if len(text_s[1]) > 40:
                        text_s[1] = f"{p2_character.name}: {", ".join([item.short_name for item in p2_items])}"
                    if len(text_s[1]) > 43:
                        text_s[1] = text_s[1][:41] + ".."
                else:
                    text_s[1] = f"{p2_character.name} (no items)"
            text_x[0] = 92
            text_y[0] = 215
            if len(p1_items) > 0:
                text_s[0] = f"{p1_character.name}: {", ".join([item.name for item in p1_items])}"
                if len(text_s[0]) > 40:
                    text_s[0] = f"{p1_character.name}: {", ".join([item.short_name for item in p1_items])}"
                if len(text_s[0]) > 43:
                    text_s[0] = text_s[0][:41] + ".."
            else:
                text_s[0] = f"{p1_character.name} (no items)"

    # Apply shuffled courses upon selecting vehicle class.
    vehicle_class = dolphin.read_word(ctx.memory_addresses.vehicle_class_w)
    if vehicle_class != ctx.last_selected_vehicle_class:
        ctx.last_selected_vehicle_class = vehicle_class
        offset = ctx.memory_addresses.cup_contents_wx
        for i_cup in ctx.cups_courses:
            for i_course in i_cup:
                dolphin.write_word(offset, game_data.COURSES[i_course].id)
                dolphin.write_word(offset + 4, ctx.memory_addresses.course_names_s[i_course])
                dolphin.write_word(offset + 8, ctx.memory_addresses.course_previews_s[i_course])
                offset += 12


    mode: int = int(dolphin.read_word(ctx.memory_addresses.mode_w))
    available_cups_courses: dict[int, set[int]] = {}
    if mode == game_data.Modes.TIMETRIAL:
        for i_cup in range(4):
            for i_course in ctx.unlocked_courses:
                if i_course in ctx.cups_courses[i_cup]:
                    if not i_cup in available_cups_courses:
                        available_cups_courses[i_cup] = set()
                    available_cups_courses[i_cup].add(ctx.cups_courses[i_cup].index(i_course))
        if len(available_cups_courses) == 0:
            # Failsafe if no tt tracks are unlocked.
            logger.info("No Time Trials unlocked yet! Changed mode to Grand Prix.")
            mode = int(game_data.Modes.GRANDPRIX)
            dolphin.write_word(ctx.memory_addresses.mode_w, mode)
            dolphin.write_word(ctx.memory_addresses.vehicle_class_w, ctx.unlocked_vehicle_class)

        # Use vanilla lap counts in time trials.
        for i_course in [c for c in game_data.RACE_COURSES]:
            dolphin.write_byte(ctx.memory_addresses.lap_count_bx + i_course.id, i_course.laps)

    
    if mode == game_data.Modes.GRANDPRIX:
        # Give option to skip x first courses.
        courses = [c for c in range(ctx.unlocked_cup_skips + 1)]
        for i_cup in ctx.unlocked_cups:
            if i_cup == game_data.CUP_ALL_CUP_TOUR:
                available_cups_courses[i_cup] = [0]
            else:
                available_cups_courses[i_cup] = courses

        # Use custom lap counts in grand prix.
        for i_course in [c for c in game_data.RACE_COURSES]:
            dolphin.write_byte(ctx.memory_addresses.lap_count_bx + i_course.id, ctx.lap_counts[i_course.name])

        # Item selection.
        in_race_placement: int = max(0, min(7, dolphin.read_word(ctx.memory_addresses.in_race_placement_wx) - 1))
        item_adr: list[int] = [
            ctx.memory_addresses.gp_next_items_bx + ctx.active_characters[0].item_offset,
            ctx.memory_addresses.gp_next_items_bx + ctx.active_characters[1].item_offset,
        ]
        total_weight = ctx.global_items_total_weights[in_race_placement]
        total_weight += ctx.character_item_total_weights[ctx.active_characters[0].name][in_race_placement]
        item_pool = ctx.global_items + ctx.character_items[ctx.active_characters[0]]
        if item_adr[0] != item_adr[1]:
            item_weights = [item.weight_table[in_race_placement] for item in item_pool]
            # Yet to be unlocked items still count towards item weights.
            weight_gap = total_weight - sum(item_weights)
            if weight_gap > 0:
                item_pool.append(game_data.ITEM_NONE)
                item_weights.append(weight_gap)
            rand_item = random.sample(item_pool, 1, counts = item_weights)[0]
            dolphin.write_byte(item_adr[0], rand_item.id)

            # Reset pool for second player only if they aren't synced.
            total_weight = ctx.global_items_total_weights[in_race_placement]
            item_pool = ctx.global_items.copy()
        total_weight += ctx.character_item_total_weights[ctx.active_characters[1].name][in_race_placement]
        item_pool += ctx.character_items[ctx.active_characters[1]]
        item_weights = [item.weight_table[in_race_placement] for item in item_pool]
        # Yet to be unlocked items still count towards item weights.
        weight_gap = total_weight - sum(item_weights)
        if weight_gap > 0:
            item_pool.append(game_data.ITEM_NONE)
            item_weights.append(weight_gap)
        rand_item = random.sample(item_pool, 1, counts = item_weights)[0]
        dolphin.write_byte(item_adr[1], rand_item.id)

        # Set All Cup Tour lenght by skipping to the second-last race. This ensures that Rainbow Road is still the last.
        if (dolphin.read_word(ctx.memory_addresses.cup_w) == game_data.CUP_ALL_CUP_TOUR and
            dolphin.read_word(ctx.memory_addresses.gp_race_no_w) == ctx.all_cup_tour_length - 2):
            dolphin.write_word(ctx.memory_addresses.gp_race_no_w, 14)

    # Force cup and course selection.
    selected_cup: int = int(dolphin.read_word(ctx.memory_addresses.cup_w))
    selected_course: int = int(dolphin.read_word(ctx.memory_addresses.menu_course_w))
    if len(available_cups_courses) > 0:
        if not selected_cup in available_cups_courses:
            direction: int = selected_cup - ctx.last_selected_cup
            direction = 1 if direction == 0 or direction == 1 else -1
            for i in range(5):
                selected_cup = wrap(selected_cup + direction, len(game_data.CUPS))
                if selected_cup in available_cups_courses:
                    break
            dolphin.write_word(ctx.memory_addresses.cup_w, selected_cup)

        for i_cup in range(len(game_data.CUPS)):
            dolphin.write_byte(ctx.memory_addresses.available_cups_bx + i_cup, int(i_cup in available_cups_courses))

        if not selected_course in available_cups_courses[selected_cup]:
            direction: int = selected_course - ctx.last_selected_course
            direction = 1 if direction == 0 or direction == 1 else -1
            for i in range(4):
                selected_course = wrap(selected_course + direction, 4)
                if selected_course in available_cups_courses[selected_cup]:
                    break
            dolphin.write_word(ctx.memory_addresses.menu_course_w, selected_course)
    
    # Shuffle All Cup Tour properly with randomized courses.
    if selected_cup == game_data.CUP_ALL_CUP_TOUR and selected_cup != ctx.last_selected_cup:
        course_order = list(range(1, 15)) # First is LC, last is RR - shuffle everything between.
        random.shuffle(course_order)
        course_order = [0, *course_order, 15]
        flat_course_list = [i_course for i_cup in ctx.cups_courses for i_course in i_cup]
        offset = 0
        for i_course in course_order:
            dolphin.write_word(ctx.memory_addresses.all_cup_tour_contents_wx + offset,
                               flat_course_list.index(i_course))
            offset += 4
        

    ctx.last_selected_cup = selected_cup
    ctx.last_selected_course = selected_course

    # Set kart stats.
    vehicle_class: int = dolphin.read_word(ctx.memory_addresses.vehicle_class_w)
    if mode == game_data.Modes.GRANDPRIX and vehicle_class == 3 and ctx.mirror_200cc:
        dolphin.write_float(ctx.memory_addresses.speed_multiplier_150cc_f, 1.4)
        dolphin.write_float(ctx.memory_addresses.max_speed_f, 250)
    else:
        dolphin.write_float(ctx.memory_addresses.speed_multiplier_150cc_f, 1.15)
        dolphin.write_float(ctx.memory_addresses.max_speed_f, 200)

    kart_stats_pointer = ctx.memory_addresses.kart_stats_pointer
    for i in range(len(game_data.KARTS)):
        kart: game_data.Kart = game_data.KARTS[i]
        kart_address = kart_stats_pointer + i * ctx.memory_addresses.kart_struct_size

        speed_1_multiplier = 1.0
        speed_2_multiplier = 1.0
        speed_3_multiplier = 1.0
        speed_4_multiplier = 1.0
        acceleration_1_addition = 0.0
        acceleration_2_addition = 0.0
        mini_turbo_addition = 0.0
        weight_addition = 0.0
        steer_addition = 0.0
        if kart == ctx.active_kart:
            # Engine upgrades by levels: .9, 1, 1.05, 1.1
            if ctx.engine_upgrade_level == 0:
                speed_1_multiplier = .9
            elif ctx.engine_upgrade_level > 1:
                speed_1_multiplier = .95 + ctx.engine_upgrade_level * .05
            for upgrade in ctx.kart_upgrades[i]:
                if upgrade == game_data.KART_UPGRADE_ACC:
                    acceleration_1_addition += 1
                    acceleration_2_addition += .1
                elif upgrade == game_data.KART_UPGRADE_OFFROAD:
                    speed_2_multiplier *= 1.1
                    speed_3_multiplier *= 1.2
                    speed_4_multiplier *= 3
                elif upgrade == game_data.KART_UPGRADE_WEIGHT:
                    weight_addition += 2
                elif upgrade == game_data.KART_UPGRADE_TURBO:
                    mini_turbo_addition += 30
                elif upgrade == game_data.KART_UPGRADE_STEER:
                    steer_addition += 1
        # Speed 1 (on road) is also general speed multiplier.
        speed_2_multiplier *= speed_1_multiplier
        speed_3_multiplier *= speed_1_multiplier
        speed_4_multiplier *= speed_1_multiplier
        stats = kart.stats
        
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_speed_on_road_f_offset, stats.speed_on_road * speed_1_multiplier)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_speed_off_road_sand_f_offset, stats.speed_off_road_sand * speed_2_multiplier)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_speed_off_road_grass_f_offset, stats.speed_off_road_grass * speed_3_multiplier)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_speed_off_road_mud_f_offset, stats.speed_off_road_mud * speed_4_multiplier)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_acceleration_1_f_offset, stats.acceleration_1 + acceleration_1_addition)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_acceleration_2_f_offset, stats.acceleration_2 + acceleration_2_addition)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_mini_turbo_f_offset, stats.mini_turbo + mini_turbo_addition)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_mass_f_offset, stats.mass + weight_addition)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_roll_f_offset, stats.roll)
        dolphin.write_float(kart_address + ctx.memory_addresses.kart_steer_f_offset, stats.steer + steer_addition)
    

    # In game message system
    ctx.message_time_left -= 1
    if ctx.message_time_left > 0:
        lines: list[str] = ctx.message_queue[0].split("\n")
        for i, text in enumerate(lines):
            # Use text slots from the end to interfere minimally with other texts.
            text_id = ctx.memory_addresses.text_amount - i - 1
            text_s[text_id] = text
            text_x[text_id] = 304
            text_y[text_id] = 13 + i * 12
            text_j[text_id] = 0
            
    # Try to show the message first, only then check for new message.
    # This causes one tick long disappearing of the message between messages,
    # making message changing more noticeable.
    if ctx.message_time_left == 0:
        ctx.message_queue.pop(0)
        if len(ctx.message_queue) > 0:
            ctx.message_time_left = 40

    for i in range(len(text_s)):
        print_ingame(ctx, text_x[i], text_y[i], text_s[i], i, text_j[i])


def wrap(value: int, max_value: int) -> int:
    if value < 0:
        return max_value - 1
    if value >= max_value:
        return 0
    return value


async def check_current_course_changed(ctx: MkddContext) -> None:
    """
    Check if the player has moved to a new stage.
    If so, update all trackers with the new stage name.
    If the stage has never been visited, additionally update the server.

    :param ctx: Mario Kart Double Dash client context.
    """
    course_id = dolphin.read_word(ctx.memory_addresses.current_course_w)
    courses: list[game_data.Course] = [c for c in game_data.COURSES if c.id == course_id]
    if len(courses) > 0:
        new_course = courses[0]
        if new_course != ctx.current_course:
            ctx.course_changed_time = dolphin.read_word(ctx.memory_addresses.game_ticks_w)
            ctx.current_course = new_course
            # Send a Bounced message containing the new stage name to all trackers connected to the current slot.
            data_to_send = {"mkdd_course_name": new_course.name}
            message = {
                "cmd": "Bounce",
                "slots": [ctx.slot],
                "data": data_to_send,
            }
            await ctx.send_msgs([message])



async def check_death(ctx: MkddContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    # TODO: Check for Lakitu.
    if ctx.slot is not None and check_ingame():
        is_dead = False
        if is_dead:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " fell off a track.")
        else:
            ctx.has_send_death = False


def check_ingame() -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    # TODO: Check if a race is on.
    return True


def dolphin_write_half(address: int, value: int) -> None:
    """
    Write a half-word/short (2 bytes) into memory.
    """
    dolphin.write_bytes(address, value.to_bytes(2, byteorder="big"))


def dolphin_write_str(address: int, value: str) -> None:
    """
    Write a string into memory.
    """
    dolphin.write_bytes(address, bytes(value, "ascii", "replace"))
    dolphin.write_byte(address + len(value), 0)


def print_ingame(ctx: MkddContext, x: int, y: int, text: str, msg_id: int, justification: int = 0) -> None:
    """
    Print text in game.

    :param ctx: Mario Kart Double Dash client context.
    :param x: X coorditate, from 0 (left) to 608 (right).
    :param y: Y coordinate, from 12 (top) to 450 (bottom).
    :param text: The text to show. One line only, max 43 characters.
    :param msg_id: Id for the text. From 0 upwards. Using same id replaces the text.
    :param justification: 1 for left justification, 0 for center, -1 for right.
    """
    text = text[:43]
    font_size = 12
    text_width = len(text) * font_size
    x += int(text_width * (justification - 1) / 2)
    address = ctx.memory_addresses.text_sx + msg_id * ctx.memory_addresses.text_size
    dolphin_write_str(address, text)
    dolphin_write_half(address + ctx.memory_addresses.text_x_offset_h, x)
    dolphin_write_half(address + ctx.memory_addresses.text_y_offset_h, y)


def queue_ingame_message(ctx: MkddContext, message: str) -> None:
    """
    Show message in game. If there's multiple messages, they will be shown one after another.

    :param ctx: Mario Kart Double Dash client context.
    :param message: The message to show. Can be 2 lines long.
    """
    ctx.message_queue.append(message)
    if len(ctx.message_queue) == 1:
        ctx.message_time_left = 40


async def dolphin_sync_task(ctx: MkddContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: Mario Kart Double Dash client context.
    """
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dolphin.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_current_course_changed(ctx)
                    await check_locations(ctx)
                    update_game(ctx)

                    if ctx.victory and not ctx.victory_sent:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.victory_sent = True
                else:
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                if dolphin.read_bytes(0x80000000, 6) != b"GM4E01":
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin.hook()
                if dolphin.is_hooked():
                    if dolphin.read_bytes(0x80000000, 6) != b"GM4E01":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        apply_patch(ctx)
                        sync_state(ctx)
                        await give_items(ctx)
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def main(connect: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Run the main async loop for Mario Kart Double Dash client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
    """
    Utils.init_logging("Mario Kart Double Dash Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = MkddContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        # Runs Universal Tracker's internal generator
        if tracker_loaded:
            ctx.run_generator()
            ctx.tags.remove("Tracker")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
