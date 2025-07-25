from typing import List
from BaseClasses import CollectionState, Region, Entrance
from .Enums import *
from .Regions import can_access_entrance_as_adult, can_access_entrance_as_child, can_access_region_as_adult, can_access_region_as_child
from worlds.oot_soh import SohWorld
#Contains a set of helpers for access rules

#TODO Some of this uses Item names that will likely move to the Events enum
def HasItem(state: CollectionState, world: "SohWorld", itemName: str, count:int = 1, can_be_child: bool = True, can_be_adult: bool = True) -> bool:
    def has(name, count=1): 
        if name in state.prog_items:
            return state.has(name, world.player, count) #To shorten the many calls in this function
        return False
    def can_use(name, count=1):
        return CanUse(state, world, name, can_be_child, can_be_adult)
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
            return (BombchusEnabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value, Items.PROGRESSIVE_BOMBCHU.value], world.player)
        #Ship def:
        #return (BombchusEnabled() && (GetInLogic(LOGIC_BUY_BOMBCHUS) || CouldPlayBowling || CarpetMerchant)) ||
        #           CheckInventory(ITEM_BOMBCHU, true);
        case Items.BOMBCHUS_5.value:
            return (BombchusEnabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value, Items.PROGRESSIVE_BOMBCHU.value], world.player)
        case Items.BOMBCHUS_10.value:
            return (BombchusEnabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value, Items.PROGRESSIVE_BOMBCHU.value], world.player)
        case Items.BOMBCHUS_20.value:
            return (BombchusEnabled(state, world) and state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player)) \
                or state.has_any([Items.BOMBCHUS_5.value, Items.BOMBCHUS_10.value, Items.BOMBCHUS_20.value, Items.PROGRESSIVE_BOMBCHU.value], world.player)
        case Items.SCARECROW.value:
            return ScarecrowsSong(state, world) and can_use(Items.HOOKSHOT.value)
        case Items.DISTANT_SCARECROW.value:
            return ScarecrowsSong(state, world) and can_use(Items.LONGSHOT.value)
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
            return HasBottle(state, world)
        case _:
            return has(itemName, count)
        
