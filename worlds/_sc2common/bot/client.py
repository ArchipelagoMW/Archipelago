from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Set, Tuple, Union

from worlds._sc2common.bot import logger

from .proto import debug_pb2 as debug_pb
from .proto import query_pb2 as query_pb
from .proto import raw_pb2 as raw_pb
from .proto import sc2api_pb2 as sc_pb
from .proto import spatial_pb2 as spatial_pb

from .data import ActionResult, ChatChannel, Race, Result, Status
from .game_data import AbilityData, GameData
from .game_info import GameInfo
from .position import Point2, Point3
from .protocol import ConnectionAlreadyClosed, Protocol, ProtocolError
from .renderer import Renderer
from .unit import Unit
from .units import Units


# pylint: disable=R0904
class Client(Protocol):

    def __init__(self, ws, save_replay_path: str = None):
        """
        :param ws:
        """
        super().__init__(ws)
        # How many frames will be waited between iterations before the next one is called
        self.game_step: int = 4
        self.save_replay_path: Optional[str] = save_replay_path
        self._player_id = None
        self._game_result = None
        # Store a hash value of all the debug requests to prevent sending the same ones again if they haven't changed last frame
        self._debug_hash_tuple_last_iteration: Tuple[int, int, int, int] = (0, 0, 0, 0)
        self._debug_draw_last_frame = False
        self._debug_texts = []
        self._debug_lines = []
        self._debug_boxes = []
        self._debug_spheres = []

        self._renderer = None
        self.raw_affects_selection = False

    @property
    def in_game(self) -> bool:
        return self._status in {Status.in_game, Status.in_replay}

    async def join_game(self, name=None, race=None, observed_player_id=None, portconfig=None, rgb_render_config=None):
        ifopts = sc_pb.InterfaceOptions(
            raw=True,
            score=True,
            show_cloaked=True,
            show_burrowed_shadows=True,
            raw_affects_selection=self.raw_affects_selection,
            raw_crop_to_playable_area=False,
            show_placeholders=True,
        )

        if rgb_render_config:
            assert isinstance(rgb_render_config, dict)
            assert "window_size" in rgb_render_config and "minimap_size" in rgb_render_config
            window_size = rgb_render_config["window_size"]
            minimap_size = rgb_render_config["minimap_size"]
            self._renderer = Renderer(self, window_size, minimap_size)
            map_width, map_height = window_size
            minimap_width, minimap_height = minimap_size

            ifopts.render.resolution.x = map_width
            ifopts.render.resolution.y = map_height
            ifopts.render.minimap_resolution.x = minimap_width
            ifopts.render.minimap_resolution.y = minimap_height

        if race is None:
            assert isinstance(observed_player_id, int), f"observed_player_id is of type {type(observed_player_id)}"
            # join as observer
            req = sc_pb.RequestJoinGame(observed_player_id=observed_player_id, options=ifopts)
        else:
            assert isinstance(race, Race)
            req = sc_pb.RequestJoinGame(race=race.value, options=ifopts)

        if portconfig:
            req.server_ports.game_port = portconfig.server[0]
            req.server_ports.base_port = portconfig.server[1]

            for ppc in portconfig.players:
                p = req.client_ports.add()
                p.game_port = ppc[0]
                p.base_port = ppc[1]

        if name is not None:
            assert isinstance(name, str), f"name is of type {type(name)}"
            req.player_name = name

        result = await self._execute(join_game=req)
        self._game_result = None
        self._player_id = result.join_game.player_id
        return result.join_game.player_id

    async def leave(self):
        """ You can use 'await self.client.leave()' to surrender midst game. """
        is_resign = self._game_result is None

        if is_resign:
            # For all clients that can leave, result of leaving the game either
            # loss, or the client will ignore the result
            self._game_result = {self._player_id: Result.Defeat}

        try:
            if self.save_replay_path is not None:
                await self.save_replay(self.save_replay_path)
                self.save_replay_path = None
            await self._execute(leave_game=sc_pb.RequestLeaveGame())
        except (ProtocolError, ConnectionAlreadyClosed):
            if is_resign:
                raise

    async def save_replay(self, path):
        logger.debug("Requesting replay from server")
        result = await self._execute(save_replay=sc_pb.RequestSaveReplay())
        with open(path, "wb") as f:
            f.write(result.save_replay.data)
        logger.info(f"Saved replay to {path}")

    async def observation(self, game_loop: int = None):
        if game_loop is not None:
            result = await self._execute(observation=sc_pb.RequestObservation(game_loop=game_loop))
        else:
            result = await self._execute(observation=sc_pb.RequestObservation())
        assert result.HasField("observation")

        if not self.in_game or result.observation.player_result:
            # Sometimes game ends one step before results are available
            if not result.observation.player_result:
                result = await self._execute(observation=sc_pb.RequestObservation())
                assert result.observation.player_result

            player_id_to_result = {}
            for pr in result.observation.player_result:
                player_id_to_result[pr.player_id] = Result(pr.result)
            self._game_result = player_id_to_result
        self._game_result = None

        # if render_data is available, then RGB rendering was requested
        if self._renderer and result.observation.observation.HasField("render_data"):
            await self._renderer.render(result.observation)

        return result

    async def step(self, step_size: int = None):
        """ EXPERIMENTAL: Change self._client.game_step during the step function to increase or decrease steps per second """
        step_size = step_size or self.game_step
        return await self._execute(step=sc_pb.RequestStep(count=step_size))

    async def get_game_data(self) -> GameData:
        result = await self._execute(
            data=sc_pb.RequestData(ability_id=True, unit_type_id=True, upgrade_id=True, buff_id=True, effect_id=True)
        )
        return GameData(result.data)

    async def dump_data(self, ability_id=True, unit_type_id=True, upgrade_id=True, buff_id=True, effect_id=True):
        """
        Dump the game data files
        choose what data to dump in the keywords
        this function writes to a text file
        call it one time in on_step with:
        await self._client.dump_data()
        """
        result = await self._execute(
            data=sc_pb.RequestData(
                ability_id=ability_id,
                unit_type_id=unit_type_id,
                upgrade_id=upgrade_id,
                buff_id=buff_id,
                effect_id=effect_id,
            )
        )
        with open("data_dump.txt", "a") as file:
            file.write(str(result.data))

    async def get_game_info(self) -> GameInfo:
        result = await self._execute(game_info=sc_pb.RequestGameInfo())
        return GameInfo(result.game_info)

    async def query_pathing(self, start: Union[Unit, Point2, Point3],
                            end: Union[Point2, Point3]) -> Optional[Union[int, float]]:
        """Caution: returns "None" when path not found
        Try to combine queries with the function below because the pathing query is generally slow.

        :param start:
        :param end:"""
        assert isinstance(start, (Point2, Unit))
        assert isinstance(end, Point2)
        if isinstance(start, Point2):
            path = [query_pb.RequestQueryPathing(start_pos=start.as_Point2D, end_pos=end.as_Point2D)]
        else:
            path = [query_pb.RequestQueryPathing(unit_tag=start.tag, end_pos=end.as_Point2D)]
        result = await self._execute(query=query_pb.RequestQuery(pathing=path))
        distance = float(result.query.pathing[0].distance)
        if distance <= 0.0:
            return None
        return distance

    async def query_pathings(self, zipped_list: List[List[Union[Unit, Point2, Point3]]]) -> List[float]:
        """Usage: await self.query_pathings([[unit1, target2], [unit2, target2]])
        -> returns [distance1, distance2]
        Caution: returns 0 when path not found

        :param zipped_list:
        """
        assert zipped_list, "No zipped_list"
        assert isinstance(zipped_list, list), f"{type(zipped_list)}"
        assert isinstance(zipped_list[0], list), f"{type(zipped_list[0])}"
        assert len(zipped_list[0]) == 2, f"{len(zipped_list[0])}"
        assert isinstance(zipped_list[0][0], (Point2, Unit)), f"{type(zipped_list[0][0])}"
        assert isinstance(zipped_list[0][1], Point2), f"{type(zipped_list[0][1])}"
        if isinstance(zipped_list[0][0], Point2):
            path = (
                query_pb.RequestQueryPathing(start_pos=p1.as_Point2D, end_pos=p2.as_Point2D) for p1, p2 in zipped_list
            )
        else:
            path = (query_pb.RequestQueryPathing(unit_tag=p1.tag, end_pos=p2.as_Point2D) for p1, p2 in zipped_list)
        results = await self._execute(query=query_pb.RequestQuery(pathing=path))
        return [float(d.distance) for d in results.query.pathing]

    async def query_building_placement(
        self,
        ability: AbilityData,
        positions: List[Union[Point2, Point3]],
        ignore_resources: bool = True
    ) -> List[ActionResult]:
        """This function might be deleted in favor of the function above (_query_building_placement_fast).

        :param ability:
        :param positions:
        :param ignore_resources:"""
        assert isinstance(ability, AbilityData)
        result = await self._execute(
            query=query_pb.RequestQuery(
                placements=(
                    query_pb.RequestQueryBuildingPlacement(ability_id=ability.id.value, target_pos=position.as_Point2D)
                    for position in positions
                ),
                ignore_resource_requirements=ignore_resources,
            )
        )
        # Unnecessary converting to ActionResult?
        return [ActionResult(p.result) for p in result.query.placements]

    async def chat_send(self, message: str, team_only: bool):
        """ Writes a message to the chat """
        ch = ChatChannel.Team if team_only else ChatChannel.Broadcast
        await self._execute(
            action=sc_pb.RequestAction(
                actions=[sc_pb.Action(action_chat=sc_pb.ActionChat(channel=ch.value, message=message))]
            )
        )

    async def debug_kill_unit(self, unit_tags: Union[Unit, Units, List[int], Set[int]]):
        """
        :param unit_tags:
        """
        if isinstance(unit_tags, Units):
            unit_tags = unit_tags.tags
        if isinstance(unit_tags, Unit):
            unit_tags = [unit_tags.tag]
        assert unit_tags

        await self._execute(
            debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(kill_unit=debug_pb.DebugKillUnit(tag=unit_tags))])
        )

    async def move_camera(self, position: Union[Unit, Units, Point2, Point3]):
        """Moves camera to the target position

        :param position:"""
        assert isinstance(position, (Unit, Units, Point2, Point3))
        if isinstance(position, Units):
            position = position.center
        if isinstance(position, Unit):
            position = position.position
        await self._execute(
            action=sc_pb.RequestAction(
                actions=[
                    sc_pb.Action(
                        action_raw=raw_pb.ActionRaw(
                            camera_move=raw_pb.ActionRawCameraMove(center_world_space=position.to3.as_Point)
                        )
                    )
                ]
            )
        )

    async def obs_move_camera(self, position: Union[Unit, Units, Point2, Point3]):
        """Moves observer camera to the target position. Only works when observing (e.g. watching the replay).

        :param position:"""
        assert isinstance(position, (Unit, Units, Point2, Point3))
        if isinstance(position, Units):
            position = position.center
        if isinstance(position, Unit):
            position = position.position
        await self._execute(
            obs_action=sc_pb.RequestObserverAction(
                actions=[
                    sc_pb.ObserverAction(camera_move=sc_pb.ActionObserverCameraMove(world_pos=position.as_Point2D))
                ]
            )
        )

    async def move_camera_spatial(self, position: Union[Point2, Point3]):
        """Moves camera to the target position using the spatial aciton interface

        :param position:"""
        assert isinstance(position, (Point2, Point3))
        action = sc_pb.Action(
            action_render=spatial_pb.ActionSpatial(
                camera_move=spatial_pb.ActionSpatialCameraMove(center_minimap=position.as_PointI)
            )
        )
        await self._execute(action=sc_pb.RequestAction(actions=[action]))

    def debug_text_simple(self, text: str):
        """ Draws a text in the top left corner of the screen (up to a max of 6 messages fit there). """
        self._debug_texts.append(DrawItemScreenText(text=text, color=None, start_point=Point2((0, 0)), font_size=8))

    def debug_text_screen(
        self,
        text: str,
        pos: Union[Point2, Point3, tuple, list],
        color: Union[tuple, list, Point3] = None,
        size: int = 8,
    ):
        """
        Draws a text on the screen (monitor / game window) with coordinates 0 <= x, y <= 1.

        :param text:
        :param pos:
        :param color:
        :param size:
        """
        assert len(pos) >= 2
        assert 0 <= pos[0] <= 1
        assert 0 <= pos[1] <= 1
        pos = Point2((pos[0], pos[1]))
        self._debug_texts.append(DrawItemScreenText(text=text, color=color, start_point=pos, font_size=size))

    def debug_text_2d(
        self,
        text: str,
        pos: Union[Point2, Point3, tuple, list],
        color: Union[tuple, list, Point3] = None,
        size: int = 8,
    ):
        return self.debug_text_screen(text, pos, color, size)

    def debug_text_world(
        self, text: str, pos: Union[Unit, Point3], color: Union[tuple, list, Point3] = None, size: int = 8
    ):
        """
        Draws a text at Point3 position in the game world.
        To grab a unit's 3d position, use unit.position3d
        Usually the Z value of a Point3 is between 8 and 14 (except for flying units). Use self.get_terrain_z_height() from bot_ai.py to get the Z value (height) of the terrain at a 2D position.

        :param text:
        :param color:
        :param size:
        """
        if isinstance(pos, Unit):
            pos = pos.position3d
        assert isinstance(pos, Point3)
        self._debug_texts.append(DrawItemWorldText(text=text, color=color, start_point=pos, font_size=size))

    def debug_text_3d(
        self, text: str, pos: Union[Unit, Point3], color: Union[tuple, list, Point3] = None, size: int = 8
    ):
        return self.debug_text_world(text, pos, color, size)

    def debug_line_out(
        self, p0: Union[Unit, Point3], p1: Union[Unit, Point3], color: Union[tuple, list, Point3] = None
    ):
        """
        Draws a line from p0 to p1.

        :param p0:
        :param p1:
        :param color:
        """
        if isinstance(p0, Unit):
            p0 = p0.position3d
        assert isinstance(p0, Point3)
        if isinstance(p1, Unit):
            p1 = p1.position3d
        assert isinstance(p1, Point3)
        self._debug_lines.append(DrawItemLine(color=color, start_point=p0, end_point=p1))

    def debug_box_out(
        self,
        p_min: Union[Unit, Point3],
        p_max: Union[Unit, Point3],
        color: Union[tuple, list, Point3] = None,
    ):
        """
        Draws a box with p_min and p_max as corners of the box.

        :param p_min:
        :param p_max:
        :param color:
        """
        if isinstance(p_min, Unit):
            p_min = p_min.position3d
        assert isinstance(p_min, Point3)
        if isinstance(p_max, Unit):
            p_max = p_max.position3d
        assert isinstance(p_max, Point3)
        self._debug_boxes.append(DrawItemBox(start_point=p_min, end_point=p_max, color=color))

    def debug_box2_out(
        self,
        pos: Union[Unit, Point3],
        half_vertex_length: float = 0.25,
        color: Union[tuple, list, Point3] = None,
    ):
        """
        Draws a box center at a position 'pos', with box side lengths (vertices) of two times 'half_vertex_length'.

        :param pos:
        :param half_vertex_length:
        :param color:
        """
        if isinstance(pos, Unit):
            pos = pos.position3d
        assert isinstance(pos, Point3)
        p0 = pos + Point3((-half_vertex_length, -half_vertex_length, -half_vertex_length))
        p1 = pos + Point3((half_vertex_length, half_vertex_length, half_vertex_length))
        self._debug_boxes.append(DrawItemBox(start_point=p0, end_point=p1, color=color))

    def debug_sphere_out(self, p: Union[Unit, Point3], r: float, color: Union[tuple, list, Point3] = None):
        """
        Draws a sphere at point p with radius r.

        :param p:
        :param r:
        :param color:
        """
        if isinstance(p, Unit):
            p = p.position3d
        assert isinstance(p, Point3)
        self._debug_spheres.append(DrawItemSphere(start_point=p, radius=r, color=color))

    async def _send_debug(self):
        """Sends the debug draw execution. This is run by main.py now automatically, if there is any items in the list. You do not need to run this manually any longer.
        Check examples/terran/ramp_wall.py for example drawing. Each draw request needs to be sent again in every single on_step iteration.
        """
        debug_hash = (
            sum(hash(item) for item in self._debug_texts),
            sum(hash(item) for item in self._debug_lines),
            sum(hash(item) for item in self._debug_boxes),
            sum(hash(item) for item in self._debug_spheres),
        )
        if debug_hash != (0, 0, 0, 0):
            if debug_hash != self._debug_hash_tuple_last_iteration:
                # Something has changed, either more or less is to be drawn, or a position of a drawing changed (e.g. when drawing on a moving unit)
                self._debug_hash_tuple_last_iteration = debug_hash
                try:
                    await self._execute(
                        debug=sc_pb.RequestDebug(
                            debug=[
                                debug_pb.DebugCommand(
                                    draw=debug_pb.DebugDraw(
                                        text=[text.to_proto()
                                              for text in self._debug_texts] if self._debug_texts else None,
                                        lines=[line.to_proto()
                                               for line in self._debug_lines] if self._debug_lines else None,
                                        boxes=[box.to_proto()
                                               for box in self._debug_boxes] if self._debug_boxes else None,
                                        spheres=[sphere.to_proto()
                                                 for sphere in self._debug_spheres] if self._debug_spheres else None,
                                    )
                                )
                            ]
                        )
                    )
                except ProtocolError:
                    return
            self._debug_draw_last_frame = True
            self._debug_texts.clear()
            self._debug_lines.clear()
            self._debug_boxes.clear()
            self._debug_spheres.clear()
        elif self._debug_draw_last_frame:
            # Clear drawing if we drew last frame but nothing to draw this frame
            self._debug_hash_tuple_last_iteration = (0, 0, 0, 0)
            await self._execute(
                debug=sc_pb.RequestDebug(
                    debug=[
                        debug_pb.DebugCommand(draw=debug_pb.DebugDraw(text=None, lines=None, boxes=None, spheres=None))
                    ]
                )
            )
            self._debug_draw_last_frame = False

    async def debug_leave(self):
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(end_game=debug_pb.DebugEndGame())]))

    async def debug_set_unit_value(self, unit_tags: Union[Iterable[int], Units, Unit], unit_value: int, value: float):
        """Sets a "unit value" (Energy, Life or Shields) of the given units to the given value.
        Can't set the life of a unit to 0, use "debug_kill_unit" for that. Also can't set the life above the unit's maximum.
        The following example sets the health of all your workers to 1:
        await self.debug_set_unit_value(self.workers, 2, value=1)"""
        if isinstance(unit_tags, Units):
            unit_tags = unit_tags.tags
        if isinstance(unit_tags, Unit):
            unit_tags = [unit_tags.tag]
        assert hasattr(
            unit_tags, "__iter__"
        ), f"unit_tags argument needs to be an iterable (list, dict, set, Units), given argument is {type(unit_tags).__name__}"
        assert (
            1 <= unit_value <= 3
        ), f"unit_value needs to be between 1 and 3 (1 for energy, 2 for life, 3 for shields), given argument is {unit_value}"
        assert all(tag > 0 for tag in unit_tags), f"Unit tags have invalid value: {unit_tags}"
        assert isinstance(value, (int, float)), "Value needs to be of type int or float"
        assert value >= 0, "Value can't be negative"
        await self._execute(
            debug=sc_pb.RequestDebug(
                debug=(
                    debug_pb.DebugCommand(
                        unit_value=debug_pb.
                        DebugSetUnitValue(unit_value=unit_value, value=float(value), unit_tag=unit_tag)
                    ) for unit_tag in unit_tags
                )
            )
        )

    async def debug_hang(self, delay_in_seconds: float):
        """ Freezes the SC2 client. Not recommended to be used. """
        delay_in_ms = int(round(delay_in_seconds * 1000))
        await self._execute(
            debug=sc_pb.RequestDebug(
                debug=[debug_pb.DebugCommand(test_process=debug_pb.DebugTestProcess(test=1, delay_ms=delay_in_ms))]
            )
        )

    async def debug_show_map(self):
        """ Reveals the whole map for the bot. Using it a second time disables it again. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=1)]))

    async def debug_control_enemy(self):
        """ Allows control over enemy units and structures similar to team games control - does not allow the bot to spend the opponent's ressources. Using it a second time disables it again.  """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=2)]))

    async def debug_food(self):
        """ Should disable food usage (does not seem to work?). Using it a second time disables it again.  """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=3)]))

    async def debug_free(self):
        """ Units, structures and upgrades are free of mineral and gas cost. Using it a second time disables it again.  """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=4)]))

    async def debug_all_resources(self):
        """ Gives 5000 minerals and 5000 vespene to the bot. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=5)]))

    async def debug_god(self):
        """ Your units and structures no longer take any damage. Using it a second time disables it again. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=6)]))

    async def debug_minerals(self):
        """ Gives 5000 minerals to the bot. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=7)]))

    async def debug_gas(self):
        """ Gives 5000 vespene to the bot. This does not seem to be working. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=8)]))

    async def debug_cooldown(self):
        """ Disables cooldowns of unit abilities for the bot. Using it a second time disables it again. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=9)]))

    async def debug_tech_tree(self):
        """ Removes all tech requirements (e.g. can build a factory without having a barracks). Using it a second time disables it again. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=10)]))

    async def debug_upgrade(self):
        """ Researches all currently available upgrades. E.g. using it once unlocks combat shield, stimpack and 1-1. Using it a second time unlocks 2-2 and all other upgrades stay researched. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=11)]))

    async def debug_fast_build(self):
        """ Sets the build time of units and structures and upgrades to zero. Using it a second time disables it again. """
        await self._execute(debug=sc_pb.RequestDebug(debug=[debug_pb.DebugCommand(game_state=12)]))

    async def quick_save(self):
        """Saves the current game state to an in-memory bookmark.
        See: https://github.com/Blizzard/s2client-proto/blob/eeaf5efaea2259d7b70247211dff98da0a2685a2/s2clientprotocol/sc2api.proto#L93"""
        await self._execute(quick_save=sc_pb.RequestQuickSave())

    async def quick_load(self):
        """Loads the game state from the previously stored in-memory bookmark.
        Caution:
            - The SC2 Client will crash if the game wasn't quicksaved
            - The bot step iteration counter will not reset
            - self.state.game_loop will be set to zero after the quickload, and self.time is dependant on it"""
        await self._execute(quick_load=sc_pb.RequestQuickLoad())


