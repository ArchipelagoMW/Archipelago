from BaseClasses import MultiWorld, Region, Entrance, CollectionState
from .locations import location_data, create_location
from worlds.generic.Rules import add_rule

def create_region(multiworld: MultiWorld, player: int, region_name: str, parent_region : Region = None,
                  region_rank = 0):
    ret = FFVCDRegion(region_name, player, multiworld, region_rank)
    # find all locations for region
    for location_data_entry in location_data:
        if location_data_entry.area == region_name:
            location_object = create_location(multiworld, player, location_data_entry, parent_region)
            location_object.parent_region = ret
            ret.locations.append(location_object)


    return ret

def setup_region_and_entrance(multiworld, player, region_name, parent_region_name, 
                              access_rule = None, region_rank = 0):
    
    parent_region = multiworld.get_region(parent_region_name, player)
    new_region = create_region(multiworld, player, region_name, parent_region, region_rank)
    new_entrance = Entrance(player, region_name, parent_region)
    new_entrance.connect(new_region)
    if access_rule:
        new_entrance.access_rule = access_rule
    parent_region.exits.append(new_entrance)
    multiworld.regions.append(new_region)

def create_regions(multiworld, player: int):
    menu_region = create_region(multiworld, player, 'Menu')
    multiworld.regions.append(menu_region)

    setup_region_and_entrance(multiworld, player, "Crystal Warp", "Menu", access_rule = None)

    setup_region_and_entrance(multiworld, player, "World 1 Access", "Crystal Warp", access_rule = None)
    setup_region_and_entrance(multiworld, player, "World 2 Access", "Crystal Warp", access_rule = \
                              lambda state: (state.has("Adamantite", player)) 
                              or (state.has("World 2 Access (Item)", player)))
    setup_region_and_entrance(multiworld, player, "World 3 Access", "Crystal Warp", access_rule = \
                              lambda state: ((state.has("Adamantite", player)\
                              and state.has("Bracelet", player)\
                              and state.has("Anti Barrier", player)))\
                              or (state.has("World 3 Access (Item)", player)))


    setup_region_and_entrance(multiworld, player, "Ancient Library", "World 1 Access", access_rule = None,
                              region_rank = 3)
    setup_region_and_entrance(multiworld, player, "Ancient Library (World 3)", "World 3 Access", access_rule = None,
                              region_rank = 7)
    setup_region_and_entrance(multiworld, player, "Ancient Library Lower", "World 1 Access", access_rule =\
                              lambda state: state.has("Ifrit's Fire", player),
                                                        region_rank = 4)
    setup_region_and_entrance(multiworld, player, "Bal Castle", "World 2 Access", access_rule = None,
                              region_rank = 5)
    setup_region_and_entrance(multiworld, player, "Bal Castle Lower", "World 3 Access", access_rule = None,
                              region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Barrier Tower", "World 2 Access", access_rule = \
                              lambda state: state.has("Submarine Key", player),
                                                        region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Big Bridge", "World 2 Access", access_rule = \
                              lambda state: state.has("Big Bridge Key", player),
                                                        region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Carwen", "World 1 Access", access_rule = None,
                              region_rank = 3)
    setup_region_and_entrance(multiworld, player, "Catapult", "World 1 Access", access_rule = None,
                              region_rank = 4)
    setup_region_and_entrance(multiworld, player, "Crescent Island", "World 1 Access", access_rule = None,
                              region_rank = 5)
    setup_region_and_entrance(multiworld, player, "Desert of Shifting Sands", "World 1 Access", access_rule = \
                              lambda state: state.has("SandwormBait", player),
                                                        region_rank = 4)
    setup_region_and_entrance(multiworld, player, "Exdeath's Castle", "World 2 Access", access_rule = \
                              lambda state: state.has("Bracelet", player) and state.has("Anti Barrier", player),
                                                        region_rank = 7)
    setup_region_and_entrance(multiworld, player, "Exdeath's Castle Lower", "World 2 Access", access_rule = \
                              lambda state: state.has("Anti Barrier", player),
                                                        region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Flying Lonka Ruins", "World 1 Access", access_rule =\
                              lambda state: state.has("Adamantite", player),
                                                        region_rank = 5)
    setup_region_and_entrance(multiworld, player, "Fork Tower", "World 3 Access", access_rule = \
                              lambda state: state.has("Elder Branch", player),
                                                        region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Great Trench", "World 3 Access", access_rule = \
                              lambda state: state.has("Trench Page", player)\
                              and state.has("Submarine Key", player),
                                                        region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Hiryuu Valley", "World 2 Access", access_rule = None,
                              region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Istory", "World 1 Access", access_rule = None,
                              region_rank = 5)
    setup_region_and_entrance(multiworld, player, "Istory Falls", "World 3 Access", access_rule = \
                          lambda state: state.has("Falls Page", player)\
                              and state.has("Submarine Key", player),
                                                        region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Jacole", "World 1 Access", access_rule = None,
                              region_rank = 5)
    setup_region_and_entrance(multiworld, player, "Karnak (On Fire)", "World 1 Access", access_rule = None)
    setup_region_and_entrance(multiworld, player, "Karnak", "World 1 Access", access_rule = \
                              lambda state: state.has("Steamship Key", player),
                                                        region_rank = 3)
    setup_region_and_entrance(multiworld, player, "Karnak Meteor", "World 1 Access", access_rule = None,
                              region_rank = 3)
    setup_region_and_entrance(multiworld, player, "Kelb", "World 2 Access", access_rule = None,
                              region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Kuzar", "World 2 Access", access_rule =  \
                              lambda state: state.has("1st Tablet", player) and 
                              state.has("2nd Tablet", player) and
                              state.has("3rd Tablet", player) and
                              state.has("4th Tablet", player),
                                                        region_rank = 7)
    setup_region_and_entrance(multiworld, player, "Lix", "World 1 Access", access_rule = None,
                              region_rank = 5)
    setup_region_and_entrance(multiworld, player, "Lonka Meteor", "World 1 Access", access_rule = None,
                              region_rank = 5)
    setup_region_and_entrance(multiworld, player, "Mirage Village", "World 3 Access", access_rule = \
                              lambda state: state.has("Mirage Radar", player),
                                                        region_rank = 9)
    setup_region_and_entrance(multiworld, player, "Moogle Village", "World 2 Access", access_rule =\
                              lambda state: state.has("Moogle Suit", player),
                                                        region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Moogle Waterway", "World 2 Access", access_rule = None,
                              region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Mua", "World 2 Access", access_rule = None,
                              region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Mua Forest", "World 2 Access", access_rule = \
                              lambda state: state.has("Elder Branch", player),
                                                        region_rank = 7)
    setup_region_and_entrance(multiworld, player, "North Mountain", "World 1 Access", access_rule = None,
                              region_rank = 2)
    setup_region_and_entrance(multiworld, player, "North Mountain (World 3)", "World 3 Access", access_rule = \
                              lambda state: state.has("Mirage Radar", player),
                                                        region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Phoenix Tower", "World 3 Access", access_rule = \
                              lambda state: state.has("Mirage Radar", player),
                                                        region_rank = 9)
    setup_region_and_entrance(multiworld, player, "Pirate's Cave", "World 1 Access", access_rule = None,
                              region_rank = 1)
    setup_region_and_entrance(multiworld, player, "Pyramid", "World 3 Access", access_rule = \
                              lambda state: state.has("Pyramid Page", player),
                                                        region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Rift (1 Tablet)", "World 3 Access", access_rule = \
                              lambda state: state.has("1st Tablet", player),
                                                        region_rank = 9)
    setup_region_and_entrance(multiworld, player, "Rift (2 Tablets)", "World 3 Access", access_rule = \
                              lambda state: state.has("1st Tablet", player) and 
                              state.has("2nd Tablet", player),
                                                        region_rank = 9)
    setup_region_and_entrance(multiworld, player, "Rift (3 Tablets)", "World 3 Access", access_rule = \
                              lambda state: state.has("1st Tablet", player) and 
                              state.has("2nd Tablet", player) and
                              state.has("3rd Tablet", player),
                                                        region_rank = 10)
    setup_region_and_entrance(multiworld, player, "Rift (4 Tablets)", "World 3 Access", access_rule = \
                              lambda state: state.has("1st Tablet", player) and 
                              state.has("2nd Tablet", player) and
                              state.has("3rd Tablet", player) and
                              state.has("4th Tablet", player),
                                                        region_rank = 10)
    setup_region_and_entrance(multiworld, player, "Rugor", "World 3 Access", access_rule = None,
                              region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Ruined City", "World 1 Access", access_rule = None,
                              region_rank = 4)
    setup_region_and_entrance(multiworld, player, "Ship Graveyard", "World 1 Access", access_rule = None,
                              region_rank = 2)
    setup_region_and_entrance(multiworld, player, "Solitary Island", "World 3 Access", access_rule = \
                              lambda state: state.has("Shrine Page", player),
                                                        region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Steamship", "World 1 Access", access_rule = \
                              lambda state: state.has("Steamship Key", player),
                                                        region_rank = 3)
    setup_region_and_entrance(multiworld, player, "Surgate Castle", "World 2 Access", access_rule = None,
                              region_rank = 6)
    setup_region_and_entrance(multiworld, player, "Torna Canal", "World 1 Access", access_rule = None,
                              region_rank = 1)
    setup_region_and_entrance(multiworld, player, "Tule", "World 1 Access", access_rule = None,
                              region_rank = 1)
    setup_region_and_entrance(multiworld, player, "Tule Pass", "World 3 Access", access_rule = None,
                              region_rank = 7)
    setup_region_and_entrance(multiworld, player, "Tycoon Castle", "World 1 Access", access_rule = None,
                              region_rank = 1)
    setup_region_and_entrance(multiworld, player, "Tycoon Meteor", "World 1 Access", access_rule = None,
                              region_rank = 1)
    setup_region_and_entrance(multiworld, player, "Void", "World 3 Access", access_rule = \
                              lambda state: state.has("1st Tablet", player) and 
                              state.has("2nd Tablet", player) and
                              state.has("3rd Tablet", player) and
                              state.has("4th Tablet", player),
                                                        region_rank = 10)
    setup_region_and_entrance(multiworld, player, "Walse Town", "World 1 Access", access_rule = None,
                              region_rank = 2)
    setup_region_and_entrance(multiworld, player, "Walse Castle", "World 1 Access", access_rule = None,
                              region_rank = 2)
    setup_region_and_entrance(multiworld, player, "Walse Meteor", "World 1 Access", access_rule = None,
                              region_rank = 2)
    setup_region_and_entrance(multiworld, player, "Walse Tower", "World 1 Access", access_rule = 
                              lambda state: state.has("Walse Tower Key", player),
                                                        region_rank = 2)
    setup_region_and_entrance(multiworld, player, "Walse Tower Sunken", "World 3 Access", access_rule = 
                              lambda state: state.has("Submarine Key", player),
                                                        region_rank = 8)
    setup_region_and_entrance(multiworld, player, "Wind Shrine", "World 1 Access", access_rule = None,
                              region_rank = 1)
    setup_region_and_entrance(multiworld, player, "Zeza Fleet", "World 2 Access", access_rule = \
                              lambda state: state.has("Hiryuu Call", player),
                                                        region_rank = 7)

    
    void_region = multiworld.get_region("Void", player)
    exdeath = multiworld.get_location("ExDeath", player)
    exdeath.parent_region = void_region
    # void_region.locations.append(exdeath)




    add_rule(exdeath, lambda state: state.has("1st Tablet", player) and state.has("2nd Tablet", player) \
             and state.has("3rd Tablet", player) and state.has("4th Tablet", player))
         

class FFVCDRegion(Region):
    def __init__(self, name, player, multiworld, region_rank):
        super().__init__(name, player, multiworld)
        self.region_rank = region_rank
        
        
                        
