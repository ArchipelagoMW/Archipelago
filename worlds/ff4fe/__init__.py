import json
import os
import threading
import typing
from typing import Mapping, Any

import Utils
import settings
from BaseClasses import Region, ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule, forbid_items_for_player
from . import events, items, locations
from . import rules as FERules
from .Client import FF4FEClient
from .itempool import create_itempool
from .items import FF4FEItem, all_items, ItemData
from .locations import FF4FELocation, all_locations, LocationData
from .options import FF4FEOptions, ff4fe_option_groups
from . import topology, flags
from .rom import FF4FEProcedurePatch


class FF4FEWebWorld(WebWorld):
    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Final Fantasy IV: Free Enterprise randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Rosalie"]
    )

    tutorials = [setup_en]

    option_groups = ff4fe_option_groups


class FF4FESettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the FF4 USA 1.1 US rom"""

        copy_to = "Final Fantasy II (USA) (Rev A).sfc"
        description = "FFII SNES 1.1 ROM File"
        md5s = ["27D02A4F03E172E029C9B82AC3DB79F7"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class FF4FEWorld(World):
    """Final Fantasy IV: Free Enterprise is an open world randomizer for the classic SNES RPG. Explore the world,
    find the Crystal, and defeat Zeromus on the moon. Adapted from the open source release of FE 4.6.0."""
    game = "Final Fantasy IV Free Enterprise"
    options_dataclass = FF4FEOptions
    options: FF4FEOptions
    settings: typing.ClassVar[FF4FESettings]

    web = FF4FEWebWorld()
    base_id = 7191991
    item_name_to_id = {item.name: id for
                       id, item in enumerate(all_items, base_id)}
    location_name_to_id = {location.name: id for
                           id, location in enumerate(all_locations, base_id)}
    item_name_groups = items.item_name_groups


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.rom_name_available_event = threading.Event()
        self.chosen_character = "None"
        self.objective_count = -1

    def is_vanilla_game(self):
        return self.get_objective_count() == 0

    def get_objective_count(self):
        if self.objective_count != -1:
            return self.objective_count
        else:
            objective_count = 0
            if self.options.ForgeTheCrystal:
                objective_count += 1
            if self.options.ConquerTheGiant:
                objective_count += 1
            if self.options.DefeatTheFiends:
                objective_count += 6
            if self.options.FindTheDarkMatter:
                objective_count += 1
            objective_count += self.options.AdditionalObjectives.value
            objective_count = min(objective_count, 32)
            self.objective_count = objective_count
            return min(objective_count, 32)

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        overworld = Region("Overworld", self.player, self.multiworld)
        underworld = Region("Underworld", self.player, self.multiworld)
        moon = Region("Moon", self.player, self.multiworld)

        self.multiworld.regions.append(overworld)
        self.multiworld.regions.append(underworld)
        self.multiworld.regions.append(moon)

        menu.connect(overworld)
        overworld.connect(underworld, "Underworld Access", lambda state: state.has("Hook", self.player)
                                                                         or state.has("Magma Key", self.player))
        overworld.connect(moon, "Moon Access", lambda state: state.has("Darkness Crystal", self.player))


        for area in topology.areas:
            new_region = Region(area, self.player, self.multiworld)
            self.multiworld.regions.append(new_region)
            if area in topology.overworld_areas:
                overworld.connect(new_region, "Overworld to " + area)
            if area in topology.hook_areas:
                underworld.connect(new_region, "Hook route to " + area, lambda state: state.has("Hook", self.player))
            if area in topology.underworld_areas:
                underworld.connect(new_region, "Underworld to " + area)
            if area in topology.moon_areas:
                moon.connect(new_region, "Moon to " + area)

        for location in all_locations:
            if location.name.startswith("Objective"): # Objectives aren't "real" locations
                continue
            if (self.options.ForgeTheCrystal.current_key == "forge" # Forge the Crystal doesn't have a Kokkol location.
                    and location.name == "Kokkol's House 2F -- Kokkol -- forge item"):
                continue
            region = self.multiworld.get_region(location.area, self.player)
            new_location = FF4FELocation(self.player, location.name, self.location_name_to_id[location.name], region)
            region.locations.append(new_location)

        for event in events.boss_events:
            region = self.multiworld.get_region(event.area, self.player)
            new_location = FF4FELocation(self.player, event.name, None, region)
            region.locations.append(new_location)

        if not self.is_vanilla_game():
            new_location = FF4FELocation(self.player, "Objectives Status", None, overworld)
            overworld.locations.append(new_location)
            new_location = FF4FELocation(self.player, "Objective Reward",
                                         self.location_name_to_id["Objective Reward"], overworld)
            overworld.locations.append(new_location)

        for i in range(self.get_objective_count()):
            new_location = FF4FELocation(self.player, f"Objective {i + 1} Status", None, overworld)
            overworld.locations.append(new_location)

    def create_item(self, item: str) -> FF4FEItem:
        item_data: ItemData = next((item_data for item_data in all_items if item_data.name == item), None)
        if not item_data:
            raise Exception(f"{item} is not a valid item name for Final Fantasy 4 Free Enterprise")
        return FF4FEItem(item, item_data.classification, self.item_name_to_id[item], self.player)

    def create_event(self, event: str) -> FF4FEItem:
        return FF4FEItem(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        item_pool, self.chosen_character, self.second_character = create_itempool(locations.all_locations, self)
        chosen_character_placed = False
        second_character_placed = False

        character_locations = locations.character_locations.copy()
        character_locations.remove("Starting Character 1")
        character_locations.remove("Starting Character 2")
        if self.options.ConquerTheGiant:
            character_locations.remove("Giant of Bab-il Character")
        if self.options.NoFreeCharacters:
            for location in locations.free_character_locations:
                character_locations.remove(location)
                self.get_location(location).place_locked_item(self.create_item("None"))
                item_pool.remove("None")
        if self.options.NoEarnedCharacters:
            for location in locations.earned_character_locations:
                character_locations.remove(location)
                self.get_location(location).place_locked_item(self.create_item("None"))
                item_pool.remove("None")

        restricted_character_allow_locations = sorted(set(character_locations) - set(locations.restricted_character_locations))
        restricted_character_forbid_locations = sorted(set(character_locations) - set(restricted_character_allow_locations))
        self.random.shuffle(restricted_character_allow_locations)
        self.random.shuffle(restricted_character_forbid_locations)

        for item in map(self.create_item, item_pool):
            # If we've specifically chosen a starting character, we place them directly even though we're not normally
            # allowed to have a restricted character as a starter.
            if item.name == self.chosen_character and not chosen_character_placed:
                self.get_location("Starting Character 1").place_locked_item(self.create_item(self.chosen_character))
                chosen_character_placed = True
                continue
            elif item.name == self.second_character and not second_character_placed:
                self.get_location("Starting Character 2").place_locked_item(self.create_item(self.second_character))
                second_character_placed = True
                continue
            elif item.name in items.characters:
                if item.name in self.options.RestrictedCharacters.value:
                    # Place restricted characters where they're allowed first, then into the other spots.
                    if len(restricted_character_allow_locations) > 0:
                        self.get_location(restricted_character_allow_locations.pop()).place_locked_item(self.create_item(item.name))
                    else:
                        self.get_location(restricted_character_forbid_locations.pop()).place_locked_item(self.create_item(item.name))
                else:
                    # Inverse of the above: unrestricted characters go into the unrestricted slots first to leave room
                    # for the restricted characters.
                    if len(restricted_character_forbid_locations) > 0:
                        self.get_location(restricted_character_forbid_locations.pop()).place_locked_item(self.create_item(item.name))
                    else:
                        self.get_location(restricted_character_allow_locations.pop()).place_locked_item(self.create_item(item.name))
                continue
            if item.name == "Crystal":
                if not self.is_vanilla_game():
                    (self.get_location("Objective Reward")
                     .place_locked_item(self.create_item("Crystal")))
                    continue
            if item.name.startswith("Objective"): # Objectives get manually placed later.
                continue
            self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        # Unplaced characters don't go in noncharacter slots, and we force slots with no character to None.
        for location in locations.character_locations:
            add_item_rule(self.get_location(location),
                          lambda item: item.name in items.characters and item.player == self.player)
            if self.options.NoFreeCharacters:
                if location in locations.free_character_locations:
                    add_item_rule(self.get_location(location),
                                  lambda item: item.name == "None")
            if self.options.NoEarnedCharacters:
                if location in locations.earned_character_locations:
                    add_item_rule(self.get_location(location),
                                  lambda item: item.name == "None")
            if len(self.options.AllowedCharacters.value.difference(self.options.RestrictedCharacters.value)) > 0:
                if location in locations.restricted_character_locations:
                    add_item_rule(self.get_location(location),
                                  lambda item: item.name not in self.options.RestrictedCharacters.value)


        for location in locations.all_locations:
            if location.name not in locations.character_locations:
                # Skip over any objectives or the Kokkol slot if they're not actually in this location pool due to options.
                if location.name.startswith("Objective") or location.name == "Kokkol's House 2F -- Kokkol -- forge item":
                    try:
                        self.get_location(location.name)
                    except KeyError:
                        continue
                # No characters in noncharacter slots, of course
                add_item_rule(self.get_location(location.name),
                              lambda item: item.name not in items.characters)
                # No key items except Dark Matters in minor slots when we're doing major/minor split.
                if (self.options.ItemPlacement.current_key == "major_minor_split" and not location.major_slot
                        and location.name not in self.options.priority_locations):
                    forbid_items_for_player(self.get_location(location.name), set(items.characters), self.player)

        # Conquer the Giant doesn't have a character, so we force it to None.
        if self.options.ConquerTheGiant:
            (self.get_location(
                "Giant of Bab-il Character")
             .place_locked_item(self.create_item("None")))

        # If we're doing Hero Challenge and we're not doing Forge the Crystal, Kokkol has a fancy weapon for our Hero.
        # The actual weapon is determined by Free Enterprise, so you can't hint if it's an Excalipur and remove
        # the potential comedy.
        if (self.options.HeroChallenge.current_key != "none"
                and not self.options.ForgeTheCrystal):
            self.get_location(
                "Kokkol's House 2F -- Kokkol -- forge item").place_locked_item(self.create_item("Advance Weapon"))

        # Zeromus requires the Pass or Moon access in addition to the Crystal. Mostly just makes the spoiler log nicer.
        set_rule(self.get_location("Zeromus"),
                 lambda state: state.has("Pass", self.player)
                                or state.has("Darkness Crystal", self.player))

        for location in [location for location in all_locations]:
            # Hook areas, of course, require Hook.
            if location.area in topology.hook_areas:
                add_rule(self.get_location(location.name),
                         lambda state: state.has("Hook", self.player))
            if location.area in topology.underworld_areas:
                # Skip over Kokkol on Forge the Crystal...
                if location.name == "Kokkol's House 2F -- Kokkol -- forge item":
                    if not location.name in self.multiworld.regions.location_cache[self.player]:
                        continue
                # ...but otherwise all underground locations require underground access.
                add_rule(self.get_location(location.name),
                         lambda state: state.has("Hook", self.player) or state.has("Magma Key", self.player))
            # Moon needs the ability to get to the moon.
            if location.area in topology.moon_areas:
                add_rule(self.get_location(location.name),
                         lambda state: state.has("Darkness Crystal", self.player))
                if self.options.UnsafeKeyItemPlacement:
                    add_rule(self.get_location(location.name),
                             lambda state: state.has("Hook", self.player) or state.has("Magma Key", self.player))
            # Otherwise, we consult the list of area-specific rules (e.g. Baron Castle requires Baron Key)..
            if location.area in FERules.area_rules.keys():
                for requirement in FERules.area_rules[location.area]:
                    add_rule(self.get_location(location.name),
                             lambda state, true_requirement=requirement: state.has(true_requirement, self.player))
            # Major slots must have useful or better.
            if location.major_slot and location.name not in self.options.exclude_locations:
                add_item_rule(self.get_location(location.name),
                              lambda item: (item.classification & (ItemClassification.useful | ItemClassification.progression)) > 0)
            # The "harder" an area, the more key items and characters we need to access.
            # This does two things. First, it ensures a wider distribution of key items so sphere 1 can't just be one
            # piece of progression, which isn't fun in FE.
            # Second of all, it includes characters in the requirements so a lategame FE area isn't equivalent to an early
            # Zelda dungeon for progression balancing.
            # Also it makes the spoiler playthrough nicer.
            for i in range(len(FERules.location_tiers.keys())):
                if (location.area in FERules.location_tiers[i]
                        and self.options.ItemPlacement.current_key == "normal"
                        and location.name not in locations.character_locations
                        and not location.name.startswith("Objective")):
                    add_rule(self.get_location(location.name),
                             lambda state, tier=i: state.has_group("characters",
                                                           self.player,
                                                           FERules.logical_gating[tier]["characters"]) and
                                           state.has_group("key_items",
                                                           self.player,
                                                           FERules.logical_gating[tier]["key_items"]))

        # Boss events follow the same rules, but they're not real locations.
        for location in [event for event in events.boss_events]:
            if location.area in topology.hook_areas:
                add_rule(self.get_location(location.name),
                         lambda state: state.has("Hook", self.player))
            if location.area in topology.underworld_areas:
                add_rule(self.get_location(location.name),
                         lambda state: state.has("Hook", self.player) or state.has("Magma Key", self.player))
            if location.area in topology.moon_areas:
                add_rule(self.get_location(location.name),
                         lambda state: state.has("Darkness Crystal", self.player))
                if self.options.UnsafeKeyItemPlacement:
                    add_rule(self.get_location(location.name),
                             lambda state: state.has("Hook", self.player) or state.has("Magma Key", self.player))
            if location.name in FERules.boss_rules.keys():
                for requirement in FERules.boss_rules[location.name]:
                    add_rule(self.get_location(location.name),
                             lambda state, true_requirement=requirement: state.has(true_requirement, self.player))
            for i in range(len(FERules.location_tiers.keys())):
                if location.area in FERules.location_tiers[i]:
                    add_rule(self.get_location(location.name),
                             lambda state, tier=i: state.has_group("characters",
                                                           self.player,
                                                           FERules.logical_gating[tier]["characters"]) and
                                           state.has_group("key_items",
                                                           self.player,
                                                           FERules.logical_gating[tier]["key_items"]))

        # Some locations need bespoke rules. This applies them.
        for location in FERules.individual_location_rules.keys():
            if location in self.multiworld.regions.location_cache[self.player]:
                ap_location = self.get_location(location)
                for requirement in FERules.individual_location_rules[location]:
                    add_rule(ap_location,
                             lambda state, true_requirement=requirement: state.has(true_requirement, self.player))

        # Bosses get locked events for spoiler log niceness.
        for event in events.boss_events:
            self.get_location(event.name).place_locked_item(
                self.create_event(event.name + " Defeated")
            )

        # Zeromus also requires the Crystal...when he needs to be fought.
        add_item_rule(self.get_location("Zeromus"),
                      lambda state: state.has("Crystal", self.player)
                                    or (self.options.ObjectiveReward.current_key == "win"
                                        and not self.is_vanilla_game()))

        # Specific objectives are FE's problem, not AP's. So on the AP side, clearing all objective
        # requires all relevant key items.
        for i in range(self.get_objective_count()):
            (self.get_location(f"Objective {i + 1} Status")
                       .place_locked_item(self.create_item(f"Objective {i + 1} Cleared")))
            for requirement in FERules.individual_location_rules["Objectives Status"]:
                add_rule(self.get_location(f"Objective {i + 1} Status"),
                         lambda state, true_requirement=requirement: state.has(true_requirement, self.player))

        # Just an event to make the spoiler playthrough look nicer.
        if not self.is_vanilla_game():
            self.get_location("Objectives Status").place_locked_item(
                self.create_event("All Objectives Cleared")
            )

        # If we have no objectives or objectives award the crystal, Zeromus is the win condition.
        # Otherwise, clearing all objectives secures victory.
        if (self.options.ObjectiveReward.current_key == "crystal"
                or self.is_vanilla_game()):
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Zeromus Defeated", self.player)

        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("All Objectives Cleared", self.player)

    def post_fill(self) -> None:
        unfilled_locations = self.multiworld.get_unfilled_locations(self.player)
        for location in unfilled_locations:
            location.item = self.create_item(self.get_filler_item_name())

    def generate_output(self, output_directory: str) -> None:
        # Standard rom name stuff.
        self.rom_name_text = f'4FE{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
        self.rom_name_text = self.rom_name_text[:20]
        self.rom_name = bytearray(self.rom_name_text, 'utf-8')
        self.rom_name.extend([0] * (20 - len(self.rom_name)))
        self.rom_name_available_event.set()

        # The placement dictionary file is what FE will use to place things.
        placement_dict = self.create_placement_file(str(self.rom_name_text))
        # We need the seed for FE to be deterministic, but not the same as another player in the game.
        placement_dict["seed"] = self.player + self.multiworld.seed
        placement_dict["output_file"] = f'{self.multiworld.get_out_file_name_base(self.player)}' + '.sfc'
        placement_dict["flags"] = flags.create_flags_from_options(self.options, self.objective_count)
        placement_dict["junk_tier"] = self.options.JunkTier.value
        placement_dict["junked_items"] = list(self.options.JunkedItems.value)
        placement_dict["kept_items"] = list(self.options.KeptItems.value)
        placement_dict["data_dir"] = Utils.user_path("data", "ff4fe")

        # Our actual patch is just a set of instructions and data for FE to use.
        patch = FF4FEProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("placement_file.json" , json.dumps(placement_dict).encode("UTF-8"))
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Slot data needed for tracker logic.
        slot_data = {
            "DarkMatterHunt": self.options.FindTheDarkMatter.current_key,
            "NoEarnedCharacters": self.options.NoEarnedCharacters.current_key,
            "NoFreeCharacters": self.options.NoEarnedCharacters.current_key,
            "PassEnabled": self.options.PassEnabled.current_key,
            "AdditionalObjectives": self.options.AdditionalObjectives.value,
            "ObjectiveReward": self.options.ObjectiveReward.current_key,
            "UnsafeKeyItemPlacement": self.options.UnsafeKeyItemPlacement.current_key,
            "ObjectivesRequired": self.options.RequiredObjectiveCount.value
        }
        return slot_data

    def create_placement_file(self, rom_name):
        placement_dict = {"rom_name": rom_name}
        for location in self.multiworld.get_filled_locations(self.player):
            # Placement dictionary doesn't need AP event logic stuff.
            if location.name in [event.name for event in events.boss_events] or location.name.startswith("Objective"):
                continue
            location_data = [loc for loc in all_locations if loc.name == location.name].pop()
            if location.item.player == self.player:
                item_data = [item for item in all_items if item.name == location.item.name].pop()
                placement_dict[location_data.fe_id] = {
                    "location_data": location_data.to_json(),
                    "item_data": item_data.to_json(),
                    "item_name": item_data.name,
                    "player_name": self.multiworld.player_name[location.item.player]
                }
            else:
                placement_dict[location_data.fe_id] = {
                    "location_data": location_data.to_json(),
                    "item_data": ItemData.create_ap_item().to_json(),
                    "item_name": location.item.name,
                    "player_name": self.multiworld.player_name[location.item.player]
                }
        return placement_dict

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def get_filler_item_name(self) -> str:
        filler_items = [item.name for item in items.filler_items]
        return self.random.choice(filler_items)
