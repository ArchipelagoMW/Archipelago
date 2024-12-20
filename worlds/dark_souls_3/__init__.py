# world/dark_souls_3/__init__.py
from collections.abc import Sequence
from collections import defaultdict
import json
from logging import warning
from typing import cast, Any, Callable, Dict, Set, List, Optional, TextIO, Union

from BaseClasses import CollectionState, MultiWorld, Region, Location, LocationProgressType, Entrance, Tutorial, ItemClassification

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import CollectionRule, ItemRule, add_rule, add_item_rule

from .Bosses import DS3BossInfo, all_bosses, default_yhorm_location
from .Items import DarkSouls3Item, DS3ItemData, Infusion, UsefulIf, filler_item_names, item_descriptions, item_dictionary, item_name_groups
from .Locations import DarkSouls3Location, DS3LocationData, location_tables, location_descriptions, location_dictionary, location_name_groups, region_order
from .Options import DarkSouls3Options, option_groups


class DarkSouls3Web(WebWorld):
    bug_report_page = "https://github.com/Marechal-L/Dark-Souls-III-Archipelago-client/issues"
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Dark Souls III randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Marech"]
    )

    setup_fr = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Marech"]
    )

    tutorials = [setup_en, setup_fr]
    option_groups = option_groups
    item_descriptions = item_descriptions
    rich_text_options_doc = True


