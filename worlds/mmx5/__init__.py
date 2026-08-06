"""Archipelago world for Mega Man X5 (PS1, NTSC-U, SLUS-01334).

Feature-complete: generation, reachability rules, disc patch (via Rom.py /
disc.py) and the BizHawkClient are all wired. The RAM interface research notes
(mmx5-ram-notes.md and friends) live in worlds/mmx5/docs/ on the author's
fork: github.com/Shinnuu/Archipelago, branch mmx5-apworld.
"""
import logging
import os
from typing import Any, ClassVar

import settings
from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from . import names, pickups
from .client import MMX5Client  # noqa: F401  (import registers the client)
from .items import BASE_ID, MMX5Item, event_table, item_groups, item_table
from .locations import MMX5Location, event_location_table, location_groups, location_table
from .options import MMX5Options
from .Rom import ACCEPTED_HASHES, MMX5ProcedurePatch, patch_rom


class MMX5Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File path of the Mega Man X5 (USA) disc image (raw 2352-byte .bin)."""
        description = "Mega Man X5 (USA) disc image"
        copy_to = "Megaman X5.bin"
        # Both the Redump dump and the +1-trailing-zero-sector variant; they
        # are byte-identical up to that pad, so patch offsets are unaffected.
        md5s = sorted(ACCEPTED_HASHES)

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MMX5Web(WebWorld):
    theme = "grassFlowers"
    bug_report_page = "https://github.com/Shinnuu/Archipelago/issues"
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

    # The OLDEST client this world is known to work with - NOT the version it
    # was developed against. The server refuses any client below this
    # (MultiServer enforces it from the multidata), so an over-high value
    # locks everyone out: v0.1.0 shipped (0, 6, 8) and no released client
    # could connect, because 0.6.8 is an unreleased development version.
    # 0.6.7 is verified: generation and live client play both confirmed.
    # Lower it if an older client is actually tested, never to match a
    # development checkout's version string.
    required_client_version = (0, 6, 7)

    # Which stage is open at the start under stage_unlocks. Chosen in
    # generate_early so create_items and set_rules see the same answer.
    starting_stage: str | None = None

    def generate_early(self) -> None:
        if self.options.stage_unlocks:
            self.starting_stage = self.random.choice(names.STAGES)

        # vanilla launch odds + the launch goal is a genuine gamble with the
        # whole run: that goal needs a SUCCESSFUL launch, there are only two
        # attempts (Enigma, then Shuttle), and even a full part set tops out at
        # 75%. Fail both and the colony falls with no third chance, so the goal
        # can never complete. Allowed deliberately - but nobody should meet it
        # as a surprise, so it is said out loud at generation.
        if self.options.launch_odds == "vanilla" and self.options.goal == "launch":
            logging.warning(
                "Mega Man X5 (%s): launch_odds=vanilla with goal=launch. This "
                "seed CAN become unwinnable - the goal needs a successful "
                "launch, there are only two attempts, and a full set of parts "
                "is still only 75%%. This combination was chosen on purpose; "
                "use launch_odds=deterministic if that is not what you want.",
                self.player_name)

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
            stage_locations[names.dna_location(stage)] = location_table[names.dna_location(stage)]
            stage_locations[names.dna_part_location(stage)] = \
                location_table[names.dna_part_location(stage)]
            region.add_locations(stage_locations, MMX5Location)
            # All 8 stages are open from the start in X5; stage_unlocks puts
            # each entrance behind its Access Codes item (rule in set_rules).
            stage_select.connect(region)

        if self.options.pickupsanity:
            # Maverick-stage pickups join their stage's region (same
            # reachability as its other locations); Sigma / Zero Space
            # pickups live in Sigma Stages, whose entrance already carries
            # the all-8-weapons rule - deliberately stricter than the game
            # opens the endgame, same reasoning as that entrance.
            by_region: dict[str, dict[str, int]] = {}
            for stage_id, _area, _idx, _iid, loc_name in pickups.PICKUPS:
                region_name = ("Sigma Stages"
                               if stage_id in pickups.ENDGAME_STAGE_IDS
                               else pickups.STAGE_PREFIX[stage_id])
                by_region.setdefault(region_name, {})[loc_name] = \
                    location_table[loc_name]
            for region_name, locs in by_region.items():
                self.multiworld.get_region(region_name, self.player) \
                    .add_locations(locs, MMX5Location)

        victory = MMX5Location(self.player, names.VICTORY, None, sigma_stages)
        victory.place_locked_item(self.create_item(names.VICTORY))
        sigma_stages.locations.append(victory)
        stage_select.connect(sigma_stages)

    def create_items(self) -> None:
        pool = []
        for name, data in item_table.items():
            pool += [self.create_item(name) for _ in range(data.count)]

        # Secret armors: option-gated, so their table count is 0 and they are
        # added here instead. They take filler slots rather than adding
        # locations - the Zero Space capsule that vanilla-holds them is not a
        # check (see the option text).
        if self.options.secret_armors_in_pool:
            pool.append(self.create_item(names.ULTIMATE_ARMOR))
            pool.append(self.create_item(names.BLACK_ZERO))

        # Stage access: the starting stage's codes are precollected (the player
        # holds them from frame one), the other seven are shuffled. Precollected
        # deliberately rather than placed locally - the starting stage must be
        # open before ANY location is reachable, so it cannot itself be a check.
        if self.options.stage_unlocks:
            for stage in names.STAGES:
                item = self.create_item(names.access_item(stage))
                if stage == self.starting_stage:
                    self.multiworld.push_precollected(item)
                else:
                    pool.append(item)

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
        #
        # Note this rule is about WEAPONS (items, receivable from any world),
        # while the all_mavericks goal is about KILLS (popcount of 0x1C4C, only
        # ever set locally). They are not the same requirement and neither
        # implies the other. The goal's kill requirement is enforced by the
        # client, and every boss is reachable and killable with no items at
        # all, so it adds no logical constraint here.
        self.multiworld.get_entrance("Stage Select -> Sigma Stages", self.player).access_rule = \
            lambda state: state.has_all(item_groups["Weapons"], self.player)

        # Stage access. Enforced in-game by the client zeroing the hub's
        # slot -> stage-id table (0x800F5050), which makes confirming a locked
        # icon a no-op; here it is only the logic half. Every location in a
        # stage lives in that stage's region, so one entrance rule covers the
        # boss, heart, capsule, tank, DNA and pickupsanity checks at once.
        if self.options.stage_unlocks:
            for stage in names.STAGES:
                codes = names.access_item(stage)
                self.multiworld.get_entrance(f"Stage Select -> {stage}",
                                             self.player).access_rule = \
                    lambda state, codes=codes: state.has(codes, self.player)

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

        # --- DNA rewards ----------------------------------------------------
        # No access rule: the DNA choice is offered for beating the Maverick,
        # and every stage is open from the start, so it is reachable exactly
        # when the boss is. (These replaced 8 PHANTOM "Energy Up pickup"
        # locations - Energy Ups are not stage items at all. See the
        # reachability plan for the four lines of evidence.)

        if self.options.goal == "launch":
            # Victory = a successful launch, which the client only powers
            # once ALL 8 parts are received (score stays 0 otherwise, and
            # the game's own score<=0 gate fails the launch cleanly).
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has(names.ENIGMA_PART, self.player, 4) \
                    and state.has(names.SHUTTLE_PART, self.player, 4)
        else:
            # sigma and all_mavericks both complete on the VICTORY event, which
            # sits behind the all-8-weapons entrance rule above. all_mavericks
            # needs no extra rule: every Maverick is reachable from the start
            # and killable with no items, so "defeat all 8" is satisfiable
            # wherever VICTORY is. The difference between the two goals is
            # in-game timing, which logic does not model - the client holds the
            # goal until the kill count reaches 8.
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

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "goal": self.options.goal.value,
            "boss_difficulty": self.options.boss_difficulty.value,
            "launch_odds": self.options.launch_odds.value,
            "pickupsanity": self.options.pickupsanity.value,
            "boss_hp_randomization": self.options.boss_hp_randomization.value,
            "stage_unlocks": self.options.stage_unlocks.value,
        }
