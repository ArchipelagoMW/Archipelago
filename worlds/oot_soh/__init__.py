from typing import List, Dict, Any

from BaseClasses import CollectionState, Item, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import SohItem, item_data_table, item_table, filler_items
from .Locations import SohLocation, base_location_table, \
    gold_skulltula_overworld_location_table, \
    gold_skulltula_dungeon_location_table, \
    shops_location_table, \
    scrubs_location_table, \
    trade_items_location_table, \
    merchants_items_location_table, \
    cows_location_table, \
    frogs_location_table, \
    beehives_location_table, \
    pots_overworld_location_table, \
    pots_dungeon_location_table, \
    crates_overworld_location_table, \
    crates_dungeon_location_table, \
    freestanding_overworld_location_table, \
    freestanding_dungeon_location_table, \
    fairies_location_table, \
    grass_overworld_location_table, \
    grass_dungeon_location_table, \
    fish_pond_location_table, \
    fish_overworld_location_table, \
    location_table
from .Options import SohOptions
from .Regions import region_data_table, reset_age_access, update_age_access
from .Rules import get_soh_rule
from .Enums import *
from .dodongos_cavern import create_dc_regions_and_rules, set_location_rules_dc


class SohWebWorld(WebWorld):
    theme = "ice"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Ship of Harkinian.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["aMannus"]
    )
    
    tutorials = [setup_en]
    game_info_languages = ["en"]


