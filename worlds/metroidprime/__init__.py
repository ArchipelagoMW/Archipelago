from pathlib import Path
from typing import Any, Dict, List
from BaseClasses import Item, Tutorial, ItemClassification
from .Items import MetroidPrimeItem, suit_upgrade_table, artifact_table, item_table, custom_suit_upgrade_table
from .PrimeOptions import MetroidPrimeOptions
from .Locations import every_location
from .Regions import create_regions
from .Rules import set_rules
from .config import make_config
from worlds.AutoWorld import World
from ..AutoWorld import WebWorld
import py_randomprime
import settings


class MetroidPrimeSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Metroid Prime ISO"""
        description = "Metroid Prime (US) v1.0 ISO file"
        copy_to = "prime.iso"

    rom_file: RomFile = RomFile.copy_to


class MetroidPrimeWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Metroid Prime for Archipelago",
        "English",
        "setup.md",
        "setup/en",
        ["Electro15", "hesto2"]
    )]


class MetroidPrimeWorld(World):
    """
    Metroid Prime is a first-person action-adventure game originally for the Gamecube. Play as
    the bounty hunter Samus Aran as she traverses the planet Tallon IV and uncovers the plans
    of the Space Pirates.
    """
    game = "Metroid Prime"
    web = MetroidPrimeWeb()
    options_dataclass = MetroidPrimeOptions
    options: MetroidPrimeOptions
    topology_present = True
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = every_location
    settings: MetroidPrimeSettings

    def create_regions(self) -> None:
        boss_selection = int(self.options.final_bosses)
        create_regions(self, boss_selection)

    def create_item(self, name: str, override: bool = False) -> "Item":
        createdthing = item_table[name]
        if override:
            return MetroidPrimeItem(name, ItemClassification.progression, createdthing.code, self.player)
        return MetroidPrimeItem(name, createdthing.classification, createdthing.code, self.player)

    def create_items(self) -> None:
        # add artifacts
        items_added = 0
        reqarts = int(self.options.required_artifacts)
        precollectedarts = [*artifact_table][reqarts:]
        neededarts = [*artifact_table][:reqarts]
        for i in precollectedarts:
            self.multiworld.push_precollected(self.create_item(i))
        for i in neededarts:
            self.multiworld.itempool += [self.create_item(i)]
            items_added += 1
        excluded = self.options.exclude_items
        spring = int(self.options.spring_ball)
        if spring == 1:
            self.multiworld.itempool += [self.create_item("Spring Ball")]
            items_added += 1
        for i in {*suit_upgrade_table, *custom_suit_upgrade_table}:
            if i == "Power Beam" or i == "Scan Visor" or i == "Power Suit" or i == "Combat Visor":
                self.multiworld.push_precollected(self.create_item(i))
            elif i in excluded.keys():
                continue
            elif i == "Missile Expansion":
                for j in range(0, 8):
                    self.multiworld.itempool += [
                        self.create_item('Missile Expansion', True)]
                items_added += 8
            elif i == "Spring Ball":
                continue
            elif i == "Energy Tank":
                for j in range(0, 8):
                    self.multiworld.itempool += [
                        self.create_item("Energy Tank", True)]
                for j in range(0, 6):
                    self.multiworld.itempool += [
                        self.create_item("Energy Tank")]
                items_added += 14
                continue
            elif i == "Ice Trap":
                continue
            elif i == "Power Bomb Expansion":
                for j in range(0, 4):
                    self.multiworld.itempool += [
                        self.create_item("Power Bomb Expansion")]
                items_added += 4
            else:
                self.multiworld.itempool += [self.create_item(i)]
                items_added += 1
        # add missiles in whatever slots we have left
        remain = 100 - items_added
        for i in range(0, remain):
            self.multiworld.itempool += [self.create_item("Missile Expansion")]

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player, every_location)
        self.multiworld.completion_condition[self.player] = lambda state: (
            state.can_reach("Mission Complete", "Region", self.player))

    def generate_output(self, output_directory: str) -> None:
        configjson = make_config(self)
        # convert configjson to json
        import json

        configjsons = json.dumps(configjson, indent=4)
        # TODO: Remove this later
        # write configjson to a file for review
        with open("config.json", "w") as file:
            file.write(configjsons)
        notifier = py_randomprime.ProgressNotifier(lambda progress, message: print("Generating ISO: ", progress, message))

        input_iso_path = Path(settings.get_settings().metroidprime_options.rom_file)
        output_iso_path = Path(f"{output_directory}\prime_out.iso")

        py_randomprime.patch_iso(input_iso_path, output_iso_path, configjson, notifier)

    def fill_slot_data(self) -> Dict[str, Any]:

        slot_data: Dict[str, Any] = {
            "spring_ball": self.options.spring_ball.value,
            "death_link": self.options.death_link.value,
            "required_artifacts": self.options.required_artifacts.value,
            "exclude_items": self.options.exclude_items.value,
            "final_bosses": self.options.final_bosses.value,
        }

        return slot_data
