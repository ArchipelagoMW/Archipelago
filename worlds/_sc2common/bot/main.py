# pylint: disable=W0212
from __future__ import annotations

import asyncio
import json
import platform
import signal
from contextlib import suppress
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import mpyq
import portpicker
from aiohttp import ClientSession, ClientWebSocketResponse
from worlds._sc2common.bot import logger
from .proto import sc2api_pb2 as sc_pb

from .bot_ai import BotAI
from .client import Client
from .controller import Controller
from .data import CreateGameError, Result, Status
from .game_state import GameState
from .maps import Map
from .player import AbstractPlayer, Bot, BotProcess, Human
from .portconfig import Portconfig
from .protocol import ConnectionAlreadyClosed, ProtocolError
from .proxy import Proxy
from .sc2process import SC2Process, kill_switch


@dataclass
class GameMatch:
    """Dataclass for hosting a match of SC2.
    This contains all of the needed information for RequestCreateGame.
    :param sc2_config: dicts of arguments to unpack into sc2process's construction, one per player
        second sc2_config will be ignored if only one sc2_instance is spawned
        e.g. sc2_args=[{"fullscreen": True}, {}]: only player 1's sc2instance will be fullscreen
    :param game_time_limit: The time (in seconds) until a match is artificially declared a Tie
    """

    map_sc2: Map
    players: List[AbstractPlayer]
    realtime: bool = False
    random_seed: int = None
    disable_fog: bool = None
    sc2_config: List[Dict] = None
    game_time_limit: int = None

    def __post_init__(self):
        # avoid players sharing names
        if len(self.players) > 1 and self.players[0].name is not None and self.players[0].name == self.players[1].name:
            self.players[1].name += "2"

        if self.sc2_config is not None:
            if isinstance(self.sc2_config, dict):
                self.sc2_config = [self.sc2_config]
            if len(self.sc2_config) == 0:
                self.sc2_config = [{}]
            while len(self.sc2_config) < len(self.players):
                self.sc2_config += self.sc2_config
            self.sc2_config = self.sc2_config[:len(self.players)]

    @property
    def needed_sc2_count(self) -> int:
        return sum(player.needs_sc2 for player in self.players)

    @property
    def host_game_kwargs(self) -> Dict:
        return {
            "map_settings": self.map_sc2,
            "players": self.players,
            "realtime": self.realtime,
            "random_seed": self.random_seed,
            "disable_fog": self.disable_fog,
        }

    def __repr__(self):
        p1 = self.players[0]
        p1 = p1.name if p1.name else p1
        p2 = self.players[1]
        p2 = p2.name if p2.name else p2
        return f"Map: {self.map_sc2.name}, {p1} vs {p2}, realtime={self.realtime}, seed={self.random_seed}"


async def _play_game_human(client, player_id, realtime, game_time_limit):
    while True:
        state = await client.observation()
        if client._game_result:
            return client._game_result[player_id]

        if game_time_limit and state.observation.observation.game_loop / 22.4 > game_time_limit:
            logger.info(state.observation.game_loop, state.observation.game_loop / 22.4)
            return Result.Tie

        if not realtime:
            await client.step()


