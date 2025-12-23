from time import time
from typing import TYPE_CHECKING

from CommonClient import logger
from NetUtils import ClientStatus
from worlds.rac3 import RAC3OPTION
from worlds.rac3.client.message import ClientMessage
from worlds.rac3.client.texthelper import get_rich_item_name
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME
from worlds.rac3.constants.messages.text_color import RAC3TEXTCOLOR
from worlds.rac3.constants.region import RAC3REGION

##################################################
# Only change point: Change filename/Class name  #
##################################################
if TYPE_CHECKING:
    from worlds.rac3.client.client import Rac3Context as Context


##################################################
# Only change point: Change filename/Class name  #
##################################################

# common functions
async def update(ctx: 'Context') -> None:
    """Called continuously"""
    ctx.game_interface.early_update()
    # Check received items
    await handle_received_items(ctx)
    # Check collected locations
    await handle_checked_locations(ctx)
    # Check player dead or not
    await handle_deathlink(ctx)
    # Check goal is checked or not
    await handle_check_goal(ctx)
    # Check planet id
    await handle_planet_changed(ctx)
    # Check player respawn
    await handle_respawn(ctx, False)
    ctx.game_interface.late_update()

    # logger.info(f"Update is called")


async def init(ctx: 'Context') -> None:
    """Called when the player connects to the AP server"""
    ctx.game_interface.init()


async def handle_planet_changed(ctx: 'Context') -> None:
    """Checks if the player is going to a different planet"""
    if ctx.slot_data is None:
        return
    planet = ctx.current_planet
    ctx.current_planet, _map = ctx.game_interface.map_switch()
    if planet is not ctx.current_planet:

        if ctx.current_planet == RAC3REGION.TYHRRANOSIS:
            ctx.game_interface.tyhrranosis_fix()

        await ctx.send_msgs([ClientMessage.set_map(ctx.slot, ctx.team, _map)])


async def handle_received_items(ctx: 'Context') -> None:
    """
    共通的なアイテム受信処理。
    """
    if ctx.slot_data is None:
        return

    # 初回だけ記録用に items_received の長さを記憶しておく
    for item in ctx.items_received[ctx.processed_item_count:]:
        ctx.game_interface.item_received(item.item, ctx.player_names[ctx.slot], ctx.player_names[item.player],
                                         item.location)
        # logger.info(f"Received item: ({item_id})")

    if ctx.processed_item_count != len(ctx.items_received):
        logger.debug(f'Update Data Package to {len(ctx.items_received)}')
        ctx.stored_data[RAC3OPTION.PROCESSED_LOCATIONS] = len(ctx.items_received)
        ctx.processed_item_count = len(ctx.items_received)
        await ctx.send_msgs([ClientMessage.set_processed(ctx.processed_item_count)])


async def handle_checked_locations(ctx: 'Context') -> None:
    """
    共通的なロケーションチェック処理。
    """
    if ctx.slot_data is None:
        return

    # logger.info(f"{ctx.server_locations}")
    new_checks = []
    for ap_code in ctx.server_locations:
        if ap_code in ctx.checked_locations:
            continue
        if ctx.game_interface.is_location_checked(ap_code):
            new_checks.append(ap_code)

    if new_checks:
        real_checks = list(await ctx.check_locations(new_checks))
        ctx.locations_checked.update(real_checks)
        for location in real_checks:
            net_item = ctx.locations_info.get(location, None)
            if net_item is not None and net_item.player != ctx.slot:
                item_to_player_names = get_rich_item_name(ctx, net_item, True)
                ctx.game_interface.notification_queue.append((f'{item_to_player_names}', RAC3BOXTHEME.DEFAULT))

    # else:
    #     logger.info("Not found new location")


async def handle_deathlink(ctx: 'Context') -> None:
    """Receive and send deathlink"""
    if not ctx.death_link:
        return
    ctx.game_interface.reload_check()
    if time() - ctx.last_death_link > 10:
        alive, message = ctx.game_interface.alive()
        if alive:
            if ctx.queued_deaths > 0:
                logger.debug(f'Deaths requires processing: {ctx.queued_deaths}')
                if ctx.game_interface.kill_player():
                    ctx.game_interface.notification_queue.append(
                        (f'{RAC3TEXTCOLOR.WHITE}Deathlink Received from {RAC3TEXTCOLOR.GREEN}'
                         f'{ctx.last_deathlink_sender}{RAC3TEXTCOLOR.WHITE}:\\n{ctx.last_deathlink_msg}',
                         RAC3BOXTHEME.DEATHLINK))
                    logger.debug(f'Deaths processed')
                    ctx.queued_deaths = 0
                    ctx.last_death_link = time()
        else:
            logger.debug(f'Sending Death, queue: {ctx.queued_deaths}')
            ctx.game_interface.notification_queue.append((f'{RAC3TEXTCOLOR.WHITE}Sending Deathlink:\\n{message}',
                                                          RAC3BOXTHEME.DEATHLINK))
            await ctx.send_death(message)
            logger.debug(f'Sent Death, queue: {ctx.queued_deaths}')


async def handle_respawn(ctx: 'Context', skip_inputs: bool = False) -> bool:
    """Check if the player should respawn"""
    if ctx.game_interface.is_reloading:
        return False
    if ctx.death_link and ctx.game_interface.action not in {0, 1, 2, 3, 4, 0x13, 0x1D, 0x2E, 0x32, 0x33, 0x34, 0x37,
                                                            0x3F, 0x40, 0x4D, 0x51, 0x52, 0x59, 0x5B, 0x5C, 0x61,
                                                            0x62, 0x75, 0x76, 0x7C, 0x80, 0x9A, 0x9B, 0x9D, 0xA3}:
        return False  # Todo: Action states
    planet_data = RAC3_REGION_DATA_TABLE[ctx.game_interface.planet]
    if planet_data.ID > 55:
        return False
    if planet_data.PAUSE_ADDRESS is not None:  # Vid comics do not have a pause address
        if ctx.game_interface.respawn_inputs() or skip_inputs:
            ctx.game_interface.unpause_game()
            ctx.game_interface.teleport_to_ship()
            return True
    return False


async def handle_check_goal(ctx: 'Context') -> None:
    """Checks if the goal is completed"""
    if ctx.slot_data is None:
        return

    victory_code = ctx.game_interface.get_victory_code()
    if victory_code in ctx.checked_locations:
        ctx.finished_game = True
        await ctx.send_msgs([ClientMessage.status_update(ClientStatus.CLIENT_GOAL)])
