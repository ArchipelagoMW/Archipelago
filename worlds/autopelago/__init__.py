import logging
import typing
from collections import deque
from collections.abc import Callable, Iterable
from typing import TypeVar

from BaseClasses import CollectionState, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from Options import OptionGroup
from worlds.AutoWorld import WebWorld, World

from .definitions_types import (
    Aura,
    AutopelagoAllRequirement,
    AutopelagoAnyRequirement,
    AutopelagoAnyTwoRequirement,
    AutopelagoGameRequirement,
    AutopelagoItemRequirement,
    AutopelagoNonProgressionItemType,
    AutopelagoRatCountRequirement,
    AutopelagoRegionDefinition,
)
from .items import (
    ENABLED_AURA_SCORE_THRESHOLD,
    classify_item_by_score,
    item_name_to_auras,
    item_name_to_id,
    items_by_game,
    lactose_intolerant_names,
    names_with_lactose,
    nonprogression_item_types,
    progression_item_names,
    score_item_by_auras,
)
from .locations import (
    autopelago_regions,
    item_key_to_name,
    item_name_groups,
    item_name_to_rat_count,
    location_name_groups,
    location_name_to_id,
    location_name_to_nonprogression_item,
    location_name_to_progression_item_name,
    location_name_to_requirement,
    max_required_rat_count,
    total_available_rat_count,
)
from .options import (
    AutopelagoGameOptions,
    ChangedTargetMessages,
    CompleteGoalMessages,
    EnabledBuffs,
    EnabledTraps,
    EnterBKModeMessages,
    EnterGoModeMessages,
    ExitBKModeMessages,
    RemindBKModeMessages,
    VictoryLocation,
)
from .util import GAME_NAME

autopelago_logger = logging.getLogger(GAME_NAME)
T = TypeVar("T")


def _is_trivial(req: AutopelagoGameRequirement):
    if "all" in req:
        return not req["all"]
    if "rat_count" in req:
        return req["rat_count"] == 0
    return False


def _is_satisfied(player: int, req: AutopelagoGameRequirement, state: CollectionState):
    if "all" in req:
        req: AutopelagoAllRequirement
        return all(_is_satisfied(player, sub_req, state) for sub_req in req["all"])
    if "any" in req:
        req: AutopelagoAnyRequirement
        return any(_is_satisfied(player, sub_req, state) for sub_req in req["any"])
    if "any_two" in req:
        req: AutopelagoAnyTwoRequirement
        return sum(1 if _is_satisfied(player, sub_req, state) else 0 for sub_req in req["any_two"]) > 1
    if "item" in req:
        req: AutopelagoItemRequirement
        return state.has(item_key_to_name[req["item"]], player)
    assert "rat_count" in req, "Only AutopelagoRatCountRequirement is expected here"
    req: AutopelagoRatCountRequirement
    return sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[player].items() if
               k in item_name_to_rat_count) >= req["rat_count"]


class AutopelagoItem(Item):
    game = GAME_NAME


class AutopelagoLocation(Location):
    game = GAME_NAME

    def __init__(self, player: int, name: str, parent: Region):
        super().__init__(player, name, location_name_to_id[name] if name in location_name_to_id else None, parent)
        if name in location_name_to_requirement:
            req = location_name_to_requirement[name]
            if not _is_trivial(req):
                self.access_rule = lambda state: _is_satisfied(player, req, state)


class AutopelagoRegion(Region):
    game = GAME_NAME
    autopelago_definition: AutopelagoRegionDefinition

    def __init__(self, autopelago_definition: AutopelagoRegionDefinition, player: int, multiworld: MultiWorld,
                 hint: str | None = None):
        super().__init__(autopelago_definition.key, player, multiworld, hint)
        self.autopelago_definition = autopelago_definition
        self.locations += (AutopelagoLocation(player, loc, self) for loc in autopelago_definition.locations)


class AutopelagoWebWorld(WebWorld):
    theme = "partyTime"
    rich_text_options_doc = True
    tutorials: typing.ClassVar[list[Tutorial]] = [Tutorial(
        tutorial_name="Setup Guide",
        description="A guide to playing Autopelago",
        language="English",
        file_name="setup_en.md",
        link="guide/en",
        authors=["airbreather"]
    )]


