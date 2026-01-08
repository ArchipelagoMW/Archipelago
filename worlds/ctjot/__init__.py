import logging
import threading
import typing
from typing import Callable

from BaseClasses import Item, Location, MultiWorld, Tutorial, Region, CollectionState, ItemClassification
from ..AutoWorld import World, WebWorld

from .Client import CTJoTSNIClient
from .Items import CTJoTItemManager
from .Locations import CTJoTLocationManager
from .Options import CTJoTOptions

ctjot_logger = logging.getLogger("Jets of Time")


class InvalidYamlException(Exception):
    """
    Custom exception thrown when we detect that the YAML was not
    generated using the mutlworld CTJoT web generator.
    """
    pass


class CTJoTWebWorld(WebWorld):
    settings_page = "https://multiworld.ctjot.com/"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Jets of Time multiworld.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Anguirel"]
    )]


class CTJoTWorld(World):
    """
    Jet of Time is an open world randomizer for the iconic JRPG Chrono Trigger.

    Players start with two characters and the winged Epoch and must journey through time finding
    additional characters and key items to save the world from the evil Lavos.
    """

    _item_manager = CTJoTItemManager()
    _location_manager = CTJoTLocationManager()

    game = "Chrono Trigger Jets of Time"
    options: CTJoTOptions
    options_dataclass = CTJoTOptions

    item_name_to_id = _item_manager.get_item_name_to_id_mapping()
    location_name_to_id = _location_manager.get_location_name_to_id_mapping()

    web = CTJoTWebWorld()

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name_available_event = threading.Event()

    def generate_early(self) -> None:
        """
        Validate the yaml was created from the CTJoT web generator
        """
        share_link = self.options.seed_share_link.value
        if "multiworld.ctjot.com" not in share_link:
            ctjot_logger.error("CTJoT YAML files must be generated from https://www.multiworld.ctjot.com")
            raise InvalidYamlException("CTJoT YAML files must be generated from https://www.multiworld.ctjot.com")

    def create_item(self, name: str) -> Item:
        """
        Create a CTJoT multiworld item.

        Overridden from World
        """
        return self._item_manager.create_item_by_name(name, self.player)

    def create_items(self) -> None:
        """
        Create items for the player from the passed in
        config data and append them to the multiworld item pool.

        Overridden from World
        """
        items_from_config = self.options.items.value
        bucket_fragments = self.options.bucket_fragments.value
        fragment_count = self.options.fragment_count.value
        game_mode = self.options.game_mode.value
        difficulty = self.options.item_difficulty.value
        tab_treasures = self.options.tab_treasures.value
        char_locations = self.options.char_locations.value

        items = []

        # Add the key items from the yaml
        for item in items_from_config:
            items.append(self._item_manager.create_item_by_id(item["id"], self.player))

        # Add fragments if bucket fragments are enabled
        if bucket_fragments and game_mode != "Lost worlds":
            for i in range(fragment_count):
                items.append(self.create_item("Fragment"))

        # If this is a Lost Worlds seed we may need to add some character specific items
        # Add these items as "useful" so they try to take up progression locations in
        # non chronosanity games
        if game_mode == "Lost worlds":
            for location in char_locations:
                if location["character"] == "Frog":
                    grand_leon = self._item_manager.get_item_data_by_name("Grand Leon")
                    hero_medal = self._item_manager.get_item_data_by_name("Hero Medal")

                    items.append(
                        self._item_manager.create_custom_item(
                            grand_leon.name, grand_leon.code, ItemClassification.useful, self.player))
                    items.append(
                        self._item_manager.create_custom_item(
                            hero_medal.name, hero_medal.code, ItemClassification.useful, self.player))
                elif location["character"] == "Robo":
                    robo_rbn = self._item_manager.get_item_data_by_name("Robo's Rbn")
                    items.append(
                        self._item_manager.create_custom_item(
                            robo_rbn.name, robo_rbn.code, ItemClassification.useful, self.player))

        all_locations = self._location_manager.get_location_ids(game_mode)

        # We need to pick the remaining items to fill out the item list
        # Shuffle the list of all locations traverse, placing an item for each one
        # until we have the same number of items as we do locations.
        # The shuffle ensures that we don't always skip the same locations at the end
        self.multiworld.random.shuffle(all_locations)

        num_items_to_place = len(all_locations) - len(items)
        for i in range(num_items_to_place):
            item = self._item_manager.get_random_item_for_location(
                all_locations[i], difficulty, tab_treasures, self.multiworld, self.player)
            items.append(item)

        # Add the selected items to the multiworld item pool
        self.multiworld.itempool += items

    def create_regions(self) -> None:
        """
        Set up the locations and rules for this player.

        Region/location data is defined in the yaml to match the chosen flag set
        Pull this data from the yaml and set up the associated AP structures

        Overridden from World
        """
        # Get region/location data from the yaml
        regions_from_config = self.options.region_list.value
        char_locations_from_config = self.options.char_locations.value
        victory_rules_from_config = self.options.victory.value
        rules_from_config = self.options.rules.value
        game_mode = self.options.game_mode.value
        menu_region = Region("Menu", self.player, self.multiworld)

        # For now just shove all locations into the menu region
        # TODO: Add separate regions?
        for region_name, location_list in regions_from_config.items():
            access_rule = self._get_access_rule(rules_from_config[region_name])
            for location_name in location_list:
                location = self._location_manager.get_location(self.player, location_name, menu_region)
                location.access_rule = access_rule
                menu_region.locations.append(location)

        # Handle event locations for character pickups
        for char_location in char_locations_from_config:
            location_name = char_location["name"]
            character_name = char_location["character"]
            location = Location(self.player, location_name, None, menu_region)
            location.event = True
            # Add character here as a locked item.
            location.place_locked_item(
                self._item_manager.create_event_item(character_name, self.player))
            location.access_rule = self._get_access_rule(rules_from_config[location_name])
            menu_region.locations.append(location)

        # Add filler locations for non-progression items
        # This will do nothing in chronosanity games, but will fill in all the missing locations
        # with filler items in non-chronosanity games.
        self._location_manager.add_filler_locations(regions_from_config, game_mode, self.player, menu_region)

        # Add victory condition event
        victory_location = Location(self.player, "Victory", None, menu_region)
        victory_location.event = True
        victory_location.access_rule = self._get_access_rule(victory_rules_from_config)
        victory_location.place_locked_item(self._item_manager.create_event_item("Victory", self.player))
        menu_region.locations.append(victory_location)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        self.multiworld.regions += [menu_region]

    def get_filler_item_name(self) -> str:
        """
        Get a random filler item.

        Overridden from World
        """
        return self.multiworld.random.choice(self._item_manager.get_junk_fill_items())

    def modify_multidata(self, multidata: dict):
        import base64
        player_name = self.multiworld.player_name[self.player]
        if player_name and player_name != "":
            new_name = base64.b64encode(bytes(player_name.encode("ascii"))).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def _get_access_rule(self, access_rules: list[list[str]]) -> Callable[[CollectionState], bool]:
        """
        Create an access rule function from yaml access_rule data.

        :param access_rules: A list contains lists of item/character requirements for this access rule
        :return: Callable access rule based on the list of requirements
        """
        def can_access(state: CollectionState) -> bool:
            # No access rules means this is sphere 1
            if len(access_rules) == 0:
                return True

            # loop through each access rule for this location
            for rule in access_rules:
                has_access = True
                for item in rule:
                    if not state.has(item, self.player):
                        has_access = False
                        break
                # Check if we have all the items from the rule
                if has_access:
                    return True

            # We didn't satisfy any of the access rules
            return False

        return can_access
