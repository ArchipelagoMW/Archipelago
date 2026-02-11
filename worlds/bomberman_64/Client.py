
from typing import TYPE_CHECKING, Set, Optional, Dict, Any
import logging
from NetUtils import ClientStatus

from base64 import b64encode
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

import time
import random

logger = logging.getLogger("Client")

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


RECV_IDX = 0x8EFC8

ITEM_INDEX = {
    0x1CAEE0F:  0x01, # Bombup
    0x1CAEE13:  0x02, # Fireup
    0x1CAEE09:  0x03, # Bomb Kick
    0x1CAEE0A:  0x04, # Power Glove
    0x1CAEE0B:  0x05, # Remote Bombs
    0x1CAEE0C:  0x06, # Power Bombs
    0x1CAEE07:  0x07, # Heart
    0x1CAEE0D:  0x08, # Gold Card
    0x1CAEE08:  0x09, # Kill Recution
    0x1CAEE10:  0x0A, # Gems
    0x1CAEE11:  0x0B, # Extra Life
    0x1CAEE06:  0x0C, # Boss Medal
    0x1CAEE12:  0x0D, # Omnicube
    0x1CAEE01:  0x0E, # Green Key
    0x1CAEE02:  0x0F, # Blue Key
    0x1CAEE03:  0x10, # Red Key
    0x1CAEE04:  0x11, # White Key
    0x1CAEE05:  0x12, # Black Key
    0x1CAEE0E:  0x13, # Rainbow Key
    0x1CAEE18:  0x14, # Fast Virus
    0x1CAEE19:  0x15, # Sticky Virus
    0x1CAEE1A:  0x16, # Slow Virus
    0x1CAEE1B:  0x17, # Bombless Virus
    0x1CAEE1C:  0x18, # Restless Virus
    0x1CAEE1D:  0x19, # Death Virus
}

REMOTEPOWER_LOOKUP = {
    0x1C8E5901: [0x03], # Untouchable Treasure Power Bomb
    0x1C8E5902: [0x01], # Untouchable Treasure Remote Bomb
    0x1C8E5911: [0x08], # To Have or Have Not Power Bomb
    0x1C8E5912: [0x08], # To Have or Have Not Remote Bomb Tower
    0x1C8E5914: [0x06], # To Have or Have Not Remote Bomb Temple
    0x1C8E5916: [0x05], # To Have or Have Not Remote Bomb Entrance

    0x1C8E5921: [0x12], # Switches and Bridges Power Bomb
    0x1C8E5922: [0x11], # Switches and Bridges Remote Bomb
    0x1C8E5931: [0x15,0x14], # Pump It Up Power Bomb

    0x1C8E5941: [0x22], # Hot On The Trail Power Bomb
    0x1C8E5942: [0x21], # Hot On The Trail Remote Bomb
    0x1C8E5951: [0x2B], # On the Right Track Power Bomb
    0x1C8E5952: [0x28], # On the Right Track Remote Bomb Entrance
    0x1C8E5954: [0x2C], # On the Right Track Remote Bomb Exit

    0x1C8E5961: [0x33], # Blizzard Peaks Power Bomb
    0x1C8E5962: [0x31], # Blizzard Peaks Remote Bomb Avalance
    0x1C8E5964: [0x33], # Blizzard Peaks Remote Bomb Snowboard
    0x1C8E5972: [0x38], # Shiny Slippery Icy FlooTHe []r Remote Bomb

    0x1C8E5981: [0x45], # Go For Broke Power Bomb
    0x1C8E5982: [0x45], # Go For Broke Remote Bomb
    0x1C8E5991: [0x4B], # Trap Tower Power Bomb Platform
    0x1C8E5993: [0x46], # Trap Tower Power Bomb Entrance
    0x1C8E5992: [0x46], # Trap Tower Remote Bomb

    0x1C8E59A2: [0x51], # Beyond the Clouds Remote Bomb Side Room
    0x1C8E59A4: [0x50], # Beyond the Clouds Remote Bomb Main Room
    0x1C8E59B1: [0x53], # Doom Castle Power Bomb
    0x1C8E59B2: [0x53,0x54], # Doom Castle Remote Bomb

}

