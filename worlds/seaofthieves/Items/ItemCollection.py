import typing
from .ItemDetail import ItemDetail
from BaseClasses import ItemClassification
from .Items import Items
class ItemCollection:
    # Note seals are not added cause we dont want them randomzed in the general pool

    def __init__(self):
        self.ItemNameToId = None
        self.ItemNameToItemDetail: typing.Dict[str, ItemDetail] = {}
        self.filler = []
        self.trap = []
        self.progression = []

        self.pre_fill_count = 0
        self.pre_fill_name_to_count = {}

    def informCollectionOfPrefillAction(self, name: str, cnt: int):
        if name in self.pre_fill_name_to_count.keys():
            self.pre_fill_name_to_count[name] += cnt
        self.pre_fill_name_to_count[name] = cnt
        self.pre_fill_count += cnt

    def getPreFillCountForName(self, name: str) -> int:
        if name in self.pre_fill_name_to_count.keys():
            return self.pre_fill_name_to_count[name]
        return 0

    def getFillerItemName(self):
        # TODO I believe this will eventually return the filler items for other worlds when that is implemented, this should be random
        return self.filler[0].name

    def getDict(self):
        if self.ItemNameToId is not None:
            return ItemCollection.ItemNameToId

        self.ItemNameToId = {}
        for item_detail in Items.__dict__.items():
            if item_detail[0].startswith("_"):
                continue
            self.ItemNameToId[item_detail[1].name] = item_detail[1].id
            self.ItemNameToItemDetail[item_detail[1].name] = item_detail[1]

            if item_detail[1].classification == ItemClassification.filler:
                self.filler.append(item_detail[1])

            elif item_detail[1].classification == ItemClassification.trap:
                self.trap.append(item_detail[1])

            elif item_detail[1].classification == ItemClassification.progression:
                self.progression.append(item_detail[1])

        return self.ItemNameToId

    def getItemCount(self):
        sum = 0
        for det in self.ItemNameToItemDetail.values():
            sum += det.countToSpawnByDefault
        return sum - self.pre_fill_count

    def getNameFromId(self, id: int) -> str:
        if self.ItemNameToId is None:
            self.getDict()
        for itm in self.ItemNameToId:
            if self.ItemNameToId[itm] == id:
                return itm

        return ""