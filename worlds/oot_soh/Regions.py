from typing import Dict, List, NamedTuple, TYPE_CHECKING
from worlds.AutoWorld import LogicMixin
from BaseClasses import MultiWorld, Region
from .Enums import *
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
    child_zelda_location_table, \
    carpenters_location_table, \
    hundred_skulls_location_table
from .location_access import root
from .location_access.overworld import \
    castle_grounds, \
    death_mountain_crater, \
    death_mountain_trail, \
    desert_colossus, \
    gerudo_fortress, \
    gerudo_valley, \
    goron_city, \
    graveyard, \
    haunted_wasteland, \
    hyrule_field, \
    kakariko, \
    kokiri_forest, \
    lake_hylia, \
    lon_lon_ranch, \
    lost_woods, \
    market, \
    sacred_forest_meadow, \
    temple_of_time, \
    thieves_hideout, \
    zoras_domain, \
    zoras_fountain, \
    zoras_river
from .location_access.dungeons import \
    bottom_of_the_well, \
    deku_tree, \
    dodongos_cavern, \
    fire_temple, \
    forest_temple, \
    ganons_castle, \
    gerudo_training_ground, \
    ice_cavern, \
    jabujabus_belly, \
    shadow_temple, \
    spirit_temple, \
    water_temple

if TYPE_CHECKING:
    from . import SohWorld


class SohRegionData(NamedTuple):
    connecting_regions: List[str] = []

class SohRegion(Region):
    game="Ship of Harkinian"

    def __init__(self, name: str, player: int, multiworld: MultiWorld, hint: str | None = None):
        super().__init__(name, player, multiworld, hint)

    def can_reach(self, state) -> bool:
        if state._soh_stale[self.player]:
            stored_age = state._soh_age[self.player]
            state._soh_update_age_reachable_regions(self.player)
            state._soh_age[self.player] = stored_age
        
        if state._soh_age[self.player] == "child":
            return self in state._soh_child_reachable_regions[self.player]
        elif state._soh_age[self.player] == "adult":
            return self in state._soh_adult_reachable_regions[self.player]
        else:
            return self in state._soh_child_reachable_regions[self.player] or self in state._soh_adult_reachable_regions[self.player]

