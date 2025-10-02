from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState, ItemClassification as IC
from .Locations import SohLocation
from worlds.generic.Rules import set_rule
from .Enums import *
from .Items import SohItem, item_data_table, ItemType, no_rules_bottles, item_name_groups

if TYPE_CHECKING:
    from . import SohWorld

import logging
logger = logging.getLogger("SOH_OOT.Logic")


class rule_wrapper:
    def __init__(self, parent_region: Regions, rule: Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool], world: "SohWorld"):
        self.parent_region = parent_region
        self.world = world
        self.rule = rule

    @staticmethod
    def wrap(parent_region: Regions, rule: Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool], world: "SohWorld") -> Callable[[CollectionState], bool]:
        wrapper = rule_wrapper(parent_region, rule, world)
        return wrapper.evaluate

    def evaluate(self, state: CollectionState) -> bool:
        return self.rule((state, self.parent_region, self.world))


def add_locations(parent_region: Regions, world: "SohWorld", 
                  locations: list[tuple[Locations, Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool]]]) -> None:
    for location in locations:
        locationName = location[0].value
        locationRule = lambda bundle: True
        if len(location) > 1:
            locationRule = location[1]
        if locationName in world.included_locations:
            locationAddress = world.included_locations.pop(location[0])
            world.get_region(parent_region.value).add_locations({locationName: locationAddress}, SohLocation)
            set_rule(world.get_location(locationName), rule_wrapper.wrap(parent_region, locationRule, world))



def connect_regions(parent_region: Regions, world: "SohWorld", 
                    child_regions: list[tuple[Regions, Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool]]]) -> None:
    for region in child_regions:
        regionName = region[0]
        regionRule = lambda bundle: True
        if len(region) > 1:
            regionRule = region[1]
        world.get_region(parent_region.value).connect(world.get_region(regionName.value), 
                                                      rule=rule_wrapper.wrap(parent_region, regionRule, world))


def add_events(parent_region: Regions, world: "SohWorld", 
               events: list[tuple[Enum, Events | Enum, Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool]]]) -> None:
    for event in events:
        event_location = event[0].value
        event_item = event[1].value
        event_rule = lambda bundle: True
        if len(event) > 2:
            event_rule = event[2]
        
        world.get_region(parent_region.value).add_locations({event_location: None}, SohLocation)
        world.get_location(event_location).place_locked_item(SohItem(event_item, IC.progression, None, world.player))
        set_rule(world.get_location(event_location), rule_wrapper.wrap(parent_region, event_rule, world))


