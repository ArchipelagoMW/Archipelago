from collections.abc import Callable
from enum import StrEnum
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import CandyBox2World

# an item is something you receive

candy_box_2_base_id: int = 7665000


class CandyBox2Item(Item):
    game: str = "Candy Box 2"


class CandyBox2ItemData(NamedTuple):
    code: int | None = None
    required_amount: Callable[["CandyBox2World"], int] = lambda _: 0
    classification: ItemClassification = ItemClassification.filler
    description: str | None = None


class CandyBox2ItemName(StrEnum):
    CANDY = "Candy"
    LOLLIPOP = "Lollipop"
    CHOCOLATE_BAR = "Chocolate Bar"
    HP_BAR = "HP Bar"
    TIME_RING = "Time Ring"
    CANDY_MERCHANTS_HAT = "Candy Merchant's Hat"
    LEATHER_GLOVES = "Leather Gloves"
    LEATHER_BOOTS = "Leather Boots"
    PROGRESSIVE_WORLD_MAP = "Progressive World Map"
    TROLLS_BLUDGEON = "Troll's Bludgeon"
    DESERT_BIRD_FEATHER = "Desert bird feather"
    BEGINNERS_GRIMOIRE = "Beginners' Grimoire"
    ADVANCED_GRIMOIRE = "Advanced Grimoire"
    SORCERESS_CAULDRON = "Sorceress' Cauldron"
    SORCERESS_HAT = "Sorceress' Hat"
    OCTOPUS_KING_CROWN = "Octopus King Crown"
    MONKEY_WIZARD_STAFF = "Monkey Wizard Staff"
    HEART_PLUG = "Heart Plug"
    POGO_STICK = "Pogo Stick"
    P_STONE = "P Stone"
    L_STONE = "L Stone"
    A_STONE = "A Stone"
    Y_STONE = "Y Stone"
    WOODEN_SWORD = "Wooden Sword"
    IRON_AXE = "Iron Axe"
    POLISHED_SILVER_SWORD = "Polished Silver Sword"
    LIGHTWEIGHT_BODY_ARMOUR = "Lightweight Body Armour"
    SCYTHE = "Scythe"
    RED_ENCHANTED_GLOVES = "Red Enchanted Gloves"
    PINK_ENCHANTED_GLOVES = "Pink Enchanted Gloves"
    SUMMONING_TRIBAL_SPEAR = "Summoning Tribal Spear"
    ENCHANTED_MONKEY_WIZARD_STAFF = "Enchanted Monkey Wizard Staff"
    ENCHANTED_KNIGHT_BODY_ARMOUR = "Enchanted Knight Body Armour"
    OCTOPUS_KING_CROWN_WITH_JASPERS = "Octopus King Crown with Jaspers"
    OCTOPUS_KING_CROWN_WITH_OBSIDIAN = "Octopus King Crown with Obsidian"
    GIANT_SPOON_OF_DOOM = "Giant Spoon of Doom"
    TRIBAL_SPEAR = "Tribal Spear"
    GIANT_SPOON = "Giant Spoon"
    DESERT_FORTRESS_KEY = "Desert Fortress Key"
    KNIGHT_BODY_ARMOUR = "Knight Body Armour"
    XINOPHERYDON_CLAW = "Xinopherydon Claw"
    UNICORN_HORN = "Unicorn Horn"
    ROCKET_BOOTS = "Rocket Boots"
    HEART_PENDANT = "Heart Pendant"
    BLACK_MAGIC_GRIMOIRE = "Black Magic Grimoire"
    FOUR_CHOCOLATE_BARS = "4 Chocolate Bars"
    PITCHFORK = "Pitchfork"
    TWENTY_CANDIES = "20 Candies"
    ONE_HUNDRED_CANDIES = "100 Candies"
    FIVE_HUNDRED_CANDIES = "500 Candies"
    THREE_LOLLIPOPS = "3 Lollipops"
    THREE_CHOCOLATE_BARS = "3 Chocolate Bars"
    THIRD_HOUSE_KEY = "Third House Key"
    SPONGE = "Sponge"
    SHELL_POWDER = "Shell Powder"
    RED_FIN = "Red Fin"
    GREEN_FIN = "Green Fin"
    PURPLE_FIN = "Purple Fin"
    LOCKED_CANDY_BOX = "Locked Candy Box"
    BOOTS_OF_INTROSPECTION = "Boots of Introspection"
    PAIN_AU_CHOCOLAT = "Pain au Chocolat"
    NOTHING_WEAPON = "Nothing (Weapon)"
    PROGRESSIVE_WEAPON = "Progressive Weapon"
    PROGRESSIVE_JUMP = "Progressive Jump"
    PROGRESSIVE_GRIMOIRE = "Progressive Grimoire"
    TWO_PAINS_AU_CHOCOLAT = "2 Pains au Chocolat"
    ACID_RAIN_SPELL = "Acid Rain Spell"
    FIREBALL_SPELL = "Fireball Spell"
    TELEPORT_SPELL = "Teleport Spell"
    ERASE_MAGIC_SPELL = "Erase Magic Spell"
    THORNS_SHIELD_SPELL = "Thorns Shield Spell"
    OBSIDIAN_WALL_SPELL = "Obsidian Wall Spell"
    BLACK_DEMONS_SPELL = "Black Demons Spell"
    FONT_TRAP = "Font Trap"


