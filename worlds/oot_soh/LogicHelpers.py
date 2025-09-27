from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState, ItemClassification as IC
from .Locations import SohLocation
from worlds.generic.Rules import set_rule
from .Enums import *
from .Items import SohItem, item_data_table, ItemType, no_rules_bottles
from .RegionAgeAccess import can_access_entrance_as_adult, can_access_entrance_as_child, can_access_region_as_adult, can_access_region_as_child

if TYPE_CHECKING:
    from . import SohWorld

import logging
logger = logging.getLogger("SOH_OOT.Logic")


# todo: add typing for child_regions, change it from a list[list] to list[tuple]
def add_locations(parent_region: str, world: "SohWorld", locations) -> None:
    for location in locations:
        locationName = location[0]
        locationRule = lambda state: True
        if(len(location) < 2):
            locationRule = location[1]
        if locationName in world.included_locations:
            locationAddress = world.included_locations.pop(location[0])
            world.get_region(parent_region).add_locations({locationName: locationAddress}, SohLocation)
            set_rule(world.get_location(locationName), locationRule)


# todo: add typing for child_regions, change it from a list[list] to list[tuple]
def connect_regions(parent_region: str, world: "SohWorld", child_regions) -> None:
    for region in child_regions:
        world.get_region(parent_region).connect(world.get_region(region[0]), rule=region[1])


# todo: add typing for events, change it from list[list] to list[tuple]
def add_events(parent_region, world: "SohWorld", events):
    for event in events:
        event_location = event[0]
        event_item = event[1]
        event_rule = event[2]
        new_event = SohLocation(world.player, event_location, None, parent_region)
        new_event.place_locked_item(SohItem(event_item, IC.progression, None, world.player))
        set_rule(new_event, event_rule)


# TODO account for starting nuts being disabled
# TODO account for starting sticks being disabled
# TODO add child wallet options
# TODO add bronze scale options
def has_item(itemName: str, state: CollectionState, world: "SohWorld", count: int = 1, can_be_child: bool = True,
             can_be_adult: bool = True) -> bool:
    player = world.player

    def can_use_item(name: str):
        return can_use(name, state, world, can_be_child, can_be_adult)

    if itemName in (Items.PROGRESSIVE_BOMBCHU.value, Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value):
        return (state.has_any((Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value,
                               Items.PROGRESSIVE_BOMBCHU.value), world.player)
                or (bombchus_enabled(state, world)
                    and state.has_any((Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT), world.player)))

    if itemName == Items.FAIRY_OCARINA.value:
        return state.has_any((Items.FAIRY_OCARINA.value, Items.OCARINA_OF_TIME.value, Items.PROGRESSIVE_OCARINA.value), player)
    elif itemName == Items.OCARINA_OF_TIME.value:
        return state.has_any_count({Items.OCARINA_OF_TIME.value: 1, Items.PROGRESSIVE_OCARINA.value: 2}, player)
    elif itemName == Items.SCARECROW.value:
        return scarecrows_song(state, world) and can_use_item(Items.HOOKSHOT.value)
    elif itemName == Items.DISTANT_SCARECROW.value:
        return scarecrows_song(state, world) and can_use_item(Items.LONGSHOT.value)
    elif itemName == Items.DEKU_SHIELD.value:
        return state.has(Events.CAN_BUY_DEKU_SHIELD, player)
    # todo: a lot of these progressive items can probably be evaluated way more simply with a collect/remove override
    elif itemName == Items.PROGRESSIVE_GORON_SWORD.value:
        return state.has_any((Items.GIANTS_KNIFE.value, Items.BIGGORONS_SWORD.value, Items.PROGRESSIVE_GORON_SWORD.value), player)
    elif itemName == Items.GORONS_BRACELET.value:
        return state.has_any((Items.GORONS_BRACELET.value, Items.STRENGTH_UPGRADE.value), player)
    elif itemName == Items.SILVER_GAUNTLETS.value:
        return state.has_any_count({Items.SILVER_GAUNTLETS.value: 1, Items.STRENGTH_UPGRADE.value: 2}, player)
    elif itemName == Items.GOLDEN_GAUNTLETS.value:
        return state.has_any_count({Items.GOLDEN_GAUNTLETS.value: 1, Items.STRENGTH_UPGRADE.value: 3}, player)
    elif itemName == Items.MAGIC_SINGLE.value:
        return state.has_any((Items.MAGIC_SINGLE.value, Items.PROGRESSIVE_MAGIC_METER.value), player)
    elif itemName == Items.MAGIC_DOUBLE.value:
        return state.has_any_count({Items.MAGIC_DOUBLE.value: 1, Items.PROGRESSIVE_MAGIC_METER.value: 2}, player)
    elif itemName == Items.ADULT_WALLET.value:
        return state.has_any((Items.ADULT_WALLET.value, Items.PROGRESSIVE_WALLET.value), player)
    elif itemName == Items.GIANT_WALLET.value:
        return state.has_any_count({Items.GIANT_WALLET.value: 1, Items.PROGRESSIVE_WALLET.value: 2}, player)
    elif itemName == Items.TYCOON_WALLET.value:
        return state.has_any_count({Items.TYCOON_WALLET.value: 1, Items.PROGRESSIVE_WALLET.value: 3}, player)
    elif itemName == Items.SILVER_SCALE.value:
        return state.has_any((Items.SILVER_SCALE.value, Items.PROGRESSIVE_SCALE.value), player)
    elif itemName == Items.GOLDEN_SCALE.value:
        return state.has_any_count({Items.GOLDEN_SCALE.value: 1, Items.PROGRESSIVE_SCALE.value: 2}, player)
    # todo: is this for being able to catch a big poe??
    elif itemName == Items.BOTTLE_WITH_BIG_POE.value:
        return has_bottle(state, world)
    else:
        return state.has(itemName, player, count)