class DrawItem:

    @staticmethod
    def to_debug_color(color: Union[tuple, Point3]):
        """ Helper function for color conversion """
        if color is None:
            return debug_pb.Color(r=255, g=255, b=255)
        # Need to check if not of type Point3 because Point3 inherits from tuple
        if isinstance(color, (tuple, list)) and not isinstance(color, Point3) and len(color) == 3:
            return debug_pb.Color(r=color[0], g=color[1], b=color[2])
        # In case color is of type Point3
        r = getattr(color, "r", getattr(color, "x", 255))
        g = getattr(color, "g", getattr(color, "y", 255))
        b = getattr(color, "b", getattr(color, "z", 255))
        if max(r, g, b) <= 1:
            r *= 255
            g *= 255
            b *= 255

        return debug_pb.Color(r=int(r), g=int(g), b=int(b))


class DrawItemScreenText(DrawItem):

    def __init__(self, start_point: Point2 = None, color: Point3 = None, text: str = "", font_size: int = 8):
        self._start_point: Point2 = start_point
        self._color: Point3 = color
        self._text: str = text
        self._font_size: int = font_size

    def to_proto(self):
        return debug_pb.DebugText(
            color=self.to_debug_color(self._color),
            text=self._text,
            virtual_pos=self._start_point.to3.as_Point,
            world_pos=None,
            size=self._font_size,
        )

    def __hash__(self):
        return hash((self._start_point, self._color, self._text, self._font_size))


