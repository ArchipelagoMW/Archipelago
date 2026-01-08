class MetamorphGroup:
    DATA_SIZE = 4

    def __init__(self, id, data):
        self.id = id
        self.items = data

    def data(self):
        return self.items
