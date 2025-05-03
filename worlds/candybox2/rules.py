from abc import abstractmethod, ABC
from enum import IntEnum
from json import JSONEncoder
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from .locations import locations, CandyBox2LocationName
from .rooms import CandyBox2Room, entrance_friendly_names
from .items import CandyBox2ItemName, items, candy_box_2_base_id
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import CandyBox2World


class CandyBox2RulesPackageRuleExpression(ABC):
    @abstractmethod
    def default(self):
        pass

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int) -> bool:
        pass

    def indirection_required(self):
        return False

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
        return self if self.constant == False else other

    def __or__(self, other):
        return self if self.constant == True else other

    def evaluate(self, world: "CandyBox2World", state: CollectionState, player: int):
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
        return True

    def default(self):
        return ["room", self.room.value]

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
        elif self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.LESS_THAN:
            return self.item_count(state, player) < self.required
        elif self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.LESS_THAN_OR_EQUAL_TO:
            return self.item_count(state, player) <= self.required
        elif self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.GREATER_THAN:
            return self.item_count(state, player) > self.required
        elif self.inequality == CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.GREATER_THAN_OR_EQUAL_TO:
            return self.item_count(state, player) >= self.required

    def item_count(self, state: CollectionState, player: int):
        if self.item == "chocolate":
            return state.count(CandyBox2ItemName.CHOCOLATE_BAR, player) + (4 * state.count(CandyBox2ItemName.FOUR_CHOCOLATE_BARS, player)) + (3 * state.count(CandyBox2ItemName.THREE_CHOCOLATE_BARS, player))
        if self.item == "lollipop":
           return state.count(CandyBox2ItemName.THREE_LOLLIPOPS, player) * 3 + state.count(CandyBox2ItemName.LOLLIPOP, player)

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
        elif self.expr == "or":
            return self.op1.evaluate(world, state, player) or self.op2.evaluate(world, state, player)

    def default(self):
        return [self.expr, self.op1.default(), self.op2.default()]

    def indirection_required(self):
        self.op1.indirection_required() or self.op2.indirection_required()

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

    def indirection_required(self):
        return self.op.indirection_required()

    def default(self):
        return [self.expr, self.op.default()]

class CandyBox2RulesPackage(JSONEncoder):
    locations: dict[int, str]
    location_rules: dict["CandyBox2LocationName", CandyBox2RulesPackageRuleExpression]

    def __init__(self, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                         allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators,
                         default=default)
        self.locations = {location: name for name, location in locations.items()}
        self.location_rules = {}

    def add_location_rule(self, location: "CandyBox2LocationName", rule: CandyBox2RulesPackageRuleExpression):
        self.location_rules[location] = rule

    def default(self, o):
        return {
            "locations": o.locations,
            "rules": {
                **{f"loc_{locations[location]}": rule.default() for location, rule in o.location_rules.items()}
            }
        }

    def apply_rules(self, world: "CandyBox2World", player: int):
        for target, rule in self.location_rules.items():
            add_rule(world.get_location(target), lambda state: rule.evaluate(world, state, player))

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

def has_weapon(weapon: CandyBox2ItemName):
    return rule_item(weapon) | rule_item(CandyBox2ItemName.PROGRESSIVE_WEAPON, weapons.index(weapon)) | CandyBox2RulesPackageRuleStartWeaponExpression(weapon)

def weapon_is_at_least(minimum_weapon: CandyBox2ItemName):
    condition = CandyBox2RulesPackageRuleConstantExpression(False)
    for weapon in weapon_strength[weapon_strength.index(minimum_weapon):]:
        condition = condition | has_weapon(weapon)
    return condition

def armor_is_at_least(minimum_armor: CandyBox2ItemName):
    condition = CandyBox2RulesPackageRuleConstantExpression(False)
    for armor in armors[armors.index(minimum_armor):]:
        condition = condition | rule_item(armor)
    return condition

