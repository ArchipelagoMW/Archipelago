from abc import ABC, abstractmethod
from enum import IntEnum
from json import JSONEncoder
from typing import TYPE_CHECKING

from BaseClasses import CollectionState

from worlds.generic.Rules import add_rule

from .expected_client_version import EXPECTED_CLIENT_VERSION
from .items import CandyBox2ItemName, candy_box_2_base_id, items
from .locations import CandyBox2Location, CandyBox2LocationData, CandyBox2LocationName, locations
from .regions import CandyBox2Region, CandyBox2RoomRegion
from .rooms import CandyBox2Room, entrance_friendly_names

if TYPE_CHECKING:
    from . import CandyBox2World


weapons = [
    CandyBox2ItemName.NOTHING_WEAPON,
    CandyBox2ItemName.WOODEN_SWORD,
    CandyBox2ItemName.IRON_AXE,
    CandyBox2ItemName.POLISHED_SILVER_SWORD,
    CandyBox2ItemName.TROLLS_BLUDGEON,
    CandyBox2ItemName.MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.TRIBAL_SPEAR,
    CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR,
    CandyBox2ItemName.GIANT_SPOON,
    CandyBox2ItemName.SCYTHE,
    CandyBox2ItemName.GIANT_SPOON_OF_DOOM,
]

weapon_strength = [
    CandyBox2ItemName.NOTHING_WEAPON,
    CandyBox2ItemName.WOODEN_SWORD,
    CandyBox2ItemName.IRON_AXE,
    CandyBox2ItemName.TRIBAL_SPEAR,
    CandyBox2ItemName.MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.POLISHED_SILVER_SWORD,
    CandyBox2ItemName.TROLLS_BLUDGEON,
    CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR,
    CandyBox2ItemName.GIANT_SPOON,
    CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.GIANT_SPOON_OF_DOOM,
    CandyBox2ItemName.SCYTHE,
]

armors = [
    CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR,
    CandyBox2ItemName.KNIGHT_BODY_ARMOUR,
    CandyBox2ItemName.ENCHANTED_KNIGHT_BODY_ARMOUR,
]

room_parents = {
    CandyBox2Room.CASTLE: "MENU",
    CandyBox2Room.TOWER: CandyBox2Room.CASTLE.value,
    CandyBox2Room.VILLAGE_SHOP: "MENU",
    CandyBox2Room.VILLAGE_FURNISHED_HOUSE: "MENU",
    CandyBox2Room.VILLAGE_QUEST_HOUSE: "MENU",
    CandyBox2Room.QUEST_THE_CELLAR: CandyBox2Room.VILLAGE_QUEST_HOUSE.value,
    CandyBox2Room.VILLAGE_FORGE: "MENU",
    CandyBox2Room.VILLAGE_MINIGAME: "MENU",
    CandyBox2Room.SQUIRREL_TREE: "MENU",
    CandyBox2Room.LONELY_HOUSE: "MENU",
    CandyBox2Room.QUEST_THE_DESERT: "MENU",
    CandyBox2Room.POGO_STICK_SPOT: "MENU",
    CandyBox2Room.LOLLIPOP_FARM: "MENU",
    CandyBox2Room.WISHING_WELL: "MENU",
    CandyBox2Room.CAVE: "MENU",
    CandyBox2Room.QUEST_THE_OCTOPUS_KING: CandyBox2Room.CAVE.value,
    CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD: CandyBox2Room.CAVE.value,
    CandyBox2Room.DIG_SPOT: "MENU",
    CandyBox2Room.QUEST_THE_BRIDGE: "MENU",
    CandyBox2Room.SORCERESS_HUT: "MENU",
    CandyBox2Room.PIER: "MENU",
    CandyBox2Room.QUEST_THE_SEA: CandyBox2Room.PIER.value,
    CandyBox2Room.LIGHTHOUSE: CandyBox2Room.PIER.value,
    CandyBox2Room.QUEST_THE_FOREST: "MENU",
    CandyBox2Room.HOLE: "MENU",
    CandyBox2Room.QUEST_THE_HOLE: CandyBox2Room.HOLE.value,
    CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE: "MENU",
    CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER: CandyBox2Room.CASTLE.value,
    CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM: CandyBox2Room.CASTLE.value,
    CandyBox2Room.CASTLE_DARK_ROOM: CandyBox2Room.CASTLE.value,
    CandyBox2Room.CASTLE_BAKEHOUSE: CandyBox2Room.CASTLE.value,
    CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM: CandyBox2Room.CASTLE.value,
    CandyBox2Room.DRAGON: CandyBox2Room.CASTLE.value,
    CandyBox2Room.QUEST_HELL: CandyBox2Room.DRAGON.value,
    CandyBox2Room.QUEST_THE_DEVELOPER: CandyBox2Room.DRAGON.value,
    CandyBox2Room.DESERT_FORTRESS: "MENU",
    CandyBox2Room.QUEST_THE_XINOPHERYDON: CandyBox2Room.DESERT_FORTRESS.value,
    CandyBox2Room.QUEST_THE_TEAPOT: CandyBox2Room.DESERT_FORTRESS.value,
    CandyBox2Room.QUEST_THE_LEDGE_ROOM: CandyBox2Room.DESERT_FORTRESS.value,
    CandyBox2Room.QUEST_THE_X_POTION: "MENU",
}


