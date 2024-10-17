from BaseClasses import ItemClassification


class ItemDetail:
    name: str = ""
    seedId: int = 8000000
    id: int = seedId

    def __init__(self, name, classification: ItemClassification, numeric=0, countToSpawnByDefault=1):
        self.name = name
        self.id = ItemDetail.seedId
        ItemDetail.seedId += 1
        self.req_qty = 1
        self.countToSpawnByDefault = countToSpawnByDefault
        self.classification: ItemClassification = classification

        # extra property to hold numerical data for things like money
        self.numeric_value = numeric
        self.sound_file: str = ""

    def __str__(self):
        return self.id