def ramdomize_table(tbl,entrysize):
    split_table = split_into_xbit_chunks(tbl,entrysize)
    random.shuffle(split_table)
    result = b''.join(split_table)
    return result

def ramdomize_music_table(tbl,entrysize):
    split_table = split_into_xbit_chunks(tbl,entrysize)
    valid_tracks = [
        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,
        0x0B,0x0C,0x0D,0x0E,0x0F,0x10,0x11,0x14,0x16,
        0x1B,0x1C,0x1D,0x1F,0x22,0x27,0x28,
    ]
    valid_jingles = [
        0x0A,0x12,0x13,0x15,0x18,0x1A,0x1E,
        0x20,0x21,0x23,0x26,0x2A,0x2D,
    ]
    temp_track = []
    temp_jingle = []
    for x in range(len(split_table)):
        if x in valid_tracks:
            temp_track.append(split_table[x])
        if x in valid_jingles:
            temp_jingle.append(split_table[x])

    random.shuffle(temp_track)
    random.shuffle(temp_jingle)

    for index in valid_tracks:
        split_table[index] = temp_track.pop(0)
    for index in valid_jingles:
        split_table[index] = temp_jingle.pop(0)
    result = b''.join(split_table)
    return result

def split_into_xbit_chunks(byte_array,size):
   #Splits a byte array into chunks of 32 bits (4 bytes).

    chunks = []
    for i in range(0, len(byte_array), size):
        chunk = byte_array[i:i + size]
        # If the last chunk is less than 4 bytes, pad it with zeros
        if len(chunk) < size:
            chunk += b'\x00' * (size - len(chunk)) 
        chunks.append(chunk)
    return chunks

