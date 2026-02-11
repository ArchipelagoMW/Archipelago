"""This module contains functions related to the game client"""
from asyncio import sleep
from time import time
from traceback import format_exc
from typing import TYPE_CHECKING

from CommonClient import logger
from NetUtils import ClientStatus
from worlds.rac3.client.message import ClientMessage
from worlds.rac3.client.texthelper import get_sent_item_message
from worlds.rac3.constants.data.location import RAC3_LOCATION_DATA_TABLE
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.input import RAC3INPUT
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME
from worlds.rac3.constants.messages.text_strings import RAC3TEXTFORMATSTRING
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.region import RAC3REGION

##################################################
# Only change point: Change filename/Class name  #
##################################################
if TYPE_CHECKING:
    from worlds.rac3.client.client import Rac3Context as Context


async def pcsx2_sync_task(ctx: 'Context'):
    """Connects to PCSX2 and loops through update functions until the connection is closed."""
    logger.info(f"Starting {RAC3OPTION.GAME_TITLE_FULL} Connector")
    version_dots = RAC3OPTION.VERSION_NUMBER.count(".")
    if version_dots >= 3:
        logger.warning("\nYou are using a development build of the RaC3 Archipelago Randomizer!\n"
                        "There may be bugs present that have not been tested fully.\n"
                        "These builds are meant for testing and bug reporting purposes "
                        "and should not be used for normal play!\n")
    connected_to_game: bool = False
    connection_retry_attempts: int = 0
    while not ctx.exit_event.is_set():
        try:
            connected_to_server = (ctx.server is not None) and (ctx.slot is not None)
            if connected_to_server and not ctx.is_connected_to_server:
                logger.info("Connected to server")
                ctx.is_connected_to_server = connected_to_server
                if ctx.slot_data.get(RAC3OPTION.VERSION, "0.0.0") < RAC3OPTION.VERSION_NUMBER:
                    await ctx.disconnect()
                    logger.warning(
                        f"Client is v{RAC3OPTION.VERSION_NUMBER}, please downgrade to v"
                        f"{ctx.slot_data[RAC3OPTION.VERSION]}")
                    await sleep(10)
                    continue
                if ctx.slot_data[RAC3OPTION.VERSION] > RAC3OPTION.VERSION_NUMBER:
                    await ctx.disconnect()
                    logger.warning(
                        f"Client is v{RAC3OPTION.VERSION_NUMBER}, please upgrade to v"
                        f"{ctx.slot_data[RAC3OPTION.VERSION]}")
                    await sleep(10)
                    continue
                if connected_to_game:
                    ctx.game_interface.init()
                else:
                    logger.info("Waiting for game connection...")

            connected_to_game = ctx.game_interface.get_connection_state()
            if connected_to_game and not ctx.is_connected_to_game:
                logger.info(f"Connected to {RAC3OPTION.GAME_TITLE_FULL}")
                ctx.last_pine_message = None
                ctx.is_connected_to_game = connected_to_game
                if connected_to_server:
                    ctx.game_interface.init()
                else:
                    logger.info("Waiting for server connection...")

            if not connected_to_game and not ctx.game_interface.is_connecting:
                if ctx.is_connected_to_game:
                    ctx.game_interface.disconnect_from_game()
                    logger.info("Connection to game lost")
                elif ctx.last_pine_message is None:
                    message = "Not connected to the PCSX2 instance"
                    logger.info(message)
                    ctx.last_pine_message = message
                ctx.game_interface.connect_to_game()
                if not ctx.game_interface.get_connection_state():
                    if connection_retry_attempts < 3:
                        connection_retry_attempts += 1

                    retry_wait = connection_retry_attempts * 10
                    logger.warning(
                        f'Could not connect to RaC3! Will retry connection in {retry_wait} seconds...\nPlease check '
                        f'your PINE settings both global and game specific, and restart PCSX2 if you changed them.')
                    await sleep(retry_wait)
                else:
                    connection_retry_attempts = 0

            if not connected_to_server:
                if ctx.server:
                    ctx.last_server_message = None
                elif ctx.last_server_message is None:
                    message = "Waiting for player to connect to server"
                    logger.info(message)
                    ctx.last_server_message = message

            if connected_to_game and connected_to_server:
                await _handle_game_ready(ctx)

        except ConnectionError:
            logger.info(f"ConnectionError")
            ctx.game_interface.disconnect_from_game()
        except Exception as e:
            logger.info(f"ExceptionError")
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(format_exc())
            # await sleep(3)

        await sleep(0.5)
    logger.info(f"{RAC3OPTION.GAME_TITLE_FULL} Client Shutdown")


