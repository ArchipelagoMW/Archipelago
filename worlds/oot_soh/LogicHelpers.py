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
def add_locations(parent_region: Enum, world: "SohWorld", locations) -> None:
    for location in locations:
        locationName = location[0].value
        locationRule = lambda state: True
        if(len(location) > 1):
            locationRule = location[1]
        if locationName in world.included_locations:
            locationAddress = world.included_locations.pop(location[0])
            world.get_region(parent_region.value).add_locations({locationName: locationAddress}, SohLocation)
            set_rule(world.get_location(locationName), locationRule)


# todo: add typing for child_regions, change it from a list[list] to list[tuple]
def connect_regions(parent_region: Enum, world: "SohWorld", child_regions) -> None:
    for region in child_regions:
        world.get_region(parent_region.value).connect(world.get_region(region[0].value), rule=region[1])


def add_events(parent_region, world: "SohWorld", events):
    for event in events:
        event_location = event[0].value
        event_item = event[1].value
        event_rule = lambda state: True
        if(len(event) > 2):
            event_rule = event[2]
        
        world.get_region(parent_region).add_locations({event_location: None}, SohLocation)
        world.get_location(event_location).place_locked_item(SohItem(event_item, IC.progression, None, world.player))
        set_rule(world.get_location(event_location), event_rule)


# TODO account for starting nuts being disabled
# TODO account for starting sticks being disabled
# TODO add child wallet options
# TODO add bronze scale options
def has_item(itemName: Enum, state: CollectionState, world: "SohWorld", count: int = 1, can_be_child: bool = True,
             can_be_adult: bool = True) -> bool:
    player = world.player

    def can_use_item(name: Enum):
        return can_use(name, state, world, can_be_child, can_be_adult)
      
    if itemName in (Items.PROGRESSIVE_BOMBCHU, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20):
        return (state.has_any((Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20,
                               Items.PROGRESSIVE_BOMBCHU.value), world.player)
                or (bombchus_enabled(state, world)
                    and state.has_any((Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT), world.player)))

    if itemName == Items.FAIRY_OCARINA:
        return state.has_any((Items.FAIRY_OCARINA.value, Items.OCARINA_OF_TIME.value, Items.PROGRESSIVE_OCARINA.value), player)
    elif itemName == Items.OCARINA_OF_TIME:
        return state.has_any_count({Items.OCARINA_OF_TIME.value: 1, Items.PROGRESSIVE_OCARINA.value: 2}, player)
    elif itemName == Items.SCARECROW:
        return scarecrows_song(state, world) and can_use_item(Items.HOOKSHOT)
    elif itemName == Items.DISTANT_SCARECROW:
        return scarecrows_song(state, world) and can_use_item(Items.LONGSHOT)
    elif itemName == Items.DEKU_SHIELD:
        return state.has(Events.CAN_BUY_DEKU_SHIELD.value, player)
    # todo: a lot of these progressive items can probably be evaluated way more simply with a collect/remove override
    elif itemName == Items.PROGRESSIVE_GORON_SWORD:
        return state.has_any((Items.GIANTS_KNIFE.value, Items.BIGGORONS_SWORD.value, Items.PROGRESSIVE_GORON_SWORD.value), player)
    elif itemName == Items.GORONS_BRACELET:
        return state.has_any((Items.GORONS_BRACELET.value, Items.STRENGTH_UPGRADE.value), player)
    elif itemName == Items.SILVER_GAUNTLETS:
        return state.has_any_count({Items.SILVER_GAUNTLETS.value: 1, Items.STRENGTH_UPGRADE.value: 2}, player)
    elif itemName == Items.GOLDEN_GAUNTLETS:
        return state.has_any_count({Items.GOLDEN_GAUNTLETS.value: 1, Items.STRENGTH_UPGRADE.value: 3}, player)
    elif itemName == Items.ADULT_WALLET:
        return state.has_any((Items.ADULT_WALLET.value, Items.PROGRESSIVE_WALLET.value), player)
    elif itemName == Items.GIANT_WALLET:
        return state.has_any_count({Items.GIANT_WALLET.value: 1, Items.PROGRESSIVE_WALLET.value: 2}, player)
    elif itemName == Items.TYCOON_WALLET:
        return state.has_any_count({Items.TYCOON_WALLET.value: 1, Items.PROGRESSIVE_WALLET.value: 3}, player)
    elif itemName == Items.SILVER_SCALE:
        return state.has_any((Items.SILVER_SCALE.value, Items.PROGRESSIVE_SCALE.value), player)
    elif itemName == Items.GOLDEN_SCALE:
        return state.has_any_count({Items.GOLDEN_SCALE.value: 1, Items.PROGRESSIVE_SCALE.value: 2}, player)
    elif itemName == Items.MAGIC_BEAN:
        return state.has_any({Items.MAGIC_BEAN_PACK.value, Events.CAN_BUY_BEANS.value}, player)
    elif itemName == Items.CHILD_WALLET:
        return state.has(Items.PROGRESSIVE_WALLET.value, player) or world.options.shuffle_childs_wallet == 0
    # todo: is this for being able to catch a big poe??
    elif itemName == Items.BOTTLE_WITH_BIG_POE:
        return has_bottle(state, world)
    elif itemName == Items.BOTTLE_WITH_BUGS:
        return has_bottle(state, world) and state.has(Events.BUG_ACCESS.value, player)
    else:
        return state.has(itemName.value, player, count)


