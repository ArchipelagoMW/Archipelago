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
        return SohItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[SohItem] = []

        # Add Base Progression Items
        item_pool.append(self.create_item("Kokiri Sword"))
        item_pool.append(self.create_item("Biggoron's Sword"))
        item_pool.append(self.create_item("Deku Shield"))
        item_pool.append(self.create_item("Hylian Shield"))
        item_pool.append(self.create_item("Mirror Shield"))
        item_pool.append(self.create_item("Goron Tunic"))
        item_pool.append(self.create_item("Zora Tunic"))
        item_pool.append(self.create_item("Iron Boots"))
        item_pool.append(self.create_item("Hover Boots"))
        item_pool.append(self.create_item("Boomerang"))
        item_pool.append(self.create_item("Lens of Truth"))
        item_pool.append(self.create_item("Megaton Hammer"))
        item_pool.append(self.create_item("Stone of Agony"))
        item_pool.append(self.create_item("Din's Fire"))
        item_pool.append(self.create_item("Farore's Wind"))
        item_pool.append(self.create_item("Nayru's Love"))
        item_pool.append(self.create_item("Fire Arrow"))
        item_pool.append(self.create_item("Ice Arrow"))
        item_pool.append(self.create_item("Light Arrow"))
        item_pool.append(self.create_item("Gerudo Membership Card"))
        item_pool.append(self.create_item("Double Defense"))
        item_pool.append(self.create_item("Claim Check"))
        for i in range(2): item_pool.append(self.create_item("Progressive Hookshot"))
        for i in range(3): item_pool.append(self.create_item("Strength Upgrade"))
        for i in range(3): item_pool.append(self.create_item("Progressive Bomb Bag"))
        for i in range(3): item_pool.append(self.create_item("Progressive Bow"))
        for i in range(3): item_pool.append(self.create_item("Progressive Slingshot"))
        for i in range(3): item_pool.append(self.create_item("Progressive Wallet"))
        for i in range(2): item_pool.append(self.create_item("Progressive Scale"))
        for i in range(2): item_pool.append(self.create_item("Progressive Nut Capacity"))
        for i in range(2): item_pool.append(self.create_item("Progressive Stick Capacity"))
        for i in range(6): item_pool.append(self.create_item("Progressive Bombchu"))
        for i in range(2): item_pool.append(self.create_item("Progressive Magic Meter"))
        for i in range(2): item_pool.append(self.create_item("Progressive Ocarina"))
        item_pool.append(self.create_item("Empty Bottle"))
        item_pool.append(self.create_item("Bottle with Ruto's Letter"))
        item_pool.append(self.create_item("Bottle with Big Poe"))
        item_pool.append(self.create_item("Bottle with Bugs"))
        item_pool.append(self.create_item("Zelda's Lullaby"))
        item_pool.append(self.create_item("Epona's Song"))
        item_pool.append(self.create_item("Saria's Song"))
        item_pool.append(self.create_item("Sun's Song"))
        item_pool.append(self.create_item("Song of Time"))
        item_pool.append(self.create_item("Song of Storms"))
        item_pool.append(self.create_item("Minuet of Forest"))
        item_pool.append(self.create_item("Bolero of Fire"))
        item_pool.append(self.create_item("Serenade of Water"))
        item_pool.append(self.create_item("Requiem of Spirit"))
        item_pool.append(self.create_item("Nocturne of Shadow"))
        item_pool.append(self.create_item("Prelude of Light"))
        item_pool.append(self.create_item("Great Deku Tree Map"))
        item_pool.append(self.create_item("Dodongo's Cavern Map"))
        item_pool.append(self.create_item("Jabu-Jabu's Belly Map"))
        item_pool.append(self.create_item("Forest Temple Map"))
        item_pool.append(self.create_item("Fire Temple Map"))
        item_pool.append(self.create_item("Water Temple Map"))
        item_pool.append(self.create_item("Spirit Temple Map"))
        item_pool.append(self.create_item("Shadow Temple Map"))
        item_pool.append(self.create_item("Bottom of the Well Map"))
        item_pool.append(self.create_item("Ice Cavern Map"))
        item_pool.append(self.create_item("Great Deku Tree Compass"))
        item_pool.append(self.create_item("Dodongo's Cavern Compass"))
        item_pool.append(self.create_item("Jabu-Jabu's Belly Compass"))
        item_pool.append(self.create_item("Forest Temple Compass"))
        item_pool.append(self.create_item("Fire Temple Compass"))
        item_pool.append(self.create_item("Water Temple Compass"))
        item_pool.append(self.create_item("Spirit Temple Compass"))
        item_pool.append(self.create_item("Shadow Temple Compass"))
        item_pool.append(self.create_item("Bottom of the Well Compass"))
        item_pool.append(self.create_item("Ice Cavern Compass"))
        item_pool.append(self.create_item("Forest Temple Boss Key"))
        item_pool.append(self.create_item("Fire Temple Boss Key"))
        item_pool.append(self.create_item("Water Temple Boss Key"))
        item_pool.append(self.create_item("Spirit Temple Boss Key"))
        item_pool.append(self.create_item("Shadow Temple Boss Key"))
        for i in range(5): item_pool.append(self.create_item("Forest Temple Small Key"))
        for i in range(8): item_pool.append(self.create_item("Fire Temple Small Key"))
        for i in range(6): item_pool.append(self.create_item("Water Temple Small Key"))
        for i in range(5): item_pool.append(self.create_item("Spirit Temple Small Key"))
        for i in range(5): item_pool.append(self.create_item("Shadow Temple Small Key"))
        for i in range(3): item_pool.append(self.create_item("Bottom of the Well Small Key"))
        for i in range(9): item_pool.append(self.create_item("Training Ground Small Key"))
        for i in range(2): item_pool.append(self.create_item("Ganon's Castle Small Key"))
        item_pool.append(self.create_item("Greg the Green Rupee"))
        for i in range(35): item_pool.append(self.create_item("Piece of Heart"))
        item_pool.append(self.create_item("Piece of Heart (WINNER)"))
        for i in range(8): item_pool.append(self.create_item("Heart Container"))
        for i in range(6): item_pool.append(self.create_item("Ice Trap"))

        # Add Ganon's Castle Boss Key when shuffled anywhere.
        if self.options.gcbk_setting == "anywhere":
            item_pool.append(self.create_item("Ganon's Castle Boss Key"))

        # Add dungeon rewards when shuffled
        if self.options.shuffle_dungeon_rewards == "anywhere":
            item_pool.append(self.create_item("Kokiri's Emerald"))
            item_pool.append(self.create_item("Goron's Ruby"))
            item_pool.append(self.create_item("Zora's Sapphire"))
            item_pool.append(self.create_item("Forest Medallion"))
            item_pool.append(self.create_item("Fire Medallion"))
            item_pool.append(self.create_item("Water Medallion"))
            item_pool.append(self.create_item("Spirit Medallion"))
            item_pool.append(self.create_item("Shadow Medallion"))
            item_pool.append(self.create_item("Light Medallion"))

        # Add overworld tokens when shuffled
        if self.options.shuffle_tokens == "overworld" or self.options.shuffle_tokens == "all":
            for i in range(56): item_pool.append(self.create_item("Gold Skulltula Token"))

        # Add dungeon tokens when shuffled
        if self.options.shuffle_tokens == "dungeon" or self.options.shuffle_tokens == "all":
            for i in range(44): item_pool.append(self.create_item("Gold Skulltula Token"))

        if self.options.shuffle_trade_items:
            item_pool.append(self.create_item("Pocket Egg"))
            item_pool.append(self.create_item("Cojiro"))
            item_pool.append(self.create_item("Odd Mushroom"))
            item_pool.append(self.create_item("Odd Potion"))
            item_pool.append(self.create_item("Poacher's Saw"))
            item_pool.append(self.create_item("Broken Goron's Sword"))
            item_pool.append(self.create_item("Prescription"))
            item_pool.append(self.create_item("Eyeball Frog"))
            item_pool.append(self.create_item("World's Finest Eyedrops"))

        if self.options.shuffle_merchants:
            item_pool.append(self.create_item("Giant's Knife"))
            item_pool.append(self.create_item("Magic Bean Pack"))

        filler_item_count: int = len(self.multiworld.get_unfilled_locations()) - len(item_pool)
        item_pool += [self.create_item(self.get_filler_item_name()) for _ in range(filler_item_count)]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None: 

        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

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