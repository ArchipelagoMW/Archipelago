from typing import TYPE_CHECKING, ClassVar, NamedTuple

from BaseClasses import (
    CollectionState,
    Entrance,
    Item,
    Location,
    Region,
    Tutorial,
)
from settings import Bool, Group
from worlds.AutoWorld import WebWorld

from .constants import gamename
from .options import HKOptionGroups
from .rules import cost_terms

if TYPE_CHECKING:
    from .resource_state_vars import RCStateVariable


class HKSettings(Group):
    class DisableMapModSpoilers(Bool):
        """Disallows the APMapMod from showing spoiler placements."""

    disable_spoilers: DisableMapModSpoilers | bool = False


class HKWeb(WebWorld):
    setup_en = Tutorial(
        "Mod Setup and Use Guide",
        "A guide to playing Hollow Knight with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ijwu"]
    )

    setup_pt_br = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Português Brasileiro",
        "setup_pt_br.md",
        "setup/pt_br",
        ["JoaoVictor-FA"]
    )

    setup_es = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Español",
        "setup_es.md",
        "setup/es",
        ["GreenMarco", "Panto UwUr"]
    )

    tutorials: ClassVar[list[Tutorial]] = [setup_en, setup_pt_br, setup_es]
    game_info_languages: ClassVar[list[str]] = ["en", "es"]

    bug_report_page = (
        "https://github.com/Ijwu/Archipelago.HollowKnight/issues/new"
        "?assignees=&labels=bug%2C+needs+investigation&template=bug_report.md&title="
    )

    option_groups = HKOptionGroups


class HKClause(NamedTuple):
    # Dict of item: count for state.has_all_counts()
    hk_item_requirements: dict[str, int]

    # list of regions that need to reachable
    hk_region_requirements: list[str]

    # list of resource state terms for the clause
    hk_state_requirements: "list[RCStateVariable]"


# default logicless rule for short circuting
default_hk_rule = [HKClause(
    hk_item_requirements={"True": 1},
    hk_region_requirements=[],
    hk_state_requirements=[],
    )]


def cacheless_hk_access_rule(spot: Location | Entrance, state: CollectionState) -> bool:
    for clause in spot.hk_rule:
        # check regions first when evaluating locations because cache should be set by now
        for region in clause.hk_region_requirements:
            if not state.can_reach_region(region, spot.player):
                return False
        if state.has_all_counts(clause.hk_item_requirements, spot.player):
            if state._hk_apply_and_validate_state(clause, spot.parent_region):
                return True
    # no clause was True,
    return False


class HKLocation(Location):
    game: str = gamename
    costs: dict[str, int] | None  # = None
    vanilla: bool  # = False
    basename: str
    hk_rule: list[HKClause]

    def __init__(
            self, player: int, name: str, code=None, parent=None,
            costs: dict[str, int] | None = None, vanilla: bool = False, basename: str | None = None
    ):
        super().__init__(player, name, code if code else None, parent)
        self.access_set = False
        self.basename = basename or name
        self.vanilla = vanilla
        if costs:
            self.costs = dict(costs)
            self.sort_costs()
        else:
            self.costs = None

    def set_hk_rule(self, rules: list[HKClause]):
        # pass
        self.hk_rule = rules
        self.access_set = True
        # self.current_access_rule = self.hk_access_rule

    def access_rule(self, state: CollectionState) -> bool:
        if self.costs:
            if "GEO" in self.costs and not state.has("Can_Replenish_Geo", self.player):
                return False
            logic_costs = {term: amount for term, amount in self.costs.items() if term != "GEO"}
            if not state.has_all_counts(logic_costs, self.player):
                return False
        return self.hk_access_rule(state) if self.access_set else True

    hk_access_rule = cacheless_hk_access_rule

    def sort_costs(self):
        if self.costs is None:
            return
        self.costs = {k: self.costs[k] for k in sorted(self.costs.keys(), key=lambda x: cost_terms[x].sort)}

    def cost_text(self, separator=" and "):
        if self.costs is None:
            return None
        return separator.join(
            f"{value} {cost_terms[term].singular if value == 1 else cost_terms[term].plural}"
            for term, value in self.costs.items()
        )


class HKItem(Item):
    game = gamename


class HKEntrance(Entrance):
    hk_rule: list[HKClause]
    _er_connected: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._er_connected = False

    def can_reach(self, state: CollectionState) -> bool:
        if not self.connected_region or not self.parent_region:
            # add to blocked_connections for GER
            state.blocked_connections[self.player].add(self)
        return super().can_reach(state)

    def set_hk_rule(self, rules: list[HKClause]):
        if rules == default_hk_rule:
            return
        self.hk_rule = rules
        indirection_connections = [region for clause in rules for region in clause.hk_region_requirements]
        if indirection_connections:
            multiworld = self.parent_region.multiworld
            for region in indirection_connections:
                reg = multiworld.get_region(region, self.player)
                multiworld.register_indirect_condition(reg, self)
        self.access_rule = self.hk_access_rule

    def access_rule(self, state: CollectionState) -> bool:
        state._hk_entrance_clause_cache[self.player][self.name] = {0: True}
        state._hk_apply_and_validate_state(default_hk_rule[0], self.parent_region, target_region=self.connected_region)
        return True

    def hk_access_rule(self, state: CollectionState) -> bool:
        assert self.hk_rule != default_hk_rule, "should never have to be here"
        if self.name not in state._hk_entrance_clause_cache[self.player]:
            # if there's no cache for this entrance, make one with everything False
            cache = state._hk_entrance_clause_cache[self.player][self.name] = \
                dict.fromkeys(range(len(self.hk_rule)), False)
        else:
            cache = state._hk_entrance_clause_cache[self.player][self.name]

        # check every clause, caching item state accessibility and tried resource state modifiers
        valid_clauses = False
        if self.name not in state._hk_checked_state_modifiers[self.player]:
            state._hk_checked_state_modifiers[self.player][self.name] = set()
        terms = state._hk_checked_state_modifiers[self.player][self.name]
        for index, clause in enumerate(self.hk_rule):
            if cache[index] or state.has_all_counts(clause.hk_item_requirements, self.player):
                cache[index] = True
                cur_term = "; ".join(handler.term_name for handler in clause.hk_state_requirements)
                if cur_term in terms:
                    continue
                # region sweep might not be done, so checking items is likely faster
                reachable = True
                for region in clause.hk_region_requirements:
                    if not state.can_reach_region(region, self.player):
                        reachable = False
                if reachable:
                    terms.add(cur_term)
                    if state._hk_apply_and_validate_state(
                            clause,
                            self.parent_region,
                            target_region=self.connected_region):
                        valid_clauses = True

        return valid_clauses


class HKRegion(Region):
    entrance_type = HKEntrance

    def can_reach(self, state) -> bool:
        if state._hk_stale[self.player]:
            # TODO: we may be able to return to only sweeping if self is not cached reachable
            # if we can reasonably kick off a sweep in location can_reach only when required
            state._hk_sweep(self.player)

        return self in state.reachable_regions[self.player]
