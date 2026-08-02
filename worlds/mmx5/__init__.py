"""Archipelago world for Mega Man X5 (PS1, NTSC-U, SLUS-01334).

Scaffold status: generates. Client (BizHawkClient) and real reachability rules
are the next phases. RAM interface documentation lives outside the repo in the
project workspace (Reference/mmx5-ram-notes.md).
"""
import os
from typing import Any, ClassVar, Dict

import settings
from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from . import names
from .client import MMX5Client  # noqa: F401  (import registers the client)
from .items import BASE_ID, MMX5Item, event_table, item_groups, item_table
from .locations import MMX5Location, event_location_table, location_groups, location_table
from .options import MMX5Options
from .Rom import HASH_US, MMX5ProcedurePatch, patch_rom


class MMX5Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File path of the Mega Man X5 (USA) disc image (raw 2352-byte .bin)."""
        description = "Mega Man X5 (USA) disc image"
        copy_to = "Megaman X5.bin"
        md5s = [HASH_US]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MMX5Web(WebWorld):
    theme = "grassFlowers"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Mega Man X5 with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Shinnuu"],
    )
    tutorials = [setup_en]


class MMX5World(World):
    """
    Mega Man X5 is the fifth entry in Capcom's Mega Man X series, released for the
    PlayStation in 2000. Play as X or Zero, defeat eight Mavericks in any order,
    and stop the colony drop before Sigma's plan comes to fruition.
    """
    game = "Mega Man X5"
    web = MMX5Web()

    options_dataclass = MMX5Options
    options: MMX5Options

    settings: ClassVar[MMX5Settings]
    settings_key = "mmx5_options"

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = location_table
    item_name_groups = item_groups
    location_name_groups = location_groups

    required_client_version = (0, 6, 0)

    def create_item(self, name: str) -> MMX5Item:
        if name in item_table:
            data = item_table[name]
            classification = data.classification
            # Launcher parts carry completion under the launch goal.
            if name in (names.ENIGMA_PART, names.SHUTTLE_PART) \
                    and self.options.goal == "launch":
                classification = ItemClassification.progression
            return MMX5Item(name, classification, data.code, self.player)
        data = event_table[name]
        return MMX5Item(name, data.classification, None, self.player)

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        stage_select = Region("Stage Select", self.player, self.multiworld)
        sigma_stages = Region("Sigma Stages", self.player, self.multiworld)
        self.multiworld.regions += [menu, stage_select, sigma_stages]

        # Intro stage is mandatory before the stage select in-game.
        intro = Region("Intro Stage", self.player, self.multiworld)
        self.multiworld.regions.append(intro)
        intro.add_locations({names.INTRO_CLEAR: location_table[names.INTRO_CLEAR]}, MMX5Location)

        menu.connect(intro)
        intro.connect(stage_select)

        for stage in names.STAGES:
            region = Region(stage, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            stage_locations = {
                names.boss_location(stage): location_table[names.boss_location(stage)],
                names.heart_location(stage): location_table[names.heart_location(stage)],
                names.capsule_location(stage): location_table[names.capsule_location(stage)],
            }
            if stage in names.STAGE_TANK:
                stage_locations[names.tank_location(stage)] = location_table[names.tank_location(stage)]
            stage_locations[names.energy_up_location(stage)] = location_table[names.energy_up_location(stage)]
            region.add_locations(stage_locations, MMX5Location)
            # All 8 stages are open from the start in X5.
            stage_select.connect(region)

        victory = MMX5Location(self.player, names.VICTORY, None, sigma_stages)
        victory.place_locked_item(self.create_item(names.VICTORY))
        sigma_stages.locations.append(victory)
        stage_select.connect(sigma_stages)

    def create_items(self) -> None:
        pool = []
        for name, data in item_table.items():
            pool += [self.create_item(name) for _ in range(data.count)]

        # Top up with filler to match unfilled locations.
        unfilled = len(self.multiworld.get_unfilled_locations(self.player))
        while len(pool) < unfilled:
            pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        # Sigma stages open once all eight Maverick weapons are in hand.
        # This is deliberately STRICTER than the game, which only requires the
        # Eurasia colony situation to resolve (story chapter derives from
        # popcount of 0x800D1C4C; the endgame opens after the Enigma/Shuttle
        # sequence plays out either way). Stricter is safe - it only narrows
        # placement, it can never strand progression - so it stays for v1.
        self.multiworld.get_entrance("Stage Select -> Sigma Stages", self.player).access_rule = \
            lambda state: state.has_all(item_groups["Weapons"], self.player)

        player = self.player
        falcon = names.ARMOR_PARTS[0:4]
        gaea = names.ARMOR_PARTS[4:8]

        # Armor is usable only as a COMPLETE set, and in AP the parts are
        # shuffled away from their vanilla capsules - so these must key on the
        # part ITEMS, never on "reached the capsule that vanilla-holds them".
        def has_falcon(state) -> bool:
            return state.has_all(falcon, player)

        def has_gaea(state) -> bool:
            return state.has_all(gaea, player)

        def needs(location: str, rule) -> None:
            self.multiworld.get_location(location, player).access_rule = rule

        # --- Armor capsules -------------------------------------------------
        # Stage<->part mapping cross-validated at two points against live
        # capsule-object id reads (Duff McWhalen = id 1 = Falcon Body,
        # Dark Dizzy = id 4 = Gaea Head), which also confirms capsule id ==
        # part index. NOTE no FALCON part requires Falcon Armor - the three
        # that do are all GAEA parts, which is sequential, not circular.
        needs(names.capsule_location(names.WHALE),
              lambda state: state.has(names.GOO_SHAVER, player))
        needs(names.capsule_location(names.FIREFLY),
              lambda state: state.has(names.CSHOT, player))
        needs(names.capsule_location(names.NECROBAT),
              lambda state: state.has(names.F_LASER, player))
        needs(names.capsule_location(names.PEGASUS), has_falcon)
        needs(names.capsule_location(names.DINOREX), has_falcon)
        needs(names.capsule_location(names.ROSERED), has_falcon)
        # Falcon Leg (Grizzly Slash) and Falcon Head (Squid Adler) need no
        # items - the latter is gated on collecting 8 energy balls during the
        # jet-bike section, which is execution, not inventory.

        # --- Heart tanks ----------------------------------------------------
        for stage in (names.GRIZZLY, names.KRAKEN, names.FIREFLY, names.ROSERED):
            needs(names.heart_location(stage), has_gaea)
        needs(names.heart_location(names.WHALE), has_falcon)
        # Dark Dizzy / The Skiver / Mattrex hearts need nothing.

        # --- Sub / W / EX tanks ---------------------------------------------
        # Stage assignment matches the client's TANK_RECORD_TO_STAGE, itself
        # derived from the placement harvest - four more agreement points.
        needs(names.tank_location(names.NECROBAT), has_falcon)
        needs(names.tank_location(names.FIREFLY),
              lambda state: state.has(names.GROUND_FIRE, player))
        # Grizzly Slash sub-tank and The Skiver W-Tank need nothing.

        # Energy-Ups are intentionally unrestricted: their per-stage
        # requirements have never been surveyed (the harvester is still
        # filling in coordinates). Flagged in the reachability plan - do NOT
        # read this absence as "verified free".

        if self.options.goal == "launch":
            # Victory = a successful launch, which the client only powers
            # once ALL 8 parts are received (score stays 0 otherwise, and
            # the game's own score<=0 gate fails the launch cleanly).
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has(names.ENIGMA_PART, self.player, 4) \
                    and state.has(names.SHUTTLE_PART, self.player, 4)
        else:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has(names.VICTORY, self.player)

    def get_filler_item_name(self) -> str:
        return names.SMALL_ENERGY

    def generate_output(self, output_directory: str) -> None:
        patch = MMX5ProcedurePatch(player=self.player,
                                   player_name=self.multiworld.player_name[self.player])
        patch_rom(self, patch)
        patch.write(os.path.join(
            output_directory,
            f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))

    def fill_slot_data(self) -> Dict[str, Any]:
        return {"goal": self.options.goal.value}
