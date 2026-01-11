import logging
import asyncio
from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient
from .locations import loc_id_start, location_data
from .items import item_table, arch_item_offset
from .rom import crystal_ram_data, magic_ram_data, ability_ram_data, item_ram_data, \
    key_item_ram_data, gil_ram_data, full_flag_dict
from typing import Dict

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

FFVCD_ROMNAME_START = 0x00FFC0
FFVCD_ROMHASH_START = 0x7FC0
ROMNAME_SIZE = 0x15
ROMHASH_SIZE = 0x15


FFVCD_EVENT_FLAG_ADDR = WRAM_START + 0x000A14
FFVCD_EVENT_FLAG_BRBLADE_CHKN_ADDR = WRAM_START + 0x001443
FFVCD_CHESTS_ADDR = WRAM_START + 0x0009D4
FFVCD_IN_MENU_FLAG_ADDR = WRAM_START + 0x00014B
FFVCD_IN_MENU_FLAG2_ADDR = WRAM_START + 0x00020D
FFVCD_IN_MENU_FLAG3_ADDR = WRAM_START + 0x000B45 # this is tied to screen visibility fade in/out
FFVCD_IN_BATTLE_FLAG_ADDR = WRAM_START + 0x00014D
FFVCD_PIANO_ADDRESS = 0xA45 #piano flags
FFVCD_CURRENT_WORLD = 0xA2D #offset from RAM start that stores current world
        
FFVCD_LOADED_GAME_FLAG = WRAM_START + 0x30
FFVCD_LOADED_GAME_FLAG2 = WRAM_START + 0x6F

FFVCD_LOAD_CHECK = WRAM_START + 0x000AC3

FFVCD_RECV_PROGRESS_ADDR = WRAM_START + 0x9F4
FFVCD_FILE_NAME_ADDR = WRAM_START + 0x5D9

FFVCD_GOAL_SETTINGS = 0x3FFFFF

tracker_event_locations = ["ExDeath","ExDeath World 2","Piano (Tule)","Piano (Carwen)","Piano (Karnak)",
                           "Piano (Jacole)","Piano (Crescent)","Piano (Mua)","Piano (Rugor)","Piano (Mirage)"]
piano_addresses = [0xC0FFF6,0xC0FFF7,0xC0FFF8,0xC0FFF9,0xC0FFFA,0xC0FFFB,0xC0FFFC,0xC0FFFD]
world_flags = ["world 1", "world 2", "world 3"]

