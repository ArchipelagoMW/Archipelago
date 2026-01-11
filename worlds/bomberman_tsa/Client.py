import typing
import logging
from typing import TYPE_CHECKING, Set, Optional, Dict, Any

from NetUtils import ClientStatus
#from .Items import id_to_string
from base64 import b64encode
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .gamemaps import *
from .planet_select import get_planet_selection, highlight_planets
from .com_ap_methods import  randomize_multi_table, split_into_xbit_chunks, ramdomize_table_with_exclude
import time
import random

logger = logging.getLogger("Client")

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext



# def ramdomize_table(tbl,entrysize):
#     split_table = split_into_xbit_chunks(tbl,entrysize)
#     random.shuffle(split_table)
#     result = b''.join(split_table)
#     return result

# def ramdomize_table_with_exclude(tbl,entrysize,excepts):
#     split_table = split_into_xbit_chunks(tbl,entrysize)
#     idxshuffle = []
#     new_table = []
#     for x in range(len(split_table)):
#         idxshuffle.append(x)
#         new_table.append(b'/x00/x00/x00/x00')
#     random.shuffle(idxshuffle)
#     for idx in range(len(split_table)):
#         if idx in excepts:
#             new_table[idx] = split_table[idx]
#             continue
#         randidx = idxshuffle.pop(0)
#         while randidx in excepts:
#             randidx = idxshuffle.pop(0)
#         new_table[idx] = split_table[randidx]
#     result = b''.join(new_table)
#     return result

# def randomize_multi_table(tbl,size1,tb2,size2,excepts):
#     split_table1 = split_into_xbit_chunks(tbl,size1)
#     split_table2 = split_into_xbit_chunks(tb2,size2)
#     idxshuffle = []
#     new_table1 = []
#     new_table2 = []
#     for x in range(len(split_table1)):
#         idxshuffle.append(x)
#         new_table1.append(b'/x00')
#         new_table2.append(b'/x00')
#     random.shuffle(idxshuffle)

#     for idx in range(len(split_table1)):
#         #logger.warning(f"{idx} : {idxshuffle}")
#         if idx in excepts:
#             new_table1[idx] = split_table1[idx]
#             new_table2[idx] = split_table2[idx]
#             continue 
#         randidx = idxshuffle.pop(0)
#         while randidx in excepts:
#             randidx = idxshuffle.pop(0)
#         #logger.warning(f"{idx} - {randidx}")
#         new_table1[idx] = split_table1[randidx]
#         new_table2[idx] = split_table2[randidx]

#     out_tbl_1 = b''.join(new_table1)
#     out_tbl_2 = b''.join(new_table2)
#     return out_tbl_1, out_tbl_2

# def split_into_xbit_chunks(byte_array,size):
#    #Splits a byte array into chunks of 32 bits (4 bytes).

#     chunks = []
#     for i in range(0, len(byte_array), size):
#         chunk = byte_array[i:i + size]
#         # If the last chunk is less than 4 bytes, pad it with zeros
#         if len(chunk) < size:
#             chunk += b'\x00' * (size - len(chunk)) 
#         chunks.append(chunk)
#     return chunks


