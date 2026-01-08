from time import time
from typing import TYPE_CHECKING

from CommonClient import logger
from NetUtils import ClientStatus

##################################################
# Only change point: Change filename/Class name  #
##################################################
if TYPE_CHECKING:
    from .Rac3Client import Rac3Context as Context


##################################################
# Only change point: Change filename/Class name  #
##################################################

# common functions
async def update(ctx: 'Context', ap_connected: bool) -> None:
    """Called continuously"""

    # Quite a lot of stuff ended up in this function, even though it might
    # have fit better in init(). It just didn't work when I put it there,
    # probably because of when the game loads stuff.

    if ap_connected and ctx.slot_data is not None:
        # Check if exit to main menu
        menu = ctx.main_menu
        await handle_main_menu(ctx)

        if menu is True and ctx.main_menu is False:
            logger.info("Updating game...")
            ctx.game_interface.file_load(ctx.checked_locations)
            logger.info("Game State Updated!")

        if not ctx.main_menu:
            # Check received items
            await handle_received_items(ctx)
            # Check collected locations
            await handle_checked_locations(ctx)
            # Check goal is checked or not
            await handle_check_goal(ctx)
            # Check planet id
            await handle_planet_changed(ctx)

            ctx.game_interface.update()

            # logger.info(f"Update is called")


async def init(ctx: 'Context', ap_connected: bool) -> None:
    """Called when the player connects to the AP server or enters a new episode"""
    if ap_connected:
        # Initialize all date
        ctx.game_interface.init()
        pass


async def handle_planet_changed(ctx: 'Context') -> None:
    if ctx.slot_data is None:
        return
    planet = ctx.current_planet
    ctx.current_planet = ctx.game_interface.map_switch()
    if planet is not ctx.current_planet:

        if ctx.current_planet == "Tyhrranosis":
            ctx.game_interface.tyhrranosis_fix()

        await ctx.send_msgs([{"cmd": 'Set',
                              "key": f'rac3_current_planet_{ctx.slot}_{ctx.team}',
                              "default": "Starship Phoenix",
                              "want_reply": False,
                              "operations": [{
                                  "operation": 'replace',
                                  "value": ctx.current_planet}]
                              }])


async def handle_received_items(ctx: 'Context') -> None:
    """
    共通的なアイテム受信処理。
    """
    if ctx.slot_data is None:
        return

    # 初回だけ記録用に items_received の長さを記憶しておく
    if not hasattr(ctx, "processed_item_count"):
        ctx.processed_item_count = -1
        new_items = ctx.items_received[0:]
    else:
        new_items = ctx.items_received[ctx.processed_item_count:]

    for index, item in enumerate(new_items):
        item_id = item.item
        ctx.game_interface.item_received(item_id, ctx.processed_item_count)
        # logger.info(f"Received item: ({item_id})")

    ctx.processed_item_count = len(ctx.items_received)


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
        if ctx.game_interface.is_location_checked(ap_code) is True:
            new_checks.append(ap_code)

    if new_checks:
        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": new_checks}])
        ctx.locations_checked.update(new_checks)
    # else:
    #     logger.info("Not found new location")


async def handle_deathlink(ctx: 'Context') -> None:
    """Receive and send deathlink"""
    if not ctx.death_link_enabled:
        return

    if time() - ctx.deathlink_timestamp > 10:
        if ctx.game_interface.alive():
            if ctx.queued_deaths > 0:
                ctx.game_interface.kill_player()
                ctx.queued_deaths -= 1
                ctx.deathlink_timestamp = time()
        else:
            # Maybe add something that writes a cause?
            await ctx.send_death()
            ctx.deathlink_timestamp = time()


async def handle_check_goal(ctx: 'Context') -> None:
    """Checks if the goal is completed"""
    if ctx.slot_data is None:
        return

    victory_code = ctx.game_interface.get_victory_code()
    if victory_code in ctx.checked_locations:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def handle_main_menu(ctx: 'Context') -> None:
    """Checks if the player has exited to the main menu"""
    if ctx.slot_data is None:
        return

    ctx.main_menu = ctx.game_interface.check_main_menu()
