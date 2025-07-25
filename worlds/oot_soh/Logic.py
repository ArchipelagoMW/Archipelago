from typing import List
from BaseClasses import CollectionState, Region, Entrance
from .Enums import *
from .Regions import can_access_entrance_as_adult, can_access_entrance_as_child, can_access_region_as_adult, can_access_region_as_child
from worlds.oot_soh import SohWorld
#Contains a set of helpers for access rules

#TODO Some of this uses Item names that will likely move to the Events enum
def HasItem(state: CollectionState, world: SohWorld, itemName: str, count:int = 1, can_be_child: bool = True, can_be_adult: bool = True) -> bool:
    def has(name, count=1): 
        if name in state.prog_items:
            return state.has(name, world.player, count) #To shorten the many calls in this function
        return False
    def can_use(name, count=1):
        return CanUse(state, world, name, can_be_child, can_be_adult)
    match itemName:
        case Items.FAIRY_OCARINA:
            return has(Items.FAIRY_OCARINA) or has(Items.OCARINA_OF_TIME) or has(Items.PROGRESSIVE_OCARINA, 1)
        case Items.OCARINA_OF_TIME:
            return has(Items.OCARINA_OF_TIME) or has(Items.PROGRESSIVE_OCARINA, 2)
        case Items.STICKS:
            return True #TODO account for starting sticks being disabled
        case Items.PROGRESSIVE_STICK_CAPACITY:
            return True
        case Items.NUTS: #TODO account for starting nuts being disabled
            return True
        case Items.PROGRESSIVE_BOMBCHU:
            return (BombchusEnabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20, Items.PROGRESSIVE_BOMBCHU], world.player)
        #Ship def:
        #return (BombchusEnabled() && (GetInLogic(LOGIC_BUY_BOMBCHUS) || CouldPlayBowling || CarpetMerchant)) ||
        #           CheckInventory(ITEM_BOMBCHU, true);
        case Items.BOMBCHUS_5:
            return (BombchusEnabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20, Items.PROGRESSIVE_BOMBCHU], world.player)
        case Items.BOMBCHUS_10:
            return (BombchusEnabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20, Items.PROGRESSIVE_BOMBCHU], world.player)
        case Items.BOMBCHUS_20:
            return (BombchusEnabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20, Items.PROGRESSIVE_BOMBCHU], world.player)
        case Items.SCARECROW:
            return ScarecrowsSong(state, world) and can_use(Items.HOOKSHOT)
        case Items.DISTANT_SCARECROW:
            return ScarecrowsSong(state, world) and can_use(Items.LONGSHOT)
        case Items.DEKU_SHIELD:
            return has(Events.CAN_BUY_DEKU_SHIELD)
        case Items.PROGRESSIVE_GORON_SWORD:
            return has(Items.GIANTS_KNIFE) or has(Items.BIGGORONS_SWORD) or has(Items.PROGRESSIVE_GORON_SWORD)
        case Items.GORONS_BRACELET:
            return has(Items.GORONS_BRACELET) or has(Items.STRENGTH_UPGRADE)
        case Items.SILVER_GAUNTLETS:
            return has(Items.SILVER_GAUNTLETS) or has(Items.STRENGTH_UPGRADE, 2)
        case Items.GOLDEN_GAUNTLETS: 
            return has(Items.GOLDEN_GAUNTLETS) or has(Items.STRENGTH_UPGRADE, 3)
        case Items.MAGIC_SINGLE:
            return has(Items.MAGIC_SINGLE) or has(Items.PROGRESSIVE_MAGIC_METER)
        case Items.MAGIC_DOUBLE:
            return has(Items.MAGIC_DOUBLE) or has(Items.PROGRESSIVE_MAGIC_METER, 2)
        case Items.CHILD_WALLET:
            return True #TODO add child wallet options
        case Items.ADULT_WALLET:
            return has(Items.ADULT_WALLET) or has(Items.PROGRESSIVE_WALLET)
        case Items.GIANT_WALLET: 
            return has(Items.GIANT_WALLET) or has(Items.PROGRESSIVE_WALLET, 2)
        case Items.TYCOON_WALLET:
            return has(Items.TYCOON_WALLET) or has(Items.PROGRESSIVE_WALLET, 3)
        case Items.BRONZE_SCALE:
            return True #TODO add bronze scale options
        case Items.SILVER_SCALE:
            return has(Items.SILVER_SCALE) or has(Items.PROGRESSIVE_SCALE)
        case Items.GOLDEN_SCALE:
            return has(Items.GOLDEN_SCALE) or has(Items.PROGRESSIVE_SCALE, 2)
        case Items.BOTTLE_WITH_BIG_POE:
            return HasBottle(state, world)
        case _:
            return has(itemName, count)
        
