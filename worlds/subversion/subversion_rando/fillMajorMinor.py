from typing import Optional
import random

from .area_rando_types import DoorPairs
from .fillInterface import FillAlgorithm
from .item_data import Item, items_unpackable
from .loadout import Loadout
from .location_data import Location, majorLocs, eTankLocs

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    Aqua, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, AccelCharge, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


class FillMajorMinor(FillAlgorithm):
    earlyItemList: list[Item]
    progressionItemList: list[Item]
    eTankList: list[Item]
    extraItemList: list[Item]

    itemLists: list[list[Item]]

    def __init__(self, door_pairs: DoorPairs) -> None:
        self.earlyItemList = [
            Missile,
            Morph,
            GravityBoots
        ]
        self.progressionItemList = [
            Super,
            Grapple,
            PowerBomb,
            Speedball,
            Bombs,
            HiJump,
            Aqua,
            DarkVisor,
            Wave,
            SpeedBooster,
            Spazer,
            Varia,
            Ice,
            MetroidSuit,
            Plasma,
            Screw,
            SpaceJump,
            Charge,
            Hypercharge,
            Xray,
            Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy
        ]
        self.eTankList = [Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy]
        self.extraItemList = [
            Refuel, Refuel, Refuel, Refuel, Refuel, Refuel, Refuel,
            DamageAmp, DamageAmp, DamageAmp, DamageAmp, DamageAmp, DamageAmp,
            AccelCharge, AccelCharge, AccelCharge, AccelCharge, AccelCharge, AccelCharge,
            SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
            SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo
        ]
        self.itemLists = [self.earlyItemList, self.progressionItemList, self.eTankList, self.extraItemList]

    def choose_placement(self,
                         availableLocations: list[Location],
                         loadout: Loadout) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """

        assert len(availableLocations), "placement algorithm received 0 available locations"

        for torpedoSearch in availableLocations:
            # print("Searching for Torpedo Bay: ", torpedoSearch['fullitemname'])
            if torpedoSearch['fullitemname'] == "Torpedo Bay":
                # print("          found Torpedo Bay")
                placeItem = random.choice([Missile, Morph])
                # print(availableLocations[0], " - - - ", placeItem)
                placeLocation = torpedoSearch
                return placeLocation, placeItem

        from_items = (
            self.earlyItemList if len(self.earlyItemList) else (
                self.progressionItemList if len(self.progressionItemList) else (
                    self.eTankList if len(self.eTankList) else (
                        self.extraItemList
                    )
                )
            )
        )

        if from_items is self.extraItemList:
            valid_locations = availableLocations
        else:  # not extraItemList
            # load majors
            valid_locations = [
                loc
                for loc in availableLocations
                if (loc['fullitemname'] in majorLocs or loc["fullitemname"] in eTankLocs)
            ]
            if from_items is self.earlyItemList and len(valid_locations) == 0 and (
                (Morph in loadout) or (
                    (GravityBoots in loadout) and (Missile in loadout)
                )
            ):
                sandy = loadout.game.all_locations["Sandy Cache"]
                # print("   ---   appending sandy cache")
                valid_locations.append(sandy)
                availableLocations.append(sandy)
            if len(valid_locations) == 0:
                return None  # fail

        return random.choice(valid_locations), random.choice(from_items)

    def count_items_remaining(self) -> int:
        return sum(len(li) for li in self.itemLists)

    def remove_from_pool(self, item: Item) -> None:
        """ removes this item from the item pool """
        for each_list in self.itemLists:
            try:
                i = each_list.index(item)
                each_list.pop(i)
                break
            except ValueError:
                # not in this list
                pass