items: dict[CandyBox2ItemName, CandyBox2ItemData] = {
    CandyBox2ItemName.CANDY: CandyBox2ItemData(candy_box_2_base_id + 0, lambda _: 0, ItemClassification.skip_balancing),
    CandyBox2ItemName.LOLLIPOP: CandyBox2ItemData(candy_box_2_base_id + 1, lambda _: 8, ItemClassification.progression),
    CandyBox2ItemName.CHOCOLATE_BAR: CandyBox2ItemData(
        candy_box_2_base_id + 2, lambda _: 3, ItemClassification.progression
    ),
    CandyBox2ItemName.HP_BAR: CandyBox2ItemData(
        candy_box_2_base_id + 3, lambda world: hp_bar_count(world), ItemClassification.useful
    ),
    CandyBox2ItemName.TIME_RING: CandyBox2ItemData(candy_box_2_base_id + 4, lambda _: 1),
    CandyBox2ItemName.CANDY_MERCHANTS_HAT: CandyBox2ItemData(candy_box_2_base_id + 5, lambda _: 1),
    CandyBox2ItemName.LEATHER_GLOVES: CandyBox2ItemData(
        candy_box_2_base_id + 6, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.LEATHER_BOOTS: CandyBox2ItemData(candy_box_2_base_id + 7, lambda _: 1),
    CandyBox2ItemName.PROGRESSIVE_WORLD_MAP: CandyBox2ItemData(
        candy_box_2_base_id + 8, lambda _: 7, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.TROLLS_BLUDGEON: CandyBox2ItemData(
        candy_box_2_base_id + 9,
        lambda world: weapon_item_count(world, 9),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.DESERT_BIRD_FEATHER: CandyBox2ItemData(
        candy_box_2_base_id + 10, lambda world: jump_item_count(world), ItemClassification.progression
    ),
    CandyBox2ItemName.BEGINNERS_GRIMOIRE: CandyBox2ItemData(
        candy_box_2_base_id + 11,
        lambda world: grimoire_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.ADVANCED_GRIMOIRE: CandyBox2ItemData(
        candy_box_2_base_id + 12, lambda world: grimoire_item_count(world), ItemClassification.progression
    ),
    CandyBox2ItemName.SORCERESS_CAULDRON: CandyBox2ItemData(
        candy_box_2_base_id + 13, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.SORCERESS_HAT: CandyBox2ItemData(candy_box_2_base_id + 14, lambda _: 1),
    CandyBox2ItemName.OCTOPUS_KING_CROWN: CandyBox2ItemData(
        candy_box_2_base_id + 15, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.MONKEY_WIZARD_STAFF: CandyBox2ItemData(
        candy_box_2_base_id + 16,
        lambda world: weapon_item_count(world, 16),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.HEART_PLUG: CandyBox2ItemData(
        candy_box_2_base_id + 17, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.POGO_STICK: CandyBox2ItemData(
        candy_box_2_base_id + 18,
        lambda world: jump_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.P_STONE: CandyBox2ItemData(candy_box_2_base_id + 19, lambda _: 1, ItemClassification.progression),
    CandyBox2ItemName.L_STONE: CandyBox2ItemData(candy_box_2_base_id + 20, lambda _: 1, ItemClassification.progression),
    CandyBox2ItemName.A_STONE: CandyBox2ItemData(candy_box_2_base_id + 21, lambda _: 1, ItemClassification.progression),
    CandyBox2ItemName.Y_STONE: CandyBox2ItemData(candy_box_2_base_id + 22, lambda _: 1, ItemClassification.progression),
    CandyBox2ItemName.WOODEN_SWORD: CandyBox2ItemData(
        candy_box_2_base_id + 23,
        lambda world: weapon_item_count(world, 23),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.IRON_AXE: CandyBox2ItemData(
        candy_box_2_base_id + 24,
        lambda world: weapon_item_count(world, 24),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.POLISHED_SILVER_SWORD: CandyBox2ItemData(
        candy_box_2_base_id + 25,
        lambda world: weapon_item_count(world, 25),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR: CandyBox2ItemData(
        candy_box_2_base_id + 26, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.SCYTHE: CandyBox2ItemData(
        candy_box_2_base_id + 27,
        lambda world: weapon_item_count(world, 27),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.RED_ENCHANTED_GLOVES: CandyBox2ItemData(
        candy_box_2_base_id + 28, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.PINK_ENCHANTED_GLOVES: CandyBox2ItemData(
        candy_box_2_base_id + 29, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR: CandyBox2ItemData(
        candy_box_2_base_id + 30,
        lambda world: weapon_item_count(world, 30),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF: CandyBox2ItemData(
        candy_box_2_base_id + 31,
        lambda world: weapon_item_count(world, 31),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.ENCHANTED_KNIGHT_BODY_ARMOUR: CandyBox2ItemData(
        candy_box_2_base_id + 32, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS: CandyBox2ItemData(
        candy_box_2_base_id + 33, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN: CandyBox2ItemData(
        candy_box_2_base_id + 34, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.GIANT_SPOON_OF_DOOM: CandyBox2ItemData(
        candy_box_2_base_id + 35,
        lambda world: weapon_item_count(world, 35),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.TRIBAL_SPEAR: CandyBox2ItemData(
        candy_box_2_base_id + 36,
        lambda world: weapon_item_count(world, 36),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.GIANT_SPOON: CandyBox2ItemData(
        candy_box_2_base_id + 37,
        lambda world: weapon_item_count(world, 37),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.DESERT_FORTRESS_KEY: CandyBox2ItemData(
        candy_box_2_base_id + 38, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.KNIGHT_BODY_ARMOUR: CandyBox2ItemData(
        candy_box_2_base_id + 39, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.XINOPHERYDON_CLAW: CandyBox2ItemData(
        candy_box_2_base_id + 40, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.UNICORN_HORN: CandyBox2ItemData(
        candy_box_2_base_id + 41, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.ROCKET_BOOTS: CandyBox2ItemData(
        candy_box_2_base_id + 42,
        lambda world: jump_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.HEART_PENDANT: CandyBox2ItemData(
        candy_box_2_base_id + 43, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.BLACK_MAGIC_GRIMOIRE: CandyBox2ItemData(
        candy_box_2_base_id + 44,
        lambda world: grimoire_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.FOUR_CHOCOLATE_BARS: CandyBox2ItemData(
        candy_box_2_base_id + 45, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.PITCHFORK: CandyBox2ItemData(
        candy_box_2_base_id + 46, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.TWENTY_CANDIES: CandyBox2ItemData(
        candy_box_2_base_id + 47, lambda _: 1, ItemClassification.skip_balancing
    ),
    CandyBox2ItemName.ONE_HUNDRED_CANDIES: CandyBox2ItemData(
        candy_box_2_base_id + 48, lambda _: 1, ItemClassification.skip_balancing
    ),
    CandyBox2ItemName.FIVE_HUNDRED_CANDIES: CandyBox2ItemData(
        candy_box_2_base_id + 49, lambda _: 1, ItemClassification.skip_balancing
    ),
    CandyBox2ItemName.THREE_LOLLIPOPS: CandyBox2ItemData(
        candy_box_2_base_id + 50, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.THREE_CHOCOLATE_BARS: CandyBox2ItemData(
        candy_box_2_base_id + 51, lambda _: 2, ItemClassification.progression
    ),
    CandyBox2ItemName.THIRD_HOUSE_KEY: CandyBox2ItemData(
        candy_box_2_base_id + 52, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.SPONGE: CandyBox2ItemData(candy_box_2_base_id + 53, lambda _: 1, ItemClassification.progression),
    CandyBox2ItemName.SHELL_POWDER: CandyBox2ItemData(
        candy_box_2_base_id + 54, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.RED_FIN: CandyBox2ItemData(candy_box_2_base_id + 55, lambda _: 1, ItemClassification.useful),
    CandyBox2ItemName.GREEN_FIN: CandyBox2ItemData(
        candy_box_2_base_id + 56, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.PURPLE_FIN: CandyBox2ItemData(
        candy_box_2_base_id + 57, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.LOCKED_CANDY_BOX: CandyBox2ItemData(
        candy_box_2_base_id + 58, lambda _: 1, ItemClassification.progression
    ),
    CandyBox2ItemName.BOOTS_OF_INTROSPECTION: CandyBox2ItemData(
        candy_box_2_base_id + 59, lambda _: 1, ItemClassification.progression | ItemClassification.useful
    ),
    CandyBox2ItemName.PAIN_AU_CHOCOLAT: CandyBox2ItemData(
        candy_box_2_base_id + 60, lambda world: pain_au_chocolat_count(world, 1), ItemClassification.useful
    ),
    CandyBox2ItemName.NOTHING_WEAPON: CandyBox2ItemData(
        candy_box_2_base_id + 61,
        lambda world: weapon_item_count(world, 61),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.PROGRESSIVE_WEAPON: CandyBox2ItemData(
        candy_box_2_base_id + 62,
        lambda world: progressive_weapon_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.PROGRESSIVE_JUMP: CandyBox2ItemData(
        candy_box_2_base_id + 63,
        lambda world: progressive_jump_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.PROGRESSIVE_GRIMOIRE: CandyBox2ItemData(
        candy_box_2_base_id + 64,
        lambda world: progressive_grimoire_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.TWO_PAINS_AU_CHOCOLAT: CandyBox2ItemData(
        candy_box_2_base_id + 65, lambda world: pain_au_chocolat_count(world, 2), ItemClassification.useful
    ),
    CandyBox2ItemName.ACID_RAIN_SPELL: CandyBox2ItemData(
        candy_box_2_base_id + 66,
        lambda world: spell_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.FIREBALL_SPELL: CandyBox2ItemData(
        candy_box_2_base_id + 67,
        lambda world: spell_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.TELEPORT_SPELL: CandyBox2ItemData(
        candy_box_2_base_id + 68,
        lambda world: spell_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.ERASE_MAGIC_SPELL: CandyBox2ItemData(
        candy_box_2_base_id + 69,
        lambda world: spell_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.THORNS_SHIELD_SPELL: CandyBox2ItemData(
        candy_box_2_base_id + 70,
        lambda world: spell_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.OBSIDIAN_WALL_SPELL: CandyBox2ItemData(
        candy_box_2_base_id + 71,
        lambda world: spell_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.BLACK_DEMONS_SPELL: CandyBox2ItemData(
        candy_box_2_base_id + 72,
        lambda world: spell_item_count(world),
        ItemClassification.progression | ItemClassification.useful,
    ),
    CandyBox2ItemName.FONT_TRAP: CandyBox2ItemData(
        candy_box_2_base_id + 73, lambda world: font_trap_count(world), ItemClassification.trap
    ),
}

filler_items: list[str] = [CandyBox2ItemName.CANDY, CandyBox2ItemName.TWENTY_CANDIES]


def weapon_item_count(world: "CandyBox2World", weapon: int):
    if world.starting_weapon == weapon:
        # We start with this weapon, so none of these are required
        return 0

    if world.starting_weapon == -1:
        # We are using Progressive Weapons, so no weapons will be added to the pool
        return 0

    return 1


def progressive_weapon_count(world: "CandyBox2World"):
    if world.starting_weapon == -1:
        return 11

    # Progressive Weapons are disabled
    return 0


def progressive_grimoire_count(world: "CandyBox2World"):
    if world.grimoires == 1:  # Progressive Grimoires
        return 3

    # Progressive Grimoires are disabled
    return 0


def grimoire_item_count(world: "CandyBox2World"):
    if world.grimoires == 0:  # Individual Grimoires
        return 1

    return 0


def spell_item_count(world: "CandyBox2World"):
    if world.grimoires == 2:  # Individual Spells
        return 1

    return 0


def jump_item_count(world: "CandyBox2World"):
    if world.progressive_jump:
        return 0

    return 1


def progressive_jump_count(world: "CandyBox2World"):
    if world.progressive_jump:
        return 3

    # Progressive Jump is disabled
    return 0


def hp_bar_count(world: "CandyBox2World"):
    if world.options.randomise_hp_bar:
        return 1

    return 0


def pain_au_chocolat_count(world: "CandyBox2World", value: int):
    if value == 1:
        return 10 - world.pains_au_chocolat

    if value == 2:
        return world.pains_au_chocolat - 5

    return 0


def font_trap_count(world: "CandyBox2World"):
    return world.font_traps
