from dataclasses import dataclass
import logging
from typing import Any, ClassVar, Dict, FrozenSet, List, Union
from typing_extensions import override

from BaseClasses import Item, ItemClassification as IC
from Options import Choice, DefaultOnToggle, FreeText, PerGameCommonOptions, Range, Toggle

from .item import SubversionItem
from .location import location_data

from subversion_rando.areaRando import RandomizeAreas
from subversion_rando.connection_data import vanilla_areas
from subversion_rando.daphne_gate import get_daphne_gate
from subversion_rando.game import CypherItems, Game, GameOptions
from subversion_rando.goal import generate_goals
from subversion_rando.item_data import unique_items
from subversion_rando.item_marker import ItemMarker, ItemMarkersOption
from subversion_rando.logic_presets import casual, expert, medium, custom_logic_tricks_from_str
from subversion_rando.trick import Trick


class SubversionLogic(Choice):
    """
    casual logic - wall jumps, mid-air morph

    expert logic - many advanced tricks and glitches

    medium logic - some common tricks without too much difficulty

    custom logic - customize logic by getting data string here: https://subversionrando.github.io/SubversionRando/
                 - use the custom_logic setting in your yaml with this data string
    """
    option_casual = 0
    option_medium = 1
    option_expert = 2
    option_custom = 3
    default = 0
    display_name = "logic preset"


class SubversionCustomLogic(FreeText):
    """ customize logic by getting data string here: https://subversionrando.github.io/SubversionRando/ """
    display_name = "custom logic string"
    default = "000000000000"

    @override
    @classmethod
    def from_any(cls, data: Any) -> "SubversionCustomLogic":
        if isinstance(data, int):
            # yaml interprets numbers with leading 0 as octal
            # We don't want octal, we want the string.

            # if it's the right number of digits it probably was interpreted as decimal, not octal
            # (octal -> decimal reduces the number of digits or keeps them the same)
            if data >= 100_000_000_000 and data < 1_000_000_000_000:
                return cls(str(data))
            else:
                # convert back to octal
                return cls(oct(data)[2:].zfill(len(SubversionCustomLogic.default)))
        assert isinstance(data, str), f"I don't know how to handle {type(data)} for {cls.__name__}"
        return cls(data)


class SubversionAreaRando(Toggle):
    """ sections of the map are shuffled around """
    display_name = "area rando"


class SubversionSmallSpaceport(DefaultOnToggle):
    """
    This removes some rooms from the spaceport so you don't have to run around as much at the beginning of the seed.

    This also reduces the missile requirements for zebetites, pink doors, and eye doors.
    """
    display_name = "small spaceport"


class SubversionEscapeShortcuts(Toggle):
    """
    The paths during escape sequences are shortened.

    In area rando, the final escape sequence is never shortened.
    (Part of the fun of area rando is finding your way out.)
    """
    display_name = "escape shortcuts"


class SubversionDaphne(Toggle):
    """
    Changes the Screw Attack blocks in the Wrecked Air Lock to two different kinds of blocks,
    so you will need 1 of 2 random items to enter the final area (instead of the normal Screw Attack requirement).

    The items that will let you through the gate are displayed in the Air Lock before it is crashed.
    """
    display_name = "randomize wrecked Daphne gate"


class SubversionShortGame(Choice):
    """ Keep the game from being too long by not putting required items in far away places. """
    display_name = "progression items"
    option_anywhere = 0
    option_not_in_thunder_lab = 1
    option_not_in_suzi = 2
    default = 1

    location_lists: ClassVar[Dict[int, List[str]]] = {
        option_anywhere: [],
        option_not_in_thunder_lab: ["Shrine Of The Animate Spark", "Enervation Chamber"],
        option_not_in_suzi: [
            "Shrine Of The Animate Spark",
            "Enervation Chamber",
            "Reef Nook",
            "Tower Rock Lookout",
            "Portico",
            "Saline Cache",
            "Suzi Ruins Map Station Access",
            "Obscured Vestibule",
            "Tram To Suzi Island"
        ]
    }

    cypher_options: ClassVar[Dict[int, CypherItems]] = {
        option_anywhere: CypherItems.Anything,
        option_not_in_thunder_lab: CypherItems.NotRequired,
        option_not_in_suzi: CypherItems.SmallAmmo
    }
    """
    This is just for its effect on objective rando,
    where SmallAmmo means the map stations in Suzi won't be required.
    """


