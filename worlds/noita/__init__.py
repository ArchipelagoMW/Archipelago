import functools
import string

from BaseClasses import Tutorial, ItemClassification, Item, MultiWorld
from worlds.AutoWorld import World, WebWorld

from . import Options, Items, Locations, Regions, Rules

# TODO: Ban higher tier wands from appearing in earlier locations
# TODO: Reaching a holy mountain unlocks the holy mountain, gate it behind an event

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
        # Generate Victory shenanigans (TODO this is temporary)
        the_work_region = self.world.get_region("The Work", self.player)
        victory_loc = Locations.NoitaLocation(self.player, "Victory", None, the_work_region)

        victory_loc.place_locked_item(self.create_event("Victory"))
        self.world.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        the_work_region.locations.append(victory_loc)

        # Create events
        self.create_events()


    def get_filler_item_name(self) -> str:
        return self.world.random.choice(Items.filler_items)


    # TODO Should we move events out to keep this slim?
    def create_event(self, name: str) -> Item:
        return Items.NoitaItem(name, ItemClassification.progression, None, self.player)


    # TODO Should we move events out to keep this slim?
    def create_events(self) -> None:
        total_locations = self.world.total_locations[self.player].value

        # TODO This is a hack for now, we throw all the chest popups in Forest
        forest_region = self.world.get_region("Forest", self.player)

        # Iterates all our generated chests and makes sure that they are accessible in a specific
        # logical order (?) TODO: Revisit and confirm this
        for i in range(1, 1 + total_locations):
            pickup_event = self.create_event(f"Pickup{(i + 1)}")

            event_loc = Locations.NoitaLocation(self.player, pickup_event.name, None, forest_region)
            event_loc.place_locked_item(pickup_event)
            event_loc.access_rule(lambda state, i=i: state.can_reach(f"Chest{i}", "Location", self.player))
            forest_region.locations.append(event_loc)


    def fill_slot_data(self):
        return {
            "seed": "".join(self.world.slot_seeds[self.player].choices(string.digits, k=16)),
            "totalLocations": self.world.total_locations[self.player].value,
            "badEffects": self.world.bad_effects[self.player].value,
            "deathLink": self.world.death_link[self.player].value,
        }
