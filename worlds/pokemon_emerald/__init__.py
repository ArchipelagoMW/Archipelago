from typing import List
from BaseClasses import ItemClassification
from Options import Toggle
from ..AutoWorld import World
from .Items import PokemonEmeraldItem, create_item_label_to_id_map, get_item_classification
from .Locations import PokemonEmeraldLocation, create_location_label_to_id_map, create_locations_with_tags
from .Options import options, get_option_value
from .Regions import create_regions
from .Rom import generate_output
from .Rules import set_default_rules, set_overworld_item_rules, set_hidden_item_rules, set_npc_gift_rules, add_hidden_item_itemfinder_rules
from .SanityCheck import sanity_check


class PokemonEmeraldWorld(World):
    """
    Desc
    """
    game: str = "Pokemon Emerald"
    option_definitions = options
    topology_present = True

    item_name_to_id = create_item_label_to_id_map()
    location_name_to_id = create_location_label_to_id_map()

    data_version = 4

    def _get_pokemon_emerald_data(self):
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'race': self.multiworld.is_race,
        }


    def create_regions(self):
        if (sanity_check() == False): raise AssertionError("Sanity check failed")

        overworld_items_option = get_option_value(self.multiworld, self.player, "overworld_items")
        hidden_items_option = get_option_value(self.multiworld, self.player, "hidden_items")
        npc_gifts_option = get_option_value(self.multiworld, self.player, "npc_gifts")

        tags = set(["Badge", "HM", "KeyItem", "Rod"])
        if (overworld_items_option == Toggle.option_true):
            tags.add("OverworldItem")
        if (hidden_items_option == Toggle.option_true):
            tags.add("HiddenItem")
        if (npc_gifts_option == Toggle.option_true):
            tags.add("NpcGift")

        create_regions(self.multiworld, self.player)
        create_locations_with_tags(self.multiworld, self.player, tags)


    def create_items(self):
        badges_option = get_option_value(self.multiworld, self.player, "badges")
        hms_option = get_option_value(self.multiworld, self.player, "hms")
        key_items_option = get_option_value(self.multiworld, self.player, "key_items")
        rods_option = get_option_value(self.multiworld, self.player, "rods")

        item_locations: List[PokemonEmeraldLocation] = []
        for region in self.multiworld.regions:
            if (region.player == self.player):
                item_locations += [location for location in region.locations if not location.id == None] # Filter events

                if (badges_option == Toggle.option_false):
                    item_locations = [location for location in item_locations if "Badge" not in location.tags]
                if (hms_option == Toggle.option_false):
                    item_locations = [location for location in item_locations if "HM" not in location.tags]
                if (key_items_option == Toggle.option_false):
                    item_locations = [location for location in item_locations if "KeyItem" not in location.tags]
                if (rods_option == Toggle.option_false):
                    item_locations = [location for location in item_locations if "Rod" not in location.tags]

        self.multiworld.itempool += [self.create_item_by_id(location.default_item_id) for location in item_locations]
    
    
    def set_rules(self):
        set_default_rules(self.multiworld, self.player)

        if (get_option_value(self.multiworld, self.player, "overworld_items") == Toggle.option_true):
            set_overworld_item_rules(self.multiworld, self.player)
        if (get_option_value(self.multiworld, self.player, "hidden_items") == Toggle.option_true):
            set_hidden_item_rules(self.multiworld, self.player)
        if (get_option_value(self.multiworld, self.player, "npc_gifts") == Toggle.option_true):
            set_npc_gift_rules(self.multiworld, self.player)

        if (get_option_value(self.multiworld, self.player, "require_itemfinder") == Toggle.option_true):
            add_hidden_item_itemfinder_rules(self.multiworld, self.player)

    def generate_basic(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        locations = self.multiworld.get_locations(self.player)

        def convert_unrandomized_items_to_events(tag: str):
            for location in locations:
                if (location.tags != None and tag in location.tags):
                    location.place_locked_item(self.create_event(self.item_id_to_name[location.default_item_id]))
                    location.address = None
                    location.is_event = True

        if (get_option_value(self.multiworld, self.player, "badges") == Toggle.option_false):
            convert_unrandomized_items_to_events("Badge")
        if (get_option_value(self.multiworld, self.player, "hms") == Toggle.option_false):
            convert_unrandomized_items_to_events("HM")
        if (get_option_value(self.multiworld, self.player, "rods") == Toggle.option_false):
            convert_unrandomized_items_to_events("Rod")
        if (get_option_value(self.multiworld, self.player, "key_items") == Toggle.option_false):
            convert_unrandomized_items_to_events("KeyItem")


    def generate_output(self, output_directory: str):
        generate_output(self.multiworld, self.player, output_directory)


    def fill_slot_data(self):
        slot_data = self._get_pokemon_emerald_data()
        for option_name in options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> PokemonEmeraldItem:
        item_id = self.item_name_to_id[name]
        return PokemonEmeraldItem(
            name,
            get_item_classification(item_id),
            item_id,
            self.player
        )

    def create_item_by_id(self, item_id: int) -> PokemonEmeraldItem:
        return PokemonEmeraldItem(
            self.item_id_to_name[item_id],
            get_item_classification(item_id),
            item_id,
            self.player
        )

    def create_event(self, name: str) -> PokemonEmeraldItem:
        return PokemonEmeraldItem(
            name,
            ItemClassification.progression,
            None,
            self.player
        )
