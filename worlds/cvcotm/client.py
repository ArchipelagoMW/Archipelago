from typing import TYPE_CHECKING, Set
from .locations import BASE_ID, get_location_names_to_ids
from .items import cvcotm_item_info, MAJORS_CLASSIFICATIONS
from .locations import cvcotm_location_info
from .cvcotm_text import cvcotm_string_to_bytearray
from .options import CompletionGoal, CVCotMDeathLink, IronMaidenBehavior
from .rom import ARCHIPELAGO_IDENTIFIER_START, ARCHIPELAGO_IDENTIFIER, AUTH_NUMBER_START, QUEUED_TEXT_STRING_START
from .data import iname, lname

from BaseClasses import ItemClassification
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
import base64
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

CURRENT_STATUS_ADDRESS = 0xD0
POISON_TIMER_TILL_DAMAGE_ADDRESS = 0xD8
POISON_DAMAGE_VALUE_ADDRESS = 0xDE
GAME_STATE_ADDRESS = 0x45D8
FLAGS_ARRAY_START = 0x25374
CARDS_ARRAY_START = 0x25674
NUM_RECEIVED_ITEMS_ADDRESS = 0x253D0
MAX_UPS_ARRAY_START = 0x2572C
MAGIC_ITEMS_ARRAY_START = 0x2572F
QUEUED_TEXTBOX_1_ADDRESS = 0x25300
QUEUED_TEXTBOX_2_ADDRESS = 0x25302
QUEUED_MSG_DELAY_TIMER_ADDRESS = 0x25304
QUEUED_SOUND_ID_ADDRESS = 0x25306
DELAY_TIMER_ADDRESS = 0x25308
CURRENT_CUTSCENE_ID_ADDRESS = 0x26000
NATHAN_STATE_ADDRESS = 0x50
CURRENT_HP_ADDRESS = 0x2562E
CURRENT_MP_ADDRESS = 0x25636
CURRENT_HEARTS_ADDRESS = 0x2563C
CURRENT_LOCATION_VALUES_START = 0x253FC
ROM_NAME_START = 0xA0

AREA_SEALED_ROOM = 0x00
AREA_BATTLE_ARENA = 0x0E
GAME_STATE_GAMEPLAY = 0x06
GAME_STATE_CREDITS = 0x21
NATHAN_STATE_SAVING = 0x34
STATUS_POISON = b"\x02"
TEXT_ID_DSS_TUTORIAL = b"\x1D\x82"
TEXT_ID_MULTIWORLD_MESSAGE = b"\xF2\x84"
SOUND_ID_UNUSED_SIMON_FANFARE = b"\x04"
SOUND_ID_MAIDEN_BREAKING = b"\x79"
# SOUND_ID_NATHAN_FREEZING = b"\x7A"
SOUND_ID_BAD_CONFIG = b"\x2D\x01"
SOUND_ID_DRACULA_CHARGE = b"\xAB\x01"
SOUND_ID_MINOR_PICKUP = b"\xB3\x01"
SOUND_ID_MAJOR_PICKUP = b"\xB4\x01"

ITEM_NAME_LIMIT = 300
PLAYER_NAME_LIMIT = 50

FLAG_HIT_IRON_MAIDEN_SWITCH = 0x2A
FLAG_SAW_DSS_TUTORIAL = 0xB1
FLAG_WON_BATTLE_ARENA = 0xB2
FLAG_DEFEATED_DRACULA_II = 0xBC

# These flags are communicated to the tracker as a bitfield using this order.
# Modifying the order will cause undetectable autotracking issues.
EVENT_FLAG_MAP = {
    FLAG_HIT_IRON_MAIDEN_SWITCH: "FLAG_HIT_IRON_MAIDEN_SWITCH",
    FLAG_WON_BATTLE_ARENA: "FLAG_WON_BATTLE_ARENA",
    0xB3: "FLAG_DEFEATED_CERBERUS",
    0xB4: "FLAG_DEFEATED_NECROMANCER",
    0xB5: "FLAG_DEFEATED_IRON_GOLEM",
    0xB6: "FLAG_DEFEATED_ADRAMELECH",
    0xB7: "FLAG_DEFEATED_DRAGON_ZOMBIES",
    0xB8: "FLAG_DEFEATED_DEATH",
    0xB9: "FLAG_DEFEATED_CAMILLA",
    0xBA: "FLAG_DEFEATED_HUGH",
    0xBB: "FLAG_DEFEATED_DRACULA_I",
    FLAG_DEFEATED_DRACULA_II: "FLAG_DEFEATED_DRACULA_II"
}

