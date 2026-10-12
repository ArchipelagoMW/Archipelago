import settings
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths
from BaseClasses import (Tutorial, ItemClassification as ItemClass)
from typing import cast, ClassVar, Any

# Jak 3 imports
from . import options
from .game_id import jak3_name, jak3_max
from .items import (item_table, ITEM_ID_KEY_START, ITEM_ID_KEY_END, ITEM_ID_FILLER_START, ITEM_ID_FILLER_END,
                    TRAP_ID_START, TRAP_ID_END, SECRET_ID_START, SECRET_ID_END, ORBSANITY_ID, Jak3ItemData, Jak3Item,
                    orb_item_table, orb_bundle_size_to_id)
from .locs import (mission_locations)
from .locs.mission_locations import (get_all_mission_locations, get_location_id, get_max_mission_locations,
                                      get_dual_check_mission_locations, main_mission_table, side_mission_table,
                                      main_tasks_to_missions, DUAL_CHECK_SLOT_OFFSET,
                                      MAX_CHECKS_PER_MISSION, get_minigame_medal_locations, get_secret_locations,
                                      get_orb_bundle_locations, secrets_table)
from .locations import (Jak3Location, all_locations_table)
from .regs.region_base import Jak3Region
from .orb_logic import can_reach_orbs, total_logic_orbs
from .rules import spargus_to_desert
from worlds.generic.Rules import CollectionRule


TOTAL_ORBS = 600


class Jak3Settings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """Path to folder containing the ArchipelagoGOAL Jak 3 mod executables (gk.exe and goalc.exe).
        Ensure this path contains forward slashes (/) only. This setting only applies if
        Auto Detect Root Directory is set to false."""
        description = "ArchipelagoGOAL Jak 3 Root Directory"

    class AutoDetectRootDirectory(settings.Bool):
        """Attempt to find the OpenGOAL installation and the Jak 3 mod executables (gk.exe and goalc.exe)
        automatically. If true, the ArchipelaGOAL Jak 3 Root Directory setting is ignored."""
        description = "ArchipelagoGOAL Jak 3 Auto Detect Root Directory"

    root_directory: RootDirectory = "C:/Program Files/OpenGOAL/features/jak3/mods/archipelagoal/archipelagoal"
    auto_detect_root_directory: AutoDetectRootDirectory = True


def launch_client():
    from . import client
    launch_subprocess(client.launch, name="Jak3Client")


components.append(Component("Jak 3 Client",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="jak3_icon"))

icon_paths["jak3_icon"] = f"ap:{__name__}/icons/jak3_icon.png"


class Jak3WebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ArchipelagoGOAL 3 (Archipelago on OpenGOAL)",
        "English",
        "setup_en.md",
        "setup/en",
        ["Blake645"]
    )

    tutorials = [setup_en]
    bug_report_page = "https://github.com/Blake645/Archipelago/issues"


