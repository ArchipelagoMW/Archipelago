import os
import json
from ..AutoWorld import World
from ..generic.Rules import set_rule
from BaseClasses import Region, Item, Location, RegionType, Entrance
from .Options import options


class PysolFCWorld(World):
    game: str = "PysolFC"
    game_table = {}
    with open(os.path.join(os.path.dirname(__file__), 'games.json'), 'r') as file:
        game_table = json.loads(file.read())
    item_name_to_id = {}
    options = options
    id = 626001
    for solgame in game_table:
        #lookup_id_to_name[id] = game["name"]
        #lookup_name_to_item[game["name"]] = {"id": id,"name": game["name"],"progression": True,"game": game}
        item_name_to_id[solgame["name"]] = id
        id += 1
        
    location_name_to_id = item_name_to_id
    def generate_basic(self):
        for solgame in self.game_table:
            self.world.itempool.append(Item(solgame['name'],True,self.item_name_to_id[solgame['name']],self.player))
        for i in range(self.world.initial_games[self.player]):
            self.world.push_precollected(self.world.random.choice(self.world.itempool))
    def create_regions(self):
        world = self.world
        menuregion = Region("Menu",RegionType.Generic,"Menu",self.player,world)
        world.regions.append(menuregion)
        start = Entrance(self.player,"Start Game",menuregion)
        menuregion.exits.append(start)
        region = Region("PysolFC",RegionType.Generic,"PysolFC",self.player,world)
        self.region = region
        world.regions.append(region)
        start.connect(region)
        for location in self.location_name_to_id:
            region.locations.append(Location(self.player, location, self.location_name_to_id[location], region))
        region.world = world
    def set_rules(self):
        for location in self.region.locations:
            try:
                if self.item_name_to_id[location.name]:
                    set_rule(location,lambda state,name=location.name: 
                        state.has(name,self.player)
                    )
            except KeyError:
                pass
        self.world.worlds[self.player].item_name_groups["completed_games"] = self.item_name_to_id
        self.world.completion_condition[self.player] = lambda state: state.has_group("completed_games",self.player,self.world.victory_number[self.player])
        