class SubversionAutoHints(Choice):
    """
    Automatically hint your early progression items
    (likely Gravity Boots, Morph Ball, Missiles - depends on what items you're expected to get first)
    """
    display_name = "hint early items"
    option_none = 0
    option_light = 1
    option_normal = 2
    default = 2
    # I thought about including option_heavy,
    # but I don't like the idea of subversion players
    # pressuring other players with lots of hints

    # this is for backwards compatibility with old yamls
    # (can be removed after some time passes)
    @override
    @classmethod
    def from_text(cls, text: str) -> Choice:  # TODO: fix typing to Self in core
        text = text.lower()
        if text == "true":
            assert isinstance(SubversionAutoHints.default, int)
            return cls(SubversionAutoHints.default)
        elif text == "false":
            return cls(SubversionAutoHints.option_none)
        return super(SubversionAutoHints, cls).from_text(text)


class SubversionTrollAmmo(Toggle):
    """
    When activated, a Super Metroid player's Missiles, Supers, and Power Bombs
    will look the same as your Missiles, Supers, and Power Bombs.

    When not activated, a Super Metroid player's ammo
    will look like generic Archipelago items.
    """
    display_name = "troll ammo"


class SubversionItemMarkers(Choice):
    """
    Simple - Items are marked on the map as large hollow dots.

    3-Tiered - Unique items are marked with large solid dots.
    Ammo tanks are marked with small dots.
    Everything else is marked with large hollow dots.
    """
    display_name = "item markers"
    option_simple = 0
    option_three_tiered = 3
    default = 0

    marker_options: ClassVar[Dict[int, ItemMarkersOption]] = {
        option_simple: ItemMarkersOption.Simple,
        option_three_tiered: ItemMarkersOption.ThreeTiered,
    }

    def get_marker(self, item: Item) -> ItemMarker:
        if self.value == SubversionItemMarkers.option_simple:
            return ItemMarker.circle

        assert self.value == SubversionItemMarkers.option_three_tiered, f"{self.value=}"
        if isinstance(item, SubversionItem):
            sv_item = item.sv_item
            if sv_item in unique_items:
                return ItemMarker.big_dot
            elif sv_item.ammo_qty != b"\x00":
                return ItemMarker.small_dot
            else:
                return ItemMarker.circle
        else:
            if item.classification & IC.progression == IC.progression:
                return ItemMarker.big_dot
            if item.classification & IC.useful == IC.useful:
                return ItemMarker.circle
            else:
                return ItemMarker.small_dot


class SubversionObjectiveRando(Range):
    """
    Choose the number of random objectives.
    0 will have just the normal space port crash objective.

    if greater than 0:
        - Accessing map stations will reveal one of the objectives.
          The objectives are tracked in the Logbook Mission page.

        - Crashing the space port is not required unless it is chosen as one of the objectives.
            - (The GFS Daphne will be both docked at the space port and crashed on the planet at the same time.)

        - The Power Bomb requirement to get to the wrecked Weapon Control Center is also removed.
    """
    display_name = "objective rando"
    range_start = 0
    range_end = 10


@dataclass
class SubversionOptions(PerGameCommonOptions):
    logic_preset: SubversionLogic
    custom_logic: SubversionCustomLogic
    area_rando: SubversionAreaRando
    small_spaceport: SubversionSmallSpaceport
    escape_shortcuts: SubversionEscapeShortcuts
    daphne_gate: SubversionDaphne
    progression_items: SubversionShortGame
    auto_hints: SubversionAutoHints
    troll_ammo: SubversionTrollAmmo
    item_markers: SubversionItemMarkers
    objective_rando: SubversionObjectiveRando


def _make_custom(data: str) -> FrozenSet[Trick]:
    try:
        logic = custom_logic_tricks_from_str(data)
        return logic
    except ValueError:
        logging.info(f'Subversion: invalid custom logic string "{data}" - defaulting to casual logic')
    return casual


def make_sv_game(options: SubversionOptions, seed: Union[int, None]) -> Game:
    logics = {
        SubversionLogic.option_casual: casual,
        SubversionLogic.option_expert: expert,
        SubversionLogic.option_medium: medium,
        SubversionLogic.option_custom: _make_custom(options.custom_logic.value)
    }

    cypher_option = SubversionShortGame.cypher_options[options.progression_items.value]

    sv_options = GameOptions(
        logics[options.logic_preset.value],
        bool(options.area_rando.value),
        "D",  # unused
        bool(options.small_spaceport.value),
        bool(options.escape_shortcuts.value),
        cypher_option,  # used only for objective rando, not for fill
        bool(options.daphne_gate.value),
        SubversionItemMarkers.marker_options[options.item_markers.value],
        options.objective_rando.value
    )

    seed = seed or 0

    connections = RandomizeAreas(False, seed) if sv_options.area_rando else vanilla_areas()

    sv_game = Game(sv_options, location_data, connections, seed)
    if sv_options.daphne_gate:
        daphne_blocks = get_daphne_gate(sv_options)
        sv_game.daphne_blocks = daphne_blocks
    if sv_options.objective_rando > 0:
        goals = generate_goals(sv_options)
        sv_game.goals = goals

    return sv_game
