import time
from typing import TYPE_CHECKING, Set, Dict

from NetUtils import ClientStatus
import asyncio

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from . import data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class SonicRushClient(BizHawkClient):
    game = "Sonic Rush"
    system = "NDS"
    patch_suffix = ".aprush"
    local_checked_locations: Set[int]
    ram_mem_domain = "Main RAM"
    goal_complete = False
    received_items_count: int = 0
    location_name_to_id: dict[str, int] | None
    datapackage_requested = False

    # Vanilla addresses offsets
    selected_character_offset = 0x2c4560
    emeralds_buffer_offset = 0x2c4588
    extra_lives_buffer_offset = 0x2c45a4
    maybe_gamestate_offset = 0x2c45b4
    sonic_storyprog_offset = 0x2c468C
    extra_lives_sonic_offset = 0x2C468E
    chaos_emeralds_offset = 0x2C468F
    level_scores_sonic_offset = 0x2c4690
    extra_lives_blaze_offset = 0x2C46E6
    level_scores_blaze_offset = 0x2c46e8

    # AP addresses offsets
    received_offset = 0x2c475e
    zone_unlocks_sonic_offset = 0x2c4760
    zone_unlocks_blaze_offset = 0x2c4761
    progressive_level_unlocks_sonic_offset = 0x2c4762
    progressive_level_unlocks_blaze_offset = 0x2c4763
    special_stages_offset = 0x2c4764
    sol_emeralds_offset = 0x2c4765
    boss_flags_offset = 0x2c4766
    sidekick_showing_offset = 0x2c4767
    deathlink_flags_offset = 0x2c4768
    # savedata_initialized_offset = 0x2c476f

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.seed_verify = False
        self.received_deathlink = False
        self.location_name_to_id = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1
        return True

    def on_package(self, ctx, cmd, args) -> None:
        if cmd == "DataPackage":
            self.location_name_to_id = args["data"]["games"][self.game]["location_name_to_id"]
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.received_deathlink = True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        try:
            if ctx.slot_data is None:
                return
            if self.location_name_to_id is None:
                if not self.datapackage_requested:
                    await ctx.send_msgs([{"cmd": "GetDataPackage", "games": [self.game]}])
                    self.datapackage_requested = True
                    logger.info("Awaiting datapackage...")
                return

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx, [
                    (self.sonic_storyprog_offset, 1, self.ram_mem_domain),
                ]
            )

            # Return if save data not yet initialized, else it's 0xff, and that's bad
            # Also after booting the entire memory will be 0x00, which is also not good for receiving items
            if int.from_bytes(read_state[0]) == 0:
                return

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (self.received_offset, 2, self.ram_mem_domain),
                ]
            )

            received_in_sav = int.from_bytes(read_state[0], "little")

            for index in range(min(self.received_items_count, received_in_sav), len(ctx.items_received)):
                network_item = ctx.items_received[index]
                name = ctx.item_names.lookup_in_game(network_item.item)
                match name:
                    # Blaze's zone unlock flags are in zone order and not location order
                    case x if x in data.zone_names_without_f_zone:
                        await self.bizhawk_2x_set_flag(
                            ctx,
                            self.zone_unlocks_sonic_offset, data.zone_number_by_name["Sonic"][x]-1,
                            self.zone_unlocks_blaze_offset, data.zone_number_by_name["Blaze"][x]-1
                        )

                    case "F-Zone":
                        await self.bizhawk_2x_set_flag(
                            ctx,
                            self.zone_unlocks_sonic_offset, 7,
                            self.zone_unlocks_blaze_offset, 7
                        )
                    case "Progressive Level Select (Sonic)":
                        if index >= received_in_sav:
                            await self.bizhawk_increase_byte(ctx, self.progressive_level_unlocks_sonic_offset)
                    case "Progressive Level Select (Blaze)":
                        if index >= received_in_sav:
                            await self.bizhawk_increase_byte(ctx, self.progressive_level_unlocks_blaze_offset)
                    case x if " Chaos Emerald" in x:
                        bit = data.emerald_bits_by_name[x[:-14]]
                        if await self.bizhawk_2x_is_byte_equal(
                            ctx,
                            self.maybe_gamestate_offset, 3,
                            self.selected_character_offset, 0
                        ):
                            await self.bizhawk_set_flag(ctx, self.emeralds_buffer_offset, bit)
                        await self.bizhawk_set_flag(ctx, self.chaos_emeralds_offset, bit)
                    case x if " Sol Emerald" in x:
                        await self.bizhawk_set_flag(ctx, self.sol_emeralds_offset, data.emerald_bits_by_name[x[:-12]])
                    case "Tails":
                        await self.bizhawk_set_flag(ctx, self.sol_emeralds_offset, 0)
                    case "Cream":
                        await self.bizhawk_set_flag(ctx, self.sol_emeralds_offset, 1)
                    case "Kidnapping Tails":
                        await self.bizhawk_unset_flag(ctx, self.sidekick_showing_offset, 0)
                    case "Kidnapping Cream":
                        await self.bizhawk_unset_flag(ctx, self.sidekick_showing_offset, 1)
                    case "Extra Life (Sonic)":
                        if index >= received_in_sav:
                            if self.bizhawk_2x_is_byte_equal(
                                ctx,
                                self.selected_character_offset, 0,
                                self.maybe_gamestate_offset, 3
                            ):
                                await self.bizhawk_increase_byte(ctx, self.extra_lives_buffer_offset)
                            else:
                                await self.bizhawk_increase_byte(ctx, self.extra_lives_sonic_offset)
                    case "Extra Life (Blaze)":
                        if index >= received_in_sav:
                            if self.bizhawk_2x_is_byte_equal(
                                ctx,
                                self.selected_character_offset, 1,
                                self.maybe_gamestate_offset, 3
                            ):
                                await self.bizhawk_increase_byte(ctx, self.extra_lives_buffer_offset)
                            else:
                                await self.bizhawk_increase_byte(ctx, self.extra_lives_blaze_offset)
                    case "Halving Extra Lives (Sonic)":
                        if index >= received_in_sav:
                            if self.bizhawk_2x_is_byte_equal(
                                ctx,
                                self.selected_character_offset, 0,
                                self.maybe_gamestate_offset, 3
                            ):
                                await self.bizhawk_halve_byte(ctx, self.extra_lives_buffer_offset)
                            else:
                                await self.bizhawk_halve_byte(ctx, self.extra_lives_sonic_offset)
                    case "Halving Extra Lives (Blaze)":
                        if index >= received_in_sav:
                            if self.bizhawk_2x_is_byte_equal(
                                ctx,
                                self.selected_character_offset, 1,
                                self.maybe_gamestate_offset, 3
                            ):
                                await self.bizhawk_halve_byte(ctx, self.extra_lives_buffer_offset)
                            else:
                                await self.bizhawk_halve_byte(ctx, self.extra_lives_blaze_offset)
                    case _:
                        raise Exception("Bad item name received: " + name)
                if index >= received_in_sav:
                    await self.bizhawk_set_halfword(ctx, self.received_offset, index+1)
                self.received_items_count = index+1
                await asyncio.sleep(0.1)

            # Check for location checks
            locations_to_send = set()

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (self.special_stages_offset, 1, self.ram_mem_domain),
                    (self.boss_flags_offset, 1, self.ram_mem_domain),
                    (self.level_scores_sonic_offset, 84, self.ram_mem_domain),
                    (self.level_scores_blaze_offset, 84, self.ram_mem_domain),
                    (self.deathlink_flags_offset, 1, self.ram_mem_domain),
                ]
            )

            special_stages_checks = int.from_bytes(read_state[0])
            boss_flags_checks = int.from_bytes(read_state[1])
            level_scores_sonic: Dict[int, Dict[int, int]] = {}
            level_scores_blaze: Dict[int, Dict[int, int]] = {}
            for zone in range(7):
                level_scores_sonic[zone] = {}
                level_scores_blaze[zone] = {}
                for act in range(3):
                    offset = zone*12+act*4
                    level_scores_sonic[zone][act] = int.from_bytes(read_state[2][offset:(offset+4)], "little")
                    level_scores_blaze[zone][act] = int.from_bytes(read_state[3][offset:(offset+4)], "little")
            dl_flags = int.from_bytes(read_state[4])

            locations_to_send.add(self.location_name_to_id["Menu"])

            # Blaze's scores are in zone order and not location order
            # Sorry for this unreadable loop pile
            for char_tup in [
                ("Sonic", level_scores_sonic),
                ("Blaze", level_scores_blaze),
            ]:
                for zone_tup in [
                    (zone_index, data.zone_name_by_number[char_tup[0]][zone_index+1])
                    for zone_index in range(7)
                ]:
                    for act_tup in [
                        (0, "Act 1", 100000, ["only_acts", "all"]),
                        (1, "Act 2", 100000, ["only_acts", "all"]),
                        (2, "Boss", 50000, ["only_bosses", "all"]),
                    ]:
                        if char_tup[1][zone_tup[0]][act_tup[0]] != 0:
                            locations_to_send.add(
                                self.location_name_to_id[
                                    f"{zone_tup[1]} {act_tup[1]} ({char_tup[0]})"
                                ]
                            )
                        if ctx.slot_data["include_s_rank_checks"] in act_tup[3]:
                            if char_tup[1][zone_tup[0]][act_tup[0]] >= act_tup[2]:
                                locations_to_send.add(
                                    self.location_name_to_id[
                                        f"{zone_tup[1]} {act_tup[1]} S Rank ({char_tup[0]})"
                                    ]
                                )

            if boss_flags_checks & 1:
                locations_to_send.add(self.location_name_to_id["F-Zone (Sonic)"])
            if boss_flags_checks & 2:
                locations_to_send.add(self.location_name_to_id["F-Zone (Blaze)"])
            if boss_flags_checks & 4:
                locations_to_send.add(self.location_name_to_id["Extra Zone"])

            for zone in data.zone_names_without_f_zone:
                if special_stages_checks & (1 << (data.zone_number_by_name["Sonic"][zone]-1)):
                    locations_to_send.add(self.location_name_to_id[f"{zone} Special Stage"])

            # Send locations if there are any to send.
            if locations_to_send != self.local_checked_locations:
                self.local_checked_locations = locations_to_send
                if locations_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locations_to_send)}])

            # Check for receiving and sending deathlink
            if ctx.slot_data:
                if "deathlink" in ctx.slot_data:
                    if ("deathlink" not in ctx.tags) and ctx.slot_data["deathlink"]:
                        await ctx.update_death_link(True)
                    elif ("deathlink" in ctx.tags) and not ctx.slot_data["deathlink"]:
                        await ctx.update_death_link(False)
                else:
                    return
            if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                dl_flags_old = dl_flags
                if self.received_deathlink:
                    self.received_deathlink = False
                    if self.bizhawk_is_byte_equal(ctx, self.maybe_gamestate_offset, 3):
                        dl_flags |= 1
                if dl_flags & 2:
                    dl_flags &= ~2
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} failed to defeat Eggman")
                if not dl_flags == dl_flags_old:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(
                            self.deathlink_flags_offset, dl_flags.to_bytes(length=1, byteorder="little"),
                            self.ram_mem_domain
                        )],
                    )

            # Check for completing the goal and send it to the server
            if not self.goal_complete:
                goaled: bool
                match ctx.slot_data["goal"]:
                    case "bosses_once":
                        goaled = False
                        if ((level_scores_sonic[0][2] or level_scores_blaze[1][2]) and
                            (level_scores_sonic[1][2] or level_scores_blaze[3][2]) and
                            (level_scores_sonic[2][2] or level_scores_blaze[2][2]) and
                            (level_scores_sonic[3][2] or level_scores_blaze[0][2]) and
                            (level_scores_sonic[4][2] or level_scores_blaze[5][2]) and
                            (level_scores_sonic[5][2] or level_scores_blaze[4][2]) and
                            (level_scores_sonic[6][2] or level_scores_blaze[6][2])):
                            if ctx.slot_data["screw_f_zone"] or boss_flags_checks & 1 or boss_flags_checks & 2:
                                goaled = True
                    case "bosses_both":
                        goaled = True
                        for zone in range(7):
                            if not (level_scores_sonic[zone][2] and level_scores_blaze[zone][2]):
                                goaled = False
                                break
                        if not (ctx.slot_data["screw_f_zone"] or (boss_flags_checks & 1 and boss_flags_checks & 2)):
                            goaled = False
                    case "extra_zone":
                        goaled = bool(boss_flags_checks & 4)
                    case "100_percent":
                        goaled = True
                        for zone in range(7):
                            if not (level_scores_sonic[zone][2] and level_scores_blaze[zone][2]):
                                goaled = False
                                break
                        if not (ctx.slot_data["screw_f_zone"] or (boss_flags_checks & 1 and boss_flags_checks & 2 and
                                                                  boss_flags_checks & 4)):
                            goaled = False
                    case _:
                        raise Exception("Bad goal in slot data: " + ctx.slot_data["goal"])

                if goaled:
                    self.goal_complete = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
        except bizhawk.ConnectorError:
            pass

    async def bizhawk_set_flag(self, ctx: "BizHawkClientContext", address: int, bit: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_bits = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, (current_bits | (1 << bit)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain)
            ],
        )

    async def bizhawk_2x_set_flag(self, ctx: "BizHawkClientContext",
                                  address_1: int, bit_1: int, address_2: int, bit_2: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address_1, 1, self.ram_mem_domain),
                (address_2, 1, self.ram_mem_domain),
            ]
        )
        current_bits_1 = int.from_bytes(read_state[0])
        current_bits_2 = int.from_bytes(read_state[1])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address_1, (current_bits_1 | (1 << bit_1)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain),
                (address_2, (current_bits_2 | (1 << bit_2)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain),
            ],
        )

    async def bizhawk_unset_flag(self, ctx: "BizHawkClientContext", address: int, bit: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_bits = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, (current_bits & ~(1 << bit)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain)
            ],
        )

    async def bizhawk_increase_byte(self, ctx: "BizHawkClientContext", address: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_byte = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, min(current_byte + 1, 255).to_bytes(length=1, byteorder="little"), self.ram_mem_domain)
            ],
        )

    async def bizhawk_halve_byte(self, ctx: "BizHawkClientContext", address: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_byte = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, (current_byte // 2).to_bytes(length=1, byteorder="little"), self.ram_mem_domain)
            ],
        )

    async def bizhawk_is_byte_equal(self, ctx: "BizHawkClientContext", address: int, byte: int) -> bool:
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        read_byte = int.from_bytes(read_state[0])
        return read_byte == byte

    async def bizhawk_2x_is_byte_equal(self, ctx: "BizHawkClientContext",
                                       address_1: int, byte_1: int,
                                       address_2: int, byte_2: int) -> bool:
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address_1, 1, self.ram_mem_domain),
                (address_2, 1, self.ram_mem_domain),
            ]
        )
        read_byte_1 = int.from_bytes(read_state[0])
        read_byte_2 = int.from_bytes(read_state[1])
        return read_byte_1 == byte_1 and read_byte_2 == byte_2

    async def bizhawk_set_halfword(self, ctx: "BizHawkClientContext", address: int, halfword: int) -> None:
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (address, halfword.to_bytes(length=2, byteorder="little"),self.ram_mem_domain)
            ]
        )
