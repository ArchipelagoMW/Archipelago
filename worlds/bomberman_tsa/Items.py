from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import BombTSAWorld


class BombTSAItem(Item):
    game = "Bomberman The Second Attack"


class BombTSAItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    num_exist: int = 1
    can_create: Callable[["BombTSAWorld"], bool] = lambda world: True
    item_type: Optional[str] = None
    fillweight: Optional[float] = None


item_data_table: Dict[str, BombTSAItemData] = {
    "Fire Stone": BombTSAItemData(
        code=0x1C30000,
        type=ItemClassification.progression,
        num_exist=0,
        item_type="Stone",
    ),
    "Ice Stone": BombTSAItemData(
        code=0x1C30001,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Stone",
		),
    "Wind Stone": BombTSAItemData(
        code=0x1C30002,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Stone",
		),
    "Earth Stone": BombTSAItemData(
        code=0x1C30003,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Stone",
		),
    "Lightning Stone": BombTSAItemData(
        code=0x1C30004,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Stone",
		),
    "Dark Stone": BombTSAItemData(
        code=0x1C30005,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Stone",
		),
    "Light Stone": BombTSAItemData(
        code=0x1C30006,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Stone",
		),
    "BombUp": BombTSAItemData(
        code=0x1C30007,
        type=ItemClassification.progression,
        num_exist= 3,
  		item_type= "Powerup",
		),
    "FireUp": BombTSAItemData(
        code=0x1C30008,
        type=ItemClassification.progression,
        num_exist= 2,
  		item_type= "Powerup",
		),
    "HealthUp": BombTSAItemData(
        code=0x1C30009,
        type=ItemClassification.useful,
        num_exist=5,
  		item_type= "Powerup",
		),
    "Guardian Glove": BombTSAItemData(
        code=0x1C3000A,
        type=ItemClassification.progression,
  		item_type= "Guardian",
		),
    "Guardian Boots": BombTSAItemData(
        code=0x1C3000B,
        type=ItemClassification.progression,
  		item_type= "Guardian",
		),
    "Guardian Helmet": BombTSAItemData(
        code=0x1C3000C,
        type=ItemClassification.progression,
  		item_type= "Guardian",
		),
    "Guardian Armor": BombTSAItemData(
        code=0x1C3000D,
        type=ItemClassification.useful,
  		item_type= "Guardian",
		),
    "Skates": BombTSAItemData(
        code=0x1C3000E,
        type=ItemClassification.progression,
  		item_type= "Powerup",
		),


    #"Alcatraz": BombTSAItemData(
    #    code=0x1C30010,
    #    type=ItemClassification.progression,
    #),
    "Aquanet Coordinates": BombTSAItemData(
        code=0x1C30011,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Coordinates",
		),
    "Horizon Coordinates": BombTSAItemData(
        code=0x1C30012,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Coordinates",
		),
    "Starlight Coordinates": BombTSAItemData(
        code=0x1C30013,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Coordinates",
		),
    "Neverland Coordinates": BombTSAItemData(
        code=0x1C30014,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Coordinates",
		),
    "Epikyur Coordinates": BombTSAItemData(
        code=0x1C30015,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Coordinates",
		),
    "Thantos Coordinates": BombTSAItemData(
        code=0x1C30016,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Coordinates",
		),
    "Noah Coordinates": BombTSAItemData(
        code=0x1C30017,
        type=ItemClassification.progression,
        num_exist= 0,
  		item_type= "Coordinates",
		),


    "Pommy Knuckle Gene": BombTSAItemData(
        code=0x1C30020,
        type=ItemClassification.progression,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Animal Gene": BombTSAItemData(
        code=0x1C30021,
        type=ItemClassification.progression,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Hammer Gene": BombTSAItemData(
        code=0x1C30022,
        type=ItemClassification.progression,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Claw Gene": BombTSAItemData(
        code=0x1C30023,
        type=ItemClassification.progression,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Penguin Gene": BombTSAItemData(
        code=0x1C30024,
        type=ItemClassification.progression,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Beast Gene": BombTSAItemData(
        code=0x1C30025,
        type=ItemClassification.progression,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Mage Gene": BombTSAItemData(
        code=0x1C30026,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Knight Gene": BombTSAItemData(
        code=0x1C30027,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Devil Gene": BombTSAItemData(
        code=0x1C30028,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Cat Gene": BombTSAItemData(
        code=0x1C30029,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Bird Gene": BombTSAItemData(
        code=0x1C3002A,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Chicken Gene": BombTSAItemData(
        code=0x1C3002B,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Dragon Gene": BombTSAItemData(
        code=0x1C3002C,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Dinosaur Gene": BombTSAItemData(
        code=0x1C3002D,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Pixie Gene": BombTSAItemData(
        code=0x1C3002E,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),
    "Pommy Shadow Gene": BombTSAItemData(
        code=0x1C3002F,
        type=ItemClassification.useful,
        num_exist= 0,
  		item_type= "Gene",
		),

    # Filler
    "200 Coins": BombTSAItemData(
        code=0x1C30030,
        type=ItemClassification.filler,
        num_exist=0,
  		item_type= "filler",
        fillweight = 0.4,
		),
    "Heart": BombTSAItemData(
        code=0x1C30031,
        type=ItemClassification.filler,
        num_exist=0,
  		item_type= "filler",
        fillweight = 0.8,
		),
    "Gold Heart": BombTSAItemData(
        code=0x1C30032,
        type=ItemClassification.filler,
        num_exist=0,
  		item_type= "filler",
        fillweight = 0.2,
		),

    # Traps
    "Stun Trap": BombTSAItemData(
        code=0x1C30040,
        type=ItemClassification.trap,
        num_exist=0,
  		item_type= "trap",
        fillweight = 0.3,
		),
    "Panic Bomb Trap": BombTSAItemData(
        code=0x1C30041,
        type=ItemClassification.trap,
        num_exist=0,
  		item_type= "trap",
        fillweight = 0.4,
		),
    "Fire Trap": BombTSAItemData(
        code=0x1C30042,
        type=ItemClassification.trap,
        num_exist=0,
  		item_type= "trap",
        fillweight = 0.3,
		),
    "Reverse Trap": BombTSAItemData(
        code=0x1C30043,
        type=ItemClassification.trap,
        num_exist=0,
  		item_type= "trap",
        fillweight = 0.4,
		),
    "Ejection Trap": BombTSAItemData(
        code=0x1C30044,
        type=ItemClassification.trap,
        num_exist=0,
  		item_type= "trap",
        fillweight = 0.0,
		),
    
    # Stage Key Items
    "Blue Gems": BombTSAItemData(
        code=0x1C30018,
        type=ItemClassification.progression,
  		item_type= "Event",
		),
    "Green Gems": BombTSAItemData(
        code=0x1C30019,
        type=ItemClassification.progression,
  		item_type= "Event",
		),
    "Red Gem": BombTSAItemData(
        code=0x1C3001A,
        type=ItemClassification.progression,
  		item_type= "Event",
		),

    "Royal Straight": BombTSAItemData(
        code=0x1C3001B,
        type=ItemClassification.progression,
  		item_type= "Event",
		),

    "Haunted House Pass": BombTSAItemData(
        code=0x1C3001C,
        type=ItemClassification.progression,
  		item_type= "Event",
		),
    "Museum Pass": BombTSAItemData(
        code=0x1C3001D,
        type=ItemClassification.progression,
  		item_type= "Event",
		),
    "Coaster Battery": BombTSAItemData(
        code=0x1C3001E,
        type=ItemClassification.progression,
  		item_type= "Event",
		),

    "Train Batteries": BombTSAItemData(
        code=0x1C3001F,
        type=ItemClassification.progression,
  		item_type= "Event",
		),
    "Warship key": BombTSAItemData(
        code=0x1C30050,
        type=ItemClassification.progression,
        num_exist= 0,
  		item_type= "Warship key",
		),


    #"Shop Coordinates": BombTSAItemData(
    #    code=0x1C30018,
    #    type=ItemClassification.progression,
    #),

    



    "Victory": BombTSAItemData(
        code=0x1CAEE12,
        type=ItemClassification.progression,
        num_exist=0,
  		item_type= "Goal",
		),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

pommy_shop_genes = [name for name,data in item_data_table.items() if data.item_type == "Gene"]
elemental_stones = [name for name,data in item_data_table.items() if data.item_type == "Stone"]
planet_coord_list = [name for name,data in item_data_table.items() if data.item_type == "Coordinates"]

item_filler = [name for name, data in item_data_table.items() if data.type == ItemClassification.filler and data.fillweight is not None]
item_filler_weight = [data.fillweight for name, data in item_data_table.items() if data.type == ItemClassification.filler and data.fillweight is not None]
trap_filler = [name for name, data in item_data_table.items() if data.type == ItemClassification.trap and data.fillweight is not None]
trap_filler_weight = [data.fillweight for name, data in item_data_table.items() if data.type == ItemClassification.trap and data.fillweight is not None]