class AutopelagoWorld(World):
    """
    Autopelago is a game that plays itself, built specifically to help practice or bulk out your Archipelago multiworld.
    It sends location checks automatically based on customizable time-based intervals and runs entirely in your browser.
    """
    game = GAME_NAME
    topology_present = False  # it's static, so setting this to True isn't actually helpful
    origin_region_name = "before_basketball"
    web = AutopelagoWebWorld()
    options_dataclass = AutopelagoGameOptions
    options: AutopelagoGameOptions
    victory_location: str
    regions_in_scope: set[str]
    locations_in_scope: set[str]
    enabled_auras: set[Aura]
    enabled_auras_by_item_id: dict[int, list[Aura]]
    option_groups: typing.ClassVar[list[OptionGroup]] = [
        OptionGroup("Message Text Replacements", [
            ChangedTargetMessages,
            EnterGoModeMessages,
            EnterBKModeMessages,
            RemindBKModeMessages,
            ExitBKModeMessages,
            CompleteGoalMessages,
        ]),
    ]

    # item_name_to_id and location_name_to_id must be filled VERY early. don't get any ideas about
    # having the user's YAML file dynamically create new items / locations or anything like that. of
    # course, we could still theoretically pre-generate arbitrarily many filler location names if we
    # want to introduce *some* configurability there.
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def __init__(self, multiworld, player):
        self.enabled_auras = set()
        super().__init__(multiworld, player)

    # insert other ClassVar values... suggestions include:
    # - item_descriptions
    # - location_descriptions
    # - hint_blacklist (should it include the goal item?)

    def generate_early(self):
        self.enabled_auras.clear()
        for aura in self.options.enabled_buffs.value:
            self.enabled_auras.add(EnabledBuffs.map[aura])
        for aura in self.options.enabled_traps.value:
            self.enabled_auras.add(EnabledTraps.map[aura])
        self.enabled_auras_by_item_id = {}
        for name, auras in item_name_to_auras.items():
            enabled_auras = [aura for aura in auras if aura in self.enabled_auras]
            if enabled_auras:
                self.enabled_auras_by_item_id[item_name_to_id[name]] = enabled_auras

        match self.options.victory_location:
            case VictoryLocation.option_captured_goldfish:
                self.victory_location = "Captured Goldfish"
            case VictoryLocation.option_secret_cache:
                self.victory_location = "Secret Cache"
            case _:
                self.victory_location = "Snakes on a Planet"

        # work out how many locations are in scope for this playthrough so that create_items can see
        # which progression items are required and which regions are in scope so that we can filter
        # which ones to generate Archipelago stuff for. there isn't a way to play the "unrandomized"
        # version of the game, but there's still some sort of logic to where the definitions file
        # places such "unrandomized" items, exactly to enable this kind of thing.
        self.locations_in_scope = set()
        q = deque((self.origin_region_name,))
        self.regions_in_scope = {self.origin_region_name,}
        while q:
            r = autopelago_regions[q.popleft()]
            locations_set = set(r.locations)
            self.locations_in_scope.update(locations_set)
            if self.victory_location in locations_set:
                # don't go beyond the victory location (all "exits" are considered "forward")
                continue
            for next_exit in r.exits:
                if next_exit in self.regions_in_scope:
                    continue
                self.regions_in_scope.add(next_exit)
                q.append(next_exit)

    def create_item(self, name: str):
        item_id = item_name_to_id[name]
        classification = \
            ItemClassification.progression if name in progression_item_names else \
            classify_item_by_score(score_item_by_auras(name, self.enabled_auras))
        return AutopelagoItem(name, classification, item_id, self.player)

    def create_items(self):
        new_items = [self.create_item(item)
                     for location, item in location_name_to_progression_item_name.items()
                     if location in self.locations_in_scope and item != "Moon Shoes"]

        # skip balancing for the pack_rat items that take us beyond the minimum limit
        rat_items = sorted(
            (item for item in new_items if item.name in item_name_to_rat_count),
            key=lambda item: (item_name_to_rat_count[item.name], 0 if item.name == item_key_to_name["pack_rat"] else 1)
        )
        for i in range(total_available_rat_count - max_required_rat_count):
            assert rat_items[i].name == item_key_to_name["pack_rat"],\
                "Expected there to be enough pack_rat fillers for this calculation."
            rat_items[i].classification |= ItemClassification.skip_balancing
        # deprioritize ALL pack_rat items.
        for item in rat_items:
            if item.name == item_key_to_name["pack_rat"]:
                item.classification |= ItemClassification.deprioritized

        self.multiworld.itempool += new_items
        excluded_names: set[str] = set(
            names_with_lactose if self.options.lactose_intolerant.value else
            lactose_intolerant_names
        )

        # nonprogression items are tricky. even just picking an item to fill a slot that's marked as
        # a buff/trap/filler is nontrivial because buffs and traps can be disabled arbitrarily.
        item_pools = { k: self._sort_nonprogression_items_for_item_type(k) for k in nonprogression_item_types }
        next_item_indices = dict.fromkeys(nonprogression_item_types, 0)

        # none of the "unrandomized" items at our locations actually say "trap"; instead, half of
        # the time we're asked for a "filler", we actually mean "trap" instead.
        next_filler_becomes_trap = False
        for loc, original_item_type in location_name_to_nonprogression_item.items():
            if loc not in self.locations_in_scope:
                continue

            item_type = original_item_type
            if item_type == "filler":
                if next_filler_becomes_trap:
                    item_type: AutopelagoNonProgressionItemType = "trap"
                next_filler_becomes_trap = not next_filler_becomes_trap

            item_pool = item_pools[item_type]
            next_item_index = next_item_indices[item_type]
            while next_item_index < len(item_pool):
                next_item = item_pool[next_item_index]
                next_item_index += 1
                if next_item in excluded_names:
                    continue
                self.multiworld.itempool.append(self.create_item(next_item))
                excluded_names.add(next_item)
                next_item_indices[item_type] = next_item_index
                break

    def create_regions(self):
        victory_region = Region("Victory", self.player, self.multiworld)
        self.multiworld.regions.append(victory_region)
        self.multiworld.completion_condition[self.player] =\
            lambda state: state.can_reach(victory_region)

        new_regions = {r.key: AutopelagoRegion(r, self.player, self.multiworld)
                       for key, r in autopelago_regions.items()
                       if key in self.regions_in_scope}
        for r in new_regions.values():
            self.multiworld.regions.append(r)
            req = r.autopelago_definition.requires
            rule: Callable[[CollectionState], bool] | None
            # disable PLC3002: the lambda must use the CURRENT value of 'req', so it needs a new scope somehow.
            rule = None if _is_trivial(req) \
                else (lambda req_: lambda state: _is_satisfied(self.player, req_, state))(req) # noqa: PLC3002
            if self.victory_location in r.autopelago_definition.locations:
                r.connect(victory_region, rule=rule)
                if self.options.victory_location == VictoryLocation.option_snakes_on_a_planet:
                    r.locations[0].place_locked_item(self.create_item("Moon Shoes"))
            else:
                for next_exit in r.autopelago_definition.exits:
                    r.connect(new_regions[next_exit], rule=rule)

    def get_filler_item_name(self):
        assert "Nothing" in self.item_name_to_id
        return "Nothing"

    def fill_slot_data(self):
        return {
            # version_stamp was more important in versions where you had to download an EXE file and
            # make sure it's compatible with the version of the APWorld file that was used. all it's
            # used for today is to give 0.10.x clients a string that they definitely don't expect so
            # that they can throw a semi-graceful error message.
            "version_stamp": "1.0.0",
            "victory_location_name": self.victory_location,
            "msg_changed_target": self.options.msg_changed_target.value,
            "msg_enter_go_mode": self.options.msg_enter_go_mode.value,
            "msg_enter_bk": self.options.msg_enter_bk.value,
            "msg_remind_bk": self.options.msg_remind_bk.value,
            "msg_exit_bk": self.options.msg_exit_bk.value,
            "msg_completed_goal": self.options.msg_completed_goal.value,
            "lactose_intolerant": bool(self.options.lactose_intolerant),

            # added in 1.0.0 so the client only needs to bake in items unlocking specific locations
            "auras_by_item_id": self.enabled_auras_by_item_id,
            "rat_counts_by_item_id": {
                item_name_to_id[name]: rat_count for name, rat_count in item_name_to_rat_count.items()
            },

            # obsolete in 1.0.0 (auras_by_item_id does the same thing) but kept for 0.11.x client support:
            "enabled_buffs": [EnabledBuffs.map[b] for b in self.options.enabled_buffs.value],
            "enabled_traps": [EnabledTraps.map[t] for t in self.options.enabled_traps.value],

            # not working yet:
            # "death_link": bool(self.options.death_link),
            # "death_delay_seconds": self.options.death_delay_seconds - 0,
        }

    def _sort_nonprogression_items_for_item_type(self, item_type: AutopelagoNonProgressionItemType):
        """
        Returns a list of ALL non-progression items, sorted by how appropriate it would be to fill a
        slot that expects an item of a given type.
        """
        items_for_base_game = self._shuffled(items_by_game[GAME_NAME])
        included_games = set(self.multiworld.game.values()) - { GAME_NAME }
        items_for_included_games = self._shuffled(
            item for g, items in items_by_game.items()
                for item in items
            if g in included_games
        )
        items_for_excluded_games = self._shuffled(
            item for g, items in items_by_game.items()
                for item in items
            if g not in included_games
        )

        # all ideal items (true buffs when we're asked for buffs, true traps when we're asked for
        # traps, true fillers when we're asked for fillers) come first, starting with the Easter egg
        # items for games present in the multiworld, followed by base game items. Easter egg items
        # for excluded games will be used only as a last resort.
        #
        # "true buff" = an item whose enabled auras are net positive
        # "true trap" = an item whose enabled auras are net negative
        # "true filler" = an item whose enabled aura effects cancel out AND whose disabled aura
        #                 effects also cancel out.
        # the remaining items are fillers, but not "true"
        items: list[str] = []
        for items_list in (items_for_included_games, items_for_base_game):
            items += (
                item for item in items_list
                if self._distance_from_ideal(item_type, item) == 0
            )

        # if item_type is "filler", then now is the time to add the non-"true" ones.
        for items_list in (items_for_included_games, items_for_base_game):
            items += (
                item for item in items_list
                if 0 < self._distance_from_ideal(item_type, item) < ENABLED_AURA_SCORE_THRESHOLD
            )

        # fill in the values for excluded games as a last resort before we move onto things like
        # yielding fillers when we're asked for traps / buffs
        items += (
                item for item in items_for_excluded_games
                if self._distance_from_ideal(item_type, item) == 0
        )
        items += (
                item for item in items_for_excluded_games
                if 0 < self._distance_from_ideal(item_type, item) < ENABLED_AURA_SCORE_THRESHOLD
        )

        # when all buffs and all traps are enabled, we don't even come close to exhausting the lists
        # of "ideal" items we built above. once things start getting disabled, we have to dip into
        # filler items to complete that list. depending on how things will evolve in the future, we
        # might even need to go beyond the fillers, so let's just extend this out to EVERYTHING that
        # we can POSSIBLY draw from.
        for items_list in (items_for_included_games, items_for_base_game, items_for_excluded_games):
            items += sorted((
                item for item in items_list
                if self._distance_from_ideal(item_type, item) >= ENABLED_AURA_SCORE_THRESHOLD
            ), key=lambda val: self._distance_from_ideal(item_type, val))
        return items

    def _distance_from_ideal(self, item_type: AutopelagoNonProgressionItemType, item: str):
        score = score_item_by_auras(item, self.enabled_auras)
        match item_type:
            case "useful_nonprogression":
                return 0 if score > ENABLED_AURA_SCORE_THRESHOLD else abs(score) + (ENABLED_AURA_SCORE_THRESHOLD * 2)
            case "trap":
                return 0 if score < -ENABLED_AURA_SCORE_THRESHOLD else abs(score) + (ENABLED_AURA_SCORE_THRESHOLD * 2)
            case _:
                return abs(score)

    def _shuffled(self, items: Iterable[T]) -> list[T]:
        to_shuffle = list(items)
        self.multiworld.random.shuffle(to_shuffle)
        return to_shuffle
