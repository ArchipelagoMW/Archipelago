from typing import Any, ClassVar, TextIO

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from Options import OptionError, OptionGroup
from .items import NineSolsItem, all_non_event_items_table, item_name_groups, create_item, create_items
from .locations_and_regions import all_non_event_locations_table, location_name_groups, create_regions
from .ut_map_page.map_page_index import map_page_index
from .jade_costs import generate_random_jade_costs
from .node_items import select_node_item_names
from .options import *


class NineSolsWebWorld(WebWorld):
    theme = "ocean"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to playing Nine Sols.",
            language="English",
            file_name="guide_en.md",
            link="guide/en",
            authors=["Ixrec"]
        )
    ]
    option_groups = [
        OptionGroup("Sol Seals", [
            ShuffleSolSeals,
            SealsForEigong,
            SealsForPrison,
            SealsForEthereal,
        ]),
        OptionGroup("Logic & Skips", [
            PreventWeakenedPrisonState,
            SkipSoulscapePlatforming,
            PreventAnnoyingRunbacks,
            LogicDifficulty,
        ]),
        OptionGroup("Root Nodes", [
            FirstRootNode,
            ShuffleSomeRootNodes,
        ]),
        OptionGroup("Shuffle Starting Abilities", [
            ShuffleGrapple,
            ShuffleWallClimb,
            ShuffleLedgeGrab,
        ]),
        OptionGroup("Jade Cost Randomization", [
            RandomizeJadeCosts,
            JadeCostMin,
            JadeCostMax,
            JadeCostPlando,
        ]),
        OptionGroup("Shop Unlocks", [
            ShopUnlocks,
            KuafuShopUnlockSolSeals,
            ChiyouShopUnlockSolSeals,
            KuafuExtraInventoryUnlockSolSeals,
        ]),
        OptionGroup("Additional Randomizations", [
            RandomizeShops,
            # skill_tree_randomization
            # entrance_randomization
        ]),
    ]