# pylint: disable=R0912,R0911,R0914
async def _play_game_ai(
    client: Client, player_id: int, ai: BotAI, realtime: bool, game_time_limit: Optional[int]
) -> Result:
    gs: GameState = None

    async def initialize_first_step() -> Optional[Result]:
        nonlocal gs
        ai._initialize_variables()

        game_data = await client.get_game_data()
        game_info = await client.get_game_info()
        ping_response = await client.ping()

        # This game_data will become self.game_data in botAI
        ai._prepare_start(
            client, player_id, game_info, game_data, realtime=realtime, base_build=ping_response.ping.base_build
        )
        state = await client.observation()
        # check game result every time we get the observation
        if client._game_result:
            await ai.on_end(client._game_result[player_id])
            return client._game_result[player_id]
        gs = GameState(state.observation)
        proto_game_info = await client._execute(game_info=sc_pb.RequestGameInfo())
        try:
            ai._prepare_step(gs, proto_game_info)
            await ai.on_before_start()
            ai._prepare_first_step()
            await ai.on_start()
        # TODO Catching too general exception Exception (broad-except)
        # pylint: disable=W0703
        except Exception as e:
            logger.exception(f"Caught unknown exception in AI on_start: {e}")
            logger.error("Resigning due to previous error")
            await ai.on_end(Result.Defeat)
            return Result.Defeat

    result = await initialize_first_step()
    if result is not None:
        return result

    async def run_bot_iteration(iteration: int):
        nonlocal gs
        logger.debug(f"Running AI step, it={iteration} {gs.game_loop / 22.4:.2f}s")
        # Issue event like unit created or unit destroyed
        await ai.issue_events()
        # In on_step various errors can occur - log properly
        try:
            await ai.on_step(iteration)
        except (AttributeError, ) as e:
            logger.exception(f"Caught exception: {e}")
            raise
        except Exception as e:
            logger.exception(f"Caught unknown exception: {e}")
            raise
        await ai._after_step()
        logger.debug("Running AI step: done")

    # Only used in realtime=True
    previous_state_observation = None
    for iteration in range(10**10):
        if realtime and gs:
            # On realtime=True, might get an error here: sc2.protocol.ProtocolError: ['Not in a game']
            with suppress(ProtocolError):
                requested_step = gs.game_loop + client.game_step
                state = await client.observation(requested_step)
                # If the bot took too long in the previous observation, request another observation one frame after
                if state.observation.observation.game_loop > requested_step:
                    logger.debug("Skipped a step in realtime=True")
                    previous_state_observation = state.observation
                    state = await client.observation(state.observation.observation.game_loop + 1)
        else:
            state = await client.observation()

        # check game result every time we get the observation
        if client._game_result:
            await ai.on_end(client._game_result[player_id])
            return client._game_result[player_id]
        gs = GameState(state.observation, previous_state_observation)
        previous_state_observation = None
        logger.debug(f"Score: {gs.score.score}")

        if game_time_limit and gs.game_loop / 22.4 > game_time_limit:
            await ai.on_end(Result.Tie)
            return Result.Tie
        proto_game_info = await client._execute(game_info=sc_pb.RequestGameInfo())
        ai._prepare_step(gs, proto_game_info)

        await run_bot_iteration(iteration)  # Main bot loop

        if not realtime:
            if not client.in_game:  # Client left (resigned) the game
                await ai.on_end(client._game_result[player_id])
                return client._game_result[player_id]

            # TODO: In bot vs bot, if the other bot ends the game, this bot gets stuck in requesting an observation when using main.py:run_multiple_games
            await client.step()
    return Result.Undecided


async def _play_game(
    player: AbstractPlayer,
    client: Client,
    realtime,
    portconfig,
    game_time_limit=None,
    rgb_render_config=None
) -> Result:
    assert isinstance(realtime, bool), repr(realtime)

    player_id = await client.join_game(
        player.name, player.race, portconfig=portconfig, rgb_render_config=rgb_render_config
    )
    logger.info(f"Player {player_id} - {player.name if player.name else str(player)}")

    if isinstance(player, Human):
        result = await _play_game_human(client, player_id, realtime, game_time_limit)
    else:
        result = await _play_game_ai(client, player_id, player.ai, realtime, game_time_limit)

    logger.info(
        f"Result for player {player_id} - {player.name if player.name else str(player)}: "
        f"{result._name_ if isinstance(result, Result) else result}"
    )

    return result

async def _setup_host_game(
    server: Controller, map_settings, players, realtime, random_seed=None, disable_fog=None, save_replay_as=None
):
    r = await server.create_game(map_settings, players, realtime, random_seed, disable_fog)
    if r.create_game.HasField("error"):
        err = f"Could not create game: {CreateGameError(r.create_game.error)}"
        if r.create_game.HasField("error_details"):
            err += f": {r.create_game.error_details}"
        logger.critical(err)
        raise RuntimeError(err)

    return Client(server._ws, save_replay_as)


async def _host_game(
    map_settings,
    players,
    realtime=False,
    portconfig=None,
    save_replay_as=None,
    game_time_limit=None,
    rgb_render_config=None,
    random_seed=None,
    sc2_version=None,
    disable_fog=None,
):

    assert players, "Can't create a game without players"

    assert any(isinstance(p, (Human, Bot)) for p in players)

    async with SC2Process(
        fullscreen=players[0].fullscreen, render=rgb_render_config is not None, sc2_version=sc2_version
    ) as server:
        await server.ping()

        client = await _setup_host_game(
            server, map_settings, players, realtime, random_seed, disable_fog, save_replay_as
        )
        # Bot can decide if it wants to launch with 'raw_affects_selection=True'
        if not isinstance(players[0], Human) and getattr(players[0].ai, "raw_affects_selection", None) is not None:
            client.raw_affects_selection = players[0].ai.raw_affects_selection

        result = await _play_game(players[0], client, realtime, portconfig, game_time_limit, rgb_render_config)
        if client.save_replay_path is not None:
            await client.save_replay(client.save_replay_path)
        try:
            await client.leave()
        except ConnectionAlreadyClosed:
            logger.error("Connection was closed before the game ended")
        await client.quit()

        return result


