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

    def generate_early(self) -> None:
        input("\033[33m WARNING: Ship of Harkinian currently only supports NO LOGIC! If you're OK with this, press Enter to continue. \033[0m")

    def create_item(self, name: str) -> SohItem:
        return SohItem(name, item_data_table[name].classification, item_data_table[name].item_id, self.player)

    def create_items(self) -> None:
        item_pool: List[SohItem] = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_data_table.items()}

        # Add Ganon's Castle Boss Key when shuffled anywhere.
        if self.options.ganons_castle_boss_key == "anywhere":
            items_to_create[Items.GANONS_CASTLE_BOSS_KEY.value] = 1

        # Add dungeon rewards when shuffled
        if self.options.shuffle_dungeon_rewards == "anywhere":
            items_to_create[Items.KOKIRIS_EMERALD.value] = 1
            items_to_create[Items.GORONS_RUBY.value] = 1
            items_to_create[Items.ZORAS_SAPPHIRE.value] = 1
            items_to_create[Items.FOREST_MEDALLION.value] = 1
            items_to_create[Items.FIRE_MEDALLION.value] = 1
            items_to_create[Items.WATER_MEDALLION.value] = 1
            items_to_create[Items.SPIRIT_MEDALLION.value] = 1
            items_to_create[Items.SHADOW_MEDALLION.value] = 1
            items_to_create[Items.LIGHT_MEDALLION.value] = 1

        # Add overworld tokens when shuffled
        if self.options.shuffle_tokens == "overworld" or self.options.shuffle_tokens == "all":
            items_to_create[Items.GOLD_SKULLTULA_TOKEN.value] += 56

        # Add dungeon tokens when shuffled
        if self.options.shuffle_tokens == "dungeon" or self.options.shuffle_tokens == "all":
            items_to_create[Items.GOLD_SKULLTULA_TOKEN.value] += 44

        if self.options.shuffle_adult_trade_items:
            items_to_create[Items.POCKET_EGG.value] = 1
            items_to_create[Items.COJIRO.value] = 1
            items_to_create[Items.ODD_MUSHROOM.value] = 1
            items_to_create[Items.ODD_POTION.value] = 1
            items_to_create[Items.POACHERS_SAW.value] = 1
            items_to_create[Items.BROKEN_GORONS_SWORD.value] = 1
            items_to_create[Items.PRESCRIPTION.value] = 1
            items_to_create[Items.EYEBALL_FROG.value] = 1
            items_to_create[Items.WORLDS_FINEST_EYEDROPS.value] = 1

        if self.options.shuffle_merchants:
            items_to_create[Items.GIANTS_KNIFE.value] = 1
            items_to_create[Items.MAGIC_BEAN_PACK.value] = 1

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
            if self.options.shuffle_adult_trade_items:
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
            if self.options.shuffle_frog_song_rupees:
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
            if self.options.shuffle_freestanding_items == "overworld" or self.options.shuffle_freestanding_items == "all":
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in freestanding_overworld_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)

            # Freestanding (Dungeon)
            if self.options.shuffle_freestanding_items == "dungeon" or self.options.shuffle_freestanding_items == "all":
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
        #self.get_location("HC Malon Egg").place_locked_item(self.create_item(WEIRD_EGG))
        #self.get_location("HC Zeldas Letter").place_locked_item(self.create_item(ZELDAS_LETTER))

        # Place Master Sword on vanilla location
        # TODO Implement MS shuffle option
        self.get_location(Locations.MARKET_TOT_MASTER_SWORD.value).place_locked_item(self.create_item(Items.MASTER_SWORD.value))

        self.get_location(Locations.GCSHOP_ITEM1.value).place_locked_item(self.create_item(Items.BUY_GORON_TUNIC.value))

        # Create a dictionary mapping blue warp rewards to their vanilla items
        dungeon_reward_item_mapping = {
            Locations.QUEEN_GOHMA.value: Items.KOKIRIS_EMERALD.value,
            Locations.KING_DODONGO.value: Items.GORONS_RUBY.value,
            Locations.BARINADE.value: Items.ZORAS_SAPPHIRE.value,
            Locations.PHANTOM_GANON.value: Items.FOREST_MEDALLION.value,
            Locations.VOLVAGIA.value: Items.FIRE_MEDALLION.value,
            Locations.MORPHA.value: Items.WATER_MEDALLION.value,
            Locations.BONGO_BONGO.value: Items.SPIRIT_MEDALLION.value,
            Locations.TWINROVA.value: Items.SHADOW_MEDALLION.value,
            Locations.LINKS_POCKET.value: Items.LIGHT_MEDALLION.value
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
        if self.options.ganons_castle_boss_key == "dungeon_rewards":
            self.get_location(Locations.MARKET_TOT_LIGHT_ARROW_CUTSCENE.value).place_locked_item(self.create_item(Items.GANONS_CASTLE_BOSS_KEY.value))

        # Preplace tokens based on settings.
        if self.options.shuffle_tokens == "off" or self.options.shuffle_tokens == "dungeon":
            token_item = self.create_item(Items.GOLD_SKULLTULA_TOKEN.value)
            for location_name, location_data in gold_skulltula_overworld_location_table.items():
                self.get_location(location_name).place_locked_item(token_item)

        if self.options.shuffle_tokens == "off" or self.options.shuffle_tokens == "overworld":
            token_item = self.create_item(Items.GOLD_SKULLTULA_TOKEN.value)
            for location_name, location_data in gold_skulltula_dungeon_location_table.items():
                self.get_location(location_name).place_locked_item(token_item)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def set_rules(self) -> None:
        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: True

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "closed_forest": self.options.closed_forest.value,
            "kakariko_gate": self.options.kakariko_gate.value,
            "door_of_time": self.options.door_of_time.value,
            "zoras_fountain": self.options.zoras_fountain.value,
            "sleeping_waterfall": self.options.sleeping_waterfall.value,
            "jabu_jabu": self.options.jabu_jabu.value,
            "lock_overworld_doors": self.options.lock_overworld_doors.value,
            "fortress_carpenters": self.options.fortress_carpenters.value,
            "rainbow_bridge": self.options.rainbow_bridge.value,
            "rainbow_bridge_stones_required": self.options.rainbow_bridge_stones_required.value,
            "rainbow_bridge_medallions_required": self.options.rainbow_bridge_medallions_required.value,
            "rainbow_bridge_dungeon_rewards_required": self.options.rainbow_bridge_dungeon_rewards_required.value,
            "rainbow_bridge_dungeons_required": self.options.rainbow_bridge_dungeons_required.value,
            "rainbow_bridge_skulltokens_required": self.options.rainbow_bridge_skulltokens_required.value,
            "ganons_trials_required": self.options.ganons_trials_required.value,
            "triforce_hunt": self.options.triforce_hunt.value,
            "triforce_hunt_required_pieces": self.options.triforce_hunt_required_pieces.value,
            "triforce_hunt_extra_pieces_percentage": self.options.triforce_hunt_extra_pieces_percentage.value,
            "shuffle_tokens": self.options.shuffle_tokens.value,
            "shuffle_master_sword": self.options.shuffle_master_sword.value,
            "shuffle_childs_wallet": self.options.shuffle_childs_wallet.value,
            "shuffle_ocarina_buttons": self.options.shuffle_ocarina_buttons.value,
            "shuffle_swim": self.options.shuffle_swim.value,
            "shuffle_weird_egg": self.options.shuffle_weird_egg.value,
            "shuffle_fishing_pole": self.options.shuffle_fishing_pole.value,
            "shuffle_deku_stick_bag": self.options.shuffle_deku_stick_bag.value,
            "shuffle_deku_nut_bag": self.options.shuffle_deku_nut_bag.value,
            "shuffle_freestanding_items": self.options.shuffle_freestanding_items.value,
            "shuffle_shops": self.options.shuffle_shops.value,
            "shuffle_fish": self.options.shuffle_fish.value,
            "shuffle_scrubs": self.options.shuffle_scrubs.value,
            "shuffle_beehives": self.options.shuffle_beehives.value,
            "shuffle_cows": self.options.shuffle_cows.value,
            "shuffle_pots": self.options.shuffle_pots.value,
            "shuffle_crates": self.options.shuffle_crates.value,
            "shuffle_merchants": self.options.shuffle_merchants.value,
            "shuffle_frog_song_rupees": self.options.shuffle_frog_song_rupees.value,
            "shuffle_adult_trade_items": self.options.shuffle_adult_trade_items.value,
            "shuffle_boss_souls": self.options.shuffle_boss_souls.value,
            "shuffle_fairies": self.options.shuffle_fairies.value,
            "shuffle_grass": self.options.shuffle_grass.value,
            "shuffle_dungeon_rewards": self.options.shuffle_dungeon_rewards.value,
            "maps_and_compasses": self.options.maps_and_compasses.value,
            "ganons_castle_boss_key": self.options.ganons_castle_boss_key.value,
            "ganons_castle_boss_key_stones_required": self.options.ganons_castle_boss_key_stones_required.value,
            "ganons_castle_boss_key_medallions_required": self.options.ganons_castle_boss_key_medallions_required.value,
            "ganons_castle_boss_key_dungeon_rewards_required": self.options.ganons_castle_boss_key_dungeon_rewards_required.value,
            "ganons_castle_boss_key_dungeons_required": self.options.ganons_castle_boss_key_dungeons_required.value,
            "ganons_castle_boss_key_skull_tokens_required": self.options.ganons_castle_boss_key_skull_tokens_required.value,
            "key_rings": self.options.key_rings.value,
            "big_poe_target_count": self.options.big_poe_target_count.value,
            "skip_child_zelda": self.options.skip_child_zelda.value,
            "skip_epona_race": self.options.skip_epona_race.value,
            "complete_mask_quest": self.options.complete_mask_quest.value,
            "skip_scarecrows_song": self.options.skip_scarecrows_song.value,
            "full_wallets": self.options.full_wallets.value,
            "bombchu_bag": self.options.bombchu_bag.value,
            "bombchu_drops": self.options.bombchu_drops.value,
            "blue_fire_arrows": self.options.blue_fire_arrows.value,
            "sunlight_arrows": self.options.sunlight_arrows.value,
            "infinite_upgrades": self.options.infinite_upgrades.value,
            "skeleton_key": self.options.skeleton_key.value,
        }
    
    def collect(self, state: CollectionState, item: Item) -> bool:
        # Temporarily disabled because logic is in progress
        #update_age_access(self, state)
        return super().collect(state, item)
    
    def remove(self, state: CollectionState, item: Item) -> bool:
        # Temporarily disabled because logic is in progress
        #reset_age_access() #TODO pass the starting age option 
        #update_age_access(self, state)
        return super().remove(state, item)