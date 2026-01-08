import logging
import time
import typing
from NetUtils import ClientStatus, color, NetworkItem
from worlds.AutoSNIClient import SNIClient
from typing import TYPE_CHECKING
from .items import treasures, BASE_ID
from .client_data import treasure_base_id, boss_flags, deluxe_essence_flags, planet_flags, consumable_table

if TYPE_CHECKING:
    from SNIClient import SNIContext

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
SRAM_1_START = 0xE00000

KSS_KIRBY_LIVES = SRAM_1_START + 0x137A
KSS_KIRBY_HP = SRAM_1_START + 0x137C
KSS_DEMO_STATE = SRAM_1_START + 0x138E
KSS_GAME_STATE = SRAM_1_START + 0x1390
KSS_GOURMET_RACE_WON = SRAM_1_START + 0x171D
KSS_DYNA_UNLOCKED = SRAM_1_START + 0x1A63
KSS_DYNA_SWITCHES = SRAM_1_START + 0x1A64
KSS_DYNA_IRON_MAM = SRAM_1_START + 0x1A67
KSS_REVENGE_CHAPTERS = SRAM_1_START + 0x1A69
KSS_RAINBOW_STAR = SRAM_1_START + 0x1A6B
KSS_CURRENT_SUBGAMES = SRAM_1_START + 0x1A85
KSS_COMPLETED_SUBGAMES = SRAM_1_START + 0x1A93
KSS_ARENA_HIGH_SCORE = SRAM_1_START + 0x1AA1
KSS_BOSS_DEFEATED = SRAM_1_START + 0x1AE7  # 4 bytes
KSS_TGCO_TREASURE = SRAM_1_START + 0x1B05  # 8 bytes
KSS_TGC0_GOLD = SRAM_1_START + 0x1B0F  # 3-byte 24-bit int
KSS_COPY_ABILITIES = SRAM_1_START + 0x1B1D  # originally Milky Way Wishes deluxe essences
KSS_MWW_ITEMS = SRAM_1_START + 0x1B20
# Remapped for sending
KSS_DYNA_COMPLETED = SRAM_1_START + 0x7A63
KSS_SENT_DYNA_SWITCH = SRAM_1_START + 0x7A64
KSS_COMPLETED_PLANETS = SRAM_1_START + 0x7A6B
KSS_SENT_TGCO_TREASURE = SRAM_1_START + 0x7B05  # 8 bytes
KSS_SENT_DELUXE_ESSENCE = SRAM_1_START + 0x7B1D  # 3 bytes

# AP-received extras
KSS_RECEIVED_SUBGAMES = SRAM_1_START + 0x8000
KSS_RECEIVED_ITEMS = SRAM_1_START + 0x8002
KSS_RECEIVED_PLANETS = SRAM_1_START + 0x8004
KSS_PLAY_SFX = SRAM_1_START + 0x8006
KSS_ACTIVATE_CANDY = SRAM_1_START + 0x8008
KSS_MIRROR_GAME = SRAM_1_START + 0x800A
KSS_MIRROR_ROOM = SRAM_1_START + 0x800C

KSS_ROMNAME = SRAM_1_START + 0x8100
KSS_DEATH_LINK_ADDR = SRAM_1_START + 0x9000
KSS_CONSUMABLE_FILTER = SRAM_1_START + 0x9001

KSS_DEATH_MESSAGES = {
    0: ("Pop Star was too much for ", "."),
    1: ("", " failed to defeat Dyna Blade."),
    2: ("", " is not very good at eating."), # like 85% sure you can't actually die naturally in Gourmet Race
    3: ("", " got lost in the great cave."),
    4: ("Meta Knight defeated ", " and took over Pop Star."),
    5: ("", " was lost in the stars."),
    6: ("", " was defeated in The Arena."),
}

