# pylint: disable=W0212
import asyncio
import os
import platform
import subprocess
import time
import traceback

from aiohttp import WSMsgType, web
from worlds._sc2common.bot import logger
from .proto import sc2api_pb2 as sc_pb

from .controller import Controller
from .data import Result, Status
from .player import BotProcess


class Proxy:
    """
    Class for handling communication between sc2 and an external bot.
    This "middleman" is needed for enforcing time limits, collecting results, and closing things properly.
    """

    def __init__(
        self,
        controller: Controller,
        player: BotProcess,
        proxyport: int,
        game_time_limit: int = None,
        realtime: bool = False,
    ):
        self.controller = controller
        self.player = player
        self.port = proxyport
        self.timeout_loop = game_time_limit * 22.4 if game_time_limit else None
        self.realtime = realtime
        logger.debug(
            f"Proxy Inited with ctrl {controller}({controller._process._port}), player {player}, proxyport {proxyport}, lim {game_time_limit}"
        )

        self.result = None
        self.player_id: int = None
        self.done = False

    async def parse_request(self, msg):
        request = sc_pb.Request()
        request.ParseFromString(msg.data)
        if request.HasField("quit"):
            request = sc_pb.Request(leave_game=sc_pb.RequestLeaveGame())
        if request.HasField("leave_game"):
            if self.controller._status == Status.in_game:
                logger.info(f"Proxy: player {self.player.name}({self.player_id}) surrenders")
                self.result = {self.player_id: Result.Defeat}
            elif self.controller._status == Status.ended:
                await self.get_response()
        elif request.HasField("join_game") and not request.join_game.HasField("player_name"):
            request.join_game.player_name = self.player.name
        await self.controller._ws.send_bytes(request.SerializeToString())

    # TODO Catching too general exception Exception (broad-except)
    # pylint: disable=W0703
    async def get_response(self):
        response_bytes = None
        try:
            response_bytes = await self.controller._ws.receive_bytes()
        except TypeError as e:
            logger.exception("Cannot receive: SC2 Connection already closed.")
            tb = traceback.format_exc()
            logger.error(f"Exception {e}: {tb}")
        except asyncio.CancelledError:
            logger.info(f"Proxy({self.player.name}), caught receive from sc2")
            try:
                x = await self.controller._ws.receive_bytes()
                if response_bytes is None:
                    response_bytes = x
            except (asyncio.CancelledError, asyncio.TimeoutError, Exception) as e:
                logger.exception(f"Exception {e}")
        except Exception as e:
            logger.exception(f"Caught unknown exception: {e}")
        return response_bytes

    async def parse_response(self, response_bytes):
        response = sc_pb.Response()
        response.ParseFromString(response_bytes)

        if not response.HasField("status"):
            logger.critical("Proxy: RESPONSE HAS NO STATUS {response}")
        else:
            new_status = Status(response.status)
            if new_status != self.controller._status:
                logger.info(f"Controller({self.player.name}): {self.controller._status}->{new_status}")
                self.controller._status = new_status

        if self.player_id is None:
            if response.HasField("join_game"):
                self.player_id = response.join_game.player_id
                logger.info(f"Proxy({self.player.name}): got join_game for {self.player_id}")

        if self.result is None:
            if response.HasField("observation"):
                obs: sc_pb.ResponseObservation = response.observation
                if obs.player_result:
                    self.result = {pr.player_id: Result(pr.result) for pr in obs.player_result}
                elif (
                    self.timeout_loop and obs.HasField("observation") and obs.observation.game_loop > self.timeout_loop
                ):
                    self.result = {i: Result.Tie for i in range(1, 3)}
                    logger.info(f"Proxy({self.player.name}) timing out")
                    act = [sc_pb.Action(action_chat=sc_pb.ActionChat(message="Proxy: Timing out"))]
                    await self.controller._execute(action=sc_pb.RequestAction(actions=act))
        return response

    async def get_result(self):
        try:
            res = await self.controller.ping()
            if res.status in {Status.in_game, Status.in_replay, Status.ended}:
                res = await self.controller._execute(observation=sc_pb.RequestObservation())
                if res.HasField("observation") and res.observation.player_result:
                    self.result = {pr.player_id: Result(pr.result) for pr in res.observation.player_result}
        # pylint: disable=W0703
        # TODO Catching too general exception Exception (broad-except)
        except Exception as e:
            logger.exception(f"Caught unknown exception: {e}")

    async def proxy_handler(self, request):
        bot_ws = web.WebSocketResponse(receive_timeout=30)
        await bot_ws.prepare(request)
        try:
            async for msg in bot_ws:
                if msg.data is None:
                    raise TypeError(f"data is None, {msg}")
                if msg.data and msg.type == WSMsgType.BINARY:

                    await self.parse_request(msg)

                    response_bytes = await self.get_response()
                    if response_bytes is None:
                        raise ConnectionError("Could not get response_bytes")

                    new_response = await self.parse_response(response_bytes)
                    await bot_ws.send_bytes(new_response.SerializeToString())

                elif msg.type == WSMsgType.CLOSED:
                    logger.error("Client shutdown")
                else:
                    logger.error("Incorrect message type")
        # pylint: disable=W0703
        # TODO Catching too general exception Exception (broad-except)
        except Exception as e:
            logger.exception(f"Caught unknown exception: {e}")
            ignored_errors = {ConnectionError, asyncio.CancelledError}
            if not any(isinstance(e, E) for E in ignored_errors):
                tb = traceback.format_exc()
                logger.info(f"Proxy({self.player.name}): Caught {e} traceback: {tb}")
        finally:
            try:
                if self.controller._status in {Status.in_game, Status.in_replay}:
                    await self.controller._execute(leave_game=sc_pb.RequestLeaveGame())
                await bot_ws.close()
            # pylint: disable=W0703
            # TODO Catching too general exception Exception (broad-except)
            except Exception as e:
                logger.exception(f"Caught unknown exception during surrender: {e}")
            self.done = True
        return bot_ws

    # pylint: disable=R0912
    async def play_with_proxy(self, startport):
        logger.info(f"Proxy({self.port}): Starting app")
        app = web.Application()
        app.router.add_route("GET", "/sc2api", self.proxy_handler)
        apprunner = web.AppRunner(app, access_log=None)
        await apprunner.setup()
        appsite = web.TCPSite(apprunner, self.controller._process._host, self.port)
        await appsite.start()

        subproc_args = {"cwd": str(self.player.path), "stderr": subprocess.STDOUT}
        if platform.system() == "Linux":
            subproc_args["preexec_fn"] = os.setpgrp
        elif platform.system() == "Windows":
            subproc_args["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

        player_command_line = self.player.cmd_line(self.port, startport, self.controller._process._host, self.realtime)
        logger.info(f"Starting bot with command: {' '.join(player_command_line)}")
        if self.player.stdout is None:
            bot_process = subprocess.Popen(player_command_line, stdout=subprocess.DEVNULL, **subproc_args)
        else:
            with open(self.player.stdout, "w+") as out:
                bot_process = subprocess.Popen(player_command_line, stdout=out, **subproc_args)

        while self.result is None:
            bot_alive = bot_process and bot_process.poll() is None
            sc2_alive = self.controller.running
            if self.done or not (bot_alive and sc2_alive):
                logger.info(
                    f"Proxy({self.port}): {self.player.name} died, "
                    f"bot{(not bot_alive) * ' not'} alive, sc2{(not sc2_alive) * ' not'} alive"
                )
                # Maybe its still possible to retrieve a result
                if sc2_alive and not self.done:
                    await self.get_response()
                logger.info(f"Proxy({self.port}): breaking, result {self.result}")
                break
            await asyncio.sleep(5)

        # cleanup
        logger.info(f"({self.port}): cleaning up {self.player !r}")
        for _i in range(3):
            if isinstance(bot_process, subprocess.Popen):
                if bot_process.stdout and not bot_process.stdout.closed:  # should not run anymore
                    logger.info(f"==================output for player {self.player.name}")
                    for l in bot_process.stdout.readlines():
                        logger.opt(raw=True).info(l.decode("utf-8"))
                    bot_process.stdout.close()
                    logger.info("==================")
                bot_process.terminate()
                bot_process.wait()
            time.sleep(0.5)
            if not bot_process or bot_process.poll() is not None:
                break
        else:
            bot_process.terminate()
            bot_process.wait()
        try:
            await apprunner.cleanup()
        # pylint: disable=W0703
        # TODO Catching too general exception Exception (broad-except)
        except Exception as e:
            logger.exception(f"Caught unknown exception during cleaning: {e}")
        if isinstance(self.result, dict):
            self.result[None] = None
            return self.result[self.player_id]
        return self.result