# TODO account for starting nuts being disabled
# TODO account for starting sticks being disabled
# TODO add child wallet options
# TODO add bronze scale options
def has_item(item: Items | Events | Enum, bundle: tuple[CollectionState, Regions, "SohWorld"], count: int = 1) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    player = world.player

    def can_use_item(name: Enum, bundle):
        return can_use(name, bundle)
      
    if item in (Items.PROGRESSIVE_BOMBCHU, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20):
        return (state.has_any((Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value,
                               Items.PROGRESSIVE_BOMBCHU.value), world.player)
                or (bombchus_enabled(bundle)
                    and state.has_any((Events.CAN_BUY_BOMBCHUS.value, Events.COULD_PLAY_BOWLING.value, Events.CARPET_MERCHANT.value), world.player)))

    if item == Items.FAIRY_OCARINA:
        return state.has_any((Items.FAIRY_OCARINA.value, Items.OCARINA_OF_TIME.value, Items.PROGRESSIVE_OCARINA.value), player)
    elif item == Items.OCARINA_OF_TIME:
        return state.has_any_count({Items.OCARINA_OF_TIME.value: 1, Items.PROGRESSIVE_OCARINA.value: 2}, player)
    elif item == Items.SCARECROW:
        return scarecrows_song(bundle) and can_use_item(Items.HOOKSHOT, bundle)
    elif item == Items.DISTANT_SCARECROW:
        return scarecrows_song(bundle) and can_use_item(Items.LONGSHOT, bundle)
    elif item == Items.DEKU_SHIELD:
        return state.has(Events.CAN_BUY_DEKU_SHIELD.value, player)
    # todo: a lot of these progressive items can probably be evaluated way more simply with a collect/remove override
    elif item == Items.PROGRESSIVE_GORON_SWORD:
        return state.has_any((Items.GIANTS_KNIFE.value, Items.BIGGORONS_SWORD.value, Items.PROGRESSIVE_GORON_SWORD.value), player)
    elif item == Items.GORONS_BRACELET:
        return state.has_any((Items.GORONS_BRACELET.value, Items.STRENGTH_UPGRADE.value), player)
    elif item == Items.SILVER_GAUNTLETS:
        return state.has_any_count({Items.SILVER_GAUNTLETS.value: 1, Items.STRENGTH_UPGRADE.value: 2}, player)
    elif item == Items.GOLDEN_GAUNTLETS:
        return state.has_any_count({Items.GOLDEN_GAUNTLETS.value: 1, Items.STRENGTH_UPGRADE.value: 3}, player)
    elif item == Items.ADULT_WALLET:
        return state.has_any((Items.ADULT_WALLET.value, Items.PROGRESSIVE_WALLET.value), player)
    elif item == Items.GIANT_WALLET:
        return state.has_any_count({Items.GIANT_WALLET.value: 1, Items.PROGRESSIVE_WALLET.value: 2}, player)
    elif item == Items.TYCOON_WALLET:
        return state.has_any_count({Items.TYCOON_WALLET.value: 1, Items.PROGRESSIVE_WALLET.value: 3}, player)
    elif item == Items.SILVER_SCALE:
        return state.has_any((Items.SILVER_SCALE.value, Items.PROGRESSIVE_SCALE.value), player)
    elif item == Items.GOLDEN_SCALE:
        return state.has_any_count({Items.GOLDEN_SCALE.value: 1, Items.PROGRESSIVE_SCALE.value: 2}, player)
    elif item == Items.MAGIC_BEAN:
        return state.has_any({Items.MAGIC_BEAN_PACK.value, Events.CAN_BUY_BEANS.value}, player)
    elif item == Items.CHILD_WALLET:
        return state.has(Items.PROGRESSIVE_WALLET.value, player) or world.options.shuffle_childs_wallet == 0
    # todo: is this for being able to catch a big poe??
    elif item == Items.BOTTLE_WITH_BIG_POE:
        return has_bottle(bundle)
    elif item == Items.BOTTLE_WITH_BUGS:
        return has_bottle(bundle) and state.has(Events.BUG_ACCESS.value, player)
    elif item == Items.BRONZE_SCALE:
        return world.options.shuffle_swim == 0 or state.has(Items.PROGRESSIVE_SCALE.value, player)
    else:
        return state.has(item.value, player, count)

def can_use_any(names: list[Enum], bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    for name in names:
        if can_use(name, bundle):
            return True
    return False

def can_use(item: Enum, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    if not has_item(item, bundle):
        return False

    def has(item_name: Enum, count: int = 1):
        return has_item(item_name, bundle, count)

    def can_use_item(item_name):
        return can_use(item_name, bundle)

    data = item_data_table

    if data[item].adult_only and not is_adult(bundle):
        return False

    if data[item].child_only and not is_child(bundle):
        return False

    if data[item].item_type == ItemType.magic and not can_use_item(Items.PROGRESSIVE_MAGIC_METER):
        return False

    if data[item].item_type == ItemType.song:
        return can_play_song(bundle, item)

    if item in (Items.FIRE_ARROW, Items.ICE_ARROW, Items.LIGHT_ARROW):
        return can_use_item(Items.PROGRESSIVE_BOW)

    if item in [Items.PROGRESSIVE_BOMBCHU,Items.BOMBCHUS_5,Items.BOMBCHUS_10,Items.BOMBCHUS_20]:
        return bombchu_refill(bundle) and bombchus_enabled(bundle)

    if item == Items.PROGRESSIVE_MAGIC_METER:
        return has(Events.AMMO_CAN_DROP) or (has_bottle(bundle) and has(Events.CAN_BUY_GREEN_POTION))
    elif item == Items.PROGRESSIVE_BOW:
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_ARROWS)
    elif item == Items.FAIRY_SLINGSHOT:
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_SEEDS)
    elif item == Items.NUTS:
        return has(Events.AMMO_CAN_DROP) and (has(Events.NUT_POT) or has(Events.NUT_CRATE) or has(Events.DEKU_BABA_NUTS))
    elif item == Items.STICKS:
        return has(Events.STICK_POT) or has(Events.DEKU_BABA_STICKS)
    elif item in (Items.PROGRESSIVE_BOMB_BAG, Items.BOMB_BAG):
        return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_BOMBS)
    elif item == Items.FISHING_POLE:
        return has(Items.CHILD_WALLET)  # as long as you have enough rubies

    return True


