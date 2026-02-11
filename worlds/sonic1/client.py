import logging

from NetUtils import ClientStatus, RawJSONtoTextParser
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import display_message, read, set_message_interval, write
from . import constants
from .sram import SegaSRAM

logger = logging.getLogger("Client")

MAGIC_BROKEN = 0x0
MAGIC_UNBROKEN = 0x1F
MAGIC_EMPTY_SEED = ' '*20

class S1Client(BizHawkClient):
    system = ("GEN",)
    patch_suffix = (".aps1",)
    game = "Sonic the Hedgehog 1"
    sram_abstraction: SegaSRAM

    async def validate_rom(self, ctx):
        # loaded_hash = await get_hash(ctx.bizhawk_ctx)
        print(ctx.rom_hash)
        if ctx.rom_hash in ["EE5D0A76A515111B589B2E523B3AC685C20E37AB", # AP-070
                            "A40C5AA20DB7F7B5C4FD25C0552E7EFA8B70A5E9"]: # AP-071 - compatible
            ctx.game = self.game
            ctx.items_handling = 0b111
            ctx.finished_game = False
            if "server_seed_name" not in ctx.__dict__:
                # Probably running on 0.5.1?
                ctx.server_seed_name = None
            if ctx.server_seed_name:
                ctx.remote_seed_name = f"{ctx.server_seed_name[-20:]:20}"
                if len(ctx.locations_checked) != 0:
                    # This is in the hopes of avoiding sending reused data
                    ctx.locations_checked.clear()
                    ctx.locations_scouted.clear()
                    ctx.stored_data_notification_keys.clear()
                    ctx.checked_locations.clear()
            else:
                ctx.remote_seed_name = MAGIC_EMPTY_SEED
            ctx.rom_seed_name = MAGIC_EMPTY_SEED
            await set_message_interval(ctx.bizhawk_ctx, 0)
            self.sram_abstraction = SegaSRAM(read, write)
            self.sram_abstraction.fields = constants.S1Layout
            # This will try to work out what byte order is in use.  Important because bizhawk has a byte swap issue
            await self.sram_abstraction.detect_type(ctx, magic=b'AS10')
            logger.info(f"Using sram type {self.sram_abstraction.ram_type}")
            self.sram_abstraction.extra_addresses.append((0x0F600, 1, "68K RAM")) # Game mode
            self.sram_abstraction.extra_addresses.append((0x0FE10, 7, "68K RAM")) # Zone and Act... v_lastspecial is 0xFE16
            ctx.curr_map = None
            ctx.my_stored_data = {}
            ctx.previous_deathlinks = set()
            ctx.complained_about_seed = ""
            ctx.messages = []
            return True
        return False

    def on_package(self, ctx, cmd, args):
        if cmd == 'RoomInfo':
            logger.debug(f"{args['seed_name']=} ?= {ctx.rom_seed_name=}")
            ctx.remote_seed_name = f"{args['seed_name'][-20:]:20}"
            if ctx.rom_seed_name != ctx.remote_seed_name:
                if ctx.rom_seed_name != MAGIC_EMPTY_SEED:
                  # CommonClient's on_package displays an error to the user in this case, but connection is not cancelled.
                  self.game_state = False
                  self.disconnect_pending = True
                if len(ctx.locations_checked) != 0:
                    # This is in the hopes of avoiding sending reused data
                    ctx.locations_checked.clear()
                    ctx.locations_scouted.clear()
                    ctx.stored_data_notification_keys.clear()
                    ctx.checked_locations.clear()
                ctx.my_stored_data = {}
        elif cmd == 'Bounced':
            #logger.info(f"{cmd=} -> {args=}")
            if "DeathLink" in args.get("tags",{}) and args["data"]["time"] not in ctx.previous_deathlinks:
                    ctx.previous_deathlinks.add(args["data"]["time"])
                    ctx.my_stored_data[f"{ctx.slot}_{ctx.team}_sonic1_deathl_in"] += 1
        elif cmd == 'Connected':
            ctx.my_stored_data = {}
        elif cmd == "Retrieved":
            #logger.info(f"{cmd=} -> {args=}")
            for (k,v) in args["keys"].items():
              ctx.my_stored_data[k] = v if v else 0
        elif cmd == "PrintJSON":
            ctx.messages.append(RawJSONtoTextParser(ctx)(args["data"]))
            #logger.info(f"{cmd=} -> {args=}... {s=}")
        super().on_package(ctx, cmd, args)

    async def game_watcher(self, ctx):
        assert isinstance(self.sram_abstraction, SegaSRAM)
        assert isinstance(self.sram_abstraction.fields, constants.S1Layout)
        if self.sram_abstraction.ram_type == -1: # Detection failure!
            # This will try to work out what byte order is in use.  Important because bizhawk has a byte swap issue
            await self.sram_abstraction.detect_type(ctx, magic=b'AS10')
            logger.info(f"Using sram type {self.sram_abstraction.ram_type}")
        if self.sram_abstraction.ram_type == -1: # Double Detection failure!
            return
        await self.sram_abstraction.read_bytes(ctx)
        if self.sram_abstraction.fields.SR_Head != b'AS10' or b'\xff' in self.sram_abstraction.fields.SR_Seed:
            return # This means we're not initialised
        seed_name = str(self.sram_abstraction.fields.SR_Seed,'ascii')
        # We're only caring about the seed in the start.
        ctx.rom_seed_name = seed_name
        slot_id = self.sram_abstraction.fields.SR_Slot
        ctx.rom_slot = slot_id

        if (not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed
             or ctx.remote_seed_name == MAGIC_EMPTY_SEED
             or getattr(ctx,"slot_data",None) is None):
            return
        
        if ctx.messages:
            s = ctx.messages.pop(0)
            await display_message(ctx.bizhawk_ctx, s)

        map_code = ctx.curr_map
        if self.sram_abstraction.extra_data[0] == b"\x0C": # Level mode
            # This fixes the oddity of the game switching to GHZ1 for special stage conclusion:
            if ctx.curr_map not in range(19,25):
                map_code = constants.level_bytes.get(self.sram_abstraction.extra_data[1][:2],0)
            else:
                map_code = ctx.curr_map
        elif self.sram_abstraction.extra_data[0] == b"\x10": # Special zone
            map_code = int(self.sram_abstraction.extra_data[1][6])+19
        elif self.sram_abstraction.extra_data[0] == b"\x04": # Title
            # Really we should only go back to the menu when we go back to the menu.  So, look for Title game mode.
            map_code = 0
        
        if ctx.curr_map != map_code:
            ctx.curr_map = map_code
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"{ctx.slot}_{ctx.team}_sonic1_area",
                "default": 0,
                "want_reply": True,
                "operations": [{
                    "operation": "replace",
                    "value": map_code,
                }],
            }])

        cleanslate = False
        missing = []
        for key in ["invinc_out", "shield_out", "speeds_out", "deathl_in", "deathl_out", "deaths", "bosses"]:
          key = f"{ctx.slot}_{ctx.team}_sonic1_{key}"
          if key not in ctx.my_stored_data:
            ctx.my_stored_data[key] = -1
            missing.append(key)
          elif ctx.my_stored_data[key] == -1:
              return
        if len(missing):
          await ctx.send_msgs([{"cmd": "Get", "keys": missing}, {"cmd": "SetNotify", "keys": missing}])
          await ctx.update_death_link(ctx.slot_data.get("recv_death", False))
          return

        if self.sram_abstraction.fields.SR_Head == b'AS10':
            # So, this should be valid save data...
            if seed_name == MAGIC_EMPTY_SEED:
                # Only, there's a blank save, so we should write the full save.
                output = [b'AS10']
                #logger.info(f"{ctx.locations_checked=} {ctx.checked_locations=}")
                output += bytes([MAGIC_BROKEN if constants.id_base+i in ctx.checked_locations else MAGIC_UNBROKEN 
                                 for i in range(1,len(constants.monitor_by_id)+1)])
                output.extend([0x0,0x0,0x0, # SR_Specials, SR_Emeralds, SR_Bosses
                               0x0,0x0,0x0, # SR_BuffGoals, SR_BuffDisR, SR_RingsFound
                               0x0,0x0,     # SR_LevelGate, SR_SSGate
                               0x0,0x0, 0x0,0x0, 0x0,0x0, 0x0,0x0, # (Invinc|Shield|SpeedS|DeathL)(in|out)
                               0x0]) # SR_Deaths
                output.append(ctx.remote_seed_name.encode())
                output.append(ctx.slot)
                await self.sram_abstraction.full_write(ctx, output)
                await self.sram_abstraction.read_bytes(ctx)
                seed_name = ctx.remote_seed_name
                ctx.rom_seed_name = seed_name
                slot_id = ctx.rom_slot = ctx.slot
                cleanslate = True

                '''
                move.w #0,(a0)+ ; Special zone bitfield
                move.w #0,(a0)+ ; Emerald bitfield, 0x00 (none), 0x01 (first em), upto 0x3F (all 6)
                ; Boss's alive bitfield: FZ Star3 Lab3 Spring3 Marb3 GH3
                move.w #0,(a0)+ ; Boss bitfield, 0x3F (none), 0x3E (GH3), upto 0x00 (all 6 alive)
                move.w #0,(a0)+ ; Buff: Disable goal blocks. 0x00 (off), 0x01 (on)
                move.w #0,(a0)+ ; Buff: Disable R. 0x00 (off), 0x01 (on)
                move.w #0,(a0)+ ; Number of rings found.
                move.w #0,(a0)+ ; Level gate bitmask.
                move.w #0,(a0)+ ; Specials gate bitmask.
                '''

            if seed_name == ctx.remote_seed_name and slot_id == ctx.slot:
                dirty = False
                mons = self.sram_abstraction.fields.SR_Monitors
                for i in range(1,len(constants.monitor_by_id)+1):
                    broken = (mons[i-1] == MAGIC_BROKEN)
                    checked = constants.id_base+i in ctx.checked_locations
                    if broken != checked:
                        #logger.info(f"{constants.monitor_by_idx[i]} {broken} != {checked}")
                        ctx.locations_checked.add(constants.id_base+i) # Do I need to do this?
                        dirty = True
                        self.sram_abstraction.fields.SR_Monitors[i-1] = MAGIC_BROKEN

                # GH3, MZ3, SY3, LZ3, SL3, FZ
                bosses = self.sram_abstraction.fields.SR_Bosses
                prev_bosses = ctx.my_stored_data.get("bosses",0)
                for bit, idx in [[1,211], [2,212], [4,213], [8,214], [16,215], [32,216]]:
                    if constants.id_base+idx not in ctx.checked_locations and bosses&bit != 0:
                        ctx.locations_checked.add(constants.id_base+idx) # Do I need to do this?
                        dirty = True
                if cleanslate:
                    bosses = prev_bosses|bosses
                    self.sram_abstraction.fields.SR_Bosses = prev_bosses|bosses
                    #self.sram_abstraction.stage(basis+2, [boss_build])
                if prev_bosses != bosses:
                    ctx.my_stored_data["bosses"] = bosses
                    await ctx.send_msgs([{"cmd": "Set", "key": f"{ctx.slot}_{ctx.team}_sonic1_bosses",
                                          "default": 0, "want_reply": True,
                                          "operations": [{"operation": "replace", "value": bosses}]}])

                #logger.info(f"Data... {clean_data[basis:]=}")
                #logger.info(f"Data... {ctx.items_received=}")
                #ctx.items_received=[NetworkItem(item=3141501088, location=3141501221, player=2, flags=2)]
                ringcount = 0
                emeraldsset = 0
                buffs = [0,0]
                levelkeys = 0
                sskeys = 0
                invinc = 0
                shield = 0
                speeds = 0
                has_fz_key = False
                for it in ctx.items_received:
                    idx = it.item - constants.id_base
                    #logger.info(["Emerald 1", "Emerald 2", "Emerald 3", "Emerald 4", "Emerald 5", "Emerald 6", "Disable GOAL blocks", "Disable R blocks"][idx-1])
                    if idx <= 6:
                        emeraldsset |= [1,2,4,8,16,32][idx-1]
                    elif idx == 7:
                        buffs[0] = 1
                    elif idx == 8:
                        buffs[1] = 1
                    elif idx in range(9,15):
                        levelkeys |= [1,2,4,8,16,32,64,128][idx-9]
                    elif idx == 15:
                      has_fz_key = True
                    elif idx == 16:
                        sskeys += 1
                    elif idx in [23,24]:
                        ringcount += 1
                    elif idx == 25:
                        invinc += 1
                    elif idx == 26:
                        shield += 1
                    elif idx in [27,28]:
                        speeds += 1
                    elif idx >= constants.filler_base-1:
                        # Junk item... do nothing
                        pass
                    else:
                        logger.info(f"Received item {idx} and I don't know what it is.")
                
                levelkeys |= 128 # bit to enable special stages
                sskeys = [0,1,3,7,15,31,63,127,255][sskeys]

                specials = self.sram_abstraction.fields.SR_Specials
                special_build = 0
                for bit, idx in [[1,221], [2,222], [4,223], [8,224], [16,225], [32,226]]:
                    if constants.id_base+idx in ctx.checked_locations:
                        special_build |= bit
                    else:
                        if specials&bit != 0:
                            ctx.locations_checked.add(constants.id_base+idx) # Do I need to do this?
                            dirty = True
                if cleanslate:
                    self.sram_abstraction.fields.SR_Specials = special_build&sskeys
                    #self.sram_abstraction.stage(basis, [special_build])


                fzl = ctx.slot_data.get("final_zone_last",0)
                show_fz_key: bool = (fzl == 0)

                if ctx.finished_game:
                  has_fz_key = True
                  show_fz_key = True

                finish_game = False
                if not ctx.finished_game and (
                        specials.bit_count()    >= ctx.slot_data.get("specials_goal",6) # Special stags goal from yaml
                    and emeraldsset.bit_count() >= ctx.slot_data.get("emerald_goal", 6) # Emerald goal from yaml
                    and ringcount               >= ctx.slot_data.get("ring_goal",  100) # Ring goal from yaml.
                ):
                    bg = ctx.slot_data.get("boss_goal",    6) # Boss goal from yaml
                    if bosses.bit_count() >= bg and (fzl in [0,1] or (fzl == 2 and bosses & 32)):
                        finish_game = True
                        has_fz_key = True
                        show_fz_key = True
                        sskeys |= 64 # bit to show victory
                    elif bosses.bit_count() >= bg - 1 and has_fz_key:
                        show_fz_key = True

                if show_fz_key:
                    levelkeys |= 64 # bit for FZ

                if ctx.slot_data.get("hard_mode", 0):
                    ringcount = 0

                self.sram_abstraction.fields.SR_Emeralds = emeraldsset
                self.sram_abstraction.fields.SR_BuffGoals = buffs[0]
                self.sram_abstraction.fields.SR_BuffDisR = buffs[1]
                self.sram_abstraction.fields.SR_RingsFound = ringcount
                self.sram_abstraction.fields.SR_LevelGate = levelkeys
                self.sram_abstraction.fields.SR_SSGate = sskeys
                self.sram_abstraction.fields.SR_Invinc_in = invinc
                self.sram_abstraction.fields.SR_Shield_in = shield
                self.sram_abstraction.fields.SR_SpeedS_in = speeds

                keys_of_interest = ['Invinc_out', 'Shield_out', 'SpeedS_out']
                if ctx.slot_data['recv_death']:
                    keys_of_interest.extend(['DeathL_in', 'DeathL_out'])
                if ctx.slot_data['send_death']:
                    keys_of_interest.append('Deaths')

                for bk in keys_of_interest:
                  vn = f"SR_{bk}"
                  k = f"{ctx.slot}_{ctx.team}_sonic1_{bk.lower()}"
                  i_out = ctx.my_stored_data[k]
                  if not i_out:
                      i_out = 0
                  if i_out > self.sram_abstraction.fields[vn]:
                      self.sram_abstraction.fields[vn] = i_out
                  elif i_out < self.sram_abstraction.fields[vn]:
                      ctx.my_stored_data[k] = i_out = self.sram_abstraction.fields[vn]
                      await ctx.send_msgs([{"cmd": "Set", "key": k,
                                            "default": 0, "want_reply": True,
                                            "operations": [{"operation": "replace", "value": i_out}]}])
                      if k == f"{ctx.slot}_{ctx.team}_sonic1_deaths":
                          await ctx.send_death("Sonic died")
                          ctx.previous_deathlinks.add(ctx.last_death_link)

                await self.sram_abstraction.commit(ctx)
                
                if dirty:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(ctx.locations_checked)}]) # Or this?
                    #logger.info(f"{ctx.locations_checked=}")

                if finish_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            else:
                seed_complaint = f"{seed_name}/{slot_id} =?= {ctx.remote_seed_name}/{ctx.slot}"
                if ctx.complained_about_seed != seed_complaint:
                    logger.info(seed_complaint)
                    ctx.complained_about_seed = seed_complaint
            #logger.info(f"{ctx.username=}")
            