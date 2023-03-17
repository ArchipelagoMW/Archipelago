from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from typing import List, Optional, Set, Union

from loguru import logger

from sc2.constants import IS_ENEMY, IS_MINE, FakeEffectID, FakeEffectRadii
from sc2.data import Alliance, DisplayType
from sc2.ids.ability_id import AbilityId
from sc2.ids.effect_id import EffectId
from sc2.ids.upgrade_id import UpgradeId
from sc2.pixel_map import PixelMap
from sc2.position import Point2, Point3
from sc2.power_source import PsionicMatrix
from sc2.score import ScoreDetails

try:
    from sc2.dicts.generic_redirect_abilities import GENERIC_REDIRECT_ABILITIES
except ImportError:
    logger.info('Unable to import "GENERIC_REDIRECT_ABILITIES"')
    GENERIC_REDIRECT_ABILITIES = {}


class Blip:

    def __init__(self, proto):
        """
        :param proto:
        """
        self._proto = proto

    @property
    def is_blip(self) -> bool:
        """Detected by sensor tower."""
        return self._proto.is_blip

    @property
    def is_snapshot(self) -> bool:
        return self._proto.display_type == DisplayType.Snapshot.value

    @property
    def is_visible(self) -> bool:
        return self._proto.display_type == DisplayType.Visible.value

    @property
    def alliance(self) -> Alliance:
        return self._proto.alliance

    @property
    def is_mine(self) -> bool:
        return self._proto.alliance == Alliance.Self.value

    @property
    def is_enemy(self) -> bool:
        return self._proto.alliance == Alliance.Enemy.value

    @property
    def position(self) -> Point2:
        """2d position of the blip."""
        return Point2.from_proto(self._proto.pos)

    @property
    def position3d(self) -> Point3:
        """3d position of the blip."""
        return Point3.from_proto(self._proto.pos)


class Common:
    ATTRIBUTES = [
        "player_id",
        "minerals",
        "vespene",
        "food_cap",
        "food_used",
        "food_army",
        "food_workers",
        "idle_worker_count",
        "army_count",
        "warp_gate_count",
        "larva_count",
    ]

    def __init__(self, proto):
        self._proto = proto

    def __getattr__(self, attr):
        assert attr in self.ATTRIBUTES, f"'{attr}' is not a valid attribute"
        return int(getattr(self._proto, attr))


class EffectData:

    def __init__(self, proto, fake=False):
        """
        :param proto:
        :param fake:
        """
        self._proto = proto
        self.fake = fake

    @property
    def id(self) -> Union[EffectId, str]:
        if self.fake:
            # Returns the string from constants.py, e.g. "KD8CHARGE"
            return FakeEffectID[self._proto.unit_type]
        return EffectId(self._proto.effect_id)

    @property
    def positions(self) -> Set[Point2]:
        if self.fake:
            return {Point2.from_proto(self._proto.pos)}
        return {Point2.from_proto(p) for p in self._proto.pos}

    @property
    def alliance(self) -> Alliance:
        return self._proto.alliance

    @property
    def is_mine(self) -> bool:
        """ Checks if the effect is caused by me. """
        return self._proto.alliance == IS_MINE

    @property
    def is_enemy(self) -> bool:
        """ Checks if the effect is hostile. """
        return self._proto.alliance == IS_ENEMY

    @property
    def owner(self) -> int:
        return self._proto.owner

    @property
    def radius(self) -> float:
        if self.fake:
            return FakeEffectRadii[self._proto.unit_type]
        return self._proto.radius

    def __repr__(self) -> str:
        return f"{self.id} with radius {self.radius} at {self.positions}"


@dataclass
class ChatMessage:
    player_id: int
    message: str