def scarecrows_song(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    # TODO handle scarecrow song option in place of the False
    return ((False and has_item(Items.FAIRY_OCARINA, bundle)
            and state.has_group_unique("Ocarina Buttons", world.player, 2))
            or (has_item(Events.CHILD_SCARECROW, bundle) and has_item(Events.ADULT_SCARECROW, bundle)))

def has_bottle(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:  # soup
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    for bottle in no_rules_bottles:
        if state.has(bottle.value, world.player):
            return True
    if state.has_all((Events.DELIVER_LETTER.value, Items.BOTTLE_WITH_RUTOS_LETTER.value), world.player):
        return True
    if state.has_all((Events.CAN_EMPTY_BIG_POES.value, Items.BOTTLE_WITH_BIG_POE.value), world.player):
        return True
    return False


def bottle_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    count = 0
    for bottle in no_rules_bottles:
        count += state.count(bottle.value, world.player)
    if state.has(Events.DELIVER_LETTER.value, world.player):
        count += state.count(Items.BOTTLE_WITH_RUTOS_LETTER.value, world.player)
    if state.has(Events.CAN_EMPTY_BIG_POES.value, world.player):
        count += state.count(Items.BOTTLE_WITH_BIG_POE.value, world.player)
    return count


def bombchu_refill(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    return state.has_any([Events.CAN_BUY_BOMBCHUS.value, Events.COULD_PLAY_BOWLING.value, Events.CARPET_MERCHANT.value], world.player) or False #TODO put enable bombchu drops option here


def bombchus_enabled(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    bombchu_bag_enabled = False
    if bombchu_bag_enabled:  # TODO bombchu bag enabled
        return has_item(Items.BOMBCHU_BAG, bundle)
    return has_item(Items.BOMB_BAG, bundle)


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


def can_play_song(bundle: tuple[CollectionState, Regions, "SohWorld"], song: Enum) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    if not has_item(Items.FAIRY_OCARINA, bundle):
        return False
    if not world.options.shuffle_ocarina_buttons:
        return True
    else:
        return state.has_all(ocarina_buttons_required[song.value], world.player)


def has_explosives(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has access to explosives (bombs or bombchus)."""
    return can_use_any([Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_BOMBCHU], bundle)


def blast_or_smash(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can blast or smash obstacles."""
    return has_explosives(bundle) or can_use(Items.MEGATON_HAMMER, bundle)


def blue_fire(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has access to blue fire."""
    return can_use(Items.BOTTLE_WITH_BLUE_FIRE, bundle)  # or blue fire arrows


def can_use_sword(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can use any sword."""
    return can_use_any([Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.PROGRESSIVE_BOMBCHU], bundle)

def has_projectile(bundle: tuple[CollectionState, Regions, "SohWorld"], age: str = "either") -> bool:
    """Check if Link has access to projectiles."""
    if has_explosives(bundle):
        return True
    child_projectiles = (can_use(Items.PROGRESSIVE_SLINGSHOT, bundle) or 
                         can_use(Items.BOOMERANG, bundle))
    adult_projectiles = (can_use(Items.PROGRESSIVE_HOOKSHOT, bundle) or 
                         can_use(Items.PROGRESSIVE_BOW, bundle))
    
    if age == "child":
        return child_projectiles
    elif age == "adult":
        return adult_projectiles
    elif age == "both":
        return child_projectiles and adult_projectiles
    else:  # "either"
        return child_projectiles or adult_projectiles


def can_use_projectile(bundle: tuple[CollectionState, Regions, "SohWorld"], age: str = "either") -> bool:
    return (can_use_any([Items.PROGRESSIVE_SLINGSHOT,Items.BOOMERANG,Items.PROGRESSIVE_HOOKSHOT,Items.PROGRESSIVE_BOW], bundle)
        or has_explosives(bundle))


def can_break_mud_walls(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return blast_or_smash(bundle) or (can_do_trick("Blue Fire Mud Walls", bundle) and blue_fire(bundle))


def can_get_deku_baba_sticks(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_use(Items.DEKU_STICK_1, bundle) or can_use(Items.BOOMERANG, bundle)


def can_get_deku_baba_nuts(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_use_sword(bundle) or can_use(Items.BOOMERANG, bundle)


def is_adult(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    return state._soh_can_reach_as_age(parent_region, Ages.ADULT, world.player)


def is_child(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    return state._soh_can_reach_as_age(parent_region, Ages.CHILD, world.player)


def starting_age(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    # Todo use is_child or is_adult based on starting age setting
    return (world.options.starting_age == 'child' and is_child(bundle)) or (world.options.starting_age == 'adult' and is_adult(bundle))


def can_damage(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can deal damage to enemies."""
    return (can_jump_slash(bundle) or
            has_explosives(bundle) or
            can_use_any([Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.DINS_FIRE], bundle)
            )


def can_attack(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can attack enemies (damage or stun)."""
    return (can_damage(bundle) or 
            can_use(Items.BOOMERANG, bundle) or
            can_use(Items.PROGRESSIVE_HOOKSHOT, bundle))


def can_standing_shield(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can use a shield for standing blocks."""
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    return (can_use(Items.MIRROR_SHIELD, bundle) or  # Only adult can use mirror shield
            (is_adult(bundle) and can_use(Items.HYLIAN_SHIELD, bundle)) or
            can_use(Items.DEKU_SHIELD, bundle))  # Only child can use deku shield


def can_shield(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can use a shield for blocking or stunning."""
    return can_use_any([Items.MIRROR_SHIELD,Items.HYLIAN_SHIELD,Items.DEKU_SHIELD], bundle)


def take_damage(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    # return CanUse(RG_BOTTLE_WITH_FAIRY) || EffectiveHealth() != 1 || CanUse(RG_NAYRUS_LOVE);
    return (can_use(Items.BOTTLE_WITH_FAIRY, bundle) or can_use(Items.NAYRUS_LOVE, bundle)
            or True)  #TODO: Implement "|| EffectiveHealth()"


def can_do_trick(trick: str, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    # TODO: Implement specific trick logic based on world settings
    # For now, return False for safety (no tricks assumed)
    return False

def can_get_nighttime_gs(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (can_use(Items.SUNS_SONG, bundle ) or
            can_do_trick("Nighttime Gold Skulltulas", bundle))


def can_break_pots(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can break pots for items."""
    return True


def can_break_crates(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can break crates."""
    return True
  

def can_break_small_crates(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can break small crates."""
    return True

def can_hit_eye_targets(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can hit eye switches/targets."""
    return can_use_any([Items.PROGRESSIVE_BOW,Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_HOOKSHOT, Items.BOOMERANG], bundle)


def can_stun_deku(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can stun Deku Scrubs."""
    return (can_attack(bundle) or can_use(Items.DEKU_NUT_BAG, bundle) or can_reflect_nuts(bundle))


def can_reflect_nuts(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can reflect Deku Nuts back at enemies."""
    return (can_use(Items.DEKU_SHIELD, bundle) or (is_adult(bundle) and has_item(Items.HYLIAN_SHIELD, bundle)))


def has_fire_source_with_torch(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has a fire source that can be used with a torch."""
    return has_fire_source(bundle) or can_use(Items.STICKS, bundle)


def has_fire_source(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has any fire source."""
    return (can_use(Items.DINS_FIRE, bundle) or 
            can_use(Items.FIRE_ARROW, bundle))

def can_jump_slash_except_hammer(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can perform a jump slash with any sword."""
    return (can_use(Items.STICKS, bundle) or can_use_sword(bundle))

def can_jump_slash(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can perform a jump slash at all"""
    return (can_jump_slash_except_hammer(bundle) or can_use(Items.MEGATON_HAMMER, bundle))

def call_gossip_fairy_except_suns(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_use_any([Items.ZELDAS_LULLABY, Items.EPONAS_SONG, Items.SONG_OF_TIME], bundle)

def call_gossip_fairy(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (call_gossip_fairy_except_suns(bundle) or
            can_use(Items.SUNS_SONG, bundle))

def can_break_lower_hives(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_break_upper_beehives(bundle) or can_use(Items.PROGRESSIVE_BOMB_BAG, bundle)

def can_break_upper_beehives(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (hookshot_or_boomerang(bundle) or
            (can_do_trick("Beehives With Bombchus", bundle) and can_use(Items.PROGRESSIVE_BOMBCHU, bundle)) and 
            (False and (can_use(Items.PROGRESSIVE_BOW, bundle) or can_use(Items.PROGRESSIVE_SLINGSHOT, bundle))))

def can_open_storms_grotto(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (can_use(Items.SONG_OF_STORMS, bundle) and
            (has_item(Items.STONE_OF_AGONY, bundle)
             or can_do_trick("Hidden Grottos without Stone of Agony", bundle)))

def can_live(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    return state.has_any_count({"Heart Container": 1, "Heart Piece": 4}, world.player)

# BELOW IS AI SLOP
# Based on C++ Logic
def can_hit_switch(bundle: tuple[CollectionState, Regions, "SohWorld"], distance: EnemyDistance = EnemyDistance.CLOSE,
                   in_water: bool = False) -> bool:
    hit = False
    
    if(distance.value <= EnemyDistance.SHORT_JUMPSLASH.value):
        hit = can_use(Items.KOKIRI_SWORD, bundle) or can_use(Items.MEGATON_HAMMER, bundle)

    if(distance.value <= EnemyDistance.MASTER_SWORD_JUMPSLASH.value):
        hit = hit or can_use(Items.MASTER_SWORD, bundle)

    if(distance.value <= EnemyDistance.LONG_JUMPSLASH.value):
        hit = hit or can_use(Items.BIGGORONS_SWORD, bundle) or can_use(Items.STICKS, bundle)

    if(distance.value <= EnemyDistance.BOMB_THROW.value):
        hit = hit or (not in_water and can_use(Items.BOMB_BAG, bundle))
        
    if(distance.value <= EnemyDistance.BOOMERANG.value):
        hit = hit or can_use(Items.BOOMERANG, bundle)

    if(distance.value <= EnemyDistance.HOOKSHOT.value):
        hit = hit or has_item(Items.PROGRESSIVE_HOOKSHOT, bundle) or can_use(Items.BOMBCHUS_5, bundle)

    if(distance.value <= EnemyDistance.LONGSHOT.value):
        hit = hit or has_item(Items.PROGRESSIVE_HOOKSHOT, bundle, 2)

    if(distance.value <= EnemyDistance.FAR.value):
        hit = hit or can_use(Items.PROGRESSIVE_SLINGSHOT, bundle) or can_use(Items.PROGRESSIVE_BOW, bundle)

    return hit

def can_kill_enemy(bundle: tuple[CollectionState, Regions, "SohWorld"], enemy: Enemies, distance: EnemyDistance = EnemyDistance.CLOSE,
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
    def can_hit_at_range(distance: EnemyDistance) -> bool:
        if distance == EnemyDistance.CLOSE:
            return (can_jump_slash(bundle) or
                    has_explosives(bundle) or
                    can_use(Items.DINS_FIRE, bundle))

        elif distance in [EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, EnemyDistance.LONG_JUMPSLASH]:
            return can_jump_slash(bundle)

        elif distance == EnemyDistance.BOMB_THROW:
            return has_explosives(bundle)

        elif distance == EnemyDistance.BOOMERANG:
            return can_use(Items.BOOMERANG, bundle)

        elif distance == EnemyDistance.HOOKSHOT:
            return can_use(Items.PROGRESSIVE_HOOKSHOT, bundle)

        elif distance == EnemyDistance.LONGSHOT:
            return can_use(Items.PROGRESSIVE_HOOKSHOT, bundle)  # Longshot is progressive hookshot level 2

        elif distance == EnemyDistance.FAR:
            return (can_use(Items.PROGRESSIVE_BOW, bundle) or
                    can_use(Items.PROGRESSIVE_SLINGSHOT, bundle) or
                    can_use(Items.PROGRESSIVE_HOOKSHOT, bundle) or
                    has_explosives(bundle))

        return False

    # Enemy-specific logic based on C++ implementation

    # Guards (need specific items or tricks)
    if enemy in [Enemies.GERUDO_GUARD, Enemies.BREAK_ROOM_GUARD]:
        return (can_use(Items.PROGRESSIVE_BOW, bundle) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, bundle) or
                has_explosives(bundle))

    # Gold Skulltulas and similar enemies that can be hit at various ranges
    if enemy in [Enemies.GOLD_SKULLTULA, Enemies.BIG_SKULLTULA]:
        return can_hit_at_range(distance)

    # Small enemies that are easy to kill
    if enemy in [Enemies.GOHMA_LARVA, Enemies.MAD_SCRUB, Enemies.DEKU_BABA, Enemies.WITHERED_DEKU_BABA]:
        return can_hit_at_range(distance)

    # Dodongo (requires explosives or specific attacks)
    if enemy == Enemies.DODONGO:
        if distance in [EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, EnemyDistance.LONG_JUMPSLASH]:
            return (can_jump_slash(bundle) or has_explosives(bundle))
        return has_explosives(bundle)

    # Lizalfos (requires good weapons)
    if enemy == Enemies.LIZALFOS:
        return (can_jump_slash(bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                has_explosives(bundle))

    # Flying enemies
    if enemy in [Enemies.KEESE, Enemies.FIRE_KEESE]:
        return can_hit_at_range(distance)

    # Bubbles (need specific attacks)
    if enemy in [Enemies.BLUE_BUBBLE, Enemies.GREEN_BUBBLE]:
        return (can_jump_slash(bundle) or
                can_use_any([Items.PROGRESSIVE_BOW,Items.PROGRESSIVE_HOOKSHOT,Items.BOOMERANG], bundle))

    # Tough enemies
    if enemy in [Enemies.DEAD_HAND, Enemies.LIKE_LIKE, Enemies.FLOORMASTER, Enemies.WALLMASTER]:
        return (can_jump_slash(bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                has_explosives(bundle))

    # Stalfos (needs good weapons)
    if enemy == Enemies.STALFOS:
        return can_hit_at_range(distance) and (
                can_jump_slash(bundle) or
                can_use(Items.MEGATON_HAMMER, bundle))

    # Iron Knuckle (very tough)
    if enemy == Enemies.IRON_KNUCKLE:
        return (can_jump_slash(bundle) or
                can_use(Items.MEGATON_HAMMER, bundle) or
                has_explosives(bundle))

    # Fire enemies
    if enemy in [Enemies.FLARE_DANCER, Enemies.TORCH_SLUG]:
        return (can_jump_slash(bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, bundle) or
                has_explosives(bundle))

    # Wolfos
    if enemy in [Enemies.WOLFOS, Enemies.WHITE_WOLFOS]:
        return (can_jump_slash(bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                has_explosives(bundle))

    # Gerudo Warrior
    if enemy == Enemies.GERUDO_WARRIOR:
        return (can_jump_slash(bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                has_explosives(bundle))

    # ReDeads and Gibdos
    if enemy in [Enemies.GIBDO, Enemies.REDEAD]:
        return (can_jump_slash(bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                can_use(Items.SUNS_SONG, bundle) or
                has_explosives(bundle))

    # Other enemies
    if enemy in [Enemies.MEG, Enemies.ARMOS, Enemies.DINOLFOS, Enemies.FREEZARD, Enemies.SHELL_BLADE, Enemies.SPIKE, Enemies.STINGER]:
        return can_hit_at_range(distance)

    # Water enemies
    if enemy in [Enemies.BIG_OCTO, Enemies.BARI, Enemies.SHABOM, Enemies.OCTOROK, Enemies.TENTACLE]:
        if in_water:
            return (can_use(Items.PROGRESSIVE_HOOKSHOT, bundle) or
                    can_use(Items.PROGRESSIVE_BOW, bundle) or
                    has_explosives(bundle))
        return can_hit_at_range(distance)

    # Bosses
    if enemy in [Enemies.GOHMA, Enemies.KING_DODONGO, Enemies.BARINADE, Enemies.PHANTOM_GANON, Enemies.VOLVAGIA,
                       Enemies.MORPHA, Enemies.BONGO_BONGO, Enemies.TWINROVA, Enemies.GANONDORF, Enemies.GANON]:
        # Bosses generally require good weapons and specific strategies
        return (can_jump_slash(bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                has_explosives(bundle))

    # Dark Link (special case)
    if enemy == Enemies.DARK_LINK:
        return (can_use(Items.MEGATON_HAMMER, bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                has_explosives(bundle))

    # Beamos (needs ranged attacks)
    if enemy == Enemies.BEAMOS:
        return (can_use(Items.PROGRESSIVE_BOW, bundle) or
                can_use(Items.PROGRESSIVE_HOOKSHOT, bundle) or
                has_explosives(bundle))

    # Purple Leever
    if enemy == Enemies.PURPLE_LEEVER:
        return can_hit_at_range(distance)

    # Anubis (tough enemy)
    if enemy == Enemies.ANUBIS:
        return (can_jump_slash(bundle) or
                can_use(Items.PROGRESSIVE_BOW, bundle) or
                has_explosives(bundle))

    # Default case - assume basic combat is sufficient
    return can_damage(bundle)


def can_pass_enemy(bundle: tuple[CollectionState, Regions, "SohWorld"], enemy: Enemies) -> bool:
    """Check if Link can pass by an enemy (usually by killing or stunning it)."""
    return can_kill_enemy(bundle, enemy) # I think that we can be more permissive here, but for now this is fine


def can_cut_shrubs(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can cut shrubs (grass, bushes)."""
    return (can_use_sword(bundle) or
            can_use(Items.BOOMERANG, bundle) or 
            has_explosives(bundle) or
            can_use(Items.GORONS_BRACELET, bundle) or
            can_use(Items.MEGATON_HAMMER, bundle))


def hookshot_or_boomerang(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has hookshot or boomerang."""
    return (can_use(Items.PROGRESSIVE_HOOKSHOT, bundle) or
            can_use(Items.BOOMERANG, bundle))

def can_open_underwater_chest(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (can_do_trick("RT Open Underwater Chest", bundle) and 
            can_use(Items.IRON_BOOTS, bundle) and 
            can_use(Items.HOOKSHOT, bundle))

def small_keys(key: Items, requiredAmount: int, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    if has_item(Items.SKELETON_KEY, bundle) or (world.options.key_rings.value and has_key_ring(key, bundle)):
        return True

    return (state.has(key.value, world.player, requiredAmount))

def has_key_ring(key : Items, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    match key:
        case Items.FOREST_TEMPLE_SMALL_KEY:
            return has_item(Items.FOREST_TEMPLE_KEY_RING, bundle)
        case Items.FIRE_TEMPLE_SMALL_KEY:
            return has_item(Items.FIRE_TEMPLE_KEY_RING, bundle)
        case Items.WATER_TEMPLE_SMALL_KEY:
            return has_item(Items.WATER_TEMPLE_KEY_RING, bundle)
        case Items.BOTTOM_OF_THE_WELL_SMALL_KEY:
            return has_item(Items.BOTTOM_OF_THE_WELL_KEY_RING, bundle)
        case Items.SHADOW_TEMPLE_SMALL_KEY:
            return has_item(Items.SHADOW_TEMPLE_KEY_RING, bundle)
        case Items.GERUDO_FORTRESS_SMALL_KEY:
            return has_item(Items.GERUDO_FORTRESS_KEY_RING, bundle)
        case Items.SPIRIT_TEMPLE_SMALL_KEY:
            return has_item(Items.SPIRIT_TEMPLE_KEY_RING, bundle)
        case Items.GANONS_CASTLE_SMALL_KEY:
            return has_item(Items.GANONS_CASTLE_KEY_RING, bundle)
        case _:
            return False

def can_get_enemy_drop(bundle: tuple[CollectionState, Regions, "SohWorld"], enemy : Enemies, distance : EnemyDistance = EnemyDistance.CLOSE, aboveLink : bool = False) -> bool:
    if not can_kill_enemy(bundle, enemy, distance):
        return False
    
    if distance.value <= EnemyDistance.MASTER_SWORD_JUMPSLASH.value:
        return True

    match enemy:
        case Enemies.GOLD_SKULLTULA:
            if distance in [EnemyDistance.BOOMERANG, EnemyDistance.HOOKSHOT, EnemyDistance.LONGSHOT]:
                return (can_use_any([Items.BOOMERANG, Items.HOOKSHOT, Items.LONGSHOT], bundle))

            return False
        case Enemies.KEESE:
            return True
        case Enemies.FIRE_KEESE:
            return True
        case _:
            return aboveLink or (distance.value <= EnemyDistance.BOOMERANG.value and can_use(Items.BOOMERANG, bundle))
        
def can_detonate_bomb_flowers(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_use_any([Items.PROGRESSIVE_BOW, Items.DINS_FIRE], bundle) or has_explosives(bundle)

def can_detonate_upright_bomb_flower(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (can_detonate_bomb_flowers(bundle) 
            or has_item(Items.GORONS_BRACELET, bundle)
            or (can_do_trick("RT BLUE FIRE MUD WALLS", bundle)
                and blue_fire(bundle)
                and (False # EffectiveHealth Function. Not sure how to implement some of the stuff that is client setting specific
                    or can_use(Items.NAYRUS_LOVE, bundle)
                ))

            )

def item_group_count(bundle: tuple[CollectionState, Regions, "SohWorld"], item_group: str) -> int:
    state = bundle[0]
    world = bundle[2]
    items = item_name_groups[item_group]
    count = 0
    for item in items:
        if (state.has(item, world.player)):
            count += 1
    return count

def ocarina_button_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return item_group_count(bundle, "Ocarina Buttons")

def stone_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return item_group_count(bundle, "Stones")

def medallion_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return item_group_count(bundle, "Medallions")

dungeon_events: list[Events] = [Events.CLEARED_DEKU_TREE, Events.CLEARED_DODONGOS_CAVERN, Events.CLEARED_JABU_JABUS_BELLY, 
                      Events.CLEARED_FOREST_TEMPLE, Events.CLEARED_FIRE_TEMPLE, Events.CLEARED_WATER_TEMPLE, 
                      Events.CLEARED_SPIRIT_TEMPLE, Events.CLEARED_SHADOW_TEMPLE]
def dungeon_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    count = 0
    for dungeon in dungeon_events:
        if has_item(dungeon, bundle):
            count += 1
    return count

def can_spawn_soil_skull(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (is_child(bundle) and can_use(Items.BOTTLE_WITH_BUGS, bundle))

def fire_timer(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return 255 if can_use(Items.GORON_TUNIC, bundle) else ((hearts(bundle) * 8) if can_do_trick("Fewer Tunic Requirements", bundle) else 0)

def water_timer(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return 255 if can_use(Items.ZORA_TUNIC, bundle) else ((hearts(bundle) * 8) if can_do_trick("Fewer Tunic Requirements", bundle) else 0)

def hearts(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    state = bundle[0]
    world = bundle[2]
    return (3 + state.count(Items.HEART_CONTAINER.value, world.player) + (state.count(Items.PIECE_OF_HEART.value, world.player) // 4))

def can_open_bomb_grotto(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return blast_or_smash(bundle) and (has_item(Items.STONE_OF_AGONY, bundle) or can_do_trick("Grottos Without Agony", bundle))

def trade_quest_step(item: Items, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]
    if (world.options.shuffle_adult_trade_items.value):
        return False
    
    hasState = False

    if (item == Items.POCKET_EGG):
        hasState = hasState or has_item(Items.POCKET_EGG, bundle)

    if (item == Items.COJIRO):
        hasState = hasState or has_item(Items.COJIRO, bundle)

    if (item == Items.ODD_MUSHROOM):
        hasState = hasState or has_item(Items.ODD_MUSHROOM, bundle)

    if (item == Items.ODD_POTION):
        hasState = hasState or has_item(Items.ODD_POTION, bundle)

    if (item == Items.POACHERS_SAW):
        hasState = hasState or has_item(Items.POACHERS_SAW, bundle)

    if (item == Items.BROKEN_GORONS_SWORD):
        hasState = hasState or has_item(Items.BROKEN_GORONS_SWORD, bundle)
    
    if (item == Items.PRESCRIPTION):
        hasState = hasState or has_item(Items.PRESCRIPTION, bundle)

    if (item == Items.WORLDS_FINEST_EYEDROPS):
        hasState = hasState or has_item(Items.WORLDS_FINEST_EYEDROPS, bundle)

    if (item == Items.CLAIM_CHECK):
        hasState = hasState or has_item(Items.CLAIM_CHECK, bundle)

    return hasState

def can_build_rainbow_bridge(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]

    greg_wildcard = 0
    if has_item(Items.GREG_THE_GREEN_RUPEE, bundle) and world.options.rainbow_bridge_greg_reward.value:
        greg_wildcard = 1

    return (world.options.rainbow_bridge.value == 1 or
            (world.options.rainbow_bridge.value == 0 and has_item(Items.SHADOW_MEDALLION, bundle) and has_item(Items.SPIRIT_MEDALLION, bundle) and can_use(Items.LIGHT_ARROW, bundle)) or
            (world.options.rainbow_bridge.value == 2 and ((stone_count(bundle) + greg_wildcard) >= world.options.rainbow_bridge_stones_required.value)) or
            (world.options.rainbow_bridge.value == 3 and ((medallion_count(bundle) + greg_wildcard) >= world.options.rainbow_bridge_medallions_required.value)) or
            (world.options.rainbow_bridge.value == 4 and ((stone_count(bundle) + medallion_count(bundle) + greg_wildcard) >= world.options.rainbow_bridge_dungeon_rewards_required.value)) or
            (world.options.rainbow_bridge.value == 5 and ((dungeon_count(bundle) + greg_wildcard) >= world.options.rainbow_bridge_dungeons_required.value)) or
            (world.options.rainbow_bridge.value == 6 and (get_gs_count(bundle) >= world.options.rainbow_bridge_skull_tokens_required.value)) or
            (world.options.rainbow_bridge.value == 7 and has_item(Items.GREG_THE_GREEN_RUPEE, bundle)))

def get_gs_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    state = bundle[0]
    world = bundle[2]
    return state.count(Items.GOLD_SKULLTULA_TOKEN.value, world.player)


def can_trigger_lacs(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]

    greg_wildcard = 0
    if has_item(Items.GREG_THE_GREEN_RUPEE, bundle) and world.options.ganons_castle_boss_key_greg_wildcard.value:
        greg_wildcard = 1

    return ((world.options.ganons_castle_boss_key. value == 2 and has_item(Items.SHADOW_MEDALLION, bundle) and has_item(Items.SPIRIT_MEDALLION, bundle)) or
            (world.options.ganons_castle_boss_key. value == 3 and (stone_count(bundle) + greg_wildcard >= world.options.ganons_castle_boss_key_stones_required.value)) or
            (world.options.ganons_castle_boss_key. value == 4 and (medallion_count(bundle) + greg_wildcard >= world.options.ganons_castle_boss_key_medallions_required.value)) or
            (world.options.ganons_castle_boss_key. value == 5 and (stone_count(bundle) + medallion_count(bundle) + greg_wildcard >= world.options.ganons_castle_boss_key_dungeon_rewards_required.value)) or 
            (world.options.ganons_castle_boss_key. value == 6 and (dungeon_count(bundle) + greg_wildcard >= world.options.ganons_castle_boss_key_dungeons_required.value)) or
            (world.options.ganons_castle_boss_key. value == 7 and (get_gs_count(bundle) >= world.options.ganons_castle_boss_key_skull_tokens_required.value)))