class CandyBox2RulesPackageRuleExpression(ABC):
    @abstractmethod
    def default(self):
        pass

    @abstractmethod
    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        pass

    def indirection_required(self) -> set["CandyBox2Room"]:
        return set()

    def __and__(self, other):
        return CandyBox2RulesPackageRuleBooleanExpression("and", self, other)

    def __or__(self, other):
        return CandyBox2RulesPackageRuleBooleanExpression("or", self, other)

    def __invert__(self):
        return CandyBox2RulesPackageRuleUnaryExpression("not", self)


class CandyBox2RulesPackageRuleConstantExpression(CandyBox2RulesPackageRuleExpression):
    constant: bool

    def __init__(self, constant: bool):
        super().__init__()
        self.constant = constant

    def __and__(self, other):
        return self if self.constant == False else other  # noqa: E712

    def __or__(self, other):
        return self if self.constant == True else other  # noqa: E712

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        return self.constant

    def default(self):
        return ["constant", self.constant]


class CandyBox2RulesPackageRuleItemExpression(CandyBox2RulesPackageRuleExpression):
    item: "CandyBox2ItemName"
    count: int

    def __init__(self, item: "CandyBox2ItemName", count: int):
        super().__init__()
        self.item = item
        self.count = count

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        if self.item == CandyBox2ItemName.PROGRESSIVE_WEAPON:
            # Special case Progressive Weapon
            # This check becomes false if progressive weapons aren't enabled
            if world.starting_weapon != -1:
                return False

        return state.has(self.item, player, self.count)

    def default(self):
        return ["item", items[self.item].code, self.count]


class CandyBox2RulesPackageRuleRoomExpression(CandyBox2RulesPackageRuleExpression):
    room: "CandyBox2Room"

    def __init__(self, room: "CandyBox2Room"):
        super().__init__()
        self.room = room

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        return state.can_reach_region(entrance_friendly_names[self.room], player)

    def indirection_required(self):
        return [self.room]

    def default(self):
        return ["room", self.room.value]


class CandyBox2RulesPackageRuleLocationExpression(CandyBox2RulesPackageRuleExpression):
    location: "CandyBox2LocationName"
    id: int

    def __init__(self, location: "CandyBox2LocationName"):
        super().__init__()
        self.location = location

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        return state.can_reach_location(self.location, player)

    def default(self):
        return ["location", locations[self.location].id]


class CandyBox2RulesPackageRuleCountExpression(CandyBox2RulesPackageRuleExpression):
    class RuleCountInequality(IntEnum):
        LESS_THAN = 0
        LESS_THAN_OR_EQUAL_TO = 1
        EQUAL_TO = 2
        GREATER_THAN_OR_EQUAL_TO = 3
        GREATER_THAN = 4

    item: str
    required: int
    inquality: RuleCountInequality

    def __init__(self, item: str, inequality: RuleCountInequality, required: int):
        super().__init__()
        self.item = item
        self.required = required
        self.inequality = inequality

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        if self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.EQUAL_TO:
            return self.item_count(state, player) == self.required
        if self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.LESS_THAN:
            return self.item_count(state, player) < self.required
        if self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.LESS_THAN_OR_EQUAL_TO:
            return self.item_count(state, player) <= self.required
        if self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.GREATER_THAN:
            return self.item_count(state, player) > self.required
        if self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.GREATER_THAN_OR_EQUAL_TO:
            return self.item_count(state, player) >= self.required
        raise Exception("Tried to evaluate a count expression with invalid inequality operator")

    def item_count(self, state: CollectionState, player: int):
        if self.item == "chocolate":
            return (
                state.count(CandyBox2ItemName.CHOCOLATE_BAR, player)
                + (4 * state.count(CandyBox2ItemName.FOUR_CHOCOLATE_BARS, player))
                + (3 * state.count(CandyBox2ItemName.THREE_CHOCOLATE_BARS, player))
            )
        if self.item == "lollipop":
            return state.count(CandyBox2ItemName.THREE_LOLLIPOPS, player) * 3 + state.count(
                CandyBox2ItemName.LOLLIPOP, player
            )
        raise Exception("Tried to evaluate a count expression with invalid item name")

    def default(self):
        return ["count", self.item, self.inequality, self.required]


class CandyBox2RulesPackageRuleStartWeaponExpression(CandyBox2RulesPackageRuleExpression):
    weapon: "CandyBox2ItemName"

    def __init__(self, weapon: "CandyBox2ItemName"):
        super().__init__()
        self.weapon = weapon

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        for item in items:
            if items[item].code - candy_box_2_base_id == world.starting_weapon and item == self.weapon:
                return True
        return False

    def default(self):
        return ["startWeapon", items[self.weapon].code]