class DarkSouls3World(World):
    """
    Dark souls III is an Action role-playing game and is part of the Souls series developed by FromSoftware.
    Played from a third-person perspective, players have access to various weapons, armour, magic, and consumables that
    they can use to fight their enemies.
    """

    game = "Dark Souls III"
    options: DarkSouls3Options
    options_dataclass = DarkSouls3Options
    web = DarkSouls3Web()
    base_id = 100000
    required_client_version = (0, 4, 2)
    item_name_to_id = {data.name: data.ap_code for data in item_dictionary.values() if data.ap_code is not None}
    location_name_to_id = {
        location.name: location.ap_code
        for locations in location_tables.values()
        for location in locations
        if location.ap_code is not None
    }
    location_name_groups = location_name_groups
    item_name_groups = item_name_groups
    location_descriptions = location_descriptions
    item_descriptions = item_descriptions

    yhorm_location: DS3BossInfo = default_yhorm_location
    """If enemy randomization is enabled, this is the boss who Yhorm the Giant should replace.
    
    This is used to determine where the Storm Ruler can be placed.
    """

    all_excluded_locations: Set[str] = set()
    """This is the same value as `self.options.exclude_locations.value` initially, but if
    `options.exclude_locations` gets cleared due to `excluded_locations: allow_useful` this still
    holds the old locations so we can ensure they don't get necessary items.
    """

    local_itempool: List[DarkSouls3Item] = []
    """The pool of all items within this particular world. This is a subset of
    `self.multiworld.itempool`."""

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.all_excluded_locations = set()

    def generate_early(self) -> None:
        self.created_regions = set()
        self.all_excluded_locations.update(self.options.exclude_locations.value)

        # Inform Universal Tracker where Yhorm is being randomized to.
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Dark Souls III" in self.multiworld.re_gen_passthrough:
                if self.multiworld.re_gen_passthrough["Dark Souls III"]["options"]["randomize_enemies"]:
                    yhorm_data = self.multiworld.re_gen_passthrough["Dark Souls III"]["yhorm"]
                    for boss in all_bosses:
                        if yhorm_data.startswith(boss.name):
                            self.yhorm_location = boss

        # Randomize Yhorm manually so that we know where to place the Storm Ruler.
        elif self.options.randomize_enemies:
            self.yhorm_location = self.random.choice(
                [boss for boss in all_bosses if self._allow_boss_for_yhorm(boss)])

            # If Yhorm is early, make sure the Storm Ruler is easily available to avoid BK
            # Iudex Gundyr is handled separately in _fill_local_items
            if (
                self.yhorm_location.name == "Vordt of the Boreal Valley" or (
                    self.yhorm_location.name == "Dancer of the Boreal Valley" and
                    not self.options.late_basin_of_vows
                )
            ):
                self.multiworld.local_early_items[self.player]["Storm Ruler"] = 1

    def _allow_boss_for_yhorm(self, boss: DS3BossInfo) -> bool:
        """Returns whether boss is a valid location for Yhorm in this seed."""

        if not self.options.enable_dlc and boss.dlc: return False

        if not self._is_location_available("PC: Storm Ruler - boss room"):
            # If the Storm Ruler isn't randomized, make sure the player can get to the normal Storm
            # Ruler location before they need to get through Yhorm.
            if boss.before_storm_ruler: return False

            # If the Small Doll also wasn't randomized, make sure Yhorm isn't blocking access to it
            # or it won't be possible to get into Profaned Capital before beating him.
            if (
                not self._is_location_available("CD: Small Doll - boss drop")
                and boss.name in {"Crystal Sage", "Deacons of the Deep"}
            ):
                return False

        if boss.name != "Iudex Gundyr": return True

        # Cemetery of Ash has very few locations and all of them are excluded by default, so only
        # allow Yhorm as Iudex Gundyr if there's at least one available location.
        return any(
            self._is_location_available(location)
            and location.name not in self.all_excluded_locations
            and location.name != "CA: Coiled Sword - boss drop"
            for location in location_tables["Cemetery of Ash"]
        )

    def create_regions(self) -> None:
        # Create Vanilla Regions
        regions: Dict[str, Region] = {"Menu": self.create_region("Menu", {})}
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Cemetery of Ash",
            "Firelink Shrine",
            "Firelink Shrine Bell Tower",
            "High Wall of Lothric",
            "Undead Settlement",
            "Road of Sacrifices",
            "Cathedral of the Deep",
            "Farron Keep",
            "Catacombs of Carthus",
            "Smouldering Lake",
            "Irithyll of the Boreal Valley",
            "Irithyll Dungeon",
            "Profaned Capital",
            "Anor Londo",
            "Lothric Castle",
            "Consumed King's Garden",
            "Grand Archives",
            "Untended Graves",
            "Archdragon Peak",
            "Kiln of the First Flame",
            "Greirat's Shop",
            "Karla's Shop",
        ]})

        # Create DLC Regions
        if self.options.enable_dlc:
            regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
                "Painted World of Ariandel (Before Contraption)",
                "Painted World of Ariandel (After Contraption)",
                "Dreg Heap",
                "Ringed City",
            ]})

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"Go To {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        regions["Menu"].exits.append(Entrance(self.player, "New Game", regions["Menu"]))
        self.multiworld.get_entrance("New Game", self.player).connect(regions["Cemetery of Ash"])

        create_connection("Cemetery of Ash", "Firelink Shrine")

        create_connection("Firelink Shrine", "High Wall of Lothric")
        create_connection("Firelink Shrine", "Firelink Shrine Bell Tower")
        create_connection("Firelink Shrine", "Kiln of the First Flame")

        create_connection("High Wall of Lothric", "Undead Settlement")
        create_connection("High Wall of Lothric", "Lothric Castle")
        create_connection("High Wall of Lothric", "Greirat's Shop")

        create_connection("Undead Settlement", "Road of Sacrifices")

        create_connection("Road of Sacrifices", "Cathedral of the Deep")
        create_connection("Road of Sacrifices", "Farron Keep")

        create_connection("Farron Keep", "Catacombs of Carthus")

        create_connection("Catacombs of Carthus", "Irithyll of the Boreal Valley")
        create_connection("Catacombs of Carthus", "Smouldering Lake")

        create_connection("Irithyll of the Boreal Valley", "Irithyll Dungeon")
        create_connection("Irithyll of the Boreal Valley", "Anor Londo")

        create_connection("Irithyll Dungeon", "Archdragon Peak")
        create_connection("Irithyll Dungeon", "Profaned Capital")
        create_connection("Irithyll Dungeon", "Karla's Shop")

        create_connection("Lothric Castle", "Consumed King's Garden")
        create_connection("Lothric Castle", "Grand Archives")

        create_connection("Consumed King's Garden", "Untended Graves")

        # Connect DLC Regions
        if self.options.enable_dlc:
            create_connection("Cathedral of the Deep", "Painted World of Ariandel (Before Contraption)")
            create_connection("Painted World of Ariandel (Before Contraption)",
                              "Painted World of Ariandel (After Contraption)")
            create_connection("Painted World of Ariandel (After Contraption)", "Dreg Heap")
            create_connection("Dreg Heap", "Ringed City")

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        # Use this to un-exclude event locations so the fill doesn't complain about items behind
        # them being unreachable.
        excluded = self.options.exclude_locations.value

        for location in location_table:
            if self._is_location_available(location):
                new_location = DarkSouls3Location(self.player, location, new_region)
                if (
                    # Exclude missable locations that don't allow useful items
                    location.missable and self.options.missable_location_behavior == "forbid_useful"
                    and not (
                        # Unless they are excluded to a higher degree already
                        location.name in self.all_excluded_locations
                        and self.options.missable_location_behavior < self.options.excluded_location_behavior
                    )
                ) or (
                    # Lift Chamber Key is missable. Exclude Lift-Chamber-Key-Locked locations if it isn't randomized
                    not self._is_location_available("FS: Lift Chamber Key - Leonhard")
                    and location.name == "HWL: Red Eye Orb - wall tower, miniboss"
                ) or (
                    # Chameleon is missable. Exclude Chameleon-locked locations if it isn't randomized
                    not self._is_location_available("AL: Chameleon - tomb after marrying Anri")
                    and location.name in {"RC: Dragonhead Shield - streets monument, across bridge",
                                          "RC: Large Soul of a Crestfallen Knight - streets monument, across bridge",
                                          "RC: Divine Blessing - streets monument, mob drop", "RC: Lapp's Helm - Lapp",
                                          "RC: Lapp's Armor - Lapp",
                                          "RC: Lapp's Gauntlets - Lapp",
                                          "RC: Lapp's Leggings - Lapp"}
                ):
                    new_location.progress_type = LocationProgressType.EXCLUDED
            else:
                # Don't allow missable duplicates of progression items to be expected progression.
                if location.name in {"PC: Storm Ruler - Siegward",
                                     "US: Pyromancy Flame - Cornyx",
                                     "US: Tower Key - kill Irina"}:
                    continue

                # Replace non-randomized items with events that give the default item
                event_item = (
                    self.create_item(location.default_item_name) if location.default_item_name
                    else DarkSouls3Item.event(location.name, self.player)
                )

                new_location = DarkSouls3Location(
                    self.player,
                    location,
                    parent = new_region,
                    event = True,
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                if location.name in excluded:
                    excluded.remove(location.name)
                    # Only remove from all_excluded if excluded does not have priority over missable
                    if not (self.options.missable_location_behavior < self.options.excluded_location_behavior):
                        self.all_excluded_locations.remove(location.name)

            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        self.created_regions.add(region_name)
        return new_region

    def create_items(self) -> None:
        # Just used to efficiently deduplicate items
        item_set: Set[str] = set()

        # Gather all default items on randomized locations
        self.local_itempool = []
        num_required_extra_items = 0
        for location in cast(List[DarkSouls3Location], self.multiworld.get_unfilled_locations(self.player)):
            if not self._is_location_available(location.name):
                raise Exception("DS3 generation bug: Added an unavailable location.")

            default_item_name = cast(str, location.data.default_item_name)
            item = item_dictionary[default_item_name]
            if item.skip:
                num_required_extra_items += 1
            elif not item.unique:
                self.local_itempool.append(self.create_item(default_item_name))
            else:
                # For unique items, make sure there aren't duplicates in the item set even if there
                # are multiple in-game locations that provide them.
                if default_item_name in item_set:
                    num_required_extra_items += 1
                else:
                    item_set.add(default_item_name)
                    self.local_itempool.append(self.create_item(default_item_name))

        injectables = self._create_injectable_items(num_required_extra_items)
        num_required_extra_items -= len(injectables)
        self.local_itempool.extend(injectables)

        # Extra filler items for locations containing skip items
        self.local_itempool.extend(self.create_item(self.get_filler_item_name()) for _ in range(num_required_extra_items))

        # Potentially fill some items locally and remove them from the itempool
        self._fill_local_items()

        # Add items to itempool
        self.multiworld.itempool += self.local_itempool

    def _create_injectable_items(self, num_required_extra_items: int) -> List[DarkSouls3Item]:
        """Returns a list of items to inject into the multiworld instead of skipped items.

        If there isn't enough room to inject all the necessary progression items
        that are in missable locations by default, this adds them to the
        player's starting inventory.
        """

        all_injectable_items = [
            item for item
            in item_dictionary.values()
            if item.inject and (not item.is_dlc or self.options.enable_dlc)
        ]
        injectable_mandatory = [
            item for item in all_injectable_items
            if item.classification == ItemClassification.progression
        ]
        injectable_optional = [
            item for item in all_injectable_items
            if item.classification != ItemClassification.progression
        ]

        number_to_inject = min(num_required_extra_items, len(all_injectable_items))
        items = (
            self.random.sample(
                injectable_mandatory,
                k=min(len(injectable_mandatory), number_to_inject)
            )
            + self.random.sample(
                injectable_optional,
                k=max(0, number_to_inject - len(injectable_mandatory))
            )
        )

        if number_to_inject < len(injectable_mandatory):
            # It's worth considering the possibility of _removing_ unimportant
            # items from the pool to inject these instead rather than just
            # making them part of the starting health back
            for item in injectable_mandatory:
                if item in items: continue
                self.multiworld.push_precollected(self.create_item(item))
                warning(
                    f"Couldn't add \"{item.name}\" to the item pool for " + 
                    f"{self.player_name}. Adding it to the starting " +
                    f"inventory instead."
                )

        return [self.create_item(item) for item in items]

    def create_item(self, item: Union[str, DS3ItemData]) -> DarkSouls3Item:
        data = item if isinstance(item, DS3ItemData) else item_dictionary[item]
        classification = None
        if self.multiworld and data.useful_if != UsefulIf.DEFAULT and (
            (
                data.useful_if == UsefulIf.BASE and
                not self.options.enable_dlc and
                not self.options.enable_ngp
            )
            or (data.useful_if == UsefulIf.NO_DLC and not self.options.enable_dlc)
            or (data.useful_if == UsefulIf.NO_NGP and not self.options.enable_ngp)
        ):
            classification = ItemClassification.useful

        if (
            self.options.randomize_weapon_level != "none"
            and data.category.upgrade_level
            # Because we require the Pyromancy Flame to be available early, don't upgrade it so it
            # doesn't get shuffled around by weapon smoothing.
            and data.name != "Pyromancy Flame"
        ):
            # if the user made an error and set a min higher than the max we default to the max
            max_5 = self.options.max_levels_in_5.value
            min_5 = min(self.options.min_levels_in_5.value, max_5)
            max_10 = self.options.max_levels_in_10.value
            min_10 = min(self.options.min_levels_in_10.value, max_10)
            weapon_level_percentage = self.options.randomize_weapon_level_percentage

            if self.random.randint(0, 99) < weapon_level_percentage:
                if data.category.upgrade_level == 5:
                    data = data.upgrade(self.random.randint(min_5, max_5))
                elif data.category.upgrade_level == 10:
                    data = data.upgrade(self.random.randint(min_10, max_10))

        if self.options.randomize_infusion and data.category.is_infusible:
            infusion_percentage = self.options.randomize_infusion_percentage
            if self.random.randint(0, 99) < infusion_percentage:
                data = data.infuse(self.random.choice(list(Infusion)))

        return DarkSouls3Item(self.player, data, classification=classification)

    def _fill_local_items(self) -> None:
        """Removes certain items from the item pool and manually places them in the local world.

        We can't do this in pre_fill because the itempool may not be modified after create_items.
        """
        # If Yhorm is at Iudex Gundyr, Storm Ruler must be randomized, so it can always be moved.
        # Fill this manually so that, if very few slots are available in Cemetery of Ash, this
        # doesn't get locked out by bad rolls on the next two fills.
        if self.yhorm_location.name == "Iudex Gundyr":
            self._fill_local_item("Storm Ruler", ["Cemetery of Ash"],
                                  lambda location: location.name != "CA: Coiled Sword - boss drop")

        # If the Coiled Sword is vanilla, it is early enough and doesn't need to be placed.
        # Don't place this in the multiworld because it's necessary almost immediately, and don't
        # mark it as a blocker for HWL because having a miniscule Sphere 1 screws with progression balancing.
        if self._is_location_available("CA: Coiled Sword - boss drop"):
            self._fill_local_item("Coiled Sword", ["Cemetery of Ash", "Firelink Shrine"])

        # If the HWL Raw Gem is vanilla, it is early enough and doesn't need to be removed. If
        # upgrade smoothing is enabled, make sure one raw gem is available early for SL1 players
        if (
            self._is_location_available("HWL: Raw Gem - fort roof, lizard")
            and self.options.smooth_upgrade_items
        ):
            self._fill_local_item("Raw Gem", [
                "Cemetery of Ash",
                "Firelink Shrine",
                "High Wall of Lothric"
            ])

    def _fill_local_item(
        self, name: str,
        regions: List[str],
        additional_condition: Optional[Callable[[DS3LocationData], bool]] = None,
    ) -> None:
        """Chooses a valid location for the item with the given name and places it there.
        
        This always chooses a local location among the given regions. If additional_condition is
        passed, only locations meeting that condition will be considered.

        If the item could not be placed, it will be added to starting inventory.
        """
        item = next((item for item in self.local_itempool if item.name == name), None)
        if not item: return

        candidate_locations = [
            location for location in (
                self.multiworld.get_location(location.name, self.player)
                for region in regions
                for location in location_tables[region]
                if self._is_location_available(location)
                and not location.missable
                and not location.conditional
                and (not additional_condition or additional_condition(location))
            )
            # We can't use location.progress_type here because it's not set
            # until after `set_rules()` runs.
            if not location.item and location.name not in self.all_excluded_locations
            and location.item_rule(item)
        ]

        self.local_itempool.remove(item)

        if not candidate_locations:
            warning(f"Couldn't place \"{name}\" in a valid location for {self.player_name}. Adding it to starting inventory instead.")
            location = next(
                (location for location in self._get_our_locations() if location.data.default_item_name == item.name),
                None
            )
            if location: self._replace_with_filler(location)
            self.multiworld.push_precollected(self.create_item(name))
            return

        location = self.random.choice(candidate_locations)
        location.place_locked_item(item)

    def _replace_with_filler(self, location: DarkSouls3Location) -> None:
        """If possible, choose a filler item to replace location's current contents with."""
        if location.locked: return

        # Try 10 filler items. If none of them work, give up and leave it as-is.
        for _ in range(0, 10):
            candidate = self.create_filler()
            if location.item_rule(candidate):
                location.item = candidate
                return

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_names)

    def set_rules(self) -> None:
        randomized_items = {item.name for item in self.local_itempool}

        self._add_shop_rules()
        self._add_npc_rules()
        self._add_transposition_rules()
        self._add_crow_rules()
        self._add_allow_useful_location_rules()
        self._add_early_item_rules(randomized_items)

        self._add_entrance_rule("Firelink Shrine Bell Tower", "Tower Key")
        self._add_entrance_rule("Undead Settlement", lambda state: (
            state.has("Small Lothric Banner", self.player)
            and self._can_get(state, "HWL: Soul of Boreal Valley Vordt")
        ))
        self._add_entrance_rule("Road of Sacrifices", "US -> RS")
        self._add_entrance_rule(
            "Cathedral of the Deep",
            lambda state: self._can_get(state, "RS: Soul of a Crystal Sage")
        )
        self._add_entrance_rule("Farron Keep", "RS -> FK")
        self._add_entrance_rule(
            "Catacombs of Carthus",
            lambda state: self._can_get(state, "FK: Soul of the Blood of the Wolf")
        )
        self._add_entrance_rule("Irithyll Dungeon", "IBV -> ID")
        self._add_entrance_rule(
            "Lothric Castle",
            lambda state: self._can_get(state, "HWL: Soul of the Dancer")
        )
        self._add_entrance_rule(
            "Untended Graves",
            lambda state: self._can_get(state, "CKG: Soul of Consumed Oceiros")
        )
        self._add_entrance_rule("Irithyll of the Boreal Valley", lambda state: (
            state.has("Small Doll", self.player)
            and self._can_get(state, "CC: Soul of High Lord Wolnir")
        ))
        self._add_entrance_rule(
            "Anor Londo",
            lambda state: self._can_get(state, "IBV: Soul of Pontiff Sulyvahn")
        )
        self._add_entrance_rule("Archdragon Peak", "Path of the Dragon")
        self._add_entrance_rule("Grand Archives", lambda state: (
            state.has("Grand Archives Key", self.player)
            and self._can_get(state, "LC: Soul of Dragonslayer Armour")
        ))
        self._add_entrance_rule("Kiln of the First Flame", lambda state: (
            state.has("Cinders of a Lord - Abyss Watcher", self.player)
            and state.has("Cinders of a Lord - Yhorm the Giant", self.player)
            and state.has("Cinders of a Lord - Aldrich", self.player)
            and state.has("Cinders of a Lord - Lothric Prince", self.player)
            and state.has("Transposing Kiln", self.player)
        ))

        if self.options.late_basin_of_vows:
            self._add_entrance_rule("Lothric Castle", lambda state: (
                state.has("Small Lothric Banner", self.player)
                # Make sure these are actually available early.
                and (
                    "Transposing Kiln" not in randomized_items
                    or state.has("Transposing Kiln", self.player)
                ) and (
                    "Pyromancy Flame" not in randomized_items
                    or state.has("Pyromancy Flame", self.player)
                )
                # This isn't really necessary, but it ensures that the game logic knows players will
                # want to do Lothric Castle after at least being _able_ to access Catacombs. This is
                # useful for smooth item placement.
                and self._has_any_scroll(state)
            ))

            if self.options.late_basin_of_vows > 1:  # After Small Doll
                self._add_entrance_rule("Lothric Castle", "Small Doll")

        # DLC Access Rules Below
        if self.options.enable_dlc:
            self._add_entrance_rule("Painted World of Ariandel (Before Contraption)", "CD -> PW1")
            self._add_entrance_rule("Painted World of Ariandel (After Contraption)", "Contraption Key")
            self._add_entrance_rule(
                "Dreg Heap",
                lambda state: self._can_get(state, "PW2: Soul of Sister Friede")
            )
            self._add_entrance_rule("Ringed City", lambda state: (
                state.has("Small Envoy Banner", self.player)
                and self._can_get(state, "DH: Soul of the Demon Prince")
            ))

            if self.options.late_dlc:
                self._add_entrance_rule(
                    "Painted World of Ariandel (Before Contraption)",
                    lambda state: state.has("Small Doll", self.player) and self._has_any_scroll(state))

            if self.options.late_dlc > 1:  # After Basin
                self._add_entrance_rule("Painted World of Ariandel (Before Contraption)", "Basin of Vows")

        # Define the access rules to some specific locations
        self._add_location_rule("HWL: Red Eye Orb - wall tower, miniboss", "Lift Chamber Key")
        self._add_location_rule("ID: Bellowing Dragoncrest Ring - drop from B1 towards pit",
                                "Jailbreaker's Key")
        self._add_location_rule("ID: Covetous Gold Serpent Ring - Siegward's cell", "Old Cell Key")
        self._add_location_rule([
            "UG: Hornet Ring - environs, right of main path after killing FK boss",
            "UG: Wolf Knight Helm - shop after killing FK boss",
            "UG: Wolf Knight Armor - shop after killing FK boss",
            "UG: Wolf Knight Gauntlets - shop after killing FK boss",
            "UG: Wolf Knight Leggings - shop after killing FK boss"
        ], lambda state: self._can_get(state, "FK: Cinders of a Lord - Abyss Watcher"))
        self._add_location_rule(
            "ID: Prisoner Chief's Ashes - B2 near, locked cell by stairs",
            "Jailer's Key Ring"
        )
        self._add_entrance_rule("Karla's Shop", "Jailer's Key Ring")

        # The static randomizer edits events to guarantee that Greirat won't go to Lothric until
        # Grand Archives is available, so his shop will always be available one way or another.
        self._add_entrance_rule("Greirat's Shop", "Cell Key")

        self._add_location_rule("HWL: Soul of the Dancer", "Basin of Vows")

        # Lump Soul of the Dancer in with LC for locations that should not be reachable
        # before having access to US. (Prevents requiring getting Basin to fight Dancer to get SLB to go to US)
        if self.options.late_basin_of_vows:
            self._add_location_rule("HWL: Soul of the Dancer", lambda state: (
                state.has("Small Lothric Banner", self.player)
                # Make sure these are actually available early.
                and (
                    "Transposing Kiln" not in randomized_items
                    or state.has("Transposing Kiln", self.player)
                ) and (
                    "Pyromancy Flame" not in randomized_items
                    or state.has("Pyromancy Flame", self.player)
                )
                # This isn't really necessary, but it ensures that the game logic knows players will
                # want to do Lothric Castle after at least being _able_ to access Catacombs. This is
                # useful for smooth item placement.
                and self._has_any_scroll(state)
            ))

            if self.options.late_basin_of_vows > 1:  # After Small Doll
                self._add_location_rule("HWL: Soul of the Dancer", "Small Doll")

        self._add_location_rule([
            "LC: Grand Archives Key - by Grand Archives door, after PC and AL bosses",
            "LC: Gotthard Twinswords - by Grand Archives door, after PC and AL bosses"
        ], lambda state: (
            self._can_get(state, "AL: Cinders of a Lord - Aldrich") and
            self._can_get(state, "PC: Cinders of a Lord - Yhorm the Giant")
        ))

        self._add_location_rule([
            "FS: Morne's Great Hammer - Eygon",
            "FS: Moaning Shield - Eygon"
        ], lambda state: (
            self._can_get(state, "LC: Soul of Dragonslayer Armour") and
            self._can_get(state, "FK: Soul of the Blood of the Wolf")
        ))

        self._add_location_rule([
            "CKG: Drakeblood Helm - tomb, after killing AP mausoleum NPC",
            "CKG: Drakeblood Armor - tomb, after killing AP mausoleum NPC",
            "CKG: Drakeblood Gauntlets - tomb, after killing AP mausoleum NPC",
            "CKG: Drakeblood Leggings - tomb, after killing AP mausoleum NPC",
        ], lambda state: self._can_go_to(state, "Archdragon Peak"))

        self._add_location_rule([
            "FK: Havel's Helm - upper keep, after killing AP belfry roof NPC",
            "FK: Havel's Armor - upper keep, after killing AP belfry roof NPC",
            "FK: Havel's Gauntlets - upper keep, after killing AP belfry roof NPC",
            "FK: Havel's Leggings - upper keep, after killing AP belfry roof NPC",
        ], lambda state: self._can_go_to(state, "Archdragon Peak"))

        self._add_location_rule([
            "RC: Dragonhead Shield - streets monument, across bridge",
            "RC: Large Soul of a Crestfallen Knight - streets monument, across bridge",
            "RC: Divine Blessing - streets monument, mob drop",
            "RC: Lapp's Helm - Lapp",
            "RC: Lapp's Armor - Lapp",
            "RC: Lapp's Gauntlets - Lapp",
            "RC: Lapp's Leggings - Lapp",
        ], "Chameleon")

        # Forbid shops from carrying items with multiple counts (the static randomizer has its own
        # logic for choosing how many shop items to sell), and from carrying soul items.
        for location in location_dictionary.values():
            if location.shop:
                self._add_item_rule(
                    location.name,
                    lambda item: (
                        item.player != self.player or
                        (item.data.count == 1 and not item.data.souls)
                    )
                )

        # This particular location is bugged, and will drop two copies of whatever item is placed
        # there.
        if self._is_location_available("US: Young White Branch - by white tree #2"):
            self._add_item_rule(
                "US: Young White Branch - by white tree #2",
                lambda item: item.player == self.player and not item.data.unique
            )
        
        # Make sure the Storm Ruler is available BEFORE Yhorm the Giant
        if self.yhorm_location.name == "Ancient Wyvern":
            # This is a white lie, you can get to a bunch of items in AP before you beat the Wyvern,
            # but this saves us from having to split the entire region in two just to mark which
            # specific items are before and after.
            self._add_entrance_rule("Archdragon Peak", "Storm Ruler")
        for location in self.yhorm_location.locations:
            self._add_location_rule(location, "Storm Ruler")

        self.multiworld.completion_condition[self.player] = lambda state: self._can_get(state, "KFF: Soul of the Lords")

    def _add_shop_rules(self) -> None:
        """Adds rules for items unlocked in shops."""

        # Ashes
        ashes = {
            "Mortician's Ashes": ["Alluring Skull", "Ember", "Grave Key"],
            "Dreamchaser's Ashes": ["Life Ring", "Hidden Blessing"],
            "Paladin's Ashes": ["Lloyd's Shield Ring"],
            "Grave Warden's Ashes": ["Ember"],
            "Prisoner Chief's Ashes": [
                "Karla's Pointed Hat", "Karla's Coat", "Karla's Gloves", "Karla's Trousers"
            ],
            "Xanthous Ashes": ["Xanthous Overcoat", "Xanthous Gloves", "Xanthous Trousers"],
            "Dragon Chaser's Ashes": ["Ember"],
            "Easterner's Ashes": [
                "Washing Pole", "Eastern Helm", "Eastern Armor", "Eastern Gauntlets",
                "Eastern Leggings", "Wood Grain Ring",
            ],
            "Captain's Ashes": [
                "Millwood Knight Helm", "Millwood Knight Armor", "Millwood Knight Gauntlets",
                "Millwood Knight Leggings", "Refined Gem",
            ]
        }
        for (ash, items) in ashes.items():
            self._add_location_rule([f"FS: {item} - {ash}" for item in items], ash)

        # Shop unlocks
        shop_unlocks = {
            "Cornyx": [
                (
                    "Great Swamp Pyromancy Tome", "Great Swamp Tome",
                    ["Poison Mist", "Fire Orb", "Profuse Sweat", "Bursting Fireball"]
                ),
                (
                    "Carthus Pyromancy Tome", "Carthus Tome",
                    ["Acid Surge", "Carthus Flame Arc", "Carthus Beacon"]
                ),
                ("Izalith Pyromancy Tome", "Izalith Tome", ["Great Chaos Fire Orb", "Chaos Storm"]),
            ],
            "Irina": [
                (
                    "Braille Divine Tome of Carim", "Tome of Carim",
                    ["Med Heal", "Tears of Denial", "Force"]
                ),
                (
                    "Braille Divine Tome of Lothric", "Tome of Lothric",
                    ["Bountiful Light", "Magic Barrier", "Blessed Weapon"]
                ),
            ],
            "Orbeck": [
                ("Sage's Scroll", "Sage's Scroll", ["Great Farron Dart", "Farron Hail"]),
                (
                    "Golden Scroll", "Golden Scroll",
                    [
                        "Cast Light", "Repair", "Hidden Weapon", "Hidden Body",
                        "Twisted Wall of Light"
                    ],
                ),
                ("Logan's Scroll", "Logan's Scroll", ["Homing Soulmass", "Soul Spear"]),
                (
                    "Crystal Scroll", "Crystal Scroll",
                    ["Homing Crystal Soulmass", "Crystal Soul Spear", "Crystal Magic Weapon"]
                ),
            ],
            "Karla": [
                ("Quelana Pyromancy Tome", "Quelana Tome", ["Firestorm", "Rapport", "Fire Whip"]),
                (
                    "Grave Warden Pyromancy Tome", "Grave Warden Tome",
                    ["Black Flame", "Black Fire Orb"]
                ),
                ("Deep Braille Divine Tome", "Deep Braille Tome", ["Gnaw", "Deep Protection"]),
                (
                    "Londor Braille Divine Tome", "Londor Tome",
                    ["Vow of Silence", "Dark Blade", "Dead Again"]
                ),
            ],
        }
        for (shop, unlocks) in shop_unlocks.items():
            for (key, key_name, items) in unlocks:
                self._add_location_rule(
                    [f"FS: {item} - {shop} for {key_name}" for item in items], key)

    def _add_npc_rules(self) -> None:
        """Adds rules for items accessible via NPC quests.

        We list missable locations here even though they never contain progression items so that the
        game knows what sphere they're in. This is especially useful for item smoothing. (We could
        add rules for boss transposition items as well, but then we couldn't freely reorder boss
        soul locations for smoothing.)

        Generally, for locations that can be accessed early by killing NPCs, we set up requirements
        assuming the player _doesn't_ so they aren't forced to start killing allies to advance the
        quest.
        """

        ## Greirat

        self._add_location_rule([
            "FS: Divine Blessing - Greirat from US",
            "FS: Ember - Greirat from US",
        ], lambda state: (
            self._can_go_to(state, "Undead Settlement")
            and state.has("Loretta's Bone", self.player)
        ))
        self._add_location_rule([
            "FS: Divine Blessing - Greirat from IBV",
            "FS: Hidden Blessing - Greirat from IBV",
            "FS: Titanite Scale - Greirat from IBV",
            "FS: Twinkling Titanite - Greirat from IBV",
            "FS: Ember - shop for Greirat's Ashes"
        ], lambda state: (
            self._can_go_to(state, "Irithyll of the Boreal Valley")
            and self._can_get(state, "FS: Divine Blessing - Greirat from US")
            # Either Patches or Siegward can save Greirat, but we assume the player will want to use
            # Patches because it's harder to screw up
            and self._can_get(state, "CD: Shotel - Patches")
        ))
        self._add_location_rule([
            "FS: Ember - shop for Greirat's Ashes",
        ], lambda state: (
            self._can_go_to(state, "Grand Archives")
            and self._can_get(state, "FS: Divine Blessing - Greirat from IBV")
        ))

        ## Patches

        # Patches will only set up shop in Firelink once he's tricked you in the bell tower. He'll
        # only do _that_ once you've spoken to Siegward after killing the Fire Demon and lit the
        # Rosaria's Bed Chamber bonfire. He _won't_ set up shop in the Cathedral if you light the
        # Rosaria's Bed Chamber bonfire before getting tricked by him, so we assume these locations
        # require the bell tower.
        self._add_location_rule([
            "CD: Shotel - Patches",
            "CD: Ember - Patches",
            "FS: Rusted Gold Coin - don't forgive Patches"
        ], lambda state: (
            self._can_go_to(state, "Firelink Shrine Bell Tower")
            and self._can_go_to(state, "Cathedral of the Deep")
        ))

        # Patches sells this after you tell him to search for Greirat in Grand Archives
        self._add_location_rule([
            "FS: Hidden Blessing - Patches after searching GA"
        ], lambda state: (
            self._can_get(state, "CD: Shotel - Patches")
            and self._can_get(state, "FS: Ember - shop for Greirat's Ashes")
        ))

        # Only make the player kill Patches once all his other items are available
        self._add_location_rule([
            "CD: Winged Spear - kill Patches",
            # You don't _have_ to kill him for this, but he has to be in Firelink at the same time
            # as Greirat to get it in the shop and that may not be feasible if the player progresses
            # Greirat's quest much faster.
            "CD: Horsehoof Ring - Patches",
        ], lambda state: (
            self._can_get(state, "FS: Hidden Blessing - Patches after searching GA")
            and self._can_get(state, "FS: Rusted Gold Coin - don't forgive Patches")
        ))

        ## Leonhard

        self._add_location_rule([
            # Talk to Leonhard in Firelink with a Pale Tongue after lighting Cliff Underside or
            # killing Greatwood. This doesn't consume the Pale Tongue, it just has to be in
            # inventory
            "FS: Lift Chamber Key - Leonhard",
            # Progress Leonhard's quest and then return to Rosaria after lighting Profaned Capital
            "CD: Black Eye Orb - Rosaria from Leonhard's quest",
        ], "Pale Tongue")

        self._add_location_rule([
            "CD: Black Eye Orb - Rosaria from Leonhard's quest",
        ], lambda state: (
            # The Black Eye Orb location won't spawn until you kill the HWL miniboss and resting at
            # the Profaned Capital bonfire.
            self._can_get(state, "HWL: Red Eye Orb - wall tower, miniboss")
            and self._can_go_to(state, "Profaned Capital")
        ))

        # Perhaps counterintuitively, you CAN fight Leonhard before you access the location that
        # would normally give you the Black Eye Orb.
        self._add_location_rule([
            "AL: Crescent Moon Sword - Leonhard drop",
            "AL: Silver Mask - Leonhard drop",
            "AL: Soul of Rosaria - Leonhard drop",
        ] + [
            f"FS: {item} - shop after killing Leonhard"
            for item in ["Leonhard's Garb", "Leonhard's Gauntlets", "Leonhard's Trousers"]
        ], "Black Eye Orb")

        ## Hawkwood
        
        # After Hawkwood leaves and once you have the Torso Stone, you can fight him for dragon
        # stones. Andre will give Swordgrass as a hint as well
        self._add_location_rule([
            "FK: Twinkling Dragon Head Stone - Hawkwood drop",
            "FS: Hawkwood's Swordgrass - Andre after gesture in AP summit"
        ], lambda state: (
            self._can_get(state, "FS: Hawkwood's Shield - gravestone after Hawkwood leaves")
            and state.has("Twinkling Dragon Torso Stone", self.player)
        ))

        ## Siegward

        # Unlock Siegward's cell after progressing his quest
        self._add_location_rule([
            "ID: Titanite Slab - Siegward",
        ], lambda state: (
            state.has("Old Cell Key", self.player)
            # Progressing Siegward's quest requires buying his armor from Patches.
            and self._can_get(state, "CD: Shotel - Patches")
        ))

        # These drop after completing Siegward's quest and talking to him in Yhorm's arena
        self._add_location_rule([
            "PC: Siegbräu - Siegward after killing boss",
            "PC: Storm Ruler - Siegward",
            "PC: Pierce Shield - Siegward",
        ], lambda state: (
            self._can_get(state, "ID: Titanite Slab - Siegward")
            and self._can_get(state, "PC: Soul of Yhorm the Giant")
        ))

        ## Sirris

        # Kill Greatwood and turn in Dreamchaser's Ashes to trigger this opportunity for invasion
        self._add_location_rule([
            "FS: Mail Breaker - Sirris for killing Creighton",
            "FS: Silvercat Ring - Sirris for killing Creighton",
            "IBV: Creighton's Steel Mask - bridge after killing Creighton",
            "IBV: Mirrah Chain Gloves - bridge after killing Creighton",
            "IBV: Mirrah Chain Leggings - bridge after killing Creighton",
            "IBV: Mirrah Chain Mail - bridge after killing Creighton",
            "IBV: Dragonslayer's Axe - Creighton drop",
            # Killing Pontiff without progressing Sirris's quest will break it.
            "IBV: Soul of Pontiff Sulyvahn"
        ], lambda state: (
            self._can_get(state, "US: Soul of the Rotted Greatwood")
            and state.has("Dreamchaser's Ashes", self.player)
        ))
        # Add indirect condition since reaching AL requires defeating Pontiff which requires defeating Greatwood in US
        self.multiworld.register_indirect_condition(
            self.get_region("Undead Settlement"),
            self.get_entrance("Go To Anor Londo")
        )

        # Kill Creighton and Aldrich to trigger this opportunity for invasion
        self._add_location_rule([
            "FS: Budding Green Blossom - shop after killing Creighton and AL boss",
            "FS: Sunset Shield - by grave after killing Hodrick w/Sirris",
            "US: Sunset Helm - Pit of Hollows after killing Hodrick w/Sirris",
            "US: Sunset Armor - pit of hollows after killing Hodrick w/Sirris",
            "US: Sunset Gauntlets - pit of hollows after killing Hodrick w/Sirris",
            "US: Sunset Leggings - pit of hollows after killing Hodrick w/Sirris",
        ], lambda state: (
            self._can_get(state, "FS: Mail Breaker - Sirris for killing Creighton")
            and self._can_get(state, "AL: Soul of Aldrich")
        ))

        # Kill Hodrick and Twin Princes to trigger the end of the quest
        self._add_location_rule([
            "FS: Sunless Talisman - Sirris, kill GA boss",
            "FS: Sunless Veil - shop, Sirris quest, kill GA boss",
            "FS: Sunless Armor - shop, Sirris quest, kill GA boss",
            "FS: Sunless Gauntlets - shop, Sirris quest, kill GA boss",
            "FS: Sunless Leggings - shop, Sirris quest, kill GA boss",
            # Killing Yorshka will anger Sirris and stop her quest, so don't expect it until the
            # quest is done
            "AL: Yorshka's Chime - kill Yorshka",
        ], lambda state: (
            self._can_get(state, "US: Soul of the Rotted Greatwood")
            and state.has("Dreamchaser's Ashes", self.player)
        ))

        ## Cornyx

        self._add_location_rule([
            "US: Old Sage's Blindfold - kill Cornyx",
            "US: Cornyx's Garb - kill Cornyx",
            "US: Cornyx's Wrap - kill Cornyx",
            "US: Cornyx's Skirt - kill Cornyx",
        ], lambda state: (
            state.has("Great Swamp Pyromancy Tome", self.player)
            and state.has("Carthus Pyromancy Tome", self.player)
            and state.has("Izalith Pyromancy Tome", self.player)
        ))

        self._add_location_rule([
            "US: Old Sage's Blindfold - kill Cornyx", "US: Cornyx's Garb - kill Cornyx",
            "US: Cornyx's Wrap - kill Cornyx", "US: Cornyx's Skirt - kill Cornyx"
        ], lambda state: (
            state.has("Great Swamp Pyromancy Tome", self.player)
            and state.has("Carthus Pyromancy Tome", self.player)
            and state.has("Izalith Pyromancy Tome", self.player)
        ))

        ## Irina

        self._add_location_rule([
            "US: Tower Key - kill Irina",
        ], lambda state: (
            state.has("Braille Divine Tome of Carim", self.player)
            and state.has("Braille Divine Tome of Lothric", self.player)
        ))

        ## Karla

        self._add_location_rule([
            "FS: Karla's Pointed Hat - kill Karla",
            "FS: Karla's Coat - kill Karla",
            "FS: Karla's Gloves - kill Karla",
            "FS: Karla's Trousers - kill Karla",
        ], lambda state: (
            state.has("Quelana Pyromancy Tome", self.player)
            and state.has("Grave Warden Pyromancy Tome", self.player)
            and state.has("Deep Braille Divine Tome", self.player)
            and state.has("Londor Braille Divine Tome", self.player)
        ))

        ## Emma

        self._add_location_rule("HWL: Basin of Vows - Emma", "Small Doll")

        ## Orbeck

        self._add_location_rule([
            "FS: Morion Blade - Yuria for Orbeck's Ashes",
            "FS: Clandestine Coat - shop with Orbeck's Ashes"
        ], lambda state: (
            state.has("Golden Scroll", self.player)
            and state.has("Logan's Scroll", self.player)
            and state.has("Crystal Scroll", self.player)
            and state.has("Sage's Scroll", self.player)
        ))

        self._add_location_rule([
            "FS: Pestilent Mist - Orbeck for any scroll",
            "FS: Young Dragon Ring - Orbeck for one scroll and buying three spells",
            # Make sure that the player can keep Orbeck around by giving him at least one scroll
            # before killing Abyss Watchers.
            "FK: Soul of the Blood of the Wolf",
            "FK: Cinders of a Lord - Abyss Watcher",
            "FS: Undead Legion Helm - shop after killing FK boss",
            "FS: Undead Legion Armor - shop after killing FK boss",
            "FS: Undead Legion Gauntlet - shop after killing FK boss",
            "FS: Undead Legion Leggings - shop after killing FK boss",
            "FS: Farron Ring - Hawkwood",
            "FS: Hawkwood's Shield - gravestone after Hawkwood leaves",
            "UG: Hornet Ring - environs, right of main path after killing FK boss",
            "UG: Wolf Knight Helm - shop after killing FK boss",
            "UG: Wolf Knight Armor - shop after killing FK boss",
            "UG: Wolf Knight Gauntlets - shop after killing FK boss",
            "UG: Wolf Knight Leggings - shop after killing FK boss",
        ], self._has_any_scroll)

        # Not really necessary but ensures players can decide which way to go
        if self.options.enable_dlc:
            self._add_entrance_rule(
                "Painted World of Ariandel (After Contraption)",
                self._has_any_scroll
            )

        ## Anri

        # Anri only leaves Road of Sacrifices once Deacons is defeated
        self._add_location_rule([
            "IBV: Ring of the Evil Eye - Anri",
            "AL: Chameleon - tomb after marrying Anri",
        ], lambda state: self._can_get(state, "CD: Soul of the Deacons of the Deep"))

        # If the player does Anri's non-marriage quest, they'll need to defeat the AL boss as well
        # before it's complete.
        self._add_location_rule([
            "AL: Anri's Straight Sword - Anri quest",
            "FS: Elite Knight Helm - shop after Anri quest",
            "FS: Elite Knight Armor - shop after Anri quest",
            "FS: Elite Knight Gauntlets - shop after Anri quest",
            "FS: Elite Knight Leggings - shop after Anri quest",
        ], lambda state: (
            self._can_get(state, "IBV: Ring of the Evil Eye - Anri") and
            self._can_get(state, "AL: Soul of Aldrich")
        ))

    def _add_transposition_rules(self) -> None:
        """Adds rules for items obtainable from Ludleth by soul transposition."""

        transpositions = [
            (
                "Soul of Boreal Valley Vordt", "Vordt",
                ["Vordt's Great Hammer", "Pontiff's Left Eye"]
            ),
            ("Soul of Rosaria", "Rosaria", ["Bountiful Sunlight"]),
            ("Soul of Aldrich", "Aldrich", ["Darkmoon Longbow", "Lifehunt Scythe"]),
            (
                "Soul of the Rotted Greatwood", "Greatwood",
                ["Hollowslayer Greatsword", "Arstor's Spear"]
            ),
            ("Soul of a Crystal Sage", "Sage", ["Crystal Sage's Rapier", "Crystal Hail"]),
            ("Soul of the Deacons of the Deep", "Deacons", ["Cleric's Candlestick", "Deep Soul"]),
            ("Soul of a Stray Demon", "Stray Demon", ["Havel's Ring", "Boulder Heave"]),
            (
                "Soul of the Blood of the Wolf", "Abyss Watchers",
                ["Farron Greatsword", "Wolf Knight's Greatsword"]
            ),
            ("Soul of High Lord Wolnir", "Wolnir", ["Wolnir's Holy Sword", "Black Serpent"]),
            ("Soul of a Demon", "Fire Demon", ["Demon's Greataxe", "Demon's Fist"]),
            (
                "Soul of the Old Demon King", "Old Demon King",
                ["Old King's Great Hammer", "Chaos Bed Vestiges"]
            ),
            (
                "Soul of Pontiff Sulyvahn", "Pontiff",
                ["Greatsword of Judgment", "Profaned Greatsword"]
            ),
            ("Soul of Yhorm the Giant", "Yhorm", ["Yhorm's Great Machete", "Yhorm's Greatshield"]),
            ("Soul of the Dancer", "Dancer", ["Dancer's Enchanted Swords", "Soothing Sunlight"]),
            (
                "Soul of Dragonslayer Armour", "Dragonslayer",
                ["Dragonslayer Greataxe", "Dragonslayer Greatshield"]
            ),
            (
                "Soul of Consumed Oceiros", "Oceiros",
                ["Moonlight Greatsword", "White Dragon Breath"]
            ),
            (
                "Soul of the Twin Princes", "Princes",
                ["Lorian's Greatsword", "Lothric's Holy Sword"]
            ),
            ("Soul of Champion Gundyr", "Champion", ["Gundyr's Halberd", "Prisoner's Chain"]),
            (
                "Soul of the Nameless King", "Nameless",
                ["Storm Curved Sword", "Dragonslayer Swordspear", "Lightning Storm"]
            ),
            ("Soul of the Lords", "Cinder", ["Firelink Greatsword", "Sunlight Spear"]),
            ("Soul of Sister Friede", "Friede", ["Friede's Great Scythe", "Rose of Ariandel"]),
            ("Soul of the Demon Prince", "Demon Prince", ["Demon's Scar", "Seething Chaos"]),
            ("Soul of Darkeater Midir", "Midir", ["Frayed Blade", "Old Moonlight"]),
            ("Soul of Slave Knight Gael", "Gael", ["Gael's Greatsword", "Repeating Crossbow"]),
        ]
        for (soul, soul_name, items) in transpositions:
            self._add_location_rule([
                f"FS: {item} - Ludleth for {soul_name}" for item in items
            ], lambda state, s=soul: (
                state.has(s, self.player) and state.has("Transposing Kiln", self.player)
            ))

    def _add_crow_rules(self) -> None:
        """Adds rules for items obtainable by trading items to the crow on Firelink roof."""

        crow = {
            "Loretta's Bone": "Ring of Sacrifice",
            # "Avelyn": "Titanite Scale", # Missing from static randomizer
            "Coiled Sword Fragment": "Titanite Slab",
            "Seed of a Giant Tree": "Iron Leggings",
            "Siegbräu": "Armor of the Sun",
            # Static randomizer can't randomize Hodrick's drop yet
            # "Vertebra Shackle": "Lucatiel's Mask",
            "Xanthous Crown": "Lightning Gem",
            "Mendicant's Staff": "Sunlight Shield",
            "Blacksmith Hammer": "Titanite Scale",
            "Large Leather Shield": "Twinkling Titanite",
            "Moaning Shield": "Blessed Gem",
            "Eleonora": "Hollow Gem",
        }
        for (given, received) in crow.items():
            name = f"FSBT: {received} - crow for {given}"
            self._add_location_rule(name, given)

            # Don't let crow items have foreign items because they're picked up in a way that's
            # missed by the hook we use to send location items
            self._add_item_rule(name, lambda item: (
                item.player == self.player
                # Because of the weird way they're delivered, crow items don't seem to support
                # infused or upgraded weapons.
                and not item.data.is_infused
                and not item.data.is_upgraded
            ))

    def _add_allow_useful_location_rules(self) -> None:
        """Adds rules for locations that can contain useful but not necessary items.

        If we allow useful items in the excluded locations, we don't want Archipelago's fill
        algorithm to consider them excluded because it never allows useful items there. Instead, we
        manually add item rules to exclude important items.
        """

        all_locations = self._get_our_locations()

        allow_useful_locations = (
            (
                {
                    location.name
                    for location in all_locations
                    if location.name in self.all_excluded_locations
                    and not location.data.missable
                }
                if self.options.excluded_location_behavior < self.options.missable_location_behavior
                else self.all_excluded_locations
            )
            if self.options.excluded_location_behavior == "allow_useful"
            else set()
        ).union(
            {
                location.name
                for location in all_locations
                if location.data.missable
                and not (
                    location.name in self.all_excluded_locations
                    and self.options.missable_location_behavior <
                        self.options.excluded_location_behavior
                )
            }
            if self.options.missable_location_behavior == "allow_useful"
            else set()
        )
        for location in allow_useful_locations:
            self._add_item_rule(
                location,
                lambda item: not item.advancement
            )

        # Prevent the player from prioritizing and "excluding" the same location
        self.options.priority_locations.value -= allow_useful_locations

        if self.options.excluded_location_behavior == "allow_useful":
            self.options.exclude_locations.value.clear()

    def _add_early_item_rules(self, randomized_items: Set[str]) -> None:
        """Adds rules to make sure specific items are available early."""

        if "Pyromancy Flame" in randomized_items:
            # Make this available early because so many items are useless without it.
            self._add_entrance_rule("Road of Sacrifices", "Pyromancy Flame")
            self._add_entrance_rule("Consumed King's Garden", "Pyromancy Flame")
            self._add_entrance_rule("Grand Archives", "Pyromancy Flame")
        if "Transposing Kiln" in randomized_items:
            # Make this available early so players can make use of their boss souls.
            self._add_entrance_rule("Road of Sacrifices", "Transposing Kiln")
            self._add_entrance_rule("Consumed King's Garden", "Transposing Kiln")
            self._add_entrance_rule("Grand Archives", "Transposing Kiln")
        # Make this available pretty early 
        if "Small Lothric Banner" in randomized_items:
            if self.options.early_banner == "early_global":
                self.multiworld.early_items[self.player]["Small Lothric Banner"] = 1
            elif self.options.early_banner == "early_local":
                self.multiworld.local_early_items[self.player]["Small Lothric Banner"] = 1

    def _has_any_scroll(self, state: CollectionState) -> bool:
        """Returns whether the given state has any scroll item."""
        return (
            state.has("Sage's Scroll", self.player)
            or state.has("Golden Scroll", self.player)
            or state.has("Logan's Scroll", self.player)
            or state.has("Crystal Scroll", self.player)
        )

    def _add_location_rule(self, location: Union[str, List[str]], rule: Union[CollectionRule, str]) -> None:
        """Sets a rule for the given location if it that location is randomized.

        The rule can just be a single item/event name as well as an explicit rule lambda.
        """
        locations = location if isinstance(location, list) else [location]
        for location in locations:
            data = location_dictionary[location]
            if data.dlc and not self.options.enable_dlc: continue
            if data.ngp and not self.options.enable_ngp: continue

            if not self._is_location_available(location): continue
            if isinstance(rule, str):
                assert item_dictionary[rule].classification == ItemClassification.progression
                rule = lambda state, item=rule: state.has(item, self.player)
            add_rule(self.multiworld.get_location(location, self.player), rule)

    def _add_entrance_rule(self, region: str, rule: Union[CollectionRule, str]) -> None:
        """Sets a rule for the entrance to the given region."""
        assert region in location_tables
        if region not in self.created_regions: return
        if isinstance(rule, str):
            if " -> " not in rule:
                assert item_dictionary[rule].classification == ItemClassification.progression
            rule = lambda state, item=rule: state.has(item, self.player)
        add_rule(self.multiworld.get_entrance("Go To " + region, self.player), rule)

    def _add_item_rule(self, location: str, rule: ItemRule) -> None:
        """Sets a rule for what items are allowed in a given location."""
        if not self._is_location_available(location): return
        add_item_rule(self.multiworld.get_location(location, self.player), rule)

    def _can_go_to(self, state, region) -> bool:
        """Returns whether state can access the given region name."""
        return state.can_reach_entrance(f"Go To {region}", self.player)

    def _can_get(self, state, location) -> bool:
        """Returns whether state can access the given location name."""
        return state.can_reach_location(location, self.player)

    def _is_location_available(
        self,
        location: Union[str, DS3LocationData, DarkSouls3Location]
    ) -> bool:
        """Returns whether the given location is being randomized."""
        if isinstance(location, DS3LocationData):
            data = location
        elif isinstance(location, DarkSouls3Location):
            data = location.data
        else:
            data = location_dictionary[location]

        return (
            not data.is_event
            and (not data.dlc or bool(self.options.enable_dlc))
            and (not data.ngp or bool(self.options.enable_ngp))
            and not (
                self.options.excluded_location_behavior == "do_not_randomize"
                and data.name in self.all_excluded_locations
            )
            and not (
                self.options.missable_location_behavior == "do_not_randomize"
                and data.missable
            )
        )

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        text = ""

        if self.yhorm_location != default_yhorm_location:
            text += f"\nYhorm takes the place of {self.yhorm_location.name} in {self.player_name}'s world\n"

        if self.options.excluded_location_behavior == "allow_useful":
            text += f"\n{self.player_name}'s world excluded: {sorted(self.all_excluded_locations)}\n"

        if text:
            text = "\n" + text + "\n"
            spoiler_handle.write(text)

    def post_fill(self):
        """If item smoothing is enabled, rearrange items so they scale up smoothly through the run.

        This determines the approximate order a given silo of items (say, soul items) show up in the
        main game, then rearranges their shuffled placements to match that order. It determines what
        should come "earlier" or "later" based on sphere order: earlier spheres get lower-level
        items, later spheres get higher-level ones. Within a sphere, items in DS3 are distributed in
        region order, and then the best items in a sphere go into the multiworld.
        """

        locations_by_sphere = [
            sorted(loc for loc in sphere if loc.item.player == self.player and not loc.locked)
            for sphere in self.multiworld.get_spheres()
        ]

        # All items in the base game in approximately the order they appear
        all_item_order: List[DS3ItemData] = [
            item_dictionary[location.default_item_name]
            for region in region_order
            # Shuffle locations within each region.
            for location in self._shuffle(location_tables[region])
            if self._is_location_available(location)
        ]

        # All DarkSouls3Items for this world that have been assigned anywhere, grouped by name
        full_items_by_name: Dict[str, List[DarkSouls3Item]] = defaultdict(list)
        for location in self.multiworld.get_filled_locations():
            if location.item.player == self.player and (
                location.player != self.player or self._is_location_available(location)
            ):
                full_items_by_name[location.item.name].append(location.item)

        def smooth_items(item_order: List[Union[DS3ItemData, DarkSouls3Item]]) -> None:
            """Rearrange all items in item_order to match that order.

            Note: this requires that item_order exactly matches the number of placed items from this
            world matching the given names.
            """

            # Convert items to full DarkSouls3Items.
            converted_item_order: List[DarkSouls3Item] = [
                item for item in (
                    (
                        # full_items_by_name won't contain DLC items if the DLC is disabled.
                        (full_items_by_name[item.name] or [None]).pop(0)
                        if isinstance(item, DS3ItemData) else item
                    )
                    for item in item_order
                )
                # Never re-order event items, because they weren't randomized in the first place.
                if item and item.code is not None
            ]

            names = {item.name for item in converted_item_order}

            all_matching_locations = [
                loc
                for sphere in locations_by_sphere
                for loc in sphere
                if loc.item.name in names
            ]

            # It's expected that there may be more total items than there are matching locations if
            # the player has chosen a more limited accessibility option, since the matching
            # locations *only* include items in the spheres of accessibility.
            if len(converted_item_order) < len(all_matching_locations):
                raise Exception(
                    f"DS3 bug: there are {len(all_matching_locations)} locations that can " +
                    f"contain smoothed items, but only {len(converted_item_order)} items to smooth."
                )

            for sphere in locations_by_sphere:
                locations = [loc for loc in sphere if loc.item.name in names]

                # Check the game, not the player, because we know how to sort within regions for DS3
                offworld = self._shuffle([loc for loc in locations if loc.game != "Dark Souls III"])
                onworld = sorted((loc for loc in locations if loc.game == "Dark Souls III"),
                                 key=lambda loc: loc.data.region_value)

                # Give offworld regions the last (best) items within a given sphere
                for location in onworld + offworld:
                    new_item = self._pop_item(location, converted_item_order)
                    location.item = new_item
                    new_item.location = location

        if self.options.smooth_upgrade_items:
            base_names = {
                "Titanite Shard", "Large Titanite Shard", "Titanite Chunk", "Titanite Slab",
                "Titanite Scale", "Twinkling Titanite", "Farron Coal", "Sage's Coal", "Giant's Coal",
                "Profaned Coal"
            }
            smooth_items([item for item in all_item_order if item.base_name in base_names])

        if self.options.smooth_soul_items:
            smooth_items([
                item for item in all_item_order
                if item.souls and item.classification != ItemClassification.progression
            ])

        if self.options.smooth_upgraded_weapons:
            upgraded_weapons = [
                location.item
                for location in self.multiworld.get_filled_locations()
                if location.item.player == self.player
                and location.item.level and location.item.level > 0
                and location.item.classification != ItemClassification.progression
            ]
            upgraded_weapons.sort(key=lambda item: item.level)
            smooth_items(upgraded_weapons)

    def _shuffle(self, seq: Sequence) -> List:
        """Returns a shuffled copy of a sequence."""
        copy = list(seq)
        self.random.shuffle(copy)
        return copy

    def _pop_item(
        self,
        location: Location,
        items: List[DarkSouls3Item]
    ) -> DarkSouls3Item:
        """Returns the next item in items that can be assigned to location."""
        for i, item in enumerate(items):
            if location.can_fill(self.multiworld.state, item, False):
                return items.pop(i)

        # If we can't find a suitable item, give up and assign an unsuitable one.
        return items.pop(0)

    def _get_our_locations(self) -> List[DarkSouls3Location]:
        return cast(List[DarkSouls3Location], self.multiworld.get_locations(self.player))

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        # Once all clients support overlapping item IDs, adjust the DS3 AP item IDs to encode the
        # in-game ID as well as the count so that we don't need to send this information at all.
        #
        # We include all the items the game knows about so that users can manually request items
        # that aren't randomized, and then we _also_ include all the items that are placed in
        # practice `item_dictionary.values()` doesn't include upgraded or infused weapons.
        items_by_name = {
            location.item.name: cast(DarkSouls3Item, location.item).data
            for location in self.multiworld.get_filled_locations()
            # item.code None is used for events, which we want to skip
            if location.item.code is not None and location.item.player == self.player
        }
        for item in item_dictionary.values():
            if item.name not in items_by_name:
                items_by_name[item.name] = item

        ap_ids_to_ds3_ids: Dict[str, int] = {}
        item_counts: Dict[str, int] = {}
        for item in items_by_name.values():
            if item.ap_code is None: continue
            if item.ds3_code: ap_ids_to_ds3_ids[str(item.ap_code)] = item.ds3_code
            if item.count != 1: item_counts[str(item.ap_code)] = item.count

        # A map from Archipelago's location IDs to the keys the static randomizer uses to identify
        # locations.
        location_ids_to_keys: Dict[int, str] = {}
        for location in cast(List[DarkSouls3Location], self.multiworld.get_filled_locations(self.player)):
            # Skip events and only look at this world's locations
            if (location.address is not None and location.item.code is not None
                    and location.data.static):
                location_ids_to_keys[location.address] = location.data.static

        slot_data = {
            "options": {
                "random_starting_loadout": self.options.random_starting_loadout.value,
                "require_one_handed_starting_weapons": self.options.require_one_handed_starting_weapons.value,
                "auto_equip": self.options.auto_equip.value,
                "lock_equip": self.options.lock_equip.value,
                "no_weapon_requirements": self.options.no_weapon_requirements.value,
                "death_link": self.options.death_link.value,
                "no_spell_requirements": self.options.no_spell_requirements.value,
                "no_equip_load": self.options.no_equip_load.value,
                "enable_dlc": self.options.enable_dlc.value,
                "enable_ngp": self.options.enable_ngp.value,
                "smooth_soul_locations": self.options.smooth_soul_items.value,
                "smooth_upgrade_locations": self.options.smooth_upgrade_items.value,
                "randomize_enemies": self.options.randomize_enemies.value,
                "randomize_mimics_with_enemies": self.options.randomize_mimics_with_enemies.value,
                "randomize_small_crystal_lizards_with_enemies": self.options.randomize_small_crystal_lizards_with_enemies.value,
                "reduce_harmless_enemies": self.options.reduce_harmless_enemies.value,
                "simple_early_bosses": self.options.simple_early_bosses.value,
                "scale_enemies": self.options.scale_enemies.value,
                "all_chests_are_mimics": self.options.all_chests_are_mimics.value,
                "impatient_mimics": self.options.impatient_mimics.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            # Reserializing here is silly, but it's easier for the static randomizer.
            "random_enemy_preset": json.dumps(self.options.random_enemy_preset.value),
            "yhorm": (
                f"{self.yhorm_location.name} {self.yhorm_location.id}"
                if self.yhorm_location != default_yhorm_location
                else None
            ),
            "apIdsToItemIds": ap_ids_to_ds3_ids,
            "itemCounts": item_counts,
            "locationIdsToKeys": location_ids_to_keys,
            # The range of versions of the static randomizer that are compatible
            # with this slot data. Incompatible versions should have at least a
            # minor version bump. Pre-release versions should generally only be
            # compatible with a single version, except very close to a stable
            # release when no changes are expected.
            #
            # This is checked by the static randomizer, which will surface an
            # error to the user if its version doesn't fall into the allowed
            # range.
            "versions": ">=3.0.0-beta.24 <3.1.0",
        }

        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data