async def _host_game_aiter(
    map_settings,
    players,
    realtime,
    portconfig=None,
    save_replay_as=None,
    game_time_limit=None,
):
    assert players, "Can't create a game without players"

    assert any(isinstance(p, (Human, Bot)) for p in players)

    async with SC2Process() as server:
        while True:
            await server.ping()

            client = await _setup_host_game(server, map_settings, players, realtime)
            if not isinstance(players[0], Human) and getattr(players[0].ai, "raw_affects_selection", None) is not None:
                client.raw_affects_selection = players[0].ai.raw_affects_selection

            try:
                result = await _play_game(players[0], client, realtime, portconfig, game_time_limit)

                if save_replay_as is not None:
                    await client.save_replay(save_replay_as)
                await client.leave()
            except ConnectionAlreadyClosed:
                logger.error("Connection was closed before the game ended")
                return

            new_players = yield result
            if new_players is not None:
                players = new_players


def _host_game_iter(*args, **kwargs):
    game = _host_game_aiter(*args, **kwargs)
    new_playerconfig = None
    while True:
        new_playerconfig = yield asyncio.get_event_loop().run_until_complete(game.asend(new_playerconfig))


async def _join_game(
    players,
    realtime,
    portconfig,
    save_replay_as=None,
    game_time_limit=None,
):
    async with SC2Process(fullscreen=players[1].fullscreen) as server:
        await server.ping()

        client = Client(server._ws)
        # Bot can decide if it wants to launch with 'raw_affects_selection=True'
        if not isinstance(players[1], Human) and getattr(players[1].ai, "raw_affects_selection", None) is not None:
            client.raw_affects_selection = players[1].ai.raw_affects_selection

        result = await _play_game(players[1], client, realtime, portconfig, game_time_limit)
        if save_replay_as is not None:
            await client.save_replay(save_replay_as)
        try:
            await client.leave()
        except ConnectionAlreadyClosed:
            logger.error("Connection was closed before the game ended")
        await client.quit()

        return result


def get_replay_version(replay_path: Union[str, Path]) -> Tuple[str, str]:
    with open(replay_path, 'rb') as f:
        replay_data = f.read()
        replay_io = BytesIO()
        replay_io.write(replay_data)
        replay_io.seek(0)
        archive = mpyq.MPQArchive(replay_io).extract()
        metadata = json.loads(archive[b"replay.gamemetadata.json"].decode("utf-8"))
        return metadata["BaseBuild"], metadata["DataVersion"]


# TODO Deprecate run_game function in favor of run_multiple_games
def run_game(map_settings, players, **kwargs) -> Union[Result, List[Optional[Result]]]:
    """
    Returns a single Result enum if the game was against the built-in computer.
    Returns a list of two Result enums if the game was "Human vs Bot" or "Bot vs Bot".
    """
    if sum(isinstance(p, (Human, Bot)) for p in players) > 1:
        host_only_args = ["save_replay_as", "rgb_render_config", "random_seed", "sc2_version", "disable_fog"]
        join_kwargs = {k: v for k, v in kwargs.items() if k not in host_only_args}

        portconfig = Portconfig()

        async def run_host_and_join():
            return await asyncio.gather(
                _host_game(map_settings, players, **kwargs, portconfig=portconfig),
                _join_game(players, **join_kwargs, portconfig=portconfig),
                return_exceptions=True
            )

        result: List[Result] = asyncio.run(run_host_and_join())
        assert isinstance(result, list)
        assert all(isinstance(r, Result) for r in result)
    else:
        result: Result = asyncio.run(_host_game(map_settings, players, **kwargs))
        assert isinstance(result, Result)
    return result


