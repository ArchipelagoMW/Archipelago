class CharacterSprite:
    def __init__(self, id, data):
        self.id = id
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data
