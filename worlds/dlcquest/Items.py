import csv
import enum
import typing
from BaseClasses import Item, ItemClassification
from . import Options, data

class DLCquestItem(Item):
    game: str = "DLCquest"

offset = 120_000

class Group(enum.Enum):
    DLC = enum.auto()

@dataclass(frozen=True)
class ItemData:
    code_without_offset: Optional[int]
    name: str
    classification: ItemClassification
    groups: Set[Group] = field(default_factory=frozenset)

    def __post_init__(self):
        if not isinstance(self.groups, frozenset):
            super().__setattr__("groups", frozenset(self.groups))

    @property
    def code(self):
        return offset + self.code_without_offset if self.code_without_offset is not None else None

    def has_any_group(self, *group: Group) -> bool:
        groups = set(group)
        return bool(groups.intersection(self.groups))


def load_item_csv():
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    items = []
    with files(data).joinpath("items.csv").open() as file:
        item_reader = csv.DictReader(file)
        for item in item_reader:
            id = int(item["id"]) if item["id"] else None
            classification = ItemClassification[item["classification"]]
            groups = {Group[group] for group in item["groups"].split(",") if group}
            items.append(ItemData(id, item["name"], classification, groups))
    return items

def initialize_item_table():
    item_table.update({item.name: item for item in all_items})