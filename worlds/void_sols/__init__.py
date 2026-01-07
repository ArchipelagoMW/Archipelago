from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World

from .Options import VoidSolsOptions
from .Items import all_items, item_data_table, VoidSolsItem
from .Locations import all_locations, setup_locations
from .Regions import create_regions, connect_regions
from .Rules import set_rules
from .Names import ItemName

class VoidSolsWeb(WebWorld):
    theme = "party"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Void Sols"
        "for Archipelago on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Cookie966507"],
    )
    tutorials = [setup]


class VoidSolsWorld(World):
    """ Void Sols is a top-down, 2D, minimalist souls-like RPG."""

    game = "Void Sols"

    options = VoidSolsOptions
    options_dataclass = VoidSolsOptions
    
    item_name_to_id = all_items
    location_name_to_id = all_locations
    
    def create_item(self, name: str) -> VoidSolsItem:
        data = item_data_table[name]
        return VoidSolsItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        active_locations = setup_locations(self)
        create_regions(self, active_locations)
        connect_regions(self)

    def set_rules(self):
        set_rules(self)

    def create_items(self):
        # Handle Starting Weapon
        starting_weapon_option = self.options.starting_weapon.value
        
        weapon_map = {
            0: ItemName.sword,
            1: ItemName.dagger,
            2: ItemName.great_hammer,
            3: ItemName.pickaxe,
            4: ItemName.halberd,
            5: ItemName.katana,
            6: ItemName.gauntlets,
            7: ItemName.morningstar,
            8: ItemName.dual_handaxes,
            9: ItemName.scythe,
            10: ItemName.frying_pan,
        }

        if starting_weapon_option == 11: # Random
            starting_weapon_name = self.random.choice(list(weapon_map.values()))
        else:
            starting_weapon_name = weapon_map.get(starting_weapon_option)
        
        # Store the actual starting weapon ID for slot_data
        self.starting_weapon_id = next((k for k, v in weapon_map.items() if v == starting_weapon_name), 0)

        if starting_weapon_name:
            self.multiworld.push_precollected(self.create_item(starting_weapon_name))

        itempool = []
        for name, data in item_data_table.items():
            quantity = data.quantity
            
            # If this is the starting weapon, reduce quantity by 1
            if name == starting_weapon_name:
                quantity -= 1
            
            if data.classification != ItemClassification.filler:
                for _ in range(quantity):
                    itempool.append(self.create_item(name))

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        needed_fillers = total_locations - len(itempool)
        
        filler_items = [name for name, data in item_data_table.items() if data.classification == ItemClassification.filler]
        
        if needed_fillers > 0:
            for _ in range(needed_fillers):
                filler_name = self.random.choice(filler_items)
                itempool.append(self.create_item(filler_name))
        elif needed_fillers < 0:
            raise Exception(f"Too many items! {len(itempool)} items for {total_locations} locations.")

        self.multiworld.itempool += itempool

    def fill_slot_data(self) -> dict:
        return {
            "enemy_randomization": self.options.enemy_randomization.value,
            "starting_weapon": self.starting_weapon_id,
            "sparks_checks": self.options.sparks_checks.value,
            "torch_checks": self.options.torch_checks.value,
            "hidden_walls_checks": self.options.hidden_walls_checks.value,
        }