def create_regions_and_locations(world: "SohWorld") -> None:

    # Fill region data table based on the regions enum list
    region_data_table: Dict[str, SohRegionData] = {}
    for entry in Regions:
        region_data_table[entry.value] = SohRegionData([])

    # Create regions.
    for region_name in region_data_table.keys():
        region = SohRegion(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)
        region.add_exits(region_data_table[region_name].connecting_regions)

        # Create locations

        # Base locations
        world.included_locations.update({
            location_name: address for location_name, address in base_location_table.items()
        })

        # Gold Skulltulas (Overworld)
        world.included_locations.update({
            location_name: address for location_name, address in gold_skulltula_overworld_location_table.items()
        })

        # Gold Skulltulas (Dungeon)
        world.included_locations.update({
            location_name: address for location_name, address in gold_skulltula_dungeon_location_table.items()
        })

        # Shops
        if world.options.shuffle_shops:
            world.included_locations.update({
                location_name: address for location_name, address in shops_location_table.items()
            })

        # Scrubs
        if world.options.shuffle_scrubs:
            world.included_locations.update({
                location_name: address for location_name, address in scrubs_location_table.items()
            })

        # Adult Trade Items
        if world.options.shuffle_adult_trade_items:
            world.included_locations.update({
                location_name: address for location_name, address in trade_items_location_table.items()
            })

        # Merchants
        if world.options.shuffle_merchants == "bean_merchant_only" or world.options.shuffle_merchants == "all":
            world.included_locations.update({
                location_name: address for location_name, address in merchants_items_location_table.items()
                if location_name == "ZR Magic Bean Salesman"
            })

        if world.options.shuffle_merchants == "all_but_beans" or world.options.shuffle_merchants == "all":
            world.included_locations.update({
                location_name: address for location_name, address in merchants_items_location_table.items()
                if location_name in {"Kak Granny's Shop", "GC Medigoron", "Wasteland Carpet Salesman"}
            })

        # Cows
        if world.options.shuffle_cows:
            world.included_locations.update({
                location_name: address for location_name, address in cows_location_table.items()
            })

        # Frogs
        if world.options.shuffle_frog_song_rupees:
            world.included_locations.update({
                location_name: address for location_name, address in frogs_location_table.items()
            })

        # Beehives
        if world.options.shuffle_beehives:
            world.included_locations.update({
                location_name: address for location_name, address in beehives_location_table.items()
            })

        # Pots (Overworld)
        if world.options.shuffle_pots == "overworld" or world.options.shuffle_pots == "all":
            world.included_locations.update({
                location_name: address for location_name, address in pots_overworld_location_table.items()
            })

        # Pots (Dungeon)
        if world.options.shuffle_pots == "dungeon" or world.options.shuffle_pots == "all":
            world.included_locations.update({
                location_name: address for location_name, address in pots_dungeon_location_table.items()
            })

        # Crates (Overworld)
        if world.options.shuffle_crates == "overworld" or world.options.shuffle_crates == "all":
            world.included_locations.update({
                location_name: address for location_name, address in crates_overworld_location_table.items()
            })

        # Crates (Dungeon)
        if world.options.shuffle_crates == "dungeon" or world.options.shuffle_crates == "all":
            world.included_locations.update({
                location_name: address for location_name, address in crates_dungeon_location_table.items()
            })

        # Freestanding (Overworld)
        if world.options.shuffle_freestanding_items == "overworld" or world.options.shuffle_freestanding_items == "all":
            world.included_locations.update({
                location_name: address for location_name, address in freestanding_overworld_location_table.items()
            })

        # Freestanding (Dungeon)
        if world.options.shuffle_freestanding_items == "dungeon" or world.options.shuffle_freestanding_items == "all":
            world.included_locations.update({
                location_name: address for location_name, address in freestanding_dungeon_location_table.items()
            })

        # Fairies
        if world.options.shuffle_fairies:
            world.included_locations.update({
                location_name: address for location_name, address in fairies_location_table.items()
            })

        # Grass (Overworld)
        if world.options.shuffle_grass == "overworld" or world.options.shuffle_grass == "all":
            world.included_locations.update({
                location_name: address for location_name, address in grass_overworld_location_table.items()
            })

        # Grass (Dungeon)
        if world.options.shuffle_grass == "dungeon" or world.options.shuffle_grass == "all":
            world.included_locations.update({
                location_name: address for location_name, address in grass_dungeon_location_table.items()
            })

        # Fish (Pond)
        if world.options.shuffle_fish == "pond" or world.options.shuffle_fish == "all":
            world.included_locations.update({
                location_name: address for location_name, address in fish_pond_location_table.items()
            })

        # Fish (Overworld)
        if world.options.shuffle_fish == "overworld" or world.options.shuffle_fish == "all":
            world.included_locations.update({
                location_name: address for location_name, address in fish_overworld_location_table.items()
            })

        # Child Zelda
        if not world.options.skip_child_zelda:
            world.included_locations.update({
                location_name: address for location_name, address in child_zelda_location_table.items()
            })

        # Carpenters
        if world.options.fortress_carpenters == "normal":
            world.included_locations.update({
                location_name: address for location_name, address in carpenters_location_table.items()
            })

        if world.options.fortress_carpenters == "fast":
            world.included_locations.update({
                location_name: address for location_name, address in carpenters_location_table.items()
                if location_name in {"GF Freed All Carpenters", "GF 1 Torch Carpenter"}
            })

        if world.options.shuffle_100_gs_reward:
            world.included_locations.update(hundred_skulls_location_table)
            
    # Set region rules and location rules after all locations are created
    all_regions = [root, castle_grounds, death_mountain_crater, death_mountain_trail, desert_colossus, gerudo_fortress,
                    gerudo_valley, goron_city, graveyard, haunted_wasteland, hyrule_field, kakariko, kokiri_forest, lake_hylia,
                    lon_lon_ranch, lost_woods, market, sacred_forest_meadow, temple_of_time, thieves_hideout, zoras_domain,
                    zoras_fountain, zoras_river, bottom_of_the_well, deku_tree, dodongos_cavern, fire_temple, forest_temple,
                    ganons_castle, gerudo_training_ground, ice_cavern, jabujabus_belly, shadow_temple, spirit_temple, water_temple]
    for region in all_regions:
        region.set_region_rules(world)

    # Place any locations that still don't have a region in the ROOT region.
    # TODO should be removed when logic is done
    for location_name, location_address in world.included_locations.items():
        world.get_region(Regions.ROOT.value).add_locations({location_name: location_address}, SohLocation)