def can_use(name: Enum, state: CollectionState, world: "SohWorld", can_be_child: bool = True, can_be_adult: bool = True) -> bool:
    if not has_item(name, state, world):
        return False

    def has(item_name: Enum, count: int = 1):
        return has_item(item_name, state, world, count, can_be_child, can_be_adult)

    def can_use_item(item_name):
        return can_use(item_name, state, world, can_be_child, can_be_adult)

    data = item_data_table

    if data[name].adult_only and not can_be_adult:
        return False

    if data[name].child_only and not can_be_child:
        return False

    if data[name].item_type == ItemType.magic and not can_use_item(Items.PROGRESSIVE_MAGIC_METER):
        return False

    if data[name].item_type == ItemType.song:
        return can_play_song(state, world, name)

    if name in (Items.FIRE_ARROW, Items.ICE_ARROW, Items.LIGHT_ARROW):
        return can_use_item(Items.PROGRESSIVE_BOW)

    if "Bombchu" in name.value:
        return bombchu_refill(state, world) and bombchus_enabled(state, world)

    if name == Items.PROGRESSIVE_MAGIC_METER:
        return has(Events.AMMO_CAN_DROP) or (has_bottle(state, world) and has(Events.CAN_BUY_GREEN_POTION))
    elif name == Items.PROGRESSIVE_BOW:
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_ARROWS)
    elif name == Items.FAIRY_SLINGSHOT:
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_SEEDS)
    elif name == Items.NUTS:
        return has(Events.AMMO_CAN_DROP) and (has(Events.NUT_POT) or has(Events.NUT_CRATE) or has(Events.DEKU_BABA_NUTS))
    elif name == Items.STICKS:
        return has(Events.STICK_POT) or has(Events.DEKU_BABA_STICKS)
    elif name in (Items.PROGRESSIVE_BOMB_BAG, Items.BOMB_BAG):
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_BOMBS)
    elif name == Items.FISHING_POLE:
        return has(Items.CHILD_WALLET)  # as long as you have enough rubies

    return True


def scarecrows_song(state: CollectionState, world: "SohWorld") -> bool:
    # TODO handle scarecrow song option in place of the False
    return ((False and has_item(Items.FAIRY_OCARINA, state, world)
            and state.has_group_unique("Ocarina Buttons", world.player, 2))
            or (has_item(Events.CHILD_SCARECROW, state, world) and has_item(Events.ADULT_SCARECROW, state, world)))

