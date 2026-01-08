import logging
import math
import settings

from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple, TextIO

from BaseClasses import Item, ItemClassification, Location, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .data_funcs import (
    item_names_to_id,
    location_names_to_id,
    item_groups,
    location_groups,
    id_to_goals,
    access_rule_for,
)

from .data.item_data import KeymastersKeepItemData, item_data
from .data.location_data import KeymastersKeepLocationData, location_data

from .data.mapping_data import (
    region_to_trial_locations,
    region_to_unlock_location_and_item,
    shop_to_shop_item_locations,
)

from .enums import (
    KeymastersKeepItems,
    KeymastersKeepGoals,
    KeymastersKeepLocations,
    KeymastersKeepRegions,
    KeymastersKeepShops,
    KeymastersKeepShopkeepers,
    KeymastersKeepTags,
)

from .game_objective_generator import GameObjectiveGenerator, GameObjectiveGeneratorData

from .options import KeymastersKeepOptions, option_groups


class KeymastersKeepItem(Item):
    game = "Keymaster's Keep"


class KeymastersKeepLocation(Location):
    game = "Keymaster's Keep"


class KeymastersKeepSettings(settings.Group):
    class ClientUnicodeFontName(str):
        """
        Determines the name of the locally installed font to use for parts of the client that may need to display
        Unicode / special characters (e.g. Song names in Japanese / Chinese).

        The default is Roboto, which is the font used by all Archipelago clients. It doesn't support Unicode / special
        characters.

        Only TTF fonts are supported. You will need to use the full name of the font file without the extension. Example:
        "NotoSansJP-Regular" for NotoSansJP-Regular.ttf.

        Using an invalid font name here will crash / hang the client on launch. Be careful!
        """

    class ClientUnicodeFontSize(int):
        pass

    client_unicode_font_name: ClientUnicodeFontName = ClientUnicodeFontName("Roboto")
    client_unicode_font_size: ClientUnicodeFontSize = ClientUnicodeFontSize(15)


class KeymastersKeepWebWorld(WebWorld):
    theme: str = "stone"

    tutorials: List[Tutorial] = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Keymaster's Keep randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serpent.AI"],
        )
    ]

    # Option presets here...
    option_groups = option_groups


