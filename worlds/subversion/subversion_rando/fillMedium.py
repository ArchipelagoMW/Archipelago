from typing import Optional
import random

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


class FillMedium(FillAlgorithm):
    earlyItemList: list[Item]
    lowPowerList: list[Item]
    highPowerList: list[Item]
    extraItemList: list[Item]

    itemLists: list[list[Item]]
    """
    itemLists should contain
    [0] earlyItemList
    [1] lowPowerList
    [2] highPowerList
    [3] extraItemList
    """

    def __init__(self, door_pairs: DoorPairs) -> None:
        self.earlyItemList = [
            Missile,
            Morph,
            GravityBoots
        ]
        self.lowPowerList = [
            Super,
            Speedball,
            Bombs,
            HiJump,
            Aqua,
            DarkVisor,
            Wave,
            SpeedBooster,
            SpaceJump,
            Charge,
            Energy, Energy, Energy, Energy, Energy
        ]
        self.highPowerList = [
            Grapple,
            PowerBomb,
            Varia,
            Ice,
            MetroidSuit,
            Screw,
            Spazer,
            Plasma,
            Hypercharge
        ]
        self.extraItemList = [
            Xray,
            DamageAmp, DamageAmp, DamageAmp,
            DamageAmp, DamageAmp, DamageAmp,
            AccelCharge, AccelCharge, AccelCharge,
            AccelCharge, AccelCharge, AccelCharge,
            Refuel, Refuel, Refuel, Refuel, Refuel, Refuel, Refuel,
            Energy, Energy, Energy, Energy,
            Energy, Energy, Energy, Energy, Energy,
            Energy, Energy, Energy, Energy,
            SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
            SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
            SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
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
            LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
            LargeAmmo, LargeAmmo, LargeAmmo
        ]

        self.itemLists = [self.earlyItemList, self.lowPowerList, self.highPowerList, self.extraItemList]

    def choose_placement(self,
                         availableLocations: list[Location],
                         loadout: Loadout) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """
        assert len(availableLocations), "placement algorithm received 0 available locations"

        from_items = (
            self.earlyItemList if len(self.earlyItemList) else (
                self.lowPowerList if len(self.lowPowerList) else (
                    self.highPowerList if len(self.highPowerList) else (
                        self.extraItemList
                    )
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
