from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState, ItemClassification as IC
from .Locations import SohLocation
from worlds.generic.Rules import set_rule
from .Enums import *
from .Items import SohItem
from .RegionAgeAccess import can_access_entrance_as_adult, can_access_entrance_as_child, can_access_region_as_adult, can_access_region_as_child
from .Options import * 

if TYPE_CHECKING:
    from . import SohWorld

import logging
logger = logging.getLogger("SOH_OOT.Logic")

def add_locations(parent_region: str, world: "SohWorld", locations = [[]]) -> None:
    for location in locations:
        locationName = location[0]
        locationRule = lambda state: True
        if(len(location) < 2):
            locationRule = location[1]
        if locationName in world.included_locations:
            locationAddress = world.included_locations.pop(location[0])
            world.get_region(parent_region).add_locations({locationName: locationAddress}, SohLocation)
            set_rule(world.get_location(locationName), locationRule)

def connect_regions(parent_region: str, world: "SohWorld", child_regions = [[]]) -> None:
    for region in child_regions:
        world.get_region(parent_region).connect(world.get_region(region[0]), rule=region[1])

def add_events(parent_region, world: "SohWorld", events = [[]]):
    for event in events:
        event_location = event[0]
        event_item = event[1]
        event_rule = event[2]
        new_event = SohLocation(world.player, event_location, None, parent_region)
        new_event.place_locked_item(SohItem(event_item, IC.progression, None, world.player))
        set_rule(new_event, event_rule)

def has_item(itemName: str, state: CollectionState, world: "SohWorld", count:int = 1, can_be_child: bool = True, can_be_adult: bool = True) -> bool:
    def has(itemName, count=1): 
        if itemName in state.prog_items[world.player]:
            result = state.has(itemName, world.player, count) #To shorten the many calls in this function
            if result:
                logger.debug(f"We HasItem({itemName})")
            return result
        return False
    def can_use_item(name, count=1):
        return can_use(name, state, world, can_be_child, can_be_adult)
    match itemName:
        case Items.FAIRY_OCARINA.value:
            return has(Items.FAIRY_OCARINA.value) or has(Items.OCARINA_OF_TIME.value) or has(Items.PROGRESSIVE_OCARINA.value, 1)
        case Items.OCARINA_OF_TIME.value:
            return has(Items.OCARINA_OF_TIME.value) or has(Items.PROGRESSIVE_OCARINA.value, 2)
        case Items.STICKS.value:
            return True #TODO account for starting sticks being disabled
        case Items.PROGRESSIVE_STICK_CAPACITY.value:
            return True
        case Items.NUTS.value: #TODO account for starting nuts being disabled
            return True
        case Items.PROGRESSIVE_BOMBCHU.value:
            return (bombchus_enabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value, Items.PROGRESSIVE_BOMBCHU.value], world.player)
        case Items.BOMBCHUS_5.value:
            return (bombchus_enabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value, Items.PROGRESSIVE_BOMBCHU.value], world.player)
        case Items.BOMBCHUS_10.value:
            return (bombchus_enabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value, Items.PROGRESSIVE_BOMBCHU.value], world.player)
        case Items.BOMBCHUS_20.value:
            return (bombchus_enabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value, Items.PROGRESSIVE_BOMBCHU.value], world.player)
        case Items.SCARECROW.value:
            return scarecrows_song(state, world) and can_use_item(Items.HOOKSHOT.value)
        case Items.DISTANT_SCARECROW.value:
            return scarecrows_song(state, world) and can_use_item(Items.LONGSHOT.value)
        case Items.DEKU_SHIELD.value:
            return has(Events.CAN_BUY_DEKU_SHIELD)
        case Items.PROGRESSIVE_GORON_SWORD.value:
            return has(Items.GIANTS_KNIFE.value) or has(Items.BIGGORONS_SWORD.value) or has(Items.PROGRESSIVE_GORON_SWORD.value)
        case Items.GORONS_BRACELET.value:
            return has(Items.GORONS_BRACELET.value) or has(Items.STRENGTH_UPGRADE.value)
        case Items.SILVER_GAUNTLETS.value:
            return has(Items.SILVER_GAUNTLETS.value) or has(Items.STRENGTH_UPGRADE.value, 2)
        case Items.GOLDEN_GAUNTLETS.value: 
            return has(Items.GOLDEN_GAUNTLETS.value) or has(Items.STRENGTH_UPGRADE.value, 3)
        case Items.MAGIC_SINGLE.value:
            return has(Items.MAGIC_SINGLE.value) or has(Items.PROGRESSIVE_MAGIC_METER.value)
        case Items.MAGIC_DOUBLE:
            return has(Items.MAGIC_DOUBLE.value) or has(Items.PROGRESSIVE_MAGIC_METER.value, 2)
        case Items.CHILD_WALLET.value:
            return True #TODO add child wallet options
        case Items.ADULT_WALLET.value:
            return has(Items.ADULT_WALLET.value) or has(Items.PROGRESSIVE_WALLET.value)
        case Items.GIANT_WALLET.value: 
            return has(Items.GIANT_WALLET.value) or has(Items.PROGRESSIVE_WALLET.value, 2)
        case Items.TYCOON_WALLET.value:
            return has(Items.TYCOON_WALLET.value) or has(Items.PROGRESSIVE_WALLET.value, 3)
        case Items.BRONZE_SCALE.value:
            return True #TODO add bronze scale options
        case Items.SILVER_SCALE.value:
            return has(Items.SILVER_SCALE.value) or has(Items.PROGRESSIVE_SCALE.value)
        case Items.GOLDEN_SCALE.value:
            return has(Items.GOLDEN_SCALE.value) or has(Items.PROGRESSIVE_SCALE.value, 2)
        case Items.BOTTLE_WITH_BIG_POE.value:
            return has_bottle(state, world)
        case _:
            return has(itemName, count)
        