def can_use(name: str, state: CollectionState, world: "SohWorld", can_be_child: bool = True, can_be_adult: bool = True) -> bool:
    if not has_item(name, state, world):
        return False

    def has(item_name: str, count: int = 1):
        return has_item(item_name, state, world, count, can_be_child, can_be_adult)

    def can_use_item(item_name):
        return can_use(item_name, state, world, can_be_child, can_be_adult)

    data = item_data_table

    if data[name].adult_only and not can_be_adult:
        return False

    if data[name].child_only and not can_be_child:
        return False

    if data[name].item_type == ItemType.magic and not can_use_item(Items.MAGIC_SINGLE.value):
        return False

    if data[name].item_type == ItemType.song:
        return can_play_song(state, world, name)

    if name in (Items.FIRE_ARROW.value, Items.ICE_ARROW.value, Items.LIGHT_ARROW.value):
        return can_use_item(Items.FAIRY_BOW.value)

    if "Bombchu" in name:
        return bombchu_refill(state, world) and bombchus_enabled(state, world)

    if name == Items.MAGIC_SINGLE.value:
        return has(Events.AMMO_CAN_DROP) or (has_bottle(state, world) and has(Events.CAN_BUY_GREEN_POTION))
    elif name == Items.FAIRY_BOW.value:
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_ARROWS)
    elif name == Items.FAIRY_SLINGSHOT.value:
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_SEEDS)
    elif name == Items.NUTS.value:
        return has(Events.AMMO_CAN_DROP) and (has(Events.NUT_POT) or has(Events.NUT_CRATE) or has(Events.DEKU_BABA_NUTS))
    elif name == Items.STICKS.value:
        return has(Events.STICK_POT) or has(Events.DEKU_BABA_STICKS)
    elif name == Items.PROGRESSIVE_BOMB_BAG.value:
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_BOMBS)
    elif name == Items.BOMB_BAG.value:
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_BOMBS)
    elif name == Items.FISHING_POLE.value:
        return has(Items.CHILD_WALLET.value)  # as long as you have enough rubies

    return True


def scarecrows_song(state: CollectionState, world: "SohWorld") -> bool:
    # TODO handle scarecrow song option in place of the False
    return ((False and has_item(Items.FAIRY_OCARINA.value, state, world)
            and state.has_group_unique("Ocarina Buttons", world.player, 2))
            or (has_item(Events.CHILD_SCARECROW, state, world) and has_item(Events.ADULT_SCARECROW, state, world)))