DEATHLINK_AREA_NAMES = ["Sealed Room", "Catacomb", "Abyss Staircase", "Audience Room", "Triumph Hallway",
                        "Machine Tower", "Eternal Corridor", "Chapel Tower", "Underground Warehouse",
                        "Underground Gallery", "Underground Waterway", "Outer Wall", "Observation Tower",
                        "Ceremonial Room", "Battle Arena"]


class CastlevaniaCotMClient(BizHawkClient):
    game = "Castlevania - Circle of the Moon"
    system = "GBA"
    patch_suffix = ".apcvcotm"
    sent_initial_packets: bool
    self_induced_death: bool
    local_checked_locations: Set[int]
    client_set_events = {flag_name: False for flag, flag_name in EVENT_FLAG_MAP.items()}
    killed_dracula_2: bool
    won_battle_arena: bool
    sent_message_queue: list
    death_causes: list
    currently_dead: bool
    synced_set_events: bool
    saw_arena_win_message: bool
    saw_dss_tutorial: bool

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            game_names = await bizhawk.read(ctx.bizhawk_ctx, [(ROM_NAME_START, 0xC, "ROM"),
                                                              (ARCHIPELAGO_IDENTIFIER_START, 12, "ROM")])
            if game_names[0].decode("ascii") != "DRACULA AGB1":
                return False
            if game_names[1] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                logger.info("ERROR: You appear to be running an unpatched version of Castlevania: Circle of the Moon. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if game_names[1].decode("ascii") != ARCHIPELAGO_IDENTIFIER:
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your client version against the version being "
                            "used by the generator.")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(AUTH_NUMBER_START, 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")
        # Initialize all the local client attributes here so that nothing will be carried over from a previous CotM if
        # the player tried changing CotM ROMs without resetting their Bizhawk Client instance.
        self.sent_initial_packets = False
        self.local_checked_locations = set()
        self.self_induced_death = False
        self.client_set_events = {flag_name: False for flag, flag_name in EVENT_FLAG_MAP.items()}
        self.killed_dracula_2 = False
        self.won_battle_arena = False
        self.sent_message_queue = []
        self.death_causes = []
        self.currently_dead = False
        self.synced_set_events = False
        self.saw_arena_win_message = False
        self.saw_dss_tutorial = False

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if ctx.slot is None:
            return
        if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
            if "cause" in args["data"]:
                cause = args["data"]["cause"]
                if cause == "":
                    cause = f"{args['data']['source']} killed you without a word!"
                if len(cause) > ITEM_NAME_LIMIT + PLAYER_NAME_LIMIT:
                    cause = cause[:ITEM_NAME_LIMIT + PLAYER_NAME_LIMIT]
            else:
                cause = f"{args['data']['source']} killed you without a word!"

            # Highlight the player that killed us in the game's orange text.
            if args['data']['source'] in cause:
                words = cause.split(args['data']['source'], 1)
                cause = words[0] + "「" + args['data']['source'] + "」" + words[1]

            self.death_causes += [cause]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None or ctx.slot is None:
            return

        try:
            # Scout all Locations and get our Set events upon initial connection.
            if not self.sent_initial_packets:
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": [code for name, code in get_location_names_to_ids().items()
                                  if code in ctx.server_locations],
                    "create_as_hint": 0
                }])
                await ctx.send_msgs([{
                    "cmd": "Get",
                    "keys": [f"castlevania_cotm_events_{ctx.team}_{ctx.slot}"]
                }])
                self.sent_initial_packets = True

            read_state = await bizhawk.read(ctx.bizhawk_ctx, [(GAME_STATE_ADDRESS, 1, "EWRAM"),
                                                              (FLAGS_ARRAY_START, 32, "EWRAM"),
                                                              (CARDS_ARRAY_START, 20, "EWRAM"),
                                                              (NUM_RECEIVED_ITEMS_ADDRESS, 2, "EWRAM"),
                                                              (MAX_UPS_ARRAY_START, 3, "EWRAM"),
                                                              (MAGIC_ITEMS_ARRAY_START, 8, "EWRAM"),
                                                              (QUEUED_TEXTBOX_1_ADDRESS, 2, "EWRAM"),
                                                              (DELAY_TIMER_ADDRESS, 2, "EWRAM"),
                                                              (CURRENT_CUTSCENE_ID_ADDRESS, 1, "EWRAM"),
                                                              (NATHAN_STATE_ADDRESS, 1, "EWRAM"),
                                                              (CURRENT_HP_ADDRESS, 18, "EWRAM"),
                                                              (CURRENT_LOCATION_VALUES_START, 2, "EWRAM")])

            game_state = int.from_bytes(read_state[0], "little")
            event_flags_array = read_state[1]
            cards_array = list(read_state[2])
            max_ups_array = list(read_state[4])
            magic_items_array = list(read_state[5])
            num_received_items = int.from_bytes(bytearray(read_state[3]), "little")
            queued_textbox = int.from_bytes(bytearray(read_state[6]), "little")
            delay_timer = int.from_bytes(bytearray(read_state[7]), "little")
            cutscene = int.from_bytes(bytearray(read_state[8]), "little")
            nathan_state = int.from_bytes(bytearray(read_state[9]), "little")
            health_stats_array = bytearray(read_state[10])
            area = int.from_bytes(bytearray(read_state[11][0:1]), "little")
            room = int.from_bytes(bytearray(read_state[11][1:]), "little")

            # Get out each of the individual health/magic/heart values.
            hp = int.from_bytes(health_stats_array[0:2], "little")
            max_hp = int.from_bytes(health_stats_array[4:6], "little")
            # mp = int.from_bytes(health_stats_array[8:10], "little") Not used. But it's here if it's ever needed!
            max_mp = int.from_bytes(health_stats_array[12:14], "little")
            hearts = int.from_bytes(health_stats_array[14:16], "little")
            max_hearts = int.from_bytes(health_stats_array[16:], "little")

            # If there's no textbox already queued, the delay timer is 0, we are not in a cutscene, and Nathan's current
            # state value is not 0x34 (using a save room), it should be safe to inject a textbox message.
            ok_to_inject = not queued_textbox and not delay_timer and not cutscene \
                and nathan_state != NATHAN_STATE_SAVING

            # Make sure we are in the Gameplay or Credits states before detecting sent locations.
            # If we are in any other state, such as the Game Over state, reset the textbox buffers back to 0 so that we
            # don't receive the most recent item upon loading back in.
            #
            # If the intro cutscene floor broken flag is not set, then assume we are in the demo; at no point during
            # regular gameplay will this flag not be set.
            if game_state not in [GAME_STATE_GAMEPLAY, GAME_STATE_CREDITS] or not event_flags_array[6] & 0x02:
                self.currently_dead = False
                await bizhawk.write(ctx.bizhawk_ctx, [(QUEUED_TEXTBOX_1_ADDRESS, [0 for _ in range(12)], "EWRAM")])
                return

            # Enable DeathLink if it's in our slot_data.
            if "DeathLink" not in ctx.tags and ctx.slot_data["death_link"]:
                await ctx.update_death_link(True)

            # Send a DeathLink if we died on our own independently of receiving another one.
            if "DeathLink" in ctx.tags and hp == 0 and not self.currently_dead:
                self.currently_dead = True

                # Check if we are in Dracula II's arena. The game considers this part of the Sealed Room area,
                # which I don't think makes sense to be player-facing like this.
                if area == AREA_SEALED_ROOM and room == 2:
                    area_of_death = "Dracula's realm"
                # If we aren't in Dracula II's arena, then take the name of whatever area the player is currently in.
                else:
                    area_of_death = DEATHLINK_AREA_NAMES[area]

                await ctx.send_death(f"{ctx.player_names[ctx.slot]} perished in {area_of_death}. Dracula has won!")

            # Update the Dracula II and Battle Arena events already being done on past separate sessions for if the
            # player is running the Battle Arena and Dracula goal.
            if f"castlevania_cotm_events_{ctx.team}_{ctx.slot}" in ctx.stored_data:
                if ctx.stored_data[f"castlevania_cotm_events_{ctx.team}_{ctx.slot}"] is not None:
                    if ctx.stored_data[f"castlevania_cotm_events_{ctx.team}_{ctx.slot}"] & 0x2:
                        self.won_battle_arena = True

                    if ctx.stored_data[f"castlevania_cotm_events_{ctx.team}_{ctx.slot}"] & 0x800:
                        self.killed_dracula_2 = True

            # If we won the Battle Arena, haven't seen the win message yet, and are in the Arena at the moment, pop up
            # the win message while playing the game's unused Theme of Simon Belmont fanfare.
            if self.won_battle_arena and not self.saw_arena_win_message and area == AREA_BATTLE_ARENA \
                    and ok_to_inject and not self.currently_dead:
                win_message = cvcotm_string_to_bytearray("      A 「WINNER」 IS 「YOU」!▶", "little middle", 0,
                                                         wrap=False)
                await bizhawk.write(ctx.bizhawk_ctx, [(QUEUED_TEXTBOX_1_ADDRESS, TEXT_ID_MULTIWORLD_MESSAGE, "EWRAM"),
                                                      (QUEUED_SOUND_ID_ADDRESS, SOUND_ID_UNUSED_SIMON_FANFARE, "EWRAM"),
                                                      (QUEUED_TEXT_STRING_START, win_message, "ROM")])
                self.saw_arena_win_message = True

            # If we have any queued death causes, handle DeathLink giving here.
            elif self.death_causes and ok_to_inject and not self.currently_dead:

                # Inject the oldest cause as a textbox message and play the Dracula charge attack sound.
                death_text = self.death_causes[0]
                death_writes = [(QUEUED_TEXTBOX_1_ADDRESS, TEXT_ID_MULTIWORLD_MESSAGE, "EWRAM"),
                                (QUEUED_SOUND_ID_ADDRESS, SOUND_ID_DRACULA_CHARGE, "EWRAM")]

                # If we are in the Battle Arena and are not using the On Including Arena DeathLink option, extend the
                # DeathLink message and don't actually kill Nathan.
                if ctx.slot_data["death_link"] != CVCotMDeathLink.option_arena_on and area == AREA_BATTLE_ARENA:
                    death_text += "◊The Battle Arena nullified the DeathLink. Go fight fair and square!"
                else:
                    # Otherwise, kill Nathan by giving him a 9999 damage-dealing poison status that hurts him as soon as
                    # the death cause textbox is dismissed.
                    death_writes += [(CURRENT_STATUS_ADDRESS, STATUS_POISON, "EWRAM"),
                                     (POISON_TIMER_TILL_DAMAGE_ADDRESS, b"\x38", "EWRAM"),
                                     (POISON_DAMAGE_VALUE_ADDRESS, b"\x0F\x27", "EWRAM")]

                # Add the final death text and write the whole shebang.
                death_writes += [(QUEUED_TEXT_STRING_START,
                                  bytes(cvcotm_string_to_bytearray(death_text + "◊", "big middle", 0)), "ROM")]
                await bizhawk.write(ctx.bizhawk_ctx, death_writes)

                # Delete the oldest death cause that we just wrote and set currently_dead to True so the client doesn't
                # think we just died on our own on the subsequent frames before the Game Over state.
                del(self.death_causes[0])
                self.currently_dead = True

            # If we have a queue of Locations to inject "sent" messages with, do so before giving any subsequent Items.
            elif self.sent_message_queue and ok_to_inject and not self.currently_dead and ctx.locations_info:
                loc = self.sent_message_queue[0]
                # Truncate the Item name. ArchipIDLE's FFXIV Item is 214 characters, for comparison.
                item_name = ctx.item_names.lookup_in_slot(ctx.locations_info[loc].item, ctx.locations_info[loc].player)
                if len(item_name) > ITEM_NAME_LIMIT:
                    item_name = item_name[:ITEM_NAME_LIMIT]
                # Truncate the player name. Player names are normally capped at 16 characters, but there is no limit on
                # ItemLink group names.
                player_name = ctx.player_names[ctx.locations_info[loc].player]
                if len(player_name) > PLAYER_NAME_LIMIT:
                    player_name = player_name[:PLAYER_NAME_LIMIT]

                sent_text = cvcotm_string_to_bytearray(f"「{item_name}」 sent to 「{player_name}」◊", "big middle", 0)

                # Set the correct sound to play depending on the Item's classification.
                if item_name == iname.ironmaidens and \
                        ctx.slot_info[ctx.locations_info[loc].player].game == "Castlevania - Circle of the Moon":
                    mssg_sfx_id = SOUND_ID_MAIDEN_BREAKING
                    sent_text = cvcotm_string_to_bytearray(f"「Iron Maidens」 broken for 「{player_name}」◊",
                                                           "big middle", 0)
                elif ctx.locations_info[loc].flags & MAJORS_CLASSIFICATIONS:
                    mssg_sfx_id = SOUND_ID_MAJOR_PICKUP
                elif ctx.locations_info[loc].flags & ItemClassification.trap:
                    mssg_sfx_id = SOUND_ID_BAD_CONFIG
                else:  # Filler
                    mssg_sfx_id = SOUND_ID_MINOR_PICKUP

                await bizhawk.write(ctx.bizhawk_ctx, [(QUEUED_TEXTBOX_1_ADDRESS, TEXT_ID_MULTIWORLD_MESSAGE, "EWRAM"),
                                                      (QUEUED_SOUND_ID_ADDRESS, mssg_sfx_id, "EWRAM"),
                                                      (QUEUED_TEXT_STRING_START, sent_text, "ROM")])

                del(self.sent_message_queue[0])

            # If the game hasn't received all items yet, it's ok to inject, and the current number of received items
            # still matches what we read before, then write the next incoming item into the inventory and, separately,
            # the textbox ID to trigger the multiworld textbox, sound effect to play when the textbox opens, number to
            # increment the received items count by, and the text to go into the multiworld textbox. The game will then
            # do the rest when it's able to.
            elif num_received_items < len(ctx.items_received) and ok_to_inject and not self.currently_dead:
                next_item = ctx.items_received[num_received_items]

                # Figure out what inventory array and offset from said array to increment based on what we are
                # receiving.
                flag_index = 0
                flag_array = b""
                inv_array = []
                inv_array_start = 0
                text_id_2 = b"\x00\x00"
                item_type = next_item.item & 0xFF00
                inv_array_index = next_item.item & 0xFF
                if item_type == 0xE600:  # Card
                    inv_array_start = CARDS_ARRAY_START
                    inv_array = cards_array
                    mssg_sfx_id = SOUND_ID_MAJOR_PICKUP
                    # If skip_tutorials is off and the saw DSS tutorial flag is not set, set the flag and display it
                    # for the second textbox.
                    if not self.saw_dss_tutorial and not ctx.slot_data["skip_tutorials"]:
                        flag_index = FLAG_SAW_DSS_TUTORIAL
                        flag_array = event_flags_array
                        text_id_2 = TEXT_ID_DSS_TUTORIAL
                elif item_type == 0xE800 and inv_array_index == 0x09:  # Maiden Detonator
                    flag_index = FLAG_HIT_IRON_MAIDEN_SWITCH
                    flag_array = event_flags_array
                    mssg_sfx_id = SOUND_ID_MAIDEN_BREAKING
                elif item_type == 0xE800:  # Any other Magic Item
                    inv_array_start = MAGIC_ITEMS_ARRAY_START
                    inv_array = magic_items_array
                    mssg_sfx_id = SOUND_ID_MAJOR_PICKUP
                    if inv_array_index > 5:  # The unused Map's index is skipped over.
                        inv_array_index -= 1
                else:  # Max Up
                    inv_array_start = MAX_UPS_ARRAY_START
                    mssg_sfx_id = SOUND_ID_MINOR_PICKUP
                    inv_array = max_ups_array

                item_name = ctx.item_names.lookup_in_slot(next_item.item)
                player_name = ctx.player_names[next_item.player]
                # Truncate the player name.
                if len(player_name) > PLAYER_NAME_LIMIT:
                    player_name = player_name[:PLAYER_NAME_LIMIT]

                # If the Item came from a different player, display a custom received message. Otherwise, display the
                # vanilla received message for that Item.
                if next_item.player != ctx.slot:
                    text_id_1 = TEXT_ID_MULTIWORLD_MESSAGE
                    if item_name == iname.ironmaidens:
                        received_text = cvcotm_string_to_bytearray(f"「Iron Maidens」 broken by "
                                                                   f"「{player_name}」◊", "big middle", 0)
                    else:
                        received_text = cvcotm_string_to_bytearray(f"「{item_name}」 received from "
                                                                   f"「{player_name}」◊", "big middle", 0)
                    text_write = [(QUEUED_TEXT_STRING_START, bytes(received_text), "ROM")]

                    # If skip_tutorials is off, display the Item's tutorial for the second textbox (if it has one).
                    if not ctx.slot_data["skip_tutorials"] and cvcotm_item_info[item_name].tutorial_id is not None:
                        text_id_2 = cvcotm_item_info[item_name].tutorial_id
                else:
                    text_id_1 = cvcotm_item_info[item_name].text_id
                    text_write = []

                # Check if the player has 255 of the item being received. If they do, don't increment that counter
                # further.
                refill_write = []
                count_write = []
                flag_write = []
                count_guard = []
                flag_guard = []

                # If there's a value to increment in an inventory array, do so here after checking to see if we can.
                if inv_array_start:
                    if inv_array[inv_array_index] + 1 > 0xFF:
                        # If it's a stat max up being received, manually give a refill of that item's stat.
                        # Normally, the game does this automatically by incrementing the number of that max up.
                        if item_name == iname.hp_max:
                            refill_write = [(CURRENT_HP_ADDRESS, int.to_bytes(max_hp, 2, "little"), "EWRAM")]
                        elif item_name == iname.mp_max:
                            refill_write = [(CURRENT_MP_ADDRESS, int.to_bytes(max_mp, 2, "little"), "EWRAM")]
                        elif item_name == iname.heart_max:
                            # If adding +6 Hearts doesn't put us over the player's current max Hearts, do so.
                            # Otherwise, set the player's current Hearts to the current max.
                            if hearts + 6 > max_hearts:
                                new_hearts = max_hearts
                            else:
                                new_hearts = hearts + 6
                            refill_write = [(CURRENT_HEARTS_ADDRESS, int.to_bytes(new_hearts, 2, "little"), "EWRAM")]
                    else:
                        # If our received count of that item is not more than 255, increment it normally.
                        inv_address = inv_array_start + inv_array_index
                        count_guard = [(inv_address, int.to_bytes(inv_array[inv_array_index], 1, "little"), "EWRAM")]
                        count_write = [(inv_address, int.to_bytes(inv_array[inv_array_index] + 1, 1, "little"),
                                        "EWRAM")]

                # If there's a flag value to set, do so here.
                if flag_index:
                    flag_bytearray_index = flag_index // 8
                    flag_address = FLAGS_ARRAY_START + flag_bytearray_index
                    flag_guard = [(flag_address, int.to_bytes(flag_array[flag_bytearray_index], 1, "little"), "EWRAM")]
                    flag_write = [(flag_address, int.to_bytes(flag_array[flag_bytearray_index] |
                                                              (0x01 << (flag_index % 8)), 1, "little"), "EWRAM")]

                await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                            [(QUEUED_TEXTBOX_1_ADDRESS, text_id_1, "EWRAM"),
                                             (QUEUED_TEXTBOX_2_ADDRESS, text_id_2, "EWRAM"),
                                             (QUEUED_MSG_DELAY_TIMER_ADDRESS, b"\x01", "EWRAM"),
                                             (QUEUED_SOUND_ID_ADDRESS, mssg_sfx_id, "EWRAM")]
                                            + count_write + flag_write + text_write + refill_write,
                                            # Make sure the number of received items and number to overwrite are still
                                            # what we expect them to be.
                                            [(NUM_RECEIVED_ITEMS_ADDRESS, read_state[3], "EWRAM")]
                                            + count_guard + flag_guard),

            locs_to_send = set()

            # Check each bit in each flag byte for set Location and event flags.
            checked_set_events = {flag_name: False for flag, flag_name in EVENT_FLAG_MAP.items()}
            for byte_index, byte in enumerate(event_flags_array):
                for i in range(8):
                    and_value = 0x01 << i
                    if byte & and_value != 0:
                        flag_id = byte_index * 8 + i

                        location_id = flag_id + BASE_ID
                        if location_id in ctx.server_locations:
                            locs_to_send.add(location_id)

                        # If the flag for pressing the Iron Maiden switch is set, and the Iron Maiden behavior is
                        # vanilla (meaning we really pressed the switch), send the Iron Maiden switch as checked.
                        if flag_id == FLAG_HIT_IRON_MAIDEN_SWITCH and ctx.slot_data["iron_maiden_behavior"] == \
                                IronMaidenBehavior.option_vanilla:
                            locs_to_send.add(cvcotm_location_info[lname.ct21].code + BASE_ID)

                        # If the DSS tutorial flag is set, let the client know, so it's not shown again for
                        # subsequently-received cards.
                        if flag_id == FLAG_SAW_DSS_TUTORIAL:
                            self.saw_dss_tutorial = True

                        if flag_id in EVENT_FLAG_MAP:
                            checked_set_events[EVENT_FLAG_MAP[flag_id]] = True

                            # Update the client's statuses for the Battle Arena and Dracula goals.
                            if flag_id == FLAG_WON_BATTLE_ARENA:
                                self.won_battle_arena = True

                            if flag_id == FLAG_DEFEATED_DRACULA_II:
                                self.killed_dracula_2 = True

            # Send Locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    # Capture all the Locations with non-local Items to send that are in ctx.missing_locations
                    # (the ones that were definitely never sent before).
                    if ctx.locations_info:
                        self.sent_message_queue += [loc for loc in locs_to_send if loc in ctx.missing_locations and
                                                    ctx.locations_info[loc].player != ctx.slot]
                    # If we still don't have the locations info at this point, send another LocationScout packet just
                    # in case something went wrong, and we never received the initial LocationInfo packet.
                    else:
                        await ctx.send_msgs([{
                            "cmd": "LocationScouts",
                            "locations": [code for name, code in get_location_names_to_ids().items()
                                          if code in ctx.server_locations],
                            "create_as_hint": 0
                        }])

                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(locs_to_send)
                    }])

            # Check the win condition depending on what our completion goal is.
            # The Dracula option requires the "killed Dracula II" flag to be set or being in the credits state.
            # The Battle Arena option requires the Shinning Armor pickup flag to be set.
            # Otherwise, the Battle Arena and Dracula option requires both of the above to be satisfied simultaneously.
            if ctx.slot_data["completion_goal"] == CompletionGoal.option_dracula:
                win_condition = self.killed_dracula_2
            elif ctx.slot_data["completion_goal"] == CompletionGoal.option_battle_arena:
                win_condition = self.won_battle_arena
            else:
                win_condition = self.killed_dracula_2 and self.won_battle_arena

            # Send game clear if we've satisfied the win condition.
            if not ctx.finished_game and win_condition:
                ctx.finished_game = True
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

            # Update the tracker event flags
            if checked_set_events != self.client_set_events and ctx.slot is not None:
                event_bitfield = 0
                for index, (flag, flag_name) in enumerate(EVENT_FLAG_MAP.items()):
                    if checked_set_events[flag_name]:
                        event_bitfield |= 1 << index

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"castlevania_cotm_events_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.client_set_events = checked_set_events

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