class BombTSAClient(BizHawkClient):
    game = "Bomberman The Second Attack"
    system = "N64"
    patch_suffix = ".apbombtsa"
    #rom: typing.Optional[bytes] = None
    local_checked_locations: Set[int]
    rom_slot_name: Optional[str]

    death_link: bool = False
    sending_death_link: bool = True
    pending_death_link: bool = False

    game_goal = 0
    noah_boss = 0
    planet_required = 7
    noah_access = 0
    music_rando = False
    efx_rando = False
    sfx_rando = False
    startbomb = 0

    door_list = {}
    firedown = False

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.rom_slot_name = None
        self.game_state = False
        self.pommy_command = None
        self.fire_command = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        # Borrowed some authentication code from Kirby 64's apworld
        from CommonClient import logger
        rom_data = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
            (0x20, 0xD, "ROM"), # 0 Rom Name
            (0x99FD0, 0x10,  "ROM"), # 1 Game Options
            (0x9A000, 0x32, "ROM"), # 2 Slot name
            (0x99FE0, 0x20, "ROM"), # 3 Slot Data
            (0x160664, 0x4B0, "RDRAM"), # 4 Music Data Part 1
            (0x160404, 0x258, "RDRAM"), # 5 Music Data Part 2
            (0x00, 0x28, "EEPROM"), # 6 Save data
            ]
        )
        filedata = [0, 0, 0, 0, 0, 0, 0, 0, 134, 2, 0, 0, 146, 134, 178, 186, 0, 252, 99, 199, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 205]
        #game_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x1FFF200, 21, "ROM")]))[0])
        try:
            # Check ROM name/patch version
            rom_name = rom_data[0].decode("ascii")
            if rom_name != "BOMBERMANTSAU":
                return False  # Not a Bomberman The Second Attack ROM
            try:
                #slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0xB86500, 32, "ROM")]))[0]
                slot_name_bytes = rom_data[2]
                self.rom_slot_name = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
            
            except UnicodeDecodeError:
                logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
                return False
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        # This is a Bomberman The Second Attack ROM
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.command_processor.commands["pommy"] = cmd_pommy
        ctx.command_processor.commands["fire"] = cmd_fire

        game_options = rom_data[1]
        self.noah_boss = rom_data[0]
        self.game_goal = game_options[1]
        deathlink = game_options[2]
        self.planet_required = game_options[5]
        self.noah_access = game_options[4]
        self.startbomb = game_options[6]
        self.pommyshop = game_options[8]


        if self.pommyshop:
            await ctx.send_msgs([{"cmd": "LocationScouts", "locations": SHOP_HINT_IDS, "create_as_hint": 1}])

        if deathlink:
            self.death_link = True

        if game_options[9] & 1:
            self.efx_rando = True
        if game_options[9] & 2:
            self.sfx_rando = True
        if game_options[9] & 4:
            self.music_rando = True
            music_table1, music_table2 = randomize_multi_table(rom_data[4],0x10,rom_data[5],0x8,INVALID_SONGS)
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0x160664, music_table1 , "RDRAM"),
                (0x160404, music_table2 , "RDRAM")
                ])

        ctx.want_slot_data = True

        logger.info("Start a game file to connect")

        return True
        

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                assert ctx.slot is not None
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)
    
    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        await ctx.send_death("Bomberman is dead.")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.rom_slot_name

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger



        try:
            ram_data = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                (0xAD700, 0x70, "RDRAM"), # 0 Stats
                (0xAC2C0, 0x50, "RDRAM"), # 1 Flag data
                #(0xABD47, 0x05, "RDRAM"), # 2 Stage
                (0xABD40, 0xC, "RDRAM"), # 2 Stage/ Game Status
                (0x255108, 0x04, "RDRAM"), # 3 In Stage
                (0xB560C, 0x04, "RDRAM"), # 4 In Shop
                (0xABD50, 0x20, "RDRAM"), # 5 Money / Pommy
                (0x410000, 0x01, "RDRAM"), # 6 Expansion
                (0xA02B8,0x20, "RDRAM"), # 7 Pad Read

                (0xABCC8,0x4, "RDRAM"), # 8 Stage Sel Target
                (0x255030,0x10, "RDRAM"), # 9 Planetsel check
                (0x1D0140,0x20, "RDRAM"), # A Free RAM
                (0x8F913,0x1, "RDRAM"), # B Display Health
                (DOOR_OFFSETS[4],0x4, "RDRAM"), # C Neverland Door
                (DOOR_OFFSETS[5],0x4, "RDRAM"), # D Epikyur Door
                (DOOR_OFFSETS[6],0x4, "RDRAM"), # E Thantos Door
                (DOOR_OFFSETS[7],0x4, "RDRAM"), # F Noah Door

                (0x160664, 0x4B0, "RDRAM"), # 10 Music Data
                (0x160404, 0x258, "RDRAM"), # 11 Music Data Part 2
                (0x927D0, 0x2B0, "RDRAM"), # 12 EFX table
                (0x182724, 0x4, "RDRAM"), # 13 SFX first entry
                ]
            )#0x16523F


            outbound_writes = []

            stat_data = ram_data[0]
            flag_data = ram_data[1]
            powerup_check = stat_data[0x40]
            cur_stage = ram_data[2][7]
            free_ram = ram_data[0xA]
            game_status = int.from_bytes(ram_data[2][0:4], byteorder='big', signed = False)
            mapid = int.from_bytes(ram_data[2][-2:], byteorder='big', signed = False)
            instage = ram_data[3]
            inshop = int.from_bytes(ram_data[4], byteorder='big', signed = False)
            #gaurdian_spawn = ram_data[4]
            money = ram_data[5][0:4]
            pommy_form = ram_data[5][0x10]
            pommy_food1 = ram_data[5][0x11]
            pommy_food2 = ram_data[5][0x12]
            pommy_food3 = ram_data[5][0x13]
            pommy_check = ram_data[5][0x14]
            planet_sel_check = ram_data[9]

            eventbytes = flag_data[0x3C:0x40]
            health_cur = stat_data[0x5F]
            health_max = ram_data[0xB][0]
            #health_max = stat_data[0x63]
            exp_byte = ram_data[6][0]
            pad_read = ram_data[7]
            stage_selection = ram_data[8]

            watched_intro = flag_data[0x1D] & 0x10
            armor = flag_data[0x1D]
            boss_clear = flag_data[0x1E]
            stage_clear = flag_data[0x1F]
            full_power = flag_data[0x29]
            recv_index = free_ram[0]

            bombtype = stat_data[0x3B]
            sfx_check = int.from_bytes(ram_data[0x13], byteorder='big', signed = False)
            
            recv_action = 0
            # Check if game file is loaded
            if watched_intro == 0x00:
                return
            self.game_state = True
            
            # Open Stage Select TEMP
            #stage_pointer_table = [0x60,0x00,0x50,0x28, 0x60,0x00,0x50,0x28, 0x60,0x00,0x50,0x28, 0x60,0x00,0x50,0x28,]
            #outbound_writes.append((0x255108, bytearray(stage_pointer_table), "RDRAM"))

            # Deathlink
            if self.death_link:
                await ctx.update_death_link(self.death_link)
            if self.pending_death_link:
                outbound_writes.append((0xB8887, bytearray([0x02]), "RDRAM"))
                outbound_writes.append((0xB888F, bytearray([0x26]), "RDRAM"))
                self.pending_death_link = False
                self.sending_death_link = True
            if "DeathLink" in ctx.tags  and ctx.last_death_link + 1 < time.time():
                if health_cur == 0 and not self.sending_death_link:
                #if death_read == 0 and not self.sending_death_link:
                    await self.send_deathlink(ctx)
                elif health_cur  != 0:
                    self.sending_death_link = False
            
            # Autoclear Horizon Puzzles
            #outbound_writes.append((0xAD4FC, bytearray([0x01]), "RDRAM"))
            # Patch Door code
            #if exp_byte == 0x00:
            #    outbound_writes.append((0x410000, DOOR_PATCH, "RDRAM"))
            # Check Locations
            locs_to_send = set()

            # Stage Clears
    
            # Handle Locations
            # LocationID: [ADDRESS, MASK]
            # Flag Locations
            for loc_id, ary in FLAG_MAP.items():
                offset = ary[0] - 0xAC2C0
                flag = flag_data[offset] & ary[1]
                try: 
                    mapexcept = ary[2]
                except IndexError:
                    if (loc_id in ctx.server_locations) and flag:
                        locs_to_send.add(loc_id)
                else:
                    if mapid == mapexcept:
                        pass
                    else:
                        if (loc_id in ctx.server_locations) and flag:
                            locs_to_send.add(loc_id)
                
                    
            # Stage Flag Locations
            # Planet, Offset, Mask
            for loc_id, ary in LEVEL_FLAG_MAP.items():
                offset = (0xAC2FC + ary[1]) - 0xAC2C0
                flag = flag_data[offset] & ary[2]
                
                if (loc_id in ctx.server_locations) and (cur_stage == ary[0]) and flag:
                    locs_to_send.add(loc_id)
            
            # Pommy Evolution Locations
            if pommy_check:
                loc_id = 0x1C3050 + (pommy_check-1)
                if (loc_id not in ctx.checked_locations) and (loc_id in ctx.server_locations):
                    locs_to_send.add(loc_id)
                outbound_writes.append((0xABD64, bytearray([0x00]), "RDRAM"))

            # Remote Bomb Locations
            if powerup_check:
                #match powerup_check:
                if powerup_check & 0x1:
                    if mapid in KICK_MAP:
                        loc_id = KICK_MAP[mapid]
                        locs_to_send.add(loc_id)
                if powerup_check & 0x2:
                    if mapid in GLOVE_MAP:
                        loc_id = GLOVE_MAP[mapid]
                        locs_to_send.add(loc_id)
                if powerup_check & 0x4:
                    if mapid in REMOTE_MAP:
                        loc_id = REMOTE_MAP[mapid]
                        locs_to_send.add(loc_id)
                outbound_writes.append((0xAD740, bytearray([0x00]), "RDRAM"))

            # Shop Locations
            if inshop == 0x800B57C0:
                for loc_id, ary in SHOP_MAP.items():
                    offset = ary[0] - 0xAC2C0
                    mask = ary[1]
                    flag = flag_data[offset] & mask
                    if flag and (loc_id not in ctx.checked_locations) and (loc_id in ctx.server_locations):
                        locs_to_send.add(loc_id)

            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send
                if locs_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])


            # Handle items
            planets = [0x1C30010]
            hp_bits = 0
            hp_shift = 0
            bomblvl = 0
            firelvl = 1
            speedlvl = 2
            #genes = 0x0000
            elemental_stone = 0
            warkeys = 0
            warshipmask = 0
            warshipmaskary = [0x20, 0x40, 0x10]
            genes = []
            stage_item_have = []
            
            for item in range(len(ctx.items_received)):
                raw_item = ctx.items_received[item].item
                # Pommy Genes
                if raw_item >= 0x1C30020 and  raw_item < 0x1C30030:
                    #shift = raw_item & 0xF
                    #mask = 1 < shift
                    #genes = genes | mask
                    genes.append(raw_item)
                # Stage Items
                elif raw_item >= 0x1C30018 and  raw_item < 0x1C30020:
                    stage_item_have.append(raw_item)
                else:
                    match raw_item:
                        case 0x1C30011: # Aquanet
                            planets.append(raw_item)
                        case 0x1C30012: # Horizon
                            planets.append(raw_item)
                        case 0x1C30013: # Starlight
                            planets.append(raw_item)
                        case 0x1C30014: # Neverland
                            planets.append(raw_item)
                        case 0x1C30015: # Epikyur
                            planets.append(raw_item)
                        case 0x1C30016: # Thantos
                            planets.append(raw_item)
                        case 0x1C30017: # Noah
                            planets.append(raw_item)
                        case 0x1C30000: # Fire Stone
                            elemental_stone = elemental_stone | 0x01
                        case 0x1C30001: # Ice Stone
                            elemental_stone = elemental_stone | 0x02
                        case 0x1C30002: # Wind Stone
                            elemental_stone = elemental_stone | 0x04
                        case 0x1C30003: # Earth Stone
                            elemental_stone = elemental_stone | 0x10
                        case 0x1C30004: # Electric
                            elemental_stone = elemental_stone | 0x08
                        case 0x1C30005: # Dark
                            elemental_stone = elemental_stone | 0x40
                        case 0x1C30006: # Light
                            elemental_stone = elemental_stone | 0x20
                        case 0x1C3000A: # Gaurdian Glove
                            armor = armor | 0x04
                        case 0x1C3000B: # Gaurdian Boots
                            armor = armor | 0x08
                        case 0x1C3000C: # Gaurdian Helmet
                            # Prevent a crash
                            if mapid in [0x861,0x8AB,0x8B4, 0x8AA]:
                                armor = armor & 0xFE
                            else:
                                armor = armor | 0x01
                        case 0x1C3000D: # Gaurdian Armor
                            armor = armor | 0x02
                        case 0x1C30007: #Bombup
                            bomblvl += 1
                            if bomblvl > 3:
                                bomblvl = 3
                        case 0x1C30008: #Bombup
                            firelvl += 1
                            if firelvl > 3:
                                firelvl = 3
                        case 0x1C30009: # HealthUp
                            hp_shift += 1
                            hp_bits = hp_bits | (1 << hp_shift)
                            #health_max += 1
                            #hpshift = (health_max -4)
                            #hp_bits = hp_bits | (1 << hpshift)
                        case 0x1C3000E: # Skates
                            speedlvl += 1
                            if speedlvl > 2:
                                speedlvl = 2
                        case 0x1C30050: # Warship keys
                            warkeys += 1
                            if warkeys > 3:
                                warkeys = 3
                            warshipmask = warshipmask | warshipmaskary[(warkeys-1)]


                    
            if self.noah_access == 0:
                generator_clears = 0
                for x in range(7):
                    mask = 1 << x
                    flag = stage_clear & mask
                    if flag:
                        generator_clears +=1
                if (generator_clears >= self.planet_required) and 0x1C30017 not in planets:
                    planets.append(0x1C30017)
            elif self.noah_access == 1:
                if warkeys == 3:
                    planets.append(0x1C30017)

            # Handle Planet Select
            if instage[2] == 0x4F:
                outbound_writes.append((0xABCC0, bytearray([0x60,0x00,0x50,0x28]), "RDRAM"))
            if instage[2] == 0x4F and (planet_sel_check[0x3] == 0x01 and planet_sel_check[0x7] == 0xFF
                                        and planet_sel_check[0xB] == 0x01 and planet_sel_check[0xF] == 0x02):
                outbound_writes.append((0x255028, get_planet_selection(planets), "RDRAM"))
                planethighlights = highlight_planets(planets,stage_clear,boss_clear,stage_selection[3])
                for offset, color in planethighlights.items():
                    outbound_writes.append((offset, color.to_bytes(4, 'big'), "RDRAM"))
                outbound_writes.append((0xB5827,bytearray([0x01]), "RDRAM")) # always display Epikyur
                outbound_writes.append((0xB587F,bytearray([0x01]), "RDRAM")) # always display Thantos

            clear_fp = full_power & 0xBF # Mask 0x40
            if self.firedown == True:
                firelvl = 0
            maxbombtype = [
                bomblvl + 1,    # 0 Fire
                bomblvl,        # 1 Ice
                bomblvl,        # 2 Wind
                1,              # 3 Earth
                bomblvl + 1,    # 4 Lightning
                1,              # 5 Light
                1               # 6 Dark
            ]
            if bombtype < 7:
                maxbombs = maxbombtype[bombtype]
            else:
                maxbombs = 1
            if maxbombs <= 0:
                maxbombs = 1
            outbound_writes.append((0xAC2E8, bytearray([clear_fp]), "RDRAM"))
            outbound_writes.append((0xAC307, bytearray([elemental_stone]), "RDRAM"))
            outbound_writes.append((0xAC2DD, bytearray([armor]), "RDRAM"))

            outbound_writes.append((0xAD733, bytearray([firelvl]), "RDRAM"))
            outbound_writes.append((0xAD737, bytearray([bomblvl]), "RDRAM"))
            outbound_writes.append((0xAD75B, bytearray([maxbombs]), "RDRAM"))
            outbound_writes.append((0xAD73F, bytearray([speedlvl]), "RDRAM"))
            #outbound_writes.append((0xAD763, bytearray([health_max]), "RDRAM"))
            outbound_writes.append((0xAC2DB, bytearray([hp_bits]), "RDRAM"))
            # Place Warship keys
            
            #health_max = hp_shift + 5
            # Handle Temp items
            if len(ctx.items_received) > recv_index:
                raw_item = ctx.items_received[recv_index].item
                updated_game_state = game_status
                #if raw_item >= 0x1C30000 and raw_item < 0x1C30030:
                    #recv_action = 0x33
                match raw_item:
                    case 0x1C30030: # money
                        cash = int.from_bytes(money, byteorder='big', signed = True) + 200
                        outbound_writes.append((0xABD50, cash.to_bytes(4, "big") , "RDRAM"))
                    case 0x1C30031: # Heart
                        health_out = health_cur + 1
                        if health_out > health_max:
                            health_out = health_max
                        outbound_writes.append((0xAD75F, bytearray([health_out]), "RDRAM"))
                    case 0x1C30032: # Gold Heart
                        outbound_writes.append((0xAD75F, bytearray([health_max]), "RDRAM"))
                
                    case 0x1C30040: # Stun Trap
                        recv_action = 0x2B
                    case 0x1C30041: # Panic Bomb Trap
                        recv_action = 0x46
                    case 0x1C30042: # Fire Trap
                        outbound_writes.append((0xB8B17, bytearray([0x06]), "RDRAM"))
                        outbound_writes.append((0xB8B12, bytearray([0x04]), "RDRAM"))
                        outbound_writes.append((0xB887A, bytearray([0x01]), "RDRAM"))
                    case 0x1C30043: # Reverse Trap
                        outbound_writes.append((0xB8B17, bytearray([0x04]), "RDRAM"))
                        outbound_writes.append((0xB8B12, bytearray([0x04]), "RDRAM"))
                        outbound_writes.append((0xB887A, bytearray([0x01]), "RDRAM"))
                    case 0x1C30044: # Ejection trap
                        updated_game_state = updated_game_state | 0x00000200
                        outbound_writes.append((0xABD40, updated_game_state.to_bytes(4, byteorder='big'), "RDRAM"))
                if recv_action:
                        outbound_writes.append((0xB8887, bytearray([0x02]), "RDRAM"))
                        outbound_writes.append((0xB888F, bytearray([recv_action]), "RDRAM"))
                        recv_action = 0
                outbound_writes.append((RECV_INDEX, (recv_index +1).to_bytes(1, "big") , "RDRAM"))

            # Handle Stage Item writes
            #stage_item_have
            #eventbytes
            #mapid
            flagbytes = eventbytes
            for item_id, ary in STAGE_ITEMS.items():
                if cur_stage == ary[0]:
                    val = int.from_bytes(flagbytes, byteorder='big', signed= False)
                    placeMapID = ary[3]
                    getMapIDs = ary[4]
                    rawmask = ary[2]
                    flags = val 

                    if item_id in stage_item_have:
                        if mapid == placeMapID:
                            mask = ary[1]
                            flags = val | mask
                        elif mapid not in getMapIDs:
                            mask = 0xFFFFFFFF - rawmask
                            flags = val & mask
                    else:
                        if mapid == placeMapID:
                            mask = 0xFFFFFFFF - rawmask
                            flags = val & mask
                        #elif mapid not in getMapIDs:
                        #    mask = 0xFFFFFFFF - rawmask
                        #    flags = val & mask
                    flagbytes = flags.to_bytes(4,byteorder='big')
                #outbound_writes.append((0xAC2FF, bytearray([(flag_data[0x3F] | warshipmask)]), "RDRAM"))
            if cur_stage == 7:
                val = int.from_bytes(flagbytes, byteorder='big', signed= False)
                flags = val | warshipmask
                flagbytes = flags.to_bytes(4,byteorder='big')
            outbound_writes.append((0xAC2FC, flagbytes, "RDRAM"))
                    
            # Door crap
            # if instage[2] == 0x4F:
            #    if mapid not in self.door_list:
            #        self.door_list[mapid] = ram_data[(8+cur_stage)][3]
            #    else:
            #        oldval = self.door_list[mapid]
            #        newval = ram_data[(8+cur_stage)][3]
            #        self.door_list[mapid] = min(oldval,newval)
            #        if pad_read[1] & 0x20 and self.door_list[mapid] == 0: # L Hold
            #            outbound_writes((DOOR_OFFSETS[cur_stage]+3), 0x00, "RDRAM")

            # Handle Pommy Command
            if self.pommy_command:
                target_evo = self.pommy_command
                evo_item = 0x1C30020 + (target_evo -1)
                if target_evo < 0x11 and target_evo > -1:
                    #evo_val = target_evo + 1
                    #mask = 1 < target_evo
                    if evo_item in genes:
                        outbound_writes.append((0xABD60, bytearray([target_evo]), "RDRAM"))
                    else:
                        logger.warning(f"Pommy does not have this gene")
                else:
                    outbound_writes.append((0xABD60, bytearray([0x00]), "RDRAM"))
                self.pommy_command = None

            # Handle Firepower Reduction
            if self.fire_command:
                if self.fire_command == 1:
                    self.firedown = not self.firedown
                elif self.fire_command == 2:
                    self.firedown = True
                elif self.fire_command == 3:
                    self.firedown = False
                self.fire_command = False



            # Handle Game Completion
            if not ctx.finished_game:
                game_cleared = False
                match self.game_goal:
                    case 0: # Final Boss
                        if (flag_data[0x1F] & 0x80):
                            game_cleared = True
                        elif (flag_data[0x1E] & 0x80) and self.noah_boss == 1:
                            game_cleared = True
                    case 1: # Generators
                        stage_clears = flag_data[0x1F] & 0x7F
                        clear_array = []
                        for x in range(6):
                            clearflag = 1 << x
                            if stage_clears & clearflag:
                                clear_array.append(clearflag)
                        if len(clear_array) >= self.planet_required:
                            game_cleared = True
                    case 2: # Stone Hunt
                        if elemental_stone == 0x7F:
                            game_cleared = True
                if game_cleared:
                    await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

                #logger.warning(f"{str(int.from_bytes(ram_data[0x10][0:4], byteorder='big', signed = False))}")
                if self.music_rando and (int.from_bytes(ram_data[0x10][0x10:0x14], byteorder='big', signed = False) == 0x017CFFFF ):
                    music_table1, music_table2 = randomize_multi_table(ram_data[0x10],0x10,ram_data[0x11],0x8,INVALID_SONGS)
                    outbound_writes.append((0x160664, music_table1, "RDRAM"))
                    outbound_writes.append((0x160404, music_table2, "RDRAM"))
                    #await bizhawk.write(ctx.bizhawk_ctx, [(0x160664, music_table1 , "RDRAM"),(0x160404, music_table2 , "RDRAM")])
                
                #logger.warning(f"{str(int.from_bytes(ram_data[0x12][0:4], byteorder='big', signed = False))}")
                if self.efx_rando and (int.from_bytes(ram_data[0x12][0:4], byteorder='big', signed = False) == 0x8005D730):
                    outbound_writes.append((0x927D0, ramdomize_table_with_exclude(ram_data[0x12],4,INVALID_EFX), "RDRAM"))
                if self.sfx_rando and sfx_check == 0x8000FF51:
                    raw_sfx_table = await bizhawk.read(ctx.bizhawk_ctx,[(0x182724, 0x20B8, "RDRAM"),])
                    outbound_writes.append((0x182724, ramdomize_table_with_exclude(raw_sfx_table[0],8,[0x374,0x375]), "RDRAM"))


                

            await bizhawk.write(ctx.bizhawk_ctx, outbound_writes)
            

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

