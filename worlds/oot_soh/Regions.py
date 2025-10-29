from typing import NamedTuple, TYPE_CHECKING
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
    tree_location_table, \
    freestanding_overworld_location_table, \
    freestanding_dungeon_location_table, \
    fairies_fountain_location_table, \
    fairies_stone_location_table, \
    fairies_bean_location_table, \
    fairies_song_location_table, \
    grass_overworld_location_table, \
    grass_dungeon_location_table, \
    fish_pond_location_table, \
    fish_overworld_location_table, \
    child_zelda_location_table, \
    carpenters_location_table, \
    hundred_skulls_location_table, \
    no_logic_crates_location_table, \
    no_logic_trees_location_table
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
    connecting_regions: list[str] = []


class SohRegion(Region):
    game = "Ship of Harkinian"

    def __init__(self, name: str, player: int, multiworld: MultiWorld, hint: str | None = None):
        super().__init__(name, player, multiworld, hint)

    def can_reach(self, state) -> bool:
        if state._soh_stale[self.player]:
            stored_age = state._soh_age[self.player]
            state._soh_update_age_reachable_regions(self.player)
            state._soh_age[self.player] = stored_age

        if state._soh_age[self.player] == Ages.CHILD:
            return self in state._soh_child_reachable_regions[self.player]
        elif state._soh_age[self.player] == Ages.ADULT:
            return self in state._soh_adult_reachable_regions[self.player]
        else:
            return self in state._soh_child_reachable_regions[self.player] or self in state._soh_adult_reachable_regions[self.player]


def create_regions_and_locations(world: "SohWorld") -> None:

    # Fill region data table based on the regions enum list
    region_data_table: dict[str, SohRegionData] = {}
    for entry in Regions:
        region_data_table[entry] = SohRegionData([])

    # exclusions
    # We don't need HC Garden if child zelda is skipped
    if world.options.skip_child_zelda:
        region_data_table.pop(Regions.HC_GARDEN)

    # Create regions.
    for region_name in region_data_table.keys():
        region = SohRegion(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)
        region.add_exits(region_data_table[region_name].connecting_regions)

        # Create locations

        # Base locations
        world.included_locations.update(base_location_table)

        # Gold Skulltulas (Overworld)
        world.included_locations.update(
            gold_skulltula_overworld_location_table)

        # Gold Skulltulas (Dungeon)
        world.included_locations.update(gold_skulltula_dungeon_location_table)

        # Shops, Add all shop locations vanilla items will get prefilled and locked
        # Todo: maybe we have to add the vanilla locations as events (id = None)
        # check if vanilla items show up in the list of checks
        world.included_locations.update(shops_location_table)

        # Scrubs
        if world.options.shuffle_scrubs:
            world.included_locations.update(scrubs_location_table)

        # Adult Trade Items
        if world.options.shuffle_adult_trade_items:
            world.included_locations.update(trade_items_location_table)

        # Merchants
        if world.options.shuffle_merchants == "bean_merchant_only" or world.options.shuffle_merchants == "all":
            world.included_locations[Locations.ZR_MAGIC_BEAN_SALESMAN] \
                = merchants_items_location_table[Locations.ZR_MAGIC_BEAN_SALESMAN]

        if world.options.shuffle_merchants == "all_but_beans" or world.options.shuffle_merchants == "all":
            for location_name in (Locations.KAK_GRANNYS_SHOP, Locations.GC_MEDIGORON,
                                  Locations.WASTELAND_CARPET_SALESMAN):
                world.included_locations[location_name] = merchants_items_location_table[location_name]

        # Cows
        if world.options.shuffle_cows:
            world.included_locations.update(cows_location_table)

        # Frogs
        if world.options.shuffle_frog_song_rupees:
            world.included_locations.update(frogs_location_table)

        # Beehives
        if world.options.shuffle_beehives:
            world.included_locations.update(beehives_location_table)

        # Pots (Overworld)
        if world.options.shuffle_pots == "overworld" or world.options.shuffle_pots == "all":
            world.included_locations.update(pots_overworld_location_table)

        # Pots (Dungeon)
        if world.options.shuffle_pots == "dungeon" or world.options.shuffle_pots == "all":
            world.included_locations.update(pots_dungeon_location_table)

        # Crates (Overworld)
        if world.options.shuffle_crates == "overworld" or world.options.shuffle_crates == "all":
            world.included_locations.update(crates_overworld_location_table)

        # Crates (Dungeon)
        if world.options.shuffle_crates == "dungeon" or world.options.shuffle_crates == "all":
            world.included_locations.update(crates_dungeon_location_table)

        # Trees
        if world.options.shuffle_trees:
            world.included_locations.update(tree_location_table)

        # Freestanding (Overworld)
        if world.options.shuffle_freestanding_items == "overworld" or world.options.shuffle_freestanding_items == "all":
            world.included_locations.update(
                freestanding_overworld_location_table)

        # Freestanding (Dungeon)
        if world.options.shuffle_freestanding_items == "dungeon" or world.options.shuffle_freestanding_items == "all":
            world.included_locations.update(
                freestanding_dungeon_location_table)

        # Fairies
        if world.options.shuffle_fountain_fairies:
            world.included_locations.update(fairies_fountain_location_table)
        if world.options.shuffle_stone_fairies:
            world.included_locations.update(fairies_stone_location_table)
        if world.options.shuffle_bean_fairies:
            world.included_locations.update(fairies_bean_location_table)
        if world.options.shuffle_song_fairies:
            world.included_locations.update(fairies_song_location_table)

        # Grass (Overworld)
        if world.options.shuffle_grass == "overworld" or world.options.shuffle_grass == "all":
            world.included_locations.update(grass_overworld_location_table)

        # Grass (Dungeon)
        if world.options.shuffle_grass == "dungeon" or world.options.shuffle_grass == "all":
            world.included_locations.update(grass_dungeon_location_table)

        # Fish (Pond)
        if world.options.shuffle_fish == "pond" or world.options.shuffle_fish == "all":
            world.included_locations.update(fish_pond_location_table)

        # Fish (Overworld)
        if world.options.shuffle_fish == "overworld" or world.options.shuffle_fish == "all":
            world.included_locations.update(fish_overworld_location_table)

        # Child Zelda
        if not world.options.skip_child_zelda:
            world.included_locations.update(child_zelda_location_table)

        # Carpenters
        if world.options.fortress_carpenters == "normal":
            world.included_locations.update(carpenters_location_table)

        if world.options.fortress_carpenters == "fast":
            for location_name in (Locations.GF_GERUDO_MEMBERSHIP_CARD, Locations.TH_1_TORCH_CARPENTER):
                world.included_locations[location_name] = carpenters_location_table[location_name]

        if world.options.shuffle_100_gs_reward:
            world.included_locations.update(hundred_skulls_location_table)

        if world.options.true_no_logic:
            if world.options.shuffle_crates == "overworld" or world.options.shuffle_crates == "all":
                world.included_locations.update(no_logic_crates_location_table)
            if world.options.shuffle_trees:
                world.included_locations.update(no_logic_trees_location_table)

    # Set region rules and location rules after all locations are created
    all_regions = [root, castle_grounds, death_mountain_crater, death_mountain_trail, desert_colossus, gerudo_fortress,
                   gerudo_valley, goron_city, graveyard, haunted_wasteland, hyrule_field, kakariko, kokiri_forest,
                   lake_hylia, lon_lon_ranch, lost_woods, market, sacred_forest_meadow, temple_of_time, thieves_hideout,
                   zoras_domain, zoras_fountain, zoras_river, bottom_of_the_well, deku_tree, dodongos_cavern,
                   fire_temple, forest_temple, ganons_castle, gerudo_training_ground, ice_cavern, jabujabus_belly,
                   shadow_temple, spirit_temple, water_temple]
    for region in all_regions:
        region.set_region_rules(world)


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