class CandyBox2RulesPackageRuleBooleanExpression(CandyBox2RulesPackageRuleExpression):
    op1: CandyBox2RulesPackageRuleExpression
    op2: CandyBox2RulesPackageRuleExpression
    expr: str

    def __init__(self, expr: str, op1: CandyBox2RulesPackageRuleExpression, op2: CandyBox2RulesPackageRuleExpression):
        super().__init__()
        self.op1 = op1
        self.op2 = op2
        self.expr = expr

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        if self.expr == "and":
            return self.op1.evaluate(world, state, player) and self.op2.evaluate(world, state, player)
        if self.expr == "or":
            return self.op1.evaluate(world, state, player) or self.op2.evaluate(world, state, player)
        raise Exception("Tried to evaluate a boolean expression with invalid operator")

    def default(self):
        return [self.expr, self.op1.default(), self.op2.default()]

    def indirection_required(self):
        return {*self.op1.indirection_required(), *self.op2.indirection_required()}


class CandyBox2RulesPackageRuleUnaryExpression(CandyBox2RulesPackageRuleExpression):
    op: CandyBox2RulesPackageRuleExpression
    expr: str

    def __init__(self, expr: str, op: CandyBox2RulesPackageRuleExpression):
        super().__init__()
        self.op = op
        self.expr = expr

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        if self.expr == "not":
            return not self.op.evaluate(world, state, player)
        raise Exception("Tried to evaluate a unary expression with invalid operator")

    def indirection_required(self):
        return self.op.indirection_required()

    def default(self):
        return [self.expr, self.op.default()]


class CandyBox2RulesPackage(JSONEncoder):
    expected_client_version: str
    locations: dict["CandyBox2LocationName", "CandyBox2LocationData"]
    location_rules: dict["CandyBox2LocationName", CandyBox2RulesPackageRuleExpression]
    room_rules: dict["CandyBox2Room", CandyBox2RulesPackageRuleExpression]
    location_parents: dict["CandyBox2LocationName", CandyBox2Room]
    room_exits: dict["CandyBox2Room", list["CandyBox2Room"]]
    goal_rule: CandyBox2RulesPackageRuleExpression

    def __init__(
        self,
        expected_client_version: str = "",
        *,
        skipkeys=False,
        ensure_ascii=True,
        check_circular=True,
        allow_nan=True,
        sort_keys=False,
        indent=None,
        separators=None,
        default=None,
    ):
        super().__init__(
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            default=default,
        )
        self.expected_client_version = expected_client_version
        self.locations = locations
        self.location_rules = {}
        self.room_rules = {}
        self.location_parents = {}
        self.room_exits = {}
        self.goal_rule = CandyBox2RulesPackageRuleConstantExpression(True)

    def set_goal_rule(self, goal_rule: CandyBox2RulesPackageRuleExpression):
        self.goal_rule = goal_rule

    def add_location_rule(
        self,
        location: "CandyBox2LocationName",
        rule: CandyBox2RulesPackageRuleExpression | None,
        parent: CandyBox2Room | None,
    ):
        if rule is not None:
            self.location_rules[location] = rule
        self.location_parents[location] = parent

    def add_room_rule(self, room: "CandyBox2Room", rule: CandyBox2RulesPackageRuleExpression):
        self.room_rules[room] = rule

    def assign_room_exits(self, room: "CandyBox2Room", exits: list["CandyBox2Room"]):
        self.room_exits[room] = exits

    def default(self, o):
        return {
            "expectedClientVersion": o.expected_client_version,
            "locations": {location.id: name for name, location in o.locations.items()},
            "locationParents": {
                o.locations[location].id: room.value
                for location, room in o.location_parents.items()
                if room is not None
            },
            "roomExits": {room.value: [exit.value for exit in exits] for room, exits in o.room_exits.items()},
            "rules": {
                "locations": {o.locations[location].id: rule.default() for location, rule in o.location_rules.items()},
                "rooms": {room: rule.default() for room, rule in o.room_rules.items()},
            },
            "goal": o.goal_rule.default(),
        }

    def apply_location_rules(self, world: "CandyBox2World", player: int):
        for target, rule in self.location_rules.items():
            try:
                add_rule(
                    world.get_location(target),
                    lambda state, r=rule, w=world, p=player: True if r is None else r.evaluate(w, state, p),
                )
            except KeyError:
                pass

    def apply_room_rules(self, rooms: dict[str, CandyBox2Region], world: "CandyBox2World", player: int):
        generated_entrances = []

        for target, region in rooms.items():
            rule = self.room_rules.get(target)
            region.locations += [
                CandyBox2Location(player, location_name.value, self.locations[location_name].id, region)
                for location_name in [
                    location
                    for location, room in self.location_parents.items()
                    if room == (None if target == "MENU" else target)
                ]
                if self.locations[location_name].is_included(world)
            ]

            parent = room_parents.get("MENU" if target is None else target)
            if parent is not None:
                entrance = rooms[parent].connect(
                    region,
                    None,
                    lambda state, r=rule, w=world, p=player: True if r is None else r.evaluate(w, state, p),
                )
                if type(region) is CandyBox2RoomRegion:
                    generated_entrances.append(entrance)
                if rule is not None:
                    for indirect_region in rule.indirection_required():
                        world.multiworld.register_indirect_condition(rooms[indirect_region], entrance)

        return generated_entrances


