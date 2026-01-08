import typing
from dataclasses import dataclass
from enum import IntEnum
from typing import Type, List, Dict

from Options import (Choice, DeathLink, PerGameCommonOptions, StartInventoryPool, Toggle, Range, OptionSet,
                     DefaultOnToggle, NamedRange)
from .Data import Locations
from .Data.Regions import Red_Cave


class SmallKeyMode(Choice):
    """
    Select how the small keys will be handled.
    [Unlocked] The key-locked gates in each dungeon will open automatically.
    [Small Keys] Small keys act like they do in the original game. Each opens one gate.
    [Key Rings] Only one key ring item is required to open every key-locked gate in a dungeon.
    """
    display_name = "Small Key Mode"
    option_unlocked = 0
    option_small_keys = 1
    option_key_rings = 2
    default = 1


class SmallKeyShuffle(Choice):
    """
    Select how the small keys or key rings will be randomized. Does nothing when small key mode is set to unlocked.
    [Vanilla] The small keys will be placed in the vanilla locations.
    [Original Dungeon] The small keys will be shuffled within their own dungeons.
    [Own World] The small keys will be shuffled within your own world.
    [Any World] The small keys will be shuffled throughout the entire multiworld.
    [Different World] The small keys will specifically be shuffled into other players' worlds.
    """
    display_name = "Shuffle Small Keys"
    option_vanilla = 0
    option_original_dungeon = 2
    option_own_world = 3
    option_any_world = 4
    option_different_world = 5
    default = 2


class BigKeyShuffle(Choice):
    """
    Select how the big keys will be randomized.
    [Vanilla] The big keys will be placed in the vanilla locations.
    [Unlocked] The big key gates will open automatically.
    [Own World] The big keys will be shuffled within your own world.
    [Any World] The big keys will be shuffled throughout the entire multiworld.
    [Different World] The big keys will specifically be shuffled into other players' worlds.
    """
    display_name = "Shuffle Big Keys"
    option_vanilla = 0
    option_unlocked = 1
    option_own_world = 3
    option_any_world = 4
    option_different_world = 5
    default = 4


class HealthCicadaShuffle(Choice):
    """
    Select how the health cicadas will be randomized.
    [Vanilla] The health cicadas will not be locations.
    [Own World] Health cicadas will be locations, and the items will be shuffled within your world.
    [Any World] The health cicadas will be shuffled throughout the entire multiworld.
    [Different World] The health cicadas will specifically be shuffled into other players' worlds.
    """
    display_name = "Shuffle Health Cicadas"
    option_vanilla = 0
    option_own_world = 1
    option_any_world = 2
    option_different_world = 3
    default = 2


class Dustsanity(Toggle):
    """
    Select if picking up dust counts as a check.
    [Off] Dust behaves as in the normal game.
    [On] Picking up dust counts as a check the first time it gets picked up by a broom. Dust will appear gold if it has yet to be picked up.
    """
    display_name = "Dustsanity"


class RedCaveAccess(Choice):
    """
    Select how progression through the Red Grotto dungeon should be handled.
    [Progressive] Three Progressive Red Grotto items will be added to the pool, and each will open the next section of the dungeon, in the following order: left, right, top.
    [Original Dungeon] Same as above, but the progression items will be restricted to the original dungeon.
    [Vanilla] The Red Grotto will open up the same way it does in vanilla. The red tentacles will not be location checks.
    """
    display_name = f"{Red_Cave.area_name()} Access"
    option_progressive = 0
    option_original_dungeon = 1
    option_vanilla = 2
    default = 0


class SplitWindmill(Toggle):
    """
    Select how the Windmill behaves.
    [Off] The Windmill behaves as it does in vanilla. Turning it on moves the three statues blocking access to the lategame dungeons.
    [On] The Windmill doesn't do anything special, and instead becomes a location. Three items are added to the pool, one for each dungeon statue.
    """
    display_name = "Split Windmill"


class IncludeBlueAndHappy(Toggle):
    """
    Select how Blue and Happy activation works
    [Off] Blue and Happy behave like in vanilla. You need to complete the gauntlets and open the dams to fight Briar.
    [On] The Blue and Happy dams become items that both need to be found to fight Briar. Both gauntlets have random items at the end.
    """
    display_name = "Include Blue and Happy"