class SohWorld(World):
    """A PC Port of Ocarina of Time"""

    game = "Ship of Harkinian"
    web = SohWebWorld()
    options: SohOptions
    options_dataclass = SohOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> SohItem:
        return SohItem(name, item_data_table[name].type, item_data_table[name].item_id, self.player)

    def create_items(self) -> None:
        item_pool: List[SohItem] = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}

        # Add Ganon's Castle Boss Key when shuffled anywhere.
        if self.options.gcbk_setting == "anywhere":
            items_to_create[GANONS_CASTLE_BOSS_KEY] = 1

        # Add dungeon rewards when shuffled
        if self.options.shuffle_dungeon_rewards == "anywhere":
            items_to_create[KOKIRIS_EMERALD] = 1
            items_to_create[GORONS_RUBY] = 1
            items_to_create[ZORAS_SAPPHIRE] = 1
            items_to_create[FOREST_MEDALLION] = 1
            items_to_create[FIRE_MEDALLION] = 1
            items_to_create[WATER_MEDALLION] = 1
            items_to_create[SPIRIT_MEDALLION] = 1
            items_to_create[SHADOW_MEDALLION] = 1
            items_to_create[LIGHT_MEDALLION] = 1

        # Add overworld tokens when shuffled
        if self.options.shuffle_tokens == "overworld" or self.options.shuffle_tokens == "all":
            items_to_create[GOLD_SKULLTULA_TOKEN] += 56

        # Add dungeon tokens when shuffled
        if self.options.shuffle_tokens == "dungeon" or self.options.shuffle_tokens == "all":
            items_to_create[GOLD_SKULLTULA_TOKEN] += 44

        if self.options.shuffle_trade_items:
            items_to_create[POCKET_EGG] = 1
            items_to_create[COJIRO] = 1
            items_to_create[ODD_MUSHROOM] = 1
            items_to_create[ODD_POTION] = 1
            items_to_create[POACHERS_SAW] = 1
            items_to_create[BROKEN_GORONS_SWORD] = 1
            items_to_create[PRESCRIPTION] = 1
            items_to_create[EYEBALL_FROG] = 1
            items_to_create[WORLDS_FINEST_EYEDROPS] = 1

        if self.options.shuffle_merchants:
            items_to_create[GIANTS_KNIFE] = 1
            items_to_create[MAGIC_BEAN_PACK] = 1

        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                item_pool.append(self.create_item(item))

        filler_item_count: int = len(self.multiworld.get_unfilled_locations()) - len(item_pool)
        item_pool += [self.create_item(self.get_filler_item_name()) for _ in range(filler_item_count)]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None: 

        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # todo: maybe easier to have region and rule making functions instead
        create_dc_regions_and_rules(self)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)

            # Base locations
            region.add_locations({
                location_name: location_data.address for location_name, location_data in base_location_table.items()
                if location_data.region == region_name
            }, SohLocation)

            # Gold Skulltulas (Overworld)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in gold_skulltula_overworld_location_table.items()
                if location_data.region == region_name
            }, SohLocation)

            # Gold Skulltulas (Dungeon)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in gold_skulltula_dungeon_location_table.items()
                if location_data.region == region_name
            }, SohLocation)

            # Shops
            if self.options.shuffle_shops:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in shops_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Scrubs
            if self.options.shuffle_scrubs:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in scrubs_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Trade Items
            if self.options.shuffle_trade_items:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in trade_items_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Merchants
            if self.options.shuffle_merchants:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in merchants_items_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Cows
            if self.options.shuffle_cows:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in cows_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Frogs
            if self.options.shuffle_frogs:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in frogs_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Beehives
            if self.options.shuffle_beehives:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in beehives_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Pots (Overworld)
            if self.options.shuffle_pots == "overworld" or self.options.shuffle_pots == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in pots_overworld_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Pots (Dungeon)
            if self.options.shuffle_pots == "dungeon" or self.options.shuffle_pots == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in pots_dungeon_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Crates (Overworld)
            if self.options.shuffle_crates == "overworld" or self.options.shuffle_crates == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in crates_overworld_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Crates (Dungeon)
            if self.options.shuffle_crates == "dungeon" or self.options.shuffle_crates == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in crates_dungeon_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Freestanding (Overworld)
            if self.options.shuffle_freestanding == "overworld" or self.options.shuffle_freestanding == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in freestanding_overworld_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Freestanding (Dungeon)
            if self.options.shuffle_freestanding == "dungeon" or self.options.shuffle_freestanding == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in freestanding_dungeon_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Fairies
            if self.options.shuffle_fairies:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in fairies_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Grass (Overworld)
            if self.options.shuffle_grass == "overworld" or self.options.shuffle_grass == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in grass_overworld_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Grass (Dungeon)
            if self.options.shuffle_grass == "dungeon" or self.options.shuffle_grass == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in grass_dungeon_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Fish (Pond)
            if self.options.shuffle_fish == "pond" or self.options.shuffle_fish == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in fish_pond_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Fish (Overworld)
            if self.options.shuffle_fish == "overworld" or self.options.shuffle_fish == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in fish_overworld_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)
                
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Keep Weird Egg and Zelda's Letter in their vanilla location until we add shuffles for them
        # Entirely disabled for now because we're forcing on Skip Child Zelda
        #self.get_location("HC Malon Egg").place_locked_item(self.create_item("Weird Egg"))
        #self.get_location("HC Zeldas Letter").place_locked_item(self.create_item("Zelda's Letter"))

        # Create a dictionary mapping blue warp rewards to their vanilla items
        dungeon_reward_item_mapping = {
            "Queen Gohma": "Kokiri's Emerald",
            "King Dodongo": "Goron's Ruby",
            "Barinade": "Zora's Sapphire",
            "Phantom Ganon": "Forest Medallion",
            "Volvagia": "Fire Medallion",
            "Morpha": "Water Medallion",
            "Bongo Bongo": "Spirit Medallion",
            "Twinrova": "Shadow Medallion",
            "Link's Pocket": "Light Medallion"
        }

        # Preplace dungeon rewards in vanilla locations when not shuffled
        if self.options.shuffle_dungeon_rewards == "off":      
            # Loop through dungeons rewards and set their items to the vanilla reward.      
            for location_name, reward_name in zip(dungeon_reward_item_mapping.keys(), dungeon_reward_item_mapping.values()):
                self.get_location(location_name).place_locked_item(self.create_item(reward_name))        

        if self.options.shuffle_dungeon_rewards == "dungeons": 
            # Extract and shuffle just the item names from location_item_mapping
            reward_names = list(dungeon_reward_item_mapping.values())
            self.random.shuffle(reward_names)
            
            # Pair each location with a unique shuffled dungeon reward
            for location_name, reward_name in zip(dungeon_reward_item_mapping.keys(), reward_names):
                self.get_location(location_name).place_locked_item(self.create_item(reward_name))

        # Place Ganons Boss Key to the Light Arrow Cutscene when set to needing specific requirements
        if self.options.gcbk_setting == "dungeon_rewards":
            self.get_location("Market ToT Light Arrow Cutscene").place_locked_item(self.create_item("Ganon's Castle Boss Key"))

        # Preplace tokens based on settings.
        if self.options.shuffle_tokens == "off" or self.options.shuffle_tokens == "dungeon":
            token_item = self.create_item("Gold Skulltula Token")
            for location_name, location_data in gold_skulltula_overworld_location_table.items():
                self.get_location(location_name).place_locked_item(token_item)

        if self.options.shuffle_tokens == "off" or self.options.shuffle_tokens == "overworld":
            token_item = self.create_item("Gold Skulltula Token")
            for location_name, location_data in gold_skulltula_dungeon_location_table.items():
                self.get_location(location_name).place_locked_item(token_item)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def set_rules(self) -> None:
        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: True

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "shuffle_dungeon_rewards": self.options.shuffle_dungeon_rewards.value,
            "gcbk_setting": self.options.gcbk_setting.value,
            "gcbk_rewards_required": self.options.gcbk_rewards_required.value,
            "shuffle_tokens": self.options.shuffle_tokens.value,
            "shuffle_shops": self.options.shuffle_shops.value,
            "shuffle_scrubs": self.options.shuffle_scrubs.value,
            "shuffle_trade_items": self.options.shuffle_trade_items.value,
            "shuffle_merchants": self.options.shuffle_merchants.value,
            "shuffle_cows": self.options.shuffle_cows.value,
            "shuffle_frogs": self.options.shuffle_frogs.value,
            "shuffle_beehives": self.options.shuffle_beehives.value,
            "shuffle_pots": self.options.shuffle_pots.value,
            "shuffle_crates": self.options.shuffle_crates.value,
            "shuffle_freestanding": self.options.shuffle_freestanding.value,
            "shuffle_fairies": self.options.shuffle_fairies.value,
            "shuffle_grass": self.options.shuffle_grass.value,
            "shuffle_fish": self.options.shuffle_fish.value,
        }
    
    def collect(self, state: CollectionState, item: Item) -> bool:
        update_age_access(self, state)
        return super().collect(state, item)
    
    def remove(self, state: CollectionState, item: Item) -> bool:
        reset_age_access() #TODO pass the starting age option 
        update_age_access(self, state)
        return super().remove(state, item)