def has_bottle(state: CollectionState, world: "SohWorld") -> bool:  # soup
    for bottle in no_rules_bottles:
        if state.has(bottle.value, world.player):
            return True
    if state.has_all((Events.DELIVER_LETTER.value, Items.BOTTLE_WITH_RUTOS_LETTER.value), world.player):
        return True
    if state.has_all((Events.CAN_EMPTY_BIG_POES.value, Items.BOTTLE_WITH_BIG_POE.value), world.player):
        return True
    return False


def bottle_count(state: CollectionState, world: "SohWorld") -> int:
    count = 0
    for bottle in no_rules_bottles:
        count += state.count(bottle.value, world.player)
    if state.has(Events.DELIVER_LETTER.value, world.player):
        count += state.count(Items.BOTTLE_WITH_RUTOS_LETTER.value, world.player)
    if state.has(Events.CAN_EMPTY_BIG_POES.value, world.player):
        count += state.count(Items.BOTTLE_WITH_BIG_POE.value, world.player)
    return count


def bombchu_refill(state: CollectionState, world: "SohWorld") -> bool:
    return state.has_any([Events.CAN_BUY_BOMBCHUS.value, Events.COULD_PLAY_BOWLING.value, Events.CARPET_MERCHANT.value], world.player) or False #TODO put enable bombchu drops option here


def bombchus_enabled(state: CollectionState, world: "SohWorld") -> bool:
    bombchu_bag_enabled = False
    if bombchu_bag_enabled:  # TODO bombchu bag enabled
        return has_item(Items.BOMBCHU_BAG, state, world)
    return has_item(Items.BOMB_BAG, state, world)


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


def can_play_song(state: CollectionState, world: "SohWorld", song: Enum) -> bool:
    if not has_item(Items.FAIRY_OCARINA, state, world):
        return False
    if not world.options.shuffle_ocarina_buttons:
        return True
    else:
        return state.has_all(ocarina_buttons_required[song.value], world.player)


