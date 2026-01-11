from typing import TYPE_CHECKING, Dict
from BaseClasses import Item, ItemClassification
from .data import data
from .groups import item_groups
from .options import ShufflePokedex, ShuffleRunningShoes

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


RENEWABLE_PROGRESSION_ITEMS = ("Fresh Water", "Soda Pop", "Lemonade", "King's Rock", "Metal Coat", "Dragon Scale",
                               "Up-Grade", "Deep Sea Scale", "Deep Sea Tooth", "Heart Scale")


class PokemonFRLGItem(Item):
    game: str = "Pokemon FireRed and LeafGreen"

    def __init__(self, name: str, classification: ItemClassification, code: int | None, player: int) -> None:
        super().__init__(name, classification, code, player)


class PokemonFRLGGlitchedToken(PokemonFRLGItem):
    game: str = "Pokemon FireRed and LeafGreen"
    TOKEN_NAME = "GLITCHED_TOKEN"

    def __init__(self, player) -> None:
        super().__init__(name=self.TOKEN_NAME, classification=ItemClassification.progression, code=None, player=player)


def create_item_name_to_id_map() -> Dict[str, int]:
    """
    Creates a map from item names to their AP item ID (code)
    """
    name_to_id_map: Dict[str, int] = {}
    for item_id, item_data in data.items.items():
        name_to_id_map[item_data.name] = item_id

    return name_to_id_map


def get_item_classification(item_id: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[item_id].classification


def add_starting_items(world: "PokemonFRLGWorld") -> None:
    if world.options.shuffle_pokedex == ShufflePokedex.option_start_with:
        world.options.start_inventory.value["Pokedex"] = 1
        world.multiworld.push_precollected(world.create_item("Pokedex"))
    if world.options.shuffle_running_shoes == ShuffleRunningShoes.option_start_with:
        world.options.start_inventory.value["Running Shoes"] = 1
        world.multiworld.push_precollected(world.create_item("Running Shoes"))
    if not world.options.shuffle_berry_pouch:
        world.options.start_inventory.value["Berry Pouch"] = 1
        world.multiworld.push_precollected(world.create_item("Berry Pouch"))
    if not world.options.shuffle_tm_case:
        world.options.start_inventory.value["TM Case"] = 1
        world.multiworld.push_precollected(world.create_item("TM Case"))
    if not world.options.shuffle_jumping_shoes:
        world.options.start_inventory.value["Jumping Shoes"] = 1
        world.multiworld.push_precollected(world.create_item("Jumping Shoes"))

def get_random_item(world: "PokemonFRLGWorld", item_classification: ItemClassification = None) -> str:
    if item_classification is None:
        item_classification = ItemClassification.useful if world.random.random() < 0.20 else ItemClassification.filler
    items = [item for item in data.items.values()
             if item.classification == item_classification and item.name not in item_groups["Unique Items"]]
    return world.random.choice(items).name

def update_renewable_to_progression(item: PokemonFRLGItem) -> None:
    if item.name in RENEWABLE_PROGRESSION_ITEMS:
        item.classification = ItemClassification.progression

def is_single_purchase_item(item: PokemonFRLGItem) -> bool:
    if (item.name in item_groups["Key Items"]
            or item.name in item_groups["Badges"]
            or item.name in item_groups["HMs"]
            or item.name in item_groups["Fly Unlocks"]):
        return True
    return False