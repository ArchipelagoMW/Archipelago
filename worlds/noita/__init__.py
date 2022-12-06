import functools
import string

from BaseClasses import Tutorial, ItemClassification, Item
from worlds.AutoWorld import World, WebWorld

client_version = 1 # TODO: Do we need this random variable??


class NoitaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Noita integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["DaftBrit"]
    )]
    theme = "partyTime"


# Keeping World slim so that it's easier to comprehend
class NoitaWorld(World):
    """
    Noita is a magical action roguelite set in a world where every pixel is physically simulated. Fight, explore, melt,
    burn, freeze, and evaporate your way through the procedurally generated world using wands you've created yourself.
    """
    game: str = "Noita"
    option_definitions = Options.noita_options
    topology_present = True

    item_name_to_id = Items.item_name_to_id
    location_name_to_id = Locations.location_name_to_id
    
    item_name_groups = Items.item_name_groups

    data_version = 1
    forced_auto_forfeit = False
    web = NoitaWeb()


    def create_regions(self) -> None:
        Regions.create_all_regions(self.world, self.player)


    def create_items(self) -> None:
        Items.create_all_items(self.world, self.player)


    def set_rules(self) -> None:
        "" #TODO


    # Generate victory conditions and other shenanigans
    def generate_basic(self) -> None:
        self.world.get_location("The Work", self.player).place_locked_item(self.create_event("Victory"))
        self.completion_condition[self.player] = lambda state: state.has("Victory")


    def get_filler_item_name(self) -> str:
        return self.world.random.choice(Items.filler_items)


    def create_event(self, name: str) -> Item:
        return Items.NoitaItem(name, ItemClassification.progression, None, self.player)


    #def create_events(world: MultiWorld, player: int) -> None:
    #    total_locations = world.total_locations[player].value
    #    world_region = world.get_region("Mines", player)
    #    for i in range(1, 1 + total_locations):
    #        event_loc = NoitaLocation(player, f"Pickup{(i + 1)}", None, world_region)
    #        event_loc.place_locked_item(NoitaItem(f"Pickup{(i + 1)}", ItemClassification.progression, None, player))
    #        event_loc.access_rule(lambda state, i=i: state.can_reach(f"Chest{(i + 1) - 1}", player))
    #        world_region.locations.append(event_loc)


    def fill_slot_data(self):
        return {
            "seed": "".join(self.world.slot_seeds[self.player].choice(string.digits) for i in range(16)),
            "totalLocations": self.world.total_locations[self.player].value,
            "badEffects": self.world.bad_effects[self.player].value,
            "deathLink": self.world.death_link[self.player].value,
        }