class Bomb64Client(BizHawkClient):
    game = "Bomberman 64"
    system = "N64"
    patch_suffix = ".apbomb64"
    current_level_storage_key: str = ""
    #rom: typing.Optional[bytes] = None
    local_checked_locations: Set[int]
    rom_slot_name: Optional[str]

    death_link: bool = False
    sending_death_link: bool = True
    pending_death_link: bool = False

    needed_cards = 10
    gamegoal = 0
    hardmode = 0

    enemy_model = 0
    enemy_ai = 0
    music_rando = False
    sound_rando = False
    goal_clear = False

    model_suffle = {}

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.rom_slot_name = None
        self.power_command = True
        self.game_state = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        # Borrowed some authentication code from Kirby 64's apworld
        from CommonClient import logger
        rom_data = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
            (0x20, 0xC, "ROM"), # 0 Rom Name
            (0xDFFB0, 0x10,  "ROM"), # 1 Game Options
            (0xDFFE0, 0x32, "ROM"), # 2 Slot name
            (0xDFFC0, 0x20, "ROM"), # 3 Slot Data
            (0xC,0x4, "EEPROM"), # 4 Save File
            (0x1BAAE4, 0x178, "RDRAM"), # 5 Music Table
            (0x1C8C64, 0x1750, "RDRAM"), # 6 Sound Table
            ]
        )
        #game_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x1FFF200, 21, "ROM")]))[0])
        try:
            # Check ROM name/patch version
            #rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x20, 0xE, "ROM")]))[0]).decode("ascii")
            rom_name = rom_data[0].decode("ascii")
            if rom_name != "BOMBERMAN64U":
                return False  # Not a Bomberman 64 ROM
            try:# #
                #slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0xDFFC0, 32, "ROM")]))[0]
                slot_name_bytes = rom_data[2]
                self.rom_slot_name = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
            except UnicodeDecodeError:
                logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
                return False
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now
        
        
        self.needed_cards = rom_data[1][0]
        self.gamegoal = rom_data[1][1]
        deathlink = rom_data[1][2]
        self.hardmode = rom_data[1][3]
        self.enemy_model = rom_data[1][4]
        self.enemy_ai = rom_data[1][5]

        if deathlink:
            self.death_link = True
        
        # This is a Bomberman 64 ROM
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.command_processor.commands["power"] = cmd_power
        self.player_name = rom_data[2].decode("ascii")
        ctx.slot = chr(rom_data[3][7])
        #self.rom = game_name

        # Randomize Music
        if rom_data[1][6]:
            self.music_rando = True
            await bizhawk.write(ctx.bizhawk_ctx, [(0x1BAAE4, ramdomize_music_table(rom_data[5],8), "RDRAM")])
        if rom_data[1][7]:
            self.sound_rando = True
            await bizhawk.write(ctx.bizhawk_ctx, [(0x1C8C64, ramdomize_table(rom_data[6],8), "RDRAM")])

        ctx.want_slot_data = True

        # Write Save File
        if rom_data[4][3] == 0x00:
            if self.hardmode:
                await bizhawk.write(ctx.bizhawk_ctx, [(0xC, bytearray([0xFF,0x80,0x00,0x80]), "EEPROM")])
            else:   
                await bizhawk.write(ctx.bizhawk_ctx, [(0xC, bytearray([0x7F,0x00,0x00,0x80]), "EEPROM")])
                


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
        #self.cycle += 1
        if ctx.slot is None:
                await ctx.send_connect(name=ctx.auth)

        try:
            ram_data = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                (0x8E575, 0x10,  "RDRAM"), # 0 Gold Cards
                (0xAEE00, 0x20, "RDRAM"), # 1 Powerup states
                (0x8E5DF, 0x64, "RDRAM"), # 2 Stage Clears
                (0x44C9B, 0x01, "RDRAM"), # 3 Game start
                (RECV_IDX, 0x1, "RDRAM"), # 4 Recv Index
                (0x44560, 0x1, "RDRAM"), # 5 In stage check
                (0x2AC620, 0x10, "RDRAM"), # 6 Other Stats
                (0x8E568, 0x4, "RDRAM"), # 7 Game Start
                (0x8EF60, 0x60, "RDRAM"), # 8 PowerRemote Checks
                (0x8E570,0x6, "RDRAM"), # 9 Custom Balls
                (0x1BAAE4, 0x170, "RDRAM"), # A Music Table
                (0x1C8C6A, 0x1, "RDRAM"), # B Sound Check
                (0x2AC5D7,0x1, "RDRAM"), # C Current Map
                ]
            )
            
            gold_cards = ram_data[0]
            powerups = ram_data[1]
            health = ram_data[1][7]
            stage_clears = ram_data[2]
            game_start = ram_data[7]

            palace_state = gold_cards[0xF]

            recv_index = ram_data[4][0]
            instage = ram_data[5][0] # checks to see what routine is loaded to 0x44560
            lives = ram_data[6][7]
            gems = ram_data[6][0xF]
            customs = ram_data[9]
            powerup_checks = ram_data[8]
            outbound_writes = []
            mapid = ram_data[0xC]
            
            if list(game_start) != [0x80,0x08,0xD4,0x30]:
                return
            self.game_state = True
            # Deathlink
            invalid_death_instage = [0x8C, 0x24, 0x27, 0x46]
            if self.death_link:
                await ctx.update_death_link(self.death_link)
            if self.pending_death_link:
                
                # Set Health to 1 then run damage routine
                if instage not in invalid_death_instage:
                    outbound_writes.append((0xAEE07, bytearray([0x01]), "RDRAM"))
                # Tell game to take damage
                    outbound_writes.append((0x8ED50, bytearray([0x01]), "RDRAM"))
                #ctx.last_death_link = time.time()
                self.pending_death_link = False
                self.sending_death_link = True
                
            if "DeathLink" in ctx.tags  and ctx.last_death_link + 1 < time.time():
                if health == 0 and not self.sending_death_link and instage not in invalid_death_instage:
                    await self.send_deathlink(ctx)
                elif health != 0 or instage in invalid_death_instage:
                    self.sending_death_link = False


            # Check Locations
            locs_to_send = set()

             # Gold Cards
            offset = 0
            for val in gold_cards:
                for bit in range(8):
                    loc_id = 0x1C8E5750 + (offset *0x10) + bit
                    mask = 1 << bit
                    flag = val & mask
                    if flag and loc_id in ctx.server_locations:
                        locs_to_send.add(loc_id)
                offset += 1

             # Stage Clears
            for val in range(24):
                offset = 4 * val
                flag = stage_clears[offset] # &0x80
                loc_id = 0x1C8E5DF0 + (offset * 0x10)
                if flag and loc_id in ctx.server_locations:
                    locs_to_send.add(loc_id)

            # Power bombs and Remote Bombs
            for loc_id, maps in REMOTEPOWER_LOOKUP.items():
                for areaid in maps:
                    lowbyte = loc_id & 0xF
                    if lowbyte % 2 == 0:
                        mask = 2
                    else:
                        mask = 1
                    val = powerup_checks[areaid]
                    flag = val & mask
                    if flag and loc_id in ctx.server_locations:
                        locs_to_send.add(loc_id)

            
            # i = 0
            # for offset in range(0x00,len(powerup_checks), 0x08):
                # flag = powerup_checks[offset + 3]
                # base_loc= 0x1C8E5900 + (i * 0x10)
                # power = flag & 0x01
                # remote = flag & 0x02
                # if power and base_loc+power in ctx.server_locations:
                    # locs_to_send.add(base_loc+power)
                # if remote and base_loc+remote in ctx.server_locations:
                    # locs_to_send.add(base_loc+remote)
                # i += 1
            
                
            # Custom Ball Checks
            for offset in range(len(customs)):
                byte = customs[offset]
                base_loc = 0x1C8E5700 + (offset * 0x10)
                for bit in range(8):
                    mask = 1 << bit
                    flag = byte & mask
                    loc_id = base_loc + bit
                    if flag and loc_id in  ctx.server_locations:
                        locs_to_send.add(loc_id)

            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send
                if locs_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            bombups = 2
            fireups = 2
            bomb_state = 0
            gold_cards_ap = 0
            kill_requirement = 30
            glove_state = False
            kick_state = False
            powers_state = [0x00,0x00,0x00,0x00,  0x00,0x00,0x00,0x00]
            stage_keys = [0,0,0,0,0,0]
            medals = 0
            for item in range(len(ctx.items_received)):
                raw_item = ctx.items_received[item].item
                match raw_item:
                    case 0x1CAEE0F: #Bombup
                        bombups += 1
                    case 0x1CAEE13: # Fireup
                        fireups += 1
                    case 0x1CAEE0B: # Remote bombs
                        bomb_state = bomb_state | 0x2
                    case 0x1CAEE0C: # Power bombs
                        if self.power_command:
                            bomb_state = bomb_state | 0x1
                    case 0x1CAEE09: # Bomb Kick
                        kick_state = True
                        powers_state[6] = 0x01
                        powers_state[7] = 0x20
                    case 0x1CAEE0A: # Power Gloves
                        glove_state = True
                        powers_state[3] = 0xA0
                    case 0x1CAEE0D: # Gold Cards
                        gold_cards_ap += 1
                        if gold_cards_ap > self.needed_cards:
                            gold_cards_ap = self.needed_cards
                        if gold_cards_ap >= self.needed_cards >> 2:
                            palace_unlock = palace_state | 0x10
                            outbound_writes.append((0x8E584, palace_unlock.to_bytes(1, "big"), "RDRAM"))
                            outbound_writes.append((0x8E628, palace_unlock.to_bytes(1, "big"), "RDRAM"))
                        #if self.gamegoal == 1 and gold_cards >= self.needed_cards:
                           #self.goal_clear = True
                    case 0x1CAEE08: # Kill count reduction
                        kill_requirement -= 5
                        if kill_requirement < 5:
                            kill_requirement = 5
                    case 0x1CAEE06:
                        medals +=1
                    case 0x1CAEE01: # Green key
                        stage_keys[0] += 1
                    case 0x1CAEE02: # Blue key
                        stage_keys[1] += 1
                    case 0x1CAEE03: # Red key
                        stage_keys[2] += 1
                    case 0x1CAEE04: # White key
                        stage_keys[3] += 1
                    case 0x1CAEE05: # Black key
                        stage_keys[4] += 1
                    case 0x1CAEE0E: # Rainbow Key
                        stage_keys[5] += 1
            if stage_keys[4] > 0:
                stage_keys[4] -=1
                outbound_writes.append((0x8EFC3, bytearray([0x01]), "RDRAM"),)

            outbound_writes.append((0xAEE0F, bombups.to_bytes(1, "big"), "RDRAM"))
            outbound_writes.append((0xAEE13, fireups.to_bytes(1, "big"), "RDRAM"))
            outbound_writes.append((0xAEE0B, bomb_state.to_bytes(1, "big"), "RDRAM"),)
            outbound_writes.append((0xBD003, kill_requirement.to_bytes(1, "big"), "RDRAM"),)
            outbound_writes.append((0xBD007, gold_cards_ap.to_bytes(1, "big"), "RDRAM"),)
            if glove_state or kick_state:
                outbound_writes.append((0x2ADFF0, bytearray(powers_state), "RDRAM"),)
                
            
            # Handle stage keys
            #if stage_code == bytearray(STAGE_CODE):
            stage_bytes = [
                0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, # [0x00] Green Gardens
                0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, # [0x10] Blue Resort
                0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, # [0x20] Red Mountain
                0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, # [0x30] White Glacier
                0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, # [0x40] Black Fortress
                0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, # [0x50] Rainbow Palace
                ]
            for world in range(len(stage_keys)):
                for level in range(stage_keys[world]):
                    byte = (world * 0x10) + (level * 0x4)+ 3
                    stage_bytes[byte] = 0x01
            palace_increment = self.needed_cards >> 2
            if gold_cards_ap >= palace_increment * 2:
                stage_bytes[0x53]=0x01
            if gold_cards_ap >= palace_increment * 3:
                stage_bytes[0x57]=0x01
            if gold_cards_ap >= self.needed_cards:
                stage_bytes[0x4B]=0x01 # Open Altier
            else:
                stage_bytes[0x4B]=0x00
            outbound_writes.append((0x8EF00, bytearray(stage_bytes), "RDRAM"),) #0x8E700
            #if fort_code == bytearray(fort_updated):
            #    await bizhawk.write(
            #                ctx.bizhawk_ctx,[(0x8E743, gold_cards.to_bytes(1, "big"), "RDRAM")],)
            #self.cycle = 0

            if len(ctx.items_received) > recv_index:
                raw_item = ctx.items_received[recv_index].item
                match raw_item:
                    case 0x1CAEE07: # Heart
                        outbound_writes.append((0xAEE07,(0x02).to_bytes(1, "big"),"RDRAM"))
                    case 0x1CAEE11: # 1UP
                        outbound_writes.append((0x2AC627, (lives + 1).to_bytes(1, "big") , "RDRAM"))
                    case 0x1CAEE10: # Gems
                        if gems > 25:
                            gems = 29
                        outbound_writes.append((0x2AC62F, (gems + 5).to_bytes(1, "big") , "RDRAM"))
                    # Traps
                    case 0x1CAEE18: # Fast
                        outbound_writes.append((0xAEE5B, (0x11).to_bytes(1, "big") , "RDRAM"))
                        outbound_writes.append((0xAEE6A, (0x400).to_bytes(2, "big") , "RDRAM"))
                    case 0x1CAEE19: # Sticky
                        outbound_writes.append((0xAEE5B, (0x12).to_bytes(1, "big") , "RDRAM"))
                        outbound_writes.append((0xAEE6A, (0x400).to_bytes(2, "big") , "RDRAM"))
                    case 0x1CAEE1A: # Slow
                        outbound_writes.append((0xAEE5B, (0x14).to_bytes(1, "big") , "RDRAM"))
                        outbound_writes.append((0xAEE6A, (0x400).to_bytes(2, "big") , "RDRAM"))
                    case 0x1CAEE1B: # Bombless
                        outbound_writes.append((0xAEE5B, (0x18).to_bytes(1, "big") , "RDRAM"))
                        outbound_writes.append((0xAEE6A, (0x400).to_bytes(2, "big") , "RDRAM"))
                    case 0x1CAEE1C: # Restless
                        outbound_writes.append((0xAEE5B, (0x30).to_bytes(1, "big") , "RDRAM"))
                        outbound_writes.append((0xAEE6A, (0x400).to_bytes(2, "big") , "RDRAM"))
                    case 0x1CAEE1D: # Death
                        outbound_writes.append((0xAEE5B, (0x90).to_bytes(1, "big") , "RDRAM"))
                        outbound_writes.append((0xAEE6A, (0x400).to_bytes(2, "big") , "RDRAM"))
                
                outbound_writes.append((RECV_IDX, (recv_index +1).to_bytes(1, "big") , "RDRAM"))
                if raw_item in ITEM_INDEX:
                   outbound_writes.append((0xBD006, bytearray([ITEM_INDEX[raw_item]]), "RDRAM"))
            

            # Send mapid to tracker
            
            mapstr = f"{int.from_bytes(mapid, 'big')}"
            if not self.current_level_storage_key:
                self.current_level_storage_key = f"bomberman64_area_0_{ctx.slot}" # Needs team slot
                ctx.set_notify(self.current_level_storage_key)
            
            if ctx.stored_data.get(self.current_level_storage_key, "") != mapstr:
                await ctx.send_msgs([
                    {
                        "cmd": "Set",
                        "key": self.current_level_storage_key,
                        "default": "0_S",
                        "want_reply": False,
                        "operations": [
                            {"operation": "replace", "value": mapstr}
                        ]
                    }
                ])
          #  await ctx.send_msgs([{
          #          "cmd": "Set", "key": f"bomberman64_area_{ctx.team}_{ctx.slot}", "operations":
          #              [{"operation": "replace", "value": f"{mapid}"}],
          #      }])

                #self.goal_clear = True
            # Send Game Clear
            goalclear = False
            if not ctx.finished_game: 
                match self.gamegoal:
                    case 0: # Altier Goal
                        if stage_clears[0x4C]:
                            goalclear = True
                    case 1: # Gold Card Goal
                        if gold_cards_ap >= self.needed_cards:
                            goalclear = True
                    case 2: # Boss Medals
                        if medals >=4:
                            goalclear = True
                if goalclear:
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])

            if self.music_rando and ram_data[0xA][0x0F] == 0xD0:
                outbound_writes.append((0x1BAAE4, ramdomize_music_table(ram_data[0xA],8), "RDRAM"))
            
            if self.sound_rando and ram_data[0xB][0] == 0x3E:
                sound_table = await bizhawk.read(ctx.bizhawk_ctx,[(0x1C8C64, 0x1750, "RDRAM"),])
                outbound_writes.append((0x1C8C64, ramdomize_table(sound_table[0],8), "RDRAM"))

            await bizhawk.write(ctx.bizhawk_ctx, outbound_writes)
        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

def cmd_power(self, sub: str = ""):
    """Allows you to reduce your firepower back down to 0, useful for building ice bridges.
    'down' to reduce, 'up' to return it back to normal or simpley /fire to toggle"""
    if self.ctx.game != "Bomberman 64":
        logger.warning(f"This command can only be used while playing Bomberman 64")
        return
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.warning(f"Must be connected to server and in game.")
        return
    elif not sub:
        self.ctx.client_handler.power_command = not self.ctx.client_handler.power_command
        logger.warning(f"Toggling Power Bombs")
    elif sub == "on" or sub == "On" :
        self.ctx.client_handler.power_command = True
        logger.warning(f"Power Bombs On")
    elif sub == "off" or sub == "Off":
        self.ctx.client_handler.power_command = False
        logger.warning(f"Power Bombs Off")
    else:
        self.ctx.client_handler.power_command = 1
        logger.warning(f"Toggling Firepower")