async def play_from_websocket(
    ws_connection: Union[str, ClientWebSocketResponse],
    player: AbstractPlayer,
    realtime: bool = False,
    portconfig: Portconfig = None,
    save_replay_as=None,
    game_time_limit: int = None,
    should_close=True,
):
    """Use this to play when the match is handled externally e.g. for bot ladder games.
    Portconfig MUST be specified if not playing vs Computer.
    :param ws_connection: either a string("ws://{address}:{port}/sc2api") or a ClientWebSocketResponse object
    :param should_close: closes the connection if True. Use False if something else will reuse the connection

    e.g. ladder usage: play_from_websocket("ws://127.0.0.1:5162/sc2api", MyBot, False, portconfig=my_PC)
    """
    session = None
    try:
        if isinstance(ws_connection, str):
            session = ClientSession()
            ws_connection = await session.ws_connect(ws_connection, timeout=120)
            should_close = True
        client = Client(ws_connection)
        result = await _play_game(player, client, realtime, portconfig, game_time_limit=game_time_limit)
        if save_replay_as is not None:
            await client.save_replay(save_replay_as)
    except ConnectionAlreadyClosed:
        logger.error("Connection was closed before the game ended")
        return None
    finally:
        if should_close:
            await ws_connection.close()
            if session:
                await session.close()

    return result


async def run_match(controllers: List[Controller], match: GameMatch, close_ws=True):
    await _setup_host_game(controllers[0], **match.host_game_kwargs)

    # Setup portconfig beforehand, so all players use the same ports
    startport = None
    portconfig = None
    if match.needed_sc2_count > 1:
        if any(isinstance(player, BotProcess) for player in match.players):
            portconfig = Portconfig.contiguous_ports()
            # Most ladder bots generate their server and client ports as [s+2, s+3], [s+4, s+5]
            startport = portconfig.server[0] - 2
        else:
            portconfig = Portconfig()

    proxies = []
    coros = []
    players_that_need_sc2 = filter(lambda lambda_player: lambda_player.needs_sc2, match.players)
    for i, player in enumerate(players_that_need_sc2):
        if isinstance(player, BotProcess):
            pport = portpicker.pick_unused_port()
            p = Proxy(controllers[i], player, pport, match.game_time_limit, match.realtime)
            proxies.append(p)
            coros.append(p.play_with_proxy(startport))
        else:
            coros.append(
                play_from_websocket(
                    controllers[i]._ws,
                    player,
                    match.realtime,
                    portconfig,
                    should_close=close_ws,
                    game_time_limit=match.game_time_limit,
                )
            )

    async_results = await asyncio.gather(*coros, return_exceptions=True)

    if not isinstance(async_results, list):
        async_results = [async_results]
    for i, a in enumerate(async_results):
        if isinstance(a, Exception):
            logger.error(f"Exception[{a}] thrown by {[p for p in match.players if p.needs_sc2][i]}")

    return process_results(match.players, async_results)


def process_results(players: List[AbstractPlayer], async_results: List[Result]) -> Dict[AbstractPlayer, Result]:
    opp_res = {Result.Victory: Result.Defeat, Result.Defeat: Result.Victory, Result.Tie: Result.Tie}
    result: Dict[AbstractPlayer, Result] = {}
    i = 0
    for player in players:
        if player.needs_sc2:
            if sum(r == Result.Victory for r in async_results) <= 1:
                result[player] = async_results[i]
            else:
                result[player] = Result.Undecided
            i += 1
        else:  # computer
            other_result = async_results[0]
            result[player] = None
            if other_result in opp_res:
                result[player] = opp_res[other_result]

    return result