class Jak3World(World):
    """
Jak 3 is a 2004 action-adventure platformer video game developed by Naughty Dog and published by Sony Computer Entertainment
for the PlayStation 2 (PS2). The game is the sequel to Jak II (2003) and serves as the conclusion of the trilogy.
The story of the previous games continues as the player takes on the dual role of recurring protagonists Jak and Daxter.
It adds new weapons, devices and playable areas.
    """

    game = jak3_name
    web = Jak3WebWorld()

    options_dataclass = options.Jak3Options
    options: options.Jak3Options

    settings: ClassVar[Jak3Settings]

    location_name_to_id = {**get_max_mission_locations(), **get_dual_check_mission_locations(),
                           **get_minigame_medal_locations(True), **get_secret_locations(),
                           **get_orb_bundle_locations(TOTAL_ORBS)}
    item_name_to_id = {item_data.name: k for k, item_data in item_table.items()}
    item_name_groups = {
        "Items": {item.name for item in item_table.values()}
    }
    location_name_groups = {}
    origin_region_name = "Mission Tree"

    completion_type: int
    completion_value: int
    total_items: int = 80
    total_prog_items: int = 55
    total_filler_items: int = 0
    total_trap_items: int = 0
    orb_bundle_item_name: str = ""
    orb_bundle_item_id: int = 0

    # Universal Tracker: allow regenerating this world from slot data, no YAML needed.
    ut_can_gen_without_yaml = True

    def generate_early(self) -> None:
        # Universal Tracker support: overwrite our options with the ones from the real seed's slot data.
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if jak3_name in self.multiworld.re_gen_passthrough:
                for key, val in self.multiworld.re_gen_passthrough[jak3_name].items():
                    try:
                        getattr(self.options, key).value = val
                    except AttributeError:
                        pass

        self.completion_type = self.options.jak_3_completion_condition.value
        if self.completion_type == options.CompletionCondition.option_complete_specific_mission:
            self.completion_value = self.options.specific_mission_for_completion.value
        elif self.completion_type == options.CompletionCondition.option_complete_number_of_missions:
            self.completion_value = self.options.number_of_missions_for_completion.value
        else:
            raise OptionError(f"Unknown completion condition selected for Jak 3: {self.completion_type}")

        if self.options.orbsanity:
            bundle_size = self.options.orbs_per_bundle.value
            self.orb_bundle_item_name = orb_item_table[bundle_size]
            self.orb_bundle_item_id = orb_bundle_size_to_id[bundle_size]

    def _num_bundles(self) -> int:
        # Only as many bundles as the orb logic can actually guarantee.
        size = self.options.orbs_per_bundle.value
        return min(TOTAL_ORBS, total_logic_orbs()) // size

    @staticmethod
    def item_data_helper(item: int) -> list[tuple[int, ItemClass, int]]:
        # count,num,classification
        data: list[tuple[int, ItemClass, int]] = []

        # Determine item classification based on ID ranges
        if ITEM_ID_KEY_START <= item <= ITEM_ID_KEY_END:
            if item in (52, 53):
                data.append((4, ItemClass.progression | ItemClass.useful, 0))
            else:
                # Key/progression items
                data.append((1, ItemClass.progression | ItemClass.useful, 0))
        elif ITEM_ID_FILLER_START <= item <= ITEM_ID_FILLER_END:
            # Filler items (will be made manually)
            data.append((0, ItemClass.filler, 0))
        elif TRAP_ID_START <= item <= TRAP_ID_END:
            # Trap items (their own table) (will also be made manually)
            data.append((0, ItemClass.trap, 0))
        elif SECRET_ID_START <= item <= SECRET_ID_END:
            # Archipelago secret unlocks — optional QoL/cosmetic, not required for reachability
            data.append((1, ItemClass.useful, 0))
        elif item in orb_bundle_size_to_id.values():
            # Orb Bundle — count is determined dynamically in create_items(), not here
            data.append((1, ItemClass.progression | ItemClass.useful, 0))
        else:
            # If we try to make items with ID's outside defined ranges, something has gone wrong
            raise KeyError(f"Tried to fill item pool with unknown ID {item}. Valid ranges: "
                           f"key items ({ITEM_ID_KEY_START}-{ITEM_ID_KEY_END}), "
                           f"filler items ({ITEM_ID_FILLER_START}-{ITEM_ID_FILLER_END})"
                           f"trap items ({TRAP_ID_START}-{TRAP_ID_END})"
                           f"secret items ({SECRET_ID_START}-{SECRET_ID_END})")
        return data

    def create_items(self) -> None:
        items_made: int = 0
        for item_name in self.item_name_to_id:
            item_id = self.item_name_to_id[item_name]

            if ITEM_ID_FILLER_START <= item_id <= ITEM_ID_FILLER_END:
                continue
            if TRAP_ID_START <= item_id <= TRAP_ID_END:
                continue
            if item_id in orb_bundle_size_to_id.values():
                continue

            data = self.item_data_helper(item_id)
            for (count, classification, num) in data:
                self.multiworld.itempool += [
                    Jak3Item(item_name, classification, item_id, self.player)
                    for _ in range(count)]
                items_made += count

        if self.options.orbsanity:
            num_bundles = self._num_bundles()
            self.multiworld.itempool += [
                Jak3Item(self.orb_bundle_item_name, ItemClass.progression | ItemClass.useful,
                         self.orb_bundle_item_id, self.player)
                for _ in range(num_bundles)]
            items_made += num_bundles

        all_regions = self.multiworld.get_regions(self.player)
        total_locations = sum(reg.location_count for reg in cast(list[Jak3Region], all_regions))
        total_filler = total_locations - items_made

        # Calculate how many filler slots to replace with traps
        trap_percent = self.options.percent_filler_replaced_with_traps.value / 100
        trap_count = int(total_filler * trap_percent)
        filler_count = total_filler - trap_count

        # If all trap weights are 0, don't place any traps
        trap_names, trap_weights = self.options.trap_weights.weighted_pair
        if all(w == 0 for w in trap_weights):
            trap_count = 0
            filler_count = total_filler

            print(f"[Jak3] total_locations={total_locations}, items_made={items_made}, total_filler={total_filler}")
            print(f"[Jak3] trap_percent={trap_percent}, trap_count={trap_count}, filler_count={filler_count}")
            print(f"[Jak3] trap_weights={list(zip(trap_names, trap_weights))}")
        self.multiworld.itempool += [self.create_filler() for _ in range(max(0, filler_count))]
        self.multiworld.itempool += [self.create_trap() for _ in range(max(0, trap_count))]

    def create_trap(self) -> Jak3Item:
        trap_names, trap_weights = self.options.trap_weights.weighted_pair
        trap_name = self.random.choices(trap_names, weights=trap_weights, k=1)[0]
        trap_id = self.item_name_to_id[trap_name]
        return Jak3Item(trap_name, ItemClass.trap, trap_id, self.player)

    def create_item(self, name: str) -> Jak3Item:
        item_id = self.item_name_to_id[name]
        _, classification, _ = self.item_data_helper(item_id)[0]
        return Jak3Item(name, classification, item_id, self.player)

    def get_filler_item_name(self) -> str:
        filler_item_names = ["Dark Eco Pill", "Light Eco Pill", "Skull Gems", "Health Pack",
                             "Scatter Gun Ammo", "Blaster Ammo", "Vulcan Fury Ammo", "Peacemaker Ammo"]
        return self.random.choice(filler_item_names)

    # The orb logic caches the reachable-orb count on the state. Any item change
    # invalidates that cache.
    def collect(self, state, item) -> bool:
        change = super().collect(state, item)
        if change:
            state.prog_items[self.player]["Reachable Orbs Fresh"] = 0
        return change

    def remove(self, state, item) -> bool:
        change = super().remove(state, item)
        if change:
            state.prog_items[self.player]["Reachable Orbs Fresh"] = 0
        return change

    def create_regions(self) -> None:
        mission_tree_region = Jak3Region("Mission Tree", self.player, self.multiworld)

        self._add_main_and_side_missions(mission_tree_region)
        self._add_secrets(mission_tree_region)
        self._add_orbsanity_bundles(mission_tree_region)
        self._add_minigame_medals(mission_tree_region)

        self.multiworld.regions.append(mission_tree_region)

        self._set_completion_condition()

    def _add_main_and_side_missions(self, mission_tree_region: Jak3Region) -> None:
        if self.options.location_check_mode == options.LocationCheckMode.option_dual_checks:
            for mission_id, mission in main_mission_table.items():
                mission_tree_region.add_jak_mission(get_location_id(mission_id, DUAL_CHECK_SLOT_OFFSET), mission.name,
                                                    mission.rule)
                for i, item_name in enumerate(mission.items_granted, start=DUAL_CHECK_SLOT_OFFSET + 1):
                    mission_tree_region.add_jak_mission(get_location_id(mission_id, i), item_name, mission.rule)
            for mission_id, mission in side_mission_table.items():
                mission_tree_region.add_jak_mission(get_location_id(mission_id, DUAL_CHECK_SLOT_OFFSET), mission.name,
                                                    mission.rule)
        else:
            checks = self.options.checks_per_mission.value
            for mission_id, mission in main_mission_table.items():
                for check in range(1, checks + 1):
                    name = f"{mission.name} - Check {check}"
                    loc_id = get_location_id(mission_id, check)
                    mission_tree_region.add_jak_mission(loc_id, name, mission.rule)
            for mission_id, mission in side_mission_table.items():
                for check in range(1, checks + 1):
                    name = f"{mission.name} - Check {check}"
                    loc_id = get_location_id(mission_id, check)
                    mission_tree_region.add_jak_mission(loc_id, name, mission.rule)

    def _add_secrets(self, mission_tree_region: Jak3Region) -> None:
        # Secrets are bought with orbs in the game, so each one needs enough reachable orbs to pay for it.
        # Costs are cumulative: buying the cheaper secrets first uses up orbs, so the Nth secret
        # (sorted by cost) needs the running total of every cost up to and including its own.
        secret_locations = get_secret_locations()
        spent = 0
        for secret in sorted(secrets_table.values(), key=lambda s: (s.cost, s.secret_id)):
            spent += secret.cost
            mission_tree_region.add_jak_mission(
                secret_locations[secret.name], secret.name,
                lambda state, player, needed=spent: can_reach_orbs(state, player, needed))

    def _add_orbsanity_bundles(self, mission_tree_region: Jak3Region) -> None:
        # Orbsanity bundles — only active when the Orbsanity option is enabled.
        # Bundle N needs N * bundle_size orbs, so it is only reachable once enough
        # areas / missions are unlocked to contain that many orbs.
        if self.options.orbsanity:
            bundle_size = self.options.orbs_per_bundle.value
            num_bundles = self._num_bundles()
            for i, (name, loc_id) in enumerate(get_orb_bundle_locations(num_bundles).items(), start=1):
                needed = bundle_size * i
                mission_tree_region.add_jak_mission(
                    loc_id, name,
                    lambda state, player, needed=needed: can_reach_orbs(state, player, needed))

    def _add_minigame_medals(self, mission_tree_region: Jak3Region) -> None:
        if not self.options.minigame_medal_checks:
            return

        power_game_mission = main_mission_table[41]
        gun_course_1_mission = main_mission_table[29]
        gun_course_2_mission = main_mission_table[37]
        gungame_mission = main_mission_table[13]
        air_time_mission = side_mission_table[158]
        total_air_time_mission = side_mission_table[159]
        jump_distance_mission = side_mission_table[160]
        total_jump_distance_mission = side_mission_table[161]
        roll_count_mission = side_mission_table[162]
        destroy_marauders_mission = side_mission_table[163]
        jetboard_bbush_mission = side_mission_table[164]
        time_trial_mission = side_mission_table[154]
        rally_mission = side_mission_table[155]

        # The Satellite minigame is located in the desert.
        satellite_rule = lambda state, player: spargus_to_desert(state, player)

        medal_rules = {
            "Daxter Pac-man Minigame - Bronze Medal": power_game_mission.rule,
            "Daxter Pac-man Minigame - Silver Medal": power_game_mission.rule,
            "Daxter Pac-man Minigame - Gold Medal": power_game_mission.rule,
            "Blaster Gun Course - Bronze Medal": gun_course_1_mission.rule,
            "Blaster Gun Course - Silver Medal": gun_course_1_mission.rule,
            "Blaster Gun Course - Gold Medal": gun_course_1_mission.rule,
            "Scatter Gun Course - Bronze Medal": gun_course_2_mission.rule,
            "Scatter Gun Course - Silver Medal": gun_course_2_mission.rule,
            "Scatter Gun Course - Gold Medal": gun_course_2_mission.rule,
            "Satellite Minigame - Bronze Medal": satellite_rule,
            "Satellite Minigame - Silver Medal": satellite_rule,
            "Satellite Minigame - Gold Medal": satellite_rule,
            "Gun Turret Minigame - Bronze Medal": gungame_mission.rule,
            "Gun Turret Minigame - Silver Medal": gungame_mission.rule,
            "Gun Turret Minigame - Gold Medal": gungame_mission.rule,
            "Air Time Challenge (Desert) - Bronze Medal": air_time_mission.rule,
            "Air Time Challenge (Desert) - Silver Medal": air_time_mission.rule,
            "Air Time Challenge (Desert) - Gold Medal": air_time_mission.rule,
            "Total Air Time Challenge (Desert) - Bronze Medal": total_air_time_mission.rule,
            "Total Air Time Challenge (Desert) - Silver Medal": total_air_time_mission.rule,
            "Total Air Time Challenge (Desert) - Gold Medal": total_air_time_mission.rule,
            "Jump Distance Challenge (Desert) - Bronze Medal": jump_distance_mission.rule,
            "Jump Distance Challenge (Desert) - Silver Medal": jump_distance_mission.rule,
            "Jump Distance Challenge (Desert) - Gold Medal": jump_distance_mission.rule,
            "Total Jump Distance Challenge (Desert) - Bronze Medal": total_jump_distance_mission.rule,
            "Total Jump Distance Challenge (Desert) - Silver Medal": total_jump_distance_mission.rule,
            "Total Jump Distance Challenge (Desert) - Gold Medal": total_jump_distance_mission.rule,
            "Roll Count Challenge (Desert) - Bronze Medal": roll_count_mission.rule,
            "Roll Count Challenge (Desert) - Silver Medal": roll_count_mission.rule,
            "Roll Count Challenge (Desert) - Gold Medal": roll_count_mission.rule,
            "Destroy Marauders Side Mission (Desert) - Bronze Medal": destroy_marauders_mission.rule,
            "Destroy Marauders Side Mission (Desert) - Silver Medal": destroy_marauders_mission.rule,
            "Destroy Marauders Side Mission (Desert) - Gold Medal": destroy_marauders_mission.rule,
            "JET-Board Side Mission (Industrial Section A) - Bronze Medal": jetboard_bbush_mission.rule,
            "JET-Board Side Mission (Industrial Section A) - Silver Medal": jetboard_bbush_mission.rule,
            "JET-Board Side Mission (Industrial Section A) - Gold Medal": jetboard_bbush_mission.rule,
            "Desert Time Trial - Bronze Medal": time_trial_mission.rule,
            "Desert Time Trial - Silver Medal": time_trial_mission.rule,
            "Desert Time Trial - Gold Medal": time_trial_mission.rule,
            "Desert Rally Side Mission - Bronze Medal": rally_mission.rule,
            "Desert Rally Side Mission - Silver Medal": rally_mission.rule,
            "Desert Rally Side Mission - Gold Medal": rally_mission.rule,
        }

        for name, loc_id in get_minigame_medal_locations(True).items():
            rule = medal_rules.get(name, lambda state, player: True)
            mission_tree_region.add_jak_mission(loc_id, name, rule)

    def _set_completion_condition(self) -> None:
        if self.completion_type == options.CompletionCondition.option_complete_specific_mission:
            mission_id = self.completion_value
            mission = main_tasks_to_missions.get(mission_id)
            if mission:
                target_name = (
                    mission.name if self.options.location_check_mode == options.LocationCheckMode.option_dual_checks
                    else f"{mission.name} - Check 1")
                self.multiworld.completion_condition[self.player] = lambda state: (
                    state.can_reach_location(target_name, player=self.player))

        elif self.completion_type == options.CompletionCondition.option_complete_number_of_missions:
            def _completion_rule(state, player) -> bool:
                completed_count = 0
                for mid, miss in main_mission_table.items():
                    if miss.has_rule and miss.rule(state, player):
                        completed_count += 1
                for sid, side_miss in side_mission_table.items():
                    if side_miss.has_rule and side_miss.rule(state, player):
                        completed_count += 1
                return completed_count >= self.completion_value

            self.multiworld.completion_condition[self.player] = lambda state: (
                _completion_rule(state=state, player=self.player))

    def fill_slot_data(self) -> dict[str, Any]:
        options_dict = self.options.as_dict(
            "jak_3_completion_condition",
            "specific_mission_for_completion",
            "number_of_missions_for_completion",
            "checks_per_mission",
            "location_check_mode",
            "jak_is_jak2",
            "trap_effect_duration",
            "randomize_burning_bush_cost",
            "burning_bush_cost_get_to",
            "burning_bush_cost_race",
            "burning_bush_cost_other",
            "minigame_medal_checks",
            "orbsanity",
            "orbs_per_bundle",
        )
        options_dict["orb_bundle_count"] = self._num_bundles()
        return options_dict