@dataclass
class AbilityLookupTemplateClass:

    @property
    def exact_id(self) -> AbilityId:
        return AbilityId(self.ability_id)

    @property
    def generic_id(self) -> AbilityId:
        """
        See https://github.com/BurnySc2/python-sc2/blob/511c34f6b7ae51bd11e06ba91b6a9624dc04a0c0/sc2/dicts/generic_redirect_abilities.py#L13
        """
        return GENERIC_REDIRECT_ABILITIES.get(self.exact_id, self.exact_id)


@dataclass
class ActionRawUnitCommand(AbilityLookupTemplateClass):
    game_loop: int
    ability_id: int
    unit_tags: List[int]
    queue_command: bool
    target_world_space_pos: Optional[Point2]
    target_unit_tag: Optional[int] = None


@dataclass
class ActionRawToggleAutocast(AbilityLookupTemplateClass):
    game_loop: int
    ability_id: int
    unit_tags: List[int]


@dataclass
class ActionRawCameraMove:
    center_world_space: Point2


@dataclass
class ActionError(AbilityLookupTemplateClass):
    ability_id: int
    unit_tag: int
    # See here for the codes of 'result': https://github.com/Blizzard/s2client-proto/blob/01ab351e21c786648e4c6693d4aad023a176d45c/s2clientprotocol/error.proto#L6
    result: int


