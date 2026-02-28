from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .songinfo import Songs

from .yarghelpers import itemnamefromindex

if TYPE_CHECKING:
    from .world import YARGWorld

ITEM_NAME_TO_ID = {}

longnames = False

#Reserve item id 1 for the filler "YARG Gem" item
#If we put future items before or after the songs is
#yet to be decided, although I (energymaster) am leaning
#towards before
itemID = 1
ITEM_NAME_TO_ID["YARG Gem"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["Star Power Bonus"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["Guitar"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["Bass"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["Rhythm"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["Drums"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["Keys"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["Pro Keys"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["Vocals"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["2 Part Harmony"] = (itemID)
itemID = itemID + 1
ITEM_NAME_TO_ID["3 Part Harmony"] = (itemID)
itemID = itemID + 1

if longnames == False:
    for index in Songs.keys():
        ITEM_NAME_TO_ID[f'"{(Songs.get(index)).songname}" by {(Songs.get(index)).artistname}'] = (itemID)
        itemID = itemID + 1

if longnames == True:
    for index in Songs.keys():
        ITEM_NAME_TO_ID[f'"{(Songs.get(index)).songname}" by {(Songs.get(index)).artistname} from {(Songs.get(index)).source}'] = (itemID)
        itemID = itemID + 1


DEFAULT_ITEM_CLASSIFICATIONS = {}

for index in Songs.keys():
    DEFAULT_ITEM_CLASSIFICATIONS[itemnamefromindex(index)] = (ItemClassification.progression)

DEFAULT_ITEM_CLASSIFICATIONS["YARG Gem"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["Star Power Bonus"] = (ItemClassification.filler)
DEFAULT_ITEM_CLASSIFICATIONS["Guitar"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["Bass"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["Rhythm"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["Drums"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["Keys"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["Pro Keys"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["Vocals"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["2 Part Harmony"] = (ItemClassification.progression)
DEFAULT_ITEM_CLASSIFICATIONS["3 Part Harmony"] = (ItemClassification.progression)

class YARGItem(Item):
    game = "YARG"


def get_random_filler_item_name(world: YARGWorld) -> str:
    return "Star Power Bonus"


def create_item_with_correct_classification(world: YARGWorld, name: str) -> YARGItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return YARGItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: YARGWorld) -> None:
    itempool: list[Item] = []

    #Create Instrument Items if shuffle is on
    if world.shuffletoggle:
        for inst in world.instrumentlist:
            toitem = ""
            
            if inst == "guitar5F":
                toitem = "Guitar"
            if inst == "bass5F":
                toitem = "Bass"
            if inst == "rhythm5F":
                toitem = "Rhythm"
            if inst == "drums":
                toitem = "Drums"
            if inst == "keys5F":
                toitem = "Keys"
            if inst == "keysPro":
                toitem = "Pro Keys"
            if inst == "vocals":
                toitem = "Vocals"
            if inst == "harmony2":
                toitem = "2 Part Harmony"
            if inst == "harmony3":
                toitem = "3 Part Harmony"

            if toitem != world.startinginstrument:    
                itempool.append(world.create_item(str(toitem)))


    for index in world.selectedsonglist:
        if index != world.starting_song:
            if index != world.starting_song2:
                itempool.append(world.create_item(itemnamefromindex(index)))
    for i in range(world.yarggemamount):
        itempool.append(world.create_item("YARG Gem"))


    #Add necessary filler
    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
