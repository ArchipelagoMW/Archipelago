import platform
from pathlib import Path

from loguru import logger
from s2clientprotocol import sc2api_pb2 as sc_pb

from sc2.player import Computer
from sc2.protocol import Protocol


class Controller(Protocol):

    def __init__(self, ws, process):
        super().__init__(ws)
        self._process = process

    @property
    def running(self):
        # pylint: disable=W0212
        return self._process._process is not None

    async def create_game(self, game_map, players, realtime: bool, random_seed=None, disable_fog=None):
        req = sc_pb.RequestCreateGame(
            local_map=sc_pb.LocalMap(map_path=str(game_map.relative_path)), realtime=realtime, disable_fog=disable_fog
        )
        if random_seed is not None:
            req.random_seed = random_seed

        for player in players:
            p = req.player_setup.add()
            p.type = player.type.value
            if isinstance(player, Computer):
                p.race = player.race.value
                p.difficulty = player.difficulty.value
                p.ai_build = player.ai_build.value

        logger.info("Creating new game")
        logger.info(f"Map:     {game_map.name}")
        logger.info(f"Players: {', '.join(str(p) for p in players)}")
        result = await self._execute(create_game=req)
        return result

    async def request_available_maps(self):
        req = sc_pb.RequestAvailableMaps()
        result = await self._execute(available_maps=req)
        return result

    async def request_save_map(self, download_path: str):
        """ Not working on linux. """
        req = sc_pb.RequestSaveMap(map_path=download_path)
        result = await self._execute(save_map=req)
        return result

    async def request_replay_info(self, replay_path: str):
        """ Not working on linux. """
        req = sc_pb.RequestReplayInfo(replay_path=replay_path, download_data=False)
        result = await self._execute(replay_info=req)
        return result

    async def start_replay(self, replay_path: str, realtime: bool, observed_id: int = 0):
        ifopts = sc_pb.InterfaceOptions(
            raw=True, score=True, show_cloaked=True, raw_affects_selection=True, raw_crop_to_playable_area=False
        )
        if platform.system() == "Linux":
            replay_name = Path(replay_path).name
            home_replay_folder = Path.home() / "Documents" / "StarCraft II" / "Replays"
            if str(home_replay_folder / replay_name) != replay_path:
                logger.warning(
                    f"Linux detected, please put your replay in your home directory at {home_replay_folder}. It was detected at {replay_path}"
                )
                raise FileNotFoundError
            replay_path = replay_name

        req = sc_pb.RequestStartReplay(
            replay_path=replay_path, observed_player_id=observed_id, realtime=realtime, options=ifopts
        )

        result = await self._execute(start_replay=req)
        assert result.status == 4, f"{result.start_replay.error} - {result.start_replay.error_details}"
        return result
