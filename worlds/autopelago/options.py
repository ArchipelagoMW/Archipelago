import logging

import yaml

from dataclasses import dataclass
from typing import Any, Mapping, Iterable, Type, TYPE_CHECKING

from Options import Toggle, PerGameCommonOptions, Choice, OptionSet, Range, OptionList, Visibility
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from Options import PlandoOptions

class FillWithDetermination(Toggle):
    """Either fills the rat with determination, or does nothing. Perhaps both.

    This option was added early on for technical reasons. It does not directly affect the game."""
    display_name = "Fill With Determination"


class VictoryLocation(Choice):
    """Optionally moves the final victory location earlier to reduce the number of locations in the multiworld.

    - **Snakes on a Planet (default):** The game goes all the way to "Moon, The". This gives the longest game.
    - **Secret Cache:** The game stops at the end of Cool World. This gives the middlest-length game.
    - **Captured Goldfish:** The game stops at the end of The Sewers. This gives the shortest game."""
    display_name = "Victory Location"
    option_snakes_on_a_planet = 0
    option_secret_cache = 1
    option_captured_goldfish = 2
    default = 0


class EnabledBuffs(OptionSet):
    """Enables various buffs that affect how the rat behaves. All are enabled by default.

    - **Well Fed:** Gets more done
    - **Lucky:** One free success
    - **Energized:** Moves faster
    - **Stylish:** Better RNG
    - **Confident:** Ignore a trap
    - **Smart:** Next check is progression"""
    display_name = "Enabled Buffs"
    valid_keys = frozenset({"Well Fed", "Lucky", "Energized", "Stylish", "Confident", "Smart"})
    default = frozenset({"Well Fed", "Lucky", "Energized", "Stylish", "Confident", "Smart"})
    map = {
        "Well Fed": "well_fed",
        "Lucky": "lucky",
        "Energized": "energized",
        "Stylish": "stylish",
        "Confident": "confident",
        "Smart": "smart",
    }


class EnabledTraps(OptionSet):
    """Enables various traps that affect how the rat behaves. All are enabled by default.

    - **Upset Tummy:** Gets less done
    - **Unlucky:** Worse RNG
    - **Sluggish:** Moves slower
    - **Distracted:** Skip a "step"
    - **Startled:** Run towards start
    - **Conspiratorial:** Next check is trap"""
    display_name = "Enabled Traps"
    valid_keys = frozenset({"Upset Tummy", "Unlucky", "Sluggish", "Distracted", "Startled", "Conspiratorial"})
    default = frozenset({"Upset Tummy", "Unlucky", "Sluggish", "Distracted", "Startled", "Conspiratorial"})

    map = {
        "Upset Tummy": "upset_tummy",
        "Unlucky": "unlucky",
        "Sluggish": "sluggish",
        "Distracted": "distracted",
        "Startled": "startled",
        "Conspiratorial": "conspiratorial",
    }


class DeathDelaySeconds(Range):
    """Sets the delay (in seconds) from a death trigger to when the rat actually "dies". Has no effect if DeathLink is disabled.

    Default: 5 (seconds)
    """
    display_name = "Death Link Delay"
    range_start = 0
    range_end = 60
    default = 5


# hack to avoid outputting the messages in flow style
class RatChatMessagesHack:
    items: list[tuple[str, int]]
    def __init__(self, *args: str):
        self.items = [(arg, 1) for arg in args]


def represent_rat_chat_messages(_dumper: yaml.Dumper, data: RatChatMessagesHack):
    return yaml.SequenceNode(tag="tag:yaml.org,2002:seq", value=[
        yaml.MappingNode(tag="tag:yaml.org,2002:map", value=[
            (yaml.ScalarNode(tag="tag:yaml.org,2002:str", value=t, style='"' if "'" in t else "'"),
             yaml.ScalarNode(tag="tag:yaml.org,2002:int", value=f'{w}'))
        ], flow_style=False) if w != 1 else
        yaml.ScalarNode(tag="tag:yaml.org,2002:str", value=t, style='"' if "'" in t else "'")
        for t, w in data.items
    ])


yaml.add_representer(RatChatMessagesHack, represent_rat_chat_messages)


class RatChatMessages(OptionList):
    # I'm just using OptionList as a shortcut for most of the validation I need here. It won't actually work anywhere in
    # either options UI, especially with the way I've got it replicating how other options can be weighted-or-not.
    visibility = Visibility.template

    @classmethod
    def from_any(cls, data: Any):
        if isinstance(data, RatChatMessagesHack):
            return super().from_any(data.items)

        if isinstance(data, Iterable):
            res: list[tuple[str, int]] = []
            for t in data:
                if isinstance(t, Mapping):
                    if len(t) != 1:
                        raise NotImplementedError(f"Dict must have only one item, got {len(t)}")
                    for kv in t.items():
                        res.append(kv)
                elif isinstance(t, str):
                    res.append((t, 1))
                else:
                    raise NotImplementedError(f"Cannot convert from non-str + non-dict, got {type(t)}")
            return super().from_any(res)

        raise NotImplementedError(f"Cannot convert from non-dict, got {type(data)}")

    def verify(self, world: Type[World], player_name: str, plando_options: 'PlandoOptions') -> None:
        if len(self.value) == 0:
            logging.warning(f"Settings file tried to set empty rat chat messages for {type(self).__name__} (player: {player_name}). This is not allowed. Reverting them to default.")
            self.value = RatChatMessages.from_any(self.default).value


