import logging
import struct
import time
import typing
import uuid
from struct import unpack, pack
from collections import defaultdict
import random

from MultiServer import mark_raw
from NetUtils import ClientStatus, color
from Utils import async_start
from worlds.AutoSNIClient import SNIClient
from .locations import boss_locations
from .gifting import kdl3_gifting_options, kdl3_trap_gifts, kdl3_gifts, update_object, pop_object, initialize_giftboxes
from .client_addrs import consumable_addrs, star_addrs
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SNIClient import SNIClientCommandProcessor, SNIContext

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
SRAM_1_START = 0xE00000

# KDL3
KDL3_HALKEN = SRAM_1_START + 0x80F0
KDL3_NINTEN = SRAM_1_START + 0x8FF0
KDL3_ROMNAME = SRAM_1_START + 0x8100
KDL3_DEATH_LINK_ADDR = SRAM_1_START + 0x9010
KDL3_GOAL_ADDR = SRAM_1_START + 0x9012
KDL3_CONSUMABLE_FLAG = SRAM_1_START + 0x9018
KDL3_STARS_FLAG = SRAM_1_START + 0x901A
KDL3_GIFTING_FLAG = SRAM_1_START + 0x901C
KDL3_LEVEL_ADDR = SRAM_1_START + 0x9020
KDL3_IS_DEMO = SRAM_1_START + 0x5AD5
KDL3_GAME_SAVE = SRAM_1_START + 0x3617
KDL3_CURRENT_WORLD = SRAM_1_START + 0x363F
KDL3_CURRENT_LEVEL = SRAM_1_START + 0x3641
KDL3_GAME_STATE = SRAM_1_START + 0x36D0
KDL3_LIFE_COUNT = SRAM_1_START + 0x39CF
KDL3_KIRBY_HP = SRAM_1_START + 0x39D1
KDL3_BOSS_HP = SRAM_1_START + 0x39D5
KDL3_STAR_COUNT = SRAM_1_START + 0x39D7
KDL3_LIFE_VISUAL = SRAM_1_START + 0x39E3
KDL3_HEART_STARS = SRAM_1_START + 0x53A7
KDL3_WORLD_UNLOCK = SRAM_1_START + 0x53CB
KDL3_LEVEL_UNLOCK = SRAM_1_START + 0x53CD
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
KDL3_GIFTING_SEND = SRAM_1_START + 0x8086
KDL3_COMPLETED_STAGES = SRAM_1_START + 0x8200
KDL3_CONSUMABLES = SRAM_1_START + 0xA000
KDL3_STARS = SRAM_1_START + 0xB000
KDL3_ITEM_QUEUE = SRAM_1_START + 0xC000

deathlink_messages = defaultdict(lambda: " was defeated.", {
    0x0200: " was bonked by apples from Whispy Woods.",
    0x0201: " was out-maneuvered by Acro.",
    0x0202: " was out-numbered by Pon & Con.",
    0x0203: " was defeated by Ado's powerful paintings.",
    0x0204: " was clobbered by King Dedede.",
    0x0205: " lost their battle against Dark Matter.",
    0x0300: " couldn't overcome the Boss Butch.",
    0x0400: " is bad at jumping.",
})


@mark_raw
def cmd_gift(self: "SNIClientCommandProcessor") -> None:
    """Toggles gifting for the current game."""
    handler = self.ctx.client_handler
    assert isinstance(handler, KDL3SNIClient)
    handler.gifting = not handler.gifting
    self.output(f"Gifting set to {handler.gifting}")
    async_start(update_object(self.ctx, f"Giftboxes;{self.ctx.team}", {
        f"{self.ctx.slot}":
            {
                "IsOpen": handler.gifting,
                **kdl3_gifting_options
            }
    }))