class CandyBox2Castable(IntEnum):
    ACID_RAIN = 0
    FIREBALL = 1
    TELEPORT = 2
    ERASE_MAGIC = 3
    THORNS_SHIELD = 4
    OBSIDIAN_WALL = 5
    BLACK_DEMONS = 6
    BLACK_HOLE = 7


def rule_item(item: "CandyBox2ItemName", count: int = 1):
    return CandyBox2RulesPackageRuleItemExpression(item, count)


def rule_room(room: "CandyBox2Room"):
    return CandyBox2RulesPackageRuleRoomExpression(room)


def rule_location(location: "CandyBox2LocationName"):
    return CandyBox2RulesPackageRuleLocationExpression(location)


def no_conditions():
    return None


def has_weapon(weapon: CandyBox2ItemName):
    return (
        rule_item(weapon)
        | rule_item(CandyBox2ItemName.PROGRESSIVE_WEAPON, weapons.index(weapon))
        | CandyBox2RulesPackageRuleStartWeaponExpression(weapon)
    )


def weapon_is_at_least(minimum_weapon: CandyBox2ItemName):
    condition = CandyBox2RulesPackageRuleConstantExpression(False)
    for weapon in weapon_strength[weapon_strength.index(minimum_weapon) :]:
        condition = condition | has_weapon(weapon)
    return condition


def armor_is_at_least(minimum_armor: CandyBox2ItemName):
    condition = CandyBox2RulesPackageRuleConstantExpression(False)
    for armor in armors[armors.index(minimum_armor) :]:
        condition = condition | rule_item(armor)
    return condition


def can_cast(castable: CandyBox2Castable):
    match castable:
        case CandyBox2Castable.ACID_RAIN:
            return (
                rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
                | rule_item(CandyBox2ItemName.ACID_RAIN_SPELL)
            )
        case CandyBox2Castable.FIREBALL:
            return (
                rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
                | rule_item(CandyBox2ItemName.FIREBALL_SPELL)
            )
        case CandyBox2Castable.TELEPORT:
            return (
                rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
                | rule_item(CandyBox2ItemName.TELEPORT_SPELL)
            )
        case CandyBox2Castable.ERASE_MAGIC:
            return (
                rule_item(CandyBox2ItemName.ADVANCED_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 2)
                | rule_item(CandyBox2ItemName.ERASE_MAGIC_SPELL)
            )
        case CandyBox2Castable.THORNS_SHIELD:
            return (
                rule_item(CandyBox2ItemName.ADVANCED_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 2)
                | rule_item(CandyBox2ItemName.THORNS_SHIELD_SPELL)
            )
        case CandyBox2Castable.OBSIDIAN_WALL:
            return (
                rule_item(CandyBox2ItemName.BLACK_MAGIC_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 3)
                | rule_item(CandyBox2ItemName.OBSIDIAN_WALL_SPELL)
            )
        case CandyBox2Castable.BLACK_DEMONS:
            return (
                rule_item(CandyBox2ItemName.BLACK_MAGIC_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 3)
                | rule_item(CandyBox2ItemName.BLACK_DEMONS_SPELL)
            )
        case CandyBox2Castable.BLACK_HOLE:
            return rule_item(CandyBox2ItemName.PURPLE_FIN)
    return None


def has_at_least_chocolates(chocolates: int):
    return CandyBox2RulesPackageRuleCountExpression(
        "chocolate", CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.GREATER_THAN_OR_EQUAL_TO, chocolates
    )


def has_all_chocolates():
    return has_at_least_chocolates(13)


# Allows the player to plant enough lollipops at the farm for 1/minute
def can_grow_lollipops():
    return (
        CandyBox2RulesPackageRuleCountExpression(
            "lollipop", CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.GREATER_THAN_OR_EQUAL_TO, 9
        )
        & rule_room(CandyBox2Room.LOLLIPOP_FARM)
        & rule_room(CandyBox2Room.LOLLIPOP_FARM)
    )


def can_farm_lollipops():
    return (
        can_grow_lollipops()
        & rule_item(CandyBox2ItemName.PITCHFORK)
        & rule_item(CandyBox2ItemName.SHELL_POWDER)
        & rule_item(CandyBox2ItemName.GREEN_FIN)
    )


# Ideally allows the player to stumble upon a quest they can use to farm candies
def can_farm_candies():
    return can_farm_lollipops()