def place_locked_items(world: "SohWorld") -> None:

    # Add Weird Egg and Zelda's Letter to their vanilla locations when not shuffled
    if not world.options.skip_child_zelda and not world.options.shuffle_weird_egg:
        world.get_location(Locations.HC_MALON_EGG).place_locked_item(
            world.create_item(Items.WEIRD_EGG))

    if not world.options.skip_child_zelda:
        world.get_location(Locations.HC_ZELDAS_LETTER).place_locked_item(
            world.create_item(Items.ZELDAS_LETTER))

    # Place Master Sword on vanilla location if not shuffled
    if not world.options.shuffle_master_sword:
        world.get_location(Locations.MARKET_TOT_MASTER_SWORD).place_locked_item(
            world.create_item(Items.MASTER_SWORD))

    # Preplace dungeon rewards in vanilla locations when not shuffled
    if world.options.shuffle_dungeon_rewards == "off":
        # Loop through dungeons rewards and set their items to the vanilla reward.
        for location_name, reward_name in zip(dungeon_reward_item_mapping.keys(), dungeon_reward_item_mapping.values()):
            world.get_location(location_name.value).place_locked_item(
                world.create_item(reward_name.value))

    # Place Ganons Boss Key
    if not world.options.ganons_castle_boss_key == "vanilla" and not world.options.ganons_castle_boss_key == "anywhere" and not world.options.triforce_hunt:
        world.get_location(Locations.MARKET_TOT_LIGHT_ARROW_CUTSCENE).place_locked_item(
            world.create_item(Items.GANONS_CASTLE_BOSS_KEY))

    if world.options.ganons_castle_boss_key == "vanilla" and not world.options.triforce_hunt:
        world.get_location(Locations.GANONS_CASTLE_TOWER_BOSS_KEY_CHEST).place_locked_item(
            world.create_item(Items.GANONS_CASTLE_BOSS_KEY))

    # Preplace tokens based on settings.
    if world.options.shuffle_skull_tokens == "off" or world.options.shuffle_skull_tokens == "dungeon":
        token_item = world.create_item(Items.GOLD_SKULLTULA_TOKEN)
        for location_name, address in gold_skulltula_overworld_location_table.items():
            world.get_location(location_name).place_locked_item(token_item)

    if world.options.shuffle_skull_tokens == "off" or world.options.shuffle_skull_tokens == "overworld":
        token_item = world.create_item(Items.GOLD_SKULLTULA_TOKEN)
        for location_name, address in gold_skulltula_dungeon_location_table.items():
            world.get_location(location_name).place_locked_item(token_item)