def cmd_pommy(self, evo: str = ""):
    # Thanks to Pokemon Red/Blue apworld
    """Swap to specified Pommy Evolution provided you have recieved the proper gene
    example: /pommy dragon"""
    valid_evos = [
        "knuckle",  # 0
        "animal",   # 1
        "hammer",   # 2
        "claw",     # 3
        "penguin",  # 4
        "beast",    # 5
        "mage",     # 6
        "knight",   # 7
        "devil",    # 8
        "cat",      # 9
        "bird",     # A
        "chicken",  # B
        "dragon",   # C
        "dinosaur", # D
        "pixie",    # E
        "shadow",   # F
        "base",     # 10
    ]
    if self.ctx.game != "Bomberman The Second Attack":
        logger.warning(f"This command can only be used while playing Bomberman The Second Attack")
        return
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.warning(f"Must be connected to server and in game.")
        return
    elif not evo:
        logger.warning(f"Please enter a valid Pommy evolution")
        return
    elif evo.lower() not in valid_evos:
        logger.warning(f"Please enter a valid Pommy evolution")
        return
    elif evo.lower() in valid_evos:
        self.ctx.client_handler.pommy_command = valid_evos.index(evo.lower())+1
    else:
        logger.warning(f"Invalid Pommy command {evo}")
        return
    
def cmd_fire(self, sub: str = ""):
    """Allows you to reduce your firepower back down to 0, useful for building ice bridges.
    'down' to reduce, 'up' to return it back to normal or simpley /fire to toggle"""
    if self.ctx.game != "Bomberman The Second Attack":
        logger.warning(f"This command can only be used while playing Bomberman The Second Attack")
        return
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.warning(f"Must be connected to server and in game.")
        return
    elif not sub:
        self.ctx.client_handler.fire_command = 1
        logger.warning(f"Toggling Firepower")
    elif sub == "down" or sub == "Down" :
        self.ctx.client_handler.fire_command = 2
        logger.warning(f"Reducing Firepower")
    elif sub == "up" or sub == "Up":
        self.ctx.client_handler.fire_command = 3
        logger.warning(f"Incrasing Firepower")
    else:
        self.ctx.client_handler.fire_command = 1
        logger.warning(f"Toggling Firepower")