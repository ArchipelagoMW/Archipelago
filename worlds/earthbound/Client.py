import logging
import struct
import typing
import time
import uuid
from struct import pack
from .game_data.local_data import client_specials, world_version, hint_bits, item_id_table, money_id_table
from .game_data.text_data import text_encoder
from .gifting.gift_tags import gift_properties
from .gifting.trait_parser import wanted_traits, trait_interpreter, gift_exclusions

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any

snes_logger = logging.getLogger("SNES")

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

EB_ROMHASH_START = 0x00FFC0
WORLD_VERSION = 0x3FF0A0
ROMHASH_SIZE = 0x15

ITEM_MODE = ROM_START + 0x04FD76

ITEMQUEUE_HIGH = WRAM_START + 0xB576
ITEM_RECEIVED = WRAM_START + 0xB570
SPECIAL_RECEIVED = WRAM_START + 0xB572
MONEY_RECIVED = WRAM_START + 0xB5F1
SAVE_FILE = WRAM_START + 0xB4A1
GIYGAS_CLEAR = WRAM_START + 0x9C11
GAME_CLEAR = WRAM_START + 0x9C85
OPEN_WINDOW = WRAM_START + 0x8958
MELODY_TABLE = WRAM_START + 0x9C1E
EARTH_POWER_FLAG = WRAM_START + 0x9C82
CUR_SCENE = WRAM_START + 0x97B8
IS_IN_BATTLE = WRAM_START + 0x9643
DEATHLINK_ENABLED = ROM_START + 0x04FD74
DEATHLINK_TYPE = ROM_START + 0x04FD75
IS_CURRENTLY_DEAD = WRAM_START + 0xB582
GOT_DEATH_FROM_SERVER = WRAM_START + 0xB583
PLAYER_JUST_DIED_SEND_DEATHLINK = WRAM_START + 0xB584
IS_ABLE_TO_RECEIVE_DEATHLINKS = WRAM_START + 0xB585
CHAR_COUNT = WRAM_START + 0x98A4
OSS_FLAG = WRAM_START + 0x5D98
HINT_SCOUNT_IDS = ROM_START + 0x310250
SCOUTED_HINT_FLAGS = WRAM_START + 0xB621
MONEY_IN_BANK = WRAM_START + 0x9835
IS_ENERGYLINK_ENABLED = ROM_START + 0x04FD78
already_tried_to_connect = False