def CanUse(state: CollectionState, world: "SohWorld", name: str, can_be_child: bool = True, can_be_adult: bool = True) -> bool:
    if not HasItem(state, world, name):
        return False
    def has(name, count=1): 
        return HasItem(state, world, name, count, can_be_child, can_be_adult)
    def can_use(name, count=1):
        return CanUse(state, world, name, can_be_child, can_be_adult)
    magic = lambda: can_use(Items.MAGIC_SINGLE.value)
    match name:
        case Items.MAGIC_SINGLE.value:
            return has(Events.AMMO_CAN_DROP) or (HasBottle(state, world) and has(Events.CAN_BUY_GREEN_POTION))
        case Items.DINS_FIRE.value:
            return can_use(Items.MAGIC_SINGLE.value)
        case Items.NAYRUS_LOVE.value:
            return can_use(Items.MAGIC_SINGLE.value)
        case Items.FARORES_WIND.value:
            return can_use(Items.MAGIC_SINGLE.value)
        case Items.LENS_OF_TRUTH.value:
            return can_use(Items.MAGIC_SINGLE.value)
        case Items.FIRE_ARROW.value:
            return can_use(Items.MAGIC_SINGLE.value) and can_use(Items.FAIRY_BOW.value)
        case Items.ICE_ARROW.value:
            return can_use(Items.MAGIC_SINGLE.value) and can_use(Items.FAIRY_BOW.value)
        case Items.LIGHT_ARROW.value:
            return can_use(Items.MAGIC_SINGLE.value) and can_use(Items.FAIRY_BOW.value)
        case Items.FAIRY_BOW.value:
            return can_be_adult and (Events.AMMO_CAN_DROP or has(Events.CAN_BUY_ARROWS))
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
            return BombchuRefill(state, world) and BombchusEnabled(state, world)
        case Items.BOMBCHUS_5.value:
            return BombchuRefill(state, world) and BombchusEnabled(state, world)
        case Items.BOMBCHUS_10.value:
            return BombchuRefill(state, world) and BombchusEnabled(state, world)
        case Items.BOMBCHUS_20.value:
            return BombchuRefill(state, world) and BombchusEnabled(state, world)
        case Items.WEIRD_EGG.value:
            return can_be_child
        case Items.BOTTLE_WITH_RUTOS_LETTER.value:
            return can_be_child
        case Items.MAGIC_BEAN.value:
            return can_be_child
        case Items.ZELDAS_LULLABY.value:
            return CanPlaySong(state, world, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value)
        case Items.EPONAS_SONG.value:
            return CanPlaySong(state, world, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value)
        case Items.PRELUDE_OF_LIGHT.value:
            return CanPlaySong(state, world, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value)
        case Items.SARIAS_SONG.value:
            return CanPlaySong(state, world, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.SUNS_SONG.value:
            return CanPlaySong(state, world, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.SONG_OF_TIME.value:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.BOLERO_OF_FIRE.value:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.REQUIEM_OF_SPIRIT.value:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.SONG_OF_STORMS.value:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CUP_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.MINUET_OF_FOREST.value:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CUP_BUTTON.value)
        case Items.SERENADE_OF_WATER.value:
            return CanPlaySong(state, world, Items.OCARINA_ABUTTON.value, Items.OCARINA_CLEFT_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value, Items.OCARINA_CDOWN_BUTTON.value)
        case Items.FISHING_POLE.value:
            return has(Items.CHILD_WALLET.value) # as long as you have enough rubies
        case _:
            return False

def ScarecrowsSong(state: CollectionState, world: "SohWorld") -> bool:
    #TODO handle scarecrow song option in place of the False
    return (False and HasItem(state, world, Items.FAIRY_OCARINA.value) and OcarinaButtons(state, world) > 2) or \
        (HasItem(state, world, Events.CHILD_SCARECROW) and HasItem(state, world, Events.ADULT_SCARECROW))

def HasBottle(state: CollectionState, world: "SohWorld") -> bool: # soup
    return BottleCount(state, world) >= 1

def BottleCount(state: CollectionState, world: "SohWorld") -> int:
    count = 0
    for name in [Items.EMPTY_BOTTLE.value, Items.BOTTLE_WITH_BLUE_POTION.value, Items.BOTTLE_WITH_BUGS.value, Items.BOTTLE_WITH_FAIRY.value, Items.BOTTLE_WITH_FISH.value, \
                  Items.BOTTLE_WITH_GREEN_POTION.value, Items.BOTTLE_WITH_GREEN_POTION.value, Items.BOTTLE_WITH_BLUE_FIRE.value, Items.BOTTLE_WITH_MILK.value, Items.BOTTLE_WITH_RED_POTION.value]:
        count += state.count(name, world.player)
    if state.has(Events.DELIVER_LETTER, world.player):
        count += state.count(Items.BOTTLE_WITH_RUTOS_LETTER.value, world.player)
    if state.has(Events.CAN_EMPTY_BIG_POES, world.player):
        count += state.count(Items.BOTTLE_WITH_BIG_POE.value, world.player)
    return count

def BombchuRefill(state: CollectionState, world: "SohWorld") -> bool:
    return state.has_any([Events.CAN_BUY_BOMBCHUS, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player) or False #TODO put enable bombchu drops option here

def BombchusEnabled(state: CollectionState, world: "SohWorld") -> bool:
    if False: #TODO bombchu bag enabled
        return HasItem(state, world, Items.BOMBCHU_BAG.value)
    return HasItem(state, world, Items.BOMB_BAG.value)

def CanPlaySong(state: CollectionState, world: "SohWorld", *buttons: str) -> bool:
    if not HasItem(state, world, Items.FAIRY_OCARINA.value):
        return False
    for button in buttons:
        if button in state.prog_items.values(): #if this is false, then button shuffle is disabled
            if not state.has(button, world.player):
                return False
        else: #button shuffle disabled
            return True
    return True

def OcarinaButtons(state: CollectionState, world: "SohWorld") -> int:
    return state.count_from_list([Items.OCARINA_ABUTTON.value, Items.OCARINA_CDOWN_BUTTON.value, Items.OCARINA_CLEFT_BUTTON.value, \
                                  Items.OCARINA_CUP_BUTTON.value, Items.OCARINA_CRIGHT_BUTTON.value], world.player)