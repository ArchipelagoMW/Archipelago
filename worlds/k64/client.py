import logging
import struct
import sys
import typing
import asyncio
from base64 import b64encode
from enum import Enum
from typing import TYPE_CHECKING

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient

from .consumable_info import consumables
from .regions import default_levels
from .rom import slot_data, crystal_requirements

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from kivymd.uix.label import MDLabel

k64_logger = logging.getLogger("K64")

ability_to_bit = {
    0x0001: 0,
    0x0002: 1,
    0x0003: 2,
    0x0004: 3,
    0x0005: 4,
    0x0006: 5,
    0x0007: 6,
    0x0200: 7,
    0x0201: 8,
    0x0202: 9,
    0x0203: 10,
    0x0204: 11,
    0x0205: 12,
    0x0206: 13,
    0x0207: 14,
    0x0208: 15,
    0x0209: 16,
    0x020A: 17,
    0x020B: 18,
    0x020C: 19,
    0x020D: 20,
    0x020E: 21,
    0x020F: 22,
    0x0210: 23,
    0x0211: 24,
    0x0212: 25,
    0x0213: 26,
    0x0214: 27,
    0x0215: 28,
    0x0216: 29,
    0x0217: 30,
    0x0218: 31,
    0x0219: 32,
    0x021A: 33,
    0x021B: 34,
}

power_combos = {
    (1, 1): 7,
    (1, 2): 8,
    (1, 3): 9,
    (1, 4): 10,
    (1, 5): 11,
    (1, 6): 12,
    (1, 7): 13,
    (2, 2): 14,
    (2, 3): 15,
    (2, 4): 16,
    (2, 5): 17,
    (2, 6): 18,
    (2, 7): 19,
    (3, 3): 20,
    (3, 4): 21,
    (3, 5): 22,
    (3, 6): 23,
    (3, 7): 24,
    (4, 4): 25,
    (4, 5): 26,
    (4, 6): 27,
    (4, 7): 28,
    (5, 5): 29,
    (5, 6): 30,
    (5, 7): 31,
    (6, 6): 32,
    (6, 7): 33,
    (7, 7): 34,
}

stage_to_byte = {
    1: [0, 1, 2],
    2: [6, 7, 8, 9],
    3: [12, 13, 14, 15],
    4: [18, 19, 20, 21],
    5: [24, 25, 26, 27],
    6: [30, 31, 32],
}

K64_IS_DEMO = 0x3387B2
K64_GAME_STATE = 0xBE4F0
K64_CURRENT_LEVEL = 0xBE500
K64_CURRENT_STAGE = 0xBE504
K64_SAVE_ADDRESS = 0xD6B00
K64_MENU_LEVEL = K64_SAVE_ADDRESS + 0x98
K64_BOSS_CRYSTALS = K64_SAVE_ADDRESS + 0xC0
K64_CRYSTAL_ARRAY = K64_SAVE_ADDRESS + 0xC8
K64_STAGE_STATUSES = K64_SAVE_ADDRESS + 0xE0
K64_ENEMY_CARDS = K64_SAVE_ADDRESS + 0x110
K64_COPY_ABILITY = K64_SAVE_ADDRESS + 0x168
K64_CRYSTAL_ADDRESS = K64_SAVE_ADDRESS + 0x170
K64_RECV_INDEX = K64_SAVE_ADDRESS + 0x174
K64_DEATHLINK_SET = K64_SAVE_ADDRESS + 0x17C
K64_FRIENDS = K64_SAVE_ADDRESS + 0x180
K64_KIRBY_LIVES = K64_SAVE_ADDRESS + 0x34C
K64_KIRBY_HEALTH = K64_SAVE_ADDRESS + 0x350
K64_STAR_COUNT = K64_SAVE_ADDRESS + 0x360
K64_KIRBY_LIVES_VISUAL = K64_SAVE_ADDRESS + 0x388
K64_KIRBY_HEALTH_VISUAL = K64_SAVE_ADDRESS + 0x38C

K64_INVINCIBILITY_CANDY = 0x12E7C9

K64_CONSUMABLES = 0x500000

K64_SPLIT_POWER_COMBO = slot_data
K64_DEATHLINK = slot_data + 1
K64_BOSS_REQUIREMENTS = crystal_requirements
K64_LEVEL_ADDRESS = 0x1FFF230


class DeathState(Enum):
    Alive = 0
    IsKillingPlayer = 1
    Dead = 2