class DrawItemWorldText(DrawItem):

    def __init__(self, start_point: Point3 = None, color: Point3 = None, text: str = "", font_size: int = 8):
        self._start_point: Point3 = start_point
        self._color: Point3 = color
        self._text: str = text
        self._font_size: int = font_size

    def to_proto(self):
        return debug_pb.DebugText(
            color=self.to_debug_color(self._color),
            text=self._text,
            virtual_pos=None,
            world_pos=self._start_point.as_Point,
            size=self._font_size,
        )

    def __hash__(self):
        return hash((self._start_point, self._text, self._font_size, self._color))


class DrawItemLine(DrawItem):

    def __init__(self, start_point: Point3 = None, end_point: Point3 = None, color: Point3 = None):
        self._start_point: Point3 = start_point
        self._end_point: Point3 = end_point
        self._color: Point3 = color

    def to_proto(self):
        return debug_pb.DebugLine(
            line=debug_pb.Line(p0=self._start_point.as_Point, p1=self._end_point.as_Point),
            color=self.to_debug_color(self._color),
        )

    def __hash__(self):
        return hash((self._start_point, self._end_point, self._color))


class DrawItemBox(DrawItem):

    def __init__(self, start_point: Point3 = None, end_point: Point3 = None, color: Point3 = None):
        self._start_point: Point3 = start_point
        self._end_point: Point3 = end_point
        self._color: Point3 = color

    def to_proto(self):
        return debug_pb.DebugBox(
            min=self._start_point.as_Point,
            max=self._end_point.as_Point,
            color=self.to_debug_color(self._color),
        )

    def __hash__(self):
        return hash((self._start_point, self._end_point, self._color))


class DrawItemSphere(DrawItem):

    def __init__(self, start_point: Point3 = None, radius: float = None, color: Point3 = None):
        self._start_point: Point3 = start_point
        self._radius: float = radius
        self._color: Point3 = color

    def to_proto(self):
        return debug_pb.DebugSphere(
            p=self._start_point.as_Point, r=self._radius, color=self.to_debug_color(self._color)
        )

    def __hash__(self):
        return hash((self._start_point, self._radius, self._color))