class KDL3SNIClient(SNIClient):
    game = "Kirby's Dream Land 3"
    patch_suffix = ".apkdl3"
    levels: typing.Dict[int, typing.List[int]] = {}
    consumables: typing.Optional[bool] = None
    stars: typing.Optional[bool] = None
    item_queue: typing.List[int] = []
    initialize_gifting: bool = False
    gifting: bool = False
    giftbox_key: str = ""
    motherbox_key: str = ""
    client_random: random.Random = random.Random()

    async def deathlink_kill_player(self, ctx: "SNIContext") -> None:
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

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from SNIClient import snes_read
        rom_name = await snes_read(ctx, KDL3_ROMNAME, 0x15)
        if rom_name is None or rom_name == bytes([0] * 0x15) or rom_name[:4] != b"KDL3":
            if "gift" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("gift")
            return False

        ctx.game = self.game
        ctx.rom = rom_name
        ctx.items_handling = 0b101  # default local items with remote start inventory
        ctx.allow_collect = True
        if "gift" not in ctx.command_processor.commands:
            ctx.command_processor.commands["gift"] = cmd_gift

        death_link = await snes_read(ctx, KDL3_DEATH_LINK_ADDR, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))
            ctx.items_handling |= (death_link[0] & 0b10)  # set local items if enabled
        return True

    async def pop_item(self, ctx: "SNIContext", in_stage: bool) -> None:
        from SNIClient import snes_buffered_write, snes_read
        if len(self.item_queue) > 0:
            item = self.item_queue.pop()
            if not in_stage and item & 0xC0:
                # can't handle this item right now, send it to the back and return to handle the rest
                self.item_queue.append(item)
                return
            ingame_queue = list(unpack("HHHHHHHH", await snes_read(ctx, KDL3_ITEM_QUEUE, 16)))
            for i in range(len(ingame_queue)):
                if ingame_queue[i] == 0x00:
                    ingame_queue[i] = item
                    snes_buffered_write(ctx, KDL3_ITEM_QUEUE, pack("HHHHHHHH", *ingame_queue))
                    break
            else:
                self.item_queue.append(item)  # no more slots, get it next go around

    async def pop_gift(self, ctx: "SNIContext") -> None:
        if self.giftbox_key in ctx.stored_data and ctx.stored_data[self.giftbox_key]:
            from SNIClient import snes_read, snes_buffered_write
            key, gift = ctx.stored_data[self.giftbox_key].popitem()
            await pop_object(ctx, self.giftbox_key, key)
            # first, special cases
            traits = [trait["Trait"] for trait in gift["Traits"]]
            if "Candy" in traits or "Invincible" in traits:
                # apply invincibility candy
                self.item_queue.append(0x43)
            elif "Tomato" in traits or "tomato" in gift["ItemName"].lower():
                # apply maxim tomato
                # only want tomatos here, no other vegetable is that good
                self.item_queue.append(0x42)
            elif "Life" in traits:
                # Apply 1-Up
                self.item_queue.append(0x41)
            elif "Currency" in traits or "Star" in traits:
                value = gift["ItemValue"]
                if value >= 50000:
                    self.item_queue.append(0x46)
                elif value >= 30000:
                    self.item_queue.append(0x45)
                else:
                    self.item_queue.append(0x44)
            elif "Trap" in traits:
                # find the best trap to apply
                if "Goo" in traits or "Gel" in traits:
                    self.item_queue.append(0x80)
                elif "Slow" in traits or "Slowness" in traits:
                    self.item_queue.append(0x81)
                elif "Eject" in traits or "Removal" in traits:
                    self.item_queue.append(0x82)
                else:
                    # just deal damage to Kirby
                    kirby_hp = struct.unpack("H", await snes_read(ctx, KDL3_KIRBY_HP, 2))[0]
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, struct.pack("H", max(kirby_hp - 1, 0)))
            else:
                # check if it's tasty
                if any(x in traits for x in ["Consumable", "Food", "Drink", "Heal", "Health"]):
                    # it's tasty!, use quality to decide how much to heal
                    quality = max((trait["Quality"] for trait in gift["Traits"]
                                   if trait["Trait"] in ["Consumable", "Food", "Drink", "Heal", "Health"]))
                    quality = min(10, quality * 2)
                else:
                    # it's not really edible, but he'll eat it anyway
                    quality = self.client_random.choices(range(0, 2), [75, 25])[0]
                kirby_hp = await snes_read(ctx, KDL3_KIRBY_HP, 1)
                gooey_hp = await snes_read(ctx, KDL3_KIRBY_HP + 2, 1)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x26]))
                if gooey_hp[0] > 0x00:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, struct.pack("H", min(kirby_hp[0] + quality // 2, 8)))
                    snes_buffered_write(ctx, KDL3_KIRBY_HP + 2, struct.pack("H", min(gooey_hp[0] + quality // 2, 8)))
                else:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, struct.pack("H", min(kirby_hp[0] + quality, 10)))

    async def pick_gift_recipient(self, ctx: "SNIContext", gift: int) -> None:
        assert ctx.slot
        if gift != 4:
            gift_base = kdl3_gifts[gift]
        else:
            gift_base = kdl3_trap_gifts[self.client_random.randint(0, 3)]
        most_applicable = -1
        most_applicable_slot = ctx.slot
        for slot, info in ctx.stored_data[self.motherbox_key].items():
            if int(slot) == ctx.slot and len(ctx.stored_data[self.motherbox_key]) > 1:
                continue
            desire = len(set(info["DesiredTraits"]).intersection([trait["Trait"] for trait in gift_base["Traits"]]))
            if desire > most_applicable:
                most_applicable = desire
                most_applicable_slot = int(slot)
            elif most_applicable_slot != ctx.slot and most_applicable == -1 and info["AcceptsAnyGift"]:
                # only send to ourselves if no one else will take it
                most_applicable_slot = int(slot)
        # print(most_applicable, most_applicable_slot)
        item_uuid = uuid.uuid4().hex
        item = {
            **gift_base,
            "ID": item_uuid,
            "Sender": ctx.player_names[ctx.slot],
            "Receiver": ctx.player_names[most_applicable_slot],
            "SenderTeam": ctx.team,
            "ReceiverTeam": ctx.team,  # for the moment
            "IsRefund": False
        }
        # print(item)
        await update_object(ctx, f"Giftbox;{ctx.team};{most_applicable_slot}", {
            item_uuid: item,
        })

    async def game_watcher(self, ctx: "SNIContext") -> None:
        try:
            from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
            rom = await snes_read(ctx, KDL3_ROMNAME, 0x15)
            if rom != ctx.rom:
                ctx.rom = None
            halken = await snes_read(ctx, KDL3_HALKEN, 6)
            if halken != b"halken":
                return
            ninten = await snes_read(ctx, KDL3_NINTEN, 6)
            if ninten != b"ninten":
                return
            if not ctx.slot:
                return
            if not self.initialize_gifting:
                self.giftbox_key = f"Giftbox;{ctx.team};{ctx.slot}"
                self.motherbox_key = f"Giftboxes;{ctx.team}"
                enable_gifting = await snes_read(ctx, KDL3_GIFTING_FLAG, 0x01)
                await initialize_giftboxes(ctx, self.giftbox_key, self.motherbox_key, bool(enable_gifting[0]))
                self.initialize_gifting = True
            # can't check debug anymore, without going and copying the value. might be important later.
            if not self.levels:
                self.levels = dict()
                for i in range(5):
                    level_data = await snes_read(ctx, KDL3_LEVEL_ADDR + (14 * i), 14)
                    self.levels[i] = [int.from_bytes(level_data[idx:idx+1], "little")
                                      for idx in range(0, len(level_data), 2)]
                self.levels[5] = [0x0205,  # Hyper Zone
                                  0,  # MG-5, can't send from here
                                  0x0300,  # Boss Butch
                                  0x0400,  # Jumping
                                  0, 0, 0]

            if self.consumables is None:
                consumables = await snes_read(ctx, KDL3_CONSUMABLE_FLAG, 1)
                self.consumables = consumables[0] == 0x01
            if self.stars is None:
                stars = await snes_read(ctx, KDL3_STARS_FLAG, 1)
                self.stars = stars[0] == 0x01
            is_demo = await snes_read(ctx, KDL3_IS_DEMO, 1)
            # 1 - recording a demo, 2 - playing back recorded, 3+ is a demo
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
            if "DeathLink" in ctx.tags and game_state[0] == 0x00 and ctx.last_death_link + 1 < time.time():
                current_hp = await snes_read(ctx, KDL3_KIRBY_HP, 1)
                current_world = struct.unpack("H", await snes_read(ctx, KDL3_CURRENT_WORLD, 2))[0]
                current_level = struct.unpack("H", await snes_read(ctx, KDL3_CURRENT_LEVEL, 2))[0]
                currently_dead = current_hp[0] == 0x00
                message = deathlink_messages[self.levels[current_world][current_level]]
                await ctx.handle_deathlink_state(currently_dead, f"{ctx.player_names[ctx.slot]}{message}")

            recv_count = await snes_read(ctx, KDL3_RECV_COUNT, 2)
            recv_amount = unpack("H", recv_count)[0]
            if recv_amount < len(ctx.items_received):
                item = ctx.items_received[recv_amount]
                recv_amount += 1
                logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                    color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                    color(ctx.player_names[item.player], 'yellow'),
                    ctx.location_names.lookup_in_slot(item.location, item.player), recv_amount, len(ctx.items_received)))

                snes_buffered_write(ctx, KDL3_RECV_COUNT, pack("H", recv_amount))
                item_idx = item.item & 0x00000F
                if item.item & 0x000070 == 0:
                    self.item_queue.append(item_idx | 0x10)
                elif item.item & 0x000010 > 0:
                    self.item_queue.append(item_idx | 0x20)
                elif item.item & 0x000020 > 0:
                    # Positive
                    self.item_queue.append(item_idx | 0x40)
                elif item.item & 0x000040 > 0:
                    self.item_queue.append(item_idx | 0x80)

            # handle gifts here
            gifting_status = await snes_read(ctx, KDL3_GIFTING_FLAG, 0x01)
            if hasattr(ctx, "gifting") and ctx.gifting:
                if gifting_status[0]:
                    gift = await snes_read(ctx, KDL3_GIFTING_SEND, 0x01)
                    if gift[0]:
                        # we have a gift to send
                        await self.pick_gift_recipient(ctx, gift[0])
                        snes_buffered_write(ctx, KDL3_GIFTING_SEND, bytes([0x00]))
                else:
                    snes_buffered_write(ctx, KDL3_GIFTING_FLAG, bytes([0x01]))
            else:
                if gifting_status[0]:
                    snes_buffered_write(ctx, KDL3_GIFTING_FLAG, bytes([0x00]))

            await snes_flush_writes(ctx)

            new_checks = []
            # level completion status
            world_unlocks = await snes_read(ctx, KDL3_WORLD_UNLOCK, 1)
            if world_unlocks[0] > 0x06:
                return  # save is not loaded, ignore
            stages_raw = await snes_read(ctx, KDL3_COMPLETED_STAGES, 60)
            stages = struct.unpack("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH", stages_raw)
            for i in range(30):
                loc_id = 0x770000 + i
                if stages[i] == 1 and loc_id not in ctx.checked_locations:
                    new_checks.append(loc_id)
                elif loc_id in ctx.checked_locations:
                    snes_buffered_write(ctx, KDL3_COMPLETED_STAGES + (i * 2), struct.pack("H", 1))

            # heart star status
            heart_stars = await snes_read(ctx, KDL3_HEART_STARS, 35)
            for i in range(5):
                start_ind = i * 7
                for j in range(6):
                    level_ind = start_ind + j
                    loc_id = 0x770100 + (6 * i) + j
                    if heart_stars[level_ind] and loc_id not in ctx.checked_locations:
                        new_checks.append(loc_id)
                    elif loc_id in ctx.checked_locations:
                        snes_buffered_write(ctx, KDL3_HEART_STARS + level_ind, bytes([0x01]))
            if self.consumables:
                consumables = await snes_read(ctx, KDL3_CONSUMABLES, 1920)
                for consumable in consumable_addrs:
                    # TODO: see if this can be sped up in any way
                    loc_id = 0x770300 + consumable
                    if loc_id not in ctx.checked_locations and consumables[consumable_addrs[consumable]] == 0x01:
                        new_checks.append(loc_id)
            if self.stars:
                stars = await snes_read(ctx, KDL3_STARS, 1920)
                for star in star_addrs:
                    if star not in ctx.checked_locations and stars[star_addrs[star]] == 0x01:
                        new_checks.append(star)

            if not game_state:
                return

            if game_state[0] != 0xFF:
                await self.pop_gift(ctx)
            await self.pop_item(ctx, game_state[0] != 0xFF)
            await snes_flush_writes(ctx)

            # boss status
            boss_flag_bytes = await snes_read(ctx, KDL3_BOSS_STATUS, 2)
            boss_flag = int.from_bytes(boss_flag_bytes, "little")
            for bitmask, boss in zip(range(1, 11, 2), boss_locations.keys()):
                if boss_flag & (1 << bitmask) > 0 and boss not in ctx.checked_locations:
                    new_checks.append(boss)

            for new_check_id in new_checks:
                ctx.locations_checked.add(new_check_id)
                location = ctx.location_names.lookup_in_game(new_check_id)
                snes_logger.info(
                    f'New Check: {location} ({len(ctx.locations_checked)}/'
                    f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
        except Exception as ex:
            # we crashed, so print log and clean up
            snes_logger.error("", exc_info=ex)
            if "gift" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("gift")
            ctx.rom = None
            ctx.game = None
