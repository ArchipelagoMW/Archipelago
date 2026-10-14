import logging
from typing import Any, ClassVar, Optional

from BaseClasses import ItemClassification, MultiWorld, Tutorial
from Options import Option, OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, Type, icon_paths
from multiprocessing import Process

from worlds.deltarune.Locations import get_location_groups, locations
from worlds.deltarune.Items import (
    DeltaruneItem,
    ItemData,
    ItemIDs,
    ItemGroups,
    change_progression_type,
    convert_filler_and_trap_to_weights,
    custom_print_itempool,
    flag_into_string,
    get_item_groups,
    items,
    glitched_item_name,
    progressive_weapon_order,
)
from worlds.deltarune.Goals import set_completion_goal
from worlds.deltarune.LogicHelper import (
    all_chapter_unlocked,
    chapters_in_order,
    include_characters,
    include_deluxedinner_fusion,
    include_dogwidow_fusion,
    include_hidden_items,
    include_punchbowl_fusion,
    include_tensionmax_fusion,
    include_truetie_fusion,
    include_tvdinner_fusion,
    included_chapter,
    progressive_weapons_kris,
    progressive_weapons_noelle,
    progressive_weapons_ralsei,
    progressive_weapons_susie,
    randomized_chapters,
    weird_route,
)
from worlds.deltarune.OSTRandomizer import randomizeOST
from worlds.deltarune.Options import (
    ChosenRoute,
    DeltaruneOptions,
    UnlockCharacters,
    deltarune_option_groups,
    options_presets,
)
from worlds.deltarune.OptionsValidator import validate_options
from worlds.deltarune.Regions import Regions
from worlds.deltarune.Rules import can_snowgrave
from worlds.deltarune.cross_chapter.Items import (
    get_filler_and_trap_items as get_cross_chapter_filler_and_trap_items,
    create_items as create_cross_chapter_items,
)
from worlds.deltarune.cross_chapter.Rules import (
    set_rules as set_cross_chapter_rules,
    handle_locked_items as handle_cross_chapter_locked_items,
)
from worlds.deltarune.chapter_1.Rules import (
    handle_locked_items as handle_chapter_1_locked_items,
    set_rules as set_chapter_1_rules,
)
from worlds.deltarune.chapter_2.Rules import (
    handle_locked_items as handle_chapter_2_locked_items,
    set_rules as set_chapter_2_rules,
)
from worlds.deltarune.chapter_3.Rules import (
    handle_locked_items as handle_chapter_3_locked_items,
    set_rules as set_chapter_3_rules,
)
from worlds.deltarune.chapter_4.Rules import (
    handle_locked_items as handle_chapter_4_locked_items,
    set_rules as set_chapter_4_rules,
)
from worlds.deltarune.chapter_5.Rules import (
    handle_locked_items as handle_chapter_5_locked_items,
    set_rules as set_chapter_5_rules,
)
from worlds.deltarune.cross_chapter.Regions import create_regions as create_cross_chapter_regions
from worlds.deltarune.chapter_1.Regions import create_regions as create_chapter_1_regions
from worlds.deltarune.chapter_2.Regions import create_regions as create_chapter_2_regions
from worlds.deltarune.chapter_3.Regions import create_regions as create_chapter_3_regions
from worlds.deltarune.chapter_4.Regions import create_regions as create_chapter_4_regions
from worlds.deltarune.chapter_5.Regions import create_regions as create_chapter_5_regions
from worlds.deltarune.cross_chapter.Items import (
    cross_chapter_items,
    create_items as create_cross_chapter_items,
    get_filler_and_trap_items as get_cross_chapter_filler_and_trap_items,
)
from worlds.deltarune.chapter_1.Items import (
    chapter1_items,
    create_items as create_chapter_1_items,
    get_filler_and_trap_items as get_chapter_1_filler_and_trap_items,
)
from worlds.deltarune.chapter_2.Items import (
    chapter2_items,
    create_items as create_chapter_2_items,
    get_filler_and_trap_items as get_chapter_2_filler_and_trap_items,
)
from worlds.deltarune.chapter_3.Items import (
    chapter3_items,
    create_items as create_chapter_3_items,
    get_filler_and_trap_items as get_chapter_3_filler_and_trap_items,
)
from worlds.deltarune.chapter_4.Items import (
    chapter4_items,
    create_items as create_chapter_4_items,
    get_filler_and_trap_items as get_chapter_4_filler_and_trap_items,
)
from worlds.deltarune.chapter_5.Items import (
    chapter5_items,
    create_items as create_chapter_5_items,
    get_filler_and_trap_items as get_chapter_5_filler_and_trap_items,
)
from worlds.deltarune.chapter_1.Locations import chapter1_locations
from worlds.deltarune.chapter_2.Locations import chapter2_locations
from worlds.deltarune.chapter_3.Locations import chapter3_locations
from worlds.deltarune.chapter_4.Locations import chapter4_locations
from worlds.deltarune.chapter_5.Locations import chapter5_locations, chapter5_weird_route_locations
from worlds.deltarune.cross_chapter.Locations import cross_chapter_locations
from worlds.deltarune.tracker import handle_auto_tracking, handle_player_icon_position