async def _handle_game_ready(ctx: 'Context') -> None:
    # Quite a lot of stuff ended up in this function, even though it might
    # have fit better in init(). It just didn't work when I put it there,
    # probably because of when the game loads stuff.

    if ctx.slot_data is not None:
        # Check if exit to main menu
        menu = ctx.main_menu
        ctx.main_menu = ctx.game_interface.check_main_menu()

        if ctx.main_menu:
            if menu:
                ctx.game_interface.main_menu = True
            if ctx.last_game_message is None:
                message = "Currently on Main Menu, please load a file..."
                logger.info(message)
                ctx.last_game_message = message
            await sleep(5)

        if menu is True and ctx.main_menu is False:
            await ctx.send_msgs([ClientMessage.status_update(ClientStatus.CLIENT_PLAYING)])
            logger.info("Starting game...")
            ctx.game_interface.reset_file()
            logger.info("Old state removed!")
            logger.info("Checking for items...")
            logger.debug(f"Data Package: {ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, 'Empty')}")
            logger.info(f"Items Received: {len(ctx.items_received)}")
            items_to_process = ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, len(ctx.items_received))
            counter = 0
            for count, item in enumerate(ctx.items_received):
                counter += 1
                logger.debug(f"Processing item {count}: {ctx.item_names.lookup_in_slot(item.item, item.player)}")
                if count > items_to_process:
                    logger.debug(f"Handle Later")
                    continue
                ctx.game_interface.important_items(item.item, ctx.player_names[ctx.slot], item.location)
            ctx.processed_item_count = min(counter, items_to_process)
            await ctx.send_msgs([ClientMessage.set_processed(ctx.processed_item_count)])
            logger.info(f"Items Processed: {ctx.processed_item_count}")
            logger.info("Checking locations...")
            counter = 0
            for loc in ctx.checked_locations:
                logger.debug(f"Collecting location: {ctx.location_names.lookup_in_slot(loc, ctx.slot)}")
                ctx.game_interface.collect_location(ctx.location_names.lookup_in_slot(loc, ctx.slot))
                counter += 1
            logger.info(f"Locations collected: {counter}")
            ctx.game_interface.fix_health()
            ctx.game_interface.reset_death_count()
            logger.info("Checking cosmetics...")
            ctx.game_interface.add_cosmetics()
            logger.info("Load the latest autosave or enter the Armor Vendor to apply cosmetics")
            logger.info("Game READY!")

        if not ctx.main_menu:
            await update(ctx)
            logger.debug(f"Data Package: {ctx.stored_data.get(RAC3OPTION.PROCESSED_LOCATIONS, 'Empty')}")


##################################################
# Only change point: Change filename/Class name  #
##################################################


# common functions
async def update(ctx: 'Context') -> None:
    """Called continuously"""
    ctx.game_interface.early_update()
    await handle_intro_skip(ctx)
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
    await handle_respawn(ctx)
    # Check sequence breaks
    await handle_sequence_break(ctx)
    ctx.game_interface.late_update()

    # logger.info(f"Update is called")


async def handle_intro_skip(ctx: 'Context') -> None:
    """Checks if the intro skip option is enabled, then skips veldin and sets required story/mission flags"""
    if ctx.slot_data is None:
        return
    if (ctx.slot_data.get(RAC3OPTION.INTRO_SKIP, False)
            and ctx.current_planet == RAC3REGION.VELDIN and not ctx.game_interface.homewarping):
        locations = []
        for ap_code in [ap_code for ap_code in ctx.missing_locations if
                        RAC3_LOCATION_DATA_TABLE[ctx.location_names.lookup_in_slot(ap_code, ctx.slot)].REGION
                        == RAC3REGION.VELDIN]:
            ctx.game_interface.collect_location(ctx.location_names.lookup_in_slot(ap_code, ctx.slot))
            ctx.locations_checked.update([ap_code])
            locations.append(ap_code)
        ctx.locations_checked.update(await ctx.check_locations(locations))
        ctx.game_interface.homewarp()


