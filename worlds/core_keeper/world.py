import hashlib

from BaseClasses import Item, ItemClassification
from Options import OptionError
from worlds.AutoWorld import World

from . import items, regions, rules
from .enemy_randomizer import build_enemy_mapping
from .boss_randomizer import build_boss_mapping
from .locations import LOCATION_METADATA, LOCATION_NAME_TO_ID
from .options import CoreKeeperOptions, LICENSE_OPTIONS
from .web_world import CoreKeeperWebWorld


class CoreKeeperWorld(World):
    """Archipelago integration for Core Keeper."""

    game = "Core Keeper"
    web = CoreKeeperWebWorld()
    options_dataclass = CoreKeeperOptions
    item_name_to_id = items.ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    def generate_early(self) -> None:
        required_items = sum(
            copies for _, option_name, copies in LICENSE_OPTIONS
            if getattr(self.options, option_name)
        )
        if required_items == 0:
            return
        boss_count = {3: 3, 2: 10, 1: 12, 0: 20}[int(self.options.goal)]
        location_count = (
            boss_count
            + ({3: 13, 2: 29, 1: 34, 0: 34}[int(self.options.goal)] if self.options.raw_materials else 0)
            + ({3: 6, 2: 12, 1: 14, 0: 14}[int(self.options.goal)] if self.options.refined_materials else 0)
            + ({3: 1, 2: 15, 1: 18, 0: 19}[int(self.options.goal)] if self.options.unique_materials else 0)
            + ({3: 3, 2: 7, 1: 9, 0: 9}[int(self.options.goal)] if self.options.key_items else 0)
            + ({3: 6, 2: 14, 1: 14, 0: 14}[int(self.options.goal)] if self.options.seeds else 0)
            + ({3: 10, 2: 18, 1: 20, 0: 20}[int(self.options.goal)] if self.options.food else 0)
            + ({3: 4, 2: 11, 1: 11, 0: 11}[int(self.options.goal)] if self.options.goldensanity else 0)
            + ({3: 3, 2: 10, 1: 10, 0: 10}[int(self.options.goal)] if self.options.cardsanity else 0)
            + ({3: 7, 2: 18, 1: 23, 0: 23}[int(self.options.goal)] if self.options.blocksanity else 0)
            + ({3: 12, 2: 39, 1: 44, 0: 44}[int(self.options.goal)] if self.options.fishsanity else 0)
            + ({3: 22, 2: 55, 1: 71, 0: 71}[int(self.options.goal)] if self.options.figurinesanity else 0)
            + ({3: 41, 2: 115, 1: 118, 0: 118}[int(self.options.goal)] if self.options.valuablesanity else 0)
            + ({3: 23, 2: 41, 1: 41, 0: 41}[int(self.options.goal)] if self.options.toolsanity else 0)
            + ({3: 32, 2: 69, 1: 75, 0: 75}[int(self.options.goal)] if self.options.weaponsanity else 0)
            + ({3: 25, 2: 59, 1: 60, 0: 60}[int(self.options.goal)] if self.options.accessanity else 0)
            + ({3: 45, 2: 101, 1: 104, 0: 104}[int(self.options.goal)] if self.options.jewelrysanity else 0)
            + ({3: 60, 2: 170, 1: 188, 0: 188}[int(self.options.goal)] if self.options.armorsanity else 0)
            + ({3: 16, 2: 26, 1: 28, 0: 28}[int(self.options.goal)] if self.options.petsanity else 0)
            + ({3: 2, 2: 4, 1: 4, 0: 5}[int(self.options.goal)] if self.options.merchantsanity else 0)
            + ({3: 18, 2: 38, 1: 50, 0: 50}[int(self.options.goal)] if self.options.enemies else 0)
            + ({3: 3, 2: 6, 1: 6, 0: 6}[int(self.options.goal)] if self.options.cattle_mutilation else 0)
            + ({3: 4, 2: 12, 1: 14, 0: 14}[int(self.options.goal)] if self.options.locked_chests else 0)
            + ({3: 36, 2: 72, 1: 108, 0: 120}[int(self.options.goal)] if self.options.skillsanity else 0)
        )
        if location_count < required_items:
            raise OptionError(
                "The selected license rewards require at least "
                f"{required_items} enabled Core Keeper checks, but this configuration has "
                f"{location_count}. Enable more check sections or disable some licenses."
            )

    def create_item(self, name: str) -> Item:
        return items.create_item(self, name)

    def get_filler_item_name(self) -> str:
        return "Empty Cache"

    def create_regions(self) -> None:
        regions.create_regions(self)

    def create_items(self) -> None:
        items.create_items(self)

    def allow_priority_overflow(self, item_names: list[str]) -> None:
        restricted_groups = set()
        if self.options.prevent_priority_in_optional_checks:
            restricted_groups.update(regions.OPTIONAL_GROUPS)
        if self.options.prevent_priority_in_sanity:
            restricted_groups.update(regions.SANITY_GROUPS)
        if not restricted_groups:
            return
        progression_count = sum(
            bool(items.ITEM_CLASSIFICATIONS[name] & ItemClassification.progression)
            for name in item_names
        )
        if progression_count == 0:
            return
        progression_item = self.create_item("Progressive Workbench License")
        locations = [
            location for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ]
        overflow = max(0, progression_count - sum(
            location.item_rule(progression_item) for location in locations
        ))
        restricted = [
            location for location in locations
            if (LOCATION_METADATA.get(location.name) or (None,))[0] in restricted_groups
            and not location.item_rule(progression_item)
        ]
        self.random.shuffle(restricted)
        for location in restricted[:overflow]:
            location.item_rule = lambda item: True

    def set_rules(self) -> None:
        rules.set_rules(self)

    def post_fill(self) -> None:
        if not self.options.early_repair_and_salvage or not self.options.repair_salvage_license:
            return
        sphere_one_milestones = {
            "defeat_glurch", "defeat_ghorm", "defeat_malugaz",
            "defeat_hive_mother", "defeat_king_slime",
        }
        guaranteed = ["Salvage and Repair Station License"]
        if self.options.furnace_license:
            guaranteed.append("Progressive Furnace License")
        for license_name in guaranteed:
            eligible_item_players = {self.player}
            eligible_location_players = {self.player}
            for group_id, group in self.multiworld.groups.items():
                if self.player in group["players"] and license_name in group["item_pool"]:
                    eligible_item_players.add(group_id)
                    eligible_location_players.update(group["players"])
            placements = [
                location for location in self.multiworld.get_locations()
                if location.item is not None
                and location.item.player in eligible_item_players
                and location.item.name == license_name
            ]
            if not placements:
                raise RuntimeError(f"Expected a placed {license_name}; found none")
            if not any(
                placement.player in eligible_location_players
                and (metadata := LOCATION_METADATA.get(placement.name)) is not None
                and set(metadata[2]).issubset(sphere_one_milestones)
                for placement in placements
            ):
                raise RuntimeError(
                    f"Early Repair and Salvage placed no {license_name} in a starting sphere"
                )

    def fill_slot_data(self) -> dict[str, object]:
        lower_wall = [
            LOCATION_NAME_TO_ID["Defeat Glurch the Abominous Mass"],
            LOCATION_NAME_TO_ID["Defeat Ghorm the Devourer"],
            LOCATION_NAME_TO_ID["Defeat Malugaz the Corrupted"],
        ]
        core_commander = lower_wall + [
            LOCATION_NAME_TO_ID["Defeat Azeos the Sky Titan"],
            LOCATION_NAME_TO_ID["Defeat Omoroth the Sea Titan"],
            LOCATION_NAME_TO_ID["Defeat Ra-Akar the Sand Titan"],
            LOCATION_NAME_TO_ID["Defeat Druidra the Wild Titan"],
            LOCATION_NAME_TO_ID["Defeat Crydra the Ice Titan"],
            LOCATION_NAME_TO_ID["Defeat Pyrdra the Fire Titan"],
            LOCATION_NAME_TO_ID["Defeat Core Commander"],
        ]
        sahabar = core_commander + [
            LOCATION_NAME_TO_ID["Defeat Nimruza, Queen of the Burrowed Sands"],
            LOCATION_NAME_TO_ID["Defeat S.A.H.A.B.A.R"],
        ]
        all_bosses = sahabar + [
            LOCATION_NAME_TO_ID["Defeat The Hive Mother"],
            LOCATION_NAME_TO_ID["Defeat King Slime"],
            LOCATION_NAME_TO_ID["Defeat Ivy the Poisonous Mass"],
            LOCATION_NAME_TO_ID["Defeat Morpha the Aquatic Mass"],
            LOCATION_NAME_TO_ID["Defeat Igneous the Molten Mass"],
            LOCATION_NAME_TO_ID["Defeat Atlantean Worm"],
            LOCATION_NAME_TO_ID["Defeat Urschleim"],
            LOCATION_NAME_TO_ID["Defeat Oblidra the Void Titan"],
        ]
        goal_ids = {3: lower_wall, 2: core_commander, 1: sahabar, 0: all_bosses}[int(self.options.goal)]
        progression_spheres = [
            lower_wall + [
                LOCATION_NAME_TO_ID["Defeat The Hive Mother"],
                LOCATION_NAME_TO_ID["Defeat King Slime"],
            ],
            core_commander[3:6] + [
                LOCATION_NAME_TO_ID["Defeat Ivy the Poisonous Mass"],
                LOCATION_NAME_TO_ID["Defeat Morpha the Aquatic Mass"],
                LOCATION_NAME_TO_ID["Defeat Igneous the Molten Mass"],
            ],
            core_commander[6:10] + [LOCATION_NAME_TO_ID["Defeat Atlantean Worm"]],
            [
                LOCATION_NAME_TO_ID["Defeat Urschleim"],
                LOCATION_NAME_TO_ID["Defeat Nimruza, Queen of the Burrowed Sands"],
                LOCATION_NAME_TO_ID["Defeat Oblidra the Void Titan"],
                LOCATION_NAME_TO_ID["Defeat S.A.H.A.B.A.R"],
            ],
        ]
        boss_access_spheres = [
            progression_spheres[0][:2] + progression_spheres[0][3:4],
            progression_spheres[0][2:3] + progression_spheres[0][4:5],
            progression_spheres[1][0:1] + progression_spheres[1][3:6],
            progression_spheres[1][1:2],
            progression_spheres[1][2:3],
            progression_spheres[2][0:1] + progression_spheres[2][4:5],
            progression_spheres[2][1:2],
            progression_spheres[2][2:3],
            progression_spheres[2][3:4],
            progression_spheres[3][0:2],
            progression_spheres[3][2:4],
        ]
        enemy_seed = int.from_bytes(hashlib.sha256(
            f"{self.multiworld.seed_name}:{self.player}:enemies".encode()
        ).digest()[:4], "little")
        boss_seed = int.from_bytes(hashlib.sha256(
            f"{self.multiworld.seed_name}:{self.player}:bosses".encode()
        ).digest()[:4], "little")
        return {
            "slot_data_version": 1,
            "core_keeper_steam_build_id": 23543556,
            "enabled_licenses": [
                item_name for item_name, option_name, _ in LICENSE_OPTIONS
                if getattr(self.options, option_name)
            ],
            "skill_xp_multiplier": 1 + int(self.options.skill_xp_multiplier) * 0.5,
            "skill_points": bool(self.options.skill_points),
            "soul_seeker_cache": bool(self.options.soul_seeker_cache),
            "titan_breath_cache": bool(self.options.titan_breath_cache),
            "phantom_spark_cache": bool(self.options.phantom_spark_cache),
            "rune_song_cache": bool(self.options.rune_song_cache),
            "credence_of_ruin_cache": bool(self.options.credence_of_ruin_cache),
            "stormbringer_cache": bool(self.options.stormbringer_cache),
            "reward_tools": bool(self.options.reward_tools),
            "reward_weapons": bool(self.options.reward_weapons),
            "reward_jewelry": bool(self.options.reward_jewelry),
            "reward_accessories": bool(self.options.reward_accessories),
            "reward_armor": bool(self.options.reward_armor),
            "early_repair_and_salvage": bool(self.options.early_repair_and_salvage),
            "prevent_priority_in_optional_checks": bool(
                self.options.prevent_priority_in_optional_checks
            ),
            "prevent_priority_in_sanity": bool(self.options.prevent_priority_in_sanity),
            "infinite_merchant_stock": bool(self.options.infinite_merchant_stock),
            "merchant_sells_crown_summon": bool(self.options.merchant_sells_crown_summon),
            "randomize_enemies": False,
            "randomizer_difficulty": 0,
            "enemy_randomizer_seed": enemy_seed,
            "enemy_randomizer_map": build_enemy_mapping(
                enemy_seed, 0
            ),
            "randomize_bosses": False,
            "boss_randomizer_seed": boss_seed,
            "boss_randomizer_map": build_boss_mapping(boss_seed),
            "bosses": bool(self.options.bosses) or int(self.options.goal) == 0,
            "goal": int(self.options.goal),
            "goal_location_id": goal_ids[-1],
            "goal_location_ids": goal_ids,
            "progression_spheres": progression_spheres,
            "boss_access_spheres": boss_access_spheres,
            "raw_materials": bool(self.options.raw_materials),
            "refined_materials": bool(self.options.refined_materials),
            "unique_materials": bool(self.options.unique_materials),
            "key_items": bool(self.options.key_items),
            "seeds": bool(self.options.seeds),
            "food": bool(self.options.food),
            "critters": bool(self.options.critters),
            "goldensanity": bool(self.options.goldensanity),
            "cardsanity": bool(self.options.cardsanity),
            "blocksanity": bool(self.options.blocksanity),
            "fishsanity": bool(self.options.fishsanity),
            "figurinesanity": bool(self.options.figurinesanity),
            "valuablesanity": bool(self.options.valuablesanity),
            "toolsanity": bool(self.options.toolsanity),
            "weaponsanity": bool(self.options.weaponsanity),
            "accessanity": bool(self.options.accessanity),
            "jewelrysanity": bool(self.options.jewelrysanity),
            "armorsanity": bool(self.options.armorsanity),
            "petsanity": bool(self.options.petsanity),
            "merchantsanity": bool(self.options.merchantsanity),
            "enemies": bool(self.options.enemies),
            "cattle_mutilation": bool(self.options.cattle_mutilation),
            "locked_chests": bool(self.options.locked_chests),
            "skillsanity": bool(self.options.skillsanity),
            "raw_material_cache_weight": int(self.options.raw_material_cache_weight),
            "refined_material_cache_weight": int(self.options.refined_material_cache_weight),
            "potions_cache_weight": int(self.options.potions_cache_weight),
            "pet_cache_weight": int(self.options.pet_cache_weight),
            "money_cache_weight": int(self.options.money_cache_weight),
            "automation_cache_weight": int(self.options.automation_cache_weight),
            "empty_cache_weight": int(self.options.empty_cache_weight),
            "death_link": int(self.options.death_link),
            "enabled_location_ids": sorted(
                location.address
                for location in self.multiworld.get_locations(self.player)
                if location.address is not None
            ),
        }