def has_projectiles():
    return (
        rule_item(CandyBox2ItemName.RED_ENCHANTED_GLOVES)
        | rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        | rule_item(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
    )


def can_jump():
    return (
        (rule_item(CandyBox2ItemName.ROCKET_BOOTS) | rule_item(CandyBox2ItemName.DESERT_BIRD_FEATHER))
        & rule_item(CandyBox2ItemName.POGO_STICK)
    ) | rule_item(CandyBox2ItemName.PROGRESSIVE_JUMP, 2)


def can_fly():
    return (rule_item(CandyBox2ItemName.ROCKET_BOOTS) & rule_item(CandyBox2ItemName.POGO_STICK)) | rule_item(
        CandyBox2ItemName.PROGRESSIVE_JUMP, 3
    )


def can_escape_hole():
    return can_fly() | can_cast(CandyBox2Castable.TELEPORT)


def can_brew(also_require_lollipops: bool):
    if also_require_lollipops:
        return rule_item(CandyBox2ItemName.SORCERESS_CAULDRON) & can_farm_candies() & can_farm_lollipops()

    return rule_item(CandyBox2ItemName.SORCERESS_CAULDRON) & can_farm_candies()


def can_heal():
    return can_brew(False) | rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)


def sea_entrance():
    return (
        weapon_is_at_least(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR)
        & has_projectiles()
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR)
        & can_heal()
    )


def can_beat_sharks():
    return sea_entrance() & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)


def generate_rules_package():
    rules_package = CandyBox2RulesPackage(EXPECTED_CLIENT_VERSION)
    generate_rules_package_location_rules(rules_package)
    generate_rules_package_room_rules(rules_package)
    generate_rules_package_exits(rules_package)
    generate_rules_package_goal_rule(rules_package)

    return rules_package