def has_explosives(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has access to explosives (bombs or bombchus)."""
    return can_use(Items.PROGRESSIVE_BOMB_BAG, state, world) or can_use(Items.PROGRESSIVE_BOMBCHU, state, world)


def blast_or_smash(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can blast or smash obstacles."""
    return has_explosives(state, world) or can_use(Items.MEGATON_HAMMER, state, world)


def blue_fire(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has access to blue fire."""
    return can_use(Items.BOTTLE_WITH_BLUE_FIRE, state, world)  # or blue fire arrows


def can_use_sword(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use any sword."""
    return (can_use(Items.KOKIRI_SWORD, state, world) or
            can_use(Items.MASTER_SWORD, state, world) or
            can_use(Items.BIGGORONS_SWORD, state, world))


def has_projectile(state: CollectionState, world: "SohWorld", age: str = "either") -> bool:
    """Check if Link has access to projectiles."""
    if has_explosives(state, world):
        return True
    child_projectiles = (can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or 
                         can_use(Items.BOOMERANG, state, world))
    adult_projectiles = (can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or 
                         can_use(Items.PROGRESSIVE_BOW, state, world))
    
    if age == "child":
        return child_projectiles
    elif age == "adult":
        return adult_projectiles
    elif age == "both":
        return child_projectiles and adult_projectiles
    else:  # "either"
        return child_projectiles or adult_projectiles


def can_use_projectile(state: CollectionState, world: "SohWorld", age: str = "either") -> bool:
    return (has_explosives(state, world) or can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or
            can_use(Items.BOOMERANG, state, world) or can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
            can_use(Items.PROGRESSIVE_BOW, state, world))


def can_break_mud_walls(state: CollectionState, world: "SohWorld") -> bool:
    return blast_or_smash(state, world) or (can_do_trick("Blue Fire Mud Walls", state, world) and blue_fire(state, world))


def can_get_deku_baba_sticks(state: CollectionState, world: "SohWorld") -> bool:
    return can_use(Items.DEKU_STICK_1, state, world) or can_use(Items.BOOMERANG, state, world)


def can_get_deku_baba_nuts(state: CollectionState, world: "SohWorld") -> bool:
    return can_use_sword(state, world) or can_use(Items.BOOMERANG, state, world)


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
    return (can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or 
            can_jump_slash(state, world) or 
            has_explosives(state, world) or 
            can_use(Items.DINS_FIRE, state, world) or
            can_use(Items.PROGRESSIVE_BOW, state, world))


def can_attack(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can attack enemies (damage or stun)."""
    return (can_damage(state, world) or 
            can_use(Items.BOOMERANG, state, world) or
            can_use(Items.PROGRESSIVE_HOOKSHOT, state, world))


def can_standing_shield(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use a shield for standing blocks."""
    return (can_use(Items.MIRROR_SHIELD, state, world) or  # Only adult can use mirror shield
            (is_adult(state, world) and can_use(Items.HYLIAN_SHIELD, state, world)) or
            can_use(Items.DEKU_SHIELD, state, world))  # Only child can use deku shield


def can_shield(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use a shield for blocking or stunning."""
    return (can_use(Items.MIRROR_SHIELD, state, world) or
            can_use(Items.HYLIAN_SHIELD, state, world) or
            can_use(Items.DEKU_SHIELD, state, world))


def take_damage(state: CollectionState, world: "SohWorld") -> bool:
    # return CanUse(RG_BOTTLE_WITH_FAIRY) || EffectiveHealth() != 1 || CanUse(RG_NAYRUS_LOVE);
    return (can_use(Items.BOTTLE_WITH_FAIRY, state, world) or can_use(Items.NAYRUS_LOVE, state, world)
            or True)  #TODO: Implement "|| EffectiveHealth()"


def can_do_trick(trick: str, state: CollectionState, world: "SohWorld") -> bool:
    # TODO: Implement specific trick logic based on world settings
    # For now, return False for safety (no tricks assumed)
    return False

def can_get_nighttime_gs(state: CollectionState, world: "SohWorld") -> bool:
    return (can_use(Items.SUNS_SONG, state, world ) or
            can_do_trick("Nighttime Gold Skulltulas", state, world))


def can_break_pots(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can break pots for items."""
    return (can_jump_slash(state, world) or 
           can_use(Items.BOOMERANG, state, world) or
           has_explosives(state, world) or
           can_use(Items.PROGRESSIVE_HOOKSHOT, state, world))


def can_break_crates(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can break crates."""
    return (can_jump_slash(state, world) or 
            has_explosives(state, world))


def can_hit_eye_targets(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can hit eye switches/targets."""
    return (can_use(Items.PROGRESSIVE_BOW, state, world) or 
            can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or
            can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
            can_use(Items.BOOMERANG, state, world))


def can_stun_deku(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can stun Deku Scrubs."""
    return can_attack(state, world) or can_use(Items.DEKU_NUT_BAG, state, world) or can_shield(state, world) # Is this right for nuts?


def can_reflect_nuts(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can reflect Deku Nuts back at enemies."""
    return can_stun_deku(state, world)


def has_fire_source_with_torch(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has a fire source that can be used with a torch."""
    return has_fire_source(state, world) or can_use(Items.STICKS, state, world)


def has_fire_source(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has any fire source."""
    return (can_use(Items.DINS_FIRE, state, world) or 
            can_use(Items.FIRE_ARROW, state, world))


def can_jump_slash(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can perform a jump slash with any sword."""
    return (can_use(Items.KOKIRI_SWORD, state, world) or 
            can_use(Items.MASTER_SWORD, state, world) or 
            can_use(Items.BIGGORONS_SWORD, state, world) or
            can_use(Items.MEGATON_HAMMER, state, world))  # Hammer can substitute for sword in some cases

def call_gossip_fairy_except_suns(state: CollectionState, world: "SohWorld") -> bool:
    return (can_use(Items.ZELDAS_LULLABY, state, world) or
            can_use(Items.EPONAS_SONG, state, world) or
            can_use(Items.SONG_OF_TIME, state, world))

def call_gossip_fairy(state: CollectionState, world: "SohWorld") -> bool:
    return (call_gossip_fairy_except_suns(state, world) or
            can_use(Items.SUNS_SONG, state, world))

def can_break_lower_hives(state: CollectionState, world: "SohWorld") -> bool:
    return can_break_upper_hives(state, world) or can_use(Items.PROGRESSIVE_BOMB_BAG, state, world)

def can_break_upper_hives(state: CollectionState, world: "SohWorld") -> bool:
    return (can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
            can_use(Items.BOOMERANG, state, world) or
            (can_do_trick("Beehives With Bombchus", state, world)
             and can_use(Items.PROGRESSIVE_BOMBCHU, state, world)))

def can_open_storms_grotto(state: CollectionState, world: "SohWorld") -> bool:
    return (can_use(Items.SONG_OF_STORMS, state, world) and
            (has_item(Items.STONE_OF_AGONY, state, world)
             or can_do_trick("Hidden Grottos without Stone of Agony", state, world)))

def can_live(state: CollectionState, world: "SohWorld") -> bool:
    return state.has_any_count({"Heart Container": 1, "Heart Piece": 4}, world.player)

# BELOW IS AI SLOP
# Based on C++ Logic

def can_hit_switch(state: CollectionState, world: "SohWorld", distance: str = "close",
                   in_water: bool = False) -> bool:
    if distance == "close":
        return (can_jump_slash(state, world) or
                has_explosives(state, world) or
                can_use(Items.BOOMERANG, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, state, world))

    elif distance in ["short_jumpslash", "master_sword_jumpslash", "long_jumpslash"]:
        return can_jump_slash(state, world)

    elif distance == "bomb_throw":
        return has_explosives(state, world)

    elif distance == "boomerang":
        return can_use(Items.BOOMERANG, state, world)

    elif distance in ["hookshot", "longshot"]:
        return can_use(Items.PROGRESSIVE_HOOKSHOT, state, world)

    elif distance == "far":
        return (can_use(Items.PROGRESSIVE_BOW, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
                has_explosives(state, world))

    return False

def can_kill_enemy(state: CollectionState, world: "SohWorld", enemy: Enum, combat_range: Enum = EnemyDistance.CLOSE,
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
    def can_hit_at_range(range_type: Enum) -> bool:
        if range_type == EnemyDistance.CLOSE:
            return (can_jump_slash(state, world) or
                    has_explosives(state, world) or
                    can_use(Items.DINS_FIRE, state, world))

        elif range_type in [EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, EnemyDistance.LONG_JUMPSLASH]:
            return can_jump_slash(state, world)

        elif range_type == EnemyDistance.BOMB_THROW:
            return has_explosives(state, world)

        elif range_type == EnemyDistance.BOOMERANG:
            return can_use(Items.BOOMERANG, state, world)

        elif range_type == EnemyDistance.HOOKSHOT:
            return can_use(Items.PROGRESSIVE_HOOKSHOT, state, world)

        elif range_type == EnemyDistance.LONGSHOT:
            return can_use(Items.PROGRESSIVE_HOOKSHOT, state, world)  # Longshot is progressive hookshot level 2

        elif range_type == EnemyDistance.FAR:
            return (can_use(Items.PROGRESSIVE_BOW, state, world) or
                    can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or
                    can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
                    has_explosives(state, world))

        return False

    # Enemy-specific logic based on C++ implementation

    # Guards (need specific items or tricks)
    if enemy in [Enemies.GERUDO_GUARD, Enemies.BREAK_ROOM_GUARD]:
        return (can_use(Items.PROGRESSIVE_BOW, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
                has_explosives(state, world))

    # Gold Skulltulas and similar enemies that can be hit at various ranges
    if enemy in [Enemies.GOLD_SKULLTULA, Enemies.BIG_SKULLTULA]:
        return can_hit_at_range(combat_range)

    # Small enemies that are easy to kill
    if enemy in [Enemies.GOHMA_LARVA, Enemies.MAD_SCRUB, Enemies.DEKU_BABA, Enemies.WITHERED_DEKU_BABA]:
        return can_hit_at_range(combat_range)

    # Dodongo (requires explosives or specific attacks)
    if enemy == Enemies.DODONGO:
        if combat_range in [EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, EnemyDistance.LONG_JUMPSLASH]:
            return (can_jump_slash(state, world) or has_explosives(state, world))
        return has_explosives(state, world)

    # Lizalfos (requires good weapons)
    if enemy == Enemies.LIZALFOS:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                has_explosives(state, world))

    # Flying enemies
    if enemy in [Enemies.KEESE, Enemies.FIRE_KEESE]:
        return can_hit_at_range(combat_range)

    # Bubbles (need specific attacks)
    if enemy in [Enemies.BLUE_BUBBLE, Enemies.GREEN_BUBBLE]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
                can_use(Items.BOOMERANG, state, world))

    # Tough enemies
    if enemy in [Enemies.DEAD_HAND, Enemies.LIKE_LIKE, Enemies.FLOORMASTER, Enemies.WALLMASTER]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                has_explosives(state, world))

    # Stalfos (needs good weapons)
    if enemy == Enemies.STALFOS:
        return can_hit_at_range(combat_range) and (
                can_jump_slash(state, world) or
                can_use(Items.MEGATON_HAMMER, state, world))

    # Iron Knuckle (very tough)
    if enemy == Enemies.IRON_KNUCKLE:
        return (can_jump_slash(state, world) or
                can_use(Items.MEGATON_HAMMER, state, world) or
                has_explosives(state, world))

    # Fire enemies
    if enemy in [Enemies.FLARE_DANCER, Enemies.TORCH_SLUG]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
                has_explosives(state, world))

    # Wolfos
    if enemy in [Enemies.WOLFOS, Enemies.WHITE_WOLFOS]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                has_explosives(state, world))

    # Gerudo Warrior
    if enemy == Enemies.GERUDO_WARRIOR:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                has_explosives(state, world))

    # ReDeads and Gibdos
    if enemy in [Enemies.GIBDO, Enemies.REDEAD]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                can_use(Items.SUNS_SONG, state, world) or
                has_explosives(state, world))

    # Other enemies
    if enemy in [Enemies.MEG, Enemies.ARMOS, Enemies.DINOLFOS, Enemies.FREEZARD, Enemies.SHELL_BLADE, Enemies.SPIKE, Enemies.STINGER]:
        return can_hit_at_range(combat_range)

    # Water enemies
    if enemy in [Enemies.BIG_OCTO, Enemies.BARI, Enemies.SHABOM, Enemies.OCTOROK, Enemies.TENTACLE]:
        if in_water:
            return (can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
                    can_use(Items.PROGRESSIVE_BOW, state, world) or
                    has_explosives(state, world))
        return can_hit_at_range(combat_range)

    # Bosses
    if enemy in [Enemies.GOHMA, Enemies.KING_DODONGO, Enemies.BARINADE, Enemies.PHANTOM_GANON, Enemies.VOLVAGIA,
                       Enemies.MORPHA, Enemies.BONGO_BONGO, Enemies.TWINROVA, Enemies.GANONDORF, Enemies.GANON]:
        # Bosses generally require good weapons and specific strategies
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                has_explosives(state, world))

    # Dark Link (special case)
    if enemy == Enemies.DARK_LINK:
        return (can_use(Items.MEGATON_HAMMER, state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                has_explosives(state, world))

    # Beamos (needs ranged attacks)
    if enemy == Enemies.BEAMOS:
        return (can_use(Items.PROGRESSIVE_BOW, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
                has_explosives(state, world))

    # Purple Leever
    if enemy == Enemies.PURPLE_LEEVER:
        return can_hit_at_range(combat_range)

    # Anubis (tough enemy)
    if enemy == Enemies.ANUBIS:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW, state, world) or
                has_explosives(state, world))

    # Default case - assume basic combat is sufficient
    return can_damage(state, world)


def can_pass_enemy(state: CollectionState, world: "SohWorld", enemy: Enum) -> bool:
    """Check if Link can pass by an enemy (usually by killing or stunning it)."""
    return can_kill_enemy(state, world, enemy) # I think that we can be more permissive here, but for now this is fine


def can_cut_shrubs(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can cut shrubs (grass, bushes)."""
    return (can_use_sword(state, world) or
            can_use(Items.BOOMERANG, state, world) or 
            has_explosives(state, world) or
            can_use(Items.GORONS_BRACELET, state, world) or
            can_use(Items.MEGATON_HAMMER, state, world))


def hookshot_or_boomerang(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has hookshot or boomerang."""
    return (can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
            can_use(Items.BOOMERANG, state, world))

def can_open_underwater_chest(state: CollectionState, world: "SohWorld") -> bool:
    return (can_do_trick("RT Open Underwater Chest", state, world) and 
            can_use(Items.IRON_BOOTS, state, world) and 
            can_use(Items.HOOKSHOT, state, world))

def small_keys(key: Items, requiredAmount: int, state: CollectionState, world: "SohWorld") -> bool:
    if has_item(Items.SKELETON_KEY, state, world) or has_key_ring(key, state, world):
        return True

    return (state.has(key.value, world.player, requiredAmount))

def has_key_ring(key : Items, state: CollectionState, world: "SohWorld") -> bool:
    match key:
        case Items.FOREST_TEMPLE_SMALL_KEY:
            return has_item(Items.FOREST_TEMPLE_KEY_RING, state, world)
        case Items.FIRE_TEMPLE_SMALL_KEY:
            return has_item(Items.FIRE_TEMPLE_KEY_RING, state, world)
        case Items.WATER_TEMPLE_SMALL_KEY:
            return has_item(Items.WATER_TEMPLE_KEY_RING, state, world)
        case Items.BOTTOM_OF_THE_WELL_SMALL_KEY:
            return has_item(Items.BOTTOM_OF_THE_WELL_KEY_RING, state, world)
        case Items.SHADOW_TEMPLE_SMALL_KEY:
            return has_item(Items.SHADOW_TEMPLE_KEY_RING, state, world)
        case Items.GERUDO_FORTRESS_SMALL_KEY:
            return has_item(Items.GERUDO_FORTRESS_KEY_RING, state, world)
        case Items.SPIRIT_TEMPLE_SMALL_KEY:
            return has_item(Items.SPIRIT_TEMPLE_KEY_RING, state, world)
        case Items.GANONS_CASTLE_SMALL_KEY:
            return has_item(Items.GANONS_CASTLE_KEY_RING, state, world)
        case _:
            return False

def can_get_enemy_drop(state: CollectionState, world: "SohWorld", enemy : Enemies, range : EnemyDistance = EnemyDistance.CLOSE, aboveLink : bool = False) -> bool:
    if not can_kill_enemy(state, world, enemy, range):
        return False
    
    if range.value <= EnemyDistance.MASTER_SWORD_JUMPSLASH.value:
        return True
    
    drop = False
    match enemy:
        case Enemies.GOLD_SKULLTULA:
            if range in [EnemyDistance.BOOMERANG, EnemyDistance.HOOKSHOT, EnemyDistance.LONGSHOT]:
                drop = (can_use(Items.BOOMERANG, state, world) or can_use(Items.HOOKSHOT, state, world) or can_use(Items.LONGSHOT, state, world))

            return drop
        case Enemies.KEESE:
            return True
        case Enemies.FIRE_KEESE:
            return True
        case _:
            return aboveLink or (range.value <= EnemyDistance.BOOMERANG.value and can_use(Items.BOOMERANG, state, world))
        
def can_detonate_bomb_flowers(state: CollectionState, world: "SohWorld") -> bool:
    return (can_use(Items.PROGRESSIVE_BOW, state, world) or has_explosives(state, world) or can_use(Items.DINS_FIRE, state, world))

def can_detonate_upright_bomb_flower(state: CollectionState, world: "SohWorld") -> bool:
    return (can_detonate_bomb_flowers(state, world) 
            or has_item(Items.GORONS_BRACELET, state, world)
            or (can_do_trick("RT BLUE FIRE MUD WALLS", state, world)
                and blue_fire(state, world)
                and (False # EffectiveHealth Function. Not sure how to implement some of the stuff that is client setting specific
                    or can_use(Items.NAYRUS_LOVE, state, world)
                ))

            ) 