def can_cast(castable: CandyBox2Castable):
    match castable:
        case CandyBox2Castable.ACID_RAIN:
            return rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE) | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
        case CandyBox2Castable.FIREBALL:
            return rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE) | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
        case CandyBox2Castable.TELEPORT:
            return rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE) | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
        case CandyBox2Castable.ERASE_MAGIC:
            return rule_item(CandyBox2ItemName.ADVANCED_GRIMOIRE) | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 2)
        case CandyBox2Castable.THORNS_SHIELD:
            return rule_item(CandyBox2ItemName.ADVANCED_GRIMOIRE) | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 2)
        case CandyBox2Castable.OBSIDIAN_WALL:
            return rule_item(CandyBox2ItemName.BLACK_MAGIC_GRIMOIRE) | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 3)
        case CandyBox2Castable.BLACK_DEMONS:
            return rule_item(CandyBox2ItemName.BLACK_MAGIC_GRIMOIRE) | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 3)
        case CandyBox2Castable.BLACK_HOLE:
            return rule_item(CandyBox2ItemName.PURPLE_FIN)

def has_at_least_chocolates(chocolates: int):
    return CandyBox2RulesPackageRuleCountExpression("chocolate", CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.GREATER_THAN_OR_EQUAL_TO, chocolates)

def has_all_chocolates():
    return has_at_least_chocolates(13)

# Allows the player to plant enough lollipops at the farm for 1/minute
def can_grow_lollipops():
    return CandyBox2RulesPackageRuleCountExpression("lollipop", CandyBox2RulesPackageRuleCountExpression.RuleCountInequality.GREATER_THAN_OR_EQUAL_TO, 9) & rule_room(CandyBox2Room.LOLLIPOP_FARM) & rule_room(CandyBox2Room.LOLLIPOP_FARM)

def can_farm_lollipops():
    return can_grow_lollipops() & rule_item(CandyBox2ItemName.PITCHFORK) & rule_item(CandyBox2ItemName.SHELL_POWDER) & rule_item(CandyBox2ItemName.GREEN_FIN)

# Ideally allows the player to stumble upon a quest they can use to farm candies
def can_farm_candies():
    return can_farm_lollipops()

def has_projectiles():
    return rule_item(CandyBox2ItemName.RED_ENCHANTED_GLOVES) | rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS) | rule_item(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)

def can_jump():
    return ((rule_item(CandyBox2ItemName.ROCKET_BOOTS) | rule_item(CandyBox2ItemName.DESERT_BIRD_FEATHER)) & rule_item(CandyBox2ItemName.POGO_STICK)) | rule_item(CandyBox2ItemName.PROGRESSIVE_JUMP, 2)

def can_fly():
    return (rule_item(CandyBox2ItemName.ROCKET_BOOTS) & rule_item(CandyBox2ItemName.POGO_STICK)) | rule_item(CandyBox2ItemName.PROGRESSIVE_JUMP, 3)

def can_escape_hole():
    return can_fly() | can_cast(CandyBox2Castable.TELEPORT)

def can_brew(also_require_lollipops: bool):
    if also_require_lollipops:
        return rule_item(CandyBox2ItemName.SORCERESS_CAULDRON) & can_farm_candies() & can_farm_lollipops()
    
    return rule_item(CandyBox2ItemName.SORCERESS_CAULDRON) & can_farm_candies()

def can_heal():
    return can_brew(False) | rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)

def sea_entrance():
    return (weapon_is_at_least(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR)
            & has_projectiles()
            & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR)
            & can_heal())

def can_beat_sharks():
    return sea_entrance() & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)

