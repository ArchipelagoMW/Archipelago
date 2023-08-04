import logging
import struct
import time
from struct import unpack, pack

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_1_START = 0xE00000

# KDL3
KDL3_ROMNAME = SRAM_1_START + 0x8100
KDL3_DEATH_LINK_ADDR = SRAM_1_START + 0x9010
KDL3_GOAL_ADDR = SRAM_1_START + 0x9012
KDL3_LEVEL_ADDR = SRAM_1_START + 0x9020
KDL3_IS_DEMO = SRAM_1_START + 0x5AD5
KDL3_GAME_STATE = SRAM_1_START + 0x36D0
KDL3_GAME_SAVE = SRAM_1_START + 0x3617
KDL3_LIFE_COUNT = SRAM_1_START + 0x39CF
KDL3_KIRBY_HP = SRAM_1_START + 0x39D1
KDL3_BOSS_HP = SRAM_1_START + 0x39D5
KDL3_LIFE_VISUAL = SRAM_1_START + 0x39E3
KDL3_HEART_STARS = SRAM_1_START + 0x53A7
KDL3_WORLD_UNLOCK = SRAM_1_START + 0x53CB
KDL3_LEVEL_UNLOCK = SRAM_1_START + 0x53CD
KDL3_CURRENT_LEVEL = SRAM_1_START + 0x53D3
KDL3_BOSS_STATUS = SRAM_1_START + 0x53D5
KDL3_INVINCIBILITY_TIMER = SRAM_1_START + 0x54B1
KDL3_MG5_STATUS = SRAM_1_START + 0x5EE4
KDL3_BOSS_BUTCH_STATUS = SRAM_1_START + 0x5EEA
KDL3_JUMPING_STATUS = SRAM_1_START + 0x5EF0
KDL3_CURRENT_BGM = SRAM_1_START + 0x733E
KDL3_SOUND_FX = SRAM_1_START + 0x7F62
KDL3_ANIMAL_FRIENDS = SRAM_1_START + 0x8000
KDL3_ABILITY_ARRAY = SRAM_1_START + 0x8020
KDL3_RECV_COUNT = SRAM_1_START + 0x8050
KDL3_HEART_STAR_COUNT = SRAM_1_START + 0x8070
KDL3_GOOEY_TRAP = SRAM_1_START + 0x8080
KDL3_SLOWNESS_TRAP = SRAM_1_START + 0x8082
KDL3_ABILITY_TRAP = SRAM_1_START + 0x8084
KDL3_COMPLETED_STAGES = SRAM_1_START + 0x8200
KDL3_CONSUMABLES = SRAM_1_START + 0xA000

consumable_addrs = {
    0: 14,
    1: 15,
    2: 84,
    3: 138,
    4: 139,
    5: 204,
    6: 214,
    7: 215,
    8: 224,
    9: 330,
    10: 353,
    11: 458,
    12: 459,
    13: 522,
    14: 525,
    15: 605,
    16: 606,
    17: 630,
    18: 671,
    19: 672,
    20: 693,
    21: 791,
    22: 851,
    23: 883,
    24: 971,
    25: 985,
    26: 986,
    27: 1024,
    28: 1035,
    29: 1036,
    30: 1038,
    31: 1039,
    32: 1170,
    33: 1171,
    34: 1377,
    35: 1378,
    36: 1413,
    37: 1494,
    38: 1666,
    39: 1808,
    40: 1809,
    41: 1816,
    42: 1856,
    43: 1857,
}