def has_bottle(state: CollectionState, world: "SohWorld") -> bool:  # soup
    if state.has_any(no_rules_bottles, world.player):
        return True
    if state.has_all((Events.DELIVER_LETTER, Items.BOTTLE_WITH_RUTOS_LETTER.value), world.player):
        return True
    if state.has_all((Events.CAN_EMPTY_BIG_POES, Items.BOTTLE_WITH_BIG_POE.value), world.player):
        return True
    return False


def bottle_count(state: CollectionState, world: "SohWorld") -> int:
    count = state.count_from_list(no_rules_bottles, world.player)
    if state.has(Events.DELIVER_LETTER, world.player):
        count += state.count(Items.BOTTLE_WITH_RUTOS_LETTER.value, world.player)
    if state.has(Events.CAN_EMPTY_BIG_POES, world.player):
        count += state.count(Items.BOTTLE_WITH_BIG_POE.value, world.player)
    return count


def bombchu_refill(state: CollectionState, world: "SohWorld") -> bool:
    return state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player) or False #TODO put enable bombchu drops option here


def bombchus_enabled(state: CollectionState, world: "SohWorld") -> bool:
    bombchu_bag_enabled = False
    if bombchu_bag_enabled:  # TODO bombchu bag enabled
        return has_item(Items.BOMBCHU_BAG.value, state, world)
    return has_item(Items.BOMB_BAG.value, state, world)


ocarina_buttons_required: dict[str, list[str]] = {
    Items.ZELDAS_LULLABY.value: [Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value,Items.OCARINA_CUP_BUTTON.value],
    Items.EPONAS_SONG.value: [Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value],
    Items.PRELUDE_OF_LIGHT.value: [Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value],
    Items.SARIAS_SONG.value: [Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value],
    Items.SUNS_SONG.value: [Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value],
    Items.SONG_OF_TIME.value: [Items.OCARINA_A_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value],
    Items.BOLERO_OF_FIRE.value: [Items.OCARINA_A_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value],
    Items.REQUIEM_OF_SPIRIT.value: [Items.OCARINA_A_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value],
    Items.SONG_OF_STORMS.value: [Items.OCARINA_A_BUTTON.value, Items.OCARINA_CUP_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value],
    Items.MINUET_OF_FOREST.value: [Items.OCARINA_A_BUTTON.value, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value],
    Items.SERENADE_OF_WATER.value: [Items.OCARINA_A_BUTTON.value, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value],
}


def can_play_song(state: CollectionState, world: "SohWorld", song: str) -> bool:
    if not has_item(Items.FAIRY_OCARINA.value, state, world):
        return False
    if not world.options.shuffle_ocarina_buttons:
        return True
    else:
        return state.has_all(ocarina_buttons_required[song], world.player)


