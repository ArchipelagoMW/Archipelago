import asyncio
import colorama
import os
from CommonClient import *
from worlds.pysol import *

class PysolContext(CommonContext):
    game = "PysolFC"
    def __init__(self, server_address, password):
        super().__init__(server_address,password)

async def pysol_startgame(self):
    os.popen(executable)
async def pysol_watcher(self):
    await asyncio.open_connection("localhost",1892)
        
async def main(args):
    ctx = PysolContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        input_task = None
        from kvui import FactorioManager
        ctx.ui = FactorioManager(ctx)
        ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
    else:
        input_task = asyncio.create_task(console_loop(ctx), name="Input")
        ui_task = None
    factorio_server_task = asyncio.create_task(pysol_startgame(ctx), name="PysolSpinupServer")
    succesful_launch = await factorio_server_task
    if succesful_launch:
        factorio_server_task = asyncio.create_task(pysol_watcher(ctx), name="PysolWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await factorio_server_task

    if ctx.server and not ctx.server.socket.closed:
        await ctx.server.socket.close()
    if ctx.server_task:
        await ctx.server_task

    while ctx.input_requests > 0:
        ctx.input_queue.put_nowait(None)
        ctx.input_requests -= 1

    if ui_task:
        await ui_task

    if input_task:
        input_task.cancel()
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Optional arguments to PySolClient follow. "
                                                 "Remaining arguments get passed into bound PySolFC instance."
                                                 "Refer to PySolFC --help for those.")
    parser.add_argument('--rcon-port', default='1892', type=int, help='Port to use to communicate with PySolFC')
    parser.add_argument('--rcon-password', help='Password to authenticate with RCON.')
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    if not Utils.is_frozen():  # Frozen state has no cmd window in the first place
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")

    args, rest = parser.parse_known_args()
    colorama.init()
    #rcon_port = args.rcon_port
    #rcon_password = args.rcon_password if args.rcon_password else ''.join(
        #random.choice(string.ascii_letters) for x in range(32))

    factorio_server_logger = logging.getLogger("PySolFCServer")
    options = Utils.get_options()
    executable = options["pysol_options"]["executable"]

    if not os.path.exists(os.path.dirname(executable)):
        raise FileNotFoundError(f"Path {os.path.dirname(executable)} does not exist or could not be accessed.")
    if os.path.isdir(executable):  # user entered a path to a directory, let's find the executable therein
        executable = os.path.join(executable, "pysol")
    if not os.path.isfile(executable):
        if os.path.isfile(executable + ".exe"):
            executable = executable + ".exe"
        elif os.path.isfile(executable + ".py"):
            executable = "python3 " +executable+".py"
        else:
            raise FileNotFoundError(f"Path {executable} is not an executable file.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
    loop.close()
    colorama.deinit()