def generate_rules_package_location_rules(rules_package: CandyBox2RulesPackage):
    rules_package.add_location_rule(CandyBox2LocationName.DISAPPOINTED_EMOTE_CHOCOLATE_BAR, can_farm_candies(), None)
    rules_package.add_location_rule(CandyBox2LocationName.HP_BAR_UNLOCK, no_conditions(), None)
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_LOLLIPOP_ON_EXHAUST_CHUTE, no_conditions(), CandyBox2Room.VILLAGE_FORGE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_WOODEN_SWORD, no_conditions(), CandyBox2Room.VILLAGE_FORGE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_IRON_AXE,
        rule_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_WOODEN_SWORD),
        CandyBox2Room.VILLAGE_FORGE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD,
        can_farm_candies() & rule_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_IRON_AXE),
        CandyBox2Room.VILLAGE_FORGE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR,
        can_farm_candies()
        & rule_location(CandyBox2LocationName.CAVE_EXIT)
        & rule_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD),
        CandyBox2Room.VILLAGE_FORGE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_SCYTHE,
        can_farm_candies()
        & rule_room(CandyBox2Room.DRAGON)
        & rule_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.VILLAGE_FORGE,
    )

    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_ON_THE_BOOKSHELF,
        no_conditions(),
        CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_IN_THE_BOOKSHELF,
        no_conditions(),
        CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_UNDER_THE_RUG,
        no_conditions(),
        CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
    )

    # Cellar rules
    rules_package.add_location_rule(
        CandyBox2LocationName.CELLAR_QUEST_CLEARED, no_conditions(), CandyBox2Room.QUEST_THE_CELLAR
    )

    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_FIRST_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_SECOND_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_THIRD_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_FOURTH_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_FIFTH_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_PUZZLE, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(CandyBox2LocationName.X_MARKS_THE_SPOT, no_conditions(), CandyBox2Room.DIG_SPOT)
    rules_package.add_location_rule(
        CandyBox2LocationName.LOCKED_CANDY_BOX_ACQUIRED, no_conditions(), CandyBox2Room.LONELY_HOUSE
    )

    # Desert rules
    rules_package.add_location_rule(
        CandyBox2LocationName.DESERT_QUEST_CLEARED,
        weapon_is_at_least(CandyBox2ItemName.IRON_AXE),
        CandyBox2Room.QUEST_THE_DESERT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.DESERT_BIRD_FEATHER_ACQUIRED,
        weapon_is_at_least(CandyBox2ItemName.IRON_AXE) & has_projectiles(),
        CandyBox2Room.QUEST_THE_DESERT,
    )

    rules_package.add_location_rule(CandyBox2LocationName.POGO_STICK, no_conditions(), CandyBox2Room.POGO_STICK_SPOT)

    # Wishing Well rules
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_RED_ENCHANTED_GLOVES,
        rule_item(CandyBox2ItemName.LEATHER_GLOVES) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_PINK_ENCHANTED_GLOVES,
        rule_item(CandyBox2ItemName.LEATHER_GLOVES) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_SUMMONING_TRIBAL_SPEAR,
        has_weapon(CandyBox2ItemName.TRIBAL_SPEAR) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF,
        has_weapon(CandyBox2ItemName.MONKEY_WIZARD_STAFF) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR,
        rule_item(CandyBox2ItemName.KNIGHT_BODY_ARMOUR) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS,
        rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN,
        rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_GIANT_SPOON_OF_DOOM,
        has_weapon(CandyBox2ItemName.GIANT_SPOON) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )

    # Bridge rules
    rules_package.add_location_rule(
        CandyBox2LocationName.TROLL_DEFEATED,
        weapon_is_at_least(CandyBox2ItemName.POLISHED_SILVER_SWORD),
        CandyBox2Room.QUEST_THE_BRIDGE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_TROLLS_BLUDGEON_ACQUIRED,
        weapon_is_at_least(CandyBox2ItemName.POLISHED_SILVER_SWORD),
        CandyBox2Room.QUEST_THE_BRIDGE,
    )

    # Cave rules
    rules_package.add_location_rule(CandyBox2LocationName.CAVE_CHOCOLATE_BAR, no_conditions(), CandyBox2Room.CAVE)
    rules_package.add_location_rule(CandyBox2LocationName.CAVE_HEART_PLUG, no_conditions(), CandyBox2Room.CAVE)
    rules_package.add_location_rule(CandyBox2LocationName.CAVE_EXIT, no_conditions(), CandyBox2Room.CAVE)
    rules_package.add_location_rule(
        CandyBox2LocationName.OCTOPUS_KING_DEFEATED,
        rule_item(CandyBox2ItemName.SORCERESS_CAULDRON)
        & weapon_is_at_least(CandyBox2ItemName.TROLLS_BLUDGEON)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_OCTOPUS_KING,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.MONKEY_WIZARD_DEFEATED,
        rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION)
        & can_cast(CandyBox2Castable.TELEPORT)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & weapon_is_at_least(CandyBox2ItemName.TROLLS_BLUDGEON)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD,
    )

    # The Hole rules
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_HEART_PENDANT_ACQUIRED, can_jump(), CandyBox2Room.QUEST_THE_HOLE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED,
        can_escape_hole() & rule_item(CandyBox2ItemName.SPONGE),
        CandyBox2Room.QUEST_THE_HOLE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED_OBSIDIAN_WALL,
        can_escape_hole() & rule_item(CandyBox2ItemName.SPONGE),
        CandyBox2Room.QUEST_THE_HOLE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED_BLACK_DEMONS,
        can_escape_hole() & rule_item(CandyBox2ItemName.SPONGE),
        CandyBox2Room.QUEST_THE_HOLE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED,
        can_escape_hole() & ((rule_item(CandyBox2ItemName.SPONGE) & can_jump()) | (can_brew(False))),
        CandyBox2Room.QUEST_THE_HOLE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_TRIBAL_WARRIOR_DEFEATED,
        can_escape_hole()
        & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_HOLE,
    )

    # TODO: possibly fly over?
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED,
        can_escape_hole()
        & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_HOLE,
    )

    # The Forest rules
    rules_package.add_location_rule(
        CandyBox2LocationName.FOREST_QUEST_CLEARED,
        weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_FOREST,
    )

    # Castle Entrance rules
    rules_package.add_location_rule(
        CandyBox2LocationName.CASTLE_ENTRANCE_QUEST_CLEARED,
        can_fly()
        | (
            weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
            & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
            & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR)
        ),
        CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.KNIGHT_BODY_ARMOUR_ACQUIRED,
        weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE,
    )

    # Castle rules
    rules_package.add_location_rule(
        CandyBox2LocationName.PITCHFORK_ACQUIRED, no_conditions(), CandyBox2Room.CASTLE_DARK_ROOM
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.GIANT_NOUGAT_MONSTER_DEFEATED,
        can_cast(CandyBox2Castable.BLACK_HOLE)
        & weapon_is_at_least(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR)
        & rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN),
        CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER,
    )

    # Egg Room
    rules_package.add_location_rule(
        CandyBox2LocationName.EGG_ROOM_QUEST_CLEARED,
        can_fly() | has_weapon(CandyBox2ItemName.NOTHING_WEAPON),
        CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM,
    )

    # The Desert Fortress
    rules_package.add_location_rule(
        CandyBox2LocationName.XINOPHERYDON_DEFEATED,
        (can_fly() | (can_brew(False) & can_jump()))
        & (
            has_weapon(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
            | rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        ),
        CandyBox2Room.QUEST_THE_XINOPHERYDON,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED,
        can_fly() | (can_brew(False) & can_jump()),
        CandyBox2Room.QUEST_THE_XINOPHERYDON,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.TEAPOT_DEFEATED,
        weapon_is_at_least(CandyBox2ItemName.SCYTHE)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN)
        & rule_item(CandyBox2ItemName.SORCERESS_CAULDRON)
        & rule_item(CandyBox2ItemName.XINOPHERYDON_CLAW),
        CandyBox2Room.QUEST_THE_TEAPOT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ROCKET_BOOTS_ACQUIRED,
        can_fly()
        | (
            rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION)
            & can_jump()
            & can_cast(CandyBox2Castable.TELEPORT)
            & (
                rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN)
                | has_weapon(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR)
            )
        ),
        CandyBox2Room.QUEST_THE_LEDGE_ROOM,
    )

    # Lollipop Farm rules
    rules_package.add_location_rule(
        CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_1, can_farm_lollipops(), CandyBox2Room.LOLLIPOP_FARM
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_2, can_farm_lollipops(), CandyBox2Room.LOLLIPOP_FARM
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_3, can_farm_lollipops(), CandyBox2Room.LOLLIPOP_FARM
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_4, can_farm_lollipops(), CandyBox2Room.LOLLIPOP_FARM
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_5, can_farm_lollipops(), CandyBox2Room.LOLLIPOP_FARM
    )

    # Hell rules
    rules_package.add_location_rule(
        CandyBox2LocationName.DEVIL_DEFEATED,
        can_cast(CandyBox2Castable.BLACK_DEMONS)
        & rule_item(CandyBox2ItemName.UNICORN_HORN)
        & rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION)
        & armor_is_at_least(CandyBox2ItemName.ENCHANTED_KNIGHT_BODY_ARMOUR)
        & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)
        & has_weapon(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF),
        CandyBox2Room.QUEST_HELL,
    )

    # Developer rules
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_DEVELOPER_DEFEATED,
        can_farm_candies() & can_cast(CandyBox2Castable.BLACK_HOLE) & can_cast(CandyBox2Castable.TELEPORT),
        CandyBox2Room.QUEST_THE_DEVELOPER,
    )

    # The Sea rules
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SPONGE_ACQUIRED, sea_entrance(), CandyBox2Room.QUEST_THE_SEA
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SHELL_POWDER_ACQUIRED, sea_entrance(), CandyBox2Room.QUEST_THE_SEA
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_RED_FIN_ACQUIRED,
        can_beat_sharks() & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS),
        CandyBox2Room.QUEST_THE_SEA,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_GREEN_FIN_ACQUIRED,
        can_beat_sharks()
        & can_cast(CandyBox2Castable.ERASE_MAGIC)
        & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS),
        CandyBox2Room.QUEST_THE_SEA,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_PURPLE_FIN_ACQUIRED,
        can_beat_sharks()
        & rule_item(CandyBox2ItemName.HEART_PENDANT)
        & rule_item(CandyBox2ItemName.HEART_PLUG)
        & can_cast(CandyBox2Castable.ERASE_MAGIC)
        & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & rule_item(CandyBox2ItemName.UNICORN_HORN),
        CandyBox2Room.QUEST_THE_SEA,
    )

    # Cyclops Puzzle
    rules_package.add_location_rule(
        CandyBox2LocationName.SOLVE_CYCLOPS_PUZZLE, rule_room(CandyBox2Room.DRAGON), CandyBox2Room.LIGHTHOUSE
    )

    # X Potion
    rules_package.add_location_rule(
        CandyBox2LocationName.YOURSELF_DEFEATED,
        rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN),
        CandyBox2Room.QUEST_THE_X_POTION,
    )

    # Cooking
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_1, has_at_least_chocolates(9), CandyBox2Room.CASTLE_BAKEHOUSE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_2, has_at_least_chocolates(10), CandyBox2Room.CASTLE_BAKEHOUSE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_3, has_at_least_chocolates(11), CandyBox2Room.CASTLE_BAKEHOUSE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_4, has_at_least_chocolates(12), CandyBox2Room.CASTLE_BAKEHOUSE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_5, has_all_chocolates(), CandyBox2Room.CASTLE_BAKEHOUSE
    )

    # Sorceress items
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE, can_grow_lollipops(), CandyBox2Room.SORCERESS_HUT
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE_ACID_RAIN,
        can_grow_lollipops(),
        CandyBox2Room.SORCERESS_HUT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE_FIREBALL,
        can_grow_lollipops(),
        CandyBox2Room.SORCERESS_HUT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE_TELEPORT,
        can_grow_lollipops(),
        CandyBox2Room.SORCERESS_HUT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_ADVANCED_GRIMOIRE, can_grow_lollipops(), CandyBox2Room.SORCERESS_HUT
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_ADVANCED_GRIMOIRE_THORNS_SHIELD,
        can_grow_lollipops(),
        CandyBox2Room.SORCERESS_HUT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_ADVANCED_GRIMOIRE_ERASE_MAGIC,
        can_grow_lollipops(),
        CandyBox2Room.SORCERESS_HUT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_HAT, can_farm_lollipops(), CandyBox2Room.SORCERESS_HUT
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_CAULDRON, can_grow_lollipops(), CandyBox2Room.SORCERESS_HUT
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_LOLLIPOP_ON_THE_SHELVES, no_conditions(), CandyBox2Room.SORCERESS_HUT
    )

    # Merchant items
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_TOP_LOLLIPOP, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_CENTRE_LOLLIPOP, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_BOTTOM_LOLLIPOP, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_TIME_RING, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_LEATHER_BOOTS, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_LEATHER_GLOVES, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_CHOCOLATE_BAR, can_farm_candies(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_CANDY_MERCHANTS_HAT, can_farm_candies(), CandyBox2Room.VILLAGE_SHOP
    )


