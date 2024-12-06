from .Configurations import SotOptionsDerived
import typing
import pickle
from .Regions.ConnectionDetails import ConnectionDetails
from .MultiworldHints import MultiworldHints
from .Locations.Shop.ShopWarehouse import ShopWarehouse
from .Hint import HintStringLibrary

class ClientInput:

    FILE_SUFFIX = "apsot"

    def __init__(self):
        self.sotOptionsDerived = None
        self.regionRules = None
        self.multiworldHints: typing.Optional[MultiworldHints] = None
        self.shopWarehouse: typing.Optional[ShopWarehouse] = None
        self.hintLibrary: typing.Optional[HintStringLibrary] = None

    def to_file(self, output_file_and_directory: str):
        with open(output_file_and_directory, 'wb') as f:
           pickle.dump(self, f)

    def from_fire(self, filename: str):
        with open(filename, 'rb') as f:
            clientInput = pickle.load(f)
        self.sotOptionsDerived = clientInput.sotOptionsDerived
        self.regionRules = clientInput.regionRules
        self.multiworldHints = clientInput.multiworldHints
        self.shopWarehouse = clientInput.shopWarehouse
        self.hintLibrary = clientInput.hintLibrary

    def hasEnoughToPlay(self) -> bool:
        return self.sotOptionsDerived is not None and self.regionRules is not None
