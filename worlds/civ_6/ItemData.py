from typing import TypedDict


class NewItemData(TypedDict):
    Type: str
    Cost: int
    UITreeRow: int
    EraType: str


class ExistingItemData(NewItemData):
    Name: str