def place_locked_items(world: "SohWorld") -> None:
    
    # Add Weird Egg and Zelda's Letter to their vanilla locations when not shuffled
    if not world.options.skip_child_zelda and not world.options.shuffle_weird_egg:
        world.get_location(Locations.HC_MALON_EGG.value).place_locked_item(world.create_item(Items.WEIRD_EGG.value))

    if not world.options.skip_child_zelda:
        world.get_location(Locations.HC_ZELDAS_LETTER.value).place_locked_item(world.create_item(Items.ZELDAS_LETTER.value))

    # Place Master Sword on vanilla location if not shuffled
    if not world.options.shuffle_master_sword:
        world.get_location(Locations.MARKET_TOT_MASTER_SWORD.value).place_locked_item(world.create_item(Items.MASTER_SWORD.value))

    # Handle vanilla goron tunic in shop
    # TODO: Proper implementation of vanilla shop items and shuffle them amongst all shops
    if world.options.shuffle_shops:
        world.get_location(Locations.GC_SHOP_ITEM1.value).place_locked_item(world.create_item(Items.BUY_GORON_TUNIC.value))

    # Create a dictionary mapping blue warp rewards to their vanilla items
    dungeon_reward_item_mapping = {
        Locations.QUEEN_GOHMA: Items.KOKIRIS_EMERALD,
        Locations.KING_DODONGO: Items.GORONS_RUBY,
        Locations.BARINADE: Items.ZORAS_SAPPHIRE,
        Locations.PHANTOM_GANON: Items.FOREST_MEDALLION,
        Locations.VOLVAGIA: Items.FIRE_MEDALLION,
        Locations.MORPHA: Items.WATER_MEDALLION,
        Locations.BONGO_BONGO: Items.SHADOW_MEDALLION,
        Locations.TWINROVA: Items.SPIRIT_MEDALLION,
        Locations.LINKS_POCKET: Items.LIGHT_MEDALLION
    }

    # Preplace dungeon rewards in vanilla locations when not shuffled
    if world.options.shuffle_dungeon_rewards == "off":      
        # Loop through dungeons rewards and set their items to the vanilla reward.      
        for location_name, reward_name in zip(dungeon_reward_item_mapping.keys(), dungeon_reward_item_mapping.values()):
            world.get_location(location_name.value).place_locked_item(world.create_item(reward_name.value))

    if world.options.shuffle_dungeon_rewards == "dungeons": 
        # Extract and shuffle just the item names from location_item_mapping
        reward_names = list(dungeon_reward_item_mapping.values())
        world.random.shuffle(reward_names)
        
        # Pair each location with a unique shuffled dungeon reward
        for location_name, reward_name in zip(dungeon_reward_item_mapping.keys(), reward_names):
            world.get_location(location_name.value).place_locked_item(world.create_item(reward_name.value))

    # Place Ganons Boss Key
    if not world.options.ganons_castle_boss_key == "vanilla" and not world.options.ganons_castle_boss_key == "anywhere" and not world.options.triforce_hunt:
        world.get_location(Locations.MARKET_TOT_LIGHT_ARROW_CUTSCENE.value).place_locked_item(world.create_item(Items.GANONS_CASTLE_BOSS_KEY.value))

    if world.options.ganons_castle_boss_key == "vanilla" and not world.options.triforce_hunt:
        world.get_location(Locations.GANONS_CASTLE_TOWER_BOSS_KEY_CHEST.value).place_locked_item(world.create_item(Items.GANONS_CASTLE_BOSS_KEY.value))

    # Preplace tokens based on settings.
    if world.options.shuffle_skull_tokens == "off" or world.options.shuffle_skull_tokens == "dungeon":
        token_item = world.create_item(Items.GOLD_SKULLTULA_TOKEN.value)
        for location_name, address in gold_skulltula_overworld_location_table.items():
            world.get_location(location_name).place_locked_item(token_item)

    if world.options.shuffle_skull_tokens == "off" or world.options.shuffle_skull_tokens == "overworld":
        token_item = world.create_item(Items.GOLD_SKULLTULA_TOKEN.value)
        for location_name, address in gold_skulltula_dungeon_location_table.items():
            world.get_location(location_name).place_locked_item(token_item)
