import string

from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld

from . import Options, Items, Locations, Regions, Rules, Events
from .Options import noita_options

# TODO: Ban higher tier wands from appearing in earlier locations
# TODO: Gate holy mountain access behind an event that triggers when you visit the same holy mountain?


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
    web = NoitaWeb()

    def create_regions(self) -> None:
        Regions.create_all_regions_and_connections(self.world, self.player)

    def create_items(self) -> None:
        Items.create_all_items(self.world, self.player)

    def set_rules(self) -> None:
        Rules.create_all_rules(self.world, self.player)

    # Generate victory conditions and other shenanigans
    def generate_basic(self) -> None:
        Events.create_all_events(self.world, self.player)

    def get_filler_item_name(self) -> str:
        return self.world.random.choice(Items.filler_items)

    # Things here will be sent to the client.
    def fill_slot_data(self):
        return {
            "seed": "".join(self.world.slot_seeds[self.player].choices(string.digits, k=16)),
            "totalLocations": self.world.total_locations[self.player].value,
            "badEffects": self.world.bad_effects[self.player].value,
            "deathLink": self.world.death_link[self.player].value,
            "victoryCondition": self.world.victory_condition[self.player].value,
            "orbsAsChecks": self.world.orbs_as_checks[self.player].value,
            "bossesAsChecks": self.world.bosses_as_checks[self.player].value,
        }