def CanUse(state: CollectionState, world: SohWorld, name: str, can_be_child: bool = True, can_be_adult: bool = True) -> bool:
    if not HasItem(state, world, name):
        return False
    def has(name, count=1): 
        return HasItem(state, world, name, count, can_be_child, can_be_adult)
    def can_use(name, count=1):
        return CanUse(state, world, name, can_be_child, can_be_adult)
    magic = lambda: can_use(Items.MAGIC_SINGLE)
    match name:
        case Items.MAGIC_SINGLE:
            return has(Events.AMMO_CAN_DROP) or (HasBottle(state, world) and has(Events.CAN_BUY_GREEN_POTION))
        case Items.DINS_FIRE:
            return can_use(Items.MAGIC_SINGLE)
        case Items.NAYRUS_LOVE:
            return can_use(Items.MAGIC_SINGLE)
        case Items.FARORES_WIND:
            return can_use(Items.MAGIC_SINGLE)
        case Items.LENS_OF_TRUTH:
            return can_use(Items.MAGIC_SINGLE)
        case Items.FIRE_ARROW:
            return can_use(Items.MAGIC_SINGLE) and can_use(Items.FAIRY_BOW)
        case Items.ICE_ARROW:
            return can_use(Items.MAGIC_SINGLE) and can_use(Items.FAIRY_BOW)
        case Items.LIGHT_ARROW:
            return can_use(Items.MAGIC_SINGLE) and can_use(Items.FAIRY_BOW)
        case Items.FAIRY_BOW:
            return can_be_adult and (Events.AMMO_CAN_DROP or has(Events.CAN_BUY_ARROWS))
        case Items.MEGATON_HAMMER:
            return can_be_adult
        case Items.IRON_BOOTS:
            return can_be_adult
        case Items.HOVER_BOOTS:
            return can_be_adult
        case Items.HOOKSHOT:
            return can_be_adult
        case Items.LONGSHOT:
            return can_be_adult
        case Items.SCARECROW:
            return can_be_adult
        case Items.DISTANT_SCARECROW:
            return can_be_adult
        case Items.GORON_TUNIC:
            return can_be_adult
        case Items.ZORA_TUNIC:
            return can_be_adult
        case Items.MIRROR_SHIELD:
            return can_be_adult
        case Items.MASTER_SWORD:
            return can_be_adult
        case Items.BIGGORONS_SWORD:
            return can_be_adult
        case Items.SILVER_GAUNTLETS:
            return can_be_adult
        case Items.GOLDEN_GAUNTLETS:
            return can_be_adult
        case Items.POCKET_EGG:
            return can_be_adult
        case Items.COJIRO:
            return can_be_adult
        case Items.ODD_MUSHROOM:
            return can_be_adult
        case Items.ODD_POTION:
            return can_be_adult
        case Items.POACHERS_SAW:
            return can_be_adult
        case Items.BROKEN_GORONS_SWORD:
            return can_be_adult
        case Items.PRESCRIPTION:
            return can_be_adult
        case Items.EYEBALL_FROG:
            return can_be_adult
        case Items.WORLDS_FINEST_EYEDROPS:
            return can_be_adult
        case Items.CLAIM_CHECK:
            return can_be_adult
        case Items.FAIRY_SLINGSHOT:
            return can_be_child and (has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_SEEDS))
        case Items.BOOMERANG:
            return can_be_child
        case Items.KOKIRI_SWORD:
            return can_be_child
        case Items.NUTS:
            return (has(Events.NUT_POT) or has(Events.NUT_CRATE) or has(Events.DEKU_BABA_NUTS)) and has(Events.AMMO_CAN_DROP)
        case Items.STICKS:
            return can_be_child and (has(Events.STICK_POT) or has(Events.DEKU_BABA_STICKS))
        case Items.DEKU_SHIELD:
            return can_be_child
        case Items.PROGRESSIVE_BOMB_BAG:
            return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_BOMBS)
        case Items.BOMB_BAG:
            return has(Events.AMMO_CAN_DROP) or has(Events.CAN_BUY_BOMBS)
        case Items.PROGRESSIVE_BOMBCHU:
            return BombchuRefill(state, world) and BombchusEnabled(state, world)
        case Items.BOMBCHUS_5:
            return BombchuRefill(state, world) and BombchusEnabled(state, world)
        case Items.BOMBCHUS_10:
            return BombchuRefill(state, world) and BombchusEnabled(state, world)
        case Items.BOMBCHUS_20:
            return BombchuRefill(state, world) and BombchusEnabled(state, world)
        case Items.WEIRD_EGG:
            return can_be_child
        case Items.BOTTLE_WITH_RUTOS_LETTER:
            return can_be_child
        case Items.MAGIC_BEAN:
            return can_be_child
        case Items.ZELDAS_LULLABY:
            return CanPlaySong(state, world, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON)
        case Items.EPONAS_SONG:
            return CanPlaySong(state, world, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON)
        case Items.PRELUDE_OF_LIGHT:
            return CanPlaySong(state, world, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON)
        case Items.SARIAS_SONG:
            return CanPlaySong(state, world, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON)
        case Items.SUNS_SONG:
            return CanPlaySong(state, world, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON, Items.OCARINA_CDOWN_BUTTON)
        case Items.SONG_OF_TIME:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON)
        case Items.BOLERO_OF_FIRE:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON)
        case Items.REQUIEM_OF_SPIRIT:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON)
        case Items.SONG_OF_STORMS:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON, Items.OCARINA_CUP_BUTTON, Items.OCARINA_CDOWN_BUTTON)
        case Items.MINUET_OF_FOREST:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON)
        case Items.SERENADE_OF_WATER:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON)
        case Items.FISHING_POLE:
            return has(Items.CHILD_WALLET) # as long as you have enough rubies
        case _:
            return False