class NineSolsWorld(World):
    game = "Nine Sols"
    web = NineSolsWebWorld()

    # Universal Tracker configuration
    ut_can_gen_without_yaml = True
    glitches_item_name = "UT Glitch Logic"
    tracker_world: ClassVar = {
        "map_page_folder": "ut_map_page",
        "map_page_maps": "maps.json",
        "map_page_locations": "locations.json",
        "map_page_setting_key": "{player}_{team}_nine_sols_area",
        "map_page_index": map_page_index
    }

    using_ut: bool
    jade_costs: dict[str, int] | str
    node_items: list[str]

    def __init__(self, multiworld, player):
        super(NineSolsWorld, self).__init__(multiworld, player)

        # initial values of instance attributes (*not* class attributes)
        self.jade_costs = 'vanilla'
        self.using_ut = False
        self.node_items = []

    def generate_early(self) -> None:
        if self.options.jade_cost_max < self.options.jade_cost_min:
            raise OptionError("jade_cost_max is less than jade_cost_min")

        # implement .yaml-less Universal Tracker support
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Nine Sols" in self.multiworld.re_gen_passthrough:
                    self.using_ut = True
                    slot_data = self.multiworld.re_gen_passthrough["Nine Sols"]

                    self.node_items = slot_data.get('node_items', [])  # in normal gen this only affects start inventory, but UT needs this for /next_progression
                    self.options.first_root_node = FirstRootNode.from_text(slot_data['first_root_node_name'])

                    self.options.seals_for_eigong.value = slot_data['seals_for_eigong']
                    self.options.seals_for_prison.value = slot_data['seals_for_prison']
                    self.options.prevent_weakened_prison_state.value = slot_data.get('prevent_weakened_prison_state', 0)
                    self.options.seals_for_ethereal.value = slot_data['seals_for_ethereal']
                    self.options.skip_soulscape_platforming.value = slot_data['skip_soulscape_platforming']
                    self.options.prevent_annoying_runbacks.value = slot_data.get('prevent_annoying_runbacks', 0)
                    self.options.logic_difficulty.value = slot_data.get('logic_difficulty', 0)
                    self.options.shop_unlocks.value = slot_data.get('shop_unlocks', 0)
                    self.options.shuffle_grapple.value = slot_data.get('shuffle_grapple', 0)
                    self.options.shuffle_wall_climb.value = slot_data.get('shuffle_wall_climb', 0)
                    self.options.shuffle_ledge_grab.value = slot_data.get('shuffle_ledge_grab', 0)
                    self.options.kuafu_shop_unlock_sol_seals.value = slot_data.get('kuafu_shop_unlock_sol_seals', 0)
                    self.options.chiyou_shop_unlock_sol_seals.value = slot_data.get('chiyou_shop_unlock_sol_seals', 0)
                    self.options.kuafu_extra_inventory_unlock_sol_seals.value = (
                        slot_data.get('kuafu_extra_inventory_unlock_sol_seals', 0))
                    self.options.randomize_shops.value = slot_data.get('randomize_shops', 0)
            return

        # generate game-specific randomizations separate from AP items/locations
        self.jade_costs = generate_random_jade_costs(self.random, self.options) \
            if self.options.randomize_jade_costs else "vanilla"

        self.node_items = select_node_item_names(self.random, self.options) \
            if self.options.shuffle_some_root_nodes else []

    # members and methods implemented by locations_and_regions.py, locations.jsonc and connections.jsonc

    location_name_to_id = all_non_event_locations_table
    location_name_groups = location_name_groups

    def create_regions(self) -> None:
        create_regions(self)

    # members and methods implemented by items.py and items.jsonc

    item_name_to_id = all_non_event_items_table
    item_name_groups = item_name_groups

    def create_item(self, name: str) -> NineSolsItem:
        return create_item(self, name)

    def create_items(self) -> None:
        create_items(self)

    def get_filler_item_name(self) -> str:
        # Used in corner cases (e.g. plando, item_links, start_inventory_from_pool)
        # where even a well-behaved world may end up "missing" items.
        # Technically this "should" be a random choice among all filler/trap items
        # the world is configured to have, but it's not worth that much effort.
        return "Jin x50"

    # members and methods related to options.py

    options_dataclass = NineSolsGameOptions
    options: NineSolsGameOptions

    # miscellaneous smaller methods

    def set_rules(self) -> None:
        # here we only set the completion condition; all the location/region rules were set in create_regions()
        # currently there is only one goal
        goal_item = 'Victory - Eggnog'
        self.multiworld.completion_condition[self.player] = lambda state: state.has(goal_item, self.player)

    def fill_slot_data(self):
        slot_data = self.options.as_dict(
            'skip_soulscape_platforming',
            'seals_for_eigong',
            'seals_for_prison',
            'seals_for_ethereal',
            'logic_difficulty',
            'shuffle_grapple',
            'shuffle_wall_climb',
            'shuffle_ledge_grab',
            'shop_unlocks',
            'kuafu_shop_unlock_sol_seals',
            'chiyou_shop_unlock_sol_seals',
            'kuafu_extra_inventory_unlock_sol_seals',
            'prevent_annoying_runbacks',
            'prevent_weakened_prison_state',
            'randomize_shops',
        )
        slot_data["first_root_node_name"] = self.options.first_root_node.current_key  # we want strings instead of ints
        slot_data["jade_costs"] = self.jade_costs
        slot_data["node_items"] = self.node_items
        # APWorld versions are not (yet?) exposed by AP servers, so the client/mod needs us to put it in slot_data
        slot_data["apworld_version"] = self.world_version.as_simple_string()
        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.jade_costs != 'vanilla':
            spoiler_handle.write(
                '\nRandomized Jade Costs for %s:\n\n%s' %
                (self.multiworld.player_name[self.player], self.jade_costs)
            )