def generate_rules_package_room_rules(rules_package: CandyBox2RulesPackage):
    rules_package.add_room_rule(CandyBox2Room.SQUIRREL_TREE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1))
    rules_package.add_room_rule(CandyBox2Room.LONELY_HOUSE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1))
    rules_package.add_room_rule(
        CandyBox2Room.DIG_SPOT, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1) & rule_room(CandyBox2Room.CAVE)
    )
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_DESERT, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1))
    rules_package.add_room_rule(CandyBox2Room.LOLLIPOP_FARM, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_BRIDGE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.WISHING_WELL, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.POGO_STICK_SPOT, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.CAVE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.SORCERESS_HUT, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 3))
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_FOREST, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 4))
    rules_package.add_room_rule(CandyBox2Room.PIER, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 4))
    rules_package.add_room_rule(CandyBox2Room.HOLE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 5))
    rules_package.add_room_rule(
        CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 5)
    )
    rules_package.add_room_rule(CandyBox2Room.CASTLE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 6))
    rules_package.add_room_rule(CandyBox2Room.TOWER, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 7))
    rules_package.add_room_rule(CandyBox2Room.VILLAGE_MINIGAME, rule_item(CandyBox2ItemName.THIRD_HOUSE_KEY))
    rules_package.add_room_rule(
        CandyBox2Room.DESERT_FORTRESS,
        rule_item(CandyBox2ItemName.DESERT_FORTRESS_KEY) & rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1),
    )
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_CELLAR, weapon_is_at_least(CandyBox2ItemName.WOODEN_SWORD))
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_X_POTION, can_brew(True))


