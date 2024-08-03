
from ..Locations import LocDetails, SOTLocation
from .Balance import Balance

class ShopLocation(SOTLocation):

    def __init__(self, locDetails: LocDetails, player: int, region, price: Balance):
        super().__init__(locDetails, player, region)
        self.item_name_override: str = ""
        self.price: Balance = price
        self.shop_abrev: str = getShopLocAbrev(locDetails)


    def display_text(self) -> str:
        return "{}: {}".format(self.item_name_override, self.price.displayString())

def getShopLocAbrev(locDetails: LocDetails) -> str:
    abrev = ""
    splits = locDetails.name.split(' ')
    for split in splits:
        abrev += splits[0]
    return locDetails.name