class GameState:

    def __init__(self, response_observation, previous_observation=None):
        """
        :param response_observation:
        :param previous_observation:
        """
        # Only filled in realtime=True in case the bot skips frames
        self.previous_observation = previous_observation
        self.response_observation = response_observation

        # https://github.com/Blizzard/s2client-proto/blob/51662231c0965eba47d5183ed0a6336d5ae6b640/s2clientprotocol/sc2api.proto#L575
        self.observation = response_observation.observation
        self.observation_raw = self.observation.raw_data
        self.player_result = response_observation.player_result
        self.common: Common = Common(self.observation.player_common)

        # Area covered by Pylons and Warpprisms
        self.psionic_matrix: PsionicMatrix = PsionicMatrix.from_proto(self.observation_raw.player.power_sources)
        # 22.4 per second on faster game speed
        self.game_loop: int = self.observation.game_loop

        # https://github.com/Blizzard/s2client-proto/blob/33f0ecf615aa06ca845ffe4739ef3133f37265a9/s2clientprotocol/score.proto#L31
        self.score: ScoreDetails = ScoreDetails(self.observation.score)
        self.abilities = self.observation.abilities  # abilities of selected units
        self.upgrades = set()
        # self.upgrades: Set[UpgradeId] = {UpgradeId(upgrade) for upgrade in self.observation_raw.player.upgrade_ids}

        # self.visibility[point]: 0=Hidden, 1=Fogged, 2=Visible
        self.visibility: PixelMap = PixelMap(self.observation_raw.map_state.visibility)
        # self.creep[point]: 0=No creep, 1=creep
        self.creep: PixelMap = PixelMap(self.observation_raw.map_state.creep, in_bits=True)

        # Effects like ravager bile shot, lurker attack, everything in effect_id.py
        # self.effects: Set[EffectData] = {EffectData(effect) for effect in self.observation_raw.effects}
        self.effects = set()
        """ Usage:
        for effect in self.state.effects:
            if effect.id == EffectId.RAVAGERCORROSIVEBILECP:
                positions = effect.positions
                # dodge the ravager biles
        """

    @cached_property
    def dead_units(self) -> Set[int]:
        """ A set of unit tags that died this frame """
        _dead_units = set(self.observation_raw.event.dead_units)
        if self.previous_observation:
            return _dead_units | set(self.previous_observation.observation.raw_data.event.dead_units)
        return _dead_units

    @cached_property
    def chat(self) -> List[ChatMessage]:
        """List of chat messages sent this frame (by either player)."""
        previous_frame_chat = self.previous_observation.chat if self.previous_observation else []
        return [
            ChatMessage(message.player_id, message.message)
            for message in chain(previous_frame_chat, self.response_observation.chat)
        ]

    @cached_property
    def alerts(self) -> List[int]:
        """
        Game alerts, see https://github.com/Blizzard/s2client-proto/blob/01ab351e21c786648e4c6693d4aad023a176d45c/s2clientprotocol/sc2api.proto#L683-L706
        """
        if self.previous_observation:
            return list(chain(self.previous_observation.observation.alerts, self.observation.alerts))
        return self.observation.alerts

    @cached_property
    def actions(self) -> List[Union[ActionRawUnitCommand, ActionRawToggleAutocast, ActionRawCameraMove]]:
        """
        List of successful actions since last frame.
        See https://github.com/Blizzard/s2client-proto/blob/01ab351e21c786648e4c6693d4aad023a176d45c/s2clientprotocol/sc2api.proto#L630-L637

        Each action is converted into Python dataclasses: ActionRawUnitCommand, ActionRawToggleAutocast, ActionRawCameraMove
        """
        previous_frame_actions = self.previous_observation.actions if self.previous_observation else []
        actions = []
        for action in chain(previous_frame_actions, self.response_observation.actions):
            action_raw = action.action_raw
            game_loop = action.game_loop
            if action_raw.HasField("unit_command"):
                # Unit commands
                raw_unit_command = action_raw.unit_command
                if raw_unit_command.HasField("target_world_space_pos"):
                    # Actions that have a point as target
                    actions.append(
                        ActionRawUnitCommand(
                            game_loop,
                            raw_unit_command.ability_id,
                            raw_unit_command.unit_tags,
                            raw_unit_command.queue_command,
                            Point2.from_proto(raw_unit_command.target_world_space_pos),
                        )
                    )
                else:
                    # Actions that have a unit as target
                    actions.append(
                        ActionRawUnitCommand(
                            game_loop,
                            raw_unit_command.ability_id,
                            raw_unit_command.unit_tags,
                            raw_unit_command.queue_command,
                            None,
                            raw_unit_command.target_unit_tag,
                        )
                    )
            elif action_raw.HasField("toggle_autocast"):
                # Toggle autocast actions
                raw_toggle_autocast_action = action_raw.toggle_autocast
                actions.append(
                    ActionRawToggleAutocast(
                        game_loop,
                        raw_toggle_autocast_action.ability_id,
                        raw_toggle_autocast_action.unit_tags,
                    )
                )
            else:
                # Camera move actions
                actions.append(ActionRawCameraMove(Point2.from_proto(action.action_raw.camera_move.center_world_space)))
        return actions

    @cached_property
    def actions_unit_commands(self) -> List[ActionRawUnitCommand]:
        """
        List of successful unit actions since last frame.
        See https://github.com/Blizzard/s2client-proto/blob/01ab351e21c786648e4c6693d4aad023a176d45c/s2clientprotocol/raw.proto#L185-L193
        """
        return list(filter(lambda action: isinstance(action, ActionRawUnitCommand), self.actions))

    @cached_property
    def actions_toggle_autocast(self) -> List[ActionRawToggleAutocast]:
        """
        List of successful autocast toggle actions since last frame.
        See https://github.com/Blizzard/s2client-proto/blob/01ab351e21c786648e4c6693d4aad023a176d45c/s2clientprotocol/raw.proto#L199-L202
        """
        return list(filter(lambda action: isinstance(action, ActionRawToggleAutocast), self.actions))

    @cached_property
    def action_errors(self) -> List[ActionError]:
        """
        List of erroneous actions since last frame.
        See https://github.com/Blizzard/s2client-proto/blob/01ab351e21c786648e4c6693d4aad023a176d45c/s2clientprotocol/sc2api.proto#L648-L652
        """
        previous_frame_errors = self.previous_observation.action_errors if self.previous_observation else []
        return [
            ActionError(error.ability_id, error.unit_tag, error.result)
            for error in chain(self.response_observation.action_errors, previous_frame_errors)
        ]