class KSSSNIClient(SNIClient):
    game = "Kirby Super Star"
    patch_suffix = ".apkss"
    item_queue: typing.List[NetworkItem] = []
    consumable_filter: int = 0
    tracker_key: str = ""

    async def deathlink_kill_player(self, ctx: "SNIContext") -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_read, snes_flush_writes
        game_state = int.from_bytes(await snes_read(ctx, KSS_GAME_STATE, 1), "little")
        if game_state == 3:
            snes_buffered_write(ctx, KSS_KIRBY_HP, int.to_bytes(0, 2, "little"))
            await snes_flush_writes(ctx)
            ctx.death_state = DeathState.dead
            ctx.last_death_link = time.time()

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from SNIClient import snes_read
        rom_name = await snes_read(ctx, KSS_ROMNAME, 0x15)
        if rom_name is None or rom_name == bytes([0] * 0x15) or rom_name[:3] != b"KSS":
            return False

        ctx.game = self.game
        ctx.rom = rom_name
        ctx.items_handling = 0b111  # full remote
        ctx.allow_collect = True

        death_link = await snes_read(ctx, KSS_DEATH_LINK_ADDR, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))
        consumable_filter = await snes_read(ctx, KSS_CONSUMABLE_FILTER, 2)
        self.consumable_filter = int.from_bytes(consumable_filter, "little")
        return True

    async def pop_item(self, ctx: "SNIContext", game_state: int) -> None:
        from SNIClient import snes_read, snes_buffered_write
        if game_state not in (0x3, 0xC):
            return
        if self.item_queue:
            item = self.item_queue.pop()
            if item.item & 0xF == 2:
                # Maxim
                snes_buffered_write(ctx, KSS_KIRBY_HP, int.to_bytes(0x46, 2, "little"))
                snes_buffered_write(ctx, KSS_KIRBY_HP + 2, int.to_bytes(0x46, 2, "little"))
                snes_buffered_write(ctx, KSS_PLAY_SFX, int.to_bytes(0x2C, 2, "little"))
            elif item.item & 0xF == 3:
                # Invincibility
                snes_buffered_write(ctx, KSS_ACTIVATE_CANDY, int.to_bytes(1, 2, "little"))
                snes_buffered_write(ctx, KSS_PLAY_SFX, int.to_bytes(0x2C, 2, "little"))
            elif game_state != 3:
                self.item_queue.insert(0, item)
                return
            elif item.item & 0xF == 1:
                # 1-Up
                lives = int.from_bytes(await snes_read(ctx, KSS_KIRBY_LIVES, 2), "little")
                snes_buffered_write(ctx, KSS_KIRBY_LIVES, int.to_bytes(lives + 1, 2, "little"))
                snes_buffered_write(ctx, KSS_PLAY_SFX, int.to_bytes(0x3E, 2, "little"))
            else:
                pass

    async def game_watcher(self, ctx: "SNIContext") -> None:
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes, DeathState

        if not ctx.slot or not ctx.server:
            return

        demo_state = int.from_bytes(await snes_read(ctx, KSS_DEMO_STATE, 2), "little")
        if not demo_state:
            return

        if not self.tracker_key and ctx.slot:
            self.tracker_key = f"KSS_STAGE_{ctx.team}_{ctx.slot}"
            ctx.set_notify(self.tracker_key)

        current_subgames = int.from_bytes(await snes_read(ctx, KSS_CURRENT_SUBGAMES, 2), "little")
        if current_subgames & 0x0080 != 0:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        game_state = int.from_bytes(await snes_read(ctx, KSS_GAME_STATE, 1), "little")

        kirby_hp = int.from_bytes(await snes_read(ctx, KSS_KIRBY_HP, 2), "little")
        mirror_game = int.from_bytes(await snes_read(ctx, KSS_MIRROR_GAME, 2), "little")
        if "DeathLink" in ctx.tags and game_state == 3 and ctx.last_death_link + 1 < time.time() \
                and ctx.death_state == DeathState.alive:
            if kirby_hp == 0:
                death_pre, death_post = KSS_DEATH_MESSAGES[mirror_game]
                await ctx.handle_deathlink_state(True, f"{death_pre}{ctx.player_names[ctx.slot]}{death_post}")
        elif "DeathLink" in ctx.tags and game_state == 3 and kirby_hp > 0:
            ctx.death_state = DeathState.alive

        if self.tracker_key:
            mirror_room = int.from_bytes(await snes_read(ctx, KSS_MIRROR_ROOM, 2), "little")
            if game_state in (0, 1):
                tracker_val = "M_M"
            else:
                tracker_val = f"{mirror_game}_{mirror_room}"
            if ctx.stored_data.get(self.tracker_key, None) != tracker_val:
                await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": self.tracker_key,
                        "default": "M_M",
                        "want_reply": False,
                        "operations": [
                            {"operation": "replace", "value": tracker_val}
                        ]
                    }])
            print(ctx.stored_data.get(self.tracker_key, None))

        save_abilities = 0
        i = 0
        non_mww = 0
        for i, ability in enumerate([item for item in ctx.items_received if item.item & 0x100]):
            save_abilities |= (1 << ((ability.item & 0xFF) - 1))
            if ability.item & 0xFF > 0x13:
                non_mww += 1
        snes_buffered_write(ctx, KSS_COPY_ABILITIES, int.to_bytes(save_abilities, 3, "little"))
        if save_abilities:
            snes_buffered_write(ctx, KSS_MWW_ITEMS, int.to_bytes(i - non_mww + 1, 1, "little"))

        known_treasures = int.from_bytes(await snes_read(ctx, KSS_TGCO_TREASURE, 8), "little")
        known_value = int.from_bytes(await snes_read(ctx, KSS_TGC0_GOLD, 4), "little")
        treasure_data = 0
        treasure_value = 0
        for treasure in [item for item in ctx.items_received if item.item & 0x200]:
            treasure_info = treasures[ctx.item_names.lookup_in_game(treasure.item)]
            treasure_value += treasure_info.value
            treasure_data |= (1 << ((treasure.item & 0xFF) - 1))
        if treasure_data != known_treasures or treasure_value != known_value:
            snes_buffered_write(ctx, KSS_TGCO_TREASURE, treasure_data.to_bytes(8, "little"))
            snes_buffered_write(ctx, KSS_TGC0_GOLD, treasure_value.to_bytes(4, "little"))

        unlocked_planets = int.from_bytes(await snes_read(ctx, KSS_RECEIVED_PLANETS, 2), "little")
        for planet_item in [item for item in ctx.items_received if item.item & 0x400]:
            planet = planet_item.item & 0xFF
            unlocked_planets |= (1 << planet)
        snes_buffered_write(ctx, KSS_RECEIVED_PLANETS, unlocked_planets.to_bytes(2, "little"))

        dyna_stage = int.from_bytes(await snes_read(ctx, KSS_DYNA_UNLOCKED, 1), "little")
        stage_count = min(4, sum(1 for item in ctx.items_received if (item.item & 0x802) == 0x802))
        if dyna_stage != stage_count:
            snes_buffered_write(ctx, KSS_DYNA_UNLOCKED, stage_count.to_bytes(1, "little"))


        unlocked_switches = int.from_bytes(await snes_read(ctx, KSS_DYNA_SWITCHES, 1), "little")
        for switch_item in [item for item in ctx.items_received if (item.item & 0x803) in (0x800, 0x801)]:
            switch = switch_item.item & 0xFF
            unlocked_switches |= (1 << switch)
        snes_buffered_write(ctx, KSS_DYNA_SWITCHES, unlocked_switches.to_bytes(1, "little"))

        planet_clear = int.from_bytes(await snes_read(ctx, KSS_RAINBOW_STAR, 1), "little")
        current_total = sum(1 for item in ctx.items_received if item.item & 0xFFFF == 0x1004)
        new_clear = 0
        for i in range(min(current_total, 8)):
            new_clear |= (1 << i)
        if planet_clear != new_clear and new_clear:
            snes_buffered_write(ctx, KSS_RAINBOW_STAR, int.to_bytes(new_clear, 1, "little"))

        recv_count = int.from_bytes(await snes_read(ctx, KSS_RECEIVED_ITEMS, 2), "little")
        if recv_count < len(ctx.items_received):
            item = ctx.items_received[recv_count]
            recv_count += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_count, len(ctx.items_received)))
            snes_buffered_write(ctx, KSS_RECEIVED_ITEMS, recv_count.to_bytes(2, "little"))
            if item.item & 0xFF00 == 0:
                # Subgame
                unlocked_subgames = int.from_bytes(await snes_read(ctx, KSS_RECEIVED_SUBGAMES, 2), "little")
                unlocked_subgames |= (1 << (item.item & 0xFF))
                snes_buffered_write(ctx, KSS_RECEIVED_SUBGAMES, unlocked_subgames.to_bytes(2, "little"))
            elif item.item & 0x100 != 0:
                snes_buffered_write(ctx, KSS_PLAY_SFX, int.to_bytes(0x44, 2, "little"))
            elif item.item & 0x200 != 0:
                snes_buffered_write(ctx, KSS_PLAY_SFX, int.to_bytes(0x86, 2, "little"))
            elif item.item & 0x400 != 0:
                snes_buffered_write(ctx, KSS_PLAY_SFX, int.to_bytes(0x42, 2, "little"))
            elif item.item & 0x800 != 0:
                snes_buffered_write(ctx, KSS_PLAY_SFX, int.to_bytes(0x4D, 2, "little"))
            elif item.item & 0x1000 != 0:
                if item.item & 0xF != 4:
                    self.item_queue.append(item)
                else:
                    snes_buffered_write(ctx, KSS_PLAY_SFX, int.to_bytes(0x43, 2, "little"))

        await self.pop_item(ctx, game_state)

        await snes_flush_writes(ctx)

        new_checks = []

        boss_flag = int.from_bytes(await snes_read(ctx, KSS_BOSS_DEFEATED, 4), "little")
        for flag, location in boss_flags.items():
            if boss_flag & flag and location not in ctx.checked_locations:
                new_checks.append(location)

        deluxe_flag = int.from_bytes(await snes_read(ctx, KSS_SENT_DELUXE_ESSENCE, 3), "little")
        for flag, location in deluxe_essence_flags.items():
            if deluxe_flag & flag and location not in ctx.checked_locations:
                new_checks.append(location)

        treasure_flag = int.from_bytes(await snes_read(ctx, KSS_SENT_TGCO_TREASURE, 8), "little")
        for flag in range(60):
            location = treasure_base_id + flag
            if (1 << flag) & treasure_flag and location not in ctx.checked_locations:
                new_checks.append(location)

        dyna_flag = int.from_bytes(await snes_read(ctx, KSS_SENT_DYNA_SWITCH, 1), "little")
        for flag, location in enumerate([BASE_ID + 9, BASE_ID + 10]):
            if (flag + 1) & dyna_flag and location not in ctx.checked_locations:
                new_checks.append(location)

        dyna_stage = int.from_bytes(await snes_read(ctx, KSS_DYNA_COMPLETED, 1), "little")
        for i in range(5):
            location = BASE_ID + 4 + i
            if dyna_stage & (1 << i) and location not in ctx.checked_locations:
                new_checks.append(location)

        dyna_mam = int.from_bytes(await snes_read(ctx, KSS_DYNA_IRON_MAM, 1), "little")
        if dyna_mam and BASE_ID + 11 not in ctx.checked_locations:
            new_checks.append(BASE_ID + 11)

        revenge = int.from_bytes(await snes_read(ctx, KSS_REVENGE_CHAPTERS, 1), "little")
        for i in range(revenge & 0x7):
            location = BASE_ID + 79 + i
            if location not in ctx.checked_locations:
                new_checks.append(location)

        mww_planets = int.from_bytes(await snes_read(ctx, KSS_COMPLETED_PLANETS, 1), "little")
        for i in range(7):
            flag = 1 << i
            location = planet_flags[flag]
            if flag & mww_planets and location not in ctx.checked_locations:
                new_checks.append(location)

        gourmet_race = int.from_bytes(await snes_read(ctx, KSS_GOURMET_RACE_WON, 1), "little")
        for i in range(3):
            flag = 1 << i
            location = BASE_ID + 12 + i
            if flag & gourmet_race and location not in ctx.checked_locations:
                new_checks.append(location)

        arena = int.from_bytes(await snes_read(ctx, KSS_ARENA_HIGH_SCORE, 1), "little")
        for i in range(arena >> 1):
            location = BASE_ID + 113 + i
            if location not in ctx.checked_locations:
                new_checks.append(location)

        if self.consumable_filter:
            consumables = bytearray()
            for i in range(0, 0x10000, 0x1000):
                consumables.extend(await snes_read(ctx, SRAM_1_START + 0x10000 + i, 0x1000))
            for consumable, data in consumable_table.items():
                if consumable & self.consumable_filter:
                    location = consumable + BASE_ID
                    offset, mask = data
                    if consumables[offset] & mask:
                        if location not in ctx.checked_locations:
                            new_checks.append(location)

        await ctx.check_locations(new_checks)
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            loc = ctx.location_names.lookup_in_game(new_check_id)
            snes_logger.info(
                f'New Check: {loc} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
