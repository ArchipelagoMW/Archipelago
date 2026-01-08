from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World

from .Options import VoidSolsOptions
from .Items import all_items, item_data_table, VoidSolsItem
from .Locations import all_locations, setup_locations
from .Regions import create_regions, connect_regions
from .Rules import set_rules
from .Names import ItemName, LocationName

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

        # Place Victory Item
        self.multiworld.get_location(LocationName.apex_world_spark_interacted, self.player).place_locked_item(
            self.create_item(ItemName.victory))

        # Place Boss Event Items
        boss_events = {
            LocationName.prison_warden_defeated_event: ItemName.prison_warden_defeated_event,
            LocationName.forest_poacher_defeated_event: ItemName.forest_poacher_defeated_event,
            LocationName.mountain_groundskeeper_defeated_event: ItemName.mountain_groundskeeper_defeated_event,
            LocationName.mines_worm_defeated_event: ItemName.greater_void_worm_defeated_event,
            LocationName.cultist_amalgamate_defeated_event: ItemName.cultist_amalgamate_defeated_event,
            LocationName.supermax_prison_infernal_warden_defeated_event: ItemName.supermax_prison_infernal_warden_defeated_event,
            LocationName.factory_immaculate_defeated_event: ItemName.factory_immaculate_defeated_event,
            LocationName.apex_gatekeeper_defeated_event: ItemName.apex_gatekeeper_defeated_event,
            LocationName.apex_zenith_defeated_event: ItemName.apex_zenith_defeated_event,
        }

        for loc_name, item_name in boss_events.items():
            self.multiworld.get_location(loc_name, self.player).place_locked_item(self.create_item(item_name))

        itempool = []
        for name, data in item_data_table.items():
            quantity = data.quantity
            
            # If this is the starting weapon, reduce quantity by 1
            if name == starting_weapon_name:
                quantity -= 1
            
            # Skip Victory as it is placed manually
            if name == ItemName.victory:
                continue

            if data.code is not None and quantity > 0:
                for _ in range(quantity):
                    itempool.append(self.create_item(name))

        # Filter out filled locations and event locations
        unfilled_locations = [loc for loc in self.multiworld.get_unfilled_locations(self.player) 
                              if loc.item is None and loc.address is not None]
        
        total_locations = len(unfilled_locations)
        needed_fillers = total_locations - len(itempool)
        
        sols_items = [
            ItemName.sols_1,
            ItemName.sols_25,
            ItemName.sols_50,
            ItemName.sols_100,
            ItemName.sols_250,
        ]
        
        if needed_fillers > 0:
            for _ in range(needed_fillers):
                filler_name = self.random.choice(sols_items)
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
            "death_link": self.options.death_link.value,
        }