class FFVCDSNIClient(SNIClient):
    game = "Final Fantasy V Career Day"
    local_set_events: Dict[str, bool]
    local_set_events = {flag_name: False for flag_name in tracker_event_locations}
    world_byte = 0
    current_world: Dict[str, bool]
    current_world = {flag_name: False for flag_name in world_flags} 
    
    async def deathlink_kill_player(self, ctx):
        pass

    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        rom_name = await snes_read(ctx, FFVCD_ROMHASH_START, ROMHASH_SIZE)

        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:2] != b"K7":
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items
        ctx.rom = rom_name
        
        return True


    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        
        ##############
        # EVENTS
        ##############
        d1 = await snes_read(ctx, FFVCD_EVENT_FLAG_ADDR, 0x100)
        start = 0xA14 # 0xA14
        ram_dict = {} 
        for idx, i in enumerate(d1):
            ram_dict[start+idx] = i


        ##############
        # CHESTS
        ##############
        d3 = await snes_read(ctx, FFVCD_CHESTS_ADDR, 0x40)

        start = 0x9D4
        for idx, i in enumerate(d3):
            ram_dict[start+idx] = i
                

        goal_flags = await snes_read(ctx,FFVCD_GOAL_SETTINGS,0x1)
    
        

        ####################            
        # PLAYER STATE CHECKS TO ALLOW RECEIVING
        ####################
        in_menu_flag = await snes_read(ctx, FFVCD_IN_MENU_FLAG_ADDR, 0x1)
        in_menu_flag2 = await snes_read(ctx, FFVCD_IN_MENU_FLAG2_ADDR, 0x1)
        in_menu_flag3 = await snes_read(ctx, FFVCD_IN_MENU_FLAG3_ADDR, 0x1)
        if in_menu_flag is None:
            return
        elif in_menu_flag[0] == 0x00 or in_menu_flag2[0] != 0xF0 or in_menu_flag3[0] < 0xF0:
            return
        
        in_battle_flag = await snes_read(ctx, FFVCD_IN_BATTLE_FLAG_ADDR, 0x1)
        if in_battle_flag is None:
            return
        elif in_battle_flag[0] == 0x10:
            return


        loaded_game_flag2 = await snes_read(ctx, FFVCD_LOADED_GAME_FLAG, 0x1)
        loaded_game_flag3 = await snes_read(ctx, FFVCD_LOADED_GAME_FLAG2, 0x1)
        if loaded_game_flag2 is None:
            return
        elif loaded_game_flag2[0] != 0x00 or loaded_game_flag3[0] != 0x00:
            return
        
        load_game_check = await snes_read(ctx, FFVCD_LOAD_CHECK, 0x1)
        if not (load_game_check[0] & 0x80) == 0x80:
            return
        
        new_checks = []
        
        def check_status_bits(ram_byte, loc_bit, direction):
            if direction:
                ret = ram_byte & (1 << loc_bit) != 0
                return ret
            else:
                ret = ram_byte & (1 << loc_bit) == 0
                return ret

        for event_flag_addr, event_flag_data in full_flag_dict.items():
            try:
                ram_address = event_flag_data['ram_address']
                ram_byte = ram_dict[ram_address]
                loc_bit = event_flag_data['bit']
                direction = event_flag_data['direction']
                loc_id = event_flag_addr + loc_id_start
                
                # exdeath special handling for victory condition
                #now checks all victory conditions
                if event_flag_addr == 0xC0FFFF:
                    status1 = check_status_bits(ram_byte, 0, direction)
                    status2 = check_status_bits(ram_byte, 1, direction)
                    status3 = check_status_bits(ram_byte, 2, direction)
                    if status1 and status2 and status3:
                        status = True
                        # Handle Victory
                        if not ctx.finished_game:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                    else:
                        status = False
                elif event_flag_addr in piano_addresses and check_status_bits(goal_flags[0],1,1): #is piano percent on
                    status = check_status_bits(ram_byte, loc_bit, direction)
                    if ram_dict[FFVCD_PIANO_ADDRESS] == 255 and not ctx.finished_game:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                # normal case
                else:
                    status = check_status_bits(ram_byte, loc_bit, direction)

                if loc_id not in ctx.locations_checked and status:
                    new_checks.append(loc_id)
                    
            
            except:
                import traceback
                print("Error checking full_flag_dict: %s" % traceback.print_exc())
        
        
        for new_check_id in new_checks:
            location = ctx.location_names.lookup_in_game(new_check_id)
            if location in tracker_event_locations:
                # Send tracker event flags
                if not self.local_set_events[location] and ctx.slot is not None:
                    snes_logger.info(f'New Event: {location}')
                    event_bitfield = 0
                    self.local_set_events[location] = True
                    for i, flag_name in enumerate(tracker_event_locations):
                        if self.local_set_events[flag_name]:
                            event_bitfield |= 1 << i
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"FFVCD_EVENTS_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "or", "value": event_bitfield}],
                    }])
            else:
                ctx.locations_checked.add(new_check_id)
                snes_logger.info(
                    f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        world_byte = ram_dict[FFVCD_CURRENT_WORLD]
        for i, k in enumerate(self.current_world.keys()):
            self.current_world[k] = bool(check_status_bits(world_byte,i,1))
            
        if world_byte != self.world_byte:
            world_bitfield = 0
            self.world_byte = world_byte
            for i, flag_name in enumerate(world_flags):
                if self.current_world[flag_name]:
                    world_bitfield |= 1 << i
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"FFVCD_WORLD_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": world_bitfield}],
            }])
            
            #for i, flag_name in enumerate(world_tracker):
             #           if self.local_set_events[flag_name]:
              #              event_bitfield |= 1 << i
            

        recv_count = await snes_read(ctx, FFVCD_RECV_PROGRESS_ADDR, 2)
        recv_index = recv_count[0] +recv_count[1] * 256

        if recv_index < len(ctx.items_received):
            try:
                item = ctx.items_received[recv_index]
                recv_index += 1
                logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                    color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                    color(ctx.player_names[item.player], 'yellow'),
                    ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
    
                recv_index_list = [recv_index % 256, recv_index // 256]            
                snes_buffered_write(ctx, FFVCD_RECV_PROGRESS_ADDR, bytes(recv_index_list))            
                arch_item_id = item.item - arch_item_offset
    
                ####################            
                # RECEIVE CRYSTALS
                ####################
                
                if arch_item_id in crystal_ram_data.keys():
                    crystal_data = crystal_ram_data[arch_item_id]
                    crystal_data_bit, crystal_data_ram_addr = crystal_data
                    
                    current_byte = await snes_read(ctx, WRAM_START + crystal_data_ram_addr, 0x01)
                    new_byte = min(current_byte[0] | (1 << crystal_data_bit), 255)
                    snes_buffered_write(ctx, WRAM_START + crystal_data_ram_addr, bytes([new_byte]))
                        
                ####################            
                # RECEIVE MAGIC
                ####################
                
                if arch_item_id in magic_ram_data.keys():
                    magic_data = magic_ram_data[arch_item_id]
                    magic_data_bit, magic_data_ram_addr = magic_data
                    
                    current_byte = await snes_read(ctx, WRAM_START + magic_data_ram_addr, 0x01)
                    new_byte = min(current_byte[0] | (1 << magic_data_bit), 255)
                    snes_buffered_write(ctx, WRAM_START + magic_data_ram_addr, bytes([new_byte]))
                        
                ####################            
                # RECEIVE ABILITY
                ####################
                
                if arch_item_id in ability_ram_data.keys():
                    ability_data = ability_ram_data[arch_item_id]
                    ability_data_bit, ability_data_ram_addr = ability_data
                    
                    # character 1 
                    current_byte = await snes_read(ctx, WRAM_START + ability_data_ram_addr, 0x01)
                    new_byte = min(current_byte[0] | (1 << ability_data_bit), 255)
                    snes_buffered_write(ctx, WRAM_START + ability_data_ram_addr, bytes([new_byte]))
    
                    # character 2
                    current_byte = await snes_read(ctx, WRAM_START + ability_data_ram_addr + 0x14, 0x01)
                    new_byte = min(current_byte[0] | (1 << ability_data_bit), 255)
                    snes_buffered_write(ctx, WRAM_START + ability_data_ram_addr + 0x14, bytes([new_byte]))
    
                    # character 3
                    current_byte = await snes_read(ctx, WRAM_START + ability_data_ram_addr + 0x28, 0x01)
                    new_byte = min(current_byte[0] | (1 << ability_data_bit), 255)
                    snes_buffered_write(ctx, WRAM_START + ability_data_ram_addr + 0x28, bytes([new_byte]))
    
                    # character 4
                    current_byte = await snes_read(ctx, WRAM_START + ability_data_ram_addr + 0x3C, 0x01)
                    new_byte = min(current_byte[0] | (1 << ability_data_bit), 255)
                    snes_buffered_write(ctx, WRAM_START + ability_data_ram_addr + 0x3C, bytes([new_byte]))
                        
                ##############
                # RECEIVE ITEMS
                ##############
                
                
                if arch_item_id in item_ram_data.keys():
                    if ctx.slot == item.player:
                        pass
                        
                    else:
        
                        d4 = await snes_read(ctx, WRAM_START + 0x640, 0x100)
                
                        ram_current_item_map = {}
                        
                        for idx, i in enumerate(d4):
                            ram_current_item_map[idx] = hex(i).replace("0x","").upper()
                        
                        for k, v in ram_current_item_map.items():
                            if len(v) == 1:
                                ram_current_item_map[k] = "0%s" % v
                                
                        new_item_byte = item_ram_data[arch_item_id]
                        
                        match_idx = None
                        for k, v in ram_current_item_map.items():
                            if v == new_item_byte:
                                match_idx = k
                                break
                                
                        if match_idx:
                            # if a match was found, find its corresponding inventory count then add 1
                            item_count_in_inventory = await snes_read(ctx, WRAM_START + 0x740 + match_idx, 0x01)
                            item_count_in_inventory = min(item_count_in_inventory[0] + 1, 99)
                            snes_buffered_write(ctx, WRAM_START + 0x740 + match_idx, bytes([item_count_in_inventory]))
                        else:
                            # if a match was not found, find the first 00 slot in inventory ids, then assign it and give it 1 count
                            new_item_idx = None
                            for k, v in ram_current_item_map.items():
                                if v == '00':
                                    new_item_idx = k
                                    break
                            
                            if new_item_idx:
                                snes_buffered_write(ctx, WRAM_START + 0x640 + new_item_idx, bytes([new_item_byte]))
                                snes_buffered_write(ctx, WRAM_START + 0x740 + new_item_idx, bytes([1]))
                            else:
                                pass
    
                ##############
                # RECEIVE GIL
                ##############
                
                
                if arch_item_id in gil_ram_data.keys():
                    if ctx.slot == item.player:
                        pass
                    else:
                            
    
                        current_bytes = await snes_read(ctx, WRAM_START + 0x947, 0x03)
                        b1, b2, b3 = current_bytes[0], current_bytes[1], current_bytes[2]
                        current_gil = (b3 * 65536) + (b2 * 256) + b1
                        current_gil += gil_ram_data[arch_item_id]
                        
                        current_gil = min(current_gil, 0xFFFFFF)
                        
                        b1 = current_gil // 65536
                        b2 = (current_gil % 65536) // 256
                        b3 = (current_gil % 65536) % 256
                        
                        
                        snes_buffered_write(ctx, WRAM_START + 0x947, bytes([b3]))
                        snes_buffered_write(ctx, WRAM_START + 0x948, bytes([b2]))
                        snes_buffered_write(ctx, WRAM_START + 0x949, bytes([b1]))
                        
    
                    
                    
                    
                    
                    
                        
                ####################            
                # RECEIVE KEY ITEMS
                ####################
                
                if arch_item_id in key_item_ram_data.keys():
                    key_item_data_entries = key_item_ram_data[arch_item_id]
                    
                    # 1005/1006 are special cases for vehicles (hiryuu / submarine)
                    # first check all other cases
                    if arch_item_id != 1005 and arch_item_id != 1006:    
                        for key_item_data_entry in key_item_data_entries:
                            
                            key_item_bit, key_item_addr_offset, key_item_direction = key_item_data_entry
    
                            current_byte = await snes_read(ctx, WRAM_START + 0xA00 + key_item_addr_offset, 0x01)
                            if key_item_direction:
                                new_byte = min(current_byte[0] | (1 << key_item_bit), 255)
                            elif not key_item_direction:
                                new_byte = current_byte[0] & ~(1 << key_item_bit)                            
                            else:
                                break
                                
                            snes_buffered_write(ctx, WRAM_START + 0xA00 + key_item_addr_offset, bytes([new_byte]))
                            
                            # this needs to be called here because some addresses have multiple bits affected
                            await snes_flush_writes(ctx)
                    # handle hiryuu / submarine
                    
                    elif arch_item_id == 1005 or arch_item_id == 1006:   
                        # first handle key item for menu text
                        key_item_bit, key_item_addr_offset, key_item_direction = key_item_data_entries[0]
                        current_byte = await snes_read(ctx, WRAM_START + 0xA00 + key_item_addr_offset, 0x01)
                        new_byte = min(current_byte[0] | (1 << key_item_bit), 255)
                        snes_buffered_write(ctx, WRAM_START + 0xA00 + key_item_addr_offset, bytes([new_byte]))
                        
                        # then handle coords writing
                        for key_item_data_entry in key_item_data_entries[1:]:
                            key_item_byte, key_item_addr_offset, key_item_direction = key_item_data_entry
                            snes_buffered_write(ctx, WRAM_START + 0xA00 + key_item_addr_offset, bytes([key_item_byte]))


                await snes_flush_writes(ctx)
            except Exception as e:
                print("\n\n\n%s\n\n\n"%e)
                    
        return 
    

# hex_map = {"01" : 0,
#            "02" : 1,
#            "04" : 2,
#            "08" : 3,
#            "10" : 4,
#            "20" : 5,
#            "40" : 6,
#            "80" : 7}

                
        
                