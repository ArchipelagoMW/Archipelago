from typing import TYPE_CHECKING, Set
from .locations import base_id, get_location_names_to_ids
from .text import cvcotm_string_to_bytearray
from .options import CompletionGoal, DeathLink

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
import base64
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


# These flags are communicated to the tracker as a bitfield using this order.
# Modifying the order will cause undetectable autotracking issues.
EVENT_FLAG_MAP = {
    0x2A: "FLAG_HIT_IRON_MAIDEN_SWITCH",
    0xB2: "FLAG_WON_BATTLE_ARENA",
    0xB3: "FLAG_DEFEATED_CERBERUS",
    0xB4: "FLAG_DEFEATED_NECROMANCER",
    0xB5: "FLAG_DEFEATED_IRON_GOLEM",
    0xB6: "FLAG_DEFEATED_ADRAMELECH",
    0xB7: "FLAG_DEFEATED_DRAGON_ZOMBIES",
    0xB8: "FLAG_DEFEATED_DEATH",
    0xB9: "FLAG_DEFEATED_CAMILLA",
    0xBA: "FLAG_DEFEATED_HUGH",
    0xBB: "FLAG_DEFEATED_DRACULA_I",
    0xBC: "FLAG_DEFEATED_DRACULA_II"
}


class CastlevaniaCotMClient(BizHawkClient):
    game = "Castlevania - Circle of the Moon"
    system = "GBA"
    patch_suffix = ".apcvcotm"
    local_dss = {}
    self_induced_death = False
    local_checked_locations: Set[int]
    client_set_events = {flag_name: False for flag, flag_name in EVENT_FLAG_MAP.items()}
    killed_dracula_2 = False
    won_battle_arena = False
    sent_message_queue = []
    death_causes = []
    currently_dead = False
    synced_set_events = False
    saw_arena_win_message = False

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            game_names = await bizhawk.read(ctx.bizhawk_ctx, [(0xA0, 0xC, "ROM"), (0x7FFF00, 12, "ROM")])
            if game_names[0].decode("ascii") != "DRACULA AGB1":
                return False
            if game_names[1] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                logger.info("ERROR: You appear to be running an unpatched version of Castlevania: Circle of the Moon. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if game_names[1].decode("ascii") != "ARCHIPELAG02":
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your client version against the version being "
                            "used by the generator.")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(0x7FFF10, 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
            if "cause" in args["data"]:
                cause = args["data"]["cause"]
                if len(cause) > 300:
                    cause = cause[0x00:0x89]
            else:
                cause = f"{args['data']['source']} killed you!"

            # Highlight the player that killed us in the game's orange text.
            if args['data']['source'] in cause:
                words = cause.split(args['data']['source'], 1)
                cause = words[0] + "「" + args['data']['source'] + "」" + words[1]

            self.death_causes += [cause]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        try:
            read_state = await bizhawk.read(ctx.bizhawk_ctx, [(0x45D8, 1, "EWRAM"),
                                                              (0x25374, 32, "EWRAM"),
                                                              (0x25674, 20, "EWRAM"),
                                                              (0x253D0, 2, "EWRAM"),
                                                              (0x2572C, 3, "EWRAM"),
                                                              (0x2572F, 8, "EWRAM"),
                                                              (0x25300, 2, "EWRAM"),
                                                              (0x25308, 2, "EWRAM"),
                                                              (0x26000, 1, "EWRAM"),
                                                              (0x50, 1, "EWRAM"),
                                                              (0x2562C, 4, "EWRAM"),
                                                              (0x253FC, 1, "EWRAM")])

            game_state = int.from_bytes(read_state[0], "little")
            flag_bytes = read_state[1]
            cards_array = list(read_state[2])
            max_ups_array = list(read_state[4])
            magic_items_array = list(read_state[5])
            num_received_items = int.from_bytes(bytearray(read_state[3]), "little")
            queued_textbox = int.from_bytes(bytearray(read_state[6]), "little")
            delay_timer = int.from_bytes(bytearray(read_state[7]), "little")
            cutscene = int.from_bytes(bytearray(read_state[8]), "little")
            nathan_state = int.from_bytes(bytearray(read_state[9]), "little")
            health = int.from_bytes(bytearray(read_state[10]), "little")
            area = int.from_bytes(bytearray(read_state[11]), "little")

            # If there's no textbox already queued, the delay timer is 0, we are not in a cutscene, and Nathan's current
            # state value is not 0x34 (using a save room), we can safely inject a textbox message.
            ok_to_inject = not queued_textbox and not delay_timer and not cutscene and nathan_state != 0x34

            # Make sure we are in the Gameplay or Credits states before detecting sent locations.
            # If we are in any other state, such as the Game Over state, reset the textbox buffers back to 0 so that we
            # don't receive the most recent item upon loading back in.
            #
            # If the intro cutscene floor broken flag is not set, then assume we are in the demo; at no point during
            # regular gameplay will this flag not be set.
            if game_state not in [0x6, 0x21] or not flag_bytes[6] & 0x02:
                self.currently_dead = False
                await bizhawk.write(ctx.bizhawk_ctx, [(0x25300, [0 for _ in range(12)], "EWRAM")])
                return

            # Enable DeathLink if it's in our slot_data.
            if "DeathLink" not in ctx.tags and ctx.slot_data["death_link"]:
                await ctx.update_death_link(True)

            # Send a DeathLink if we died on our own independently of receiving another one.
            if "DeathLink" in ctx.tags and health == 0 and not self.currently_dead:
                self.currently_dead = True
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} perished. Dracula has won!")

            # Scout all Locations and get our Set events.
            if ctx.locations_info == {}:
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": [code for name, code in get_location_names_to_ids().items()],
                    "create_as_hint": 0
                }])
                await ctx.send_msgs([{
                    "cmd": "Get",
                    "keys": [f"castlevania_cotm_events_{ctx.team}_{ctx.slot}"]
                }])
                # Some other parts of this need the scouted Location info and Set events, so return now.
                return

            # Update the Dracula II and Battle Arena events already being done on past separate sessions for if the
            # player is running the Battle Arena and Dracula goal.
            if f"castlevania_cotm_events_{ctx.team}_{ctx.slot}" in ctx.stored_data:
                if ctx.stored_data[f"castlevania_cotm_events_{ctx.team}_{ctx.slot}"] is not None:
                    if ctx.stored_data[f"castlevania_cotm_events_{ctx.team}_{ctx.slot}"] & 0x1:
                        self.won_battle_arena = True

                    if ctx.stored_data[f"castlevania_cotm_events_{ctx.team}_{ctx.slot}"] & 0x800:
                        self.killed_dracula_2 = True

            # Capture all the Locations with local DSS Cards, so we can trigger the Location check off the Card being
            # put in the inventory by the game.
            if self.local_dss == {}:
                self.local_dss = {loc.item & 0xFF: location_id for location_id, loc in ctx.locations_info.items()
                                  if loc.player == ctx.slot and (loc.item >> 8) & 0xFF == 0xE6}

            # If we won the Battle Arena, haven't seen the win message yet, and are in the Arena at the moment, pop up
            # the win message while playing the game's unused Theme of Simon Belmont fanfare.
            if self.won_battle_arena and not self.saw_arena_win_message and area == 0x0E \
                    and ok_to_inject and not self.currently_dead:
                win_message = cvcotm_string_to_bytearray("      A 「WINNER」 IS 「YOU」!▶", "little middle", 0,
                                                         wrap=False)
                await bizhawk.write(ctx.bizhawk_ctx, [(0x25300, [0x1D, 0x82], "EWRAM"),
                                                      (0x25306, [0x04], "EWRAM"),
                                                      (0x7CEB00, win_message, "ROM")])
                self.saw_arena_win_message = True

            # If we have any queued death causes, handle DeathLink giving here.
            elif self.death_causes and ok_to_inject and not self.currently_dead:

                # Inject the oldest cause as a textbox message and play the Dracula charge attack sound.
                death_text = self.death_causes[0]
                death_writes = [(0x25300, [0x1D, 0x82], "EWRAM"),
                                (0x25306, [0xAB, 0x01], "EWRAM")]

                # If we are in the Battle Arena and are not using the On Including Arena DeathLink option, extend the
                # DeathLink message and don't actually kill Nathan.
                if ctx.slot_data["death_link"] != DeathLink.option_arena_on and area == 0x0E:
                    death_text += "◊The Battle Arena nullified the DeathLink. Go fight fair and square!"
                else:
                    # Otherwise, kill Nathan by giving him a 9999 damage-dealing poison status that hurts him as soon as
                    # the death cause textbox is dismissed.
                    death_writes += [(0xD0, [0x02], "EWRAM"),
                                     (0xD8, [0x38], "EWRAM"),
                                     (0xDE, [0x0F, 0x27], "EWRAM")]

                # Add the final death text and write the whole shebang.
                death_writes += [(0x7CEB00, cvcotm_string_to_bytearray(death_text + "◊", "big middle", 0), "ROM")]
                await bizhawk.write(ctx.bizhawk_ctx, death_writes)

                # Delete the oldest death cause that we just wrote and set currently_dead to True so the client doesn't
                # think we just died on our own on the subsequent frames before the Game Over state.
                del(self.death_causes[0])
                self.currently_dead = True

            # If we have a queue of Locations to inject "sent" messages with, do so before giving any subsequent Items.
            elif self.sent_message_queue and ok_to_inject and not self.currently_dead:
                loc = self.sent_message_queue[0]
                # Truncate the Item name at 300 characters. ArchipIDLE's FFXIV Item is 214 characters, for comparison.
                item_name = ctx.item_names[ctx.locations_info[loc].item]
                if len(item_name) > 300:
                    item_name = item_name[:300]
                # Truncate the player name at 50 characters. Player names are normally capped at 16 characters, but
                # there is no limit on ItemLink group names.
                player_name = ctx.player_names[ctx.locations_info[loc].player]
                if len(player_name) > 50:
                    player_name = player_name[:50]

                sent_text = cvcotm_string_to_bytearray(f"「{item_name}」 sent to 「{player_name}」◊", "big middle", 0)

                # Set the correct sound to play depending on the Item's classification.
                if ctx.locations_info[loc].flags & 0b011:  # Progression or Useful
                    mssg_sfx_id = 0x1B4
                elif ctx.locations_info[loc].flags & 0b100:  # Trap
                    mssg_sfx_id = 0x7A
                else:  # Filler
                    mssg_sfx_id = 0x1B3

                await bizhawk.write(ctx.bizhawk_ctx, [(0x25300, [0x1D, 0x82], "EWRAM"),
                                                      (0x25306, bytearray(int.to_bytes(
                                                          mssg_sfx_id, 2, "little")), "EWRAM"),
                                                      (0x7CEB00, sent_text, "ROM")])

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
                item_type = next_item.item & 0xFF00
                item_index = next_item.item & 0xFF
                if item_type == 0xE600:  # Card
                    inv_offset = 0x25674
                    inv_array = cards_array
                    mssg_sfx_id = 0x1B4
                elif item_type == 0xE800:  # Magic Item
                    inv_offset = 0x2572F
                    inv_array = magic_items_array
                    mssg_sfx_id = 0x1B4
                    if item_index > 5:  # The unused Map's index is skipped over.
                        item_index -= 1
                else:  # Max Up
                    inv_offset = 0x2572C
                    mssg_sfx_id = 0x1B3
                    inv_array = max_ups_array

                item_name = ctx.item_names[next_item.item]
                player_name = ctx.player_names[next_item.player]
                # Truncate the player name at 50 characters.
                if len(player_name) > 50:
                    player_name = player_name[:50]

                received_text = cvcotm_string_to_bytearray(f"「{item_name}」 received from "
                                                           f"「{player_name}」◊", "big middle", 0)

                await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                            [(0x25300, [0x1D, 0x82], "EWRAM"),
                                             (0x25304, [1], "EWRAM"),
                                             (0x25306, bytearray(int.to_bytes(mssg_sfx_id, 2, "little")), "EWRAM"),
                                             (inv_offset + item_index, [inv_array[item_index] + 1], "EWRAM"),
                                             (0x7CEB00, received_text, "ROM")],
                                            # Make sure the number of received items is still what we expected it to be.
                                            [(0x253D0, read_state[3], "EWRAM")]),

            locs_to_send = set()

            # Check for set Location and event flags.
            checked_set_events = {flag_name: False for flag, flag_name in EVENT_FLAG_MAP.items()}
            for byte_index, byte in enumerate(flag_bytes):
                for i in range(8):
                    and_value = 0x01 << i
                    if byte & and_value != 0:
                        flag_id = byte_index * 8 + i

                        location_id = flag_id + base_id
                        if location_id in ctx.server_locations:
                            locs_to_send.add(location_id)

                        if flag_id in EVENT_FLAG_MAP:
                            checked_set_events[EVENT_FLAG_MAP[flag_id]] = True

                            # Update the client's status for the Battle Arena and Dracula goals.
                            if flag_id == 0xB2:
                                self.won_battle_arena = True

                            if flag_id == 0xBC:
                                self.killed_dracula_2 = True

            # Check for acquired local DSS Cards.
            for byte_index, byte in enumerate(cards_array):
                if byte and byte_index in self.local_dss:
                    locs_to_send.add(self.local_dss[byte_index])

            # Send Locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    # Capture all the Locations with non-local Items to send that are in ctx.missing_locations
                    # (the ones that were definitely never sent before).
                    self.sent_message_queue += [loc for loc in locs_to_send if loc in ctx.missing_locations and
                                                ctx.locations_info[loc].player != ctx.slot]

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
