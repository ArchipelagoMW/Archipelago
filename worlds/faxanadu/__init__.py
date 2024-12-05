from typing import Any, Dict, List

from BaseClasses import Item, Location, Tutorial, ItemClassification, MultiWorld
from worlds.AutoWorld import WebWorld, World
from . import Items, Locations, Regions, Rules
from .Options import FaxanaduOptions
from worlds.generic.Rules import set_rule


DAXANADU_VERSION = "0.3.0"


class FaxanaduLocation(Location):
    game: str = "Faxanadu"


class FaxanaduItem(Item):
    game: str = "Faxanadu"


class FaxanaduWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Faxanadu randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Daivuk"]
    )]
    theme = "dirt"


class FaxanaduWorld(World):
    """
    Faxanadu is an action role-playing platform video game developed by Hudson Soft for the Nintendo Entertainment System
    """
    options_dataclass = FaxanaduOptions
    options: FaxanaduOptions
    game = "Faxanadu"
    web = FaxanaduWeb()

    item_name_to_id = {item.name: item.id for item in Items.items if item.id is not None}
    item_name_to_item = {item.name: item for item in Items.items}
    location_name_to_id = {loc.name: loc.id for loc in Locations.locations if loc.id is not None}

    def __init__(self, world: MultiWorld, player: int):
        self.filler_ratios: Dict[str, int] = {}
        
        super().__init__(world, player)

    def create_regions(self):
        Regions.create_regions(self)

        # Add locations into regions
        for region in self.multiworld.get_regions(self.player):
            for loc in [location for location in Locations.locations if location.region == region.name]:
                location = FaxanaduLocation(self.player, loc.name, loc.id, region)

                # In Faxanadu, Poison hurts you when picked up. It makes no sense to sell them in shops
                if loc.type == Locations.LocationType.shop:
                    location.item_rule = lambda item, player=self.player: not (player == item.player and item.name == "Poison")
                
                region.locations.append(location)

    def set_rules(self):
        Rules.set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Killed Evil One", self.player)

    def create_item(self, name: str) -> FaxanaduItem:
        item: Items.ItemDef = self.item_name_to_item[name]
        return FaxanaduItem(name, item.classification, item.id, self.player)

    # Returns how many red potions were prefilled into shops
    def prefill_shop_red_potions(self) -> int:
        red_potion_in_shop_count = 0
        if self.options.keep_shop_red_potions:
            red_potion_item = self.item_name_to_item["Red Potion"]
            red_potion_shop_locations = [
                loc
                for loc in Locations.locations
                if loc.type == Locations.LocationType.shop and loc.original_item == Locations.ItemType.red_potion
            ]
            for loc in red_potion_shop_locations:
                location = self.get_location(loc.name)
                location.place_locked_item(FaxanaduItem(red_potion_item.name, red_potion_item.classification, red_potion_item.id, self.player))
                red_potion_in_shop_count += 1
        return red_potion_in_shop_count

    def put_wingboot_in_shop(self, shops, region_name):
        item = self.item_name_to_item["Wingboots"]
        shop = shops.pop(region_name)
        slot = self.random.randint(0, len(shop) - 1)
        loc = shop[slot]
        location = self.get_location(loc.name)
        location.place_locked_item(FaxanaduItem(item.name, item.classification, item.id, self.player))

        # Put a rule right away that we need to have to unlocked.
        set_rule(location, lambda state: state.has("Unlock Wingboots", self.player))

    # Returns how many wingboots were prefilled into shops
    def prefill_shop_wingboots(self) -> int:
        # Collect shops
        shops: Dict[str, List[Locations.LocationDef]] = {}
        for loc in Locations.locations:
            if loc.type == Locations.LocationType.shop:
                if self.options.keep_shop_red_potions and loc.original_item == Locations.ItemType.red_potion:
                    continue # Don't override our red potions
                shops.setdefault(loc.region, []).append(loc)
        
        shop_count = len(shops)
        wingboots_count = round(shop_count / 2.5) # On 10 shops, we should have about 4 shops with wingboots

        # At least one should be in the first 4 shops. Because we require wingboots to progress past that point.
        must_have_regions = [region for i, region in enumerate(shops) if i < 4]
        self.put_wingboot_in_shop(shops, self.random.choice(must_have_regions))

        # Fill in the rest randomly in remaining shops
        for i in range(wingboots_count - 1): # -1 because we added one already
            region = self.random.choice(list(shops.keys()))
            self.put_wingboot_in_shop(shops, region)

        return wingboots_count

    def create_items(self) -> None:
        itempool: List[FaxanaduItem] = []

        # Prefill red potions in shops if option is set
        red_potion_in_shop_count = self.prefill_shop_red_potions()

        # Prefill wingboots in shops
        wingboots_in_shop_count = self.prefill_shop_wingboots()

        # Create the item pool, excluding fillers.
        prefilled_count = red_potion_in_shop_count + wingboots_in_shop_count
        for item in Items.items:
            # Ignore pendant if turned off
            if item.name == "Pendant" and not self.options.include_pendant:
                continue

            # ignore fillers for now, we will fill them later
            if item.classification in [ItemClassification.filler, ItemClassification.trap] and \
               item.progression_count == 0:
                continue

            prefill_loc = None
            if item.prefill_location:
                prefill_loc = self.get_location(item.prefill_location)

            # if require dragon slayer is turned on, we need progressive shields to be progression
            item_classification = item.classification
            if self.options.require_dragon_slayer and item.name == "Progressive Shield":
                item_classification = ItemClassification.progression

            if prefill_loc:
                prefill_loc.place_locked_item(FaxanaduItem(item.name, item_classification, item.id, self.player))
                prefilled_count += 1
            else:
                for i in range(item.count - item.progression_count):
                    itempool.append(FaxanaduItem(item.name, item_classification, item.id, self.player))
                for i in range(item.progression_count):
                    itempool.append(FaxanaduItem(item.name, ItemClassification.progression, item.id, self.player))

        # Set up filler ratios
        self.filler_ratios = {
            item.name: item.count
            for item in Items.items
            if item.classification in [ItemClassification.filler, ItemClassification.trap]
        }

        # If red potions are locked in shops, remove the count from the ratio.
        self.filler_ratios["Red Potion"] -= red_potion_in_shop_count

        # Remove poisons if not desired
        if not self.options.include_poisons:
            self.filler_ratios["Poison"] = 0

        # Randomly add fillers to the pool with ratios based on og game occurrence counts.
        filler_count = len(Locations.locations) - len(itempool) - prefilled_count
        for i in range(filler_count):
            itempool.append(self.create_item(self.get_filler_item_name()))
                
        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(self.filler_ratios.keys()), weights=list(self.filler_ratios.values()))[0]
    
    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict("keep_shop_red_potions", "random_musics", "random_sounds", "random_npcs", "random_monsters", "random_rewards")
        slot_data["daxanadu_version"] = DAXANADU_VERSION
        return slot_data