class KDL3SNIClient(SNIClient):
    game = "Kirby's Dream Land 3"
    latest_world = 0x01
    latest_level = 0x01
    levels = None
    item_queue = []

    async def deathlink_kill_player(self, ctx) -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read
        game_state = await snes_read(ctx, KDL3_GAME_STATE, 1)
        if game_state[0] == 0xFF:
            return  # despite how funny it is, don't try to kill Kirby in a menu

        current_stage = await snes_read(ctx, KDL3_CURRENT_LEVEL, 1)
        if current_stage[0] == 0x7:  # boss stage
            boss_hp = await snes_read(ctx, KDL3_BOSS_HP, 1)
            if boss_hp[0] == 0:
                return  # receiving a deathlink after defeating a boss has softlock potential

        current_hp = await snes_read(ctx, KDL3_KIRBY_HP, 1)
        if current_hp[0] == 0:
            return  # don't kill Kirby while he's already dead
        snes_buffered_write(ctx, KDL3_KIRBY_HP, bytes([0x00]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

    async def validate_rom(self, ctx) -> bool:
        from SNIClient import snes_read
        rom_name = await snes_read(ctx, KDL3_ROMNAME, 0x15)
        if rom_name is None or rom_name == bytes([0] * 0x15) or rom_name[:4] != b"KDL3":
            return False

        ctx.game = self.game
        ctx.rom = rom_name
        ctx.items_handling = 0b111  # always remote items
        ctx.allow_collect = True

        death_link = await snes_read(ctx, KDL3_DEATH_LINK_ADDR, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        return True

    async def pop_item(self, ctx):
        from SNIClient import snes_buffered_write, snes_read
        if len(self.item_queue) > 0:
            item = self.item_queue.pop()
            # special handling for the remaining three
            item_idx = item.item & 0x0000FF
            if item_idx == 0x21:
                # 1-Up
                life_count = await snes_read(ctx, KDL3_LIFE_COUNT, 1)
                life_bytes = pack("H", life_count[0] + 1)
                snes_buffered_write(ctx, KDL3_LIFE_COUNT, life_bytes)
                snes_buffered_write(ctx, KDL3_LIFE_VISUAL, life_bytes)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x33]))
            elif item_idx == 0x22:
                # Maxim Tomato
                # Check for Gooey
                gooey_hp = await snes_read(ctx, KDL3_KIRBY_HP + 2, 1)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x26]))
                if gooey_hp[0] > 0x00:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, bytes([0x08]))
                    snes_buffered_write(ctx, KDL3_KIRBY_HP + 2, bytes([0x08]))
                else:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, bytes([0x0A]))
            elif item_idx == 0x23:
                # Invincibility Candy
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x26]))
                snes_buffered_write(ctx, KDL3_INVINCIBILITY_TIMER, bytes([0x84, 0x03]))
            elif item_idx == 0x40:
                check_gooey_r = await snes_read(ctx, KDL3_GOOEY_TRAP, 2)
                check_gooey = struct.unpack("H", check_gooey_r)
                if check_gooey[0] == 0:
                    snes_buffered_write(ctx, KDL3_GOOEY_TRAP, bytes([0x01, 0x00]))
                else:
                    self.item_queue.append(item)  # We can't apply this yet
            elif item_idx == 0x41:
                check_slow_r = await snes_read(ctx, KDL3_SLOWNESS_TRAP, 2)
                check_slow = struct.unpack("H", check_slow_r)
                if check_slow[0] == 0:
                    snes_buffered_write(ctx, KDL3_SLOWNESS_TRAP, bytes([0x84, 0x03]))
                    snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0xA7]))
                else:
                    self.item_queue.append(item)  # We can't apply this yet
            elif item_idx == 0x42:
                check_ability_r = await snes_read(ctx, KDL3_ABILITY_TRAP, 2)
                check_ability = struct.unpack("H", check_ability_r)
                if check_ability[0] == 0:
                    snes_buffered_write(ctx, KDL3_ABILITY_TRAP, bytes([0x01, 0x00]))
                else:
                    self.item_queue.append(item)  # We can't apply this yet

    async def game_watcher(self, ctx) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        halken = await snes_read(ctx, WRAM_START, 6)
        if halken != b"halken":
            return
        # can't check debug anymore, without going and copying the value. might be important later.
        is_demo = await snes_read(ctx, KDL3_IS_DEMO, 1)  # 1 - recording a demo, 2 - playing back recorded, 3+ is a demo
        if is_demo[0] > 0x00:
            return
        current_save = await snes_read(ctx, KDL3_GAME_SAVE, 1)
        goal = await snes_read(ctx, KDL3_GOAL_ADDR, 1)
        boss_butch_status = await snes_read(ctx, KDL3_BOSS_BUTCH_STATUS + (current_save[0] * 2), 1)
        mg5_status = await snes_read(ctx, KDL3_MG5_STATUS + (current_save[0] * 2), 1)
        jumping_status = await snes_read(ctx, KDL3_JUMPING_STATUS + (current_save[0] * 2), 1)
        if boss_butch_status[0] == 0xFF:
            return  # save file is not created, ignore
        if (goal[0] == 0x00 and boss_butch_status[0] == 0x01) \
                or (goal[0] == 0x01 and boss_butch_status[0] == 0x03) \
                or (goal[0] == 0x02 and mg5_status[0] == 0x03) \
                or (goal[0] == 0x03 and jumping_status[0] == 0x03):
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        current_bgm = await snes_read(ctx, KDL3_CURRENT_BGM, 1)
        if current_bgm[0] in (0x00, 0x21, 0x22, 0x23, 0x25, 0x2A, 0x2B):
            return  # null, title screen, opening, save select, true and false endings
        game_state = await snes_read(ctx, KDL3_GAME_STATE, 1)
        current_hp = await snes_read(ctx, KDL3_KIRBY_HP, 1)
        if "DeathLink" in ctx.tags and game_state[0] == 0x00 and ctx.last_death_link + 1 < time.time():
            currently_dead = current_hp[0] == 0x00
            await ctx.handle_deathlink_state(currently_dead)

        if self.levels is None:
            self.levels = dict()
            for i in range(5):
                level_data = await snes_read(ctx, KDL3_LEVEL_ADDR + (14 * i), 14)
                self.levels[i] = unpack("HHHHHHH", level_data)

        recv_count = await snes_read(ctx, KDL3_RECV_COUNT, 1)
        recv_amount = recv_count[0]
        if recv_amount < len(ctx.items_received):
            item = ctx.items_received[recv_amount]
            recv_amount += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_amount, len(ctx.items_received)))

            snes_buffered_write(ctx, KDL3_RECV_COUNT, pack("H", recv_amount))
            if item.item & 0x000070 == 0:
                ability = item.item & 0x00000F
                snes_buffered_write(ctx, KDL3_ABILITY_ARRAY + (ability * 2), pack("H", ability))
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x32]))
            elif item.item & 0x000010 > 0:
                friend = (item.item & 0x00000F)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x32]))
                snes_buffered_write(ctx, KDL3_ANIMAL_FRIENDS + (friend << 1), bytes([friend + 1]))
            elif item.item == 0x770020:
                # Heart Star
                heart_star_count = await snes_read(ctx, KDL3_HEART_STAR_COUNT, 1)
                snes_buffered_write(ctx, KDL3_HEART_STAR_COUNT, pack("H", heart_star_count[0] + 1))
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x16]))
            else:
                self.item_queue.append(item)

        await snes_flush_writes(ctx)

        new_checks = []
        # level completion status
        world_unlocks = await snes_read(ctx, KDL3_WORLD_UNLOCK, 1)
        if world_unlocks[0] > 0x06:
            return  # save is not loaded, ignore
        stages_raw = await snes_read(ctx, KDL3_COMPLETED_STAGES, 60)
        stages = struct.unpack("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH", stages_raw)
        for i in range(30):
            loc_id = 0x770000 + i + 1
            if stages[i] == 1 and loc_id not in ctx.checked_locations:
                new_checks.append(loc_id)
            elif stages[i] == 0 and loc_id in ctx.checked_locations:
                snes_buffered_write(ctx, KDL3_COMPLETED_STAGES + (i * 2), struct.pack("H", 1))

        # heart star status
        heart_stars = await snes_read(ctx, KDL3_HEART_STARS, 35)
        for i in range(5):
            start_ind = i * 7
            for j in range(1, 7):
                level_ind = start_ind + j - 1
                loc_id = 0x770100 + (6 * i) + j
                if heart_stars[level_ind] and loc_id not in ctx.checked_locations:
                    new_checks.append(loc_id)
                elif not heart_stars[level_ind] and loc_id in ctx.checked_locations:
                    # only handle collected heart stars
                    snes_buffered_write(ctx, KDL3_HEART_STARS + level_ind, bytes([0x01]))
        await snes_flush_writes(ctx)
        # consumable status
        consumables = await snes_read(ctx, KDL3_CONSUMABLES, 1920)
        for consumable in consumable_addrs:
            # TODO: see if this can be sped up in any way
            if consumables[consumable_addrs[consumable]] == 0x01:
                loc_id = 0x770300 + consumable
                if loc_id not in ctx.checked_locations:
                    new_checks.append(loc_id)
        # boss status
        boss_flag_bytes = await snes_read(ctx, KDL3_BOSS_STATUS, 2)
        boss_flag = unpack("H", boss_flag_bytes)[0]
        if boss_flag & 2 > 0 and 0x770200 not in ctx.checked_locations:
            new_checks.append(0x770200)
        if boss_flag & 8 > 0 and 0x770201 not in ctx.checked_locations:
            new_checks.append(0x770201)
        if boss_flag & 32 > 0 and 0x770202 not in ctx.checked_locations:
            new_checks.append(0x770202)
        if boss_flag & 128 > 0 and 0x770203 not in ctx.checked_locations:
            new_checks.append(0x770203)
        if boss_flag & 512 > 0 and 0x770204 not in ctx.checked_locations:
            new_checks.append(0x770204)

        rom = await snes_read(ctx, KDL3_ROMNAME, 0x15)
        if rom != ctx.rom:
            ctx.rom = None

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        if game_state[0] != 0xFF:
            await self.pop_item(ctx)