K64_WORLD_REMAP = {
    0: "Pop Star",
    1: "Rock Star",
    2: "Aqua Star",
    3: "Neo Star",
    4: "Shiver Star",
    5: "Ripple Star",
    6: "Zero-Two"
}


class K64Client(BizHawkClient):
    game = "Kirby 64 - The Crystal Shards"
    system = "N64"
    patch_suffix = ".apk64cs"
    current_level_storage_key: str = ""
    death_link: typing.Optional[bool] = None
    rom: typing.Optional[bytes] = None
    levels: typing.Optional[typing.Dict[int, typing.List[int]]] = None
    split_power_combos: typing.Optional[bool] = None
    boss_requirements: typing.Optional[bytes] = None
    crystal_label: "MDLabel" = None
    death_state: DeathState = DeathState.Alive

    def interpret_copy_ability(self, current, new_ability):
        if self.split_power_combos:
            # simple, just allow the new power combo
            xor_val = 1 << ability_to_bit[new_ability]
            output = current | (current ^ xor_val)
        else:
            # complex, we need to figure out what abilities they are allowed to have
            # since we have the currently unlocked abilities,and they can only get abilities related to the newly
            # obtained ability, we can just loop once
            shifter = 1
            copy_abilties = {}
            for i in range(1, 8):
                copy_abilties[i] = shifter & current
                shifter <<= 1
            new = new_ability & 0xFF
            copy_abilties[new] = 1
            output = current | 1 << new - 1
            for i in range(1, 8):
                if copy_abilties[i]:
                    if i < new:
                        output |= (1 << power_combos[i, new])
                    else:
                        output |= (1 << power_combos[new, i])

        return K64_COPY_ABILITY, struct.pack(">Q", output), "RDRAM"

    async def deathlink_kill_player(self, ctx) -> None:
        # what a mess
        # they store his HP as a float...
        # there's 7 possible values...
        # and he only dies after taking a hit at 0 hp
        # all of the handling is in basepatch
        from worlds._bizhawk import write
        self.death_state = DeathState.IsKillingPlayer
        await write(ctx.bizhawk_ctx, [(K64_DEATHLINK_SET, int.to_bytes(1, 4, "big"), "RDRAM")])

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        if self.rom:
            ctx.auth = b64encode(self.rom).decode()

    async def validate_rom(self, ctx) -> bool:
        from worlds._bizhawk import RequestFailedError, read

        def false() -> bool:
            if self.crystal_label and ctx.ui:
                if self.crystal_label in ctx.ui.connect_layout.children:
                    ctx.ui.connect_layout.remove_widget(self.crystal_label)
            return False

        try:
            kirby = (await read(ctx.bizhawk_ctx, [(0x20, 7, "ROM")]))[0]
            if kirby != b"Kirby64":
                return false()
            game_name = ((await read(ctx.bizhawk_ctx, [(0x1FFF200, 21, "ROM")]))[0])
            if game_name[:3] != b"K64":
                return false()
        except UnicodeDecodeError:
            return false()
        except RequestFailedError:
            return false()  # Should verify on the next pass
        ctx.game = self.game
        self.rom = game_name
        ctx.items_handling = 0b111
        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                assert ctx.slot is not None
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    asyncio.create_task(self.deathlink_kill_player(ctx))

    async def update_crystal_label(self, ctx: "BizHawkClientContext"):
        from kvui import TooltipLabel

        if not self.crystal_label:
            self.crystal_label = TooltipLabel(text=f"", size_hint_x=None, width=125, halign="center", valign="center")
            ctx.ui.connect_layout.add_widget(self.crystal_label)

        current_crystals = sum(1 for item in ctx.items_received if item.item == 0x0020)
        highest = 1
        for crystal in self.boss_requirements:
            if current_crystals < crystal:
                self.crystal_label.text = f"Level {highest}: {current_crystals}/{crystal}"
                break
            highest += 1
        else:
            self.crystal_label.text = "Level 7"

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk import read, write

        if ctx.server is None:
            return

        if ctx.slot is None:
            await ctx.send_connect(name=ctx.auth)

        if ctx.slot_data is None:
            return

        if not self.current_level_storage_key:
            self.current_level_storage_key = f"k64_current_level_{ctx.team}_{ctx.slot}"
            ctx.set_notify(self.current_level_storage_key)

        if self.levels is None:
            levels = (await read(ctx.bizhawk_ctx, [
                (K64_LEVEL_ADDRESS, 56, "ROM")
            ]))[0]
            self.levels = {}
            level_counter = 0
            for level, stage_num in zip(range(1, 7), (4, 5, 5, 5, 5, 4)):
                self.levels[level] = []
                for i in range(stage_num):
                    self.levels[level].append(struct.unpack(">H", levels[level_counter:level_counter+2])[0])
                    level_counter += 2

        if self.death_link is None:
            deathlink = (await read(ctx.bizhawk_ctx, [
                (K64_DEATHLINK, 1, "ROM")
            ]))[0]

            self.death_link = bool(deathlink[0])
            await ctx.update_death_link(self.death_link)

        if self.split_power_combos is None:
            split_power_combos = (await read(ctx.bizhawk_ctx, [
                (K64_SPLIT_POWER_COMBO, 1, "ROM")
            ]))[0]

            self.split_power_combos = bool(split_power_combos[0])

        if self.boss_requirements is None:
            boss_requirements = (await read(ctx.bizhawk_ctx, [
                (K64_BOSS_REQUIREMENTS, 6, "ROM")
            ]))
            self.boss_requirements = boss_requirements[0]

        (halken, is_demo, game_state, stage_array, boss_crystals, crystal_array,
         copy_ability, crystals, recv_index, health, health_visual,
         lives, lives_visual, current_level, current_stage,
         menu_level, consumable_checks, star_count) = await read(ctx.bizhawk_ctx, [
            (K64_SAVE_ADDRESS, 16, "RDRAM"),
            (K64_IS_DEMO, 4, "RDRAM"),
            (K64_GAME_STATE, 4, "RDRAM"),
            (K64_STAGE_STATUSES, 42, "RDRAM"),
            (K64_BOSS_CRYSTALS, 8, "RDRAM"),
            (K64_CRYSTAL_ARRAY, 24, "RDRAM"),
            (K64_COPY_ABILITY, 8, "RDRAM"),
            (K64_CRYSTAL_ADDRESS, 4, "RDRAM"),
            (K64_RECV_INDEX, 4, "RDRAM"),
            (K64_KIRBY_HEALTH, 4, "RDRAM"),
            (K64_KIRBY_HEALTH_VISUAL, 4, "RDRAM"),
            (K64_KIRBY_LIVES, 4, "RDRAM"),
            (K64_KIRBY_LIVES_VISUAL, 4, "RDRAM"),
            (K64_CURRENT_LEVEL, 4, "RDRAM"),
            (K64_CURRENT_STAGE, 4, "RDRAM"),
            (K64_MENU_LEVEL, 4, "RDRAM"),
            (K64_CONSUMABLES, 0xC80, "RDRAM"),
            (K64_STAR_COUNT, 4, "RDRAM"),
            ])

        if halken != b'-HALKEN--KIRBY4-':
            return

        game_state_val = int.from_bytes(game_state, "big")
        if game_state_val in range(11):
            # 0x0 - 0xA are main menu states
            # 0xB is the world select
            return

        if boss_crystals[6] != 0:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        if self.death_link:
            if self.death_state != DeathState.Dead and int.from_bytes(health_visual, "big") == 0:
                if self.death_state == DeathState.Alive:
                    # send a death link
                    await ctx.send_death(
                        f"{ctx.player_names[ctx.slot]} couldn't handle {K64_WORLD_REMAP[int.from_bytes(current_level, 'big')]}.")
                self.death_state = DeathState.Dead
            elif int.from_bytes(health_visual, "big") != 0 and self.death_state == DeathState.Dead:
                self.death_state = DeathState.Alive

        writes = []

        recv_count = struct.unpack(">I", recv_index)[0]
        if recv_count < len(ctx.items_received):
            item = ctx.items_received[recv_count]
            recv_count += 1

            writes.append((K64_RECV_INDEX, struct.pack(">I", recv_count), "RDRAM"))
            if item.item in ability_to_bit:
                writes.append(self.interpret_copy_ability(struct.unpack(">Q", copy_ability)[0], item.item))
            elif item.item & 0x100:
                writes.append((K64_FRIENDS + (item.item & 0xF), int.to_bytes(1, 1, "little"), "RDRAM"))
            elif item.item == 0x0020:
                # crystal shard
                writes.append((K64_CRYSTAL_ADDRESS, struct.pack(">I", struct.unpack(">I", crystals)[0] + 1), "RDRAM"))
            elif item.item == 0x0021:
                # 1-Up
                current_lives = int.from_bytes(lives, "big")
                writes.extend([
                    (K64_KIRBY_LIVES, struct.pack(">I", current_lives + 1), "RDRAM"),
                    (K64_KIRBY_LIVES_VISUAL, struct.pack(">I", current_lives + 1), "RDRAM"),
                ])
            elif item.item == 0x0022:
                # Maxim Tomato
                writes.extend([
                    (K64_KIRBY_HEALTH, struct.pack(">f", 6), "RDRAM"),
                    (K64_KIRBY_HEALTH_VISUAL, struct.pack(">I", 6), "RDRAM"),
                ])
            elif item.item == 0x0023:
                # Invincibility Candy
                writes.extend([(K64_INVINCIBILITY_CANDY, [1], "RDRAM")])
            elif item.item == 0x0024:
                # Small Star
                writes.extend([
                    (K64_STAR_COUNT, int.to_bytes(int.from_bytes(star_count, "big") + 1, 4, "big"), "RDRAM"),
                ])
            elif item.item in (0x0025, 0x0026, 0x0027, 0x0028):
                # Food
                new_health = min(int(struct.unpack(">f", health)[0]) + 1, 6)
                writes.extend([
                    (K64_KIRBY_HEALTH, struct.pack(">f", new_health), "RDRAM"),
                    (K64_KIRBY_HEALTH_VISUAL, struct.pack(">I", new_health), "RDRAM"),
                ])

        # update crystals here
        if ctx.ui:
            await self.update_crystal_label(ctx)

        # update data storage
        if game_state_val == 0xC:
            # We are on a world menu, update to that world
            world_str = f"{int.from_bytes(menu_level, 'big')}_S"
            if ctx.stored_data.get(self.current_level_storage_key, "") != world_str:
                await ctx.send_msgs([
                    {
                        "cmd": "Set",
                        "key": self.current_level_storage_key,
                        "default": "0_S",
                        "want_reply": False,
                        "operations": [
                            {"operation": "replace", "value": world_str}
                        ]
                    }
                ])
        elif game_state_val == 0xF:
            # We are in a stage, update to that stage
            stage_str = f"{int.from_bytes(current_level, 'big')}_{int.from_bytes(current_stage, 'big')}"
            if ctx.stored_data.get(self.current_level_storage_key, "") != stage_str:
                await ctx.send_msgs([
                    {
                        "cmd": "Set",
                        "key": self.current_level_storage_key,
                        "default": "0_S",
                        "want_reply": False,
                        "operations": [
                            {"operation": "replace", "value": stage_str}
                        ]
                    }
                ])

        new_checks = []

        for i, crystal in zip(range(6), boss_crystals):
            # purposely leave out the last two
            loc_id = i + 0x0200
            if loc_id not in ctx.checked_locations and crystal != 0x00:
                new_checks.append(loc_id)

        # check stages
        for level, stage_num in zip(range(1, 7), (3, 4, 4, 4, 4, 3)):
            for stage in range(stage_num):
                loc_id = self.levels[level][stage]
                if loc_id not in ctx.checked_locations and stage_array[stage_to_byte[level][stage]] == 0x02:
                    new_checks.append(loc_id)
                elif loc_id in ctx.checked_locations:
                    writes.append((K64_STAGE_STATUSES + stage_to_byte[level][stage], [2], "RDRAM"))

        # check crystals
        for level, stage_num in zip(range(6), (3, 4, 4, 4, 4, 3)):
            level_crystals = struct.unpack("I", crystal_array[level*4:(level*4)+4])[0]
            for stage in range(stage_num):
                shifter = (stage * 8)
                current_crystal = 0x0101 + (((default_levels[level + 1][stage] & 0xFF) - 1) * 3)
                for i in range(3):
                    if level_crystals & (1 << shifter) and current_crystal not in ctx.checked_locations:
                        new_checks.append(current_crystal)
                    shifter += 1
                    current_crystal += 1

        # check consumables
        for location in ctx.missing_locations:
            if location in consumables:
                idx, shift = consumables[location]
                check_val = int.from_bytes(consumable_checks[idx: idx + 8])
                if check_val & shift:
                    new_checks.append(location)


        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_slot(new_check_id)
            k64_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
        await ctx.check_locations(new_checks)

        await write(ctx.bizhawk_ctx, writes)