class KeymastersKeepWorld(World):
    """
    Embark on a quest through the Keymaster's Keep, a mysterious castle where every door and passage hides a series of
    video game chalenges, and only the right keys can unlock the path forward. Complete challenges, find keys, uncover
    artifacts of resolve, and face the ultimate trial to claim victory.
    """

    options_dataclass = KeymastersKeepOptions
    options: KeymastersKeepOptions

    settings_key = "keymasters_keep_options"
    settings: ClassVar[KeymastersKeepSettings]

    game = "Keymaster's Keep"

    item_name_to_id = item_names_to_id()
    location_name_to_id = location_names_to_id()

    item_name_groups = item_groups()
    location_name_groups = location_groups()

    required_client_version: Tuple[int, int, int] = (0, 5, 1)

    web = KeymastersKeepWebWorld()

    area_game_optional_constraints: Dict[str, List[str]]
    area_games: Dict[str, str]
    area_trial_game_objectives: Dict[str, List[str]]
    area_trials: Dict[KeymastersKeepRegions, List[KeymastersKeepLocationData]]
    area_trials_maximum: int
    area_trials_minimum: int
    artifacts_of_resolve_required: int
    artifacts_of_resolve_total: int
    excluded_games_difficult_objectives: List[str]
    excluded_games_time_consuming_objectives: List[str]
    filler_item_names: List[str] = item_groups()["Filler"]
    game_medley_game_selection: List[str]
    game_medley_mode: bool
    game_medley_percentage_chance: int
    game_selection: List[str]
    goal: KeymastersKeepGoals
    goal_game: str
    goal_game_optional_constraints: List[str]
    goal_trial_game_objective: str
    hints_reveal_objectives: bool
    include_adult_only_or_unrated_games: bool
    include_difficult_objectives: bool
    include_modern_console_games: bool
    include_time_consuming_objectives: bool
    keep_areas: int
    keep_data: Any
    lock_combinations: Dict[KeymastersKeepRegions, Optional[List[KeymastersKeepItems]]]
    lock_magic_keys_maximum: int
    lock_magic_keys_minimum: int
    magic_keys_required: int
    magic_keys_total: int
    selected_areas: List[KeymastersKeepRegions]
    selected_magic_keys: List[KeymastersKeepItems]
    shop_data: Dict[KeymastersKeepRegions, Any]
    shop_hints: bool
    shop_items_maximum: int
    shop_items_minimum: int
    shop_items_progression_percentage_chance: int
    shops: bool
    shops_percentage_chance: int
    unlocked_areas: int
    unused_magic_keys: Set[KeymastersKeepItems]
    unused_relics: Set[KeymastersKeepItems]
    used_magic_keys: Set[KeymastersKeepItems]
    used_relics: Set[KeymastersKeepItems]

    def generate_early(self) -> None:
        self.goal = id_to_goals()[self.options.goal.value]

        self.goal_game = None
        self.goal_game_optional_constraints = None
        self.goal_trial_game_objective = None

        self.artifacts_of_resolve_required = self.options.artifacts_of_resolve_required.value
        self.artifacts_of_resolve_total = self.options.artifacts_of_resolve_total.value

        if self.artifacts_of_resolve_required > self.artifacts_of_resolve_total:
            self.artifacts_of_resolve_total = self.artifacts_of_resolve_required

            if self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
                logging.warning(
                    f"Keymaster's Keep: {self.player_name} has more required artifacts than total artifacts. Using "
                    "required amount for total."
                )

        self.magic_keys_required = self.options.magic_keys_required.value
        self.magic_keys_total = self.options.magic_keys_total.value

        if self.magic_keys_required > self.magic_keys_total:
            self.magic_keys_total = self.magic_keys_required

            if self.goal == KeymastersKeepGoals.MAGIC_KEY_HEIST:
                logging.warning(
                    f"Keymaster's Keep: {self.player_name} has more required magic keys than total magic keys. Using "
                    "required amount for total."
                )

        self.keep_areas = self.options.keep_areas.value

        self.unlocked_areas = self.options.unlocked_areas.value

        self.lock_magic_keys_minimum = self.options.lock_magic_keys_minimum.value
        self.lock_magic_keys_maximum = self.options.lock_magic_keys_maximum.value

        if self.lock_magic_keys_minimum > self.lock_magic_keys_maximum:
            self.lock_magic_keys_maximum = self.lock_magic_keys_minimum

            logging.warning(
                f"Keymaster's Keep: {self.player_name} has a minimum lock magic keys value greater than the maximum. "
                "Using minimum value for maximum."
            )

        self.area_trials_minimum = self.options.area_trials_minimum.value
        self.area_trials_maximum = self.options.area_trials_maximum.value

        if self.area_trials_minimum > self.area_trials_maximum:
            self.area_trials_maximum = self.area_trials_minimum

            logging.warning(
                f"Keymaster's Keep: {self.player_name} has a minimum area trials value greater than the maximum. "
                "Using minimum value for maximum."
            )

        self.shops = bool(self.options.shops_)
        self.shops_percentage_chance = self.options.shops_percentage_chance.value

        self.shop_items_minimum = self.options.shop_items_minimum.value
        self.shop_items_maximum = self.options.shop_items_maximum.value

        if self.shop_items_minimum > self.shop_items_maximum:
            self.shop_items_maximum = self.shop_items_minimum

            logging.warning(
                f"Keymaster's Keep: {self.player_name} has a minimum shop items value greater than the maximum. "
                "Using minimum value for maximum."
            )

        self.shop_items_progression_percentage_chance = self.options.shop_items_progression_percentage_chance.value
        self.shop_hints = bool(self.options.shop_hints)

        smallest_possible_trial_count: int = self.area_trials_minimum * self.keep_areas

        shop_count: int = 0
        smallest_possible_shop_item_count: int = 0

        if self.shops:
            shop_count = math.ceil((self.shops_percentage_chance / 100.0) * self.keep_areas)
            smallest_possible_shop_item_count = self.shop_items_minimum * shop_count

            smallest_possible_trial_count = self.area_trials_minimum * (self.keep_areas - shop_count)
            smallest_possible_trial_count += smallest_possible_shop_item_count

        locations_needed: int = self.magic_keys_total

        if self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            locations_needed += self.artifacts_of_resolve_total

        if self.shops:
            locations_needed += 50  # We add unique relics to the pool when shops are enabled

        area_trials_range_modified: bool = False

        if locations_needed > smallest_possible_trial_count:
            area_trials_range_modified = True

            while True:
                self.area_trials_minimum += 1

                if self.area_trials_maximum < self.area_trials_minimum:
                    self.area_trials_maximum = self.area_trials_minimum

                smallest_possible_trial_count = self.area_trials_minimum * self.keep_areas

                if self.shops:
                    smallest_possible_trial_count = self.area_trials_minimum * (self.keep_areas - shop_count)
                    smallest_possible_trial_count += smallest_possible_shop_item_count

                if smallest_possible_trial_count >= locations_needed:
                    break

        if area_trials_range_modified:
            logging.warning(
                f"Keymaster's Keep: {self.player_name} has had their area trials range modified to ensure enough "
                "trials are available to generate successfully."
            )

        self._generate_keep()

        self.game_medley_mode = bool(self.options.game_medley_mode)
        self.game_medley_percentage_chance = self.options.game_medley_percentage_chance.value
        self.game_medley_game_selection = list(self.options.game_medley_game_selection.value)

        self.game_selection = list(self.options.game_selection.value)

        self.include_adult_only_or_unrated_games = bool(self.options.include_adult_only_or_unrated_games)
        self.include_modern_console_games = bool(self.options.include_modern_console_games)

        self.include_difficult_objectives = bool(self.options.include_difficult_objectives)
        self.excluded_games_difficult_objectives = list(self.options.excluded_games_difficult_objectives.value)

        self.include_time_consuming_objectives = bool(self.options.include_time_consuming_objectives)

        self.excluded_games_time_consuming_objectives = list(
            self.options.excluded_games_time_consuming_objectives.value
        )

        self.hints_reveal_objectives = bool(self.options.hints_reveal_objectives)

        self._generate_game_objective_data()

    def create_regions(self) -> None:
        #### Menu -> Keymaster's Keep
        region_menu: Region = Region(KeymastersKeepRegions.MENU.value, self.player, self.multiworld)

        region_keymasters_keep: Region = Region(
            KeymastersKeepRegions.KEYMASTERS_KEEP.value, self.player, self.multiworld
        )

        region_menu.connect(region_keymasters_keep)

        self.multiworld.regions.append(region_menu)

        #### Keymaster's Keep
        region_keymasters_keep.connect(region_menu)

        ### Keymaster's Keep -> Keymaster's Keep Areas
        area: KeymastersKeepRegions
        for area in self.selected_areas:
            ## Unlock Location
            location_enum_item: KeymastersKeepLocations
            item_enum_item: KeymastersKeepItems

            location_enum_item, item_enum_item = region_to_unlock_location_and_item[area]
            data: KeymastersKeepLocationData = location_data[location_enum_item]

            unlock_location: KeymastersKeepLocation = KeymastersKeepLocation(
                self.player,
                location_enum_item.value,
                data.archipelago_id,
                region_keymasters_keep,
            )

            access_rule: Optional[str] = access_rule_for(self.lock_combinations[area], self.player)

            if access_rule is not None:
                unlock_location.access_rule = eval(access_rule)

            unlock_location.place_locked_item(self.create_item(item_enum_item.value))

            region_keymasters_keep.locations.append(unlock_location)

            ## Entrance
            region_area: Region = Region(area.value, self.player, self.multiworld)
            region_keymasters_keep.connect(region_area, rule=eval(access_rule_for([item_enum_item], self.player)))

            ## Keymaster's Keep Area
            region_area.connect(region_keymasters_keep)

            # Assign Trial Locations
            if area in self.area_trials:
                trial: KeymastersKeepLocationData
                for trial in self.area_trials[area]:
                    trial_location: KeymastersKeepLocation = KeymastersKeepLocation(
                        self.player,
                        trial.name,
                        trial.archipelago_id,
                        region_area,
                    )

                    region_area.locations.append(trial_location)

            # Handle Shops
            if area in self.shop_data:
                shop: KeymastersKeepShops = self.shop_data[area]["shop"]

                region_shop_enum_item: KeymastersKeepRegions = KeymastersKeepRegions(f"Shop: {shop.value}")
                region_shop: Region = Region(region_shop_enum_item.value, self.player, self.multiworld)

                region_area.connect(region_shop)
                region_shop.connect(region_area)

                i: int
                shop_item_data: Tuple[KeymastersKeepLocationData, KeymastersKeepItems]
                for i, shop_item_data in enumerate(self.shop_data[area]["shop_items"]):
                    data, relic = shop_item_data

                    shop_item_location: KeymastersKeepLocation = KeymastersKeepLocation(
                        self.player,
                        data.name,
                        data.archipelago_id,
                        region_shop,
                    )

                    shop_item_location.access_rule = eval(access_rule_for([relic], self.player))

                    region_shop.locations.append(shop_item_location)

                    if self.random.randint(1, 100) <= self.shop_items_progression_percentage_chance:
                        self.options.priority_locations.value.add(data.name)

                self.multiworld.regions.append(region_shop)

            self.multiworld.regions.append(region_area)

        ### Goal
        region_endgame: Region = Region(KeymastersKeepRegions.ENDGAME.value, self.player, self.multiworld)

        location_victory: KeymastersKeepLocation = KeymastersKeepLocation(
            self.player,
            "Victory",
            None,
            region_endgame,
        )

        location_victory.place_locked_item(
            KeymastersKeepItem(
                "Victory",
                ItemClassification.progression,
                None,
                self.player,
            )
        )

        region_endgame.locations.append(location_victory)

        if self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            # Unlock Location
            unlock_location: KeymastersKeepLocation = KeymastersKeepLocation(
                self.player,
                KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_UNLOCK.value,
                location_data[KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_UNLOCK].archipelago_id,
                region_keymasters_keep,
            )

            unlock_location.place_locked_item(
                self.create_item(KeymastersKeepItems.UNLOCK_THE_KEYMASTERS_CHALLENGE_CHAMBER.value)
            )

            unlock_location.access_rule = lambda state: state.has(
                KeymastersKeepItems.ARTIFACT_OF_RESOLVE.value,
                self.player,
                count=self.artifacts_of_resolve_required
            )

            region_keymasters_keep.locations.append(unlock_location)

            # Challenge Chamber
            region_challenge_chamber: Region = Region(
                KeymastersKeepRegions.THE_KEYMASTERS_CHALLENGE_CHAMBER.value, self.player, self.multiworld
            )

            region_keymasters_keep.connect(
                region_challenge_chamber,
                rule=eval(access_rule_for([KeymastersKeepItems.UNLOCK_THE_KEYMASTERS_CHALLENGE_CHAMBER], self.player))
            )

            region_challenge_chamber.connect(region_keymasters_keep)

            location_challenge: KeymastersKeepLocation = KeymastersKeepLocation(
                self.player,
                KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_VICTORY.value,
                location_data[KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_VICTORY].archipelago_id,
                region_challenge_chamber,
            )

            location_challenge.place_locked_item(
                self.create_item(KeymastersKeepItems.KEYMASTERS_KEEP_CHALLENGE_COMPLETE.value)
            )

            region_challenge_chamber.locations.append(location_challenge)

            # Endgame
            region_challenge_chamber.connect(
                region_endgame,
                rule=eval(access_rule_for([KeymastersKeepItems.KEYMASTERS_KEEP_CHALLENGE_COMPLETE], self.player))
            )

            region_endgame.connect(region_challenge_chamber)

            self.multiworld.regions.append(region_challenge_chamber)
        elif self.goal == KeymastersKeepGoals.MAGIC_KEY_HEIST:
            # Endgame
            region_keymasters_keep.connect(
                region_endgame,
                rule=eval(access_rule_for(self.selected_magic_keys, self.player)),
            )

            region_endgame.connect(region_keymasters_keep)

        self.multiworld.regions.append(region_keymasters_keep)
        self.multiworld.regions.append(region_endgame)

    def create_items(self) -> None:
        item_pool: List[KeymastersKeepItem] = list()

        # Magic Keys
        magic_key: KeymastersKeepItems
        for magic_key in self.selected_magic_keys:
            item: KeymastersKeepItem = self.create_item(magic_key.value)

            if magic_key in self.unused_magic_keys and self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
                item.classification = ItemClassification.filler

            item_pool.append(item)

        # Relics
        if self.shops:
            relic: KeymastersKeepItems
            for relic in (self.unused_relics | self.used_relics):
                item: KeymastersKeepItem = self.create_item(relic.value)

                if relic in self.unused_relics:
                    item.classification = ItemClassification.filler

                item_pool.append(item)

        # Artifacts of Resolve
        if self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            i: int
            for i in range(self.artifacts_of_resolve_total):
                item: KeymastersKeepItem = self.create_item(KeymastersKeepItems.ARTIFACT_OF_RESOLVE.value)

                if i >= self.artifacts_of_resolve_required:
                    item.classification = ItemClassification.useful

                item_pool.append(item)

        # Filler
        total_location_count: int = len(self.multiworld.get_unfilled_locations(self.player))
        to_fill_location_count: int = total_location_count - len(item_pool)

        item_pool += [self.create_filler() for _ in range(to_fill_location_count)]

        self.multiworld.itempool += item_pool

    def create_item(self, name: str) -> KeymastersKeepItem:
        data: KeymastersKeepItemData = item_data[KeymastersKeepItems(name)]

        return KeymastersKeepItem(
            name,
            data.classification,
            data.archipelago_id,
            self.player,
        )

    def generate_basic(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "area_game_optional_constraints": self.area_game_optional_constraints,
            "area_games": self.area_games,
            "area_trial_game_objectives": self.area_trial_game_objectives,
            "area_trials": {area.value: [trial.name for trial in trials] for area, trials in self.area_trials.items()},
            "area_trials_maximum": self.area_trials_maximum,
            "area_trials_minimum": self.area_trials_minimum,
            "artifacts_of_resolve_required": self.artifacts_of_resolve_required,
            "artifacts_of_resolve_total": self.artifacts_of_resolve_total,
            "game_medley_mode": self.game_medley_mode,
            "game_medley_percentage_chance": self.game_medley_percentage_chance,
            "goal": self.goal.value,
            "goal_game": self.goal_game,
            "goal_game_optional_constraints": self.goal_game_optional_constraints,
            "goal_trial_game_objective": self.goal_trial_game_objective,
            "hints_reveal_objectives": self.hints_reveal_objectives,
            "include_adult_only_or_unrated_games": self.include_adult_only_or_unrated_games,
            "include_difficult_objectives": self.include_difficult_objectives,
            "include_modern_console_games": self.include_modern_console_games,
            "include_time_consuming_objectives": self.include_time_consuming_objectives,
            "lock_combinations": dict(),
            "lock_magic_keys_maximum": self.lock_magic_keys_maximum,
            "lock_magic_keys_minimum": self.lock_magic_keys_minimum,
            "magic_keys_required": self.magic_keys_required,
            "magic_keys_total": self.magic_keys_total,
            "selected_magic_keys": [key.value for key in self.selected_magic_keys],
            "shop_data": dict(),
            "shop_hints": self.shop_hints,
            "shop_items_maximum": self.shop_items_maximum,
            "shop_items_minimum": self.shop_items_minimum,
            "shop_items_progression_percentage_chance": self.shop_items_progression_percentage_chance,
            "shops": self.shops,
            "shops_percentage_chance": self.shops_percentage_chance,
            "unlocked_areas": self.unlocked_areas,
            "used_magic_keys": [key.value for key in self.used_magic_keys],
        }

        area: KeymastersKeepRegions
        keys: Optional[List[KeymastersKeepItems]]
        for area, keys in self.lock_combinations.items():
            if keys is None:
                slot_data["lock_combinations"][area.value] = None
                continue

            slot_data["lock_combinations"][area.value] = [key.value for key in keys]

        if self.shops:
            shop_area: KeymastersKeepRegions
            shop_data: Dict[str, Any]
            for shop_area, shop_data in self.shop_data.items():
                slot_data["shop_data"][shop_area.value] = {
                    "shop": shop_data["shop"].value,
                    "shopkeeper": shop_data["shopkeeper"].value,
                    "shop_items": dict(),
                }

                shop_item_data: Tuple[KeymastersKeepLocationData, KeymastersKeepItems]
                for shop_item_data in shop_data["shop_items"]:
                    data, relic = shop_item_data

                    slot_data["shop_data"][shop_area.value]["shop_items"][data.name] = {
                        "archipelago_id": data.archipelago_id,
                        "relic": {"archipelago_id": item_data[relic].archipelago_id, "name": relic.value},
                        "item": dict(),
                    }

                    location: KeymastersKeepLocation = self.get_location(data.name)

                    slot_data["shop_data"][shop_area.value]["shop_items"][data.name]["item"]["name"] = (
                        location.item.name
                    )

                    slot_data["shop_data"][shop_area.value]["shop_items"][data.name]["item"]["classification"] = (
                        location.item.classification.value
                    )

                    slot_data["shop_data"][shop_area.value]["shop_items"][data.name]["item"]["player"] = (
                        location.item.player
                    )

        return slot_data

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        data: Dict[int, str] = dict()

        if self.hints_reveal_objectives:
            area: KeymastersKeepRegions
            trial_locations: List[KeymastersKeepLocationData]
            for area, trial_locations in self.area_trials.items():
                trial_location: KeymastersKeepLocationData
                for trial_location in trial_locations:
                    data[trial_location.archipelago_id] = (
                        f"{self.area_games[area.value]}: {self.area_trial_game_objectives[trial_location.name]}"
                    )

        if self.shops:
            shop_area: KeymastersKeepRegions
            shop_data: Dict[str, Any]
            for shop_area, shop_data in self.shop_data.items():
                shop_item_data: Tuple[KeymastersKeepLocationData, KeymastersKeepItems]
                for shop_item_data in shop_data["shop_items"]:
                    data[shop_item_data[0].archipelago_id] = f"{shop_area.value} - {shop_data['shop'].value}"

        hint_data[self.player] = data

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        # Lock Combinations
        spoiler_handle.write("\nRequired Keys:")

        area: KeymastersKeepRegions
        keys: Optional[List[KeymastersKeepItems]]
        for area, keys in self.lock_combinations.items():
            if keys is None:
                spoiler_handle.write(f"\n    {area.value}: Unlocked")
                continue

            spoiler_handle.write(f"\n    {area.value}: {', '.join(key.value for key in keys)}")

        # Shops
        if self.shops:
            spoiler_handle.write("\n\nShops:")

            shop_area: KeymastersKeepRegions
            shop_data: Dict[str, Any]
            for shop_area, shop_data in self.shop_data.items():
                shop: KeymastersKeepShops = shop_data["shop"]
                shopkeeper: KeymastersKeepShopkeepers = shop_data["shopkeeper"]

                spoiler_handle.write(f"\n    {shop_area.value} - {shop.value} (Shopkeeper: {shopkeeper.value})")

                shop_item_data: Tuple[KeymastersKeepLocationData, KeymastersKeepItems]
                for shop_item_data in shop_data["shop_items"]:
                    data, relic = shop_item_data
                    spoiler_handle.write(f"\n        {data.name.split(' - ')[1]} - Cost: 1x {relic.value}")

        # Area Games
        spoiler_handle.write("\n\nArea Games:")

        area: str
        game: str
        for area, game in self.area_games.items():
            spoiler_handle.write(f"\n    {area}: {game}")

        # Area Trial Game Objectives
        spoiler_handle.write("\n\nArea Trial Game Objectives:")

        trial: str
        objective: str
        for trial, objective in self.area_trial_game_objectives.items():
            spoiler_handle.write(f"\n    {trial}: {objective}")

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_item_names)

    def _generate_keep(self) -> None:
        # Select Areas
        potential_areas: List[KeymastersKeepRegions] = list()

        excluded_areas: Tuple[KeymastersKeepRegions, ...] = (
            KeymastersKeepRegions.ENDGAME,
            KeymastersKeepRegions.THE_KEYMASTERS_CHALLENGE_CHAMBER,
            KeymastersKeepRegions.KEYMASTERS_KEEP,
            KeymastersKeepRegions.MENU,
        )

        area: KeymastersKeepRegions
        for area in KeymastersKeepRegions:
            if area not in excluded_areas and not area.name.startswith("SHOP_"):
                potential_areas.append(area)

        self.selected_areas = self.random.sample(potential_areas, self.keep_areas)

        # Select Magic Keys
        potential_magic_keys: List[KeymastersKeepItemData] = list()

        item: KeymastersKeepItems
        data: KeymastersKeepItemData
        for item, data in item_data.items():
            if KeymastersKeepTags.KEYS in data.tags:
                potential_magic_keys.append(item)

        self.selected_magic_keys = self.random.sample(potential_magic_keys, self.magic_keys_total)

        # Generate Lock Combinations
        self.lock_combinations = dict()
        used_keys: Set[KeymastersKeepItems] = set()

        i: int
        area: KeymastersKeepRegions
        for i, area in enumerate(self.selected_areas):
            if i < self.unlocked_areas:
                self.lock_combinations[area] = None
                continue

            key_count: int = self.random.randint(self.lock_magic_keys_minimum, self.lock_magic_keys_maximum)

            # Conditionally force single key locks to prevent overly restrictive starts and generation failures
            if i < self.unlocked_areas + (5 - self.unlocked_areas):
                key_count = 1

            keys_to_lock: List[KeymastersKeepItems] = self.random.sample(self.selected_magic_keys, key_count)

            key: KeymastersKeepItems
            for key in keys_to_lock:
                used_keys.add(key)

            self.lock_combinations[area] = keys_to_lock

        self.used_magic_keys = used_keys
        self.unused_magic_keys = set(self.selected_magic_keys) - used_keys

        # Determine Shop Areas
        self.shop_data = dict()
        self.area_shop_items = dict()

        if self.shops:
            self.used_relics = set()

            shuffled_shops: List[KeymastersKeepShops] = list(KeymastersKeepShops)
            self.random.shuffle(shuffled_shops)

            shuffled_shopkeepers: List[KeymastersKeepShopkeepers] = list(KeymastersKeepShopkeepers)
            self.random.shuffle(shuffled_shopkeepers)

            shuffled_relics: List[KeymastersKeepItems] = list(KeymastersKeepItems)
            shuffled_relics = [relic for relic in shuffled_relics if relic.name.startswith("RELIC_")]
            self.random.shuffle(shuffled_relics)

            shop_count: int = 0
            relic_index: int = 0

            i: int
            area: KeymastersKeepRegions
            for i, area in enumerate(self.selected_areas):
                # Don't assign shops to the first 3 areas
                if i < 3:
                    continue

                if self.random.randint(1, 100) <= self.shops_percentage_chance:
                    self.shop_data[area] = {
                        "shop": shuffled_shops[shop_count],
                        "shopkeeper": shuffled_shopkeepers[shop_count],
                        "shop_items": list(),
                    }

                    possible_shop_item_locations: List[KeymastersKeepLocationData] = location_data[
                        shop_to_shop_item_locations[self.shop_data[area]["shop"]]
                    ]

                    shop_item_count: int = self.random.randint(self.shop_items_minimum, self.shop_items_maximum)

                    shop_item_location_data: KeymastersKeepLocationData
                    for shop_item_location_data in possible_shop_item_locations[:shop_item_count]:
                        self.shop_data[area]["shop_items"].append(
                            (shop_item_location_data, shuffled_relics[relic_index])
                        )

                        self.used_relics.add(shuffled_relics[relic_index])
                        relic_index += 1

                    shop_count += 1

                if shop_count >= 10:
                    break

            self.unused_relics = set(shuffled_relics) - self.used_relics

        # Assign Trials to Areas
        self.area_trials = dict()

        area: KeymastersKeepRegions
        for area in self.selected_areas:
            if area in self.shop_data:
                continue

            possible_trials: List[KeymastersKeepLocationData] = location_data[region_to_trial_locations[area]]
            trial_count: int = self.random.randint(self.area_trials_minimum, self.area_trials_maximum)

            self.area_trials[area] = self.random.sample(possible_trials, trial_count)

    def _generate_game_objective_data(self) -> None:
        game_selection: List[str] = sorted(self.game_selection[:])

        generator: GameObjectiveGenerator = GameObjectiveGenerator(
            game_selection,
            self.game_medley_game_selection,
            self.game_medley_mode,
            self.include_adult_only_or_unrated_games,
            self.include_modern_console_games,
            self.include_difficult_objectives,
            self.include_time_consuming_objectives,
            self.options
        )

        plan: List[int] = list()

        area: KeymastersKeepRegions
        trial_locations: List[KeymastersKeepLocationData]
        for area, trial_locations in self.area_trials.items():
            plan.append(len(trial_locations))

        if self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            plan.append(1)

        game_objective_data: GameObjectiveGeneratorData = generator.generate_from_plan(
            plan,
            self.random,
            self.include_difficult_objectives,
            self.excluded_games_difficult_objectives,
            self.include_time_consuming_objectives,
            self.excluded_games_time_consuming_objectives,
            self.game_medley_mode,
            self.game_medley_percentage_chance,
        )

        self.area_games = dict()
        self.area_game_optional_constraints = dict()

        i: int
        for i, area in enumerate(self.area_trials.keys()):
            self.area_games[area.value] = game_objective_data[i][0].name
            self.area_game_optional_constraints[area.value] = game_objective_data[i][1]

        self.area_trial_game_objectives = dict()

        for i, (area, trial_locations) in enumerate(self.area_trials.items()):
            ii: int
            trial_location: KeymastersKeepLocationData
            for ii, trial_location in enumerate(trial_locations):
                self.area_trial_game_objectives[trial_location.name] = game_objective_data[i][2][ii]

        if self.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            self.goal_game = game_objective_data[-1][0].name
            self.goal_game_optional_constraints = game_objective_data[-1][1]
            self.goal_trial_game_objective = game_objective_data[-1][2][0]