def generate_rules_package():
    rules_package = CandyBox2RulesPackage()
    rules_package.add_location_rule(CandyBox2LocationName.DISAPPOINTED_EMOTE_CHOCOLATE_BAR, can_farm_candies())
    rules_package.add_location_rule(CandyBox2LocationName.VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD, can_farm_candies())
    rules_package.add_location_rule(CandyBox2LocationName.VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR, can_farm_candies() & rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 3))
    

    # TODO: Forge locations should depend on previous forge location where applicable
    rules_package.add_location_rule(CandyBox2LocationName.VILLAGE_FORGE_BUY_SCYTHE, can_farm_candies() & rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 3) & rule_room(CandyBox2Room.DRAGON))

    # Cellar rules
    rules_package.add_location_rule(CandyBox2LocationName.CELLAR_QUEST_CLEARED, weapon_is_at_least(CandyBox2ItemName.WOODEN_SWORD))

    # Desert rules
    rules_package.add_location_rule(CandyBox2LocationName.DESERT_QUEST_CLEARED, weapon_is_at_least(CandyBox2ItemName.IRON_AXE))

    rules_package.add_location_rule(CandyBox2LocationName.DESERT_BIRD_FEATHER_ACQUIRED, weapon_is_at_least(CandyBox2ItemName.IRON_AXE) & has_projectiles())

    # Wishing Well rules
    rules_package.add_location_rule(CandyBox2LocationName.ENCHANT_RED_ENCHANTED_GLOVES, rule_item(CandyBox2ItemName.LEATHER_GLOVES) & has_all_chocolates())
    rules_package.add_location_rule(CandyBox2LocationName.ENCHANT_PINK_ENCHANTED_GLOVES, rule_item(CandyBox2ItemName.LEATHER_GLOVES) & has_all_chocolates())
    rules_package.add_location_rule(CandyBox2LocationName.ENCHANT_SUMMONING_TRIBAL_SPEAR, has_weapon(CandyBox2ItemName.TRIBAL_SPEAR) & has_all_chocolates())
    rules_package.add_location_rule(CandyBox2LocationName.ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF, has_weapon(CandyBox2ItemName.MONKEY_WIZARD_STAFF) & has_all_chocolates())
    rules_package.add_location_rule(CandyBox2LocationName.ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR, rule_item(CandyBox2ItemName.KNIGHT_BODY_ARMOUR) & has_all_chocolates())
    rules_package.add_location_rule(CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS, rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN) & has_all_chocolates())
    rules_package.add_location_rule(CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN, rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN) & has_all_chocolates())
    rules_package.add_location_rule(CandyBox2LocationName.ENCHANT_GIANT_SPOON_OF_DOOM, has_weapon(CandyBox2ItemName.GIANT_SPOON) & has_all_chocolates())

    # Bridge rules
    rules_package.add_location_rule(CandyBox2LocationName.TROLL_DEFEATED, weapon_is_at_least(CandyBox2ItemName.POLISHED_SILVER_SWORD))
    rules_package.add_location_rule(CandyBox2LocationName.THE_TROLLS_BLUDGEON_ACQUIRED, weapon_is_at_least(CandyBox2ItemName.POLISHED_SILVER_SWORD))

    # Cave rules
    rules_package.add_location_rule(CandyBox2LocationName.OCTOPUS_KING_DEFEATED, rule_item(CandyBox2ItemName.SORCERESS_CAULDRON) & weapon_is_at_least(CandyBox2ItemName.TROLLS_BLUDGEON) & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))
    rules_package.add_location_rule(CandyBox2LocationName.MONKEY_WIZARD_DEFEATED, rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION) & can_cast(CandyBox2Castable.TELEPORT) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS) & weapon_is_at_least(CandyBox2ItemName.TROLLS_BLUDGEON) & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # The Hole rules
    rules_package.add_location_rule(CandyBox2LocationName.THE_HOLE_HEART_PENDANT_ACQUIRED, can_jump())
    rules_package.add_location_rule(CandyBox2LocationName.THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED, can_escape_hole() & rule_item(CandyBox2ItemName.SPONGE))
    rules_package.add_location_rule(CandyBox2LocationName.THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED, can_escape_hole() & rule_item(CandyBox2ItemName.SPONGE) & can_jump())
    rules_package.add_location_rule(CandyBox2LocationName.THE_HOLE_TRIBAL_WARRIOR_DEFEATED, can_escape_hole() & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS) & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # TODO: possibly fly over?
    rules_package.add_location_rule(CandyBox2LocationName.THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED, can_escape_hole() & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS) & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # The Forest rules
    rules_package.add_location_rule(CandyBox2LocationName.FOREST_QUEST_CLEARED, weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS) & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # Castle Entrance rules
    rules_package.add_location_rule(CandyBox2LocationName.CASTLE_ENTRANCE_QUEST_CLEARED, can_fly() | (weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS) & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR)))
    rules_package.add_location_rule(CandyBox2LocationName.KNIGHT_BODY_ARMOUR_ACQUIRED, weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS) & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # Castle rules
    rules_package.add_location_rule(CandyBox2LocationName.GIANT_NOUGAT_MONSTER_DEFEATED, can_cast(CandyBox2Castable.BLACK_HOLE) & weapon_is_at_least(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR) & rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN))

    # Egg Room
    rules_package.add_location_rule(CandyBox2LocationName.EGG_ROOM_QUEST_CLEARED, can_fly() | has_weapon(CandyBox2ItemName.NOTHING_WEAPON))

    # The Desert Fortress
    rules_package.add_location_rule(CandyBox2LocationName.XINOPHERYDON_DEFEATED, can_fly() & (has_weapon(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) | rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)))
    rules_package.add_location_rule(CandyBox2LocationName.XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED, can_fly())
    rules_package.add_location_rule(CandyBox2LocationName.TEAPOT_DEFEATED, weapon_is_at_least(CandyBox2ItemName.SCYTHE) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN) & rule_item(CandyBox2ItemName.SORCERESS_CAULDRON) & rule_item(CandyBox2ItemName.XINOPHERYDON_CLAW))
    rules_package.add_location_rule(CandyBox2LocationName.ROCKET_BOOTS_ACQUIRED, can_fly() | (rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION) & can_jump() & can_cast(CandyBox2Castable.TELEPORT) & (rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN) | has_weapon(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR))))

    # Hell rules
    rules_package.add_location_rule(CandyBox2LocationName.DEVIL_DEFEATED, can_cast(CandyBox2Castable.BLACK_DEMONS) & rule_item(CandyBox2ItemName.UNICORN_HORN) & rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION) & armor_is_at_least(CandyBox2ItemName.ENCHANTED_KNIGHT_BODY_ARMOUR) & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES) & has_weapon(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF))

    # Developer rules
    rules_package.add_location_rule(CandyBox2LocationName.THE_DEVELOPER_DEFEATED, can_farm_candies() & can_cast(CandyBox2Castable.BLACK_HOLE) & can_cast(CandyBox2Castable.TELEPORT))

    # The Sea rules
    rules_package.add_location_rule(CandyBox2LocationName.THE_SPONGE_ACQUIRED, sea_entrance())
    rules_package.add_location_rule(CandyBox2LocationName.THE_SHELL_POWDER_ACQUIRED, sea_entrance())
    rules_package.add_location_rule(CandyBox2LocationName.THE_RED_FIN_ACQUIRED, can_beat_sharks() & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS))
    rules_package.add_location_rule(CandyBox2LocationName.THE_GREEN_FIN_ACQUIRED, can_beat_sharks() & can_cast(CandyBox2Castable.ERASE_MAGIC) & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS))
    rules_package.add_location_rule(CandyBox2LocationName.THE_PURPLE_FIN_ACQUIRED, can_beat_sharks() & rule_item(CandyBox2ItemName.HEART_PENDANT) & rule_item(CandyBox2ItemName.HEART_PLUG) & can_cast(CandyBox2Castable.ERASE_MAGIC) & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES) & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS) & rule_item(CandyBox2ItemName.UNICORN_HORN))

    # Cyclops Puzzle
    rules_package.add_location_rule(CandyBox2LocationName.SOLVE_CYCLOPS_PUZZLE, rule_room(CandyBox2Room.DRAGON))

    # X Potion
    rules_package.add_location_rule(CandyBox2LocationName.YOURSELF_DEFEATED, rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN))

    # Cooking
    rules_package.add_location_rule(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_1, has_at_least_chocolates(9))
    rules_package.add_location_rule(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_2, has_at_least_chocolates(10))
    rules_package.add_location_rule(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_3, has_at_least_chocolates(11))
    rules_package.add_location_rule(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_4, has_at_least_chocolates(12))
    rules_package.add_location_rule(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_5, has_all_chocolates())

    # Sorceress items
    rules_package.add_location_rule(CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE, can_grow_lollipops())
    rules_package.add_location_rule(CandyBox2LocationName.SORCERESS_HUT_ADVANCED_GRIMOIRE, can_grow_lollipops())
    rules_package.add_location_rule(CandyBox2LocationName.SORCERESS_HUT_HAT, can_farm_lollipops())
    rules_package.add_location_rule(CandyBox2LocationName.SORCERESS_HUT_CAULDRON, can_grow_lollipops())

    # Merchant items
    rules_package.add_location_rule(CandyBox2LocationName.VILLAGE_SHOP_CHOCOLATE_BAR, can_farm_candies())
    rules_package.add_location_rule(CandyBox2LocationName.VILLAGE_SHOP_CANDY_MERCHANTS_HAT, can_farm_candies())

    return rules_package