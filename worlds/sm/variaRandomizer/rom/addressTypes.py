from .rom import snes_to_pc, pc_to_snes

class Byte(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value]

class Word(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value, self.value+1]

class Long(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value, self.value+1, self.value+2]

class ValueSingle(object):
    def __init__(self, value, storage=Word):
        self.value = snes_to_pc(value)
        self.storage = storage

    def getOne(self):
        return self.value

    def getAll(self):
        return [self.value]

    def getWeb(self):
        return self.storage(self.value).expand()

class ValueList(object):
    def __init__(self, values, storage=Word):
        self.values = [snes_to_pc(value) for value in values]
        self.storage = storage

    def getOne(self):
        return self.values[0]

    def getAll(self):
        return self.values

    def getWeb(self):
        out = []
        for value in self.values:
            out += self.storage(value).expand()
        return out

class ValueRange(object):
    def __init__(self, start, length=-1, end=-1):
        self.start = snes_to_pc(start)
        if length != -1:
            self.end = self.start + length
            self.length = length
        else:
            self.end = snes_to_pc(end)
            self.length = self.end - self.start

    def getOne(self):
        return self.start

    def getAll(self):
        return [self.start+i for i in range(self.length)]

    def getWeb(self):
        return [self.start, self.end]