def can_use(name: Items, state: CollectionState, world: SohWorld, can_be_child: bool = True, can_be_adult: bool = True) -> bool:
    if not has_item(name, state, world):
        return False
    def has(name, count=1): 
        return has_item(name, state, world, count, can_be_child, can_be_adult)
    def can_use_item(name, count=1):
        return can_use(name, state, world, can_be_child, can_be_adult)
    match name:
        case Items.MAGIC_SINGLE.value:
            return has(Events.AMMO_CAN_DROP) or (has_bottle(state, world) and has(Events.CAN_BUY_GREEN_POTION))
        case Items.DINS_FIRE.value:
            return can_use_item(Items.MAGIC_SINGLE.value)
        case Items.NAYRUS_LOVE.value:
            return can_use_item(Items.MAGIC_SINGLE.value)
        case Items.FARORES_WIND.value:
            return can_use_item(Items.MAGIC_SINGLE.value)
        case Items.LENS_OF_TRUTH.value:
            return can_use_item(Items.MAGIC_SINGLE.value)
        case Items.FIRE_ARROW.value:
            return can_use_item(Items.MAGIC_SINGLE.value) and can_use_item(Items.FAIRY_BOW.value)
        case Items.ICE_ARROW.value:
            return can_use_item(Items.MAGIC_SINGLE.value) and can_use_item(Items.FAIRY_BOW.value)
        case Items.LIGHT_ARROW.value:
            return can_use_item(Items.MAGIC_SINGLE.value) and can_use_item(Items.FAIRY_BOW.value)
        case Items.FAIRY_BOW.value:
            return can_be_adult and (has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_ARROWS))
        case Items.MEGATON_HAMMER.value:
            return can_be_adult
        case Items.IRON_BOOTS.value:
            return can_be_adult
        case Items.HOVER_BOOTS.value:
            return can_be_adult
        case Items.HOOKSHOT.value:
            return can_be_adult
        case Items.LONGSHOT.value:
            return can_be_adult
        case Items.SCARECROW.value:
            return can_be_adult
        case Items.DISTANT_SCARECROW.value:
            return can_be_adult
        case Items.GORON_TUNIC.value:
            return can_be_adult
        case Items.ZORA_TUNIC.value:
            return can_be_adult
        case Items.MIRROR_SHIELD.value:
            return can_be_adult
        case Items.MASTER_SWORD.value:
            return can_be_adult
        case Items.BIGGORONS_SWORD.value:
            return can_be_adult
        case Items.SILVER_GAUNTLETS.value:
            return can_be_adult
        case Items.GOLDEN_GAUNTLETS.value:
            return can_be_adult
        case Items.POCKET_EGG.value:
            return can_be_adult
        case Items.COJIRO.value:
            return can_be_adult
        case Items.ODD_MUSHROOM.value:
            return can_be_adult
        case Items.ODD_POTION.value:
            return can_be_adult
        case Items.POACHERS_SAW.value:
            return can_be_adult
        case Items.BROKEN_GORONS_SWORD.value:
            return can_be_adult
        case Items.PRESCRIPTION.value:
            return can_be_adult
        case Items.EYEBALL_FROG.value:
            return can_be_adult
        case Items.WORLDS_FINEST_EYEDROPS.value:
            return can_be_adult
        case Items.CLAIM_CHECK.value:
            return can_be_adult
        case Items.FAIRY_SLINGSHOT.value:
            return can_be_child and (has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_SEEDS))
        case Items.BOOMERANG.value:
            return can_be_child
        case Items.KOKIRI_SWORD.value:
            return can_be_child
        case Items.NUTS.value:
            return (has(Events.NUT_POT) or has(Events.NUT_CRATE) or has(Events.DEKU_BABA_NUTS)) and has(Events.AMMO_CAN_DROP)
        case Items.STICKS.value:
            return can_be_child and (has(Events.STICK_POT) or has(Events.DEKU_BABA_STICKS))
        case Items.DEKU_SHIELD.value:
            return can_be_child
        case Items.PROGRESSIVE_BOMB_BAG.value:
            return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_BOMBS)
        case Items.BOMB_BAG.value:
            return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_BOMBS)
        case Items.PROGRESSIVE_BOMBCHU.value:
            return bombchu_refill(state, world) and bombchus_enabled(state, world)
        case Items.BOMBCHUS_5.value:
            return bombchu_refill(state, world) and bombchus_enabled(state, world)
        case Items.BOMBCHUS_10.value:
            return bombchu_refill(state, world) and bombchus_enabled(state, world)
        case Items.BOMBCHUS_20.value:
            return bombchu_refill(state, world) and bombchus_enabled(state, world)
        case Items.WEIRD_EGG.value:
            return can_be_child
        case Items.BOTTLE_WITH_RUTOS_LETTER.value:
            return can_be_child
        case Items.MAGIC_BEAN.value:
            return can_be_child
        case Items.ZELDAS_LULLABY.value:
            return can_play_song(state, world, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value)
        case Items.EPONAS_SONG.value:
            return can_play_song(state, world, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value)
        case Items.PRELUDE_OF_LIGHT.value:
            return can_play_song(state, world, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value)
        case Items.SARIAS_SONG.value:
            return can_play_song(state, world, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.SUNS_SONG.value:
            return can_play_song(state, world, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.SONG_OF_TIME.value:
            return can_play_song(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.BOLERO_OF_FIRE.value:
            return can_play_song(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.REQUIEM_OF_SPIRIT.value:
            return can_play_song(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.SONG_OF_STORMS.value:
            return can_play_song(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CUP_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.MINUET_OF_FOREST.value:
            return can_play_song(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value)
        case Items.SERENADE_OF_WATER.value:
            return can_play_song(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.FISHING_POLE.value:
            return has(Items.CHILD_WALLET) # as long as you have enough rubies
        case _:
            return False

def scarecrows_song(state: CollectionState, world: SohWorld) -> bool:
    #TODO handle scarecrow song option in place of the False
    return (False and has_item(Items.FAIRY_OCARINA.value, state, world) and OcarinaButtons(state, world) > 2) or \
        (has_item(Events.CHILD_SCARECROW, state, world) and has_item(Events.ADULT_SCARECROW, state, world))

def has_bottle(state: CollectionState, world: SohWorld) -> bool: # soup
    return bottle_count(state, world) >= 1

def bottle_count(state: CollectionState, world: SohWorld) -> int:
    count = 0
    for name in [Items.EMPTY_BOTTLE.value, Items.BOTTLE_WITH_BLUE_POTION.value, Items.BOTTLE_WITH_BUGS.value, Items.BOTTLE_WITH_FAIRY.value, Items.BOTTLE_WITH_FISH.value, \
                  Items.BOTTLE_WITH_GREEN_POTION.value, Items.BOTTLE_WITH_GREEN_POTION.value, Items.BOTTLE_WITH_BLUE_FIRE.value, Items.BOTTLE_WITH_MILK.value, Items.BOTTLE_WITH_RED_POTION.value]:
        count += state.count(name, world.player)
    if state.has(Events.DELIVER_LETTER, world.player):
        count += state.count(Items.BOTTLE_WITH_RUTOS_LETTER.value, world.player)
    if state.has(Events.CAN_EMPTY_BIG_POES, world.player):
        count += state.count(Items.BOTTLE_WITH_BIG_POE.value, world.player)
    return count

def bombchu_refill(state: CollectionState, world: SohWorld) -> bool:
    return state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player) or False #TODO put enable bombchu drops option here

def bombchus_enabled(state: CollectionState, world: SohWorld) -> bool:
    if False: #TODO bombchu bag enabled
        return HasItem(state, world, Items.BOMBCHU_BAG.value)
    return has_item(Items.BOMB_BAG, state, world)

def can_play_song(state: CollectionState, world: SohWorld, *buttons: str) -> bool:
    if not has_item(Items.FAIRY_OCARINA, state, world):
        return False
    for button in buttons:
        if button in state.prog_items.values(): #if this is false, then button shuffle is disabled
            if not state.has(button, world.player):
                return False
        else: #button shuffle disabled
            return True
    return True

def ocarina_buttons(state: CollectionState, world: SohWorld) -> int:
    return state.count_from_list([Items.OCARINA_ABUTTON.value, Items.OCARINA_CDOWN_BUTTON.value, Items.OCARINA_CLEFT_BUTTON.value, \
                                  Items.OCARINA_CUP_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value], world.player)

def has_explosives(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link has access to explosives (bombs or bombchus)."""
    return can_use(Items.PROGRESSIVE_BOMB_BAG, state, world) or can_use(Items.PROGRESSIVE_BOMBCHU, state, world)

def blast_or_smash(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can blast or smash obstacles."""
    return has_explosives(state, world) or can_use(Items.MEGATON_HAMMER, state, world)

def blue_fire(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link has access to blue fire."""
    return can_use(Items.BOTTLE_WITH_BLUE_FIRE, state, world)  # or blue fire arrows

def can_use_sword(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can use any sword."""
    return (can_use(Items.KOKIRI_SWORD, state, world) or
            can_use(Items.MASTER_SWORD, state, world) or
            can_use(Items.BIGGORONS_SWORD, state, world))

def has_projectile(state: CollectionState, world: SohWorld, age: str = "either") -> bool:
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

def can_use_projectile(state: CollectionState, world: SohWorld, age: str = "either") -> bool:
    return (has_explosives(state, world) or can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or
            can_use(Items.BOOMERANG, state, world) or can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
            can_use(Items.PROGRESSIVE_BOW, state, world))

def can_break_mud_walls(state: CollectionState, world: SohWorld) -> bool:
    return blast_or_smash(state, world) or (can_do_trick("Blue Fire Mud Walls", state, world) and blue_fire(state, world))

def can_get_deku_baba_sticks(state: CollectionState, world: SohWorld) -> bool:
    return can_use(Items.DEKU_STICK_1, state, world) or can_use(Items.BOOMERANG, state, world)

def can_get_deku_baba_nuts(state: CollectionState, world: SohWorld) -> bool:
    return can_use_sword(state, world) or can_use(Items.BOOMERANG, state, world)

def is_adult(state: CollectionState, world: SohWorld) -> bool:
    # For now, return True as a placeholder since age logic is complex and context-dependent
    # The real age checking should be done through the CanUse function's can_be_adult parameter
    # TODO: Implement proper age checking based on world settings and progression
    return True

def is_child(state: CollectionState, world: "SohWorld") -> bool:
    # For now, return True as a placeholder since age logic is complex and context-dependent
    # The real age checking should be done through the CanUse function's can_be_adult parameter
    # TODO: Implement proper age checking based on world settings and progression
    return True

def can_damage(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can deal damage to enemies."""
    return (can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or 
            can_jump_slash(state, world) or 
            has_explosives(state, world) or 
            can_use(Items.DINS_FIRE, state, world) or
            can_use(Items.PROGRESSIVE_BOW, state, world))


def can_attack(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can attack enemies (damage or stun)."""
    return (can_damage(state, world) or 
            can_use(Items.BOOMERANG, state, world) or
            can_use(Items.PROGRESSIVE_HOOKSHOT, state, world))

def can_standing_shield(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can use a shield for standing blocks."""
    return (can_use(Items.MIRROR_SHIELD, state, world) or # Only adult can use mirror shield
            (is_adult(state, world) and can_use(Items.HYLIAN_SHIELD, state, world)) or
            can_use(Items.DEKU_SHIELD, state, world)) # Only child can use deku shield

def can_shield(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can use a shield for blocking or stunning."""
    return (can_use(Items.MIRROR_SHIELD, state, world) or
            can_use(Items.HYLIAN_SHIELD, state, world) or
            can_use(Items.DEKU_SHIELD, state, world))

def take_damage(state: CollectionState, world: SohWorld) -> bool:
    # return CanUse(RG_BOTTLE_WITH_FAIRY) || EffectiveHealth() != 1 || CanUse(RG_NAYRUS_LOVE);
    return (can_use(Items.BOTTLE_WITH_FAIRY, state, world) or can_use(Items.NAYRUS_LOVE, state, world)
            or True)  #TODO: Implement "|| EffectiveHealth()"

def can_do_trick(trick: str, state: CollectionState, world: SohWorld) -> bool:
    # TODO: Implement specific trick logic based on world settings
    # For now, return False for safety (no tricks assumed)
    return False


def can_break_pots(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can break pots for items."""
    return (can_jump_slash(state, world) or 
           can_use(Items.BOOMERANG, state, world) or
           has_explosives(state, world) or
           can_use(Items.PROGRESSIVE_HOOKSHOT, state, world))


def can_break_crates(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can break crates."""
    return (can_jump_slash(state, world) or 
           has_explosives(state, world))


def can_hit_eye_targets(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can hit eye switches/targets."""
    return (can_use(Items.PROGRESSIVE_BOW, state, world) or 
           can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or
           can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
           can_use(Items.BOOMERANG, state, world))


def can_stun_deku(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can stun Deku Scrubs."""
    return can_attack(state, world) or can_use(Items.DEKU_NUT_BAG, state, world) or can_shield(state, world) # Is this right for nuts?


def can_reflect_nuts(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can reflect Deku Nuts back at enemies."""
    return can_stun_deku(state, world)

def has_fire_source_with_torch(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link has a fire source that can be used with a torch."""
    return has_fire_source(state, world) or can_use(Items.STICKS, state, world)

def has_fire_source(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link has any fire source."""
    return (can_use(Items.DINS_FIRE, state, world) or 
           can_use(Items.FIRE_ARROW, state, world))


def can_jump_slash(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can perform a jump slash with any sword."""
    return (can_jump_slash_except_hammer(state, world) or can_use(Items.MEGATON_HAMMER, state, world))  # Hammer can substitute for sword in some cases

def can_jump_slash_except_hammer(state: CollectionState, world: SohWorld):
    return can_use(Items.KOKIRI_SWORD, state, world) or can_use(Items.MASTER_SWORD, state, world) or can_use(Items.BIGGORONS_SWORD, state, world)


def can_hit_switch(state: CollectionState, world: SohWorld, distance: CombatRanges = CombatRanges.CLOSE,
                   in_water: bool = False) -> bool:
    if distance <= CombatRanges.SHORT_JUMPSLASH and (can_use(Items.KOKIRI_SWORD, state, world) or can_use(Items.MEGATON_HAMMER, state, world)):
        return True
    if distance <= CombatRanges.MASTER_SWORD_JUMPSLASH and can_use(Items.MASTER_SWORD, state, world):
        return True
    if distance <= CombatRanges.LONG_JUMPSLASH and (can_use(Items.BIGGORONS_SWORD, state, world) or can_use(Items.STICKS, state, world)):
        return True
    if distance <= CombatRanges.BOMB_THROW and not in_water and can_use(Items.BOMB_BAG, state, world):
        return True
    if distance <= CombatRanges.HOOKSHOT and (can_use(Items.HOOKSHOT, state, world) or can_use(Items.BOMBCHUS_5, state, world)):
        return True
    if distance <= CombatRanges.LONGSHOT and can_use(Items.LONGSHOT, state, world):
        return True
    if distance <= CombatRanges.FAR and (can_use(Items.FAIRY_SLINGSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world)):
        return True
    return False

def can_kill_enemy(state: CollectionState, world: SohWorld, enemy: Enemies, combat_range: CombatRanges = CombatRanges.CLOSE,
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
    def can_hit_at_range(range_type: CombatRanges) -> bool:
        if range_type == CombatRanges.CLOSE and can_use(Items.MEGATON_HAMMER, state, world):
            return True
        if range_type <= CombatRanges.SHORT_JUMPSLASH and can_use(Items.KOKIRI_SWORD, state, world):
            return True
        if range_type <= CombatRanges.MASTER_SWORD_JUMPSLASH and can_use(Items.MASTER_SWORD, state, world):
            return True
        if range_type <= CombatRanges.LONG_JUMPSLASH and (can_use(Items.BIGGORONS_SWORD, state, world) or can_use(Items.STICKS, state, world)):
            return True
        if range_type <= CombatRanges.BOMB_THROW and (not in_water and can_use(Items.BOMB_BAG, state, world)):
            return True
        if range_type <= CombatRanges.HOOKSHOT and (can_use(Items.HOOKSHOT, state, world) or (wall_or_floor and can_use(Items.BOMBCHUS_5, state, world))):
            return True
        if range_type <= CombatRanges.LONGSHOT and can_use(Items.LONGSHOT, state, world):
            return True
        if range_type <= CombatRanges.FAR and (can_use(Items.FAIRY_SLINGSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world)):
            return True
        return False

    # Enemy-specific logic based on C++ implementation

    if enemy in [Enemies.GERUDO_GUARD, Enemies.BREAK_ROOM_GUARD]:
        return False

    if enemy == Enemies.GOLD_SKULLTULA:
        return can_hit_at_range(combat_range) or (combat_range <= CombatRanges.LONGSHOT and (wall_or_floor and can_use(Items.BOMBCHUS_5, state, world))) or \
            (combat_range <= CombatRanges.BOOMERANG and can_use(Items.DINS_FIRE, state, world))

    if enemy == Enemies.BIG_SKULLTULA:
        return can_hit_at_range(combat_range) or (combat_range <= CombatRanges.BOOMERANG and can_use(Items.DINS_FIRE, state, world))

    if enemy in [Enemies.GOHMA_LARVA, Enemies.MAD_SCRUB, Enemies.DEKU_BABA]:
        return can_attack(state, world)
    
    if enemy == Enemies.DODONGO:
        return can_use_sword(state, world) or can_use(Items.MEGATON_HAMMER, state, world) or (quantity <= 5 and can_use(Items.STICKS, state, world)) or \
                has_explosives(state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world)

    if enemy == Enemies.LIZALFOS:
        return (can_jump_slash(state, world) or can_use(Items.PROGRESSIVE_BOW, state, world) or has_explosives(state, world)) \
            or can_use(Items.FAIRY_SLINGSHOT, state, world)

    if enemy in [Enemies.KEESE, Enemies.FIRE_KEESE]:
        return can_hit_at_range(combat_range) or (combat_range == CombatRanges.CLOSE and can_use(Items.KOKIRI_SWORD, state, world)) \
            or (combat_range <= CombatRanges.BOOMERANG and can_use(Items.BOOMERANG, state, world))

    if enemy in Enemies.BLUE_BUBBLE:
        return blast_or_smash(state, world) or can_use(Items.PROGRESSIVE_BOW, state, world) or \
            ((can_jump_slash_except_hammer(state, world) or can_use(Items.PROGRESSIVE_SLINGSHOT, state, world)) and \
             (can_use(Items.NUTS, state, world) or hookshot_or_boomerang(state, world) or can_standing_shield(state, world)))

    if enemy == Enemies.DEAD_HAND:
        return can_use_sword(state, world) or (can_use(Items.STICKS, state, world) and False) # replace False with ctx->GetTrickOption(RT_BOTW_CHILD_DEADHAND));

    if enemy == Enemies.WITHERED_DEKU_BABA:
        return can_attack(state, world) or can_use(Items.BOOMERANG, state, world)

    if enemy in [Enemies.LIKE_LIKE, Enemies.FLOORMASTER]:
        return can_use_sword(state, world) or (can_use(Items.STICKS, state, world) and False) #TODO replace False with dead hand child option

    if enemy == Enemies.STALFOS:
        return can_hit_at_range(combat_range) or (combat_range == CombatRanges.CLOSE and can_use(Items.KOKIRI_SWORD, state, world))

    if enemy == Enemies.IRON_KNUCKLE:
        return (can_use_sword(state, world) or
                can_use(Items.MEGATON_HAMMER, state, world) or
                has_explosives(state, world))

    if enemy == Enemies.FLARE_DANCER:
        return can_use(Items.MEGATON_HAMMER, state, world) or \
               can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or \
               (has_explosives(state, world) and (can_jump_slash_except_hammer(state, world) or can_use(Items.PROGRESSIVE_BOW, state, world) or \
                    can_use(Items.PROGRESSIVE_SLINGSHOT, state, world) or can_use(Items.BOOMERANG, state, world)))

    if enemy in [Enemies.WOLFOS, Enemies.WHITE_WOLFOS, Enemies.WALLMASTER]:
        return can_jump_slash(state, world) or can_use(Items.FAIRY_BOW, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world) or \
                   can_use(Items.BOMBCHUS_5, state, world) or can_use(Items.DINS_FIRE, state, world) or \
                   (can_use(Items.BOMB_BAG, state, world) and (can_use(Items.NUTS, state, world) or can_use(Items.HOOKSHOT, state, world) or can_use(Items.BOOMERANG, state, world)))

    if enemy == Enemies.GERUDO_WARRIOR:
        return can_jump_slash(state, world) or can_use(Items.FAIRY_BOW, state, world) or \
                    (False and #TODO replace False with Gerudo warrior with hard weapon trick option
                    (can_use(Items.FAIRY_SLINGSHOT, state, world) or can_use(Items.BOMBCHUS_5, state, world)))

    if enemy in [Enemies.GIBDO, Enemies.REDEAD]:
        return can_jump_slash(state, world) or \
               can_use(Items.DINS_FIRE, state, world)

    if enemy == Enemies.MEG:
        return can_use(Items.FAIRY_BOW, state, world) or can_use(Items.HOOKSHOT, state, world) or has_explosives(state, world)
    
    if enemy == Enemies.ARMOS:
        return blast_or_smash(state, world) or can_use(Items.MASTER_SWORD, state, world) or can_use(Items.BIGGORONS_SWORD, state, world) or can_use(Items.STICKS, state, world) or \
                   can_use(Items.FAIRY_BOW, state, world) or \
                   ((can_use(Items.NUTS, state, world) or can_use(Items.HOOKSHOT, state, world) or can_use(Items.BOOMERANG, state, world)) and
                    (can_use(Items.KOKIRI_SWORD, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world)))

    if enemy == Enemies.GREEN_BUBBLE:
        return can_jump_slash(state, world) or can_use(Items.FAIRY_BOW, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world) or has_explosives(state, world)

    if enemy == Enemies.DINOLFOS:
        return can_jump_slash(state, world) or can_use(Items.FAIRY_BOW, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world) or \
                   (not timer and can_use(Items.BOMBCHUS_5, state, world))
    
    if enemy == Enemies.TORCH_SLUG:
        return can_jump_slash(state, world) or has_explosives(state, world) or can_use(Items.FAIRY_BOW, state, world)
    
    if enemy == Enemies.FREEZARD:
        return can_use(Items.MASTER_SWORD, state, world) or can_use(Items.BIGGORONS_SWORD, state, world) or can_use(Items.MEGATON_HAMMER, state, world) or \
                   can_use(Items.STICKS, state, world) or has_explosives(state, world) or can_use(Items.HOOKSHOT, state, world) or can_use(Items.DINS_FIRE, state, world) or \
                   can_use(Items.FIRE_ARROW, state, world)

    if enemy == Enemies.SHELL_BLADE:
        return can_jump_slash(state, world) or has_explosives(state, world) or can_use(Items.HOOKSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world) or can_use(Items.DINS_FIRE, state, world)

    if enemy == Enemies.SPIKE:
        return can_use(Items.MASTER_SWORD, state, world) or can_use(Items.BIGGORONS_SWORD, state, world) or can_use(Items.MEGATON_HAMMER, state, world) or \
                can_use(Items.STICKS, state, world) or has_explosives(state, world) or can_use(Items.HOOKSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world) or \
                can_use(Items.DINS_FIRE, state, world)

    if enemy == Enemies.STINGER:
        return can_hit_at_range(combat_range) or (combat_range == CombatRanges.CLOSE and can_use(Items.KOKIRI_SWORD, state, world))

    if enemy == Enemies.BIG_OCTO:
        # If chasing octo is annoying but with rolls you can catch him, and you need rang to get into this room
        # without shenanigans anyway. Bunny makes it free
        return can_use(Items.KOKIRI_SWORD, state, world) or can_use(Items.STICKS, state, world) or can_use(Items.MASTER_SWORD, state, world)
    if enemy == Enemies.GOHMA:
        return has_boss_soul(Items.GOHMAS_SOUL, state, world) and can_jump_slash(state, world) and \
               (can_use(Items.NUTS, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world) or hookshot_or_boomerang(state, world))
    if enemy == Enemies.KING_DODONGO:
        return has_boss_soul(Items.KING_DODONGOS_SOUL, state, world) and can_jump_slash(state, world) and \
               (can_use(Items.BOMB_BAG, state, world) or has_item(Items.GORONS_BRACELET, state, world) or \
               (False and can_access_region_as_adult(state, world, Regions.DODONGOS_CAVERN_BOSS_ROOM) and can_use(Items.BOMBCHUS_5, state, world))) #TODO replace False with ctx->get_trick_option(RT_DC_DODONGO_CHU)
    if enemy == Enemies.BARINADE:
        return has_boss_soul(Items.BARINADES_SOUL, state, world) and can_use(Items.BOOMERANG, state, world) and can_jump_slash_except_hammer(state, world)
    if enemy == Enemies.PHANTOM_GANON:
        return has_boss_soul(Items.PHANTOM_GANONS_SOUL, state, world) and can_use_sword(state, world) and \
               (can_use(Items.HOOKSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world))
    if enemy == Enemies.VOLVAGIA:
        return has_boss_soul(Items.VOLVAGIAS_SOUL, state, world) and can_use(Items.MEGATON_HAMMER, state, world)
    if enemy == Enemies.MORPHA:
        return has_boss_soul(Items.MORPHAS_SOUL, state, world) and \
               (can_use(Items.HOOKSHOT, state, world) or \
                (False and has_item("Bronze Scale", state, world))) and \
               (can_use_sword(state, world) or can_use(Items.MEGATON_HAMMER, state, world)) #TODO replace False with ctx->get_trick_option(RT_WATER_MORPHA_WITHOUT_HOOKSHOT)
    if enemy == Enemies.BONGO_BONGO:
        return has_boss_soul(Items.BONGO_BONGOS_SOUL, state, world) and \
               (can_use(Items.LENS_OF_TRUTH, state, world) or False) and can_use_sword(state, world) and \
               (can_use(Items.HOOKSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world) or \
                False) #TODO replace the Falses with ctx->get_trick_option(RT_LENS_BONGO) and ctx->get_trick_option(RT_SHADOW_BONGO)
    if enemy == Enemies.TWINROVA:
        return has_boss_soul(Items.TWINROVAS_SOUL, state, world) and can_use(Items.MIRROR_SHIELD, state, world) and \
               (can_use_sword(state, world) or can_use(Items.MEGATON_HAMMER, state, world))
    if enemy == Enemies.GANONDORF:
        # RANDOTODO: Trick to use hammer (no jumpslash) or stick (only jumpslash) instead of a sword to reflect the
        # energy ball and either of them regardless of jumpslashing to damage and kill ganondorf

        # Bottle is not taken into account since a sword, hammer or stick are required
        # for killing ganondorf and all of those can reflect the energy ball
        # This will not be the case once ammo logic in taken into account as
        # sticks are limited and using a bottle might become a requirement in that case
        return has_boss_soul(Items.GANONS_SOUL, state, world) and can_use(Items.LIGHT_ARROW, state, world) and can_use_sword(state, world)
    if enemy == Enemies.GANON:
        return has_boss_soul(Items.GANONS_SOUL, state, world) and can_use(Items.MASTER_SWORD, state, world)
    if enemy == Enemies.DARK_LINK:
        # RANDOTODO Dark link is buggy right now, retest when he is not
        return can_jump_slash(state, world) or can_use(Items.FAIRY_BOW, state, world)
    if enemy == Enemies.ANUBIS:
        # there's a restoration that allows beating them with mirror shield + some way to trigger their attack
        return has_fire_source(state, world)
    if enemy == Enemies.BEAMOS:
        return has_explosives(state, world)
    if enemy == Enemies.PURPLE_LEEVER:
        # dies on it's own, so this is the conditions to spawn it (killing 10 normal leevers)
        # Sticks and Ice arrows work but will need ammo capacity logic
        # other methods can damage them but not kill them, and they run when hit, making them impractical
        return can_use(Items.MASTER_SWORD, state, world) or can_use(Items.BIGGORONS_SWORD, state, world)
    if enemy == Enemies.TENTACLE:
        return can_use(Items.BOOMERANG, state, world)
    if enemy == Enemies.BARI:
        return hookshot_or_boomerang(state, world) or can_use(Items.FAIRY_BOW, state, world) or has_explosives(state, world) or can_use(Items.MEGATON_HAMMER, state, world) or \
               can_use(Items.STICKS, state, world) or can_use(Items.DINS_FIRE, state, world) or (take_damage(state, world) and can_use_sword(state, world))
    if enemy == Enemies.SHABOM:
        # RANDOTODO when you add better damage logic, you can kill this by taking hits
        return can_use(Items.BOOMERANG, state, world) or can_use(Items.NUTS, state, world) or can_jump_slash(state, world) or can_use(Items.DINS_FIRE, state, world) or \
               can_use(Items.ICE_ARROW, state, world)
    if enemy == Enemies.OCTOROK:
        return can_reflect_nuts(state, world) or hookshot_or_boomerang(state, world) or can_use(Items.FAIRY_BOW, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world) or \
               can_use(Items.BOMB_BAG, state, world) or (wall_or_floor and can_use(Items.BOMBCHUS_5, state, world))

    return False

def has_boss_soul(soul: Items, state: CollectionState, world: SohWorld):
    soulsanity = world.options.shuffle_boss_souls.value
    if soulsanity == ShuffleBossSouls.option_off:
        return True
    if soul == Items.GANONS_SOUL:
        return True if soulsanity == ShuffleBossSouls.option_on else state.has(Items.GANONS_SOUL, world.player)
    return state.has(soul, world.player)

def can_pass_enemy(state: CollectionState, world: SohWorld, enemy: Enemies) -> bool:
    """Check if Link can pass by an enemy (usually by killing or stunning it)."""
    return can_kill_enemy(state, world, enemy) # I think that we can be more permissive here, but for now this is fine


def can_cut_shrubs(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link can cut shrubs (grass, bushes)."""
    return (can_use_sword(state, world) or
            can_use(Items.BOOMERANG, state, world) or 
            has_explosives(state, world) or
            can_use(Items.GORONS_BRACELET, state, world) or
            can_use(Items.MEGATON_HAMMER, state, world))


def hookshot_or_boomerang(state: CollectionState, world: SohWorld) -> bool:
    """Check if Link has hookshot or boomerang."""
    return (can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) or
            can_use(Items.BOOMERANG, state, world))