all_item_data: list[ItemData] = chapter1_items + chapter2_items + chapter3_items + chapter4_items + chapter5_items + cross_chapter_items

all_locations = []

for region, location in cross_chapter_locations.items():
    all_locations += location
for region, location in chapter1_locations.items():
    all_locations += location
for region, location in chapter2_locations.items():
    all_locations += location
for region, location in chapter3_locations.items():
    all_locations += location
for region, location in chapter4_locations.items():
    all_locations += location
for region, location in chapter5_locations.items():
    all_locations += location
for region, location in chapter5_weird_route_locations.items():
    all_locations += location


def run_client():
    print("running deltarune client")
    from .DeltaruneClient import main  # lazy import

    p = Process(target=main)
    p.start()


components.append(
    Component(
        "DELTARUNE Client",
        func=run_client,
        component_type=Type.CLIENT,
        icon="deltarune",
        game_name="DELTARUNE",
        supports_uri=True,
    )
)

# I apologize for the name of the icon - Emerald
icon_paths["deltarune"] = f"ap:{__name__}/icons/gay_deltarune.png"

class DeltaruneWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago DELTARUNE software on your computer. This guide covers "
            "single-player, multiworld, and related software.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Mewlif"],
        )
    ]

    option_groups = deltarune_option_groups
    options_presets = options_presets
    rich_text_options_doc = True