class StartBroom(Choice):
    """Select which broom to start with."""
    display_name = "Starting Broom"
    option_none = 0
    option_normal = 1
    option_wide = 2
    option_long = 3
    option_swap = 4
    default = 0


class NexusGateShuffle(Choice):
    """
    Determines how nexus gates and warp pads work.
    If enabled, nexus gates will become items, and warp pads will become locations.
    Nexus gates that are pre-opened are excluded from this.
    The "All Except Endgame" option excludes the GO, Blue, and Happy gates / pads.
    """
    display_name = "Shuffle Nexus Gates"
    option_off = 0
    option_all_except_endgame = 1
    option_all = 2
    default = 0
    alias_false = 0
    alias_true = 1


class NexusGatesOpen(Choice):
    """
    Select which Nexus Gates are open from the start. Street is always open.
    [Street Only] Only the Street gate is open.
    [Street and Fields] The Street and Fields gates are open.
    [Early] The gates for pre-dungeon areas near Fields are also open.
    [Random Count] A number of random gates will be open. The number is specified in another option.
    [Random Pre-Endgame] Same as above, but the GO, Blue, and Happy gates are excluded.
    """
    display_name = "Open Nexus Gates"
    option_street_only = 0
    option_street_and_fields = 1
    option_early = 2
    option_all = 3
    option_random_count = 4
    option_random_pre_endgame = 5
    default = 1


class RandomNexusGateOpenCount(Range):
    """
    The amount of random Nexus Gates to be opened from the start. Only has an effect if Nexus Gates is set to random.
    """
    display_name = "Random Open Nexus Gates Count"
    range_start = 1
    range_end = len(Locations.nexus_pad_locations)
    default = 4


class CustomNexusGatesOpen(OptionSet):
    """
    Specify specific Nexus Gates to open from the start.
    If set, this will override the value of nexus_gates_open.
    Note that the Street Nexus Gate will always be open.
    """
    display_name = "Custom Open Nexus Gates"
    valid_keys = set(location.region.area_name() for location in Locations.nexus_pad_locations)


class VictoryCondition(Choice):
    """
    Select the end goal of your game.
    [Defeat Briar] Reach the credits screen after defeating the Briar.
    [Final Gate] Open the final gate in the top section of the Nexus and interact with the console beyond it. Postgame must be enabled for this, else the goal will revert to Briar.
    """
    display_name = "Victory Condition"
    option_defeat_briar = 0
    option_final_gate = 1
    default = 0


class FieldsSecretPaths(Toggle):
    """
    Toggles whether the secret paths towards three of the secret chests in Fields are in logic without Expanded Swap.
    """
    display_name = "Fields Secret Paths"


class GateType(IntEnum):
    UNLOCKED = 0
    CARDS = 1
    GREEN = 2
    RED = 3
    BLUE = 4
    BOSSES = 5


class GateRequirements:
    name: str

    @classmethod
    def typename(cls):
        return cls.name.lower().replace(' ', '_') + '_gate'

    @classmethod
    def cardname(cls):
        return cls.typename() + '_cards'

    @classmethod
    def bossname(cls):
        return cls.typename() + '_bosses'

    @classmethod
    def typeoption(cls, options: 'AnodyneGameOptions'):
        return typing.cast(cls.Gate, options.__getattribute__(cls.typename()))

    @classmethod
    def cardoption(cls, options: 'AnodyneGameOptions'):
        return typing.cast(cls.GateCardReq, options.__getattribute__(cls.cardname()))

    @classmethod
    def bossoption(cls, options: 'AnodyneGameOptions'):
        return typing.cast(cls.GateBossReq, options.__getattribute__(cls.bossname()))

    @classmethod
    def shorthand(cls, options: 'AnodyneGameOptions'):
        t = cls.typeoption(options)
        if t == GateType.CARDS:
            num = cls.cardoption(options)
            return f"cards_{num}"
        elif t == GateType.BOSSES:
            num = cls.bossoption(options)
            return f"bosses_{num}"
        return t.current_key

    class Gate(Choice):
        """
        Select the type of the {0} gate. Note that the big key requirements will cause the gate to unlock if the Big Key Shuffle is set to unlocked.
        [Unlocked] This gate starts unlocked.
        [Cards] This gate opens with a number of cards specified in the {0} gate card requirement option.
        [Green Key] This gate opens with the green key.
        [Red Key] This gate opens with the red key.
        [Blue Key] This gate opens with the blue key.
        [Bosses] This gate has a configurable amount of bosses required to be defeated, specified in the {0} gate boss requirement option.
        """
        option_unlocked = int(GateType.UNLOCKED)
        option_cards = int(GateType.CARDS)
        option_green_key = int(GateType.GREEN)
        option_red_key = int(GateType.RED)
        option_blue_key = int(GateType.BLUE)
        option_bosses = int(GateType.BOSSES)

    class GateCardReq(Range):
        """
        Choose how many cards are required to open the {0} gate. Postgame must be enabled to choose a number above 37 for all but the nexus and final gates.
        """
        range_start = 1
        range_end = 49

    class GateBossReq(Range):
        """
        Choose how many bosses are required to open the {0} gate. Boss rush kills don't count for this.
        """
        range_start = 1
        range_end = 8
        default = 1