def generate_rules_package_exits(rules_package: CandyBox2RulesPackage):
    rules_package.assign_room_exits(
        CandyBox2Room.VILLAGE,
        [
            CandyBox2Room.VILLAGE_SHOP,
            CandyBox2Room.VILLAGE_FORGE,
            CandyBox2Room.VILLAGE_MINIGAME,
            CandyBox2Room.VILLAGE_QUEST_HOUSE,
            CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
            CandyBox2Room.QUEST_THE_X_POTION,
        ],
    )
    rules_package.assign_room_exits(CandyBox2Room.VILLAGE_QUEST_HOUSE, [CandyBox2Room.QUEST_THE_CELLAR])
    rules_package.assign_room_exits(
        CandyBox2Room.WORLD_MAP,
        [
            CandyBox2Room.SQUIRREL_TREE,
            CandyBox2Room.LONELY_HOUSE,
            CandyBox2Room.DIG_SPOT,
            CandyBox2Room.QUEST_THE_DESERT,
            CandyBox2Room.DESERT_FORTRESS,
            CandyBox2Room.LOLLIPOP_FARM,
            CandyBox2Room.WISHING_WELL,
            CandyBox2Room.POGO_STICK_SPOT,
            CandyBox2Room.QUEST_THE_BRIDGE,
            CandyBox2Room.SORCERESS_HUT,
            CandyBox2Room.CAVE,
            CandyBox2Room.PIER,
            CandyBox2Room.QUEST_THE_FOREST,
            CandyBox2Room.HOLE,
            CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE,
            CandyBox2Room.CASTLE,
        ],
    )
    rules_package.assign_room_exits(
        CandyBox2Room.DESERT_FORTRESS,
        [CandyBox2Room.QUEST_THE_LEDGE_ROOM, CandyBox2Room.QUEST_THE_XINOPHERYDON, CandyBox2Room.QUEST_THE_TEAPOT],
    )
    rules_package.assign_room_exits(
        CandyBox2Room.CAVE, [CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD, CandyBox2Room.QUEST_THE_OCTOPUS_KING]
    )
    rules_package.assign_room_exits(CandyBox2Room.PIER, [CandyBox2Room.QUEST_THE_SEA, CandyBox2Room.LIGHTHOUSE])
    rules_package.assign_room_exits(CandyBox2Room.HOLE, [CandyBox2Room.QUEST_THE_HOLE])
    rules_package.assign_room_exits(
        CandyBox2Room.CASTLE,
        [
            CandyBox2Room.CASTLE_DARK_ROOM,
            CandyBox2Room.CASTLE_BAKEHOUSE,
            CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM,
            CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM,
            CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER,
            CandyBox2Room.DRAGON,
            CandyBox2Room.TOWER,
        ],
    )
    rules_package.assign_room_exits(CandyBox2Room.DRAGON, [CandyBox2Room.QUEST_THE_DEVELOPER, CandyBox2Room.QUEST_HELL])

def generate_rules_package_goal_rule(rules_package: CandyBox2RulesPackage):
    rules_package.set_goal_rule(
        rule_room(CandyBox2Room.TOWER) &
        rule_item(CandyBox2ItemName.P_STONE) &
        rule_item(CandyBox2ItemName.L_STONE) &
        rule_item(CandyBox2ItemName.A_STONE) &
        rule_item(CandyBox2ItemName.Y_STONE) &
        rule_item(CandyBox2ItemName.LOCKED_CANDY_BOX)
    )
