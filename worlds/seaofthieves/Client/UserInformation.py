from worlds.seaofthieves.Configurations.SotOptionsDerived import SotOptionsDerived
from worlds.seaofthieves import ClientInput
from typing import Optional


class SotLoginCredentials:

    def __init__(self, msCookie: str):
        self.msCookie = msCookie


class SotAnalyzerDetails:

    def __init__(self, shipName: Optional[str], pirateName: Optional[str]):
        self.shipName: Optional[str] = shipName
        self.pirateName: Optional[str] = pirateName

    def set_pirate(self, name: str) -> None:
        self.pirateName = name
        self.shipName = None

    def set_ship(self, name: str) -> None:
        self.shipName = name
        self.pirateName = None

    def get_ship(self) -> Optional[str]:
        return self.shipName

    def get_pirate(self) -> Optional[str]:
        return self.pirateName


class UserInformation:

    def __init__(self, sotLoginCreds: Optional[SotLoginCredentials] = None,
                 sotAnalyzerDetails: Optional[SotAnalyzerDetails] = None, clientInput: Optional[ClientInput] = None):
        self.__initialize(sotLoginCreds, sotAnalyzerDetails, clientInput)

    def __initialize(self, sotLoginCreds: Optional[SotLoginCredentials] = None,
                     sotAnalyzerDetails: Optional[SotAnalyzerDetails] = None,
                     clientInput: Optional[ClientInput] = None):
        self.loginCreds: Optional[SotLoginCredentials] = sotLoginCreds
        self.analyzerDetails: Optional[SotAnalyzerDetails] = sotAnalyzerDetails
        self.generationData: Optional[ClientInput] = ClientInput() if clientInput is None else clientInput

    def hasEnoughToPlay(self) -> bool:
        return self.generationData.hasEnoughToPlay()