gatereq_classes: List[Type[GateRequirements]] = []
gate_lookup: Dict[str, Type[GateRequirements]] = dict()


def gate_req(gate_type: GateType, cards: int = 1):
    def decorator(cls: Type[GateRequirements]):
        # Need to reset module from abc to this module, and put the classes into global scope to make pickle work on them
        cls.Gate = type(f"{cls.__name__}_Type", (cls.Gate,),
                        {"__doc__": cls.Gate.__doc__.format(cls.name), "default": int(gate_type),
                         '__module__': __name__})

        cls.GateCardReq = type(f"{cls.__name__}_CardReq", (cls.GateCardReq,),
                               {"__doc__": cls.GateCardReq.__doc__.format(cls.name), "default": cards,
                                '__module__': __name__})
        cls.GateBossReq = type(f"{cls.__name__}_BossReq", (cls.GateBossReq,),
                               {"__doc__": cls.GateBossReq.__doc__.format(cls.name), '__module__': __name__})
        globals()[cls.Gate.__name__] = cls.Gate
        globals()[cls.GateCardReq.__name__] = cls.GateCardReq
        globals()[cls.GateBossReq.__name__] = cls.GateBossReq
        gatereq_classes.append(cls)
        gate_lookup[cls.typename()] = cls
        return cls

    return decorator


def add_options(cls: Type[PerGameCommonOptions]):
    for c in gatereq_classes:
        cls.__annotations__.update({
            c.typename(): c.Gate,
            c.cardname(): c.GateCardReq,
            c.bossname(): c.GateBossReq
        })
    return cls


@gate_req(GateType.CARDS, 4)
class OverworldGauntletGate(GateRequirements):
    name = "Overworld Gauntlet"


@gate_req(GateType.GREEN)
class OverworldFieldsGate(GateRequirements):
    name = "Overworld Fields"


@gate_req(GateType.RED)
class FieldsGate(GateRequirements):
    name = "Fields Terminal"


@gate_req(GateType.CARDS, 8)
class BeachGauntletGate(GateRequirements):
    name = "Beach Gauntlet"


@gate_req(GateType.GREEN)
class WindmillEntranceGate(GateRequirements):
    name = "Windmill Entrance"


@gate_req(GateType.RED)
class WindmillMiddleGate(GateRequirements):
    name = "Windmill Middle"


@gate_req(GateType.BLUE)
class WindmillTopGate(GateRequirements):
    name = "Windmill Top"


@gate_req(GateType.CARDS, 16)
class SuburbGate(GateRequirements):
    name = "Suburb"


@gate_req(GateType.CARDS, 24)
class CellGate(GateRequirements):
    name = "Cell"


@gate_req(GateType.CARDS, 36)
class EndgameRequirement(GateRequirements):
    name = "Terminal Endgame"


@gate_req(GateType.CARDS, 47)
class PostgameBlank(GateRequirements):
    name = "Blank Postgame"


@gate_req(GateType.CARDS, 49)
class PostgameEnd(GateRequirements):
    name = "Nexus North Final"