def has_explosives(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has access to explosives (bombs or bombchus)."""
    return can_use(Items.PROGRESSIVE_BOMB_BAG.value, state, world) or can_use(Items.PROGRESSIVE_BOMBCHU.value, state, world)


def blast_or_smash(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can blast or smash obstacles."""
    return has_explosives(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world)


def blue_fire(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has access to blue fire."""
    return can_use(Items.BOTTLE_WITH_BLUE_FIRE.value, state, world)  # or blue fire arrows


def can_use_sword(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use any sword."""
    return (can_use(Items.KOKIRI_SWORD.value, state, world) or
            can_use(Items.MASTER_SWORD.value, state, world) or
            can_use(Items.BIGGORONS_SWORD.value, state, world))


def has_projectile(state: CollectionState, world: "SohWorld", age: str = "either") -> bool:
    """Check if Link has access to projectiles."""
    if has_explosives(state, world):
        return True
    child_projectiles = (can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or 
                         can_use(Items.BOOMERANG.value, state, world))
    adult_projectiles = (can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or 
                         can_use(Items.PROGRESSIVE_BOW.value, state, world))
    
    if age == "child":
        return child_projectiles
    elif age == "adult":
        return adult_projectiles
    elif age == "both":
        return child_projectiles and adult_projectiles
    else:  # "either"
        return child_projectiles or adult_projectiles


def can_use_projectile(state: CollectionState, world: "SohWorld", age: str = "either") -> bool:
    return (has_explosives(state, world) or can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or
            can_use(Items.BOOMERANG.value, state, world) or can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
            can_use(Items.PROGRESSIVE_BOW.value, state, world))


def can_break_mud_walls(state: CollectionState, world: "SohWorld") -> bool:
    return blast_or_smash(state, world) or (can_do_trick("Blue Fire Mud Walls", state, world) and blue_fire(state, world))


def can_get_deku_baba_sticks(state: CollectionState, world: "SohWorld") -> bool:
    return can_use(Items.DEKU_STICK_1.value, state, world) or can_use(Items.BOOMERANG.value, state, world)


def can_get_deku_baba_nuts(state: CollectionState, world: "SohWorld") -> bool:
    return can_use_sword(state, world) or can_use(Items.BOOMERANG.value, state, world)


def is_adult(state: CollectionState, world: "SohWorld") -> bool:
    # For now, return True as a placeholder since age logic is complex and context-dependent
    # The real age checking should be done through the CanUse function's can_be_adult parameter
    # TODO: Implement proper age checking based on world settings and progression
    return True


def is_child(state: CollectionState, world: "SohWorld") -> bool:
    # For now, return True as a placeholder since age logic is complex and context-dependent
    # The real age checking should be done through the CanUse function's can_be_adult parameter
    # TODO: Implement proper age checking based on world settings and progression
    return True


def can_damage(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can deal damage to enemies."""
    return (can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or 
            can_jump_slash(state, world) or 
            has_explosives(state, world) or 
            can_use(Items.DINS_FIRE.value, state, world) or
            can_use(Items.PROGRESSIVE_BOW.value, state, world))


def can_attack(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can attack enemies (damage or stun)."""
    return (can_damage(state, world) or 
            can_use(Items.BOOMERANG.value, state, world) or
            can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world))


def can_standing_shield(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use a shield for standing blocks."""
    return (can_use(Items.MIRROR_SHIELD.value, state, world) or  # Only adult can use mirror shield
            (is_adult(state, world) and can_use(Items.HYLIAN_SHIELD.value, state, world)) or
            can_use(Items.DEKU_SHIELD.value, state, world))  # Only child can use deku shield


def can_shield(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use a shield for blocking or stunning."""
    return (can_use(Items.MIRROR_SHIELD.value, state, world) or
            can_use(Items.HYLIAN_SHIELD.value, state, world) or
            can_use(Items.DEKU_SHIELD.value, state, world))


def take_damage(state: CollectionState, world: "SohWorld") -> bool:
    # return CanUse(RG_BOTTLE_WITH_FAIRY) || EffectiveHealth() != 1 || CanUse(RG_NAYRUS_LOVE);
    return (can_use(Items.BOTTLE_WITH_FAIRY.value, state, world) or can_use(Items.NAYRUS_LOVE.value, state, world)
            or True)  #TODO: Implement "|| EffectiveHealth()"


def can_do_trick(trick: str, state: CollectionState, world: "SohWorld") -> bool:
    # TODO: Implement specific trick logic based on world settings
    # For now, return False for safety (no tricks assumed)
    return False


def can_break_pots(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can break pots for items."""
    return (can_jump_slash(state, world) or 
           can_use(Items.BOOMERANG.value, state, world) or
           has_explosives(state, world) or
           can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world))


def can_break_crates(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can break crates."""
    return (can_jump_slash(state, world) or 
            has_explosives(state, world))


def can_hit_eye_targets(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can hit eye switches/targets."""
    return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or 
            can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or
            can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
            can_use(Items.BOOMERANG.value, state, world))


def can_stun_deku(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can stun Deku Scrubs."""
    return can_attack(state, world) or can_use(Items.DEKU_NUT_BAG.value, state, world) or can_shield(state, world) # Is this right for nuts?


def can_reflect_nuts(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can reflect Deku Nuts back at enemies."""
    return can_stun_deku(state, world)


def has_fire_source_with_torch(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has a fire source that can be used with a torch."""
    return has_fire_source(state, world) or can_use(Items.STICKS, state, world)


def has_fire_source(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has any fire source."""
    return (can_use(Items.DINS_FIRE.value, state, world) or 
            can_use(Items.FIRE_ARROW.value, state, world))


def can_jump_slash(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can perform a jump slash with any sword."""
    return (can_use(Items.KOKIRI_SWORD.value, state, world) or 
            can_use(Items.MASTER_SWORD.value, state, world) or 
            can_use(Items.BIGGORONS_SWORD.value, state, world) or
            can_use(Items.MEGATON_HAMMER.value, state, world))  # Hammer can substitute for sword in some cases


# BELOW IS AI SLOP
# Based on C++ Logic

def can_hit_switch(state: CollectionState, world: "SohWorld", distance: str = "close",
                   in_water: bool = False) -> bool:
    if distance == "close":
        return (can_jump_slash(state, world) or
                has_explosives(state, world) or
                can_use(Items.BOOMERANG.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world))

    elif distance in ["short_jumpslash", "master_sword_jumpslash", "long_jumpslash"]:
        return can_jump_slash(state, world)

    elif distance == "bomb_throw":
        return has_explosives(state, world)

    elif distance == "boomerang":
        return can_use(Items.BOOMERANG.value, state, world)

    elif distance in ["hookshot", "longshot"]:
        return can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world)

    elif distance == "far":
        return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                has_explosives(state, world))

    return False

def can_kill_enemy(state: CollectionState, world: "SohWorld", enemy: str, combat_range: str = CombatRanges.CLOSE.value,
                   wall_or_floor: bool = True, quantity: int = 1, timer: bool = False, in_water: bool = False) -> bool:
    """
    Check if Link can kill a specific enemy at a given combat range.
    Based on the C++ Logic::CanKillEnemy implementation.

    Args:
        enemy: Enemy type (e.g., "gold_skulltula", "keese", etc.)
        combat_range: Combat range - "close", "short_jumpslash", "master_sword_jumpslash",
                     "long_jumpslash", "bomb_throw", "boomerang", "hookshot", "longshot", "far"
        wall_or_floor: Whether enemy is on wall or floor
        quantity: Number of enemies (for ammo considerations)
        timer: Whether there's a timer constraint
        in_water: Whether the fight is underwater
    """

    # Define what weapons work at each range
    def can_hit_at_range(range_type: str) -> bool:
        if range_type == CombatRanges.CLOSE.value:
            return (can_jump_slash(state, world) or
                    has_explosives(state, world) or
                    can_use(Items.DINS_FIRE.value, state, world))

        elif range_type in [CombatRanges.SHORT_JUMPSLASH.value, CombatRanges.MASTER_SWORD_JUMPSLASH.value, CombatRanges.LONG_JUMPSLASH.value]:
            return can_jump_slash(state, world)

        elif range_type == CombatRanges.BOMB_THROW.value:
            return has_explosives(state, world)

        elif range_type == CombatRanges.BOOMERANG.value:
            return can_use(Items.BOOMERANG.value, state, world)

        elif range_type == CombatRanges.HOOKSHOT.value:
            return can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world)

        elif range_type == CombatRanges.LONGSHOT.value:
            return can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world)  # Longshot is progressive hookshot level 2

        elif range_type == CombatRanges.FAR.value:
            return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                    can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or
                    can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                    has_explosives(state, world))

        return False

    # Enemy-specific logic based on C++ implementation

    # Guards (need specific items or tricks)
    if enemy in [Enemies.GERUDO_GUARD.value, Enemies.BREAK_ROOM_GUARD.value]:
        return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                has_explosives(state, world))

    # Gold Skulltulas and similar enemies that can be hit at various ranges
    if enemy in [Enemies.GOLD_SKULLTULA.value, Enemies.BIG_SKULLTULA.value]:
        return can_hit_at_range(combat_range)

    # Small enemies that are easy to kill
    if enemy in [Enemies.GOHMA_LARVA.value, Enemies.MAD_SCRUB.value, Enemies.DEKU_BABA.value, Enemies.WITHERED_DEKU_BABA.value]:
        return can_hit_at_range(combat_range)

    # Dodongo (requires explosives or specific attacks)
    if enemy == Enemies.DODONGO.value:
        if combat_range in [CombatRanges.CLOSE.value, CombatRanges.SHORT_JUMPSLASH.value, CombatRanges.MASTER_SWORD_JUMPSLASH.value, CombatRanges.LONG_JUMPSLASH.value]:
            return (can_jump_slash(state, world) or has_explosives(state, world))
        return has_explosives(state, world)

    # Lizalfos (requires good weapons)
    if enemy == Enemies.LIZALFOS.value:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Flying enemies
    if enemy in [Enemies.KEESE.value, Enemies.FIRE_KEESE.value]:
        return can_hit_at_range(combat_range)

    # Bubbles (need specific attacks)
    if enemy in [Enemies.BLUE_BUBBLE.value, Enemies.GREEN_BUBBLE.value]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                can_use(Items.BOOMERANG.value, state, world))

    # Tough enemies
    if enemy in [Enemies.DEAD_HAND.value, Enemies.LIKE_LIKE.value, Enemies.FLOORMASTER.value, Enemies.WALLMASTER.value]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Stalfos (needs good weapons)
    if enemy == Enemies.STALFOS.value:
        return can_hit_at_range(combat_range) and (
                can_jump_slash(state, world) or
                can_use(Items.MEGATON_HAMMER.value, state, world))

    # Iron Knuckle (very tough)
    if enemy == Enemies.IRON_KNUCKLE.value:
        return (can_jump_slash(state, world) or
                can_use(Items.MEGATON_HAMMER.value, state, world) or
                has_explosives(state, world))

    # Fire enemies
    if enemy in [Enemies.FLARE_DANCER.value, Enemies.TORCH_SLUG.value]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                has_explosives(state, world))

    # Wolfos
    if enemy in [Enemies.WOLFOS.value, Enemies.WHITE_WOLFOS.value]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Gerudo Warrior
    if enemy == Enemies.GERUDO_WARRIOR.value:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # ReDeads and Gibdos
    if enemy in [Enemies.GIBDO.value, Enemies.REDEAD.value]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.SUNS_SONG.value, state, world) or
                has_explosives(state, world))

    # Other enemies
    if enemy in [Enemies.MEG.value, Enemies.ARMOS.value, Enemies.DINOLFOS.value, Enemies.FREEZARD.value, Enemies.SHELL_BLADE.value, Enemies.SPIKE.value, Enemies.STINGER.value]:
        return can_hit_at_range(combat_range)

    # Water enemies
    if enemy in [Enemies.BIG_OCTO.value, Enemies.BARI.value, Enemies.SHABOM.value, Enemies.OCTOROK.value, Enemies.TENTACLE.value]:
        if in_water:
            return (can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                    can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                    has_explosives(state, world))
        return can_hit_at_range(combat_range)

    # Bosses
    if enemy in [Enemies.GOHMA.value, Enemies.KING_DODONGO.value, Enemies.BARINADE.value, Enemies.PHANTOM_GANON.value, Enemies.VOLVAGIA.value,
                       Enemies.MORPHA.value, Enemies.BONGO_BONGO.value, Enemies.TWINROVA.value, Enemies.GANONDORF.value, Enemies.GANON.value]:
        # Bosses generally require good weapons and specific strategies
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Dark Link (special case)
    if enemy == Enemies.DARK_LINK.value:
        return (can_use(Items.MEGATON_HAMMER.value, state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Beamos (needs ranged attacks)
    if enemy == Enemies.BEAMOS.value:
        return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                has_explosives(state, world))

    # Purple Leever
    if enemy == Enemies.PURPLE_LEEVER.value:
        return can_hit_at_range(combat_range)

    # Anubis (tough enemy)
    if enemy == Enemies.ANUBIS.value:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Default case - assume basic combat is sufficient
    return can_damage(state, world)


def can_pass_enemy(state: CollectionState, world: "SohWorld", enemy: str) -> bool:
    """Check if Link can pass by an enemy (usually by killing or stunning it)."""
    return can_kill_enemy(state, world, enemy) # I think that we can be more permissive here, but for now this is fine


def can_cut_shrubs(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can cut shrubs (grass, bushes)."""
    return (can_use_sword(state, world) or
            can_use(Items.BOOMERANG.value, state, world) or 
            has_explosives(state, world) or
            can_use(Items.GORONS_BRACELET.value, state, world) or
            can_use(Items.MEGATON_HAMMER.value, state, world))


def hookshot_or_boomerang(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has hookshot or boomerang."""
    return (can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
            can_use(Items.BOOMERANG.value, state, world))