class EarthBoundClient(SNIClient):
    game = "EarthBound"
    patch_suffix = ".apeb"
    most_recent_connect: str = ""
    client_version: str = world_version
    hint_list: list[int] = []
    hinted_shop_locations: list[int] = []

    async def deathlink_kill_player(self, ctx: "SNIContext") -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read
        battle_hp = {
            1: WRAM_START + 0x9FBF,
            2: WRAM_START + 0xA00D,
            3: WRAM_START + 0xA05B,
            4: WRAM_START + 0xA0A9,
        }

        active_hp = {
            1: WRAM_START + 0x9A15,
            2: WRAM_START + 0x9A74,
            3: WRAM_START + 0x9AD3,
            4: WRAM_START + 0x9B32,
        }

        scrolling_hp = {
            1: WRAM_START + 0x9A13,
            2: WRAM_START + 0x9A72,
            3: WRAM_START + 0x9AD1,
            4: WRAM_START + 0x9B30,
        }

        deathlink_mode = await snes_read(ctx, DEATHLINK_TYPE, 1)
        oss_flag = await snes_read(ctx, OSS_FLAG, 1)
        is_currently_dead = await snes_read(ctx, IS_CURRENTLY_DEAD, 1)
        can_receive_deathlinks = await snes_read(ctx, IS_ABLE_TO_RECEIVE_DEATHLINKS, 1)
        is_in_battle = await snes_read(ctx, IS_IN_BATTLE, 1)
        char_count = await snes_read(ctx, CHAR_COUNT, 1)
        snes_buffered_write(ctx, GOT_DEATH_FROM_SERVER, bytes([0x01]))
        text_open = await snes_read(ctx, OPEN_WINDOW, 1)

        if text_open is None: #Catch None reads from client jank????????
            return

        if is_currently_dead[0] != 0x00 or can_receive_deathlinks[0] == 0x00:
            return

        # If suppression is set and we're not in a battle dont do deathlinks
        if oss_flag[0] != 0x00 and is_in_battle[0] == 0x00:
            return

        # Prevent overworld deaths while a menu is open
        if not is_in_battle[0] and text_open[0] != 0xFF:
            return

        for i in range(char_count[0]):
            w_cur_char = WRAM_START + 0x986F + i
            current_char = await snes_read(ctx, w_cur_char, 1)
            snes_buffered_write(ctx, active_hp[current_char[0]], bytes([0x00, 0x00]))
            snes_buffered_write(ctx, battle_hp[i + 1], bytes([0x00, 0x00]))
            if deathlink_mode[0] == 0 or is_in_battle[0] == 0:
                # This should be the check for instant or mercy. Write the value, call it here
                snes_buffered_write(ctx, scrolling_hp[current_char[0]], bytes([0x00, 0x00]))
        await snes_flush_writes(ctx)
        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

    def on_package(self, ctx, cmd: str, args: dict[str, typing.Any]) -> None:
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None)

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from SNIClient import snes_read

        rom_name = await snes_read(ctx, EB_ROMHASH_START, ROMHASH_SIZE)
        apworld_version = await snes_read(ctx, WORLD_VERSION, 16)

        item_handling = await snes_read(ctx, ITEM_MODE, 1)
        if rom_name is None or rom_name[:6] != b"MOM2AP":
            return False

        apworld_version = apworld_version.decode("utf-8").strip("\x00")
        if apworld_version != self.most_recent_connect and apworld_version != self.client_version:
            ctx.gui_error("Bad Version", f"EarthBound APWorld version {self.client_version} does not match generated version {apworld_version}")
            self.most_recent_connect = apworld_version
            return False

        ctx.game = self.game
        if item_handling[0] == 0x00:
            ctx.items_handling = 0b001
        else:
            ctx.items_handling = 0b111
        ctx.rom = rom_name

        death_link = await snes_read(ctx, DEATHLINK_ENABLED, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))
        return True

    async def game_watcher(self, ctx: "SNIContext") -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read, snes_write
        giygas_clear = await snes_read(ctx, GIYGAS_CLEAR, 0x1)
        game_clear = await snes_read(ctx, GAME_CLEAR, 0x1)
        item_received = await snes_read(ctx, ITEM_RECEIVED, 0x1)
        special_received = await snes_read(ctx, SPECIAL_RECEIVED, 0x1)
        money_received = await snes_read(ctx, MONEY_RECIVED, 0x2)
        save_num = await snes_read(ctx, SAVE_FILE, 0x1)
        text_open = await snes_read(ctx, OPEN_WINDOW, 1)
        melody_table = await snes_read(ctx, MELODY_TABLE, 2)
        earth_power_absorbed = await snes_read(ctx, EARTH_POWER_FLAG, 1)
        cur_script = await snes_read(ctx, CUR_SCENE, 1)
        rom = await snes_read(ctx, EB_ROMHASH_START, ROMHASH_SIZE)
        scouted_hint_flags = await snes_read(ctx, SCOUTED_HINT_FLAGS, 1)
        gift_target = await snes_read(ctx, WRAM_START + 0xB5E7, 2)
        outbound_gifts = await snes_read(ctx, WRAM_START + 0x31D0, 1)
        shop_scout = await snes_read(ctx, WRAM_START + 0x0770, 1)
        shop_scouts_enabled = await snes_read(ctx, ROM_START + 0x04FD77, 1)
        outgoing_energy = await snes_read(ctx, MONEY_IN_BANK, 4)
        if rom != ctx.rom:
            ctx.rom = None
            return
        
        if giygas_clear[0] & 0x01 == 0x01:  # Are we in the epilogue
            return

        if save_num[0] == 0x00:  # If on the title screen
            return

        if ctx.slot is None:
            return

        if outgoing_energy is None: #None Catcher
            return


        if f"GiftBoxes;{ctx.team}" not in ctx.stored_data:
            await ctx.send_msgs([{
                "cmd": "SetNotify",
                "keys": [f"GiftBoxes;{ctx.team}"]
            }])

        # GIFTING DATA
        if f"GiftBox;{ctx.team};{ctx.slot}" not in ctx.stored_data:
            local_giftbox = {
                            str(ctx.slot): {
                                "is_open": True,
                                "accepts_any_gift": False,
                                "desired_traits": wanted_traits,
                                "minimum_gift_data_version": 2,
                                "maximum_gift_data_version": 3}}
            await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"GiftBoxes;{ctx.team}",
                        "want_reply": False,
                        "default": {},
                        "operations": [{"operation": "update", "value": local_giftbox}]
                    }])
        
            await ctx.send_msgs([{
                        "cmd": "Get",
                        "keys": [f"GiftBox;{ctx.team};{ctx.slot}"]
                    }])

            await ctx.send_msgs([{
                        "cmd": "SetNotify",
                        "keys": [f"GiftBox;{ctx.team};{ctx.slot}", f"GiftBoxes;{ctx.team}"]
                    }])

        inbox = ctx.stored_data.get(f"GiftBox;{ctx.team};{ctx.slot}")
        motherbox = ctx.stored_data.get(f"GiftBoxes;{ctx.team}")
        if inbox:
            gift_item_name = "None"
            key, gift = next(iter(inbox.items()))
            if "item_name" in gift or "ItemName" in gift:
                gift_item_name = gift.get("item_name", gift.get("ItemName"))
            if gift_item_name in item_id_table and gift_item_name not in gift_exclusions:
                # If the name matches an EB item, convert it to one (even if not coming from EB)
                item = item_id_table[gift_item_name]
            else:
                item = trait_interpreter(gift)

            inbox_queue = await snes_read(ctx, WRAM_START + 0x3200, 1)
            # Pause if the receiver queue is full
            if not inbox_queue[0]:
                await snes_write(ctx, [(WRAM_START + 0x3200, bytes([item]))])
                inbox.pop(key)
                await ctx.send_msgs([{
                            "cmd": "Set",
                            "key": f"GiftBox;{ctx.team};{ctx.slot}",
                            "want_reply": False,
                            "default": {},
                            "operations": [{"operation": "pop", "value": key}]
                        }])

        # We're in the Gift selection menu. This should write the selected player's name into RAM
        # for parsing.
        # TODO; CHECK A SETNOTIFY HERE
        gift_target = int.from_bytes(gift_target, byteorder="little")

        # Giftbox checking for the gift menu UI
        if gift_target != 0x00 and motherbox is not None:
            gift_recipient = str(gift_target)
            recip_name = ctx.player_names[gift_target]
            recip_name = get_alias(recip_name, ctx.slot_info[gift_target].name)
            recip_name = text_encoder(recip_name, 20)
            if gift_recipient in motherbox:
                if "IsOpen" in motherbox[gift_recipient]:
                    motherbox[gift_recipient]["is_open"] = motherbox[gift_recipient].pop("IsOpen")
                    
            if gift_recipient in motherbox and motherbox[gift_recipient]["is_open"]:
                recip_name.extend(text_encoder(" (Open)", 20))
            else:
                recip_name.extend(text_encoder(" (Closed)", 20))
            recip_name.append(0x00)
            await snes_write(ctx, [(WRAM_START + 0xFF80, recip_name)])
            await snes_write(ctx, [(WRAM_START + 0xB5E7, bytes([0x00, 0x00]))])
            await snes_write(ctx, [(WRAM_START + 0xB573, bytes([0x00, 0x00]))])
            
            gift_flag_byte = await snes_read(ctx, WRAM_START + 0xB622, 1)
            gift_flag_byte = gift_flag_byte[0] | 0x04
            await snes_write(ctx, [(WRAM_START + 0xB622, bytes([gift_flag_byte]))])

        if outbound_gifts[0] != 0x00 and motherbox is not None:
            gift_buffer = await snes_read(ctx, WRAM_START + 0x31D1, 3)
            gift_item_id = gift_buffer[0]
            gift = gift_properties[gift_item_id]
            recipient = struct.unpack("H", gift_buffer[-2:])
            if str(recipient[0]) in motherbox:
                # Check if the player's box is open, refund if not
                if "IsOpen" in motherbox[str(recipient[0])]:
                    # Does the recipient 0 thing work if > 255? Will need some testing.
                    motherbox[str(recipient[0])]["is_open"] = motherbox[str(recipient[0])].pop("IsOpen")

                if "AcceptsAnyGift" in motherbox[str(recipient[0])]:
                    motherbox[str(recipient[0])]["accepts_any_gift"] = motherbox[str(recipient[0])].pop("AcceptsAnyGift")

                if "DesiredTraits" in motherbox[str(recipient[0])]:
                    motherbox[str(recipient[0])]["desired_traits"] = motherbox[str(recipient[0])].pop("DesiredTraits")

                if "Trait" in motherbox[str(recipient[0])]["desired_traits"]:
                    motherbox[str(recipient[0])]["desired_traits"]["trait"] = motherbox[str(recipient[0])]["desired_traits"].pop("Trait")

            if str(recipient[0]) in motherbox and motherbox[str(recipient[0])]["is_open"] and (any(
                        motherbox[str(recipient[0])]["accepts_any_gift"] or
                        trait["trait"] in motherbox[str(recipient[0])]["desired_traits"] for trait in gift.traits)):
                was_refunded = False
                recipient = recipient[0]
            else:
                was_refunded = True
                recipient = ctx.slot
            guid = str(uuid.uuid4())
            outgoing_gift = {
                            guid: {
                                "id": guid,
                                "item_name": gift.name,
                                "amount": 1,
                                "item_value": gift.value,
                                "traits": gift.traits,
                                "sender_slot": ctx.slot,
                                "receiver_slot": recipient,
                                "sender_team": ctx.team,
                                "receiver_team": ctx.team,  # ??? Should be Receive slot team?
                                "is_refund": was_refunded}}

            await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"GiftBox;{ctx.team};{recipient}",  # Receiver team here too
                        "want_reply": True,
                        "default": {},
                        "operations": [{"operation": "update", "value": outgoing_gift}]
                    }])
            
            gift_queue = await snes_read(ctx, WRAM_START + 0x31D4, 0x21)
            # shuffle the entire queue down 3 bytes
            outbox_full_byte = await snes_read(ctx, WRAM_START + 0xB622, 1)

            await snes_write(ctx, [(WRAM_START + 0x31D1, gift_queue)])
            await snes_write(ctx, [(WRAM_START + 0x31D0, bytes([outbound_gifts[0] - 1]))])
            outbox_full_byte = outbox_full_byte[0] & ~0x08
            await snes_write(ctx, [(WRAM_START + 0xB622, bytes([outbox_full_byte]))])

        if (game_clear[0] & 0x01 == 0x01) and not ctx.finished_game:  # Goal should ignore the item queue and textbox check
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        
        for i in range(6):
            if scouted_hint_flags[0] & hint_bits[i]:
                if i not in self.hint_list:
                    scoutable_hint = await snes_read(ctx, HINT_SCOUNT_IDS + (i * 3), 3)
                    if not scoutable_hint[2]:
                        scoutable_hint = (int.from_bytes(scoutable_hint[:2], byteorder="little") + 0xEB0000)
                        self.hint_list.append(i)
                        await ctx.send_msgs([{"cmd": "CreateHints", "locations": [scoutable_hint], "player": ctx.player}])
                    else:
                        hint = self.slot_data['hint_man_hints'][i]
                        await ctx.send_msgs([{"cmd": "CreateHints", "locations": [hint[0]], "player": hint[1]}])
                        self.hint_list.append(i)
        
        if shop_scout[0] and shop_scouts_enabled[0]:
            shop_slots = []
            for i in range(7):
                slot_id = (0xEB0FF9 + (shop_scout[0] * 7) + i)
                if slot_id in ctx.server_locations and slot_id not in self.hinted_shop_locations:
                    shop_slots.append(slot_id)
            
            if shop_slots:
                if shop_scouts_enabled[0] == 2:
                    await ctx.send_msgs([{"cmd": "CreateHints", "locations": shop_slots, "player": ctx.slot}])
                    await snes_write(ctx, [(WRAM_START + 0x0770, bytes([0x00]))])
                else:
                    prog_shops = []
                    await ctx.send_msgs([{"cmd": "LocationScouts", "locations": shop_slots, "create_as_hint": 0}])
                    for location in shop_slots:
                        if location in ctx.locations_info:
                            self.hinted_shop_locations.append(location)
                            if ctx.locations_info[location].flags & 0x01:
                                prog_shops.append(location)
                    if prog_shops:
                        await ctx.send_msgs([{"cmd": "CreateHints", "locations": prog_shops, "player": ctx.slot}])

        melody_data = f"{ctx.team}_{ctx.slot}_melody_status"
        earth_power_data = f"{ctx.team}_{ctx.slot}_earthpower"
        current_melodies = int.from_bytes(melody_table, "little")
        earth_power_state = int.from_bytes(earth_power_absorbed, "little")

        if melody_data not in ctx.stored_data or (ctx.stored_data[melody_data] != current_melodies) or (ctx.stored_data[earth_power_data] != earth_power_state):
            await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": melody_data,
                        "default": None,
                        "want_reply": True,
                        "operations": [{"operation": "replace", "value": int.from_bytes(melody_table, "little")}]},
                        {
                        "cmd": "Set",
                        "key": earth_power_data,
                        "default": None,
                        "want_reply": True,
                        "operations": [{"operation": "replace", "value": int.from_bytes(earth_power_absorbed, "little")}]
                    }])

        # death link handling goes here
        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            send_deathlink = await snes_read(ctx, PLAYER_JUST_DIED_SEND_DEATHLINK, 1)
            currently_dead = send_deathlink[0] != 0x00
            if send_deathlink[0] != 0x00:
                snes_buffered_write(ctx, PLAYER_JUST_DIED_SEND_DEATHLINK, bytes([0x00]))
            await ctx.handle_deathlink_state(currently_dead)

        new_checks = []
        from .game_data.local_data import check_table

        location_ram_data = await snes_read(ctx, WRAM_START + 0x9C00, 0x88)
        shop_location_flags = await snes_read(ctx, WRAM_START + 0xB721, 0x41)
        for loc_id, loc_data in check_table.items():
            if loc_id not in ctx.locations_checked:
                if loc_id >= 0xEB1000:
                    data = shop_location_flags[loc_data[0]]
                else:
                    data = location_ram_data[loc_data[0]]
                masked_data = data & (1 << loc_data[1])
                bit_set = masked_data != 0
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if bit_set != invert_bit and loc_id in ctx.server_locations:
                    if text_open[0] == 0xFF or shop_scout[0]:  # Don't check locations while in a textbox
                        new_checks.append(loc_id)
                        
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_slot(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
            await snes_write(ctx, [(WRAM_START + 0x0770, bytes([0]))])

        if item_received[0] or special_received[0] != 0x00 or money_received[0] != 0x00:  # If processing any item from the server
            return

        is_energylink_enabled = await snes_read(ctx, IS_ENERGYLINK_ENABLED, 1)
        is_requesting_energy = await snes_read(ctx, WRAM_START + 0x0790, 1)
        energy_withdrawal = await snes_read(ctx, WRAM_START + 0x0796, 4)
        ctx.set_notify(f"EnergyLink{ctx.team}")
        energy = ctx.stored_data.get(f"EnergyLink{ctx.team}", 0)
        exchange_rate = 1000000
        if is_energylink_enabled[0]:

            deposited_energy = int.from_bytes(outgoing_energy, byteorder="little")
            if deposited_energy:
                deposited_energy *= exchange_rate
                await snes_write(ctx, [(MONEY_IN_BANK, (0x00).to_bytes(4, byteorder="little"))])
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "slot": ctx.slot, "operations":
                        [{"operation": "add", "value": deposited_energy},
                            {"operation": "max", "value": 0}]}])

            if is_requesting_energy[0] and energy:  # This is just to pull the current number for a display.
                energy //= exchange_rate
                if energy > 9999999:
                    energy = 9999999
                    cap_flag = await snes_read(ctx, WRAM_START + 0xB623, 1)
                    cap_flag = int.from_bytes(cap_flag)
                    cap_flag |= 0x20
                    await snes_write(ctx, [(WRAM_START + 0xB623, cap_flag.to_bytes(1, byteorder="little"))])

                await snes_write(ctx, [(WRAM_START + 0x0792, int(energy).to_bytes(4, byteorder="little"))])
                await snes_write(ctx, [(WRAM_START + 0x0790, (0x00).to_bytes(1, byteorder="little"))])

            if any(energy_withdrawal) and energy:
                withdrawal = int.from_bytes(energy_withdrawal, byteorder="little")
                withdrawal *= exchange_rate
                energy = ctx.stored_data.get(f"EnergyLink{ctx.team}", 0)  # Refresh the value

                if withdrawal > energy:
                    energy_success = 2
                    withdrawal = energy
                else:
                    energy_success = 1

                await snes_write(ctx, [(WRAM_START + 0x97D0, (withdrawal // exchange_rate).to_bytes(4, byteorder="little"))])
                await snes_write(ctx, [(WRAM_START + 0x0796, (0x00).to_bytes(4, byteorder="little"))])
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "slot": ctx.slot, "operations":
                        [{"operation": "add", "value": (withdrawal * -1)},
                            {"operation": "max", "value": 0}]}])
                await snes_write(ctx, [(WRAM_START + 0x079A, energy_success.to_bytes(1, byteorder="little"))])  # Signal the game to continue

        if cur_script[0]:  # Stop items during cutscenes
            return

        recv_count = await snes_read(ctx, ITEMQUEUE_HIGH, 2)
        recv_index = struct.unpack("H", recv_count)[0]
        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            item_id = (item.item - 0xEB0000)
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_slot(item.item), "red", "bold"),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))

            snes_buffered_write(ctx, ITEMQUEUE_HIGH, pack("H", recv_index))
            if item_id <= 0xFD:
                snes_buffered_write(ctx, WRAM_START + 0xB570, bytes([item_id]))
            elif item_id in money_id_table:
                snes_buffered_write(ctx, WRAM_START + 0xB5F1, bytes([list(money_id_table).index(item_id) + 1]))
            else:
                snes_buffered_write(ctx, WRAM_START + 0xB572, bytes([client_specials[item_id]]))

        await snes_flush_writes(ctx)


def get_alias(alias: str, slot_name: str) -> str:
    try:
        index = alias.index(f" ({slot_name}")
    except ValueError:
        return alias
    return alias[:index]