# pylint: disable=R0912
async def maintain_SCII_count(count: int, controllers: List[Controller], proc_args: List[Dict] = None):
    """Modifies the given list of controllers to reflect the desired amount of SCII processes"""
    # kill unhealthy ones.
    if controllers:
        to_remove = []
        alive = await asyncio.wait_for(
            asyncio.gather(*(c.ping() for c in controllers if not c._ws.closed), return_exceptions=True), timeout=20
        )
        i = 0  # for alive
        for controller in controllers:
            if controller._ws.closed:
                if not controller._process._session.closed:
                    await controller._process._session.close()
                to_remove.append(controller)
            else:
                if not isinstance(alive[i], sc_pb.Response):
                    try:
                        await controller._process._close_connection()
                    finally:
                        to_remove.append(controller)
                i += 1
        for c in to_remove:
            c._process._clean(verbose=False)
            if c._process in kill_switch._to_kill:
                kill_switch._to_kill.remove(c._process)
            controllers.remove(c)

    # spawn more
    if len(controllers) < count:
        needed = count - len(controllers)
        if proc_args:
            index = len(controllers) % len(proc_args)
        else:
            proc_args = [{} for _ in range(needed)]
            index = 0
        extra = [SC2Process(**proc_args[(index + _) % len(proc_args)]) for _ in range(needed)]
        logger.info(f"Creating {needed} more SC2 Processes")
        for _ in range(3):
            if platform.system() == "Linux":
                # Works on linux: start one client after the other
                # pylint: disable=C2801
                new_controllers = [await asyncio.wait_for(sc.__aenter__(), timeout=50) for sc in extra]
            else:
                # Doesnt seem to work on linux: starting 2 clients nearly at the same time
                new_controllers = await asyncio.wait_for(
                    # pylint: disable=C2801
                    asyncio.gather(*[sc.__aenter__() for sc in extra], return_exceptions=True),
                    timeout=50
                )

            controllers.extend(c for c in new_controllers if isinstance(c, Controller))
            if len(controllers) == count:
                await asyncio.wait_for(asyncio.gather(*(c.ping() for c in controllers)), timeout=20)
                break
            extra = [
                extra[i] for i, result in enumerate(new_controllers) if not isinstance(new_controllers, Controller)
            ]
        else:
            logger.critical("Could not launch sufficient SC2")
            raise RuntimeError

    # kill excess
    while len(controllers) > count:
        proc = controllers.pop()
        proc = proc._process
        logger.info(f"Removing SCII listening to {proc._port}")
        await proc._close_connection()
        proc._clean(verbose=False)
        if proc in kill_switch._to_kill:
            kill_switch._to_kill.remove(proc)


def run_multiple_games(matches: List[GameMatch]):
    return asyncio.get_event_loop().run_until_complete(a_run_multiple_games(matches))


# TODO Catching too general exception Exception (broad-except)
# pylint: disable=W0703
async def a_run_multiple_games(matches: List[GameMatch]) -> List[Dict[AbstractPlayer, Result]]:
    """Run multiple matches.
    Non-python bots are supported.
    When playing bot vs bot, this is less likely to fatally crash than repeating run_game()
    """
    if not matches:
        return []

    results = []
    controllers = []
    for m in matches:
        result = None
        dont_restart = m.needed_sc2_count == 2
        try:
            await maintain_SCII_count(m.needed_sc2_count, controllers, m.sc2_config)
            result = await run_match(controllers, m, close_ws=dont_restart)
        except SystemExit as e:
            logger.info(f"Game exit'ed as {e} during match {m}")
        except Exception as e:
            logger.exception(f"Caught unknown exception: {e}")
            logger.info(f"Exception {e} thrown in match {m}")
        finally:
            if dont_restart:  # Keeping them alive after a non-computer match can cause crashes
                await maintain_SCII_count(0, controllers, m.sc2_config)
            results.append(result)
    kill_switch.kill_all()
    return results


# TODO Catching too general exception Exception (broad-except)
# pylint: disable=W0703
async def a_run_multiple_games_nokill(matches: List[GameMatch]) -> List[Dict[AbstractPlayer, Result]]:
    """Run multiple matches while reusing SCII processes.
    Prone to crashes and stalls
    """
    # FIXME: check whether crashes between bot-vs-bot are avoidable or not
    if not matches:
        return []

    # Start the matches
    results = []
    controllers = []
    for m in matches:
        logger.info(f"Starting match {1 + len(results)} / {len(matches)}: {m}")
        result = None
        try:
            await maintain_SCII_count(m.needed_sc2_count, controllers, m.sc2_config)
            result = await run_match(controllers, m, close_ws=False)
        except SystemExit as e:
            logger.critical(f"Game sys.exit'ed as {e} during match {m}")
        except Exception as e:
            logger.exception(f"Caught unknown exception: {e}")
            logger.info(f"Exception {e} thrown in match {m}")
        finally:
            for c in controllers:
                try:
                    await c.ping()
                    if c._status != Status.launched:
                        await c._execute(leave_game=sc_pb.RequestLeaveGame())
                except Exception as e:
                    logger.exception(f"Caught unknown exception: {e}")
                    if not (isinstance(e, ProtocolError) and e.is_game_over_error):
                        logger.info(f"controller {c.__dict__} threw {e}")

            results.append(result)

    # Fire the killswitch manually, instead of letting the winning player fire it.
    await asyncio.wait_for(asyncio.gather(*(c._process._close_connection() for c in controllers)), timeout=50)
    kill_switch.kill_all()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    return results