class DeltaruneWorld(World):
    """
    Deltarune is an episodic role-playing video game created by American indie developer Toby Fox.
    """

    # region Archipelago World properties
    game = "DELTARUNE"
    options_dataclass = DeltaruneOptions
    options: DeltaruneOptions
    web = DeltaruneWeb()

    item_name_to_id = {name: id.value for id, name in items.items()}
    item_name_groups = get_item_groups(all_item_data)

    location_name_to_id = {name: id.value for id, name in locations.items()}
    location_name_groups = get_location_groups(all_locations)

    origin_region_name = Regions.chapter_select
    # endregion

    # region Universal Tracker properties
    glitches_item_name = glitched_item_name

    ut_can_gen_without_yaml = True

    tracker_world: ClassVar = {
        "map_page_folder": "tracker",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": [
            "locations/chapter1.json",
            "locations/chapter2.json",
            "locations/chapter3.json",
            "locations/chapter4.json",
            "locations/overview.json",
        ],
        "map_page_index": handle_auto_tracking,
        "map_page_setting_key": "{player}_{team}_current_location",
        "location_icon_coords": handle_player_icon_position,
        "location_setting_key": "{player}_{team}_current_location",
    }
    # endregion

    # region DELTARUNE properties
    max_deltarune_chapter = 5
    # endregion

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        self.cached_filler_and_trap_weights: dict[int, float] = None
        self.weapon_to_progressive_weapon_index: dict[ItemGroups, dict[ItemIDs, int]] = {}
        self.included_chapters: list[int] = []
        self.randomized: dict[str, Any] = {}

    # region Archipelago Functions
    def create_item(self, name: str) -> DeltaruneItem:
        if name == glitched_item_name:
            return DeltaruneItem(name, ItemClassification.progression, -1, self.player)

        item_data = next((item_data for item_data in all_item_data if items[item_data.code] == name), None)

        if item_data is None:
            raise ValueError(f"Item name '{name}' not found in item data.")

        new_item_data = change_progression_type(self, item_data)

        return DeltaruneItem(
            name,
            new_item_data.classification,
            new_item_data.code.value,
            self.player,
            new_item_data.changing_classification,
        )

    def _get_deltarune_data(self):
        return {
            "options": self.options.as_dict(
                # No Group
                "options_creator_reminder",
                "progression_balancing",
                "accessibility",
                "have_starwalker",
                "shuffle_ost",
                # Goal
                "chosen_route",
                "recruits_sanity",
                "lose_recruits_sanity",
                "randomize_secret_bosses",
                "macguffin_extra",
                # Chapters
                "randomize_chapters",
                "random_safety_chapter_inclusion",
                "starting_chapter",
                # Chapter 1
                "include_chapter_1",
                "macguffin_chapter_1",
                "chapter_1_recruit",
                # Chapter 2
                "include_chapter_2",
                "macguffin_chapter_2",
                # Chapter 3
                "include_chapter_3",
                "macguffin_chapter_3",
                "include_shadow_mantle",
                "randomize_sword_route",
                "shadow_mantle_holder_as_secret_boss",
                "exclude_t_rank_board",
                "exclude_z_rank_board",
                "physical_challenge_rank_sanity",
                "exclude_t_rank_physical_challenge",
                "exclude_z_rank_physical_challenge",
                "allow_doom_board_without_all_characters",
                # Chapter 4
                "include_chapter_4",
                "macguffin_chapter_4",
                "include_mike",
                "exclude_mike_platinum",
                # Chapter 5
                "include_chapter_5",
                "macguffin_chapter_5",
                # Items
                "include_hidden_items",
                "include_secret_bosses_items_requirement",
                "mysterykey_from_pink_coins",
                "door_key_from_broken_keys",
                "include_unused_items",
                "progressive_kris_weapons",
                "progressive_susie_weapons",
                "progressive_ralsei_weapons",
                "progressive_noelle_weapons",
                "unlock_characters",
                "start_with_random_character",
                "unlock_fun_gang_actions",
                # Gameplay
                "better_odds",
                "remove_starting_equipment",
                "item_balancing",
                "pink_twin_ribbon_unnerf",
                "rock_video_sanity",
                "exclude_t_rank_rock_video",
                "exclude_z_rank_rock_video",
                # Logic Difficulty
                "speedrun_gliches_as_logic",
                "nohit_as_logic",
                "annoying_farming_as_logic",
                # Links
                "death_link",
                "death_link_group",
                "damage_link",
                "damage_link_group",
                # Fillers Weight
                "filler_healing_weight",
                "filler_currency_weight",
                "trap_weight",
                "filler_armor_weight",
                "filler_tension_weight",
                "filler_smile_weight",
                toggles_as_bools=True,
            ),
            "randomized": self.randomized,
            "world_seed": self.random.getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
        }

    def fill_slot_data(self):
        return self._get_deltarune_data()

    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            self.randomized = slot_data.get("randomized", {})

            slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))
        else:
            self.fill_chapter_included_array()

            self.randomized["ost"] = randomizeOST(self)

            validate_options(self)

        # Recall in case of option change or for UT that didn't fill the first time
        self.fill_chapter_included_array()

    def get_filler_item_name(self):
        if self.cached_filler_and_trap_weights == None:
            self.fill_weighted_fillers_and_traps()

        if len(self.cached_filler_and_trap_weights) == 0:
            return items[ItemIDs.what_interesting_behavior]

        return items[
            self.random.choices(
                list(self.cached_filler_and_trap_weights.keys()),
                weights=list(self.cached_filler_and_trap_weights.values()),
            )[0]
        ]

    # endregion

    # region Universal Tracker Functions
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data

    # endregion

    # region Archipelago Generation process functions
    def create_regions(self):
        # every_connections = CCLocationsAndRegions.get_cross_chapter_mandatory_connection(self)

        create_cross_chapter_regions(self)
        if included_chapter(self, 1):
            create_chapter_1_regions(self)
        if included_chapter(self, 2):
            create_chapter_2_regions(self)
        if included_chapter(self, 3):
            create_chapter_3_regions(self)
        if included_chapter(self, 4):
            create_chapter_4_regions(self)
        if included_chapter(self, 5):
            create_chapter_5_regions(self)
        # if included_chapter(6): Ch6LocationAndRegions.create_regions(self)
        # if included_chapter(7): Ch7LocationAndRegions.create_regions(self)

    def set_rules(self):

        set_cross_chapter_rules(self)
        if included_chapter(self, 1):
            set_chapter_1_rules(self)
        if included_chapter(self, 2):
            if weird_route(self):
                self.get_region(Regions.ch2_cyber_city).connect(
                    self.get_region(Regions.ch2_mansion_lobby_weird_route), rule=can_snowgrave(self)
                )
            set_chapter_2_rules(self)
        if included_chapter(self, 3):
            set_chapter_3_rules(self)
        if included_chapter(self, 4):
            set_chapter_4_rules(self)
        if included_chapter(self, 5):
            set_chapter_5_rules(self)
        # if included_chapter(6): set_chapter_6_rules(self)
        # if included_chapter(7): set_chapter_7_rules(self)

        set_completion_goal(self)

        # from Utils import visualize_regions

        # state = self.multiworld.get_all_state(False)
        # state.update_reachable_regions(self.player)
        # visualize_regions(self.get_region(self.origin_region_name), f"deltarune_regions{self.player}.puml")

    def create_items(self):
        if len(self.included_chapters) == 0:
            self.multiworld.push_precollected(self.create_item(items[ItemIDs.what_interesting_behavior]))
            return

        item_pool: list[ItemData] = []

        item_pool += create_cross_chapter_items(self)
        handle_cross_chapter_locked_items(self)
        if included_chapter(self, 1):
            item_pool += create_chapter_1_items(self)
            handle_chapter_1_locked_items(self)
        if included_chapter(self, 2):
            item_pool += create_chapter_2_items(self)
            handle_chapter_2_locked_items(self)
        if included_chapter(self, 3):
            item_pool += create_chapter_3_items(self)
            handle_chapter_3_locked_items(self)
        if included_chapter(self, 4):
            item_pool += create_chapter_4_items(self)
            handle_chapter_4_locked_items(self)
        if included_chapter(self, 5):
            item_pool += create_chapter_5_items(self)
            handle_chapter_5_locked_items(self)
        # if included_chapter(6): Ch6Items.create_items(self)
        # if included_chapter(7): Ch7Items.create_items(self)

        if progressive_weapons_kris(self):
            self.handle_progressive_weapon(item_pool, ItemGroups.kris_weapons)
        if progressive_weapons_susie(self):
            self.handle_progressive_weapon(item_pool, ItemGroups.susie_weapons)
        if progressive_weapons_ralsei(self):
            self.handle_progressive_weapon(item_pool, ItemGroups.ralsei_weapons)
        if progressive_weapons_noelle(self):
            self.handle_progressive_weapon(item_pool, ItemGroups.noelle_weapons)
        self.handle_chapter_keys(item_pool)
        self.handle_macguffins_items(item_pool)
        self.handle_random_character(item_pool)

        item_pool_names_and_amounts = []

        for item_data in item_pool:
            item_pool_names_and_amounts += [items[item_data.code]] * item_data.amount

        self.add_filler_items_used_in_fusion(item_pool_names_and_amounts)

        item_pool_converted = [self.create_item(item) for item in item_pool_names_and_amounts]

        self.handle_item_unfill_and_overflows(item_pool_converted)

        self.multiworld.itempool += item_pool_converted

    # endregion

    # region DELTARUNE Generation functions

    def add_filler_items_used_in_fusion(self, item_pool_before_convert):
        if include_truetie_fusion(self):
            item_pool_before_convert += [items[ItemIDs.frayedbowtie]]

        if include_tvdinner_fusion(self):
            item_pool_before_convert += [items[ItemIDs.tvslop]] * 2

        if include_deluxedinner_fusion(self):
            item_pool_before_convert += [items[ItemIDs.tvdinner]] * 2

        if include_punchbowl_fusion(self) or include_tensionmax_fusion(self):
            item_pool_before_convert += [items[ItemIDs.scarlixir]]

        if include_dogwidow_fusion(self) and include_hidden_items(self):
            # dogdollar must be find at their original location if hidden items not included
            item_pool_before_convert += [items[ItemIDs.dogdollar]]

    def fill_chapter_included_array(self):
        self.included_chapters = []

        for chapterToCheck in range(1, self.max_deltarune_chapter + 1, 1):
            if getattr(self.options, f"include_chapter_{chapterToCheck}"):
                self.included_chapters.append(chapterToCheck)

    def get_weapon_progression_index(self, character: ItemGroups, weapon: ItemIDs):
        if character not in self.weapon_to_progressive_weapon_index:
            return 666

        if weapon not in self.weapon_to_progressive_weapon_index[character]:
            return 666

        return self.weapon_to_progressive_weapon_index[character][weapon]

    def fill_weighted_fillers_and_traps(self):
        filler_pool = get_cross_chapter_filler_and_trap_items(self)

        if included_chapter(self, 1):
            filler_pool += get_chapter_1_filler_and_trap_items(self)
        if included_chapter(self, 2):
            filler_pool += get_chapter_2_filler_and_trap_items(self)
        if included_chapter(self, 3):
            filler_pool += get_chapter_3_filler_and_trap_items(self)
        if included_chapter(self, 4):
            filler_pool += get_chapter_4_filler_and_trap_items(self)
        if included_chapter(self, 5):
            filler_pool += get_chapter_5_filler_and_trap_items(self)

        self.cached_filler_and_trap_weights = convert_filler_and_trap_to_weights(filler_pool, self.options)

    def handle_macguffins_items(self, item_pool: list[ItemData]):
        if included_chapter(self, 1) and self.options.macguffin_chapter_1.value > 0:
            item_data = next(
                (item_data for item_data in item_pool if item_data.code == ItemIDs.king_shape_key_piece), None
            )
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_1.value + self.options.macguffin_extra.value
            )
        if included_chapter(self, 2) and self.options.macguffin_chapter_2.value > 0:
            item_data = next((item_data for item_data in item_pool if item_data.code == ItemIDs.keygen_2_segment), None)
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_2.value + self.options.macguffin_extra.value
            )
        if included_chapter(self, 3) and self.options.macguffin_chapter_3.value > 0:
            item_data = next((item_data for item_data in item_pool if item_data.code == ItemIDs.remote_battery), None)
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_3.value + self.options.macguffin_extra.value
            )
        if included_chapter(self, 4) and self.options.macguffin_chapter_4.value > 0:
            item_data = next(
                (item_data for item_data in item_pool if item_data.code == ItemIDs.combination_lock_digit), None
            )
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_4.value + self.options.macguffin_extra.value
            )
        if (
            included_chapter(self, 5)
            and self.options.chosen_route.value != ChosenRoute.option_weird_route
            and self.options.macguffin_chapter_5.value > 0
        ):
            item_data = next((item_data for item_data in item_pool if item_data.code == ItemIDs.jarona_lesson), None)
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_5.value + self.options.macguffin_extra.value
            )

    def handle_random_character(self, item_pool: list[ItemData]):
        if not include_characters(self):
            return

        # Do not start with random if Kris isn't randomized
        if (
            self.options.start_with_random_character.value == 1
            and self.options.unlock_characters.value == UnlockCharacters.option_true
        ):
            characters = [
                item for item in item_pool if ItemGroups.characters in item.groups and item.code != ItemIDs.noelle
            ]

            if len(characters) == 0:
                logging.info(
                    "[DELTARUNE] Failed to start with a random character because there is no character in item pool"
                )
                return

            chosen = self.random.choice(characters)
            item_pool.remove(chosen)
            self.multiworld.push_precollected(self.create_item(items[chosen.code]))

    def handle_chapter_keys(self, item_pool: list[ItemData]):
        if all_chapter_unlocked(self):
            return

        starting_chapter = -1

        if chapters_in_order(self):
            starting_chapter = self.get_first_chapter()
        elif randomized_chapters(self):
            if self.options.starting_chapter.value == 0:
                starting_chapter = self.random.choice(self.included_chapters)
            else:
                starting_chapter = self.options.starting_chapter.value

        if starting_chapter == -1:
            return

        item_name = f"Chapter {starting_chapter} Unlock"

        if randomized_chapters(self):
            item_id = self.item_name_to_id[item_name]
            item_pool.remove(next((item_data for item_data in item_pool if item_data.code == item_id), None))

        self.multiworld.push_precollected(self.create_item(item_name))

    def handle_item_unfill_and_overflows(self, item_pool: list[DeltaruneItem]):
        unfilled = len(self.multiworld.get_unfilled_locations(self.player))
        # Remove random junk items if the item pool overflows
        if len(item_pool) > unfilled:
            amount_to_remove = len(item_pool) - unfilled
            logging.info(f"[DELTARUNE] Item pool overflow: {amount_to_remove}")
            valid_items_indexes = [index for index, item in enumerate(item_pool) if item.excludable]
            indexes_to_remove = []

            for i in range(amount_to_remove):
                if len(valid_items_indexes) == 0:
                    logging.warning(
                        f"[DELTARUNE] PANIC MODE! Not enough filler/trap item to remove, removing useful items"
                    )
                    valid_items_indexes = [
                        index
                        for index, item in enumerate(item_pool)
                        if item.useful
                        and not item.advancement
                        and item.code not in self.item_name_groups[ItemGroups.progressive_weapons]
                    ]
                    print(valid_items_indexes)
                chosen = self.random.choice(valid_items_indexes)
                indexes_to_remove.append(chosen)
                valid_items_indexes.remove(chosen)
                item = item_pool[chosen]
                logging.info(
                    f"[DELTARUNE] Removing {item.name} {flag_into_string(item.classification)} for {self.player_name}"
                )

            indexes_to_remove.sort(reverse=True)

            for i in indexes_to_remove:
                item_pool.pop(i)

        unfilled_amount = len(self.multiworld.get_unfilled_locations(self.player))
        # Fill remaining items with randomly generated junk
        while len(item_pool) < unfilled_amount:
            item_pool.append(self.create_filler())

    def handle_progressive_weapon(
        self,
        itempool: list[ItemData],
        character: ItemGroups,
    ):
        if len(itempool) == 0:
            return

        self.weapon_to_progressive_weapon_index[character] = {}
        weapons_character_in_pool = [
            item
            for item in itempool
            if character in item.groups
            and item.classification != ItemClassification.filler
            and ItemGroups.progressive_weapons not in item.groups
        ]

        weapons_with_index = []

        # Remove them from the item pool
        for weapon in weapons_character_in_pool:
            weapons_with_index.append((weapon.code, progressive_weapon_order[character].index(weapon.code)))
            if weapon.amount > 1:
                newweapon = ItemData(
                    weapon.code,
                    weapon.classification,
                    should_be_included=weapon.should_be_included,
                    groups=weapon.groups,
                    amount=weapon.amount - 1,
                    blacklist_filler=weapon.blacklist_filler,
                    changing_classification=weapon.changing_classification,
                )
                itempool.remove(weapon)
                itempool.append(newweapon)
            else:
                itempool.remove(weapon)

        weapons_with_index.sort(key=lambda w: w[1])

        index = 1

        for weapon in weapons_with_index:
            self.weapon_to_progressive_weapon_index[character][weapon[0]] = index
            index += 1

        match character:
            case ItemGroups.kris_weapons:
                itempool += [
                    ItemData(
                        ItemIDs.progressive_kris_weapons,
                        ItemClassification.useful,
                        groups=[ItemGroups.weapons, ItemGroups.kris_weapons, ItemGroups.progressive_weapons],
                        amount=len(weapons_character_in_pool),
                    )
                ]
            case ItemGroups.susie_weapons:
                itempool += [
                    ItemData(
                        ItemIDs.progressive_susie_weapons,
                        ItemClassification.useful,
                        groups=[ItemGroups.weapons, ItemGroups.susie_weapons, ItemGroups.progressive_weapons],
                        amount=len(weapons_character_in_pool),
                    )
                ]
            case ItemGroups.ralsei_weapons:
                itempool += [
                    ItemData(
                        ItemIDs.progressive_ralsei_weapons,
                        ItemClassification.useful,
                        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons, ItemGroups.progressive_weapons],
                        amount=len(weapons_character_in_pool),
                        changing_classification=True,
                    )
                ]
            case ItemGroups.noelle_weapons:
                itempool += [
                    ItemData(
                        ItemIDs.progressive_noelle_weapons,
                        ItemClassification.useful | ItemClassification.progression,
                        groups=[ItemGroups.weapons, ItemGroups.noelle_weapons, ItemGroups.progressive_weapons],
                        amount=len(weapons_character_in_pool),
                    )
                ]
            case _:
                raise ValueError("Invalid character for progressive weapon")

    # endregion

    # region DELTARUNE Option helpers

    def get_first_chapter(self) -> int:
        return self.included_chapters[0]

    def get_previous_in_order_chapter(self, chapter: int):
        if chapter <= 1:
            return -1

        for chapterToCheck in range(chapter - 1, 0, -1):
            if chapterToCheck in self.included_chapters:
                return chapterToCheck

        return -1

    def get_next_in_order_chapter(self, chapter: int):
        if chapter > self.max_deltarune_chapter:
            return -1

        for chapterToCheck in range(chapter + 1, self.max_deltarune_chapter + 1, 1):
            if chapterToCheck in self.included_chapters:
                return chapterToCheck

        return -1

    # endregion