class ChangedTargetMessages(RatChatMessages):
    """What messages the rat can say when a buff or trap is added to the queue of location checks to send before resuming its normal logic.

    Specify the message itself, or with an optional weight to have that message appear more often (default weight is 1).

    The text {LOCATION} will be replaced with the name of the actual location.

    If you want to disable rat chat, then you're in the wrong place. Do that from the settings menu in the game client itself."""
    display_name = "Messages - Changed Target"

    default = RatChatMessagesHack(
        "Oh, hey, what's that thing over there at {LOCATION}?",
        "There's something at {LOCATION}, I'm sure of it!",
        "Something at {LOCATION} smells good!",
        "There's a rumor that something's going on at {LOCATION}!",
    )


class EnterGoModeMessages(RatChatMessages):
    """What messages the rat can say when it first realizes that it can complete its goal.

    Specify the message itself, or with an optional weight to have that message appear more often (default weight is 1).

    If you want to disable rat chat, then you're in the wrong place. Do that from the settings menu in the game client itself."""
    display_name = "Messages - Go Mode"

    default = RatChatMessagesHack(
        "That's it! I have everything I need! The goal is in sight!",
    )


class EnterBKModeMessages(RatChatMessages):
    """What messages the rat can say when it first sees that no further location checks are in logic.

    Specify the message itself, or with an optional weight to have that message appear more often (default weight is 1).

    If you want to disable rat chat, then you're in the wrong place. Do that from the settings menu in the game client itself."""
    display_name = "Messages - Enter BK Mode"

    default = RatChatMessagesHack(
        "I don't have anything to do right now. Go team!",
        "Hey, I'm completely stuck. But I still believe in you!",
        "I've run out of things to do. How are you?",
        "I'm out of things for now, gonna get a coffee. Anyone want something?",
    )


class RemindBKModeMessages(RatChatMessages):
    """What messages the rat can say to occasionally remind the players that it has no further location checks in logic.

    Specify the message itself, or with an optional weight to have that message appear more often (default weight is 1).

    If you want to disable rat chat, then you're in the wrong place. Do that from the settings menu in the game client itself."""
    display_name = "Messages - Still BK"

    default = RatChatMessagesHack(
        "I don't have anything to do right now. Go team!",
        "Hey, I'm completely stuck. But I still believe in you!",
        "I've run out of things to do. How are you?",
        "I'm out of things for now, gonna get a coffee. Anyone want something?",
    )


class ExitBKModeMessages(RatChatMessages):
    """What messages the rat can say after one or more location checks become in logic.

    Specify the message itself, or with an optional weight to have that message appear more often (default weight is 1).

    If you want to disable rat chat, then you're in the wrong place. Do that from the settings menu in the game client itself."""
    display_name = "Messages - Exit BK"

    default = RatChatMessagesHack(
        "Yippee, that's just what I needed!",
        "I'm back! I knew you could do it!",
        "Sweet, I'm unblocked! Thanks!",
        "Squeak-squeak, it's rattin' time!",
    )


class CompleteGoalMessages(RatChatMessages):
    """What messages the rat can say to celebrate victory.

    Specify the message itself, or with an optional weight to have that message appear more often (default weight is 1).

    If you want to disable rat chat, then you're in the wrong place. Do that from the settings menu in the game client itself."""
    display_name = "Messages - Victory"

    default = RatChatMessagesHack(
        "Yeah, I did it! er... WE did it!",
    )


class LactoseIntolerantMode(Toggle):
    """Replaces all references to lactose-containing products with less offensive ones."""
    display_name = "Lactose Intolerant Mode"


@dataclass
class AutopelagoGameOptions(PerGameCommonOptions):
    fill_with_determination: FillWithDetermination
    victory_location: VictoryLocation
    enabled_buffs: EnabledBuffs
    enabled_traps: EnabledTraps
    msg_changed_target: ChangedTargetMessages
    msg_enter_go_mode: EnterGoModeMessages
    msg_enter_bk: EnterBKModeMessages
    msg_remind_bk: RemindBKModeMessages
    msg_exit_bk: ExitBKModeMessages
    msg_completed_goal: CompleteGoalMessages
    lactose_intolerant: LactoseIntolerantMode

    # not working yet:
    # death_link: DeathLink
    # death_delay_seconds: DeathDelaySeconds