def ScarecrowsSong(state: CollectionState, world: SohWorld) -> bool:
    #TODO handle scarecrow song option in place of the False
    return (False and HasItem(state, world, Items.FAIRY_OCARINA) and OcarinaButtons(state, world) > 2) or \
        (HasItem(state, world, Events.CHILD_SCARECROW) and HasItem(state, world, Events.ADULT_SCARECROW))

def HasBottle(state: CollectionState, world: SohWorld) -> bool: # soup
    return BottleCount(state, world) >= 1

def BottleCount(state: CollectionState, world: SohWorld) -> int:
    count = 0
    for name in [Items.EMPTY_BOTTLE, Items.BOTTLE_WITH_BLUE_POTION, Items.BOTTLE_WITH_BUGS, Items.BOTTLE_WITH_FAIRY, Items.BOTTLE_WITH_FISH, \
                  Items.BOTTLE_WITH_GREEN_POTION, Items.BOTTLE_WITH_GREEN_POTION, Items.BOTTLE_WITH_BLUE_FIRE, Items.BOTTLE_WITH_MILK, Items.BOTTLE_WITH_RED_POTION]:
        count += state.count(name, world.player)
    if state.has(Events.DELIVER_LETTER, world.player):
        count += state.count(Items.BOTTLE_WITH_RUTOS_LETTER, world.player)
    if state.has(Events.CAN_EMPTY_BIG_POES, world.player):
        count += state.count(Items.BOTTLE_WITH_BIG_POE, world.player)
    return count

def BombchuRefill(state: CollectionState, world: SohWorld) -> bool:
    return state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player) or False #TODO put enable bombchu drops option here

def BombchusEnabled(state: CollectionState, world: SohWorld) -> bool:
    if False: #TODO bombchu bag enabled
        return HasItem(state, world, Items.BOMBCHU_BAG)
    return HasItem(state, world, Items.BOMB_BAG)

def CanPlaySong(state: CollectionState, world: SohWorld, *buttons: str) -> bool:
    if not HasItem(state, world, Items.FAIRY_OCARINA):
        return False
    for button in buttons:
        if button in state.prog_items.values(): #if this is false, then button shuffle is disabled
            if not state.has(button, world.player):
                return False
        else: #button shuffle disabled
            return True
    return True

def OcarinaButtons(state: CollectionState, world: SohWorld) -> int:
    return state.count_from_list([Items.OCARINA_ABUTTON, Items.OCARINA_CDOWN_BUTTON, Items.OCARINA_CLEFT_BUTTON, \
                                  Items.OCARINA_CUP_BUTTON, Items.OCARINA_CRIGHT_BUTTON], world.player)