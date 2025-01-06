from typing import ClassVar, Dict, Any, Type
from BaseClasses import Region, Location, Item, Tutorial
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .Items import items, base_id
from .Locations import locations
from .Rules import create_rules
from .Options import CatQuestOptions

class CatQuestWeb(WebWorld):
    theme = "grassFlowers"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Cat Quest randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Nikkilite"]
    )]

class CatQuestWorld(World):
    """
    Cat Quest is a small open world ARPG set in a cute world full of cats and cat puns. 
    Slash and dodge enemies while completing quests, dungeons and obtaining new gear.
    """

    game = "Cat Quest"
    web = CatQuestWeb()
    data_version = 1

    item_name_to_id = {item["name"]: item["id"] for item in items}
    location_name_to_id = {loc["name"]: loc["id"] for loc in locations}
    
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = CatQuestOptions
    options: CatQuestOptions

    required_client_version = (0, 4, 0)

    def __init__(self, multiworld, player):
        super(CatQuestWorld, self).__init__(multiworld, player)

    def get_filler_item_name(self) -> str:
        return "500 Exp"

    def create_item(self, name: str) -> "CatQuestItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id - 1

        return CatQuestItem(name, items[id]["classification"], item_id, player=self.player)

    def create_items(self) -> None:
        for item in items:
            count = item["count"]
            
            if count <= 0:
                continue
            else:
                for i in range(count):
                    self.multiworld.itempool.append(self.create_item(item["name"]))

        junk = 45
        self.multiworld.itempool += [self.create_item(self.get_filler_item_name()) for _ in range(junk)]

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        
        main_region = Region("Felingard", self.player, self.multiworld)

        for loc in self.location_name_to_id.keys():
            main_region.locations.append(CatQuestLocation(self.player, loc, self.location_name_to_id[loc], main_region))

        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)

        self.multiworld.completion_condition[self.player] = lambda state: (state.has("Royal Art of Water Walking", self.player) and state.has("Royal Art of Flight", self.player))


    def set_rules(self):
        create_rules(self, locations)

    def fill_slot_data(self) -> Dict[str, Any]:
        options = self.options

        settings = {
            "goal": int(options.goal),
        }
    
        slot_data = {
            "settings": settings,
        }
    
        return slot_data

class CatQuestItem(Item):
    game: str = "Cat Quest"

class CatQuestLocation(Location):
    game: str = "Cat Quest"