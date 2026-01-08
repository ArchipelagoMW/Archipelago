from ...data.text import get_bytes, get_string

class Dialog():
    def __init__(self, id, type, data):
        self.id = id
        self.type = type
        self._text = get_string(data, self.type)

        self.modified = False
        self.original_data = data

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self.modified = True
        self._text = value

    def data(self):
        if self.modified:
            # only convert modified text
            # converting every dialog frees up a lot of space (~7-10k bytes) but is slightly slower
            # remove modified flag and convert all if extra dialog space needed
            return get_bytes(self.text, self.type)
        return self.original_data

    def __str__(self):
        return f"{self.id:<4} '{self.text}'"

    def print(self):
        print(str(self))
