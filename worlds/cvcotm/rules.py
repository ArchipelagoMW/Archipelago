from typing import Dict, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import CollectionRule
from .data import iname, lname
from .options import CompletionGoal, IronMaidenBehavior

if TYPE_CHECKING:
    from . import CVCotMWorld


class CVCotMRules:
    player: int
    world: "CVCotMWorld"
    rules: Dict[str, CollectionRule]
    required_last_keys: int
    iron_maiden_behavior: int
    nerf_roc_wing: int
    ignore_cleansing: int
    completion_goal: int

    def __init__(self, world: "CVCotMWorld") -> None:
        self.player = world.player
        self.world = world
        self.required_last_keys = world.required_last_keys
        self.iron_maiden_behavior = world.options.iron_maiden_behavior.value
        self.nerf_roc_wing = world.options.nerf_roc_wing.value
        self.ignore_cleansing = world.options.ignore_cleansing.value
        self.completion_goal = world.options.completion_goal.value

        self.location_rules = {
            # Sealed Room
            lname.sr3: self.has_jump_level_5,
            # Catacomb
            lname.cc1: self.has_push,
            lname.cc3: self.has_jump_level_1,
            lname.cc3b: lambda state:
                (self.has_jump_level_1(state) and self.has_ice_or_stone(state)) or self.has_jump_level_4(state),
            lname.cc5: self.has_tackle,
            lname.cc8b: lambda state: self.has_jump_level_3(state) or self.has_kick(state),
            lname.cc14b: lambda state: self.has_jump_level_1(state) or self.has_kick(state),
            lname.cc25: self.has_jump_level_1,
            # Abyss Staircase
            lname.as4: self.has_jump_level_4,
            # Audience Room
            lname.ar9: self.has_push,
            lname.ar11: self.has_tackle,
            lname.ar14b: self.has_jump_level_4,
            lname.ar17b: lambda state: self.has_jump_level_2(state) or self.has_kick(state),
            lname.ar19: lambda state: self.has_jump_level_2(state) or self.has_kick(state),
            lname.ar26: lambda state: self.has_tackle(state) and self.has_jump_level_5(state),
            lname.ar27: lambda state: self.has_tackle(state) and self.has_push(state),
            lname.ar30: lambda state:
                (self.has_jump_level_3(state) and self.has_ice_or_stone(state)) or self.has_jump_level_4(state),
            lname.ar30b: lambda state:
                (self.has_jump_level_3(state) and self.has_ice_or_stone(state)) or self.has_jump_level_4(state),
            # Outer Wall
            lname.ow0: self.has_jump_level_4,
            lname.ow1: lambda state: self.has_jump_level_5(state) or self.has_ice_or_stone(state),
            # Triumph Hallway
            lname.th3: lambda state:
                (self.has_kick(state) and self.has_ice_or_stone(state)) or self.has_jump_level_2(state),
            # Machine Tower
            lname.mt3: lambda state: self.has_jump_level_2(state) or self.has_kick(state),
            lname.mt6: lambda state: self.has_jump_level_2(state) or self.has_kick(state),
            lname.mt14: self.has_tackle,
            # Chapel Tower
            lname.ct1: lambda state: self.has_jump_level_2(state) or self.has_ice_or_stone(state),
            lname.ct4: self.has_push,
            lname.ct10: self.has_push,
            lname.ct13: lambda state: self.has_jump_level_2(state) or self.has_ice_or_stone(state),
            lname.ct22: self.broke_iron_maidens,
            lname.ct26: lambda state:
                (self.has_jump_level_3(state) and self.has_ice_or_stone(state)) or self.has_jump_level_4(state),
            lname.ct26b: lambda state:
                (self.has_jump_level_3(state) and self.has_ice_or_stone(state)) or self.has_jump_level_4(state),
            # Underground Gallery
            lname.ug1: self.has_push,
            lname.ug2: self.has_push,
            lname.ug3: lambda state: self.has_jump_level_2(state) or self.has_ice_or_stone(state),
            lname.ug3b: lambda state: self.has_jump_level_4(state) or self.has_ice_or_stone(state),
            lname.ug8: self.has_tackle,
            # Underground Warehouse
            lname.uw10: lambda state:
                (self.has_jump_level_4(state) and self.has_ice_or_stone(state)) or self.has_jump_level_5(state),
            lname.uw14: lambda state: self.has_jump_level_2(state) or self.has_ice_or_stone(state),
            lname.uw16b: lambda state:
                (self.has_jump_level_2(state) and self.has_ice_or_stone(state)) or self.has_jump_level_3(state),
            # Underground Waterway
            lname.uy5: lambda state: self.has_jump_level_3(state) or self.has_ice_or_stone(state),
            lname.uy8: self.has_jump_level_2,
            lname.uy12b: self.can_touch_water,
            lname.uy17: self.can_touch_water,
            lname.uy13: self.has_jump_level_3,
            lname.uy18: self.has_jump_level_3,
            # Ceremonial Room
            lname.cr1: lambda state: self.has_jump_level_2(state) or self.has_kick(state),
            lname.dracula: self.has_jump_level_2,
        }

        self.entrance_rules = {
            "Catacomb to Stairway": lambda state: self.has_jump_level_1(state) or self.has_kick(state),
            "Stairway to Audience": self.has_jump_level_1,
            "Audience to Machine Bottom": self.has_tackle,
            "Audience to Machine Top": lambda state: self.has_jump_level_2(state) or self.has_kick(state),
            "Audience to Chapel": lambda state:
                (self.has_jump_level_2(state) and self.has_ice_or_stone(state)) or self.has_jump_level_3(state)
                or self.has_kick(state),
            "Audience to Gallery": lambda state: self.broke_iron_maidens(state) and self.has_push(state),
            "Audience to Warehouse": self.has_push,
            "Audience to Waterway": self.broke_iron_maidens,
            "Audience to Observation": self.has_jump_level_5,
            "Ceremonial Door": self.can_open_ceremonial_door,
            "Corridor to Gallery": self.broke_iron_maidens,
            "Escape the Gallery Pit": lambda state: self.has_jump_level_2(state) or self.has_kick(state),
            "Climb to Chapel Top": lambda state: self.has_jump_level_3(state) or self.has_kick(state),
            "Arena Passage": lambda state: self.has_push(state) and self.has_jump_level_2(state),
            "Dip Into Waterway End": self.has_jump_level_3,
            "Gallery Upper to Lower": self.has_tackle,
            "Gallery Lower to Upper": self.has_tackle,
            "Into Warehouse Main": self.has_tackle,
            "Into Waterway Main": self.can_touch_water,
        }

    def has_jump_level_1(self, state: CollectionState) -> bool:
        """Double or Roc Wing, regardless of Roc being nerfed or not."""
        return state.has_any([iname.double, iname.roc_wing], self.player)

    def has_jump_level_2(self, state: CollectionState) -> bool:
        """Specifically Roc Wing, regardless of Roc being nerfed or not."""
        return state.has(iname.roc_wing, self.player)

    def has_jump_level_3(self, state: CollectionState) -> bool:
        """Roc Wing and Double OR Kick Boots if Roc is nerfed. Otherwise, just Roc."""
        if self.nerf_roc_wing:
            return state.has(iname.roc_wing, self.player) and \
                   state.has_any([iname.double, iname.kick_boots], self.player)
        else:
            return state.has(iname.roc_wing, self.player)

    def has_jump_level_4(self, state: CollectionState) -> bool:
        """Roc Wing and Kick Boots specifically if Roc is nerfed. Otherwise, just Roc."""
        if self.nerf_roc_wing:
            return state.has_all([iname.roc_wing, iname.kick_boots], self.player)
        else:
            return state.has(iname.roc_wing, self.player)

    def has_jump_level_5(self, state: CollectionState) -> bool:
        """Roc Wing, Double, AND Kick Boots if Roc is nerfed. Otherwise, just Roc."""
        if self.nerf_roc_wing:
            return state.has_all([iname.roc_wing, iname.double, iname.kick_boots], self.player)
        else:
            return state.has(iname.roc_wing, self.player)

    def has_tackle(self, state: CollectionState) -> bool:
        return state.has(iname.tackle, self.player)

    def has_push(self, state: CollectionState) -> bool:
        return state.has(iname.heavy_ring, self.player)

    def has_kick(self, state: CollectionState) -> bool:
        return state.has(iname.kick_boots, self.player)

    def has_ice_or_stone(self, state: CollectionState) -> bool:
        """Valid DSS combo that allows freezing or petrifying enemies to use as platforms."""
        return state.has_any([iname.serpent, iname.cockatrice], self.player) and \
            state.has_any([iname.mercury, iname.mars], self.player)

    def can_touch_water(self, state: CollectionState) -> bool:
        """Cleansing unless it's ignored, in which case this will always return True."""
        return self.ignore_cleansing or state.has(iname.cleansing, self.player)

    def broke_iron_maidens(self, state: CollectionState) -> bool:
        """Maiden Detonator unless the Iron Maidens start broken, in which case this will always return True."""
        return (self.iron_maiden_behavior == IronMaidenBehavior.option_start_broken
                or state.has(iname.ironmaidens, self.player))

    def can_open_ceremonial_door(self, state: CollectionState) -> bool:
        """The required number of Last Keys. If 0 keys are required, this should always return True."""
        return state.has(iname.last_key, self.player, self.required_last_keys)

    def set_cvcotm_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            # Set each Entrance's rule if it should have one.
            for ent in region.entrances:
                if ent.name in self.entrance_rules:
                    ent.access_rule = self.entrance_rules[ent.name]

            # Set each Location's rule if it should have one.
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]

        # Set the World's completion condition depending on what its Completion Goal option is.
        if self.completion_goal == CompletionGoal.option_dracula:
            multiworld.completion_condition[self.player] = lambda state: state.has(iname.dracula, self.player)
        elif self.completion_goal == CompletionGoal.option_battle_arena:
            multiworld.completion_condition[self.player] = lambda state: state.has(iname.shinning_armor, self.player)
        else:
            multiworld.completion_condition[self.player] = \
                lambda state: state.has_all([iname.dracula, iname.shinning_armor], self.player)
