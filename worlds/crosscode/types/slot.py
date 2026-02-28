import typing

class SlotOptions(typing.TypedDict):
    vtShadeLock: int | bool
    meteorPassage: bool
    vtSkip: bool
    keyrings: list[int]
    questRando: bool
    hiddenQuestRewardMode: str
    hiddenQuestObfuscationLevel: str
    questDialogHints: bool
    progressiveChains: dict[int, list[int]]
    shopSendMode: str
    shopReceiveMode: str
    shopDialogHints: bool
    chestClearanceLevels: dict[int, str]

class SlotData(typing.TypedDict):
    mode: str
    dataVersion: str
    options: SlotOptions
