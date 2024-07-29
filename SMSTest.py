import dolphin_memory_engine
import asyncio
from CommonClient import ClientCommandProcessor, CommonContext, logger, gui_enabled, server_loop, get_base_parser

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = "Dolphin connection was lost."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."


class SMSCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        if isinstance(self.ctx, SMSContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class SMSContext(CommonContext):
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.dolphin_sync_task = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS

    def run_gui(self):
        from kvui import GameManager

        class SMSManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago SMS Client"

        self.ui = SMSManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def dolphin_sync_task(ctx: SMSContext):
    while not ctx.exit_event.is_set():
        courses = dolphin_memory_engine.read_byte(0x803e970e)

        if courses == 0x00:
            # Set events on Delfino Plaza while we are in Airstrip
            # Delfino plaza events 0x805789f8, 0x805789f9
            # Cutscenes viewed 0x805789fa, 0x805789fb
            # Events 0x805789fc, 0x805789fd
            events = dolphin_memory_engine.read_bytes(0x805789f8, 6)
            int_events = int.from_bytes(events, "big")

            # Set all events and cgs watched, except for befriend Yoshi
            int_events |= 0xFF7FFFFFFFFF
            events = int_events.to_bytes(6, "big")
            dolphin_memory_engine.write_bytes(0x805789f8, events)

        # Only mess with nozzles outside Delfino Airstrip or Title screen
        elif courses != 0x00 and courses != 0x0f:
            game_state_address = dolphin_memory_engine.follow_pointers(0x80005518, [0x04, 0x64])
            game_state = dolphin_memory_engine.read_byte(game_state_address)

            # Game on normal state 4?
            if game_state == 4:
                unlocked_nozzles = []
                mario_status_address = dolphin_memory_engine.follow_pointers(0x8040e0e8, [0x11a])
                mario_status = dolphin_memory_engine.read_byte(mario_status_address)
                primary_nozzle_address = dolphin_memory_engine.follow_pointers(0x8040e0e8, [0x3e4, 0x1c84])
                secondary_nozzle_address = dolphin_memory_engine.follow_pointers(0x8040e0e8, [0x3e4, 0x1c85])
                primary_nozzle = dolphin_memory_engine.read_byte(primary_nozzle_address)
                secondary_nozzle = dolphin_memory_engine.read_byte(secondary_nozzle_address)

                game_nozzles = {
                    "Spray Nozzle": 0,
                    "Rocket Nozzle": 1,
                    "Hover Nozzle": 4,
                    "Turbo Nozzle": 5
                }

                if len(unlocked_nozzles) == 0:
                    if mario_status & (1 << 7):
                        mario_status &= (0 << 7)
                        dolphin_memory_engine.write_byte(mario_status_address, mario_status)
                else:
                    if not (mario_status & (1 << 7)):
                        mario_status |= (1 << 7)
                        dolphin_memory_engine.write_byte(mario_status_address, mario_status)
                    # Update Box status
                    delfino_box = dolphin_memory_engine.read_byte(0x805789f4)
                    level_box = dolphin_memory_engine.read_byte(0x805789f5)
                    if "Rocket Nozzle" not in unlocked_nozzles:
                        if delfino_box & (1 << 6):
                            delfino_box &= (0 << 6)
                            dolphin_memory_engine.write_byte(0x805789f4, delfino_box)
                        if level_box & (1 << 0) or level_box & (1 << 2):
                            level_box &= (0 << 0)
                            level_box &= (0 << 2)
                            dolphin_memory_engine.write_byte(0x805789f5, level_box)
                    else:
                        if not (delfino_box & (1 << 6)):
                            delfino_box |= (1 << 6)
                            dolphin_memory_engine.write_byte(0x805789f4, delfino_box)
                        if not (level_box & (1 << 0) or level_box & (1 << 2)):
                            level_box |= (1 << 0)
                            level_box |= (1 << 2)
                            dolphin_memory_engine.write_byte(0x805789f5, level_box)
                    if "Turbo Nozzle" not in unlocked_nozzles:
                        if delfino_box & (1 << 7):
                            delfino_box &= (0 << 7)
                            dolphin_memory_engine.write_byte(0x805789f4, delfino_box)
                        if level_box & (1 << 1) or level_box & (1 << 3):
                            level_box &= (0 << 1)
                            level_box &= (0 << 3)
                            dolphin_memory_engine.write_byte(0x805789f5, level_box)
                    else:
                        if not (delfino_box & (1 << 7)):
                            delfino_box |= (1 << 7)
                            dolphin_memory_engine.write_byte(0x805789f4, delfino_box)
                        if not (level_box & (1 << 1) or level_box & (1 << 3)):
                            level_box |= (1 << 1)
                            level_box |= (1 << 3)
                            dolphin_memory_engine.write_byte(0x805789f5, level_box)

                    unlock_nozzles_value = []
                    for n in unlocked_nozzles:
                        unlock_nozzles_value.append(game_nozzles[n])

                    if len(unlock_nozzles_value) > 0:
                        if primary_nozzle not in unlock_nozzles_value:
                            dolphin_memory_engine.write_byte(primary_nozzle_address, unlock_nozzles_value[0])
                        if secondary_nozzle not in unlock_nozzles_value:
                            dolphin_memory_engine.write_byte(secondary_nozzle_address, unlock_nozzles_value[0])
        await asyncio.sleep(0.2)


def main(connect=None, password=None):
    async def _main(connect, password):
        ctx = SMSContext(connect, password)
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        dolphin_memory_engine.hook()
        if dolphin_memory_engine.is_hooked():
            logger.info("Hooked to Dolphin")

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")
        await ctx.dolphin_sync_task
        await asyncio.sleep(.25)

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        await asyncio.sleep(.5)

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
