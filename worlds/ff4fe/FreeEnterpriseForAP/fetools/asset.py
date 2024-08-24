import dataclasses
import uuid
import base64
import json
import time
import os

@dataclasses.dataclass
class Asset:
    id : str = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())

        self.ctime = None
        self.mtime = None

    @property
    def fields(self):
        return dataclasses.fields(self)

    def asdict(self):
        data = dataclasses.asdict(self)
        for field in self.fields:
            if field.type is bytes:
                data[field.name] = base64.b64encode(data[field.name]).decode('utf-8')
        return data

    @classmethod
    def fromdict(cls, data):
        asset = cls()
        data = data.copy()
        for field in asset.fields:
            if field.type is bytes and field.name in data and type(data[field.name]) is str:
                data[field.name] = base64.b64decode(data[field.name])
        return dataclasses.replace(asset, **data)

    @classmethod
    def fromfile(cls, file_path):
        with open(file_path, 'r') as infile:
            data = json.load(infile)

        asset = cls.fromdict(data)
        asset.ctime = os.path.getctime(file_path)
        asset.mtime = os.path.getmtime(file_path)

        return asset

    def save(self, file_path):
        with open(file_path, 'w') as outfile:
            json.dump(self.asdict(), outfile, indent=4)

        self.ctime = os.path.getctime(file_path)
        self.mtime = os.path.getmtime(file_path)


# Helper decorator that takes a class and returns the equivalent dataclass, inheriting from Asset
def assetclass(cls):
    base_dataclass = dataclasses.dataclass(cls)
    field_tuples = [ (f.name, f.type, f) for f in dataclasses.fields(base_dataclass) ]
    return dataclasses.make_dataclass(cls.__name__, field_tuples, bases=(Asset,))

if __name__ == '__main__':
    @assetclass
    class Foo:
        king: str = "blah"
        queen: int = 12
        jack: bytes = bytes([1,2,3])

    x = Foo()
    setattr(x, 'futon', 'blablah')
    print(type(x))
    print(x.asdict())
    print(x.id)

