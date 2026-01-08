import random
from typing import Optional

from .area_rando_types import DoorPairs
from .fillInterface import FillAlgorithm
from .item_data import Item, items_unpackable
from .loadout import Loadout
from .location_data import Location

# this will not update any of the parameters it is given
# but it will return an item to place at a location


(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    Aqua, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, AccelCharge, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


class FillSpeedrun(FillAlgorithm):
    earlyItemList: list[Item]
    progressionItemList: list[Item]
    extraItemList: list[Item]
    itemLists: list[list[Item]]
    """
    itemLists should contain
    [0] earlyItemList
    [1] progressionItemList
    [2] extraItemList
    """

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
            Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy
        ]
        self.extraItemList = [
            Hypercharge,
            Xray,
            DamageAmp, DamageAmp, DamageAmp, DamageAmp, DamageAmp, DamageAmp,
            AccelCharge, AccelCharge, AccelCharge, AccelCharge, AccelCharge, AccelCharge,
            Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy,
            Refuel, Refuel, Refuel, Refuel, Refuel, Refuel, Refuel,
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

        self.itemLists = [self.earlyItemList, self.progressionItemList, self.extraItemList]

    def choose_placement(self,
                         availableLocations: list[Location],
                         loadout: Loadout) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """
        assert len(availableLocations), "placement algorithm received 0 available locations"

        if availableLocations[0]['fullitemname'] == "TORPEDO BAY":
            return availableLocations[0], random.choice([Missile, Morph])

        from_items = (
            self.earlyItemList if len(self.earlyItemList) else (
                self.progressionItemList if len(self.progressionItemList) else (
                    self.extraItemList
                )
            )
        )

        assert len(from_items), "tried to place item when placement algorithm has 0 items left in item pool"

        return random.choice(availableLocations), random.choice(from_items)

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
