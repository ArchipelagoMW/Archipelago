import os

import settings

from BaseClasses import ItemClassification, Tutorial, Item, CollectionState
from Fill import fast_fill
from typing import ClassVar

from worlds.AutoWorld import WebWorld, World

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
from .Data import obelisks, mirror_shards, portals, excluded_portals, \
    excluded_obelisks, level_locations
from .Items import GLItem, item_table, item_list, gauntlet_item_name_groups
from .Locations import LocationData, all_locations, location_table, get_locations_by_tags
from .Options import GLOptions, IncludedAreas, IncludedTraps
from .Regions import connect_regions, create_regions
from .Rom import GLProcedurePatch, write_files
from .Rules import set_rules, goal_conditions


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
    class RetorarchPath(settings.UserFolderPath):
        """The location of your Retroarch folder"""
        description = "Retroarch Folder"

    class RomFile(settings.UserFilePath):
        """File name of the GL US rom"""
        copy_to = "Gauntlet Legends (U) [!].z64"
        description = "Gauntlet Legends ROM File"
        md5s = ["9cb963e8b71f18568f78ec1af120362e"]

    retroarch_path: RetorarchPath = RetorarchPath(None)
    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


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
    item_name_groups = gauntlet_item_name_groups
    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    excluded_regions: set
    items: list[Item]
    unlockable: set

    disabled_locations: set[str]

    def generate_early(self) -> None:
        self.disabled_locations = set()
        self.excluded_regions = set()
        self.unlockable = set()
        self.items = []

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

        self.disabled_locations.update([location.name for location in all_locations
                                        if location.difficulty > self.options.max_difficulty])
        self.excluded_regions.update([region for region in IncludedAreas.valid_keys if region not in self.options.included_areas.value])
        self.options.boss_goal_count.value = min(self.options.boss_goal_count.value,
                                                 6 - len([region for region in self.excluded_regions if region != "Battlefield"]))

        create_regions(self)
        connect_regions(self)
        if not self.options.infinite_keys:
            self.lock_item("Valley of Fire - Key 1", "Key")
            self.lock_item("Valley of Fire - Key 5", "Key")

        if not self.options.obelisks:
            self.lock_item("Valley of Fire - Obelisk", "Valley of Fire Obelisk")
            self.lock_item("Dagger Peak - Obelisk", "Dagger Peak Obelisk")
            self.lock_item("Cliffs of Desolation - Obelisk", "Cliffs of Desolation Obelisk")
            self.lock_item("Castle Courtyard - Obelisk", "Castle Courtyard Obelisk")
            self.lock_item("Dungeon of Torment - Obelisk", "Dungeon of Torment Obelisk")
            self.lock_item("Poisoned Fields - Obelisk", "Poisoned Fields Obelisk")
            self.lock_item("Haunted Cemetery - Obelisk", "Haunted Cemetery Obelisk")

        if not self.options.mirror_shards:
            self.lock_item("Dragon's Lair - Dragon Mirror Shard", "Dragon Mirror Shard")
            self.lock_item("Chimera's Keep - Chimera Mirror Shard", "Chimera Mirror Shard")
            self.lock_item("Vat of the Plague Fiend - Plague Fiend Mirror Shard", "Plague Fiend Mirror Shard")
            self.lock_item("Yeti's Cavern - Yeti Mirror Shard", "Yeti Mirror Shard")

    def fill_slot_data(self) -> dict:
        characters = [
            self.options.unlock_character_one.value,
            self.options.unlock_character_two.value,
            self.options.unlock_character_three.value,
            self.options.unlock_character_four.value,
        ]
        chests_barrels = self.options.chests_barrels.value
        return {
            "player": self.player,
            "chests": int(chests_barrels == 3 or chests_barrels == 1),
            "barrels": int(chests_barrels == 3 or chests_barrels == 2),
            "speed": self.options.permanent_speed.value,
            "keys": self.options.infinite_keys.value,
            "characters": characters,
            "max": self.options.max_difficulty.value,
            "instant_max": self.options.instant_max.value,
            "death_link": self.options.death_link.value,
            "portals": self.options.portals.value,
            "included_areas": [area for area in IncludedAreas.valid_keys if area in self.options.included_areas.value],
            "mirror_shards": self.options.mirror_shards.value,
            "obelisks": self.options.obelisks.value,
            "goal": self.options.goal.value,
            "boss_goal_count": self.options.boss_goal_count.value,
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
            skipped_items.add("Speed Boots")
        skipped_items.update([item for item in IncludedTraps.valid_keys if item not in self.options.included_traps.value])
        if not self.options.obelisks:
            skipped_items.update([obelisk for obelisk in obelisks if obelisk not in self.unlockable])
        if not self.options.mirror_shards:
            skipped_items.update([shard for shard in mirror_shards if shard not in self.unlockable])
        if not self.options.portals:
            skipped_items.update([item for item in portals.keys()])
        if len(self.excluded_regions) > 0:
            for region in self.excluded_regions:
                skipped_items.update(excluded_portals.get(region, []))
                skipped_items.update(excluded_obelisks.get(region, []))
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

            freq = item.frequency
            if item.item_name == "Anti-Death Halo" and "Death" not in skipped_items and self.options.traps_frequency.value >= 30:
                freq *= 2

            filler_items += [item.item_name for _ in range(freq)]
            self.random.shuffle(filler_items)

        if len(self.options.included_traps.value) != 0:
            traps_frequency = int(len(self.get_locations()) * (self.options.traps_frequency / 100)) // len(self.options.included_traps.value)
            for item in self.options.included_traps.value:
                self.multiworld.itempool += [self.create_item(item) for _ in range(traps_frequency)]
                item_required_count -= traps_frequency

        for i in range(item_required_count):
            if i < int(item_required_count * (self.options.local_filler_frequency / 100)):
                if self.multiworld.players > 1:
                    self.items.append(self.create_item(filler_items.pop()))
                else:
                    self.multiworld.itempool.append(self.create_item(filler_items.pop()))
            else:
                self.multiworld.itempool.append(self.create_item(filler_items.pop()))


    def set_rules(self) -> None:
        set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: goal_conditions(state, self)

    def pre_fill(self) -> None:
        local_item_count = len(self.items)
        unfilled_locations = self.multiworld.get_unfilled_locations(self.player)
        unfilled_names = {loc.name for loc in unfilled_locations}
        skipped = get_locations_by_tags("skipped_local")
        no_obelisk_locs = get_locations_by_tags("no_obelisks")

        # Group available locations by level
        level_locs = {}
        for level_id, level in level_locations.items():
            if level_id & 0x8 == 0x8:
                continue
            available = [loc for loc in level if loc.name in unfilled_names and loc.name not in skipped]
            if available:
                level_locs[level_id] = sorted(available, key=lambda l: l.difficulty, reverse=True)

        all_available = [loc for locs in level_locs.values() for loc in locs]

        # Calculate target per level, ensuring we don't fill entire regions
        target_per_level = (local_item_count // len(level_locs)) + 2 if level_locs else 0
        local_locations = []

        for level_id, locs in level_locs.items():
            # Leave at least 1 location unfilled per region if possible
            max_from_level = max(1, len(locs) - 1) if len(locs) > 1 else len(locs)
            count = min(target_per_level, max_from_level)

            # Split into harder/easier halves
            mid = len(locs) // 2
            harder, easier = locs[:mid], locs[mid:]
            self.random.shuffle(harder)
            self.random.shuffle(easier)

            # Take 60% from harder, 40% from easier
            harder_count = int(count * 0.6)
            easier_count = count - harder_count
            local_locations.extend(self.get_location(l.name) for l in harder[:harder_count])
            local_locations.extend(self.get_location(l.name) for l in easier[:easier_count])

        # If still need more, pull from levels with most remaining availability
        if len(local_locations) < local_item_count:
            used_names = {loc.name for loc in local_locations}
            remaining = []
            for level_id, locs in level_locs.items():
                available = [l for l in locs if l.name not in used_names]
                for loc in available:
                    remaining.append((loc, len(available)))

            remaining.sort(key=lambda x: x[1], reverse=True)
            needed = local_item_count - len(local_locations)
            local_locations.extend(self.get_location(loc.name) for loc, _ in remaining[:needed])

        # Ensure obelisk accessibility
        used_names = {loc.name for loc in local_locations}
        remaining_unfilled = [loc.name for loc in all_available if loc.name not in used_names]

        if remaining_unfilled and all(name in no_obelisk_locs for name in remaining_unfilled):
            chosen_no_obelisk = [loc for loc in local_locations if loc.name in no_obelisk_locs]
            unchosen_obelisk_ok = [loc for loc in all_available
                                   if loc.name not in used_names and loc.name not in no_obelisk_locs]

            swap_count = min(len(chosen_no_obelisk) // 2, len(unchosen_obelisk_ok))
            if swap_count > 0:
                self.random.shuffle(chosen_no_obelisk)
                self.random.shuffle(unchosen_obelisk_ok)

                for i in range(swap_count):
                    local_locations.remove(chosen_no_obelisk[i])
                    local_locations.append(self.get_location(unchosen_obelisk_ok[i].name))

        # Final shuffle and fill
        local_locations = local_locations[:local_item_count]
        self.random.shuffle(self.items)
        self.random.shuffle(local_locations)
        fast_fill(self.multiworld, self.items, local_locations)

    def create_item(self, name: str) -> GLItem:
        item = item_table[name]
        return GLItem(item.item_name, item.progression, item.id, self.player)

    def lock_item(self, location: str, item_name: str) -> None:
        item = self.create_item(item_name)
        if location in self.disabled_locations:
            self.unlockable.update({item_name})
            return
        self.get_location(location).place_locked_item(item)

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        if change and "Runestone" in item.name:
            state.prog_items[item.player]["stones"] += 1
        if change and (ItemClassification.progression in item.classification):
            state.prog_items[item.player]["progression"] += 1
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change and "Runestone" in item.name:
            state.prog_items[item.player]["stones"] -= 1
        if change and (ItemClassification.progression in item.classification):
            state.prog_items[item.player]["progression"] -= 1
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
