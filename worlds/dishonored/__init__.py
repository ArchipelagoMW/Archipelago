from worlds.AutoWorld import World
from BaseClasses import Item, Location, Region, ItemClassification

class DishonoredItem(Item):
    game = "Dishonored"

class DishonoredLocation(Location):
    game = "Dishonored"

class DishonoredWorld(World):
    game = "Dishonored"
    topology_present = False

    item_name_to_id = {"Rune de Test": 990001}
    location_name_to_id = {"Coffre de Test": 990001}

    def create_locations(self):
        # On crée un emplacement virtuel que le client devra valider
        self.multiworld.get_location("Ramasser 100 pièces", self.player).place_locked_item(...)

    def create_regions(self):
        # 1. Création des zones
        menu = Region("Menu", self.player, self.multiworld)
        main_zone = Region("Zone Principale", self.player, self.multiworld)
        
        # 2. Emplacement de test
        loc = DishonoredLocation(self.player, "Coffre de Test", 990001, main_zone)
        main_zone.locations.append(loc)
        
        menu.connect(main_zone)
        self.multiworld.regions.append(menu)
        self.multiworld.regions.append(main_zone)

    def create_items(self):
        # 3. Objet de test placé sur l'emplacement
        item = DishonoredItem("Rune de Test", ItemClassification.progression, 990001, self.player)
        self.multiworld.get_location("Coffre de Test", self.player).place_locked_item(item)