class RandomizeColorPuzzle(DefaultOnToggle):
    """
    If enabled, the GO color block puzzle is randomized, and the player needs to beat each of the late game bosses to find the correct solution.
    If disabled, the vanilla solution is used, and the dungeons are not logically required to beat the game.
    """
    display_name = "Randomize GO Color Puzzle"


class PostgameMode(Choice):
    """
    Determines how the Swap upgrade behaves.
    Note that even when "Expanded Swap" is available, Swap will not work in almost every room the way it does in the base game. It will be limited to rooms near postgame content, so that you can reach those checks/areas without breaking the rest of the game's logic.
    [Disabled] Swap is only used to access the top half of GO, and all postgame areas will be removed from logic.
    [Vanilla] Expanded Swap unlocks upon defeating Briar.
    [Unlocked] Expanded Swap is automatically available upon receiving the Swap item.
    [Progressive] The first Progressive Swap will behave like pre-Briar Swap, and the second is the Expanded Swap.
    """
    display_name = "Postgame Mode"
    option_disabled = 0
    option_vanilla = 1
    option_unlocked = 2
    option_progressive = 3
    default = 0


class IncludeForestBunnyChest(Toggle):
    """Include the chest that forces you to wait almost 2 hours to access it."""
    display_name = "Include Forest Bunny Chest"


class TrapPercentage(Range):
    """Determines how many traps will be generated."""
    display_name = "Traps Percentage"
    range_end = 100
    default = 25


class CardAmount(NamedRange):
    """
    Sets the amount of cards available in the item pool.
    If there are not enough locations or card slots available when "Extra cards" is added, this number will automatically get lowered.
    This setting will then be used as the actual maximum for card requirements of any big gates in logic.
    Special values:
    [Vanilla] 37 with postgame disabled, 49 otherwise.
    [Auto] Maximum of all in-logic big card gates(postgame gates excluded if postgame is disabled).
    """
    display_name = "Base cards in item pool"
    option_vanilla = -1
    option_auto = -2
    range_start = 0
    range_end = 49
    default = option_vanilla
    special_range_names = {
        "vanilla": -1,
        "auto": -2,
    }


class ExtraCardAmount(Range):
    """
    Sets the amount of extra cards in the item pool. Note that this setting combined with "Base cards in item pool"
    will never exceed the maximum of 49 cards.
    """
    range_start = 0
    range_end = 49
    default = 0


class MitraHints(Choice):
    """
    Sets how Mitra's hints work. She gives one free hint and then gives additional hints after defeating bosses.
    [None] Mitra does not give any hints.
    [Vague] Mitra only tells you the location of a progression item, but not what it is.
    [Precise] Mitra tells you the exact location of one of your progression items.
    [Precise Hint] Same as Precise, but will be sent out as a hint.
    """
    display_name = "Mitra Hint Mode"
    option_none = 0
    option_vague = 1
    option_precise = 2
    option_precise_hint = 3
    default = 1


@dataclass
@add_options
class AnodyneGameOptions(PerGameCommonOptions):
    # Game Options
    start_broom: StartBroom
    victory_condition: VictoryCondition
    postgame_mode: PostgameMode
    mitra_hints: MitraHints
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    # Key Logic
    small_key_mode: SmallKeyMode
    small_key_shuffle: SmallKeyShuffle
    big_key_shuffle: BigKeyShuffle
    # Cards
    card_amount: CardAmount
    extra_cards: ExtraCardAmount
    # Logic Changes
    split_windmill: SplitWindmill
    include_blue_happy: IncludeBlueAndHappy
    fields_secret_paths: FieldsSecretPaths
    randomize_color_puzzle: RandomizeColorPuzzle
    nexus_gate_shuffle: NexusGateShuffle
    red_grotto_access: RedCaveAccess
    # Starting Nexus Gates
    nexus_gates_open: NexusGatesOpen
    random_nexus_gate_open_count: RandomNexusGateOpenCount
    custom_nexus_gates_open: CustomNexusGatesOpen
    # Extra Locations
    dustsanity: Dustsanity
    health_cicada_shuffle: HealthCicadaShuffle
    forest_bunny_chest: IncludeForestBunnyChest
    # Filler Items
    traps_percentage: TrapPercentage