async def handle_received_items(ctx: 'Context') -> None:
    """Process items received from the AP server"""
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
    """Check for new locations collected, send these to the AP server"""
    if ctx.slot_data is None:
        return

    # logger.info(f"{ctx.server_locations}")
    new_checks = []
    for ap_code in ctx.server_locations:
        if ap_code in ctx.checked_locations | ctx.locations_checked:
            continue
        if ctx.game_interface.is_location_checked(ap_code):
            new_checks.append(ap_code)

    if new_checks:
        real_checks = list(await ctx.check_locations(new_checks))
        ctx.locations_checked.update(real_checks)
        for location in real_checks:
            net_item = ctx.locations_info.get(location, None)
            if net_item is not None and net_item.player != ctx.slot:
                item_to_player_names = get_sent_item_message(ctx, net_item, True)
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
                        (f'{RAC3TEXTFORMATSTRING.WHITE}Deathlink Received from {RAC3TEXTFORMATSTRING.GREEN}'
                         f'{ctx.last_deathlink_sender}{RAC3TEXTFORMATSTRING.WHITE}:\\n{ctx.last_deathlink_msg}',
                         RAC3BOXTHEME.DEATHLINK))
                    logger.debug(f'Deaths processed')
                    ctx.queued_deaths = 0
                    ctx.last_death_link = time()
        else:
            logger.debug(f'Sending Death, queue: {ctx.queued_deaths}')
            ctx.game_interface.notification_queue.append((f'{RAC3TEXTFORMATSTRING.WHITE}Sending Deathlink:\\n{message}',
                                                          RAC3BOXTHEME.DEATHLINK))
            await ctx.send_death(message)
            logger.debug(f'Sent Death, queue: {ctx.queued_deaths}')


async def handle_check_goal(ctx: 'Context') -> None:
    """Checks if the goal is completed"""
    if ctx.slot_data is None:
        return

    victory_code = ctx.game_interface.get_victory_code()
    if victory_code in ctx.checked_locations:
        ctx.finished_game = True
        await ctx.send_msgs([ClientMessage.status_update(ClientStatus.CLIENT_GOAL)])


async def handle_planet_changed(ctx: 'Context') -> None:
    """Checks if the player is changing planet"""
    if ctx.slot_data is None:
        return
    last_planet = ctx.current_planet
    ctx.current_planet, _map = ctx.game_interface.map_switch()
    if last_planet is not ctx.current_planet:

        if ctx.current_planet == RAC3REGION.TYHRRANOSIS:
            ctx.game_interface.tyhrranosis_fix()

        ctx.game_interface.softlock_warning()

        await ctx.send_msgs([ClientMessage.set_map(ctx.slot, ctx.team, _map)])


async def handle_respawn(ctx: 'Context', force_respawn: bool = False, force_load: bool = False):
    """Check if the player should respawn"""
    if ctx.game_interface.is_reloading:
        return
    if ctx.death_link and ctx.game_interface.action not in {0, 1, 2, 3, 4, 0x13, 0x1D, 0x2E, 0x32, 0x33, 0x34, 0x37,
                                                            0x3F, 0x40, 0x4D, 0x51, 0x52, 0x59, 0x5B, 0x5C, 0x61,
                                                            0x62, 0x75, 0x76, 0x7C, 0x80, 0x9A, 0x9B, 0x9D, 0xA3}:
        if force_load:
            logger.error(f'Player cannot homewarp right now')
        elif force_respawn:
            logger.error(f'Player cannot respawn right now')
        return  # Todo: Action states
    planet_data = RAC3_REGION_DATA_TABLE[ctx.game_interface.planet]
    if planet_data.ID > 55:
        return
    if planet_data.PAUSE_ADDRESS is not None:  # Vid comics do not have a pause address
        if ctx.game_interface.check_inputs(RAC3INPUT.SQUARE, True) or force_respawn:
            ctx.game_interface.unpause_game()
            ctx.game_interface.teleport_to_ship()
            return
        if ctx.game_interface.check_intro():
            if force_load:
                logger.error(f'Player cannot homewarp right now')
            elif force_respawn:
                logger.error(f'Player cannot respawn right now')
            return
        if ctx.game_interface.check_inputs(RAC3INPUT.RELOAD, True) or force_load:
            ctx.game_interface.unpause_game()
            ctx.game_interface.homewarp()
            return
    if ctx.game_interface.check_inputs(RAC3INPUT.RELOAD) or force_load:
        ctx.game_interface.homewarp()
        return
    return


async def handle_sequence_break(ctx: 'Context') -> None:
    """Undoes the flags for infobot locations when sequence breaking if you haven't checked the corresponding location
    yet"""
    if ctx.slot_data is None:
        return
    ctx.game_interface.sequence_break()
