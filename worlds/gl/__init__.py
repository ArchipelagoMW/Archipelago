import os
import settings

from BaseClasses import ItemClassification, Tutorial, Item, CollectionState
from Fill import fast_fill
from typing import ClassVar

from worlds.AutoWorld import WebWorld, World

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
from .Data import item_dict, local_levels, skipped_local_locations, obelisks, mirror_shards
from .Items import GLItem, item_table, item_list
from .Locations import LocationData, all_locations, location_table
from .Options import GLOptions
from .Regions import connect_regions, create_regions
from .Rom import GLProcedurePatch, write_files
from .Rules import set_rules


def launch_client(*args):
    from .GauntletLegendsClient import launch
    launch_subprocess(launch, name="GauntletLegendsClient", args=args)


components.append(
    Component(
        "Gauntlet Legends Client",
        func=launch_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apgl"),
    ),
)


class GauntletLegendsWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to playing Gauntlet Legends",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["jamesbrq"],
        ),
    ]


class GLSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the GL US rom"""

        copy_to = "Gauntlet Legends (U) [!].z64"
        description = "Gauntlet Legends ROM File"
        md5s = ["9cb963e8b71f18568f78ec1af120362e"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = False


class GauntletLegendsWorld(World):
    """
    Adventure through the 5 realms to collect 13 runestones
    and defeat the evil skorne. Treasure, enemies, and death
    awaits.
    """

    game = "Gauntlet Legends"
    web = GauntletLegendsWebWorld()
    options_dataclass = GLOptions
    options: GLOptions
    settings: ClassVar[GLSettings]
    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    excluded_regions: set
    death: list[Item]
    items: list[Item]

    disabled_locations: set[str]

    def generate_early(self) -> None:
        self.disabled_locations = set()
        self.excluded_regions = set()
        self.death = []
        self.items = []
        self.options.max_difficulty_value.value = max(self.options.max_difficulty_value.value, self.options.local_players.value)

    def create_regions(self) -> None:
        if self.options.chests_barrels == "none":
            self.disabled_locations.update([
                location.name
                for location in all_locations
                if "Chest" in location.name or ("Barrel" in location.name and "Barrel of Gold" not in location.name)
            ])
        elif self.options.chests_barrels == "all_chests":
            self.disabled_locations.update([
                location.name
                for location in all_locations
                if "Barrel" in location.name and "Barrel of Gold" not in location.name
            ])
        elif self.options.chests_barrels == "all_barrels":
            self.disabled_locations.update([location.name for location in all_locations if "Chest" in location.name])

        if self.options.max_difficulty_toggle:
            self.disabled_locations.update([location.name for location in all_locations
                                        if location.difficulty > self.options.max_difficulty_value])

        create_regions(self)
        connect_regions(self)
        if not self.options.infinite_keys:
            self.lock_item("Valley of Fire - Key 1", "Key")
            self.lock_item("Valley of Fire - Key 5", "Key")

        if not self.options.obelisks:
            self.lock_item("Valley of Fire - Obelisk", "Mountain Obelisk 1")
            self.lock_item("Dagger Peak - Obelisk", "Mountain Obelisk 2")
            self.lock_item("Cliffs of Desolation - Obelisk", "Mountain Obelisk 3")
            self.lock_item("Castle Courtyard - Obelisk", "Castle Obelisk 1")
            self.lock_item("Dungeon of Torment - Obelisk", "Castle Obelisk 2")
            self.lock_item("Poisoned Fields - Obelisk", "Town Obelisk 1")
            self.lock_item("Haunted Cemetery - Obelisk", "Town Obelisk 2")

        if not self.options.mirror_shards:
            self.lock_item("Dragon's Lair - Dragon Mirror Shard", "Dragon Mirror Shard")
            self.lock_item("Chimera's Keep - Chimera Mirror Shard", "Chimera Mirror Shard")
            self.lock_item("Vat of the Plague Fiend - Plague Fiend Mirror Shard", "Plague Fiend Mirror Shard")
            self.lock_item("Yeti's Cavern - Yeti Mirror Shard", "Yeti Mirror Shard")

    def fill_slot_data(self) -> dict:
        dshard = self.get_location("Dragon's Lair - Dragon Mirror Shard").item
        yshard = self.get_location("Yeti's Cavern - Yeti Mirror Shard").item
        cshard = self.get_location("Chimera's Keep - Chimera Mirror Shard").item
        fshard = self.get_location("Vat of the Plague Fiend - Plague Fiend Mirror Shard").item
        shard_values = [
            item_dict[dshard.code] if dshard.player == self.player else [0x27, 0x4],
            item_dict[yshard.code] if yshard.player == self.player else [0x27, 0x4],
            item_dict[cshard.code] if cshard.player == self.player else [0x27, 0x4],
            item_dict[fshard.code] if fshard.player == self.player else [0x27, 0x4],
        ]
        characters = [
            self.options.unlock_character_one.value,
            self.options.unlock_character_two.value,
            self.options.unlock_character_three.value,
            self.options.unlock_character_four.value,
        ]
        chests_barrels = self.options.chests_barrels.value
        return {
            "player": self.player,
            "players": self.options.local_players.value,
            "shards": shard_values,
            "chests": bool(chests_barrels == 3 or chests_barrels == 1),
            "barrels": bool(chests_barrels == 3 or chests_barrels == 2),
            "speed": self.options.permanent_speed.value,
            "keys": self.options.infinite_keys.value,
            "characters": characters,
            "max": (self.options.max_difficulty_value.value if self.options.max_difficulty_toggle else 4),
            "instant_max": self.options.instant_max.value,
            "death_link": bool((self.options.death_link.value == 1))
        }

    def create_items(self) -> None:
        # First add in all progression and useful items
        required_items = []
        precollected = [item for item in item_list if item.item_name in [item.name for item in self.multiworld.precollected_items[self.player]]]
        skipped_items = set()
        item_required_count = len(self.multiworld.get_unfilled_locations(self.player))
        if self.options.infinite_keys:
            skipped_items.add("Key")
        if self.options.permanent_speed:
            skipped_items.add("Boots")
        if self.options.traps_choice == "only_death" or self.options.traps_choice == "none_active":
            skipped_items.add("Poison Fruit")
        if self.options.traps_choice == "only_fruit" or self.options.traps_choice == "none_active":
            skipped_items.add("Death")
        if not self.options.obelisks:
            skipped_items.update(obelisks)
        if not self.options.mirror_shards:
            skipped_items.update(mirror_shards)
        for item in [item_ for item_ in item_list
                     if (ItemClassification.progression in item_.progression
                     or ItemClassification.useful in item_.progression)
                     and item_.item_name not in precollected
                     and item_.item_name not in skipped_items]:
            freq = item.frequency
            required_items += [item.item_name for _ in range(freq)]
            item_required_count -= freq

        self.multiworld.itempool += [self.create_item(item_name) for item_name in required_items]

        # Then, get a random amount of fillers until we have as many items as we have locations
        filler_items = []
        for item in [item_ for item_ in item_list
                     if ItemClassification.progression not in item_.progression
                     and ItemClassification.useful not in item_.progression
                     and item_.item_name not in skipped_items]:

            freq = item.frequency + (30 if self.options.infinite_keys else 0) + (5 if self.options.permanent_speed else 0)
            if item.item_name == "Invulnerability" or item.item_name == "Anti-Death Halo":
                freq = item.frequency
            if item.item_name == "Anti-Death Halo" and "Death" not in skipped_items and self.options.traps_frequency >= 50:
                freq *= 2

            filler_items += [item.item_name for _ in range(freq)]
            self.random.shuffle(filler_items)

        traps_frequency = int(len(self.get_locations()) * (self.options.traps_frequency / 100))
        if self.options.traps_choice == "all_active":
            traps_frequency //= 2
        if self.options.traps_choice == "only_death" or self.options.traps_choice == "all_active":
            self.death += [self.create_item("Death") for _ in range(traps_frequency)]
            item_required_count -= traps_frequency
        if self.options.traps_choice == "only_fruit" or self.options.traps_choice == "all_active":
            self.multiworld.itempool += [self.create_item("Poison Fruit") for _ in range(traps_frequency)]
            item_required_count -= traps_frequency

        for i in range(item_required_count):
            if i < int(item_required_count * (self.options.local_filler_frequency / 100)):
                self.items.append(self.create_item(filler_items.pop()))
            else:
                self.multiworld.itempool.append(self.create_item(filler_items.pop()))


    def set_rules(self) -> None:
        set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(
            "Gates of the Underworld", "Region", self.player,
        )

    def pre_fill(self) -> None:
        # A percentage of all items will be placed locally, all deaths will be placed locally
        local_item_count = len(self.items) + len(self.death)
        local_locations = []
        unfilled_locations = self.multiworld.get_unfilled_locations(self.player)
        unfilled_names = {location.name for location in unfilled_locations}

        for level in local_levels:
            level = [location for location in level if
                     location.name in unfilled_names and location.name not in skipped_local_locations]
            self.random.shuffle(level)
            for i in range(min(len(level), (local_item_count // len(local_levels)) + 3)):
                local_locations.append(self.get_location(level[i].name))

        # If we don't have enough locations, add more from remaining unfilled locations
        if len(local_locations) < local_item_count:
            used_location_names = {loc.name for loc in local_locations}
            remaining_unfilled = [loc for loc in unfilled_locations
                                  if loc.name not in used_location_names
                                  and loc.name not in skipped_local_locations]
            self.random.shuffle(remaining_unfilled)

            needed = local_item_count - len(local_locations)
            for i in range(min(needed, len(remaining_unfilled))):
                local_locations.append(remaining_unfilled[i])

        # Only slice if we have more than needed
        local_locations = local_locations[:local_item_count]
        self.random.shuffle(self.items)
        self.random.shuffle(local_locations)
        fast_fill(self.multiworld, self.items + self.death, local_locations)

    def create_item(self, name: str) -> GLItem:
        item = item_table[name]
        return GLItem(item.item_name, item.progression, item.id, self.player)

    def lock_item(self, location: str, item_name: str):
        item = self.create_item(item_name)
        self.get_location(location).place_locked_item(item)

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        if change and "Runestone" in item.name:
            state.prog_items[item.player]["stones"] += 1
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change and "Runestone" in item.name:
            state.prog_items[item.player]["stones"] -= 1
        return change

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(filter(lambda item: item.progression == ItemClassification.filler, item_list))).item_name

    def generate_output(self, output_directory: str) -> None:
        patch = GLProcedurePatch(player=self.player, player_name=self.player_name)
        write_files(self, patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}",
        )
        patch.write(rom_path)
